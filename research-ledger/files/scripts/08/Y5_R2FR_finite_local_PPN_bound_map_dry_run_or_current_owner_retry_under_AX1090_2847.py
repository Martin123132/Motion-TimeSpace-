from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2847-Y5-R2FR-finite-local-PPN-bound-map-dry-run-or-current-owner-retry-under-AX1090.md"

SRC_2846_DOC = ROOT / "2846-Y5-R2FR-parent-current-owner-or-finite-local-PPN-input-contract-under-AX1090.md"
SRC_2846_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2846_FINITE_LOCAL_PPN_INPUT_CONTRACT.csv"
SRC_2846_FORMULA = RESIDUALS / "P8_Y5_R2FR_2846_LOCAL_PPN_FORMULA_PACK_NONCLAIM.csv"
SRC_2846_NEXT = RESIDUALS / "P8_Y5_R2FR_2846_NEXT_TARGET.csv"
SRC_2846_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2846_VALIDATION.csv"
SRC_2631 = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"
SRC_1181 = ROOT / "1181-Y5-R10-PPN-KS-residual-vector-source-pack-or-parent-Q-identity-proof.md"
SRC_1883 = ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2847_SOURCE_REGISTER.csv",
    "bound_map": RESIDUALS / "P8_Y5_R2FR_2847_DRY_RUN_BOUND_MAP.csv",
    "input_gates": RESIDUALS / "P8_Y5_R2FR_2847_PREDICTION_INPUT_GATES.csv",
    "score_rules": RESIDUALS / "P8_Y5_R2FR_2847_NO_CANCELLATION_SCORE_RULES.csv",
    "dry_results": RESIDUALS / "P8_Y5_R2FR_2847_DRY_RUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2847_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2847_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2847_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2847_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2847_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "bound_map_copy": LOCAL_BOUNDS / "RAB_CAB_finite_local_PPN_bound_map_2847_NONCLAIM.csv",
    "input_gates_copy": SOURCE_WEIGHT / "RAB_CAB_local_PPN_prediction_input_gates_2847_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2847_first_finite_local_PPN_prediction_row_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_FINITE_LOCAL_PPN_DRY_RUN_2847_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    needles = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in needles if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2847_0_2846_doc", SRC_2846_DOC, "NEXT2846_0_2847;VAL2846_OVERALL", "2846 selected finite local PPN dry run"),
        ("SRC2847_1_2846_contract", SRC_2846_CONTRACT, "PPN2846_4_A_total;PPN2846_8_full_vector", "2846 finite local PPN input contract"),
        ("SRC2847_2_2846_formula", SRC_2846_FORMULA, "FORM2846_0_A_total;FORM2846_3_theorem_zero", "2846 local PPN formula pack"),
        ("SRC2847_3_2846_next", SRC_2846_NEXT, "NEXT2846_0_2847", "2846 handoff"),
        ("SRC2847_4_2846_validation", SRC_2846_VALIDATION, "VAL2846_OVERALL", "2846 validation"),
        ("SRC2847_5_2631", SRC_2631, "PPNV2631_8_total_abs;RG2631_0_no_gamma_only;PBOUND2631_0_gamma", "2631 full-vector/no-cancellation PPN gate"),
        ("SRC2847_6_1181", SRC_1181, "PPNV1181_0_gamma;PPNV1181_1_beta;PPNV1181_2_eta_Nordtvedt;G1181_2_preferred_frame_vector", "1181 comparator scaffold"),
        ("SRC2847_7_1883", SRC_1883, "DPB1883_0_CR_delta_p;DPB1883_1_QR_delta_p;DPB1883_2_gamma_combo", "delta_p/q_R_hat bridge and gamma combo"),
        ("SRC2847_8_local_bounds", SRC_LOCAL_BOUNDS, "Cassini_Shapiro_gamma_2003;Will_2014_PPN_beta_table;Will_2014_PPN_alpha1_table;LLR_Biskupek_Muller_Torre_2021", "local bound comparator table"),
    ]
    return [source_row(*spec) for spec in specs]


def bound_map_rows() -> list[dict[str, Any]]:
    specs = [
        ("BM2847_0_gamma", "gamma_minus_1", "2.3e-05", "Cassini_Shapiro_gamma_2003", "gamma_obs_minus_1=(delta_p+4*b_R*delta_p)/(1-2*b_R*delta_p)+Delta_gamma_tail+q_loc_gamma", "delta_p;q_R_hat;b_R;tail;q_loc_gamma;GM_convention", "PREDICTION_INPUTS_MISSING"),
        ("BM2847_1_beta", "beta_minus_1", "7.8e-05", "Will_2014_PPN_beta_table", "beta_MTS_minus_1=Delta_beta_total_abs with no-cancellation absolute components", "Delta_beta_source;operator;q_loc;boundary;readout;second_order_map", "PREDICTION_INPUTS_MISSING"),
        ("BM2847_2_eta", "eta_Nordtvedt", "4.5e-04", "1181_LLR_beta_eta", "eta_MTS=4*beta_MTS-gamma_MTS-3+nonmetric_source_flags", "gamma_MTS;beta_MTS;WEP/source coupling;q_loc", "PREDICTION_INPUTS_MISSING"),
        ("BM2847_3_alpha1", "alpha1", "1e-04", "Will_2014_PPN_alpha1_table", "alpha1_MTS=F_alpha1(d_R,frame_selection,q_loc_vector,domain_tail)", "d_R_response_matrix;frame_covariance;q_loc_vector", "PREFERRED_FRAME_INPUTS_MISSING"),
        ("BM2847_4_alpha2", "alpha2", "2e-09", "Will_2014_PPN_alpha2_table", "alpha2_MTS=F_alpha2(d_R,spin_precession_residual,domain_tail)", "d_R_response_matrix;spin_precession_projection;domain_tail", "PREFERRED_FRAME_INPUTS_MISSING"),
        ("BM2847_5_alpha3", "alpha3", "4e-20", "Will_2014_PPN_alpha3_table", "alpha3_MTS=F_alpha3(boundary_flux,source_current,momentum_nonconservation)", "boundary_flux;source_current_owner;momentum_flux_projection", "PREFERRED_FRAME_INPUTS_MISSING"),
        ("BM2847_6_xi", "xi", "4e-09", "Will_2014_PPN_xi_table", "xi_MTS=F_xi(domain_anisotropy,boundary_location_tail)", "domain_anisotropy;boundary_tail;projection_matrix", "PREFERRED_LOCATION_INPUTS_MISSING"),
        ("BM2847_7_Gdot", "Gdot_over_G", "9.6e-15 yr^-1", "LLR_Biskupek_Muller_Torre_2021", "Gdot_MTS/G=M_eff_dot/M_eff+readout_G_dot+source_charge_flux", "source_mass_conservation;readout_G;charge_flux", "SOURCE_NORMALIZATION_INPUTS_MISSING"),
        ("BM2847_8_clock", "alpha_clock_redshift", "2.48e-05", "Galileo_redshift_Delva_2018", "clock_MTS=F_clock(readout_frame,source_normalization,q_loc_time)", "clock_readout;frame_owner;q_loc_time", "CLOCK_READOUT_INPUTS_MISSING"),
        ("BM2847_9_total", "Delta_PPN_abs", "componentwise bounds", "2631_full_vector_rule", "Delta_PPN_abs=sum_abs(active_components) unless parent identity proves exact cancellation", "all channel values or theorem-zero certificates", "TOTAL_SCORE_BLOCKED"),
    ]
    return [
        nonclaim(
            {
                "bound_id": bound_id,
                "observable": observable,
                "comparator_bound": bound,
                "comparator_source": source,
                "mts_prediction_formula": formula,
                "required_inputs": required,
                "dry_run_status": status,
                "comparator_present": True,
                "mts_prediction_present": False,
                "control_only": True,
            }
        )
        for bound_id, observable, bound, source, formula, required, status in specs
    ]


def input_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATEIN2847_0_branch", "branch_selector", "parent theorem or finite branch must be explicit", "MISSING_BRANCH_CLOSURE"),
        ("GATEIN2847_1_A_total", "A_total", "requires Q_CAB, q_R_eff and sigma_R or parent theorem-zero", "MISSING_COMPUTABLE_INPUTS"),
        ("GATEIN2847_2_delta_p_qRhat", "delta_p/q_R_hat", "requires measured GM convention and finite charge/theorem-zero", "MISSING_GM_AND_CHARGE_INPUTS"),
        ("GATEIN2847_3_b_R", "b_R", "common-frame/no-shadow Weyl response must be zero or finite", "MISSING_B_R"),
        ("GATEIN2847_4_beta_vector", "Delta_beta_total_abs", "all second-order/source/readout beta pieces required", "MISSING_BETA_VECTOR"),
        ("GATEIN2847_5_preferred_frame", "d_R/alpha_i response", "disformal/vector/domain projection required", "MISSING_PREFERRED_FRAME_PROJECTION"),
        ("GATEIN2847_6_source_weight", "w_R/Delta_w", "source-current/no-prefactor theorem or finite source weights required", "MISSING_SOURCE_WEIGHT"),
        ("GATEIN2847_7_endpoint_readout", "endpoint/readout/GM tails", "boundary endpoint and measured-GM readout must be zero or finite", "MISSING_ENDPOINT_READOUT"),
        ("GATEIN2847_8_q_loc", "q_loc/Khat", "physical local residual projection needed through PPN order", "MISSING_QLOC_PROFILE"),
        ("GATEIN2847_9_sources", "source paths", "every finite/theorem input needs local path and anchor", "MISSING_SOURCE_PATHS"),
    ]
    return [
        nonclaim(
            {
                "input_gate_id": gate_id,
                "required_input": required,
                "why_needed": why,
                "gate_status": status,
                "gate_passed": False,
                "control_only": True,
            }
        )
        for gate_id, required, why, status in specs
    ]


def score_rule_rows() -> list[dict[str, Any]]:
    specs = [
        ("RULE2847_0_comparator_not_claim", "A sourced comparator row alone never counts as an MTS pass.", "ACTIVE"),
        ("RULE2847_1_no_gamma_only", "A small gamma/delta_p lane cannot pass while beta, preferred-frame, source, endpoint, readout or q_loc channels remain live.", "ACTIVE"),
        ("RULE2847_2_no_cancellation", "Use componentwise absolute envelopes unless a parent identity proves exact cancellation.", "ACTIVE"),
        ("RULE2847_3_theorem_zero", "A theorem-zero row is accepted only with parent-signed source/action path and no placeholder clauses.", "ACTIVE"),
        ("RULE2847_4_finite_input", "A finite prediction row is accepted only with numeric value, units, source path, source anchor, and projection map.", "ACTIVE"),
        ("RULE2847_5_total_vector", "Local GR/Newton reduction requires all local PPN/vector gates closed, not only the R_AB/gamma branch.", "ACTIVE"),
    ]
    return [
        nonclaim(
            {
                "rule_id": rule_id,
                "rule": rule,
                "status": status,
                "control_only": True,
            }
        )
        for rule_id, rule, status in specs
    ]


def dry_result_rows() -> list[dict[str, Any]]:
    specs = [
        ("DRY2847_0_schema", "bound-map schema", "PASS_SCHEMA_ONLY", "comparator rows and prediction slots are present"),
        ("DRY2847_1_predictions", "MTS finite prediction rows", "FAIL_MISSING_INPUTS", "A_total, delta_p/q_R_hat, b_R, beta vector, preferred-frame, endpoint/readout and q_loc inputs are missing"),
        ("DRY2847_2_scoring", "numeric score", "NOT_RUN", "dry run refuses scoring while prediction rows are missing"),
        ("DRY2847_3_claim", "local GR/Newton/PPN claim", "BLOCKED", "full-vector gates are open and parent owner theorem is not signed"),
        ("DRY2847_4_next", "first finite/theorem row target", "SELECTED", "next step should fill the first real A_total/delta_p/q_R_hat row or parent theorem-zero certificate"),
    ]
    return [
        nonclaim(
            {
                "dry_run_id": dry_id,
                "object": obj,
                "result": result,
                "reason": reason,
                "control_only": True,
            }
        )
        for dry_id, obj, result, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2847_0_bound_map", "bound map created", "PASS_CONTROL_ONLY", "schema exists but no score"),
        ("CG2847_1_prediction_rows", "MTS prediction rows source-ready", "BLOCKED", "finite/theorem inputs missing"),
        ("CG2847_2_full_vector", "full PPN residual vector source-ready", "BLOCKED", "many vector components open"),
        ("CG2847_3_local_GR", "local GR/Newton reduction", "BLOCKED", "cannot follow from dry-run schema"),
        ("CG2847_4_public_claim", "public/local claim", "BLOCKED", "private nonclaim checkpoint only"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "gate_passed": False,
                "control_check_passed": status == "PASS_CONTROL_ONLY",
                "control_only": True,
            }
        )
        for gate_id, claim, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2847_0_dry_run", "The local PPN dry-run map is ready but not score-ready.", "SCHEMA_READY_NONCLAIM", "comparators and prediction slots exist, but MTS predictions are missing"),
        ("DEC2847_1_testing_path", "Testing can begin only after the first theorem-zero or finite A_total/delta_p/q_R_hat row exists.", "SELECTED", "otherwise the runner only tests missing data"),
        ("DEC2847_2_no_gamma_only", "Gamma-only local victory remains forbidden.", "LOCKED", "2631 full-vector/no-cancellation guard is carried forward"),
        ("DEC2847_3_no_claim", "No local-GR/Newton/PPN claim.", "LOCKED", "dry-run schema is not evidence"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "control_only": True,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2847_0_2848",
                "status": "selected_primary",
                "target_doc": "2848-Y5-R2FR-first-finite-local-PPN-prediction-row-or-parent-theorem-zero-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_finite_local_PPN_prediction_row_or_parent_theorem_zero_under_AX1090_2848.py",
                "mission": "try to fill the first real source-backed A_total/delta_p/q_R_hat prediction row or a parent theorem-zero certificate; otherwise keep the PPN dry-run blocked",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("COPY2847_0_bound_map", OUTPUTS["bound_map"], BRANCH_OUTPUTS["bound_map_copy"], "portable dry-run local PPN bound map"),
        ("COPY2847_1_input_gates", OUTPUTS["input_gates"], BRANCH_OUTPUTS["input_gates_copy"], "portable prediction input gate list"),
        ("COPY2847_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue handoff"),
        ("COPY2847_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable decision ledger"),
    ]
    rows = []
    for copy_id, src, dst, purpose in copies:
        shutil.copyfile(src, dst)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(src),
                    "copy_path": str(dst),
                    "purpose": purpose,
                    "exists": dst.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "copy_path", "source_table"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if isinstance(value, str) and value:
                    path = Path(value)
                    if path.is_absolute():
                        paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_ready",
        "gate_passed",
        "mts_prediction_present",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if key in row and row[key] is True:
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {"numeric_prediction", "prediction_value", "mts_prediction_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key in numeric_keys:
                value = row.get(key)
                if value not in (None, "", "MISSING"):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2847_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2847_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2847_2_bound_map_channels", len(rows_by_name["bound_map"]) >= 10, "dry-run bound map has gamma/beta/eta/preferred-frame/clock/total channels"),
        ("VAL2847_3_predictions_missing", not any(row["mts_prediction_present"] for row in rows_by_name["bound_map"]), "MTS numeric prediction rows remain missing"),
        ("VAL2847_4_input_gates_blocked", not any(row["gate_passed"] for row in rows_by_name["input_gates"]), "prediction input gates remain blocked"),
        ("VAL2847_5_no_cancellation_rules", any(row["rule_id"] == "RULE2847_2_no_cancellation" for row in rows_by_name["score_rules"]), "no-cancellation scoring rule recorded"),
        ("VAL2847_6_dry_run_no_score", any(row["dry_run_id"] == "DRY2847_2_scoring" and row["result"] == "NOT_RUN" for row in rows_by_name["dry_results"]), "dry run refuses numeric scoring"),
        ("VAL2847_7_next_target_2848", any(row["next_id"] == "NEXT2847_0_2848" and row["selected"] for row in rows_by_name["next"]), "2848 first finite prediction/theorem-zero target selected"),
        ("VAL2847_8_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2847_9_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2847_10_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2847_11_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2847_12_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2847_13_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no MTS numeric prediction rows inserted"),
        ("VAL2847_14_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2847_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2847_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {"validation_id": validation_id, "passed": passed, "detail": detail, "timestamp_utc": ts()}
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2847_OVERALL",
            "passed": overall,
            "detail": "2847 builds a nonclaim local PPN dry-run bound map with comparator rows, blocks scoring because MTS prediction inputs are missing, and selects the first finite prediction/theorem-zero row as next target.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2847 - Y5 R2FR Finite Local PPN Bound Map Dry Run Or Current Owner Retry Under AX1090

Status: `Y5_R2FR_2847_local_PPN_bound_map_schema_ready_predictions_missing_nonclaim`

## Private Verdict

2847 moves the local branch from pure derivation audit into a testable dry-run shape.

The useful result: the local PPN comparator map is now explicit enough to run once real MTS prediction inputs exist. It carries gamma, beta, Nordtvedt eta, preferred-frame/location, Gdot, clock, and total no-cancellation channels.

The hard blocker: this is still **not a score**. Every MTS prediction lane is missing at least one theorem-zero certificate or finite source-backed input. The dry-run therefore refuses local-GR/PPN scoring.

The key formula lane remains:

```text
A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi)
delta_p_const=c^2*A_total/(2 G M_source)
q_R_hat_const=-c^2*A_total/(G M_source)
```

Next target: fill the first real `A_total/delta_p/q_R_hat` prediction row or a parent theorem-zero certificate. Until then, the comparator bounds are useful scaffolding, not evidence.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Dry-Run Bound Map

{markdown_table(rows["bound_map"], ["bound_id", "observable", "comparator_bound", "comparator_source", "dry_run_status", "mts_prediction_present", "valid_for_claim"])}

## Prediction Input Gates

{markdown_table(rows["input_gates"], ["input_gate_id", "required_input", "gate_status", "why_needed", "gate_passed", "valid_for_claim"])}

## No-Cancellation Score Rules

{markdown_table(rows["score_rules"], ["rule_id", "rule", "status", "valid_for_claim"])}

## Dry-Run Results

{markdown_table(rows["dry_results"], ["dry_run_id", "object", "result", "reason", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["claim_gates"], ["claim_gate_id", "claim", "status", "reason", "gate_passed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["bound_map"] = bound_map_rows()
    rows["input_gates"] = input_gate_rows()
    rows["score_rules"] = score_rule_rows()
    rows["dry_results"] = dry_result_rows()
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "bound_map", "input_gates", "score_rules", "dry_results", "claim_gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2847_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2847_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
