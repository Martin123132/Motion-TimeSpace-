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
DOC = ROOT / "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1042-R10-positive-X-nohair-alpha3-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1042_POSITIVE_NOHAIR_TEMPLATE_NONCLAIM.csv"
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
            "SRC1042_0_1041_next",
            "source-intake/mts_residuals/P8_Y5_R10_1041_NEXT_TARGET.csv",
            "1042-Y5-R10-sourcefree-positive-X-nohair-identity",
            "1041 handoff to source-free positive X no-hair identity or alpha3 prior.",
        ),
        (
            "SRC1042_1_1041_noflux",
            "source-intake/mts_residuals/P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv",
            "NFR1041_0_positive_energy",
            "1041 positive energy/no-flux route.",
        ),
        (
            "SRC1042_2_1041_priors",
            "source-intake/mts_residuals/P8_Y5_R10_1041_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
            "BCP1041_1_Phi_boundary_local",
            "1041 boundary coefficient prior template.",
        ),
        (
            "SRC1042_3_energy_identity",
            "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "E506_vector_tensor_positive_operator",
            "Existing positive operator/no-hair identity templates.",
        ),
        (
            "SRC1042_4_579_contract",
            "source-intake/mts_residuals/P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
            "PXC579_4_hidden_source_silence",
            "Explicit parent X block contract with hidden source and boundary clauses.",
        ),
        (
            "SRC1042_5_580_candidate",
            "source-intake/mts_residuals/P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv",
            "PB580_2_positive_sourcefree_massive_X",
            "Positive source-free massive X candidate branch.",
        ),
        (
            "SRC1042_6_action_terms",
            "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "A7_bulk_X_nohair_or_curve",
            "Parent action term contract for bulk X no-hair or curve.",
        ),
        (
            "SRC1042_7_min_parent",
            "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "A511_3_extra_field_silence",
            "Minimal parent local-GR action blocks.",
        ),
        (
            "SRC1042_8_Theta_template",
            "source-intake/mts_residuals/P8_Y5_R10_1041_THETAX_PX_TEMPLATE_CONTRACT.csv",
            "TPX1041_4_positive_scalar_example",
            "1041 Theta_X/P_X positive scalar-like template.",
        ),
        (
            "SRC1042_9_candidate_classifier",
            "source-intake/mts_residuals/P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv",
            "XC1041_2_positive_sourcefree_physical_X",
            "1041 parent X candidate classifier.",
        ),
        (
            "SRC1042_10_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R7_alpha3",
            "Local bound ledger with alpha3 anchor.",
        ),
        (
            "SRC1042_11_R10_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 nonclaim R10 bound review candidate.",
        ),
        (
            "SRC1042_12_R10_runner",
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


def nohair_identity_rows() -> list[dict[str, str]]:
    return [
        {
            "identity_id": "NH1042_0_operator_setup",
            "statement": "Let X be a retained local extra mode on compact exterior A with equation L_X X = J_X.",
            "formula": "L_X = -nabla_mu(Z_X^{mu nu} nabla_nu .) + M_X^2 + nonnegative mixing, with self-adjoint boundary class",
            "status": "FORMAL_SETUP_NOT_PARENT_SELECTED",
            "claim_effect": "sets the positive operator theorem target",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "identity_id": "NH1042_1_energy_identity",
            "statement": "Multiplying by X and integrating gives the no-hair energy identity.",
            "formula": "int_A [Z_X^{mu nu} nabla_mu X nabla_nu X + M_X^2 X^2 + positive_mix] dV = int_A X J_X dV + Phi_boundary_local",
            "status": "CONDITIONAL_MATH_DERIVED",
            "claim_effect": "if right-hand side is zero and left-hand side positive, X must vanish",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "identity_id": "NH1042_2_positive_zero_theorem",
            "statement": "If Z_X is positive, M_X^2 has a positive gap, J_X=0, Phi_boundary_local=0, and no topological/gauge zero mode remains, then X=0 on A.",
            "formula": "Z_X>=Z_min>0, M_X^2>=m_min^2>0, J_X=0, Phi_boundary=0 => norm[X]^2=0 => X=0",
            "status": "THEOREM_CONDITIONAL_ON_UNSIGNED_PREMISES",
            "claim_effect": "would close physical positive-X local hair without needing an R10 fit",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "identity_id": "NH1042_3_local_GR_effect_if_closed",
            "statement": "If NH1042_2 is parent-signed channelwise, the local compact exterior has no active finite X profile.",
            "formula": "X=0 implies no bulk X exchange from the compact source-free branch; residual rows only survive outside the theorem domain",
            "status": "CONDITIONAL_EFFECT_ONLY",
            "claim_effect": "can support local-GR reduction only after source, boundary, topology, and matter readout clauses close",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "identity_id": "NH1042_4_failure_branch",
            "statement": "If any premise fails, the branch becomes a finite-range residual problem.",
            "formula": "alpha_X(lambda_X)=K_X(lambda_X) Qbar_XH(lambda_X) qbar_XT(lambda_X) plus absolute boundary/source tails",
            "status": "RESIDUAL_BRANCH_RETAINED",
            "claim_effect": "R10/alpha3/PPN/WEP/clock/Gdot rows stay live and nonclaim until sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "identity_id": "NH1042_5_verdict",
            "statement": "The no-hair identity is derived as mathematics, but not claimed for MTS because its four owner premises remain unsigned.",
            "formula": "need parent L_X plus Z_X>0, M_X^2>0, J_X=0, Phi_boundary=0/topology gates",
            "status": "CONDITIONAL_THEOREM_DERIVED_FULL_CLAIM_BLOCKED",
            "claim_effect": "move to premise gates and alpha3 prior first-fill",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def premise_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "NHP1042_0_LX_owner",
            "premise": "parent L_X is selected",
            "required_test": "explicit parent X action with field normalization and boundary class",
            "current_status": "MISSING_PARENT_LX",
            "if_missing": "energy identity remains a template",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NHP1042_1_Z_positive",
            "premise": "Z_X positive kinetic operator",
            "required_test": "second variation gives Z_X>=Z_min>0 in the local branch with gauge/topology handled",
            "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "if_missing": "ghost/anti-elliptic or sign-indefinite mode can evade no-hair",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NHP1042_2_mass_gap",
            "premise": "M_X^2 positive local gap",
            "required_test": "Hessian gives M_X^2>=m_min^2>0 with units and no flat zero mode",
            "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "if_missing": "massless/topological/long-range X mode can remain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NHP1042_3_source_zero",
            "premise": "J_X=0 channelwise",
            "required_test": "ordinary matter, constants, boundary, projector, domain, and memory sources vanish by parent identity",
            "current_status": "SOURCE_ZERO_NOT_DERIVED",
            "if_missing": "positive field is sourced and becomes empirical alpha(lambda)",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NHP1042_4_boundary_flux_zero",
            "premise": "Phi_boundary_local=0",
            "required_test": "boundary flux, source worldtube, reference subtraction, and topology/corner terms vanish or are bounded",
            "current_status": "BOUNDARY_FLUX_ZERO_NOT_DERIVED",
            "if_missing": "alpha3/R10 boundary coefficient rows remain active",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NHP1042_5_no_zero_mode",
            "premise": "no topological/gauge zero mode outside proper quotient",
            "required_test": "kernel of L_X is quotient/proper or fixed by boundary/reference data",
            "current_status": "TOPOLOGY_KERNEL_GATE_OPEN",
            "if_missing": "positive norm may kill only nonzero modes, leaving topological hair",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "NHP1042_6_verdict",
            "premise": "claim-grade source-free positive no-hair",
            "required_test": "NHP1042_0 through NHP1042_5 all pass together",
            "current_status": "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED",
            "if_missing": "keep theorem as conditional and retain nonclaim priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "source_id": "SZ1042_0_matter_pullback",
            "channel": "ordinary matter and constants",
            "zero_condition": "partial_X hat_g=0 and partial_X ordinary constants/material labels=0 before readout",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "residual_if_open": "qbar_XT; WEP; clock; R10 test charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_id": "SZ1042_1_boundary_source",
            "channel": "boundary/source worldtube",
            "zero_condition": "Q_edge, B_X, and source boundary flux vanish or are orthogonal to Pi_M",
            "current_status": "BOUNDARY_OWNER_OPEN",
            "residual_if_open": "Qbar_edge_XH(lambda); Phi_boundary_local; alpha3",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_id": "SZ1042_2_projector_domain",
            "channel": "projector/domain selector",
            "zero_condition": "projector/domain sector is topological, first-class, or positive source-free with zero stress/flux",
            "current_status": "PROJECTOR_DOMAIN_SOURCE_OPEN",
            "residual_if_open": "preferred-frame PPN; alpha3; R10 domain tail",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_id": "SZ1042_3_memory_kernel",
            "channel": "memory/history kernel",
            "zero_condition": "compact-local memory kernel is silent, screened, or constant universal calibration",
            "current_status": "MEMORY_SOURCE_OPEN",
            "residual_if_open": "Gdot; alpha3; R10 memory tail",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_id": "SZ1042_4_source_normalization",
            "channel": "measured source mass and calibration",
            "zero_condition": "Pi_M^H source measure is orthogonal to X hair and measured GM uses same charge",
            "current_status": "SOURCE_MEASURE_OPEN",
            "residual_if_open": "Qbar_XH; M_H_ref; PPN source normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "source_id": "SZ1042_5_verdict",
            "channel": "J_X=0 total",
            "zero_condition": "all channels SZ1042_0 through SZ1042_4 vanish by one parent identity or are bounded absolutely",
            "current_status": "FAIL_CURRENT_CLAIM_JX_ZERO_NOT_SIGNED",
            "residual_if_open": "finite positive-X branch remains empirical/nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def boundary_flux_prior_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    alpha3 = bounds.get("R7_alpha3", {})
    return [
        {
            "prior_id": "PBF1042_0_Phi_boundary_local_definition",
            "coefficient": "Phi_boundary_local",
            "definition": "surface flux term in the positive-X energy identity",
            "formula": "Phi_boundary_local = int_partialA X Z_X n^mu nabla_mu X dS plus any declared finite-jet/counterterm/reference contributions",
            "observable_links": "alpha3;R10;Gdot;PPN preferred-frame",
            "bound_rule": "theorem-zero if Phi_boundary_local=0; otherwise combine with K_boundary_alpha3 through |K_boundary_alpha3 Phi_boundary_local| <= 4e-20",
            "external_anchor": alpha3.get("reference_path_or_url", "MISSING_ALPHA3_SOURCE"),
            "anchor_bound": alpha3.get("upper_bound", "MISSING_ALPHA3_BOUND"),
            "current_status": "FIRST_PRIOR_ROW_FILLED_VALUE_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "PBF1042_1_theorem_zero_route",
            "coefficient": "Phi_boundary_local",
            "definition": "zero-flux theorem route",
            "formula": "Phi_boundary_local=0 if X=0 on boundary, n.grad X=0 by regularity, or exact/topological boundary flux cancels with fixed reference without deleting GR charges",
            "observable_links": "alpha3;R10;Gdot",
            "bound_rule": "requires parent boundary class, no corner/harmonic leak, and source worldtube separation",
            "external_anchor": "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "anchor_bound": "theorem-zero only",
            "current_status": "THEOREM_ZERO_NOT_SIGNED",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "PBF1042_2_numeric_prior_route",
            "coefficient": "Phi_boundary_local",
            "definition": "numeric diagnostic prior route",
            "formula": "if Phi_boundary_local has numeric value Phi, then |K_boundary_alpha3| <= 4e-20/|Phi| for nonzero Phi",
            "observable_links": "alpha3",
            "bound_rule": "requires Phi units, normalization, source path, uncertainty, and no-cancellation policy",
            "external_anchor": alpha3.get("reference_path_or_url", "MISSING_ALPHA3_SOURCE"),
            "anchor_bound": alpha3.get("upper_bound", "MISSING_ALPHA3_BOUND"),
            "current_status": "NUMERIC_VALUE_NOT_AVAILABLE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def alpha3_prior_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    alpha3 = bounds.get("R7_alpha3", {})
    return [
        {
            "alpha3_id": "A3F1042_0_first_fill",
            "observable": "alpha3",
            "mts_formula": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "external_bound": alpha3.get("upper_bound", "MISSING_ALPHA3_BOUND"),
            "units": alpha3.get("units", "dimensionless"),
            "reference": alpha3.get("reference_path_or_url", "MISSING_ALPHA3_SOURCE"),
            "filled_component": "Phi_boundary_local definition and theorem-zero/numeric route",
            "missing_component": "K_boundary_alpha3; numeric Phi_boundary_local or theorem-zero proof",
            "claim_status": "NONCLAIM_FIRST_FILL",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def r10_impact_rows() -> list[dict[str, str]]:
    return [
        {
            "impact_id": "R10I1042_0_if_nohair_closes",
            "branch": "source-free positive no-hair closes",
            "effect": "X=0 in the compact local exterior; no bulk finite-X profile contributes to local fifth-force scoring",
            "remaining_caveat": "must still prove matter/readout/source-normalization and boundary/source-worldtube scopes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "impact_id": "R10I1042_1_if_source_open",
            "branch": "J_X or qbar_XT open",
            "effect": "positive physical X is sourced; R10 alpha(lambda) and WEP/clock/PPN residual rows stay live",
            "remaining_caveat": "requires K_X, Qbar_XH, qbar_XT, lambda_X, and promoted bound curve",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "impact_id": "R10I1042_2_if_boundary_open",
            "branch": "Phi_boundary_local open",
            "effect": "boundary alpha3 and R10 edge residuals stay live with absolute no-cancellation addition",
            "remaining_caveat": "requires K_boundary_alpha3 or edge K/Qbar/qbar rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "positive_X_nohair_conditional",
            "curve_id": "MTS_1042_POSITIVE_X_NOHAIR_CONDITIONAL",
            "lambda_value": "MISSING_ZX_MX_RATIO",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_PARENT_SIGNED_Z_M_J_PHI_PREMISES",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "if Z_X>0, M_X^2>0, J_X=0, Phi_boundary=0, no zero modes, then X=0",
            "derivation_status": "template_invalid_nohair_premises_unsigned",
            "formula_reference": "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md::NH1042_2",
            "source_file": "MISSING_PARENT_LX_SOURCE_FILE",
            "assumptions": "conditional theorem only",
            "valid_for_claim": "false",
            "notes": "Mathematical route is clean, MTS ownership is open.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "alpha3_phi_boundary_first_fill",
            "curve_id": "MTS_1042_ALPHA3_PHI_PRIOR",
            "lambda_value": "MISSING_NOT_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL",
            "alpha_bound": "4e-20",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R7_alpha3",
            "force_law_form": "alpha3_MTS=K_boundary_alpha3 Phi_boundary_local; |K Phi| <= 4e-20",
            "derivation_status": "template_invalid_phi_prior_value_missing",
            "formula_reference": "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md::PBF1042_0",
            "source_file": "MISSING_PHI_BOUNDARY_SOURCE_FILE",
            "assumptions": "private nonclaim first-fill row",
            "valid_for_claim": "false",
            "notes": "Alpha3 prior scaffold only.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "finite_X_residual_if_nohair_fails",
            "curve_id": "MTS_1042_FINITE_X_RESIDUAL",
            "lambda_value": "MISSING_PARENT_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KX_QBAR_XH_QBAR_XT_PLUS_TAILS",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "alpha_X(lambda)=K_X Qbar_XH qbar_XT plus absolute boundary/source tails",
            "derivation_status": "template_invalid_residual_inputs_missing",
            "formula_reference": "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md::NH1042_4",
            "source_file": "MISSING_RESIDUAL_SOURCE_FILE",
            "assumptions": "no cancellation between channels",
            "valid_for_claim": "false",
            "notes": "Fallback branch if nohair premises fail.",
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1042_0_runner_status",
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
    identity_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
    phi_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in identity_rows:
        rows.append(
            {
                "refusal_id": f"REF1042_{row['identity_id']}",
                "object": row["statement"],
                "current_status": row["status"],
                "refusal_status": "nohair_theorem_not_claim_promoted",
                "failure_reasons": row["claim_effect"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in premise_rows:
        rows.append(
            {
                "refusal_id": f"REF1042_{row['gate_id']}",
                "object": row["premise"],
                "current_status": row["current_status"],
                "refusal_status": "nohair_premise_gate_failed",
                "failure_reasons": row["if_missing"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in source_rows:
        rows.append(
            {
                "refusal_id": f"REF1042_{row['source_id']}",
                "object": row["channel"],
                "current_status": row["current_status"],
                "refusal_status": "source_zero_not_claim_promoted",
                "failure_reasons": row["residual_if_open"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in phi_rows:
        rows.append(
            {
                "refusal_id": f"REF1042_{row['prior_id']}",
                "object": row["coefficient"],
                "current_status": row["current_status"],
                "refusal_status": "phi_boundary_prior_not_scoreable",
                "failure_reasons": row["bound_rule"],
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
            "gate_id": "CGATE1042_0_nohair",
            "claim": "source-free positive X no-hair closes local branch",
            "gate_pass": "false",
            "reason": "identity is derived conditionally, but L_X, Z_X, M_X^2, J_X, Phi_boundary, and topology gates are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1042_1_local_GR",
            "claim": "local GR/no finite X profile follows",
            "gate_pass": "false",
            "reason": "nohair premises and matter/source readout clauses remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1042_2_alpha3_prior",
            "claim": "Phi_boundary alpha3 prior is score-ready",
            "gate_pass": "false",
            "reason": "Phi_boundary_local is defined, but theorem-zero or numeric source value is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1042_3_R10",
            "claim": "R10 alpha(lambda) is score-ready",
            "gate_pass": "false",
            "reason": "K_X, Qbar_XH, qbar_XT, lambda_X, and promoted bound curve remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1042_0_theorem_status",
            "decision": "The positive/source-free no-hair theorem is mathematically clean but only conditional.",
            "because": "multiplying by X gives a positive norm identity, but MTS has not parent-signed Z_X, M_X^2, J_X, Phi_boundary, or topology gates.",
            "next_action": "try to prove the missing source-zero and boundary-flux-zero premises one level upstream",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1042_1_prior_status",
            "decision": "The first alpha3 prior fill should target Phi_boundary_local.",
            "because": "Phi_boundary is both the no-hair obstruction and the alpha3/R10 boundary residual amplitude.",
            "next_action": "derive Phi_boundary_local=0 from boundary class/no-flux, or source a numeric diagnostic value",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1042_2_next_target",
            "decision": "Next target should attack source-zero and boundary-flux-zero separately.",
            "because": "operator positivity is useless for local GR unless the right-hand side of the energy identity vanishes.",
            "next_action": "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
            "objective": "try to prove J_X=0 and Phi_boundary_local=0 channelwise for ordinary matter, boundary, projector, domain, and memory sectors; if this fails, build a nonclaim alpha3 prior value/template for Phi_boundary_local",
            "include": "source-zero Ward clauses, matter pullback, boundary flux no-hair, projector/domain topological silence, memory silence, alpha3 Phi prior schema",
            "exclude": "invented J/Phi/K values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    source_zero_rows_: list[dict[str, str]],
    phi_rows: list[dict[str, str]],
    alpha3_rows_: list[dict[str, str]],
    r10_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1042_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1042 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1042_1_nohair_identity_derived_conditional",
            any(row["identity_id"] == "NH1042_1_energy_identity" and row["status"] == "CONDITIONAL_MATH_DERIVED" for row in identity_rows)
            and any(row["identity_id"] == "NH1042_5_verdict" and row["status"] == "CONDITIONAL_THEOREM_DERIVED_FULL_CLAIM_BLOCKED" for row in identity_rows),
            "positive-X no-hair identity is derived conditionally and blocked for claim",
        )
    )
    checks.append(
        (
            "V1042_2_premise_gates_block_claim",
            len(premise_rows) >= 7
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_NOHAIR_NOT_PARENT_SIGNED" for row in premise_rows)
            and all(not flag(row["valid_for_claim"]) for row in premise_rows),
            "nohair premise gates identify missing L_X, Z, M, J, Phi, and topology clauses",
        )
    )
    checks.append(
        (
            "V1042_3_source_zero_channels",
            {"ordinary matter and constants", "boundary/source worldtube", "projector/domain selector", "memory/history kernel", "measured source mass and calibration"}.issubset(
                {row["channel"] for row in source_zero_rows_}
            )
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_JX_ZERO_NOT_SIGNED" for row in source_zero_rows_),
            "source-zero audit covers the main hidden source channels",
        )
    )
    checks.append(
        (
            "V1042_4_phi_boundary_first_fill",
            any(
                row["prior_id"] == "PBF1042_0_Phi_boundary_local_definition"
                and row["anchor_bound"] == "4e-20"
                and row["score_ready"] == "false"
                for row in phi_rows
            ),
            "Phi_boundary_local first prior row is filled with alpha3 anchor but remains nonclaim",
        )
    )
    checks.append(
        (
            "V1042_5_alpha3_first_fill_nonclaim",
            bool(alpha3_rows_)
            and alpha3_rows_[0]["claim_status"] == "NONCLAIM_FIRST_FILL"
            and alpha3_rows_[0]["external_bound"] == "4e-20",
            "alpha3 first-fill ledger is nonclaim and source-anchored",
        )
    )
    checks.append(
        (
            "V1042_6_R10_impact_retained",
            len(r10_rows) >= 3 and all(not flag(row["valid_for_claim"]) for row in r10_rows),
            "R10/local residual impacts remain nonclaim",
        )
    )
    checks.append(
        (
            "V1042_7_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1042_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1042 nonclaim rows",
        )
    )
    checks.append(
        (
            "V1042_9_claim_gates_blocked",
            all(row["gate_pass"] == "false" and not flag(row["claim_allowed"]) for row in claim_rows),
            "all local-GR/empirical claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1042_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1042_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
        OUT / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
        OUT / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv",
        OUT / "P8_Y5_R10_1042_BOUNDARY_FLUX_PRIOR_FIRST_FILL.csv",
        OUT / "P8_Y5_R10_1042_ALPHA3_PRIOR_FIRST_FILL.csv",
        OUT / "P8_Y5_R10_1042_R10_RESIDUAL_IMPACT.csv",
        OUT / "P8_Y5_R10_1042_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1042_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1042_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1042_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1042_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1042_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1042_11_generated_files_in_post_checkpoint",
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
            "V1042_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1042_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1042 source-free positive X no-hair or alpha3 prior first-fill validation summary",
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
    identity_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    source_zero_rows_: list[dict[str, str]],
    phi_rows: list[dict[str, str]],
    alpha3_rows_: list[dict[str, str]],
    r10_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1042 Y5 R10 source-free positive X no-hair identity or alpha3 prior first fill",
        "",
        "**Progress:** the positive/source-free no-hair theorem is now written cleanly. If `Z_X>0`, `M_X^2>0`, `J_X=0`, `Phi_boundary_local=0`, and no topological/gauge zero mode remains, then the local compact exterior forces `X=0`.",
        "",
        "**Claim ceiling:** the theorem is conditional. MTS has not yet parent-signed `L_X`, the positive Hessian, source-zero, boundary-flux-zero, or topology/kernel gates.",
        "",
        "**Fallback fill:** the first alpha3 prior row now defines `Phi_boundary_local` as the boundary flux in the positive-X identity and links it to `|K_boundary_alpha3 Phi_boundary_local| <= 4e-20`, but it remains nonclaim.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Positive X no-hair identity",
        md_table(identity_rows, ["identity_id", "statement", "formula", "status", "claim_effect", "valid_for_claim"]),
        "## No-hair premise gate",
        md_table(premise_rows, ["gate_id", "premise", "required_test", "current_status", "if_missing", "valid_for_claim"]),
        "## Source-zero clause audit",
        md_table(source_zero_rows_, ["source_id", "channel", "zero_condition", "current_status", "residual_if_open", "valid_for_claim"]),
        "## Boundary flux prior first fill",
        md_table(phi_rows, ["prior_id", "coefficient", "definition", "formula", "observable_links", "bound_rule", "anchor_bound", "current_status", "score_ready", "valid_for_claim"]),
        "## Alpha3 prior first fill",
        md_table(alpha3_rows_, ["alpha3_id", "observable", "mts_formula", "external_bound", "reference", "filled_component", "missing_component", "claim_status", "score_ready", "valid_for_claim"]),
        "## R10 residual impact",
        md_table(r10_rows, ["impact_id", "branch", "effect", "remaining_caveat", "valid_for_claim"]),
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
    identity_rows = nohair_identity_rows()
    premise_rows = premise_gate_rows()
    source_zero_rows_ = source_zero_rows()
    bounds = local_bounds_index()
    phi_rows = boundary_flux_prior_rows(bounds)
    alpha3_rows_ = alpha3_prior_rows(bounds)
    r10_rows = r10_impact_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(identity_rows, premise_rows, source_zero_rows_, phi_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        identity_rows,
        premise_rows,
        source_zero_rows_,
        phi_rows,
        alpha3_rows_,
        r10_rows,
        mts_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1042_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv", identity_rows)
    write_csv(OUT / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv", premise_rows)
    write_csv(OUT / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv", source_zero_rows_)
    write_csv(OUT / "P8_Y5_R10_1042_BOUNDARY_FLUX_PRIOR_FIRST_FILL.csv", phi_rows)
    write_csv(OUT / "P8_Y5_R10_1042_ALPHA3_PRIOR_FIRST_FILL.csv", alpha3_rows_)
    write_csv(OUT / "P8_Y5_R10_1042_R10_RESIDUAL_IMPACT.csv", r10_rows)
    write_csv(OUT / "P8_Y5_R10_1042_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1042_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1042_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1042_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1042_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1042_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        identity_rows,
        premise_rows,
        source_zero_rows_,
        phi_rows,
        alpha3_rows_,
        r10_rows,
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
        raise SystemExit(f"1042 validation failed: {failed}")


if __name__ == "__main__":
    main()
