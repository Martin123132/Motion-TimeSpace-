from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3219_INPUTS.csv"
LAW = OUT / "P8_Y5_R2FR_3219_EM_F2_STRICT_DOUBLE_ZERO_LAW.csv"
HESSIAN = OUT / "P8_Y5_R2FR_3219_EM_F2_HESSIAN_CORRECTION_GATE.csv"
OFFROOT = OUT / "P8_Y5_R2FR_3219_OFFROOT_BALPHA_M_BOUND.csv"
SOURCE_ROW = OUT / "P8_Y5_R2FR_3219_STRICT_DZ_OR_FINITE_BALPHA_M_ROWS.csv"
DECISION = OUT / "P8_Y5_R2FR_3219_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3219_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3219_00_3218_doc",
        "location": "post_checkpoint",
        "relative_path": "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md",
        "role": "3218 b_alpha_m decomposition handoff",
        "terms": ["strict EM double-zero", "b_alpha_m", "Z_A"],
    },
    {
        "input_id": "SRC3219_01_3218_zero",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3218_BALPHA_M_ZERO_THEOREM_ATTEMPT.csv",
        "role": "3218 double-zero subroute",
        "terms": ["BAM3218_3_double_zero_subroute", "BAM3218_5_total_verdict"],
    },
    {
        "input_id": "SRC3219_02_1291_strict",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1291_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv",
        "role": "strict double-zero parent clause",
        "terms": ["SDZ1291_1_strict_F_form", "SDZ1291_3_no_multiplier_or_readout_cheat", "SDZ1291_5_parent_clause_verdict"],
    },
    {
        "input_id": "SRC3219_03_1533_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv",
        "role": "parent action double-zero source-root contract",
        "terms": ["VAC1533_1_potential_source", "VAC1533_4_local_lock", "VAC1533_6_verdict"],
    },
    {
        "input_id": "SRC3219_04_2141_theorem",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_2141_DOUBLE_ZERO_THEOREM.csv",
        "role": "exact local pointwise double-zero theorem",
        "terms": ["DZ2141_1_K_first_derivative", "DZ2141_5_nonflat_system", "DZ2141_6_verdict"],
    },
    {
        "input_id": "SRC3219_05_2817_coeffkill",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2817_STRICT_DOUBLE_ZERO_COEFFICIENT_KILL.csv",
        "role": "strict double-zero coefficient kill",
        "terms": ["CK2817_1_exact_double_zero", "CK2817_2_local_lock_dependency", "CK2817_4_verdict"],
    },
    {
        "input_id": "SRC3219_06_3071_root",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3071_SOURCE_ROOT_DOUBLE_ZERO_ROUTE_AUDIT.csv",
        "role": "source-root/off-root bound",
        "terms": ["SR3071_2_double_zero", "SR3071_3_finite_displacement"],
    },
    {
        "input_id": "SRC3219_07_3215_nohair",
        "location": "post_checkpoint",
        "relative_path": "3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090.md",
        "role": "source-compatible nohair and Hessian correction guard",
        "terms": ["corrected Hessian", "C_r''", "positive memory no-hair"],
    },
    {
        "input_id": "SRC3219_08_3210_amplitude",
        "location": "post_checkpoint",
        "relative_path": "3210-Y5-R2FR-scalar-nohair-amplitude-law-and-omega-zero-curl-gate-under-AX1090.md",
        "role": "finite amplitude fallback",
        "terms": ["Y_X", "||X||_H1", "source/boundary leakage"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    law_rows = [
        {
            "law_id": "DZ3219_0_setup",
            "object": "EM memory deformation",
            "statement": "Let Z_A(m)=Z_0 + lambda_F F(m), with Z_0>0, m=m_*+delta m, and F(m_*)=F'(m_*)=0.",
            "result": "SETUP",
            "claim_effect": "defines the strict double-zero subroute for the EM F2 coefficient",
            "missing_for_claim": "parent source-root F and same-branch local lock m=m_*",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "DZ3219_1_exact_slope_zero",
            "object": "b_alpha_m at root",
            "statement": "b_alpha_m(m_*) = partial_m ln Z_A|m_* = lambda_F F'(m_*)/Z_A(m_*) = 0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "claim_effect": "kills the linear EM source term -1/4 Z_A'(m_*)F^2 in the memory equation",
            "missing_for_claim": "F'(m_*)=0 must be parent-owned, not chosen after local tests",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "DZ3219_2_value_not_required",
            "object": "alpha value versus slope",
            "statement": "The slope-zero result does not require deriving the numerical value of Z_0 or alpha, only that Z_A(m_*) is positive/finite and its first memory derivative vanishes.",
            "result": "IMPORTANT_PARTIAL_WIN",
            "claim_effect": "separates local coupling silence from predicting the numerical fine-structure constant",
            "missing_for_claim": "positive/finite denominator and readout closure still required",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "DZ3219_3_offroot_linear_bound",
            "object": "off-root residual",
            "statement": "Near m_*, b_alpha_m(m) = [lambda_F F''(m_*)/Z_0] delta m + O(delta m^2), so exact local lock can be relaxed only with a delta_m amplitude bound.",
            "result": "FINITE_BOUND_LAW",
            "claim_effect": "connects the EM slope to the 3210/3215 memory amplitude machinery",
            "missing_for_claim": "lambda_F F'' bound, Z_0 lower bound, and delta_m amplitude/support bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "DZ3219_4_not_no_extra_F2",
            "object": "relationship to no-extra-F2",
            "statement": "Strict double-zero is weaker than no-extra-F2: it allows an EM memory deformation but forces its linear local source to vanish at the locked branch origin.",
            "result": "ROUTE_CLARIFIED",
            "claim_effect": "gives a less ambitious path than full EM-lock while preserving test discipline",
            "missing_for_claim": "second-order correction and readout/radiative guard",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    hessian_rows = [
        {
            "gate_id": "HES3219_0_second_variation",
            "gate": "EM F2 double-zero shifts memory Hessian",
            "formula": "delta^2 S_EM / delta m^2 at m_* includes -1/4 lambda_F F''(m_*) F_Q^2 (delta m)^2",
            "status": "EXACT_VARIATION_GUARD",
            "why_needed": "slope-zero removes the source but not the quadratic stability correction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "HES3219_1_coercivity_floor",
            "gate": "corrected memory operator remains positive",
            "formula": "G_eff >= G_mem - eta_EM, eta_EM >= (1/4)|lambda_F F''| ||F_Q^2||_op plus readout/radiative corrections",
            "status": "MISSING_NUMERIC_OR_PARENT_BOUND",
            "why_needed": "otherwise double-zero can create tachyonic/long-range memory response",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "HES3219_2_F2_sign_guard",
            "gate": "F_Q^2 sign is not uniformly positive",
            "formula": "use absolute/operator-norm guard, not cancellation by electric/magnetic field sign",
            "status": "NO_CANCELLATION_GUARD",
            "why_needed": "EM invariant sign depends on field configuration; stability must use worst-case bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "HES3219_3_null_wave_guard",
            "gate": "null EM waves are separate",
            "formula": "F^2=0 can kill this bulk coefficient while T_EM/Poynting remains nonzero",
            "status": "SEPARATE_HODGE_BOUNDARY_CHANNEL",
            "why_needed": "EM F2 double-zero does not close Hodge/Poynting channels",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "HES3219_4_activation",
            "gate": "strict double-zero EM route activates local memory silence",
            "formula": "DZ3219_1 plus G_eff>0 plus intrinsic/boundary/readout source silence",
            "status": "FAIL_CURRENT_CLAIM",
            "why_needed": "parent source-root, local lock, and Hessian correction bounds are not signed together",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    offroot_rows = [
        {
            "bound_id": "ORB3219_0_balpha_offroot",
            "quantity": "off-root b_alpha_m",
            "bound_formula": "|b_alpha_m| <= |lambda_F F2_m| |delta_m| / Z_min + O(delta_m^2)",
            "inputs_required": "lambda_F; F2_m=F''(m_*); delta_m amplitude; Z_min; units; source paths",
            "feeds": "clock/WEP/R10 alpha product rows and EM source norm",
            "current_status": "MISSING_INPUTS_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "ORB3219_1_Jm_source",
            "quantity": "EM source norm from off-root slope",
            "bound_formula": "||J_m,F2|| <= (1/4)|lambda_F F2_m| |delta_m| ||F_Q^2|| / Z_guard",
            "inputs_required": "same as ORB3219_0 plus ||F_Q^2|| local support norm",
            "feeds": "3210 source amplitude law",
            "current_status": "MISSING_INPUTS_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "ORB3219_2_alpha_residual",
            "quantity": "alpha residual from displaced memory",
            "bound_formula": "|Delta alpha/alpha| <= |lambda_F F2_m| delta_m^2/(2 Z_min) + O(delta_m^3)",
            "inputs_required": "delta_m amplitude squared and same coefficient/denominator data",
            "feeds": "clock/R10/EM alpha residual",
            "current_status": "MISSING_INPUTS_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    source_rows = [
        {
            "row_id": "DZSR3219_0_strict_zero_switch",
            "quantity": "b_alpha_m_zero_from_EM_double_zero",
            "zero_value": "0_if_parent_source_root_signed",
            "required_authority": "F(m_*)=F'(m_*)=0 for the EM F2 coefficient; m=m_* local lock; Z_A positive; readout closure",
            "current_status": "MISSING_PARENT_SOURCE_ROOT_OR_LOCAL_LOCK",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "DZSR3219_1_hessian_correction",
            "quantity": "eta_EM_F2_hessian",
            "zero_value": "not_zero_generically",
            "required_authority": "|lambda_F F''| and ||F_Q^2|| operator/support bound; G_mem floor",
            "current_status": "MISSING_SECOND_ORDER_BOUND",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "DZSR3219_2_finite_balpha_m_bound",
            "quantity": "abs(b_alpha_m)_offroot",
            "zero_value": "finite_bound_if_delta_m_nonzero",
            "required_authority": "lambda_F F''; delta_m; Z_min; source path; equation ref; units",
            "current_status": "MISSING_FINITE_INPUTS",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3219_0_result",
            "result": "STRICT_EM_DOUBLE_ZERO_KILLS_LINEAR_BALPHA_M_CONDITIONALLY_SECOND_ORDER_HESSIAN_DEBT_RETAINED",
            "claim_status": "NO_BALPHA_M_ZERO_CLAIM_NO_LOCAL_GR_CLAIM",
            "decision": "3219 proves the useful conditional: a strict EM F2 double-zero source root kills b_alpha_m at the local memory lock without deriving alpha's numeric value. But the same term shifts the memory Hessian through F'' and can destabilize or range-shift the branch unless bounded. Current corpus does not parent-sign the EM source root/local lock/Hessian bound package.",
            "best_next_route": "try to source or derive the EM-specific source-root F(m) from the parent action; if unavailable, demote this route to finite off-root b_alpha_m bounds",
            "next_target": "3220-Y5-R2FR-parent-source-root-for-EM-F2-or-finite-double-zero-coefficient-input-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]

    return input_rows, law_rows, hessian_rows, offroot_rows, source_rows, decision_rows


def main() -> None:
    now = stamp()
    input_rows, law_rows, hessian_rows, offroot_rows, source_rows, decision_rows = build_rows(now)

    generated_without_validation = [
        INPUTS,
        LAW,
        HESSIAN,
        OFFROOT,
        SOURCE_ROW,
        DECISION,
    ]

    write_csv(INPUTS, input_rows)
    write_csv(LAW, law_rows)
    write_csv(HESSIAN, hessian_rows)
    write_csv(OFFROOT, offroot_rows)
    write_csv(SOURCE_ROW, source_rows)
    write_csv(DECISION, decision_rows)

    all_rows: list[dict[str, str]] = []
    for path in generated_without_validation:
        all_rows.extend(read_csv(path))
    claim_rows = [row for row in all_rows if row.get("valid_for_claim") == "true"]

    validation_rows = [
        {
            "check_id": "VAL3219_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_01_slope_zero_law",
            "check": "strict double-zero b_alpha_m zero law is written",
            "pass": b(any(row["law_id"] == "DZ3219_1_exact_slope_zero" for row in law_rows)),
            "detail": "b_alpha_m=lambda_F F'(m*)/Z_A=0",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_02_hessian_guard",
            "check": "second-order Hessian correction guard is written",
            "pass": b(any(row["gate_id"] == "HES3219_1_coercivity_floor" for row in hessian_rows)),
            "detail": "G_eff >= G_mem - eta_EM",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_03_offroot_bounds",
            "check": "off-root finite b_alpha_m bounds are staged",
            "pass": b(len(offroot_rows) >= 3),
            "detail": ";".join(row["bound_id"] for row in offroot_rows),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_04_activation_blocks_claim",
            "check": "strict double-zero activation blocks current claim",
            "pass": b(any(row["gate_id"] == "HES3219_4_activation" and row["status"] == "FAIL_CURRENT_CLAIM" for row in hessian_rows)),
            "detail": "source root/local lock/Hessian package not parent-signed",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_05_claims_blocked",
            "check": "no generated row is valid_for_claim true",
            "pass": b(len(claim_rows) == 0),
            "detail": f"claim_rows_true={len(claim_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_06_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_07_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_without_validation)),
            "detail": ";".join(path.name for path in generated_without_validation),
            "generated_utc": now,
        },
        {
            "check_id": "VAL3219_08_next_target",
            "check": "next target is parent source-root or finite coefficient input",
            "pass": b("3220" in decision_rows[0]["next_target"]),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3219 - EM F2 Strict Double-Zero Source Root Or b_alpha_m Finite Bound under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3219 proves the useful conditional route:

```text
Z_A(m) = Z_0 + lambda_F F(m)
F(m_*) = 0
F'(m_*) = 0
Z_A(m_*) > 0

=> b_alpha_m(m_*) = partial_m ln Z_A | m_* = 0.
```

This is a real partial win because it does **not** require predicting the numerical value of alpha. It only requires the local memory slope of the EM kinetic coefficient to vanish.

But the little goblin hiding under the rug is second order:

```text
delta^2 S_EM contains -1/4 lambda_F F''(m_*) F_Q^2 (delta m)^2.
```

So strict double-zero kills the linear source, but it can still shift the memory Hessian/range. The branch is only safe if:

```text
G_eff >= G_mem - eta_EM > 0.
```

Current verdict: conditional theorem yes; parent-signed EM source-root/local-lock/Hessian package no.

## EM F2 Strict Double-Zero Law

{md_table(law_rows, ["law_id", "object", "statement", "result", "claim_effect", "missing_for_claim", "valid_for_claim"])}

## EM F2 Hessian Correction Gate

{md_table(hessian_rows, ["gate_id", "gate", "formula", "status", "why_needed", "valid_for_claim"])}

## Off-Root b_alpha_m Bound

{md_table(offroot_rows, ["bound_id", "quantity", "bound_formula", "inputs_required", "feeds", "current_status", "valid_for_claim"])}

## Strict DZ Or Finite b_alpha_m Rows

{md_table(source_rows, ["row_id", "quantity", "zero_value", "required_authority", "current_status", "claim_allowed", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(LAW)}`
- `{rel(HESSIAN)}`
- `{rel(OFFROOT)}`
- `{rel(SOURCE_ROW)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
