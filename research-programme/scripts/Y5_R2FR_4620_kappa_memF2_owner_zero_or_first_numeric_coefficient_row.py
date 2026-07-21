from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4620"
CLAIM_ID = "L-462"
BRANCH_ID = "MTS_R2FR_Y5_KAPPA_MEMF2_OWNER_ZERO_4620"
MARKER = "PPC4161_KAPPA_MEMF2_OWNER_ZERO_OR_FIRST_NUMERIC_COEFFICIENT_ROW_4620"
PACKET_MARKER = "PPC4161_PACKET_KAPPA_MEMF2_OWNER_ZERO_4620"
DECISION = "KAPPA_MEMF2_ZERO_ROUTES_EXACT_FINITE_NUMERIC_ROW_TEMPLATE_READY_NONCLAIM"
NEXT_TARGET = "4621-Y5-R2FR-Zmem-M2mem-positive-operator-source-or-bound-row.md"

DOC_PATH = POST / "4620-Y5-R2FR-kappa-memF2-owner-zero-or-first-numeric-coefficient-row.md"
FORMAL_PATH = FORMAL / "636-PPC4161-kappa-memF2-owner-zero-or-first-numeric-coefficient-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4620_SOURCE_REGISTER.csv"
ZERO_ROUTE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_ZERO_ROUTES.csv"
NUMERIC_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv"
BOUND_IMPACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_CMEMORY_BOUND_IMPACT_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4620_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4620_VALIDATION.csv"

CSV_4619_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4619_NEXT_TARGET.csv"
CSV_4619_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv"
CSV_4619_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4619_KAPPA_MEMF2_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4619_CLASS = SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_CLASSIFICATION.csv"
CSV_4618_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4618_MEMORY_CLASS_SCALAR_NOHAIR_THEOREM.csv"
CSV_4616_PROOF = SOURCE_DIR / "P8_Y5_R2FR_4616_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
CSV_4437_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_ZERO_ROWS.csv"
CSV_4437_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_SURVIVOR_ROWS.csv"
CSV_4506_EXTREMUM = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_1099_COUNTER = SOURCE_DIR / "P8_Y5_R10_1099_COUNTEREXAMPLE_LEDGER.csv"
CSV_1099_EXCLUSION = SOURCE_DIR / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
CSV_1235_MD = POST / "1235-Y5-R10-unique-F2-typed-coefficient-domain-or-QCD-color-edge-owner.md"
CSV_1312_MD = POST / "1312-Y5-R10-RAB-b-alpha-no-vertex-or-source-backed-coefficient.md"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4620_00_4619_next", CSV_4619_NEXT, "4620-Y5-R2FR-kappa-memF2-owner-zero-or-first-numeric-coefficient-row.md", "4619 selected kappa_memF2."),
        ("SRC4620_01_4619_theorem", CSV_4619_THEOREM, "FMO4619_3_finite_derivative_law", "4619 finite derivative law."),
        ("SRC4620_02_4619_source", CSV_4619_SOURCE, "KMF4619_0_kappa_memF2", "4619 kappa source row."),
        ("SRC4620_03_4619_class", CSV_4619_CLASS, "OWN4619_2_linear_mixed", "4619 owner classification."),
        ("SRC4620_04_4618_nohair", CSV_4618_THEOREM, "MCS4618_3_extremum_double_zero_route", "4618 extremum route."),
        ("SRC4620_05_4616_counter", CSV_4616_PROOF, "VIP4616_2_scalar_functional_countermodel", "4616 scalar F2 countermodel."),
        ("SRC4620_06_4437_zero", CSV_4437_ZERO, "ZERO4437_0_C_XF2", "4437 fixed branch C_XF2 zero."),
        ("SRC4620_07_4437_survivor", CSV_4437_SURVIVOR, "SURV4437_1_global_unique_F2", "4437 global F2 survivor."),
        ("SRC4620_08_4506_extremum", CSV_4506_EXTREMUM, "MEXT4506_1_branch_extremum", "4506 branch extremum."),
        ("SRC4620_09_4506_body", CSV_4506_BODY, "BCIN4506_0_memory_density", "4506 memory body-charge law."),
        ("SRC4620_10_1099_counter", CSV_1099_COUNTER, "CX1099_1_fX", "1099 fX F2 counterexample."),
        ("SRC4620_11_1099_exclusion", CSV_1099_EXCLUSION, "EXC1099_1_U1_gauge", "1099 symmetry exclusion audit."),
        ("SRC4620_12_1235_typed", CSV_1235_MD, "UF21235_1_typed_domain_route", "1235 typed coefficient domain route."),
        ("SRC4620_13_1312_alpha", CSV_1312_MD, "BA1312_3_no_hidden_fF2", "1312 hidden F2 alpha wound."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def zero_route_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": "KZ4620_0_typed_domain_zero",
            "route": "typed coefficient-domain exclusion",
            "statement": "If Arg(Coeff(F_Q^2)) excludes memory/hidden scalar objects, kappa_memF2 is ill-typed and equals zero.",
            "proof_value": "This is the strongest clean route because it removes the operator before any local source or no-hair estimate.",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "needed_inputs": "parent object-language certificate for Coeff(F_Q^2); memory scalar sort; no readout/radiative reentry",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "KZ4620_1_fixed_branch_zero",
            "route": "fixed q-basic standard branch",
            "statement": "In the fixed q-basic visible branch, no independent MTS-visible F2 slot exists, so kappa_memF2=0 branch-conditionally.",
            "proof_value": "Imports the 4437 C_XF2=0 result and applies it to the memory coefficient only inside the same branch.",
            "current_status": "PRIVATE_BRANCH_ZERO_NOT_GLOBAL",
            "needed_inputs": "same branch: fixed lambda_A, fixed g_J, no hidden coefficient slot, readout after variation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "KZ4620_2_branch_extremum_zero",
            "route": "branch extremum/double-zero",
            "statement": "If Z_Q_eff(m)=Z_Q0+1/2 Z2_mem delta_m^2+... at the selected branch, then kappa_memF2=partial_m Z_Q_eff|0=0.",
            "proof_value": "This is weaker than no-Hom but still useful: it kills first-order C_memory_F2 while leaving quadratic/profile rows explicit.",
            "current_status": "EXTREMUM_NOT_PARENT_SIGNED_FOR_EM_F2",
            "needed_inputs": "parent-selected EM coefficient functional, extremum condition, readout/radiative stability",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "KZ4620_3_shift_or_selection_symmetry",
            "route": "exact memory shift/selection symmetry",
            "statement": "If the parent memory symmetry permits only derivative or even dependence on m_mem in visible EM coefficients, then the linear kappa_memF2 term is forbidden.",
            "proof_value": "This is a possible derivation route, but only if the symmetry is parent-owned and survives boundary/readout projection.",
            "current_status": "SYMMETRY_NOT_PARENT_SIGNED",
            "needed_inputs": "parent memory transformation law; EM coefficient transformation; anomaly/readout closure",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "route_id": "KZ4620_4_countermodel",
            "route": "mixed scalar operator countermodel",
            "statement": "If the target exists and no symmetry/domain rule excludes it, DeltaS=-(1/4)int mu_obs kappa_memF2 delta_m F_Q^2 is legal.",
            "proof_value": "This prevents a fake zero: ordinary covariance and U1 gauge symmetry do not remove the mixed coefficient.",
            "current_status": "COUNTERMODEL_RETAINED",
            "needed_inputs": "source-backed kappa_memF2 or theorem-zero route",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def numeric_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KNUM4620_0_first_numeric_template",
            "symbol": "kappa_memF2",
            "quantity": "linear memory/F2 Maxwell kinetic coefficient",
            "definition": "partial_m Z_Q_eff at selected branch",
            "normal_form": "Z_Q_eff(m)=Z_Q0+kappa_memF2 delta_m+O(delta_m^2)",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "units": "Maxwell coefficient per memory-field unit",
            "source_required": "parent EM coefficient functional or EFT/readout matching source; not inferred from bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KNUM4620_1_dimensionless_ratio",
            "symbol": "epsilon_memF2",
            "quantity": "dimensionless F2-memory derivative",
            "definition": "epsilon_memF2 := kappa_memF2/Z_Q_eff_min",
            "normal_form": "C_memory_F2=|epsilon_memF2| Delta_v m_mem",
            "value": "MISSING_KAPPA_AND_ZQEFF",
            "units": "per memory-field unit",
            "source_required": "kappa_memF2 plus positive Z_Q_eff_min",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KNUM4620_2_zero_certificate",
            "symbol": "ZK_memF2",
            "quantity": "kappa zero certificate",
            "definition": "one of typed-domain zero, fixed-branch zero, branch extremum, or exact shift symmetry",
            "normal_form": "kappa_memF2=0",
            "value": "MISSING_PARENT_ZERO_CERTIFICATE",
            "units": "boolean certificate",
            "source_required": "same-branch parent signature with source path",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def impact_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "impact_id": "IM4620_0_Cmemory",
            "quantity": "C_memory_F2",
            "formula": "C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem",
            "if_zero": "kappa_memF2=0 removes the first-order memory/F2 contribution from H_XF2",
            "if_finite": "requires Zmem/M2mem/rho/Qboundary amplitude row before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "impact_id": "IM4620_1_HXF2",
            "quantity": "H_XF2",
            "formula": "H_XF2 <= H_XF2_without_memory + |epsilon_memF2| Delta_v m_mem",
            "if_zero": "memory term drops from the EM Hom vector",
            "if_finite": "feeds clock/PPN/R10/orbital arenas only after K_A/tau_A projections",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "impact_id": "IM4620_2_next_operator",
            "quantity": "Delta_v m_mem",
            "formula": "Delta_v m_mem bound depends on Z_mem, M2_mem, rho_mem and Q_boundary_mem",
            "if_zero": "positive no-hair removes memory profile",
            "if_finite": "4621 should source positive-operator rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4620_0_no_symmetry_shortcut",
            "rule": "Do not ban kappa_memF2 using ordinary covariance or U1 gauge invariance.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4620_1_same_branch_only",
            "rule": "Do not combine fixed-branch F2 zero with dynamic-branch memory amplitude rows.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4620_2_no_numeric_backfit",
            "rule": "Do not define kappa_memF2 by saturating R10/clock/PPN/WEP bounds.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4620_0_parent_domain",
            "claim_blocked": "kappa_memF2=0 by typed domain",
            "missing_signature": "Arg(Coeff(F_Q^2)) excludes memory/hidden scalar sorts",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4620_1_extremum",
            "claim_blocked": "kappa_memF2=0 by branch extremum",
            "missing_signature": "parent EM coefficient functional has partial_m Z_Q_eff=0 at selected branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4620_2_numeric_row",
            "claim_blocked": "finite memory/F2 scoring",
            "missing_signature": "kappa_memF2, Z_Q_eff_min, Z_mem, M2_mem, rho_mem, Q_boundary_mem",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4620_0_zero",
            "requirement": "same-branch typed-domain/no-Hom, fixed branch, extremum, or exact symmetry certificate for kappa_memF2=0",
            "current_status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4620_1_numeric",
            "requirement": "source-backed kappa_memF2 and Z_Q_eff_min, plus Zmem/M2mem/rho/boundary profile rows",
            "current_status": "BLOCKED_NUMERIC_ROWS_MISSING",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4620_0",
            "decision": DECISION,
            "what_changed": "kappa_memF2 now has exact zero gates and a first numeric row template; no coefficient can hide in generic memory language.",
            "claim_status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "exact_path": "typed-domain/no-Hom, fixed branch, branch extremum, or exact symmetry",
            "fallback_path": "source kappa_memF2 and Z_Q_eff_min, then source Zmem/M2mem/rho/Qboundary for Delta_v m_mem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "kappa_memF2 zero routes and first numeric row template are written; next is Zmem/M2mem positive-operator sourcing or bound row.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "why": "Even with kappa_memF2 isolated, finite scoring requires the memory amplitude operator values.",
            "derive_path": "prove Z_mem/M2_mem positive no-hair and rho_mem=Q_boundary_mem=0 on the same branch",
            "fallback_path": "fill source-backed Z_mem, M2_mem, rho_mem and Q_boundary_mem rows for Delta_v m_mem",
            "claim_allowed": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4620 - kappa_memF2 Owner Zero Or First Numeric Coefficient Row

Generated UTC: `{now}`

Marker: `{MARKER}`

## Result

4620 names the first coefficient that must either vanish or be sourced:

```text
kappa_memF2 := partial_m Z_Q_eff | branch
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem
```

The clean zero gates are:

```text
Arg(Coeff(F_Q^2)) excludes m_mem,
or fixed q-basic standard branch has no F2 slot,
or partial_m Z_Q_eff|branch = 0,
or exact parent memory symmetry forbids the linear term.
```

If none is signed, the first numeric row is `kappa_memF2`, followed by `Z_Q_eff_min`, `Z_mem`, `M2_mem`, `rho_mem`, and `Q_boundary_mem`.

## Source Register

{markdown_table(tables["sources"])}

## kappa_memF2 Zero Routes

{markdown_table(tables["zero_routes"])}

## First Numeric Row Nonclaim

{markdown_table(tables["numeric_rows"])}

## C_memory Bound Impact Rows

{markdown_table(tables["impact"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

`{NEXT_TARGET}`
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 636 - kappa_memF2 Owner Zero Or First Numeric Coefficient Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Coefficient

```text
kappa_memF2 := partial_m Z_Q_eff | branch
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem
```

## Zero Gates

`kappa_memF2=0` follows only from same-branch typed-domain/no-Hom, fixed q-basic standard branch, branch extremum, or exact parent memory symmetry.

## Finite Gate

If the mixed operator survives, `kappa_memF2` must be source-backed before any R10, PPN, clock, WEP, orbital or local-GR scoring.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "sector": "local_gr_empirical_interface",
        "claim": "4620 names kappa_memF2 as the first memory/F2 coefficient and stages exact zero gates plus a nonclaim first numeric row template.",
        "evidence": "Generated kappa zero routes, numeric row templates, C_memory bound impacts, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "kappa_memF2_zero_routes_and_first_numeric_template_nonclaim",
        "next_action": NEXT_TARGET,
        "risk": "Killing kappa_memF2 by ordinary symmetry, mixing branches, or back-fitting coefficient values from empirical limits.",
        "owner": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until kappa_memF2 and the memory amplitude operator rows are parent-zero or source-backed.",
    }
    existing = read_text(CLAIMS_PATH)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not existing.endswith("\n"):
            handle.write("\n")
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    missing_sources = [row["source_id"] for row in tables["sources"] if not row["path_exists"] or not row["needle_found"]]
    add("VAL4620_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, ZERO_ROUTE_CSV, NUMERIC_ROW_CSV, BOUND_IMPACT_CSV, CONTROL_CSV,
        BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4620_01_csv_parse", csv_ok, ";".join(details))

    zero_text = "\n".join(str(row) for row in tables["zero_routes"])
    numeric_text = "\n".join(str(row) for row in tables["numeric_rows"])
    impact_text = "\n".join(str(row) for row in tables["impact"])
    add("VAL4620_02_zero_routes", "typed coefficient-domain exclusion" in zero_text and "branch extremum" in zero_text and "COUNTERMODEL_RETAINED" in zero_text, "zero routes plus countermodel present")
    add("VAL4620_03_numeric_template", "kappa_memF2" in numeric_text and "epsilon_memF2" in numeric_text and "MISSING_NUMERIC_OR_DERIVED_ZERO" in numeric_text, "numeric template present")
    add("VAL4620_04_impact_rows", "C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem" in impact_text and "Z_mem" in impact_text, "impact rows present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4620_05_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4620_06_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4620_07_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4620_08_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4620_09_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4620_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4620_11_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4620_12_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4620_13_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4620_OVERALL", all(row["status"] == "PASS" for row in rows), "4620 kappa_memF2 checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "zero_routes": zero_route_rows(now),
        "numeric_rows": numeric_rows(now),
        "impact": impact_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(ZERO_ROUTE_CSV, tables["zero_routes"])
    write_csv(NUMERIC_ROW_CSV, tables["numeric_rows"])
    write_csv(BOUND_IMPACT_CSV, tables["impact"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - kappa_memF2 Owner Zero Or First Numeric Coefficient Row

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4620 names the first coefficient: `kappa_memF2 := partial_m Z_Q_eff|branch`. It is zero only by same-branch typed-domain/no-Hom, fixed q-basic standard branch, branch extremum, or exact parent memory symmetry. If none is signed, the finite law is `C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem`; the next work is to source `Z_mem/M2_mem/rho_mem/Q_boundary_mem` or prove their positive no-hair zero.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - kappa_memF2 Owner Zero Or First Numeric Coefficient Row

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now routes the memory/F2 branch through one named coefficient and one named amplitude operator. Next target: prove/source the `Z_mem/M2_mem` positive-operator row or bound the finite amplitude.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4620 validation failed: {failed}")
    print(f"4620 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
