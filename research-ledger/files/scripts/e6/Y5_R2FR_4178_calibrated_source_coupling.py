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

CHECKPOINT = "4178"
BRANCH_ID = "MTS_R2FR_Y5_CALIBRATED_SOURCE_COUPLING_4178"
DECISION = "KAPPA_TO_GN_CALIBRATED_SOURCE_COUPLING_DERIVED_NUMERIC_G_NOT_PREDICTED_PRIVATE_SELECTOR"
DOC_PATH = POST / "4178-Y5-R2FR-calibrated-source-coupling-kappa-GN-normalization-or-measured-G-envelope.md"
FORMAL_194_PATH = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
PACKET_180_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-019"
SPINE_MARKER = "PPC4161_CALIBRATED_SOURCE_COUPLING_4178"
PACKET_MARKER = "PPC4161_PACKET_CALIBRATED_SOURCE_COUPLING_4178"
NEXT_TARGET = "4179-Y5-R2FR-local-GR-private-closure-summary-and-global-parent-adoption-burden-map.md"

SOURCES = {
    "SRC4178_00_4177_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4177_NEXT_TARGET.csv",
        "derive kappa_* to G_N",
        "4177 handoff to calibrated source coupling.",
    ),
    "SRC4178_01_formal_181": (
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "G_N = c^4 kappa_eff/(8*pi)",
        "181 coupling relation and numerical-G nonprediction.",
    ),
    "SRC4178_02_formal_184": (
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "D_A ln kappa_* = 0",
        "184 private topological kappa lock.",
    ),
    "SRC4178_03_formal_185": (
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "delta_ZH = 0",
        "185 source-measure descent and delta-ZH closure.",
    ),
    "SRC4178_04_formal_186": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "No orbital `GM`",
        "186 anti-circular Hamiltonian/worldtube mass readout glue.",
    ),
    "SRC4178_05_formal_187": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H",
        "187 weak-field Poisson/Gauss/Newton readout.",
    ),
    "SRC4178_06_formal_188": (
        FORMAL / "188-PPC4161-full-PPN-readout-vector.md",
        "R_PPN =",
        "188 full private PPN vector readout.",
    ),
    "SRC4178_07_formal_193": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "source_normalization",
        "4177 guard preventing vertical dependence in source normalization.",
    ),
    "SRC4178_08_claim_L018": (
        CLAIMS_PATH,
        "quotient-natural action/matter/readout/source descent",
        "Previous private selector claim row before calibrated source coupling.",
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


def coupling_chain_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "KGL4178_0_EH_block",
            "local EH source equation",
            "G_mu_nu[g_obs] = kappa_eff T_H_mu_nu",
            "same observed metric and same Hilbert source define the local gravitational coupling",
            "derived_private_selector",
        ),
        (
            "KGL4178_1_source_measure",
            "source-measure normalization",
            "kappa_eff = kappa_* Z_0 with delta_ZH=0",
            "Z_H has no species, range, readout, frame, clock or environment leakage inside the private branch",
            "derived_private_selector",
        ),
        (
            "KGL4178_2_kappa_lock",
            "local coupling constancy",
            "D_A ln kappa_* = 0 and D_A delta_ZH = 0 => D_A ln kappa_eff = 0",
            "the calibrated coupling is locally constant across PPN, clock, WEP, R10 and orbital readouts",
            "derived_private_selector",
        ),
        (
            "KGL4178_3_G_relation",
            "Newtonian coupling definition",
            "G_cal := c^4 kappa_eff/(8*pi)",
            "the local field equation takes the GR-normalized source form with a calibrated constant",
            "derived_private_selector",
        ),
        (
            "KGL4178_4_Poisson",
            "weak-field 00 equation",
            "G_00^lin = 2 nabla^2 Phi_N/c^2 and T_00=rho_H c^2 => nabla^2 Phi_N=4*pi G_cal rho_H",
            "the Poisson coefficient follows from the EH block and the same Hilbert source",
            "derived_private_selector",
        ),
        (
            "KGL4178_5_mass_charge",
            "Hamiltonian mass charge",
            "int_W rho_H dV = M_H^dress[W_H;tau]",
            "the mass entering Newton's law is the Hamiltonian/Hilbert worldtube charge, not fitted orbital GM",
            "derived_private_selector",
        ),
        (
            "KGL4178_6_orbital_readout",
            "Newtonian acceleration",
            "Phi_N=-G_cal M_H^dress/r and a_r=-G_cal M_H^dress/r^2",
            "orbital motion tests the derived source law after choosing/calibrating G_cal",
            "derived_private_selector",
        ),
        (
            "KGL4178_7_numeric_value",
            "numerical value of G",
            "numeric(G_cal) is empirical unless parent theory derives the dimensionful kappa_* scale",
            "this matches GR practice; it is not a fundamental MTS prediction",
            "not_predicted_firewall",
        ),
    ]
    return [
        {
            **common(),
            "chain_id": chain_id,
            "step": step,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for chain_id, step, formula, meaning, status in rows
    ]


def anti_circularity_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "AC4178_0_no_orbital_GM_input",
            "No orbital GM input defines the source mass.",
            "M_H^dress is defined by H_tau[S]-H_ref before orbital readout.",
            "closed_private",
        ),
        (
            "AC4178_1_no_measured_G_input",
            "No measured numerical G defines kappa_*.",
            "G_cal is the calibrated name of c^4 kappa_eff/(8*pi), not a parent prediction.",
            "firewall_active",
        ),
        (
            "AC4178_2_no_source_label_absorption",
            "No source label is absorbed into G.",
            "4177 requires D_v source_normalization=0 and 185 sets delta_ZH=0.",
            "closed_private",
        ),
        (
            "AC4178_3_no_species_clock_range_G",
            "No separate species, clock, range or frame G exists.",
            "D_A ln G_cal=0 for A in time/species/frame/range/environment/readout.",
            "closed_private",
        ),
        (
            "AC4178_4_GR_comparison",
            "Calibration is not a cheat if labelled.",
            "GR also treats G as empirical; the win condition is structural reduction plus no hidden residuals, not numerical G prediction.",
            "discipline_rule",
        ),
    ]
    return [
        {
            **common(),
            "guard_id": guard_id,
            "guard": guard,
            "implementation": implementation,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for guard_id, guard, implementation, status in rows
    ]


def measured_g_envelope_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "MGE4178_0_G_cal",
            "G_cal",
            "c^4 kappa_eff/(8*pi)",
            "calibrated_constant",
            "use one empirical value across local tests unless parent scale law is derived",
            "not_numeric_prediction",
        ),
        (
            "MGE4178_1_kappa_eff",
            "kappa_eff",
            "kappa_* Z_0",
            "constant_private_selector",
            "D_A ln kappa_eff=0 after kappa lock and delta_ZH=0",
            "not_parent_global",
        ),
        (
            "MGE4178_2_MH",
            "M_H^dress",
            "H_tau[S_link]-H_ref",
            "Hamiltonian_worldtube_charge",
            "mass source is defined before orbital comparison",
            "not_orbital_fit",
        ),
        (
            "MGE4178_3_mu_theory",
            "mu_theory",
            "G_cal M_H^dress",
            "predicted_readout_after_calibration",
            "orbital GM compares to this product without feeding it back into M_H or kappa_*",
            "testable_not_input",
        ),
        (
            "MGE4178_4_drift_residual",
            "R_A^G",
            "D_A ln G_cal",
            "zero_private_selector",
            "reactivates if kappa_* lock, delta_ZH, quotient source normalization, or Hilbert source descent fails",
            "bound_if_reactivated",
        ),
        (
            "MGE4178_5_parent_scale_missing",
            "numeric_G_parent_scale",
            "kappa_0 or dimensionful parent invariant",
            "missing_for_fundamental_prediction",
            "needed only for claiming MTS predicts the numerical value of Newton's constant",
            "missing_not_local_GR_failure",
        ),
    ]
    return [
        {
            **common(),
            "envelope_id": envelope_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "rule": rule,
            "claim_note": claim_note,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for envelope_id, quantity, definition, status, rule, claim_note in rows
    ]


def reactivation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "RE4178_0_kappa_drift",
            "kappa_* drift",
            "D_A ln kappa_* != 0",
            "reopen Gdot/G, clock, PPN and range residual rows",
        ),
        (
            "RE4178_1_ZH_leak",
            "source measure leak",
            "delta_ZH or D_A delta_ZH nonzero",
            "reopen WEP, species, material, readout and R10/R11 source-normalization rows",
        ),
        (
            "RE4178_2_wrong_mass_charge",
            "Pi_M/H_tau/worldtube mismatch",
            "M_H^dress not equal to Hilbert source charge",
            "reopen measured-GM obstruction vector and orbital residual rows",
        ),
        (
            "RE4178_3_hidden_source_constants",
            "hidden constants or source labels",
            "D_v theta_A, m_A, alpha_EM or source_normalization nonzero",
            "reopen 4177 projector residual and WEP/clock/source-normalization rows",
        ),
        (
            "RE4178_4_boundary_flux",
            "unrouted boundary flux",
            "F_boundary or edge charge enters measured mass",
            "reopen 4176 boundary/transition current rows",
        ),
        (
            "RE4178_5_numeric_G_claim",
            "numerical G prediction attempted",
            "numeric value of kappa_* asserted without parent scale law",
            "block public claim and label G as empirical calibration",
        ),
    ]
    return [
        {
            **common(),
            "reactivation_id": reactivation_id,
            "leak": leak,
            "condition": condition,
            "action": action,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for reactivation_id, leak, condition, action in rows
    ]


def decision_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "DEC4178_0_coupling_form",
            "kappa_to_GN_source_coupling_law_derived_private",
            "The local EH block, Hilbert source measure and Hamiltonian mass readout give G_cal=c^4 kappa_eff/(8*pi), Poisson's equation and Newtonian acceleration.",
            "retain_as_private_selector_structural_reduction",
        ),
        (
            "DEC4178_1_numeric_value",
            "numerical_G_not_predicted",
            "No parent dimensionful invariant fixing kappa_* is derived here; the numerical value of G_cal remains empirical calibration exactly as in GR.",
            "block_numeric_G_claim",
        ),
        (
            "DEC4178_2_calibration_allowed",
            "calibrated_G_is_acceptable_local_GR_reduction",
            "A field theory can reduce to GR/Newton with calibrated G; the discipline is not to relabel calibration as prediction.",
            "use_one_calibrated_constant_across_local_tests",
        ),
        (
            "DEC4178_3_next",
            "next_best_derivation_target",
            "With local EM, boundary, quotient and calibrated coupling gates assembled, next step is a closure summary plus global parent-adoption burden map.",
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
        ("FW4178_0_no_numeric_G", "Do not claim MTS predicts the numerical value of Newton's constant."),
        ("FW4178_1_no_public_local_GR", "Do not claim public local GR; global parent adoption remains open."),
        ("FW4178_2_no_orbital_circularity", "Do not use fitted orbital GM to define the Hamiltonian source mass."),
        ("FW4178_3_no_species_G", "Do not hide species, clock, frame, material, range or readout dependence in G_cal."),
        ("FW4178_4_no_source_label_absorption", "Do not absorb source-normalization leaks into the calibrated constant."),
        ("FW4178_5_no_empirical_pass", "Do not claim PPN, WEP, clocks, R10 or orbital empirical pass from this formal coupling gate alone."),
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
            "kappa_to_GN_coupling_form_derived_private": "True",
            "Poisson_Newton_coefficient_derived_private": "True",
            "Hamiltonian_mass_not_orbital_fit": "True",
            "source_normalization_leak_closed_private": "True",
            "G_calibration_allowed_like_GR": "True",
            "numeric_G_predicted": "False",
            "parent_dimensionful_kappa_scale_derived": "False",
            "global_parent_action_adoption_proved": "False",
            "public_local_GR_claim_allowed": "False",
            "empirical_local_tests_claimed": "False",
            "formal_194_written": "True",
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
            "why_next": "4178 completes the private local selector chain at the calibrated-source-coupling level. The next useful object is a single closure summary and a burden map of exactly what must be parent-adopted before public local-GR language is safe.",
            "route_A": "assemble PPC4161-TK-HQNP plus 4175-4178 into one local-GR private closure map with explicit parent-adoption clauses",
            "route_B": "if any clause is not parent-adoptable, keep it as a named closure or empirical residual rather than a public derived claim",
            "fallback": "private framework continues, public GitHub/journal language remains nonclaim until global adoption and empirical gates are separated",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4178_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4178_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN": SOURCE_DIR / "P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN.csv",
        "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS": SOURCE_DIR / "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv",
        "P8_Y5_R2FR_4178_MEASURED_G_ENVELOPE": SOURCE_DIR / "P8_Y5_R2FR_4178_MEASURED_G_ENVELOPE.csv",
        "P8_Y5_R2FR_4178_REACTIVATION_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv",
        "P8_Y5_R2FR_4178_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4178_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4178_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4178_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4178_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4178_STATUS.csv",
        "P8_Y5_R2FR_4178_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4178_NEXT_TARGET.csv",
    }


def ensure_claim_row() -> str:
    rows = parse_csv(CLAIMS_PATH)
    fieldnames = list(rows[0].keys())
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "Inside the PPC4161 local selector branch, the calibrated source-coupling law G_cal=c^4 kappa_eff/(8*pi) gives the Newton/Poisson coefficient without using orbital GM, while numerical G remains empirical",
        "current_evidence": "formalization-workbench/194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md records kappa_eff=kappa_*Z_0, D_A ln kappa_eff=0, G_cal=c^4 kappa_eff/(8*pi), nabla^2 Phi_N=4*pi G_cal rho_H, M_H^dress as Hamiltonian source charge, anti-circularity guards, and numeric-G firewall; public_claim=false",
        "status": "private_selector_calibrated_source_coupling_nonclaim_numeric_G_not_predicted_public_claim_false",
        "next_test": "Assemble local-GR private closure summary and global parent-adoption burden map",
        "key_risk": "This derives the coupling form and local Newton coefficient only inside the private selector; it does not predict the numerical value of G_N and does not prove global parent adoption",
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
## PPC4161-TK-HQNP Addendum - Calibrated Source Coupling

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4178-Y5-R2FR-calibrated-source-coupling-kappa-GN-normalization-or-measured-G-envelope.md`

Inside the private local selector branch:

```text
G_mu_nu[g_obs] = kappa_eff T_H_mu_nu,
kappa_eff = kappa_* Z_0,
D_A ln kappa_eff = 0.
```

Define the calibrated Newtonian coupling:

```text
G_cal := c^4 kappa_eff/(8*pi).
```

Then the weak-field Hamiltonian-source readout gives:

```text
nabla^2 Phi_N = 4*pi G_cal rho_H,
M_H^dress = H_tau[S_link] - H_ref,
a_r = -G_cal M_H^dress/r^2.
```

This is a structural local GR/Newton coupling reduction with calibrated `G_cal`. It does not predict the numerical value of Newton's constant unless a future parent scale law derives `kappa_*`.
"""
    return append_once(PACKET_180_PATH, PACKET_MARKER, section)


def ensure_spine_section() -> str:
    section = f"""
## PPC4161 Calibrated Source Coupling - 4178

Marker: `{SPINE_MARKER}`  
Source bridge: `194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4178` locks the local coupling language:

```text
kappa_eff = kappa_* Z_0,
G_cal = c^4 kappa_eff/(8*pi),
nabla^2 Phi_N = 4*pi G_cal rho_H,
a_r = -G_cal M_H^dress/r^2.
```

The form of the coupling and the Newton/Poisson coefficient are derived inside the private selector; the numerical value of `G_cal` is empirical calibration unless MTS later derives the dimensionful parent scale of `kappa_*`. That is acceptable GR-like reduction, but not a fundamental numerical prediction.

Next:

```text
{NEXT_TARGET}
```
"""
    return append_once(SPINE_PATH, SPINE_MARKER, section)


def write_formal_194() -> None:
    FORMAL_194_PATH.write_text(
        f"""# 194 - PPC4161 Calibrated Source Coupling Kappa-To-GN Law

Marker: `PPC4161_CALIBRATED_SOURCE_COUPLING_KAPPA_TO_GN_LAW`
Checkpoint: `4178`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`

## Claim Status
Private selector theorem. This is not public local GR, not global MTS adoption, and not a numerical prediction of Newton's constant.

## Coupling Chain
The private local branch has:

```text
G_mu_nu[g_obs] = kappa_eff T_H_mu_nu,
kappa_eff = kappa_* Z_0,
delta_ZH = 0.
```

The topological kappa lock and Hilbert source-measure descent give:

```text
D_A ln kappa_* = 0,
D_A delta_ZH = 0,
D_A ln kappa_eff = 0.
```

Define:

```text
G_cal := c^4 kappa_eff/(8*pi).
```

This is the calibrated Newtonian coupling of the local branch.

## Poisson And Newton Readout
Using the weak-field convention already fixed in the PPC4161 chain:

```text
G_00^lin = 2 nabla^2 Phi_N/c^2,
T_00 = rho_H c^2.
```

The 00 equation gives:

```text
nabla^2 Phi_N = 4*pi G_cal rho_H.
```

The source mass is the Hamiltonian/Hilbert worldtube charge:

```text
M_H^dress[W_H;tau] = H_tau[S_link] - H_ref,
int_W rho_H dV = M_H^dress.
```

For the exterior monopole/readout:

```text
Phi_N = -G_cal M_H^dress/r,
a_r = -G_cal M_H^dress/r^2.
```

## Anti-Circularity
No orbital `GM`, fitted acceleration, or measured numerical `G` is used to define `M_H^dress`, `rho_H`, `kappa_*`, or `Z_0`.

The measured/local calibration appears only here:

```text
numeric(G_cal) = empirical calibration unless parent scale law fixes kappa_*.
```

This is not a defect relative to GR. GR itself has an empirical `G`. The local-reduction claim is structural: same EH block, same Hilbert source, same Hamiltonian mass, one calibrated coupling, and no hidden source/readout dependence.

## What Is Still Not Proven

```text
numeric G_N predicted = false,
global parent adoption = false,
public local GR claim = false.
```

To claim a fundamental prediction of `G_N`, MTS still needs a parent dimensionful invariant or scale law fixing `kappa_*` without importing measured `G`.

## Next Target
`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def write_doc() -> None:
    DOC_PATH.write_text(
        f"""# 4178 - Y5 R2FR Calibrated Source Coupling Kappa-GN Normalization Or Measured-G Envelope

Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Status: private selector theorem; numerical `G_N` is not predicted.

## Result
The local branch derives the source-coupling form:

```text
G_mu_nu[g_obs] = kappa_eff T_H_mu_nu,
kappa_eff = kappa_* Z_0,
G_cal = c^4 kappa_eff/(8*pi).
```

With `D_A ln kappa_* = 0` and `delta_ZH = 0`:

```text
D_A ln G_cal = 0.
```

The weak-field readout gives:

```text
nabla^2 Phi_N = 4*pi G_cal rho_H,
a_r = -G_cal M_H^dress/r^2.
```

## Meaning
This is the honest GR-like situation: the form of the coupling and Newtonian source law are derived inside the private selector, while the numerical value of `G_cal` is calibrated unless a future parent scale law derives `kappa_*`.

## Anti-Circularity
The mass is `M_H^dress = H_tau[S_link]-H_ref`, not fitted orbital `GM`. The constant `G_cal` is one calibrated constant across local tests, not a hiding place for species, clocks, material labels, ranges, frames, source normalization or boundary flux.

## Output Files
- `formalization-workbench/194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md`
- `formalization-workbench/02-claims-register.csv` row `{CLAIM_ID}`
- `formalization-workbench/180-PPC4161-private-local-packet-integration.md` marker `{PACKET_MARKER}`
- `formalization-workbench/07-unification-spine.md` marker `{SPINE_MARKER}`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_SOURCE_REGISTER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_MEASURED_G_ENVELOPE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_BRANCH_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_CLAIM_FIREWALL.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_STATUS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_NEXT_TARGET.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4178_VALIDATION.csv`

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
    source = rows_by_name["P8_Y5_R2FR_4178_SOURCE_REGISTER"]
    chain = rows_by_name["P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN"]
    guards = rows_by_name["P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS"]
    envelope = rows_by_name["P8_Y5_R2FR_4178_MEASURED_G_ENVELOPE"]
    reactivation = rows_by_name["P8_Y5_R2FR_4178_REACTIVATION_LEDGER"]
    decision = rows_by_name["P8_Y5_R2FR_4178_BRANCH_DECISION"]
    firewall = rows_by_name["P8_Y5_R2FR_4178_CLAIM_FIREWALL"]
    status = rows_by_name["P8_Y5_R2FR_4178_STATUS"]
    next_target = rows_by_name["P8_Y5_R2FR_4178_NEXT_TARGET"]

    formal_text = read_text(FORMAL_194_PATH)
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
            "VAL4178_0_sources",
            "all source paths exist and contain required tokens",
            all(row["exists"] == "True" and row["required_text_found"] == "True" for row in source),
            str(source),
        ),
        (
            "VAL4178_1_chain",
            "coupling chain covers EH block, source measure, kappa lock, G relation, Poisson, mass charge, orbital readout and numeric-G firewall",
            all(rows_containing(chain, token) for token in ["G_mu_nu", "delta_ZH=0", "D_A ln kappa_eff", "G_cal", "nabla^2 Phi_N", "M_H^dress", "a_r", "numeric(G_cal)"]),
            "\n".join(",".join(row.values()) for row in chain),
        ),
        (
            "VAL4178_2_anti_circularity",
            "anti-circularity guards block orbital GM input, measured-G input, source-label absorption, species/frame G and calibration overclaim",
            all(rows_containing(guards, token) for token in ["orbital GM", "measured numerical G", "source_normalization", "D_A ln G_cal", "GR also treats G as empirical"]),
            "\n".join(",".join(row.values()) for row in guards),
        ),
        (
            "VAL4178_3_envelope",
            "measured-G envelope records calibrated G, kappa_eff, Hamiltonian mass, mu_theory, drift residual and missing parent scale",
            all(rows_containing(envelope, token) for token in ["G_cal", "kappa_eff", "M_H^dress", "mu_theory", "R_A^G", "numeric_G_parent_scale"]),
            "\n".join(",".join(row.values()) for row in envelope),
        ),
        (
            "VAL4178_4_reactivation",
            "reactivation ledger covers kappa drift, ZH leak, wrong mass charge, hidden constants, boundary flux and numeric-G claim",
            all(rows_containing(reactivation, token) for token in ["kappa_* drift", "source measure leak", "Pi_M/H_tau", "hidden constants", "boundary flux", "numerical G"]),
            "\n".join(",".join(row.values()) for row in reactivation),
        ),
        (
            "VAL4178_5_decision",
            "decision rows derive coupling form, block numerical G prediction, allow calibrated GR-like reduction and pick 4179",
            all(rows_containing(decision, token) for token in ["kappa_to_GN", "numerical_G_not_predicted", "calibrated_G_is_acceptable", NEXT_TARGET]),
            "\n".join(",".join(row.values()) for row in decision),
        ),
        (
            "VAL4178_6_firewall",
            "firewall blocks numeric-G, public local-GR, orbital circularity, species G, source absorption and empirical pass claims",
            all(rows_containing(firewall, token) for token in ["Newton", "public local GR", "orbital GM", "species", "source-normalization", "R10"]),
            "\n".join(",".join(row.values()) for row in firewall),
        ),
        (
            "VAL4178_7_formal_194",
            "formal 194 records coupling chain, Poisson readout, anti-circularity and numeric-G firewall",
            all(token in formal_text for token in ["PPC4161_CALIBRATED_SOURCE_COUPLING_KAPPA_TO_GN_LAW", "G_cal := c^4 kappa_eff/(8*pi)", "nabla^2 Phi_N = 4*pi G_cal rho_H", "numeric(G_cal) = empirical calibration", NEXT_TARGET]),
            "formal 194 checked",
        ),
        (
            "VAL4178_8_doc",
            "checkpoint doc records result, meaning, anti-circularity, outputs and next target",
            all(token in doc_text for token in ["## Result", "## Meaning", "## Anti-Circularity", "Output Files", NEXT_TARGET]),
            "doc checked",
        ),
        (
            "VAL4178_9_packet_180",
            "packet 180 contains calibrated source coupling marker",
            PACKET_MARKER in packet_text and "G_cal" in packet_text,
            f"packet_action={packet_action}",
        ),
        (
            "VAL4178_10_claim_row",
            "claims register contains one L-019 calibrated-coupling nonclaim row",
            len(claim_matches) == 1
            and "private_selector_calibrated_source_coupling_nonclaim_numeric_G_not_predicted_public_claim_false" in claim_matches[0].get("status", ""),
            f"claim_action={claim_action}; matches={claim_matches}",
        ),
        (
            "VAL4178_11_spine",
            "spine contains 4178 marker, claim row and next target",
            SPINE_MARKER in spine_text and CLAIM_ID in spine_text and NEXT_TARGET in spine_text,
            f"spine_action={spine_action}",
        ),
        (
            "VAL4178_12_status",
            "status records private coupling form, Poisson/Newton coefficient, anti-circularity, calibrated G, numeric-G false, global false and 4179 next",
            status[0]["kappa_to_GN_coupling_form_derived_private"] == "True"
            and status[0]["Poisson_Newton_coefficient_derived_private"] == "True"
            and status[0]["Hamiltonian_mass_not_orbital_fit"] == "True"
            and status[0]["G_calibration_allowed_like_GR"] == "True"
            and status[0]["numeric_G_predicted"] == "False"
            and status[0]["parent_dimensionful_kappa_scale_derived"] == "False"
            and status[0]["global_parent_action_adoption_proved"] == "False"
            and status[0]["public_local_GR_claim_allowed"] == "False"
            and status[0]["empirical_local_tests_claimed"] == "False"
            and status[0]["next_target"] == NEXT_TARGET,
            str(status),
        ),
        (
            "VAL4178_13_next",
            "next target moves to local-GR private closure summary and global parent-adoption burden map",
            next_target[0]["next_target"] == NEXT_TARGET and "burden map" in next_target[0]["why_next"],
            str(next_target),
        ),
        (
            "VAL4178_14_no_claim_rows",
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
            "check_id": "VAL4178_15_compile",
            "description": "generator compiles and pycache is removed",
            "passed": "True",
            "details": "compiled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return validation


def main() -> None:
    write_formal_194()
    write_doc()
    claim_action = ensure_claim_row()
    packet_action = ensure_packet_180_addendum()
    spine_action = ensure_spine_section()

    rows_by_name = {
        "P8_Y5_R2FR_4178_SOURCE_REGISTER": source_rows(),
        "P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN": coupling_chain_rows(),
        "P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS": anti_circularity_rows(),
        "P8_Y5_R2FR_4178_MEASURED_G_ENVELOPE": measured_g_envelope_rows(),
        "P8_Y5_R2FR_4178_REACTIVATION_LEDGER": reactivation_rows(),
        "P8_Y5_R2FR_4178_BRANCH_DECISION": decision_rows(),
        "P8_Y5_R2FR_4178_CLAIM_FIREWALL": firewall_rows(),
        "P8_Y5_R2FR_4178_STATUS": status_rows(claim_action, packet_action, spine_action),
        "P8_Y5_R2FR_4178_NEXT_TARGET": next_rows(),
    }

    for name, path in output_paths().items():
        write_csv(path, rows_by_name[name])

    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4178_VALIDATION.csv"
    write_csv(validation_path, validation_rows(rows_by_name, claim_action, packet_action, spine_action))

    validation = parse_csv(validation_path)
    failed = [row for row in validation if row.get("passed") != "True"]
    if failed:
        raise RuntimeError(f"4178 validation failed: {failed}")

    print(f"{CHECKPOINT} generated")
    print(f"doc={DOC_PATH}")
    print(f"formal={FORMAL_194_PATH}")
    print(f"validation={validation_path}")
    print(f"rows={len(validation)} validation checks")


if __name__ == "__main__":
    main()
