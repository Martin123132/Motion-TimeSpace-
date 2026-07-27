from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "987_doc",
            "path": "987-Y5-R10-Coulomb-to-alphaEM-normal-form-or-parent-zero-gate.md",
            "role": "immediate handoff: Coulomb/WEP routes to b_theta_alpha_EM",
            "needle": "CLEAN_FINITE_ROUTE_BUT_PARENT_UNSIGNED",
        },
        {
            "source_id": "646_clock_sources",
            "path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "role": "source-backed clock alpha sensitivity pairs",
            "needle": "CAS646_1_YbE3E2",
        },
        {
            "source_id": "647_clock_product",
            "path": "source-intake/mts_residuals/P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
            "role": "clock product bounds on kappa_alpha times tau_clock",
            "needle": "CPB647_1_YbE3E2",
        },
        {
            "source_id": "647_H0_diagnostic",
            "path": "source-intake/mts_residuals/P8_Y5_R10_647_H0_NORMALIZED_DIAGNOSTIC.csv",
            "role": "H0-normalized diagnostic for clock product bound",
            "needle": "H0D647_1_YbE3E2",
        },
        {
            "source_id": "650_screen_rule",
            "path": "source-intake/mts_residuals/P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv",
            "role": "same-screen/no-clock-only alpha branch policy",
            "needle": "USR650_0_shared_screen_variable",
        },
        {
            "source_id": "651_WEP_stress",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv",
            "role": "WEP alpha/Coulomb pressure and beta_source target",
            "needle": "WAS651_0_alpha_Coulomb",
        },
        {
            "source_id": "651_DD_charge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv",
            "role": "Damour-Donoghue style source-backed Coulomb charge estimates",
            "needle": "Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb",
        },
        {
            "source_id": "765_vertical_norm",
            "path": "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md",
            "role": "EM-lock theorem shape and lambda_F2 counterexample",
            "needle": "VGN765_5_alpha_zero_conditional",
        },
        {
            "source_id": "767_no_alpha_vertex",
            "path": "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
            "role": "no-alpha-vertex and WEP closure quarantine after alpha pressure",
            "needle": "PMR767_3_no_alpha_mass_vertex",
        },
        {
            "source_id": "448_constant_hazard",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "constant-sector warning: alpha_EM direct vertices remain hazards",
            "needle": "alpha_EM(Z)",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def joint_alpha_variable_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "JAV988_0_alpha_slot",
            "object": "b_alpha := d ln alpha_EM / d Xhat",
            "clock_form": "enters d ln(nu_a/nu_b) through delta_K_alpha*b_alpha*tau_clock",
            "WEP_form": "enters eta_AB through DeltaQ_alpha_AB*beta_source_alpha*b_alpha*tau_WEP",
            "current_status": "same_symbol_identified_not_parent_normalized",
            "blocker": "Xhat/chi_X normalization, tau_clock/tau_WEP, and beta_source_alpha are not parent-owned",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "JAV988_1_clock_product",
            "object": "clock product bound",
            "clock_form": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 from Yb+ E3/E2 bookkeeping row",
            "WEP_form": "does not by itself bound WEP because WEP also needs source normalization",
            "current_status": "source_backed_product_bound_nonclaim",
            "blocker": "standalone b_alpha requires derived tau_clock dynamics",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "JAV988_2_WEP_product",
            "object": "WEP alpha/Coulomb force product",
            "clock_form": "same local alpha branch if finite alpha survives",
            "WEP_form": "eta_alpha ~= DeltaQ_alpha*beta_source_alpha*b_alpha*tau_WEP",
            "current_status": "stress_test_pressure_not_pass",
            "blocker": "unit source normalization overshoots MICROSCOPE in the 651 smoke model",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "JAV988_3_cross_arena_policy",
            "object": "shared local alpha screen/domain classifier",
            "clock_form": "S_lab_alpha cannot be clock-only",
            "WEP_form": "same parent screen/domain rule must be used in WEP/R10/local EM unless a theorem-zero replaces it",
            "current_status": "policy_gate_active",
            "blocker": "D_parent(domain) and local silence are not derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "JAV988_4_normalization_warning",
            "object": "Coulomb sensitivity normalization",
            "clock_form": "clock K_alpha values are dimensionless sensitivity coefficients",
            "WEP_form": "987 rough Coulomb proxy and 651 Damour-Donoghue charge are not the same unit system",
            "current_status": "normalization_collision_quarantined",
            "blocker": "do not mix 987 proxy DeltaQ with 651 DD charge without an explicit conversion theorem",
            "valid_for_claim": "false",
        },
    ]


def clock_product_import_rows() -> list[dict[str, str]]:
    product_rows = read_csv_rows(OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv")
    diagnostic_rows = {
        row.get("clock_pair_id", ""): row
        for row in read_csv_rows(OUT / "P8_Y5_R10_647_H0_NORMALIZED_DIAGNOSTIC.csv")
    }
    imported: list[dict[str, str]] = []
    for row in product_rows:
        diagnostic = diagnostic_rows.get(row.get("clock_pair_id", ""), {})
        imported.append(
            {
                "import_id": f"CLOCK988_{row.get('clock_pair_id', 'unknown')}",
                "clock_pair": row.get("clock_pair", ""),
                "product_bound_1sigma_yr_inv": row.get("conservative_abs_product_bound_1sigma_yr_inv", ""),
                "product_bound_2sigma_yr_inv": row.get("conservative_abs_product_bound_2sigma_yr_inv", ""),
                "H0_normalized_1sigma_if_assumed": diagnostic.get("bound_on_abs_kappa_times_dchi_dN_1sigma", ""),
                "interpretation": "bounds b_alpha*tau_clock_time only; H0-normalized value is diagnostic unless tau_clock=H0*dchi/dN is derived",
                "standalone_b_alpha_bound_ready": "false",
                "valid_for_claim": "false",
            }
        )
    return imported


def WEP_alpha_pressure_rows() -> list[dict[str, str]]:
    stress_rows = read_csv_rows(OUT / "P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv")
    imported: list[dict[str, str]] = []
    for row in stress_rows:
        imported.append(
            {
                "import_id": f"WEP988_{row.get('stress_id', 'unknown')}",
                "channel": row.get("channel", ""),
                "eta_bound_used": row.get("eta_bound_used", ""),
                "delta_Q_abs": row.get("delta_Q_TA6V_minus_PtRh10_abs", ""),
                "unit_source_eta_prediction": row.get("unit_source_eta_prediction", ""),
                "overshoot_factor_vs_MICROSCOPE": row.get("overshoot_factor_vs_MICROSCOPE", ""),
                "required_abs_beta_source_max": row.get("required_abs_beta_source_max", ""),
                "verdict": row.get("verdict", ""),
                "score_ready": "false",
                "valid_for_claim": "false",
            }
        )
    return imported


def normalization_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "norm_id": "NORM988_0_proxy_collision",
            "quantity": "DeltaQ_Coulomb",
            "987_value_or_form": "-2.574514671e+00 rough proxy from 983/987 symbolic route",
            "651_value_or_form": "-1.989808886825e-03 Damour-Donoghue style alpha/Coulomb charge",
            "rule": "use 651 for source-backed WEP stress; use 987 only as route/proxy unless a conversion map is written",
            "status": "quarantined_no_claim",
            "valid_for_claim": "false",
        },
        {
            "norm_id": "NORM988_1_time_vs_force_units",
            "quantity": "clock product versus WEP eta",
            "987_value_or_form": "b_alpha*profile_X",
            "651_value_or_form": "beta_source_alpha*b_alpha*tau_WEP",
            "rule": "yr^-1 clock bounds cannot be applied to dimensionless WEP eta without tau/domain/source maps",
            "status": "units_gate_blocks_shortcut",
            "valid_for_claim": "false",
        },
        {
            "norm_id": "NORM988_2_beta_source_not_screen",
            "quantity": "beta_source_alpha",
            "987_value_or_form": "P_C_alpha/profile_X placeholder",
            "651_value_or_form": "<=4.797780522732e-05 alpha-only or <=2.887280314062e-05 robust surface-including target",
            "rule": "beta_source_alpha is a source/force normalization debt, not the clock screen S_lab_alpha",
            "status": "finite_branch_debt_written",
            "valid_for_claim": "false",
        },
    ]


def EM_lock_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "EMLOCK988_0_parent_charge_generator",
            "required_signature": "compact parent charge generator T_Q is a varied parent-action object with fixed lattice normalization",
            "if_signed": "charge unit cannot be rescaled by hand",
            "current_status": "not_parent_signed",
            "blocker": "T_Q exists as theorem shape only, not as an owned parent field in the current corpus",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "EMLOCK988_1_unique_Maxwell_F2",
            "required_signature": "observed F_Q^2 is inherited only from the parent curvature norm",
            "if_signed": "g_EM is fixed by the parent norm instead of an independent alpha source",
            "current_status": "failed_current_corpus",
            "blocker": "lambda_A F_Q^2 counterterm remains legal unless forbidden by parent symmetry",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "EMLOCK988_2_current_owner",
            "required_signature": "matter current, charge labels, and Maxwell source normalization descend from the same T_Q owner",
            "if_signed": "WEP/R10 source-test charge normalization cannot float independently",
            "current_status": "not_parent_signed",
            "blocker": "current rescaling counterexample remains open",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "EMLOCK988_3_readout_descent",
            "required_signature": "Hodge star, coframe, and hbar*c readout are quotient-fixed for dimensionless alpha_EM",
            "if_signed": "clock/spectroscopy alpha drift cannot re-enter through units",
            "current_status": "not_parent_signed",
            "blocker": "coframe/Hodge/readout leak remains possible",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "EMLOCK988_4_no_alpha_vertex",
            "required_signature": "no alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), or binding-response vertex survives in S_matter",
            "if_signed": "composition-dependent Coulomb channel is theorem-zero locally",
            "current_status": "not_parent_signed",
            "blocker": "parent matter functor/no-alpha-vertex remains an explicit closure, not a derivation",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "EMLOCK988_5_theorem_verdict",
            "required_signature": "EMLOCK988_0 through EMLOCK988_4 are all parent-signed",
            "if_signed": "b_theta_alpha_EM=0 and both WEP alpha/Coulomb and clock alpha channels close structurally",
            "current_status": "conditional_exact_but_not_promoted",
            "blocker": "unique F2, current owner, readout descent, and no-alpha vertex are unsigned",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG988_0_btheta_alpha_bound",
            "claim": "MTS has a numeric b_theta_alpha_EM bound",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "clock gives product bounds only and WEP needs beta_source/tau normalization",
        },
        {
            "gate_id": "CG988_1_clock_pass",
            "claim": "MTS passes clock/fine-structure tests",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "tau_clock dynamics or EM-lock theorem is missing",
        },
        {
            "gate_id": "CG988_2_WEP_pass",
            "claim": "MTS passes MICROSCOPE/WEP alpha channel",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "unit-source finite alpha route fails 651 stress; needs beta_source suppression or zero theorem",
        },
        {
            "gate_id": "CG988_3_EM_lock_zero",
            "claim": "EM-lock theorem proves b_theta_alpha_EM=0",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "the theorem is exact as a contract but parent signatures are not supplied",
        },
        {
            "gate_id": "CG988_4_local_GR",
            "claim": "alpha branch closes local GR/Newton/PPN",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "even alpha silence does not replace the EH/PPN/source-normalization derivation",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC988_0_joint_gate",
            "topic": "finite alpha route",
            "result": "alpha route is not killed but is now cross-arena expensive",
            "reason": "same b_alpha must face clocks, WEP, R10, and local EM without arena-specific screens",
            "next_action": "prefer theorem-zero/EM-lock over fitted suppression where possible",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC988_1_safest_route",
            "topic": "least-scrutiny path",
            "result": "EM-lock theorem is the cleanest route if parent signatures can be found",
            "reason": "exact zero from parent Maxwell inheritance beats a tuned beta_source_alpha story",
            "next_action": "hunt T_Q, unique F2, current owner, and readout descent signatures",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC988_2_fallback_route",
            "topic": "finite route if EM-lock fails",
            "result": "source-normalization owner must supply beta_source_alpha suppression",
            "reason": "651 requires roughly <=4.8e-05 alpha-only or <=2.887e-05 robust surface-including beta target in the smoke model",
            "next_action": "derive beta_source_alpha from parent source functional or mark finite alpha as closure-only",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC988_3_best_next",
            "topic": "next checkpoint",
            "result": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
            "reason": "this directly attacks the missing coupling owner rather than running more unowned tests",
            "next_action": "write 989 EM-lock signature/input owner audit with beta_source fallback",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
            "objective": "try to parent-sign the EM-lock theorem clauses; if any fail, identify the exact source-normalization owner needed for beta_source_alpha suppression",
            "include": "T_Q owner, unique Maxwell F2 gate, charge-current owner, readout descent, no-alpha vertex, beta_source_alpha fallback target",
            "exclude": "clock pass, WEP pass, b_theta_alpha claim, invented beta_source values, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def is_positive_number(value: str) -> bool:
    try:
        return float(value) > 0.0
    except (TypeError, ValueError):
        return False


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    joint_alpha: list[dict[str, str]],
    clocks: list[dict[str, str]],
    WEP_rows: list[dict[str, str]],
    normalization: list[dict[str, str]],
    EM_lock: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    joint_ok = any(row["gate_id"] == "JAV988_0_alpha_slot" for row in joint_alpha) and all(row["valid_for_claim"] == "false" for row in joint_alpha)
    clock_ok = any(row["clock_pair"] == "171Yb+ E3 / 171Yb+ E2" and is_positive_number(row["product_bound_1sigma_yr_inv"]) for row in clocks)
    WEP_ok = any(row["import_id"] == "WEP988_WAS651_0_alpha_Coulomb" and is_positive_number(row["required_abs_beta_source_max"]) for row in WEP_rows)
    norm_ok = any(row["norm_id"] == "NORM988_0_proxy_collision" and row["status"] == "quarantined_no_claim" for row in normalization)
    EM_lock_ok = any(row["clause_id"] == "EMLOCK988_5_theorem_verdict" and row["current_status"] == "conditional_exact_but_not_promoted" for row in EM_lock)
    claims_ok = all(row["claim_allowed"] == "false" and row["gate_pass"] == "false" for row in claims)
    decision_ok = any(row["decision_id"] == "DEC988_3_best_next" and "989-Y5-R10" in row["result"] for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V988_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all local source files exist and needles are found"},
        {"check_id": "V988_1_joint_alpha_gate", "result": "pass" if joint_ok else "fail", "detail": "single alpha slot is written as cross-arena nonclaim"},
        {"check_id": "V988_2_clock_product_import", "result": "pass" if clock_ok else "fail", "detail": "Yb clock product bound imported as product-only"},
        {"check_id": "V988_3_WEP_pressure_import", "result": "pass" if WEP_ok else "fail", "detail": "WEP alpha beta_source target imported as nonclaim pressure"},
        {"check_id": "V988_4_normalization_quarantine", "result": "pass" if norm_ok else "fail", "detail": "987/651 Coulomb normalization mismatch is explicitly quarantined"},
        {"check_id": "V988_5_EM_lock_nonclaim", "result": "pass" if EM_lock_ok else "fail", "detail": "EM-lock theorem is conditional exact but not promoted"},
        {"check_id": "V988_6_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "clock/WEP/btheta/local-GR claims are blocked"},
        {"check_id": "V988_7_next_decision", "result": "pass" if decision_ok else "fail", "detail": "989 EM-lock signature/source-normalization target selected"},
        {"check_id": "V988_8_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V988_9_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V988_READY",
            "result": "pass" if ready else "fail",
            "detail": "988 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    joint_alpha: list[dict[str, str]],
    clocks: list[dict[str, str]],
    WEP_rows: list[dict[str, str]],
    normalization: list[dict[str, str]],
    EM_lock: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 988 Y5 R10: AlphaEM WEP Clock Joint Prior Or EM-Lock Theorem",
        "",
        "Status: `Y5_R10_988_alphaEM_WEP_clock_joint_gate_written_EM_lock_conditional_not_parent_signed_nonclaim`",
        "",
        "Claim ceiling: no clock pass, no WEP pass, no `b_theta_alpha_EM` bound, no EM-lock zero claim, no local-GR claim.",
        "",
        "## Readout",
        "",
        "988 ties the 987 Coulomb/WEP route to the older clock and WEP pressure chain. The finite alpha branch is not dead, but it is no longer allowed to hide in one arena: the same alpha variable must face clocks, WEP, R10, and local EM with consistent normalization.",
        "",
        "The cleanest route remains a parent-signed EM-lock theorem. If the parent owns the charge generator, Maxwell kinetic term, current normalization, readout descent, and no-alpha vertex, then `b_theta_alpha_EM=0`. Current files do not sign those clauses, so this is a contract, not a claim.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Joint Alpha Variable Gate",
        "",
        md_table(joint_alpha, ["gate_id", "object", "clock_form", "WEP_form", "current_status", "blocker", "valid_for_claim"]),
        "",
        "## Clock Product Import",
        "",
        md_table(clocks, ["import_id", "clock_pair", "product_bound_1sigma_yr_inv", "product_bound_2sigma_yr_inv", "H0_normalized_1sigma_if_assumed", "interpretation", "standalone_b_alpha_bound_ready", "valid_for_claim"]),
        "",
        "## WEP Alpha Pressure Import",
        "",
        md_table(WEP_rows, ["import_id", "channel", "eta_bound_used", "delta_Q_abs", "unit_source_eta_prediction", "overshoot_factor_vs_MICROSCOPE", "required_abs_beta_source_max", "verdict", "score_ready", "valid_for_claim"]),
        "",
        "## Normalization Gates",
        "",
        md_table(normalization, ["norm_id", "quantity", "987_value_or_form", "651_value_or_form", "rule", "status", "valid_for_claim"]),
        "",
        "## EM-Lock Theorem Gate",
        "",
        md_table(EM_lock, ["clause_id", "required_signature", "if_signed", "current_status", "blocker", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    joint_alpha = joint_alpha_variable_rows()
    clocks = clock_product_import_rows()
    WEP_rows = WEP_alpha_pressure_rows()
    normalization = normalization_gate_rows()
    EM_lock = EM_lock_theorem_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, joint_alpha, clocks, WEP_rows, normalization, EM_lock, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_988_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv", joint_alpha)
    write_csv(OUT / "P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv", clocks)
    write_csv(OUT / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", WEP_rows)
    write_csv(OUT / "P8_Y5_R10_988_NORMALIZATION_GATES.csv", normalization)
    write_csv(OUT / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv", EM_lock)
    write_csv(OUT / "P8_Y5_R10_988_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_988_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_988_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_988_VALIDATION.csv", validation)
    write_doc(sources, joint_alpha, clocks, WEP_rows, normalization, EM_lock, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
