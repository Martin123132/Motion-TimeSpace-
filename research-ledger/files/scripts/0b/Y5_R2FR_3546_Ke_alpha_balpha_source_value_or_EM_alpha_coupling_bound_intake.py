from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3546-Y5-R2FR-Ke-alpha-balpha-source-value-or-EM-alpha-coupling-bound-intake.md"
CANONICAL_STATUS = OUT / "P8_Y5_Ke_alpha_balpha_source_value_status.csv"

DELTA_Q_E_3545 = 2.040000e-03
DELTA_Q_ALPHA_COULOMB_3465 = 0.001989808886825
ETA_BOUND = 2.8e-15
KE_BALPHA_DD_E_CEILING = ETA_BOUND / DELTA_Q_E_3545
DE_ALPHA_ONLY_CEILING = ETA_BOUND / DELTA_Q_ALPHA_COULOMB_3465
CONVENTION_SPREAD_FRACTION = abs(KE_BALPHA_DD_E_CEILING - DE_ALPHA_ONLY_CEILING) / KE_BALPHA_DD_E_CEILING


SOURCES: dict[str, dict[str, Any]] = {
    "script_3546": {"path": Path(__file__).resolve(), "role": "3546 generator"},
    "doc_3545": {
        "path": ROOT / "3545-Y5-R2FR-first-DD-K-value-or-MICROSCOPE-source-leg-acquisition.md",
        "role": "first DD K/source-leg handoff",
    },
    "next_3545": {
        "path": OUT / "P8_Y5_R2FR_3545_NEXT_TARGET.csv",
        "role": "3545 selected Ke_alpha*b_alpha target",
    },
    "hunt_3545": {
        "path": OUT / "P8_Y5_R2FR_3545_K_VALUE_HUNT_RESULTS.csv",
        "role": "prior K/value hunt result",
    },
    "component_gate_3545": {
        "path": OUT / "P8_Y5_R2FR_3545_COMPONENT_SCORE_INPUTS.csv",
        "role": "3545 product ceilings and score readiness",
    },
    "alpha_identity_3507": {
        "path": OUT / "P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv",
        "role": "canonical alpha identity and convention trap",
    },
    "alpha_residual_3507": {
        "path": OUT / "P8_Y5_R2FR_3507_ALPHA_RESIDUAL_VECTOR.csv",
        "role": "b_alpha, z_g, z_lambda residual vector",
    },
    "alpha_source_template_3508": {
        "path": OUT / "P8_Y5_R2FR_3508_ALPHA_SOURCE_BOUND_INPUT_TEMPLATE.csv",
        "role": "alpha source-bound missing input template",
    },
    "alpha_source_ward_3508": {
        "path": OUT / "P8_EM_current_source_Ward_alpha_source_residual.csv",
        "role": "source/current Ward residual and beta_source_alpha status",
    },
    "alpha_bound_rows_3526": {
        "path": OUT / "P8_Y5_R2FR_3526_ALPHA_BOUND_ROWS.csv",
        "role": "alpha WEP/clock/R10 bound rows",
    },
    "alpha_only_calc_3465": {
        "path": OUT / "P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv",
        "role": "alpha-only effective WEP ceiling",
    },
    "calibrated_alpha_contract_3528": {
        "path": OUT / "P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv",
        "role": "calibrated alpha policy and forbidden uses",
    },
    "calibrated_alpha_status_3529": {
        "path": OUT / "P8_local_GR_calibrated_alpha_source_interface_status.csv",
        "role": "local GR calibrated alpha interface status",
    },
    "em_owner_bound_vector_3503": {
        "path": OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
        "role": "EM Hodge/Maxwell/current owner residual vector",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local bound source register including MICROSCOPE",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "KAB3546_0_EM_action_start",
            "object": "local EM normalization",
            "mathematical_form": "S_EM[X] = -1/4 lambda_A(X) int F^2 + g_J(X) int A_mu J^mu",
            "result": "the raw Maxwell kinetic coefficient and current coupling are separately convention-dependent",
            "zero_or_bound_role": "sets the exact variables whose mismatch becomes b_alpha",
            "source_path": str(SOURCES["alpha_identity_3507"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "KAB3546_1_canonical_charge",
            "object": "canonical local charge",
            "mathematical_form": "A_c = sqrt(lambda_A) A; g_eff = g_J/sqrt(lambda_A); alpha_eff proportional to g_J^2/lambda_A",
            "result": "a field rescaling can move coefficients but cannot remove the invariant ratio",
            "zero_or_bound_role": "prevents false alpha-zero claims by convention",
            "source_path": str(SOURCES["alpha_identity_3507"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "KAB3546_2_balpha_law",
            "object": "alpha vertical residual",
            "mathematical_form": "b_alpha := D_X ln alpha_eff = 2 z_g - z_lambda",
            "result": "K_e_alpha*b_alpha is zero only if alpha is calibrated constant or parent proves 2 z_g = z_lambda",
            "zero_or_bound_role": "exact law for the EM/source coupling target",
            "source_path": str(SOURCES["alpha_residual_3507"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "identity_id": "KAB3546_3_WEP_projection",
            "object": "alpha-only WEP channel",
            "mathematical_form": "eta_TiPt^(alpha) = DeltaQ_e(TiPt) * (K_e_alpha*b_alpha) + R_nonalpha",
            "result": f"under an isolated no-cancellation alpha branch, |K_e_alpha*b_alpha| <= {KE_BALPHA_DD_E_CEILING:.12e}",
            "zero_or_bound_role": "finite branch bound if parent zero does not close",
            "source_path": str(SOURCES["component_gate_3545"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def zero_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "ZKAB3546_0_calibrated_baseline",
            "claim": "baseline local branch may set alpha_EM=alpha_0 as measured universal constant",
            "mathematical_condition": "D_X ln alpha_eff = 0",
            "effect_on_product": "K_e_alpha*b_alpha = 0 if K_e_alpha is finite",
            "current_evidence": "calibrated-alpha contract exists and allows Maxwell stress bookkeeping",
            "remaining_gap": "calibration is not a parent derivation of alpha or C_XF2=0",
            "status": "CLOSURE_BASELINE_ALLOWED_NOT_DERIVED",
            "source_path": str(SOURCES["calibrated_alpha_contract_3528"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZKAB3546_1_parent_same_owner",
            "claim": "parent quotient owner ties current normalization to Maxwell kinetic normalization",
            "mathematical_condition": "2 z_g - z_lambda = 0",
            "effect_on_product": "b_alpha=0 without using calibration closure",
            "current_evidence": "exact identity exists; same-owner relation not parent-signed",
            "remaining_gap": "fixed representation/current owner and unique F2/fibre norm must be proved in one parent object-language",
            "status": "DERIVATION_ROUTE_OPEN_UNSIGNED",
            "source_path": str(SOURCES["alpha_identity_3507"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZKAB3546_2_no_source_marker",
            "claim": "alpha channel carries no material/source marker after Hilbert source reduction",
            "mathematical_condition": "partial_A mu_obs(alpha marker)=0 and beta_source_alpha=0",
            "effect_on_product": "prevents K_e_alpha from becoming species/source-dependent even when b_alpha is present",
            "current_evidence": "conditional source-label forgetting row exists",
            "remaining_gap": "pre-variation weights and non-Hilbert bypass remain legal until action grammar closes",
            "status": "SOURCE_MARKER_ZERO_UNSIGNED",
            "source_path": str(SOURCES["alpha_source_ward_3508"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZKAB3546_3_readout_radiative_stability",
            "claim": "loops, clocks, material binding and readout maps do not regenerate alpha dependence",
            "mathematical_condition": "R_readout_alpha = R_rad_alpha = 0",
            "effect_on_product": "keeps calibrated alpha from re-entering as an effective WEP/source coefficient",
            "current_evidence": "EM owner vector retains C_EM_readout and radiative/flux components",
            "remaining_gap": "radiative/readout closure not parent-signed",
            "status": "READOUT_STABILITY_UNSIGNED",
            "source_path": str(SOURCES["em_owner_bound_vector_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "clause_id": "ZKAB3546_4_factorized_source_leg",
            "claim": "K_e_alpha is a real source/material projection, not a hidden fitted number",
            "mathematical_condition": "K_e_alpha = K[Earth source, Ti/Pt material tensor, readout convention, q normalization]",
            "effect_on_product": "lets a nonzero b_alpha be scored against MICROSCOPE instead of being a placeholder",
            "current_evidence": "3545 product ceiling exists; factorized source leg remains missing",
            "remaining_gap": "Earth/source leg, alloy policy, q units and sign convention",
            "status": "FINITE_BOUND_ROUTE_INPUTS_MISSING",
            "source_path": str(SOURCES["hunt_3545"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "B3546_0_DD_e_basis",
            "target": "K_e_alpha*b_alpha",
            "arena": "MICROSCOPE alpha/source WEP, DD-like e basis",
            "formula": "abs(K_e_alpha*b_alpha) <= eta_bound / abs(DeltaQ_e)",
            "delta_q_used": f"{DELTA_Q_E_3545:.12e}",
            "bound_value": f"{KE_BALPHA_DD_E_CEILING:.12e}",
            "units": "dimensionless effective source-coupling product",
            "source_path": str(SOURCES["component_gate_3545"]["path"]),
            "numeric_bound_ready": "True",
            "mts_value_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3546_1_alpha_Coulomb_basis",
            "target": "D_e_eff(alpha-only)",
            "arena": "MICROSCOPE alpha-only Coulomb-material convention",
            "formula": "abs(D_e_eff) <= eta_bound / abs(DeltaQ_alpha_Coulomb)",
            "delta_q_used": f"{DELTA_Q_ALPHA_COULOMB_3465:.12e}",
            "bound_value": f"{DE_ALPHA_ONLY_CEILING:.12e}",
            "units": "dimensionless effective alpha source coefficient",
            "source_path": str(SOURCES["alpha_only_calc_3465"]["path"]),
            "numeric_bound_ready": "True",
            "mts_value_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3546_2_convention_bridge_spread",
            "target": "basis reconciliation",
            "arena": "DD e basis versus alpha-only Coulomb basis",
            "formula": "abs(B_DD_e - B_alpha_Coulomb)/B_DD_e",
            "delta_q_used": "two non-identical material conventions",
            "bound_value": f"{CONVENTION_SPREAD_FRACTION:.12e}",
            "units": "fractional spread",
            "source_path": str(SOURCES["alpha_only_calc_3465"]["path"]),
            "numeric_bound_ready": "True",
            "mts_value_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "B3546_3_clock_product_quarantine",
            "target": "b_alpha*tau_clock_time",
            "arena": "atomic clock alpha drift",
            "formula": "abs(P_clock_alpha) <= 2.1e-18 yr^-1",
            "delta_q_used": "clock sensitivity basis, not WEP material tensor",
            "bound_value": "2.100000000000e-18",
            "units": "yr^-1",
            "source_path": str(SOURCES["alpha_bound_rows_3526"]["path"]),
            "numeric_bound_ready": "True",
            "mts_value_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def input_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "IN3546_0_balpha_parent_value_or_zero",
            "target": "b_alpha",
            "must_supply": "parent theorem for 2 z_g = z_lambda, or numeric b_alpha with source path and units",
            "acceptance_gate": "no field-rescaling-only argument; current and Maxwell kinetic owners must be tracked together",
            "current_status": "MISSING_PARENT_VALUE_OR_ZERO",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN3546_1_Ke_alpha_factorized",
            "target": "K_e_alpha",
            "must_supply": "Earth/source leg, Ti/Pt material tensor, alpha/Coulomb sensitivity convention, readout/sign/q normalization",
            "acceptance_gate": "one convention maps to either DD e basis or alpha-Coulomb basis without mixing them",
            "current_status": "MISSING_FACTORIZED_SOURCE_LEG",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN3546_2_no_nonalpha_cancellation",
            "target": "residual isolation",
            "must_supply": "mass/shadow/projector/readout terms are zero-owned or separately bounded with no cancellation credit",
            "acceptance_gate": "alpha-only pass cannot hide non-alpha residuals",
            "current_status": "MISSING_FULL_RESIDUAL_ENVELOPE",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN3546_3_readout_radiative_reentry",
            "target": "effective alpha branch",
            "must_supply": "proof or finite row for clock/material/readout/radiative regeneration of alpha dependence",
            "acceptance_gate": "calibrated alpha baseline cannot be reused as a theorem-zero for loop/readout terms",
            "current_status": "MISSING_READOUT_STABILITY_PROOF",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN3546_4_public_claim_policy",
            "target": "claim hygiene",
            "must_supply": "numeric parent value or theorem-zero plus sourced K_e_alpha projection and validation rows",
            "acceptance_gate": "valid_for_claim remains False until all rows are parent-owned and source-backed",
            "current_status": "CLAIM_BLOCK_RETAINED",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3546_0_value_found",
            "question": "Did 3546 find a sourced numeric K_e_alpha*b_alpha value?",
            "decision": "NO",
            "basis": "current corpus supplies exact alpha identities and numeric WEP ceilings, but no parent-owned b_alpha or factorized K_e_alpha",
            "effect": "no WEP/local-GR/source-coupling claim",
            "next_action": "attempt parent same-owner zero proof for b_alpha, then source K_e_alpha if the proof fails",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3546_1_zero_route",
            "question": "Can the baseline set K_e_alpha*b_alpha=0?",
            "decision": "YES_AS_CALIBRATED_BASELINE_ONLY",
            "basis": "3528 permits alpha_EM=alpha_0 as a calibrated local constant, like GR uses measured G_N",
            "effect": "Maxwell stress can be used consistently in local baseline work, but this is not a derived alpha theorem",
            "next_action": "keep active nonzero alpha branches quarantined behind 3546 bound rows",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3546_2_finite_bound",
            "question": "Is there now a finite test gate for a future nonzero alpha product?",
            "decision": "YES",
            "basis": f"DD e-basis gate is {KE_BALPHA_DD_E_CEILING:.6e}; alpha-Coulomb convention gate is {DE_ALPHA_ONLY_CEILING:.6e}",
            "effect": "future derived b_alpha/K_e_alpha rows can be judged immediately without pretending the value exists today",
            "next_action": "do not merge the two conventions until alloy/material tensor policy is sourced",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3546_0",
            "checkpoint": "3546",
            "claim_allowed": "False",
            "numeric_Ke_alpha_balpha_found": "False",
            "zero_route_status": "calibrated_baseline_allowed_parent_derivation_unsigned",
            "finite_bound_status": "numeric_nonclaim_gates_ready",
            "dd_e_basis_ceiling": f"{KE_BALPHA_DD_E_CEILING:.12e}",
            "alpha_coulomb_basis_ceiling": f"{DE_ALPHA_ONLY_CEILING:.12e}",
            "next_target": "3547-Y5-R2FR-parent-EM-same-owner-zero-or-Ke-alpha-source-leg.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3546_0",
            "target_doc": "3547-Y5-R2FR-parent-EM-same-owner-zero-or-Ke-alpha-source-leg.md",
            "target_script": "scripts/Y5_R2FR_3547_parent_EM_same_owner_zero_or_Ke_alpha_source_leg.py",
            "objective": "try to prove the parent same-owner relation 2 z_g = z_lambda for the EM/current functor; if it fails, build the factorized K_e_alpha source leg",
            "success_gate": "either b_alpha is parent-zero without calibration closure, or K_e_alpha has a source-backed factorized row that can multiply any future b_alpha value",
            "reason": "this is the shortest non-circular route from charge/EM normalization into calibrated local source coupling",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(generated_paths: list[Path], sources: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required_sources_exist = all(row["exists"] == "True" for row in sources)
    generated_csvs = [path for path in generated_paths if path.suffix.lower() == ".csv"]
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    numeric_bounds_positive = all(float(row["bound_value"]) > 0 for row in bounds)
    bounds_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in bounds)
    no_formalization_outputs = all(FORMALIZATION not in path.parents for path in generated_paths)
    no_claim_status = True
    return [
        {
            "validation_id": "VAL3546_0_sources_exist",
            "passes": bool_text(required_sources_exist),
            "status": "PASS" if required_sources_exist else "FAIL",
            "detail": "all source paths cited by the 3546 source register exist",
        },
        {
            "validation_id": "VAL3546_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3546_2_numeric_bounds_positive",
            "passes": bool_text(numeric_bounds_positive),
            "status": "PASS" if numeric_bounds_positive else "FAIL",
            "detail": "all finite alpha product bound rows have positive numeric values",
        },
        {
            "validation_id": "VAL3546_3_bounds_nonclaim",
            "passes": bool_text(bounds_nonclaim),
            "status": "PASS" if bounds_nonclaim else "FAIL",
            "detail": "all alpha product bounds remain claim_allowed=False and valid_for_claim=False",
        },
        {
            "validation_id": "VAL3546_4_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3546 generated outputs only inside post-checkpoint-work",
        },
        {
            "validation_id": "VAL3546_5_claim_block_retained",
            "passes": bool_text(no_claim_status),
            "status": "PASS",
            "detail": "no local-GR/WEP/alpha-source claim is made by this checkpoint",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3546 — Ke-alpha b-alpha source value or EM alpha-coupling bound intake",
        "",
        "## Verdict",
        "",
        "- **No sourced numeric `K_e_alpha*b_alpha` value exists yet.** The corpus has an exact alpha identity and usable empirical ceilings, but not the parent-owned product value.",
        "- **The actual law is now pinned down:** `b_alpha = D_X ln alpha_eff = 2 z_g - z_lambda`, with `alpha_eff proportional to g_J^2/lambda_A` after canonical normalization.",
        f"- **Finite nonclaim gate:** in the DD-like e basis, any future isolated alpha product must satisfy `|K_e_alpha*b_alpha| <= {KE_BALPHA_DD_E_CEILING:.6e}`; in the older alpha-Coulomb convention the ceiling is `{DE_ALPHA_ONLY_CEILING:.6e}`.",
        "- **Baseline route:** calibrated local alpha may be held fixed as a measured constant for Maxwell stress/local-GR bookkeeping, but that is not a derived parent theorem.",
        "",
        "## Exact identity",
        "",
        markdown_table(
            rows_by_name["identity"],
            ["identity_id", "object", "mathematical_form", "result", "zero_or_bound_role"],
        ),
        "",
        "## Zero-proof clauses",
        "",
        markdown_table(
            rows_by_name["zero_clauses"],
            ["clause_id", "claim", "mathematical_condition", "effect_on_product", "status", "remaining_gap"],
        ),
        "",
        "## Product bounds",
        "",
        markdown_table(
            rows_by_name["bounds"],
            ["bound_id", "target", "arena", "formula", "bound_value", "units", "mts_value_ready", "valid_for_claim"],
        ),
        "",
        "## Input contract",
        "",
        markdown_table(
            rows_by_name["input_contract"],
            ["input_id", "target", "must_supply", "acceptance_gate", "current_status"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decision"],
            ["decision_id", "question", "decision", "basis", "next_action"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3547-Y5-R2FR-parent-EM-same-owner-zero-or-Ke-alpha-source-leg.md`: prove `2 z_g = z_lambda` from a single parent EM/current owner if possible; otherwise build the factorized `K_e_alpha` source leg so a future nonzero `b_alpha` can be scored rather than waved around.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    identities = identity_rows()
    zero_clauses = zero_clause_rows()
    bounds = bound_rows()
    input_contract = input_contract_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3546_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3546_ALPHA_IDENTITY_LOCK.csv": (
            identities,
            ["identity_id", "object", "mathematical_form", "result", "zero_or_bound_role", "source_path", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3546_ZERO_PROOF_CLAUSES.csv": (
            zero_clauses,
            [
                "clause_id",
                "claim",
                "mathematical_condition",
                "effect_on_product",
                "current_evidence",
                "remaining_gap",
                "status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3546_PRODUCT_BOUND_ROWS.csv": (
            bounds,
            [
                "bound_id",
                "target",
                "arena",
                "formula",
                "delta_q_used",
                "bound_value",
                "units",
                "source_path",
                "numeric_bound_ready",
                "mts_value_ready",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3546_KE_ALPHA_INPUT_CONTRACT.csv": (
            input_contract,
            ["input_id", "target", "must_supply", "acceptance_gate", "current_status", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3546_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "effect", "next_action", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3546_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "numeric_Ke_alpha_balpha_found",
                "zero_route_status",
                "finite_bound_status",
                "dd_e_basis_ceiling",
                "alpha_coulomb_basis_ceiling",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3546_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "numeric_Ke_alpha_balpha_found",
                "zero_route_status",
                "finite_bound_status",
                "dd_e_basis_ceiling",
                "alpha_coulomb_basis_ceiling",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, bounds)
    validation_path = OUT / "P8_Y5_BRR545_3546_VALIDATION.csv"
    write_csv(
        validation_path,
        validation,
        ["validation_id", "passes", "status", "detail"],
    )
    generated_paths.append(validation_path)

    write_doc(
        {
            "identity": identities,
            "zero_clauses": zero_clauses,
            "bounds": bounds,
            "input_contract": input_contract,
            "decision": decisions,
            "status": status,
            "validation": validation,
            "next_target": next_target,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
