import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3804"
BRANCH = "MTS_R2FR_Y5_QX_CALIBRATION_COMPANION_CLOSURE_OR_LOCAL_BOUND_RUNNER_3804"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3804-Y5-R2FR-qX-calibration-companion-closure-or-local-bound-runner.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3804_qX_calibration_companion_closure_or_local_bound_runner.py"

P_3770 = PCW / "3770-Y5-R2FR-source-action-leak-zero-or-WEP-EM-PPN-bound.md"
P_3771 = PCW / "3771-Y5-R2FR-constants-material-marker-leak-zero-or-clock-WEP-alpha-bound.md"
P_3777 = PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md"
P_3790 = PCW / "3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md"
P_3791 = PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_3802 = PCW / "3802-Y5-R2FR-parent-Qshear-spectral-action-clause-or-epsilonYV-bound.md"
P_3803 = PCW / "3803-Y5-R2FR-qX-same-source-no-extra-force-closure-or-epsilon-sourceXQ-bound.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_3803_BOUND = RESIDUALS / "P8_Y5_R2FR_3803_EPSILON_SOURCE_XQ_BOUND_ROWS.csv"
C_3803_ARENA = RESIDUALS / "P8_Y5_R2FR_3803_ARENA_SOURCE_PROJECTION_ROWS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3804_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3804_COMPANION_CLOSURE_THEOREM.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3804_CALIBRATION_COMPANION_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3804_CURRENT_COMPANION_AUDIT.csv",
    "input_vector": RESIDUALS / "P8_Y5_R2FR_3804_COMPANION_INPUT_VECTOR.csv",
    "arena_matrix": RESIDUALS / "P8_Y5_R2FR_3804_ARENA_TRANSFER_MATRIX.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_3804_LOCAL_BOUND_RUNNER_DRYRUN.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3804_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3804_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3804_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3804_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3804_VALIDATION.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC3804_0_3803_handoff",
        "path": P_3803,
        "needle": "epsilon_XQ_force_abs",
        "role": "3803 selected q_X companion calibration and bound-runner wiring",
    },
    {
        "source_id": "SRC3804_1_3790_qstar",
        "path": P_3790,
        "needle": "beta_q,A := Lie_EA ln q_*",
        "role": "charge-unit superselection theorem and beta_q fallback rows",
    },
    {
        "source_id": "SRC3804_2_3791_ZEM",
        "path": P_3791,
        "needle": "beta_Z,A := Lie_EA ln Z_EM",
        "role": "Maxwell normalization, lambda_A, and alpha-readout guard",
    },
    {
        "source_id": "SRC3804_3_3792_same_current",
        "path": P_3792,
        "needle": "epsilon_J_Q_total_abs",
        "role": "same-current Ward/Hilbert residual vector",
    },
    {
        "source_id": "SRC3804_4_3771_theta",
        "path": P_3771,
        "needle": "L_leak_theta",
        "role": "constants/material/source-marker leak and clock/WEP/R10 interfaces",
    },
    {
        "source_id": "SRC3804_5_3777_domain",
        "path": P_3777,
        "needle": "Pi_M_total",
        "role": "total-system domain, EM/Poynting tail, and boundary support map",
    },
    {
        "source_id": "SRC3804_6_3770_source",
        "path": P_3770,
        "needle": "J_A^src := delta S_src/dzeta^A",
        "role": "source-action leak operator and WEP/PPN source projection",
    },
    {
        "source_id": "SRC3804_7_3802_Qspec",
        "path": P_3802,
        "needle": "L_Qspec=lambda_X",
        "role": "Qspec constraint stress owner slot",
    },
    {
        "source_id": "SRC3804_8_3803_bound_rows",
        "path": C_3803_BOUND,
        "needle": "ESX3803_9_epsilon_XQ_force_abs",
        "role": "3803 q_X force residual vector input",
    },
    {
        "source_id": "SRC3804_9_3803_arena_rows",
        "path": C_3803_ARENA,
        "needle": "ARX3803_0_WEP",
        "role": "3803 arena projection formulas",
    },
    {
        "source_id": "SRC3804_10_spine",
        "path": P_SPINE,
        "needle": "3804-Y5-R2FR-qX-calibration-companion-closure-or-local-bound-runner.md",
        "role": "live spine target for this checkpoint",
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


def source_register(timestamp):
    rows = []
    for spec in SOURCE_SPECS:
        exists = spec["path"].exists()
        needle_found = False
        if exists:
            needle_found = spec["needle"] in read_text(spec["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(spec["path"]),
                "exists": bool_text(exists),
                "needle": spec["needle"],
                "needle_found": bool_text(needle_found),
                "role": spec["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    specs = [
        (
            "CCT3804_0_companion_vector",
            "q_X companion vector definition",
            "Define C_qX_companion_abs = eps_betaq + epsilon_ZEM_XQ + epsilon_J_Q + epsilon_theta_XQ + epsilon_kappa_XQ + epsilon_shadow_XQ + epsilon_Qspec_stress + epsilon_boundary_XQ + epsilon_domain_XQ + epsilon_arena_coeff. Then N_qX_local_abs = N_Qspec_local_abs + epsilon_source_XQ + C_qX_companion_abs.",
            "DEFINITION_FROM_3790_3791_3792_3771_3777_3803",
            "The q_X local branch now has one executable residual vector instead of separate calibration caveats.",
            "numeric/theorem-zero values for companion components are missing",
        ),
        (
            "CCT3804_1_triangular_closure_order",
            "non-circular closure order",
            "A non-smuggled q_X closure must proceed q_* superselection -> fixed Z_EM/no F2 counterterm -> same-current Hilbert source -> theta/source marker silence -> Qspec stress inclusion -> boundary/domain silence -> arena transfer coefficients. Later gates may use earlier zero theorems, but no gate may be fit from the arena it is meant to predict.",
            "DERIVED_DEPENDENCY_ORDER",
            "This prevents fitting alpha, clocks, R10, or orbital GM and then calling the fitted normalization a derivation.",
            "strict corpus signs only conditional theorem shapes, not the whole chain",
        ),
        (
            "CCT3804_2_qstar_simplification",
            "q_* branch simplification",
            "If q_* is parent-signed as compact charge-lattice/superselection data, then beta_q,A=0 and d beta_q,A=0, so eps_betaq=eps_qA+eps_betaqF+eps_dbetaqA=0. This removes charge-unit drift from R_A/dR_A but does not fix Z_EM or alpha_EM.",
            "EXACT_CONDITIONAL_IMPORT_FROM_3790",
            "The charge-unit branch can simplify the local EM residual algebra without overclaiming fine-structure ownership.",
            "parent U1 bundle/generator/lattice owner remains unsigned",
        ),
        (
            "CCT3804_3_ZEM_lambda_gate",
            "Z_EM and lambda gate",
            "epsilon_ZEM_XQ=0 only if Z_EM is q_X-owned or superselected, the parent generator norm is nonrescalable, no independent lambda_A F^2 or f(X_Q)F^2 operator is legal, and observed alpha/current/readout normalization descends. Otherwise beta_Z,A, lambda_A, b_Z_hidden, and b_alpha_readout remain finite inputs.",
            "EXACT_CONDITIONAL_WITH_COUNTEREXAMPLE_GUARD",
            "This is the main calibration throat: compact U1 helps but does not derive the Maxwell kinetic coefficient.",
            "no-independent-F2/product-sequester theorem is not parent-signed",
        ),
        (
            "CCT3804_4_same_current_domain_gate",
            "same-current plus total-domain gate",
            "epsilon_J_Q and epsilon_domain_XQ vanish only when charged matter, EM stress, binding/apparatus stress, Poynting/tails, and boundary bookkeeping are varied inside one descended total source action over a total-system domain with no unowned flux.",
            "EXACT_CONDITIONAL_SOURCE_DOMAIN_IMPORT",
            "Real EM/Poynting stress is either ordinary Hilbert source mass or an explicit residual; it cannot be erased.",
            "total q_X source action, EM descent, Poynting/tail, and boundary certificates remain unsigned",
        ),
        (
            "CCT3804_5_theta_kappa_shadow_gate",
            "source marker and frame gate",
            "epsilon_theta_XQ, epsilon_kappa_XQ, and epsilon_shadow_XQ vanish only if constants/material labels/source normalization, kappa_eff, and sector frames are q_X-owned/superselected or depend only on q_obs. Unit rescaling alone is not sufficient for Newton GM or absolute G.",
            "EXACT_CONDITIONAL_MARKER_FRAME_GATE",
            "This keeps local GR/Newton calibration tied to source normalization rather than a hidden units move.",
            "theta/source, kappa, and frame owner clauses remain unsigned",
        ),
        (
            "CCT3804_6_runner_acceptance_rule",
            "local bound runner acceptance rule",
            "For each arena a in {WEP, PPN_gamma, PPN_beta, R10, clock, orbital, Gdot}, evaluate pred_a = sum_i C_ai r_i. The arena is claim-eligible only if every r_i is theorem-zero or sourced numeric, every C_ai is sourced or exact, and pred_a <= bound_a without borrowing fitted constants from that same arena.",
            "EXECUTABLE_NONCLAIM_GATE",
            "Testing can start as soon as rows are populated, but the runner will refuse placeholder victories.",
            "all current 3804 dry-run arenas are blocked by missing component values or coefficients",
        ),
    ]
    rows = []
    for theorem_id, claim_piece, mathematical_form, derivation_status, result_if_signed, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "derivation_status": derivation_status,
                "result_if_signed": result_if_signed,
                "missing_for_current_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def contract_rows(timestamp):
    specs = [
        ("CCC3804_0_qstar", "q_* superselection", "q_* is fixed compact U1 charge-lattice/generator data before EM readout.", "MISSING_PARENT_U1_LATTICE_GENERATOR_OWNER"),
        ("CCC3804_1_ZEM", "Z_EM fixed normalization", "Z_EM is fixed by parent curvature/generator norm and cannot receive independent X_Q-dependent F2 terms.", "MISSING_ZEM_OWNER_AND_NO_INDEPENDENT_F2"),
        ("CCC3804_2_lambda", "lambda_A exclusion", "lambda_A F_obs^2 and f(X_Q)F_obs^2 are forbidden by parent operator-domain exhaustion or bounded.", "MISSING_OPERATOR_DOMAIN_EXHAUSTION"),
        ("CCC3804_3_current", "same-current owner", "J_Q is varied from the same descended source action that owns Maxwell source and Hilbert stress.", "MISSING_QX_SAME_CURRENT_OWNER"),
        ("CCC3804_4_theta", "theta/source markers", "masses, charges, material labels, clock markers, binding fractions, and source normalization are q_X-owned or superselected.", "MISSING_THETA_SOURCE_MARKER_SUPERSELECTION"),
        ("CCC3804_5_kappa", "kappa calibration", "kappa_eff and source coupling scale are q_X-owned/global or bounded independently of orbital fitting.", "MISSING_KAPPA_XQ_CALIBRATION"),
        ("CCC3804_6_shadow", "single observed frame", "matter, light, EM, clocks, and source readout use one observed metric/coframe under q_X.", "MISSING_SHADOW_FRAME_XQ_CERTIFICATE"),
        ("CCC3804_7_Qspec_stress", "Qspec stress", "L_Qspec Hilbert/coframe variation is included in T_total, projected silent, or bounded.", "MISSING_QSPEC_STRESS_OWNER"),
        ("CCC3804_8_domain", "total domain", "Pi_M_total/source domain includes descended EM/Poynting/binding/apparatus support or bounds omitted tails.", "MISSING_TOTAL_SYSTEM_DOMAIN_BOUND"),
        ("CCC3804_9_arena_coefficients", "arena transfer coefficients", "C_ai coefficients from local residuals to WEP/PPN/R10/clock/orbital/Gdot are exact or source-backed.", "MISSING_ARENA_PROJECTION_COEFFICIENTS"),
    ]
    rows = []
    for clause_id, clause, requirement, current_status in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "clause_id": clause_id,
                "clause": clause,
                "requirement": requirement,
                "current_status": current_status,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def audit_rows(timestamp):
    specs = [
        ("AUD3804_0_qstar", "q_*", "3790 gives an exact conditional superselection theorem.", "CONDITIONAL_ZERO_AVAILABLE", "not strict-current signed"),
        ("AUD3804_1_ZEM", "Z_EM/lambda", "3791 shows ordinary symmetries allow F2 and f(Xhat)F2 counterterms.", "ACTIVE_COUNTEREXAMPLE", "operator-domain exhaustion missing"),
        ("AUD3804_2_current", "epsilon_J_Q", "3792 gives exact same-current Ward/Hilbert theorem.", "CONDITIONAL_ZERO_AVAILABLE", "same q_X source action/domain not signed"),
        ("AUD3804_3_theta", "theta/source markers", "3771 names L_leak_theta and bound interfaces.", "CONDITIONAL_ZERO_AVAILABLE", "superselection/source normalization missing"),
        ("AUD3804_4_domain", "boundary/domain", "3777 defines Pi_M_total and total-system domain rules.", "CONDITIONAL_CONSTRUCTION_AVAILABLE", "EM tail/Poynting/domain flux certificates missing"),
        ("AUD3804_5_Qspec", "Qspec stress", "3802/3803 require L_Qspec stress inclusion or projection silence.", "REQUIRED_NOT_FILLED", "no Hilbert stress owner certificate"),
        ("AUD3804_6_runner", "local bound runner", "3803 arena rows exist but all coefficients are marked missing.", "DRY_RUN_BLOCKED", "component values and C_ai coefficients missing"),
    ]
    rows = []
    for audit_id, item, current_evidence, status, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "item": item,
                "current_evidence": current_evidence,
                "status": status,
                "missing_for_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def input_vector_rows(timestamp):
    specs = [
        ("R3804_0_eps_betaq", "eps_betaq", "eps_qA + eps_betaqF + eps_dbetaqA", "dimensionless", "MISSING_QSTAR_PARENT_SIGNATURE_OR_BETAQ_BOUND", "q_* compact-lattice theorem or numeric beta_q profile", "R_A;dR_A;alpha_source"),
        ("R3804_1_epsilon_ZEM_XQ", "epsilon_ZEM_XQ", "|partial_XQ ln Z_EM| + |lambda_A| + |b_Z_hidden| + |b_alpha_readout|", "dimensionless", "MISSING_ZEM_LAMBDA_XQ_CERTIFICATE", "Z_EM fixed-normalization/no-F2 theorem or alpha/readout bounds", "R10;clock;WEP;PPN"),
        ("R3804_2_epsilon_J_Q", "epsilon_J_Q", "epsilon_J_Q_total_abs from same-current Ward/Hilbert vector", "dimensionless", "MISSING_QX_SAME_CURRENT_CERTIFICATE", "one q_X descended total source action", "WEP;PPN;Newton;R10;clock"),
        ("R3804_3_epsilon_theta_XQ", "epsilon_theta_XQ", "epsilon_theta + b_alpha + b_mu + b_material + b_clock + b_source_norm projected under q_X", "dimensionless", "MISSING_THETA_XQ_SILENCE_CERTIFICATE", "theta/source marker superselection or sourced sensitivities", "WEP;clock;R10;Newton"),
        ("R3804_4_epsilon_kappa_XQ", "epsilon_kappa_XQ", "|partial_XQ ln kappa_eff| plus source-coupling calibration drift", "dimensionless", "MISSING_KAPPA_XQ_OWNER", "global/q_X kappa theorem or Gdot/PPN source bound", "Gdot;PPN;orbital"),
        ("R3804_5_epsilon_shadow_XQ", "epsilon_shadow_XQ", "sector-frame/coframe dependence on X_Q outside q_obs", "dimensionless", "MISSING_SHADOW_FRAME_XQ_BOUND", "single observed frame under q_X or finite frame bound", "PPN;clock"),
        ("R3804_6_epsilon_Qspec_stress", "epsilon_Qspec_stress", "unowned Hilbert stress from L_Qspec", "dimensionless", "MISSING_QSPEC_STRESS_INCLUSION_OR_BOUND", "include Qspec stress, projection silence, or finite stress row", "PPN;Newton;WEP;orbital"),
        ("R3804_7_epsilon_boundary_XQ", "epsilon_boundary_XQ", "Qspec/B_Q/EM/source boundary flux under q_X", "dimensionless", "MISSING_QX_BOUNDARY_FLUX_CERTIFICATE", "no-flux theorem or finite flux bound", "R10;Newton;orbital;clock"),
        ("R3804_8_epsilon_domain_XQ", "epsilon_domain_XQ", "mismatch between q_X total source domain and field/support tails", "dimensionless", "MISSING_QX_TOTAL_DOMAIN_CERTIFICATE", "Pi_M_total domain closure or tail/domain bound", "Newton;orbital;PPN;WEP"),
        ("R3804_9_epsilon_arena_coeff", "epsilon_arena_coeff", "uncertainty/absence of C_ai transfer coefficients", "dimensionless", "MISSING_ARENA_PROJECTION_COEFFICIENTS", "exact local transfer map or source-backed sensitivity matrix", "all_arenas"),
        ("R3804_10_C_qX_companion_abs", "C_qX_companion_abs", "sum_abs(R3804_0 through R3804_9)", "dimensionless", "ABS_SUM_BOUND_READY_COMPONENTS_MISSING", "all component rows theorem-zero or numeric", "local_GR_gate"),
        ("R3804_11_N_qX_local_abs", "N_qX_local_abs", "N_Qspec_local_abs + epsilon_source_XQ + C_qX_companion_abs", "dimensionless", "LOCAL_QX_BOUND_READY_NUMERIC_INPUTS_MISSING", "Qspec selector/source-force/companion rows all filled", "local_GR_gate"),
    ]
    rows = []
    for row_id, symbol, formula, units, current_value, required, feeds in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "current_value": current_value,
                "required_source_or_zero": required,
                "feeds": feeds,
                "status": "REQUIRED_NOT_FILLED",
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def arena_matrix_rows(timestamp):
    specs = [
        ("AM3804_0_WEP", "eta_XQ_AB", "C_WEP_source*epsilon_source_XQ + C_WEP_theta*epsilon_theta_XQ + C_WEP_Z*epsilon_ZEM_XQ + C_WEP_domain*epsilon_domain_XQ + C_WEP_Qspec*epsilon_Qspec_stress", "2.8e-15", "dimensionless", "epsilon_source_XQ;epsilon_theta_XQ;epsilon_ZEM_XQ;epsilon_domain_XQ;epsilon_Qspec_stress"),
        ("AM3804_1_PPN_gamma", "delta_gamma_XQ", "C_gamma_source*epsilon_XQ_force_abs + C_gamma_shadow*epsilon_shadow_XQ + C_gamma_Qspec*epsilon_Qspec_stress + C_gamma_domain*epsilon_domain_XQ", "2.3e-05", "dimensionless", "epsilon_XQ_force_abs;epsilon_shadow_XQ;epsilon_Qspec_stress;epsilon_domain_XQ"),
        ("AM3804_2_PPN_beta", "delta_beta_XQ", "C_beta_source*epsilon_XQ_force_abs + C_beta_kappa*epsilon_kappa_XQ + C_beta_theta*epsilon_theta_XQ + C_beta_domain*epsilon_domain_XQ", "7.8e-05", "dimensionless", "epsilon_XQ_force_abs;epsilon_kappa_XQ;epsilon_theta_XQ;epsilon_domain_XQ"),
        ("AM3804_3_R10", "alpha_R10_XQ(lambda)", "C_R10_source(lambda)*epsilon_source_XQ + C_R10_Z(lambda)*epsilon_ZEM_XQ + C_R10_boundary(lambda)*epsilon_boundary_XQ + C_R10_theta(lambda)*epsilon_theta_XQ", "requires_alpha_bound_lambda_curve", "dimensionless", "epsilon_source_XQ;epsilon_ZEM_XQ;epsilon_boundary_XQ;epsilon_theta_XQ"),
        ("AM3804_4_clock", "b_clock_XQ", "C_clock_theta*epsilon_theta_XQ + C_clock_Z*epsilon_ZEM_XQ + C_clock_shadow*epsilon_shadow_XQ + C_clock_boundary*epsilon_boundary_XQ", "requires_clock_product_or_sensitivity_split", "yr^-1_or_dimensionless_product", "epsilon_theta_XQ;epsilon_ZEM_XQ;epsilon_shadow_XQ;epsilon_boundary_XQ"),
        ("AM3804_5_orbital", "delta_mu_XQ", "C_mu_source*epsilon_source_XQ + C_mu_kappa*epsilon_kappa_XQ + C_mu_Qspec*epsilon_Qspec_stress + C_mu_domain*epsilon_domain_XQ + C_mu_boundary*epsilon_boundary_XQ", "requires_non_circular_source_denominator", "dimensionless", "epsilon_source_XQ;epsilon_kappa_XQ;epsilon_Qspec_stress;epsilon_domain_XQ;epsilon_boundary_XQ"),
        ("AM3804_6_Gdot", "dlnG_XQ_dt", "d_t epsilon_kappa_XQ + d_t epsilon_theta_XQ + d_t epsilon_source_XQ + d_t epsilon_domain_XQ", "9.6e-15 yr^-1", "yr^-1", "epsilon_kappa_XQ;epsilon_theta_XQ;epsilon_source_XQ;epsilon_domain_XQ"),
    ]
    rows = []
    for arena_id, observable, transfer_formula, bound_reference, units, required_inputs in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "arena_id": arena_id,
                "observable": observable,
                "transfer_formula": transfer_formula,
                "bound_reference": bound_reference,
                "units": units,
                "required_inputs": required_inputs,
                "coefficient_status": "MISSING_ARENA_PROJECTION_COEFFICIENTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def runner_rows(timestamp, input_rows, arena_rows):
    missing_symbols = [row["symbol"] for row in input_rows if row["current_value"].startswith("MISSING") or "MISSING" in row["current_value"]]
    rows = []
    for arena in arena_rows:
        required = arena["required_inputs"].split(";")
        missing_required = [symbol for symbol in required if symbol in missing_symbols or symbol == "epsilon_XQ_force_abs"]
        if arena["coefficient_status"].startswith("MISSING"):
            missing_required.append("C_ai")
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "arena_id": arena["arena_id"],
                "observable": arena["observable"],
                "dryrun_status": "BLOCKED_MISSING_INPUTS",
                "missing_inputs": ";".join(sorted(set(missing_required))),
                "bound_reference": arena["bound_reference"],
                "predicted_value": "NOT_EVALUATED",
                "acceptance_rule": "all inputs numeric_or_theorem_zero and all C_ai sourced/exact and predicted_value <= bound_reference",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )
    return rows


def claim_gate_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    input_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["input_vector"])
    runner_blocked = all(row["dryrun_status"] == "BLOCKED_MISSING_INPUTS" and row["claim_allowed"] == "false" for row in grouped["runner"])
    specs = [
        ("CG3804_0_sources", sources_ok and needles_ok, "all source paths and needles found"),
        ("CG3804_1_companion_law", True, "C_qX_companion_abs and N_qX_local_abs law emitted"),
        ("CG3804_2_triangular_order", True, "non-circular closure order emitted"),
        ("CG3804_3_qstar_current_signed", False, "q_* superselection is conditional but not strict-current signed"),
        ("CG3804_4_ZEM_lambda_closed", False, "Z_EM/lambda/no-F2 gate remains open"),
        ("CG3804_5_same_current_domain_closed", False, "same-current total domain and boundary clauses remain open"),
        ("CG3804_6_input_rows_nonclaim", input_nonclaim, "all companion input rows remain nonclaim blockers"),
        ("CG3804_7_runner_refuses_placeholders", runner_blocked, "local bound runner dry-run blocks every arena with missing inputs"),
        ("CG3804_8_local_GR_claim", False, "no q_X local-GR/Newton/EM/PPN/R10/clock/orbital claim allowed"),
    ]
    rows = []
    for gate_id, passed, details in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "gate_id": gate_id,
                "pass": bool_text(passed),
                "claim_allowed": "false",
                "details": details,
                "valid_for_claim": "false",
            }
        )
    return rows


def decision_rows(timestamp):
    specs = [
        (
            "DEC3804_0_progress",
            "The q_X companion problem is now one executable residual vector.",
            "C_qX_companion_abs collects q_*, Z_EM/lambda, same-current, theta/source, kappa/frame, Qspec stress, boundary/domain, and arena coefficients.",
            "Use this runner as the gate before any local-GR or empirical scoring claim.",
        ),
        (
            "DEC3804_1_pressure_point",
            "The strongest remaining obstruction is the visible-coefficient operator domain.",
            "Terms like f(X_Q)F^2, m_A(X_Q), kappa(X_Q), or source weights can pass quotient bookkeeping while changing observables.",
            "Next derive a no-XQ-visible-coefficient sequester theorem, or accept component bound acquisition.",
        ),
        (
            "DEC3804_2_nonclaim",
            "No claim follows from 3804.",
            "The dry-run intentionally blocks every arena because component values and transfer coefficients are missing.",
            "Keep all rows private/nonclaim until theorem-zero or source-backed numeric inputs exist.",
        ),
    ]
    rows = []
    for decision_id, decision, rationale, action in specs:
        rows.append(
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
        )
    return rows


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3805-Y5-R2FR-no-XQ-visible-coefficient-sequester-theorem-or-component-bound-acquisition.md",
            "target_script": "scripts/Y5_R2FR_3805_no_XQ_visible_coefficient_sequester_theorem_or_component_bound_acquisition.py",
            "objective": "Try to prove a parent object-language rule that X_Q cannot appear in visible coefficients f(X_Q)F^2, m_A(X_Q), kappa(X_Q), source weights, clock/material markers, or boundary weights outside the declared B_Q path; if it fails, prioritize first source-backed component bounds for epsilon_ZEM_XQ, epsilon_theta_XQ, and epsilon_source_XQ.",
            "avoid": "do not fit visible coefficients from local tests and then treat the fitted coefficients as parent-derived",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_QX_COMPANION_VECTOR_AND_LOCAL_BOUND_RUNNER_DRYRUN",
            "headline": "q_X companion gates are collected into C_qX_companion_abs and a dry-run local bound runner; all arenas remain blocked by missing component values or transfer coefficients.",
            "claim_allowed": "false",
            "next_target": "3805 no-XQ visible-coefficient sequester theorem or component bound acquisition",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    input_nonclaim = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["input_vector"])
    runner_blocked = all(row["dryrun_status"] == "BLOCKED_MISSING_INPUTS" for row in grouped["runner"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_patterns = ("*Y5_R2FR_3804*", "*3804-Y5*", "*P8_Y5*3804*")
    fwb_hits = []
    if FWB.exists():
        for pattern in fwb_patterns:
            fwb_hits.extend(FWB.rglob(pattern))
    fwb_clean = not fwb_hits
    pycache_clean = not (PCW / "scripts" / "__pycache__").exists()
    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    script_text = read_text(SCRIPT_PATH) if SCRIPT_PATH.exists() else ""
    mojibake_c2 = chr(0x00C2)
    replacement_char = chr(0xFFFD)
    bad_chars_clean = mojibake_c2 not in doc_text + script_text and replacement_char not in doc_text + script_text
    checks = [
        ("sources_exist", sources_ok, "every cited source path exists"),
        ("needles_found", needles_ok, "every cited source needle was found"),
        ("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3804 markdown document written"),
        ("companion_vector_present", "C_qX_companion_abs" in theorem_text and "N_qX_local_abs" in theorem_text, "companion vector and local residual law emitted"),
        ("triangular_order_present", "q_* superselection -> fixed Z_EM/no F2 counterterm" in theorem_text, "non-circular closure order emitted"),
        ("runner_acceptance_present", "pred_a = sum_i C_ai r_i" in theorem_text, "runner acceptance theorem emitted"),
        ("input_rows_nonclaim", input_nonclaim, "all companion input rows remain nonclaim blockers"),
        ("runner_blocks_placeholders", runner_blocked, "dry-run blocks arenas with missing inputs"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3804 files written under formalization-workbench"),
        ("pycache_removed", pycache_clean, "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    rows = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
    return rows


def row_bullet(row, key_fields):
    label = " ".join(f"`{row[field]}`" for field in key_fields if field in row and row[field])
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped):
    lines = [
        "# 3804 - qX Calibration Companion Closure or Local Bound Runner",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_QX_COMPANION_VECTOR_AND_LOCAL_BOUND_RUNNER_DRYRUN`.",
        "",
        "3804 converts the q_X companion problem into an executable local gate. The core object is",
        "",
        "`C_qX_companion_abs = eps_betaq + epsilon_ZEM_XQ + epsilon_J_Q + epsilon_theta_XQ + epsilon_kappa_XQ + epsilon_shadow_XQ + epsilon_Qspec_stress + epsilon_boundary_XQ + epsilon_domain_XQ + epsilon_arena_coeff`.",
        "",
        "The local q_X residual is therefore",
        "",
        "`N_qX_local_abs = N_Qspec_local_abs + epsilon_source_XQ + C_qX_companion_abs`.",
        "",
        "This is not a pass. It is a runner-ready contract: every local arena remains blocked until each component is theorem-zero or source-backed numeric, and every transfer coefficient `C_ai` is exact or sourced.",
        "",
        "## Result In Plain Terms",
        "",
        "The coupling issue has now become a visible-coefficient issue. q_* can be conditionally zeroed by charge-lattice superselection, but that does not derive `Z_EM`, alpha, current normalization, source markers, or domain closure. The live danger is terms like `f(X_Q)F^2`, `m_A(X_Q)`, `kappa(X_Q)`, source weights, clock/material markers, or boundary weights outside the declared `B_Q` path.",
        "",
        "So the next useful leap is a sequester theorem: prove the parent object language forbids visible coefficients depending on `X_Q`, or stop pretending and acquire component bounds.",
        "",
        "## Compact Result",
        "",
        "`q_*` has an exact conditional zero branch, but it does not fix `Z_EM`.",
        "",
        "`Z_EM/lambda_A` is the sharpest calibration throat because `F^2` counterterms are symmetry-legal unless parent-excluded.",
        "",
        "`C_qX_companion_abs` is now the private local-GR runner vector.",
        "",
        "The dry-run blocks every arena by design because placeholders are not evidence.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Companion Closure Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Calibration Companion Contract", "contract", ["clause_id", "clause"]),
        ("Current Companion Audit", "audit", ["audit_id", "item"]),
        ("Companion Input Vector", "input_vector", ["row_id", "symbol"]),
        ("Arena Transfer Matrix", "arena_matrix", ["arena_id", "observable"]),
        ("Local Bound Runner Dryrun", "runner", ["arena_id", "observable"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decisions", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "contract": contract_rows(timestamp),
        "audit": audit_rows(timestamp),
        "input_vector": input_vector_rows(timestamp),
        "arena_matrix": arena_matrix_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["runner"] = runner_rows(timestamp, grouped["input_vector"], grouped["arena_matrix"])
    grouped["gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["contract"], grouped["contract"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["input_vector"], grouped["input_vector"])
    write_csv(OUTPUTS["arena_matrix"], grouped["arena_matrix"])
    write_csv(OUTPUTS["runner"], grouped["runner"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    write_markdown(grouped)
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()

    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
