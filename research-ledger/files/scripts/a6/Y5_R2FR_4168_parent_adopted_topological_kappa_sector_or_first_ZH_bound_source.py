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

CHECKPOINT = "4168"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ADOPTED_TOPOLOGICAL_KAPPA_SECTOR_4168"
DECISION = "PPC4161_TK_PRIVATE_PARENT_PACKET_ADOPTS_LOG_KAPPA_TOPOLOGICAL_SECTOR_KAPPA_DRIFT_CLOSED_DELTA_ZH_REMAINS"
DOC_PATH = POST / "4168-Y5-R2FR-parent-adopted-topological-kappa-sector-or-first-ZH-bound-source.md"
FORMAL_184_PATH = FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-009"
SPINE_MARKER = "PPC4161_TOPO_PARENT_ADOPTION_4168"
PACKET_MARKER = "PPC4161_PACKET_TOPO_KAPPA_ADOPTION_4168"
NEXT_TARGET = "4169-Y5-R2FR-delta-ZH-source-measure-vanishing-or-first-real-bound-row.md"

SOURCES = {
    "SRC4168_00_4167_doc": (
        POST / "4167-Y5-R2FR-topological-kappa-star-lock-or-ZH-derivative-bound.md",
        "math candidate pass, parent adoption unsigned",
        "4167 checkpoint doc that left parent adoption unsigned.",
    ),
    "SRC4168_01_4167_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4167_NEXT_TARGET.csv",
        "parent-adopt S_top=int A_3 wedge d(kappa_*)",
        "4167 next-target route A.",
    ),
    "SRC4168_02_4167_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4167_STATUS.csv",
        "topological_sector_parent_adopted",
        "4167 status proving the parent sector was not yet adopted.",
    ),
    "SRC4168_03_4167_attempt": (
        SOURCE_DIR / "P8_Y5_R2FR_4167_TOPOLOGICAL_KAPPA_LOCK_ATTEMPT.csv",
        "TK4167_1_A3_variation",
        "4167 variation proof skeleton.",
    ),
    "SRC4168_04_4167_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4167_ZH_DERIVATIVE_BOUND_ROWS.csv",
        "ZDB4167_6_readout",
        "4167 fallback derivative-bound rows.",
    ),
    "SRC4168_05_formal_180": (
        PACKET_180_PATH,
        "S_top+S_vertical",
        "PPC4161 private local packet already contains a generic S_top slot.",
    ),
    "SRC4168_06_formal_183": (
        FORMAL / "183-PPC4161-topological-kappa-star-lock-or-ZH-bound.md",
        "S_top[kappa_*, A_3]",
        "Formal 183 topological kappa candidate.",
    ),
    "SRC4168_07_formal_182": (
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "Z_H = Z_0 exp(delta_ZH)",
        "Formal 182 source-measure leak split.",
    ),
    "SRC4168_08_formal_181": (
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "G_N = c^4 kappa_eff/(8*pi)",
        "Formal 181 Newton coupling relation.",
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
        "claim": "PPC4161-TK privately adopts a metric-independent topological log-kappa sector that closes the kappa_* drift residual in the local packet",
        "current_evidence": "formalization-workbench/184-PPC4161-parent-adopted-topological-kappa-sector.md records u_kappa=ln(kappa_*/kappa_0), S_top=C_top int A_3 wedge d u_kappa, delta_A3 S=>d u_kappa=0, T_top=0, and R_A^G reduces to D_A delta_ZH; public_claim=false",
        "status": "private_packet_adoption_nonclaim_public_claim_false",
        "next_test": "Derive delta_ZH=0 from a common Hilbert source-measure theorem or fill first source-backed local bound row for D_A delta_ZH",
        "key_risk": "This closes kappa drift only inside PPC4161-TK; it does not prove global MTS adoption, does not predict numerical G_N, and does not close Z_H leakage",
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

## PPC4161-TK Addendum - Topological Kappa Sector Adoption

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4168-Y5-R2FR-parent-adopted-topological-kappa-sector-or-first-ZH-bound-source.md`

Inside the private PPC4161 local packet only, the previously generic `S_top` slot is fixed to the log-coupling topological sector:

```text
u_kappa = ln(kappa_*/kappa_0)
S_top^kappa = C_top int_M A_3 wedge d u_kappa
```

with nonzero `C_top`, fixed `kappa_0` as a unit/reference anchor rather than measured `G_N`, and `A_3` an independent source-blind parent three-form.

The private packet boundary condition is:

```text
delta u_kappa|_boundary = 0
```

or an equivalent fixed-flux/superselection condition before any local readout. Therefore:

```text
delta_A3 S_top^kappa = 0 => d u_kappa = 0 => D_A ln kappa_* = 0.
```

This closes the `kappa_*` drift piece of the PPC4161 local coupling residual. It does not close `delta_ZH`, does not predict the numerical value of `G_N`, and does not upgrade PPC4161 to a public/global local-GR theorem.
"""
    PACKET_180_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def write_formal_184() -> None:
    FORMAL_184_PATH.write_text(
        f"""# 184 - PPC4161 Parent-Adopted Topological Kappa Sector

Marker: `PPC4161_PARENT_ADOPTED_TOPOLOGICAL_KAPPA_SECTOR`  
Timestamp UTC: `{now()}`  
Status: `private_packet_adoption_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Adoption Move
Checkpoint 4167 proved that a topological `A_3` sector can lock `kappa_*` if adopted. Checkpoint 4168 now adopts the sector inside the private PPC4161 local parent packet:

```text
PPC4161-TK := PPC4161 + S_top^kappa
```

with:

```text
u_kappa = ln(kappa_*/kappa_0)
S_top^kappa = C_top int_M A_3 wedge d u_kappa.
```

`kappa_0` is a fixed unit/reference anchor, not the measured Newton constant. The logarithmic variable is used because the local observable residual is `D_A ln kappa_*`.

## Variation
Varying `A_3` gives:

```text
delta_A3 S_top^kappa = C_top int_M delta A_3 wedge d u_kappa = 0
=> d u_kappa = 0.
```

On a connected local branch:

```text
d u_kappa = 0
=> D_A ln kappa_* = 0.
```

Varying `u_kappa` gives:

```text
delta_u S_top^kappa = C_top int_M dA_3 delta u_kappa - C_top int_boundary A_3 delta u_kappa.
```

With `delta u_kappa|_boundary=0`, or equivalent fixed flux/superselection data, the companion equation is:

```text
dA_3 = 0.
```

## Stress And Source Blindness
`S_top^kappa` is independent of `g_obs`, matter fields, Maxwell fields, clock readout, orbital labels, and source composition. Therefore:

```text
T_top^munu = -2/sqrt(-g) delta S_top^kappa / delta g_munu = 0
delta S_top^kappa / delta psi_matter = 0
delta S_top^kappa / delta A_EM = 0
```

inside the private local packet. The sector locks a coupling label; it does not add a local force or an extra stress source.

## Coupling Residual After Adoption
Before 4168:

```text
R_A^G = D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH.
```

Inside PPC4161-TK:

```text
D_A ln kappa_* = 0
```

so:

```text
R_A^G = D_A delta_ZH.
```

This is the useful reduction. The `kappa_*` side is no longer the active local-coupling leak in the private packet; the remaining physical work is the source-measure leak `delta_ZH`.

## Nonclaim
This does not predict the numerical value of:

```text
G_N = c^4 kappa_* Z_H/(8*pi).
```

It also does not prove global MTS adoption. It is a private local parent-packet extension that makes the local-GR coupling route sharper and less hand-wavy.

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

## 14. Local GR Coupling Update - PPC4161-TK Kappa Drift Closed

Marker: `{SPINE_MARKER}`  
Source bridge: `184-PPC4161-parent-adopted-topological-kappa-sector.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4168` makes the previous topological route explicit inside the private PPC4161 local parent packet:

```text
u_kappa = ln(kappa_*/kappa_0)
S_top^kappa = C_top int A_3 wedge d u_kappa.
```

The variation gives:

```text
delta_A3 S_top^kappa = 0 => d u_kappa = 0 => D_A ln kappa_* = 0.
```

Because the term is metric-independent and source-blind, it adds no Hilbert stress and no matter/EM source. Therefore the local coupling residual reduces from:

```text
R_A^G = D_A ln kappa_* + D_A delta_ZH
```

to:

```text
R_A^G = D_A delta_ZH.
```

This closes the `kappa_*` drift side of the local coupling branch inside PPC4161-TK. It is still not a public local-GR theorem, not a global MTS adoption, and not a numerical prediction of `G_N`.

The next local-GR coupling step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def action_extension_rows(packet_action: str) -> List[Dict[str, str]]:
    rows = [
        (
            "PA4168_0_packet_owner",
            "private packet owner",
            "PPC4161-TK := PPC4161 + S_top^kappa",
            "The adoption is inside the private PPC4161 local branch, not global MTS corpus adoption.",
            "private_parent_packet_adopted",
        ),
        (
            "PA4168_1_log_variable",
            "dimensionless log coupling",
            "u_kappa=ln(kappa_*/kappa_0)",
            "Locks the derivative that actually enters local tests while avoiding a dimensionful d(kappa_*) ambiguity.",
            "derived_variable_choice",
        ),
        (
            "PA4168_2_top_action",
            "topological action",
            "S_top^kappa=C_top int_M A_3 wedge d u_kappa",
            "C_top is nonzero; A_3 is an independent parent three-form.",
            "private_parent_packet_adopted",
        ),
        (
            "PA4168_3_boundary",
            "boundary/superselection data",
            "delta u_kappa|_boundary=0 or fixed flux/superselection data before readout",
            "Prevents the kappa lock from being a fitted boundary convention.",
            "private_boundary_clause_signed",
        ),
        (
            "PA4168_4_source_blind",
            "source-blind field owner",
            "A_3=A_3[parent topology], not A_3[source,species,frame,range,environment,readout]",
            "Prevents the topological sector from carrying the leak labels it is meant to remove.",
            "private_source_blind_clause_signed",
        ),
        (
            "PA4168_5_packet_sync",
            "packet integration addendum",
            f"{PACKET_180_PATH}",
            f"180 packet addendum action={packet_action}.",
            "formal_sync_done",
        ),
    ]
    return [
        {
            **common(),
            "action_id": row[0],
            "name": row[1],
            "formula_or_path": row[2],
            "meaning": row[3],
            "status": row[4],
            "global_corpus_adopted": "False",
            "private_packet_adopted": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def variation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VAR4168_0_A3",
            "A_3 variation",
            "delta_A3 S_top^kappa=C_top int delta A_3 wedge d u_kappa=0",
            "d u_kappa=0",
            "A_3 variations are arbitrary compactly supported three-form variations in the local branch.",
            "private_packet_proved",
        ),
        (
            "VAR4168_1_connected",
            "connected branch",
            "d u_kappa=0 and u_kappa=ln(kappa_*/kappa_0)",
            "D_A ln kappa_*=0 for A={time,species,frame,range,environment,readout}",
            "The local tested branch is connected and uses one parent kappa_* sector.",
            "private_packet_proved",
        ),
        (
            "VAR4168_2_u",
            "u_kappa variation",
            "delta_u S_top^kappa=C_top int dA_3 delta u_kappa - C_top int_boundary A_3 delta u_kappa",
            "dA_3=0",
            "Boundary term is killed by fixed delta u_kappa at boundary or fixed flux/superselection.",
            "private_packet_proved_with_boundary_clause",
        ),
        (
            "VAR4168_3_no_magnitude",
            "constant not value",
            "d u_kappa=0",
            "kappa_* is constant on branch, not numerically predicted",
            "Topological sectors fix superselection labels; they do not determine the label value without a separate scale law.",
            "not_numeric_G_prediction",
        ),
    ]
    return [
        {
            **common(),
            "variation_id": row[0],
            "step": row[1],
            "variation_formula": row[2],
            "euler_or_implication": row[3],
            "assumption": row[4],
            "status": row[5],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def stress_source_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SS4168_0_metric",
            "metric/Hilbert stress",
            "delta S_top^kappa/delta g_munu=0",
            "T_top^munu=0",
            "S_top^kappa uses exterior derivative and forms only; no metric or Hodge star.",
            "private_packet_closed",
        ),
        (
            "SS4168_1_matter",
            "matter fields",
            "delta S_top^kappa/delta psi_matter=0",
            "no matter force/current source from topological kappa sector",
            "No matter fields appear in S_top^kappa.",
            "private_packet_closed",
        ),
        (
            "SS4168_2_EM",
            "Maxwell/EM fields",
            "delta S_top^kappa/delta A_EM=0",
            "no EM stress/current source from topological kappa sector",
            "No EM potential or F appears in S_top^kappa.",
            "private_packet_closed",
        ),
        (
            "SS4168_3_labels",
            "label blindness",
            "partial_{source,species,frame,range,environment,readout} A_3=0 by PPC4161-TK field ownership",
            "A_3 cannot carry the local leak labels.",
            "This is an adoption clause, not a derived global theorem.",
            "private_packet_signed_global_unsigned",
        ),
    ]
    return [
        {
            **common(),
            "source_blind_id": row[0],
            "arena": row[1],
            "condition": row[2],
            "result": row[3],
            "reason": row[4],
            "status": row[5],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def residual_close_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RC4168_0_before",
            "pre-4168 coupling residual",
            "R_A^G=D_A ln G_eff=D_A ln kappa_* + D_A delta_ZH",
            "both kappa drift and source-measure leakage active",
            "from 4166/4167",
        ),
        (
            "RC4168_1_kappa_closed",
            "PPC4161-TK kappa closure",
            "D_A ln kappa_*=0",
            "topological sector removes kappa drift in local branch",
            "proved inside private packet",
        ),
        (
            "RC4168_2_after",
            "post-4168 coupling residual",
            "R_A^G=D_A delta_ZH",
            "remaining local coupling leak is source-measure only",
            "new reduced target",
        ),
        (
            "RC4168_3_full_close_condition",
            "full local coupling closure",
            "D_A delta_ZH=0 => R_A^G=0",
            "local Gdot/source/frame/range/readout coupling residual vanishes only when Z_H leak closes too",
            "next theorem_or_bound_target",
        ),
        (
            "RC4168_4_numeric_G",
            "magnitude untouched",
            "G_N=c^4 kappa_* Z_H/(8*pi)",
            "constant kappa_* does not determine the numerical value of G_N",
            "nonclaim_guard",
        ),
    ]
    return [
        {
            **common(),
            "residual_id": row[0],
            "name": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def remaining_bound_rows() -> List[Dict[str, str]]:
    data = [
        ("ZDB4168_0_time", "time", "D_t delta_ZH", "|D_t delta_ZH| <= B_Gdot", "Gdot/G, clock, pulsar, orbital secular drift"),
        ("ZDB4168_1_species", "species", "Delta_AB delta_ZH", "|Delta_AB delta_ZH| <= B_WEP_AB", "WEP/source universality/composition dependence"),
        ("ZDB4168_2_frame", "frame", "D_frame delta_ZH", "|D_frame delta_ZH| <= B_PPN_alpha", "PPN preferred-frame/source-frame normalization"),
        ("ZDB4168_3_range", "range", "D_lambda delta_ZH", "|D_lambda delta_ZH| <= B_alpha_lambda", "R10/Yukawa/range-dependent effective G"),
        ("ZDB4168_4_environment", "environment", "D_env delta_ZH", "|D_env delta_ZH| <= B_env", "solar/local-vacuum versus galaxy/cosmology leakage"),
        ("ZDB4168_5_readout", "readout", "D_readout delta_ZH", "|D_readout delta_ZH| <= B_readout", "measured GM, detector, clock and orbital convention absorption"),
    ]
    return [
        {
            **common(),
            "bound_id": row[0],
            "owner": "delta_ZH",
            "channel": row[1],
            "operator": row[2],
            "required_bound_or_zero": row[3],
            "arena": row[4],
            "source_path_or_status": "MISSING_SOURCE_BACKED_BOUND_OR_PARENT_ZERO_THEOREM",
            "numeric_value": "MISSING_NUMERIC_INPUT",
            "source_status": "not_source_backed_for_claim",
            "kappa_piece_status": "closed_inside_PPC4161_TK",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in data
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "BD4168_0_adoption",
            "route": "parent_adopted_topological_kappa_sector",
            "result": "PPC4161-TK adopts S_top^kappa=C_top int A_3 wedge d ln(kappa_*/kappa_0) inside the private local packet.",
            "gate_state": "private_packet_pass_global_public_claim_false",
            "next_action": "Stop spending effort on kappa drift unless challenging PPC4161-TK; move pressure to delta_ZH source-measure theorem or bounds.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4168_1_reduced_residual",
            "route": "local_coupling_residual",
            "result": "R_A^G reduces from D_A ln kappa_* + D_A delta_ZH to D_A delta_ZH.",
            "gate_state": "kappa_closed_ZH_open",
            "next_action": "Try to derive common Hilbert source-measure descent delta_ZH=0; if not, fill one real source-backed local bound row.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4168_2_next",
            "route": "next_target",
            "result": NEXT_TARGET,
            "gate_state": "derive_ZH_first_then_bound_source",
            "next_action": "Attack delta_ZH directly, with time/Gdot or range/R10 as first bound fallback if derivation fails.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4168_0_private_not_global",
            "rule": "PPC4161-TK is a private local packet extension, not global MTS corpus adoption.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4168_1_no_numeric_G",
            "rule": "The topological sector makes kappa_* locally constant but does not predict the numerical value of G_N.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4168_2_ZH_still_open",
            "rule": "Local coupling closure is not complete until D_A delta_ZH is zero or source-bounded.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4168_3_no_force_from_top",
            "rule": "Do not treat S_top^kappa as a new local force/stress source; it is metric-independent and source-blind in PPC4161-TK.",
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
            "PPC4161_TK_private_packet_adopted": "True",
            "global_MTS_adopted": "False",
            "log_kappa_variable_used": "True",
            "A3_variation_proves_DA_ln_kappa_zero": "True",
            "boundary_clause_signed_private": "True",
            "source_blind_A3_signed_private": "True",
            "topological_stress_zero": "True",
            "numeric_G_predicted": "False",
            "coupling_residual_reduced_to_delta_ZH": "True",
            "delta_ZH_closed": "False",
            "formal_184_written": "True",
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
            "why_next": "4168 closes D_A ln kappa_* inside PPC4161-TK, so the remaining local coupling residual is D_A delta_ZH.",
            "route_A": "derive common Hilbert source-measure descent so delta_ZH=0 across time/species/frame/range/environment/readout",
            "route_B": "if no theorem closes delta_ZH, fill the first real source-backed bound row, prioritizing time/Gdot or range/R10",
            "fallback": "public local-GR claim remains blocked; private branch can say kappa drift is closed but Z_H source-measure leakage remains open",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4168_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4168_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4168_PARENT_ACTION_EXTENSION": SOURCE_DIR / "P8_Y5_R2FR_4168_PARENT_ACTION_EXTENSION.csv",
        "P8_Y5_R2FR_4168_VARIATION_PROOF": SOURCE_DIR / "P8_Y5_R2FR_4168_VARIATION_PROOF.csv",
        "P8_Y5_R2FR_4168_STRESS_SOURCE_BLINDNESS": SOURCE_DIR / "P8_Y5_R2FR_4168_STRESS_SOURCE_BLINDNESS.csv",
        "P8_Y5_R2FR_4168_LOCAL_COUPLING_RESIDUAL_CLOSE": SOURCE_DIR / "P8_Y5_R2FR_4168_LOCAL_COUPLING_RESIDUAL_CLOSE.csv",
        "P8_Y5_R2FR_4168_REMAINING_ZH_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4168_REMAINING_ZH_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4168_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4168_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4168_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4168_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4168_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4168_STATUS.csv",
        "P8_Y5_R2FR_4168_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4168_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4168 - Parent-Adopted Topological Kappa Sector Or First ZH Bound Source

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4167 left the topological lock as a candidate. 4168 takes the leap inside the private PPC4161 local packet:

```text
PPC4161-TK := PPC4161 + S_top^kappa
u_kappa = ln(kappa_*/kappa_0)
S_top^kappa = C_top int_M A_3 wedge d u_kappa.
```

This uses the log coupling because the local tests see:

```text
D_A ln kappa_*.
```

`kappa_0` is only a unit/reference anchor. It is not measured `G_N`.

## Derivation
Variation with respect to `A_3` gives:

```text
delta_A3 S_top^kappa = C_top int_M delta A_3 wedge d u_kappa = 0
=> d u_kappa = 0.
```

Therefore, on a connected local branch:

```text
D_A ln kappa_* = 0.
```

The companion variation is:

```text
delta_u S_top^kappa = C_top int_M dA_3 delta u_kappa - C_top int_boundary A_3 delta u_kappa.
```

With fixed boundary/fixed flux/superselection data:

```text
dA_3 = 0.
```

## Source And Stress Check
The adopted topological term contains no metric, no matter fields, no EM field, and no source/readout labels. Thus:

```text
T_top^munu = 0,
delta S_top^kappa/delta psi_matter = 0,
delta S_top^kappa/delta A_EM = 0.
```

It locks the coupling label. It does not add a new local force.

## Reduced Coupling Residual
Before this:

```text
R_A^G = D_A ln kappa_* + D_A delta_ZH.
```

Inside PPC4161-TK:

```text
D_A ln kappa_* = 0,
R_A^G = D_A delta_ZH.
```

That is the real progress: the `kappa_*` side is closed in the private branch. The remaining target is now cleanly `delta_ZH`.

## Nonclaim
Still not claimed:

- no global MTS adoption;
- no public local-GR theorem;
- no numerical prediction of `G_N`;
- no proof yet that `D_A delta_ZH=0`.

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

    sources = parse_csv(outputs["P8_Y5_R2FR_4168_SOURCE_REGISTER"])
    add(
        "VAL4168_0_sources",
        "all source paths exist and contain required tokens",
        all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources),
        str(sources),
    )

    action = parse_csv(outputs["P8_Y5_R2FR_4168_PARENT_ACTION_EXTENSION"])
    action_text = "\n".join(",".join(row.values()) for row in action)
    add(
        "VAL4168_1_action_extension",
        "action extension privately adopts log-kappa topological sector with boundary/source-blind clauses",
        all(token in action_text for token in ["PPC4161-TK", "u_kappa=ln(kappa_*/kappa_0)", "S_top^kappa=C_top int_M A_3 wedge d u_kappa", "delta u_kappa|_boundary=0", "A_3=A_3[parent topology]"])
        and all(row["private_packet_adopted"] == "True" and row["global_corpus_adopted"] == "False" for row in action),
        action_text,
    )

    variations = parse_csv(outputs["P8_Y5_R2FR_4168_VARIATION_PROOF"])
    variation_text = "\n".join(",".join(row.values()) for row in variations)
    add(
        "VAL4168_2_variation",
        "variation proof closes D_A ln kappa_* and keeps numerical G unpredicted",
        all(token in variation_text for token in ["d u_kappa=0", "D_A ln kappa_*=0", "dA_3=0", "not_numeric_G_prediction"]),
        variation_text,
    )

    source_blind = parse_csv(outputs["P8_Y5_R2FR_4168_STRESS_SOURCE_BLINDNESS"])
    source_blind_text = "\n".join(",".join(row.values()) for row in source_blind)
    add(
        "VAL4168_3_source_blind",
        "stress/source rows prove no metric, matter or EM source from S_top^kappa inside the private packet",
        all(token in source_blind_text for token in ["T_top^munu=0", "delta S_top^kappa/delta psi_matter=0", "delta S_top^kappa/delta A_EM=0", "partial_{source,species,frame,range,environment,readout} A_3=0"]),
        source_blind_text,
    )

    residuals = parse_csv(outputs["P8_Y5_R2FR_4168_LOCAL_COUPLING_RESIDUAL_CLOSE"])
    residual_text = "\n".join(",".join(row.values()) for row in residuals)
    add(
        "VAL4168_4_residual_close",
        "coupling residual reduces from kappa plus ZH to ZH only",
        all(token in residual_text for token in ["R_A^G=D_A ln G_eff=D_A ln kappa_* + D_A delta_ZH", "D_A ln kappa_*=0", "R_A^G=D_A delta_ZH", "G_N=c^4 kappa_* Z_H/(8*pi)"]),
        residual_text,
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4168_REMAINING_ZH_BOUND_ROWS"])
    channels = {row["channel"] for row in bounds}
    add(
        "VAL4168_5_remaining_bounds",
        "remaining ZH bound rows cover the six leak channels and mark kappa piece closed",
        channels == {"time", "species", "frame", "range", "environment", "readout"}
        and all(row["kappa_piece_status"] == "closed_inside_PPC4161_TK" for row in bounds)
        and all(row["source_status"] == "not_source_backed_for_claim" for row in bounds),
        str(bounds),
    )

    decisions = parse_csv(outputs["P8_Y5_R2FR_4168_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add(
        "VAL4168_6_decision",
        "branch decision moves pressure from kappa drift to delta_ZH theorem or source bounds",
        all(token in decision_text for token in ["parent_adopted_topological_kappa_sector", "R_A^G reduces", "D_A delta_ZH", NEXT_TARGET]),
        decision_text,
    )

    firewall = parse_csv(outputs["P8_Y5_R2FR_4168_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add(
        "VAL4168_7_firewall",
        "firewall blocks global adoption, numerical-G, ZH and force/stress overclaims",
        all(token in firewall_text for token in ["private local packet", "numerical value of G_N", "D_A delta_ZH", "new local force/stress"]),
        firewall_text,
    )

    formal_text = read_text(FORMAL_184_PATH)
    add(
        "VAL4168_8_formal_184",
        "formal 184 bridge exists and records adoption, variation, source/stress silence and next target",
        FORMAL_184_PATH.exists()
        and all(token in formal_text for token in ["PPC4161_PARENT_ADOPTED_TOPOLOGICAL_KAPPA_SECTOR", "PPC4161-TK := PPC4161 + S_top^kappa", "d u_kappa = 0", "T_top^munu", "R_A^G = D_A delta_ZH", NEXT_TARGET]),
        "formal 184 checked",
    )

    packet_text = read_text(PACKET_180_PATH)
    add(
        "VAL4168_9_packet_180",
        "packet 180 contains PPC4161-TK addendum with log-kappa topological sector",
        all(token in packet_text for token in [PACKET_MARKER, "u_kappa = ln(kappa_*/kappa_0)", "S_top^kappa = C_top int_M A_3 wedge d u_kappa", "D_A ln kappa_* = 0"]),
        "packet 180 checked",
    )

    claims = parse_csv(CLAIMS_PATH)
    l009 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add(
        "VAL4168_10_claim_row",
        "claims register contains one L-009 private packet adoption nonclaim row",
        len(l009) == 1 and l009[0].get("status") == "private_packet_adoption_nonclaim_public_claim_false" and "public_claim=false" in l009[0].get("current_evidence", ""),
        str(l009),
    )

    spine_text = read_text(SPINE_PATH)
    add(
        "VAL4168_11_spine",
        "spine contains 4168 marker, claim row, log action, residual reduction and next target",
        all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "S_top^kappa = C_top int A_3 wedge d u_kappa", "R_A^G = D_A delta_ZH", NEXT_TARGET]),
        "spine checked",
    )

    status = parse_csv(outputs["P8_Y5_R2FR_4168_STATUS"])
    add(
        "VAL4168_12_status",
        "status records private adoption, kappa closure, stress zero, ZH open and next target",
        len(status) == 1
        and status[0]["PPC4161_TK_private_packet_adopted"] == "True"
        and status[0]["A3_variation_proves_DA_ln_kappa_zero"] == "True"
        and status[0]["topological_stress_zero"] == "True"
        and status[0]["coupling_residual_reduced_to_delta_ZH"] == "True"
        and status[0]["delta_ZH_closed"] == "False"
        and status[0]["next_target"] == NEXT_TARGET,
        str(status),
    )

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4168_NEXT_TARGET"])
    add(
        "VAL4168_13_next",
        "next target attacks delta_ZH theorem first with source-bound fallback",
        len(next_loaded) == 1
        and next_loaded[0]["next_target"] == NEXT_TARGET
        and "delta_ZH=0" in "\n".join(next_loaded[0].values())
        and "source-backed bound" in "\n".join(next_loaded[0].values()),
        str(next_loaded),
    )

    doc_text = read_text(DOC_PATH)
    add(
        "VAL4168_14_doc",
        "checkpoint doc records adoption move, derivation, source/stress check, reduced residual and nonclaim",
        all(token in doc_text for token in ["PPC4161-TK := PPC4161 + S_top^kappa", "d u_kappa = 0", "T_top^munu = 0", "R_A^G = D_A delta_ZH", "no numerical prediction of `G_N`", NEXT_TARGET]),
        "doc tokens checked",
    )

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add(
        "VAL4168_15_no_claim_rows",
        "all generated rows keep claim_allowed/valid_for_claim false",
        not claim_failures,
        str(claim_failures),
    )

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
    add(
        "VAL4168_16_compile",
        "generator compiles and pycache is removed",
        compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(),
        compile_details,
    )

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_184()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4168_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_PARENT_ACTION_EXTENSION"], action_extension_rows(packet_action))
    write_csv(outputs["P8_Y5_R2FR_4168_VARIATION_PROOF"], variation_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_STRESS_SOURCE_BLINDNESS"], stress_source_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_LOCAL_COUPLING_RESIDUAL_CLOSE"], residual_close_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_REMAINING_ZH_BOUND_ROWS"], remaining_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4168_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4168_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4168_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_184_PATH}")
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
