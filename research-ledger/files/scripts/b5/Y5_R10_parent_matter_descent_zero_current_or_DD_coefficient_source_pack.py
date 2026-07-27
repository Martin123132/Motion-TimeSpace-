from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1087-parent-matter-descent-or-DD-coefficient-pack" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1087_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1087_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
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


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


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


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1087_0_1086_next", "source-intake/mts_residuals/P8_Y5_R10_1086_NEXT_TARGET.csv", "1087-Y5-R10-parent-matter-descent-zero-current-or-DD-coefficient-source-pack.md", "1086 handoff."),
        ("SRC1087_1_1086_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1086_VALIDATION.csv", "V1086_SUMMARY", "1086 validation summary."),
        ("SRC1087_2_1086_source_current", "source-intake/mts_residuals/P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv", "SCZ1086_5_verdict", "source-current zero failed current claim."),
        ("SRC1087_3_1086_parent_DD", "source-intake/mts_residuals/P8_Y5_R10_1086_DD_PARENT_MAP_FIRST_ROW_ATTEMPT.csv", "PDM1086_4_verdict", "parent-to-DD first row missing."),
        ("SRC1087_4_1086_pressure", "source-intake/mts_residuals/P8_Y5_R10_1086_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv", "CPR1086_2_equal_two_component_bulk_Earth", "coefficient pressure rows."),
        ("SRC1087_5_1086_no_cancel", "source-intake/mts_residuals/P8_Y5_R10_1086_NO_CANCELLATION_GUARD.csv", "NCG1086_0_no_pair_tuning", "no-cancellation policy."),
        ("SRC1087_6_618_source_zero", "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv", "SZ618_0_qbar_XT_chain_rule", "conditional source-zero route."),
        ("SRC1087_7_1045_matter_functor", "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_6_verdict", "parent matter functor not signed."),
        ("SRC1087_8_1045_lift", "source-intake/mts_residuals/P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv", "VLG1045_4_verdict", "vertical lift descent gate."),
        ("SRC1087_9_1078_object", "source-intake/mts_residuals/P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv", "OL1078_4_verdict", "object-language not signed."),
        ("SRC1087_10_1078_measure", "source-intake/mts_residuals/P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv", "AM1078_4_verdict", "action-measure not signed."),
        ("SRC1087_11_1078_current", "source-intake/mts_residuals/P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv", "CO1078_4_verdict", "current-owner not fully signed."),
        ("SRC1087_12_1079_premise", "source-intake/mts_residuals/P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv", "PR1079_4_no_pre_action_species_weight", "pre-action species weight leak."),
        ("SRC1087_13_1081_DD_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv", "DDB1081_0_alpha_Coulomb", "external DD basis."),
        ("SRC1087_14_1082_units", "source-intake/mts_residuals/P8_Y5_R10_1082_COEFFICIENT_UNITS_CONTRACT.csv", "CUC1082_3_C_parent", "coefficient unit contract."),
        ("SRC1087_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_matter_descent_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "descent_id": "PMD1087_0_target",
            "needed_clause": "S_matter descends through observed quotient data",
            "mathematical_statement": "S_matter[Psi_A,e_obs,omega_obs,theta_A] with e_obs=Obs_e(q(Phi)), Dq[v_X]=0, and no X-dependent hidden marker",
            "current_evidence": "MFS1045_0 through MFS1045_6 define the signature but end FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "result": "TARGET_SHARPENED_NOT_SIGNED",
            "missing_for_claim": "single parent action signature for q, e_obs, omega, Psi_A, theta_A, and no shadow frame",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "descent_id": "PMD1087_1_geometry_chain_rule",
            "needed_clause": "visible geometry is quotient-owned",
            "mathematical_statement": "Lie_vX e_obs = D Obs_e[Dq(v_X)] = 0 and hence Lie_vX g_obs=0",
            "current_evidence": "QG1045_1 gives exact conditional sublemma, but MFS1045_1 remains SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "result": "CONDITIONAL_SUBLEMMA_ONLY",
            "missing_for_claim": "parent-derived observed quotient/coframe functor and independent-connection silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "descent_id": "PMD1087_2_matter_lift",
            "needed_clause": "vertical lift on ordinary matter is fixed/gauge, not physical",
            "mathematical_statement": "delta_v Psi_A=0 or an owned gauge/local Lorentz/diffeomorphism lift with boundary-only variation",
            "current_evidence": "VLG1045_0/VLG1045_1 are clean options, but VLG1045_4 verdict fails",
            "result": "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent map assigning v_X to every ordinary matter species and boundary class",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "descent_id": "PMD1087_3_material_constants",
            "needed_clause": "Lie_vX theta_A=0 for ordinary masses, charges, clocks, and representation constants",
            "mathematical_statement": "theta_A are fixed representation/superselection data or explicit retained residual fields",
            "current_evidence": "MFS1045_5 and PS613_3 keep constant/superselection route unsigned",
            "result": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "missing_for_claim": "parent superselection theorem for material constants or explicit residual coefficient rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "descent_id": "PMD1087_4_pre_action_weights",
            "needed_clause": "no species/material weight w_A multiplies S_A before variation",
            "mathematical_statement": "S_matter cannot contain independent inert weights w_A S_A not carried by a field/current/representation",
            "current_evidence": "OL1078_4 and AM1078_4 do not sign object-language/action-measure exclusion; PR1079_4 is NOT_SIGNED",
            "result": "PRE_ACTION_WEIGHT_LEAK_SURVIVES",
            "missing_for_claim": "object-language or action-measure parent clause forbidding independent source-only weights",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "descent_id": "PMD1087_5_hidden_domain_boundary",
            "needed_clause": "hidden/source/domain and boundary terms are silent or separately bounded",
            "mathematical_statement": "no shadow frame, support shift, edge charge, or domain marker contributes to delta_X S_matter",
            "current_evidence": "MFS1045_4, VLG1045_3, and SZ618_1/SZ618_2 retain boundary/no-pole blockers",
            "result": "HIDDEN_DOMAIN_TERMS_NOT_CLOSED",
            "missing_for_claim": "no-shadow frame theorem, boundary charge silence, no physical X pole or explicit bounded rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "descent_id": "PMD1087_6_verdict",
            "needed_clause": "qbar_XT=0 parent matter descent theorem",
            "mathematical_statement": "all clauses PMD1087_0 through PMD1087_5 close from one parent action",
            "current_evidence": "each strong clause exists as a contract/sublemma, but at least one counterexample survives in every route",
            "result": "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED",
            "missing_for_claim": "parent object-language/action-measure/current-owner/matter-functor signature in one action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def zero_current_clause_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "ZCC1087_0_object_language",
            "future_parent_contract": "ordinary matter action arguments are only observed quotient geometry, owned matter fields, representation data, gauge connections, and universal constants",
            "would_kill": "source-only inert species weights and material markers",
            "current_status": "OBJECT_LANGUAGE_NOT_SIGNED",
            "source_row": "OL1078_4_verdict",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZCC1087_1_action_measure",
            "future_parent_contract": "one parent action measure/hbar normalization for ordinary matter sectors before readout",
            "would_kill": "relative action multipliers w_A that only appear through active source strength",
            "current_status": "ACTION_MEASURE_NOT_SIGNED",
            "source_row": "AM1078_4_verdict",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZCC1087_2_variation_order",
            "future_parent_contract": "Hilbert/current extraction occurs before material/readout projection",
            "would_kill": "post-variation material selector redefinitions",
            "current_status": "CONDITIONAL_SUBTHEOREM_ONLY",
            "source_row": "NCO1079_3_post_variation_selector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZCC1087_3_matter_functor",
            "future_parent_contract": "Psi_A lives in a parent matter bundle functor over observed quotient geometry with fixed/gauge vertical lift",
            "would_kill": "physical material lift along v_X",
            "current_status": "PARENT_MATTER_FUNCTOR_NOT_SIGNED",
            "source_row": "MFS1045_6_verdict",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "ZCC1087_4_constant_superselection",
            "future_parent_contract": "ordinary matter constants theta_A are X-trivial representation/superselection data unless retained as explicit residual fields",
            "would_kill": "alpha/mass/clock source-current leaks",
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "source_row": "MFS1045_5_constants_split",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_coefficient_source_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "pack_id": "DDSP1087_0_c_alpha",
            "coefficient": "c_alpha",
            "definition": "dimensionless coefficient multiplying Q_alpha_Coulomb after parent normalization",
            "required_source": "parent EM/fine-structure derivative N_X * partial_X ln alpha_EM with units/signs",
            "current_status": "MISSING_PARENT_EM_DERIVATIVE",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "DDSP1087_1_c_surface",
            "coefficient": "c_surface",
            "definition": "dimensionless coefficient multiplying Q_surface_binding after parent normalization",
            "required_source": "parent nuclear/surface/binding derivative N_X * partial_X ln a_surface_or_binding with units/signs",
            "current_status": "MISSING_PARENT_BINDING_DERIVATIVE",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "DDSP1087_2_q_tail",
            "coefficient": "q_tail(A)",
            "definition": "absolute envelope for material composition response not spanned by alpha/surface DD rows",
            "required_source": "parent material basis completeness proof or source-backed residual envelope over tested materials",
            "current_status": "MISSING_TAIL_BASIS_AND_ENVELOPE",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_SOURCE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "DDSP1087_3_same_branch_normalization",
            "coefficient": "N_X/K_X/lambda_X lock",
            "definition": "one normalization connecting Z_X, M_X^2, lambda_X, K_X, source profile, and DD coefficients",
            "required_source": "same parent branch range and Green-function normalization",
            "current_status": "MISSING_SAME_BRANCH_NORMALIZATION",
            "source_path": "P8_Y5_R10_1085_RANGE_ACQUISITION_SCHEMA.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "DDSP1087_4_readout_source_profile",
            "coefficient": "K_MICROSCOPE * Q_source_eff(lambda)",
            "definition": "source/readout leg needed before DD coefficients can become an eta prediction",
            "required_source": "PREM/profile lambda owner and official MICROSCOPE arrays",
            "current_status": "MISSING_PROFILE_READOUT",
            "source_path": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_template_rows() -> list[dict[str, str]]:
    return [
        {
            "template_id": "DDCOEFF1087_0_alpha",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "c_alpha",
            "value": "MISSING_PARENT_EM_DERIVATIVE",
            "units": "dimensionless_in_DD_convention_after_N_X",
            "sign": "MISSING",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
            "notes": "do not fill from smoke-fit or cancellation line",
        },
        {
            "template_id": "DDCOEFF1087_1_surface",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "c_surface",
            "value": "MISSING_PARENT_BINDING_DERIVATIVE",
            "units": "dimensionless_in_DD_convention_after_N_X",
            "sign": "MISSING",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
            "notes": "do not fill from smoke-fit or cancellation line",
        },
        {
            "template_id": "DDCOEFF1087_2_tail",
            "branch_id": "MTS_WEP_finite_branch",
            "coefficient": "q_tail_envelope",
            "value": "MISSING_MATERIAL_BASIS_ENVELOPE",
            "units": "dimensionless_charge_envelope",
            "sign": "absolute_envelope",
            "source_path": "MISSING_PARENT_OR_EMPIRICAL_SOURCE",
            "valid_for_claim": "false",
            "notes": "required because two DD rows are not a complete material basis",
        },
    ]


def all_material_no_cancellation_rows() -> list[dict[str, str]]:
    return [
        {
            "policy_id": "AMC1087_0_pair_line_forbidden",
            "forbidden_move": "use the TA6V-PtRh10 cancellation line as a theory result",
            "why_forbidden": "one-pair cancellation is not invariant under changing material pair",
            "acceptable_replacement": "derive coefficient vector from parent action or prove coefficient vector zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "AMC1087_1_basis_completeness",
            "forbidden_move": "score only c_alpha and c_surface as if they span all ordinary matter response",
            "why_forbidden": "DD alpha/surface rows are useful dominant channels but not a parent-complete basis here",
            "acceptable_replacement": "tail envelope q_tail(A) with material coverage statement",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "AMC1087_2_same_branch_requirement",
            "forbidden_move": "combine coefficient from one branch with lambda/profile/readout from another",
            "why_forbidden": "it would make range and amplitude independently tuneable",
            "acceptable_replacement": "one branch supplies Z_X, M_X^2, N_X, c_alpha, c_surface, K_X, Q_source_eff, and readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def pressure_summary_rows() -> list[dict[str, str]]:
    input_rows = read_csv(OUT / "P8_Y5_R10_1086_NONCLAIM_COEFFICIENT_PRESSURE_ROWS.csv")
    rows: list[dict[str, str]] = []
    for row in input_rows:
        rows.append(
            {
                "pressure_id": row["pressure_id"].replace("CPR1086", "CPS1087"),
                "component": row["component"],
                "required_abs_coefficient_max": row["required_abs_coefficient_max"],
                "meaning": "if the coefficient is real and in this nonclaim bulk/readout convention, it must be below this scale",
                "claim_blocker": row["claim_blocker"],
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1087_0_matter_descent_or_coefficients_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_MATTER_DESCENT_ZERO_OR_DD_COEFFICIENT_SOURCE_PACK",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
            "inputs_present": "conditional descent clauses; DD coefficient source-pack schema; nonclaim pressure rows; MICROSCOPE bound",
            "required_inputs": "parent-signed matter descent zero or real c_alpha/c_surface/q_tail pack with same-branch range/profile/readout",
            "derivation_status": "MATTER_DESCENT_NOT_SIGNED_COEFFICIENT_PACK_EMPTY",
            "valid_for_claim": "false",
            "notes": "runner must refuse; 1087 writes the exact parent contract and source-pack placeholders only",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1087_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.15e}",
            "bound_units": "dimensionless",
            "bound_source": "https://arxiv.org/abs/2209.15487",
            "source_row": "MICROSCOPE_final_TiPt_source_charge_proxy:R1_WEP_source_charge;doi:10.1103/PhysRevLett.129.121102",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; MTS prediction remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1087_0_matter_descent_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "passed_rows": str(product_status.get("passed_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing parent matter descent zero and empty DD coefficient pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1087_0_matter_descent",
            "claim_component": "qbar_XT=0 parent matter descent",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PMD1087_6_verdict=PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1087_1_coefficient_pack",
            "claim_component": "DD coefficient source pack",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "c_alpha, c_surface, q_tail, same-branch normalization, and readout are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1087_2_no_cancellation",
            "claim_component": "all-material no-cancellation policy",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "policy written, but it blocks rather than permits a WEP claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1087_3_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DECISION1087_0",
            "decision": "matter descent remains the cleanest theorem route but is not signed",
            "because": "geometry chain rule exists, yet matter lift, constants, pre-action weights, and hidden/domain terms are not owned by one parent action",
            "next_action": "try to write the minimal parent ordinary-matter signature clause, or demote to finite coefficient intake",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DECISION1087_1",
            "decision": "DD coefficient source-pack is ready but empty",
            "because": "the exact columns and no-cancellation policy are now explicit, but no parent coefficient source exists",
            "next_action": "attack the parent ordinary-matter action signature before filling phenomenological coefficients",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1087_0_1088",
            "next_target": "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
            "objective": "attempt the minimal parent ordinary-matter signature clause that would sign object-language, action-measure, matter functor, constant superselection, and variation order together; if it cannot be derived, open finite DD coefficient intake as explicitly phenomenological",
            "include": "single parent action clause; no species weights; matter bundle over observed quotient; theta_A superselection; variation-before-readout; finite coefficient intake fallback",
            "exclude": "post-hoc coefficient fitting; pair cancellation; unit source proxy; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    descent_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    source_pack_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    cancellation_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1087_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1087_1_matter_descent_attempt_complete", any(row["descent_id"] == "PMD1087_6_verdict" and row["result"] == "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED" for row in descent_rows), "parent matter descent attempt ends in explicit nonclaim verdict"))
    checks.append(("V1087_2_zero_clause_contract_complete", len(clause_rows) == 5 and all(row["valid_for_claim"] == "false" for row in clause_rows), "zero-current parent clause contract is explicit"))
    checks.append(("V1087_3_source_pack_empty_nonclaim", len(source_pack_rows) == 5 and all("MISSING" in row["current_status"] or "MISSING" in row["source_path"] for row in source_pack_rows), "DD coefficient source-pack remains empty and nonclaim"))
    checks.append(("V1087_4_template_placeholders", len(template_rows) == 3 and all(row["valid_for_claim"] == "false" and "MISSING" in row["value"] for row in template_rows), "coefficient intake template contains only missing placeholders"))
    checks.append(("V1087_5_no_cancellation_policy", len(cancellation_rows) == 3 and all(row["valid_for_claim"] == "false" for row in cancellation_rows), "all-material no-cancellation policy is present"))
    checks.append(("V1087_6_pressure_summary_numeric", len(pressure_rows) == 3 and all(parse_float(row["required_abs_coefficient_max"]) is not None for row in pressure_rows), "coefficient pressure summary rows are numeric"))
    checks.append(("V1087_7_prediction_missing_nonclaim", any("MISSING_PARENT_MATTER_DESCENT_ZERO" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "generic prediction row remains missing descent/coefficient inputs"))
    checks.append(("V1087_8_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1087_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1087_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1087_11_next_target", any(row["next_target"].startswith("1088-Y5-R10-minimal-parent") for row in next_rows), "1088 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1087_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1087_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1087 CSV outputs parse cleanly"))
    checks.append(("V1087_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1087_SUMMARY", True, "parent matter descent zero not signed; DD coefficient source-pack contract written but empty; no WEP claim allowed"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    descent_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    source_pack_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    cancellation_rows: list[dict[str, str]],
    pressure_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1087-Y5-R10 parent matter descent zero-current or DD coefficient source-pack",
            "",
            "## Current verdict",
            "1087 tries the clean theorem route again and still cannot sign it. The chain-rule geometry part is solid as a conditional sublemma, but qbar_XT=0 needs one parent ordinary-matter signature to own the matter lift, material constants, no species weights, no shadow/source/domain terms, and variation-before-readout. Since that parent signature is not in the corpus, the finite branch stays alive. The fallback DD coefficient source-pack is now exact, but empty and explicitly nonclaim.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Parent matter descent attempt",
            md_table(descent_rows, ["descent_id", "needed_clause", "mathematical_statement", "result", "missing_for_claim"]),
            "## Zero-current clause contract",
            md_table(clause_rows, ["clause_id", "future_parent_contract", "would_kill", "current_status", "source_row"]),
            "## DD coefficient source-pack",
            md_table(source_pack_rows, ["pack_id", "coefficient", "definition", "current_status", "source_path"]),
            "## Coefficient intake template",
            md_table(template_rows, ["template_id", "coefficient", "value", "units", "source_path", "notes"]),
            "## All-material no-cancellation policy",
            md_table(cancellation_rows, ["policy_id", "forbidden_move", "why_forbidden", "acceptable_replacement"]),
            "## Coefficient pressure summary",
            md_table(pressure_rows, ["pressure_id", "component", "required_abs_coefficient_max", "claim_blocker"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    descent_rows = parent_matter_descent_attempt_rows()
    clause_rows = zero_current_clause_contract_rows()
    source_pack_rows = dd_coefficient_source_pack_rows()
    template_rows = dd_template_rows()
    cancellation_rows = all_material_no_cancellation_rows()
    pressure_rows = pressure_summary_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1087_SOURCE_REGISTER.csv",
        "descent_attempt": OUT / "P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
        "zero_clause_contract": OUT / "P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv",
        "source_pack": OUT / "P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK.csv",
        "coefficient_template": OUT / "P8_Y5_R10_1087_DD_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
        "no_cancellation": OUT / "P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv",
        "pressure_summary": OUT / "P8_Y5_R10_1087_COEFFICIENT_PRESSURE_SUMMARY.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1087_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1087_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1087_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1087_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1087_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1087_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["descent_attempt"], descent_rows)
    write_csv(outputs["zero_clause_contract"], clause_rows)
    write_csv(outputs["source_pack"], source_pack_rows)
    write_csv(outputs["coefficient_template"], template_rows)
    write_csv(outputs["no_cancellation"], cancellation_rows)
    write_csv(outputs["pressure_summary"], pressure_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        descent_rows,
        clause_rows,
        source_pack_rows,
        template_rows,
        cancellation_rows,
        pressure_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        descent_rows,
        clause_rows,
        source_pack_rows,
        template_rows,
        cancellation_rows,
        pressure_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
