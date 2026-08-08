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

CHECKPOINT = "4169"
BRANCH_ID = "MTS_R2FR_Y5_DELTA_ZH_SOURCE_MEASURE_DESCENT_4169"
DECISION = "PPC4161_TK_H_HILBERT_SOURCE_DESCENT_CLOSES_DELTA_ZH_PRIVATE_PACKET_MASS_READOUT_GLUE_REMAINS"
DOC_PATH = POST / "4169-Y5-R2FR-delta-ZH-source-measure-vanishing-or-first-real-bound-row.md"
FORMAL_185_PATH = FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-010"
SPINE_MARKER = "PPC4161_DELTA_ZH_SOURCE_DESCENT_4169"
PACKET_MARKER = "PPC4161_PACKET_HILBERT_SOURCE_DESCENT_4169"
NEXT_TARGET = "4170-Y5-R2FR-Hilbert-source-charge-to-worldtube-mass-readout-glue.md"

SOURCES = {
    "SRC4169_00_4168_doc": (
        POST / "4168-Y5-R2FR-parent-adopted-topological-kappa-sector-or-first-ZH-bound-source.md",
        "R_A^G = D_A delta_ZH",
        "4168 checkpoint doc reducing the coupling residual to delta_ZH.",
    ),
    "SRC4169_01_4168_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4168_NEXT_TARGET.csv",
        "derive common Hilbert source-measure descent",
        "4168 next-target route A.",
    ),
    "SRC4169_02_4168_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4168_STATUS.csv",
        "delta_ZH_closed",
        "4168 status showing delta_ZH was still open.",
    ),
    "SRC4169_03_4168_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4168_LOCAL_COUPLING_RESIDUAL_CLOSE.csv",
        "R_A^G=D_A delta_ZH",
        "4168 residual reduction table.",
    ),
    "SRC4169_04_180_packet": (
        PACKET_180_PATH,
        "S_matter[psi,g_obs,theta]+S_EM[A,g_obs]",
        "PPC4161 packet already declares same observed metric matter/EM action slots.",
    ),
    "SRC4169_05_184_topo": (
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "D_A ln kappa_* = 0",
        "4168 formal bridge proving kappa drift closure in PPC4161-TK.",
    ),
    "SRC4169_06_182_ZH": (
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "Z_H = Z_0 exp(delta_ZH)",
        "4166 formal bridge defining the physical source-measure leak.",
    ),
    "SRC4169_07_1229_contract": (
        POST / "1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md",
        "If S_matter descends to c_* Sbar_m",
        "Earlier universal source-coupling theorem contract.",
    ),
    "SRC4169_08_4155_source_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained",
        "Worldtube/Hilbert/Poynting source-current assembly.",
    ),
    "SRC4169_09_HSM541": (
        SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "HSM541_2_observed_worldtube_source",
        "Hamiltonian source-measure contract, still leaving mass-readout glue separate.",
    ),
    "SRC4169_10_1009_parent_chain": (
        POST / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "S_matter[psi,g_obs]",
        "Parent action contract row for universal matter coupling.",
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
        "claim": "PPC4161-TK-H privately adopts a single Hilbert-descended matter/EM/binding source action, closing the delta_ZH local coupling leak inside the private packet",
        "current_evidence": "formalization-workbench/185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md records S_src=S_matter+S_EM+S_binding+dB_impr+S_rest, one observed g_obs measure, no species/readout multipliers, T_parent^H=Z0 T_H with delta_ZH=0, and R_A^G=0 inside PPC4161-TK-H; public_claim=false",
        "status": "private_packet_source_descent_nonclaim_public_claim_false",
        "next_test": "Glue the Hilbert source current to the worldtube/Hamiltonian mass readout, or keep mass-readout/PPN residual gates active",
        "key_risk": "This closes the local coupling multiplier only inside PPC4161-TK-H; it does not prove global corpus adoption, measured-G magnitude, Pi_M/H_tau mass readout glue, or full PPN",
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

## PPC4161-TK-H Addendum - Hilbert Source-Measure Descent

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4169-Y5-R2FR-delta-ZH-source-measure-vanishing-or-first-real-bound-row.md`

Inside the private PPC4161-TK local packet, ordinary local sources are restricted to one Hilbert-descended source action:

```text
S_src = S_matter[psi,g_obs,theta]
      + S_EM[A,g_obs]
      + S_binding[psi,A,g_obs]
      + int dB_impr
      + S_rest^top/zero.
```

There are no independent source weights `w_A`, no species-dependent action multipliers, no range/frame/environment/readout labels in the source measure, and the same observed metric/coframe `g_obs` is used for matter, EM, clocks, and the local EH source equation.

Therefore:

```text
T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu
T_parent^H = Z_0 T_H
Z_H = Z_0 exp(delta_ZH)
delta_ZH = 0
```

with `Z_0` the single common normalization already absorbable into the calibrated local coupling. Since checkpoint 4168 closed `D_A ln kappa_*`, the PPC4161-TK-H local coupling residual becomes:

```text
R_A^G = D_A ln kappa_* + D_A delta_ZH = 0.
```

This does not identify the Hilbert source charge with a measured worldtube/orbital mass; that Pi_M/H_tau/readout glue remains the next gate.
"""
    PACKET_180_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def write_formal_185() -> None:
    FORMAL_185_PATH.write_text(
        f"""# 185 - PPC4161 Hilbert Source-Measure Descent And Delta-ZH Closure

Marker: `PPC4161_HILBERT_SOURCE_MEASURE_DESCENT_DELTA_ZH_CLOSURE`  
Timestamp UTC: `{now()}`  
Status: `private_packet_source_descent_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Source-Measure Descent Clause
Inside the private PPC4161-TK packet, define:

```text
PPC4161-TK-H := PPC4161-TK + H_src
```

where `H_src` is the Hilbert source-measure descent clause:

```text
S_src = S_matter[psi,g_obs,theta]
      + S_EM[A,g_obs]
      + S_binding[psi,A,g_obs]
      + int dB_impr
      + S_rest^top/zero.
```

All ordinary local source sectors use the same observed metric/coframe and the same volume measure. Independent source weights are not admitted:

```text
S_src != sum_A w_A S_A,    D_A w_B = 0 only because no w_B exists.
```

## Hilbert Source Identity
The local source stress is defined by the same action that appears in the local EH equation:

```text
T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu.
```

The EM/Poynting contribution is not an add-on:

```text
T_H = T_matter + T_EM + T_binding + T_impr_exact + T_rest_top/zero.
```

Exact improvements contribute boundary terms only, and the retained rest sector is topological or zero in the compact local collar.

## Delta-ZH Closure
The previous source-measure split was:

```text
T_parent^H = Z_H T_H + T_leak,
Z_H = Z_0 exp(delta_ZH).
```

Under `H_src`, there is one common source normalization only:

```text
T_parent^H = Z_0 T_H,    T_leak = 0.
```

Thus the physical leak is absent:

```text
delta_ZH = 0,
D_A delta_ZH = 0,
A in {{time,species,frame,range,environment,readout}}.
```

The common `Z_0` is the same absorbable normalization already isolated in checkpoint 4166. It is not a hidden composition/range/readout dependence.

## Coupling Residual
Checkpoint 4168 gave:

```text
D_A ln kappa_* = 0.
```

Therefore inside PPC4161-TK-H:

```text
R_A^G = D_A ln G_eff
      = D_A ln kappa_* + D_A delta_ZH
      = 0.
```

## What Remains
This closes the local coupling multiplier residual inside the private packet. It does not yet prove:

- global MTS parent adoption;
- the numerical value of `G_N`;
- Hilbert charge to worldtube/orbital measured mass glue;
- full PPN readout beyond the already guarded local branch;
- empirical source-backed pass rows.

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

## 15. Local GR Coupling Update - Delta-ZH Source-Measure Closure

Marker: `{SPINE_MARKER}`  
Source bridge: `185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4169` adds a private PPC4161-TK-H source-measure descent clause:

```text
S_src = S_matter[psi,g_obs,theta] + S_EM[A,g_obs] + S_binding[psi,A,g_obs] + int dB_impr + S_rest^top/zero.
```

The same observed metric/coframe and one source action define the Hilbert stress:

```text
T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu.
```

No independent source multipliers `w_A` are admitted inside PPC4161-TK-H, so:

```text
T_parent^H = Z_0 T_H,
Z_H = Z_0 exp(delta_ZH),
delta_ZH = 0.
```

Together with the 4168 topological kappa lock:

```text
D_A ln kappa_* = 0,
R_A^G = D_A ln kappa_* + D_A delta_ZH = 0.
```

This closes the local coupling multiplier residual inside the private packet. It is still not a public local-GR claim: Hilbert charge to worldtube/orbital measured mass readout, full PPN, numerical `G_N`, empirical pass rows, and global MTS adoption remain open.

The next local-GR source step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def descent_action_rows(packet_action: str) -> List[Dict[str, str]]:
    rows = [
        (
            "HSD4169_0_branch",
            "private branch definition",
            "PPC4161-TK-H := PPC4161-TK + H_src",
            "The Hilbert source-measure descent clause is adopted only in the private local packet.",
            "private_packet_adopted",
        ),
        (
            "HSD4169_1_source_action",
            "single source action",
            "S_src=S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding[psi,A,g_obs]+int dB_impr+S_rest^top/zero",
            "Matter, EM/Poynting, binding and exact improvements are assembled once before readout.",
            "private_packet_adopted",
        ),
        (
            "HSD4169_2_no_weights",
            "no independent source multipliers",
            "S_src != sum_A w_A S_A",
            "There is no surviving delta w_A object to generate delta_ZH inside this branch.",
            "source_weight_countermodel_excluded_inside_private_packet",
        ),
        (
            "HSD4169_3_same_metric",
            "same observed metric/coframe",
            "g_obs and theta are common for matter, EM, clocks and local EH source equation",
            "Frame/readout dependence cannot enter through separate source measures.",
            "private_packet_adopted",
        ),
        (
            "HSD4169_4_exact_rest",
            "improvement/rest-sector silence",
            "int dB_impr exact; S_rest^top/zero carries no local Hilbert source in collar",
            "Boundary/topological leftovers do not create a bulk local source multiplier.",
            "private_packet_adopted_with_boundary_guard",
        ),
        (
            "HSD4169_5_packet_sync",
            "packet integration addendum",
            str(PACKET_180_PATH),
            f"180 packet addendum action={packet_action}.",
            "formal_sync_done",
        ),
    ]
    return [
        {
            **common(),
            "descent_id": row[0],
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


def variational_proof_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "VP4169_0_definition",
            "Hilbert stress definition",
            "T_H^munu=-2/sqrt(-g_obs) delta S_src/delta g_obs_munu",
            "The source stress is defined by the same local action that couples to the EH equation.",
            "identity_inside_private_packet",
        ),
        (
            "VP4169_1_parent_source",
            "parent-to-Hilbert comparison",
            "T_parent^H=Z_H T_H+T_leak",
            "This is the only place a source-measure multiplier could hide.",
            "comparison_form",
        ),
        (
            "VP4169_2_descent",
            "single-action descent",
            "S_src descends through q to one Sbar_src[g_obs,psi,A,theta]",
            "Since the same action defines T_parent^H and T_H, only one common Z_0 remains.",
            "private_packet_proved",
        ),
        (
            "VP4169_3_ZH",
            "ZH split closure",
            "Z_H=Z_0 exp(delta_ZH), T_parent^H=Z_0 T_H, T_leak=0",
            "The physical source-measure leak is zero after the common normalization is separated.",
            "delta_ZH_zero_inside_private_packet",
        ),
        (
            "VP4169_4_residual",
            "coupling residual closure",
            "R_A^G=D_A ln kappa_* + D_A delta_ZH = 0 + 0 = 0",
            "4168 closes kappa drift; 4169 closes source-measure leak in the private packet.",
            "private_packet_local_coupling_residual_zero",
        ),
    ]
    return [
        {
            **common(),
            "proof_id": row[0],
            "step": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def channel_closure_rows() -> List[Dict[str, str]]:
    data = [
        ("time", "D_t delta_ZH", "no time-dependent source measure multiplier in S_src"),
        ("species", "Delta_AB delta_ZH", "no independent species weights w_A in S_src"),
        ("frame", "D_frame delta_ZH", "same observed metric/coframe defines all source stresses"),
        ("range", "D_lambda delta_ZH", "no range-labeled source coupling in local Hilbert action"),
        ("environment", "D_env delta_ZH", "compact local collar uses the same source action rather than environment-selected weights"),
        ("readout", "D_readout delta_ZH", "source action fixed before detector/orbital readout"),
    ]
    return [
        {
            **common(),
            "channel_id": f"ZH4169_{index}_{channel}",
            "channel": channel,
            "operator": operator,
            "closure_formula": f"{operator}=0",
            "reason": reason,
            "status": "closed_inside_PPC4161_TK_H_private_packet",
            "fallback_if_branch_rejected": f"restore bound row |{operator}|<=B_{channel}",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for index, (channel, operator, reason) in enumerate(data)
    ]


def remaining_gates_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RG4169_0_worldtube_mass",
            "Hilbert current to worldtube mass",
            "M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total)",
            "not_closed",
            "The source multiplier is closed, but the measured/orbital mass readout still needs Pi_M/H_tau glue.",
        ),
        (
            "RG4169_1_charge_integrability",
            "Hamiltonian charge integrability",
            "delta H_tau=int_S(delta Q_tau-i_tau theta)",
            "not_closed",
            "Need fixed reference, integrable variation and same time generator.",
        ),
        (
            "RG4169_2_radial_closure",
            "exterior charge radial closure",
            "int_A(C_EH+C_extra+C_projector+C_boundary)=0",
            "not_closed",
            "Need exterior annulus no-flux/constraint closure for the measured source mass.",
        ),
        (
            "RG4169_3_full_PPN",
            "full PPN readout",
            "Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}",
            "guarded_not_public",
            "Coupling residual closure is not automatically a full PPN theorem.",
        ),
        (
            "RG4169_4_numerical_G",
            "Newton constant magnitude",
            "G_N=c^4 kappa_* Z_0/(8*pi)",
            "not_predicted",
            "The branch permits calibration but still does not derive the numerical value.",
        ),
        (
            "RG4169_5_global_adoption",
            "global MTS parent adoption",
            "PPC4161-TK-H subset != full MTS action",
            "not_closed",
            "The closure is private/local, not the whole field theory.",
        ),
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


def fallback_bound_rows() -> List[Dict[str, str]]:
    data = [
        ("time", "D_t delta_ZH", "|D_t delta_ZH|<=B_Gdot"),
        ("species", "Delta_AB delta_ZH", "|Delta_AB delta_ZH|<=B_WEP_AB"),
        ("frame", "D_frame delta_ZH", "|D_frame delta_ZH|<=B_PPN_alpha"),
        ("range", "D_lambda delta_ZH", "|D_lambda delta_ZH|<=B_alpha_lambda"),
        ("environment", "D_env delta_ZH", "|D_env delta_ZH|<=B_env"),
        ("readout", "D_readout delta_ZH", "|D_readout delta_ZH|<=B_readout"),
    ]
    return [
        {
            **common(),
            "fallback_id": f"FB4169_{index}_{channel}",
            "channel": channel,
            "operator": operator,
            "required_if_PPC4161_TK_H_rejected": bound,
            "source_path_or_status": "NOT_ACTIVE_IF_PRIVATE_DESCENT_ACCEPTED__MISSING_IF_REJECTED",
            "numeric_value": "MISSING_NUMERIC_INPUT_IF_REJECTED",
            "status": "fallback_only_branch_rejection_bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for index, (channel, operator, bound) in enumerate(data)
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "BD4169_0_descent",
            "route": "Hilbert_source_measure_descent",
            "result": "PPC4161-TK-H closes delta_ZH by using one Hilbert-descended source action for matter, EM/Poynting, binding and exact improvements.",
            "gate_state": "private_packet_pass_public_claim_false",
            "next_action": "Move to Hilbert current/worldtube/Hamiltonian mass readout glue rather than circling kappa or ZH multipliers.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4169_1_coupling",
            "route": "local_coupling_residual",
            "result": "Inside PPC4161-TK-H, R_A^G=D_A ln kappa_* + D_A delta_ZH=0.",
            "gate_state": "coupling_multiplier_closed_private_packet",
            "next_action": "Do not call public local-GR pass; mass readout, PPN and empirical gates remain.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4169_2_next",
            "route": "next_target",
            "result": NEXT_TARGET,
            "gate_state": "source_multiplier_closed_mass_charge_glue_open",
            "next_action": "Derive M_H^dress/W/H_tau/Pi_M equality to measured Newtonian source mass, or keep explicit residual rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4169_0_private_not_global",
            "rule": "PPC4161-TK-H is a private local packet extension, not global MTS corpus adoption.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4169_1_no_numeric_G",
            "rule": "delta_ZH=0 closes source-measure leakage but does not predict the numerical value of G_N.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4169_2_mass_readout_open",
            "rule": "Hilbert source stress closure does not by itself identify the measured/orbital source mass; Pi_M/H_tau/worldtube glue remains open.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4169_3_no_full_PPN_claim",
            "rule": "Coupling multiplier closure is not a full PPN theorem for gamma, beta, alpha_i, zeta_i or xi.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4169_4_branch_rejection_bounds",
            "rule": "If the Hilbert source descent clause is rejected, all six delta_ZH derivative-bound rows reactivate.",
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
            "PPC4161_TK_H_private_packet_adopted": "True",
            "global_MTS_adopted": "False",
            "single_Hilbert_source_action_adopted": "True",
            "independent_source_weights_allowed": "False",
            "EM_Poynting_in_Hilbert_source": "True",
            "delta_ZH_closed_private": "True",
            "R_A_G_closed_private": "True",
            "worldtube_mass_readout_glue_closed": "False",
            "full_PPN_closed": "False",
            "numeric_G_predicted": "False",
            "formal_185_written": "True",
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
            "why_next": "4169 closes the local coupling multiplier residual inside PPC4161-TK-H, but the Hilbert source current still has to be glued to the measured/worldtube Newtonian mass readout.",
            "route_A": "derive M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total) with fixed reference, integrable charge and exterior closure",
            "route_B": "if the glue is not derivable, retain explicit Pi_M/H_tau/worldtube residual rows and source-backed bounds",
            "fallback": "public local-GR claim remains blocked even though kappa and delta_ZH multipliers are closed inside the private packet",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4169_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4169_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4169_HILBERT_SOURCE_DESCENT_ACTION": SOURCE_DIR / "P8_Y5_R2FR_4169_HILBERT_SOURCE_DESCENT_ACTION.csv",
        "P8_Y5_R2FR_4169_VARIATIONAL_SOURCE_MEASURE_PROOF": SOURCE_DIR / "P8_Y5_R2FR_4169_VARIATIONAL_SOURCE_MEASURE_PROOF.csv",
        "P8_Y5_R2FR_4169_DELTA_ZH_CHANNEL_CLOSURE": SOURCE_DIR / "P8_Y5_R2FR_4169_DELTA_ZH_CHANNEL_CLOSURE.csv",
        "P8_Y5_R2FR_4169_REMAINING_MASS_READOUT_AND_PPN_GATES": SOURCE_DIR / "P8_Y5_R2FR_4169_REMAINING_MASS_READOUT_AND_PPN_GATES.csv",
        "P8_Y5_R2FR_4169_BOUND_FALLBACK_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4169_BOUND_FALLBACK_ROWS.csv",
        "P8_Y5_R2FR_4169_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4169_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4169_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4169_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4169_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4169_STATUS.csv",
        "P8_Y5_R2FR_4169_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4169_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4169 - Delta-ZH Source-Measure Vanishing Or First Real Bound Row

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4168 reduced the coupling residual to:

```text
R_A^G = D_A delta_ZH.
```

4169 takes the derivation route first and defines the private PPC4161-TK-H branch:

```text
PPC4161-TK-H := PPC4161-TK + H_src.
```

The source clause is:

```text
S_src = S_matter[psi,g_obs,theta]
      + S_EM[A,g_obs]
      + S_binding[psi,A,g_obs]
      + int dB_impr
      + S_rest^top/zero.
```

No independent species/source weights `w_A` are admitted.

## Variational Derivation
The same action defines the local Hilbert source:

```text
T_H^munu = -2/sqrt(-g_obs) delta S_src/delta g_obs_munu.
```

The parent-to-Hilbert source split was:

```text
T_parent^H = Z_H T_H + T_leak,
Z_H = Z_0 exp(delta_ZH).
```

But under `H_src`:

```text
T_parent^H = Z_0 T_H,
T_leak = 0,
delta_ZH = 0.
```

The EM/Poynting sector is included in `T_H`; it is not a separate source multiplier.

## Coupling Residual
Using the 4168 topological kappa lock:

```text
D_A ln kappa_* = 0
```

the private packet coupling residual becomes:

```text
R_A^G = D_A ln kappa_* + D_A delta_ZH = 0.
```

## Important Guard
This closes the local coupling multiplier leak only inside PPC4161-TK-H. It does not close:

- Hilbert source charge to worldtube/orbital measured mass;
- Pi_M/H_tau/readout glue;
- full PPN;
- numerical `G_N`;
- global MTS adoption.

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

    sources = parse_csv(outputs["P8_Y5_R2FR_4169_SOURCE_REGISTER"])
    add("VAL4169_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    descent = parse_csv(outputs["P8_Y5_R2FR_4169_HILBERT_SOURCE_DESCENT_ACTION"])
    descent_text = "\n".join(",".join(row.values()) for row in descent)
    add(
        "VAL4169_1_descent_action",
        "descent action adopts PPC4161-TK-H, single source action, no source weights, same metric and rest/improvement silence",
        all(token in descent_text for token in ["PPC4161-TK-H", "S_src=S_matter", "S_src != sum_A w_A S_A", "g_obs and theta", "S_rest^top/zero"])
        and all(row["private_packet_adopted"] == "True" and row["global_corpus_adopted"] == "False" for row in descent),
        descent_text,
    )

    proof = parse_csv(outputs["P8_Y5_R2FR_4169_VARIATIONAL_SOURCE_MEASURE_PROOF"])
    proof_text = "\n".join(",".join(row.values()) for row in proof)
    add(
        "VAL4169_2_variational_proof",
        "proof rows derive Hilbert stress, T_parent comparison, delta_ZH zero and R_A^G zero",
        all(token in proof_text for token in ["T_H^munu", "T_parent^H=Z_H T_H+T_leak", "Z_H=Z_0 exp(delta_ZH)", "R_A^G=D_A ln kappa_* + D_A delta_ZH = 0 + 0 = 0"]),
        proof_text,
    )

    channels = parse_csv(outputs["P8_Y5_R2FR_4169_DELTA_ZH_CHANNEL_CLOSURE"])
    channel_set = {row["channel"] for row in channels}
    add(
        "VAL4169_3_channels",
        "all six delta_ZH channels are closed inside PPC4161-TK-H and have fallback if branch rejected",
        channel_set == {"time", "species", "frame", "range", "environment", "readout"}
        and all(row["status"] == "closed_inside_PPC4161_TK_H_private_packet" for row in channels)
        and all("restore bound row" in row["fallback_if_branch_rejected"] for row in channels),
        str(channels),
    )

    gates = parse_csv(outputs["P8_Y5_R2FR_4169_REMAINING_MASS_READOUT_AND_PPN_GATES"])
    gate_text = "\n".join(",".join(row.values()) for row in gates)
    add(
        "VAL4169_4_remaining_gates",
        "remaining gates explicitly include worldtube mass, H_tau charge, radial closure, PPN, numerical G and global adoption",
        all(token in gate_text for token in ["M_H^dress", "delta H_tau", "int_A", "Delta_PPN", "G_N=c^4 kappa_* Z_0/(8*pi)", "PPC4161-TK-H subset"]),
        gate_text,
    )

    fallbacks = parse_csv(outputs["P8_Y5_R2FR_4169_BOUND_FALLBACK_ROWS"])
    fallback_channels = {row["channel"] for row in fallbacks}
    add(
        "VAL4169_5_fallbacks",
        "fallback bound rows remain nonclaim and activate only if PPC4161-TK-H is rejected",
        fallback_channels == {"time", "species", "frame", "range", "environment", "readout"}
        and all(row["status"] == "fallback_only_branch_rejection_bound" for row in fallbacks)
        and all(row["valid_for_claim"] == "False" for row in fallbacks),
        str(fallbacks),
    )

    decisions = parse_csv(outputs["P8_Y5_R2FR_4169_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add(
        "VAL4169_6_decision",
        "branch decision moves from source multipliers to mass-readout glue",
        all(token in decision_text for token in ["Hilbert_source_measure_descent", "R_A^G=D_A ln kappa_* + D_A delta_ZH=0", NEXT_TARGET]),
        decision_text,
    )

    firewall = parse_csv(outputs["P8_Y5_R2FR_4169_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add(
        "VAL4169_7_firewall",
        "firewall blocks global, numerical-G, mass-readout, full-PPN and branch-rejection overclaims",
        all(token in firewall_text for token in ["private local packet", "numerical value of G_N", "Pi_M/H_tau/worldtube", "full PPN", "six delta_ZH"]),
        firewall_text,
    )

    formal_text = read_text(FORMAL_185_PATH)
    add(
        "VAL4169_8_formal_185",
        "formal 185 bridge exists and records source descent, delta_ZH closure, residual zero and next target",
        FORMAL_185_PATH.exists()
        and all(token in formal_text for token in ["PPC4161_HILBERT_SOURCE_MEASURE_DESCENT_DELTA_ZH_CLOSURE", "S_src = S_matter", "delta_ZH = 0", "R_A^G = D_A ln G_eff", NEXT_TARGET]),
        "formal 185 checked",
    )

    packet_text = read_text(PACKET_180_PATH)
    add(
        "VAL4169_9_packet_180",
        "packet 180 contains PPC4161-TK-H Hilbert source descent addendum",
        all(token in packet_text for token in [PACKET_MARKER, "S_src = S_matter[psi,g_obs,theta]", "T_parent^H = Z_0 T_H", "delta_ZH = 0", "R_A^G = D_A ln kappa_* + D_A delta_ZH = 0"]),
        "packet 180 checked",
    )

    claims = parse_csv(CLAIMS_PATH)
    l010 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add(
        "VAL4169_10_claim_row",
        "claims register contains one L-010 private source descent nonclaim row",
        len(l010) == 1 and l010[0].get("status") == "private_packet_source_descent_nonclaim_public_claim_false" and "public_claim=false" in l010[0].get("current_evidence", ""),
        str(l010),
    )

    spine_text = read_text(SPINE_PATH)
    add(
        "VAL4169_11_spine",
        "spine contains 4169 marker, claim row, source descent, delta_ZH zero and next target",
        all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "S_src = S_matter", "delta_ZH = 0", "R_A^G = D_A ln kappa_* + D_A delta_ZH = 0", NEXT_TARGET]),
        "spine checked",
    )

    status = parse_csv(outputs["P8_Y5_R2FR_4169_STATUS"])
    add(
        "VAL4169_12_status",
        "status records private source descent, delta_ZH closure, R_A^G closure, and remaining gates open",
        len(status) == 1
        and status[0]["PPC4161_TK_H_private_packet_adopted"] == "True"
        and status[0]["single_Hilbert_source_action_adopted"] == "True"
        and status[0]["EM_Poynting_in_Hilbert_source"] == "True"
        and status[0]["delta_ZH_closed_private"] == "True"
        and status[0]["R_A_G_closed_private"] == "True"
        and status[0]["worldtube_mass_readout_glue_closed"] == "False"
        and status[0]["full_PPN_closed"] == "False"
        and status[0]["next_target"] == NEXT_TARGET,
        str(status),
    )

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4169_NEXT_TARGET"])
    add(
        "VAL4169_13_next",
        "next target moves to Hilbert charge/worldtube measured mass glue",
        len(next_loaded) == 1
        and next_loaded[0]["next_target"] == NEXT_TARGET
        and "M_H^dress" in "\n".join(next_loaded[0].values())
        and "Pi_M/H_tau/worldtube" in "\n".join(next_loaded[0].values()),
        str(next_loaded),
    )

    doc_text = read_text(DOC_PATH)
    add(
        "VAL4169_14_doc",
        "checkpoint doc records move, derivation, coupling residual closure and guard",
        all(token in doc_text for token in ["PPC4161-TK-H := PPC4161-TK + H_src", "T_parent^H = Z_0 T_H", "delta_ZH = 0", "R_A^G = D_A ln kappa_* + D_A delta_ZH = 0", NEXT_TARGET]),
        "doc tokens checked",
    )

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4169_15_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

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
    add("VAL4169_16_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_185()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4169_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_HILBERT_SOURCE_DESCENT_ACTION"], descent_action_rows(packet_action))
    write_csv(outputs["P8_Y5_R2FR_4169_VARIATIONAL_SOURCE_MEASURE_PROOF"], variational_proof_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_DELTA_ZH_CHANNEL_CLOSURE"], channel_closure_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_REMAINING_MASS_READOUT_AND_PPN_GATES"], remaining_gates_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_BOUND_FALLBACK_ROWS"], fallback_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4169_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4169_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4169_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_185_PATH}")
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
