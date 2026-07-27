from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()

CHECKPOINT = "4211"
CLAIM_ID = "L-052"
BRANCH_ID = "MTS_R2FR_Y5_HTAU_MHSOURCE_PARENT_CHARGE_OWNER_4211"
DECISION = (
    "HTAU_MHSOURCE_PARENT_CHARGE_OWNER_CONTRACT_WRITTEN_INTEGRABILITY_REFERENCE_"
    "POSITIVITY_AND_SAME_SOURCE_UNSIGNED_VISIBLE_MATTER_SCORECARD_READY_NONCLAIM"
)
FORMAL_PATH = FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md"
DOC_PATH = POST / "4211-Y5-R2FR-Htau-MHsource-parent-charge-owner-or-visible-matter-residual-scorecard.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_MARKER = "PPC4161_HTAU_MHSOURCE_PARENT_CHARGE_OWNER_4211"
PACKET_MARKER = "PPC4161_PACKET_HTAU_MHSOURCE_PARENT_CHARGE_OWNER_4211"
NEXT_TARGET = "4212-Y5-R2FR-Htau-integrability-first-operator-or-source-scorecard-first-row.md"

SOURCES = {
    "SRC4211_00_4210_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4210_NEXT_TARGET.csv",
        "H_tau/M_H",
        "4210 selected the source-charge pressure point.",
    ),
    "SRC4211_01_226_visible": (
        FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md",
        "epsilon_visible_EM_total =",
        "4210 visible matter residual envelope.",
    ),
    "SRC4211_02_186_htau_glue": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref",
        "Hamiltonian worldtube mass readout glue.",
    ),
    "SRC4211_03_187_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "int_W rho_H dV = M_H^dress",
        "Newton readout requires same source charge.",
    ),
    "SRC4211_04_190_parent_selector": (
        FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md",
        "Hamiltonian/worldtube charge readout;",
        "Parent selector requires the Hamiltonian/worldtube readout.",
    ),
    "SRC4211_05_192_boundary": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "delta H_tau = int_partialW",
        "Boundary/no-flux sector interface.",
    ),
    "SRC4211_06_194_gcal": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "No orbital `GM`",
        "Calibrated G bridge forbids orbital-GM source shortcut.",
    ),
    "SRC4211_07_1015_same_object": (
        POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "current MTS lacks parent worldtube/source-measure/class",
        "Same-object equality remains unsigned.",
    ),
    "SRC4211_08_1017_integrability": (
        POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "Pi_M^H is only notation.",
        "Hamiltonian source charge is notation until integrability/reference/denominator lock.",
    ),
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def common() -> Dict[str, str]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT}


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


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def owner_contract_rows() -> List[Dict[str, str]]:
    items = [
        (
            "HMO4211_0_same_source_worldtube",
            "same Hilbert source worldtube",
            "W_H is fixed by the parent visible-matter/Hilbert support before Newton, PPN, clock, or orbital readout",
            "unsigned_current_branch",
            "1015 says same-object worldtube/source-measure/class is not parent-signed",
        ),
        (
            "HMO4211_1_visible_matter_inclusion",
            "visible matter import is inside the source",
            "J_H_total and T_H include S_vis from 4210 before building rho_H or M_H^dress",
            "contract_written_nonclaim",
            "visible constants may be calibrated, but any MTS-specific deviations feed epsilon_visible_EM_total",
        ),
        (
            "HMO4211_2_covariant_phase_space_owner",
            "parent theta/Q_tau decomposition",
            "delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total) is computed from the parent local packet action",
            "unsigned_current_branch",
            "explicit L_X, theta_X, Q_X and omega_X decomposition is still missing",
        ),
        (
            "HMO4211_3_integrability",
            "Hamiltonian integrability",
            "field-space curl of delta H_tau vanishes or is bounded on the chosen source surface family",
            "unsigned_current_branch",
            "1017 retained delta_H_tau_nonintegrable_over_MH as missing",
        ),
        (
            "HMO4211_4_reference_lock",
            "fixed reference subtraction",
            "H_ref is selected once by a parent rule and cannot absorb source calibration or radial drift",
            "unsigned_current_branch",
            "reference shift Delta_ref_over_MH remains missing",
        ),
        (
            "HMO4211_5_tau_frame_lock",
            "same tau/coframe/source frame",
            "tau_source=tau_charge=tau_clock=tau_readout and the observed coframe are locked before comparing arenas",
            "unsigned_current_branch",
            "no same-frame tau certificate exists yet",
        ),
        (
            "HMO4211_6_positive_denominator",
            "positive stable M_H_ref",
            "M_H_ref is a same-frame positive dressed source charge denominator, not a bare mass or orbital GM",
            "unsigned_current_branch",
            "M_H_ref remains source-ready but unfilled",
        ),
        (
            "HMO4211_7_boundary_silence",
            "boundary and symplectic flux silence",
            "linked surfaces in the source-free collar have zero or bounded symplectic/boundary leakage",
            "unsigned_current_branch",
            "192 routes nonzero radiative/boundary terms back into charge rows",
        ),
        (
            "HMO4211_8_anti_circularity",
            "no orbital-GM denominator",
            "M_H^dress is defined before orbital acceleration, fitted GM, or measured numerical G enters",
            "guardrail_written",
            "194 forbids using orbital GM to define the source mass the theorem is meant to derive",
        ),
        (
            "HMO4211_9_claim_gate",
            "local GR source-charge claim gate",
            "source charge owner closes only if HMO4211_0 through HMO4211_8 are parent-signed or quantitatively bounded",
            "fails_current_claim",
            "integrability, reference, tau, denominator, and same-source equality remain unsigned",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": item[0],
            "clause": item[1],
            "required_condition": item[2],
            "status": item[3],
            "current_issue": item[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for item in items
    ]


def residual_scorecard_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "SCR4211_0_delta_Htau",
            "delta_H_tau_nonintegrable_over_MH",
            "field-space curl obstruction of the Hamiltonian source charge normalized by M_H_ref",
            "dimensionless",
            "MISSING_INTEGRABILITY_THEOREM_OR_NUMERIC_ROW",
            "R10;PPN;clocks;orbital;Newton",
        ),
        (
            "SCR4211_1_Delta_ref",
            "Delta_ref_over_MH",
            "reference subtraction shift/drift normalized by M_H_ref",
            "dimensionless",
            "MISSING_PARENT_REFERENCE_RULE",
            "R10;PPN;clocks;orbital;Newton",
        ),
        (
            "SCR4211_2_boundary_flux",
            "symplectic_boundary_flux_over_MH",
            "linked-surface boundary or symplectic leakage normalized by M_H_ref",
            "dimensionless",
            "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "R10;PPN;clocks;orbital;Newton",
        ),
        (
            "SCR4211_3_worldtube_domain",
            "Delta_worldtube_domain",
            "mismatch between Hilbert source worldtube, topological representative, and readout domain",
            "dimensionless_or_set_distance",
            "MISSING_PARENT_WORLD_TUBE_SELECTOR",
            "R10;PPN;orbital;Newton",
        ),
        (
            "SCR4211_4_PiM_metric",
            "Delta_PiM_metric",
            "difference between Pi_M/Hilbert charge map and observed source metric/coframe readout",
            "dimensionless",
            "MISSING_SOURCE_MEASURE_EQUALITY",
            "PPN;clocks;orbital;Newton",
        ),
        (
            "SCR4211_5_visible_EM",
            "epsilon_visible_EM_total",
            "absolute visible-sector deviation envelope imported from 4210",
            "dimensionless",
            "MISSING_NUMERIC_COMPONENTS_BUT_SCHEMA_READY",
            "R10;WEP;clocks;PPN;source_mass",
        ),
        (
            "SCR4211_6_alpha_guard",
            "alpha_total_guard(lambda)",
            "side-channel guard for alpha/Hodge/current/material/radiative EM deviations versus local bounds",
            "bound_function",
            "MISSING_ALPHA_BOUND_INPUTS_AND_PARENT_SCALE_LAW",
            "R10;clocks;WEP;PPN",
        ),
        (
            "SCR4211_7_MHref",
            "M_H_ref",
            "positive same-frame Hamiltonian source-charge denominator",
            "mass_or_charge_normalization",
            "MISSING_STABLE_MH_REF",
            "R10;PPN;clocks;orbital;Newton",
        ),
        (
            "SCR4211_8_total",
            "epsilon_source_charge_total",
            "no-cancellation envelope: |delta_H_tau|+|Delta_ref|+|boundary_flux|+|domain|+|PiM_metric|+epsilon_visible_EM_total",
            "dimensionless_after_MHref_normalization",
            "NOT_COMPUTED_ALL_COMPONENTS_MISSING",
            "R10;PPN;clocks;orbital;Newton",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row[0],
            "quantity": row[1],
            "definition": row[2],
            "units": row[3],
            "numeric_value": "MISSING",
            "status": row[4],
            "affected_arenas": row[5],
            "source_path": "MISSING_SOURCE_OR_THEOREM_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def route_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "HMR4211_0_parent_owner",
            "Parent-sign source charge",
            "derive same-source worldtube, theta/Q_tau, integrability, fixed H_ref, tau lock, positive M_H_ref and boundary silence",
            "would reopen Newton/local-GR source closure",
            "preferred_derivation_route",
        ),
        (
            "HMR4211_1_scorecard",
            "Fill residual scorecard",
            "source or bound delta_H_tau, Delta_ref, boundary_flux, worldtube/domain, PiM_metric, visible_EM and M_H_ref",
            "keeps branch empirical and nonclaim until rows are real",
            "fallback_nonclaim_route",
        ),
        (
            "HMR4211_2_calibrated_visible",
            "Use calibrated visible matter only",
            "import standard visible matter constants as q-basic readout constants while quarantining MTS-specific deviations",
            "allowed for GR-style local readout but not alpha prediction",
            "safe_baseline_route",
        ),
        (
            "HMR4211_3_forbidden_shortcut",
            "Forbid orbital-GM closure",
            "do not define M_H_ref or M_H^dress from fitted orbital GM, acceleration, or measured G",
            "would make the derivation circular",
            "forbidden_route",
        ),
    ]
    return [
        {
            **common(),
            "route_id": row[0],
            "route": row[1],
            "action": row[2],
            "effect": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4211_0",
            "decision": DECISION,
            "source_charge_owner_contract_written": "True",
            "visible_matter_included": "True",
            "Htau_integrability_signed": "False",
            "H_ref_fixed_by_parent": "False",
            "M_H_ref_positive_source_backed": "False",
            "same_worldtube_source_measure_signed": "False",
            "orbital_GM_shortcut_allowed": "False",
            "source_charge_scorecard_ready": "True",
            "Newton_local_GR_claim": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    blocks = [
        ("FW4211_0_Newton", "Newton source-mass derivation", "blocked_until_Htau_MHdress_parent_owned"),
        ("FW4211_1_local_GR", "local GR reduction claim", "blocked_until_source_charge_owner_and_PPN_residuals_close"),
        ("FW4211_2_R10", "R10/local fifth-force pass", "blocked_until_M_H_ref_and_all_source_residual_rows_are_real"),
        ("FW4211_3_PPN", "PPN pass", "blocked_until_delta_Htau_Delta_ref_boundary_PiM_visible_EM_rows_bound"),
        ("FW4211_4_clocks", "clock/local-time pass", "blocked_until_tau_frame_lock_and_visible_EM_residuals_bound"),
        ("FW4211_5_orbits", "orbital readout pass", "blocked_until_orbital_GM_not_used_as_denominator"),
        ("FW4211_6_alpha", "MTS alpha prediction", "blocked_until_parent_gJ_lambdaA_scale_law_exists"),
    ]
    return [
        {
            **common(),
            "firewall_id": row[0],
            "claim_family": row[1],
            "blocker": row[2],
            "status": "blocked_nonclaim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in blocks
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4211",
            "status": "source_charge_owner_contract_written_scorecard_ready_nonclaim",
            "strong_result": "the exact source-charge owner contract now exists as a gate, not a vague missing item",
            "weak_result": "current MTS still lacks parent-signed H_tau integrability, fixed H_ref, positive M_H_ref, tau lock and same-source equality",
            "project_effect": "local GR route remains alive but cannot be claimed until the source-charge denominator and numerator rows close",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target": NEXT_TARGET,
            "why": "4211 turns H_tau/M_Hdress into a clause-by-clause owner gate; the next useful leap is to attack the first hard clause directly rather than circle the whole gate.",
            "route_A": "derive H_tau integrability from explicit theta_total/Q_tau/omega_total for the local packet sector",
            "route_B": "if derivation fails, fill first source-charge scorecard row with a real theorem-zero or numeric bound",
            "route_C": "keep calibrated visible matter and alpha prediction quarantines intact",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""# 227 - PPC4161 Htau MHsource Parent Charge Owner

Marker: `{SPINE_MARKER}`
Checkpoint: `{CHECKPOINT}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Purpose

This checkpoint turns the remaining source-mass gap into an exact owner contract. The Newton/GR branch is not allowed to use a fitted orbital `GM`, a bare mass, or a reference-only normalization as the source charge. It must use a parent-owned Hamiltonian/Hilbert charge:

```text
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
int_W rho_H dV_H = M_H^dress[W_H;tau]
```

4210 permits calibrated standard visible matter constants in the local readout. 4211 asks the harder question: whether that visible source is the same object as the Hamiltonian charge that sources the Newton/GR limit.

## Owner Contract

The source-charge bridge is claim-grade only if all clauses hold in the same branch:

1. `W_H` is the compact Hilbert source worldtube fixed before readout.
2. `S_vis` from 4210 is included in `J_H_total` and `T_H`.
3. `theta_total`, `Q_tau`, and `omega_total` are computed from the parent local packet action.
4. `delta H_tau[S]=int_S(delta Q_tau-i_tau theta_total)` is integrable on the chosen surface family.
5. `H_ref` is selected once by the parent rule and is derivative-silent under source/radius/frame changes.
6. `tau_source=tau_charge=tau_clock=tau_readout` and the observed coframe are locked.
7. `M_H_ref` is positive, stable, same-frame, and source-backed.
8. boundary/symplectic/radiative leakage in the local collar is zero or explicitly bounded.
9. no orbital `GM`, fitted acceleration, or measured numerical `G` defines `M_H^dress`.

If any clause is unsigned, the result is not local GR. It is a residual scorecard.

## Residual Envelope

The current nonclaim envelope is:

```text
epsilon_source_charge_total =
|delta_H_tau_nonintegrable_over_MH|
+ |Delta_ref_over_MH|
+ |symplectic_boundary_flux_over_MH|
+ |Delta_worldtube_domain|
+ |Delta_PiM_metric|
+ epsilon_visible_EM_total.
```

`M_H_ref` is part of the gate, not a free denominator. If it is missing, every normalized row remains nonclaim.

## Result

The contract is now explicit and source-backed, but not closed. Current MTS still lacks the parent-owned integrability/reference/denominator signatures required to claim the local Newton/GR source mass bridge.

## Next Target

`{NEXT_TARGET}` should attack the first hard clause: construct the explicit local-packet `theta_total/Q_tau/omega_total` operator and try to prove Hamiltonian integrability, or fill the first real source-scorecard row.
"""


def checkpoint_doc() -> str:
    return f"""# 4211 Y5 R2FR Htau MHsource parent charge owner or visible matter residual scorecard

**Status:** `{DECISION}`.

**What moved forward:** the `H_tau/M_H^dress` problem is no longer a vague blocker. It is a clause-by-clause parent owner contract with a named residual scorecard and an anti-circularity firewall.

**Claim ceiling:** no Newton source-mass derivation, local-GR claim, R10 pass, PPN pass, clock pass, orbital pass, or MTS alpha prediction is allowed from 4211.

## Key law

```text
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
int_W rho_H dV_H = M_H^dress[W_H;tau]
```

## Current verdict

The route is still viable but not closed: same-source worldtube, Hamiltonian integrability, fixed reference, tau/coframe lock, positive `M_H_ref`, and boundary silence are not parent-signed in the current packet.

## Files written

- `formalization-workbench\\227-PPC4161-Htau-MHsource-parent-charge-owner.md`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4211_HTAU_MHSOURCE_OWNER_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4211_SOURCE_CHARGE_RESIDUAL_SCORECARD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_4211_DECISION.csv`

## Next target

`{NEXT_TARGET}`.
"""


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker not in text:
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n" + block.strip() + "\n")


def update_registers() -> None:
    claim_row = (
        f'{CLAIM_ID},local_gr,'
        f'"The H_tau/M_Hdress parent source-charge owner contract is written: Newton/local-GR source mass must come from a same-worldtube Hamiltonian/Hilbert charge with integrable H_tau, fixed H_ref, tau/coframe lock, positive M_H_ref, boundary silence and no orbital-GM shortcut; current MTS retains a visible-matter/source-charge residual scorecard and makes no claim.",'
        f'"4211 source audit, owner contract, residual scorecard, route matrix, decision row and firewall.",'
        f'private_Htau_MHsource_owner_contract_nonclaim_scorecard_ready,'
        f'"Derive theta_total/Q_tau/omega_total integrability for the local packet sector or fill the first source-charge scorecard row with a real theorem-zero or numeric bound.",'
        f'"The bridge is promising only if M_Hdress is parent-owned; using orbital GM or a reference denominator would be circular."'
    )
    if f"{CLAIM_ID}," not in read_text(CLAIMS_PATH):
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(claim_row + "\n")

    spine_block = f"""### PPC4161 Htau MHsource Parent Charge Owner - 4211

Marker: `{SPINE_MARKER}`
Claim register row: `{CLAIM_ID}`

4211 fixes the local source-mass bridge into a hard contract:

```text
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
int_W rho_H dV_H = M_H^dress[W_H;tau].
```

The branch remains nonclaim until same-source worldtube, Hamiltonian integrability, fixed reference, tau/coframe lock, positive `M_H_ref`, boundary silence, and the no-orbital-GM guard are all parent-owned or bounded."""
    append_once(SPINE_PATH, SPINE_MARKER, spine_block)

    packet_block = f"""## PPC4161 Packet Htau MHsource Parent Charge Owner - 4211

Marker: `{PACKET_MARKER}`

The packet now treats `H_tau/M_H^dress` as the root source-charge gate. Visible matter is imported from 4210, but Newton/local-GR closure is still blocked until the Hamiltonian charge denominator and numerator residuals close without orbital-GM circularity."""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)


def validate(rows_by_file: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    source = rows_by_file["P8_Y5_R2FR_4211_SOURCE_REGISTER.csv"]
    contract = rows_by_file["P8_Y5_R2FR_4211_HTAU_MHSOURCE_OWNER_CONTRACT.csv"]
    scorecard = rows_by_file["P8_Y5_R2FR_4211_SOURCE_CHARGE_RESIDUAL_SCORECARD.csv"]
    routes = rows_by_file["P8_Y5_R2FR_4211_ROUTE_MATRIX.csv"]
    decision = rows_by_file["P8_Y5_R2FR_4211_DECISION.csv"][0]
    firewall = rows_by_file["P8_Y5_R2FR_4211_CLAIM_FIREWALL.csv"]
    all_rows_flat = [row for rows in rows_by_file.values() for row in rows]
    required_clauses = {
        "HMO4211_0_same_source_worldtube",
        "HMO4211_1_visible_matter_inclusion",
        "HMO4211_2_covariant_phase_space_owner",
        "HMO4211_3_integrability",
        "HMO4211_4_reference_lock",
        "HMO4211_5_tau_frame_lock",
        "HMO4211_6_positive_denominator",
        "HMO4211_7_boundary_silence",
        "HMO4211_8_anti_circularity",
        "HMO4211_9_claim_gate",
    }
    required_quantities = {
        "delta_H_tau_nonintegrable_over_MH",
        "Delta_ref_over_MH",
        "symplectic_boundary_flux_over_MH",
        "Delta_worldtube_domain",
        "Delta_PiM_metric",
        "epsilon_visible_EM_total",
        "alpha_total_guard(lambda)",
        "M_H_ref",
        "epsilon_source_charge_total",
    }
    checks = [
        ("VAL4211_0_sources_exist", "all source paths exist", all(row["exists"] == "True" for row in source)),
        ("VAL4211_1_source_needles", "all source needles found", all(row["required_text_found"] == "True" for row in source)),
        ("VAL4211_2_contract_complete", "owner contract contains every required clause", required_clauses.issubset({row["contract_id"] for row in contract})),
        ("VAL4211_3_visible_included", "visible matter inclusion is explicit", any(row["contract_id"] == "HMO4211_1_visible_matter_inclusion" for row in contract)),
        ("VAL4211_4_anti_circularity", "orbital-GM shortcut is forbidden", any(row["contract_id"] == "HMO4211_8_anti_circularity" and row["status"] == "guardrail_written" for row in contract)),
        ("VAL4211_5_scorecard_complete", "source-charge scorecard covers all retained rows", required_quantities.issubset({row["quantity"] for row in scorecard})),
        ("VAL4211_6_scorecard_missing", "scorecard remains missing/nonclaim", all(row["numeric_value"] == "MISSING" for row in scorecard)),
        ("VAL4211_7_routes", "route matrix covers owner, scorecard, baseline and forbidden shortcut", {"HMR4211_0_parent_owner", "HMR4211_1_scorecard", "HMR4211_2_calibrated_visible", "HMR4211_3_forbidden_shortcut"}.issubset({row["route_id"] for row in routes})),
        ("VAL4211_8_decision_nonclaim", "decision keeps source and local-GR claims false", decision["Htau_integrability_signed"] == "False" and decision["Newton_local_GR_claim"] == "False"),
        ("VAL4211_9_firewall", "firewall blocks all local arenas", {"Newton source-mass derivation", "local GR reduction claim", "R10/local fifth-force pass", "PPN pass", "clock/local-time pass", "orbital readout pass", "MTS alpha prediction"}.issubset({row["claim_family"] for row in firewall})),
        ("VAL4211_10_no_claim_flags", "all generated claim flags remain false", all(row.get("claim_allowed", "False") == "False" and row.get("valid_for_claim", "False") == "False" for row in all_rows_flat)),
        ("VAL4211_11_docs_written", "formal and checkpoint docs written", FORMAL_PATH.exists() and DOC_PATH.exists()),
        ("VAL4211_12_claim_register", "claim register contains L-052", CLAIM_ID + "," in read_text(CLAIMS_PATH)),
        ("VAL4211_13_spine_marker", "spine marker present", SPINE_MARKER in read_text(SPINE_PATH)),
        ("VAL4211_14_packet_marker", "packet marker present", PACKET_MARKER in read_text(PACKET_PATH)),
    ]
    return [
        {
            **common(),
            "check_id": check_id,
            "check": check,
            "passed": str(bool(passed)),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, check, passed in checks
    ]


def write_all() -> None:
    FORMAL_PATH.write_text(formal_doc(), encoding="utf-8", newline="\n")
    DOC_PATH.write_text(checkpoint_doc(), encoding="utf-8", newline="\n")
    rows_by_file = {
        "P8_Y5_R2FR_4211_SOURCE_REGISTER.csv": source_rows(),
        "P8_Y5_R2FR_4211_HTAU_MHSOURCE_OWNER_CONTRACT.csv": owner_contract_rows(),
        "P8_Y5_R2FR_4211_SOURCE_CHARGE_RESIDUAL_SCORECARD.csv": residual_scorecard_rows(),
        "P8_Y5_R2FR_4211_ROUTE_MATRIX.csv": route_rows(),
        "P8_Y5_R2FR_4211_DECISION.csv": decision_rows(),
        "P8_Y5_R2FR_4211_CLAIM_FIREWALL.csv": firewall_rows(),
        "P8_Y5_R2FR_4211_STATUS.csv": status_rows(),
        "P8_Y5_R2FR_4211_NEXT_TARGET.csv": next_target_rows(),
    }
    for filename, rows in rows_by_file.items():
        write_csv(SOURCE_DIR / filename, rows)
    update_registers()
    validation = validate(rows_by_file)
    write_csv(SOURCE_DIR / "P8_Y5_BRR545_4211_VALIDATION.csv", validation)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    write_all()
    print(DECISION)
    print(f"formal={FORMAL_PATH}")
    print(f"checkpoint={DOC_PATH}")
    print(f"validation={SOURCE_DIR / 'P8_Y5_BRR545_4211_VALIDATION.csv'}")
    print("rows=15 validation checks")


if __name__ == "__main__":
    main()
