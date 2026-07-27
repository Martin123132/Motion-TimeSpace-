from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "982-Y5-R10-coupling-bound-projection-matrix-skeleton-and-screening-runner.md"
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
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "981_doc",
            "path": "981-Y5-R10-finite-coupling-prior-source-acquisition-bkappa-Gdot-alpha3.md",
            "role": "handoff selecting projection matrix/screening runner",
            "needle": "DEC981_3_best_next",
        },
        {
            "source_id": "981_candidates",
            "path": "source-intake/mts_residuals/P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv",
            "role": "source-backed observational candidate bounds",
            "needle": "CP981_0_b_kappa_species_split_WEP",
        },
        {
            "source_id": "981_web_sources",
            "path": "source-intake/mts_residuals/P8_Y5_R10_981_WEB_SOURCE_LEDGER.csv",
            "role": "web provenance ledger",
            "needle": "WEB981_1_LLR_GDOT",
        },
        {
            "source_id": "981_anchor_reconciliation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_981_LOCAL_ANCHOR_RECONCILIATION.csv",
            "role": "local anchor/source reconciliation",
            "needle": "LAR981_1_417_alpha3",
        },
        {
            "source_id": "980_fallback",
            "path": "source-intake/mts_residuals/P8_Y5_R10_980_FINITE_PRIOR_FALLBACK.csv",
            "role": "finite-prior fallback selected after no-marker theorem rejection",
            "needle": "FP980_0_b_kappa_species_split",
        },
        {
            "source_id": "979_priority",
            "path": "source-intake/mts_residuals/P8_Y5_R10_979_QBAR_PRIOR_SOURCE_PRIORITY.csv",
            "role": "coupling-prior priority rows",
            "needle": "QPRI979_2_K_boundary_alpha3",
        },
        {
            "source_id": "978_qbar_rows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_978_QBAR_SOURCE_PRIOR_RUNNER_ROWS.csv",
            "role": "qbar/source prior row schema",
            "needle": "QSP978_4_species_source_weight",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "parent matter sector component definitions",
            "needle": "PMC622_5_universal_source",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "alpha3/Gdot local anchor source",
            "needle": "alpha3_flux",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def coefficient_slots() -> list[dict[str, str]]:
    return [
        {
            "coefficient_id": "COEF982_0_b_kappa_source_weight",
            "component": "b_kappa",
            "parameter": "species_source_weight_splitting",
            "meaning": "composition/species dependence of active gravitational source normalization",
            "current_status": "MISSING_PARENT_UNIVERSAL_SOURCE_OR_NUMERIC_PROJECTION",
            "units": "dimensionless",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF982_1_b_kappa_running",
            "component": "b_kappa",
            "parameter": "d_ln_Geff_dXhat_or_dlnGdt",
            "meaning": "local/environmental running of effective gravitational coupling",
            "current_status": "MISSING_XHAT_TIME_ENVIRONMENT_MAP",
            "units": "dimensionless per Xhat or yr^-1",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF982_2_b_theta_constants",
            "component": "b_theta",
            "parameter": "d_ln_alpha_EM_dXhat and d_ln_mass_ratio_dXhat",
            "meaning": "MTS dependence of ordinary matter constants",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_CLOCK_EM_PRIOR",
            "units": "dimensionless",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF982_3_b_m_marker",
            "component": "b_m",
            "parameter": "marker_coupling_projection",
            "meaning": "unclassified material/quotient marker coupling",
            "current_status": "MISSING_MARKER_TAXONOMY_OR_BOUND",
            "units": "dimensionless",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF982_4_K_boundary_alpha3",
            "component": "boundary_alpha3_flux",
            "parameter": "K_boundary_alpha3",
            "meaning": "boundary/local projection into preferred-frame alpha3-like residual",
            "current_status": "MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX",
            "units": "dimensionless",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "COEF982_5_qbarXT_vec",
            "component": "qbarXT_vec",
            "parameter": "P_A_qbarXT_vec",
            "meaning": "ordinary/local test-body residual vector after failed theorem-zero route",
            "current_status": "MISSING_K_X_QBAR_XH_LAMBDA_AND_BOUND_CURVE",
            "units": "dimensionless vector projection",
            "valid_for_claim": "false",
        },
    ]


def projection_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "projection_id": "PMAT982_0_WEP_eta_TiPt",
            "observable": "eta_TiPt",
            "source_prior": "CP981_0_b_kappa_species_split_WEP",
            "screening_bound": "6.992e-15",
            "bound_units": "dimensionless",
            "projection_formula": "eta_TiPt = S_TiPt_bkappa*b_kappa + S_TiPt_btheta*b_theta + S_TiPt_bm*b_m + S_TiPt_bNH*b_NH",
            "required_projection_inputs": "S_TiPt_bkappa,S_TiPt_btheta,S_TiPt_bm,S_TiPt_bNH,composition_charge_basis",
            "missing_marker": "MISSING_SOURCE_CHARGE_PROJECTION",
            "runner_status": "not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PMAT982_1_Gdot_orbital",
            "observable": "Gdot_over_G",
            "source_prior": "CP981_1_kappa_running_Gdot",
            "screening_bound": "2.420e-14",
            "bound_units": "yr^-1",
            "projection_formula": "Gdot/G = (d ln Geff/d Xhat)*(d Xhat/dt)_local + B_boundary_time",
            "required_projection_inputs": "dXhat_dt_local,environment_profile,clock_or_orbital_epoch_map,B_boundary_time",
            "missing_marker": "MISSING_ENVIRONMENT_PROFILE_AND_XHAT_TIME_MAP",
            "runner_status": "not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PMAT982_2_alpha3_strong_pulsar",
            "observable": "alpha3_hat_strong",
            "source_prior": "CP981_2_alpha3_strong_pulsar",
            "screening_bound": "4.000e-20",
            "bound_units": "dimensionless",
            "projection_formula": "alpha3_hat = P_strong_boundary*K_boundary_alpha3 + P_strong_bkappa*b_kappa + P_strong_spin*B_spin",
            "required_projection_inputs": "strong_to_local_matching,P_strong_boundary,P_strong_bkappa,P_strong_spin,compactness_sensitivity",
            "missing_marker": "MISSING_STRONG_TO_LOCAL_PPN_PROJECTION",
            "runner_status": "not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PMAT982_3_alpha3_weak_solar",
            "observable": "alpha3_weak_solar",
            "source_prior": "CP981_3_alpha3_weak_solar",
            "screening_bound": "6.000e-10",
            "bound_units": "dimensionless",
            "projection_formula": "alpha3_weak = P_weak_boundary*K_boundary_alpha3 + P_weak_bkappa*b_kappa + P_weak_frame*b_g",
            "required_projection_inputs": "P_weak_boundary,P_weak_bkappa,P_weak_frame,local_preferred_frame_map",
            "missing_marker": "MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX",
            "runner_status": "not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "projection_id": "PMAT982_4_R10_alpha_lambda",
            "observable": "alpha_lambda_R10",
            "source_prior": "QSP978_7_qbarXT_vec plus R10 bound curve",
            "screening_bound": "MISSING_REAL_ALPHA_LAMBDA_BOUND_FOR_THIS_ROW",
            "bound_units": "dimensionless",
            "projection_formula": "alpha_pred(lambda)=K_X*Qbar_XH(lambda)*P_A_qbarXT_vec",
            "required_projection_inputs": "K_X,Qbar_XH(lambda),P_A_qbarXT_vec,lambda_X,source_backed_alpha_bound(lambda)",
            "missing_marker": "MISSING_R10_PARENT_COEFFICIENTS_AND_BOUND_CURVE",
            "runner_status": "not_scoreable",
            "valid_for_claim": "false",
        },
    ]


def screening_runner_rows(projections: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for projection in projections:
        missing_inputs = [
            item.strip()
            for item in projection["required_projection_inputs"].split(",")
            if item.strip()
        ]
        has_numeric_bound = projection["screening_bound"].replace(".", "", 1).replace("e-", "", 1).replace("e+", "", 1).isdigit()
        scoreable = has_numeric_bound and projection["missing_marker"] == ""
        rows.append(
            {
                "screen_id": projection["projection_id"].replace("PMAT", "SCREEN"),
                "observable": projection["observable"],
                "source_prior": projection["source_prior"],
                "numeric_bound_present": flag(has_numeric_bound),
                "projection_inputs_missing_count": str(len(missing_inputs)),
                "missing_marker": projection["missing_marker"],
                "screen_result": "would_score_if_projection_supplied" if scoreable else "blocked_missing_projection",
                "claim_allowed": "false",
                "detail": "screening bound is a source anchor only; MTS coefficient projection is not supplied",
                "valid_for_claim": "false",
            }
        )
    return rows


def identity_sanity_rows() -> list[dict[str, str]]:
    return [
        {
            "sanity_id": "IS982_0_WEP_identity",
            "observable": "eta_TiPt",
            "identity_assumption": "S_TiPt_bkappa=1 and all other sensitivities zero",
            "identity_bound_on_slot": "abs(b_kappa) <= 6.992e-15",
            "why_not_claim": "composition/source-charge projection is not derived; identity assumption is a debug convention only",
            "valid_for_claim": "false",
        },
        {
            "sanity_id": "IS982_1_Gdot_identity",
            "observable": "Gdot_over_G",
            "identity_assumption": "dXhat/dt=1 yr^-1 and no boundary term",
            "identity_bound_on_slot": "abs(d_ln_Geff/dXhat) <= 2.420e-14",
            "why_not_claim": "Xhat time/environment map is missing",
            "valid_for_claim": "false",
        },
        {
            "sanity_id": "IS982_2_alpha3hat_identity",
            "observable": "alpha3_hat_strong",
            "identity_assumption": "P_strong_boundary=1 and no strong/local mismatch",
            "identity_bound_on_slot": "abs(K_boundary_alpha3) <= 4.000e-20",
            "why_not_claim": "strong-field alpha3_hat is not automatically local weak-field alpha3",
            "valid_for_claim": "false",
        },
        {
            "sanity_id": "IS982_3_alpha3weak_identity",
            "observable": "alpha3_weak_solar",
            "identity_assumption": "P_weak_boundary=1 and other channels zero",
            "identity_bound_on_slot": "abs(K_boundary_alpha3) <= 6.000e-10",
            "why_not_claim": "weak-field projection matrix is missing and source is preliminary",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE982_0_projection_matrix_written",
            "claim": "projection matrix skeleton exists",
            "gate_pass": "true",
            "claim_allowed": "false",
            "why_not": "skeleton existence is not a physics pass",
        },
        {
            "gate_id": "CGATE982_1_WEP_score",
            "claim": "b_kappa is bounded by MICROSCOPE",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "source-charge/composition sensitivity matrix is missing",
        },
        {
            "gate_id": "CGATE982_2_Gdot_score",
            "claim": "kappa-running branch is bounded",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "Xhat time/environment map is missing",
        },
        {
            "gate_id": "CGATE982_3_alpha3_score",
            "claim": "K_boundary_alpha3 is bounded",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "strong/weak alpha3 projection matrices are missing",
        },
        {
            "gate_id": "CGATE982_4_R10_score",
            "claim": "R10 alpha(lambda) branch is scoreable",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "K_X, Qbar_XH(lambda), P_A qbarXT vector, lambda_X, and source-backed bound curve are missing",
        },
        {
            "gate_id": "CGATE982_5_local_GR",
            "claim": "local GR/Newton/PPN/R10 branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "screening-only runner blocks every arena while projections are missing",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC982_0_matrix",
            "topic": "projection discipline",
            "result": "projection_matrix_skeleton_written",
            "reason": "each observational anchor now has an explicit map from MTS coefficient slots to measured channel",
            "next_action": "fill one projection map rather than adding more source anchors",
        },
        {
            "decision_id": "DEC982_1_screening_runner",
            "topic": "runner status",
            "result": "screening_runner_blocks_all_claims",
            "reason": "numeric source bounds exist but every row has missing MTS projection inputs",
            "next_action": "keep identity assumptions as debug-only rows",
        },
        {
            "decision_id": "DEC982_2_best_next",
            "topic": "next checkpoint",
            "result": "WEP_source_charge_projection_first",
            "reason": "WEP/source-splitting is the most direct b_kappa pressure and maps onto the universal-source theorem gap",
            "next_action": "write 983 WEP/source-charge projection matrix attempt for MICROSCOPE Ti/Pt",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "983-Y5-R10-WEP-source-charge-projection-matrix-MICROSCOPE-TiPt.md",
            "objective": "derive or skeletonize the composition/source-charge projection from MICROSCOPE Ti/Pt eta into MTS b_kappa, b_theta, and marker slots",
            "include": "Ti/Pt composition sensitivity placeholders, b_kappa vs b_theta separation, source-charge basis, nonclaim screening row",
            "exclude": "claiming WEP pass, invented composition coefficients, local-GR promotion, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    projections: list[dict[str, str]],
    screens: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    coefficient_nonclaim_ok = all(row["valid_for_claim"] == "false" and row["current_status"].startswith("MISSING_") for row in coefficients)
    projection_nonclaim_ok = all(row["valid_for_claim"] == "false" and row["missing_marker"].startswith("MISSING_") for row in projections)
    screen_blocks_ok = all(row["screen_result"] == "blocked_missing_projection" and row["claim_allowed"] == "false" for row in screens)
    identity_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in identity_rows)
    claims_ok = all(row["claim_allowed"] == "false" for row in claims)
    next_decision_ok = any(row["decision_id"] == "DEC982_2_best_next" and row["result"] == "WEP_source_charge_projection_first" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {
            "check_id": "V982_0_sources",
            "result": "pass" if sources_ok else "fail",
            "detail": "all local handoff/source files exist and needles are found",
        },
        {
            "check_id": "V982_1_coefficients_nonclaim",
            "result": "pass" if coefficient_nonclaim_ok else "fail",
            "detail": "coefficient slots are explicit missing-input nonclaim rows",
        },
        {
            "check_id": "V982_2_projection_rows_nonclaim",
            "result": "pass" if projection_nonclaim_ok else "fail",
            "detail": "projection rows keep MISSING_* markers",
        },
        {
            "check_id": "V982_3_screening_blocks",
            "result": "pass" if screen_blocks_ok else "fail",
            "detail": "screening runner blocks every claim while projections are missing",
        },
        {
            "check_id": "V982_4_identity_rows_nonclaim",
            "result": "pass" if identity_nonclaim_ok else "fail",
            "detail": "identity sanity rows are debug-only nonclaim rows",
        },
        {
            "check_id": "V982_5_claim_gates_safe",
            "result": "pass" if claims_ok else "fail",
            "detail": "claim gates do not allow local-GR or coefficient-bound claims",
        },
        {
            "check_id": "V982_6_next_decision",
            "result": "pass" if next_decision_ok else "fail",
            "detail": "983 WEP/source-charge projection selected",
        },
        {
            "check_id": "V982_7_next_target_written",
            "result": "pass" if next_ok else "fail",
            "detail": "next target row is present and nonclaim",
        },
        {
            "check_id": "V982_8_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
        },
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V982_READY",
            "result": "pass" if ready else "fail",
            "detail": "982 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    projections: list[dict[str, str]],
    screens: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 982 Y5 R10: Coupling Bound Projection Matrix Skeleton And Screening Runner",
        "",
        "Status: `Y5_R10_982_projection_matrix_skeleton_written_screening_runner_blocks_all_claims_missing_MTS_projection_maps`",
        "",
        "Claim ceiling: screening infrastructure only. No WEP, `Gdot`, `alpha3`, R10, PPN, Newtonian-limit, or local-GR pass is claimed.",
        "",
        "## Readout",
        "",
        "981 gave source-backed observational anchors. 982 turns those anchors into the actual map we need:",
        "",
        "`observable_vector = ProjectionMatrix * MTS_residual_coefficient_vector`.",
        "",
        "The runner is intentionally conservative. It accepts that numeric source bounds exist, but refuses to score any MTS coefficient while the projection matrix contains `MISSING_*` entries. This prevents the classic mistake of treating an experimental bound as if it were already a bound on the theory's private coefficient.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Coefficient Slots",
        "",
        md_table(coefficients, ["coefficient_id", "component", "parameter", "meaning", "current_status", "units", "valid_for_claim"]),
        "",
        "## Projection Matrix Skeleton",
        "",
        md_table(projections, ["projection_id", "observable", "source_prior", "screening_bound", "bound_units", "projection_formula", "required_projection_inputs", "missing_marker", "runner_status", "valid_for_claim"]),
        "",
        "## Screening Runner",
        "",
        md_table(screens, ["screen_id", "observable", "numeric_bound_present", "projection_inputs_missing_count", "missing_marker", "screen_result", "claim_allowed", "valid_for_claim"]),
        "",
        "## Identity Sanity Rows",
        "",
        md_table(identity_rows, ["sanity_id", "observable", "identity_assumption", "identity_bound_on_slot", "why_not_claim", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
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
    coefficients = coefficient_slots()
    projections = projection_matrix_rows()
    screens = screening_runner_rows(projections)
    identity_rows = identity_sanity_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, coefficients, projections, screens, identity_rows, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_982_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_982_COEFFICIENT_SLOTS.csv", coefficients)
    write_csv(OUT / "P8_Y5_R10_982_PROJECTION_MATRIX_SKELETON.csv", projections)
    write_csv(OUT / "P8_Y5_R10_982_SCREENING_RUNNER.csv", screens)
    write_csv(OUT / "P8_Y5_R10_982_IDENTITY_SANITY_ROWS.csv", identity_rows)
    write_csv(OUT / "P8_Y5_R10_982_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_982_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_982_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_982_VALIDATION.csv", validation)
    write_doc(sources, coefficients, projections, screens, identity_rows, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
