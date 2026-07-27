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
DOC = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1038-R10-Omega-DCX-beta-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1038_OMEGA_DCX_OR_BETA_BOUND_TEMPLATE_NONCLAIM.csv"
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
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    return {row.get("row_id", ""): row for row in rows}


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1038_0_1037_next",
            "source-intake/mts_residuals/P8_Y5_R10_1037_NEXT_TARGET.csv",
            "1038-Y5-R10-parent-Omega-DCX",
            "1037 handoff selecting parent Omega/DCX/vertical-generator closure or beta-bound acquisition.",
        ),
        (
            "SRC1038_1_1037_no_pole",
            "source-intake/mts_residuals/P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
            "NP1037_2_momentum_map",
            "1037 exact missing no-pole object list.",
        ),
        (
            "SRC1038_2_1037_beta",
            "source-intake/mts_residuals/P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
            "BB1037_7_beta_product_guard",
            "1037 bounded beta source/test fallback with c_g-squared guard.",
        ),
        (
            "SRC1038_3_590_gate",
            "source-intake/mts_residuals/P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
            "MCG590_0_parent_Omega",
            "590 mapping closure gate for parent Omega and DC_X gaps.",
        ),
        (
            "SRC1038_4_590_field_map",
            "source-intake/mts_residuals/P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
            "field_block",
            "590 field-by-field vertical action candidate map.",
        ),
        (
            "SRC1038_5_582_momentum",
            "source-intake/mts_residuals/P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
            "MMT582_4_no_pole_result",
            "582 first-class momentum-map closure theorem template.",
        ),
        (
            "SRC1038_6_582_gate",
            "source-intake/mts_residuals/P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
            "NPG582_5_no_pole_claim",
            "582 no-pole gate status.",
        ),
        (
            "SRC1038_7_581_certificate",
            "source-intake/mts_residuals/P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
            "NPC581_6_claim_gate",
            "581 no-pole certificate template.",
        ),
        (
            "SRC1038_8_670_chain",
            "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
            "NQ670_8_no_pole_result",
            "670 no-pole quotient proof chain.",
        ),
        (
            "SRC1038_9_944_frame_leak",
            "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "FLB944_0_cg_weyl",
            "944 frame-leak bound pack containing older linear c_g shorthand.",
        ),
        (
            "SRC1038_10_945_bound_rows",
            "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "BND945_0_cg_value",
            "945 first local frame-leak bound rows.",
        ),
        (
            "SRC1038_11_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R7_alpha3",
            "External local bound anchor ledger for WEP, clocks, PPN, and orbital rows.",
        ),
        (
            "SRC1038_12_R10_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 Eot-Wash 2020 review-candidate R10 bound curve, nonclaim.",
        ),
        (
            "SRC1038_13_R10_runner",
            "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "MTS_REQUIRED_COLUMNS",
            "Existing R10 alpha(lambda) bound prediction runner.",
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


def closure_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "ODC1038_0_parent_Omega",
            "object": "parent symplectic form",
            "needed_statement": "Omega_Y = delta Theta_Y on the full parent variable set before quotienting or gauge fixing",
            "derivation_attempt": "1038 cannot reconstruct Theta_Y from the current ledgers; existing rows only name the missing object",
            "current_status": "MISSING_PARENT_OMEGA",
            "if_missing": "DC_X^dagger cannot be identified with an Omega-flat vertical vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_1_DCX_operator",
            "object": "linearized constraint/source operator D C_X",
            "needed_statement": "C_X^nu[Phi]=0 is parent-owned and D C_X maps field variations into the X constraint covector",
            "derivation_attempt": "590 gives the intended C_X=-nabla P+J_eff shape but not a parent-owned operator with domains",
            "current_status": "MISSING_DCX_OPERATOR",
            "if_missing": "the adjoint DC_X^dagger is pairing-dependent bookkeeping, not a generator proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_2_Omega_flat_map",
            "object": "Omega-flat vertical generator identity",
            "needed_statement": "i_{v_X} Omega_Y = delta C_X[epsilon] or DC_X^dagger epsilon = Omega_Y^flat(v_X[epsilon])",
            "derivation_attempt": "identity cannot be checked without both Omega_Y and D C_X",
            "current_status": "NOT_COMPARABLE_WITHOUT_OMEGA_AND_DCX",
            "if_missing": "rank-zero/null directions do not prove gauge; a physical or edge mode can remain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_3_vertical_generator_fields",
            "object": "field-by-field vertical generator",
            "needed_statement": "v_X is specified on metric/coframe, momenta, domain/memory/projector, matter/readout, and boundary fields",
            "derivation_attempt": "standard diffeo/local-Lorentz candidates exist for metric/coframe only; MTS extra sectors are unmapped",
            "current_status": "FIELD_MAP_INCOMPLETE",
            "if_missing": "the putative gauge direction can leak into source/test charges",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_4_boundary_differentiability",
            "object": "boundary charge Q_X",
            "needed_statement": "delta Q_X cancels all boundary variation and Q_X is zero, exact, or proper on the local branch",
            "derivation_attempt": "582 and 1037 identify the boundary-charge obstruction; no current file signs Q_X=0",
            "current_status": "MISSING_BOUNDARY_CHARGE_ZERO",
            "if_missing": "R10 source charge can be hidden in edge hair or Qbar_XH",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_5_bracket_closure",
            "object": "first-class bracket and boundary cocycle",
            "needed_statement": "{G_X[epsilon],G_X[eta]} = G_X[[epsilon,eta]] + K_boundary and K_boundary=0 for local transformations",
            "derivation_attempt": "the algebra is stated as a target in 582; K_boundary is not computed",
            "current_status": "MISSING_BRACKET_KBOUNDARY",
            "if_missing": "the X direction may be second-class, anomalous, or edge-charged",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_6_degree_count",
            "object": "reduced phase-space degree count",
            "needed_statement": "primary/secondary first-class pair removes the local X pair and reduced Omega is nondegenerate without an X stabilizer",
            "derivation_attempt": "rank/constraint count remains a named obligation rather than an evaluated count",
            "current_status": "MISSING_DEGREE_COUNT",
            "if_missing": "no-pole can be confused with under-specified dynamics",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_7_matter_readout",
            "object": "matter/no-marker descent",
            "needed_statement": "S_matter = Sbar[q(Phi), psi, theta] and ordinary constants/readouts carry no representative-X marker",
            "derivation_attempt": "existing contracts isolate the requirement but do not parent-sign it",
            "current_status": "MISSING_MATTER_QUOTIENT",
            "if_missing": "beta_s and beta_t remain live even if the bulk X pole is gauge-like",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "ODC1038_8_verdict",
            "object": "exact no-physical-X-pole certificate",
            "needed_statement": "ODC1038_0 through ODC1038_7 close from one parent action and boundary prescription",
            "derivation_attempt": "1038 sharpens the obstruction but does not close it",
            "current_status": "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED",
            "if_missing": "start source-backed beta bound acquisition while keeping derivation route open",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def vertical_generator_rows() -> list[dict[str, str]]:
    return [
        {
            "field_block": "metric_or_coframe",
            "candidate_vertical_action": "v_X[g]=L_epsilon g or v_X[e]=L_epsilon e plus local Lorentz compensation",
            "Omega_flat_target": "metric/coframe component of Omega_Y^flat(v_X)",
            "DCX_target": "metric/coframe component of D C_X^dagger epsilon",
            "status": "STANDARD_CANDIDATE_NOT_PARENT_DECLARED",
            "missing_input": "observed metric/coframe ownership and parent symplectic potential",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_block": "canonical_momenta_or_boundary_charge",
            "candidate_vertical_action": "v_X[pi]=L_epsilon pi plus density and boundary improvements",
            "Omega_flat_target": "momentum and boundary component of Omega_Y^flat(v_X)",
            "DCX_target": "integration-by-parts boundary term in delta C_X[epsilon]",
            "status": "NOT_WRITTEN_FOR_MTS",
            "missing_input": "canonical variables or covariant phase-space charge split",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_block": "Gamma_Khat_qloc_sector",
            "candidate_vertical_action": "v_X[T_GK]=L_epsilon T_GK if the sector is a parent tensor stress",
            "Omega_flat_target": "extra-sector contribution to Omega_Y^flat(v_X)",
            "DCX_target": "Euler/Ward stress-divergence covector",
            "status": "CONDITIONAL_NOT_INTEGRATED_WITH_DCX",
            "missing_input": "parent S_GK, Helmholtz integrability, and actual DC_X owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_block": "domain_memory_projector_fields",
            "candidate_vertical_action": "v_X[Phi^A]=L_epsilon Phi^A or quotient-vertical representative shift",
            "Omega_flat_target": "domain/memory/projector component of Omega_Y^flat(v_X)",
            "DCX_target": "extra-sector component of D C_X^dagger",
            "status": "UNMAPPED",
            "missing_input": "transformation law for chi_D, Q_coh, memory, projector, and boundary variables",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_block": "matter_readout_constants",
            "candidate_vertical_action": "v_X[psi]=0 and v_X[theta_A]=0 only if matter descends through q",
            "Omega_flat_target": "matter component should vanish or be quotient-pullback only",
            "DCX_target": "no source/test marker covector",
            "status": "NOT_DERIVED",
            "missing_input": "matter action descent and no-marker theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_block": "boundary_edge_modes",
            "candidate_vertical_action": "proper compact transformation or exact boundary representative shift",
            "Omega_flat_target": "no residual boundary charge in Omega_Y^flat(v_X)",
            "DCX_target": "Q_X=0/exact/proper and K_boundary=0",
            "status": "NOT_DERIVED",
            "missing_input": "boundary differentiability, Q_X, and cocycle computation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def no_pole_gate_rows(closure_rows: list[dict[str, str]], vertical_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    blockers = [row["current_status"] for row in closure_rows if row["current_status"] != "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED"]
    blockers.extend(row["status"] for row in vertical_rows if row["status"] not in {"STANDARD_CANDIDATE_NOT_PARENT_DECLARED"})
    return [
        {
            "gate_id": "NPG1038_0_exact_no_pole",
            "claim": "finite local X has no physical exchange pole in the local GR/Newton branch",
            "gate_pass": "false",
            "failure_reasons": ";".join(blockers),
            "minimum_to_flip": "parent Omega_Y, D C_X, v_X on all fields, Q_X=0/proper/exact, K_boundary=0, degree count, matter descent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def beta_acquisition_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    def bound(row_id: str, column: str) -> str:
        return bounds.get(row_id, {}).get(column, "MISSING_LOCAL_BOUND_ROW")

    return [
        {
            "acquisition_id": "BBA1038_0_R10_beta_product",
            "component": "abs_beta_product_R10",
            "empirical_anchor": str(BOUND_CANDIDATE),
            "anchor_value_or_bound": "alpha_bound(lambda) review-candidate curve",
            "required_theory_projection": "K_X^R10(lambda), beta_s_abs, beta_t_abs, and absolute tails",
            "current_status": "BOUND_CURVE_REVIEW_ONLY_KX_PROFILE_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_1_WEP_marker_diff",
            "component": "b_A,b_alpha differential composition leakage",
            "empirical_anchor": bound("R1_WEP_source_charge", "reference_path_or_url"),
            "anchor_value_or_bound": bound("R1_WEP_source_charge", "upper_bound"),
            "required_theory_projection": "material sensitivities and source/test differential marker map",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_2_clock_marker",
            "component": "b_alpha,b_clock redshift or frequency leakage",
            "empirical_anchor": bound("R2_clock_redshift", "reference_path_or_url"),
            "anchor_value_or_bound": bound("R2_clock_redshift", "upper_bound"),
            "required_theory_projection": "clock sensitivity coefficients and MTS constant/readout descent",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_3_PPN_common_frame_gamma",
            "component": "tau_PPN c_g or disformal gamma response",
            "empirical_anchor": bound("R3_gamma", "reference_path_or_url"),
            "anchor_value_or_bound": bound("R3_gamma", "upper_bound"),
            "required_theory_projection": "weak-field gauge-fixed map from frame leak to gamma-1",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_4_PPN_beta",
            "component": "delta_beta_source and nonlinear-tail response",
            "empirical_anchor": bound("R4_beta", "reference_path_or_url"),
            "anchor_value_or_bound": bound("R4_beta", "upper_bound"),
            "required_theory_projection": "post-Newtonian nonlinear response of beta_s/beta_t tails",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_5_preferred_frame_flux",
            "component": "vector/domain/preferred-frame leakage",
            "empirical_anchor": "R5_alpha1;R6_alpha2;R7_alpha3;R8_xi",
            "anchor_value_or_bound": ";".join(
                [
                    bound("R5_alpha1", "upper_bound"),
                    bound("R6_alpha2", "upper_bound"),
                    bound("R7_alpha3", "upper_bound"),
                    bound("R8_xi", "upper_bound"),
                ]
            ),
            "required_theory_projection": "map domain/boundary/vector leakage into preferred-frame PPN coefficients",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_6_Gdot_support",
            "component": "support/source drift and effective G drift",
            "empirical_anchor": bound("R9_Gdot", "reference_path_or_url"),
            "anchor_value_or_bound": f"{bound('R9_Gdot', 'upper_bound')} {bound('R9_Gdot', 'units')}",
            "required_theory_projection": "worldtube/source support map into Gdot/G",
            "current_status": "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "acquisition_id": "BBA1038_7_score_gate",
            "component": "claim-safe bounded residual vector",
            "empirical_anchor": "R10;WEP;clock;PPN;orbital anchors",
            "anchor_value_or_bound": "multiple",
            "required_theory_projection": "all component projections numeric, unit-matched, sourced, and no-cancellation absolute-added",
            "current_status": "CLAIM_BLOCKED_UNTIL_PARENT_PROJECTIONS_EXIST",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def legacy_quarantine_rows() -> list[dict[str, str]]:
    return [
        {
            "quarantine_id": "LCG1038_0_944_linear_shorthand",
            "source_row": "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv:FLB944_0_cg_weyl",
            "legacy_formula": "alpha_R10 ~ K_X(lambda) Qbar_XH tau_R10 c_g",
            "quarantine_action": "BOOKKEEPING_ONLY_NOT_SCOREABLE",
            "replacement_rule": "a naked linear c_g row is rejected unless Qbar_XH explicitly and source-backed contains the source leg; universal source/test Weyl leakage is c_g^2",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "quarantine_id": "LCG1038_1_runner_guard",
            "source_row": "all future MTS alpha(lambda) candidate rows",
            "legacy_formula": "alpha_predicted = numeric * c_g",
            "quarantine_action": "REJECT_AS_UNDERFACTORED_SOURCE_TEST_PRODUCT",
            "replacement_rule": "require beta_s beta_t or a declared source leg in Qbar_XH with source path and units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def cross_arena_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "CAR1038_0_R10",
            "arena": "short-range fifth force",
            "incoming_theory_row": "K_X^R10(lambda) beta_s_abs beta_t_abs plus absolute tails",
            "external_anchor": "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "blocker": "K_X profile and promoted bound curve missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "CAR1038_1_PPN",
            "arena": "local weak field and preferred-frame PPN",
            "incoming_theory_row": "common-frame, disformal, vector/domain, and nonlinear-tail residual vector",
            "external_anchor": "local_bound_claims.csv rows R3 through R8",
            "blocker": "arena projection matrix missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "CAR1038_2_WEP_clock",
            "arena": "composition, clocks, and EM/material markers",
            "incoming_theory_row": "b_A, b_alpha, b_clock, and readout descent residuals",
            "external_anchor": "local_bound_claims.csv rows R1 and R2",
            "blocker": "material/clock sensitivity map missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "CAR1038_3_orbital_source",
            "arena": "orbital/source support and G drift",
            "incoming_theory_row": "support, domain, boundary, and non-Hilbert current residuals",
            "external_anchor": "local_bound_claims.csv row R9",
            "blocker": "worldtube/source support projection missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "Omega_DCX_no_pole_certificate_attempt",
            "curve_id": "MTS_1038_OMEGA_DCX_NOPOLE",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_OMEGA_DCX_VERTICAL_GENERATOR_CERTIFICATE",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "alpha_X=0 only if the parent Omega/DCX/vertical/boundary/degree/matter certificate closes",
            "derivation_status": "template_invalid_no_pole_not_closed",
            "formula_reference": "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md::ODC1038_8",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "no physical X pole cannot be asserted from conditional quotient math alone",
            "valid_for_claim": "false",
            "notes": "Derivation-first branch remains open but unsigned.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "bounded_beta_cross_arena_template",
            "curve_id": "MTS_1038_BOUNDED_BETA_TEMPLATE",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_TIMES_BETA_S_ABS_BETA_T_ABS_PLUS_TAILS",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "|alpha_X(lambda)| <= |K_X^R10(lambda)|[beta_s_abs beta_t_abs + abs_tail(lambda)]",
            "derivation_status": "template_invalid_beta_projection_inputs_missing",
            "formula_reference": "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md::BBA1038_7",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "absolute tails add; no cancellation credit",
            "valid_for_claim": "false",
            "notes": "Fallback branch is schema-ready only.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "legacy_linear_cg_refusal",
            "curve_id": "MTS_1038_LINEAR_CG_QUARANTINE",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_DECLARED_SOURCE_LEG_LINEAR_CG_FORBIDDEN",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "universal Weyl source/test branch contributes as c_g^2, not naked c_g",
            "derivation_status": "template_invalid_legacy_linear_cg_quarantined",
            "formula_reference": "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md::LCG1038_0",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv",
            "assumptions": "linear c_g allowed only if Qbar_XH contains a sourced source leg",
            "valid_for_claim": "false",
            "notes": "Prevents accidental optimistic R10 scoring.",
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1038_0_runner_status",
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
    closure_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    legacy_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in closure_rows:
        rows.append(
            {
                "refusal_id": f"REF1038_{row['audit_id']}",
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "no_pole_claim_rejected_current_corpus",
                "failure_reasons": f"{row['current_status']};CLAIM_POLICY_FALSE",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in beta_rows:
        rows.append(
            {
                "refusal_id": f"REF1038_{row['acquisition_id']}",
                "object": row["component"],
                "current_status": row["current_status"],
                "refusal_status": "beta_bound_row_rejected_missing_projection",
                "failure_reasons": f"{row['current_status']};SCORE_READY_FALSE;CLAIM_POLICY_FALSE",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in legacy_rows:
        rows.append(
            {
                "refusal_id": f"REF1038_{row['quarantine_id']}",
                "object": row["legacy_formula"],
                "current_status": row["quarantine_action"],
                "refusal_status": "legacy_linear_cg_rejected_unless_source_leg_declared",
                "failure_reasons": "NAKED_LINEAR_CG_FORBIDDEN;CLAIM_POLICY_FALSE",
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
            "gate_id": "CGATE1038_0_no_pole",
            "claim": "the local X branch is pure gauge/no physical pole",
            "gate_pass": "false",
            "reason": "parent Omega, D C_X, all-field v_X, boundary charge/cocycle, degree count, and matter descent remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1038_1_beta_bound",
            "claim": "bounded beta residual vector can be scored against local tests",
            "gate_pass": "false",
            "reason": "external anchors exist, but MTS projection coefficients and units do not",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1038_2_linear_cg",
            "claim": "naked linear c_g R10 row is scoreable",
            "gate_pass": "false",
            "reason": "source/test product requires beta_s beta_t; universal Weyl branch gives c_g^2 unless a source leg is explicitly contained in Qbar_XH",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1038_3_R10_pass",
            "claim": "R10/local-GR pass is established",
            "gate_pass": "false",
            "reason": "runner smoke intentionally has zero claim-valid MTS and bound rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1038_0_derivation_status",
            "decision": "Omega/DCX closure was attempted and rejected as a current claim.",
            "because": "the present corpus names the correct geometric objects but does not supply the parent symplectic form, linearized constraint operator, or boundary charge computation.",
            "next_action": "either write Q_X and K_boundary explicitly from a parent action, or move one beta row at a time into sourced projection form",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1038_1_empirical_status",
            "decision": "Beta-bound acquisition is now staged without claiming a pass.",
            "because": "real external anchors exist for R10, WEP, clocks, PPN, and Gdot, but no MTS arena projection matrix exists yet.",
            "next_action": "build the first projection row that maps one parent residual into one external observable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1038_2_linear_cg_status",
            "decision": "Legacy linear c_g shorthand is quarantined.",
            "because": "a source-test interaction needs both legs; treating universal frame leakage as linear is too optimistic and would be attacked immediately.",
            "next_action": "make future R10 candidate rows declare beta_s beta_t or an explicit source leg inside Qbar_XH",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1038_3_next_target",
            "decision": "Next target should attack boundary charge/cocycle first, while keeping beta acquisition ready.",
            "because": "Q_X=0 and K_boundary=0 are the sharpest single remaining no-pole obstruction and also decide whether edge charge becomes a beta source.",
            "next_action": "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
            "objective": "try to compute or prove silence of Q_X and K_boundary for the local vertical branch; if this fails, fill the first source-backed beta projection row without claiming a pass",
            "include": "boundary variation of G_X, Q_X exact/proper/zero tests, K_boundary cocycle, compact-support local transformation limit, first beta source row schema",
            "exclude": "invented parent action terms, naked linear c_g scoring, cancellation between beta tails, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    vertical_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    legacy_rows: list[dict[str, str]],
    cross_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1038_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1038 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1038_1_closure_audit_blocks_claim",
            len(closure_rows) >= 9
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_CLOSED" for row in closure_rows)
            and all(not flag(row["valid_for_claim"]) for row in closure_rows),
            "Omega/DCX closure audit ends in a blocked no-pole verdict",
        )
    )
    checks.append(
        (
            "V1038_2_vertical_map_complete_nonclaim",
            {"metric_or_coframe", "canonical_momenta_or_boundary_charge", "domain_memory_projector_fields", "matter_readout_constants", "boundary_edge_modes"}.issubset(
                {row["field_block"] for row in vertical_rows}
            )
            and all(not flag(row["valid_for_claim"]) for row in vertical_rows),
            "vertical generator map covers core, extra, matter, and boundary blocks without claim promotion",
        )
    )
    checks.append(
        (
            "V1038_3_no_pole_gate_blocked",
            bool(gate_rows)
            and gate_rows[0]["gate_pass"] == "false"
            and "MISSING_PARENT_OMEGA" in gate_rows[0]["failure_reasons"],
            "no-pole gate is explicitly blocked by parent Omega/DCX gaps",
        )
    )
    checks.append(
        (
            "V1038_4_beta_acquisition_staged_nonclaim",
            len(beta_rows) >= 8
            and any("4e-20" in row.get("anchor_value_or_bound", "") for row in beta_rows)
            and all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in beta_rows),
            "beta-bound acquisition uses source-backed anchors but keeps every row nonclaim",
        )
    )
    checks.append(
        (
            "V1038_5_linear_cg_quarantined",
            any(row["quarantine_id"] == "LCG1038_0_944_linear_shorthand" for row in legacy_rows)
            and all(not flag(row["valid_for_claim"]) for row in legacy_rows),
            "legacy linear c_g shorthand is quarantined",
        )
    )
    checks.append(
        (
            "V1038_6_cross_arena_routing_complete",
            {row["arena"] for row in cross_rows}
            == {
                "short-range fifth force",
                "local weak field and preferred-frame PPN",
                "composition, clocks, and EM/material markers",
                "orbital/source support and G drift",
            },
            "cross-arena bound routing covers R10, PPN, WEP/clock, and orbital/source channels",
        )
    )
    checks.append(
        (
            "V1038_7_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke alpha template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1038_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1038 nonclaim rows",
        )
    )
    checks.append(
        (
            "V1038_9_claim_gates_blocked",
            all(row["gate_pass"] == "false" and not flag(row["claim_allowed"]) for row in claim_rows),
            "all claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1038_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1038_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv",
        OUT / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv",
        OUT / "P8_Y5_R10_1038_NO_POLE_CLAIM_GATE.csv",
        OUT / "P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv",
        OUT / "P8_Y5_R10_1038_LEGACY_LINEAR_CG_QUARANTINE.csv",
        OUT / "P8_Y5_R10_1038_CROSS_ARENA_BOUND_ROUTING.csv",
        OUT / "P8_Y5_R10_1038_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1038_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1038_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1038_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1038_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1038_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1038_11_generated_files_in_post_checkpoint",
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
            "V1038_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1038_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1038 parent Omega/DCX closure or beta-bound acquisition validation summary",
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
    closure_rows: list[dict[str, str]],
    vertical_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    legacy_rows: list[dict[str, str]],
    cross_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1038 Y5 R10 parent Omega/DCX vertical generator closure or beta-bound acquisition",
        "",
        "**Status:** attempted the exact no-pole route first. The obstruction is now brutally clear: the current corpus has the right target objects, but not the parent `Omega_Y`, parent-owned `D C_X`, all-field `v_X`, boundary `Q_X`, cocycle `K_boundary`, degree count, or matter/no-marker descent needed to claim no physical `X` pole.",
        "",
        "**Fallback:** source-backed beta-bound acquisition is staged across R10, WEP, clocks, PPN, and orbital/source tests. Every row remains nonclaim until MTS projection coefficients and units exist.",
        "",
        "**Important correction:** the old naked linear `c_g` R10 shorthand is quarantined. A source-test force needs `beta_s beta_t`; a universal Weyl leakage contributes as `c_g^2` unless a sourced source leg is explicitly declared inside `Qbar_XH`.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Omega/DCX closure audit",
        md_table(closure_rows, ["audit_id", "object", "needed_statement", "derivation_attempt", "current_status", "if_missing", "valid_for_claim"]),
        "## Vertical generator field map",
        md_table(vertical_rows, ["field_block", "candidate_vertical_action", "Omega_flat_target", "DCX_target", "status", "missing_input", "valid_for_claim"]),
        "## No-pole claim gate",
        md_table(gate_rows, ["gate_id", "claim", "gate_pass", "failure_reasons", "minimum_to_flip", "claim_allowed", "valid_for_claim"]),
        "## Beta-bound source acquisition",
        md_table(beta_rows, ["acquisition_id", "component", "empirical_anchor", "anchor_value_or_bound", "required_theory_projection", "current_status", "score_ready", "valid_for_claim"]),
        "## Legacy linear c_g quarantine",
        md_table(legacy_rows, ["quarantine_id", "source_row", "legacy_formula", "quarantine_action", "replacement_rule", "valid_for_claim"]),
        "## Cross-arena bound routing",
        md_table(cross_rows, ["route_id", "arena", "incoming_theory_row", "external_anchor", "blocker", "valid_for_claim"]),
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
    closure_rows = closure_audit_rows()
    vertical_rows = vertical_generator_rows()
    gate_rows = no_pole_gate_rows(closure_rows, vertical_rows)
    beta_rows = beta_acquisition_rows(local_bounds_index())
    legacy_rows = legacy_quarantine_rows()
    cross_rows = cross_arena_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(closure_rows, beta_rows, legacy_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        closure_rows,
        vertical_rows,
        gate_rows,
        beta_rows,
        legacy_rows,
        cross_rows,
        mts_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1038_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv", closure_rows)
    write_csv(OUT / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv", vertical_rows)
    write_csv(OUT / "P8_Y5_R10_1038_NO_POLE_CLAIM_GATE.csv", gate_rows)
    write_csv(OUT / "P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv", beta_rows)
    write_csv(OUT / "P8_Y5_R10_1038_LEGACY_LINEAR_CG_QUARANTINE.csv", legacy_rows)
    write_csv(OUT / "P8_Y5_R10_1038_CROSS_ARENA_BOUND_ROUTING.csv", cross_rows)
    write_csv(OUT / "P8_Y5_R10_1038_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1038_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1038_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1038_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1038_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1038_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        closure_rows,
        vertical_rows,
        gate_rows,
        beta_rows,
        legacy_rows,
        cross_rows,
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
        raise SystemExit(f"1038 validation failed: {failed}")


if __name__ == "__main__":
    main()
