from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1039-R10-boundary-QX-Kboundary-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1039_BOUNDARY_QX_KBOUNDARY_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def local_bounds_index() -> dict[str, dict[str, str]]:
    return {row.get("row_id", ""): row for row in read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")}


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1039_0_1038_next",
            "source-intake/mts_residuals/P8_Y5_R10_1038_NEXT_TARGET.csv",
            "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
            "1038 handoff to boundary charge/cocycle or first beta row.",
        ),
        (
            "SRC1039_1_1038_closure",
            "source-intake/mts_residuals/P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv",
            "ODC1038_4_boundary_differentiability",
            "1038 boundary obstruction inside the Omega/DCX closure audit.",
        ),
        (
            "SRC1039_2_581_boundary",
            "source-intake/mts_residuals/P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv",
            "BCA581_5_verdict",
            "581 boundary charge audit.",
        ),
        (
            "SRC1039_3_582_boundary",
            "source-intake/mts_residuals/P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv",
            "BD582_5_verdict",
            "582 boundary differentiability audit.",
        ),
        (
            "SRC1039_4_669_theta_QX",
            "source-intake/mts_residuals/P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv",
            "V669_2_charge",
            "669 Noether current/charge decomposition ledger.",
        ),
        (
            "SRC1039_5_671_owner_gate",
            "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
            "BCG671_5_boundary_cocycle",
            "671 boundary charge owner gate.",
        ),
        (
            "SRC1039_6_735_proper_domain",
            "source-intake/mts_residuals/P8_Y5_R10_735_PROPER_BOUNDARY_DOMAIN_THEOREM.csv",
            "PBD735_2_charge",
            "735 proper compact-support boundary-domain theorem.",
        ),
        (
            "SRC1039_7_1019_exactness",
            "source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
            "BE1019_6_verdict",
            "1019 boundary exactness clauses.",
        ),
        (
            "SRC1039_8_976_alpha3",
            "source-intake/mts_residuals/P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv",
            "KBA976_0_formula",
            "976 alpha3 source acquisition row for K_boundary.",
        ),
        (
            "SRC1039_9_977_alpha3_status",
            "source-intake/mts_residuals/P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv",
            "KBS977_0_alpha3_formula",
            "977 K_boundary alpha3 non-scoreable status.",
        ),
        (
            "SRC1039_10_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R7_alpha3",
            "External local bounds including the alpha3 anchor.",
        ),
        (
            "SRC1039_11_R10_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 nonclaim R10 bound review candidate.",
        ),
        (
            "SRC1039_12_R10_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 alpha(lambda) runner.",
        ),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def compact_boundary_lemma_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "QK1039_0_variational_identity",
            "statement": "For a differentiable local generator G_X[epsilon], the possible obstruction is a finite-jet surface density k_X[delta Y, epsilon] on partial Sigma.",
            "derivation": "delta G_X[epsilon] = bulk constraint variation + integral_partialSigma k_X[delta Y, epsilon]; Q_X is chosen to cancel or own this term.",
            "status": "STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_G",
            "claim_scope": "sets the problem; does not prove silence",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "QK1039_1_proper_collar_condition",
            "statement": "If epsilon_X and all finite jets entering k_X vanish on an open collar of partial Sigma, every local boundary monomial containing epsilon_X or its jets vanishes pointwise.",
            "derivation": "support(epsilon_X) compactly contained in Sigma implies epsilon_X|partialSigma = nabla^a epsilon_X|partialSigma = 0 for required finite derivative order a.",
            "status": "DERIVED_NARROW_CONDITIONAL_ZERO",
            "claim_scope": "proper compact representative transformations only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "QK1039_2_QX_zero",
            "statement": "Under QK1039_1, Q_X[epsilon] = integral_partialSigma q_X[epsilon] = 0 and delta Q_X[epsilon] = 0.",
            "derivation": "q_X and delta q_X are finite-jet local surface expressions in epsilon_X and fields; the epsilon_X jet factors vanish on the boundary collar.",
            "status": "DERIVED_NARROW_PROPER_BRANCH_ONLY",
            "claim_scope": "kills representative edge charge for compact local gauge variations, not physical source or large transformations",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "QK1039_3_Kboundary_zero",
            "statement": "Under QK1039_1 for both epsilon_X and eta_X, K_boundary[epsilon,eta] = 0 for any finite-jet local boundary cocycle.",
            "derivation": "the cocycle is a surface bilinear in the generators and finite jets; every boundary term contains a vanished generator jet.",
            "status": "DERIVED_NARROW_PROPER_BRANCH_ONLY",
            "claim_scope": "compact proper algebra closes with zero boundary cocycle",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "QK1039_4_GR_charge_guard",
            "statement": "The proper-X zero does not erase observed ADM/time/rotation or GR Hamiltonian charges.",
            "derivation": "the vanishing condition applies to representative X parameters only; physical Hamiltonian generators remain in the observed boundary sector.",
            "status": "GUARD_RETAINED",
            "claim_scope": "prevents a fake proof that deletes GR charges to save MTS",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "QK1039_5_source_boundary_limit",
            "statement": "The compact/proper lemma does not prove Q_X=0 for source worldtubes, large transformations, reference-boundary terms, or range-kernel weighted edge projections.",
            "derivation": "R10 and local source tests can involve nonzero boundary/support data; those terms are exactly the BCA581/BD582/BCG671 residuals.",
            "status": "FULL_LOCAL_CLAIM_STILL_BLOCKED",
            "claim_scope": "source/test beta rows remain active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "QK1039_6_verdict",
            "statement": "Q_X=0 and K_boundary=0 are derived only for the proper compact representative sub-branch.",
            "derivation": "QK1039_1 through QK1039_4 close the narrow boundary algebra, while QK1039_5 blocks promotion to R10/local-GR.",
            "status": "DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED",
            "claim_scope": "useful GR-reduction hygiene, not an empirical pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def qx_kboundary_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "QKG1039_0_proper_compact_sublemma",
            "claim": "proper compact representative-X transformations carry no boundary charge or cocycle",
            "gate_status": "conditional_narrow_pass",
            "evidence": "epsilon_X and required finite jets vanish on a boundary collar, forcing Q_X and K_boundary surface densities to vanish",
            "not_enough_because": "does not cover source worldtubes, large/non-proper transformations, reference terms, mass projection, or range-kernel edge rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "QKG1039_1_full_QX_zero",
            "claim": "Q_X=0 for all local source/test boundaries",
            "gate_status": "fail_current_claim",
            "evidence": "BCG671 and BE1019 keep Q_edge and exactness clauses open",
            "not_enough_because": "B_X owner, exact primitive, counterterm, reference subtraction, and projector orthogonality remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "QKG1039_2_full_Kboundary_zero",
            "claim": "K_boundary=0 for source/test or improper edge transformations",
            "gate_status": "fail_current_claim",
            "evidence": "the compact-collar proof only controls finite-jet terms with vanished generator data",
            "not_enough_because": "parent Omega and differentiable generator bracket are still not computed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def boundary_residual_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "BRES1039_0_Qbar_edge_XH",
            "symbol": "Qbar_edge_XH(lambda)",
            "formula_or_contract": "Qbar_edge_XH(lambda)=integral_partialSigma F_lambda epsilon_nu B_X^nu with source/reference projection",
            "why_retained": "non-proper/source boundary values are not killed by the compact representative lemma",
            "missing_inputs": "B_X owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "BRES1039_1_K_boundary_alpha3",
            "symbol": "K_boundary_alpha3",
            "formula_or_contract": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "why_retained": "the alpha3 preferred-frame anchor is extremely tight and is the cleanest first boundary-flux projection",
            "missing_inputs": "K_boundary_alpha3; Phi_boundary_local; projection normalization; theorem-zero or numeric source",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "BRES1039_2_reference_mass_projection",
            "symbol": "Pi_M^H[Q_edge]",
            "formula_or_contract": "mass/Hamiltonian reference projector must be orthogonal to Q_edge or explicitly bounded",
            "why_retained": "a zero boundary charge proof must not delete physical GR mass/energy charges",
            "missing_inputs": "reference subtraction; Pi_M action on edge charge; no-double-count split",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "residual_id": "BRES1039_3_no_double_count",
            "symbol": "Q_bulk + Q_edge split",
            "formula_or_contract": "bulk and edge source terms must be orthogonal or explicitly added in absolute value",
            "why_retained": "source charge cannot be hidden twice or canceled by bookkeeping",
            "missing_inputs": "projection rules and source split",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def first_beta_projection_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    alpha3 = bounds.get("R7_alpha3", {})
    return [
        {
            "projection_id": "FBP1039_0_boundary_alpha3",
            "residual_symbol": "K_boundary_alpha3 * Phi_boundary_local",
            "observable": "alpha3",
            "projection_formula": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "empirical_anchor": alpha3.get("reference_path_or_url", "MISSING_R7_ALPHA3_SOURCE"),
            "bound": alpha3.get("upper_bound", "MISSING_R7_ALPHA3_BOUND"),
            "bound_units": alpha3.get("units", "dimensionless"),
            "required_inputs": "K_boundary_alpha3; Phi_boundary_local; normalization; source_path or theorem-zero",
            "current_status": "SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "FBP1039_1_R10_edge_beta",
            "residual_symbol": "Qbar_edge_XH(lambda) * qbar_XT(lambda)",
            "observable": "alpha_R10(lambda)",
            "projection_formula": "|alpha_edge(lambda)| <= |K_X^R10(lambda)| |Qbar_edge_XH(lambda)| |qbar_XT(lambda)| plus absolute tails",
            "empirical_anchor": str(BOUND_CANDIDATE),
            "bound": "alpha_bound(lambda) review-candidate curve",
            "bound_units": "dimensionless",
            "required_inputs": "K_X^R10(lambda); Qbar_edge_XH(lambda); qbar_XT(lambda); promoted bound curve; units",
            "current_status": "BOUND_CURVE_REVIEW_ONLY_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "FBP1039_2_absolute_tail_gate",
            "residual_symbol": "boundary_abs_tail",
            "observable": "all local arenas",
            "projection_formula": "unknown Q_X/K_boundary/source-support components add in absolute value; no cancellation credit",
            "empirical_anchor": "R10;alpha3;PPN;WEP;clock;Gdot ledgers",
            "bound": "multiple",
            "bound_units": "mixed",
            "required_inputs": "component theorem-zero or numeric bound rows",
            "current_status": "CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha3_anchor_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    alpha3 = bounds.get("R7_alpha3", {})
    return [
        {
            "anchor_id": "A3A1039_0_source_bound",
            "dataset_id": alpha3.get("dataset_id", "MISSING_DATASET"),
            "observable": alpha3.get("observable", "alpha3"),
            "upper_bound": alpha3.get("upper_bound", "MISSING_BOUND"),
            "units": alpha3.get("units", "dimensionless"),
            "reference": alpha3.get("reference_path_or_url", "MISSING_REFERENCE"),
            "use_in_1039": "anchor only for first beta projection row; not an MTS pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "proper_compact_QX_Kboundary_zero_sublemma",
            "curve_id": "MTS_1039_PROPER_COMPACT_BOUNDARY_ZERO",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_EXTENSION_TO_SOURCE_TEST_BOUNDARIES",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "Q_X=K_boundary=0 only for compact proper representative-X transformations",
            "derivation_status": "template_invalid_narrow_sublemma_not_full_R10_branch",
            "formula_reference": "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md::QK1039_6",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "proper compact support does not cover source/test boundary residuals",
            "valid_for_claim": "false",
            "notes": "The clean sublemma is useful but not scoreable.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "boundary_alpha3_projection_template",
            "curve_id": "MTS_1039_KBOUNDARY_ALPHA3_TEMPLATE",
            "lambda_value": "MISSING_NOT_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL",
            "alpha_bound": "4e-20",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R7_alpha3",
            "force_law_form": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "derivation_status": "template_invalid_projection_coefficients_missing",
            "formula_reference": "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md::FBP1039_0",
            "source_file": "MISSING_K_BOUNDARY_ALPHA3_SOURCE_FILE",
            "assumptions": "alpha3 anchor is source-backed but MTS projection is missing",
            "valid_for_claim": "false",
            "notes": "First beta/projection row staged without claim.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "R10_edge_beta_template",
            "curve_id": "MTS_1039_R10_EDGE_BETA_TEMPLATE",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_QBAR_EDGE_XH_QBAR_XT",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "|alpha_edge| <= |K_X^R10| |Qbar_edge_XH| |qbar_XT| plus absolute tails",
            "derivation_status": "template_invalid_edge_projection_missing",
            "formula_reference": "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md::FBP1039_1",
            "source_file": "MISSING_EDGE_SOURCE_FILE",
            "assumptions": "no naked linear c_g; no cancellation between tails",
            "valid_for_claim": "false",
            "notes": "R10 edge row remains blocked.",
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1039_0_runner_status",
            "runner_output_dir": str(RUN_DIR),
            "mts_rows": str(status.get("mts_rows")),
            "bound_rows": str(status.get("bound_rows")),
            "valid_mts_rows": str(status.get("valid_mts_rows")),
            "valid_bound_rows": str(status.get("valid_bound_rows")),
            "comparison_rows": str(status.get("comparison_rows")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "expected_result": "blocked_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def placeholder_refusal_rows(
    lemma_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in lemma_rows:
        if row["status"] != "DERIVED_NARROW_PROPER_BRANCH_ONLY":
            rows.append(
                {
                    "refusal_id": f"REF1039_{row['lemma_id']}",
                    "object": row["statement"],
                    "current_status": row["status"],
                    "refusal_status": "full_boundary_claim_not_promoted",
                    "failure_reasons": f"{row['status']};CLAIM_POLICY_FALSE",
                    "score_eligible": "false",
                    "claim_allowed": "false",
                    "valid_for_claim": "false",
                    "generated_utc": stamp(),
                }
            )
    for row in gate_rows:
        rows.append(
            {
                "refusal_id": f"REF1039_{row['gate_id']}",
                "object": row["claim"],
                "current_status": row["gate_status"],
                "refusal_status": "boundary_gate_not_claim_promoted",
                "failure_reasons": row["not_enough_because"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in residual_rows:
        rows.append(
            {
                "refusal_id": f"REF1039_{row['residual_id']}",
                "object": row["symbol"],
                "current_status": row["missing_inputs"],
                "refusal_status": "residual_retained_missing_inputs",
                "failure_reasons": f"{row['missing_inputs']};SCORE_READY_FALSE",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in projection_rows:
        rows.append(
            {
                "refusal_id": f"REF1039_{row['projection_id']}",
                "object": row["residual_symbol"],
                "current_status": row["current_status"],
                "refusal_status": "projection_row_rejected_missing_coefficients",
                "failure_reasons": f"{row['current_status']};SCORE_READY_FALSE",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE1039_0_compact_proper_sublemma",
            "claim": "compact proper representative-X boundary transformations are silent",
            "gate_pass": "conditional_narrow_only",
            "reason": "finite-jet boundary terms vanish when the representative generator and required jets vanish on the boundary collar",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1039_1_full_local_GR",
            "claim": "local GR/no-pole boundary branch is fully closed",
            "gate_pass": "false",
            "reason": "source worldtubes, reference/mass projection, exactness, counterterms, parent bracket, and matter/source readout remain unproved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1039_2_alpha3_projection",
            "claim": "K_boundary alpha3 row is score-ready",
            "gate_pass": "false",
            "reason": "alpha3 external anchor exists but K_boundary_alpha3 and Phi_boundary_local are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1039_3_R10_edge",
            "claim": "R10 edge beta row is score-ready",
            "gate_pass": "false",
            "reason": "R10 bound curve is review-only and K_X/Qbar_edge/qbar_XT are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1039_0_boundary_derivation",
            "decision": "A real but narrow boundary result was derived: proper compact representative-X transformations have Q_X=0 and K_boundary=0.",
            "because": "finite-jet boundary charges and cocycles vanish pointwise when the generator and required jets vanish on the boundary collar.",
            "next_action": "do not promote to R10/local-GR; attack the non-proper/source boundary formula next",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1039_1_empirical_fallback",
            "decision": "The first beta/projection fallback row is alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local.",
            "because": "alpha3 has a source-backed tight anchor, and existing 976/977 files already isolated this exact missing K/Phi pair.",
            "next_action": "derive or source K_boundary_alpha3 and Phi_boundary_local, or prove both theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1039_2_next_target",
            "decision": "Next target should write the parent boundary charge formula rather than inventing a numeric coefficient.",
            "because": "a formula for B_X/Q_X decides both the no-pole route and the K_boundary_alpha3 fallback row.",
            "next_action": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "objective": "derive the explicit parent boundary charge density B_X/Q_X from the symplectic potential and allowed boundary class; if this cannot close, build the nonclaim alpha3 projection coefficient row for K_boundary_alpha3 and Phi_boundary_local",
            "include": "Theta_Y boundary term, B_X surface density, exact/proper split, reference subtraction, Pi_M/Pi_EH projection, K_boundary cocycle formula, alpha3 projection normalization",
            "exclude": "invented K_boundary values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1039_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1039 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1039_1_compact_boundary_sublemma",
            any(row["lemma_id"] == "QK1039_2_QX_zero" and row["status"] == "DERIVED_NARROW_PROPER_BRANCH_ONLY" for row in lemma_rows)
            and any(row["lemma_id"] == "QK1039_3_Kboundary_zero" and row["status"] == "DERIVED_NARROW_PROPER_BRANCH_ONLY" for row in lemma_rows)
            and any(row["lemma_id"] == "QK1039_5_source_boundary_limit" and row["status"] == "FULL_LOCAL_CLAIM_STILL_BLOCKED" for row in lemma_rows),
            "proper compact Q_X/K_boundary zero is derived but source-boundary promotion is blocked",
        )
    )
    checks.append(
        (
            "V1039_2_qx_kboundary_gates_nonclaim",
            len(gate_rows) >= 3 and all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gate_rows),
            "Q_X/K_boundary gates keep all claims non-promoted",
        )
    )
    checks.append(
        (
            "V1039_3_boundary_residuals_retained",
            {"Qbar_edge_XH(lambda)", "K_boundary_alpha3", "Pi_M^H[Q_edge]", "Q_bulk + Q_edge split"}.issubset(
                {row["symbol"] for row in residual_rows}
            )
            and all(row["score_ready"] == "false" for row in residual_rows),
            "boundary source/test residuals are retained and non-scoreable",
        )
    )
    checks.append(
        (
            "V1039_4_first_projection_alpha3_anchor",
            any(row["projection_id"] == "FBP1039_0_boundary_alpha3" and row["bound"] == "4e-20" for row in projection_rows)
            and all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in projection_rows),
            "first beta projection uses source-backed alpha3 anchor but remains nonclaim",
        )
    )
    checks.append(
        (
            "V1039_5_alpha3_anchor_source_backed",
            bool(alpha3_rows) and alpha3_rows[0]["upper_bound"] == "4e-20" and "Will" in alpha3_rows[0]["dataset_id"],
            "alpha3 external anchor is captured from local bound ledger",
        )
    )
    checks.append(
        (
            "V1039_6_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1039_7_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1039 nonclaim rows",
        )
    )
    checks.append(
        (
            "V1039_8_claim_gates_blocked",
            all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all public/empirical claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1039_9_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1039_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
        OUT / "P8_Y5_R10_1039_QX_KBOUNDARY_CLAIM_GATE.csv",
        OUT / "P8_Y5_R10_1039_BOUNDARY_RESIDUAL_BETA_ROW.csv",
        OUT / "P8_Y5_R10_1039_FIRST_BETA_PROJECTION_TEMPLATE.csv",
        OUT / "P8_Y5_R10_1039_ALPHA3_BOUND_ANCHOR_LEDGER.csv",
        OUT / "P8_Y5_R10_1039_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1039_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1039_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1039_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1039_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1039_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1039_10_generated_files_in_post_checkpoint",
            all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in generated_files if path.exists() or path.parent.exists()),
            "all generated files are under post-checkpoint-work",
        )
    )
    formalization_touches = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
                formalization_touches.append(path)
    checks.append(
        (
            "V1039_11_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1039_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1039 boundary Q_X/K_boundary or beta-bound first row validation summary",
            "generated_utc": stamp(),
        }
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    return rows


def write_doc(
    source_rows: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    projection_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1039 Y5 R10 boundary charge QX/Kboundary zero or beta-bound first row",
        "",
        "**Derived narrow result:** for proper compact representative-`X` transformations, where the generator and required finite jets vanish on a boundary collar, both `Q_X` and `K_boundary` vanish. That is real hygiene for the GR-reduction route.",
        "",
        "**Claim ceiling:** this does **not** close the full local-GR/R10 branch. Source worldtubes, large/non-proper transformations, reference/mass projections, exactness, counterterms, and the parent bracket are still open.",
        "",
        "**Fallback staged:** the first concrete beta/projection row is `alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local`, anchored to the source-backed `alpha3 <= 4e-20` bound but nonclaim until `K_boundary_alpha3` and `Phi_boundary_local` are derived or sourced.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Compact/proper boundary silence lemma",
        md_table(lemma_rows, ["lemma_id", "statement", "derivation", "status", "claim_scope", "claim_allowed", "valid_for_claim"]),
        "## QX/Kboundary claim gate",
        md_table(gate_rows, ["gate_id", "claim", "gate_status", "evidence", "not_enough_because", "claim_allowed", "valid_for_claim"]),
        "## Boundary residual beta rows",
        md_table(residual_rows, ["residual_id", "symbol", "formula_or_contract", "why_retained", "missing_inputs", "score_ready", "valid_for_claim"]),
        "## First beta projection template",
        md_table(projection_rows, ["projection_id", "residual_symbol", "observable", "projection_formula", "empirical_anchor", "bound", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
        "## Alpha3 anchor ledger",
        md_table(alpha3_rows, ["anchor_id", "dataset_id", "observable", "upper_bound", "units", "reference", "use_in_1039", "valid_for_claim"]),
        "## MTS alpha smoke template",
        md_table(mts_rows, ["model_id", "branch_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"]),
        "## Runner smoke status",
        md_table(smoke_rows, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
        "## Placeholder refusal runner",
        md_table(refusal_rows, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
        "## Claim gates",
        md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision ledger",
        md_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
        "## Next target",
        md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if RUN_DIR.exists():
        shutil.rmtree(RUN_DIR)
    RUN_DIR.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    lemma_rows = compact_boundary_lemma_rows()
    gate_rows = qx_kboundary_gate_rows()
    residual_rows = boundary_residual_rows()
    bounds = local_bounds_index()
    projection_rows = first_beta_projection_rows(bounds)
    alpha3_rows = alpha3_anchor_rows(bounds)
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(lemma_rows, gate_rows, residual_rows, projection_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        lemma_rows,
        gate_rows,
        residual_rows,
        projection_rows,
        alpha3_rows,
        mts_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1039_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv", lemma_rows)
    write_csv(OUT / "P8_Y5_R10_1039_QX_KBOUNDARY_CLAIM_GATE.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_1039_BOUNDARY_RESIDUAL_BETA_ROW.csv", residual_rows)
    write_csv(OUT / "P8_Y5_R10_1039_FIRST_BETA_PROJECTION_TEMPLATE.csv", projection_rows)
    write_csv(OUT / "P8_Y5_R10_1039_ALPHA3_BOUND_ANCHOR_LEDGER.csv", alpha3_rows)
    write_csv(OUT / "P8_Y5_R10_1039_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1039_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1039_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1039_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1039_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1039_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        lemma_rows,
        gate_rows,
        residual_rows,
        projection_rows,
        alpha3_rows,
        mts_rows,
        smoke_rows,
        refusal_rows,
        claim_rows,
        decisions,
        validation,
        next_rows,
    )

    if validation[0]["result"] != "pass":
        failed = [row for row in validation if row["result"] == "fail"]
        raise SystemExit(f"1039 validation failed: {failed}")


if __name__ == "__main__":
    main()
