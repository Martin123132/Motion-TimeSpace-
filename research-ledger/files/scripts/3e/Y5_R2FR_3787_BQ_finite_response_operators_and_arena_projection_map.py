import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3787"
BRANCH = "MTS_R2FR_Y5_BQ_FINITE_RESPONSE_OPERATORS_AND_ARENA_PROJECTION_MAP_3787"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3787-Y5-R2FR-BQ-finite-response-operators-and-arena-projection-map.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3787_SOURCE_REGISTER.csv",
    "response": RESIDUALS / "P8_Y5_R2FR_3787_BQ_RESPONSE_OPERATOR_MAP.csv",
    "arenas": RESIDUALS / "P8_Y5_R2FR_3787_ARENA_PROJECTION_MAP.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_3787_NO_CANCELLATION_ENVELOPE.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_3787_COEFFICIENT_ACQUISITION_LEDGER.csv",
    "runner_schema": RESIDUALS / "P8_Y5_R2FR_3787_FINITE_RUNNER_SCHEMA.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3787_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3787_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3787_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3787_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3787_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md",
    PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    PCW / "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md",
    PCW / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
    PCW / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
    PCW / "1202-Y5-R10-conservative-geometry-kernel-or-qDT-profile-family.md",
    PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_path": str(path),
            "exists": path.exists(),
            "source_role": "BQ_response_projection_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def response_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "response_id": "RSP3787_0_RA_norm",
            "observable_response": "R_A",
            "formula": "||R_A|| <= C_owner epsilon_BQ_owner + C_chart epsilon_BQ_chart + C_descent epsilon_BQ_descent + C_q |beta_q,A| ||A_obs||",
            "feeds": "A_basicness;charged_matter_phase;Wilson_local_patch",
            "missing_inputs": "C_owner;C_chart;C_descent;C_q;A_obs_norm;local_patch_norm",
            "status": "SYMBOLIC_RESPONSE_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "response_id": "RSP3787_1_dRA_norm",
            "observable_response": "dR_A",
            "formula": "||dR_A|| <= C_rank epsilon_BQ_rank + C_descent_d epsilon_BQ_descent + C_node epsilon_node",
            "feeds": "F_basicness;Maxwell_stress;PPN_gamma_beta;EM_tail",
            "missing_inputs": "C_rank;C_descent_d;C_node;differential_norm;rank_projection",
            "status": "SYMBOLIC_RESPONSE_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "response_id": "RSP3787_2_action_leak",
            "observable_response": "delta_A S_EM",
            "formula": "|delta_A S_EM| <= C_Z |beta_Z,A| + C_dR ||dR_A|| + C_JR ||J_Q|| ||R_A|| + C_lambda |lambda_A|",
            "feeds": "WEP;source_conservation;clock_alpha;Gdot",
            "missing_inputs": "C_Z;C_dR;C_JR;C_lambda;J_Q_norm;field_energy_norm",
            "status": "SYMBOLIC_RESPONSE_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "response_id": "RSP3787_3_alpha_source",
            "observable_response": "alpha_and_source_leakage",
            "formula": "epsilon_alpha_source <= |beta_Z,A| + |beta_q,A| + |lambda_A| + epsilon_J_Q + epsilon_BQ_norm",
            "feeds": "alpha_EM;R10;clock;WEP;source_coupling",
            "missing_inputs": "beta_Z,A;beta_q,A;lambda_A;epsilon_J_Q;epsilon_BQ_norm",
            "status": "SYMBOLIC_RESPONSE_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "response_id": "RSP3787_4_total_BQ",
            "observable_response": "epsilon_BQ_total_abs",
            "formula": "epsilon_BQ_total_abs=|epsilon_BQ_owner|+|epsilon_BQ_rank|+|epsilon_BQ_chart|+|epsilon_BQ_descent|+|epsilon_BQ_norm|",
            "feeds": "no_cancellation_parent_branch_gate",
            "missing_inputs": "component_values_or_zero_theorems",
            "status": "OFFICIAL_ABS_SUM_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def arena_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_0_PPN_gamma",
            "arena": "PPN_gamma",
            "bound_or_envelope": "2.3e-5",
            "projection_formula": "delta_gamma_EM <= G_gamma_R ||R_A|| + G_gamma_dR ||dR_A|| + G_gamma_Z |beta_Z,A| + G_gamma_shadow epsilon_shadow_EM",
            "required_inputs": "G_gamma_R;G_gamma_dR;G_gamma_Z;epsilon_shadow_EM;response_norms",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_1_PPN_beta",
            "arena": "PPN_beta",
            "bound_or_envelope": "7.8e-5",
            "projection_formula": "delta_beta_EM <= G_beta_R ||R_A|| + G_beta_dR ||dR_A|| + G_beta_src epsilon_alpha_source + G_beta_nl epsilon_BQ_rank",
            "required_inputs": "G_beta_R;G_beta_dR;G_beta_src;G_beta_nl",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_2_WEP",
            "arena": "WEP_eta",
            "bound_or_envelope": "2.8e-15",
            "projection_formula": "eta_EM_AB <= G_eta_R Delta_AB||R_A|| + G_eta_Z Delta_AB|beta_Z,A| + G_eta_J Delta_AB epsilon_J_Q + G_eta_BQ Delta_AB epsilon_BQ_norm",
            "required_inputs": "composition_sensitivities;G_eta_R;G_eta_Z;G_eta_J;G_eta_BQ",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_3_Gdot",
            "arena": "Gdot_or_source_rate",
            "bound_or_envelope": "9.6e-15 yr^-1",
            "projection_formula": "|d ln G_eff/dt|_EM <= |dt beta_Z|+|dt beta_q|+|dt epsilon_BQ_descent|+|dt epsilon_J_Q|+source_exchange_rate",
            "required_inputs": "time_derivative_model;source_exchange_rate;clock_units",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_4_R10",
            "arena": "R10_short_range_alpha_lambda",
            "bound_or_envelope": "R10_alpha_lambda_bound_curve_or_anchor",
            "projection_formula": "alpha_pred(lambda)_BQ <= G_R10(lambda)[epsilon_BQ_total_abs + epsilon_alpha_source + epsilon_node]",
            "required_inputs": "G_R10(lambda);lambda_map;source_density_projection;real_bound_curve",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_5_clocks",
            "arena": "clock_alpha_product",
            "bound_or_envelope": "clock_pair_product_bounds",
            "projection_formula": "|d ln nu_i/dt - d ln nu_j/dt|_BQ <= K_alpha_ij |dt epsilon_alpha_source| + K_BQ_ij |dt epsilon_BQ_norm|",
            "required_inputs": "clock_sensitivity_pair;time_derivative_map;readout_model",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "arena_id": "ARENA3787_6_orbital",
            "arena": "orbital_GM_and_range",
            "bound_or_envelope": "arena_specific_ephemeris_or_orbital_bounds",
            "projection_formula": "delta_mu_orbit_BQ <= G_orbit_R ||R_A|| + G_orbit_tail epsilon_BQ_total_abs + G_orbit_source epsilon_J_Q",
            "required_inputs": "orbit_source_projection;M_H_ref;no_orbital_GM_import_guard",
            "score_status": "NOT_SCORE_READY",
            "valid_for_claim": False,
        },
    ]


def envelope_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "envelope_id": "ENV3787_0_no_cancellation",
            "rule": "All B_Q residual components enter with absolute values unless a parent theorem signs a protected cancellation.",
            "formula": "E_BQ_abs=sum_i |epsilon_i|",
            "claim_status": "ACTIVE_GUARD",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "envelope_id": "ENV3787_1_zero_or_bound",
            "rule": "A component may be removed only by a zero theorem with source path, or by a numeric/source-backed bound with units and arena projection.",
            "formula": "component_status in {THEOREM_ZERO, SOURCE_BOUND}; otherwise MISSING_COMPONENT_INPUT",
            "claim_status": "ACTIVE_GUARD",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "envelope_id": "ENV3787_2_no_fit_backfill",
            "rule": "Do not infer B_Q coefficients from successful local-GR/EM tests; coefficients must come before comparison.",
            "formula": "projection_coeff_source != fitted_to_target_observable",
            "claim_status": "ACTIVE_GUARD",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "envelope_id": "ENV3787_3_claim_block",
            "rule": "No local-GR/EM claim if any official residual component or arena projection coefficient is missing.",
            "formula": "claim_allowed=false unless all component_values and all G_arena coefficients are source-backed or theorem-zero",
            "claim_status": "ACTIVE_GUARD",
            "valid_for_claim": False,
        },
    ]


def acquisition_rows(timestamp):
    required = [
        ("ACQ3787_0_C_owner", "C_owner", "response coefficient from multiplet-owner failure to R_A norm", "MISSING_SOURCE_OR_THEOREM", "R_A;local_GR"),
        ("ACQ3787_1_C_rank", "C_rank", "rank-loss coefficient from epsilon_BQ_rank to dR_A/EM stress", "MISSING_SOURCE_OR_THEOREM", "PPN;EM_stress"),
        ("ACQ3787_2_C_chart", "C_chart", "bundle chart/Wilson leakage coefficient into R_A", "MISSING_SOURCE_OR_THEOREM", "Wilson;defects"),
        ("ACQ3787_3_C_descent", "C_descent,C_descent_d", "q_obs descent leakage coefficients into R_A and dR_A", "MISSING_SOURCE_OR_THEOREM", "local_GR;PPN"),
        ("ACQ3787_4_alpha", "beta_Z,A,beta_q,A,lambda_A,epsilon_J_Q", "alpha/source/current normalization values or zero theorems", "MISSING_SOURCE_OR_THEOREM", "alpha;WEP;R10;clocks"),
        ("ACQ3787_5_G_arena", "G_gamma,G_beta,G_eta,G_R10,G_clock,G_orbit", "arena projection coefficients", "MISSING_SOURCE_OR_THEOREM", "PPN;WEP;R10;clocks;orbital"),
        ("ACQ3787_6_norms", "A_obs_norm,J_Q_norm,field_energy_norm", "local field/source norm convention and units", "MISSING_SOURCE_OR_THEOREM", "all_arenas"),
        ("ACQ3787_7_bounds", "real bound curves/envelopes", "source-backed external comparison curves and uncertainty policy", "MISSING_OR_PARTIAL_SOURCE", "R10;clocks;orbital"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "acquisition_id": acq_id,
            "symbol": symbol,
            "needed_evidence": evidence,
            "current_status": status,
            "arena": arena,
            "valid_for_claim": False,
        }
        for acq_id, symbol, evidence, status, arena in required
    ]


def runner_schema_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "field": "branch_id",
            "required": True,
            "description": "finite B_Q branch identifier",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "field": "component_symbol",
            "required": True,
            "description": "epsilon_BQ_owner/rank/chart/descent/norm or linked alpha/current residual",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "field": "component_value",
            "required": True,
            "description": "numeric value or THEOREM_ZERO; MISSING blocks claim",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "field": "units",
            "required": True,
            "description": "dimensionless, normed field unit, yr^-1, or arena-normalized units",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "field": "source_path_or_url",
            "required": True,
            "description": "local theorem path, source-backed data path, DOI, or URL",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "field": "projection_coefficient",
            "required": True,
            "description": "arena response coefficient with source or theorem",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "field": "no_cancellation_policy",
            "required": True,
            "description": "absolute_sum unless protected cancellation theorem is cited",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3787_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3787_1_response_map",
            "pass": True,
            "claim_allowed": False,
            "details": "symbolic response operator map emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3787_2_arena_map",
            "pass": True,
            "claim_allowed": False,
            "details": "arena projection formulas emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3787_3_numeric_score_ready",
            "pass": False,
            "claim_allowed": False,
            "details": "component values and projection coefficients remain missing",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3787_4_no_cancellation",
            "pass": True,
            "claim_allowed": False,
            "details": "absolute-sum no-cancellation envelope emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3787_5_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "not claimable until response coefficients and component bounds are source-backed or theorem-zero",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3787_0_progress",
            "decision": "The finite B_Q branch is now response-operator shaped.",
            "action": "Use it as the official nonclaim bridge from B_Q residuals to local EM/GR observables.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3787_1_not_score_ready",
            "decision": "No numerical arena score is allowed yet.",
            "action": "Acquire or derive component values, norm conventions, and projection coefficients first.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3787_2_next",
            "decision": "Next target should fill the first coefficient/source pack, not rerun symbolic mapping.",
            "action": "Start with R_A/dR_A coefficients because they feed PPN and EM stress most directly.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3788-Y5-R2FR-BQ-first-coefficient-source-pack-RA-dRA.md",
            "target_script": "scripts/Y5_R2FR_3788_BQ_first_coefficient_source_pack_RA_dRA.py",
            "objective": "Acquire or derive the first source-backed coefficients and norm conventions for C_owner, C_rank, C_chart, C_descent, A_obs_norm, and dR_A projection; keep all rows nonclaim until numeric/source-backed.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "BQ_FINITE_RESPONSE_OPERATOR_MAP_EMITTED_NOT_SCORE_READY",
            "plain_verdict": "3787 turns the official B_Q finite residual vector into a response-operator map for R_A, dR_A, EM action leakage, alpha/source leakage, and PPN/WEP/R10/clock/orbital arenas. It remains nonclaim because component values, norm conventions, and projection coefficients are not source-backed yet.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3787 markdown document written"),
        (
            "response_map",
            len(grouped["response"]) >= 5,
            "response operator rows emitted",
        ),
        (
            "arena_map",
            len(grouped["arenas"]) >= 7,
            "PPN/WEP/R10/clock/orbital arena rows emitted",
        ),
        (
            "no_cancellation",
            any(row["envelope_id"] == "ENV3787_0_no_cancellation" for row in grouped["envelope"]),
            "absolute-sum no-cancellation guard emitted",
        ),
        (
            "acquisition",
            len(grouped["acquisition"]) >= 8,
            "coefficient acquisition ledger emitted",
        ),
        (
            "runner_schema",
            len(grouped["runner_schema"]) >= 7,
            "finite runner schema emitted",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3787_5_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "EM/local-GR claim gate remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3788-"),
            "3788 coefficient source-pack target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3787 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3787 - B_Q Finite Response Operators and Arena Projection Map",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3787 makes the finite fallback useful. The official `B_Q` residuals now feed explicit response operators for `R_A`, `dR_A`, Maxwell action leakage, alpha/source leakage, and the main test arenas. This is not a numerical pass: the component values, norm conventions, and arena projection coefficients are still missing. But the branch is now score-shaped rather than vague.",
        "",
        render_section("B_Q Response Operator Map", grouped["response"], ["response_id", "observable_response"]),
        render_section("Arena Projection Map", grouped["arenas"], ["arena_id", "arena"]),
        render_section("No-Cancellation Envelope", grouped["envelope"], ["envelope_id"]),
        render_section("Coefficient Acquisition Ledger", grouped["acquisition"], ["acquisition_id", "symbol"]),
        render_section("Finite Runner Schema", grouped["runner_schema"], ["field"]),
        render_section("Claim Gates", grouped["claim_gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "response": response_rows(timestamp),
        "arenas": arena_rows(timestamp),
        "envelope": envelope_rows(timestamp),
        "acquisition": acquisition_rows(timestamp),
        "runner_schema": runner_schema_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["response"], grouped["response"])
    write_csv(OUTPUTS["arenas"], grouped["arenas"])
    write_csv(OUTPUTS["envelope"], grouped["envelope"])
    write_csv(OUTPUTS["acquisition"], grouped["acquisition"])
    write_csv(OUTPUTS["runner_schema"], grouped["runner_schema"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3787 validation failed: {failures}")
    print("wrote 3787 checkpoint: B_Q finite response operator map emitted")


if __name__ == "__main__":
    main()
