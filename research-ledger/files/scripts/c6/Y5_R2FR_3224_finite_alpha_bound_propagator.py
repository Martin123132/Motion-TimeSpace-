from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3224-Y5-R2FR-finite-alpha-bound-propagator-clock-WEP-R10-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3224_INPUTS.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3224_PROPAGATOR_CONTRACT.csv"
ANCHORS = OUT / "P8_Y5_R2FR_3224_IMPORTED_BOUND_ANCHORS.csv"
MTS = OUT / "P8_Y5_R2FR_3224_MTS_ALPHA_INPUT_READINESS.csv"
COMPARISON = OUT / "P8_Y5_R2FR_3224_PRODUCT_COMPARISON_RESULTS.csv"
BLOCKERS = OUT / "P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv"
DECISION = OUT / "P8_Y5_R2FR_3224_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3224_VALIDATION.csv"

CLOCK = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
WEP = OUT / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"
R10 = OUT / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"
SMOKE_3223 = OUT / "P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv"


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
        "input_id": "SRC3224_00_3223_doc",
        "location": "post_checkpoint",
        "relative_path": "3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090.md",
        "role": "3223 handoff and finite formula",
        "terms": ["NO_RQ_SOURCE_SIGNED", "b_alpha_m", "3224", "smoke runner"],
    },
    {
        "input_id": "SRC3224_01_3223_formula",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_FINITE_ALPHA_BOUND_FORMULA.csv",
        "role": "finite b_alpha formula",
        "terms": ["FORM3223_1_offroot_bound", "FORM3223_3_hessian_guard"],
    },
    {
        "input_id": "SRC3224_02_3223_smoke",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_FINITE_ALPHA_SMOKE_INPUTS.csv",
        "role": "MTS finite alpha smoke inputs",
        "terms": ["SMOKE3223_1_lambda_D", "SMOKE3223_5_tau_clock", "SMOKE3223_7_tau_R10"],
    },
    {
        "input_id": "SRC3224_03_3223_runner",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3223_ALPHA_SMOKE_RUNNER_RESULTS.csv",
        "role": "3223 runner refusal",
        "terms": ["schema_smoke_only", "claim_allowed"],
    },
    {
        "input_id": "SRC3224_04_clock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "clock alpha product bound anchors",
        "terms": ["ACB1052_2", "product_bound_1sigma_yr_inv", "standalone_balpha_ready"],
    },
    {
        "input_id": "SRC3224_05_WEP",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
        "role": "WEP alpha projection anchors",
        "terms": ["AWP1052_0_alpha_Coulomb", "required_abs_beta_source_max", "tau_WEP"],
    },
    {
        "input_id": "SRC3224_06_R10",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv",
        "role": "R10 alpha projection definition",
        "terms": ["RAP1052_0_product_law", "tau_R10", "clock_to_R10_transfer"],
    },
    {
        "input_id": "SRC3224_07_1091",
        "location": "post_checkpoint",
        "relative_path": "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
        "role": "finite residual route warning",
        "terms": ["FR1091_0_b_alpha", "tau_clock_time", "ODH1091_6_verdict"],
    },
    {
        "input_id": "SRC3224_08_3219",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "off-root alpha/Hessian guard",
        "terms": ["ORB3219_0_balpha_offroot", "G_eff", "HES3219_1_coercivity_floor"],
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

    contract_rows = [
        {
            "contract_id": "PROP3224_0_acceptance_rule",
            "arena": "all",
            "prediction_formula": "accept prediction only if every required MTS input is numeric, finite, sourced, and valid_for_claim=true",
            "required_mts_inputs": "b_alpha_m theorem-zero switch OR finite lambda_D, ||D_m R_Q||, Delta m, Z_min plus arena tau/projection",
            "bound_source": "arena-specific imported anchor",
            "claim_rule": "claim_allowed only if prediction_valid_for_claim and bound_valid_for_claim and abs(prediction)<=bound",
            "current_status": "RUNNER_RULE_ACTIVE",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PROP3224_1_clock",
            "arena": "clock",
            "prediction_formula": "|dot alpha/alpha|_MTS = |b_alpha_m * tau_clock_time|",
            "required_mts_inputs": "b_alpha_m or finite bound; tau_clock_time source row; clock readout domain",
            "bound_source": "ACB1052 clock product rows",
            "claim_rule": "do not treat clock product bound as standalone b_alpha_m unless tau_clock_time is derived",
            "current_status": "ANCHOR_IMPORTED_PREDICTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PROP3224_2_WEP",
            "arena": "WEP",
            "prediction_formula": "eta_alpha_MTS = b_alpha_m * tau_WEP * beta_source_alpha * DeltaQ_alpha",
            "required_mts_inputs": "b_alpha_m; tau_WEP; beta_source_alpha; material/source-test projection",
            "bound_source": "AWP1052 MICROSCOPE alpha/Coulomb projection row",
            "claim_rule": "clock alpha bound cannot transfer to WEP without shared domain/projection theorem",
            "current_status": "ANCHOR_IMPORTED_PREDICTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PROP3224_3_R10",
            "arena": "R10",
            "prediction_formula": "alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda)+epsilon_tail(lambda)",
            "required_mts_inputs": "b_alpha_m or beta source map; tau_R10; K_X(lambda); source/test material projections; bound curve",
            "bound_source": "RAP1052 R10 projection definition plus future R10 bound curve",
            "claim_rule": "do not set tau_R10 or K_X to unity; no clock-to-R10 shortcut",
            "current_status": "DEFINITION_IMPORTED_BOUND_AND_PROJECTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PROP3224_4_hessian_stress_guard",
            "arena": "all",
            "prediction_formula": "G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0",
            "required_mts_inputs": "G_mem, lambda_D, ||D_m R_Q||, ||F_Q^2||, stress/readout bounds",
            "bound_source": "3219/3223 Hessian guards",
            "claim_rule": "alpha product pass is not enough for Maxwell/local safety",
            "current_status": "GUARD_MISSING_INPUTS",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    anchor_rows: list[dict[str, object]] = []
    for row in read_csv(CLOCK):
        bound_1 = maybe_float(row.get("product_bound_1sigma_yr_inv"))
        bound_2 = maybe_float(row.get("product_bound_2sigma_yr_inv"))
        anchor_rows.append(
            {
                "anchor_id": row.get("bound_id", ""),
                "arena": "clock",
                "source_file": CLOCK.name,
                "observable": row.get("clock_pair", ""),
                "bound_value": bound_1 if bound_1 is not None else "MISSING_NUMERIC_BOUND",
                "bound_value_2sigma": bound_2 if bound_2 is not None else "MISSING_NUMERIC_BOUND",
                "units": "yr^-1",
                "interpretation": row.get("interpretation", ""),
                "score_ready": row.get("standalone_balpha_ready", "false"),
                "valid_for_claim": row.get("valid_for_claim", "false"),
                "import_status": "NUMERIC_PRODUCT_BOUND_IMPORTED_NONCLAIM" if bound_1 is not None else "MISSING_NUMERIC_BOUND",
                "generated_utc": now,
            }
        )
    for row in read_csv(WEP):
        bound = maybe_float(row.get("eta_bound"))
        beta_max = maybe_float(row.get("required_abs_beta_source_max"))
        anchor_rows.append(
            {
                "anchor_id": row.get("projection_id", ""),
                "arena": row.get("arena", "WEP"),
                "source_file": WEP.name,
                "observable": row.get("channel", ""),
                "bound_value": bound if bound is not None else "MISSING_NUMERIC_BOUND",
                "bound_value_2sigma": "",
                "units": "dimensionless eta",
                "interpretation": f"required_abs_beta_source_max={beta_max}" if beta_max is not None else row.get("missing_for_claim", ""),
                "score_ready": row.get("score_ready", "false"),
                "valid_for_claim": row.get("valid_for_claim", "false"),
                "import_status": "NUMERIC_PROJECTION_BOUND_IMPORTED_NONCLAIM" if bound is not None else "MISSING_NUMERIC_BOUND",
                "generated_utc": now,
            }
        )
    for row in read_csv(R10):
        anchor_rows.append(
            {
                "anchor_id": row.get("projection_id", ""),
                "arena": row.get("arena", "R10"),
                "source_file": R10.name,
                "observable": row.get("formula", ""),
                "bound_value": "MISSING_PROMOTED_R10_BOUND_OR_PROJECTION",
                "bound_value_2sigma": "",
                "units": "dimensionless alpha(lambda)",
                "interpretation": row.get("missing_inputs", ""),
                "score_ready": row.get("score_ready", "false"),
                "valid_for_claim": row.get("valid_for_claim", "false"),
                "import_status": "DEFINITION_ONLY_NONCLAIM",
                "generated_utc": now,
            }
        )

    mts_rows: list[dict[str, object]] = []
    for row in read_csv(SMOKE_3223):
        numeric_value = maybe_float(row.get("value"))
        source_path = str(row.get("source_path", ""))
        source_ok = bool(source_path) and not source_path.startswith("MISSING")
        numeric_ready = row.get("numeric_ready", "false").lower() == "true" and numeric_value is not None
        claim_ready = row.get("valid_for_claim", "false").lower() == "true" and numeric_ready and source_ok
        mts_rows.append(
            {
                "input_id": row.get("input_id", ""),
                "quantity": row.get("quantity", ""),
                "value": row.get("value", ""),
                "numeric_value": numeric_value if numeric_value is not None else "MISSING_OR_PLACEHOLDER",
                "units": row.get("units", ""),
                "source_path": source_path,
                "source_ok": b(source_ok),
                "numeric_ready": b(numeric_ready),
                "valid_for_claim": b(claim_ready),
                "readiness_status": "CLAIM_READY" if claim_ready else "SCHEMA_ONLY_OR_MISSING_SOURCE",
                "generated_utc": now,
            }
        )

    claim_ready_inputs = {row["quantity"]: row for row in mts_rows if row["valid_for_claim"] == "true"}
    anchor_claim_ready = [row for row in anchor_rows if row["valid_for_claim"] == "true" and maybe_float(row["bound_value"]) is not None]
    has_prediction = bool(claim_ready_inputs)
    has_claim_bound = bool(anchor_claim_ready)
    comparison_rows = [
        {
            "comparison_id": "CMP3224_0_clock",
            "arena": "clock",
            "prediction_formula": "|b_alpha_m * tau_clock_time|",
            "prediction_value": "NOT_COMPUTED",
            "bound_value": "2.1e-18 best imported product anchor, nonclaim",
            "comparison_status": "blocked_missing_claim_ready_prediction",
            "claim_allowed": "false",
            "issues": "b_alpha_m/tau_clock_time not claim-ready; imported clock rows are product bounds only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "comparison_id": "CMP3224_1_WEP",
            "arena": "WEP",
            "prediction_formula": "b_alpha_m * tau_WEP * beta_source_alpha * DeltaQ_alpha",
            "prediction_value": "NOT_COMPUTED",
            "bound_value": "2.8e-15 MICROSCOPE eta anchor, nonclaim",
            "comparison_status": "blocked_missing_projection_inputs",
            "claim_allowed": "false",
            "issues": "tau_WEP and beta_source_alpha missing; no clock-to-WEP shortcut",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "comparison_id": "CMP3224_2_R10",
            "arena": "R10",
            "prediction_formula": "alpha_X(lambda)=K_X beta_s beta_t + epsilon_tail",
            "prediction_value": "NOT_COMPUTED",
            "bound_value": "MISSING_PROMOTED_BOUND_CURVE_AND_PROJECTIONS",
            "comparison_status": "blocked_missing_R10_projection_and_bound_curve",
            "claim_allowed": "false",
            "issues": "tau_R10, K_X(lambda), source/test beta projections, and promoted bound curve missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "comparison_id": "CMP3224_3_runner_summary",
            "arena": "all",
            "prediction_formula": "strict acceptance gate",
            "prediction_value": f"claim_ready_inputs={len(claim_ready_inputs)}",
            "bound_value": f"claim_ready_bounds={len(anchor_claim_ready)}",
            "comparison_status": "runner_refuses_claims",
            "claim_allowed": b(has_prediction and has_claim_bound),
            "issues": "no claim-ready MTS prediction inputs and no claim-ready imported anchor rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    blocker_rows = [
        {
            "blocker_id": "BLK3224_0_first_MTS_scalar",
            "needed_input": "one of: exact b_alpha_m=0 theorem switch OR finite b_alpha_m bound",
            "why_first": "without this the propagator has no MTS prediction to send into any arena",
            "candidate_source": "R_Z parent residual or finite lambda_D/DRQ/Delta_m/Z_min row",
            "current_status": "MISSING",
            "next_action": "source lambda_D, ||D_m R_Q||, Delta m, and Z_min or source-sign exact R_Q root",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "blocker_id": "BLK3224_1_clock_projection",
            "needed_input": "tau_clock_time",
            "why_first": "clock rows bound b_alpha*tau, not b_alpha alone",
            "candidate_source": "clock readout/local Xhat normalization row",
            "current_status": "MISSING",
            "next_action": "do not divide the clock bound by an assumed tau",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "blocker_id": "BLK3224_2_WEP_projection",
            "needed_input": "tau_WEP and beta_source_alpha",
            "why_first": "WEP alpha/Coulomb test needs source/test material projection",
            "candidate_source": "material sensitivity/source label theorem or finite prior row",
            "current_status": "MISSING",
            "next_action": "fill beta_source_alpha and tau_WEP before comparison",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "blocker_id": "BLK3224_3_R10_projection",
            "needed_input": "tau_R10, K_X(lambda), beta_s, beta_t, promoted bound curve",
            "why_first": "R10 cannot inherit clock/WEP alpha constraints without profile/material maps",
            "candidate_source": "R10 alpha-bound acquisition and Yukawa profile convention",
            "current_status": "MISSING",
            "next_action": "keep R10 at definition-only until bound curve/projections are real",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "blocker_id": "BLK3224_4_stress_readout",
            "needed_input": "eta_stress and eta_readout",
            "why_first": "alpha product pass would still not prove Maxwell stress/Poynting or observed alpha safety",
            "candidate_source": "R_H/R_W stress-readout residual theorem or finite bound",
            "current_status": "MISSING",
            "next_action": "retain separate Maxwell stress gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3224_0_result",
            "decision": "FINITE_ALPHA_PROPAGATOR_BUILT_NO_CLAIM_READY_PREDICTIONS",
            "because": "clock/WEP/R10 anchors can be imported, but MTS b_alpha/projection inputs remain placeholders or nonclaim product rows",
            "claim_status": "NO_CLOCK_NO_WEP_NO_R10_NO_MAXWELL_STRESS_NO_LOCAL_GR_CLAIM",
            "next_action": "source the first real finite MTS input: exact b_alpha zero switch, or lambda_D/DRQ/Delta_m/Z_min for finite bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3224_1_next_target",
            "decision": "3225-Y5-R2FR-first-real-alpha-input-acquisition-balpha-zero-or-lambdaD-DRQ-Zmin-under-AX1090",
            "because": "the propagator is now ready; the bottleneck is not arena plumbing but the first source-backed MTS alpha input",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "prioritize R_Z exact-zero source row; fallback to finite lambda_D, ||D_m R_Q||, Delta m, and Z_min acquisition",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, contract_rows, anchor_rows, mts_rows, comparison_rows, blocker_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    anchor_rows: list[dict[str, object]],
    mts_rows: list[dict[str, object]],
    comparison_rows: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, CONTRACT, ANCHORS, MTS, COMPARISON, BLOCKERS, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    numeric_anchors = sum(maybe_float(row["bound_value"]) is not None for row in anchor_rows)
    claim_ready_mts = sum(row["valid_for_claim"] == "true" for row in mts_rows)
    claims_allowed = sum(row["claim_allowed"] == "true" for row in comparison_rows)
    claim_true_count = 0
    for rows in [input_rows, contract_rows, anchor_rows, mts_rows, comparison_rows, blocker_rows, decision_rows]:
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
        {"check_id": "VAL3224_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3224_01_bound_anchors_imported", "pass": b(numeric_anchors >= 4), "detail": f"numeric_anchors={numeric_anchors}", "generated_utc": now},
        {"check_id": "VAL3224_02_no_claim_ready_mts_inputs", "pass": b(claim_ready_mts == 0), "detail": f"claim_ready_mts={claim_ready_mts}", "generated_utc": now},
        {"check_id": "VAL3224_03_runner_refuses_claims", "pass": b(claims_allowed == 0), "detail": f"claim_allowed_rows={claims_allowed}", "generated_utc": now},
        {"check_id": "VAL3224_04_first_input_blockers_written", "pass": b(len(blocker_rows) >= 5), "detail": ";".join(row["blocker_id"] for row in blocker_rows), "generated_utc": now},
        {"check_id": "VAL3224_05_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3224_06_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3224_07_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3224_08_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3225-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    anchor_rows: list[dict[str, object]],
    mts_rows: list[dict[str, object]],
    comparison_rows: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3224 - Finite Alpha Bound Propagator Clock/WEP/R10 under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3224 builds the finite-alpha propagator.

The important result is not a pass. It is a reusable gate:

```text
MTS alpha input -> clock/WEP/R10 product prediction -> compare only against source-valid bounds.
```

The propagator imports real anchor rows where they exist:

```text
clock: product bounds such as |b_alpha * tau_clock_time|
WEP: MICROSCOPE alpha/Coulomb projection target
R10: projection law definitions, but no promoted bound/projection package
```

It refuses claims because the MTS side is still missing the first real input:

```text
exact b_alpha_m=0 theorem switch
or finite lambda_D, ||D_m R_Q||, Delta m, Z_min.
```

So this is progress in the non-glamorous but necessary sense: the arena plumbing now exists, and it will not let fake unity projections or clock-to-WEP/R10 shortcuts through.

Current verdict: `FINITE_ALPHA_PROPAGATOR_BUILT_NO_CLAIM_READY_PREDICTIONS`.

## Propagator Contract

{md_table(contract_rows, ["contract_id", "arena", "prediction_formula", "required_mts_inputs", "bound_source", "claim_rule", "current_status", "valid_for_claim"])}

## Imported Bound Anchors

{md_table(anchor_rows, ["anchor_id", "arena", "observable", "bound_value", "units", "interpretation", "score_ready", "valid_for_claim", "import_status"])}

## MTS Alpha Input Readiness

{md_table(mts_rows, ["input_id", "quantity", "value", "numeric_value", "source_ok", "numeric_ready", "valid_for_claim", "readiness_status"])}

## Product Comparison Results

{md_table(comparison_rows, ["comparison_id", "arena", "prediction_formula", "prediction_value", "bound_value", "comparison_status", "claim_allowed", "issues", "valid_for_claim"])}

## First Real Input Blockers

{md_table(blocker_rows, ["blocker_id", "needed_input", "why_first", "candidate_source", "current_status", "next_action", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_PROPAGATOR_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_IMPORTED_BOUND_ANCHORS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_MTS_ALPHA_INPUT_READINESS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_PRODUCT_COMPARISON_RESULTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_FIRST_REAL_INPUT_BLOCKERS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3224_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, contract_rows, anchor_rows, mts_rows, comparison_rows, blocker_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (CONTRACT, contract_rows),
        (ANCHORS, anchor_rows),
        (MTS, mts_rows),
        (COMPARISON, comparison_rows),
        (BLOCKERS, blocker_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(now, input_rows, contract_rows, anchor_rows, mts_rows, comparison_rows, blocker_rows, decision_rows)
    write_csv(VALIDATION, validation)
    write_doc(input_rows, contract_rows, anchor_rows, mts_rows, comparison_rows, blocker_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
