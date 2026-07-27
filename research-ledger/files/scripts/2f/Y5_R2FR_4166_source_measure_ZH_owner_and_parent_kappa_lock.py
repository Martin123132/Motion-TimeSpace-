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

CHECKPOINT = "4166"
BRANCH_ID = "MTS_R2FR_Y5_ZH_SOURCE_MEASURE_AND_KAPPA_LOCK_4166"
DECISION = "ZH_COMMON_SOURCE_FACTOR_SPLIT_AND_KAPPA_LOCK_CONTRACT_DERIVED_ZH_ONE_ONLY_AS_NORMALIZATION_GAUGE"
DOC_PATH = POST / "4166-Y5-R2FR-source-measure-ZH-owner-and-parent-kappa-lock.md"
FORMAL_182_PATH = FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
CLAIM_ID = "L-007"
SPINE_MARKER = "PPC4161_ZH_KAPPA_LOCK_4166"
NEXT_TARGET = "4167-Y5-R2FR-topological-kappa-star-lock-or-ZH-derivative-bound.md"

SOURCES = {
    "SRC4166_00_recovery_bookmark": (
        POST / "000-recovery-bookmark-20260703-drive-upgrade.md",
        "4166-Y5-R2FR-source-measure-ZH-owner-and-parent-kappa-lock.md",
        "Drive-upgrade recovery bookmark.",
    ),
    "SRC4166_01_4165_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4165_NEXT_TARGET.csv",
        "source-measure Z_H ownership",
        "4165 next-target handoff.",
    ),
    "SRC4166_02_4165_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4165_NO_GO_AND_PARENT_CONTRACT.csv",
        "SOURCE_MEASURE_ZH_REQUIRED",
        "4165 no-go/source-measure contract.",
    ),
    "SRC4166_03_formal_181": (
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "kappa_eff = kappa_* Z_H",
        "Formal 181 coupling bridge.",
    ),
    "SRC4166_04_4155_source_lock": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total)",
        "Most recent worldtube/Hilbert source lock.",
    ),
    "SRC4166_05_HSM541_contract": (
        SOURCE_DIR / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "HSM541_2_observed_worldtube_source",
        "Hamiltonian source-measure contract.",
    ),
    "SRC4166_06_1229_contract": (
        POST / "1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md",
        "THM1229_0_target",
        "Universal source-coupling contract and countermodel.",
    ),
    "SRC4166_07_1016_selector": (
        POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "W_source = closure(supp J_H[tau])",
        "Parent worldtube/source-measure selector contract.",
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
        "claim": "PPC4161 separates the source-measure factor Z_H into a common normalization gauge plus physical leak residuals",
        "current_evidence": "formalization-workbench/182-PPC4161-ZH-source-measure-and-kappa-lock.md records Z_H=Z_0 exp(delta_ZH), common Z_0 absorbable into kappa_*, and derivative/leak gates; public_claim=false",
        "status": "private_nonclaim_public_claim_false",
        "next_test": "Either derive topological/measure ownership of kappa_* and prove delta_ZH channels vanish, or fill Z_H derivative bound rows for time/species/frame/range/environment/readout",
        "key_risk": "Z_H=1 is only a normalization gauge after all physical source-measure leaks are zero; otherwise measured G can hide a real WEP/PPN/clock/orbital residual",
    }
    existing = [row for row in rows if row.get("claim_id") == CLAIM_ID]
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


def write_formal_182() -> None:
    FORMAL_182_PATH.write_text(
        f"""# 182 - PPC4161 ZH Source-Measure And Kappa Lock

Marker: `PPC4161_ZH_SOURCE_MEASURE_AND_KAPPA_LOCK`  
Timestamp UTC: `{now()}`  
Status: `private_spine_branch_nonclaim`  
Claim status: `not_public_local_GR_claim`

## Source-Measure Split
The coupling throat is:

```text
kappa_eff = kappa_* Z_H
G_N = c^4 kappa_* Z_H/(8*pi)
```

The physically useful split is:

```text
Z_H = Z_0 exp(delta_ZH)
```

where `Z_0` is a common source normalization and `delta_ZH` carries all physical source-measure leakage.

## Normalization Gauge
If all local derivative/leak channels vanish,

```text
D_A delta_ZH = 0,  A in {{time,species,frame,range,environment,readout}},
```

then `Z_0` can be absorbed into a redefined local coupling:

```text
kappa_bar = kappa_* Z_0,
Z_H -> 1
```

This is a gauge/normalization choice, not a numerical prediction of `G_N`.

## Physical Residuals
If any `D_A delta_ZH` is nonzero, it produces real local residuals:

```text
Gdot/G = D_t ln(kappa_* Z_H)
eta_species ~ Delta_species delta_ZH
PPN preferred-frame/readout residuals ~ D_frame/readout delta_ZH
range/local-environment residuals ~ D_range/env delta_ZH
```

## Kappa Lock
`kappa_*` is locally safe only if it is parent-owned and source-blind:

```text
D_A ln kappa_* = 0
```

or if every nonzero channel is source-backed and below local bounds.

## Nonclaim
This bridge does not derive the numerical value of `G_N`. It derives the factorization and shows exactly what must be zero or bounded before a local-GR coupling claim can be made.

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

## 12. Local GR Coupling Update - ZH Source-Measure/Kappa Lock

Marker: `{SPINE_MARKER}`  
Source bridge: `182-PPC4161-ZH-source-measure-and-kappa-lock.md`  
Claim register row: `{CLAIM_ID}`

Checkpoint `4166` sharpens the coupling throat:

```text
kappa_eff = kappa_* Z_H,
Z_H = Z_0 exp(delta_ZH).
```

The common source normalization `Z_0` is absorbable into `kappa_*`; the physical content is the leak vector:

```text
D_A delta_ZH,  A in {{time,species,frame,range,environment,readout}}.
```

Thus `Z_H -> 1` is allowed only as a normalization gauge after physical source-measure leaks are zero or bounded. This keeps the local-GR branch honest: measured `G_N` may calibrate one common factor, but it cannot hide species/frame/range/time source residuals.

The next local-GR coupling step is:

```text
{NEXT_TARGET}
```
"""
    SPINE_PATH.write_text(text.rstrip() + section + "\n", encoding="utf-8")
    return "added"


def factorization_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "ZH4166_0_define",
            "Parent-to-Hilbert source measure factor",
            "T_parent^H = Z_H T_H + T_leak",
            "Z_H is the common factor relating the parent source measure to the Hilbert stress used in the local EH equation.",
            "definition",
        ),
        (
            "ZH4166_1_split",
            "Common-plus-leak decomposition",
            "Z_H = Z_0 exp(delta_ZH)",
            "Z_0 is one common normalization; delta_ZH contains time/species/frame/range/environment/readout dependence.",
            "derived_factorization",
        ),
        (
            "ZH4166_2_absorb_common",
            "Absorb one common source normalization into the measured coupling",
            "kappa_bar = kappa_* Z_0; G_N = c^4 kappa_bar/(8*pi)",
            "A universal constant factor is locally indistinguishable from the usual calibrated Newton constant.",
            "derived_gauge_lock",
        ),
        (
            "ZH4166_3_gauge_condition",
            "Normalization gauge condition",
            "Z_H -> 1 is allowed iff delta_ZH=0 or all D_A delta_ZH vanish in local tested channels",
            "Setting Z_H=1 before proving leak silence is a closure assumption, not a derivation.",
            "conditional_not_public_claim",
        ),
        (
            "ZH4166_4_residual_if_fail",
            "Physical leak residual",
            "D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH",
            "All local coupling tests see derivatives or differences of the leak, not the absorbed common factor.",
            "derived_residual_law",
        ),
    ]
    return [
        {
            **common(),
            "factor_id": row[0],
            "name": row[1],
            "equation": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def leak_channel_rows() -> List[Dict[str, str]]:
    data = [
        ("time", "D_t delta_ZH", "Gdot/G and clock/orbital secular drift", "clock/orbital bounds or parent stationary theorem"),
        ("species", "Delta_AB delta_ZH", "WEP/source universality and composition-dependent gravity", "source-label forgetting theorem or WEP component rows"),
        ("frame", "D_frame delta_ZH", "PPN alpha_i/preferred-frame source normalization", "same observed coframe/source-frame theorem"),
        ("range", "D_lambda delta_ZH", "R10/Yukawa/range-dependent effective G", "range-blind source measure theorem or alpha(lambda) bound rows"),
        ("environment", "D_env delta_ZH", "Solar/local-vacuum versus galaxy/cosmology leakage", "local collar no-leak theorem or environment derivative bound"),
        ("readout", "D_readout delta_ZH", "measured GM, detector, clock, and orbital convention absorption", "variation-before-readout plus fixed reference theorem"),
    ]
    return [
        {
            **common(),
            "channel_id": f"ZHL4166_{index}_{name}",
            "channel": name,
            "leak_operator": operator,
            "arena": arena,
            "needed_zero_or_bound": needed,
            "current_status": "not_publicly_closed_zero_inside_PPC4161_only_if_parent_clauses_hold",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for index, (name, operator, arena, needed) in enumerate(data)
    ]


def kappa_lock_rows() -> List[Dict[str, str]]:
    rows = [
        (
            "KL4166_0_local_constant",
            "Local constant branch",
            "D_A ln kappa_* = 0 for A in {time,species,frame,range,environment,readout}",
            "This is sufficient for local Gdot/source universality once delta_ZH channels vanish.",
            "conditional_private_branch",
        ),
        (
            "KL4166_1_parent_owned",
            "Parent ownership condition",
            "kappa_* must be a parent coupling/invariant, not a parameter chosen after local readout",
            "Otherwise kappa_* can absorb source-measure mistakes and hide residuals.",
            "required_not_yet_numeric_prediction",
        ),
        (
            "KL4166_2_topological_option",
            "Topological/superselection option",
            "S_kappa = int A_3 wedge d(kappa_*) or equivalent implies d kappa_*=0 on the local branch",
            "This would lock drift but still would not predict the numerical value without a parent scale law.",
            "candidate_next_route",
        ),
        (
            "KL4166_3_empirical_option",
            "Calibrated-G option",
            "kappa_bar = 8*pi G_N/c^4 is empirical, while D_A ln(kappa_bar)=0 is the tested local condition",
            "This is acceptable if labelled like GR and not advertised as a fundamental prediction.",
            "honest_fallback",
        ),
    ]
    return [
        {
            **common(),
            "lock_id": row[0],
            "name": row[1],
            "equation_or_condition": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "theorem_id": "THM4166_0_ZH_gauge_theorem",
            "statement": "If the parent matter/source measure descends to one common Hilbert source factor and all delta_ZH leak channels vanish, then Z_H may be set to 1 by local normalization gauge.",
            "formula": "Z_H=Z_0 exp(delta_ZH), delta_ZH=0 => kappa_bar=kappa_*Z_0 and Z_H->1",
            "proof_status": "conditional_private_theorem",
            "blocked_part": "parent proof that all leak channels vanish for current full MTS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "THM4166_1_leak_residual_theorem",
            "statement": "If any physical source-measure leak survives, measured G_N can absorb only one common factor and the remaining derivatives/differences are observable residuals.",
            "formula": "D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH",
            "proof_status": "derived_residual_identity",
            "blocked_part": "numeric/source-backed bounds for nonzero leak channels",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def verdict_rows(claim_action: str, spine_action: str) -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "verdict_id": "V4166_0_movement",
            "result": "The source-measure throat is sharpened from 'derive Z_H' to 'split Z_H into common gauge factor plus physical leak vector'.",
            "status": "real_derivation_progress",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "V4166_1_ZH_one",
            "result": "Z_H=1 is permitted only as normalization gauge after leak silence, not as an independent physical theorem.",
            "status": "conditional_private_gauge",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "V4166_2_kappa",
            "result": "Parent kappa_* still needs topological/superselection ownership or it remains calibrated-G fallback.",
            "status": "next_derivation_target",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "verdict_id": "V4166_3_sync",
            "result": f"formal bridge 182 written; claim row action={claim_action}; spine action={spine_action}",
            "status": "formal_nonclaim_sync",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "firewall_id": "FW4166_0_no_magic_ZH",
            "rule": "Do not set Z_H=1 as a physical theorem unless delta_ZH leak channels are parent-zero or bounded.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4166_1_measured_G_not_a_sponge",
            "rule": "Measured G_N may absorb one common normalization, not species/frame/range/time/readout source leaks.",
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "firewall_id": "FW4166_2_no_numerical_G_claim",
            "rule": "This checkpoint does not predict the numerical value of G_N.",
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
            "recovery_bookmark_created": "True",
            "ZH_factorization_derived": "True",
            "ZH_one_as_normalization_gauge_only": "True",
            "leak_residual_vector_defined": "True",
            "parent_kappa_numeric_predicted": "False",
            "formal_182_written": "True",
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
            "why_next": "4166 reduces coupling closure to either a topological/superselection kappa_* lock or explicit Z_H derivative bound rows.",
            "route_A": "derive d kappa_*=0 from a parent topological/superselection sector without importing measured G",
            "route_B": "fill source-backed derivative bounds for delta_ZH in time/species/frame/range/environment/readout channels",
            "fallback": "keep local G_N calibrated and only claim PPC4161 conditional GR-like limit, not a fundamental G prediction",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    DOC_PATH.write_text(
        f"""# 4166 - Source-Measure ZH Owner And Parent Kappa Lock

Timestamp UTC: `{now()}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Recovery Note
This checkpoint continues from the verified drive-upgrade recovery bookmark:

```text
post-checkpoint-work/000-recovery-bookmark-20260703-drive-upgrade.md
```

## Coupling Throat
4165 left:

```text
kappa_eff = kappa_* Z_H,
G_N = c^4 kappa_* Z_H/(8*pi).
```

The new result is the source-measure split:

```text
Z_H = Z_0 exp(delta_ZH).
```

`Z_0` is one common source normalization. It can be absorbed into:

```text
kappa_bar = kappa_* Z_0.
```

This means `Z_H -> 1` is not a miracle. It is a legitimate local normalization gauge only after all physical leak channels in `delta_ZH` vanish or are bounded.

## Physical Leak Vector
The physical content is:

```text
D_A ln G_eff = D_A ln kappa_* + D_A delta_ZH,
A in {{time,species,frame,range,environment,readout}}.
```

So measured `G_N` can hide one common factor, but cannot hide:

- time drift;
- species/source-composition dependence;
- frame/readout dependence;
- range dependence;
- local-environment leakage.

## Conditional ZH Theorem
If the parent matter/source measure descends to one common Hilbert source factor and all leak channels vanish, then:

```text
Z_H=Z_0,  kappa_bar=kappa_*Z_0,  Z_H -> 1.
```

This is a conditional private theorem inside the PPC4161 local branch. It is not a public local-GR claim and not a prediction of the numerical value of `G_N`.

## Kappa Lock
The remaining parent question is now sharp:

```text
D_A ln kappa_* = 0
```

must follow from a parent topological/superselection sector, or else `kappa_bar=8*piG_N/c^4` remains an empirical calibration exactly as in GR.

## Next Target
`{NEXT_TARGET}`

## Outputs
{chr(10).join(f"- `{path}`" for path in outputs.values())}
""",
        encoding="utf-8",
    )


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4166_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4166_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4166_ZH_FACTORIZATION": SOURCE_DIR / "P8_Y5_R2FR_4166_ZH_FACTORIZATION.csv",
        "P8_Y5_R2FR_4166_ZH_LEAK_CHANNELS": SOURCE_DIR / "P8_Y5_R2FR_4166_ZH_LEAK_CHANNELS.csv",
        "P8_Y5_R2FR_4166_KAPPA_LOCK_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4166_KAPPA_LOCK_CONTRACT.csv",
        "P8_Y5_R2FR_4166_THEOREM_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4166_THEOREM_STATUS.csv",
        "P8_Y5_R2FR_4166_VERDICT": SOURCE_DIR / "P8_Y5_R2FR_4166_VERDICT.csv",
        "P8_Y5_R2FR_4166_CLAIM_FIREWALL": SOURCE_DIR / "P8_Y5_R2FR_4166_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4166_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4166_STATUS.csv",
        "P8_Y5_R2FR_4166_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4166_NEXT_TARGET.csv",
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

    sources = parse_csv(outputs["P8_Y5_R2FR_4166_SOURCE_REGISTER"])
    add("VAL4166_0_sources", "all source paths exist and contain required tokens", all(row["exists"] == "True" and row["required_text_found"] == "True" for row in sources), str(sources))

    factors = parse_csv(outputs["P8_Y5_R2FR_4166_ZH_FACTORIZATION"])
    factor_text = "\n".join(",".join(row.values()) for row in factors)
    add("VAL4166_1_factorization", "factorization derives Z_H split, common absorption, gauge condition and residual law", all(token in factor_text for token in ["Z_H = Z_0 exp(delta_ZH)", "kappa_bar = kappa_* Z_0", "Z_H -> 1", "D_A ln G_eff"]), factor_text)

    leaks = parse_csv(outputs["P8_Y5_R2FR_4166_ZH_LEAK_CHANNELS"])
    expected_channels = {"time", "species", "frame", "range", "environment", "readout"}
    add("VAL4166_2_leaks", "leak vector covers all six local derivative/readout channels", {row["channel"] for row in leaks} == expected_channels, str([row["channel"] for row in leaks]))

    locks = parse_csv(outputs["P8_Y5_R2FR_4166_KAPPA_LOCK_CONTRACT"])
    lock_text = "\n".join(",".join(row.values()) for row in locks)
    add("VAL4166_3_kappa_lock", "kappa lock contract covers constant branch, parent ownership, topological option and empirical fallback", all(token in lock_text for token in ["D_A ln kappa_* = 0", "Parent ownership", "S_kappa", "empirical"]), lock_text)

    theorem = parse_csv(outputs["P8_Y5_R2FR_4166_THEOREM_STATUS"])
    theorem_text = "\n".join(",".join(row.values()) for row in theorem)
    add("VAL4166_4_theorem", "theorem rows record conditional Z_H gauge theorem and leak residual identity", all(token in theorem_text for token in ["conditional_private_theorem", "derived_residual_identity", "D_A ln G_eff"]), theorem_text)

    formal_text = read_text(FORMAL_182_PATH)
    add("VAL4166_5_formal_182", "formal 182 bridge exists and records Z_H split, normalization gauge and next target", FORMAL_182_PATH.exists() and all(token in formal_text for token in ["PPC4161_ZH_SOURCE_MEASURE_AND_KAPPA_LOCK", "Z_H = Z_0 exp(delta_ZH)", "kappa_bar = kappa_* Z_0", NEXT_TARGET]), "formal 182 checked")

    claims = parse_csv(CLAIMS_PATH)
    l007 = [row for row in claims if row.get("claim_id") == CLAIM_ID]
    add("VAL4166_6_claim_row", "claims register contains one L-007 private nonclaim row", len(l007) == 1 and l007[0].get("status") == "private_nonclaim_public_claim_false" and "public_claim=false" in l007[0].get("current_evidence", ""), str(l007))

    spine_text = read_text(SPINE_PATH)
    add("VAL4166_7_spine", "spine contains 4166 marker, claim row, Z_H split and next target", all(token in spine_text for token in [SPINE_MARKER, CLAIM_ID, "Z_H = Z_0 exp(delta_ZH)", NEXT_TARGET]), "spine checked")

    firewall = parse_csv(outputs["P8_Y5_R2FR_4166_CLAIM_FIREWALL"])
    firewall_text = "\n".join(",".join(row.values()) for row in firewall)
    add("VAL4166_8_firewall", "firewall blocks magic Z_H=1, measured-G sponge and numerical-G claims", all(token in firewall_text for token in ["Z_H=1", "Measured G_N", "numerical value of G_N"]), firewall_text)

    status = parse_csv(outputs["P8_Y5_R2FR_4166_STATUS"])
    add("VAL4166_9_status", "status records bookmark, factorization, leak vector, nonclaim and next target", len(status) == 1 and status[0]["recovery_bookmark_created"] == "True" and status[0]["ZH_factorization_derived"] == "True" and status[0]["leak_residual_vector_defined"] == "True" and status[0]["parent_kappa_numeric_predicted"] == "False" and status[0]["next_target"] == NEXT_TARGET, str(status))

    next_rows_loaded = parse_csv(outputs["P8_Y5_R2FR_4166_NEXT_TARGET"])
    add(
        "VAL4166_10_next",
        "next target moves to kappa-star topological lock or Z_H derivative bounds",
        len(next_rows_loaded) == 1
        and next_rows_loaded[0]["next_target"] == NEXT_TARGET
        and "delta_ZH" in "\n".join(next_rows_loaded[0].values()),
        str(next_rows_loaded),
    )

    doc_text = read_text(DOC_PATH)
    add("VAL4166_11_doc", "checkpoint doc records recovery, Z_H split, leak vector, kappa lock and next target", all(token in doc_text for token in ["000-recovery-bookmark-20260703-drive-upgrade.md", "Z_H = Z_0 exp(delta_ZH)", "D_A ln G_eff", "D_A ln kappa_* = 0", NEXT_TARGET]), "doc tokens checked")

    claim_failures: List[str] = []
    for name, path in outputs.items():
        for index, row in enumerate(parse_csv(path), start=1):
            if row.get("claim_allowed", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:claim_allowed={row.get('claim_allowed')}")
            if row.get("valid_for_claim", "") not in ("", "False"):
                claim_failures.append(f"{name}:{index}:valid_for_claim={row.get('valid_for_claim')}")
    add("VAL4166_12_no_claim_rows", "all generated rows keep claim_allowed/valid_for_claim false", not claim_failures, str(claim_failures))

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
    add("VAL4166_13_compile", "generator compiles and pycache is removed", compile_ok and not (SCRIPT_PATH.parent / "__pycache__").exists(), compile_details)

    return checks


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_formal_182()
    claim_action = ensure_claim_row()
    spine_action = ensure_spine_section()
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4166_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4166_ZH_FACTORIZATION"], factorization_rows())
    write_csv(outputs["P8_Y5_R2FR_4166_ZH_LEAK_CHANNELS"], leak_channel_rows())
    write_csv(outputs["P8_Y5_R2FR_4166_KAPPA_LOCK_CONTRACT"], kappa_lock_rows())
    write_csv(outputs["P8_Y5_R2FR_4166_THEOREM_STATUS"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4166_VERDICT"], verdict_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4166_CLAIM_FIREWALL"], firewall_rows())
    write_csv(outputs["P8_Y5_R2FR_4166_STATUS"], status_rows(claim_action, spine_action))
    write_csv(outputs["P8_Y5_R2FR_4166_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    validation = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4166_VALIDATION.csv"
    write_csv(validation_path, validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"claim_action: {claim_action}")
    print(f"spine_action: {spine_action}")
    print(f"wrote: {FORMAL_182_PATH}")
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
