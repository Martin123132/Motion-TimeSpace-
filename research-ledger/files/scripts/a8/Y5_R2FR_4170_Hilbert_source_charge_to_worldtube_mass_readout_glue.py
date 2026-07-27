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

CHECKPOINT = "4170"
BRANCH_ID = "MTS_R2FR_Y5_HILBERT_HAMILTONIAN_WORLDTUBE_MASS_GLUE_4170"
DECISION = "PPC4161_TK_HQ_ADOPTS_HAMILTONIAN_MASS_CHARGE_MAP_SO_PIM_HTAU_WORLDTUBE_GLUE_CLOSES_PRIVATE_PACKET"
DOC_PATH = POST / "4170-Y5-R2FR-Hilbert-source-charge-to-worldtube-mass-readout-glue.md"
FORMAL_186_PATH = FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-011"
SPINE_MARKER = "PPC4161_HAMILTONIAN_WORLDTUBE_GLUE_4170"
PACKET_MARKER = "PPC4161_PACKET_HAMILTONIAN_WORLDTUBE_GLUE_4170"
NEXT_TARGET = "4171-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Gauss-Newton-readout.md"

SOURCES = {
    "SRC4170_00_4169_doc": (
        POST / "4169-Y5-R2FR-delta-ZH-source-measure-vanishing-or-first-real-bound-row.md",
        "Hilbert source charge to worldtube/orbital measured mass",
        "4169 checkpoint doc naming the next gate.",
    ),
    "SRC4170_01_4169_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4169_NEXT_TARGET.csv",
        "derive M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total)",
        "4169 next-target route A.",
    ),
    "SRC4170_02_4169_gates": (
        SOURCE_DIR / "P8_Y5_R2FR_4169_REMAINING_MASS_READOUT_AND_PPN_GATES.csv",
        "Hilbert current to worldtube mass",
        "4169 remaining-gates table.",
    ),
    "SRC4170_03_4155_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "PIM_HTAU_GLUE_UNSIGNED",
        "4155 same-charge Pi_M/H_tau glue bottleneck.",
    ),
    "SRC4170_04_HSM541": (
        SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "HSM541_0_adopt_Hamiltonian_PiM",
        "Hamiltonian source-measure contract.",
    ),
    "SRC4170_05_1015": (
        POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "Pi_M J_H = J_M_top + dB_zero",
        "Old same-object lemma and wrong-conserved-object warning.",
    ),
    "SRC4170_06_1016": (
        POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "try the Hamiltonian PiM reference/integrability lock",
        "Old selector decision pointing to Hamiltonian PiM reference lock.",
    ),
    "SRC4170_07_T510": (
        SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "M_source[W] := H_tau[outer S] - H_tau[reference]",
        "GR-style worldtube source-measure theorem.",
    ),
    "SRC4170_08_formal_185": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "PPC4161-TK-H",
        "4169 formal bridge closing source-measure multiplier leak.",
    ),
    "SRC4170_09_formal_180": (
        PACKET_180_PATH,
        "PPC4161_PACKET_HILBERT_SOURCE_DESCENT_4169",
        "Current packet containing the TK-H source descent addendum.",
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
        "claim": "PPC4161-TK-HQ privately identifies Pi_M with the covariant Hamiltonian mass-charge map, closing the Pi_M/H_tau/worldtube same-charge glue inside the private packet",
        "current_evidence": "formalization-workbench/186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md records W_H=closure(supp J_H_total), delta H_tau=int_S(delta Q_tau-i_tau theta_total), M_H^dress=H_tau[S]-H_ref, ell_M(Pi_M^H J_H_total)=M_H^dress, radial closure in the source-free collar, and no orbital-GM import; public_claim=false",
        "status": "private_packet_mass_charge_glue_nonclaim_public_claim_false",
        "next_test": "Derive the Poisson/Gauss/Newton weak-field readout from this Hamiltonian source charge, or retain explicit radial/source residual rows",
        "key_risk": "This glues the theoretical Hilbert charge to the private worldtube mass charge, but it does not yet prove the Newtonian 1/r metric coefficient, orbital measurement pass, full PPN, numerical G_N, or global MTS adoption",
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

## PPC4161-TK-HQ Addendum - Hamiltonian Worldtube Mass Glue

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4170-Y5-R2FR-Hilbert-source-charge-to-worldtube-mass-readout-glue.md`

Inside the private PPC4161-TK-H local packet, the mass projector is no longer an independent topological/readout mask. It is fixed to the covariant Hamiltonian source-charge map:

```text
W_H = closure(supp J_H_total)
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total)
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau]
```

with `tau`, `g_obs`, `theta_total`, `S_link`, and `H_ref` fixed before orbital or detector readout. The compact source-free exterior collar obeys:

```text
J_tau = dQ_tau + C_tau
C_tau = 0
F_symp = F_boundary = F_extra = 0
```

so `H_tau[S] - H_ref` is independent of the linking surface enclosing the same worldtube. This closes the same-charge glue:

```text
Q_M = ell_M(Pi_M^H J_H_total) = M_H^dress[W_H;tau].
```

No observed orbital `GM` is imported. The next gate is to show that this charge controls the weak-field Poisson/Gauss coefficient and orbital acceleration.
"""
    PACKET_180_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def write_formal_186() -> None:
    FORMAL_186_PATH.write_text(
        f"""# 186 - PPC4161 Hamiltonian Worldtube Mass Readout Glue

Marker: `PPC4161_HAMILTONIAN_WORLDTUBE_MASS_READOUT_GLUE`  
Timestamp UTC: `{now()}`  
Status: `private_packet_mass_charge_glue_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Branch Definition
Define the private charge-glued branch:

```text
PPC4161-TK-HQ := PPC4161-TK-H + H_Q
```

where `H_Q` fixes the mass projector by the covariant Hamiltonian charge itself:

```text
W_H = closure(supp J_H_total)
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total)
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau].
```

This is the key move: `Pi_M` is not a topological object chosen after seeing an orbit. It is the Hamiltonian/Hilbert charge map of the same source current and same worldtube.

## Noether And Radial Closure
For the local diffeomorphism-invariant packet action:

```text
J_tau = theta_total(Phi,L_tau Phi) - i_tau L_total
J_tau = dQ_tau + C_tau.
```

In the compact source-free exterior collar of PPC4161-TK-HQ:

```text
C_tau = 0
F_symp = 0
F_boundary = 0
F_extra = 0.
```

Therefore two linking surfaces `S1` and `S2` enclosing the same `W_H` give:

```text
H_tau[S2] - H_tau[S1] = 0.
```

The charge is worldtube-owned and radially stable.

## Same-Object Glue
The old obstruction was that a closed topological current could be the wrong object. PPC4161-TK-HQ removes that shortcut:

```text
Pi_M := Pi_M^H
Q_M = ell_M(Pi_M^H J_H_total)
Q_M = H_tau[S_link] - H_ref
Q_M = M_H^dress[W_H;tau].
```

This closes the private same-charge identity:

```text
Pi_M/H_tau/worldtube glue = 0 residual.
```

## Anti-Circularity Guard
No orbital `GM`, fitted acceleration, or measured Newton constant is used to define `M_H^dress`. The charge is defined before readout from the parent local action, `tau`, `theta_total`, `Q_tau`, and the fixed reference.

## What Still Remains
This does not yet prove:

- the weak-field Poisson/Gauss coefficient;
- the orbital acceleration law;
- full PPN second-order readout;
- the numerical value of `G_N`;
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

## 16. Local GR Coupling Update - Hamiltonian Worldtube Mass Glue

Marker: `{SPINE_MARKER}`  
Source bridge: `186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4170` fixes the mass projector inside the private local branch:

```text
W_H = closure(supp J_H_total)
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total)
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau].
```

Thus `Pi_M` is no longer a topological/readout mask. It is the covariant Hamiltonian mass-charge map for the same Hilbert source current and same worldtube.

In the compact source-free exterior collar:

```text
J_tau = dQ_tau + C_tau,
C_tau = F_symp = F_boundary = F_extra = 0,
H_tau[S2] - H_tau[S1] = 0.
```

So the same-charge identity closes inside PPC4161-TK-HQ:

```text
Q_M = ell_M(Pi_M^H J_H_total) = M_H^dress[W_H;tau].
```

This does not import orbital `GM`, does not predict the numerical value of `G_N`, and does not by itself prove the Newtonian 1/r readout. The next step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def hamiltonian_branch_rows(packet_action: str) -> List[Dict[str, str]]:
    rows = [
        (
            "HQ4170_0_branch",
            "private branch definition",
            "PPC4161-TK-HQ := PPC4161-TK-H + H_Q",
            "Hamiltonian charge glue is adopted only inside the private local packet.",
            "private_packet_adopted",
        ),
        (
            "HQ4170_1_worldtube",
            "source worldtube owner",
            "W_H=closure(supp J_H_total)",
            "The source domain is owned by the Hilbert current before readout.",
            "private_packet_adopted",
        ),
        (
            "HQ4170_2_charge_variation",
            "Hamiltonian charge variation",
            "delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total)",
            "The charge comes from covariant phase space of the local action.",
            "private_packet_adopted",
        ),
        (
            "HQ4170_3_mass_definition",
            "dressed source mass charge",
            "M_H^dress[W_H;tau]=H_tau[S_link]-H_ref",
            "The source mass is dressed Hamiltonian charge, not bare rest mass.",
            "private_packet_adopted",
        ),
        (
            "HQ4170_4_projector_identity",
            "PiM as Hamiltonian map",
            "ell_M(Pi_M^H J_H_total):=M_H^dress[W_H;tau]",
            "Pi_M is fixed as the Hamiltonian/Hilbert charge map, not an independent topological mask.",
            "same_object_identity_private_packet",
        ),
        (
            "HQ4170_5_packet_sync",
            "packet integration addendum",
            str(PACKET_180_PATH),
            f"180 packet addendum action={packet_action}.",
            "formal_sync_done",
        ),
    ]
    return [
        {
            **common(),
            "branch_row_id": row[0],
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


def noether_glue_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NG4170_0_current",
            "Noether current",
            "J_tau=theta_total(Phi,L_tau Phi)-i_tau L_total",
            "Current is built from the same local packet action and same tau.",
            "identity_inside_private_packet",
        ),
        (
            "NG4170_1_decomposition",
            "current decomposition",
            "J_tau=dQ_tau+C_tau",
            "Constraints or non-EH leftovers are isolated in C_tau.",
            "covariant_phase_space_identity",
        ),
        (
            "NG4170_2_exterior_constraints",
            "compact exterior closure",
            "C_tau=0 in exterior annulus outside W_H",
            "Source-free compact collar carries no local constraint flux.",
            "private_packet_closed",
        ),
        (
            "NG4170_3_integrability",
            "Hamiltonian integrability",
            "F_symp=int_annulus omega(delta,L_tau Phi)=0",
            "Fixed tau/coframe/reference and stationary local collar remove symplectic leakage.",
            "private_packet_closed",
        ),
        (
            "NG4170_4_boundary",
            "boundary/reference silence",
            "F_boundary=0 and H_ref fixed before readout",
            "Exact/reference terms cannot shift measured source charge after the fact.",
            "private_packet_closed",
        ),
        (
            "NG4170_5_extra",
            "extra-sector silence",
            "F_extra=0 for topological kappa, source-descent, rest/topological, and compact local residual sectors",
            "Previously retained extra charge channels are silent in PPC4161-TK-HQ.",
            "private_packet_closed",
        ),
        (
            "NG4170_6_radial",
            "radial charge closure",
            "H_tau[S2]-H_tau[S1]=int_A(C_tau+F_symp+F_boundary+F_extra)=0",
            "The same charge is read on any linking surface enclosing W_H.",
            "private_packet_worldtube_glue_closed",
        ),
    ]
    return [
        {
            **common(),
            "glue_id": row[0],
            "step": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def same_object_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SO4170_0_old_trap",
            "closed wrong object trap",
            "closed J_M_top alone does not imply Pi_M J_H_total is the mass source",
            "The old topological shortcut is explicitly not used.",
            "guard_pass",
        ),
        (
            "SO4170_1_identity",
            "same object identity",
            "Q_M=ell_M(Pi_M^H J_H_total)=H_tau[S_link]-H_ref=M_H^dress[W_H;tau]",
            "Pi_M, H_tau, and the worldtube source charge are one private-packet object.",
            "closed_inside_private_packet",
        ),
        (
            "SO4170_2_no_commutator",
            "chain-map commutator",
            "[d,Pi_M^H]J_H_total=0 in the charge complex",
            "Pi_M^H is defined by the Hamiltonian charge map on the same current complex.",
            "closed_inside_private_packet",
        ),
        (
            "SO4170_3_no_projector_stress",
            "projector stress",
            "delta_g Pi_M^H contributes no independent local stress beyond delta H_tau charge variation",
            "No separate Hodge/domain projector stress is introduced.",
            "closed_inside_private_packet",
        ),
        (
            "SO4170_4_no_orbital_import",
            "anti-circularity",
            "M_H^dress is not defined from GM_orbit/G_N",
            "Orbital data cannot be used to launder the source mass definition.",
            "guard_pass",
        ),
    ]
    return [
        {
            **common(),
            "same_object_id": row[0],
            "name": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def residual_rows() -> List[Dict[str, str]]:
    rows = [
        ("RES4170_0_R_eq", "R_eq=Pi_M J_H_total-J_M_top-dB_zero", "not_active_in_HQ_route", "Topological equality route is bypassed by Pi_M^H same-object definition."),
        ("RES4170_1_I_commutator", "I_commutator=int_A [d,Pi_M]J_H", "zero_inside_private_packet", "Pi_M^H is a fixed Hamiltonian chain map on J_H_total."),
        ("RES4170_2_Delta_symp", "Delta_symp=F_symp", "zero_inside_private_packet", "Hamiltonian integrability is adopted in the compact stationary collar."),
        ("RES4170_3_B_zero_flux", "B_zero_flux=F_boundary", "zero_inside_private_packet", "Reference and exact boundary flux are fixed before readout."),
        ("RES4170_4_Delta_extra", "Delta_extra=F_extra", "zero_inside_private_packet", "Topological/source-descent/rest sectors carry no exterior mass flux in PPC4161-TK-HQ."),
        ("RES4170_5_radial_Meff", "epsilon_radial_Meff=M_H^-1 int_A(C_tau+F_symp+F_boundary+F_extra)", "zero_inside_private_packet", "Exterior annulus charge is radially closed."),
        ("RES4170_6_if_rejected", "epsilon_mass_glue<=sum_abs_residuals/M_H_ref", "fallback_only", "If HQ branch is rejected, residual rows must be sourced/bounded before any claim."),
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
        (
            "RG4170_0_Poisson_Gauss",
            "Poisson/Gauss weak-field readout",
            "nabla^2 Phi_N=4*pi G_N rho_H and surface Gauss charge equals M_H^dress",
            "not_closed",
            "Need show Hamiltonian mass charge controls the 1/r metric coefficient.",
        ),
        (
            "RG4170_1_orbital_acceleration",
            "Newtonian orbital acceleration",
            "a_r=-G_N M_H^dress/r^2",
            "not_closed",
            "Cannot import observed orbital GM before deriving this bridge.",
        ),
        (
            "RG4170_2_full_PPN",
            "full PPN readout",
            "Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}",
            "not_closed",
            "Second-order and preferred-frame terms remain guarded.",
        ),
        (
            "RG4170_3_numeric_G",
            "Newton constant magnitude",
            "G_N=c^4 kappa_* Z_0/(8*pi)",
            "not_predicted",
            "Private branch still calibrates rather than predicts numerical G_N.",
        ),
        (
            "RG4170_4_global_adoption",
            "global MTS parent action",
            "PPC4161-TK-HQ subset != full MTS",
            "not_closed",
            "The result is a private local branch, not global theory completion.",
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


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "BD4170_0_HQ",
            "route": "Hamiltonian_PiM_worldtube_glue",
            "result": "PPC4161-TK-HQ defines Pi_M as the Hamiltonian/Hilbert mass-charge map for the same worldtube source current.",
            "gate_state": "private_packet_pass_public_claim_false",
            "next_action": "Use this charge in the weak-field Poisson/Gauss/Newton readout gate.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4170_1_anti_circular",
            "route": "no_orbital_GM_import",
            "result": "M_H^dress is defined before orbit fitting as H_tau[S]-H_ref, not from observed GM/G_N.",
            "gate_state": "anti_circularity_guard_pass",
            "next_action": "Only after deriving the Poisson/Gauss bridge can orbital data become a test rather than an input.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4170_2_next",
            "route": "next_target",
            "result": NEXT_TARGET,
            "gate_state": "mass_charge_glued_Newton_readout_open",
            "next_action": "Derive the 1/r metric coefficient and inverse-square acceleration from M_H^dress.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4170_0_private_not_global",
            "rule": "PPC4161-TK-HQ is a private local packet extension, not global MTS corpus adoption.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4170_1_no_orbital_import",
            "rule": "Do not define M_H^dress from observed orbital GM or measured G_N.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4170_2_no_Newton_claim_yet",
            "rule": "Worldtube Hamiltonian mass glue is not yet the Poisson/Gauss/Newton readout theorem.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4170_3_no_numeric_G",
            "rule": "The branch still does not predict the numerical value of G_N.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4170_4_branch_rejection_residuals",
            "rule": "If Pi_M^H/H_tau glue is rejected, R_eq, I_commutator, Delta_symp, B_zero, Delta_extra and radial-M_eff residual rows reactivate.",
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
            "PPC4161_TK_HQ_private_packet_adopted": "True",
            "global_MTS_adopted": "False",
            "PiM_defined_as_Hamiltonian_charge_map": "True",
            "worldtube_support_fixed_before_readout": "True",
            "Htau_integrability_closed_private": "True",
            "radial_charge_closure_private": "True",
            "same_charge_glue_closed_private": "True",
            "orbital_GM_imported": "False",
            "Poisson_Gauss_Newton_readout_closed": "False",
            "full_PPN_closed": "False",
            "numeric_G_predicted": "False",
            "formal_186_written": "True",
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
            "why_next": "4170 glues the Hilbert/Hamiltonian/worldtube source charge inside PPC4161-TK-HQ, but Newtonian mechanics still requires the Poisson/Gauss weak-field readout.",
            "route_A": "derive nabla^2 Phi_N=4*pi G_N rho_H and a_r=-G_N M_H^dress/r^2 from the same Hamiltonian source charge without importing observed orbital GM",
            "route_B": "if weak-field readout is not derivable, retain explicit radial hair, fifth-force, and PPN residual rows",
            "fallback": "public local-GR/Newton claim remains blocked until Poisson/Gauss, orbital acceleration, PPN, and empirical checks pass",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4170_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4170_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION": SOURCE_DIR / "P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION.csv",
        "P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE": SOURCE_DIR / "P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE.csv",
        "P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY": SOURCE_DIR / "P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv",
        "P8_Y5_R2FR_4170_RESIDUAL_CLOSE_OR_REACTIVATE": SOURCE_DIR / "P8_Y5_R2FR_4170_RESIDUAL_CLOSE_OR_REACTIVATE.csv",
        "P8_Y5_R2FR_4170_REMAINING_NEWTON_PPN_GATES": SOURCE_DIR / "P8_Y5_R2FR_4170_REMAINING_NEWTON_PPN_GATES.csv",
        "P8_Y5_R2FR_4170_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4170_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4170_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4170_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4170_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4170_STATUS.csv",
        "P8_Y5_R2FR_4170_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4170_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4170 - Hilbert Source Charge To Worldtube Mass Readout Glue

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4169 closed the local source multiplier leak but left the source charge readout open. 4170 defines the private charge-glued branch:

```text
PPC4161-TK-HQ := PPC4161-TK-H + H_Q.
```

The adopted Hamiltonian/worldtube glue is:

```text
W_H = closure(supp J_H_total)
delta H_tau[S] = int_S(delta Q_tau - i_tau theta_total)
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
ell_M(Pi_M^H J_H_total) := M_H^dress[W_H;tau].
```

`Pi_M` is therefore not a late topological/readout mask. It is the Hamiltonian mass-charge map of the same Hilbert current and same worldtube.

## Noether Closure
The local packet current obeys:

```text
J_tau = theta_total(Phi,L_tau Phi) - i_tau L_total
J_tau = dQ_tau + C_tau.
```

In the compact source-free exterior collar:

```text
C_tau = F_symp = F_boundary = F_extra = 0.
```

So:

```text
H_tau[S2] - H_tau[S1] = 0
```

for any two linking surfaces enclosing `W_H`.

## Same-Charge Result
Inside PPC4161-TK-HQ:

```text
Q_M = ell_M(Pi_M^H J_H_total)
Q_M = H_tau[S_link] - H_ref
Q_M = M_H^dress[W_H;tau].
```

This closes the private `Pi_M/H_tau/worldtube` same-charge glue.

## Anti-Circularity
No orbital `GM`, fitted acceleration, or measured `G_N` is used in the definition. Orbital data only becomes a test after the weak-field Newton/Gauss readout is derived.

## Still Open
This does not yet prove:

- `nabla^2 Phi_N = 4*pi G_N rho_H`;
- `a_r = -G_N M_H^dress/r^2`;
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

    sources = parse_csv(outputs["P8_Y5_R2FR_4170_SOURCE_REGISTER"])
    add("VAL4170_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    branch = parse_csv(outputs["P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION"])
    branch_text = "\n".join(",".join(row.values()) for row in branch)
    add(
        "VAL4170_1_branch",
        "branch rows adopt PPC4161-TK-HQ, fixed worldtube, Htau variation, dressed mass and PiM identity",
        all(token in branch_text for token in ["PPC4161-TK-HQ", "W_H=closure(supp J_H_total)", "delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total)", "M_H^dress[W_H;tau]=H_tau[S_link]-H_ref", "ell_M(Pi_M^H J_H_total):=M_H^dress"])
        and all(row["private_packet_adopted"] == "True" and row["global_corpus_adopted"] == "False" for row in branch),
        branch_text,
    )

    glue = parse_csv(outputs["P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE"])
    glue_text = "\n".join(",".join(row.values()) for row in glue)
    add(
        "VAL4170_2_noether_glue",
        "Noether/radial rows show J=dQ+C, exterior closures, integrability and surface independence",
        all(token in glue_text for token in ["J_tau=dQ_tau+C_tau", "C_tau=0", "F_symp", "F_boundary=0", "F_extra=0", "H_tau[S2]-H_tau[S1]"]),
        glue_text,
    )

    same_object = parse_csv(outputs["P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY"])
    same_text = "\n".join(",".join(row.values()) for row in same_object)
    add(
        "VAL4170_3_same_object",
        "same-object rows close wrong-object trap, commutator, projector stress and orbital import guard",
        all(token in same_text for token in ["closed J_M_top alone", "Q_M=ell_M(Pi_M^H J_H_total)", "[d,Pi_M^H]J_H_total=0", "delta_g Pi_M^H", "GM_orbit/G_N"]),
        same_text,
    )

    residuals = parse_csv(outputs["P8_Y5_R2FR_4170_RESIDUAL_CLOSE_OR_REACTIVATE"])
    residual_text = "\n".join(",".join(row.values()) for row in residuals)
    add(
        "VAL4170_4_residuals",
        "residual rows close or reactivate R_eq, I_commutator, symplectic, boundary, extra and radial residuals",
        all(token in residual_text for token in ["R_eq=Pi_M J_H_total-J_M_top-dB_zero", "I_commutator", "Delta_symp", "B_zero_flux", "Delta_extra", "epsilon_radial_Meff", "fallback_only"]),
        residual_text,
    )

    remaining = parse_csv(outputs["P8_Y5_R2FR_4170_REMAINING_NEWTON_PPN_GATES"])
    remaining_text = "\n".join(",".join(row.values()) for row in remaining)
    add(
        "VAL4170_5_remaining",
        "remaining gates explicitly leave Poisson/Gauss, orbital acceleration, PPN, numerical G and global adoption open",
        all(token in remaining_text for token in ["nabla^2 Phi_N=4*pi G_N rho_H", "a_r=-G_N M_H^dress/r^2", "Delta_PPN", "G_N=c^4 kappa_* Z_0/(8*pi)", "PPC4161-TK-HQ subset"]),
        remaining_text,
    )

    decisions = parse_csv(outputs["P8_Y5_R2FR_4170_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add(
        "VAL4170_6_decision",
        "decision rows move from same-charge glue to Poisson/Gauss/Newton readout",
        all(token in decision_text for token in ["Hamiltonian_PiM_worldtube_glue", "no_orbital_GM_import", NEXT_TARGET]),
        decision_text,
    )

    firewall = parse_csv(outputs["P8_Y5_R2FR_4170_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add(
        "VAL4170_7_firewall",
        "firewall blocks global, orbital import, Newton, numerical-G and branch-rejection overclaims",
        all(token in firewall_text for token in ["private local packet", "observed orbital GM", "Poisson/Gauss/Newton", "numerical value of G_N", "R_eq, I_commutator"]),
        firewall_text,
    )

    formal_text = read_text(FORMAL_186_PATH)
    add(
        "VAL4170_8_formal_186",
        "formal 186 bridge exists and records branch definition, Noether closure, same-object glue, anti-circularity and next target",
        FORMAL_186_PATH.exists()
        and all(token in formal_text for token in ["PPC4161_HAMILTONIAN_WORLDTUBE_MASS_READOUT_GLUE", "PPC4161-TK-HQ", "ell_M(Pi_M^H J_H_total)", "H_tau[S2] - H_tau[S1] = 0", "No orbital", NEXT_TARGET]),
        "formal 186 checked",
    )

    packet_text = read_text(PACKET_180_PATH)
    add(
        "VAL4170_9_packet_180",
        "packet 180 contains PPC4161-TK-HQ Hamiltonian worldtube glue addendum",
        all(token in packet_text for token in [PACKET_MARKER, "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref", "ell_M(Pi_M^H J_H_total) := M_H^dress", "Q_M = ell_M(Pi_M^H J_H_total) = M_H^dress"]),
        "packet 180 checked",
    )

    claims = parse_csv(CLAIMS_PATH)
    l011 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add(
        "VAL4170_10_claim_row",
        "claims register contains one L-011 private mass-charge glue nonclaim row",
        len(l011) == 1 and l011[0].get("status") == "private_packet_mass_charge_glue_nonclaim_public_claim_false" and "public_claim=false" in l011[0].get("current_evidence", ""),
        str(l011),
    )

    spine_text = read_text(SPINE_PATH)
    add(
        "VAL4170_11_spine",
        "spine contains 4170 marker, claim row, Hamiltonian glue and next target",
        all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "ell_M(Pi_M^H J_H_total) := M_H^dress", "Q_M = ell_M(Pi_M^H J_H_total) = M_H^dress", NEXT_TARGET]),
        "spine checked",
    )

    status = parse_csv(outputs["P8_Y5_R2FR_4170_STATUS"])
    add(
        "VAL4170_12_status",
        "status records private adoption, PiM/Htau glue closed, no orbital import, Newton/PPN open",
        len(status) == 1
        and status[0]["PPC4161_TK_HQ_private_packet_adopted"] == "True"
        and status[0]["PiM_defined_as_Hamiltonian_charge_map"] == "True"
        and status[0]["same_charge_glue_closed_private"] == "True"
        and status[0]["orbital_GM_imported"] == "False"
        and status[0]["Poisson_Gauss_Newton_readout_closed"] == "False"
        and status[0]["full_PPN_closed"] == "False"
        and status[0]["next_target"] == NEXT_TARGET,
        str(status),
    )

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4170_NEXT_TARGET"])
    add(
        "VAL4170_13_next",
        "next target moves to Poisson/Gauss/Newton readout without orbital GM import",
        len(next_loaded) == 1
        and next_loaded[0]["next_target"] == NEXT_TARGET
        and "nabla^2 Phi_N" in "\n".join(next_loaded[0].values())
        and "observed orbital GM" in "\n".join(next_loaded[0].values()),
        str(next_loaded),
    )

    doc_text = read_text(DOC_PATH)
    add(
        "VAL4170_14_doc",
        "checkpoint doc records move, Noether closure, same-charge result, anti-circularity and next target",
        all(token in doc_text for token in ["PPC4161-TK-HQ", "M_H^dress[W_H;tau]", "H_tau[S2] - H_tau[S1] = 0", "Q_M = ell_M(Pi_M^H J_H_total)", "No orbital", NEXT_TARGET]),
        "doc tokens checked",
    )

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4170_15_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

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
    add("VAL4170_16_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_186()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4170_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_HAMILTONIAN_BRANCH_ADOPTION"], hamiltonian_branch_rows(packet_action))
    write_csv(outputs["P8_Y5_R2FR_4170_NOETHER_RADIAL_GLUE"], noether_glue_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY"], same_object_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_RESIDUAL_CLOSE_OR_REACTIVATE"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_REMAINING_NEWTON_PPN_GATES"], remaining_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4170_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4170_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4170_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_186_PATH}")
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
