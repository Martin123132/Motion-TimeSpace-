from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3225-Y5-R2FR-first-real-alpha-input-acquisition-balpha-zero-or-lambdaD-DRQ-Zmin-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3225_INPUTS.csv"
ZERO = OUT / "P8_Y5_R2FR_3225_BALPHA_ZERO_ACQUISITION_AUDIT.csv"
FINITE = OUT / "P8_Y5_R2FR_3225_FINITE_INPUT_ACQUISITION_AUDIT.csv"
PRODUCT = OUT / "P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv"
FIRST = OUT / "P8_Y5_R2FR_3225_FIRST_REAL_INPUT_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3225_VALIDATION.csv"

CLOCK = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
WEP = OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"


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


def maybe_float(value: object) -> float | None:
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.lower().startswith("missing") or text.lower() in {"not_applicable", "none", "nan"}:
            return None
        number = float(text)
        if not math.isfinite(number):
            return None
        return number
    except Exception:
        return None


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:200]}")
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
        "input_id": "SRC3225_00_3224_doc",
        "location": "post_checkpoint",
        "relative_path": "3224-Y5-R2FR-finite-alpha-bound-propagator-clock-WEP-R10-under-AX1090.md",
        "role": "3224 handoff and first-input blocker",
        "terms": ["first real MTS alpha input", "lambda_D", "Z_min", "3225"],
    },
    {
        "input_id": "SRC3225_01_3224_mts",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3224_MTS_ALPHA_INPUT_READINESS.csv",
        "role": "MTS alpha input readiness",
        "terms": ["SMOKE3223_1_lambda_D", "SMOKE3223_4_Z_min", "SCHEMA_ONLY_OR_MISSING_SOURCE"],
    },
    {
        "input_id": "SRC3225_02_3224_blockers",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv",
        "role": "first real input blockers",
        "terms": ["BLK3224_0_first_MTS_scalar", "BLK3224_1_clock_projection", "BLK3224_2_WEP_projection"],
    },
    {
        "input_id": "SRC3225_03_3224_anchors",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3224_IMPORTED_BOUND_ANCHORS.csv",
        "role": "imported clock/WEP/R10 anchor rows",
        "terms": ["ACB1052_2", "AWP1052_0_alpha_Coulomb", "RAP1052_0_product_law"],
    },
    {
        "input_id": "SRC3225_04_3218",
        "location": "post_checkpoint",
        "relative_path": "3218-Y5-R2FR-EM-F2-vertex-owner-for-memory-slope-zero-or-balpha-m-source-row-under-AX1090.md",
        "role": "b_alpha formula and zero routes",
        "terms": ["b_alpha_m", "Z_A", "BAM3218_5_total_verdict", "countermodel"],
    },
    {
        "input_id": "SRC3225_05_3223_formula",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv",
        "role": "finite b_alpha formulas",
        "terms": ["FORM3223_1_offroot_bound", "FORM3223_2_alpha_residual", "FORM3223_3_hessian_guard"],
    },
    {
        "input_id": "SRC3225_06_1057",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "unique Maxwell subblock status",
        "terms": ["UMS1057_2_no_independent_F2", "UMS1057_5_verdict"],
    },
    {
        "input_id": "SRC3225_07_1058",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "operator-domain exhaustion status",
        "terms": ["VOE1058_3_no_hidden_visible_hom", "VOE1058_5_verdict"],
    },
    {
        "input_id": "SRC3225_08_clock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "clock alpha product bound",
        "terms": ["ACB1052_2", "2.1e-18", "standalone_balpha_ready"],
    },
    {
        "input_id": "SRC3225_09_WEP",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
        "role": "WEP alpha projection bound",
        "terms": ["AWP1052_0_alpha_Coulomb", "required_abs_beta_source_max", "delta_Q_abs"],
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

    zero_rows = [
        {
            "audit_id": "BZ3225_0_exact_RZ_zero",
            "target_input": "b_alpha_m = 0",
            "required_derivation": "R_Z=Z_A-C_P N_Q is parent-owned, Delta Z_A=lambda_D||R_Z||^2, and R_Z=0 on the same local branch",
            "current_evidence": "R_Z is the best target but remains template-only; no source-signed parent R_Z row exists",
            "status": "NOT_ACQUIRED",
            "missing_for_claim": "parent R_Z object; same-branch root; no independent lambda_A/f(I)F_Q^2; readout closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "BZ3225_1_no_extra_F2_route",
            "target_input": "b_alpha_m = 0 by absence",
            "required_derivation": "unique Maxwell subblock plus operator-domain exhaustion forbids independent F_Q^2 coefficients",
            "current_evidence": "1057/1058 explicitly keep this theorem unpromoted",
            "status": "NOT_ACQUIRED",
            "missing_for_claim": "operator-domain exhaustion/no-hidden-visible hom theorem and radiative/readout closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "BZ3225_2_double_zero_route",
            "target_input": "b_alpha_m = 0 by strict double-zero",
            "required_derivation": "F_EM(m_*)=F_EM'(m_*)=0 for the EM F_Q^2 coefficient and m=m_* local lock",
            "current_evidence": "3219/3220/3221 prove theorem shape but not parent EM source-root ownership",
            "status": "NOT_ACQUIRED",
            "missing_for_claim": "parent EM source-root owner; Hessian/stress/readout guards",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "BZ3225_3_verdict",
            "target_input": "first exact zero input",
            "required_derivation": "one exact-zero route source-signs all clauses",
            "current_evidence": "none source-signed in bounded current corpus",
            "status": "EXACT_ZERO_INPUT_NOT_ACQUIRED",
            "missing_for_claim": "source-signed exact zero theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    finite_rows = [
        {
            "input_id": "FI3225_0_C_D",
            "quantity": "C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min",
            "needed_for": "|b_alpha_m| <= C_D |Delta m|",
            "current_value": "MISSING",
            "source_status": "not source-backed",
            "why_not_acquired": "lambda_D, D_m R_Q, and Z_min all remain placeholder rows",
            "next_source_action": "source R_Z finite coefficient package or exact zero switch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FI3225_1_Delta_m",
            "quantity": "Delta m",
            "needed_for": "finite off-root b_alpha_m branch",
            "current_value": "MISSING",
            "source_status": "not EM-attached",
            "why_not_acquired": "local amplitude machinery exists elsewhere but not tied to EM R_Q/Z_A branch",
            "next_source_action": "tie local lock/amplitude law to same EM branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FI3225_2_tau_clock",
            "quantity": "tau_clock_time",
            "needed_for": "clock product prediction |b_alpha_m tau_clock_time|",
            "current_value": "MISSING",
            "source_status": "clock product bound exists but tau is not derived",
            "why_not_acquired": "clock rows bound the product only",
            "next_source_action": "derive clock readout/local Xhat normalization before standalone b_alpha_m",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FI3225_3_tau_WEP_beta",
            "quantity": "tau_WEP * beta_source_alpha",
            "needed_for": "WEP alpha/Coulomb product prediction",
            "current_value": "MISSING",
            "source_status": "not source-backed",
            "why_not_acquired": "WEP projection ledger names required beta/tau but does not provide MTS value",
            "next_source_action": "derive/source material projection and source-test alpha coupling",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "input_id": "FI3225_4_Zmin_shortcut_refusal",
            "quantity": "Z_min",
            "needed_for": "denominator of finite alpha bound",
            "current_value": "MISSING",
            "source_status": "do not set by convention",
            "why_not_acquired": "alpha normalization/gauge norm owner remains unsigned; using observed alpha would be readout fitting unless contracted",
            "next_source_action": "source parent gauge norm or keep Z_min as explicit finite input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    clock_best = next(row for row in read_csv(CLOCK) if row.get("bound_id") == "ACB1052_2")
    clock_bound_1 = maybe_float(clock_best.get("product_bound_1sigma_yr_inv"))
    clock_bound_2 = maybe_float(clock_best.get("product_bound_2sigma_yr_inv"))
    wep_alpha = next(row for row in read_csv(WEP) if row.get("projection_id") == "AWP1052_0_alpha_Coulomb")
    eta_bound = maybe_float(wep_alpha.get("eta_bound"))
    delta_q = maybe_float(wep_alpha.get("delta_Q_abs"))
    beta_max = maybe_float(wep_alpha.get("required_abs_beta_source_max"))

    product_rows = [
        {
            "constraint_id": "PC3225_0_clock_1sigma",
            "arena": "clock",
            "derived_constraint": "C_D |Delta m tau_clock_time| <= product_bound_1sigma",
            "numeric_bound": f"{clock_bound_1:.6e}" if clock_bound_1 is not None else "MISSING_NUMERIC_BOUND",
            "units": "yr^-1 in the clock-time convention",
            "source_anchor": "ACB1052_2",
            "what_is_real": "source-backed clock product bound",
            "what_is_missing": "C_D, Delta m, tau_clock_time individually",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "constraint_id": "PC3225_1_clock_2sigma",
            "arena": "clock",
            "derived_constraint": "C_D |Delta m tau_clock_time| <= product_bound_2sigma",
            "numeric_bound": f"{clock_bound_2:.6e}" if clock_bound_2 is not None else "MISSING_NUMERIC_BOUND",
            "units": "yr^-1 in the clock-time convention",
            "source_anchor": "ACB1052_2",
            "what_is_real": "source-backed clock product bound",
            "what_is_missing": "C_D, Delta m, tau_clock_time individually",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "constraint_id": "PC3225_2_WEP_alpha",
            "arena": "MICROSCOPE_WEP",
            "derived_constraint": "C_D |Delta m tau_WEP beta_source_alpha| <= eta_bound / delta_Q_abs",
            "numeric_bound": f"{(eta_bound / delta_q):.6e}" if eta_bound is not None and delta_q else "MISSING_NUMERIC_BOUND",
            "units": "dimensionless product in selected WEP projection convention",
            "source_anchor": "AWP1052_0_alpha_Coulomb",
            "what_is_real": "source-backed eta_bound and alpha/Coulomb delta_Q_abs",
            "what_is_missing": "C_D, Delta m, tau_WEP, beta_source_alpha",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "constraint_id": "PC3225_3_WEP_unit_source_beta_anchor",
            "arena": "MICROSCOPE_WEP",
            "derived_constraint": "if unit source prediction convention is used, |beta_source_alpha| must stay below required_abs_beta_source_max",
            "numeric_bound": f"{beta_max:.6e}" if beta_max is not None else "MISSING_NUMERIC_BOUND",
            "units": "dimensionless beta_source_alpha under 1052 convention",
            "source_anchor": "AWP1052_0_alpha_Coulomb",
            "what_is_real": "source-backed 1052 required beta threshold",
            "what_is_missing": "MTS beta_source_alpha theorem/prior and tau_WEP",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "constraint_id": "PC3225_4_R10_none",
            "arena": "R10",
            "derived_constraint": "no numeric product constraint can be derived yet",
            "numeric_bound": "MISSING_PROMOTED_R10_BOUND_AND_PROJECTIONS",
            "units": "dimensionless alpha(lambda)",
            "source_anchor": "RAP1052_0..2 definitions only",
            "what_is_real": "projection law language",
            "what_is_missing": "tau_R10, K_X(lambda), beta_s, beta_t, promoted bound curve",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    first_rows = [
        {
            "decision_id": "FIRST3225_0_exact_input",
            "candidate_first_input": "exact b_alpha_m=0",
            "result": "not_acquired",
            "why": "no exact zero route is source-signed",
            "usable_progress": "keeps exact route as R_Z source target",
            "next_action": "try source-sign R_Z or abandon exact-zero for finite bound acquisition",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "FIRST3225_1_finite_input",
            "candidate_first_input": "finite C_D and Delta m",
            "result": "not_acquired",
            "why": "lambda_D, D_m R_Q, Z_min, and EM-attached Delta m remain missing",
            "usable_progress": "defines C_D := 2|lambda_D|||D_mR_Q||^2/Z_min as the first compact coefficient target",
            "next_action": "source C_D package or source one constituent with units",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "FIRST3225_2_product_constraint",
            "candidate_first_input": "real anchor-derived product constraints",
            "result": "acquired_as_nonclaim_constraint",
            "why": "clock and WEP source anchors yield numeric constraints on combined MTS products",
            "usable_progress": "C_D|Delta m tau_clock| <= 2.1e-18 yr^-1 and C_D|Delta m tau_WEP beta_alpha| <= eta/deltaQ",
            "next_action": "use these as target inequalities when sourcing C_D, Delta m, tau_clock, tau_WEP, beta_source_alpha",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "FIRST3225_3_next_target",
            "candidate_first_input": "3226-Y5-R2FR-CD-coefficient-package-or-clock-product-saturation-bound-under-AX1090",
            "result": "next",
            "why": "the first productive acquisition target is now C_D or a bounded product involving C_D",
            "usable_progress": "turn missing lambda_D/DRQ/Zmin into a single coefficient package with source/units gates",
            "next_action": "derive/source C_D directly or set explicit prior-width targets from clock/WEP products",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, zero_rows, finite_rows, product_rows, first_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    first_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, ZERO, FINITE, PRODUCT, FIRST]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    exact_claims = sum(row["valid_for_claim"] == "true" for row in zero_rows)
    finite_claims = sum(row["valid_for_claim"] == "true" for row in finite_rows)
    numeric_constraints = sum(maybe_float(row["numeric_bound"]) is not None for row in product_rows)
    product_claims = sum(row["claim_allowed"] == "true" for row in product_rows)
    progress_row = any(row["decision_id"] == "FIRST3225_2_product_constraint" and row["result"] == "acquired_as_nonclaim_constraint" for row in first_rows)
    claim_true_count = 0
    for rows in [input_rows, zero_rows, finite_rows, product_rows, first_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3225_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3225_01_exact_zero_not_claimed", "pass": b(exact_claims == 0), "detail": f"exact_claims={exact_claims}", "generated_utc": now},
        {"check_id": "VAL3225_02_finite_inputs_not_claimed", "pass": b(finite_claims == 0), "detail": f"finite_claims={finite_claims}", "generated_utc": now},
        {"check_id": "VAL3225_03_product_constraints_numeric", "pass": b(numeric_constraints >= 4), "detail": f"numeric_constraints={numeric_constraints}", "generated_utc": now},
        {"check_id": "VAL3225_04_product_constraints_nonclaim", "pass": b(product_claims == 0), "detail": f"product_claims={product_claims}", "generated_utc": now},
        {"check_id": "VAL3225_05_progress_row_written", "pass": b(progress_row), "detail": "anchor-derived product constraints acquired as nonclaim constraints", "generated_utc": now},
        {"check_id": "VAL3225_06_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3225_07_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3225_08_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3225_09_next_target", "pass": b(first_rows[-1]["candidate_first_input"].startswith("3226-")), "detail": str(first_rows[-1]["candidate_first_input"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3225 - First Real Alpha Input Acquisition: b_alpha Zero Or lambdaD/DRQ/Zmin under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3225 tries to acquire the first real MTS alpha input.

The exact input is still not acquired:

```text
b_alpha_m = 0
```

is not source-signed, because `R_Z`, no-extra-`F^2`, strict EM double-zero, and readout closure are still not all owned by the parent action.

The finite standalone input is also not acquired:

```text
C_D := 2 |lambda_D| ||D_m R_Q||^2 / Z_min
|b_alpha_m| <= C_D |Delta m|
```

because `lambda_D`, `D_m R_Q`, `Z_min`, and the EM-attached `Delta m` amplitude are still missing.

But 3225 does get a real nonclaim constraint out of the data anchors:

```text
C_D |Delta m tau_clock_time| <= 2.1e-18 yr^-1       (best clock 1sigma anchor)
C_D |Delta m tau_WEP beta_source_alpha| <= eta_bound / DeltaQ_alpha
```

For the MICROSCOPE alpha/Coulomb row this gives:

```text
C_D |Delta m tau_WEP beta_source_alpha| <= {next(row["numeric_bound"] for row in product_rows if row["constraint_id"] == "PC3225_2_WEP_alpha")}
```

This is not an MTS pass. It is the first useful target inequality for the finite coupling branch.

Current verdict: `FIRST_STANDALONE_ALPHA_INPUT_NOT_ACQUIRED_PRODUCT_CONSTRAINTS_DERIVED`.

## Exact b_alpha Zero Acquisition Audit

{md_table(zero_rows, ["audit_id", "target_input", "required_derivation", "status", "missing_for_claim", "valid_for_claim"])}

## Finite Input Acquisition Audit

{md_table(finite_rows, ["input_id", "quantity", "needed_for", "current_value", "source_status", "why_not_acquired", "next_source_action", "valid_for_claim"])}

## Product Constraints From Anchors

{md_table(product_rows, ["constraint_id", "arena", "derived_constraint", "numeric_bound", "units", "source_anchor", "what_is_real", "what_is_missing", "claim_allowed", "valid_for_claim"])}

## First Real Input Decision

{md_table(first_rows, ["decision_id", "candidate_first_input", "result", "why", "usable_progress", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_BALPHA_ZERO_ACQUISITION_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_FINITE_INPUT_ACQUISITION_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_PRODUCT_CONSTRAINTS_FROM_ANCHORS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_FIRST_REAL_INPUT_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3225_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, zero_rows, finite_rows, product_rows, first_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (ZERO, zero_rows),
        (FINITE, finite_rows),
        (PRODUCT, product_rows),
        (FIRST, first_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, zero_rows, finite_rows, product_rows, first_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, zero_rows, finite_rows, product_rows, first_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
