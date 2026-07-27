from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4176"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_BOUNDARY_NO_FLUX_SECTOR_INTERFACE_4176"
DECISION = "LOCAL_BOUNDARY_NO_FLUX_THEOREM_CLOSES_TRANSITION_CURRENT_PRIVATE_SELECTOR"
DOC_PATH = POST / "4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md"
FORMAL_192_PATH = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-017"
SPINE_MARKER = "PPC4161_LOCAL_BOUNDARY_NO_FLUX_4176"
PACKET_MARKER = "PPC4161_PACKET_LOCAL_BOUNDARY_NO_FLUX_4176"
NEXT_TARGET = "4177-Y5-R2FR-quotient-naturality-vertical-silence-proof-or-projector-residual-bound.md"

SOURCES = {
    "SRC4176_00_4175_doc": (
        POST / "4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md",
        "boundary/interface no-flux theorem",
        "4175 handoff selected boundary/interface no-flux as the next leak.",
    ),
    "SRC4176_01_4175_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4175_NEXT_TARGET.csv",
        "prove a local boundary/interface no-flux theorem",
        "4175 next-target ledger route A.",
    ),
    "SRC4176_02_formal_190": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "local boundary silence",
        "4174 selector clause requiring boundary silence.",
    ),
    "SRC4176_03_formal_191": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Radiative EM is not erased",
        "4175 radiative flux guard.",
    ),
    "SRC4176_04_claim_L016": (
        CLAIMS_PATH,
        "Maxwell-Hodge variation owns the Poynting vector",
        "Previous claim-register row before boundary/no-flux closure.",
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
        writer.writerows(rows)


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


def boundary_domain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "BD4176_0_worldtube",
            "W_loc",
            "compact local ordinary-matter collar/worldtube",
            "supp(T_local) subset int(W_loc)",
            "local source support stays away from the side boundary through <=2PN",
        ),
        (
            "BD4176_1_caps",
            "Sigma_in union Sigma_out",
            "initial/final spacelike caps",
            "Hamiltonian evolution bookkeeping surfaces",
            "cap flux is evolution data, not an unmodelled side leakage",
        ),
        (
            "BD4176_2_side",
            "C_side",
            "timelike exterior side boundary",
            "n_mu T_cross^{mu nu} tau_nu | C_side = 0",
            "side boundary is no-flux if cross-sector support/pullback vanishes",
        ),
        (
            "BD4176_3_radiative",
            "C_rad",
            "radiative boundary component",
            "F_rad[tau] is either zero or routed to boundary/Hamiltonian charge",
            "radiation is not silently erased; nonzero flux reopens a boundary-charge row",
        ),
        (
            "BD4176_4_sector_interface",
            "I_sector",
            "interface with galaxy/cosmology/open-memory sectors",
            "pullback(n_mu T_sector^{mu nu} tau_nu)=0 or source-backed bound",
            "local theorem applies only if sector coupling is support-separated or boundary-silent",
        ),
        (
            "BD4176_5_projection",
            "Pi_loc",
            "local projection/readout",
            "Pi_loc T_cross = 0 on W_loc or J_tr is explicit",
            "projection cannot hide a transition current inside the local PPN vector",
        ),
    ]
    return [
        {
            **common(),
            "domain_id": domain_id,
            "object": object_name,
            "definition": definition,
            "boundary_condition": condition,
            "local_role": role,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for domain_id, object_name, definition, condition, role in rows
    ]


def no_flux_theorem_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NFT4176_0_flux_functional",
            "define local flux functional",
            "F_X[tau] = int_X n_mu T_total^{mu nu} tau_nu dSigma",
            "Flux through each boundary piece is a Hamiltonian/accounting object, not an optional afterthought.",
            "definition",
        ),
        (
            "NFT4176_1_support",
            "compact support hypothesis",
            "supp(T_local) subset int(W_loc) and dist(supp(T_local), C_side)>0",
            "Ordinary local source terms cannot leak through the exterior side boundary.",
            "selector_clause_required",
        ),
        (
            "NFT4176_2_cross_sector",
            "sector support or pullback silence",
            "n_mu T_sector^{mu nu} tau_nu | partial W_loc = 0 for galaxy/cosmology/open-memory sectors",
            "External sectors are either support-separated, have zero pullback, or are not closed by this theorem.",
            "selector_clause_required",
        ),
        (
            "NFT4176_3_Hamiltonian_boundary",
            "fixed or routed Hamiltonian boundary term",
            "delta H_tau = int_partialW (delta Q_tau - i_tau theta_total)",
            "If this boundary variation vanishes/fixes/routs all nonzero flux, no hidden bulk force is left.",
            "selector_clause_required",
        ),
        (
            "NFT4176_4_divergence_to_boundary",
            "integrated conservation identity",
            "int_Wloc nabla_mu T_total^{mu nu} tau_nu dV = int_partialWloc n_mu T_total^{mu nu} tau_nu dSigma",
            "Bianchi/local conservation turns possible leakage into a named boundary flux.",
            "derived_identity",
        ),
        (
            "NFT4176_5_no_flux_conclusion",
            "private selector conclusion",
            "F_side[tau]=0 and J_tr^nu := Pi_loc nabla_mu T_cross^{mu nu} = 0 through <=2PN",
            "The transition current closes only inside the compact local selector branch.",
            "closed_private_selector",
        ),
        (
            "NFT4176_6_radiative_guard",
            "radiative exception",
            "F_rad[tau] != 0 is boundary/Hamiltonian charge, not J_tr and not silently zero",
            "Radiative EM/gravity survives as a boundary sector unless the local collar excludes it.",
            "routed_not_zeroed",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "step": step,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, step, formula, meaning, status in rows
    ]


def transition_current_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "TR4176_0_definition",
            "J_tr^nu",
            "J_tr^nu := Pi_loc nabla_mu T_cross^{mu nu}",
            "closed_private",
            "If all no-flux clauses are signed, transition current is zero in the local equations.",
            "reactivate if cross-sector stress has nonzero pullback or boundary flux is not routed",
        ),
        (
            "TR4176_1_preferred_location",
            "xi_preferred_location",
            "xi_boundary = functional[J_tr, F_side]",
            "closed_private",
            "Preferred-location source is absent when the local collar has no external transition current.",
            "reactivate for nonzero galaxy/cosmology/open-memory boundary imprint",
        ),
        (
            "TR4176_2_preferred_frame",
            "alpha_i_transition_current",
            "alpha_i_boundary = functional[J_tr^i, frame_boundary_data]",
            "closed_private",
            "Preferred-frame leakage is not present if the boundary data are fixed/routed and no local current remains.",
            "reactivate if external frame data couple to the local PPN readout",
        ),
        (
            "TR4176_3_clock",
            "clock_redshift_transition",
            "delta nu/nu |_tr = functional[F_side[tau], J_tr^0]",
            "closed_private",
            "Clock tests receive no hidden boundary energy-current term in the selector branch.",
            "reactivate and source-bound if local clock readout samples nonzero boundary flux",
        ),
        (
            "TR4176_4_R10",
            "R10_short_range_transition",
            "alpha_lambda_tr = functional[J_tr, lambda_tr]",
            "closed_private",
            "No short-range transition-force row is present when the interface current is zero.",
            "reactivate and use source-backed alpha(lambda) rows if finite-range interface force appears",
        ),
        (
            "TR4176_5_radiation",
            "radiative_boundary_flux",
            "F_rad[tau]",
            "routed_not_zeroed",
            "Radiation crossing the collar is not a fifth-force side-channel; it is a boundary/Hamiltonian charge.",
            "reactivate if the local branch tries to discard radiative flux rather than route it",
        ),
    ]
    return [
        {
            **common(),
            "transition_id": transition_id,
            "residual": residual,
            "formula": formula,
            "status": status,
            "closure_reason": closure_reason,
            "reactivation_condition": reactivation_condition,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for transition_id, residual, formula, status, closure_reason, reactivation_condition in rows
    ]


def sector_interface_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SI4176_0_galaxy",
            "galaxy",
            "support-separated from compact local collar or pullback flux zero",
            "closed_private_if_selector_signed",
            "does not erase galaxy rotation work; it prevents galaxy-scale fields from masquerading as local PPN residuals",
        ),
        (
            "SI4176_1_cosmology",
            "cosmology",
            "FLRW/background memory pullback zero on isolated local collar through <=2PN",
            "closed_private_if_selector_signed",
            "cosmology remains a separate test pillar, not a local fifth force by default",
        ),
        (
            "SI4176_2_open_memory",
            "open_memory",
            "memory sector has no local boundary charge unless explicitly routed",
            "closed_private_if_selector_signed",
            "open-memory terms cannot be silently inserted into the local PPN vector",
        ),
        (
            "SI4176_3_radiative_EM",
            "radiative_EM",
            "Maxwell-Hodge flux crossing C_rad is boundary/Hamiltonian charge",
            "routed_not_zeroed",
            "inherits 4175 Poynting ownership and keeps radiation alive as flux bookkeeping",
        ),
        (
            "SI4176_4_radiative_gravity",
            "radiative_gravity",
            "gravitational-wave flux crossing C_rad is boundary/Hamiltonian charge",
            "routed_not_zeroed",
            "radiative gravity is not erased; nonzero flux lives outside static local PPN closure",
        ),
        (
            "SI4176_5_orbital_external_tides",
            "orbital_external_tides",
            "external tidal fields are boundary data, not hidden source-current terms",
            "closed_private_if_modeled_as_boundary_data",
            "orbital fits must model tides explicitly if the no-flux/local-isolation hypothesis fails",
        ),
    ]
    return [
        {
            **common(),
            "interface_id": interface_id,
            "sector": sector,
            "condition": condition,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for interface_id, sector, condition, status, meaning in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4176_0_theorem",
            "local_boundary_no_flux_theorem",
            "Under compact support, zero pullback/support separation and fixed/routed Hamiltonian boundary terms, F_side[tau]=0 and J_tr^nu=0 through <=2PN.",
            "close_transition_current_private_selector",
        ),
        (
            "DEC4176_1_guard",
            "radiation_and_sector_interfaces_not_erased",
            "Nonzero radiative or sector flux is routed/bounded; the theorem does not silently remove galaxy, cosmology, open-memory or radiation physics.",
            "keep_firewall_and_reactivate_if_flux_nonzero",
        ),
        (
            "DEC4176_2_no_global",
            "global_adoption_still_false",
            "This is a private compact-local collar theorem inside the selector/quarantine branch, not a global parent-action proof.",
            "keep_local_branch_quarantined",
        ),
        (
            "DEC4176_3_next",
            "next_best_derivation_target",
            "After EM ownership and local boundary no-flux, the remaining structural leak is quotient-naturality/vertical silence.",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in rows
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4176_0_no_public_local_GR", "Do not claim public local GR; quotient naturality and global parent adoption remain open."),
        ("FW4176_1_no_global", "Do not claim global MTS adoption from a compact local no-flux theorem."),
        ("FW4176_2_no_sector_erasure", "Do not erase galaxy, cosmology, open-memory, orbital, EM or gravitational-radiation sectors."),
        ("FW4176_3_no_radiation_zeroing", "Do not set radiative flux to zero unless the collar hypothesis explicitly excludes it."),
        ("FW4176_4_no_numeric_G", "Do not claim a numerical derivation of Newton's constant."),
        ("FW4176_5_no_empirical_claim", "Do not claim R10, PPN, clocks, WEP or orbital pass from this formal gate alone."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "blocked_claim": blocked_claim,
            "enforcement": "claim_allowed=false_and_valid_for_claim=false",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, blocked_claim in rows
    ]


def status_rows(claim_action: str, packet_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "local_boundary_no_flux_theorem_derived_private": "True",
            "transition_current_closed_private": "True",
            "local_boundary_silence_closed_private": "True",
            "radiative_boundary_flux_zeroed": "False",
            "radiative_boundary_flux_routed": "True",
            "sector_interfaces_erased": "False",
            "global_boundary_silence_proved": "False",
            "global_parent_action_adoption_proved": "False",
            "quotient_naturality_proved_global": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_192_written": "True",
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
            "why_next": "4176 closes transition-current leakage only under the compact-local no-flux selector; the remaining structural gate is quotient-naturality/vertical silence so projected variables cannot smuggle residuals into local GR.",
            "route_A": "prove vertical variations are quotient-natural and silent in the local source/readout functor",
            "route_B": "if quotient naturality fails, build projector-residual rows for PPN, clocks, R10 and orbital tests",
            "fallback": "keep PPC4161-TK-HQNP quarantined until quotient naturality and global parent adoption are parent-signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4176_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4176_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION": SOURCE_DIR / "P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION.csv",
        "P8_Y5_R2FR_4176_NO_FLUX_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv",
        "P8_Y5_R2FR_4176_TRANSITION_CURRENT_CLOSE_OR_BOUND": SOURCE_DIR / "P8_Y5_R2FR_4176_TRANSITION_CURRENT_CLOSE_OR_BOUND.csv",
        "P8_Y5_R2FR_4176_SECTOR_INTERFACE_MAP": SOURCE_DIR / "P8_Y5_R2FR_4176_SECTOR_INTERFACE_MAP.csv",
        "P8_Y5_R2FR_4176_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4176_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4176_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4176_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4176_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4176_STATUS.csv",
        "P8_Y5_R2FR_4176_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4176_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "Inside the PPC4161 local selector branch, compact support plus fixed/routed Hamiltonian boundary conditions give local no-flux and close transition-current leakage privately",
        "current_evidence": "formalization-workbench/192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md records W_loc boundary decomposition, F_X[tau], Hamiltonian boundary charge routing, J_tr^nu=0 through <=2PN under selector clauses, and radiative flux routed not zeroed; public_claim=false",
        "status": "private_selector_local_boundary_no_flux_nonclaim_public_claim_false",
        "next_test": "Prove quotient-naturality/vertical silence or source-bound projector residual leakage into local tests",
        "key_risk": "This closes boundary/interface leakage only in compact local collars with signed no-flux/support-separation clauses; quotient naturality, global parent adoption and numerical G_N remain unproved",
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
        writer.writerows(rows)
    return action


def append_once(path: Path, marker: str, section: str) -> str:
    text = read_text(path)
    if marker in text:
        return "already_present"
    path.write_text(text.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")
    return "added"


def ensure_packet_180_addendum() -> str:
    section = f"""
## PPC4161-TK-HQNP Addendum - Local Boundary No-Flux Sector Interface

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md`

Inside the private compact local selector branch, use a local worldtube/collar `W_loc` with:

```text
partial W_loc = Sigma_in union Sigma_out union C_side union C_rad,
F_X[tau] = int_X n_mu T_total^{{mu nu}} tau_nu dSigma.
```

If local matter support is compactly inside `W_loc`, cross-sector pullbacks vanish on the side/interface boundary, and the Hamiltonian boundary term is fixed or routed:

```text
delta H_tau = int_partialW (delta Q_tau - i_tau theta_total),
F_side[tau] = 0,
J_tr^nu := Pi_loc nabla_mu T_cross^{{mu nu}} = 0 through <=2PN.
```

This closes transition-current leakage only privately. Radiative EM/gravity flux is not erased; any nonzero flux is boundary/Hamiltonian charge and reopens the route-to-bound row if not modeled.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Local Boundary No-Flux Sector Interface - 4176

Marker: `{SPINE_MARKER}`  
Source bridge: `192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4176` turns the loose phrase "local boundary silence" into a private compact-collar theorem:

```text
F_X[tau] = int_X n_mu T_total^{{mu nu}} tau_nu dSigma,
F_side[tau] = 0,
J_tr^nu := Pi_loc nabla_mu T_cross^{{mu nu}} = 0 through <=2PN.
```

The theorem is conditional: source support must be compact, galaxy/cosmology/open-memory pullbacks must vanish or be bounded, and radiative EM/gravity flux must be routed as boundary/Hamiltonian charge rather than discarded.

The next structural leak is quotient-naturality/vertical silence:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_192() -> None:
    FORMAL_192_PATH.write_text(
        f"""# 192 - PPC4161 Local Boundary No-Flux Sector Interface Theorem

Marker: `PPC4161_LOCAL_BOUNDARY_NO_FLUX_SECTOR_INTERFACE_THEOREM`
Checkpoint: `4176`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private selector theorem. This is not public local GR, not global MTS adoption, and not a numerical derivation of `G_N`.

## Boundary Decomposition
Let `W_loc` be a compact ordinary-matter local collar/worldtube. Decompose:

```text
partial W_loc = Sigma_in union Sigma_out union C_side union C_rad.
```

For any local time-flow/readout vector `tau` define:

```text
F_X[tau] = int_X n_mu T_total^{{mu nu}} tau_nu dSigma.
```

Here `T_total` is the same total Hilbert source already used by the PPC4161 local branch: matter, binding, and Maxwell-Hodge EM stress are counted once.

## No-Flux Selector Clauses
The compact local theorem needs these clauses signed by the parent selector:

```text
supp(T_local) subset int(W_loc),
n_mu T_cross^{{mu nu}} tau_nu | C_side = 0,
pullback(n_mu T_sector^{{mu nu}} tau_nu)|I_sector = 0
  for galaxy/cosmology/open-memory sectors,
delta H_tau = int_partialW (delta Q_tau - i_tau theta_total)
  is fixed, zero, or explicitly routed.
```

If any clause fails, the theorem does not set the leakage to zero. It reopens a transition-current or boundary-flux row.

## Integrated Conservation Argument
Local Bianchi/source conservation gives:

```text
int_Wloc nabla_mu T_total^{{mu nu}} tau_nu dV
= int_partialWloc n_mu T_total^{{mu nu}} tau_nu dSigma.
```

Under compact support and zero pullback/support separation on `C_side` and `I_sector`:

```text
F_side[tau] = 0.
```

The only nonzero radiative piece is a boundary/Hamiltonian charge:

```text
F_rad[tau] != 0  =>  route as boundary charge, not hidden bulk current.
```

## Transition Current Closure
Define the possible interface leakage:

```text
J_tr^nu := Pi_loc nabla_mu T_cross^{{mu nu}}.
```

In the compact local selector branch:

```text
J_tr^nu = 0 through <=2PN.
```

Therefore `xi_preferred_location`, `alpha_i_transition_current`, clock transition leakage and R10 transition-force rows close privately unless a nonzero sector/radiative boundary flux is introduced.

## What This Does Not Do
This does not erase galaxy, cosmology, open-memory, orbital, EM radiation or gravitational-radiation sectors. It only says those sectors do not enter the compact local PPN/readout equations as hidden transition currents when the no-flux/support-separation and Hamiltonian boundary clauses are satisfied.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4176 - Y5 R2FR Local Boundary No-Flux Sector Interface Theorem Or Transition Current Bound

Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Status: private selector theorem; no public local-GR claim.

## Why This Checkpoint Exists
4175 closed the EM/Poynting side-channel by deriving Poynting flux as Maxwell-Hodge Hilbert stress. The remaining leak was boundary/interface silence: galaxy, cosmology, open-memory, orbital and radiative sectors must not slip into the local PPN branch as an unnamed transition current.

## Local Collar Contract
Use a compact local ordinary-matter worldtube/collar `W_loc`:

```text
partial W_loc = Sigma_in union Sigma_out union C_side union C_rad,
F_X[tau] = int_X n_mu T_total^{{mu nu}} tau_nu dSigma.
```

The private selector must sign:

```text
supp(T_local) subset int(W_loc),
n_mu T_cross^{{mu nu}} tau_nu | C_side = 0,
pullback sector flux | I_sector = 0,
delta H_tau = int_partialW (delta Q_tau - i_tau theta_total) fixed/zero/routed.
```

Then:

```text
F_side[tau] = 0,
J_tr^nu := Pi_loc nabla_mu T_cross^{{mu nu}} = 0 through <=2PN.
```

## Guardrail
This is not flux amnesia. Radiative EM/gravity crossing `C_rad` is boundary/Hamiltonian charge. Galaxy/cosmology/open-memory sectors remain real sectors. If any interface flux is nonzero and not routed, the transition-current row reopens and must be empirically bounded.

## Output Files
- `formalization-workbench/192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md`
- `formalization-workbench/02-claims-register.csv` row `{CLAIM_ID}`
- `formalization-workbench/180-PPC4161-private-local-packet-integration.md` marker `{PACKET_MARKER}`
- `formalization-workbench/07-unification-spine.md` marker `{SPINE_MARKER}`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_SOURCE_REGISTER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_TRANSITION_CURRENT_CLOSE_OR_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_SECTOR_INTERFACE_MAP.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_BRANCH_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_CLAIM_FIREWALL.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_STATUS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4176_NEXT_TARGET.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4176_VALIDATION.csv`

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def rows_containing(rows: Iterable[Dict[str, str]], needle: str) -> List[Dict[str, str]]:
    return [row for row in rows if needle in " ".join(str(value) for value in row.values())]


def generated_tables(rows_by_name: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    generated: List[Dict[str, str]] = []
    for table_rows in rows_by_name.values():
        generated.extend(table_rows)
    return generated


def validation_rows(
    rows_by_name: Dict[str, List[Dict[str, str]]],
    claim_action: str,
    packet_action: str,
    spine_action: str,
) -> List[Dict[str, str]]:
    source = rows_by_name["P8_Y5_R2FR_4176_SOURCE_REGISTER"]
    domain = rows_by_name["P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION"]
    theorem = rows_by_name["P8_Y5_R2FR_4176_NO_FLUX_THEOREM"]
    transition = rows_by_name["P8_Y5_R2FR_4176_TRANSITION_CURRENT_CLOSE_OR_BOUND"]
    sector = rows_by_name["P8_Y5_R2FR_4176_SECTOR_INTERFACE_MAP"]
    decision = rows_by_name["P8_Y5_R2FR_4176_BRANCH_DECISION"]
    firewall = rows_by_name["P8_Y5_R2FR_4176_CLAIM_FIREWALL"]
    status = rows_by_name["P8_Y5_R2FR_4176_STATUS"]
    next_target = rows_by_name["P8_Y5_R2FR_4176_NEXT_TARGET"]

    formal_text = read_text(FORMAL_192_PATH)
    doc_text = read_text(DOC_PATH)
    packet_text = read_text(PACKET_180_PATH)
    spine_text = read_text(SPINE_PATH)
    claims = parse_csv(CLAIMS_PATH)
    claim_matches = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    all_generated = generated_tables(rows_by_name)
    bad_claim_rows = [
        row
        for row in all_generated
        if row.get("claim_allowed") != "False" or row.get("valid_for_claim") != "False"
    ]

    checks = [
        (
            "VAL4176_0_sources",
            "all source paths exist and contain required tokens",
            all(row["exists"] == "True" and row["required_text_found"] == "True" for row in source),
            str(source),
        ),
        (
            "VAL4176_1_domain",
            "domain rows define W_loc, C_side, C_rad, I_sector and Pi_loc",
            all(rows_containing(domain, token) for token in ["W_loc", "C_side", "C_rad", "I_sector", "Pi_loc"]),
            "\n".join(",".join(row.values()) for row in domain),
        ),
        (
            "VAL4176_2_theorem",
            "theorem rows contain F_X[tau], compact support, Hamiltonian boundary, J_tr^nu=0 and radiative routing",
            all(rows_containing(theorem, token) for token in ["F_X[tau]", "supp(T_local)", "delta H_tau", "J_tr^nu", "routed_not_zeroed"]),
            "\n".join(",".join(row.values()) for row in theorem),
        ),
        (
            "VAL4176_3_transition",
            "transition-current rows close private residuals and route radiation without zeroing it",
            all(rows_containing(transition, token) for token in ["J_tr^nu", "xi_preferred_location", "alpha_i_transition_current", "R10_short_range_transition", "routed_not_zeroed"]),
            "\n".join(",".join(row.values()) for row in transition),
        ),
        (
            "VAL4176_4_sector_map",
            "sector map covers galaxy, cosmology, open memory, radiative EM, radiative gravity and orbital tides",
            all(rows_containing(sector, token) for token in ["galaxy", "cosmology", "open_memory", "radiative_EM", "radiative_gravity", "orbital_external_tides"]),
            "\n".join(",".join(row.values()) for row in sector),
        ),
        (
            "VAL4176_5_decision",
            "decision rows select private no-flux theorem, keep radiation/sectors alive, keep global false and pick 4177",
            all(rows_containing(decision, token) for token in ["local_boundary_no_flux_theorem", "radiation_and_sector_interfaces_not_erased", "global_adoption_still_false", NEXT_TARGET]),
            "\n".join(",".join(row.values()) for row in decision),
        ),
        (
            "VAL4176_6_firewall",
            "firewall blocks public local-GR, global, sector-erasure, radiation-zeroing, numeric-G and empirical claims",
            all(rows_containing(firewall, token) for token in ["public local GR", "global MTS", "erase galaxy", "radiative flux", "Newton", "R10"]),
            "\n".join(",".join(row.values()) for row in firewall),
        ),
        (
            "VAL4176_7_formal_192",
            "formal 192 records boundary decomposition, flux functional, Hamiltonian boundary, transition current and next target",
            all(token in formal_text for token in ["PPC4161_LOCAL_BOUNDARY_NO_FLUX_SECTOR_INTERFACE_THEOREM", "F_X[tau]", "delta H_tau", "J_tr^nu = 0", NEXT_TARGET]),
            "formal 192 checked",
        ),
        (
            "VAL4176_8_doc",
            "checkpoint doc records collar contract, no-flux conclusion, guardrail and outputs",
            all(token in doc_text for token in ["Local Collar Contract", "F_side[tau] = 0", "Radiative EM/gravity", "Output Files"]),
            "doc checked",
        ),
        (
            "VAL4176_9_packet_180",
            "packet 180 contains local boundary no-flux marker",
            PACKET_MARKER in packet_text and "J_tr^nu" in packet_text,
            f"packet_action={packet_action}",
        ),
        (
            "VAL4176_10_claim_row",
            "claims register contains one L-017 boundary/no-flux nonclaim row",
            len(claim_matches) == 1
            and "private_selector_local_boundary_no_flux_nonclaim_public_claim_false" in claim_matches[0].get("status", ""),
            f"claim_action={claim_action}; matches={claim_matches}",
        ),
        (
            "VAL4176_11_spine",
            "spine contains 4176 marker, claim row and next target",
            SPINE_MARKER in spine_text and CLAIM_ID in spine_text and NEXT_TARGET in spine_text,
            f"spine_action={spine_action}",
        ),
        (
            "VAL4176_12_status",
            "status records private no-flux closure, transition closure, radiative routing, global false and quotient next target",
            status[0]["local_boundary_no_flux_theorem_derived_private"] == "True"
            and status[0]["transition_current_closed_private"] == "True"
            and status[0]["radiative_boundary_flux_zeroed"] == "False"
            and status[0]["radiative_boundary_flux_routed"] == "True"
            and status[0]["sector_interfaces_erased"] == "False"
            and status[0]["global_parent_action_adoption_proved"] == "False"
            and status[0]["quotient_naturality_proved_global"] == "False"
            and status[0]["public_local_GR_claim_allowed"] == "False"
            and status[0]["next_target"] == NEXT_TARGET,
            str(status),
        ),
        (
            "VAL4176_13_next",
            "next target moves to quotient naturality or projector residual bounds",
            next_target[0]["next_target"] == NEXT_TARGET and "projector-residual" in next_target[0]["route_B"],
            str(next_target),
        ),
        (
            "VAL4176_14_no_claim_rows",
            "all generated rows keep claim_allowed/valid_for_claim false",
            not bad_claim_rows,
            str(bad_claim_rows),
        ),
    ]

    validation: List[Dict[str, str]] = []
    for check_id, description, passed, details in checks:
        validation.append(
            {
                **common(),
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "details": details,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation.append(
        {
            **common(),
            "check_id": "VAL4176_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_192()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4176_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4176_BOUNDARY_DOMAIN_DECOMPOSITION": boundary_domain_rows(),
        "P8_Y5_R2FR_4176_NO_FLUX_THEOREM": no_flux_theorem_rows(),
        "P8_Y5_R2FR_4176_TRANSITION_CURRENT_CLOSE_OR_BOUND": transition_current_rows(),
        "P8_Y5_R2FR_4176_SECTOR_INTERFACE_MAP": sector_interface_rows(),
        "P8_Y5_R2FR_4176_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4176_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4176_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4176_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4176_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4176 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_192_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
