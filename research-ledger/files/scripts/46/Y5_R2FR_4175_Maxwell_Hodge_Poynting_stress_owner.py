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

CHECKPOINT = "4175"
BRANCH_ID = "MTS_R2FR_Y5_MAXWELL_HODGE_POYNTING_STRESS_OWNER_4175"
DECISION = "MAXWELL_HODGE_POYNTING_STRESS_OWNER_THEOREM_CLOSES_EM_SIDE_CHANNEL_PRIVATE_SELECTOR"
DOC_PATH = POST / "4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md"
FORMAL_191_PATH = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-016"
SPINE_MARKER = "PPC4161_MAXWELL_HODGE_POYNTING_OWNER_4175"
PACKET_MARKER = "PPC4161_PACKET_MAXWELL_HODGE_POYNTING_OWNER_4175"
NEXT_TARGET = "4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md"

SOURCES = {
    "SRC4175_00_4174_doc": (
        POST / "4174-Y5-R2FR-parent-action-global-adoption-or-explicit-local-branch-quarantine.md",
        "EM/Poynting stress is the most physical remaining leak",
        "4174 selected the EM/Poynting owner gate.",
    ),
    "SRC4175_01_4174_em_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4174_EM_POYNTING_OWNER_GATE.csv",
        "S_Maxwell-Hodge[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu",
        "4174 EM/Poynting gate rows.",
    ),
    "SRC4175_02_4174_selector": (
        SOURCE_DIR / "P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES.csv",
        "Maxwell-Hodge/Poynting stress ownership",
        "4174 selector clause SEL4174_4.",
    ),
    "SRC4175_03_formal_185": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "The EM/Poynting contribution is not an add-on",
        "Prior Hilbert source descent included EM/Poynting in the same source action.",
    ),
    "SRC4175_04_formal_190": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "T_EM^0i",
        "4174 formal selector/quarantine bridge identifying the Poynting target.",
    ),
    "SRC4175_05_claim_L015": (
        CLAIMS_PATH,
        "conditional_selector_theorem_quarantined_nonclaim_public_claim_false",
        "Claim register handoff before 4175.",
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


def action_variation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MH4175_0_action",
            "Maxwell-Hodge action",
            "S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu",
            "parent local selector contains only this EM kinetic owner plus binding/improvement terms",
            "adopted_private_selector",
        ),
        (
            "MH4175_1_field_strength",
            "gauge field strength",
            "F_mu_nu = d_mu A_nu - d_nu A_mu",
            "depends on A and g_obs for index/Hodge operations, not on an independent source metric",
            "derived_identity",
        ),
        (
            "MH4175_2_Hilbert_stress",
            "metric variation",
            "T_EM^mu_nu = F^mu_alpha F^nu_alpha - 1/4 g_obs^mu_nu F_alpha_beta F^alpha_beta",
            "all EM energy density, pressure and momentum flux enter the same Hilbert tensor",
            "derived_private_selector",
        ),
        (
            "MH4175_3_no_weight",
            "no independent EM source multiplier",
            "delta S_parent/dg_obs contains T_EM once, not Z_EM T_EM plus T_EM_leak",
            "prevents a hidden EM-dependent gravitational coupling",
            "derived_private_selector",
        ),
        (
            "MH4175_4_improvement",
            "exact/improvement terms",
            "dB_impr can alter boundary charge bookkeeping but not create a bulk Poynting force channel",
            "boundary flux must be counted in Hamiltonian charge if nonzero",
            "guarded_private_selector",
        ),
    ]
    return [
        {
            **common(),
            "step_id": step_id,
            "operation": operation,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for step_id, operation, formula, meaning, status in rows
    ]


def poynting_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "PNT4175_0_observer_split",
            "local observer split",
            "Choose local tetrad n^mu,e_i^mu with E_i=F_i_mu n^mu and B_i=starF_i_mu n^mu",
            "defines electric and magnetic fields relative to the same g_obs observer",
        ),
        (
            "PNT4175_1_energy_density",
            "EM energy density",
            "rho_EM = T_EM(n,n) = 1/2 (E^2 + B^2)",
            "EM energy gravitates through T_total with no extra weight",
        ),
        (
            "PNT4175_2_flux",
            "Poynting vector",
            "S_i = -T_EM(n,e_i) = (E cross B)_i",
            "Poynting flux is a component of T_EM, not a new field or force",
        ),
        (
            "PNT4175_3_momentum_density",
            "EM momentum density",
            "g_EM_i = S_i/c^2 in SI units, or g_EM_i = S_i when c=1",
            "momentum flow is owned by the same Hilbert stress tensor",
        ),
        (
            "PNT4175_4_radiative_boundary",
            "radiative EM flux",
            "nonzero EM radiation crossing a collar boundary is boundary/Hamiltonian flux, not a hidden local bulk source",
            "does not erase radiative EM sector; it routes it correctly",
        ),
    ]
    return [
        {
            **common(),
            "poynting_id": poynting_id,
            "identity": identity,
            "formula": formula,
            "local_role": role,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for poynting_id, identity, formula, role in rows
    ]


def conservation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "CONS4175_0_Maxwell",
            "Maxwell equation",
            "nabla_mu F^mu_nu = J_nu",
            "uses the same g_obs/Hodge operator as the Hilbert stress variation",
            "derived_private_selector",
        ),
        (
            "CONS4175_1_EM_divergence",
            "EM stress divergence",
            "nabla_mu T_EM^mu_nu = -F_nu_lambda J^lambda",
            "EM stress exchanges four-force with charged matter but is not separately conserved when J is nonzero",
            "derived_private_selector",
        ),
        (
            "CONS4175_2_matter_exchange",
            "matter/binding exchange",
            "nabla_mu T_matter+binding^mu_nu = F_nu_lambda J^lambda",
            "Lorentz force appears as internal exchange between matter and EM sectors",
            "derived_private_selector",
        ),
        (
            "CONS4175_3_total",
            "total conservation",
            "nabla_mu (T_matter+binding^mu_nu + T_EM^mu_nu) = 0",
            "Bianchi identity sees one conserved total source",
            "derived_private_selector",
        ),
        (
            "CONS4175_4_zeta3",
            "PPN conservation row",
            "zeta3_EM_side_channel = 0",
            "4172 zeta3 closure is now supported by Maxwell-Hodge ownership instead of a bare label",
            "closed_private_selector",
        ),
    ]
    return [
        {
            **common(),
            "conservation_id": conservation_id,
            "identity": identity,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for conservation_id, identity, formula, meaning, status in rows
    ]


def side_channel_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "EMSC4175_0_epsilon_EM_extra_inner",
            "epsilon_EM_extra_inner",
            "closed_private",
            "No independent S_Poynting_background, S_EM_weighted_species, hidden EM-current multiplier or second EM metric is admitted in the selector branch.",
            "reactivate if parent action contains extra EM source weight, disformal EM metric, hidden current, or non-Hilbert Poynting term",
        ),
        (
            "EMSC4175_1_zeta3",
            "zeta3",
            "closed_private",
            "Poynting stress is T_EM flux and total matter+EM stress is conserved.",
            "reactivate if EM energy/momentum is not counted in T_total or is counted twice",
        ),
        (
            "EMSC4175_2_WEP_clock",
            "WEP_eta_and_clock_redshift_EM_leak",
            "closed_private",
            "The same g_obs couples to matter, clocks and Maxwell-Hodge EM stress.",
            "reactivate if EM binding energy receives a species/readout/source multiplier",
        ),
        (
            "EMSC4175_3_R10_force",
            "short_range_EM_background_force",
            "closed_private",
            "No Poynting-background fifth force exists after Maxwell-Hodge ownership.",
            "reactivate and source-bound if an independent finite-range EM-background force term is introduced",
        ),
        (
            "EMSC4175_4_boundary_flux",
            "radiative_boundary_flux",
            "routed_not_zeroed",
            "Nonzero EM radiation flux is counted in boundary/Hamiltonian charge and not silently discarded.",
            "reactivate local boundary no-flux gate if flux crosses the compact local collar",
        ),
    ]
    return [
        {
            **common(),
            "side_channel_id": side_channel_id,
            "residual": residual,
            "status": status,
            "closure_reason": closure_reason,
            "reactivation_condition": reactivation_condition,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for side_channel_id, residual, status, closure_reason, reactivation_condition in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4175_0_owner_theorem",
            "Maxwell_Hodge_Poynting_owner_theorem",
            "The Poynting vector is T_EM flux from metric variation of S_Maxwell-Hodge; it is not a separate source.",
            "close_EM_side_channel_private_selector",
        ),
        (
            "DEC4175_1_no_global",
            "global_adoption_still_false",
            "The theorem is inside the PPC4161 local selector/quarantine branch; it does not globally sign boundary silence or quotient naturality.",
            "keep_local_branch_quarantined",
        ),
        (
            "DEC4175_2_next",
            "next_best_derivation_target",
            "After EM ownership, the largest remaining local leak is boundary/interface no-flux between local collars and galaxy/cosmology/open-memory/radiative branches.",
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
        ("FW4175_0_no_global", "Do not claim global MTS adoption from Maxwell-Hodge ownership."),
        ("FW4175_1_no_public_local_GR", "Do not claim public local GR; boundary silence and quotient naturality remain open."),
        ("FW4175_2_no_radiation_erasure", "Do not erase radiative EM; nonzero boundary flux must be routed through boundary/Hamiltonian charge."),
        ("FW4175_3_no_numeric_G", "Do not claim a numerical derivation of Newton's constant."),
        ("FW4175_4_no_hidden_EM", "Do not add a separate Poynting/background source after counting T_EM in T_total."),
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
            "Maxwell_Hodge_Poynting_owner_theorem_derived_private": "True",
            "EM_Poynting_side_channel_closed_private": "True",
            "zeta3_EM_conservation_closed_private": "True",
            "radiative_boundary_flux_zeroed": "False",
            "radiative_boundary_flux_routed": "True",
            "global_parent_action_adoption_proved": "False",
            "local_boundary_silence_proved_global": "False",
            "quotient_naturality_proved_global": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "formal_191_written": "True",
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
            "why_next": "4175 closes the EM/Poynting side-channel inside the private selector; the next largest leak is whether local collar boundaries are truly no-flux/support-separated from galaxy, cosmology, open-memory and radiative sectors.",
            "route_A": "prove a local boundary/interface no-flux theorem for compact local collars from parent support and Hamiltonian boundary conditions",
            "route_B": "if boundary silence cannot be proved, build transition-current residuals and source-backed local PPN/clock/R10 bounds",
            "fallback": "keep PPC4161-TK-HQNP quarantined until boundary silence and quotient naturality are parent-signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4175_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4175_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION": SOURCE_DIR / "P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION.csv",
        "P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION": SOURCE_DIR / "P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION.csv",
        "P8_Y5_R2FR_4175_TOTAL_CONSERVATION_AND_LORENTZ_EXCHANGE": SOURCE_DIR / "P8_Y5_R2FR_4175_TOTAL_CONSERVATION_AND_LORENTZ_EXCHANGE.csv",
        "P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE": SOURCE_DIR / "P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE.csv",
        "P8_Y5_R2FR_4175_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4175_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4175_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4175_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4175_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4175_STATUS.csv",
        "P8_Y5_R2FR_4175_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4175_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "Inside the PPC4161 local selector branch, Maxwell-Hodge variation owns the Poynting vector as EM Hilbert stress, closing the EM side-channel privately",
        "current_evidence": "formalization-workbench/191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md records S_MH=-1/4 int sqrt(-g)F^2, T_EM from metric variation, Poynting flux as T_EM^0i, total matter+EM conservation, zeta3_EM_side_channel=0, and radiative boundary flux routed rather than erased; public_claim=false",
        "status": "private_selector_Maxwell_Hodge_Poynting_owner_nonclaim_public_claim_false",
        "next_test": "Prove local boundary/interface no-flux theorem or bound transition-current leakage into local PPN/clock/R10 tests",
        "key_risk": "This closes EM ownership only inside the private selector; global parent adoption, boundary silence, quotient naturality and numerical G_N remain unproved",
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
## PPC4161-TK-HQNP Addendum - Maxwell-Hodge/Poynting Stress Ownership

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md`

Inside the private local selector branch:

```text
S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu.
```

Metric variation gives one EM Hilbert stress:

```text
T_EM^mu_nu = F^mu_alpha F^nu_alpha - 1/4 g_obs^mu_nu F_alpha_beta F^alpha_beta.
```

In a local observer split:

```text
rho_EM = 1/2 (E^2+B^2),
S_i = -T_EM(n,e_i) = (E cross B)_i.
```

Therefore the Poynting vector is already part of `T_total`; it is not a separate background force/source channel. Nonzero radiative EM boundary flux is routed through boundary/Hamiltonian charge and is not silently zeroed.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Maxwell-Hodge/Poynting Stress Owner - 4175

Marker: `{SPINE_MARKER}`  
Source bridge: `191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4175` closes the EM/Poynting side-channel inside the private local selector:

```text
S_MH[A,g_obs] -> T_EM^mu_nu,
S_i = -T_EM(n,e_i) = (E cross B)_i,
nabla_mu (T_matter+binding^mu_nu + T_EM^mu_nu) = 0.
```

The important physical point is that EM flux is not ignored; it is owned by the Maxwell-Hodge Hilbert stress or routed as boundary/Hamiltonian flux. It cannot be added again as a hidden local source.

The next remaining local leak is boundary/interface silence:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_191() -> None:
    FORMAL_191_PATH.write_text(
        f"""# 191 - PPC4161 Maxwell-Hodge/Poynting Stress Owner Theorem

Marker: `PPC4161_MAXWELL_HODGE_POYNTING_STRESS_OWNER_THEOREM`
Checkpoint: `4175`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private selector theorem, not a public local-GR claim and not global MTS adoption.

## Maxwell-Hodge Owner
Inside the compact local selector branch:

```text
S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu.
```

The Hilbert variation gives:

```text
T_EM^mu_nu =
F^mu_alpha F^nu_alpha
- 1/4 g_obs^mu_nu F_alpha_beta F^alpha_beta.
```

Thus EM energy density, stress, momentum density and flux all enter the same `T_total` used by the local EH equation.

## Poynting Identification
For local observer `n` and spatial triad `e_i`:

```text
rho_EM = T_EM(n,n) = 1/2(E^2+B^2),
S_i = -T_EM(n,e_i) = (E cross B)_i.
```

So the Poynting vector is not a separate background field. It is the spatial energy-flux component of the Maxwell-Hodge Hilbert stress.

## Conservation And Exchange
With Maxwell equation `nabla_mu F^mu_nu = J_nu`:

```text
nabla_mu T_EM^mu_nu = -F_nu_lambda J^lambda,
nabla_mu T_matter+binding^mu_nu = F_nu_lambda J^lambda,
nabla_mu T_total^mu_nu = 0,
nabla_mu (T_matter+binding^mu_nu + T_EM^mu_nu) = 0.
```

The Lorentz force is internal exchange between matter and EM, not nonconservation of the total source.

## Side-Channel Closure

```text
epsilon_EM_extra_inner = 0,
zeta3_EM_side_channel = 0.
```

This holds only while the parent selector forbids independent EM source weights, hidden EM-current multipliers, a second EM metric, or a standalone Poynting-background term.

## Radiative Boundary Guard
Radiative EM is not erased. If nonzero EM flux crosses the local collar boundary, it is boundary/Hamiltonian flux and must be routed there. It is not silently zeroed and not counted twice as a hidden bulk source.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4175 - Maxwell-Hodge/Poynting Stress Owner Theorem Or EM Side-Channel Bound

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4174 isolated the EM/Poynting owner gate as the most physical coupling leak. 4175 closes it inside the private selector branch.

## Derivation

```text
S_MH[A,g_obs] = -1/4 int sqrt(-g_obs) F_mu_nu F^mu_nu
```

varies to:

```text
T_EM^mu_nu = F^mu_alpha F^nu_alpha - 1/4 g_obs^mu_nu F_alpha_beta F^alpha_beta.
```

The local Poynting vector is:

```text
S_i = -T_EM(n,e_i) = (E cross B)_i.
```

Therefore Poynting flux is already owned by the Hilbert source tensor. It cannot be added again as a hidden background force/source.

## Conservation

```text
nabla_mu T_EM^mu_nu = -F_nu_lambda J^lambda,
nabla_mu T_matter+binding^mu_nu = F_nu_lambda J^lambda,
nabla_mu T_total^mu_nu = 0.
```

So the Lorentz force is internal matter-EM exchange, while total source conservation remains intact.

## Guardrail
Radiative EM flux is not erased. Nonzero flux across the collar boundary must be boundary/Hamiltonian charge flux. The next target is the boundary/interface no-flux theorem.

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

    sources = parse_csv(outputs["P8_Y5_R2FR_4175_SOURCE_REGISTER"])
    add("VAL4175_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    action = parse_csv(outputs["P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION"])
    action_text = "\n".join(",".join(row.values()) for row in action)
    add("VAL4175_1_action", "action variation rows contain Maxwell-Hodge action, F definition, T_EM and no independent multiplier", all(token in action_text for token in ["S_MH[A,g_obs]", "F_mu_nu", "T_EM^mu_nu", "T_EM_leak", "dB_impr"]), action_text)

    poynting = parse_csv(outputs["P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION"])
    poynting_text = "\n".join(",".join(row.values()) for row in poynting)
    add("VAL4175_2_poynting", "Poynting rows identify observer split, energy density, flux, momentum density and radiative boundary routing", all(token in poynting_text for token in ["E_i=F_i_mu n^mu", "rho_EM", "S_i = -T_EM", "S_i/c^2", "boundary/Hamiltonian flux"]), poynting_text)

    conservation = parse_csv(outputs["P8_Y5_R2FR_4175_TOTAL_CONSERVATION_AND_LORENTZ_EXCHANGE"])
    conservation_text = "\n".join(",".join(row.values()) for row in conservation)
    add("VAL4175_3_conservation", "conservation rows show Maxwell equation, EM divergence, matter exchange, total conservation and zeta3 closure", all(token in conservation_text for token in ["nabla_mu F^mu_nu = J_nu", "nabla_mu T_EM^mu_nu", "nabla_mu T_matter+binding", "nabla_mu (T_matter+binding^mu_nu + T_EM^mu_nu) = 0", "zeta3_EM_side_channel = 0"]), conservation_text)

    side = parse_csv(outputs["P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE"])
    side_text = "\n".join(",".join(row.values()) for row in side)
    add("VAL4175_4_side_channels", "side-channel rows close EM extra, zeta3, WEP/clock and R10 force residuals while routing boundary flux", all(token in side_text for token in ["epsilon_EM_extra_inner", "zeta3", "WEP_eta_and_clock", "short_range_EM_background_force", "routed_not_zeroed"]), side_text)

    decisions = parse_csv(outputs["P8_Y5_R2FR_4175_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add("VAL4175_5_decision", "decision rows select Maxwell-Hodge owner theorem, keep global adoption false and choose boundary next", all(token in decision_text for token in ["Maxwell_Hodge_Poynting_owner_theorem", "global_adoption_still_false", "boundary/interface no-flux", NEXT_TARGET]), decision_text)

    firewall = parse_csv(outputs["P8_Y5_R2FR_4175_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4175_6_firewall", "firewall blocks global, public local-GR, radiation erasure, numeric-G and hidden-EM claims", all(token in firewall_text for token in ["global MTS", "public local GR", "radiative EM", "Newton's constant", "Poynting/background"]), firewall_text)

    formal_text = read_text(FORMAL_191_PATH)
    add("VAL4175_7_formal_191", "formal 191 records Maxwell-Hodge owner, Poynting identification, conservation, side-channel closure, boundary guard and next target", FORMAL_191_PATH.exists() and all(token in formal_text for token in ["PPC4161_MAXWELL_HODGE_POYNTING_STRESS_OWNER_THEOREM", "T_EM^mu_nu", "S_i = -T_EM", "nabla_mu T_total^mu_nu = 0", "epsilon_EM_extra_inner = 0", "Radiative Boundary Guard", NEXT_TARGET]), "formal 191 checked")

    packet_text = read_text(PACKET_180_PATH)
    add("VAL4175_8_packet_180", "packet 180 contains Maxwell-Hodge/Poynting addendum", all(token in packet_text for token in [PACKET_MARKER, "S_MH[A,g_obs]", "T_EM^mu_nu", "Poynting vector is already part of `T_total`"]), "packet 180 checked")

    claims = parse_csv(CLAIMS_PATH)
    l016 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4175_9_claim_row", "claims register contains one L-016 Maxwell-Hodge/Poynting nonclaim row", len(l016) == 1 and l016[0].get("status") == "private_selector_Maxwell_Hodge_Poynting_owner_nonclaim_public_claim_false" and "public_claim=false" in l016[0].get("current_evidence", ""), str(l016))

    spine_text = read_text(SPINE_PATH)
    add("VAL4175_10_spine", "spine contains 4175 marker, claim row and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "Maxwell-Hodge Hilbert stress", NEXT_TARGET]), "spine checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4175_STATUS"])
    add("VAL4175_11_status", "status records EM owner closure private, radiative flux routed not zeroed, global adoption false and boundary next target", len(status) == 1 and status[0]["Maxwell_Hodge_Poynting_owner_theorem_derived_private"] == "True" and status[0]["EM_Poynting_side_channel_closed_private"] == "True" and status[0]["radiative_boundary_flux_zeroed"] == "False" and status[0]["global_parent_action_adoption_proved"] == "False" and status[0]["next_target"] == NEXT_TARGET, str(status))

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4175_NEXT_TARGET"])
    add("VAL4175_12_next", "next target moves to local boundary no-flux/interface theorem or transition current bound", len(next_loaded) == 1 and next_loaded[0]["next_target"] == NEXT_TARGET and "transition-current" in "\n".join(next_loaded[0].values()), str(next_loaded))

    doc_text = read_text(DOC_PATH)
    add("VAL4175_13_doc", "checkpoint doc records derivation, conservation, guardrail and output list", all(token in doc_text for token in ["Maxwell-Hodge/Poynting Stress Owner", "T_EM^mu_nu", "S_i = -T_EM", "nabla_mu T_total^mu_nu = 0", "Radiative EM flux is not erased", "Outputs"]), "doc checked")

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4175_14_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

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
    add("VAL4175_15_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def write_outputs(outputs: Dict[str, Path]) -> None:
    write_csv(outputs["P8_Y5_R2FR_4175_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_MAXWELL_HODGE_ACTION_VARIATION"], action_variation_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_POYNTING_STRESS_IDENTIFICATION"], poynting_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_TOTAL_CONSERVATION_AND_LORENTZ_EXCHANGE"], conservation_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE"], side_channel_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4175_NEXT_TARGET"], next_rows())


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_191()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_outputs(outputs)
    write_csv(outputs["P8_Y5_R2FR_4175_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4175_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_191_PATH}")
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
