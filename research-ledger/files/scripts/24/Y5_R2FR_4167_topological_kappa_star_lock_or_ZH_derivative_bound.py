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

CHECKPOINT = "4167"
BRANCH_ID = "MTS_R2FR_Y5_TOPOLOGICAL_KAPPA_STAR_LOCK_OR_ZH_DERIVATIVE_BOUND_4167"
DECISION = "TOPOLOGICAL_KAPPA_CONSTANCY_LEMMA_CONSTRUCTED_BUT_PARENT_ADOPTION_UNSIGNED_ZH_BOUND_ROWS_REQUIRED"
DOC_PATH = POST / "4167-Y5-R2FR-topological-kappa-star-lock-or-ZH-derivative-bound.md"
FORMAL_183_PATH = FORMAL / "183-PPC4161-topological-kappa-star-lock-or-ZH-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-008"
SPINE_MARKER = "PPC4161_KAPPA_TOPO_OR_ZH_BOUND_4167"
NEXT_TARGET = "4168-Y5-R2FR-parent-adopted-topological-kappa-sector-or-first-ZH-bound-source.md"

SOURCES = {
    "SRC4167_00_4166_doc": (
        POST / "4166-Y5-R2FR-source-measure-ZH-owner-and-parent-kappa-lock.md",
        "D_A ln kappa_* = 0",
        "4166 handoff that isolated the parent kappa_* lock.",
    ),
    "SRC4167_01_4166_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4166_NEXT_TARGET.csv",
        "derive d kappa_*=0",
        "4166 next-target route A/B split.",
    ),
    "SRC4167_02_4166_kappa_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4166_KAPPA_LOCK_CONTRACT.csv",
        "S_kappa = int A_3 wedge d(kappa_*)",
        "Topological/superselection option recorded by 4166.",
    ),
    "SRC4167_03_4166_leak_channels": (
        SOURCE_DIR / "P8_Y5_R2FR_4166_ZH_LEAK_CHANNELS.csv",
        "D_readout delta_ZH",
        "Six physical Z_H leak channels from 4166.",
    ),
    "SRC4167_04_parent_chain_1009": (
        POST / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "S_kappa_top[kappa_eff,A_3]",
        "Older parent-action contract containing the candidate kappa topological sector.",
    ),
    "SRC4167_05_AW_ratio_3045": (
        POST / "source-intake" / "parent-action" / "AW_coefficient_ratio_law_3045_CONDITIONAL_NONCLAIM.csv",
        "A_W=kappa_eff c^4/(8*pi*G_ref)",
        "Newton coefficient ratio law that shows where G_ref/kappa_eff must lock.",
    ),
    "SRC4167_06_AW_lock_3052": (
        POST / "source-intake" / "parent-action" / "AW_Newton_lock_status_3052_BLOCKED_NONCLAIM.csv",
        "BLOCKED_READOUT_GATES_NOT_SIGNED",
        "Blocked Newton-lock status before the PPC4161 coupling cleanup.",
    ),
    "SRC4167_07_HSM541": (
        SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "HSM541_6_constant_universal_G",
        "Earlier constant/universal G source-measure gate.",
    ),
    "SRC4167_08_4155_source_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "PIM_HTAU_GLUE_UNSIGNED",
        "Same-charge Hilbert/source projector glue still unsigned.",
    ),
    "SRC4167_09_formal_182": (
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "Z_H = Z_0 exp(delta_ZH)",
        "Formal bridge from 4166.",
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
        "claim": "PPC4161 has a candidate topological route to local kappa_* constancy, but the route is not a public local-GR claim until parent adoption and boundary/source-blind clauses are signed",
        "current_evidence": "formalization-workbench/183-PPC4161-topological-kappa-star-lock-or-ZH-bound.md records S_top=int A_3 wedge d(kappa_*), delta_A3 S => d kappa_*=0 if adopted, and fallback Z_H/kappa derivative-bound rows; public_claim=false",
        "status": "private_candidate_nonclaim_public_claim_false",
        "next_test": "Either parent-adopt the topological kappa sector with fixed boundary/superselection and source-blind clauses, or fill the first source-backed Z_H/kappa derivative-bound rows",
        "key_risk": "The topological lemma proves constancy only inside the candidate sector; without parent adoption it is just a clean closure mechanism, and it never predicts the numerical value of G_N by itself",
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


def write_formal_183() -> None:
    FORMAL_183_PATH.write_text(
        f"""# 183 - PPC4161 Topological Kappa-Star Lock Or ZH Bound

Marker: `PPC4161_TOPOLOGICAL_KAPPA_STAR_LOCK_OR_ZH_BOUND`  
Timestamp UTC: `{now()}`  
Status: `private_candidate_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Candidate Topological Lock
The clean parent mechanism for local coupling constancy is a topological/superselection term:

```text
S_top[kappa_*, A_3] = int_M A_3 wedge d(kappa_*).
```

Here `kappa_*` is a scalar parent coupling and `A_3` is a three-form Lagrange multiplier/topological potential. Variation with respect to `A_3` gives:

```text
delta_A3 S_top = int_M delta A_3 wedge d(kappa_*) = 0
=> d(kappa_*) = 0.
```

On a connected local branch this implies:

```text
D_A ln kappa_* = 0.
```

This is the desired local lock, but only if this sector is genuinely parent-adopted.

## Boundary And Source-Blind Clauses
Variation with respect to `kappa_*` gives, up to boundary sign conventions:

```text
dA_3 = 0
```

plus a boundary term. Therefore the route requires:

```text
delta kappa_*|_boundary = 0
```

or an equivalent fixed flux/superselection sector. It also requires that `A_3` carries no source, species, frame, range, environment, or readout labels. Otherwise the apparent lock can smuggle in the same leakage we were trying to remove.

## What Is Proven
If the above clauses are parent-signed, then local drift of `kappa_*` is killed:

```text
D_A ln kappa_* = 0.
```

That is real structural progress.

## What Is Not Proven
This does not predict the numerical value of Newton's constant:

```text
G_N = c^4 kappa_* Z_H/(8*pi)
```

still needs either a parent scale law or an honest empirical calibration, as in GR.

## Fallback Bound Law
If the topological sector is not parent-adopted, the local coupling residual is:

```text
R_A^G = D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH.
```

Each local arena must then provide a source-backed bound:

```text
|R_A^G| <= B_A^local.
```

This bridge therefore converts the coupling problem into a binary gate:

```text
parent topological lock adopted
OR
source-backed derivative bounds filled.
```

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

## 13. Local GR Coupling Update - Topological Kappa Or ZH Bound

Marker: `{SPINE_MARKER}`  
Source bridge: `183-PPC4161-topological-kappa-star-lock-or-ZH-bound.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4167` takes the clean derivation-first route. A candidate parent topological term,

```text
S_top[kappa_*, A_3] = int A_3 wedge d(kappa_*),
```

gives:

```text
delta_A3 S_top = 0 => d(kappa_*) = 0.
```

So the local `kappa_*` drift problem has a precise possible mechanism: a superselected/topological coupling sector. The proof is clean inside the candidate sector, but the branch is still not a public local-GR claim because parent adoption, boundary fixing/fixed flux, source-blindness, and numerical scale ownership remain unsigned.

If the topological route is not adopted, the fallback residual is:

```text
R_A^G = D_A ln kappa_* + D_A delta_ZH,
|R_A^G| <= B_A^local.
```

The next local-GR coupling step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def topological_attempt_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "TK4167_0_candidate_action",
            "candidate topological kappa sector",
            "S_top[kappa_*,A_3]=int_M A_3 wedge d(kappa_*)",
            "Introduces a Lagrange-multiplier/topological three-form whose Euler equation can lock kappa_*.",
            "candidate_constructed_not_parent_adopted",
            "False",
        ),
        (
            "TK4167_1_A3_variation",
            "A_3 variation",
            "delta_A3 S_top=int_M delta A_3 wedge d(kappa_*)=0 => d(kappa_*)=0",
            "This proves local constancy of kappa_* inside any connected branch where the sector is adopted.",
            "math_valid_if_candidate_action_adopted",
            "False",
        ),
        (
            "TK4167_2_kappa_variation",
            "kappa_* variation",
            "delta_kappa S_top=int_M dA_3 delta kappa_* - int_boundary A_3 delta kappa_*",
            "The companion equation is dA_3=0 only after boundary/fixed-flux conditions are specified.",
            "boundary_clause_required",
            "False",
        ),
        (
            "TK4167_3_connected_branch",
            "connected local branch implication",
            "d(kappa_*)=0 => D_A ln kappa_*=0 for A={time,species,frame,range,environment,readout}",
            "This kills the local Gdot/source/frame/range/readout part coming from kappa_*.",
            "conditional_constancy_lemma",
            "False",
        ),
        (
            "TK4167_4_source_blindness",
            "no hidden labels",
            "A_3 must not carry source/species/frame/range/environment/readout labels",
            "Otherwise the topological term can re-import the leak vector in disguised form.",
            "parent_clause_unsigned",
            "False",
        ),
        (
            "TK4167_5_numeric_G",
            "not a numerical G prediction",
            "G_N=c^4 kappa_* Z_H/(8*pi) still needs parent scale law or empirical calibration",
            "Topological constancy fixes drift, not magnitude.",
            "not_numeric_G_prediction",
            "False",
        ),
    ]
    return [
        {
            **common(),
            "attempt_id": row[0],
            "clause": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "parent_signed": row[5],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "theorem_id": "THM4167_0_topological_constancy_lemma",
            "statement": "If a parent-adopted source-blind topological sector S_top=int A_3 wedge d(kappa_*) exists with fixed boundary/fixed flux conditions, then kappa_* is locally constant on each connected branch.",
            "proof": "delta_A3 S_top=0 gives d(kappa_*)=0; connectedness gives D_A ln kappa_*=0 for all local derivative/readout directions.",
            "formula": "S_top=int A_3 wedge d(kappa_*); delta_A3 S_top=>d(kappa_*)=0",
            "proof_status": "derived_inside_candidate_sector_parent_adoption_unsigned",
            "blocked_part": "parent action adoption, boundary/fixed-flux clause, source-blind A_3, and numerical scale law",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "THM4167_1_coupling_residual_bound_law",
            "statement": "If the topological lock is not parent-adopted, local tests constrain the sum of kappa_* drift and Z_H leak derivatives.",
            "proof": "From G_eff=c^4 kappa_* Z_H/(8*pi) and Z_H=Z_0 exp(delta_ZH), derivatives remove the common constant Z_0.",
            "formula": "R_A^G=D_A ln G_eff=D_A ln kappa_* + D_A delta_ZH; |R_A^G|<=B_A^local",
            "proof_status": "derived_identity_needs_source_backed_bounds",
            "blocked_part": "numeric/source-backed B_A rows for time/species/frame/range/environment/readout",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def derivative_bound_rows() -> List[Dict[str, str]]:
    data = [
        (
            "KDB4167_0_kappa_star_superselection",
            "kappa_star",
            "all",
            "D_A ln kappa_*",
            "If topological sector is adopted then D_A ln kappa_*=0; otherwise |D_A ln kappa_*|<=B_kappa_A.",
            "parent topological adoption or local drift bounds",
            "MISSING_PARENT_ADOPTION_OR_NUMERIC_BOUND",
            "dimension depends on channel",
        ),
        (
            "ZDB4167_1_time",
            "delta_ZH",
            "time",
            "D_t delta_ZH",
            "|D_t ln kappa_* + D_t delta_ZH| <= B_Gdot",
            "Gdot/G, pulsar/orbital secular drift, clocks",
            "MISSING_SOURCE_BACKED_GDOT_BOUND_ROW",
            "1/time",
        ),
        (
            "ZDB4167_2_species",
            "delta_ZH",
            "species",
            "Delta_AB delta_ZH",
            "|Delta_AB ln kappa_* + Delta_AB delta_ZH| <= B_WEP_AB",
            "WEP/source universality/composition dependence",
            "MISSING_SOURCE_BACKED_WEP_BOUND_ROW",
            "dimensionless",
        ),
        (
            "ZDB4167_3_frame",
            "delta_ZH",
            "frame",
            "D_frame delta_ZH",
            "|D_frame ln kappa_* + D_frame delta_ZH| <= B_PPN_alpha",
            "PPN preferred-frame and source-frame normalization",
            "MISSING_SOURCE_BACKED_PPN_FRAME_BOUND_ROW",
            "dimensionless or per frame parameter",
        ),
        (
            "ZDB4167_4_range",
            "delta_ZH",
            "range",
            "D_lambda delta_ZH",
            "|D_lambda ln kappa_* + D_lambda delta_ZH| <= B_alpha_lambda",
            "R10/Yukawa/range-dependent effective G",
            "MISSING_SOURCE_BACKED_R10_ALPHA_LAMBDA_BOUND_ROW",
            "per length or dimensionless alpha(lambda)",
        ),
        (
            "ZDB4167_5_environment",
            "delta_ZH",
            "environment",
            "D_env delta_ZH",
            "|D_env ln kappa_* + D_env delta_ZH| <= B_env",
            "solar/local-vacuum versus galaxy/cosmology leakage",
            "MISSING_SOURCE_BACKED_ENVIRONMENT_BOUND_ROW",
            "dimensionless environment contrast",
        ),
        (
            "ZDB4167_6_readout",
            "delta_ZH",
            "readout",
            "D_readout delta_ZH",
            "|D_readout ln kappa_* + D_readout delta_ZH| <= B_readout",
            "measured GM, detector, clock, orbital convention absorption",
            "MISSING_SOURCE_BACKED_READOUT_BOUND_ROW",
            "dimensionless readout/systematic contrast",
        ),
    ]
    return [
        {
            **common(),
            "bound_id": row[0],
            "owner": row[1],
            "channel": row[2],
            "operator": row[3],
            "required_bound_or_zero": row[4],
            "arena": row[5],
            "source_path_or_status": row[6],
            "units": row[7],
            "numeric_value": "MISSING_NUMERIC_INPUT",
            "source_status": "not_source_backed_for_claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in data
    ]


def branch_decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "BD4167_0_route_A",
            "route": "topological_kappa_star_lock",
            "result": "A clean constancy lemma is derived inside the candidate action S_top=int A_3 wedge d(kappa_*).",
            "gate_state": "math_candidate_pass_parent_adoption_unsigned",
            "next_action": "Find or write the parent action clause that truly adopts this sector with source-blind A_3 and fixed boundary/fixed flux conditions.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4167_1_route_B",
            "route": "ZH_and_kappa_derivative_bounds",
            "result": "Fallback bound rows are now explicit for kappa_star plus time/species/frame/range/environment/readout Z_H channels.",
            "gate_state": "source_rows_missing",
            "next_action": "Fill first source-backed local bound row rather than repeating abstract missingness.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "BD4167_2_next",
            "route": "next_target",
            "result": NEXT_TARGET,
            "gate_state": "continue_derivation_first_then_source_first_if_unsigned",
            "next_action": "Either parent-adopt the topological sector or acquire one real bound input for the dominant local residual channel.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4167_0_no_parent_adoption_no_claim",
            "rule": "The topological kappa lemma is not a public local-GR claim unless the parent action actually adopts S_top or an equivalent superselection sector.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4167_1_no_boundary_smuggle",
            "rule": "Boundary/fixed-flux conditions must be fixed before readout; otherwise d(kappa_*)=0 can be a boundary convention rather than a theorem.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4167_2_no_source_labels",
            "rule": "A_3 may not carry source, species, frame, range, environment, or readout labels in the local branch.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4167_3_no_numeric_G_prediction",
            "rule": "d(kappa_*)=0 proves constancy, not the numerical value of G_N.",
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
            "topological_constancy_lemma_constructed": "True",
            "topological_sector_parent_adopted": "False",
            "boundary_clause_signed": "False",
            "source_blind_A3_signed": "False",
            "numeric_G_predicted": "False",
            "ZH_kappa_derivative_bound_rows_created": "True",
            "formal_183_written": "True",
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
            "why_next": "4167 proves d(kappa_*)=0 inside a clean candidate topological sector but cannot claim it until parent adoption, boundary, and source-blind clauses are signed.",
            "route_A": "parent-adopt S_top=int A_3 wedge d(kappa_*) or equivalent superselection sector and prove A_3 is source-blind with fixed boundary/fixed flux",
            "route_B": "fill first source-backed derivative-bound row for R_A^G=D_A ln kappa_* + D_A delta_ZH, prioritizing time/Gdot or range/R10",
            "fallback": "keep local G_N calibrated and keep PPC4161 as a private conditional GR-like branch only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4167_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4167_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4167_TOPOLOGICAL_KAPPA_LOCK_ATTEMPT": SOURCE_DIR / "P8_Y5_R2FR_4167_TOPOLOGICAL_KAPPA_LOCK_ATTEMPT.csv",
        "P8_Y5_R2FR_4167_THEOREM_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4167_THEOREM_STATUS.csv",
        "P8_Y5_R2FR_4167_ZH_DERIVATIVE_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4167_ZH_DERIVATIVE_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4167_BRANCH_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4167_BRANCH_DECISION.csv",
        "P8_Y5_R2FR_4167_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4167_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4167_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4167_STATUS.csv",
        "P8_Y5_R2FR_4167_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4167_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4167 - Topological Kappa-Star Lock Or ZH Derivative Bound

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## What Was Attempted
The clean route was tried first: construct a parent topological/superselection mechanism for:

```text
D_A ln kappa_* = 0.
```

The candidate action is:

```text
S_top[kappa_*,A_3] = int_M A_3 wedge d(kappa_*).
```

Variation with respect to `A_3` gives:

```text
delta_A3 S_top = int_M delta A_3 wedge d(kappa_*) = 0
=> d(kappa_*) = 0.
```

On a connected local branch:

```text
d(kappa_*) = 0 => D_A ln kappa_* = 0.
```

That is the exact local suppression condition we wanted for the `kappa_*` half of the coupling throat.

## Why It Is Still Not A Claim
The proof is real inside the candidate sector, but the sector itself is not yet signed as a parent MTS action clause. The unsigned clauses are:

- parent adoption of `S_top` or equivalent;
- fixed boundary/fixed flux condition for the `kappa_*` variation;
- source-blind `A_3` with no species/frame/range/environment/readout labels;
- separate parent scale law if one wants to predict the numerical value of `G_N`.

So the status is:

```text
math candidate pass, parent adoption unsigned, public claim false.
```

## Fallback Bound Law
If the topological sector is not adopted, the physical local residual is now explicit:

```text
R_A^G = D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH.
```

Every local arena must supply:

```text
|R_A^G| <= B_A^local.
```

The new CSV bound rows therefore name the exact missing inputs for time, species, frame, range, environment, and readout channels without pretending they are already sourced.

## Verdict
This is not another vague missingness loop. It is a real fork:

```text
either adopt the topological kappa sector
or source the derivative-bound residual rows.
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

    sources = parse_csv(outputs["P8_Y5_R2FR_4167_SOURCE_REGISTER"])
    add(
        "VAL4167_0_sources",
        "all source paths exist and contain required tokens",
        all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources),
        str(sources),
    )

    attempt = parse_csv(outputs["P8_Y5_R2FR_4167_TOPOLOGICAL_KAPPA_LOCK_ATTEMPT"])
    attempt_text = "\n".join(",".join(row.values()) for row in attempt)
    add(
        "VAL4167_1_topological_attempt",
        "topological attempt records candidate action, A3 variation, boundary clause, source-blindness and no numerical G prediction",
        all(token in attempt_text for token in ["S_top[kappa_*,A_3]", "d(kappa_*)=0", "boundary", "source/species/frame/range/environment/readout", "not_numeric_G_prediction"]),
        attempt_text,
    )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4167_THEOREM_STATUS"])
    theorem_text = "\n".join(",".join(row.values()) for row in theorem)
    add(
        "VAL4167_2_theorems",
        "theorem rows include conditional topological constancy and coupling residual bound law",
        all(token in theorem_text for token in ["delta_A3 S_top=>d(kappa_*)=0", "R_A^G=D_A ln G_eff", "source_backed_bounds"]),
        theorem_text,
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4167_ZH_DERIVATIVE_BOUND_ROWS"])
    channels = {row["channel"] for row in bounds if row["owner"] == "delta_ZH"}
    add(
        "VAL4167_3_bound_channels",
        "fallback bound rows cover all six ZH leak channels plus kappa_star",
        channels == {"time", "species", "frame", "range", "environment", "readout"} and any(row["owner"] == "kappa_star" for row in bounds),
        str(bounds),
    )

    bound_text = "\n".join(",".join(row.values()) for row in bounds)
    add(
        "VAL4167_4_bound_nonclaim",
        "bound rows remain nonclaim and carry missing source/numeric status until filled",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" and row["source_status"] == "not_source_backed_for_claim" for row in bounds)
        and "MISSING_NUMERIC_INPUT" in bound_text,
        bound_text,
    )

    decisions = parse_csv(outputs["P8_Y5_R2FR_4167_BRANCH_DECISION"])
    decision_text = "\n".join(",".join(row.values()) for row in decisions)
    add(
        "VAL4167_5_decision",
        "branch decision selects parent adoption or first real derivative-bound source row",
        all(token in decision_text for token in ["topological_kappa_star_lock", "ZH_and_kappa_derivative_bounds", NEXT_TARGET]),
        decision_text,
    )

    firewall = parse_csv(outputs["P8_Y5_R2FR_4167_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add(
        "VAL4167_6_firewall",
        "firewall blocks parent-adoption, boundary, source-label and numerical-G overclaims",
        all(token in firewall_text for token in ["parent action", "Boundary", "source, species", "numerical value of G_N"]),
        firewall_text,
    )

    formal_text = read_text(FORMAL_183_PATH)
    add(
        "VAL4167_7_formal_183",
        "formal 183 bridge exists and records topological action, d kappa lock, fallback bound law and next target",
        FORMAL_183_PATH.exists()
        and all(token in formal_text for token in ["PPC4161_TOPOLOGICAL_KAPPA_STAR_LOCK_OR_ZH_BOUND", "S_top[kappa_*, A_3]", "d(kappa_*) = 0", "R_A^G", NEXT_TARGET]),
        "formal 183 checked",
    )

    claims = parse_csv(CLAIMS_PATH)
    l008 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add(
        "VAL4167_8_claim_row",
        "claims register contains one L-008 private nonclaim row",
        len(l008) == 1 and l008[0].get("status") == "private_candidate_nonclaim_public_claim_false" and "public_claim=false" in l008[0].get("current_evidence", ""),
        str(l008),
    )

    spine_text = read_text(SPINE_PATH)
    add(
        "VAL4167_9_spine",
        "spine contains 4167 marker, claim row, topological action and next target",
        all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "S_top[kappa_*, A_3]", NEXT_TARGET]),
        "spine checked",
    )

    status = parse_csv(outputs["P8_Y5_R2FR_4167_STATUS"])
    add(
        "VAL4167_10_status",
        "status records lemma constructed, parent unsigned, no numeric G, bound rows created and next target",
        len(status) == 1
        and status[0]["topological_constancy_lemma_constructed"] == "True"
        and status[0]["topological_sector_parent_adopted"] == "False"
        and status[0]["numeric_G_predicted"] == "False"
        and status[0]["ZH_kappa_derivative_bound_rows_created"] == "True"
        and status[0]["next_target"] == NEXT_TARGET,
        str(status),
    )

    next_loaded = parse_csv(outputs["P8_Y5_R2FR_4167_NEXT_TARGET"])
    add(
        "VAL4167_11_next",
        "next target records parent adoption route and derivative-bound source route",
        len(next_loaded) == 1
        and next_loaded[0]["next_target"] == NEXT_TARGET
        and "parent-adopt" in "\n".join(next_loaded[0].values())
        and "source-backed derivative-bound" in "\n".join(next_loaded[0].values()),
        str(next_loaded),
    )

    doc_text = read_text(DOC_PATH)
    add(
        "VAL4167_12_doc",
        "checkpoint doc records derivation attempt, unsigned clauses, fallback bound law and verdict",
        all(token in doc_text for token in ["delta_A3 S_top", "d(kappa_*) = 0", "parent adoption unsigned", "R_A^G", "not another vague missingness loop", NEXT_TARGET]),
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
        "VAL4167_13_no_claim_rows",
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
        "VAL4167_14_compile",
        "generator compiles and pycache is removed",
        compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(),
        compile_details,
    )

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_183()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4167_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4167_TOPOLOGICAL_KAPPA_LOCK_ATTEMPT"], topological_attempt_rows())
    write_csv(outputs["P8_Y5_R2FR_4167_THEOREM_STATUS"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4167_ZH_DERIVATIVE_BOUND_ROWS"], derivative_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4167_BRANCH_DECISION"], branch_decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4167_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4167_STATUS"], status_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4167_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4167_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_183_PATH}")
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
