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
DOC = ROOT / "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1037-R10-no-pole-beta-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1037_NO_POLE_OR_BETA_TEMPLATE_NONCLAIM.csv"
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


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        (
            "SRC1037_0_1036_next",
            "source-intake/mts_residuals/P8_Y5_R10_1036_NEXT_TARGET.csv",
            "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md",
            "1036 handoff to no-pole theorem or bounded beta runner.",
        ),
        (
            "SRC1037_1_1036_branch",
            "source-intake/mts_residuals/P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv",
            "BR1036_0_no_physical_X_pole",
            "1036 branch fork selecting no-pole as best route and bounded beta as fallback.",
        ),
        (
            "SRC1037_2_1036_parent_audit",
            "source-intake/mts_residuals/P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
            "PX1036_5_no_pole_alternative",
            "1036 parent finite-X/no-pole audit.",
        ),
        (
            "SRC1037_3_581_certificate",
            "source-intake/mts_residuals/P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv",
            "NPC581_6_claim_gate",
            "581 no-pole certificate template.",
        ),
        (
            "SRC1037_4_581_chain",
            "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
            "QVT581_7_alpha_result",
            "581 quotient/vertical theorem chain.",
        ),
        (
            "SRC1037_5_582_momentum",
            "source-intake/mts_residuals/P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
            "MMT582_4_no_pole_result",
            "582 first-class momentum-map closure theorem.",
        ),
        (
            "SRC1037_6_582_gate",
            "source-intake/mts_residuals/P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
            "NPG582_5_no_pole_claim",
            "582 no-pole gate failure status.",
        ),
        (
            "SRC1037_7_590_vertical_map",
            "source-intake/mts_residuals/P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
            "matter_readout",
            "590 field-by-field vertical action map.",
        ),
        (
            "SRC1037_8_590_gate",
            "source-intake/mts_residuals/P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
            "MCG590_6_matter_quotient",
            "590 mapping closure gate showing parent Omega/DC_X/vertical generator gaps.",
        ),
        (
            "SRC1037_9_670_no_pole",
            "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
            "NQ670_8_no_pole_result",
            "670 no-pole proof chain and missing premises.",
        ),
        (
            "SRC1037_10_1027_qbar_schema",
            "source-intake/mts_residuals/P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
            "BQT1027_3_total_abs_guard",
            "1027 bounded qbar_XT no-cancellation schema.",
        ),
        (
            "SRC1037_11_945_frame_bounds",
            "source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv",
            "BND945_0_cg_value",
            "945 first frame-leak bound rows.",
        ),
        (
            "SRC1037_12_bound_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 R10 bound review candidate, nonclaim.",
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


def no_pole_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "NP1037_0_q_kernel",
            "criterion": "vertical X is in the kernel of the parent quotient",
            "mathematical_test": "Dq[v_X]=0 and q is parent-defined before variation",
            "current_evidence": "670 gives conditional kernel transfer; 581 says parent projection is open",
            "result": "PARTIAL_MATH_ONLY_NOT_PARENT_SIGNED",
            "if_missing": "X can still be a physical field rather than a representative choice",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NP1037_1_action_descent",
            "criterion": "bulk action descends through q",
            "mathematical_test": "S_bulk[Phi]=S_red[q(Phi)] so H(v_X,.)=0 and no vertical Green operator exists",
            "current_evidence": "581/670 mark action factorization conditional; 1036 says parent X row not owned",
            "result": "CONDITIONAL_DESCENT_NOT_SIGNED",
            "if_missing": "a physical finite Hessian block can survive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NP1037_2_momentum_map",
            "criterion": "vertical X is generated by a first-class differentiable constraint",
            "mathematical_test": "delta G_X=Omega(delta Phi,v_X), G_X=int epsilon C_X+Q_X, and bracket closes",
            "current_evidence": "582 writes theorem; 590 says parent Omega, DC_X, v_X, boundary differentiability missing",
            "result": "MISSING_PARENT_OMEGA_DCX_VERTICAL_GENERATOR",
            "if_missing": "zero Hessian is not enough; it may indicate an under-specified field, edge mode, or second-class remnant",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NP1037_3_boundary_silence",
            "criterion": "vertical transformations carry no local boundary charge",
            "mathematical_test": "Q_X=0/exact/proper and K_boundary=0 for compact local vertical transformations",
            "current_evidence": "581/582/670 keep boundary charge, cocycle, and differentiability open",
            "result": "MISSING_BOUNDARY_CHARGE_ZERO",
            "if_missing": "X can reappear as edge hair or Qbar_XH source charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NP1037_4_degree_count",
            "criterion": "constraints remove the local X pair",
            "mathematical_test": "primary/secondary first-class pair removes X and reduced Omega has no proper X stabilizer",
            "current_evidence": "581/582/590 all leave rank/degree count incomplete",
            "result": "MISSING_DEGREE_COUNT",
            "if_missing": "no-pole cannot be distinguished from hidden dynamics",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NP1037_5_matter_readout",
            "criterion": "ordinary matter/readout descends through q and no marker sees X",
            "mathematical_test": "S_matter=Sbar[Obs(q(Phi)),psi,theta] and Lie_vX theta=0",
            "current_evidence": "1027/1028/955 write exact contracts but parent schema is unsigned",
            "result": "MISSING_MATTER_NO_MARKER_SIGNATURE",
            "if_missing": "beta_s/beta_t rows remain live even if the bulk pole is controlled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "NP1037_6_verdict",
            "criterion": "no physical local X pole in the GR/Newton branch",
            "mathematical_test": "NP1037_0 through NP1037_5 all close from one parent action",
            "current_evidence": "the route is sharp, but the parent certificate is incomplete",
            "result": "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED",
            "if_missing": "build bounded beta_s/beta_t runner and retain no-cancellation tails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def pole_countermodel_rows() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "PCM1037_0_second_class_X",
            "countermodel": "X has a degenerate-looking Hessian but constraints are second class or incomplete",
            "why_it_matters": "no Green kernel cannot be claimed without first-class closure and degree count",
            "blocked_by": "parent Omega, DC_X, bracket, degree-count proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "PCM1037_1_edge_mode",
            "countermodel": "bulk vertical variation is pure gauge, but boundary charge Q_X survives",
            "why_it_matters": "R10 source charge can be carried by Qbar_XH/edge hair",
            "blocked_by": "boundary differentiability, Q_X=0/proper/exact, K_boundary=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "PCM1037_2_shadow_matter_frame",
            "countermodel": "ordinary matter uses a universal X-dependent Weyl/disformal frame",
            "why_it_matters": "WEP may look fine while beta_s=beta_t=c_g and R10 sees c_g^2",
            "blocked_by": "no-shadow-frame theorem or numeric c_g/b_dis bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "PCM1037_3_marker_constants",
            "countermodel": "masses, EM constants, or material markers carry X-dependence",
            "why_it_matters": "clock/WEP/composition constraints become tied to R10 beta rows",
            "blocked_by": "no-marker theorem or b_A/b_alpha bounds",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "PCM1037_4_hidden_support",
            "countermodel": "non-Hilbert current, source support, or domain/boundary tail sources X",
            "why_it_matters": "alpha_X can survive even if visible Hilbert matter descends",
            "blocked_by": "q_nonH, Delta_W_support, q_domain, and q_boundary zero/bound rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bounded_beta_rows() -> list[dict[str, str]]:
    return [
        {
            "beta_id": "BB1037_0_beta_source_geom",
            "leg": "source",
            "symbol": "beta_s_geom",
            "definition": "source-body X charge from common Weyl/disformal observed-frame leakage",
            "formula_or_bound": "|beta_s_geom| <= |profile_s^W c_g| + |profile_s^dis b_dis|",
            "required_inputs": "profile_s^W;profile_s^dis;c_g;b_dis;source support;units;source_path",
            "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "observable_links": "R10;PPN;WEP;clock",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_1_beta_test_geom",
            "leg": "test",
            "symbol": "beta_t_geom",
            "definition": "test/readout X charge from common Weyl/disformal observed-frame leakage",
            "formula_or_bound": "|beta_t_geom| <= |tau_R10 c_g| + |tau_dis b_dis|",
            "required_inputs": "tau_R10;tau_dis;c_g;b_dis;test material/readout profile;units;source_path",
            "current_status": "MISSING_ARENA_PROJECTION",
            "observable_links": "R10;PPN;WEP;clock",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_2_beta_source_marker",
            "leg": "source",
            "symbol": "beta_s_marker",
            "definition": "source composition/material/EM marker X charge",
            "formula_or_bound": "|beta_s_marker| <= sum_A |S_sA b_A| + |S_salpha b_alpha|",
            "required_inputs": "source material sensitivities;b_A;b_alpha;EM/binding convention;source_path",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "observable_links": "WEP;clock;composition;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_3_beta_test_marker",
            "leg": "test",
            "symbol": "beta_t_marker",
            "definition": "test material/readout marker X charge",
            "formula_or_bound": "|beta_t_marker| <= sum_A |S_tA b_A| + |S_talpha b_alpha|",
            "required_inputs": "test material sensitivities;b_A;b_alpha;readout convention;source_path",
            "current_status": "MISSING_MARKER_READOUT_PROJECTION",
            "observable_links": "WEP;clock;composition;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_4_beta_source_nonH",
            "leg": "source",
            "symbol": "beta_s_nonH",
            "definition": "source-side non-Hilbert/boundary/domain/support X current",
            "formula_or_bound": "|beta_s_nonH| <= |q_nonH_s| + |Delta_W_support_s| + |q_domain_s| + |q_boundary_s|",
            "required_inputs": "non-Hilbert current;support shift;domain current;boundary charge;units;source_path",
            "current_status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "observable_links": "R10;orbital;source_normalization;local_GR",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_5_beta_test_nonH",
            "leg": "test",
            "symbol": "beta_t_nonH",
            "definition": "test/readout-side non-Hilbert/boundary/domain/support X current",
            "formula_or_bound": "|beta_t_nonH| <= |q_nonH_t| + |Delta_W_support_t| + |q_domain_t| + |q_boundary_t|",
            "required_inputs": "readout support;non-Hilbert current;domain/boundary tail;units;source_path",
            "current_status": "MISSING_HIDDEN_TEST_ZERO_OR_NUMERIC_BOUND",
            "observable_links": "R10;orbital;source_normalization;local_GR",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_6_beta_abs_totals",
            "leg": "source_and_test",
            "symbol": "beta_s_abs;beta_t_abs",
            "definition": "absolute no-cancellation source/test beta envelopes",
            "formula_or_bound": "beta_s_abs=sum_i |beta_s_i|; beta_t_abs=sum_i |beta_t_i|",
            "required_inputs": "all component rows BB1037_0 through BB1037_5 theorem-zero or numeric/source-backed",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "observable_links": "all_local_arenas",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "beta_id": "BB1037_7_beta_product_guard",
            "leg": "source_times_test",
            "symbol": "abs_beta_product",
            "definition": "claim-safe source-test product for finite exchange",
            "formula_or_bound": "|beta_s beta_t| <= beta_s_abs beta_t_abs; universal Weyl gives c_g^2 contribution",
            "required_inputs": "beta_s_abs;beta_t_abs;declaration whether Qbar_XH already contains source leg",
            "current_status": "CLAIM_BLOCKED",
            "observable_links": "R10;PPN;WEP;clock;orbital",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tail_envelope_rows() -> list[dict[str, str]]:
    return [
        {
            "tail_id": "TAIL1037_0_alpha_envelope",
            "quantity": "abs_alpha_X(lambda)",
            "formula": "|alpha_X| <= |K_X^R10(lambda)| * [beta_s_abs beta_t_abs + abs_tail_source_test(lambda)]",
            "missing_inputs": "K_X^R10;beta_s_abs;beta_t_abs;tail rows;promoted alpha_bound(lambda)",
            "current_status": "MISSING_NUMERIC_ENVELOPE",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tail_id": "TAIL1037_1_no_cancellation_policy",
            "quantity": "tail addition rule",
            "formula": "unknown components add in absolute value; no cancellation credit between c_g,b_dis,b_A,b_alpha,q_nonH,boundary/support",
            "missing_inputs": "component theorem-zero or numeric/source-backed bounds",
            "current_status": "POLICY_ACTIVE",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tail_id": "TAIL1037_2_R10_score_gate",
            "quantity": "R10 comparison gate",
            "formula": "score only if abs_alpha_X(lambda) and alpha_bound(lambda) are numeric, sourced, unit-matched, and valid_for_claim=true",
            "missing_inputs": "MTS prediction and promoted bound curve",
            "current_status": "CLAIM_BLOCKED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def arena_routing_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ARENA1037_0_R10",
            "arena": "short-range fifth force",
            "receives": "K_X^R10 beta_s beta_t plus absolute tails",
            "required_projection": "lambda profile, source/test support, tau_R10, bound curve",
            "current_status": "BLOCKED_BY_BETA_KX_BOUND",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "arena_id": "ARENA1037_1_PPN",
            "arena": "PPN/local weak field",
            "receives": "common frame c_g, disformal b_dis, non-Hilbert/support tails",
            "required_projection": "gauge-fixed response matrix for gamma,beta,preferred-frame rows",
            "current_status": "BLOCKED_ARENA_PROJECTION_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "arena_id": "ARENA1037_2_WEP_clock",
            "arena": "WEP, clocks, EM/material markers",
            "receives": "b_A,b_alpha,c_g marker/readout sensitivities",
            "required_projection": "material sensitivities, clock coefficients, composition pairs",
            "current_status": "BLOCKED_MARKER_DESCENT_OR_NUMERIC_BOUNDS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "arena_id": "ARENA1037_3_orbital_source",
            "arena": "orbital/source normalization/local GR",
            "receives": "q_nonH, Delta_W_support, boundary/domain support tails",
            "required_projection": "worldtube/source support and orbital observable map",
            "current_status": "BLOCKED_SUPPORT_THEOREM_OR_BOUND_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "no_physical_X_pole_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1037_NO_POLE_OR_BETA_TEMPLATE_NONCLAIM",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_NO_PHYSICAL_X_POLE_CERTIFICATE",
            "alpha_bound": "not_applicable_until_no_pole_theorem_signed",
            "alpha_bound_source": "not_applicable_until_no_pole_theorem_signed",
            "force_law_form": "no active finite Yukawa pole only if quotient/constraint/boundary/matter certificate closes",
            "derivation_status": "template_invalid_no_pole_not_parent_signed",
            "formula_reference": "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md::NP1037_6",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "no alpha=0 credit without full no-pole certificate",
            "valid_for_claim": "false",
            "notes": "Structural route only; current claim fails.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "bounded_beta_product_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1037_NO_POLE_OR_BETA_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_TIMES_BETA_S_ABS_BETA_T_ABS_TAILS",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "|alpha_X| <= |K_X^R10| [beta_s_abs beta_t_abs + abs_tail]",
            "derivation_status": "template_invalid_bounded_beta_inputs_missing",
            "formula_reference": "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md::TAIL1037_0",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "absolute no-cancellation envelope; c_g contributes quadratically in universal Weyl branch",
            "valid_for_claim": "false",
            "notes": "Fallback runner row only.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "universal_weyl_cg_squared_template",
            "curve_id": "R10_alpha_lambda_curve_MTS_1037_NO_POLE_OR_BETA_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_PROFILE_CG_SQUARED",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "universal Weyl source/test branch: alpha_X proportional to K_X^R10 c_g^2",
            "derivation_status": "template_invalid_cg_and_KX_missing",
            "formula_reference": "1037-Y5-R10-no-physical-X-pole-theorem-or-bounded-beta-runner.md::BB1037_7",
            "source_file": "MISSING_PARENT_SOURCE_FILE",
            "assumptions": "linear-c_g scoring forbidden unless source leg is already explicitly inside Qbar_XH",
            "valid_for_claim": "false",
            "notes": "Coupling-law guard row.",
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1037_0_runner_status",
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


def placeholder_refusal_rows(beta_rows: list[dict[str, str]], no_pole_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, row in enumerate(no_pole_rows):
        rows.append(
            {
                "refusal_id": f"REF1037_NOPOLE_{index}",
                "object": row["criterion"],
                "current_status": row["result"],
                "refusal_status": "no_pole_claim_rejected_current_corpus",
                "failure_reasons": f"{row['result']};CLAIM_POLICY_FALSE",
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for index, row in enumerate(beta_rows):
        rows.append(
            {
                "refusal_id": f"REF1037_BETA_{index}",
                "object": row["symbol"],
                "current_status": row["current_status"],
                "refusal_status": "bounded_beta_row_rejected_missing_inputs",
                "failure_reasons": f"{row['current_status']};SCORE_READY_FALSE;CLAIM_POLICY_FALSE",
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
            "gate_id": "CGATE1037_0_no_pole",
            "claim": "finite local X mode has no physical pole",
            "gate_pass": "false",
            "reason": "parent Omega, DC_X, vertical action, boundary charge, degree count, and matter/no-marker signature remain incomplete",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1037_1_alpha_zero",
            "claim": "R10 alpha_X=0 locally",
            "gate_pass": "false",
            "reason": "no-pole and hidden-tail clauses are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1037_2_bounded_beta",
            "claim": "bounded beta_s/beta_t rows are score-ready",
            "gate_pass": "false",
            "reason": "all beta component rows still contain missing theorem-zero or numeric/source-backed inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1037_3_linear_cg",
            "claim": "linear c_g can be scored against R10",
            "gate_pass": "false",
            "reason": "universal Weyl source/test branch contributes c_g squared",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1037_4_R10_pass",
            "claim": "R10 pass is established",
            "gate_pass": "false",
            "reason": "MTS rows and external bound curve remain nonclaim/unscoreable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1037_0_no_pole_status",
            "decision": "No-pole remains the cleanest GR-reduction route, but it fails current-claim status.",
            "because": "the route requires parent Omega, DC_X, field-by-field vertical generator, boundary charge silence, degree count, and matter/no-marker descent together.",
            "next_action": "attack the missing parent Omega/DC_X/vertical-generator closure directly",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1037_1_beta_fallback_status",
            "decision": "The fallback is now a bounded beta_s/beta_t acquisition problem.",
            "because": "if a physical finite pole survives, R10 must see beta_s beta_t plus absolute tails, not a single coupling.",
            "next_action": "fill theorem-zero or numeric/source-backed beta component rows one by one",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1037_2_empirical_status",
            "decision": "Testing can proceed only after parent or beta rows exist.",
            "because": "the R10 curve is still review-candidate and the MTS alpha template has no valid numeric rows.",
            "next_action": "keep runner smoke blocked until promoted data and beta/K_X rows exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1037_3_next_target",
            "decision": "Next target is parent Omega/DC_X/vertical generator closure or beta bound acquisition.",
            "because": "that is the exact missing object list behind the no-pole theorem; failing it moves us honestly to bounded residuals.",
            "next_action": "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
            "objective": "try to close the exact no-pole certificate objects: parent symplectic form Omega, D C_X, field-by-field vertical generator, boundary differentiability, bracket closure, and degree count; if this fails, start source-backed beta bound acquisition",
            "include": "Omega-flat map, DC_X operator, vertical action on metric/coframe/matter/boundary fields, Q_X boundary charge, K_boundary, reduced degree count, beta_s/beta_t acquisition schema",
            "exclude": "asserted gauge/no-pole status, invented beta values, linear-c_g R10 scoring, cancellation between tails, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    no_pole_rows: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    tail_rows: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1037_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1037 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1037_1_no_pole_audit_complete",
            len(no_pole_rows) >= 7
            and any(row["result"] == "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED" for row in no_pole_rows),
            "no-pole audit covers q-kernel, action descent, momentum map, boundary, degree count, matter, and verdict",
        )
    )
    checks.append(
        (
            "V1037_2_countermodels_complete",
            len(countermodels) >= 5
            and all(not flag(row["valid_for_claim"]) for row in countermodels),
            "countermodel ledger blocks weak no-pole shortcuts",
        )
    )
    checks.append(
        (
            "V1037_3_beta_rows_complete",
            len(beta_rows) >= 8
            and any("c_g^2" in row["formula_or_bound"] for row in beta_rows)
            and all(row["score_ready"] == "false" for row in beta_rows),
            "bounded beta schema includes source/test legs and c_g-squared guard",
        )
    )
    checks.append(
        (
            "V1037_4_tail_envelope_active",
            any(row["tail_id"] == "TAIL1037_1_no_cancellation_policy" for row in tail_rows)
            and all(not flag(row["claim_allowed"]) for row in tail_rows),
            "absolute no-cancellation tail policy is active",
        )
    )
    checks.append(
        (
            "V1037_5_arena_routing_complete",
            {row["arena_id"] for row in arena_rows}
            == {"ARENA1037_0_R10", "ARENA1037_1_PPN", "ARENA1037_2_WEP_clock", "ARENA1037_3_orbital_source"},
            "arena routing covers R10, PPN, WEP/clock, and orbital/source channels",
        )
    )
    checks.append(
        (
            "V1037_6_mts_template_schema",
            bool(mts_rows) and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys())),
            "MTS R10 alpha template has existing runner schema",
        )
    )
    checks.append(
        (
            "V1037_7_mts_template_nonclaim",
            bool(mts_rows) and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS template rows remain nonclaim",
        )
    )
    checks.append(
        (
            "V1037_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false",
            "existing R10 runner refuses the 1037 nonclaim smoke rows",
        )
    )
    checks.append(
        (
            "V1037_9_claim_gates_blocked",
            all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claim_rows),
            "all claim gates refuse promotion",
        )
    )
    checks.append(
        (
            "V1037_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1037_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
        OUT / "P8_Y5_R10_1037_POLE_COUNTERMODEL_LEDGER.csv",
        OUT / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv",
        OUT / "P8_Y5_R10_1037_ABSOLUTE_TAIL_ENVELOPE.csv",
        OUT / "P8_Y5_R10_1037_ARENA_ROUTING_MAP.csv",
        OUT / "P8_Y5_R10_1037_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1037_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1037_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1037_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1037_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1037_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1037_11_generated_files_in_post_checkpoint",
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
            "V1037_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1037_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1037 no-pole theorem or bounded beta runner validation summary",
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
    no_pole_rows: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    tail_rows: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1037 Y5 R10 no physical X pole theorem or bounded beta runner",
        "",
        "**Status:** The no-physical-`X`-pole route is still the cleanest local-GR reduction route, but it is **not proved** in the current corpus. The exact missing objects are now isolated: parent `Omega`, `D C_X`, field-by-field vertical action, boundary differentiability/charge, bracket closure, degree count, and matter/no-marker descent.",
        "",
        "**Fallback:** if the no-pole certificate does not close, the finite branch is a bounded `beta_s beta_t` problem with absolute tails. R10 must not be scored with a naked linear `c_g`; universal Weyl source/test coupling contributes as `c_g^2`.",
        "",
        "**Claim ceiling:** no `alpha=0`, no no-pole claim, no invented beta values, no linear-`c_g` R10 score, no R10/local-GR pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1037.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## No physical X pole audit",
        md_table(no_pole_rows, ["audit_id", "criterion", "mathematical_test", "result", "if_missing", "valid_for_claim"]),
        "## Pole countermodel ledger",
        md_table(countermodels, ["countermodel_id", "countermodel", "why_it_matters", "blocked_by", "valid_for_claim"]),
        "## Bounded beta source/test template",
        md_table(beta_rows, ["beta_id", "leg", "symbol", "formula_or_bound", "current_status", "observable_links", "score_ready", "valid_for_claim"]),
        "## Absolute tail envelope",
        md_table(tail_rows, ["tail_id", "quantity", "formula", "missing_inputs", "current_status", "claim_allowed", "valid_for_claim"]),
        "## Arena routing map",
        md_table(arena_rows, ["arena_id", "arena", "receives", "required_projection", "current_status", "valid_for_claim"]),
        "## MTS alpha template update",
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
    no_pole_rows = no_pole_audit_rows()
    countermodels = pole_countermodel_rows()
    beta_rows = bounded_beta_rows()
    tail_rows = tail_envelope_rows()
    arena_rows = arena_routing_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(beta_rows, no_pole_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        no_pole_rows,
        countermodels,
        beta_rows,
        tail_rows,
        arena_rows,
        mts_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1037_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv", no_pole_rows)
    write_csv(OUT / "P8_Y5_R10_1037_POLE_COUNTERMODEL_LEDGER.csv", countermodels)
    write_csv(OUT / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv", beta_rows)
    write_csv(OUT / "P8_Y5_R10_1037_ABSOLUTE_TAIL_ENVELOPE.csv", tail_rows)
    write_csv(OUT / "P8_Y5_R10_1037_ARENA_ROUTING_MAP.csv", arena_rows)
    write_csv(OUT / "P8_Y5_R10_1037_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1037_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1037_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1037_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1037_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1037_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        no_pole_rows,
        countermodels,
        beta_rows,
        tail_rows,
        arena_rows,
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
        raise SystemExit(f"1037 validation failed: {failed}")


if __name__ == "__main__":
    main()
