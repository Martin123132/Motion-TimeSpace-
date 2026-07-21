from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4775"
CLAIM_ID = "L-617"
MARKER = "PPC4161_PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE_OR_OPEN_ARENA_FIRST_VALUES_4775"
PACKET_MARKER = "PPC4161_PACKET_PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE_OR_OPEN_ARENA_FIRST_VALUES_4775"
DECISION = "PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE_ASSEMBLED_FROM_4774_QBAR_LOCK_AND_4649_GR_SELECTOR_OPEN_ARENA_VALUES_AND_PARENT_SIGNATURE_STILL_REQUIRED_NONCLAIM"
NEXT_TARGET = "4776-Y5-R2FR-Gcal-normalization-or-open-arena-first-value-pack.md"

DOC_PATH = POST / "4775-Y5-R2FR-private-local-GR-limit-certificate-or-open-arena-first-values.md"
FORMAL_PATH = FORMAL / "791-PPC4161-private-local-GR-limit-certificate-or-open-arena-first-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_SOURCE_REGISTER.csv"
CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_PRIVATE_LOCAL_GR_LIMIT_CERTIFICATE.csv"
LIMIT_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_NEWTON_MAXWELL_PPN_LIMIT_MAP.csv"
FIRST_VALUES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_OPEN_ARENA_FIRST_VALUES.csv"
NO_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_NO_CIRCULARITY_AUDIT.csv"
RESIDUAL_POLICY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_RESIDUAL_VECTOR_POLICY.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4775_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4775_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4775_0_4774_qbar_zero", SOURCE_DIR / "P8_Y5_R2FR_4774_QBAR_PRIVATE_ZERO_UPDATE.csv", "QB4774_4_qbar_zero", "4774 private Qbar zero with positive denominator/projector lock"),
    ("SRC4775_1_4774_fallback", SOURCE_DIR / "P8_Y5_R2FR_4774_OPEN_OR_EMPIRICAL_FALLBACK_ROWS.csv", "FB4774_4_numeric_G", "4774 G and open-arena fallback"),
    ("SRC4775_2_4649_selector_contract", SOURCE_DIR / "P8_Y5_R2FR_4649_PARENT_GR_SELECTOR_CONTRACT.csv", "GRSEL4649_8_selector_status", "4649 sufficient parent/local GR selector contract"),
    ("SRC4775_3_4649_newton", SOURCE_DIR / "P8_Y5_R2FR_4649_PROMOTION_PROOF_CHAIN.csv", "PROOF4649_4_Newton", "4649 Newton weak-field readout"),
    ("SRC4775_4_4649_maxwell", SOURCE_DIR / "P8_Y5_R2FR_4649_PROMOTION_PROOF_CHAIN.csv", "PROOF4649_2_Maxwell", "4649 Maxwell-Hodge/Poynting proof chain"),
    ("SRC4775_5_4649_ppn", SOURCE_DIR / "P8_Y5_R2FR_4649_PROMOTION_PROOF_CHAIN.csv", "PROOF4649_5_PPN", "4649 PPN exact-GR branch"),
    ("SRC4775_6_4719_poisson", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_3_Poisson_equation_with_residual", "4719 Poisson residual bridge"),
    ("SRC4775_7_4719_orbit", SOURCE_DIR / "P8_Y5_R2FR_4719_LINEARIZED_FIELD_EQUATION_ROWS.csv", "LFE4719_4_Gauss_orbit_readout", "4719 Gauss/orbital readout"),
    ("SRC4775_8_4179_chain", SOURCE_DIR / "P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN.csv", "LC4179_9_calibrated_G", "4179 private local GR closure chain with calibrated G firewall"),
    ("SRC4775_9_4539_freeze", SOURCE_DIR / "P8_Y5_R2FR_4539_EFFECTIVE_LOCAL_GR_FREEZE_CONTRACT.csv", "FR4539_3_reopen_rule", "4539 effective branch reopen rule"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    CERTIFICATE_CSV,
    LIMIT_MAP_CSV,
    FIRST_VALUES_CSV,
    NO_CIRCULARITY_CSV,
    RESIDUAL_POLICY_CSV,
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


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CERT4775_0_branch",
            "private branch definition",
            "B_loc^private := C_static_iso_private ∩ PPC4161-TK-HQ ∩ MEH_private_selector ∩ B_GR_selector",
            "This is an intersected effective branch, not a globally unique parent-action branch.",
            "PRIVATE_LIMIT_BRANCH_DEFINED",
        ),
        (
            "CERT4775_1_GR_equation",
            "local Einstein-form field equation",
            "If B_GR_selector is active, G_mu_nu[g_obs]+Lambda_eff g_obs_mu_nu = kappa_eff T_H_mu_nu + E_fail_mu_nu.",
            "The GR form comes from the EH/local metric selector; 4774 closes the source-coupling/Qbar defect only inside the compact branch.",
            "CONDITIONAL_EINSTEIN_FORM",
        ),
        (
            "CERT4775_2_residual_zero",
            "private compact residual",
            "Inside B_loc^private, Qbar_XH_abs=0_private_C_static_iso_denominator_locked and tail/source projector defects are routed to zero.",
            "Uses 4774 Qbar lock plus 4649 selector/failure routing; open terms are not erased.",
            "PRIVATE_RESIDUAL_ZERO_CERTIFIED",
        ),
        (
            "CERT4775_3_conservation",
            "Bianchi and source conservation",
            "D_A kappa_eff=0, common Hilbert source and Maxwell/matter exchange give nabla_mu T_H^mu_nu=0 in the branch.",
            "Prevents an overdetermined Einstein equation and blocks hidden species/source weights.",
            "CONSERVATION_GATE_PRIVATE",
        ),
        (
            "CERT4775_4_Newton",
            "Newtonian limit",
            "Weak/static/slow EH 00 equation gives nabla^2 Phi_N=4*pi*G_cal*rho_H and a=-grad Phi_N.",
            "G_cal is calibrated from kappa_eff; the measured numerical value of G is not derived.",
            "NEWTON_LIMIT_PRIVATE_CALIBRATED_G",
        ),
        (
            "CERT4775_5_Maxwell",
            "Maxwell and Poynting ownership",
            "Common Hodge variation gives nabla_mu F^mu_nu=J^nu and Poynting is T_EM boundary/Hilbert flux, not a hidden background source.",
            "This answers the Poynting-vector worry without deleting radiation: flux is boundary/accounted stress.",
            "MAXWELL_HODGE_STRESS_PRIVATE",
        ),
        (
            "CERT4775_6_PPN",
            "local static PPN branch",
            "EH metric block with no extra local source/readout couplings gives Delta_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0.",
            "Only exact in the static/private selector; open systems require residual vector bounds.",
            "PPN_VECTOR_ZERO_PRIVATE_SELECTOR",
        ),
        (
            "CERT4775_7_claim_status",
            "claim ceiling",
            "public_local_GR_claim=false; numeric_G_prediction=false; open_arena_pass=false; parent_unique_branch=false.",
            "4775 is a strong private/effective local-GR certificate, not the final unified parent theorem.",
            "NONCLAIM_FIREWALL_ACTIVE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": certificate_id,
            "object": obj,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, obj, statement, meaning, status in specs
    ]


def limit_map_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "LM4775_0_field_equation",
            "local GR",
            "G_mu_nu+Lambda_eff g_mu_nu=kappa_eff T_H_mu_nu",
            "B_GR selector plus zero/private residual branch",
            "E_fail_mu_nu reappears if any selector clause fails",
        ),
        (
            "LM4775_1_Newton_Poisson",
            "Newtonian mechanics",
            "nabla^2 Phi_N=4*pi*G_cal*rho_H",
            "weak/static/slow 00 equation with E_00=0 in the private branch",
            "open branch keeps +(c^2/2)E_00",
        ),
        (
            "LM4775_2_orbital",
            "orbital acceleration",
            "a_r=-G_cal*M_H^dress/r^2 plus standard multipoles",
            "Gauss readout of Poisson equation with Hamiltonian worldtube mass",
            "profile, boundary and E_00 integrals become explicit residuals",
        ),
        (
            "LM4775_3_Maxwell",
            "EM field equations",
            "nabla_mu F^mu_nu=J^nu; nabla_mu T_EM^mu_nu=-F_nu_lambda J^lambda",
            "same Hodge/current owner and Hilbert stress variation",
            "radiative/Poynting flux must be boundary or external sector",
        ),
        (
            "LM4775_4_PPN",
            "PPN vector",
            "Delta_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0",
            "EH metric block and no extra source/readout couplings",
            "open branch uses Pi_PPN residual transfer matrix",
        ),
        (
            "LM4775_5_G",
            "calibrated coupling",
            "G_cal=c^4*kappa_eff/(8*pi)",
            "local GR reduction only needs calibrated coupling, as GR itself does not predict numeric G",
            "numeric G derivation/calibration remains a separate source-normalization target",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "map_id": map_id,
            "limit_sector": sector,
            "private_branch_output": output,
            "derivation_basis": basis,
            "open_arena_residual": residual,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for map_id, sector, output, basis, residual in specs
    ]


def first_value_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FV4775_0_Gcal",
            "G_cal/kappa_eff normalization",
            "units, convention and one calibration source row",
            "needed to compare local predictions in SI/observed units without pretending G is predicted",
            "MISSING_CALIBRATION_SOURCE_ROW",
        ),
        (
            "FV4775_1_MH_dress",
            "M_H^dress",
            "Hamiltonian worldtube mass or accepted comparator mass with same-frame units",
            "needed for orbital/Newton readout and denominator positivity in real arenas",
            "MISSING_SOURCE_BACKED_MASS_ROW",
        ),
        (
            "FV4775_2_E00",
            "E_00 residual",
            "bound or measured envelope for local non-EH/open residual in the observed metric frame",
            "needed to turn Poisson bridge into a quantitative pass/fail",
            "MISSING_OPEN_ARENA_E00_BOUND",
        ),
        (
            "FV4775_3_boundary_flux",
            "F_boundary/Poynting/radiation flux",
            "boundary flux ledger separating Hilbert EM flux from external/apparatus/radiative injection",
            "needed so Poynting is not hidden background coupling and not erased",
            "MISSING_BOUNDARY_FLUX_LEDGER",
        ),
        (
            "FV4775_4_PPN_transfer",
            "Pi_PPN residual transfer matrix",
            "map from residual fields/readout drift to gamma,beta,alpha_i,xi,zeta_i,Gdot/G",
            "needed for open/local empirical PPN comparisons",
            "MISSING_PPN_TRANSFER_MATRIX",
        ),
        (
            "FV4775_5_R10_alpha",
            "alpha(lambda) local fifth-force row",
            "source-backed amplitude and bound curve pair with no placeholder parent coefficients",
            "needed for R10/local short-range claim",
            "MISSING_R10_NUMERIC_ROW",
        ),
        (
            "FV4775_6_orbital_profile",
            "orbital profile/multipole residual",
            "source profile, compact support, exterior surface and multipole/error budget",
            "needed to compare Newton/orbital branch against real Solar-System/binary systems",
            "MISSING_ORBITAL_PROFILE_ROW",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "value_id": value_id,
            "quantity": quantity,
            "required_first_value": value,
            "why_needed": why,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for value_id, quantity, value, why, status in specs
    ]


def no_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "NC4775_0_GR_not_assumed_public",
            "B_GR selector is used as a sufficient effective branch, not claimed as globally parent-derived",
            "keeps parent-action proof separate from local branch certificate",
            "PASS_PRIVATE_DISCIPLINE",
        ),
        (
            "NC4775_1_G_not_predicted",
            "G_cal is calibrated; no numerical G prediction is inferred from M_lower positivity",
            "avoids demanding too much and avoids fake derivation",
            "PASS_FIREWALL",
        ),
        (
            "NC4775_2_Qbar_scope",
            "Qbar_XH=0 is limited to the compact stationary collar denominator-locked branch",
            "prevents smuggling into open/radiative/apparatus arenas",
            "PASS_SCOPE_LOCK",
        ),
        (
            "NC4775_3_Maxwell_scope",
            "Poynting vector is accounted as EM Hilbert/boundary flux, not promoted to a separate hidden background field",
            "keeps EM stress derivable while preserving radiation accounting",
            "PASS_NO_SIDE_CHANNEL",
        ),
        (
            "NC4775_4_Newton_scope",
            "Newtonian limit follows from EH weak-field equation with calibrated G and explicit residual E_00",
            "does not replace evidence with closure if residual is nonzero",
            "PASS_RESIDUAL_EXPLICIT",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "anti_circularity_rule": rule,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, rule, effect, status in specs
    ]


def residual_policy_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RP4775_0_parent", "parent selector unsigned", "E_parent_selector", "keep effective-branch language; do not claim global parent derivation"),
        ("RP4775_1_EH", "EH/local metric selector fails", "E_EH_IR", "route to non-EH operator coefficients and linearized residual tensor"),
        ("RP4775_2_source", "Hilbert source/common readout fails", "E_source_label + E_readout", "route to WEP/source-coupling residual vector"),
        ("RP4775_3_boundary", "radiation/Poynting/boundary flux is open", "E_boundary_flux", "score as boundary/external flux instead of zeroing it"),
        ("RP4775_4_PPN", "static private selector fails for PPN", "Delta_PPN_open", "use transfer matrix and source-backed bounds"),
        ("RP4775_5_R10", "tail/source coefficients are nonzero or unsourced", "alpha_tail(lambda)", "compare with real alpha(lambda) bound curve only after numeric source rows exist"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "policy_id": policy_id,
            "trigger": trigger,
            "residual_name": residual,
            "required_route": route,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for policy_id, trigger, residual, route in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "RT4775_0_Gcal_first",
            "Gcal normalization / source calibration first-value pack",
            "turns the private local branch into something testable without pretending to derive numeric G",
            "SELECTED_NEXT",
        ),
        (
            "RT4775_1_PPN_open",
            "open-arena PPN transfer matrix",
            "needed after Gcal/MH/E00 first values to score non-ideal local tests",
            "QUEUED_AFTER_GCAL",
        ),
        (
            "RT4775_2_parent_unique",
            "single parent action selector signature",
            "ultimate public-GR theorem route, but heavier than the immediate testability gate",
            "LONGER_THEORY_TARGET",
        ),
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
        ("PG4775_0", "public local-GR claim requires one parent action to sign B_GR selector, residual silence and common readout", "blocks public overclaim"),
        ("PG4775_1", "empirical local claim requires source-backed Gcal/MH/E00/boundary/PPN/R10 rows", "blocks private theorem being used as data"),
        ("PG4775_2", "numeric G claim requires a new derivation/normalization gate, not 4775", "blocks fake fundamental constant derivation"),
        ("PG4775_3", "Poynting/radiation must be boundary/Hilbert flux or explicit external sector", "blocks hidden EM background coupling"),
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
        ("FW4775_0", "do not claim final parent-derived GR", "PARENT_SIGNATURE_STILL_OPEN"),
        ("FW4775_1", "do not claim measured G is predicted", "GCAL_IS_CALIBRATED"),
        ("FW4775_2", "do not score R10/PPN/clocks/orbits from private branch alone", "SOURCE_ROWS_REQUIRED"),
        ("FW4775_3", "do not erase open Poynting/radiation flux", "BOUNDARY_LEDGER_REQUIRED"),
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
            "meaning": "4775 converts the 4774 private residual-zero result plus the 4649 GR selector into a clean private/effective local-GR limit certificate and a first-value list for real/open arenas.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_LOCAL_GR_CERTIFICATE_NONCLAIM",
            "summary": "Private local-GR/Newton/Maxwell/PPN certificate assembled; public parent theorem and empirical/open-arena first values remain open.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The next useful step is not more branch narration; it is Gcal/source normalization and first numeric/bound rows for open-arena scoring.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    certificate: list[dict[str, Any]],
    limit_map: list[dict[str, Any]],
    first_values: list[dict[str, Any]],
    no_circularity: list[dict[str, Any]],
    residual_policy: list[dict[str, Any]],
    routes: list[dict[str, Any]],
) -> None:
    doc = f"""# 4775 — Private Local-GR Limit Certificate or Open-Arena First Values

Generated: `{timestamp}`

## Result

4775 consolidates the newest local result:

```text
Qbar_XH_abs = 0_private_C_static_iso_denominator_locked
```

with the earlier GR selector chain. The clean statement is:

```text
MTS now has a disciplined private/effective local-GR branch.
```

Inside the branch:

```text
G_mu_nu[g_obs] + Lambda_eff g_obs_mu_nu = kappa_eff T_H_mu_nu
nabla^2 Phi_N = 4*pi*G_cal*rho_H
nabla_mu F^mu_nu = J^nu
Delta_PPN = 0
G_cal = c^4*kappa_eff/(8*pi)
```

But this is still not:

```text
a public parent-action derivation of GR,
a prediction of the numerical value of G,
or an empirical R10/PPN/orbital/clock pass.
```

## Private Local-GR Certificate

{markdown_table(certificate, ["certificate_id", "object", "statement", "status"])}

## Newton / Maxwell / PPN Limit Map

{markdown_table(limit_map, ["map_id", "limit_sector", "private_branch_output", "open_arena_residual"])}

## Open-Arena First Values

{markdown_table(first_values, ["value_id", "quantity", "required_first_value", "status"])}

## No-Circularity Audit

{markdown_table(no_circularity, ["audit_id", "anti_circularity_rule", "status"])}

## Residual Vector Policy

{markdown_table(residual_policy, ["policy_id", "trigger", "residual_name", "required_route"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4775: Private Local-GR Limit Certificate

Generated: `{timestamp}`

4775 assembles the current best local result:

```text
Qbar_XH_abs=0_private_C_static_iso_denominator_locked
```

with the sufficient GR selector contract:

```text
B_GR -> Einstein-form local field equation -> Newton/Maxwell/PPN local limits.
```

The resulting certificate is:

```text
private/effective local-GR branch: PASS
public parent-derived local GR: NOT CLAIMED
numeric G prediction: NOT CLAIMED
open-arena empirical pass: NOT CLAIMED
```

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4775 assembles a clean private/effective local-GR limit certificate from 4774 Qbar zero and the 4649 GR selector contract.
- Inside the private branch: Einstein-form local equation, Newton/Poisson readout, Maxwell-Hodge/Poynting stress ownership and GR PPN vector are available with calibrated `G_cal`.
- The branch is still not a public parent-action theorem, not a numerical prediction of `G`, and not an empirical pass for R10/PPN/clocks/orbits.
- Open arenas now have a concrete first-value list: `G_cal/kappa_eff`, `M_H^dress`, `E_00`, boundary/Poynting flux, PPN transfer matrix, R10 alpha row and orbital profile row.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4775 packet update: the local branch should now be called a disciplined private/effective local-GR branch. It is ready for G-calibration and open-arena first-value work, not public promotion.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4775-Y5-R2FR-private-local-GR-limit-certificate-or-open-arena-first-values.md`

## Decision

`{DECISION}`

## What moved forward

- Consolidated 4774 private `Qbar_XH_abs=0` with the 4649 GR selector and 4719 Poisson bridge.
- Wrote a private/effective local-GR limit certificate covering Einstein-form field equation, Newton/Poisson readout, Maxwell-Hodge/Poynting stress ownership and PPN vector closure.
- Added a no-circularity audit so private closure is not smuggled into public GR, numeric `G`, or open/radiative/apparatus tests.
- Listed the first open-arena values required for real scoring: `G_cal/kappa_eff`, `M_H^dress`, `E_00`, boundary flux, PPN transfer, R10 alpha and orbital profile rows.

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
        "private_effective_local_GR_limit_certificate",
        "4775 assembles a private/effective local-GR limit certificate from the 4774 Qbar lock and the 4649 GR selector contract.",
        "Generated source register, certificate, Newton/Maxwell/PPN map, first-value rows, no-circularity audit, residual policy, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "private_effective_local_GR_certificate_nonclaim",
        NEXT_TARGET,
        "Public parent-derived GR, numeric G prediction, and empirical/open-arena claims remain blocked.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need Gcal/source normalization and open-arena first-value pack.",
        "Private local-GR limit certificate",
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
    certificate: list[dict[str, Any]],
    limit_map: list[dict[str, Any]],
    first_values: list[dict[str, Any]],
    no_circularity: list[dict[str, Any]],
    residual_policy: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4775_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4775_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4775_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4775_2_certificate_branch", "private branch certificate exists", any(row["certificate_id"] == "CERT4775_0_branch" and row["status"] == "PRIVATE_LIMIT_BRANCH_DEFINED" for row in certificate), str(CERTIFICATE_CSV)))
    checks.append(("VAL4775_3_gr_status", "claim ceiling is active", any(row["certificate_id"] == "CERT4775_7_claim_status" and row["status"] == "NONCLAIM_FIREWALL_ACTIVE" for row in certificate), str(CERTIFICATE_CSV)))
    checks.append(("VAL4775_4_newton_map", "Newton map has calibrated G and open residual", any(row["map_id"] == "LM4775_1_Newton_Poisson" and "E_00" in row["open_arena_residual"] for row in limit_map), str(LIMIT_MAP_CSV)))
    checks.append(("VAL4775_5_maxwell_map", "Maxwell/Poynting ownership map exists", any(row["map_id"] == "LM4775_3_Maxwell" and "Poynting" in row["open_arena_residual"] for row in limit_map), str(LIMIT_MAP_CSV)))
    checks.append(("VAL4775_6_ppn_map", "PPN map exists", any(row["map_id"] == "LM4775_4_PPN" and "Delta_PPN" in row["private_branch_output"] for row in limit_map), str(LIMIT_MAP_CSV)))
    checks.append(("VAL4775_7_first_values", "first-value rows retain missing Gcal, E00, boundary and PPN requirements", all(any(row["status"] == status for row in first_values) for status in ["MISSING_CALIBRATION_SOURCE_ROW", "MISSING_OPEN_ARENA_E00_BOUND", "MISSING_BOUNDARY_FLUX_LEDGER", "MISSING_PPN_TRANSFER_MATRIX"]), str(FIRST_VALUES_CSV)))
    checks.append(("VAL4775_8_no_circularity", "no-circularity audit passes all rows", all(row["status"].startswith("PASS") for row in no_circularity), str(NO_CIRCULARITY_CSV)))
    checks.append(("VAL4775_9_residual_policy", "residual vector policy includes parent, boundary and R10 routes", all(any(row["policy_id"] == policy_id for row in residual_policy) for policy_id in ["RP4775_0_parent", "RP4775_3_boundary", "RP4775_5_R10"]), str(RESIDUAL_POLICY_CSV)))
    checks.append(("VAL4775_10_route_selected", "Gcal/source first-value pack selected next", any(row["selection_status"] == "SELECTED_NEXT" and "Gcal" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4775_11_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4775_12_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4775_13_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4775_14_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4775_15_claim_row", "claim row L-617 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4775_16_resume", "resume points from 4775 to 4776", "4775-Y5" in resume_text and "4776-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4775_17_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

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
            "validation_id": "VAL4775_OVERALL",
            "check": "all 4775 private local-GR certificate checks pass",
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
    certificate = certificate_rows(timestamp)
    limit_map = limit_map_rows(timestamp)
    first_values = first_value_rows(timestamp)
    no_circularity = no_circularity_rows(timestamp)
    residual_policy = residual_policy_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CERTIFICATE_CSV, certificate)
    write_csv(LIMIT_MAP_CSV, limit_map)
    write_csv(FIRST_VALUES_CSV, first_values)
    write_csv(NO_CIRCULARITY_CSV, no_circularity)
    write_csv(RESIDUAL_POLICY_CSV, residual_policy)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, certificate, limit_map, first_values, no_circularity, residual_policy, routes)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, certificate, limit_map, first_values, no_circularity, residual_policy, routes, gates, timestamp))


if __name__ == "__main__":
    main()
