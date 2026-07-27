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
DOC = ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1041-R10-ThetaX-PX-prior-nonclaim-smoke" / "results"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1041_THETAX_PX_TEMPLATE_NONCLAIM.csv"
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
            "SRC1041_0_1040_next",
            "source-intake/mts_residuals/P8_Y5_R10_1040_NEXT_TARGET.csv",
            "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
            "1040 handoff to parent X-sector Theta_X/P_X owner or coefficient prior.",
        ),
        (
            "SRC1041_1_1040_BX_formula",
            "source-intake/mts_residuals/P8_Y5_R10_1040_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
            "BX1040_1_candidate_charge_density",
            "1040 B_X/Q_X formula contract.",
        ),
        (
            "SRC1041_2_1040_alpha3",
            "source-intake/mts_residuals/P8_Y5_R10_1040_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
            "A3P1040_0_formula",
            "1040 alpha3 coefficient inequality.",
        ),
        (
            "SRC1041_3_579_contract",
            "source-intake/mts_residuals/P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv",
            "PXC579_4_hidden_source_silence",
            "579 explicit parent X block contract.",
        ),
        (
            "SRC1041_4_580_candidates",
            "source-intake/mts_residuals/P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv",
            "PB580_1_quotient_vertical_constraint",
            "580 parent block candidate ranking.",
        ),
        (
            "SRC1041_5_action_terms",
            "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "A7_bulk_X_nohair_or_curve",
            "Parent action terms and residual routes.",
        ),
        (
            "SRC1041_6_min_action",
            "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "A511_3_extra_field_silence",
            "Minimal local-GR parent action block list.",
        ),
        (
            "SRC1041_7_667_fallback",
            "source-intake/mts_residuals/P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv",
            "RF667_0_LX_theta_Qtau_owner",
            "667 residual fallback row for L_X/Theta_X/Q_X.",
        ),
        (
            "SRC1041_8_extra_energy",
            "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "E506_vector_tensor_positive_operator",
            "Positive operator/no-hair identity candidates.",
        ),
        (
            "SRC1041_9_668_owner",
            "source-intake/mts_residuals/P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv",
            "SO668_2_MTS_extra_LX",
            "668 sector owner audit.",
        ),
        (
            "SRC1041_10_local_bounds",
            "source-intake/local_bounds/local_bound_claims.csv",
            "R7_alpha3",
            "Local bound ledger with alpha3 anchor.",
        ),
        (
            "SRC1041_11_R10_candidate",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "R10_VECTOR_2020_REVIEW_0000",
            "1034 nonclaim R10 bound review candidate.",
        ),
        (
            "SRC1041_12_R10_runner",
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


def candidate_classifier_rows() -> list[dict[str, str]]:
    return [
        {
            "candidate_id": "XC1041_0_absent_quotient",
            "parent_route": "X is not a primitive parent field",
            "ThetaX_PX_result": "Theta_X=0 and P_X=0 because there is no independent X variation",
            "boundary_result": "B_X=0 if the quotient/nonprimitive claim is parent-proved",
            "risk": "must prove X is a coordinate/readout artefact before variation, not a post-hoc deletion",
            "rank": "1",
            "current_status": "BEST_THEOREM_ROUTE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "candidate_id": "XC1041_1_first_class_vertical_constraint",
            "parent_route": "X is a first-class vertical gauge/constraint direction",
            "ThetaX_PX_result": "Theta_X exists on the parent fields and Omega-flat(v_X)=delta C_X; P_X is owned by the momentum-map constraint",
            "boundary_result": "B_X/Q_X vanish only for proper compact transformations unless Q_X exact/proper and K_boundary=0 are proved",
            "risk": "requires parent Omega, D C_X, all-field v_X, bracket closure, degree count, and matter descent",
            "rank": "2",
            "current_status": "BEST_ACTIVE_ROUTE_BUT_INCOMPLETE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "candidate_id": "XC1041_2_positive_sourcefree_physical_X",
            "parent_route": "X is a physical positive operator but source-free in the local branch",
            "ThetaX_PX_result": "for first-derivative quadratic sector, Theta_X^mu=Z_X nabla^mu X delta X plus mixing terms",
            "boundary_result": "B_X and Phi_boundary vanish only if J_X=0 and boundary flux=0/no-hair are parent-proved",
            "risk": "a physical Green function exists; any source/readout leakage becomes a fifth-force residual",
            "rank": "3",
            "current_status": "VIABLE_NOHAIR_ROUTE_INPUTS_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "candidate_id": "XC1041_3_sourced_residual",
            "parent_route": "X is a physical sourced field",
            "ThetaX_PX_result": "Theta_X/P_X are standard once L_X is chosen, but the branch must be empirically scored",
            "boundary_result": "alpha(lambda), alpha3, PPN, WEP, clock, and Gdot coefficient rows become live",
            "risk": "not a local-GR derivation by itself; it is a testable residual framework",
            "rank": "4",
            "current_status": "EMPIRICAL_FALLBACK_ONLY",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "candidate_id": "XC1041_4_universal_conformal",
            "parent_route": "matter sees exp(2 a X) g",
            "ThetaX_PX_result": "standard scalar-field Theta_X if X has a kinetic block",
            "boundary_result": "source/test coupling is at least quadratic in a universal coupling unless source leg is separately declared",
            "risk": "cheap universal coupling does not prove GR; it creates a fifth-force countermodel unless a=0 is derived",
            "rank": "5",
            "current_status": "COUNTERMODEL_NOT_SOLUTION",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def thetax_px_template_rows() -> list[dict[str, str]]:
    return [
        {
            "template_id": "TPX1041_0_general_variation",
            "object": "finite-order parent X sector",
            "formula": "delta L_X = E_A delta Y_X^A + nabla_mu Theta_X^mu(delta Y_X)",
            "owned_if": "L_X is selected with field normalization, derivative order, density convention, and boundary class",
            "current_status": "GENERAL_TEMPLATE_DERIVED_NOT_PARENT_SELECTED",
            "claim_effect": "defines the upstream object needed for Q_X, B_X, K_boundary, and no-hair identities",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "TPX1041_1_first_derivative",
            "object": "first-derivative template",
            "formula": "Theta_X^mu(delta Y)=Pi_A^mu delta Y^A, Pi_A^mu := partial L_X / partial(nabla_mu Y^A)",
            "owned_if": "L_X has no higher derivatives or higher-derivative boundary terms have been reduced by auxiliary fields",
            "current_status": "FORMULA_READY_LX_MISSING",
            "claim_effect": "turns a chosen L_X into a computable symplectic potential",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "TPX1041_2_finite_jet",
            "object": "higher finite-jet template",
            "formula": "Theta_X^mu=sum_{r=0}^{N-1} Pi_A^{mu alpha_1...alpha_r} nabla_{alpha_1}...nabla_{alpha_r} delta Y^A",
            "owned_if": "finite derivative order N and all corner/counterterm conventions are declared",
            "current_status": "FORMULA_READY_FINITE_JET_ORDER_MISSING",
            "claim_effect": "fixes which epsilon_X jets must vanish for proper boundary silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "TPX1041_3_Noether_PX",
            "object": "P_X from vertical generator",
            "formula": "insert delta_epsilon Y^A=R^A_nu epsilon^nu + R^{A mu}_nu nabla_mu epsilon^nu + ... into Theta_X; P_X^{mu nu} is the coefficient package whose divergence enters C_X^nu",
            "owned_if": "v_X action on every parent field and the tensor/density convention for C_X are fixed",
            "current_status": "CONTRACT_READY_FIELD_ACTION_AND_CONVENTION_MISSING",
            "claim_effect": "connects Theta_X to B_X^nu=sigma n_mu P_X^{mu nu}+...",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "TPX1041_4_positive_scalar_example",
            "object": "minimal positive scalar-like residual example",
            "formula": "L_X=-1/2 Z_X nabla_mu X nabla^mu X -1/2 M_X^2 X^2 + J_X X gives Theta_X^mu=-Z_X nabla^mu X delta X",
            "owned_if": "X really is the retained scalar amplitude, Z_X>0, M_X^2>0, J_X and boundary data are source-owned",
            "current_status": "EXAMPLE_ONLY_NOT_SELECTED",
            "claim_effect": "if J_X=0 and boundary flux=0, no-hair can set X=0; otherwise alpha(lambda) is live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "TPX1041_5_verdict",
            "object": "Theta_X/P_X owner status",
            "formula": "Theta_X/P_X template is mathematically ready, but no parent X block is selected or proved",
            "owned_if": "one candidate in XC1041 closes its owner gates",
            "current_status": "FAIL_CURRENT_CLAIM_THETAX_PX_NOT_PARENT_OWNED",
            "claim_effect": "use nonclaim priors/templates for boundary coefficients until a parent block is signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def owner_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "TOG1041_0_parent_route",
            "needed": "select one parent X route",
            "test": "absent quotient, first-class vertical constraint, positive sourcefree field, or sourced residual is chosen before scoring",
            "current_status": "ROUTE_NOT_PARENT_SELECTED",
            "if_missing": "Theta_X/P_X remain a menu rather than an action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TOG1041_1_field_content",
            "needed": "field list and transformation law",
            "test": "Y_X^A and delta_epsilon Y_X^A are declared for metric/coframe, extra modes, domain/memory, matter, and boundary fields",
            "current_status": "FIELD_ACTION_INCOMPLETE",
            "if_missing": "P_X cannot be computed from Theta_X",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TOG1041_2_operator_signs",
            "needed": "positive/no-pole or residual operator",
            "test": "Z_X, M_X^2, Hessian signs, or first-class rank/degree count are derived",
            "current_status": "OPERATOR_SIGNS_MISSING",
            "if_missing": "local-GR reduction cannot tell no-hair from hidden dynamics",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TOG1041_3_source_zero",
            "needed": "source/test blindness",
            "test": "J_X=0, qbar_XT=0, Qbar_XH=0, or bounded coefficient rows are sourced channelwise",
            "current_status": "SOURCE_ZERO_OR_BOUND_MISSING",
            "if_missing": "R10/WEP/clock/PPN/orbital residual rows remain live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TOG1041_4_boundary_flux",
            "needed": "boundary no-flux or coefficient row",
            "test": "Phi_boundary_local=0 theorem or alpha3/R10 boundary coefficients are source-backed",
            "current_status": "BOUNDARY_FLUX_ZERO_OR_BOUND_MISSING",
            "if_missing": "K_boundary_alpha3 and edge R10 templates remain nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "TOG1041_5_verdict",
            "needed": "claim-grade Theta_X/P_X owner",
            "test": "TOG1041_0 through TOG1041_4 pass together",
            "current_status": "FAIL_CURRENT_CLAIM_THETAX_PX_OWNER_MISSING",
            "if_missing": "demote to nonclaim coefficient priors/templates",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def noflux_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "NFR1041_0_positive_energy",
            "route": "positive source-free operator",
            "identity": "int_A <X,L_X X> = positive_norm[X] + Phi_boundary_local",
            "zero_condition": "positive_norm plus Phi_boundary_local=0 plus J_X=0 forces X=0 modulo pure gauge/topological class",
            "missing": "L_X, sign proof, source-zero, boundary flux theorem, allowed topology",
            "current_status": "PROMISING_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "NFR1041_1_topological_exact",
            "route": "topological/exact boundary sector",
            "identity": "L_boundary=dB or class-only topological density with no local metric/source variation",
            "zero_condition": "edge flux is fixed background subtraction or exact on the certified boundary class",
            "missing": "boundary class owner, harmonic/corner control, reference subtraction",
            "current_status": "ROUTE_OPEN_NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "NFR1041_2_first_class_constraint",
            "route": "constraint/gauge no-pole",
            "identity": "Omega_flat(v_X)=delta C_X and Q_X=K_boundary=0 on the relevant local branch",
            "zero_condition": "no physical X Green function exists and no source/test marker sees X",
            "missing": "parent Omega, D C_X, bracket, degree count, matter descent",
            "current_status": "ROUTE_OPEN_NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_prior_rows(bounds: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    alpha3 = bounds.get("R7_alpha3", {})
    return [
        {
            "prior_id": "BCP1041_0_K_boundary_alpha3",
            "coefficient": "K_boundary_alpha3",
            "observable": "alpha3",
            "prior_or_bound_rule": "if Phi_boundary_local is sourced and nonzero, |K_boundary_alpha3| <= 4e-20/|Phi_boundary_local|",
            "external_anchor": alpha3.get("reference_path_or_url", "MISSING_ALPHA3_SOURCE"),
            "anchor_bound": alpha3.get("upper_bound", "MISSING_ALPHA3_BOUND"),
            "required_inputs": "Phi_boundary_local numeric/source-backed or theorem-zero; normalization; uncertainty policy",
            "current_status": "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "BCP1041_1_Phi_boundary_local",
            "coefficient": "Phi_boundary_local",
            "observable": "alpha3;R10;Gdot",
            "prior_or_bound_rule": "Phi_boundary_local=0 by no-flux theorem, or numeric amplitude with units and source path",
            "external_anchor": "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv; local_bound_claims.csv:R7_alpha3",
            "anchor_bound": "theorem-zero or observable-specific bounds",
            "required_inputs": "boundary norm, surface, units, time/source normalization, topology/corner policy",
            "current_status": "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "BCP1041_2_edge_R10_coefficients",
            "coefficient": "K_edge;Qbar_edge_XH;qbar_XT",
            "observable": "alpha_R10(lambda)",
            "prior_or_bound_rule": "|alpha_edge|=|K_edge Qbar_edge_XH qbar_XT| must be <= alpha_bound(lambda) after curve promotion",
            "external_anchor": str(BOUND_CANDIDATE),
            "anchor_bound": "review-candidate alpha_bound(lambda) only",
            "required_inputs": "K_edge(lambda), Qbar_edge_XH(lambda), qbar_XT, lambda support, promoted bound curve",
            "current_status": "NONCLAIM_PRIOR_SCHEMA_READY_INPUTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def action_selection_rows() -> list[dict[str, str]]:
    return [
        {
            "selection_id": "SEL1041_0_do_not_select_yet",
            "decision": "Do not select a public parent X action at 1041.",
            "reason": "the corpus has candidate routes but no source file proving the required L_X/Theta_X/P_X package",
            "safe_use": "use the templates as contracts for the next derivation step",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SEL1041_1_best_derivation_next",
            "decision": "Best next derivation is the positive/nohair or first-class-constraint owner route, not a sourced residual fit.",
            "reason": "those are the only routes that can genuinely reduce to local GR rather than merely survive empirical bounds",
            "safe_use": "try to close source-free energy identity or first-class momentum-map owner before coefficient priors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SEL1041_2_fallback_prior",
            "decision": "If the owner route stalls, use alpha3/R10 coefficient priors as private diagnostic scaffolding.",
            "reason": "the exact inequality is known, but numeric K/Phi values would be invented today",
            "safe_use": "nonclaim rows only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def mts_template_rows() -> list[dict[str, str]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "ThetaX_PX_owner_contract",
            "curve_id": "MTS_1041_THETAX_PX_OWNER_TEMPLATE",
            "lambda_value": "MISSING_PARENT_ROUTE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_PARENT_THETAX_PX_OWNER",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "Theta_X/P_X determine B_X, Q_X, K_boundary, and any edge alpha(lambda)",
            "derivation_status": "template_invalid_parent_route_not_selected",
            "formula_reference": "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md::TPX1041_5",
            "source_file": "MISSING_PARENT_LX_SOURCE_FILE",
            "assumptions": "no parent X action selected",
            "valid_for_claim": "false",
            "notes": "Owner contract only.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "positive_nohair_zero_template",
            "curve_id": "MTS_1041_POSITIVE_NOHAIR_TEMPLATE",
            "lambda_value": "MISSING_ZX_MX_RATIO",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_JX_ZERO_AND_BOUNDARY_FLUX_ZERO",
            "alpha_bound": "MISSING_PROMOTED_R10_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv is review-only",
            "force_law_form": "if Z_X>0, M_X^2>0, J_X=0, Phi_boundary=0, then X=0 by energy identity",
            "derivation_status": "template_invalid_operator_and_source_zero_missing",
            "formula_reference": "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md::NFR1041_0",
            "source_file": "MISSING_POSITIVE_OPERATOR_SOURCE_FILE",
            "assumptions": "no-hair route not parent-signed",
            "valid_for_claim": "false",
            "notes": "Potentially powerful route, no claim.",
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "alpha3_coefficient_prior_template",
            "curve_id": "MTS_1041_ALPHA3_PRIOR_TEMPLATE",
            "lambda_value": "MISSING_NOT_R10_RANGE",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_K_BOUNDARY_ALPHA3_PHI_BOUNDARY_LOCAL",
            "alpha_bound": "4e-20",
            "alpha_bound_source": "source-intake/local_bounds/local_bound_claims.csv:R7_alpha3",
            "force_law_form": "|K_boundary_alpha3 Phi_boundary_local| <= 4e-20",
            "derivation_status": "template_invalid_prior_inputs_missing",
            "formula_reference": "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md::BCP1041_0",
            "source_file": "MISSING_ALPHA3_COEFFICIENT_SOURCE_FILE",
            "assumptions": "private nonclaim prior row",
            "valid_for_claim": "false",
            "notes": "Diagnostic only.",
        },
    ]


def runner_smoke_rows(status: dict[str, object]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1041_0_runner_status",
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
    candidates: list[dict[str, str]],
    templates: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in candidates:
        rows.append(
            {
                "refusal_id": f"REF1041_{row['candidate_id']}",
                "object": row["parent_route"],
                "current_status": row["current_status"],
                "refusal_status": "candidate_not_parent_selected",
                "failure_reasons": row["risk"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in templates:
        rows.append(
            {
                "refusal_id": f"REF1041_{row['template_id']}",
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "ThetaX_PX_template_not_claim_promoted",
                "failure_reasons": row["owned_if"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in owner_rows:
        rows.append(
            {
                "refusal_id": f"REF1041_{row['gate_id']}",
                "object": row["needed"],
                "current_status": row["current_status"],
                "refusal_status": "owner_gate_failed",
                "failure_reasons": row["if_missing"],
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    for row in prior_rows:
        rows.append(
            {
                "refusal_id": f"REF1041_{row['prior_id']}",
                "object": row["coefficient"],
                "current_status": row["current_status"],
                "refusal_status": "coefficient_prior_not_scoreable",
                "failure_reasons": row["required_inputs"],
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
            "gate_id": "CGATE1041_0_parent_X_owner",
            "claim": "parent X-sector action owns Theta_X/P_X",
            "gate_pass": "false",
            "reason": "candidate routes are ranked and templates are written, but no L_X/field-content/operator/source/boundary package is parent-selected",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1041_1_local_GR_reduction",
            "claim": "local GR/no-pole branch follows from the X sector",
            "gate_pass": "false",
            "reason": "absent-quotient/first-class/no-hair routes remain unsigned; sourced residual route is not a derivation of GR",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1041_2_alpha3_prior",
            "claim": "alpha3 coefficient prior is executable",
            "gate_pass": "false",
            "reason": "K_boundary_alpha3 and Phi_boundary_local remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE1041_3_R10",
            "claim": "R10 edge/bulk alpha(lambda) is score-ready",
            "gate_pass": "false",
            "reason": "K_edge/K_X, Qbar, qbar, lambda support, and promoted bound curve remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1041_0_parent_route_status",
            "decision": "Do not pretend a parent X action is selected yet.",
            "because": "1041 derives the generic Theta_X/P_X machinery but does not find a source file proving any candidate route.",
            "next_action": "attack the positive/nohair source-zero route or first-class momentum-map route directly",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1041_1_best_route",
            "decision": "Best derivation route remains absent/quotient or first-class constraint; best fallback route is positive source-free no-hair.",
            "because": "these can actually reduce to local GR, while sourced residuals only build a testable fifth-force branch.",
            "next_action": "derive the source-free positive operator identity with J_X=0 and Phi_boundary=0, or close the first-class constraints",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1041_2_next_target",
            "decision": "Next target should test the source-free positive operator/no-hair route.",
            "because": "it is the most concrete route that can convert Theta_X/P_X templates into a real local-GR reduction without inventing coefficients.",
            "next_action": "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
            "objective": "try to derive the source-free positive X-sector no-hair identity with Z_X>0, M_X^2>0, J_X=0, and Phi_boundary=0; if it fails, build the first nonclaim alpha3 prior row for K_boundary_alpha3 or Phi_boundary_local",
            "include": "positive operator identity, source-zero clauses, boundary flux zero, topology/gauge caveats, Hessian sign gates, alpha3 prior schema",
            "exclude": "invented Z/M/J/K/Phi values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate(
    source_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    noflux_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    selection_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "V1041_0_sources_exist",
            all(flag(row["exists"]) and flag(row["needle_found"]) for row in source_rows),
            "all 1041 source paths exist and expected needles are present",
        )
    )
    checks.append(
        (
            "V1041_1_candidates_ranked",
            len(candidate_rows) >= 5
            and candidate_rows[0]["candidate_id"] == "XC1041_0_absent_quotient"
            and any(row["current_status"] == "BEST_ACTIVE_ROUTE_BUT_INCOMPLETE" for row in candidate_rows),
            "parent X candidate routes are ranked without selection",
        )
    )
    checks.append(
        (
            "V1041_2_ThetaX_PX_templates",
            any(row["template_id"] == "TPX1041_1_first_derivative" and "Theta_X^mu" in row["formula"] for row in template_rows)
            and any(row["template_id"] == "TPX1041_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_THETAX_PX_NOT_PARENT_OWNED" for row in template_rows),
            "Theta_X/P_X templates are written and not parent-promoted",
        )
    )
    checks.append(
        (
            "V1041_3_owner_gates_fail_safely",
            len(owner_rows) >= 6
            and any(row["current_status"] == "FAIL_CURRENT_CLAIM_THETAX_PX_OWNER_MISSING" for row in owner_rows)
            and all(not flag(row["valid_for_claim"]) for row in owner_rows),
            "owner gates identify missing route, field action, signs, source-zero, and boundary flux",
        )
    )
    checks.append(
        (
            "V1041_4_nohair_routes_staged",
            {"positive source-free operator", "topological/exact boundary sector", "constraint/gauge no-pole"}.issubset(
                {row["route"] for row in noflux_rows}
            )
            and all(not flag(row["valid_for_claim"]) for row in noflux_rows),
            "no-hair and constraint routes are staged as nonclaim derivation targets",
        )
    )
    checks.append(
        (
            "V1041_5_coefficient_priors_nonclaim",
            len(prior_rows) >= 3
            and any(row["coefficient"] == "K_boundary_alpha3" for row in prior_rows)
            and all(row["score_ready"] == "false" and not flag(row["valid_for_claim"]) for row in prior_rows),
            "alpha3/R10 coefficient prior templates remain nonclaim",
        )
    )
    checks.append(
        (
            "V1041_6_action_selection_refused",
            any(row["selection_id"] == "SEL1041_0_do_not_select_yet" for row in selection_rows)
            and all(not flag(row["valid_for_claim"]) for row in selection_rows),
            "no parent action is falsely selected at 1041",
        )
    )
    checks.append(
        (
            "V1041_7_mts_template_schema_nonclaim",
            bool(mts_rows)
            and set(MTS_REQUIRED_COLUMNS).issubset(set(mts_rows[0].keys()))
            and all(not flag(row["valid_for_claim"]) for row in mts_rows),
            "MTS smoke template has runner schema and no claim-valid rows",
        )
    )
    checks.append(
        (
            "V1041_8_runner_smoke_refuses_claim",
            bool(smoke_rows)
            and smoke_rows[0]["R10_pass_for_claim"] == "false"
            and smoke_rows[0]["claim_allowed"] == "false"
            and smoke_rows[0]["valid_mts_rows"] == "0",
            "existing R10 runner refuses the 1041 nonclaim rows",
        )
    )
    checks.append(
        (
            "V1041_9_claim_gates_blocked",
            all(row["gate_pass"] == "false" and not flag(row["claim_allowed"]) for row in claim_rows),
            "all local-GR/empirical claim gates remain blocked",
        )
    )
    checks.append(
        (
            "V1041_10_next_target_written",
            bool(next_rows)
            and next_rows[0]["next_target"] == "1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md",
            "next target row is present",
        )
    )
    generated_files = [
        DOC,
        OUT / "P8_Y5_R10_1041_SOURCE_REGISTER.csv",
        OUT / "P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv",
        OUT / "P8_Y5_R10_1041_THETAX_PX_TEMPLATE_CONTRACT.csv",
        OUT / "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv",
        OUT / "P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv",
        OUT / "P8_Y5_R10_1041_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv",
        OUT / "P8_Y5_R10_1041_ACTION_SELECTION_DECISION.csv",
        OUT / "P8_Y5_R10_1041_RUNNER_SMOKE_STATUS.csv",
        OUT / "P8_Y5_R10_1041_PLACEHOLDER_REFUSAL_RUNNER.csv",
        OUT / "P8_Y5_R10_1041_CLAIM_GATES.csv",
        OUT / "P8_Y5_R10_1041_DECISION_LEDGER.csv",
        OUT / "P8_Y5_R10_1041_NEXT_TARGET.csv",
        OUT / "P8_Y5_BRR545_1041_VALIDATION.csv",
        MTS_TEMPLATE,
    ]
    checks.append(
        (
            "V1041_11_generated_files_in_post_checkpoint",
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
            "V1041_12_formalization_untouched",
            not formalization_touches,
            f"formalization-workbench modified-file count since script start is {len(formalization_touches)}",
        )
    )
    rows = [
        {
            "check_id": "V1041_SUMMARY",
            "result": "pass" if all(result for _, result, _ in checks) else "fail",
            "detail": "1041 parent X-sector Theta_X/P_X owner or boundary coefficient prior validation summary",
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
    candidate_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    noflux_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    selection_rows: list[dict[str, str]],
    mts_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    sections = [
        "# 1041 Y5 R10 parent X-sector ThetaX/PX owner or boundary coefficient prior",
        "",
        "**Progress:** the parent-action menu is now explicit. `Theta_X` and `P_X` can be computed once a lawful `L_X` route is selected; until then they remain contracts, not claims.",
        "",
        "**Best routes:** absent/quotient `X` is strongest if proved; first-class vertical constraint is the best active derivation route; positive source-free no-hair is the best concrete fallback. A sourced `X` is empirical, not a GR derivation.",
        "",
        "**Claim ceiling:** no parent `L_X`, `Theta_X`, or `P_X` owner is selected at 1041. Alpha3/R10 coefficient priors remain private nonclaim scaffolding.",
        "",
        "## Source register",
        md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
        "## Parent X candidate classifier",
        md_table(candidate_rows, ["candidate_id", "parent_route", "ThetaX_PX_result", "boundary_result", "risk", "rank", "current_status", "valid_for_claim"]),
        "## ThetaX/PX template contract",
        md_table(template_rows, ["template_id", "object", "formula", "owned_if", "current_status", "claim_effect", "valid_for_claim"]),
        "## ThetaX owner gate",
        md_table(owner_rows, ["gate_id", "needed", "test", "current_status", "if_missing", "valid_for_claim"]),
        "## No-flux theorem-zero route",
        md_table(noflux_rows, ["route_id", "route", "identity", "zero_condition", "missing", "current_status", "valid_for_claim"]),
        "## Boundary coefficient prior template",
        md_table(prior_rows, ["prior_id", "coefficient", "observable", "prior_or_bound_rule", "anchor_bound", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
        "## Action selection decision",
        md_table(selection_rows, ["selection_id", "decision", "reason", "safe_use", "valid_for_claim"]),
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
    candidate_rows = candidate_classifier_rows()
    template_rows = thetax_px_template_rows()
    owner_rows = owner_gate_rows()
    noflux_rows = noflux_route_rows()
    prior_rows = coefficient_prior_rows(local_bounds_index())
    selection_rows = action_selection_rows()
    mts_rows = mts_template_rows()
    write_csv(MTS_TEMPLATE, mts_rows, MTS_REQUIRED_COLUMNS)
    runner_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, RUN_DIR)
    smoke_rows = runner_smoke_rows(runner_result["status"])
    refusal_rows = placeholder_refusal_rows(candidate_rows, template_rows, owner_rows, prior_rows)
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation = validate(
        source_rows,
        candidate_rows,
        template_rows,
        owner_rows,
        noflux_rows,
        prior_rows,
        selection_rows,
        mts_rows,
        smoke_rows,
        claim_rows,
        next_rows,
    )

    write_csv(OUT / "P8_Y5_R10_1041_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv", candidate_rows)
    write_csv(OUT / "P8_Y5_R10_1041_THETAX_PX_TEMPLATE_CONTRACT.csv", template_rows)
    write_csv(OUT / "P8_Y5_R10_1041_THETAX_OWNER_GATE.csv", owner_rows)
    write_csv(OUT / "P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv", noflux_rows)
    write_csv(OUT / "P8_Y5_R10_1041_BOUNDARY_COEFFICIENT_PRIOR_TEMPLATE.csv", prior_rows)
    write_csv(OUT / "P8_Y5_R10_1041_ACTION_SELECTION_DECISION.csv", selection_rows)
    write_csv(OUT / "P8_Y5_R10_1041_RUNNER_SMOKE_STATUS.csv", smoke_rows)
    write_csv(OUT / "P8_Y5_R10_1041_PLACEHOLDER_REFUSAL_RUNNER.csv", refusal_rows)
    write_csv(OUT / "P8_Y5_R10_1041_CLAIM_GATES.csv", claim_rows)
    write_csv(OUT / "P8_Y5_R10_1041_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1041_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_1041_VALIDATION.csv", validation)
    write_doc(
        source_rows,
        candidate_rows,
        template_rows,
        owner_rows,
        noflux_rows,
        prior_rows,
        selection_rows,
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
        raise SystemExit(f"1041 validation failed: {failed}")


if __name__ == "__main__":
    main()
