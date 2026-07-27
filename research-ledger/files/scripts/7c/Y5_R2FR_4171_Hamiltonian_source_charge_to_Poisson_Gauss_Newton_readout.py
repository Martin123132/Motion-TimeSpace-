from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4171"
BRANCH_ID = "MTS_R2FR_Y5_HAMILTONIAN_SOURCE_CHARGE_TO_POISSON_GAUSS_NEWTON_4171"
DECISION = "PPC4161_TK_HQN_DERIVES_FIRST_ORDER_POISSON_GAUSS_NEWTON_READOUT_PRIVATE_PACKET_FULL_PPN_REMAINS"
DOC_PATH = POST / "4171-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Gauss-Newton-readout.md"
FORMAL_187_PATH = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-012"
SPINE_MARKER = "PPC4161_POISSON_GAUSS_NEWTON_4171"
PACKET_MARKER = "PPC4161_PACKET_POISSON_GAUSS_NEWTON_READOUT_4171"
NEXT_TARGET = "4172-Y5-R2FR-PPC4161-full-PPN-readout-gamma-beta-alpha-xi-zeta.md"

SOURCES = {
    "SRC4171_00_4170_doc": (
        POST / "4170-Y5-R2FR-Hilbert-source-charge-to-worldtube-mass-readout-glue.md",
        "No orbital `GM`, fitted acceleration, or measured `G_N` is used",
        "4170 checkpoint doc with anti-circularity guard.",
    ),
    "SRC4171_01_4170_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4170_NEXT_TARGET.csv",
        "derive nabla^2 Phi_N=4*pi G_N rho_H",
        "4170 next-target route A.",
    ),
    "SRC4171_02_4170_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4170_STATUS.csv",
        "Poisson_Gauss_Newton_readout_closed",
        "4170 status showing Newton readout was open.",
    ),
    "SRC4171_03_4170_remaining": (
        SOURCE_DIR / "P8_Y5_R2FR_4170_REMAINING_NEWTON_PPN_GATES.csv",
        "a_r=-G_N M_H^dress/r^2",
        "4170 remaining Newton and PPN gates.",
    ),
    "SRC4171_04_formal_181": (
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H",
        "Earlier formal weak-field readout target.",
    ),
    "SRC4171_05_formal_186": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "M_H^dress[W_H;tau]",
        "4170 Hamiltonian/worldtube source charge bridge.",
    ),
    "SRC4171_06_formal_180": (
        PACKET_180_PATH,
        "No observed orbital `GM` is imported",
        "Current packet anti-circularity guard.",
    ),
    "SRC4171_07_worldtube_theorem": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "g_00=-1+2G_ref M_source/r",
        "GR-style Newton/PPN readout warning after worldtube glue.",
    ),
    "SRC4171_08_HSM541": (
        SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "nabla^2 Phi=4*pi*G_ref*rho_H",
        "Hamiltonian source-measure Poisson/Gauss readout contract.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, required_text, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": required_text,
                "required_text_found": str(required_text in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161-TK-HQN privately derives the first-order Poisson/Gauss/Newton readout from the Hamiltonian source charge without importing orbital GM",
        "current_evidence": "formalization-workbench/187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md records weak-field EH 00 equation G00_lin=2 nabla2 Phi_N/c^2, T00=rho_H c^2, kappa_eff=8*pi G_N/c^4, hence nabla2 Phi_N=4*pi G_N rho_H, Gauss integral gives M_H^dress, and slow geodesic gives a=-grad Phi_N; public_claim=false",
        "status": "private_packet_newton_readout_nonclaim_public_claim_false",
        "next_test": "Run the full PPC4161 PPN readout for gamma, beta, alpha_i, zeta_i and xi, then empirical local tests",
        "key_risk": "This is first-order Newtonian readout inside a private branch; it does not prove full PPN, global MTS adoption, empirical pass, or numerical G_N prediction",
    }
    normalized_new = {field: new_row.get(field, "") for field in fieldnames}
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    if existing:
        changed = False
        for row in rows:
            if row.get("claim_id") == CLAIM_ID:
                for field, value in normalized_new.items():
                    if row.get(field) != value:
                        row[field] = value
                        changed = True
        action = "updated" if changed else "already_present"
    else:
        rows.append(normalized_new)
        action = "added"

    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return action


def ensure_packet_180_addendum() -> str:
    text = read_text(PACKET_180_PATH)
    if PACKET_MARKER in text:
        return "already_present"
    section = f"""

## PPC4161-TK-HQN Addendum - Poisson/Gauss/Newton Readout

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4171-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Gauss-Newton-readout.md`

Inside the private PPC4161-TK-HQ local packet, take the EH weak-field slow-motion readout:

```text
g_00 = -c^2 - 2 Phi_N + higher order
T_00 = rho_H c^2 + higher order
kappa_eff = 8*pi G_N/c^4
G_00^lin = 2 nabla^2 Phi_N/c^2
```

The 00 equation gives:

```text
nabla^2 Phi_N = 4*pi G_N rho_H.
```

The source density is the Hamiltonian source density whose compact integral is fixed by 4170:

```text
int_W rho_H dV = M_H^dress[W_H;tau].
```

Gauss' theorem gives:

```text
int_S grad Phi_N dot dS = 4*pi G_N M_H^dress.
```

For the exterior monopole/spherical or far-field leading term:

```text
Phi_N = -G_N M_H^dress/r
a = -grad Phi_N
a_r = -G_N M_H^dress/r^2.
```

No orbital `GM` is imported. Orbital motion is now a downstream test of the derived readout. Full PPN remains the next gate.
"""
    PACKET_180_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def write_formal_187() -> None:
    FORMAL_187_PATH.write_text(
        f"""# 187 - PPC4161 Poisson/Gauss/Newton Readout From Hamiltonian Source Charge

Marker: `PPC4161_POISSON_GAUSS_NEWTON_READOUT_FROM_HAMILTONIAN_SOURCE`  
Timestamp UTC: `{now()}`  
Status: `private_packet_newton_readout_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Branch Definition
Define:

```text
PPC4161-TK-HQN := PPC4161-TK-HQ + weak-field EH Newton readout.
```

The local branch already has:

```text
G_munu = kappa_eff T_H_munu
G_N = c^4 kappa_eff/(8*pi)
Q_M = M_H^dress[W_H;tau].
```

## Weak-Field 00 Equation
Use the slow-motion weak-field metric convention:

```text
g_00 = -c^2 - 2 Phi_N + higher order
T_00 = rho_H c^2 + higher order
G_00^lin = 2 nabla^2 Phi_N/c^2.
```

The 00 component gives:

```text
2 nabla^2 Phi_N/c^2 = kappa_eff rho_H c^2.
```

Using:

```text
kappa_eff = 8*pi G_N/c^4
```

gives:

```text
nabla^2 Phi_N = 4*pi G_N rho_H.
```

## Gauss Charge
The source mass density is not an orbital fit. It is the density whose compact Hamiltonian charge is:

```text
int_W rho_H dV = M_H^dress[W_H;tau].
```

Gauss' theorem then gives:

```text
int_S grad Phi_N dot dS = 4*pi G_N M_H^dress.
```

For an exterior monopole/spherical source, or the leading far-field monopole outside a compact source:

```text
Phi_N = -G_N M_H^dress/r + constant
```

and the slow geodesic limit gives:

```text
a = -grad Phi_N,
a_r = -G_N M_H^dress/r^2.
```

## Anti-Circularity
No observed orbital `GM`, fitted acceleration, or measured numerical value of `G_N` is used to define the source charge. Orbital data is now a test of the derived branch, not an input to it.

## What Remains
This closes the first-order Newtonian Poisson/Gauss readout inside the private branch. It does not close:

- full PPN: gamma, beta, alpha_i, zeta_i, xi;
- empirical Solar-system/orbital residual tests;
- numerical prediction of `G_N`;
- global MTS parent adoption.

Next target:

```text
{NEXT_TARGET}
```
""",
        encoding="utf-8",
    )


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## 17. Local GR Coupling Update - Poisson/Gauss/Newton Readout

Marker: `{SPINE_MARKER}`  
Source bridge: `187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4171` derives the first-order Newtonian readout inside the private branch:

```text
G_00^lin = 2 nabla^2 Phi_N/c^2
T_00 = rho_H c^2
kappa_eff = 8*pi G_N/c^4
```

so:

```text
nabla^2 Phi_N = 4*pi G_N rho_H.
```

Using the Hamiltonian source charge from `4170`:

```text
int_W rho_H dV = M_H^dress[W_H;tau],
int_S grad Phi_N dot dS = 4*pi G_N M_H^dress.
```

The exterior monopole/far-field readout gives:

```text
Phi_N = -G_N M_H^dress/r,
a_r = -G_N M_H^dress/r^2.
```

This is a real Newtonian bridge inside PPC4161-TK-HQN and it does not import orbital `GM`. It is still not a public local-GR claim because full PPN, empirical local tests, numerical `G_N`, and global MTS adoption remain open.

The next local-GR source step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def weak_field_rows(packet_action: str) -> List[Dict[str, str]]:
    rows = [
        ("WF4171_0_branch", "private branch", "PPC4161-TK-HQN := PPC4161-TK-HQ + weak-field EH Newton readout", "private_packet_adopted"),
        ("WF4171_1_metric", "metric convention", "g_00=-c^2-2 Phi_N + higher order", "weak_field_slow_motion"),
        ("WF4171_2_source", "source approximation", "T_00=rho_H c^2 + higher order", "slow_motion_source"),
        ("WF4171_3_EH_linear", "linearized 00 equation", "G_00^lin=2 nabla^2 Phi_N/c^2", "EH_weak_field_identity"),
        ("WF4171_4_coupling", "coupling normalization", "kappa_eff=8*pi G_N/c^4", "from_181_4165_4169_chain"),
        ("WF4171_5_packet_sync", "packet integration addendum", str(PACKET_180_PATH), f"formal_sync_done_{packet_action}"),
    ]
    return [
        {
            **common(),
            "weak_field_id": row[0],
            "name": row[1],
            "formula_or_path": row[2],
            "status": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def poisson_rows() -> List[Dict[str, str]]:
    rows = [
        ("PG4171_0_start", "00 equation", "G_00^lin=kappa_eff T_00", "2 nabla^2 Phi_N/c^2 = kappa_eff rho_H c^2", "EH weak-field equation with Hamiltonian source density"),
        ("PG4171_1_substitute", "substitute coupling", "kappa_eff=8*pi G_N/c^4", "2 nabla^2 Phi_N/c^2 = 8*pi G_N rho_H/c^2", "uses calibrated local G_N relation, not numerical prediction"),
        ("PG4171_2_poisson", "Poisson equation", "nabla^2 Phi_N = 4*pi G_N rho_H", "Poisson readout closed inside private branch", "derived_private_packet"),
        ("PG4171_3_source_charge", "source mass integral", "int_W rho_H dV = M_H^dress[W_H;tau]", "source is 4170 Hamiltonian charge, not orbital GM", "same_charge_source"),
        ("PG4171_4_gauss", "Gauss integral", "int_S grad Phi_N dot dS = 4*pi G_N M_H^dress", "surface flux equals same Hamiltonian source charge", "derived_private_packet"),
    ]
    return [
        {
            **common(),
            "poisson_id": row[0],
            "step": row[1],
            "input_formula": row[2],
            "output_formula": row[3],
            "meaning": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def orbital_rows() -> List[Dict[str, str]]:
    rows = [
        ("OR4171_0_monopole", "exterior monopole/far-field potential", "Phi_N=-G_N M_H^dress/r + constant", "requires compact source exterior monopole or leading far-field term"),
        ("OR4171_1_geodesic", "slow geodesic equation", "a=-grad Phi_N", "test-particle slow-motion limit of the same metric"),
        ("OR4171_2_radial", "inverse-square acceleration", "a_r=-G_N M_H^dress/r^2", "Newtonian acceleration derived from Hamiltonian source charge"),
        ("OR4171_3_anti_circular", "no orbital import", "GM_orbit not used to define M_H^dress or G_N", "orbital measurements become tests only after derivation"),
        ("OR4171_4_multipoles", "non-spherical compact source guard", "Phi_N=-G_N M_H^dress/r + multipoles", "monopole result is leading far-field unless spherical symmetry is assumed"),
    ]
    return [
        {
            **common(),
            "orbital_id": row[0],
            "name": row[1],
            "formula": row[2],
            "guard_or_meaning": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def residual_rows() -> List[Dict[str, str]]:
    rows = [
        ("NR4171_0_Poisson_residual", "Delta_Poisson = nabla^2 Phi_N - 4*pi G_N rho_H", "zero_inside_private_packet", "closed by EH weak-field 00 equation"),
        ("NR4171_1_Gauss_residual", "Delta_Gauss = int_S grad Phi_N dot dS - 4*pi G_N M_H^dress", "zero_inside_private_packet", "closed by Gauss theorem and 4170 charge"),
        ("NR4171_2_orbital_import", "Delta_orbital_import", "zero_by_guard", "GM_orbit is not used as input"),
        ("NR4171_3_radial_hair", "epsilon_radial_hair", "zero_for_monopole_or_retained_multipoles", "multipoles remain if non-spherical/non-far-field"),
        ("NR4171_4_if_rejected", "epsilon_Newton_readout", "fallback_only", "if weak-field EH readout is rejected, retain radial hair/fifth-force/source residual rows"),
    ]
    return [
        {
            **common(),
            "residual_id": row[0],
            "quantity": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def remaining_gate_rows() -> List[Dict[str, str]]:
    rows = [
        ("RG4171_0_full_PPN_gamma_beta", "full PPN gamma/beta", "gamma-1 and beta-1", "not_closed", "first-order Newton does not prove second-order metric readout"),
        ("RG4171_1_preferred_frame", "PPN preferred-frame/conservation", "alpha_i, zeta_i, xi", "not_closed", "requires full PPC4161 PPN readout and side-channel silence"),
        ("RG4171_2_empirical_orbital", "empirical orbital tests", "fit residuals after derived GM_source", "not_run", "orbital data is now a test, not an input"),
        ("RG4171_3_R10_clock_WEP", "R10, clocks, WEP", "local bound pass rows", "not_closed", "first-order Newton does not close all local arenas"),
        ("RG4171_4_numeric_G", "Newton constant magnitude", "G_N=c^4 kappa_* Z_0/(8*pi)", "not_predicted", "calibrated local constant, not fundamental numerical prediction"),
        ("RG4171_5_global", "global MTS adoption", "PPC4161-TK-HQN subset != full MTS", "not_closed", "private local branch only"),
    ]
    return [
        {
            **common(),
            "gate_id": row[0],
            "gate": row[1],
            "formula": row[2],
            "status": row[3],
            "why_remaining": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "BD4171_0_Newton",
            "route": "Hamiltonian_source_to_Poisson_Gauss_Newton",
            "result": "PPC4161-TK-HQN derives nabla^2 Phi_N=4*pi G_N rho_H and a_r=-G_N M_H^dress/r^2 inside the private branch.",
            "gate_state": "first_order_Newton_private_pass_public_claim_false",
            "next_action": "Run full PPN readout rather than re-opening the source charge or importing orbital GM.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4171_1_anti_circular",
            "route": "orbital_data_as_test",
            "result": "Orbital GM is not used as an input; it is downstream evidence after the Poisson/Gauss bridge.",
            "gate_state": "anti_circularity_guard_pass",
            "next_action": "Use orbital data only in empirical validation once PPN gates are staged.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4171_2_next",
            "route": "next_target",
            "result": NEXT_TARGET,
            "gate_state": "Newton_first_order_closed_full_PPN_open",
            "next_action": "Derive or bound gamma, beta, alpha_i, zeta_i and xi.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4171_0_private_not_public",
            "rule": "PPC4161-TK-HQN is a private local branch, not a public local-GR claim.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4171_1_no_orbital_import",
            "rule": "Do not use observed orbital GM, fitted acceleration, or measured G_N to define M_H^dress.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4171_2_no_full_PPN_claim",
            "rule": "First-order Poisson/Gauss/Newton readout is not full PPN.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4171_3_no_numeric_G",
            "rule": "This checkpoint does not predict the numerical value of Newton's constant.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4171_4_multipole_guard",
            "rule": "The exact inverse-square radial law is monopole/spherical or leading far-field; compact non-spherical multipoles require residual bookkeeping.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "PPC4161_TK_HQN_private_packet_adopted": "True",
            "global_MTS_adopted": "False",
            "Poisson_equation_derived_private": "True",
            "Gauss_charge_readout_derived_private": "True",
            "inverse_square_monopole_derived_private": "True",
            "orbital_GM_imported": "False",
            "full_PPN_closed": "False",
            "empirical_orbital_tests_run": "False",
            "numeric_G_predicted": "False",
            "formal_187_written": "True",
            "claim_register_action": claim_action,
            "packet_180_action": packet_action,
            "spine_action": spine_action,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why_next": "4171 closes first-order Newtonian Poisson/Gauss readout inside the private branch, but full local GR requires PPN gamma, beta, preferred-frame, conservation and empirical gates.",
            "route_A": "derive PPC4161 PPN vector gamma-1, beta-1, alpha_i, zeta_i and xi from the same EH/local packet assumptions",
            "route_B": "if any PPN component is not derivable, retain explicit residual rows and source-backed bounds",
            "fallback": "public local-GR claim remains blocked until full PPN and empirical local tests pass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4171_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4171_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4171_WEAK_FIELD_READOUT": SOURCE_DIR / "P8_Y5_R2FR_4171_WEAK_FIELD_READOUT.csv",
        "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION.csv",
        "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT": SOURCE_DIR / "P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT.csv",
        "P8_Y5_R2FR_4171_RESIDUAL_CLOSE_OR_REACTIVATE": SOURCE_DIR / "P8_Y5_R2FR_4171_RESIDUAL_CLOSE_OR_REACTIVATE.csv",
        "P8_Y5_R2FR_4171_REMAINING_PPN_EMPIRICAL_GATES": SOURCE_DIR / "P8_Y5_R2FR_4171_REMAINING_PPN_EMPIRICAL_GATES.csv",
        "P8_Y5_R2FR_4171_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4171_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4171_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4171_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4171_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4171_STATUS.csv",
        "P8_Y5_R2FR_4171_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4171_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4171 - Hamiltonian Source Charge To Poisson/Gauss/Newton Readout

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4170 glued the Hamiltonian source charge:

```text
Q_M = M_H^dress[W_H;tau].
```

4171 derives the weak-field Newton readout from that same charge:

```text
G_00^lin = 2 nabla^2 Phi_N/c^2
T_00 = rho_H c^2
kappa_eff = 8*pi G_N/c^4.
```

Therefore:

```text
nabla^2 Phi_N = 4*pi G_N rho_H.
```

## Gauss And Acceleration
The compact source charge is:

```text
int_W rho_H dV = M_H^dress[W_H;tau].
```

Thus:

```text
int_S grad Phi_N dot dS = 4*pi G_N M_H^dress.
```

For the exterior monopole/spherical case, or leading far-field compact-source term:

```text
Phi_N = -G_N M_H^dress/r,
a = -grad Phi_N,
a_r = -G_N M_H^dress/r^2.
```

## Anti-Circularity
No observed orbital `GM`, fitted acceleration, or measured numerical `G_N` is used to define the charge. Orbits are downstream tests now.

## What Remains
This is first-order Newtonian recovery inside a private branch. It does not close full PPN:

```text
Delta_PPN = gamma-1, beta-1, alpha_i, zeta_i, xi.
```

## Next Target
`{NEXT_TARGET}`

## Outputs
{chr(10).join(f"- `{path}`" for path in outputs.values())}
""",
        encoding="utf-8",
    )


def validate(outputs: Dict[str, Path]) -> List[Dict[str, str]]:
    checks: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, details: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(passed),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = parse_csv(outputs["P8_Y5_R2FR_4171_SOURCE_REGISTER"])
    add("VAL4171_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    weak = parse_csv(outputs["P8_Y5_R2FR_4171_WEAK_FIELD_READOUT"])
    weak_text = "\n".join(",".join(row.values()) for row in weak)
    add("VAL4171_1_weak_field", "weak-field rows define branch, metric, source, linear EH equation and coupling", all(token in weak_text for token in ["PPC4161-TK-HQN", "g_00=-c^2-2 Phi_N", "T_00=rho_H c^2", "G_00^lin=2 nabla^2 Phi_N/c^2", "kappa_eff=8*pi G_N/c^4"]), weak_text)

    poisson = parse_csv(outputs["P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION"])
    poisson_text = "\n".join(",".join(row.values()) for row in poisson)
    add("VAL4171_2_poisson", "Poisson/Gauss rows derive Poisson equation and surface charge from M_H dress", all(token in poisson_text for token in ["nabla^2 Phi_N = 4*pi G_N rho_H", "int_W rho_H dV = M_H^dress", "int_S grad Phi_N dot dS = 4*pi G_N M_H^dress"]), poisson_text)

    orbital = parse_csv(outputs["P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT"])
    orbital_text = "\n".join(",".join(row.values()) for row in orbital)
    add("VAL4171_3_orbital", "orbital rows derive monopole potential, slow geodesic and inverse-square acceleration with anti-circularity and multipole guard", all(token in orbital_text for token in ["Phi_N=-G_N M_H^dress/r", "a=-grad Phi_N", "a_r=-G_N M_H^dress/r^2", "GM_orbit", "multipoles"]), orbital_text)

    residuals = parse_csv(outputs["P8_Y5_R2FR_4171_RESIDUAL_CLOSE_OR_REACTIVATE"])
    residual_text = "\n".join(",".join(row.values()) for row in residuals)
    add("VAL4171_4_residuals", "residual rows close Poisson, Gauss and orbital import while retaining rejection fallback", all(token in residual_text for token in ["Delta_Poisson", "Delta_Gauss", "Delta_orbital_import", "epsilon_Newton_readout", "fallback_only"]), residual_text)

    remaining = parse_csv(outputs["P8_Y5_R2FR_4171_REMAINING_PPN_EMPIRICAL_GATES"])
    remaining_text = "\n".join(",".join(row.values()) for row in remaining)
    add("VAL4171_5_remaining", "remaining gates keep full PPN, empirical tests, R10/clock/WEP, numerical G and global adoption open", all(token in remaining_text for token in ["gamma-1", "alpha_i", "fit residuals", "R10", "G_N=c^4 kappa_* Z_0/(8*pi)", "PPC4161-TK-HQN subset"]), remaining_text)

    decisions = parse_csv(outputs["P8_Y5_R2FR_4171_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add("VAL4171_6_decision", "decision rows move from Newton readout to full PPN", all(token in decision_text for token in ["Hamiltonian_source_to_Poisson_Gauss_Newton", "Orbital GM is not used", NEXT_TARGET]), decision_text)

    firewall = parse_csv(outputs["P8_Y5_R2FR_4171_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4171_7_firewall", "firewall blocks public, orbital-import, full-PPN, numerical-G and multipole overclaims", all(token in firewall_text for token in ["private local branch", "observed orbital GM", "not full PPN", "Newton's constant", "multipoles"]), firewall_text)

    formal_text = read_text(FORMAL_187_PATH)
    add("VAL4171_8_formal_187", "formal 187 bridge exists and records branch, Poisson derivation, Gauss readout, acceleration and next target", FORMAL_187_PATH.exists() and all(token in formal_text for token in ["PPC4161_POISSON_GAUSS_NEWTON_READOUT_FROM_HAMILTONIAN_SOURCE", "nabla^2 Phi_N = 4*pi G_N rho_H", "int_S grad Phi_N dot dS", "a_r = -G_N M_H^dress/r^2", NEXT_TARGET]), "formal 187 checked")

    packet_text = read_text(PACKET_180_PATH)
    add("VAL4171_9_packet_180", "packet 180 contains PPC4161-TK-HQN Newton readout addendum", all(token in packet_text for token in [PACKET_MARKER, "nabla^2 Phi_N = 4*pi G_N rho_H", "int_S grad Phi_N dot dS", "a_r = -G_N M_H^dress/r^2"]), "packet 180 checked")

    claims = parse_csv(CLAIMS_PATH)
    l012 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4171_10_claim_row", "claims register contains one L-012 private Newton readout nonclaim row", len(l012) == 1 and l012[0].get("status") == "private_packet_newton_readout_nonclaim_public_claim_false" and "public_claim=false" in l012[0].get("current_evidence", ""), str(l012))

    spine_text = read_text(SPINE_PATH)
    add("VAL4171_11_spine", "spine contains 4171 marker, claim row, Poisson/Gauss/Newton equations and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "nabla^2 Phi_N = 4*pi G_N rho_H", "a_r = -G_N M_H^dress/r^2", NEXT_TARGET]), "spine checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4171_STATUS"])
    add("VAL4171_12_status", "status records Poisson/Gauss/Newton private closure and PPN/empirical/numeric-G open", len(status) == 1 and status[0]["Poisson_equation_derived_private"] == "True" and status[0]["Gauss_charge_readout_derived_private"] == "True" and status[0]["inverse_square_monopole_derived_private"] == "True" and status[0]["orbital_GM_imported"] == "False" and status[0]["full_PPN_closed"] == "False" and status[0]["next_target"] == NEXT_TARGET, str(status))

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4171_NEXT_TARGET"])
    add("VAL4171_13_next", "next target moves to full PPN readout and source-backed residual rows if needed", len(next_loaded) == 1 and next_loaded[0]["next_target"] == NEXT_TARGET and "gamma-1" in "\n".join(next_loaded[0].values()) and "source-backed bounds" in "\n".join(next_loaded[0].values()), str(next_loaded))

    doc_text = read_text(DOC_PATH)
    add("VAL4171_14_doc", "checkpoint doc records move, Poisson/Gauss derivation, acceleration, anti-circularity and next target", all(token in doc_text for token in ["Q_M = M_H^dress", "nabla^2 Phi_N = 4*pi G_N rho_H", "a_r = -G_N M_H^dress/r^2", "No observed orbital", NEXT_TARGET]), "doc tokens checked")

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4171_15_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_details = "compiled"
    except Exception as exc:
        compile_ok = False
        compile_details = repr(exc)
    finally:
        cache = SCRIPT_PATH.parent / "__pycache__"
        if cache.exists():
            shutil.rmtree(cache)
    add("VAL4171_16_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_187()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4171_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_WEAK_FIELD_READOUT"], weak_field_rows(packet_action))
    write_csv(outputs["P8_Y5_R2FR_4171_POISSON_GAUSS_DERIVATION"], poisson_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_ORBITAL_ACCELERATION_READOUT"], orbital_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_RESIDUAL_CLOSE_OR_REACTIVATE"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_REMAINING_PPN_EMPIRICAL_GATES"], remaining_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4171_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4171_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4171_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_187_PATH}")
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['details']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
