import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3809"
BRANCH = "MTS_R2FR_Y5_MAXWELL_NORMALIZATION_PARENT_INNER_PRODUCT_OR_ALPHA_FINITE_3809"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3809-Y5-R2FR-Maxwell-normalization-from-parent-inner-product-or-alpha-finite-branch.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3809_Maxwell_normalization_from_parent_inner_product_or_alpha_finite_branch.py"

P_3808 = PCW / "3808-Y5-R2FR-visible-coefficient-type-system-from-representation-superselection-or-finite-bounds.md"
P_3791 = PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"
P_1057 = PCW / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
P_1058 = PCW / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
P_1099 = PCW / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
P_1100 = PCW / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
P_1110 = PCW / "1110-Y5-R10-alpha-normalization-vs-drift-two-track-ledger.md"
P_1111 = PCW / "1111-Y5-R10-alpha-drift-zero-theorem-or-product-source-vector.md"
P_1112 = PCW / "1112-Y5-R10-ZQeff-descent-clause-audit-or-alpha-product-runner-contract.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_1052 = PCW / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3809_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv",
    "zqeff": RESIDUALS / "P8_Y5_R2FR_3809_ZQEFF_DECOMPOSITION.csv",
    "tracks": RESIDUALS / "P8_Y5_R2FR_3809_ALPHA_TWO_TRACK_LEDGER.csv",
    "products": RESIDUALS / "P8_Y5_R2FR_3809_FINITE_ALPHA_PRODUCT_CONTRACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3809_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3809_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3809_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3809_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3809_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3809_0_3808_ZEM_guard", P_3808, "ORT3808_5_ZEM_guard", "3808 guard: q_star does not derive Z_EM/alpha"),
    ("SRC3809_1_3791_ZEM", P_3791, "ZFT3791_1_conditional_zero", "3791 fixed-normalization theorem"),
    ("SRC3809_2_1057_noF2", P_1057, "UMS1057_2_no_independent_F2", "1057 no-independent-F2 gate"),
    ("SRC3809_3_1058_ZA", P_1058, "ACP1058_0_ZA_decomposition", "1058 alpha counterterm decomposition"),
    ("SRC3809_4_1099_owner", P_1099, "UEM1099_1_chain_rule", "1099 unique EM owner chain-rule theorem"),
    ("SRC3809_5_1100_TQ", P_1100, "TQT1100_0_exact_conditional", "1100 T_Q/gauge-norm signature theorem"),
    ("SRC3809_6_1110_tracks", P_1110, "TRACK1110_N0", "1110 normalization/drift two-track split"),
    ("SRC3809_7_1111_drift", P_1111, "ADZ1111_1_chain_rule", "1111 alpha drift chain-rule theorem"),
    ("SRC3809_8_1112_descent", P_1112, "ZQD1112_0_sandwich_statement", "1112 Z_Q_eff descent sandwich theorem"),
    ("SRC3809_9_3792_current", P_3792, "SCW3792_1_same_current_definition", "same-current owner required for alpha source/readout"),
    ("SRC3809_10_1052_product", P_1052, "TCN1052_4_verdict", "clock product is not standalone b_alpha"),
    ("SRC3809_11_spine", P_SPINE, "3809-Y5-R2FR-Maxwell-normalization-from-parent-inner-product-or-alpha-finite-branch.md", "live spine target"),
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows(timestamp):
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    rows = [
        (
            "MNT3809_0_parent_inner_product",
            "parent Maxwell coefficient candidate",
            "If A_parent=A_Q T_Q+A_perp and S_parent contains -C_P/4 int mu_obs <F_parent,F_parent>_P, then the Q subblock contributes Z_parent=C_P N_Q with N_Q=<T_Q,T_Q>_P.",
            "EXACT_CONDITIONAL_SUBBLOCK_CALCULATION",
            "This gives one legitimate parent-owned Maxwell kinetic coefficient candidate.",
            "T_Q parent object; fixed nonrescalable N_Q; C_P parent owner",
        ),
        (
            "MNT3809_1_parent_vertical_silence",
            "vertical silence of parent piece",
            "For local vertical v, D_v(C_P N_Q)=0 if C_P and N_Q are q_obs-owned or representation/superselection data. This is the Maxwell instance of the 3808 ObsRep chain rule.",
            "EXACT_CONDITIONAL_CHAIN_RULE",
            "The parent piece can be locally safe without deriving alpha's numerical value.",
            "parent-signed C_P/N_Q ownership",
        ),
        (
            "MNT3809_2_rescaling_countermodel",
            "fixed norm is not optional",
            "If N_Q is not parent-fixed, T_Q -> s T_Q with compensating A_Q/current/charge normalization preserves observed form while leaving no unique alpha owner.",
            "COUNTERMODEL_RETAINED",
            "Compact U(1) labels alone do not fix the continuous EM coupling.",
            "nonrescalable fibre norm, level, index, monopole, Ward, or equivalent owner",
        ),
        (
            "MNT3809_3_no_extra_F2_countermodel",
            "parent piece is insufficient if extra F2 is legal",
            "Even with Z_parent=C_P N_Q, a legal DeltaS=-1/4 int mu_obs(lambda_A+f_X(X_Q)+f_hid(I))F_Q^2 changes Z_Q_eff and can carry vertical drift.",
            "COUNTEREXAMPLE_RETAINED",
            "No alpha theorem-zero follows from the parent subblock unless the visible operator domain forbids extra F2 coefficients.",
            "operator-domain exhaustion; no hidden-visible coefficient morphism; radiative closure",
        ),
        (
            "MNT3809_4_ZQeff_descent",
            "effective Maxwell normalization descent",
            "Let Z_Q_eff=C_P N_Q+lambda_A_common+f_hid(I_hid)+Delta_rad(mu,X)+Delta_readout(rho,X). If Z_Q_eff=Zbar(q_obs,theta_rep) and v in ker(Dq_obs), then D_v Z_Q_eff=0 and b_alpha=-D_v ln Z_Q_eff=0 on nonsingular local domains.",
            "EXACT_CONDITIONAL_DESCENT_THEOREM",
            "This is the clean local alpha-drift zero theorem; it is a chain-rule result, not a fitted cancellation.",
            "parent norm descent; hidden sequester; radiative/readout descent; same-current/readout owner",
        ),
        (
            "MNT3809_5_absolute_value_split",
            "absolute alpha normalization versus local drift",
            "A universal constant lambda_A_common may be absorbed/calibrated into measured alpha without producing local drift, but that is not a parent prediction of alpha's absolute value. Local tests care about D_v ln Z_Q_eff and arena products.",
            "EXACT_BOOKKEEPING_SPLIT",
            "Prevents the false move of claiming alpha prediction from calibration, while preserving local drift tests.",
            "parent value of C_P N_Q and no/fixed lambda_A for absolute prediction",
        ),
        (
            "MNT3809_6_strict_verdict",
            "strict current promotion",
            "The theorem shapes are exact, but the current corpus does not parent-sign C_P/N_Q descent, no-extra-F2, hidden-visible sequester, radiative/readout closure, or same-current arena maps.",
            "PASS_CONDITIONAL_FAIL_STRICT_CURRENT",
            "Alpha remains a finite product-level branch, not a local-GR/EM/WEP/R10 claim.",
            "MISSING_PARENT_NORM;MISSING_NO_EXTRA_F2;MISSING_RADIOUT_CLOSURE;MISSING_ALPHA_PRODUCT_INPUTS",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "status": status,
            "consequence": consequence,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for theorem_id, claim_piece, statement, status, consequence, missing in rows
    ]


def zqeff_rows(timestamp):
    rows = [
        ("ZQ3809_0_parent_norm", "C_P N_Q", "parent curvature/gauge-norm contribution", "zero if C_P and N_Q are parent-owned vertical-silent data", "UNSIGNED_SYMBOLIC_PARENT_PIECE", "MISSING_PARENT_NORM_OR_LEVEL"),
        ("ZQ3809_1_common_lambda", "lambda_A_common", "universal calibration contribution", "drift-zero if one universal constant, but not an alpha prediction", "CALIBRATION_ONLY_NOT_PREDICTION", "MISSING_NO_OR_FIXED_LAMBDA_FOR_VALUE_CLAIM"),
        ("ZQ3809_2_hidden_F2", "f_hid(I_hid) or f_X(X_Q)", "hidden/local scalar coefficient of F_Q^2", "zero only if no hidden-visible coefficient morphism or exact shift/product functor is signed", "UNSIGNED_COUNTEREXAMPLE", "MISSING_HIDDEN_VISIBLE_SEQUESTER"),
        ("ZQ3809_3_radiative", "Delta_rad(mu,X)", "loop/threshold/running effective counterterm", "zero only if effective action preserves parent coefficient domain", "UNSIGNED_COUNTEREXAMPLE", "MISSING_RADIOUT_CLOSURE"),
        ("ZQ3809_4_readout", "Delta_readout(rho,X)", "clock/spectrum/material readout contribution", "zero only if readout factors through q_obs and fixed representation data", "UNSIGNED_COUNTEREXAMPLE", "MISSING_READOUT_DESCENT"),
        ("ZQ3809_5_total", "Z_Q_eff", "total effective Maxwell normalization", "local alpha drift zero if all numerator drift pieces vanish and Z_Q_eff is finite", "FINITE_BRANCH_RETAINED", "MISSING_ALL_ZERO_CLAUSES_OR_SOURCE_BACKED_PRODUCT"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "term_id": term_id,
            "term": term,
            "meaning": meaning,
            "zero_condition": zero_condition,
            "current_status": status,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for term_id, term, meaning, zero_condition, status, missing in rows
    ]


def track_rows(timestamp):
    rows = [
        (
            "TRACK3809_N0",
            "normalization",
            "absolute alpha value",
            "alpha_EM measured/calibrated unless parent predicts C_P, N_Q, readout convention, and forbids/fixes lambda_A",
            "CALIBRATION_NOT_EVIDENCE",
            "do not claim alpha value prediction",
        ),
        (
            "TRACK3809_N1",
            "normalization",
            "parent alpha prediction",
            "requires parent-derived C_P N_Q plus no/fixed lambda_A and readout convention",
            "BLOCKED_PARENT_VALUE_NOT_DERIVED",
            "park as long-form parent-action target",
        ),
        (
            "TRACK3809_D0",
            "drift_product",
            "b_alpha=-D_v ln Z_Q_eff",
            "local alpha drift coefficient must be theorem-zero or source-backed numeric",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_SOURCE",
            "derive Z_Q_eff descent or source finite coefficient",
        ),
        (
            "TRACK3809_D1",
            "clock",
            "b_alpha*tau_clock_time",
            "clock rows bind only the product; no standalone b_alpha until tau_clock is parent-derived",
            "PRODUCT_BOUND_IMPORTED_NONCLAIM",
            "retain 2.1e-18 yr^-1 pressure row",
        ),
        (
            "TRACK3809_D2",
            "WEP",
            "beta_source_alpha*b_alpha*tau_WEP",
            "WEP alpha branch needs source normalization, material map, and tau_WEP",
            "PRODUCT_TARGET_NONCLAIM",
            "no clock-to-WEP shortcut",
        ),
        (
            "TRACK3809_D3",
            "R10",
            "K_X^R10(lambda)*beta_source*beta_test*tau_R10",
            "R10 branch needs numeric product and claim-valid alpha_bound(lambda)",
            "MISSING_R10_PRODUCT_AND_PROMOTED_BOUND",
            "symbolic rows remain runner-refused",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "track_id": track_id,
            "track": track,
            "quantity": quantity,
            "rule": rule,
            "current_status": status,
            "next_action": action,
            "valid_for_claim": "false",
        }
        for track_id, track, quantity, rule, status, action in rows
    ]


def product_rows(timestamp):
    rows = [
        ("APC3809_0_alpha_drift", "shared_alpha", "b_alpha=-D_v ln Z_Q_eff", "MISSING_THEOREM_ZERO_OR_SOURCE_BACKED_COEFFICIENT", "dimensionless", "derive Z_Q_eff descent or source finite b_alpha/c_alpha", "false"),
        ("APC3809_1_clock", "clock", "P_clock_alpha=b_alpha*tau_clock_time", "2.1e-18", "yr^-1", "tau_clock_time or direct MTS product prediction; no standalone division", "false"),
        ("APC3809_2_WEP", "MICROSCOPE_WEP", "P_WEP_alpha=beta_source_alpha*b_alpha*tau_WEP", "4.797780522732e-05", "dimensionless target", "beta_source_alpha, tau_WEP, material map, or direct parent product theorem", "false"),
        ("APC3809_3_R10", "R10_short_range", "P_R10_alpha(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)*tau_R10", "MISSING_CLAIM_VALID_BOUND_CURVE_AND_PRODUCT", "dimensionless alpha(lambda)", "lambda_X, K_X, beta_s, beta_t, tau_R10, epsilon_tail, promoted alpha_bound(lambda)", "false"),
        ("APC3809_4_same_current", "cross_arena", "same alpha branch/current/readout feeds clock WEP R10", "MISSING_PARENT_READOUT_FUNCTOR", "dimensionless consistency", "same-current owner plus readout/descent contract", "false"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "prediction_id": pred_id,
            "arena": arena,
            "product_symbol": symbol,
            "available_bound_or_status": bound,
            "units": units,
            "required_inputs": required,
            "valid_for_claim": valid,
        }
        for pred_id, arena, symbol, bound, units, required, valid in rows
    ]


def gate_rows(timestamp, grouped):
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    theorem_present = any(row["theorem_id"] == "MNT3809_4_ZQeff_descent" for row in grouped["theorem"])
    split_present = any(row["theorem_id"] == "MNT3809_5_absolute_value_split" for row in grouped["theorem"])
    rows = [
        ("CG3809_0_sources", all_sources, False, "all source needles found" if all_sources else "missing source or needle"),
        ("CG3809_1_parent_subblock", True, False, "parent inner-product subblock theorem emitted conditionally"),
        ("CG3809_2_ZQeff_descent", theorem_present, False, "Z_Q_eff descent theorem emitted conditionally"),
        ("CG3809_3_two_track_split", split_present, False, "absolute normalization versus local drift split emitted"),
        ("CG3809_4_parent_norm_signed", False, False, "C_P/N_Q descent is not strict-current signed"),
        ("CG3809_5_no_extra_F2_signed", False, False, "lambda_A/f_X F2 exclusion is not strict-current signed"),
        ("CG3809_6_readout_current_signed", False, False, "same-current/readout/radiative closure remains unsigned"),
        ("CG3809_7_products_score_ready", False, False, "finite alpha product rows still lack MTS predictions/projections"),
        ("CG3809_8_claims_closed", True, False, "no alpha/local-GR/WEP/R10/clock claim allowed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": gate_id,
            "pass": str(passed).lower(),
            "claim_allowed": str(claim_allowed).lower(),
            "details": details,
            "valid_for_claim": "false",
        }
        for gate_id, passed, claim_allowed, details in rows
    ]


def decision_rows(timestamp):
    rows = [
        (
            "DEC3809_0_result",
            "Maxwell normalization has a real conditional parent route.",
            "The parent inner-product subblock gives Z_parent=C_P N_Q and vertical silence follows by chain rule if C_P/N_Q are ObsRep/superselection data.",
            "Do not demand alpha's numerical value here; demand parent universality and no hidden drift.",
        ),
        (
            "DEC3809_1_blocker",
            "The strict route is still blocked by exactly named clauses.",
            "Rescaling, lambda_A/f_X F2, radiative/readout re-entry, and same-current/source maps remain open.",
            "Keep b_alpha/product rows nonclaim until Z_Q_eff descent is signed or finite product inputs are sourced.",
        ),
        (
            "DEC3809_2_next",
            "Attack parent-owned Z_Q_eff readout/descent contract next.",
            "One global descent/readout theorem could silence clock, WEP, and R10 alpha products without separate fitted coefficients.",
            "Move to 3810 parent-owned readout/descent contract or alpha product input acquisition.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": action,
            "valid_for_claim": "false",
        }
        for decision_id, decision, because, action in rows
    ]


def next_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md",
            "target_script": "scripts/Y5_R2FR_3810_parent_owned_ZQeff_readout_descent_contract_or_alpha_product_inputs.py",
            "objective": "Try to construct the global parent-owned readout/descent contract that makes Z_Q_eff=Zbar(q_obs,theta_rep) and keeps alpha readout, same current, and radiative reductions inside the same branch; if it fails, begin finite alpha product input acquisition under the strict 3809 contract.",
            "avoid": "do not claim absolute alpha prediction; do not divide clock bounds by assumed tau; do not transfer clock to WEP/R10 without source/readout maps; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_MAXWELL_NORMALIZATION_ZQEFF_DESCENT_THEOREM_ALPHA_FINITE_BRANCH_RETAINED",
            "summary": "3809 derives the conditional parent Maxwell inner-product and Z_Q_eff descent theorem, separates absolute alpha normalization from local alpha drift, and keeps alpha product rows nonclaim because parent norm/no-F2/readout/current clauses remain unsigned.",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(timestamp, grouped):
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            load_csv(path)
    fwb_hits = list(FWB.rglob("*3809*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3809 markdown document written"),
        ("parent_subblock_present", any(row["theorem_id"] == "MNT3809_0_parent_inner_product" for row in grouped["theorem"]), "parent inner-product theorem emitted"),
        ("ZQeff_descent_present", any(row["theorem_id"] == "MNT3809_4_ZQeff_descent" for row in grouped["theorem"]), "Z_Q_eff descent theorem emitted"),
        ("two_track_split_present", any(row["theorem_id"] == "MNT3809_5_absolute_value_split" for row in grouped["theorem"]), "absolute normalization/local drift split emitted"),
        ("counterterms_retained", any(row["term_id"] == "ZQ3809_5_total" for row in grouped["zqeff"]), "Z_Q_eff finite branch retained"),
        ("products_nonclaim", all(row["valid_for_claim"] == "false" for row in grouped["products"]), "finite alpha products remain nonclaim"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("formalization_clean", not fwb_hits, "no 3809 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


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
        "# 3809 - Maxwell Normalization From Parent Inner Product Or Alpha Finite Branch",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_MAXWELL_NORMALIZATION_ZQEFF_DESCENT_THEOREM_ALPHA_FINITE_BRANCH_RETAINED`.",
        "",
        "3809 folds the older alpha chain back into the current local-GR spine. The useful theorem is clean: a parent inner product can supply `Z_parent=C_P N_Q`, and if the full effective Maxwell normalization descends as `Z_Q_eff=Zbar(q_obs,theta_rep)`, then local vertical alpha drift vanishes by chain rule.",
        "",
        "The important split is now explicit: absolute measured `alpha` is a normalization/calibration track unless the parent fixes `C_P N_Q` and forbids/fixes `lambda_A`; local tests are a drift/product track governed by `b_alpha=-D_v ln Z_Q_eff` and the clock/WEP/R10 product maps.",
        "",
        "Current result is nonclaim. `C_P/N_Q`, no-extra-`F^2`, hidden-visible sequester, radiative/readout closure, and same-current arena maps are still unsigned, so alpha remains a finite product-level branch.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Maxwell Normalization Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("ZQeff Decomposition", "zqeff", ["term_id", "term"]),
        ("Alpha Two-Track Ledger", "tracks", ["track_id", "quantity"]),
        ("Finite Alpha Product Contract", "products", ["prediction_id", "arena"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
        lines.append("")
    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "zqeff": zqeff_rows(timestamp),
        "tracks": track_rows(timestamp),
        "products": product_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
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
