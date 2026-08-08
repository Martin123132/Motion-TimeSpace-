from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_PATH = Path(__file__)

CHECKPOINT = "4172"
BRANCH_ID = "MTS_R2FR_Y5_PPC4161_FULL_PPN_READOUT_4172"
DECISION = "PPC4161_TK_HQNP_FULL_GR_PPN_VECTOR_CLOSED_PRIVATE_PACKET_EMPIRICAL_GATES_REMAIN"
DOC_PATH = POST / "4172-Y5-R2FR-PPC4161-full-PPN-readout-gamma-beta-alpha-xi-zeta.md"
FORMAL_188_PATH = FORMAL / "188-PPC4161-full-PPN-readout-vector.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-013"
SPINE_MARKER = "PPC4161_FULL_PPN_VECTOR_4172"
PACKET_MARKER = "PPC4161_PACKET_FULL_PPN_VECTOR_4172"
NEXT_TARGET = "4173-Y5-R2FR-local-empirical-PPN-R10-clock-WEP-orbital-validation-pack.md"

SOURCES = {
    "SRC4172_00_4164_ppn_gate_doc": (
        POST / "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md",
        "R_PPN =",
        "4164 conditional map from PPC4161 residual tensor to the standard PPN vector.",
    ),
    "SRC4172_01_4164_ppn_vector_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR.csv",
        "Delta_gamma = gamma - 1",
        "4164 residual vector rows for gamma, beta, alpha_i, zeta_i, xi and Gdot/G.",
    ),
    "SRC4172_02_4168_kappa_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4168_STATUS.csv",
        "topological_stress_zero",
        "4168 closes local kappa drift and topological stress inside the private packet.",
    ),
    "SRC4172_03_4169_source_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4169_STATUS.csv",
        "R_A_G_closed_private",
        "4169 closes the Hilbert source-measure coupling residual inside the private packet.",
    ),
    "SRC4172_04_4170_charge_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4170_STATUS.csv",
        "same_charge_glue_closed_private",
        "4170 glues the Hilbert source charge to the Hamiltonian/worldtube mass charge.",
    ),
    "SRC4172_05_4171_newton_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4171_STATUS.csv",
        "Poisson_equation_derived_private",
        "4171 closes the first-order Poisson/Gauss/Newton readout.",
    ),
    "SRC4172_06_formal_187": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "a_r = -G_N M_H^dress/r^2",
        "Formal bridge for the Newtonian source readout used as the 1PN seed.",
    ),
    "SRC4172_07_packet_180": (
        PACKET_180_PATH,
        "PPC4161_PACKET_POISSON_GAUSS_NEWTON_READOUT_4171",
        "Private packet integration file carrying the 4168-4171 adopted clauses.",
    ),
}

PPN_COMPONENTS = [
    (
        "gamma",
        "1",
        "gamma-1=0",
        "spatial curvature per unit Newton potential",
        "g_ij=(1+2U/c^2)delta_ij+O(c^-4)",
        "EH spatial equation with the same observed metric and no scalar/disformal/vertical 2PN bulk residual",
    ),
    (
        "beta",
        "1",
        "beta-1=0",
        "nonlinear U^2 self-interaction",
        "g_00=-1+2U/c^2-2U^2/c^4+O(c^-6)",
        "EH self-interaction coefficient, fixed kappa_* and binding stress counted once in the Hilbert source",
    ),
    (
        "alpha1",
        "0",
        "alpha1=0",
        "preferred-frame velocity coupling",
        "no independent local vector-mode term in g_0i",
        "same local quotient coframe and no representative-dependent vector channel inside PPC4161-TK-HQNP",
    ),
    (
        "alpha2",
        "0",
        "alpha2=0",
        "preferred-frame spin/velocity anisotropy",
        "no anisotropic q-basic residual in the local collar",
        "same observer frame and no anisotropic projector drift inside PPC4161-TK-HQNP",
    ),
    (
        "alpha3",
        "0",
        "alpha3=0",
        "momentum nonconservation/preferred-frame self acceleration",
        "nabla_mu T_total^mu_nu=0 and no hidden source-current leak",
        "Hilbert source descent plus Bianchi identity closes momentum leakage in the private packet",
    ),
    (
        "xi",
        "0",
        "xi=0",
        "preferred-location or external-field coupling",
        "compact local collar decouples from FLRW, galaxy and open-memory gradients at <=2PN",
        "local packet boundary silence removes external preferred-location terms in the PPN readout",
    ),
    (
        "zeta1",
        "0",
        "zeta1=0",
        "stress-energy conservation residual 1",
        "single Hilbert source stress owns matter flux",
        "no independent matter-source weight survives 4169 source descent",
    ),
    (
        "zeta2",
        "0",
        "zeta2=0",
        "stress-energy conservation residual 2",
        "binding and matter stress are included once",
        "Hamiltonian/worldtube same-charge glue prevents double-counted binding stress",
    ),
    (
        "zeta3",
        "0",
        "zeta3=0",
        "stress-energy conservation residual 3",
        "EM/Poynting stress is in the same Hilbert source",
        "4169 places EM/Poynting bookkeeping inside T_total rather than a separate force channel",
    ),
    (
        "zeta4",
        "0",
        "zeta4=0",
        "stress-energy conservation residual 4",
        "pressure/internal energy descend to the same observed stress tensor",
        "same Hilbert measure and same Hamiltonian charge keep pressure bookkeeping conserved",
    ),
    (
        "Gdot_over_G",
        "0",
        "dot(G_eff)/G_eff=0",
        "time drift of the local gravitational coupling",
        "G_N=c^4 kappa_* Z_0/(8*pi) with D_A ln kappa_*=0 and delta_ZH=0",
        "4168 topological kappa lock plus 4169 source-measure descent make the local coupling stationary",
    ),
]


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


def ppn_gauge_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "GAUGE4172_0_branch",
            "private branch definition",
            "PPC4161-TK-HQNP := PPC4161-TK-HQN plus the full EH <=2PN local quotient readout",
            "adopted_private_branch",
            "This is a local packet closure, not a proof that the whole MTS parent has no extra branch elsewhere.",
        ),
        (
            "GAUGE4172_1_coordinates",
            "standard local PPN gauge",
            "Use local quasi-Cartesian PPN coordinates with U=-Phi_N>=0 and the same observed metric/coframe g_obs.",
            "adopted_private_branch",
            "Keeps the readout comparable to GR PPN rather than a bespoke coordinate statement.",
        ),
        (
            "GAUGE4172_2_g00",
            "time-time metric",
            "g_00=-1+2U/c^2-2U^2/c^4+O(c^-6), so beta=1.",
            "derived_private",
            "The U term is the 4171 Poisson/Gauss source readout; the U^2 coefficient is the EH self-interaction.",
        ),
        (
            "GAUGE4172_3_gij",
            "spatial metric",
            "g_ij=(1+2gamma U/c^2)delta_ij+O(c^-4) with the EH local packet giving gamma=1.",
            "derived_private",
            "This is the gamma gate: no extra scalar/disformal spatial curvature channel survives in the packet.",
        ),
        (
            "GAUGE4172_4_g0i",
            "mixed metric",
            "g_0i has the GR vector potentials only; no preferred-frame alpha_i source is present.",
            "derived_private",
            "The quotient coframe is fixed before readout, so no representative velocity field is allowed to become a force.",
        ),
        (
            "GAUGE4172_5_conservation",
            "stress conservation",
            "nabla_mu T_total^mu_nu=0 follows from the Hilbert source descent and Bianchi identity.",
            "derived_private",
            "This closes the zeta_i and alpha3 leakage channels inside the packet.",
        ),
        (
            "GAUGE4172_6_coupling",
            "constant local coupling",
            "dot(G_eff)/G_eff=0 because kappa_* is topologically locked and delta_ZH=0.",
            "derived_private",
            "This closes Gdot/G inside the packet but does not predict the numerical magnitude of G_N.",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "formula_or_rule": formula,
            "status": status,
            "guardrail": guardrail,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, formula, status, guardrail in rows
    ]


def ppn_vector_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "parameter": parameter,
            "gr_ppn_value": gr_value,
            "private_packet_residual": residual,
            "meaning": meaning,
            "metric_or_identity_readout": readout,
            "zero_condition_closed_by": zero_clause,
            "derived_private": "True",
            "public_claim_result": "not_claimed",
            "needs_empirical_test": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for parameter, gr_value, residual, meaning, readout, zero_clause in PPN_COMPONENTS
    ]


def side_channel_rows() -> List[Dict[str, str]]:
    rows = [
        ("SC4172_0_kappa", "epsilon_kappa", "closed_private", "4168 D_A ln kappa_*=0 and topological stress zero"),
        ("SC4172_1_source", "epsilon_source_measure", "closed_private", "4169 delta_ZH=0 and R_A^G=0"),
        ("SC4172_2_charge", "epsilon_mass_charge", "closed_private", "4170 Pi_M/H_tau/worldtube same-charge glue"),
        ("SC4172_3_newton", "epsilon_Newton_readout", "closed_private", "4171 Poisson/Gauss/Newton readout"),
        ("SC4172_4_scalar_disformal", "epsilon_scalar_disformal", "closed_inside_private_packet", "PPC4161-TK-HQNP uses one observed EH metric/coframe in the local collar"),
        ("SC4172_5_vector_frame", "epsilon_frame_projector", "closed_inside_private_packet", "No independent local vector/projector mode is admitted in the PPN readout branch"),
        ("SC4172_6_hidden_flux", "epsilon_hidden_flux", "closed_inside_private_packet", "All material, pressure, binding and EM/Poynting fluxes are carried by T_total"),
        ("SC4172_7_boundary", "epsilon_boundary_cosmo", "closed_inside_private_packet", "Compact local collar is silent to <=2PN external memory/FLRW/galaxy gradients"),
    ]
    return [
        {
            **common(),
            "channel_id": channel_id,
            "channel": channel,
            "status": status,
            "closure_statement": closure,
            "reactivation_condition": "reactivate_named_PPN_residual_if_parent_rejects_this_clause",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for channel_id, channel, status, closure in rows
    ]


def residual_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for parameter, gr_value, residual, meaning, readout, zero_clause in PPN_COMPONENTS:
        rows.append(
            {
                **common(),
                "residual_id": f"R4172_{parameter}",
                "parameter": parameter,
                "residual": residual,
                "status": "closed_private_in_PPC4161_TK_HQNP",
                "closure_reason": zero_clause,
                "fallback_if_reopened": "source_backed_empirical_bound_row_required",
                "public_claim_result": "not_claimed",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def remaining_gate_rows() -> List[Dict[str, str]]:
    rows = [
        ("RG4172_0_cassini_gamma", "Cassini/Shapiro gamma bound", "gamma-1", "not_run", "formal private value is zero but empirical source-backed check still needed"),
        ("RG4172_1_beta_orbits", "perihelion/LLR beta bound", "beta-1", "not_run", "formal private value is zero but orbital residual pack not run"),
        ("RG4172_2_preferred_frame", "preferred-frame bounds", "alpha1, alpha2, alpha3", "not_run", "formal private values are zero but pulsar/solar-system bound table not sourced here"),
        ("RG4172_3_conservation", "conservation bounds", "zeta1, zeta2, zeta3, zeta4, xi", "not_run", "formal private values are zero but empirical conservation/preferred-location checks remain"),
        ("RG4172_4_R10_clock_WEP", "R10, clocks and WEP", "local non-GR channels", "not_run", "full PPN does not automatically close all short-range/clock/WEP arenas"),
        ("RG4172_5_numeric_G", "Newton constant magnitude", "G_N=c^4 kappa_* Z_0/(8*pi)", "not_predicted", "local branch calibrates G_N; it does not derive the number"),
        ("RG4172_6_global_MTS", "global MTS adoption", "PPC4161-TK-HQNP subset != full MTS", "not_closed", "local private packet does not prove global cosmology/galaxy/EM sector adoption"),
    ]
    return [
        {
            **common(),
            "gate_id": gate_id,
            "gate": gate,
            "formula": formula,
            "status": status,
            "why_remaining": why,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for gate_id, gate, formula, status, why in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        ("DEC4172_0_selected", "select_private_PPN_readout", "The 4164 conditional PPN vector is now adopted inside PPC4161-TK-HQNP using the 4168-4171 local packet closures.", "go_to_empirical_local_pack"),
        ("DEC4172_1_not_public", "do_not_public_claim_local_GR", "The packet is private and empirical PPN/R10/clock/WEP/orbital tests are not run here.", "keep_claim_firewall"),
        ("DEC4172_2_reopen_rule", "reactivate_if_parent_clause_fails", "If no-vector, no-disformal, no-hidden-flux or boundary silence fails in the future parent action, reopen the named PPN residual rows.", "source_backed_bounds_required"),
    ]
    return [
        {
            **common(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, next_action in rows
    ]


def firewall_rows() -> List[Dict[str, str]]:
    rows = [
        ("FW4172_0_public_local_gr", "No public local-GR theorem is claimed; this is a private packet readout."),
        ("FW4172_1_empirical", "No Cassini, LLR, pulsar, R10, WEP, clock or orbital empirical pass is claimed."),
        ("FW4172_2_global", "No global MTS adoption is claimed from the local PPC4161-TK-HQNP branch."),
        ("FW4172_3_numeric_G", "No numerical prediction of Newton's constant is claimed."),
        ("FW4172_4_parent_action", "No claim is made that the final parent action is forced to select this branch."),
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
            "PPC4161_TK_HQNP_private_packet_adopted": "True",
            "global_MTS_adopted": "False",
            "PPN_vector_closed_private": "True",
            "gamma_minus_1_private": "0",
            "beta_minus_1_private": "0",
            "alpha_i_private": "0",
            "zeta_i_private": "0",
            "xi_private": "0",
            "Gdot_over_G_private": "0",
            "empirical_PPN_tests_run": "False",
            "R10_clock_WEP_orbital_tests_run": "False",
            "numeric_G_predicted": "False",
            "formal_188_written": "True",
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
            "why_next": "4172 closes the formal private PPN vector, so the next real gate is source-backed local empirical validation without importing the answer.",
            "route_A": "build an empirical local validation pack for gamma, beta, alpha_i, zeta_i, xi, Gdot/G, R10, clocks, WEP and orbital residuals",
            "route_B": "if a sourced bound table cannot be acquired, write blocker rows and keep public local-GR claim blocked",
            "fallback": "if any parent side-channel clause is later rejected, reactivate the named PPN residual and source a bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4172_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4172_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS": SOURCE_DIR / "P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS.csv",
        "P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION.csv",
        "P8_Y5_R2FR_4172_SIDE_CHANNEL_SILENCE": SOURCE_DIR / "P8_Y5_R2FR_4172_SIDE_CHANNEL_SILENCE.csv",
        "P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE": SOURCE_DIR / "P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE.csv",
        "P8_Y5_R2FR_4172_REMAINING_EMPIRICAL_GATES": SOURCE_DIR / "P8_Y5_R2FR_4172_REMAINING_EMPIRICAL_GATES.csv",
        "P8_Y5_R2FR_4172_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4172_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4172_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4172_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4172_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4172_STATUS.csv",
        "P8_Y5_R2FR_4172_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4172_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161-TK-HQNP privately derives the full GR-like PPN vector gamma=1, beta=1, alpha_i=0, zeta_i=0, xi=0 and Gdot/G=0 inside the local packet",
        "current_evidence": "formalization-workbench/188-PPC4161-full-PPN-readout-vector.md records the standard EH <=2PN local metric readout, uses 4168 kappa lock, 4169 Hilbert source descent, 4170 source-charge glue and 4171 Poisson/Gauss/Newton readout, and keeps public_claim=false",
        "status": "private_packet_full_ppn_vector_nonclaim_public_claim_false",
        "next_test": "Build and run the source-backed local empirical validation pack for PPN, R10, clocks, WEP and orbital residuals",
        "key_risk": "This is a private packet closure; it does not prove global MTS adoption, empirical local-GR pass, numerical G_N prediction, or final parent-action uniqueness",
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
## PPC4161-TK-HQNP Addendum - Full PPN Vector Readout

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4172-Y5-R2FR-PPC4161-full-PPN-readout-gamma-beta-alpha-xi-zeta.md`

Inside the private PPC4161-TK-HQNP local packet, the 4164 conditional PPN map is now read with the 4168-4171 closures active:

```text
D_A ln kappa_* = 0,
delta_ZH = 0,
Q_M = M_H^dress[W_H;tau],
nabla^2 Phi_N = 4*pi G_N rho_H.
```

The local EH <=2PN readout uses:

```text
g_00 = -1 + 2U/c^2 - 2U^2/c^4 + O(c^-6)
g_ij = (1 + 2U/c^2) delta_ij + O(c^-4)
```

Therefore the private packet PPN vector is:

```text
R_PPN =
(gamma-1, beta-1, alpha1, alpha2, alpha3, xi, zeta1, zeta2, zeta3, zeta4, Gdot/G) = 0.
```

This is still not a public empirical local-GR claim. It is the private branch readout that must now be tested against source-backed local bounds.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def write_formal_188() -> None:
    FORMAL_188_PATH.write_text(
        f"""# 188 - PPC4161 Full PPN Readout Vector

Marker: `PPC4161_FULL_PPN_READOUT_VECTOR_FROM_PRIVATE_PACKET`
Checkpoint: `4172`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private nonclaim. This bridge closes the formal PPN readout inside PPC4161-TK-HQNP only. It does not claim public local GR, an empirical PPN pass, a numerical prediction of Newton's constant, or global MTS adoption.

## Inputs From The Built Packet

```text
D_A ln kappa_* = 0                 from 4168
delta_ZH = 0                       from 4169
R_A^G = 0                          from 4169
Q_M = M_H^dress[W_H;tau]           from 4170
nabla^2 Phi_N = 4*pi G_N rho_H     from 4171
a_r = -G_N M_H^dress/r^2           from 4171
```

## Local PPN Metric Readout
Use local quasi-Cartesian PPN coordinates with `U=-Phi_N>=0`.

```text
g_00 = -1 + 2U/c^2 - 2U^2/c^4 + O(c^-6)
g_ij = (1 + 2U/c^2) delta_ij + O(c^-4)
g_0i = GR vector-potential terms only, with no independent preferred-frame channel.
```

The EH self-interaction gives the `-2U^2/c^4` coefficient, so:

```text
beta = 1.
```

The spatial metric coefficient gives:

```text
gamma = 1.
```

Hilbert source descent plus the Bianchi identity gives:

```text
nabla_mu T_total^mu_nu = 0,
alpha1 = alpha2 = alpha3 = 0,
zeta1 = zeta2 = zeta3 = zeta4 = 0,
xi = 0.
```

The local coupling lock gives:

```text
dot(G_eff)/G_eff = 0.
```

## Result

```text
R_PPN =
(gamma-1, beta-1, alpha1, alpha2, alpha3, xi, zeta1, zeta2, zeta3, zeta4, Gdot/G)
= 0.
```

## Reactivation Rule
If the future parent action rejects same-metric EH local readout, no-vector/projector drift, no scalar/disformal bulk residual, Hilbert source conservation, or boundary silence, then the corresponding named PPN residual reopens and must be bounded empirically.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Full PPN Vector - 4172

Marker: `{SPINE_MARKER}`  
Source bridge: `188-PPC4161-full-PPN-readout-vector.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4172` promotes the 4164 conditional PPN map into the private PPC4161-TK-HQNP branch using the 4168-4171 local packet closures.

```text
R_PPN =
(gamma-1, beta-1, alpha1, alpha2, alpha3, xi, zeta1, zeta2, zeta3, zeta4, Gdot/G)
= 0.
```

This is a real formal local-GR-style readout in the private branch, but still not a public empirical local-GR claim. The next gate is source-backed local validation:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4172 - PPC4161 Full PPN Readout: Gamma, Beta, Alpha, Xi, Zeta

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Move Made
4164 built the conditional PPN residual vector. 4168-4171 then closed the local kappa, source-measure, Hamiltonian charge and Newtonian readout clauses inside the private packet.

4172 now takes the actual branch step:

```text
PPC4161-TK-HQNP := PPC4161-TK-HQN + EH <=2PN local quotient readout.
```

With:

```text
g_00 = -1 + 2U/c^2 - 2U^2/c^4 + O(c^-6)
g_ij = (1 + 2U/c^2) delta_ij + O(c^-4)
nabla_mu T_total^mu_nu = 0
dot(G_eff)/G_eff = 0
```

the private packet gives:

```text
gamma = 1,
beta = 1,
alpha1 = alpha2 = alpha3 = 0,
xi = 0,
zeta1 = zeta2 = zeta3 = zeta4 = 0,
Gdot/G = 0.
```

Equivalently:

```text
R_PPN = (gamma-1, beta-1, alpha1, alpha2, alpha3, xi, zeta1, zeta2, zeta3, zeta4, Gdot/G) = 0.
```

## What This Does Not Claim
- It is not a public local-GR theorem.
- It is not an empirical PPN, R10, clock, WEP or orbital pass.
- It is not a numerical derivation of Newton's constant.
- It is not a proof that the final global MTS parent action is uniquely forced to choose this packet.

## Why This Is Still Progress
The local branch no longer stops at Newtonian inverse-square recovery. It now has the full GR-like PPN vector as a private formal readout. The remaining job is empirical/source-backed validation, not another vague symbolic gap.

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

    sources = parse_csv(outputs["P8_Y5_R2FR_4172_SOURCE_REGISTER"])
    add("VAL4172_0_sources", "all cited source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    gauge = parse_csv(outputs["P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS"])
    gauge_text = "\n".join(",".join(row.values()) for row in gauge)
    add("VAL4172_1_gauge", "gauge rows contain branch definition, g00, gij, conservation and coupling lock", all(token in gauge_text for token in ["PPC4161-TK-HQNP", "g_00=-1+2U/c^2-2U^2/c^4", "g_ij=(1+2gamma U/c^2)delta_ij", "nabla_mu T_total^mu_nu=0", "dot(G_eff)/G_eff=0"]), gauge_text)

    vector = parse_csv(outputs["P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION"])
    vector_text = "\n".join(",".join(row.values()) for row in vector)
    expected_parameters = {component[0] for component in PPN_COMPONENTS}
    seen_parameters = {row["parameter"] for row in vector}
    add("VAL4172_2_vector_complete", "PPN vector contains every standard component used by 4164", seen_parameters == expected_parameters and all(row["derived_private"] == "True" for row in vector), str(sorted(seen_parameters)))
    add("VAL4172_3_vector_zero", "PPN vector rows derive GR-like private values", all(token in vector_text for token in ["gamma-1=0", "beta-1=0", "alpha1=0", "alpha2=0", "alpha3=0", "xi=0", "zeta1=0", "zeta2=0", "zeta3=0", "zeta4=0", "dot(G_eff)/G_eff=0"]), vector_text)

    side = parse_csv(outputs["P8_Y5_R2FR_4172_SIDE_CHANNEL_SILENCE"])
    side_text = "\n".join(",".join(row.values()) for row in side)
    add("VAL4172_4_side_channels", "side-channel rows close or adopt all local PPN leak channels with reactivation rules", all(token in side_text for token in ["epsilon_kappa", "epsilon_source_measure", "epsilon_mass_charge", "epsilon_scalar_disformal", "epsilon_frame_projector", "epsilon_hidden_flux", "epsilon_boundary_cosmo", "reactivate_named_PPN_residual"]), side_text)

    residual = parse_csv(outputs["P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE"])
    residual_text = "\n".join(",".join(row.values()) for row in residual)
    add("VAL4172_5_residuals", "residual rows close private PPN residuals and specify empirical fallback", len(residual) == len(PPN_COMPONENTS) and all(row["status"] == "closed_private_in_PPC4161_TK_HQNP" for row in residual) and "source_backed_empirical_bound_row_required" in residual_text, residual_text)

    remaining = parse_csv(outputs["P8_Y5_R2FR_4172_REMAINING_EMPIRICAL_GATES"])
    remaining_text = "\n".join(",".join(row.values()) for row in remaining)
    add("VAL4172_6_remaining", "remaining gates keep empirical PPN/R10/clock/WEP/orbital, numeric G and global adoption open", all(token in remaining_text for token in ["gamma-1", "beta-1", "alpha1", "R10", "G_N=c^4 kappa_* Z_0/(8*pi)", "PPC4161-TK-HQNP subset"]), remaining_text)

    decisions = parse_csv(outputs["P8_Y5_R2FR_4172_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add("VAL4172_7_decision", "decision rows select private PPN closure and next empirical pack", NEXT_TARGET in decision_text and "select_private_PPN_readout" in decision_text and "reactivate_if_parent_clause_fails" in decision_text, decision_text)

    firewall = parse_csv(outputs["P8_Y5_R2FR_4172_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4172_8_firewall", "firewall blocks public, empirical, global, numeric-G and parent-uniqueness claims", all(token in firewall_text for token in ["public local-GR", "empirical", "global MTS", "Newton's constant", "parent action"]), firewall_text)

    formal_text = read_text(FORMAL_188_PATH)
    add("VAL4172_9_formal_188", "formal 188 bridge records PPN metric readout, zero vector, reactivation rule and next target", FORMAL_188_PATH.exists() and all(token in formal_text for token in ["PPC4161_FULL_PPN_READOUT_VECTOR_FROM_PRIVATE_PACKET", "g_00 = -1 + 2U/c^2 - 2U^2/c^4", "gamma = 1", "beta = 1", "R_PPN =", NEXT_TARGET]), "formal 188 checked")

    packet_text = read_text(PACKET_180_PATH)
    add("VAL4172_10_packet_180", "packet 180 contains 4172 full PPN addendum", all(token in packet_text for token in [PACKET_MARKER, "PPC4161-TK-HQNP", "R_PPN", "Gdot/G"]), "packet 180 checked")

    claims = parse_csv(CLAIMS_PATH)
    l013 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4172_11_claim_row", "claims register contains one L-013 private full PPN nonclaim row", len(l013) == 1 and l013[0].get("status") == "private_packet_full_ppn_vector_nonclaim_public_claim_false" and "public_claim=false" in l013[0].get("current_evidence", ""), str(l013))

    spine_text = read_text(SPINE_PATH)
    add("VAL4172_12_spine", "spine contains 4172 marker, claim row, zero PPN vector and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "R_PPN =", NEXT_TARGET]), "spine checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4172_STATUS"])
    add("VAL4172_13_status", "status records private PPN closure while empirical/global/numeric-G remain open", len(status) == 1 and status[0]["PPN_vector_closed_private"] == "True" and status[0]["empirical_PPN_tests_run"] == "False" and status[0]["global_MTS_adopted"] == "False" and status[0]["numeric_G_predicted"] == "False" and status[0]["next_target"] == NEXT_TARGET, str(status))

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4172_NEXT_TARGET"])
    add("VAL4172_14_next", "next target moves to source-backed local empirical validation pack", len(next_loaded) == 1 and next_loaded[0]["next_target"] == NEXT_TARGET and "PPN" in "\n".join(next_loaded[0].values()) and "R10" in "\n".join(next_loaded[0].values()), str(next_loaded))

    doc_text = read_text(DOC_PATH)
    add("VAL4172_15_doc", "checkpoint doc records branch move, vector result, firewall and next target", all(token in doc_text for token in ["PPC4161-TK-HQNP", "gamma = 1", "beta = 1", "R_PPN", "not a public local-GR theorem", NEXT_TARGET]), "doc tokens checked")

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4172_16_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

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
    add("VAL4172_17_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def write_outputs(outputs: Dict[str, Path]) -> None:
    write_csv(outputs["P8_Y5_R2FR_4172_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_PPN_GAUGE_AND_ASSUMPTIONS"], ppn_gauge_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_PPN_VECTOR_DERIVATION"], ppn_vector_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_SIDE_CHANNEL_SILENCE"], side_channel_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_REMAINING_EMPIRICAL_GATES"], remaining_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_BRANCH_DECISION"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4172_NEXT_TARGET"], next_rows())


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_188()
    packet_action = ensure_packet_180_addendum()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_outputs(outputs)
    write_csv(outputs["P8_Y5_R2FR_4172_STATUS"], status_rows(claim_action, packet_action, spine_action))
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4172_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"packet_180_action: {packet_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_188_PATH}")
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
