from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def parse_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "947_doc",
            "path": "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
            "role": "handoff: source side improved but coefficient/projection handshake missing",
            "needle": "source side cleaner",
        },
        {
            "source_id": "947_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_947_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V947_13_validation_rows_ready",
        },
        {
            "source_id": "947_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_947_NEXT_TARGET.csv",
            "role": "948 target selection",
            "needle": "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md",
        },
        {
            "source_id": "947_bound_interface",
            "path": "source-intake/mts_residuals/P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv",
            "role": "clock/WEP interface rows inherited from 947",
            "needle": "BI947_3_clock_product_AlHg",
        },
        {
            "source_id": "647_clock_product_bound",
            "path": "source-intake/mts_residuals/P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
            "role": "source-backed clock product bounds",
            "needle": "CPB647_0_AlHg",
        },
        {
            "source_id": "647_tau_clock_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
            "role": "clock product-map definition",
            "needle": "TAU647_0_time_drift",
        },
        {
            "source_id": "646_clock_alpha_sensitivity",
            "path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "role": "clock alpha sensitivities",
            "needle": "CAS646_1_YbE3E2",
        },
        {
            "source_id": "766_clock_source_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_766_CLOCK_ALPHA_SOURCE_LOCK.csv",
            "role": "clock source-lock and Galileo exclusion",
            "needle": "R2R766_Galileo_repair",
        },
        {
            "source_id": "651_WEP_stress",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv",
            "role": "WEP source-normalization stress bounds",
            "needle": "WAS651_1_surface_binding",
        },
        {
            "source_id": "651_material_model",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv",
            "role": "MICROSCOPE material model",
            "needle": "MM651_TA6V_Ti",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "constant/source no-marker contract",
            "needle": "S2_constant_sector_universality",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "no-marker/no-spurion theorem attempt",
            "needle": "NMS763_2_constant_superselection",
        },
        {
            "source_id": "633_matter_frame_cases",
            "path": "source-intake/mts_residuals/P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv",
            "role": "matter-frame candidate classification",
            "needle": "MFC633_7_631_variation",
        },
        {
            "source_id": "631_source_charge_law",
            "path": "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "role": "source/test charge law with quotient-zero branch",
            "needle": "Q631_1_quotient_zero_charge",
        },
        {
            "source_id": "local_bounds",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "local WEP/clock empirical anchors",
            "needle": "R1_WEP_source_charge",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def constant_superselection_attempt() -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "CST948_0_target",
            "statement": "ordinary constants and source weights are selector-trivial superselection labels",
            "mathematical_form": "for every local vertical v in ker(Dq), Lie_v theta_univ=0 and Lie_v kappa_A=0",
            "proof_status": "target_identified",
            "what_is_proved_here": "this is exactly the clause needed to kill b_A and clock alpha drift from marker/quotient leakage",
            "blocking_gap": "not yet parent-selected as an axiom/theorem of S_parent",
            "counterexample_status": "legal_until_excluded",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST948_1_conditional_chain_rule",
            "statement": "if S_matter descends through q and constants are external labels, vertical variations cannot change ordinary constants",
            "mathematical_form": "S_matter=Sbar[q(Phi),Psi,theta_univ] and v(theta_univ)=0 imply Lie_v S_matter=<Dq[v],delta Sbar/dq>=0",
            "proof_status": "valid_conditional_lemma",
            "what_is_proved_here": "under the stated premises, b_A=0 and kappa_alpha*tau leakage is absent",
            "blocking_gap": "premises are stronger than the current parent corpus signs",
            "counterexample_status": "counterexamples excluded only if premises are parent-signed",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST948_2_constant_sector",
            "statement": "alpha_EM, charge normalization, and mass ratios do not depend on markers or quotient representatives",
            "mathematical_form": "partial_m theta_A=partial_IQ theta_A=partial_A theta_A=0",
            "proof_status": "not_derived",
            "what_is_proved_here": "no new proof beyond the conditional no-species contract",
            "blocking_gap": "species_internal_constants counterexample remains allowed by current sources",
            "counterexample_status": "legal",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST948_3_source_weight",
            "statement": "source normalization is species blind and does not carry a selector-dependent kappa_A",
            "mathematical_form": "J_source=sum_A kappa T_A with Lie_v kappa=0 and no kappa_A(X)",
            "proof_status": "not_parent_signed",
            "what_is_proved_here": "identifies the precise WEP source-normalization condition",
            "blocking_gap": "selector-blind measured-GM/source-current theorem missing",
            "counterexample_status": "species-weighted source remains legal",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST948_4_countermodel",
            "statement": "metric descent alone does not force constants or source weights to be marker-free",
            "mathematical_form": "q(Phi) fixed but theta_A=theta_0 exp(epsilon m_A) gives Lie_v theta_A != 0 when Lie_v m_A != 0",
            "proof_status": "countermodel_blocks_unconditional_theorem",
            "what_is_proved_here": "a quotient metric can be silent while ordinary constants still leak unless no-marker/constant clauses are imposed",
            "blocking_gap": "must forbid matter-visible marker dependence at parent-action level",
            "counterexample_status": "legal_until_no_marker_parent_clause",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "CST948_5_total_verdict",
            "statement": "constant-superselection/no-marker theorem sets b_A and clock product leakage to zero",
            "mathematical_form": "b_A=kappa_alpha*tau_clock_time=0 from parent-signed constant/source/no-marker clauses",
            "proof_status": "not_closed_current_corpus",
            "what_is_proved_here": "conditional route is mathematically clean, but not parent-owned",
            "blocking_gap": "S0/S1/S2/S3/S4 plus NMS763 constant/source clauses remain unsigned",
            "counterexample_status": "countermodel_retained",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def clock_product_runner() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv"):
        bound_1sigma = parse_float(source.get("conservative_abs_product_bound_1sigma_yr_inv", ""))
        bound_2sigma = parse_float(source.get("conservative_abs_product_bound_2sigma_yr_inv", ""))
        product_symbol = "kappa_alpha * tau_clock_time"
        rows.append(
            {
                "run_id": f"CLK948_{len(rows)}_{source.get('clock_pair_id', 'unknown')}",
                "clock_pair": source.get("clock_pair", ""),
                "product_symbol": product_symbol,
                "projection_law": "d ln(alpha_EM)/dt = kappa_alpha * tau_clock_time",
                "bound_1sigma_abs": "" if bound_1sigma is None else f"{bound_1sigma:.12e}",
                "bound_2sigma_abs": "" if bound_2sigma is None else f"{bound_2sigma:.12e}",
                "units": "yr^-1",
                "source_measurements": source.get("source_measurements", ""),
                "mts_prediction_abs": "MISSING_MTS_PRODUCT",
                "score_rule": f"pass only if abs({product_symbol}) <= bound",
                "source_bound_ready": flag(bound_1sigma is not None and bound_1sigma > 0),
                "mts_prediction_ready": "false",
                "score_ready": "false",
                "verdict": "BOUND_ONLY_NONCLAIM_STANDALONE_PRODUCT_MISSING",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def wep_product_runner() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv"):
        if source.get("required_abs_beta_source_max") == "not_applicable":
            rows.append(
                {
                    "run_id": f"WEP948_{len(rows)}_{source.get('stress_id', 'unknown')}",
                    "channel": source.get("channel", ""),
                    "product_symbol": "not_applicable",
                    "eta_bound": source.get("eta_bound_used", ""),
                    "unit_source_eta_prediction": source.get("unit_source_eta_prediction", ""),
                    "required_abs_product_max": "not_applicable",
                    "units": "dimensionless",
                    "score_rule": "clock screen alone is not a WEP source-force prediction",
                    "source_bound_ready": "false",
                    "mts_prediction_ready": "false",
                    "score_ready": "false",
                    "verdict": source.get("verdict", "diagnostic_only"),
                    "valid_for_claim": "false",
                    "generated_utc": stamp(),
                }
            )
            continue
        eta_bound = parse_float(source.get("eta_bound_used", ""))
        unit_eta = parse_float(source.get("unit_source_eta_prediction", ""))
        existing_cap = parse_float(source.get("required_abs_beta_source_max", ""))
        computed_cap = eta_bound / unit_eta if eta_bound is not None and unit_eta not in (None, 0.0) else None
        cap = existing_cap if existing_cap is not None else computed_cap
        rows.append(
            {
                "run_id": f"WEP948_{len(rows)}_{source.get('stress_id', 'unknown')}",
                "channel": source.get("channel", ""),
                "product_symbol": "beta_source_normalized",
                "eta_bound": "" if eta_bound is None else f"{eta_bound:.12e}",
                "unit_source_eta_prediction": "" if unit_eta is None else f"{unit_eta:.12e}",
                "required_abs_product_max": "" if cap is None else f"{cap:.12e}",
                "units": "dimensionless",
                "score_rule": "|beta_source_normalized| <= required_abs_product_max for this channel",
                "source_bound_ready": flag(cap is not None and cap > 0),
                "mts_prediction_ready": "false",
                "score_ready": "false",
                "verdict": "BOUND_ONLY_NONCLAIM_MTS_SOURCE_NORMALIZATION_MISSING",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def product_bound_scoreboard(
    clock_rows: list[dict[str, str]],
    wep_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    numeric_wep_caps = [
        parse_float(row["required_abs_product_max"])
        for row in wep_rows
        if parse_float(row.get("required_abs_product_max", "")) is not None
    ]
    min_wep_cap = min(numeric_wep_caps) if numeric_wep_caps else None
    zero_theorem_closed = any(row["theorem_id"] == "CST948_5_total_verdict" and row["closes_zero"] == "true" for row in theorem_rows)
    return [
        {
            "score_id": "PBS948_0_clock_product",
            "arena": "clock alpha drift",
            "best_bound_statement": "Yb E3/E2 gives the strongest loaded product bound",
            "best_bound_value": min((parse_float(row["bound_1sigma_abs"]) for row in clock_rows if parse_float(row["bound_1sigma_abs"]) is not None), default=float("nan")),
            "best_bound_units": "yr^-1",
            "mts_input_needed": "numeric kappa_alpha*tau_clock_time or theorem-zero constant sector",
            "can_score_now": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "score_id": "PBS948_1_WEP_product",
            "arena": "MICROSCOPE/WEP source normalization",
            "best_bound_statement": "surface/binding diagnostic gives the tightest loaded beta_source cap",
            "best_bound_value": "" if min_wep_cap is None else f"{min_wep_cap:.12e}",
            "best_bound_units": "dimensionless",
            "mts_input_needed": "numeric source-normalized beta_source or theorem-zero species/source charge",
            "can_score_now": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "score_id": "PBS948_2_zero_theorem",
            "arena": "constant-superselection/no-marker",
            "best_bound_statement": "if parent-signed, products are zero and local clock/WEP side constraints are automatically silent",
            "best_bound_value": "0" if zero_theorem_closed else "NOT_DERIVED",
            "best_bound_units": "coefficient",
            "mts_input_needed": "parent-signed S0/S1/S2/S3/S4 plus no-marker clauses",
            "can_score_now": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC948_0_theorem_attempt",
            "topic": "constant-superselection/no-marker theorem",
            "result": "conditional_lemma_valid_but_not_parent_signed",
            "reason": "the chain-rule zero proof works if constants/source weights are external selector-trivial labels, but current corpus still permits marker-dependent constants/source weights",
            "next_action": "try to parent-sign a constant-sector clause or keep finite source coefficients as explicit inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC948_1_clock_runner",
            "topic": "clock product-bound runner",
            "result": "source_bound_executable_nonclaim",
            "reason": "Al/Hg and Yb product bounds are source-backed, but standalone MTS product is missing",
            "next_action": "add candidate input schema for kappa_alpha*tau_clock_time or derive zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC948_2_WEP_runner",
            "topic": "WEP source-product runner",
            "result": "diagnostic_beta_caps_executable_nonclaim",
            "reason": "MICROSCOPE stress rows produce explicit beta_source caps, but source normalization and MTS b_A are missing",
            "next_action": "derive source-normalization species-blind theorem or provide finite beta_source input",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE948_0_constant_superselection",
            "claim": "b_A and clock product leakage are theorem-zero",
            "required_condition": "parent action signs constant-sector universality, source-weight universality, and no-marker clauses",
            "current_evidence": "conditional lemma plus legal countermodel",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE948_1_clock_product_score",
            "claim": "clock product bound passed by MTS",
            "required_condition": "numeric MTS prediction for |kappa_alpha*tau_clock_time| or zero theorem",
            "current_evidence": "source bounds only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE948_2_WEP_product_score",
            "claim": "MICROSCOPE/WEP product bound passed by MTS",
            "required_condition": "numeric source-normalized beta_source/b_A or zero theorem",
            "current_evidence": "diagnostic beta caps only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE948_3_local_GR",
            "claim": "local GR/PPN/R10 branch passes",
            "required_condition": "R10/PPN projections plus source/clock coefficients all closed",
            "current_evidence": "948 improves clock/WEP side only; R10/PPN still blocked from 947",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "949-Y5-R10-parent-constant-sector-superselection-action-clause-or-finite-source-coefficient-input.md",
            "objective": "either parent-sign the constant/source no-marker clause that makes clock/WEP products theorem-zero, or create a finite candidate input schema for kappa_alpha*tau_clock_time and beta_source so the new product runners can score future MTS predictions",
            "include": "S0-S4 constant/source clauses, no-marker countermodel exclusion, clock product bound input, WEP beta_source cap input, nonclaim candidate schema",
            "exclude": "claiming local-GR, claiming WEP/clock pass from source-only bounds, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    clock_rows: list[dict[str, str]],
    wep_rows: list[dict[str, str]],
    scoreboard_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passes else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_947_VALIDATION.csv"))
    theorem_not_closed = any(row["theorem_id"] == "CST948_5_total_verdict" and row["closes_zero"] == "false" for row in theorem_rows)
    countermodel_present = any(row["theorem_id"] == "CST948_4_countermodel" for row in theorem_rows)
    clock_numeric = all(parse_float(row["bound_1sigma_abs"]) is not None and parse_float(row["bound_1sigma_abs"]) > 0 for row in clock_rows)
    clock_nonclaim = all(row["mts_prediction_ready"] == "false" and row["score_ready"] == "false" for row in clock_rows)
    wep_numeric = all(
        row["required_abs_product_max"] == "not_applicable"
        or (parse_float(row["required_abs_product_max"]) is not None and parse_float(row["required_abs_product_max"]) > 0)
        for row in wep_rows
    )
    wep_nonclaim = all(row["mts_prediction_ready"] == "false" and row["score_ready"] == "false" for row in wep_rows)
    scoreboard_nonclaim = all(row["can_score_now"] == "false" and row["claim_allowed"] == "false" for row in scoreboard_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = target_rows and target_rows[0]["next_target"].startswith("949-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, theorem_rows, clock_rows, wep_rows, scoreboard_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V948_0_sources_exist_and_needles", sources_ok, "all 948 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V948_1_prior_947_clean", prior_clean, "P8_Y5_BRR545_947_VALIDATION.csv clean")
    add("V948_2_theorem_not_closed", theorem_not_closed, "constant-superselection total theorem remains unclosed")
    add("V948_3_countermodel_retained", countermodel_present, "marker-dependent constant countermodel recorded")
    add("V948_4_clock_bounds_numeric", clock_numeric, "clock product bounds are positive numeric rows")
    add("V948_5_clock_runner_nonclaim", clock_nonclaim, "clock runner has no MTS product prediction")
    add("V948_6_WEP_caps_numeric", wep_numeric, "WEP source-product caps are numeric or explicitly diagnostic-only")
    add("V948_7_WEP_runner_nonclaim", wep_nonclaim, "WEP runner has no MTS source-normalized prediction")
    add("V948_8_scoreboard_nonclaim", scoreboard_nonclaim, "scoreboard can_score_now=false for every row")
    add("V948_9_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V948_10_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V948_11_next_target_selected", target_selected, "949 parent constant-sector or finite source coefficient target selected")
    add("V948_12_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V948_13_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V948_14_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    clock_rows: list[dict[str, str]],
    wep_rows: list[dict[str, str]],
    scoreboard_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 948 Y5 R10: Clock/WEP Product-Bound Runner Or Constant-Superselection No-Marker Theorem

Status: `Y5_R10_948_product_bound_runners_written_constant_superselection_theorem_not_closed_nonclaim`

Claim ceiling: `clock_WEP_source_bounds_executable_only_no_zero_theorem_no_local_GR_claim`

## Result

This checkpoint took the 947 opening and made it sharper. The theorem route was attempted first: if ordinary constants/source weights are parent-signed superselection labels, then the chain-rule descent proof kills `b_A` and clock leakage cleanly.

That proof is valid only conditionally. The current corpus still permits the countermodel where the quotient metric descends but ordinary constants or source weights depend on a matter-visible marker. So the theorem does not close.

The useful win is practical: the clock and WEP source-side inequalities are now explicit nonclaim runners. They cannot score MTS yet, but when a future parent coefficient or zero theorem appears, these rows are ready to receive it.

```text
derive-zero route: clean but unsigned,
finite-product route: executable as source-side bound only,
no WEP/clock/local-GR claim promoted.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Constant-Superselection Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "statement", "proof_status", "blocking_gap", "counterexample_status", "closes_zero"])}

## Clock Product-Bound Runner

{md_table(clock_rows, ["run_id", "clock_pair", "product_symbol", "bound_1sigma_abs", "bound_2sigma_abs", "mts_prediction_abs", "score_ready", "verdict"])}

## WEP Product-Bound Runner

{md_table(wep_rows, ["run_id", "channel", "product_symbol", "required_abs_product_max", "score_rule", "score_ready", "verdict"])}

## Product-Bound Scoreboard

{md_table(scoreboard_rows, ["score_id", "arena", "best_bound_statement", "best_bound_value", "mts_input_needed", "can_score_now", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    theorem_rows = constant_superselection_attempt()
    clock_rows = clock_product_runner()
    wep_rows = wep_product_runner()
    scoreboard_rows = product_bound_scoreboard(clock_rows, wep_rows, theorem_rows)
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        theorem_rows,
        clock_rows,
        wep_rows,
        scoreboard_rows,
        decision_rows,
        claim_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_948_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv",
        theorem_rows,
        [
            "theorem_id",
            "statement",
            "mathematical_form",
            "proof_status",
            "what_is_proved_here",
            "blocking_gap",
            "counterexample_status",
            "closes_zero",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv",
        clock_rows,
        [
            "run_id",
            "clock_pair",
            "product_symbol",
            "projection_law",
            "bound_1sigma_abs",
            "bound_2sigma_abs",
            "units",
            "source_measurements",
            "mts_prediction_abs",
            "score_rule",
            "source_bound_ready",
            "mts_prediction_ready",
            "score_ready",
            "verdict",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv",
        wep_rows,
        [
            "run_id",
            "channel",
            "product_symbol",
            "eta_bound",
            "unit_source_eta_prediction",
            "required_abs_product_max",
            "units",
            "score_rule",
            "source_bound_ready",
            "mts_prediction_ready",
            "score_ready",
            "verdict",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_PRODUCT_BOUND_SCOREBOARD.csv",
        scoreboard_rows,
        [
            "score_id",
            "arena",
            "best_bound_statement",
            "best_bound_value",
            "best_bound_units",
            "mts_input_needed",
            "can_score_now",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_948_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_948_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        theorem_rows,
        clock_rows,
        wep_rows,
        scoreboard_rows,
        decision_rows,
        claim_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
