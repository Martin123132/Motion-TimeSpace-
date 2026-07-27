from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4345"
CLAIM_ID = "L-186"
BRANCH = "MTS_R2FR_Y5_FIRST_SOURCE_BACKED_OWNER_TAIL_OR_KPERP_SCORE_ROW_4345"
DECISION = "FIRST_NORMALIZED_OWNER_TAIL_AND_KPERP_SCORE_ROWS_BUILT_SOURCE_FORMULA_BACKED_NUMERIC_NONCLAIM"
MARKER = "PPC4161_FIRST_SOURCE_BACKED_OWNER_TAIL_OR_KPERP_SCORE_ROW_4345"
PACKET_MARKER = "PPC4161_PACKET_FIRST_SOURCE_BACKED_OWNER_TAIL_OR_KPERP_SCORE_ROW_4345"
NEXT_TARGET = "4346-Y5-R2FR-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md"

FORMAL_PATH = FORMAL / "361-PPC4161-first-source-backed-owner-tail-or-Kperp-score-row.md"
DOC_PATH = POST / "4345-Y5-R2FR-first-source-backed-owner-tail-or-Kperp-score-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4345_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

LAMBDA1_DIRICHLET_UNIT = math.pi**2
LAMBDA_RI_SMOKE = LAMBDA1_DIRICHLET_UNIT
STRICT_UNIT_CEILING = 1.0e-16

ARENA_GATES = [
    ("delta_phi_fraction", 1.0e-5, "dimensionless", "59-local-ppn-branch-framework.md:112"),
    ("delta_gamma", 1.0e-5, "dimensionless", "59-local-ppn-branch-framework.md:113"),
    ("delta_beta", 1.0e-4, "dimensionless", "59-local-ppn-branch-framework.md:114"),
    ("alpha1", 1.0e-4, "dimensionless", "59-local-ppn-branch-framework.md:115"),
    ("alpha2", 1.0e-5, "dimensionless", "59-local-ppn-branch-framework.md:116"),
    ("eta_AB", 1.0e-13, "dimensionless", "59-local-ppn-branch-framework.md:117"),
    ("Gdot_over_G", 4.0e-14, "per_year", "59-local-ppn-branch-framework.md:118"),
    ("chi_local_leak_fraction", 1.0e-5, "dimensionless", "59-local-ppn-branch-framework.md:119"),
    ("clock_delta_z", 1.0e-16, "dimensionless", "59-local-ppn-branch-framework.md:120"),
]

SOURCES = [
    (
        "SRC4345_00_4344_next",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "4345-Y5-R2FR-first-source-backed-owner-tail-or-Kperp-score-row.md",
        "4344 handoff selecting first source-backed score row.",
    ),
    (
        "SRC4345_01_4344_lambda",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "lambda_RI := Z_RI,min lambda_1(D_RI) + M_RI,min^2 - Eta_RI > 0,",
        "Adjoint positivity formula.",
    ),
    (
        "SRC4345_02_4344_owner_tail",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "Y_owner_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI",
        "Owner-tail score formula.",
    ),
    (
        "SRC4345_03_4344_kperp",
        FORMAL / "360-PPC4161-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md",
        "Y_Kperp_i := |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)",
        "Kperp score formula.",
    ),
    (
        "SRC4345_04_59_targets",
        FORMAL / "59-local-ppn-branch-framework.md",
        "The first local branch gate uses conservative internal targets:",
        "Local arena gate table.",
    ),
    (
        "SRC4345_05_59_clock",
        FORMAL / "59-local-ppn-branch-framework.md",
        "| `clock_delta_z` | `<= 1e-16` |",
        "Strict clock ceiling.",
    ),
    (
        "SRC4345_06_217_strict_unit",
        FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md",
        "The strict unit-weight dimensionless ceiling is `1e-16` from `clock_delta_z`",
        "Existing Kperp strict unit-weight diagnostic.",
    ),
    (
        "SRC4345_07_327_poincare",
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "Poincare/Dirichlet collar gap",
        "Dirichlet/Poincare gap precedent.",
    ),
    (
        "SRC4345_08_218_kperp_inverse",
        FORMAL / "218-PPC4161-parent-tensor-operator-LT-coercivity.md",
        "||K_perp|| <= (|S_T|+|B_T|+|I_T|+|Z_Tmode|)/(Z_T lambda_D + M_T^2).",
        "Kperp inverse-bound source.",
    ),
    (
        "SRC4345_09_216_hyperbolic_guard",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "elliptic/static proof != hyperbolic incoming-mode proof.",
        "Static proof firewall.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
        line_number = find_line(path, needle)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
            }
        )
    return rows


def lambda_rows() -> List[Dict[str, str]]:
    return [
        {
            "lambda_id": "LAM4345_0_dirichlet_unit_smoke",
            "quantity": "lambda_RI",
            "formula": "lambda_RI=Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI",
            "normalization": "unit Dirichlet interval/collar smoke: ell_RI=1, Z_RI,min=1, M_RI,min^2=0, Eta_RI=0",
            "lambda1_value": f"{LAMBDA1_DIRICHLET_UNIT:.17g}",
            "lambda_RI_value": f"{LAMBDA_RI_SMOKE:.17g}",
            "positive": str(LAMBDA_RI_SMOKE > 0),
            "source_backed_formula": "True",
            "numeric_dry_run": "True",
            "claim_valid": "False",
            "valid_for_claim": "False",
            "notes": "analytic Poincare smoke row only; real collar geometry, units, Ricci correction and Eta_RI remain unsourced",
        },
        {
            "lambda_id": "LAM4345_1_real_claim_gate",
            "quantity": "lambda_RI_real",
            "formula": "Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI > 0",
            "normalization": "physical collar",
            "lambda1_value": "MISSING_REAL_COLLAR_SPECTRUM",
            "lambda_RI_value": "MISSING_REAL_VALUE",
            "positive": "UNPROVEN",
            "source_backed_formula": "True",
            "numeric_dry_run": "False",
            "claim_valid": "False",
            "valid_for_claim": "False",
            "notes": "must be filled before local-GR or local-test claim",
        },
    ]


def arena_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "arena_id": f"GATE4345_{index:02d}_{name}",
            "observable": name,
            "bound": f"{bound:.17g}",
            "units": units,
            "source": source,
            "used_as_claim_bound": "False",
            "valid_for_claim": "False",
        }
        for index, (name, bound, units, source) in enumerate(ARENA_GATES)
    ]


def owner_tail_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for name, bound, units, source in ARENA_GATES:
        residual_ceiling = LAMBDA_RI_SMOKE * bound
        rows.append(
            {
                "score_id": f"OWN4345_{name}",
                "arena": name,
                "formula": "Y_owner_a = R_Lambda/lambda_RI with Pi_a^RI=C_Lambda=1 and B_RI=I_RI=0",
                "lambda_RI_used": f"{LAMBDA_RI_SMOKE:.17g}",
                "arena_bound": f"{bound:.17g}",
                "R_Lambda_ceiling_normalized": f"{residual_ceiling:.17g}",
                "units": units,
                "source": source,
                "score_status": "NORMALIZED_DRY_RUN_ONLY",
                "claim_valid": "False",
                "valid_for_claim": "False",
                "notes": "real Pi, C_Lambda, B_RI, I_RI, units and lambda_RI must replace unit smoke values",
            }
        )
    return rows


def kperp_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for name, bound, units, source in ARENA_GATES:
        rows.append(
            {
                "score_id": f"KPERP4345_{name}",
                "arena": name,
                "formula": "Y_Kperp_i=|W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)",
                "unit_weight_product_ceiling": f"{bound:.17g}",
                "units": units,
                "source": source,
                "strict_global_ceiling": f"{STRICT_UNIT_CEILING:.17g}",
                "score_status": "NORMALIZED_DRY_RUN_ONLY",
                "claim_valid": "False",
                "valid_for_claim": "False",
                "notes": "if W_i^K=1 and units are dimensionless, product must be below this arena bound; real transfer matrix required",
            }
        )
    rows.append(
        {
            "score_id": "KPERP4345_STRICT_UNIT_WEIGHT",
            "arena": "strict_unit_weight_all_dimensionless",
            "formula": "max_i Y_Kperp_i <= min dimensionless local gate",
            "unit_weight_product_ceiling": f"{STRICT_UNIT_CEILING:.17g}",
            "units": "dimensionless",
            "source": "217-PPC4161-Kperp-finite-coefficient-vector.md:37",
            "strict_global_ceiling": f"{STRICT_UNIT_CEILING:.17g}",
            "score_status": "STRICT_DIAGNOSTIC",
            "claim_valid": "False",
            "valid_for_claim": "False",
            "notes": "existing strict diagnostic from clock_delta_z; not a physical pass",
        }
    )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4345_0_current",
            "branch_input": "current corpus through 4344",
            "action": "RUN_NORMALIZED_NONCLAIM_SCORE_ROWS",
            "output": "lambda_RI unit smoke positive; owner-tail and Kperp product ceilings computed for internal local gates",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4345_1_claim_future",
            "branch_input": "real lambda_RI, B_RI, I_RI, C_T, S_T, B_T, I_T, Z_T, W_i^K and arena projections",
            "action": "RUN_CLAIM_ELIGIBLE_SCORE_AFTER_SOURCE_BACKING",
            "output": "compare real owner-tail/Kperp residuals against local gates",
            "claim_policy": "claim only after all rows are real, sourced, fixed before scoring and below gates",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4345_0",
            "forbidden_shortcut": "Treating unit Dirichlet lambda_RI smoke as the real collar spectrum",
            "reason": "real collar geometry, boundary choice, units, Ricci correction and Eta_RI remain unsourced",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4345_1",
            "forbidden_shortcut": "Treating unit W_i^K as the physical arena transfer",
            "reason": "real W_i^K and dimensions must be derived before claim scoring",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4345_2",
            "forbidden_shortcut": "Ignoring B_RI or I_RI in owner-tail scoring",
            "reason": "boundary and incoming-mode terms are separate score rows unless proved zero",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4345_3",
            "forbidden_shortcut": "Calling normalized dry-run score rows empirical evidence",
            "reason": "these rows validate the scoring contract only, not the physical values",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4345_0",
            "decision": DECISION,
            "reason": "4345 creates the first executable local owner-tail/Kperp score rows using sourced formulas and internal gate values, while marking all numeric rows as normalized nonclaim smoke until real coefficients are supplied",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4345_0",
            "item": "lambda_RI",
            "status": "UNIT_DIRICHLET_SMOKE_POSITIVE_REAL_VALUE_OPEN",
            "notes": f"lambda_RI_smoke={LAMBDA_RI_SMOKE:.6g}",
        },
        {
            "status_id": "STAT4345_1",
            "item": "owner-tail score",
            "status": "NORMALIZED_CEILINGS_COMPUTED",
            "notes": "R_Lambda ceilings equal lambda_RI_smoke times each arena gate under unit transfer",
        },
        {
            "status_id": "STAT4345_2",
            "item": "Kperp score",
            "status": "STRICT_UNIT_WEIGHT_CEILING_1E_MINUS_16",
            "notes": "strict diagnostic inherited from clock_delta_z",
        },
        {
            "status_id": "STAT4345_3",
            "item": "next target",
            "status": "REAL_VALUES_OR_CLEAN_SECTOR",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4345_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the real lambda_RI and Kperp/owner-tail coefficients be sourced, or can clean sector/zero theorems remove them before scoring?",
            "preferred_route": "source/sign physical lambda_RI, B_RI=0, I_RI=0 and Kperp clean sector",
            "fallback_route": "fill real numeric C_T,S_T,B_T,I_T,Z_T,W_i^K, Pi_a^RI, B_RI and I_RI rows and run the nonclaim score table",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 361 PPC4161 first source-backed owner-tail or Kperp score row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, source coupling closure, or a fundamental prediction of `G_N`.

## Result

4345 turns the 4344 score formulas into an executable **normalized nonclaim** score table.

The adjoint smoke row uses a source-backed Dirichlet/Poincare analytic value:

```text
ell_RI=1, Z_RI,min=1, M_RI,min^2=0, Eta_RI=0
lambda_1(D_RI)=pi^2
lambda_RI,smoke=pi^2={LAMBDA_RI_SMOKE:.17g}.
```

This is not the physical collar value. It is a scoring-contract dry run.

For owner-tail scoring under unit transfer:

```text
Y_owner_a = R_Lambda/lambda_RI
R_Lambda <= lambda_RI,smoke * bound_a.
```

For Kperp scoring under unit transfer:

```text
Y_Kperp_i = |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)
```

so with `|W_i^K|=1` the product ceiling is each local arena bound. The strict unit-weight diagnostic is:

```text
C_T(|S_T|+|B_T|+|I_T|+|Z_T|) <= {STRICT_UNIT_CEILING:.1e}.
```

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Lambda Rows

{md_table(tables["lambda"], ["lambda_id", "quantity", "formula", "normalization", "lambda1_value", "lambda_RI_value", "positive", "source_backed_formula", "numeric_dry_run", "claim_valid", "valid_for_claim", "notes"])}

## Arena Gates

{md_table(tables["arena"], ["arena_id", "observable", "bound", "units", "source", "used_as_claim_bound", "valid_for_claim"])}

## Owner Tail Score Rows

{md_table(tables["owner"], ["score_id", "arena", "formula", "lambda_RI_used", "arena_bound", "R_Lambda_ceiling_normalized", "units", "source", "score_status", "claim_valid", "valid_for_claim", "notes"])}

## Kperp Score Rows

{md_table(tables["kperp"], ["score_id", "arena", "formula", "unit_weight_product_ceiling", "units", "source", "strict_global_ceiling", "score_status", "claim_valid", "valid_for_claim", "notes"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4345 Y5-R2FR first source-backed owner-tail or Kperp score row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4345 builds the first executable nonclaim score rows.

```text
lambda_RI,smoke = pi^2 = {LAMBDA_RI_SMOKE:.17g}
R_Lambda ceiling = lambda_RI,smoke * bound_a
Y_Kperp_i = |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)
strict unit-weight ceiling = {STRICT_UNIT_CEILING:.1e}
```

These rows are source-formula-backed and numeric, but not claim-valid: real collar spectrum, transfer constants, units, boundary terms, and Kperp coefficients still have to replace the smoke values.

## Handoff

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4345 creates the first executable normalized nonclaim owner-tail/Kperp score rows. "
                    "Using the source-backed Dirichlet/Poincare smoke normalization ell_RI=1, Z_RI=1, M_RI^2=0 and Eta_RI=0 gives lambda_RI,smoke=pi^2, so owner-tail residual ceilings are R_Lambda<=pi^2*bound_a under unit transfer. "
                    "The Kperp unit-transfer row scores Y_Kperp_i=|W_i^K|C_T(|S_T|+|B_T|+|I_T|+|Z_T|) against the internal local gates, with the strict unit-weight diagnostic 1e-16 inherited from clock_delta_z. "
                    "All numeric rows are nonclaim dry-run rows until real collar spectrum, transfer constants, units, boundary terms and Kperp coefficients are source-backed and fixed before scoring."
                ),
                "4345 source register, lambda rows, arena gates, owner-tail score rows, Kperp score rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_first_normalized_owner_tail_Kperp_score_rows_nonclaim",
                "Replace smoke values with real lambda_RI, B_RI, I_RI, C_T, S_T, B_T, I_T, Z_T, W_i^K and arena projection rows, or prove clean sector/zero theorems.",
                "Treating unit Dirichlet lambda_RI as real collar spectrum; treating unit W_i^K as physical transfer; ignoring B_RI/I_RI; calling normalized dry-run rows empirical evidence.",
            ]
        )


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4345_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4345_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4345_lambda_positive", "lambda_RI smoke row is positive", any(row["lambda_id"] == "LAM4345_0_dirichlet_unit_smoke" and row["positive"] == "True" for row in tables["lambda"]), "lambda")
    add("VAL4345_lambda_not_claim", "real lambda row remains not claim valid", any(row["lambda_id"] == "LAM4345_1_real_claim_gate" and row["claim_valid"] == "False" for row in tables["lambda"]), "lambda")
    add("VAL4345_arena_count", "all internal arena gates are present", len(tables["arena"]) == len(ARENA_GATES), "arena")
    add("VAL4345_owner_rows", "owner-tail rows cover each arena", len(tables["owner"]) == len(ARENA_GATES), "owner")
    add("VAL4345_kperp_rows", "Kperp rows cover arenas plus strict row", len(tables["kperp"]) == len(ARENA_GATES) + 1, "kperp")
    add("VAL4345_strict_ceiling", "strict Kperp unit ceiling is 1e-16", any(row["score_id"] == "KPERP4345_STRICT_UNIT_WEIGHT" and row["unit_weight_product_ceiling"] == f"{STRICT_UNIT_CEILING:.17g}" for row in tables["kperp"]), "kperp")
    add("VAL4345_no_claim_flags", "all valid_for_claim flags false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4345_runner_nonclaim", "current runner is nonclaim dry run", any(row["runner_id"] == "RUN4345_0_current" and "NONCLAIM" in row["action"] for row in tables["runner"]), "runner")
    add("VAL4345_firewalls", "unit smoke and transfer firewalls exist", any("unit Dirichlet" in row["forbidden_shortcut"] for row in tables["firewall"]) and any("unit W_i" in row["forbidden_shortcut"] for row in tables["firewall"]), "firewall")
    add("VAL4345_next_target", "next target is 4346 real values or clean sector", any("4346" in row["next_target"] for row in tables["next"]), "next")
    add("VAL4345_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4345_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4345_post_handoff", "post doc contains handoff", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4345_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4345_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4345_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4345_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4345_SOURCE_REGISTER.csv",
        "lambda": SOURCE_DIR / "P8_Y5_R2FR_4345_LAMBDA_RI_ROWS.csv",
        "arena": SOURCE_DIR / "P8_Y5_R2FR_4345_ARENA_GATES.csv",
        "owner": SOURCE_DIR / "P8_Y5_R2FR_4345_OWNER_TAIL_SCORE_ROWS.csv",
        "kperp": SOURCE_DIR / "P8_Y5_R2FR_4345_KPERP_SCORE_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4345_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4345_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4345_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4345_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4345_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "lambda": lambda_rows(),
        "arena": arena_gate_rows(),
        "owner": owner_tail_rows(),
        "kperp": kperp_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4345 first normalized owner-tail/Kperp score rows

Marker: `{MARKER}`

4345 makes the first local owner-tail/Kperp score table executable. It uses a normalized Dirichlet smoke value `lambda_RI=pi^2` and the internal local gates to compute `R_Lambda` ceilings and Kperp unit-transfer ceilings. The strict Kperp diagnostic remains `1e-16` from `clock_delta_z`; all rows are nonclaim until real transfer constants, units and source coefficients replace the smoke values.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4345 packet first normalized owner-tail/Kperp score rows

Marker: `{PACKET_MARKER}`

Packet update: the owner-tail and Kperp route now has executable nonclaim ceilings. The next work is no longer writing the score formula; it is replacing the normalized smoke inputs with real `lambda_RI`, `B_RI`, `I_RI`, `W_i^K`, `C_T`, `S_T`, `B_T`, `I_T`, and `Z_T` rows or proving the clean sector zero.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
