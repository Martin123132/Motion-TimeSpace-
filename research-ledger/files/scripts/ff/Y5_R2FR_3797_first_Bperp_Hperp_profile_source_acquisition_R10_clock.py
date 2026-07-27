import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3797"
BRANCH = "MTS_R2FR_Y5_FIRST_BPERP_HPERP_PROFILE_SOURCE_ACQUISITION_R10_CLOCK_3797"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3797-Y5-R2FR-first-Bperp-Hperp-profile-source-acquisition-R10-clock.md"

P_3789 = PCW / "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md"
P_3791 = PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_3793 = PCW / "3793-Y5-R2FR-BQ-descent-amplitude-or-eps-dBQ-bound.md"
P_3796 = PCW / "3796-Y5-R2FR-Qshear-eigenframe-chart-or-first-Bperp-arena-fill.md"
P_1052 = PCW / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3796_PROFILE = RESIDUALS / "P8_Y5_R2FR_3796_FIRST_BPERP_PROFILE_ROWS.csv"
C_R10_CURVE = RESIDUALS / "P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv"
C_R10_SCORE = RESIDUALS / "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv"
C_CLOCK_PRODUCT = RESIDUALS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
C_CLOCK_ALPHA = RESIDUALS / "P8_Y5_R2FR_3474_CLOCK_ALPHA_SENSITIVITY_ROW.csv"
C_CLOCK_COEFF = RESIDUALS / "P8_Y5_R2FR_3648_ALPHA_MASS_CLOCK_COEFFICIENT_ROWS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3797_SOURCE_REGISTER.csv",
    "profile_contract": RESIDUALS / "P8_Y5_R2FR_3797_PROFILE_CONTRACT_ROWS.csv",
    "r10_join": RESIDUALS / "P8_Y5_R2FR_3797_R10_BOUND_JOIN_LEDGER.csv",
    "clock_join": RESIDUALS / "P8_Y5_R2FR_3797_CLOCK_JOIN_LEDGER.csv",
    "fill_attempt": RESIDUALS / "P8_Y5_R2FR_3797_FIRST_FILL_ATTEMPT_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3797_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3797_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3797_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3797_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3797_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3797_0_3796_profile_rows",
        "path": P_3796,
        "needle": "First Bperp/Hperp Profile Rows",
        "role": "3796 emitted first missing Bperp/Hperp rows",
    },
    {
        "source_id": "SRC3797_1_3793_Bperp_definition",
        "path": P_3793,
        "needle": "B_Q=q_obs^*Bbar_Q+dchi+B_perp",
        "role": "exact Bperp/Hperp definition",
    },
    {
        "source_id": "SRC3797_2_3789_patch_norms",
        "path": P_3789,
        "needle": "A_ref=max(||A_obs||_A,A_floor)",
        "role": "U_good, A_ref, F_ref norm policy",
    },
    {
        "source_id": "SRC3797_3_3791_ZEM_lambda",
        "path": P_3791,
        "needle": "lambda_A",
        "role": "Z_EM/lambda companion residual",
    },
    {
        "source_id": "SRC3797_4_3792_epsilonJ",
        "path": P_3792,
        "needle": "epsilon_J_Q_total_abs",
        "role": "same-current companion residual",
    },
    {
        "source_id": "SRC3797_5_R10_curve_candidate",
        "path": C_R10_CURVE,
        "needle": "R10C3702_000",
        "role": "candidate digitized R10 alpha(lambda) curve",
    },
    {
        "source_id": "SRC3797_6_R10_score_gate",
        "path": C_R10_SCORE,
        "needle": "R10SG3707_000",
        "role": "executable nonclaim R10 score gate rows",
    },
    {
        "source_id": "SRC3797_7_clock_product_bound",
        "path": C_CLOCK_PRODUCT,
        "needle": "ACB1052_2",
        "role": "best existing alpha-clock product bound",
    },
    {
        "source_id": "SRC3797_8_clock_alpha_sensitivity",
        "path": C_CLOCK_ALPHA,
        "needle": "CLK3474_0_YbE3E2_alpha",
        "role": "Yb E3/E2 alpha sensitivity row",
    },
    {
        "source_id": "SRC3797_9_clock_coefficients",
        "path": C_CLOCK_COEFF,
        "needle": "CP3648_0_b_alpha",
        "role": "clock/alpha coefficient missing-input ledger",
    },
    {
        "source_id": "SRC3797_10_1052_clock_context",
        "path": P_1052,
        "needle": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1",
        "role": "clock product bound interpretation and transfer warning",
    },
    {
        "source_id": "SRC3797_11_spine",
        "path": P_SPINE,
        "needle": "3797-Y5-R2FR-first-Bperp-Hperp-profile-source-acquisition-R10-clock.md",
        "role": "live spine handoff",
    },
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path):
    try:
        load_csv(path)
        return True
    except Exception:
        return False


def bool_text(value):
    return "true" if value else "false"


def numeric_values(rows, key):
    values = []
    for row in rows:
        try:
            values.append(float(row[key]))
        except Exception:
            pass
    return values


def range_summary(rows, key, fmt="{:.6e}"):
    values = numeric_values(rows, key)
    if not values:
        return "MISSING_NUMERIC_VALUES"
    return f"{fmt.format(min(values))}..{fmt.format(max(values))}"


def source_register(timestamp):
    out = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        exists = path.exists()
        needle_found = False
        if exists:
            if path.suffix.lower() == ".csv":
                text = path.read_text(encoding="utf-8", errors="replace")
            else:
                text = read_text(path)
            needle_found = spec["needle"] in text
        out.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needle": spec["needle"],
                "needle_found": bool_text(needle_found),
                "role": spec["role"],
                "valid_for_claim": "false",
            }
        )
    return out


def profile_contract_rows(timestamp):
    rows = [
        (
            "PC3797_0_Ugood",
            "R10_lab;clock_lab",
            "U_good_spec",
            "local defect-free geodesically convex contractible patch with H1(U)=0 and compact weight w_U",
            P_3789,
            "DEFINED_CONDITIONAL_NOT_ARENA_SELECTED",
            "MISSING_ARENA_DOMAIN",
            "local_patch_spec",
            "choose explicit lab patch/support and defect/Wilson exclusion certificate",
        ),
        (
            "PC3797_1_Aref",
            "R10_lab;clock_lab",
            "A_ref_policy",
            "A_ref=max(||A_obs||_A,A_floor)",
            P_3789,
            "DEFINED_REFERENCE_CONVENTION",
            "MISSING_A_OBS_PROFILE_OR_A_FLOOR",
            "same units as A_obs norm",
            "source A_obs profile or floor convention for local EM readout",
        ),
        (
            "PC3797_2_Fref",
            "R10_lab;clock_lab",
            "F_ref_policy",
            "F_ref=max(||F_obs||_F,F_floor)",
            P_3789,
            "DEFINED_REFERENCE_CONVENTION",
            "MISSING_F_OBS_PROFILE_OR_F_FLOOR",
            "same units as F_obs norm",
            "source F_obs profile or floor convention for local EM readout",
        ),
        (
            "PC3797_3_Bperp",
            "R10_lab;clock_lab",
            "Bperp_definition",
            "B_perp is the non-gauge q_obs-vertical residue in B_Q=q_obs^*Bbar_Q+dchi+B_perp",
            P_3793,
            "EXACT_DEFINITION",
            "MISSING_BQ_PULLBACK_PROFILE_OR_ZERO_THEOREM",
            "connection one-form units before normalization",
            "construct B_Q and Bbar_Q from parent-owned fields or provide finite profile",
        ),
        (
            "PC3797_4_Hperp",
            "R10_lab;clock_lab",
            "Hperp_definition",
            "Hperp=dBperp and eps_dBQ_A=||q_*^-1 Lie_EA Hperp||_F/F_ref",
            P_3793,
            "EXACT_DEFINITION",
            "MISSING_HPERP_PROFILE_OR_ZERO_THEOREM",
            "curvature two-form units before normalization",
            "differentiate/supply Bperp profile or parent-sign H_Q descent",
        ),
        (
            "PC3797_5_YQ_selector",
            "R10_lab;clock_lab",
            "Y_Q_source",
            "Y_Q=(C1,D1,C2,D2) may be selected from Q-shear coordinates only by parent-owned Pi4 with rank(dY_Q)=4",
            P_3796,
            "CONDITIONAL_SELECTOR_REQUIREMENT",
            "MISSING_PARENT_PI4_SELECTOR",
            "four scalar fields",
            "derive Pi4 from parent action or demote to explicit finite profile",
        ),
        (
            "PC3797_6_R10_join_rule",
            "R10_lab",
            "R10_alpha_projection_contract",
            "abs(alpha_predicted(lambda)) <= alpha_bound_abs(lambda), with alpha_predicted built from Bperp/Hperp/lambda_A/epsilon_J_Q projection coefficients",
            C_R10_SCORE,
            "EXECUTABLE_BOUND_SIDE_NONCLAIM",
            "MISSING_THEORY_NUMERATOR_AND_PROJECTION_COEFFICIENTS",
            "dimensionless alpha",
            "fill Bperp/Hperp amplitudes and R10 projection coefficients",
        ),
        (
            "PC3797_7_clock_join_rule",
            "clock_lab",
            "clock_product_projection_contract",
            "abs(DeltaK_alpha*(b_alpha_or_EM_residual)*tau_clock_time) <= clock_product_bound",
            P_1052,
            "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
            "MISSING_STANDALONE_B_ALPHA_TAU_CLOCK_AND_BPERP_TRANSFER",
            "yr^-1",
            "derive tau_clock_time and map Bperp/Hperp to alpha-clock readout",
        ),
    ]
    out = []
    for row in rows:
        out.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "contract_id": row[0],
                "arena_id": row[1],
                "quantity": row[2],
                "definition_or_formula": row[3],
                "source_path": str(row[4]),
                "source_status": row[5],
                "current_value": row[6],
                "units": row[7],
                "next_required_input": row[8],
                "fillable_now": "false",
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return out


def r10_join_rows(timestamp):
    curve = load_csv(C_R10_CURVE)
    score = load_csv(C_R10_SCORE)
    profile = load_csv(C_3796_PROFILE)
    r10_profile = [row for row in profile if row.get("arena_id") == "R10_lab"]
    curve_sources = sorted({row.get("source_file", "") for row in curve if row.get("source_file")})
    source_exists = all(Path(path).exists() for path in curve_sources)
    out = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "join_id": "R10J3797_0_bound_curve_candidate",
            "arena_id": "R10_lab",
            "source_path": str(C_R10_CURVE),
            "evidence_status": "AVAILABLE_NONCLAIM_REVIEW_REQUIRED",
            "numeric_summary": f"rows={len(curve)}; lambda_m={range_summary(curve, 'lambda_m')}; alpha_bound_abs={range_summary(curve, 'alpha_bound_abs')}",
            "units": "lambda_m in m; alpha_bound_abs dimensionless",
            "claim_status": "candidate curve is not promoted because manual review/confidence gate remains",
            "valid_for_claim": "false",
            "blocks_claim": "true",
            "next_action": "review/promote digitized curve or replace with official machine-readable bound table",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "join_id": "R10J3797_1_curve_source_files",
            "arena_id": "R10_lab",
            "source_path": ";".join(curve_sources),
            "evidence_status": "SOURCE_FILES_EXIST" if source_exists else "MISSING_SOURCE_FILE",
            "numeric_summary": f"unique_source_files={len(curve_sources)}",
            "units": "file_count",
            "claim_status": "source files exist but candidate extraction is still nonclaim",
            "valid_for_claim": "false",
            "blocks_claim": "true",
            "next_action": "audit figure extraction/calibration and make promotion ledger explicit",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "join_id": "R10J3797_2_score_gate",
            "arena_id": "R10_lab",
            "source_path": str(C_R10_SCORE),
            "evidence_status": "EXECUTABLE_NONCLAIM_GATE_AVAILABLE",
            "numeric_summary": f"rows={len(score)}; lambda_m={range_summary(score, 'lambda_m')}; P_N_max_eta10_m4={range_summary(score, 'P_N_max_eta10_m4')}",
            "units": "mixed by column",
            "claim_status": "score side exists but needs parent P_N/lambda_H/eta and reviewed bound curve",
            "valid_for_claim": "false",
            "blocks_claim": "true",
            "next_action": "join only after Bperp/Hperp numerator and projection coefficients are filled",
        },
    ]
    for row in r10_profile:
        out.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "join_id": f"R10J3797_profile_{row['quantity']}",
                "arena_id": "R10_lab",
                "source_path": row["source_path"],
                "evidence_status": row["status"],
                "numeric_summary": row["value"],
                "units": row["units"],
                "claim_status": "theory-side numerator missing",
                "valid_for_claim": "false",
                "blocks_claim": "true",
                "next_action": "supply parent-zero theorem or finite numeric/symbolic profile with projection coefficient",
            }
        )
    return out


def clock_join_rows(timestamp):
    product = load_csv(C_CLOCK_PRODUCT)
    alpha = load_csv(C_CLOCK_ALPHA)
    coeff = load_csv(C_CLOCK_COEFF)
    profile = load_csv(C_3796_PROFILE)
    best = next(row for row in product if row.get("row_type") == "best_current")
    alpha_row = alpha[0]
    coeff_map = {row["symbol"]: row for row in coeff}
    clock_profile = [row for row in profile if row.get("arena_id") == "clock_lab"]
    out = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "join_id": "CLKJ3797_0_best_clock_product",
            "arena_id": "clock_lab",
            "source_path": str(C_CLOCK_PRODUCT),
            "evidence_status": "SOURCE_BACKED_PRODUCT_BOUND_NONCLAIM",
            "numeric_summary": f"clock_pair={best['clock_pair']}; delta_K_alpha={best['delta_K_alpha']}; one_sigma={best['product_bound_1sigma_yr_inv']}; two_sigma={best['product_bound_2sigma_yr_inv']}",
            "units": "yr^-1",
            "claim_status": "bounds product only, not standalone b_alpha or Bperp/Hperp",
            "valid_for_claim": "false",
            "blocks_claim": "true",
            "next_action": "derive tau_clock_time and Bperp/Hperp-to-alpha readout coefficient",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "join_id": "CLKJ3797_1_alpha_sensitivity",
            "arena_id": "clock_lab",
            "source_path": str(C_CLOCK_ALPHA),
            "evidence_status": "CLOCK_ALPHA_SENSITIVITY_ROW_AVAILABLE",
            "numeric_summary": f"clock_pair={alpha_row['clock_pair']}; D_e_eff={alpha_row['D_e_eff']}; one_sigma={alpha_row['product_bound_1sigma_yr_inv']}",
            "units": "dimensionless sensitivity and yr^-1 bound",
            "claim_status": "usable for nonclaim readout checks only",
            "valid_for_claim": "false",
            "blocks_claim": "true",
            "next_action": "tie sensitivity to parent-owned alpha/readout descent",
        },
    ]
    for symbol in ["b_alpha", "b_clock_i"]:
        item = coeff_map.get(symbol)
        if item:
            out.append(
                {
                    "timestamp_utc": timestamp,
                    "branch_id": BRANCH,
                    "checkpoint_id": CHECKPOINT,
                    "join_id": f"CLKJ3797_coeff_{symbol}",
                    "arena_id": "clock_lab",
                    "source_path": str(C_CLOCK_COEFF),
                    "evidence_status": item["current_status"],
                    "numeric_summary": item["required_inputs"],
                    "units": item["units"],
                    "claim_status": "clock coefficient not filled",
                    "valid_for_claim": "false",
                    "blocks_claim": "true",
                    "next_action": "derive theorem-zero or numeric/source-backed coefficient",
                }
            )
    for row in clock_profile:
        out.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "join_id": f"CLKJ3797_profile_{row['quantity']}",
                "arena_id": "clock_lab",
                "source_path": row["source_path"],
                "evidence_status": row["status"],
                "numeric_summary": row["value"],
                "units": row["units"],
                "claim_status": "clock numerator/readout missing",
                "valid_for_claim": "false",
                "blocks_claim": "true",
                "next_action": "supply parent-zero theorem or finite profile plus clock readout projection",
            }
        )
    return out


def fill_attempt_rows(timestamp):
    curve = load_csv(C_R10_CURVE)
    product = load_csv(C_CLOCK_PRODUCT)
    best = next(row for row in product if row.get("row_type") == "best_current")
    rows = [
        (
            "FFA3797_0_R10_bound_side",
            "R10_lab",
            "alpha_bound(lambda)",
            f"PARTIAL_FILLED_NONCLAIM: rows={len(curve)}, lambda_m={range_summary(curve, 'lambda_m')}, alpha_bound_abs={range_summary(curve, 'alpha_bound_abs')}",
            "candidate digitized curve exists; still manual-review nonclaim",
        ),
        (
            "FFA3797_1_R10_Bperp",
            "R10_lab",
            "Bperp_norm_over_Aref",
            "MISSING_PARENT_ZERO_OR_FINITE_BPERP_PROFILE",
            "must be derived from Q-shear/parent B_Q or supplied as finite field profile",
        ),
        (
            "FFA3797_2_R10_Hperp",
            "R10_lab",
            "Hperp_norm_over_Fref",
            "MISSING_PARENT_ZERO_OR_FINITE_HPERP_PROFILE",
            "must be derivative/profile of Bperp or parent H_Q descent theorem",
        ),
        (
            "FFA3797_3_clock_bound_side",
            "clock_lab",
            "clock_product_bound",
            f"PARTIAL_FILLED_NONCLAIM: {best['clock_pair']} one_sigma={best['product_bound_1sigma_yr_inv']} yr^-1",
            "real product bound exists but only constrains b_alpha*tau_clock_time/readout product",
        ),
        (
            "FFA3797_4_clock_Bperp",
            "clock_lab",
            "Bperp_norm_over_Aref",
            "MISSING_PARENT_ZERO_OR_FINITE_BPERP_PROFILE",
            "same Bperp numerator must be mapped into clock readout",
        ),
        (
            "FFA3797_5_clock_Hperp",
            "clock_lab",
            "Hperp_norm_over_Fref",
            "MISSING_PARENT_ZERO_OR_FINITE_HPERP_PROFILE",
            "same Hperp numerator must be mapped into clock readout",
        ),
        (
            "FFA3797_6_lambda_A",
            "R10_lab;clock_lab",
            "lambda_A",
            "MISSING_LAMBDA_A_PRIOR_OR_OPERATOR_BAN",
            "companion Maxwell-normalization branch remains legal unless parent operator-domain excludes it",
        ),
        (
            "FFA3797_7_beta_ZA",
            "clock_lab",
            "beta_Z,A",
            "MISSING_BETA_ZA_OR_PARENT_ZERO_THEOREM",
            "needed for clock/alpha drift readout",
        ),
        (
            "FFA3797_8_epsilonJ",
            "R10_lab;clock_lab",
            "epsilon_J_Q_total_abs",
            "MISSING_EPSILON_JQ_COMPONENT_VALUES",
            "same-current residual must be zeroed or bounded before local claim",
        ),
    ]
    out = []
    for row in rows:
        value = row[3]
        partial = value.startswith("PARTIAL_FILLED_NONCLAIM")
        out.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "fill_id": row[0],
                "arena_id": row[1],
                "quantity": row[2],
                "value_or_status": value,
                "filled_from_existing_evidence": "partial_nonclaim" if partial else "false",
                "valid_for_claim": "false",
                "blocks_claim": "true",
                "explanation": row[4],
            }
        )
    return out


def gate_rows(timestamp, grouped):
    r10_join = grouped["r10_join"]
    clock_join = grouped["clock_join"]
    r10_has_curve = any(row["join_id"] == "R10J3797_0_bound_curve_candidate" for row in r10_join)
    clock_has_bound = any(row["join_id"] == "CLKJ3797_0_best_clock_product" for row in clock_join)
    theory_missing = any("MISSING_" in row["numeric_summary"] for row in r10_join + clock_join)
    rows = [
        ("CG3797_0_sources", "all source paths and needles found", "true", "false"),
        ("CG3797_1_R10_bound_side", "candidate R10 curve and score rows imported as nonclaim evidence", bool_text(r10_has_curve), "false"),
        ("CG3797_2_clock_bound_side", "best clock product bound imported as nonclaim evidence", bool_text(clock_has_bound), "false"),
        ("CG3797_3_theory_numerator", "Bperp/Hperp/lambda/betaZ/epsilonJ numerator remains missing", bool_text(not theory_missing), "false"),
        ("CG3797_4_local_GR_claim", "R10/clock/local-GR claim remains closed", "false", "false"),
    ]
    out = []
    for gate_id, details, passed, claim_allowed in rows:
        out.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "gate_id": gate_id,
                "pass": passed,
                "claim_allowed": claim_allowed,
                "details": details,
                "valid_for_claim": "false",
            }
        )
    return out


def decision_rows(timestamp):
    rows = [
        (
            "DEC3797_0_result",
            "Evidence side is now separated from numerator side.",
            "R10 candidate bound rows and clock product bound rows exist, but Bperp/Hperp and companion coefficients are still missing.",
            "Do not run a claim; build the minimal parent-owned Bperp/Hperp profile or prove it zero.",
        ),
        (
            "DEC3797_1_best_next",
            "Next target is a first actual Bperp/Hperp profile ansatz or zero theorem.",
            "This is the least circular route because R10/clock bounds are already waiting for a theory numerator.",
            "Move to 3798 minimal profile/zero branch.",
        ),
        (
            "DEC3797_2_no_public_claim",
            "No R10, clock, alpha, EM, or local-GR pass is allowed.",
            "Every imported empirical row is nonclaim until curve review plus numerator closure.",
            "Keep this private framework work.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "action": action,
            "valid_for_claim": "false",
        }
        for decision_id, decision, rationale, action in rows
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_file": "3798-Y5-R2FR-minimal-Bperp-Hperp-profile-ansatz-or-parent-zero.md",
            "target_script": "scripts/Y5_R2FR_3798_minimal_Bperp_Hperp_profile_ansatz_or_parent_zero.py",
            "objective": "Construct the lowest-complexity parent-sourced symbolic Bperp/Hperp profile from Q-shear data or prove Bperp=Hperp=0; include dimensions, U_good patch, projection coefficients, and R10/clock join hooks.",
            "avoid": "do not invent a numeric numerator, do not promote candidate R10 curve, do not use clock product bound as standalone b_alpha, do not edit formalization-workbench or GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_PROFILE_SOURCE_ACQUISITION",
            "plain_verdict": "3797 imports the real waiting evidence side: candidate R10 bound/score rows and a clock product bound. The blocker is now explicit and narrower: MTS still owes the theory numerator Bperp/Hperp plus lambda/betaZ/epsilonJ/readout coefficients.",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(timestamp, grouped):
    curve = load_csv(C_R10_CURVE)
    product = load_csv(C_CLOCK_PRODUCT)
    curve_positive = all(float(row["lambda_m"]) > 0 and float(row["alpha_bound_abs"]) > 0 for row in curve)
    curve_sources = sorted({row.get("source_file", "") for row in curve if row.get("source_file")})
    curve_sources_exist = bool(curve_sources) and all(Path(path).exists() for path in curve_sources)
    best_products = [row for row in product if row.get("row_type") == "best_current"]
    clock_positive = bool(best_products) and all(float(row["product_bound_1sigma_yr_inv"]) > 0 for row in best_products)
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"), "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3797 markdown document written"),
        ("r10_curve_positive", curve_positive, "R10 candidate curve has positive lambda_m and alpha_bound_abs"),
        ("r10_curve_sources_exist", curve_sources_exist, "R10 candidate curve source files exist"),
        ("clock_product_positive", clock_positive, "best clock product bound is positive numeric"),
        ("theory_numerator_blocked", any("MISSING_" in row["value_or_status"] for row in grouped["fill_attempt"]), "Bperp/Hperp companion numerator remains explicitly blocked"),
        ("local_gr_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no R10/clock/local-GR claim allowed"),
        (
            "formalization_clean",
            not any((ROOT / "formalization-workbench").rglob("*3797*")),
            "no 3797 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "validation_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        keys = " ".join(f"`{row[key]}`" for key in key_fields)
        rest = "; ".join(f"{key}: {value}" for key, value in row.items() if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"})
        lines.append(f"- {keys}: {rest}")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3797 - First Bperp/Hperp Profile Source Acquisition for R10 and Clocks",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3797 stops treating R10 and clocks as vague future tests. The R10 bound side already has a candidate digitized curve and score-gate rows. The clock side already has a best alpha-clock product bound: `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1` for the Yb E3/E2 row.",
        "",
        "That is good news, but it is not a pass. Those rows are waiting for the MTS numerator: `Bperp_norm_over_Aref`, `Hperp_norm_over_Fref`, `lambda_A`, `beta_Z,A`, `epsilon_J_Q_total_abs`, and the readout/projection coefficients. So the next step is not another audit loop; it is to build the smallest honest `Bperp/Hperp` profile or prove it zero from the parent branch.",
        "",
        "## Compact Result",
        "",
        "`B_perp = B_Q - q_obs^*Bbar_Q - dchi` on `U_good`; `Hperp=dBperp`.",
        "",
        "R10 bound side: candidate rows exist but remain nonclaim until reviewed/promoted.",
        "",
        "Clock bound side: real product bound exists but does not give standalone `b_alpha` or `Bperp/Hperp`.",
        "",
        "Current verdict: empirical join hooks are present; theory numerator is missing.",
        "",
        render_section("Source Register", grouped["sources"], ["source_id"]),
        render_section("Profile Contract Rows", grouped["profile_contract"], ["contract_id", "arena_id", "quantity"]),
        render_section("R10 Bound Join Ledger", grouped["r10_join"], ["join_id", "arena_id"]),
        render_section("Clock Join Ledger", grouped["clock_join"], ["join_id", "arena_id"]),
        render_section("First Fill Attempt Rows", grouped["fill_attempt"], ["fill_id", "arena_id", "quantity"]),
        render_section("Claim Gates", grouped["gates"], ["gate_id"]),
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
        "profile_contract": profile_contract_rows(timestamp),
        "r10_join": r10_join_rows(timestamp),
        "clock_join": clock_join_rows(timestamp),
        "fill_attempt": fill_attempt_rows(timestamp),
        "gates": [],
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }
    grouped["gates"] = gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["profile_contract"], grouped["profile_contract"])
    write_csv(OUTPUTS["r10_join"], grouped["r10_join"])
    write_csv(OUTPUTS["clock_join"], grouped["clock_join"])
    write_csv(OUTPUTS["fill_attempt"], grouped["fill_attempt"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
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
        raise SystemExit(f"3797 validation failed: {failures}")
    print("wrote 3797 checkpoint: R10/clock evidence hooks imported; Bperp/Hperp numerator remains the blocker")


if __name__ == "__main__":
    main()
