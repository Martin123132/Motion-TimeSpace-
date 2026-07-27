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

CHECKPOINT = "4165"
BRANCH_ID = "MTS_R2FR_Y5_KAPPA_G_NORMALIZATION_DERIVATION_4165"
DECISION = "KAPPA_TO_NEWTON_G_RELATION_AND_SUPERSELECTION_GATE_DERIVED_NUMERICAL_G_PARENT_PREDICTION_BLOCKED"
DOC_PATH = POST / "4165-Y5-R2FR-kappa-G-normalization-superselection-or-coupling-derivation.md"
FORMAL_181_PATH = FORMAL / "181-PPC4161-kappa-G-normalization-gate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-006"
SPINE_MARKER = "PPC4161_KAPPA_G_GATE_4165"
NEXT_TARGET = "4166-Y5-R2FR-source-measure-ZH-owner-and-parent-kappa-lock.md"

SOURCES = {
    "SRC4165_00_4164_doc": (
        POST / "4164-Y5-R2FR-PPC4161-local-PPN-readout-gate.md",
        "Reason: the next exposed coupling issue is `kappa_*`",
        "4164 exposes kappa/G as the next gate.",
    ),
    "SRC4165_01_4164_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4164_NEXT_TARGET.csv",
        "derive kappa_* as a superselected coupling",
        "4164 machine-readable next target.",
    ),
    "SRC4165_02_4062_calibration": (
        POST / "4062-Y5-R2FR-second-order-remainder-and-cnorm-newtonG-calibration-gate.md",
        "G_N := c^4 kappa_eff/(8*pi),    kappa_eff = kappa_* Z_0",
        "Earlier calibrated-G gate.",
    ),
    "SRC4165_03_4063_newton_readout": (
        POST / "4063-Y5-R2FR-explicit-EH-weak-field-newton-ppn-readout-contract.md",
        "nabla^2 Phi_N = 4*pi*G_N*rho_H.",
        "Earlier weak-field Newton readout.",
    ),
    "SRC4165_04_4164_ppn_vector": (
        SOURCE_DIR / "P8_Y5_R2FR_4164_PPN_RESIDUAL_VECTOR.csv",
        "Gdot_over_G",
        "4164 Gdot/G residual row.",
    ),
    "SRC4165_05_red_team_kappa": (
        FORMAL / "06-consistency-red-team.md",
        "κ_GR = 8πG/c⁴",
        "Notation/coupling red-team warning.",
    ),
    "SRC4165_06_aw_ratio": (
        POST / "source-intake" / "parent-action" / "AW_coefficient_ratio_law_3045_CONDITIONAL_NONCLAIM.csv",
        "A_W=kappa_eff c^4/(8*pi*G_ref)",
        "Prior action-amplitude ratio law.",
    ),
    "SRC4165_07_newton_lock": (
        POST / "source-intake" / "parent-action" / "AW_Newton_lock_status_3052_BLOCKED_NONCLAIM.csv",
        "A_W = kappa_eff c^4/(8*pi*G_ref)",
        "Prior Newton lock status.",
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
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gravity",
        "claim": "PPC4161 gives a conditional private route from kappa_eff to the Newtonian coupling and PPN Gdot/G silence",
        "current_evidence": "formalization-workbench/181-PPC4161-kappa-G-normalization-gate.md records G_N=c^4*kappa_eff/(8*pi), kappa_eff=kappa_*Z_H, superselection conditions, and numerical-G non-prediction; public_claim=false",
        "status": "private_nonclaim_public_claim_false",
        "next_test": "Derive or source Z_H and parent kappa_* ownership; otherwise retain G_N as an empirical calibration constant with Gdot/species/frame/range residual bounds",
        "key_risk": "A constant calibrated G_N is acceptable local GR practice, but it is not a fundamental MTS prediction unless parent kappa_* and source measure Z_H are derived without importing measured G",
    }
    if existing:
        changed = False
        for row in rows:
            if row.get("claim_id") == CLAIM_ID:
                for key, value in new_row.items():
                    if row.get(key) != value:
                        row[key] = value
                        changed = True
        action = "updated" if changed else "already_present"
    else:
        rows.append(new_row)
        action = "added"

    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return action


def write_formal_181() -> None:
    FORMAL_181_PATH.write_text(
        f"""# 181 - PPC4161 Kappa-G Normalization Gate

Marker: `PPC4161_KAPPA_G_NORMALIZATION_GATE`  
Timestamp UTC: `{now()}`  
Status: `private_spine_branch_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Coupling Relation
For the compact PPC4161 local branch:

```text
G_mu_nu(g_obs) = kappa_eff T^H_mu_nu + residual_mu_nu
kappa_eff = kappa_* Z_H
G_N = c^4 kappa_eff/(8*pi)
```

Here `Z_H` is the parent-to-Hilbert source-measure normalization. If the packet source convention sets `Z_H=1`, then `G_N=c^4 kappa_*/(8*pi)`.

## Derived Part
The weak-field readout gives:

```text
nabla^2 Phi_N = 4*pi G_N rho_H
a_r = -G_N M_H/r^2
```

and the 4164 PPN gate gives:

```text
Gdot/G = 0
```

only if `kappa_*` and `Z_H` are locally superselected.

## Non-Derived Part
The numerical value of `G_N` is not predicted here. A parent prediction would require a source-backed parent invariant with the units of `kappa_*`, plus a source-measure theorem for `Z_H`, with no measured `G` smuggled into the definition.

## Contract
The next proof target is:

```text
{NEXT_TARGET}
```

Either derive `kappa_*` and `Z_H` from the parent action/measure, or label local `G_N` as an empirical calibration constant in exactly the honest sense used by GR.
""",
        encoding="utf-8",
    )


def ensure_spine_section() -> str:
    text = read_text(SPINE_PATH)
    if SPINE_MARKER in text:
        return "already_present"
    section = f"""

## 11. Local GR Coupling Update - PPC4161 Kappa-G Gate

Marker: `{SPINE_MARKER}`  
Source bridge: `181-PPC4161-kappa-G-normalization-gate.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4165` derives the local relation:

```text
G_N = c^4 kappa_eff/(8*pi),
kappa_eff = kappa_* Z_H.
```

Inside the PPC4161 private local packet, local PPN `Gdot/G` silence follows only if `kappa_*` and the source-measure factor `Z_H` are superselected:

```text
D_t ln(kappa_* Z_H) = D_species ln(kappa_* Z_H) = D_frame ln(kappa_* Z_H) = D_range ln(kappa_* Z_H) = 0.
```

This improves the local-GR spine because the coupling throat is now explicit. It still does **not** predict the numerical value of Newton's constant. The next local-GR spine step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def derivation_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "KG4165_0_action_variation",
            "Vary the local EH packet with respect to g_obs.",
            "G_mu_nu(g_obs)=kappa_eff T^H_mu_nu + R_mu_nu",
            "kappa_eff is the coefficient actually seen by the Hilbert source after parent source-measure projection.",
            "derived_relation",
        ),
        (
            "KG4165_1_source_measure",
            "Split the effective coupling into parent coupling and source measure.",
            "kappa_eff = kappa_* Z_H",
            "Z_H=1 only if the parent-to-Hilbert source map is normalized and common across matter sectors.",
            "derived_accounting_identity",
        ),
        (
            "KG4165_2_newton_limit",
            "Use the weak-field slow-motion 00 equation.",
            "nabla^2 Phi_N = (c^4 kappa_eff/2) rho_H = 4*pi G_N rho_H",
            "G_N = c^4 kappa_eff/(8*pi) follows from matching the Poisson coefficient.",
            "derived_weak_field_readout",
        ),
        (
            "KG4165_3_orbital_readout",
            "Integrate Poisson over a compact source.",
            "surface_integral grad Phi_N.dS = 4*pi G_N M_H; a_r=-G_N M_H/r^2",
            "The measured orbital GM is the product G_N*M_H, so it cannot separately prove numerical G.",
            "derived_with_calibration_caveat",
        ),
        (
            "KG4165_4_ppn_gdot",
            "Differentiate the effective coupling.",
            "dot(G_eff)/G_eff = dot(kappa_*)/kappa_* + dot(Z_H)/Z_H",
            "4164 Gdot/G silence requires both terms to vanish or be bounded.",
            "derived_residual_law",
        ),
        (
            "KG4165_5_species_frame_range",
            "Take derivatives with respect to species, frame, range, environment and readout convention.",
            "D_A ln G_eff = D_A ln kappa_* + D_A ln Z_H",
            "WEP/R10/PPN safety requires these derivatives to vanish or be source-bounded.",
            "derived_residual_family",
        ),
    ]
    return [
        {
            **common(),
            "derivation_id": row[0],
            "step": row[1],
            "equation": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def superselection_rows() -> List[Dict[str, str]]:
    rows = [
        ("time", "D_t ln(kappa_* Z_H)=0", "Gdot/G", "clock/orbital secular drift"),
        ("species", "D_species ln(kappa_* Z_H)=0", "WEP/source universality", "composition-dependent source charge"),
        ("frame", "D_frame ln(kappa_* Z_H)=0", "PPN preferred-frame", "alpha_i leakage"),
        ("range", "D_range ln(kappa_* Z_H)=0", "R10/Yukawa/local range tests", "finite-range or screening-dependent G"),
        ("environment", "D_env ln(kappa_* Z_H)=0", "Solar/local-vacuum collar", "local-cosmology or galaxy-memory leakage"),
        ("readout", "D_readout ln(kappa_* Z_H)=0", "measured GM convention", "unit/clock/source-reference absorption"),
    ]
    return [
        {
            **common(),
            "gate_id": f"SS4165_{index}_{name}",
            "derivative_channel": name,
            "required_zero_or_bound": equation,
            "protects": protects,
            "failure_mode": failure,
            "current_status": "zero_inside_PPC4161_only_if_kappa_and_ZH_parent_owned",
            "needed_evidence": "parent theorem or numeric/source-backed bound row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for index, (name, equation, protects, failure) in enumerate(rows)
    ]


def no_go_contract_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "NG4165_0_dimensional_no_go",
            "A local EH/PPN readout with no dimensionful parent invariant cannot predict the numerical value of G_N.",
            "kappa_* has dimensions; symmetries fix form and universality, not the measured dimensional number.",
            "NO_NUMERICAL_G_PREDICTION_FROM_CURRENT_PACKET",
        ),
        (
            "NG4165_1_rescaling_no_go",
            "The local equation only observes kappa_eff T^H_mu_nu.",
            "A common rescaling of source normalization and kappa_eff leaves local metric predictions unchanged until an independent mass/current measure fixes Z_H.",
            "SOURCE_MEASURE_ZH_REQUIRED",
        ),
        (
            "PC4165_0_parent_invariant",
            "A successful parent prediction must provide kappa_* = F[I_MTS,c,...] with correct units.",
            "F must be defined without measured G_N, orbital GM, Cavendish calibration, or arena-specific fitting.",
            "PARENT_KAPPA_CONTRACT",
        ),
        (
            "PC4165_1_source_measure",
            "A successful parent prediction must provide Z_H from the same matter/current measure used in the Hilbert stress tensor.",
            "Z_H must be common across species, clocks, frames, ranges and local environments, or every derivative channel needs a bound.",
            "PARENT_ZH_CONTRACT",
        ),
        (
            "PC4165_2_calibration_allowed",
            "If no parent invariant is supplied, local G_N can remain an empirical calibration constant.",
            "This is not embarrassing: it is the same status as the numerical coupling in practical GR, provided MTS does not advertise it as predicted.",
            "HONEST_CALIBRATED_GR_LIMIT_ALLOWED",
        ),
    ]
    return [
        {
            **common(),
            "contract_id": row[0],
            "statement": row[1],
            "reason": row[2],
            "verdict": row[3],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def verdict_rows(claim_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "verdict_id": "V4165_0_relation",
            "result": "G_N=c^4*kappa_eff/(8*pi) and kappa_eff=kappa_*Z_H are derived as the local weak-field coupling relation.",
            "strength": "derived_relation",
            "public_claim_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "V4165_1_superselection",
            "result": "Gdot/G and source-universality silence reduce to derivative-zero gates for ln(kappa_*Z_H).",
            "strength": "derived_residual_gate",
            "public_claim_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "V4165_2_numerical_G",
            "result": "The numerical value of G_N is not parent-predicted by the current PPC4161 packet.",
            "strength": "blocked_until_parent_invariant_and_ZH_owner",
            "public_claim_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "V4165_3_formal_sync",
            "result": f"formal bridge 181 written; claim row action={claim_action}; spine action={spine_action}",
            "strength": "formal_nonclaim_sync",
            "public_claim_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4165_0_no_G_prediction",
            "rule": "Do not claim MTS predicts the numerical value of Newton's constant unless parent kappa_* and Z_H are sourced without measured G.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4165_1_G_calibration_allowed",
            "rule": "Calibrated G_N is allowed as a local GR limit, but must be labelled empirical calibration rather than derived MTS constant.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4165_2_ZH_not_hidden",
            "rule": "Do not hide source-measure normalization inside measured GM; Z_H must be parent-owned or bounded.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows(claim_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "result": DECISION,
            "G_relation_derived": "True",
            "kappa_eff_split_defined": "True",
            "superselection_gate_derived": "True",
            "numerical_G_parent_predicted": "False",
            "calibrated_G_allowed_if_labelled": "True",
            "formal_181_written": "True",
            "claim_register_action": claim_action,
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
            "why_next": "4165 isolates the remaining coupling throat into parent kappa_* ownership and source-measure Z_H ownership.",
            "route_A": "derive a parent invariant or topological/measure law fixing kappa_* without measured G",
            "route_B": "derive Z_H=1 from the same Hilbert source/current measure, or emit bounded derivative rows",
            "fallback": "retain G_N as empirical calibration and test only derivative/residual channels",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4165 - Kappa-G Normalization Superselection Or Coupling Derivation

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
4164 mapped PPC4161 to the local PPN vector but left the coupling throat exposed. 4165 attacks that throat directly.

## Derived Coupling Relation
Start from the local packet equation:

```text
G_mu_nu(g_obs) = kappa_eff T^H_mu_nu + R_mu_nu,
kappa_eff = kappa_* Z_H.
```

In the weak-field, slow-motion limit:

```text
nabla^2 Phi_N = (c^4 kappa_eff/2) rho_H.
```

Matching to Poisson form gives:

```text
G_N = c^4 kappa_eff/(8*pi)
    = c^4 kappa_* Z_H/(8*pi).
```

So the local route to Newton is now explicit. Newton's constant is not an extra plateau axiom in this branch; it is the weak-field readout of the EH coupling times the parent source-measure normalization.

## Superselection Law
The local PPN `Gdot/G` and source-universality gates reduce to:

```text
D_A ln G_eff = D_A ln(kappa_* Z_H)
             = D_A ln kappa_* + D_A ln Z_H,
```

for derivative channels:

```text
A in {{time, species, frame, range, environment, readout}}.
```

The PPC4161 local branch is safe only if those channels are parent-zero or empirically bounded.

## No-Go Result
The current packet does **not** predict the numerical value of `G_N`.

Reason: a dimensional coupling cannot be numerically derived from local symmetry/readout alone. The local metric equation observes the product `kappa_eff T^H_mu_nu`; without a parent-owned `kappa_*` invariant and a source-measure theorem for `Z_H`, one can calibrate the product but not predict its absolute measured value.

This is not fatal. It means the honest MTS local-GR position is:

```text
relation derived;
universality/superselection gated;
numerical G calibrated unless parent invariant + Z_H theorem are later derived.
```

That is the same practical status GR has for the numerical value of `G`, while still letting MTS try for a deeper derivation later.

## Parent Contract
To promote this beyond calibration, a future parent action must satisfy:

1. produce `kappa_* = F(parent invariants)` with correct dimensions;
2. define `Z_H` from the same Hilbert/current measure used by matter;
3. forbid measured `G`, orbital `GM`, or arena-fitted constants inside `F`;
4. prove `D_A ln(kappa_* Z_H)=0` for local tested channels, or supply bounds.

## Formal Sync
- Formal bridge: `181-PPC4161-kappa-G-normalization-gate.md`
- Claim row: `{CLAIM_ID}`
- Spine marker: `{SPINE_MARKER}`

## Next Target
`{NEXT_TARGET}`

## Outputs
{chr(10).join(f"- `{path}`" for path in outputs.values())}
""",
        encoding="utf-8",
    )


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4165_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4165_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4165_KAPPA_G_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4165_KAPPA_G_DERIVATION.csv",
        "P8_Y5_R2FR_4165_SUPERSELECTION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4165_SUPERSELECTION_GATE.csv",
        "P8_Y5_R2FR_4165_NO_GO_AND_PARENT_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4165_NO_GO_AND_PARENT_CONTRACT.csv",
        "P8_Y5_R2FR_4165_VERDICT": SOURCE_DIR / "P8_Y5_R2FR_4165_VERDICT.csv",
        "P8_Y5_R2FR_4165_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4165_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4165_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4165_STATUS.csv",
        "P8_Y5_R2FR_4165_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4165_NEXT_TARGET.csv",
    }


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

    sources = parse_csv(outputs["P8_Y5_R2FR_4165_SOURCE_REGISTER"])
    add("VAL4165_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    derivation = parse_csv(outputs["P8_Y5_R2FR_4165_KAPPA_G_DERIVATION"])
    derivation_text = "\n".join(",".join(row.values()) for row in derivation)
    add("VAL4165_1_derivation", "derivation rows contain kappa_eff split, Newton limit, G_N relation and derivative residuals", all(token in derivation_text for token in ["kappa_eff = kappa_* Z_H", "G_N = c^4 kappa_eff/(8*pi)", "dot(G_eff)/G_eff", "D_A ln G_eff"]), derivation_text)

    superselection = parse_csv(outputs["P8_Y5_R2FR_4165_SUPERSELECTION_GATE"])
    expected_channels = {"time", "species", "frame", "range", "environment", "readout"}
    add("VAL4165_2_superselection", "superselection gate covers time/species/frame/range/environment/readout channels", {row["derivative_channel"] for row in superselection} == expected_channels, str([row["derivative_channel"] for row in superselection]))

    contract = parse_csv(outputs["P8_Y5_R2FR_4165_NO_GO_AND_PARENT_CONTRACT"])
    contract_text = "\n".join(",".join(row.values()) for row in contract)
    add("VAL4165_3_contract", "contract records dimensional no-go, source-measure no-go, parent invariant, Z_H and calibration route", all(token in contract_text for token in ["NO_NUMERICAL_G_PREDICTION", "SOURCE_MEASURE_ZH_REQUIRED", "PARENT_KAPPA_CONTRACT", "PARENT_ZH_CONTRACT", "HONEST_CALIBRATED_GR_LIMIT_ALLOWED"]), contract_text)

    verdict = parse_csv(outputs["P8_Y5_R2FR_4165_VERDICT"])
    verdict_text = "\n".join(",".join(row.values()) for row in verdict)
    add("VAL4165_4_verdict", "verdict derives relation and blocks numerical-G prediction", "derived_relation" in verdict_text and "blocked_until_parent_invariant_and_ZH_owner" in verdict_text, verdict_text)

    formal_text = read_text(FORMAL_181_PATH)
    add("VAL4165_5_formal_181", "formal 181 bridge exists with coupling relation, no numerical-G claim and next target", FORMAL_181_PATH.exists() and all(token in formal_text for token in ["PPC4161_KAPPA_G_NORMALIZATION_GATE", "G_N = c^4 kappa_eff/(8*pi)", "not predicted", NEXT_TARGET]), "formal 181 checked")

    claims = parse_csv(CLAIMS_PATH)
    l006 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4165_6_claim_row", "claims register contains one L-006 private nonclaim row", len(l006) == 1 and l006[0].get("status") == "private_nonclaim_public_claim_false" and "public_claim=false" in l006[0].get("current_evidence", ""), str(l006))

    spine_text = read_text(SPINE_PATH)
    add("VAL4165_7_spine", "spine contains 4165 marker, claim row, G relation and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "G_N = c^4 kappa_eff/(8*pi)", NEXT_TARGET]), "spine checked")

    firewall = parse_csv(outputs["P8_Y5_R2FR_4165_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4165_8_firewall", "firewall blocks numerical-G claim and hidden Z_H absorption", all(token in firewall_text for token in ["numerical value of Newton's constant", "Calibrated G_N", "Z_H"]), firewall_text)

    status = parse_csv(outputs["P8_Y5_R2FR_4165_STATUS"])
    add("VAL4165_9_status", "status records derived relation, superselection gate, calibrated-G allowance and no numerical-G prediction", len(status) == 1 and status[0]["G_relation_derived"] == "True" and status[0]["superselection_gate_derived"] == "True" and status[0]["numerical_G_parent_predicted"] == "False" and status[0]["calibrated_G_allowed_if_labelled"] == "True", str(status))

    next_rows_loaded = parse_csv(outputs["P8_Y5_R2FR_4165_NEXT_TARGET"])
    add("VAL4165_10_next", "next target is source-measure Z_H and parent kappa lock", len(next_rows_loaded) == 1 and next_rows_loaded[0]["next_target"] == NEXT_TARGET and "Z_H" in next_rows_loaded[0]["why_next"], str(next_rows_loaded))

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4165_11_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

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
    add("VAL4165_12_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_181()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4165_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4165_KAPPA_G_DERIVATION"], derivation_rows())
    write_csv(outputs["P8_Y5_R2FR_4165_SUPERSELECTION_GATE"], superselection_rows())
    write_csv(outputs["P8_Y5_R2FR_4165_NO_GO_AND_PARENT_CONTRACT"], no_go_contract_rows())
    write_csv(outputs["P8_Y5_R2FR_4165_VERDICT"], verdict_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4165_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4165_STATUS"], status_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4165_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4165_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_181_PATH}")
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
