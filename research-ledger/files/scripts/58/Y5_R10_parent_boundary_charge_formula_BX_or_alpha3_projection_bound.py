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
DOC = ROOT / "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1040-R10-BX-alpha3-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1040_BX_ALPHA3_TEMPLATE_NONCLAIM.csv"
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
            "SRC1040_0_1039_next",
            "source-intake/mts_residuals/P8_Y5_R10_1039_NEXT_TARGET.csv",
            "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "1039 handoff to explicit B_X/Q_X or alpha3 projection coefficient row.",
        ),
        (
            "SRC1040_1_1039_lemma",
            "source-intake/mts_residuals/P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
            "QK1039_5_source_boundary_limit",
            "1039 compact/proper zero sublemma and source-boundary blocker.",
        ),
        (
            "SRC1040_2_1039_projection",
            "source-intake/mts_residuals/P8_Y5_R10_1039_FIRST_BETA_PROJECTION_TEMPLATE.csv",
            "FBP1039_0_boundary_alpha3",
            "1039 first beta projection template.",
        ),
        (
            "SRC1040_3_667_variation",
            "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv",
            "VL667_3_Hamiltonian_variation",
            "667 covariant phase-space and Hamiltonian boundary variation ledger.",
        ),
        (
            "SRC1040_4_668_owner",
            "source-intake/mts_residuals/P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
            "SO668_2_MTS_extra_LX",
            "668 owner audit showing L_X, Theta_X, Q_X missing sector-by-sector.",
        ),
        (
            "SRC1040_5_591_DCX",
            "source-intake/mts_residuals/P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
            "DC591_4_boundary_pairing",
            "591 DC_X boundary-pairing formula.",
        ),
        (
            "SRC1040_6_584_repair",
            "source-intake/mts_residuals/P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv",
            "OR584_2_boundary_exact_repair",
            "584 owner repair attempt for boundary exactness.",
        ),
        (
            "SRC1040_7_584_edge_law",
            "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv",
            "EEL584_0_edge_charge",
            "584 symbolic edge charge law.",
        ),
        (
            "SRC1040_8_671_owner_gate",
            "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
            "BCG671_0_boundary_charge_definition",
            "671 boundary charge owner gate.",
        ),
        (
            "SRC1040_9_1019_exactness",
            "source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
            "BE1019_6_verdict",
            "1019 exactness/counterterm/cocycle clauses.",
        ),
        (
            "SRC1040_10_976_alpha3",
            "source-intake/mts_residuals/P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv",
            "KBA976_0_formula",
            "976 K_boundary alpha3 source acquisition.",
        ),
        (
            "SRC1040_11_977_alpha3_status",
            "source-intake/mts_residuals/P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv",
            "KBS977_0_alpha3_formula",
            "977 K_boundary alpha3 status.",
        ),
        (
            "SRC1040_12_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R7_alpha3",
            "Local bound ledger with alpha3 anchor.",
        ),
        (
            "SRC1040_13_R10_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 nonclaim R10 bound review candidate.",
        ),
        (
            "SRC1040_14_R10_runner",
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


def bx_formula_rows() -> list[dict[str, str]]:
    return [
        {
            "formula_id": "BX1040_0_bulk_pairing",
            "object": "boundary pairing from D C_X",
            "formula": "delta int_Sigma epsilon_nu C_X^nu contains - int_partialSigma n_mu epsilon_nu delta P_X^{mu nu} plus convention-dependent density terms",
            "derivation_status": "DERIVED_FROM_DCX_CONTRACT",
            "owner_status": "P_X and density convention not parent-owned",
            "claim_effect": "identifies the boundary charge density that must be cancelled, exact, or bounded",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "BX1040_1_candidate_charge_density",
            "object": "B_X surface density",
            "formula": "B_X^nu = sigma n_mu P_X^{mu nu} + B_ct^nu + B_ref^nu + B_exact^nu, with sigma fixed by the G_bulk +/- Q convention",
            "derivation_status": "FORMULA_SHAPE_DERIVED_SIGN_CONVENTION_OPEN",
            "owner_status": "P_X, counterterm, reference subtraction, and exact primitive missing",
            "claim_effect": "turns edge charge into a concrete coefficient contract rather than an undefined coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "BX1040_2_candidate_QX",
            "object": "Q_X boundary charge",
            "formula": "Q_X[epsilon] = int_partialSigma epsilon_nu B_X^nu dS",
            "derivation_status": "CONTRACT_READY_NOT_PARENT_SIGNED",
            "owner_status": "requires Theta_X/L_X sector owner and allowed boundary class",
            "claim_effect": "proper compact branch gives zero; source/large branch remains scoreable residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "BX1040_3_exactness_route",
            "object": "exact/pure boundary repair",
            "formula": "B_X = d_boundary b_X + B_X^pure and int_partialSigma epsilon d_boundary b_X = int_partialpartialSigma epsilon b_X - int_partialSigma d_boundary epsilon b_X",
            "derivation_status": "MATHEMATICAL_ROUTE_ONLY",
            "owner_status": "b_X, harmonic sector, corner terms, and kernel derivative term not derived",
            "claim_effect": "exactness can close only with boundary-class and range-kernel conditions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "BX1040_4_verdict",
            "object": "parent B_X/Q_X formula status",
            "formula": "B_X/Q_X formula shape is now explicit, but parent ownership is not closed",
            "derivation_status": "FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED",
            "owner_status": "MISSING_PARENT_LX_THETAX_PX_REFERENCE_PROJECTOR",
            "claim_effect": "move to parent source row or alpha3/R10 nonclaim coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def bx_owner_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "BXG1040_0_LX_owner",
            "needed_object": "parent L_X sector",
            "closure_test": "L_X[g,X,nabla X] explicitly selected with field normalization and boundary class",
            "current_status": "MISSING_SECTOR_LAGRANGIAN_OWNER",
            "if_missing": "Theta_X and P_X remain formal placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1040_1_ThetaX_owner",
            "needed_object": "parent symplectic potential Theta_X",
            "closure_test": "delta L_X = E_X delta X + d Theta_X(delta X) with finite boundary jet order",
            "current_status": "MISSING_THETA_X",
            "if_missing": "Q_X differentiability and K_boundary bracket cannot be computed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1040_2_PX_owner",
            "needed_object": "boundary momentum P_X^{mu nu}",
            "closure_test": "P_X is derived from L_X or V_def, not inserted as a free tensor",
            "current_status": "MISSING_PX_OWNER",
            "if_missing": "B_X = n.P_X is a contract only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1040_3_density_convention",
            "needed_object": "tensor versus densitized P convention",
            "closure_test": "choose C_X=-nabla P+J or C_X=-(1/sqrt(g))partial Ptilde+J before scoring signs/units",
            "current_status": "CONVENTION_GATE_OPEN",
            "if_missing": "B_X sign, volume terms, and units are ambiguous",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1040_4_source_boundary_class",
            "needed_object": "allowed non-proper source boundary class",
            "closure_test": "source worldtube, reference surface, and compact exterior boundary classes are separated",
            "current_status": "MISSING_SOURCE_BOUNDARY_CLASS",
            "if_missing": "proper-gauge zero may be incorrectly promoted to a source/test theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1040_5_verdict",
            "needed_object": "claim-grade B_X owner package",
            "closure_test": "BXG1040_0 through BXG1040_4 pass together",
            "current_status": "FAIL_CURRENT_CLAIM_BX_NOT_PARENT_OWNED",
            "if_missing": "keep B_X/Q_X rows as nonclaim coefficient contracts",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def reference_projector_rows() -> list[dict[str, str]]:
    return [
        {
            "split_id": "RPS1040_0_observed_GR_charge",
            "sector": "observed EH/ADM/time/rotation charge",
            "rule": "retain in Q_obs and do not force to zero by representative-X proper-domain choice",
            "missing": "Pi_EH/Pi_M reference action on the full Q_tau charge",
            "claim_status": "GUARD_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "split_id": "RPS1040_1_representative_X_charge",
            "sector": "proper compact representative-X charge",
            "rule": "Q_X^proper=0 from 1039 collar lemma",
            "missing": "extension to non-proper/source boundary values",
            "claim_status": "NARROW_ZERO_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "split_id": "RPS1040_2_edge_source_projection",
            "sector": "edge/source residual charge",
            "rule": "Qbar_edge_XH(lambda)=Pi_M^H[int_partialSigma F_lambda epsilon.B_X]/M_H",
            "missing": "Pi_M^H, F_lambda, B_X owner, source boundary class, units",
            "claim_status": "RETAIN_NONCLAIM_RESIDUAL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "split_id": "RPS1040_3_no_double_count",
            "sector": "bulk plus edge source split",
            "rule": "alpha_total uses orthogonal split or absolute addition; no cancellation credit between bulk and edge rows",
            "missing": "projection orthogonality proof or numeric split",
            "claim_status": "RETAIN_ABSOLUTE_TAIL_POLICY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def kboundary_cocycle_rows() -> list[dict[str, str]]:
    return [
        {
            "cocycle_id": "KBC1040_0_contract",
            "object": "boundary cocycle",
            "formula": "K_boundary[epsilon,eta]=delta_eta Q_X[epsilon]-delta_epsilon Q_X[eta]-Q_X[[epsilon,eta]] plus possible i_{v_eta}i_{v_epsilon} Omega_boundary convention terms",
            "needed_inputs": "differentiable G_X, parent Omega_Y, v_X action on all fields, sign convention",
            "current_status": "FORMULA_CONTRACT_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "cocycle_id": "KBC1040_1_proper_zero",
            "object": "proper compact cocycle",
            "formula": "K_boundary=0 when epsilon, eta, and required finite jets vanish on the boundary collar",
            "needed_inputs": "same finite-jet boundary class as 1039",
            "current_status": "NARROW_ZERO_INHERITED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "cocycle_id": "KBC1040_2_source_alpha3",
            "object": "preferred-frame flux projection",
            "formula": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "needed_inputs": "K_boundary_alpha3, Phi_boundary_local, projection normalization",
            "current_status": "SOURCE_ANCHOR_READY_COEFFICIENTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha3_projection_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    alpha3 = bounds.get("R7_alpha3", {})
    return [
        {
            "projection_id": "A3P1040_0_formula",
            "observable": "alpha3",
            "mts_formula": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "external_bound": alpha3.get("upper_bound", "MISSING_R7_ALPHA3_BOUND"),
            "units": alpha3.get("units", "dimensionless"),
            "reference": alpha3.get("reference_path_or_url", "MISSING_R7_ALPHA3_SOURCE"),
            "coefficient_bound_rule": "if Phi_boundary_local is numeric and nonzero, |K_boundary_alpha3| <= 4e-20/|Phi_boundary_local|",
            "current_status": "COEFFICIENT_RULE_WRITTEN_PHI_AND_K_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "A3P1040_1_theorem_zero_route",
            "observable": "alpha3",
            "mts_formula": "alpha3_MTS = 0 if K_boundary_alpha3=0 or Phi_boundary_local=0 from a parent theorem",
            "external_bound": alpha3.get("upper_bound", "MISSING_R7_ALPHA3_BOUND"),
            "units": alpha3.get("units", "dimensionless"),
            "reference": alpha3.get("reference_path_or_url", "MISSING_R7_ALPHA3_SOURCE"),
            "coefficient_bound_rule": "theorem-zero must cite B_X exactness/no-flux or boundary flux amplitude zero",
            "current_status": "THEOREM_ZERO_NOT_SIGNED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "projection_id": "A3P1040_2_numeric_route",
            "observable": "alpha3",
            "mts_formula": "|K_boundary_alpha3 * Phi_boundary_local| <= 4e-20",
            "external_bound": alpha3.get("upper_bound", "MISSING_R7_ALPHA3_BOUND"),
            "units": alpha3.get("units", "dimensionless"),
            "reference": alpha3.get("reference_path_or_url", "MISSING_R7_ALPHA3_SOURCE"),
            "coefficient_bound_rule": "requires source-backed K, Phi, normalization, uncertainty policy, and no-cancellation tail addition",
            "current_status": "NUMERIC_ROUTE_INPUTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def r10_edge_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "edge_id": "R10E1040_0_Qbar_edge",
            "symbol": "Qbar_edge_XH(lambda)",
            "formula": "Pi_M^H[int_partialSigma F_lambda(s) epsilon_nu B_X^nu(s) dS]/M_H",
            "missing_inputs": "B_X owner; F_lambda; Pi_M^H; source boundary class; units",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "edge_id": "R10E1040_1_alpha_edge",
            "symbol": "alpha_edge(lambda)",
            "formula": "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT(lambda)",
            "missing_inputs": "K_edge; Qbar_edge_XH; qbar_XT; lambda support; promoted R10 bound curve",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "BX_QX_formula_contract",
            "curve_id": "MTS_1040_BX_QX_CONTRACT",
            "lambda_value": "MISSING_SOURCE_BOUNDARY_CLASS",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_BX_OWNER_AND_EDGE_PROJECTION",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "Q_X[epsilon]=int_partialSigma epsilon_nu(sigma n_mu P_X^{mu nu}+B_ct^nu+B_ref^nu+B_exact^nu)dS",
            "derivation_status": "template_invalid_formula_shape_not_parent_owned",
            "formula_reference": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md::BX1040_2",
            "source_file": "MISSING_PARENT_LX_THETAX_SOURCE_FILE",
            "assumptions": "sign/density/reference convention not claim-grade",
            "valid_for_claim": "false",
            "notes": "Concrete formula contract, not R10 evidence.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "boundary_alpha3_projection_bound_rule",
            "curve_id": "MTS_1040_ALPHA3_COEFFICIENT_TEMPLATE",
            "lambda_value": "MISSING_NOT_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL",
            "alpha_bound": "4e-20",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R7_alpha3",
            "force_law_form": "alpha3_MTS=K_boundary_alpha3 Phi_boundary_local; |K|<=4e-20/|Phi| if Phi is sourced nonzero",
            "derivation_status": "template_invalid_alpha3_coefficients_missing",
            "formula_reference": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md::A3P1040_0",
            "source_file": "MISSING_K_BOUNDARY_ALPHA3_OR_PHI_SOURCE_FILE",
            "assumptions": "alpha3 anchor is source-backed; MTS coefficient row is not",
            "valid_for_claim": "false",
            "notes": "First executable bound rule staged but nonclaim.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "R10_edge_contract",
            "curve_id": "MTS_1040_R10_EDGE_CONTRACT",
            "lambda_value": "MISSING_EDGE_LAMBDA_SUPPORT",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KEDGE_QBAR_EDGE_QBAR_XT",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT(lambda)",
            "derivation_status": "template_invalid_edge_inputs_missing",
            "formula_reference": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md::R10E1040_1",
            "source_file": "MISSING_EDGE_SOURCE_FILE",
            "assumptions": "no cancellation with bulk or frame tails",
            "valid_for_claim": "false",
            "notes": "R10 edge contract remains blocked.",
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1040_0_runner_status",
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
    formula_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in formula_rows:
        rows.append(
            {
                "refusal_id": f"REF1040_{row['formula_id']}",
                "object": row["object"],
                "current_status": row["derivation_status"],
                "refusal_status": "formula_not_claim_promoted",
                "failure_reasons": row["owner_status"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in owner_rows:
        rows.append(
            {
                "refusal_id": f"REF1040_{row['gate_id']}",
                "object": row["needed_object"],
                "current_status": row["current_status"],
                "refusal_status": "owner_gate_failed",
                "failure_reasons": row["if_missing"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in alpha3_rows:
        rows.append(
            {
                "refusal_id": f"REF1040_{row['projection_id']}",
                "object": row["mts_formula"],
                "current_status": row["current_status"],
                "refusal_status": "alpha3_projection_not_scoreable",
                "failure_reasons": row["coefficient_bound_rule"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in edge_rows:
        rows.append(
            {
                "refusal_id": f"REF1040_{row['edge_id']}",
                "object": row["symbol"],
                "current_status": row["missing_inputs"],
                "refusal_status": "R10_edge_row_not_scoreable",
                "failure_reasons": row["missing_inputs"],
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
            "gate_id": "CGATE1040_0_BX_formula",
            "claim": "B_X/Q_X is parent-derived",
            "gate_pass": "false",
            "reason": "formula shape is explicit, but L_X, Theta_X, P_X, density convention, reference terms, and boundary class are not parent-owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1040_1_local_GR_boundary",
            "claim": "full local-GR boundary silence is closed",
            "gate_pass": "false",
            "reason": "proper compact silence remains narrow; non-proper/source boundary and projection rows remain active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1040_2_alpha3",
            "claim": "alpha3 projection row is executable",
            "gate_pass": "false",
            "reason": "source-backed alpha3 bound exists but K_boundary_alpha3 and Phi_boundary_local are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1040_3_R10_edge",
            "claim": "R10 edge contract is score-ready",
            "gate_pass": "false",
            "reason": "K_edge, Qbar_edge_XH, qbar_XT, lambda support, and promoted bound curve are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1040_0_formula_status",
            "decision": "B_X/Q_X is now a concrete formula contract, not a vague missing coupling.",
            "because": "DC_X boundary pairing fixes the required surface density up to sign/density/reference conventions.",
            "next_action": "select or derive the parent L_X/Theta_X/P_X package, or retain the formula as a nonclaim coefficient contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1040_1_alpha3_status",
            "decision": "alpha3 has a usable bound rule but no MTS coefficient yet.",
            "because": "|K_boundary_alpha3 Phi_boundary_local| <= 4e-20 is the exact scoring inequality once K and Phi exist.",
            "next_action": "derive theorem-zero for K/Phi or source numeric values with normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1040_2_next_target",
            "decision": "Next target should try to source the parent X-sector symplectic potential.",
            "because": "Theta_X is the upstream object that would fix P_X, B_X, differentiability, K_boundary, and the alpha3 projection coefficient.",
            "next_action": "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
            "objective": "try to derive or select the parent X-sector symplectic potential Theta_X and momentum P_X that own B_X; if this cannot close, create nonclaim priors/templates for K_boundary_alpha3 and Phi_boundary_local",
            "include": "candidate L_X blocks, delta L_X, Theta_X, P_X tensor/density convention, boundary finite-jet order, no-flux theorem-zero route, alpha3 coefficient prior schema",
            "exclude": "invented numeric K/Phi values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    split_rows: list[dict[str, str]],
    cocycle_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1040_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1040 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1040_1_BX_formula_contract",
            any(row["formula_id"] == "BX1040_1_candidate_charge_density" and "B_X^nu" in row["formula"] for row in formula_rows)
            and any(row["formula_id"] == "BX1040_4_verdict" and row["derivation_status"] == "FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED" for row in formula_rows),
            "B_X/Q_X formula contract is written but not parent-promoted",
        )
    )
    checks.append(
        (
            "V1040_2_owner_gates_fail_safely",
            len(owner_rows) >= 6
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_BX_NOT_PARENT_OWNED" for row in owner_rows)
            and all(not flag(row["valid_for_claim"]) for row in owner_rows),
            "owner gates identify missing L_X/Theta_X/P_X package",
        )
    )
    checks.append(
        (
            "V1040_3_reference_projector_guard",
            {"observed EH/ADM/time/rotation charge", "edge/source residual charge", "bulk plus edge source split"}.issubset(
                {row["sector"] for row in split_rows}
            ),
            "reference/projector split protects GR charges and keeps edge residual separate",
        )
    )
    checks.append(
        (
            "V1040_4_cocycle_contract",
            any(row["cocycle_id"] == "KBC1040_0_contract" and "delta_eta Q_X" in row["formula"] for row in cocycle_rows)
            and any(row["cocycle_id"] == "KBC1040_2_source_alpha3" for row in cocycle_rows),
            "K_boundary cocycle and alpha3 projection contracts are present",
        )
    )
    checks.append(
        (
            "V1040_5_alpha3_bound_rule",
            any(
                row["projection_id"] == "A3P1040_0_formula"
                and row["external_bound"] == "4e-20"
                and row["score_ready"] == "false"
                for row in alpha3_rows
            ),
            "alpha3 coefficient bound rule uses source-backed anchor but remains nonclaim",
        )
    )
    checks.append(
        (
            "V1040_6_R10_edge_contract_nonclaim",
            len(edge_rows) >= 2 and all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in edge_rows),
            "R10 edge contract remains nonclaim and non-scoreable",
        )
    )
    checks.append(
        (
            "V1040_7_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1040_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1040 nonclaim rows",
        )
    )
    checks.append(
        (
            "V1040_9_claim_gates_blocked",
            all(row["gate_pass"] == "false" and not flag(row["claim_allowed"]) for row in claim_rows),
            "all empirical/local-GR claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1040_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1040_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
        OUT / "P8_Y5_R10_1040_BX_OWNER_GATE.csv",
        OUT / "P8_Y5_R10_1040_REFERENCE_PROJECTOR_SPLIT.csv",
        OUT / "P8_Y5_R10_1040_KBOUNDARY_COCYCLE_CONTRACT.csv",
        OUT / "P8_Y5_R10_1040_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
        OUT / "P8_Y5_R10_1040_R10_EDGE_INPUT_CONTRACT.csv",
        OUT / "P8_Y5_R10_1040_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1040_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1040_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1040_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1040_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1040_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1040_11_generated_files_in_post_checkpoint",
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
            "V1040_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1040_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1040 parent boundary charge formula or alpha3 projection bound validation summary",
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
    formula_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    split_rows: list[dict[str, str]],
    cocycle_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1040 Y5 R10 parent boundary charge formula B_X or alpha3 projection bound",
        "",
        "**Progress:** the source-boundary charge is no longer a foggy missing coupling. The current best contract is `Q_X[epsilon]=int_partialSigma epsilon_nu B_X^nu dS`, with `B_X^nu = sigma n_mu P_X^{mu nu} + B_ct^nu + B_ref^nu + B_exact^nu`.",
        "",
        "**Claim ceiling:** this is a formula contract, not a pass. The parent `L_X`, `Theta_X`, `P_X`, tensor/density convention, reference subtraction, source boundary class, and projector split are still not signed.",
        "",
        "**Bound route:** the alpha3 fallback is now an exact inequality: `|K_boundary_alpha3 Phi_boundary_local| <= 4e-20`. That is ready to score only after `K_boundary_alpha3` and `Phi_boundary_local` are theorem-zero or source-backed.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Parent boundary charge formula",
        md_table(formula_rows, ["formula_id", "object", "formula", "derivation_status", "owner_status", "claim_effect", "valid_for_claim"]),
        "## B_X owner gate",
        md_table(owner_rows, ["gate_id", "needed_object", "closure_test", "current_status", "if_missing", "valid_for_claim"]),
        "## Reference/projector split",
        md_table(split_rows, ["split_id", "sector", "rule", "missing", "claim_status", "valid_for_claim"]),
        "## K_boundary cocycle contract",
        md_table(cocycle_rows, ["cocycle_id", "object", "formula", "needed_inputs", "current_status", "valid_for_claim"]),
        "## Alpha3 projection coefficient template",
        md_table(alpha3_rows, ["projection_id", "observable", "mts_formula", "external_bound", "reference", "coefficient_bound_rule", "current_status", "score_ready", "valid_for_claim"]),
        "## R10 edge input contract",
        md_table(edge_rows, ["edge_id", "symbol", "formula", "missing_inputs", "score_ready", "valid_for_claim"]),
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
    formula_rows = bx_formula_rows()
    owner_rows = bx_owner_gate_rows()
    split_rows = reference_projector_rows()
    cocycle_rows = kboundary_cocycle_rows()
    alpha3_rows = alpha3_projection_rows(local_bounds_index())
    edge_rows = r10_edge_contract_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(formula_rows, owner_rows, alpha3_rows, edge_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        formula_rows,
        owner_rows,
        split_rows,
        cocycle_rows,
        alpha3_rows,
        edge_rows,
        mts_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1040_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv", formula_rows)
    write_csv(OUT / "P8_Y5_R10_1040_BX_OWNER_GATE.csv", owner_rows)
    write_csv(OUT / "P8_Y5_R10_1040_REFERENCE_PROJECTOR_SPLIT.csv", split_rows)
    write_csv(OUT / "P8_Y5_R10_1040_KBOUNDARY_COCYCLE_CONTRACT.csv", cocycle_rows)
    write_csv(OUT / "P8_Y5_R10_1040_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv", alpha3_rows)
    write_csv(OUT / "P8_Y5_R10_1040_R10_EDGE_INPUT_CONTRACT.csv", edge_rows)
    write_csv(OUT / "P8_Y5_R10_1040_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1040_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1040_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1040_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1040_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1040_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        formula_rows,
        owner_rows,
        split_rows,
        cocycle_rows,
        alpha3_rows,
        edge_rows,
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
        raise SystemExit(f"1040 validation failed: {failed}")


if __name__ == "__main__":
    main()
