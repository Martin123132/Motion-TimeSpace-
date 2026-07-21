from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4542"
CLAIM_ID = "L-384"
BRANCH_ID = "MTS_R2FR_Y5_CGAMMA_PARENT_MEMORY_EQUATION_OR_FIRST_BOUND_4542"
MARKER = "PPC4161_CGAMMA_PARENT_MEMORY_EQUATION_OR_FIRST_PROJECTION_BOUND_ROW_4542"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_PARENT_MEMORY_EQUATION_OR_FIRST_PROJECTION_BOUND_ROW_4542"
DECISION = "PARENT_MEMORY_EQUATION_NOT_FOUND_FIRST_CGAMMA_GDOT_PRODUCT_BOUND_PROMOTED_NONCLAIM"
NEXT_TARGET = "4543-Y5-R2FR-cGamma-Gdot-product-bound-to-profile-coefficient-or-parent-memory-operator.md"

FORMAL_PATH = FORMAL / "558-PPC4161-cGamma-parent-memory-equation-or-first-projection-bound-row.md"
DOC_PATH = POST / "4542-Y5-R2FR-cGamma-parent-memory-equation-or-first-projection-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4542_SOURCE_REGISTER.csv"
MEMORY_EQUATION_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_PARENT_MEMORY_EQUATION_AUDIT.csv"
PRODUCT_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_CGAMMA_PRODUCT_BOUND_LAW.csv"
STRICTEST_BOUNDS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_STRICTEST_CGAMMA_PRODUCT_BOUNDS.csv"
FIRST_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_FIRST_SELECTED_BOUND_ROW.csv"
CONVERSION_REQUIREMENTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_PRODUCT_TO_COEFFICIENT_REQUIREMENTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4542_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4542_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4542_00_4541_status",
            "label": "4541 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4541_STATUS.csv",
            "needle": "c_Gamma_projection_bound_route_active",
            "role": "4541 activates c_Gamma projection-bound route",
        },
        {
            "source_id": "SRC4542_01_4541_bounds",
            "label": "4541 projection-bound route",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4541_CGAMMA_PROJECTION_BOUND_ROUTE.csv",
            "needle": "best_first_empirical_fallback",
            "role": "orbital/Gdot selected as first empirical fallback",
        },
        {
            "source_id": "SRC4542_02_4188_nohair",
            "label": "4188 support/no-hair attempt",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_SUPPORT_NOHAIR_PROOF_ATTEMPT.csv",
            "needle": "SPA4188_0_parent_operator",
            "role": "parent memory equation not found",
        },
        {
            "source_id": "SRC4542_03_4188_product_law",
            "label": "4188 product law",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_LAW.csv",
            "needle": "LAW4188_1_linear_bound",
            "role": "finite product-bound identity",
        },
        {
            "source_id": "SRC4542_04_4188_bound_imports",
            "label": "4188 bound imports",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_BOUND_IMPORTS.csv",
            "needle": "IMP4188_B4173_10_Gdot",
            "role": "source-backed Gdot bound import",
        },
        {
            "source_id": "SRC4542_05_4188_runner",
            "label": "4188 product-bound runner",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv",
            "needle": "RUN4188_B4173_10_Gdot",
            "role": "Gdot product row",
        },
        {
            "source_id": "SRC4542_06_4188_strictest",
            "label": "4188 strictest product bounds",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv",
            "needle": "C_Gamma_Gdot",
            "role": "strictest product-bound summary",
        },
        {
            "source_id": "SRC4542_07_4188_priority",
            "label": "4188 priority decision",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4188_PRIORITY_DECISION.csv",
            "needle": "derive_or_fill C_Gamma_metric and C_Gamma_Gdot/orbital first",
            "role": "metric and Gdot/orbital prioritized before R10",
        },
        {
            "source_id": "SRC4542_08_4189_status",
            "label": "4189 projection split",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4189_STATUS.csv",
            "needle": "parent_memory_equation_found",
            "role": "parent memory equation remains missing after projection split",
        },
        {
            "source_id": "SRC4542_09_4190_status",
            "label": "4190 finite profile bounds",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4190_STATUS.csv",
            "needle": "finite_profile_bounds_ready",
            "role": "profile bounds ready but numeric profile absent",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def memory_equation_audit_rows() -> list[dict[str, Any]]:
    attempts = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_SUPPORT_NOHAIR_PROOF_ATTEMPT.csv")
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "audit_id": attempt["attempt_id"].replace("SPA4188", "MEA4542"),
                "required_clause": attempt["required_clause"],
                "old_status": attempt["current_status"],
                "4542_verdict": "PARENT_MEMORY_EQUATION_NOT_FOUND" if attempt["attempt_id"] == "SPA4188_0_parent_operator" else "STILL_UNSIGNED_OR_PARTIAL",
                "why_it_matters": attempt["why_it_matters"],
                "next_action": attempt["next_action"],
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def product_law_rows() -> list[dict[str, Any]]:
    old_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_LAW.csv")
    rows: list[dict[str, Any]] = []
    for old in old_rows:
        rows.append(
            {
                "law_id": old["law_id"].replace("LAW4188", "LAW4542"),
                "statement": old["statement"],
                "consequence": old["consequence"],
                "status": old["status"],
                "current_chain_action": "imported_into_4542",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def strictest_bound_rows() -> list[dict[str, Any]]:
    old_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv")
    rows: list[dict[str, Any]] = []
    for old in old_rows:
        selected = old["effective_product"] == "C_Gamma_Gdot"
        rows.append(
            {
                "bound_id": old["effective_product"].replace("C_Gamma", "B4542_CGamma"),
                "effective_product": old["effective_product"],
                "strictest_observable": old["strictest_observable"],
                "strictest_arena": old["strictest_arena"],
                "max_abs_effective_product": old["max_abs_effective_product"],
                "units": old["units"],
                "source_bound_id": old["source_bound_id"],
                "interpretation": old["interpretation"],
                "selected_first_current_chain": b(selected),
                "claim_status": "source_backed_product_bound_not_cGamma_value",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def first_bound_rows() -> list[dict[str, Any]]:
    runner_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_BOUND_RUNNER.csv")
    gdot = next(row for row in runner_rows if row["effective_product"] == "C_Gamma_Gdot")
    return [
        {
            "first_bound_id": "FB4542_0_CGamma_Gdot",
            "selected_reason": "orbital/Gdot was recommended before R10 and directly tests local Newton/source-coupling drift",
            "arena": gdot["arena"],
            "observable": gdot["observable"],
            "effective_product": gdot["effective_product"],
            "linearized_residual_model": gdot["linearized_residual_model"],
            "unit_normalized_jacobian": gdot["unit_normalized_jacobian"],
            "max_abs_effective_product": gdot["max_abs_effective_product"],
            "units": gdot["units"],
            "source_bound_id": gdot["source_bound_id"],
            "source_id": gdot["source_id"],
            "claim_status": "nonclaim_product_bound_not_cGamma_alone",
            "required_to_convert_to_cGamma": "supply J_Gdot^Gamma and ||P_Gdot Gamma_mem|| with units and no-cancellation guard",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def conversion_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "CR4542_0_formula",
            "requirement": "define C_Gamma_Gdot = J_Gdot^Gamma * c_Gamma * ||P_Gdot Gamma_mem|| + tensor_perp_piece",
            "why": "without the Jacobian and profile norm, the product bound cannot be divided into a bound on c_Gamma",
            "status": "missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "CR4542_1_units",
            "requirement": "state units for J_Gdot^Gamma and the memory profile so C_Gamma_Gdot has units yr^-1",
            "why": "prevents dimensionless/product confusion",
            "status": "missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "CR4542_2_no_cancellation",
            "requirement": "do not cancel C_Gamma_Gdot against kappa drift, metric fit, or ephemeris nuisance terms",
            "why": "the bound is channelwise and must remain a robustness guard",
            "status": "active_guard",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "CR4542_3_parent_operator",
            "requirement": "if a parent memory equation L_Gamma Gamma_mem=J_Gamma is later found, use it to compute or zero the profile before empirical scoring",
            "why": "derivation-first route remains preferred",
            "status": "open_parent_route",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4542_0_parent_memory_equation",
            "gate": "parent memory equation",
            "status": "FAIL_NOT_FOUND",
            "meaning": "no L_Gamma Gamma_mem = J_Gamma parent equation is currently available",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4542_1_first_product_bound",
            "gate": "first cGamma product bound",
            "status": "PASS_NONCLAIM_PRODUCT_BOUND",
            "meaning": "C_Gamma_Gdot <= 2.42e-14 yr^-1 is source-backed as product bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4542_2_cGamma_bound",
            "gate": "bound on c_Gamma itself",
            "status": "BLOCKED_MISSING_JACOBIAN_PROFILE",
            "meaning": "need J_Gdot^Gamma and memory profile norm before dividing the product bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4542_3_R10",
            "gate": "R10 cGamma claim",
            "status": "DEFERRED",
            "meaning": "R10 waits for alpha projection and reviewed bound curve",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4542_4_public_local_GR",
            "gate": "public local GR",
            "status": "BLOCKED_NONCLAIM",
            "meaning": "cGamma has product bounds, not parent zero or coefficient-level bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4542_0",
            "decision": DECISION,
            "meaning": "4542 tries the parent memory equation route and finds it still absent. Instead of stopping at 'missing', it promotes the first concrete source-backed product bound: C_Gamma_Gdot <= 2.42e-14 yr^-1. This is not a c_Gamma value; it is the first current-chain product guard.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4542_0",
            "target": NEXT_TARGET,
            "objective": "convert the C_Gamma_Gdot product bound into a profile/coefficient statement or derive the missing parent memory operator",
            "derive_first": "find L_Gamma Gamma_mem=J_Gamma and compute J_Gdot^Gamma/profile norm",
            "fallback": "keep C_Gamma_Gdot as product bound and add C_Gamma_metric or C_Gamma_vector next",
            "avoid": "calling C_Gamma_Gdot a prediction for c_Gamma itself",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "parent_memory_equation_found": "False",
            "first_product_bound_promoted": "C_Gamma_Gdot",
            "C_Gamma_Gdot_max_abs": "2.42e-14",
            "C_Gamma_Gdot_units": "yr^-1",
            "c_Gamma_value_or_bound_available": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    memory_audit: list[dict[str, Any]],
    product_laws: list[dict[str, Any]],
    strictest: list[dict[str, Any]],
    first_bound: list[dict[str, Any]],
    conversion: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4542_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    parent_missing = any(row["audit_id"] == "MEA4542_0_parent_operator" and row["4542_verdict"] == "PARENT_MEMORY_EQUATION_NOT_FOUND" for row in memory_audit)
    checks.append({"validation_id": "VAL4542_01_parent_equation", "status": "PASS" if parent_missing else "FAIL", "detail": "parent memory equation missing is explicitly recorded"})

    law_ok = any(row["law_id"] == "LAW4542_1_linear_bound" for row in product_laws)
    checks.append({"validation_id": "VAL4542_02_product_law", "status": "PASS" if law_ok else "FAIL", "detail": "finite cGamma product law imported"})

    gdot_ok = any(row["effective_product"] == "C_Gamma_Gdot" and row["selected_first_current_chain"] == "True" and row["max_abs_effective_product"] == "2.42e-14" for row in strictest)
    checks.append({"validation_id": "VAL4542_03_gdot_selected", "status": "PASS" if gdot_ok else "FAIL", "detail": "C_Gamma_Gdot selected as first current-chain product bound"})

    first_ok = first_bound and first_bound[0]["effective_product"] == "C_Gamma_Gdot" and first_bound[0]["claim_status"] == "nonclaim_product_bound_not_cGamma_alone"
    checks.append({"validation_id": "VAL4542_04_first_bound", "status": "PASS" if first_ok else "FAIL", "detail": "first selected bound row is nonclaim product bound"})

    conversion_ok = any(row["requirement_id"] == "CR4542_0_formula" and row["status"] == "missing" for row in conversion)
    checks.append({"validation_id": "VAL4542_05_conversion_guard", "status": "PASS" if conversion_ok else "FAIL", "detail": "conversion to cGamma requires missing Jacobian/profile"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    public_block = any(row["claim_gate_id"] == "CG4542_4_public_local_GR" and row["status"] == "BLOCKED_NONCLAIM" for row in gates)
    checks.append({"validation_id": "VAL4542_06_claim_firewall", "status": "PASS" if gates_ok and public_block else "FAIL", "detail": "all claim gates remain nonclaim"})

    csv_paths = [SOURCE_REGISTER, MEMORY_EQUATION_AUDIT_CSV, PRODUCT_LAW_CSV, STRICTEST_BOUNDS_CSV, FIRST_BOUND_CSV, CONVERSION_REQUIREMENTS_CSV, CLAIM_GATES_CSV, DECISION_CSV, NEXT_CSV, STATUS_CSV]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4542_07_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4542_08_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4542_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4542 cGamma parent memory equation or first projection-bound row"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    memory_audit: list[dict[str, Any]],
    product_laws: list[dict[str, Any]],
    strictest: list[dict[str, Any]],
    first_bound: list[dict[str, Any]],
    conversion: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4542 - cGamma parent memory equation or first projection-bound row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4541 left `c_Gamma` as the active local memory coefficient. 4542 tries the derivation-first route:

```text
L_Gamma Gamma_mem = J_Gamma
```

with sign, source, boundary and tensor no-hair clauses. Current evidence still does **not** provide that parent memory equation.

So 4542 promotes the first concrete bound row instead of stopping:

```text
|C_Gamma_Gdot| <= 2.42e-14 yr^-1.
```

This is source-backed as a **product bound**, not a value of `c_Gamma`. The conversion still needs:

```text
C_Gamma_Gdot = J_Gdot^Gamma * c_Gamma * ||P_Gdot Gamma_mem|| + tensor_perp_piece.
```

Until `J_Gdot^Gamma` and the memory profile norm are parent-derived or sourced, the row is a nonclaim guard on the effective product.

## Parent Memory Equation Audit

{markdown_table(memory_audit)}

## cGamma Product-Bound Law

{markdown_table(product_laws)}

## Strictest Product Bounds

{markdown_table(strictest)}

## First Selected Bound Row

{markdown_table(first_bound)}

## Product-To-Coefficient Requirements

{markdown_table(conversion)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_memory_bound",
        "claim": "4542 fails to find a parent cGamma memory equation but promotes the first source-backed product bound: |C_Gamma_Gdot| <= 2.42e-14 yr^-1, explicitly nonclaim and not a bound on c_Gamma itself.",
        "current_evidence": "Generated source register, parent memory equation audit, cGamma product-bound law, strictest product bounds, first selected bound row, conversion requirements, claim gates, status and validation CSVs.",
        "status": "first_cGamma_Gdot_product_bound_nonclaim_parent_memory_equation_missing",
        "next_test": NEXT_TARGET,
        "key_risk": "Dividing the product bound into c_Gamma without J_Gdot^Gamma and memory profile units.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Product-bound row guards local-G drift but does not prove cGamma zero, local GR, or R10 pass.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    memory_audit = memory_equation_audit_rows()
    product_laws = product_law_rows()
    strictest = strictest_bound_rows()
    first_bound = first_bound_rows()
    conversion = conversion_requirement_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MEMORY_EQUATION_AUDIT_CSV, memory_audit)
    write_csv(PRODUCT_LAW_CSV, product_laws)
    write_csv(STRICTEST_BOUNDS_CSV, strictest)
    write_csv(FIRST_BOUND_CSV, first_bound)
    write_csv(CONVERSION_REQUIREMENTS_CSV, conversion)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, memory_audit, product_laws, strictest, first_bound, conversion, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, memory_audit, product_laws, strictest, first_bound, conversion, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4542 cGamma Parent Memory Equation Or First Projection-Bound Row

Marker: `{MARKER}`  
4542 tries the parent memory equation route for `c_Gamma` and confirms the equation is still not found. It then promotes the first useful current-chain product bound: `|C_Gamma_Gdot| <= 2.42e-14 yr^-1`. This is explicitly a product bound, not a value or prediction for `c_Gamma`; conversion requires `J_Gdot^Gamma` and the memory profile norm. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4542 Packet Integration - First cGamma Product Bound

Marker: `{PACKET_MARKER}`  
The packet now carries a first nonclaim `c_Gamma` product bound: `C_Gamma_Gdot` is bounded by `2.42e-14 yr^-1`. The parent memory equation remains absent, and this row cannot be divided into a `c_Gamma` bound until the Gdot projection Jacobian and memory profile are sourced.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
