from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_NAME = "928-Y5-R10-instantiate-compact-BF-lattice-or-retain-KBFH-residual-bound-row.md"
STATUS = "Y5_R10_928_compact_BF_lattice_not_instantiated_KBFH_retained_as_explicit_residual_bound_rows"
CLAIM_CEILING = "KBFH_residual_bound_rows_only_no_numeric_KBFH_no_WEP_R10_PPN_Newton_or_local_GR_claim"
NEXT_TARGET = "929-Y5-R10-KBFH-residual-bound-runner-smoke-or-compact-period-proof.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "927_doc",
            "path": "927-Y5-R10-compact-BF-lattice-parent-action-contract-or-JHH-source-proof.md",
            "role": "compact BF parent-action contract and next target",
            "needle": "K_H/k_M = N_B/N_H",
        },
        {
            "source_id": "927_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_927_VALIDATION.csv",
            "role": "proves 927 validation passed",
            "needle": "V927_10_validation_rows_ready",
        },
        {
            "source_id": "927_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_927_COMPACT_BF_PARENT_ACTION_CONTRACT.csv",
            "role": "contract clauses to instantiate or demote",
            "needle": "CBF927_2_normalized_BF_action",
        },
        {
            "source_id": "512_symbol_map",
            "path": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
            "role": "current MTS symbol map; no compact A_M/B_M lattice instantiation",
            "needle": "no_symbol_fully_promotes_local_GR",
        },
        {
            "source_id": "511_parent_ansatz",
            "path": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
            "role": "minimal local-GR parent action and fixed-point gates",
            "needle": "current_MTS_has_not_yet_matched_the_contract",
        },
        {
            "source_id": "920_force_bound_pack",
            "path": "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md",
            "role": "A_M holonomy and K_BF_H force-bound source-ready schema",
            "needle": "SR920_1_K_BF_H",
        },
        {
            "source_id": "921_weak_field_map",
            "path": "921-Y5-R10-FM-force-weak-field-map-and-KBFH-units-bound-runner.md",
            "role": "weak-field residual map and local bound interface",
            "needle": "epsilon_FM := |K_BF_H|",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "source-backed local bound rows for residual coupling fallback",
            "needle": "R10_fifth_force",
        },
        {
            "source_id": "R10_curve",
            "path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "role": "R10 curve status; still cannot score without real alpha(lambda) prediction and curve",
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "current MTS symbols do not instantiate the compact BF lattice; K_BF_H is retained as an explicit residual coupling rather than hidden normalization",
            "what_changed": "the failed compact-lattice route now produces a source-backed local-bound fallback matrix with every row blocked until numeric parent inputs exist",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def instantiation_rows() -> list[dict[str, object]]:
    return [
        {
            "test_id": "INST928_0_A_M_compact_period",
            "contract_clause": "CBF927_0_compact_parent_fields",
            "current_symbol_candidate": "A_M mass-gauge one-form from 920",
            "evidence_found": "dA_M=0 and conditional exactness if H1(D)=0/no defects",
            "result": "fail_for_claim",
            "reason": "flat/exact one-form is not a compact gauge field with parent-derived integral periods",
            "fallback": "retain A_M_holonomy/A_M_norm as residual input",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "INST928_1_B_M_compact_period",
            "contract_clause": "CBF927_0;CBF927_2",
            "current_symbol_candidate": "B_M from 924/927 symbolic BF normalization",
            "evidence_found": "B_M appears in the symbolic parent-action candidate only",
            "result": "fail_for_claim",
            "reason": "no current MTS symbol map supplies B_M compact 2-form periods or a boundary flux unit",
            "fallback": "retain B_M_charge_unit/B_zero_flux as residual input",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "INST928_2_kappa_A3_not_enough",
            "contract_clause": "CBF927_1_large_gauge_invariance",
            "current_symbol_candidate": "A_3/kappa topological sector from 511/512",
            "evidence_found": "topological kappa route can make kappa_eff constant conditionally",
            "result": "not_applicable_for_KBFH_claim",
            "reason": "A_3 fixes kappa/G drift if adopted; it is not the compact A_M/B_M mass-gauge BF lattice",
            "fallback": "do not borrow kappa topology to normalize K_BF_H",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "INST928_3_JHH_source_lattice",
            "contract_clause": "CBF927_3_source_current_lattice",
            "current_symbol_candidate": "J_H/Hilbert source current",
            "evidence_found": "universal matter/source frame is a conditional ansatz; source-measure glue remains open",
            "result": "fail_for_claim",
            "reason": "J_H is not parent-derived as an integral compact source lattice current",
            "fallback": "retain J_H normalization/source-lattice residual input",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "INST928_4_same_worldtube",
            "contract_clause": "CBF927_4_same_worldtube_boundary_class",
            "current_symbol_candidate": "W_source=supp(J_H[e_obs]) plus B_M boundary class",
            "evidence_found": "worldtube support is a guardrail; same-class certificate remains missing",
            "result": "fail_for_claim",
            "reason": "no certificate ties B_M boundary flux to the same Hilbert source worldtube",
            "fallback": "retain wrong-charge/topological-class residual gate",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "INST928_5_ratio",
            "contract_clause": "CBF927_5;CBF927_6",
            "current_symbol_candidate": "K_BF_H/k_M = R_BJ",
            "evidence_found": "conditional ratio law from 925-927",
            "result": "conditional_only",
            "reason": "N_B, N_H, source measure, and Gauss readout are not parent-signed",
            "fallback": "K_BF_H_residual remains explicit and unscored",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def residual_parameter_rows() -> list[dict[str, object]]:
    return [
        {
            "parameter_id": "KRES928_0_KBFH_over_kM_residual",
            "symbol": "K_BF_H/k_M",
            "meaning": "residual mass-gauge source coupling ratio after compact-BF instantiation fails",
            "formula": "K_BF_H/k_M = R_BJ + delta_K_res, with R_BJ symbolic and delta_K_res retained",
            "required_inputs": "A_M_norm; B_M_charge_unit; J_H_source_lattice; same_worldtube_certificate; projection_coefficients",
            "current_value": "MISSING_PARENT_NORMALIZATION",
            "status": "retained_residual_not_prediction",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "parameter_id": "KRES928_1_epsilon_FM_residual",
            "symbol": "epsilon_FM",
            "meaning": "dimensionless local pressure from K_BF_H branch before arena projection",
            "formula": "epsilon_FM = |K_BF_H| |A_M| |dPiMJ_leak| / N_FM + |K_BF_H| |B_zero_flux| / N_B",
            "required_inputs": "K_BF_H_units; A_M_norm; dPiMJ_numeric; B_zero_flux; N_FM; N_B",
            "current_value": "MISSING_NUMERIC_RESIDUAL_INPUTS",
            "status": "retained_residual_not_prediction",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def bound_rows() -> list[dict[str, object]]:
    wanted = {
        "R1_WEP_source_charge": "eta_FM_AB",
        "R2_clock_redshift": "alpha_clock_FM",
        "R3_gamma": "delta_gamma_FM",
        "R4_beta": "delta_beta_FM",
        "R5_alpha1": "alpha1_FM",
        "R6_alpha2": "alpha2_FM",
        "R7_alpha3": "alpha3_FM",
        "R8_xi": "xi_FM",
        "R9_Gdot": "Gdot_FM_over_G",
        "R10_fifth_force": "alpha_FM_lambda",
    }
    rows: list[dict[str, object]] = []
    for index, bound in enumerate(read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")):
        row_id = bound["row_id"]
        if row_id not in wanted:
            continue
        symbol = wanted[row_id]
        if row_id == "R10_fifth_force":
            prediction_template = "alpha_FM(lambda) = C_R10_FM(lambda) * epsilon_FM(lambda)"
            missing = "MISSING_KBFH_RESIDUAL; MISSING_RANGE_LAW; MISSING_ALPHA_LAMBDA_PREDICTION; R10_CURVE_PLACEHOLDER"
        else:
            prediction_template = f"{symbol} = C_{row_id}_FM * epsilon_FM"
            missing = "MISSING_KBFH_RESIDUAL; MISSING_EPSILON_FM; MISSING_PROJECTION_COEFFICIENT"
        rows.append(
            {
                "bound_row_id": f"KBOUND928_{index}_{row_id}",
                "source_dataset_id": bound["dataset_id"],
                "local_bound_row": row_id,
                "observable": bound["observable"],
                "upper_bound": bound["upper_bound"],
                "bound_units": bound["units"],
                "residual_symbol": symbol,
                "prediction_template": prediction_template,
                "missing_inputs": missing,
                "score_status": "blocked_missing_KBFH_residual_inputs",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def fallback_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD928_0_compact_BF_instantiation",
            "branch": "compact_BF_lattice",
            "verdict": "not_instantiated_for_current_MTS",
            "reason": "current MTS symbol map lacks compact A_M/B_M periods, source lattice, and same-worldtube certificate",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD928_1_KBFH_residual",
            "branch": "residual_coupling_fallback",
            "verdict": "retained_explicitly",
            "reason": "K_BF_H now becomes a named residual coupling with source-backed local bound rows, not a hidden normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD928_2_next",
            "branch": "next_runner",
            "verdict": "selected",
            "reason": "run a strict residual-bound smoke runner or retry compact-period proof with concrete parent-symbol candidates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE928_0_compact_BF_pass",
            "claim": "current MTS instantiates compact BF lattice",
            "blocker": "A_M/B_M compact periods and large-gauge invariance are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE928_1_KBFH_numeric",
            "claim": "K_BF_H/k_M has numeric value or +/-1",
            "blocker": "N_B/N_H not sourced; K_BF_H retained as residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE928_2_bound_rows_score",
            "claim": "WEP/R10/clock/PPN/local bound rows pass",
            "blocker": "all prediction templates still have MISSING_* inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE928_3_Newton_local_GR",
            "claim": "source-normalized Newton/local GR is derived",
            "blocker": "source measure, Gauss readout, PPN followthrough, and residual scoring remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "run a strict smoke evaluator over K_BF_H residual rows or provide a concrete compact-period proof for A_M/B_M",
            "include": "parse residual rows, require no MISSING inputs for scoring, keep R10 symbolic until real alpha(lambda) prediction and bound curve exist, retry compact-period proof only with source-backed parent symbols",
            "exclude": "numeric pass claims, hidden G/M absorption, +/-1 promotion without proof, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    sources: list[dict[str, object]],
    instantiation: list[dict[str, object]],
    residual_params: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = OUT / "P8_Y5_BRR545_927_VALIDATION.csv"
    prior_rows = read_csv(prior) if prior.exists() else []
    prior_ok = bool(prior_rows) and all(row.get("result") == "pass" for row in prior_rows)
    instantiation_failed_cleanly = any(row["result"] == "fail_for_claim" for row in instantiation) and all(row["valid_for_claim"] == "false" for row in instantiation)
    residual_written = len(residual_params) >= 2 and all(row["valid_for_claim"] == "false" for row in residual_params)
    bound_rows_blocked = len(bounds) >= 10 and all(row["valid_for_claim"] == "false" and "MISSING" in str(row["missing_inputs"]) for row in bounds)
    changed = formalization_changed_count()
    generated = instantiation + residual_params + bounds + decisions + gates
    false_fields = ("claim_allowed", "valid_for_claim")
    return [
        {
            "check_id": "V928_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source path or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_1_prior_927_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_927_VALIDATION.csv clean" if prior_ok else "927 validation missing or not clean",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_2_compact_BF_instantiation_failed_cleanly",
            "result": "pass" if instantiation_failed_cleanly else "fail",
            "detail": "compact BF instantiation is explicitly blocked without promotion",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_3_KBFH_residual_written",
            "result": "pass" if residual_written else "fail",
            "detail": "K_BF_H and epsilon_FM residual parameters are explicit nonclaim rows",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_4_source_bound_rows_blocked",
            "result": "pass" if bound_rows_blocked else "fail",
            "detail": "source-backed local bound rows are joined but all predictions remain blocked",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_5_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "compact-BF, numeric KBFH, local-bound, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_6_decisions_nonclaim",
            "result": "pass" if all_false(decisions, false_fields) else "fail",
            "detail": "fallback decisions are explicit and nonclaim",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_7_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_8_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_9_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("929-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V928_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    instantiation: list[dict[str, object]],
    residual_params: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 928 - Y5/R10 Instantiate Compact BF Lattice Or Retain KBFH Residual Bound Row

Private instantiation checkpoint. This is not a public WEP, clock, PPN, R10, Newton, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the compact BF lattice route does not instantiate against the current MTS symbol map.**

The useful consequence is not to bury the coupling. `K_BF_H/k_M` is now retained as an explicit residual coupling:

```text
K_BF_H/k_M = R_BJ + delta_K_res,
epsilon_FM = |K_BF_H| |A_M| |dPiMJ_leak| / N_FM + |K_BF_H| |B_zero_flux| / N_B.
```

Every local-bound row remains blocked until the missing parent inputs are supplied. This is the honest route: either prove the compact periods/same-worldtube lattice, or score the residual with real source-backed inputs.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Compact BF Instantiation Audit

{md_table(instantiation, ["test_id", "contract_clause", "current_symbol_candidate", "evidence_found", "result", "reason", "fallback", "valid_for_claim", "generated_utc"])}

## KBFH Residual Parameters

{md_table(residual_params, ["parameter_id", "symbol", "meaning", "formula", "required_inputs", "current_value", "status", "valid_for_claim", "generated_utc"])}

## Residual Bound Rows

{md_table(bounds, ["bound_row_id", "source_dataset_id", "local_bound_row", "observable", "upper_bound", "bound_units", "residual_symbol", "prediction_template", "missing_inputs", "score_status", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = build_sources()
    summary = summary_rows()
    instantiation = instantiation_rows()
    residual_params = residual_parameter_rows()
    bounds = bound_rows()
    decisions = fallback_decision_rows()
    gates = claim_gate_rows()
    next_target = next_rows()
    validation = validation_rows(sources, instantiation, residual_params, bounds, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_928_SOURCE_REGISTER.csv", sources, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_COMPACT_BF_INSTANTIATION_AUDIT.csv", instantiation, ["test_id", "contract_clause", "current_symbol_candidate", "evidence_found", "result", "reason", "fallback", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_KBFH_RESIDUAL_PARAMETERS.csv", residual_params, ["parameter_id", "symbol", "meaning", "formula", "required_inputs", "current_value", "status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_KBFH_RESIDUAL_BOUND_ROWS.csv", bounds, ["bound_row_id", "source_dataset_id", "local_bound_row", "observable", "upper_bound", "bound_units", "residual_symbol", "prediction_template", "missing_inputs", "score_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_928_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_928_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(sources, summary, instantiation, residual_params, bounds, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
