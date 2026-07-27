from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3508-Y5-R2FR-current-source-normalization-Ward-identity-or-alpha-source-bound.md"
CANONICAL_WARD_RESIDUAL = OUT / "P8_EM_current_source_Ward_alpha_source_residual.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3508": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3507": {
        "path": ROOT / "3507-Y5-R2FR-scalar-gauge-coupling-owner-DXlambda-zero-or-alpha-bound-runner.md",
        "role": "3507 scalar coupling identity handoff",
    },
    "alpha_residual_3507": {
        "path": OUT / "P8_EM_scalar_coupling_owner_alpha_residual.csv",
        "role": "3507 alpha residual vector",
    },
    "alpha_identity_3507": {
        "path": OUT / "P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv",
        "role": "3507 alpha coupling identity",
    },
    "alpha_contract_1055": {
        "path": ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
        "role": "alpha owner and matter-functor contract",
    },
    "matter_functor_1045": {
        "path": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "role": "parent matter functor signature audit",
    },
    "matter_source_3235": {
        "path": OUT / "P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv",
        "role": "matter source functor derivation",
    },
    "current_source_1453": {
        "path": OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv",
        "role": "current/source normalization owner attempt",
    },
    "ward_universality_contract": {
        "path": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
        "role": "source-current Ward universality contract",
    },
    "ward_owner_contract": {
        "path": OUT / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "Ward source-owner identity contract",
    },
    "source_norm_vector": {
        "path": OUT / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "source normalization coefficient vector",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def ward_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "ward_id": "WARD3508_0_gauge_current_owner",
            "object": "J_Q",
            "identity": "Gauge invariance of the same matter action defines and conserves the visible charge current.",
            "mathematical_form": "J_Q^mu := (1/sqrt(-g_obs)) delta S_matter/delta A_Q_mu;  nabla_mu J_Q^mu = 0 on matter shell",
            "derivation": "Vary S_matter under A_Q -> A_Q+d epsilon and Psi_A -> exp(i q_A epsilon)Psi_A. After the matter equations, the coefficient of epsilon gives the Noether/Ward identity.",
            "what_it_kills": "post-hoc current definitions and downstream charge-current rescalings if variation-before-readout is signed",
            "what_survives": "a pre-variation scalar coupling kappa_A(X) inside S_matter or an independent source-only current slot",
            "status": "EXACT_STANDARD_WARD_IF_COMMON_ACTION",
            "source_path": str(SOURCES["current_source_1453"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "ward_id": "WARD3508_1_diffeomorphism_Lorentz_force_owner",
            "object": "T_H and J_Q",
            "identity": "The Hilbert stress and the EM current are linked by the diffeomorphism Ward identity of one matter action.",
            "mathematical_form": "nabla_mu T_H^{mu nu} = F_Q^{nu}{}_{mu} J_Q^mu + E_Psi nabla^nu Psi + owned spin/connection terms",
            "derivation": "Vary S_matter under an observed-frame diffeomorphism. The metric/coframe variation gives T_H, the gauge-field Lie derivative gives F.J, and matter equations remove E_Psi terms.",
            "what_it_kills": "treating EM current and active stress as independently normalized after variation",
            "what_survives": "relative weights already present in S_matter before the Ward identity is taken",
            "status": "EXACT_IF_SINGLE_OBSERVED_MATTER_ACTION",
            "source_path": str(SOURCES["ward_universality_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "ward_id": "WARD3508_2_vertical_current_normalization",
            "object": "z_g = D_X ln g_J",
            "identity": "If charge labels and the current functor are fixed quotient representation data, the vertical derivative of the current normalization vanishes.",
            "mathematical_form": "S_A=S_A[Psi_A,e_obs(q),A_Q,theta_A^0], D_X theta_A^0=0, no kappa_A(X)A_Q.J_A => z_g=0",
            "derivation": "The chain rule has no X-owner for g_J once A_Q and theta_A are the only current arguments; a vertical motion in ker(Dq) cannot change the representation charge or the current normalization.",
            "what_it_kills": "the z_g half of b_alpha_X=2 z_g-z_lambda",
            "what_survives": "matter functor and no-source-only-slot are still not parent-signed in the current corpus",
            "status": "CONDITIONAL_ZERO_THEOREM_NOT_LIVE_CLAIM",
            "source_path": str(SOURCES["matter_functor_1045"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "ward_id": "WARD3508_3_species_blind_source_functor",
            "object": "beta_source_alpha and epsilon_species_A",
            "identity": "If the gravitational source is the total Hilbert variation of the same source-label-forgetting matter functor, alpha/source marker charges are structurally unavailable.",
            "mathematical_form": "T_total=sum_A 2/sqrt(-g_obs) delta S_A/delta g_obs; no F((T_A,A))->kappa_A T_A selector",
            "derivation": "The parent source map sees the summed Hilbert current, not a list of species labels after variation. A material-selector source charge cannot be formed without adding an extra object to the source functor.",
            "what_it_kills": "beta_source_alpha, epsilon_species_A, eta_source_AB, post-variation material source selectors",
            "what_survives": "pre-variation weights w_A(X)S_A and non-Hilbert source bypasses unless banned by the parent object language",
            "status": "CONDITIONAL_SOURCE_LABEL_FORGETTING_THEOREM",
            "source_path": str(SOURCES["alpha_contract_1055"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "ward_id": "WARD3508_4_prevariation_weight_limit",
            "object": "w_A(X) and kappa_A(X)",
            "identity": "Ward identities do not remove a source/charge prefactor that was already inserted inside the action before variation.",
            "mathematical_form": "S_matter=sum_A w_A(X) S_A or S_int=sum_A kappa_A(X) A_Q.J_A still has Ward identities with weighted T_A,J_A",
            "derivation": "A symmetry identity differentiates the action it is given. If the action already contains weights, the identity conserves the weighted currents rather than proving the weights absent.",
            "what_it_kills": "false proof that conservation alone fixes normalization",
            "what_survives": "source-only scalar slots, species weights, hidden material markers",
            "status": "COUNTERMODEL_RETAINED",
            "source_path": str(SOURCES["current_source_1453"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "ward_id": "WARD3508_5_alpha_consequence",
            "object": "b_alpha_X",
            "identity": "If WARD3508_2 closes, the alpha residual reduces from b_alpha_X=2z_g-z_lambda to b_alpha_X=-z_lambda.",
            "mathematical_form": "z_g=0 => D_X ln alpha_eff = -D_X ln lambda_A",
            "derivation": "Substitute the current-normalization zero theorem into the exact 3507 scalar coupling identity.",
            "what_it_kills": "current/readout part of alpha drift and alpha-source composition branch",
            "what_survives": "Maxwell kinetic scalar owner z_lambda and derivative-lambda force",
            "status": "EXACT_CONDITIONAL_REDUCTION",
            "source_path": str(SOURCES["alpha_identity_3507"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def residual_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CSR3508_0_z_g",
            "residual": "z_g",
            "incoming_status": "CURRENT_OWNER_UNSIGNED",
            "3508_result": "conditional zero if current is varied from fixed quotient matter functor",
            "formula": "z_g=D_X ln g_J",
            "zero_condition": "fixed representation theta_A, no kappa_A(X), no source-only current slot",
            "remaining_blocker": "matter functor/no-source-only action grammar not parent-signed",
            "observable_links": "alpha_EM; WEP; R10; charge_readout",
            "claim_allowed": "False",
        },
        {
            "row_id": "CSR3508_1_b_alpha_X",
            "residual": "b_alpha_X",
            "incoming_status": "EXACT_IDENTITY_NOT_NUMERIC",
            "3508_result": "reduces to -z_lambda if z_g closes",
            "formula": "b_alpha_X=2z_g-zlambda -> -zlambda",
            "zero_condition": "z_g=0 and z_lambda=0",
            "remaining_blocker": "z_lambda/fixed Maxwell kinetic owner still unsigned",
            "observable_links": "alpha_EM; clocks; spectroscopy; Coulomb_binding",
            "claim_allowed": "False",
        },
        {
            "row_id": "CSR3508_2_beta_source_alpha",
            "residual": "beta_source_alpha",
            "incoming_status": "ALPHA_SOURCE_MARKER_LIVE",
            "3508_result": "conditional zero if source-label-forgetting Hilbert functor is parent-signed",
            "formula": "partial_A mu_obs = 0 for alpha/source material marker",
            "zero_condition": "T_total is the only active source and no F((T_A,A))->kappa_A T_A selector exists",
            "remaining_blocker": "pre-variation source weights and non-Hilbert bypasses remain legal",
            "observable_links": "WEP; R10; source_composition; clock_redshift",
            "claim_allowed": "False",
        },
        {
            "row_id": "CSR3508_3_epsilon_species_A",
            "residual": "epsilon_species_A",
            "incoming_status": "RETAINED_SOURCE_NORMALIZATION_COEFFICIENT",
            "3508_result": "conditional zero for post-variation species source selectors only",
            "formula": "epsilon_species_A = Delta_A mu_obs/(G_ref M_H)",
            "zero_condition": "source functor forgets species labels before source coupling selection",
            "remaining_blocker": "w_A(X)S_A pre-action weight countermodel",
            "observable_links": "eta_source_AB; WEP; local_GR_source",
            "claim_allowed": "False",
        },
        {
            "row_id": "CSR3508_4_postvariation_rescaling",
            "residual": "postvariation_current_rescaling",
            "incoming_status": "READOUT_ORDER_UNSIGNED",
            "3508_result": "killed conditionally: readout after Hilbert/Noether variation cannot redefine parent source",
            "formula": "J_parent := delta S/delta A; T_parent := delta S/delta g before readout",
            "zero_condition": "variation-before-readout and parent source definition signed",
            "remaining_blocker": "readout-order/source model not parent-signed globally",
            "observable_links": "charge_readout; clock; source_calibration",
            "claim_allowed": "False",
        },
        {
            "row_id": "CSR3508_5_prevariation_weight",
            "residual": "prevariation_weight",
            "incoming_status": "COUNTERMODEL_RETAINED",
            "3508_result": "not killed by Ward; must be banned by action grammar or bounded",
            "formula": "S_matter=sum_A w_A(X)S_A",
            "zero_condition": "no source-only scalar/material marker argument in parent matter constructor",
            "remaining_blocker": "object-language/domain exhaustion theorem required",
            "observable_links": "WEP; source_composition; Newton_G; PPN",
            "claim_allowed": "False",
        },
        {
            "row_id": "CSR3508_6_nonHilbert_bypass",
            "residual": "nonHilbert_source_bypass",
            "incoming_status": "PARALLEL_GATE_OPEN",
            "3508_result": "not killed by ordinary Hilbert Ward unless all active source currents are declared Hilbert/improvement-owned",
            "formula": "J_src = kappa T_H + sum_A zeta_A J_NH,A",
            "zero_condition": "non-Hilbert currents are exact improvements with zero exterior flux or retained as explicit residuals",
            "remaining_blocker": "owner divergence/flux theorem not complete",
            "observable_links": "PPN; source_normalization; boundary_flux",
            "claim_allowed": "False",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ASBIN3508_0_z_g_alpha",
            "arena": "alpha/clock/spectroscopy",
            "residual": "z_g",
            "predicted_value": "MISSING_DX_LN_GJ",
            "predicted_units": "dimensionless_derivative_or_declared_scale",
            "bound_value": "MISSING_ALPHA_CLOCK_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["alpha_residual_3507"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ASBIN3508_1_beta_source_alpha_WEP",
            "arena": "WEP/source composition",
            "residual": "beta_source_alpha",
            "predicted_value": "MISSING_ALPHA_SOURCE_COMPOSITION_MAP",
            "predicted_units": "dimensionless",
            "bound_value": "MISSING_WEP_SOURCE_BOUND",
            "bound_units": "dimensionless",
            "source_path": str(SOURCES["source_norm_vector"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ASBIN3508_2_epsilon_species_A",
            "arena": "local source normalization",
            "residual": "epsilon_species_A",
            "predicted_value": "MISSING_SPECIES_SOURCE_CHARGE",
            "predicted_units": "dimensionless",
            "bound_value": "MISSING_ETA_SOURCE_BOUND",
            "bound_units": "dimensionless",
            "source_path": str(SOURCES["source_norm_vector"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ASBIN3508_3_prevariation_weight",
            "arena": "matter action/source weight",
            "residual": "prevariation_weight",
            "predicted_value": "MISSING_WA_PROFILE",
            "predicted_units": "dimensionless_or_derivative",
            "bound_value": "MISSING_SOURCE_WEIGHT_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["matter_source_3235"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "ASBIN3508_4_nonHilbert_bypass",
            "arena": "PPN/source-current bypass",
            "residual": "nonHilbert_source_bypass",
            "predicted_value": "MISSING_ZETA_NH",
            "predicted_units": "dimensionless_or_flux",
            "bound_value": "MISSING_PPN_SOURCE_BYPASS_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["ward_owner_contract"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def run_alpha_source_bound_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        predicted = parse_float(str(row["predicted_value"]))
        bound = parse_float(str(row["bound_value"]))
        if row["valid_for_claim"] != "True":
            verdict = "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM"
            passes = "False"
        elif predicted is None or bound is None or bound <= 0:
            verdict = "BLOCKED_MISSING_NUMERIC_PREDICTION_OR_BOUND"
            passes = "False"
        else:
            passes = bool_text(abs(predicted) <= bound)
            verdict = "PASS_NUMERIC_ALPHA_SOURCE_BOUND" if passes == "True" else "FAIL_NUMERIC_ALPHA_SOURCE_BOUND"
        results.append(
            {
                "row_id": row["row_id"].replace("ASBIN", "ASRUN"),
                "arena": row["arena"],
                "residual": row["residual"],
                "predicted_value": row["predicted_value"],
                "bound_value": row["bound_value"],
                "pass_condition": "abs(predicted_value) <= bound_value with sourced numeric rows",
                "runner_verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return results


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3508_0_Ward_identity_useful",
            "decision": "Ward identities do real work, but only after the action domain is fixed.",
            "rationale": "They lock Noether current and Hilbert stress to the same action and kill post-variation rescaling, but they conserve any pre-variation weights already inserted.",
            "effect": "z_g is a conditional zero theorem, not a live claim.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3508_1_alpha_progress",
            "decision": "If the matter functor is parent-signed, b_alpha_X reduces to -z_lambda.",
            "rationale": "The 3507 identity plus WARD3508_2 removes the current/readout half of alpha drift.",
            "effect": "The remaining coupling frontier splits cleanly into matter-functor source slots and Maxwell kinetic owner.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3508_2_best_next_target",
            "decision": "Attack source-only matter slots before claiming local GR source universality.",
            "rationale": "The surviving loophole is not the Ward identity; it is the allowed action grammar w_A(X), kappa_A(X), and non-Hilbert source bypass.",
            "effect": "Next derivation should ban those slots from the parent matter constructor or make their bounds executable.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3509-Y5-R2FR-no-source-only-matter-functor-signature-or-zg-bound.md",
            "next_script": "scripts/Y5_R2FR_3509_no_source_only_matter_functor_signature_or_zg_bound.py",
            "objective": "Derive whether the parent matter constructor forbids w_A(X), kappa_A(X), source-only material markers, and non-Hilbert active source bypasses; if not, fill z_g/beta_source_alpha/WEP/source-normalization bound rows.",
            "success_gate": "Either source-only matter slots are excluded by parent object-language/domain exhaustion, or every surviving source-normalization residual has numeric-ready non-claim bound inputs.",
            "forbidden_shortcuts": "Do not use Ward conservation alone as a normalization proof; do not set source weights to one by convention.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ward_ids = {row["ward_id"] for row in ward_rows}
    residual_names = {row["residual"] for row in residuals}
    all_claim_false = all(
        row.get("valid_for_claim") == "False"
        for table in [sources, ward_rows, bound_inputs, runner_results, decisions, next_rows]
        for row in table
    ) and all(row.get("claim_allowed") == "False" for row in residuals)
    all_blocked = all("BLOCKED" in row["runner_verdict"] for row in runner_results)
    validation = [
        {
            "check_id": "VAL3508_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_1_Ward_identities_present",
            "passed": bool_text({"WARD3508_0_gauge_current_owner", "WARD3508_1_diffeomorphism_Lorentz_force_owner", "WARD3508_2_vertical_current_normalization"}.issubset(ward_ids)),
            "detail": "gauge, diffeomorphism, and vertical current identities written",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_2_residual_map_complete",
            "passed": bool_text({"z_g", "b_alpha_X", "beta_source_alpha", "epsilon_species_A", "prevariation_weight", "nonHilbert_source_bypass"}.issubset(residual_names)),
            "detail": "current/source residual map covers alpha and local source branches",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_3_balpha_reduction_present",
            "passed": bool_text(any(row["residual"] == "b_alpha_X" and "-zlambda" in row["formula"] for row in residuals)),
            "detail": "b_alpha_X reduction under z_g=0 recorded",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_4_bound_runner_blocks_placeholders",
            "passed": bool_text(all_blocked),
            "detail": "all alpha-source bound rows remain blocked until numeric sourced inputs exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_5_no_claim_flags",
            "passed": bool_text(all_claim_false),
            "detail": "no 3508 output row is valid_for_claim=True or claim_allowed=True",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_6_next_target_source_only_slots",
            "passed": bool_text(next_rows[0]["next_doc"].startswith("3509") and "source-only" in next_rows[0]["objective"]),
            "detail": "source-only matter slot theorem selected as next derivation target",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3508_7_formalization_workbench_not_targeted",
            "passed": bool_text(FORMALIZATION.exists() and str(DOC).startswith(str(ROOT))),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        },
    ]
    validation.append(
        {
            "check_id": "VAL3508_SUMMARY",
            "passed": bool_text(all(row["passed"] == "True" for row in validation)),
            "detail": "PASS" if all(row["passed"] == "True" for row in validation) else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return validation


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    ward_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3508 - Current/Source Normalization Ward Identity Or Alpha-Source Bound",
                "",
                "## Summary",
                "- **Derived gain:** one common observed matter action gives exact gauge and diffeomorphism Ward identities tying `J_Q` and `T_H` before readout.",
                "- **Real zero route:** if the parent matter functor fixes representation data and forbids `kappa_A(X)`/`w_A(X)` source-only slots, then `z_g=0` and `b_alpha_X` reduces to `-zlambda`.",
                "- **Hard limit:** Ward conservation alone cannot prove normalization; it preserves pre-variation weights if the action was allowed to contain them.",
                "- **Next best move:** ban source-only matter slots from the parent action grammar, or bound `z_g`, `beta_source_alpha`, and species-source residuals explicitly.",
                "",
                "## Ward Identity Theorems",
                markdown_table(
                    ward_rows,
                    ["ward_id", "object", "identity", "mathematical_form", "what_it_kills", "what_survives", "status"],
                ),
                "",
                "## Residual Reduction Map",
                markdown_table(
                    residuals,
                    ["row_id", "residual", "3508_result", "formula", "zero_condition", "remaining_blocker", "claim_allowed"],
                ),
                "",
                "## Alpha-Source Bound Input Template",
                markdown_table(
                    bound_inputs,
                    ["row_id", "arena", "residual", "predicted_value", "bound_value", "source_path", "valid_for_claim"],
                ),
                "",
                "## Runner Results",
                markdown_table(
                    runner_results,
                    ["row_id", "arena", "residual", "pass_condition", "runner_verdict", "passes_bound", "claim_allowed"],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"],
                ),
                "",
                "## Validation",
                markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {now_utc()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    ward_rows = ward_identity_rows()
    residuals = residual_reduction_rows()
    bound_inputs = bound_input_rows()
    runner_results = run_alpha_source_bound_rows(bound_inputs)
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation_rows = validate(sources, ward_rows, residuals, bound_inputs, runner_results, decisions, next_rows)

    write_csv(OUT / "P8_Y5_R2FR_3508_SOURCE_REGISTER.csv", sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        OUT / "P8_Y5_R2FR_3508_CURRENT_SOURCE_WARD_IDENTITY.csv",
        ward_rows,
        ["ward_id", "object", "identity", "mathematical_form", "derivation", "what_it_kills", "what_survives", "status", "source_path", "valid_for_claim"],
    )
    residual_fields = [
        "row_id",
        "residual",
        "incoming_status",
        "3508_result",
        "formula",
        "zero_condition",
        "remaining_blocker",
        "observable_links",
        "claim_allowed",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3508_ZG_BETA_SOURCE_REDUCTION.csv", residuals, residual_fields)
    write_csv(CANONICAL_WARD_RESIDUAL, residuals, residual_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3508_ALPHA_SOURCE_BOUND_INPUT_TEMPLATE.csv",
        bound_inputs,
        ["row_id", "arena", "residual", "predicted_value", "predicted_units", "bound_value", "bound_units", "source_path", "valid_for_claim"],
    )
    runner_fields = [
        "row_id",
        "arena",
        "residual",
        "predicted_value",
        "bound_value",
        "pass_condition",
        "runner_verdict",
        "passes_bound",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3508_ALPHA_SOURCE_BOUND_RUNNER_RESULTS.csv", runner_results, runner_fields)
    write_csv(OUT / "P8_EM_alpha_source_bound_runner_results.csv", runner_results, runner_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3508_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "rationale", "effect", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3508_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_BRR545_3508_VALIDATION.csv", validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(ward_rows, residuals, bound_inputs, runner_results, decisions, next_rows, validation_rows)


if __name__ == "__main__":
    main()
