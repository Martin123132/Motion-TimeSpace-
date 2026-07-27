from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1719"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1719 - JH Source Current Norm Or dPiM Domain Operator Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1719_0_1718_doc",
        "source_key": "1718_doc",
        "source_path": ROOT / "1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md",
        "needles": ["NEXT1718_0_primary", "NDB1718_0_domain_numerator_contract"],
    },
    {
        "source_id": "SRC1719_1_1718_validation",
        "source_key": "1718_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1718_VALIDATION.csv",
        "needles": ["VAL1718_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1719_2_1718_numerator_contract",
        "source_key": "1718_numerator_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_ICOMMUTATOR_DOMAIN_NUMERATOR_BOUND_CONTRACT.csv",
        "needles": ["NDB1718_0_domain_numerator_contract", "MISSING_OPERATOR_NORM;MISSING_JH_NORM"],
    },
    {
        "source_id": "SRC1719_3_1718_first_row",
        "source_key": "1718_first_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1718_NDOMAIN_FIRST_NUMERATOR_ROW.csv",
        "needles": ["NDR1718_0_worldtube_support_numerator_bound_candidate", "MISSING_SOURCE_CURRENT_NORM"],
    },
    {
        "source_id": "SRC1719_4_449_doc",
        "source_key": "449_doc",
        "source_path": ROOT / "449-source-current-Ward-universality-theorem-attempt.md",
        "needles": ["conditional_Hilbert_source_current_theorem", "not_parent_derived"],
    },
    {
        "source_id": "SRC1719_5_942_doc",
        "source_key": "942_doc",
        "source_path": ROOT / "942-Y5-R10-parent-worldtube-selector-source-frame-or-CbetaN5-kernel-fill.md",
        "needles": ["J_H[tau] = star(T_obs(tau,.))", "conditional_theorem_built_no_claim"],
    },
    {
        "source_id": "SRC1719_6_943_doc",
        "source_key": "943_doc",
        "source_path": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
        "needles": ["DER943_3_one_Hilbert_current", "conditional definition"],
    },
    {
        "source_id": "SRC1719_7_943_contract",
        "source_key": "943_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "needles": ["CFC943_2_matter_functor", "not_parent_signed"],
    },
    {
        "source_id": "SRC1719_8_941_template",
        "source_key": "941_template",
        "source_path": RESIDUALS / "P8_Y5_R10_941_RESIDUAL_TEMPLATE.csv",
        "needles": ["RWT941_1_worldtube_domain_shift", "MISSING_DOMAIN_SELECTOR_BOUND"],
    },
    {
        "source_id": "SRC1719_9_942_worldtube_rows",
        "source_key": "942_worldtube_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_942_WORLDTUBE_RESIDUAL_ROWS.csv",
        "needles": ["WTR942_0_Delta_worldtube_domain", "MISSING_PARENT_SELECTOR_OR_NUMERIC_BOUND"],
    },
    {
        "source_id": "SRC1719_10_1357_profiles",
        "source_key": "1357_profiles",
        "source_path": RESIDUALS / "P8_Y5_R10_1357_ICOMMUTATOR_SOURCE_PROFILE_ROWS.csv",
        "needles": ["ICP1357_0_fixed_domain_derivative", "RETAINED_NONCLAIM"],
    },
    {
        "source_id": "SRC1719_11_1358_doc",
        "source_key": "1358_doc",
        "source_path": ROOT / "1358-Y5-R10-RAB-PiM-fixed-chainmap-parent-signature-or-Icommutator-first-profile-row.md",
        "needles": ["IFR1358_0_Icommutator_domain_first_profile", "MISSING_INT_A_DPiM_DOMAIN_JH"],
    },
    {
        "source_id": "SRC1719_12_1358_schema",
        "source_key": "1358_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1358_ICOMMUTATOR_FIRST_PROFILE_ROW_SCHEMA.csv",
        "needles": ["IFR1358_0_Icommutator_domain_first_profile", "MISSING_INT_A_DPiM_DOMAIN_JH"],
    },
    {
        "source_id": "SRC1719_13_1359_intake",
        "source_key": "1359_intake",
        "source_path": RESIDUALS / "P8_Y5_R10_1359_ICOMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
        "needles": ["ISI1359_2_numerator", "MISSING_INT_A_DPiM_DOMAIN_JH"],
    },
    {
        "source_id": "SRC1719_14_1360_intake",
        "source_key": "1360_intake",
        "source_path": RESIDUALS / "P8_Y5_R10_1360_MHREF_SURFACE_INTAKE_ROWS.csv",
        "needles": ["MSI1360_6_domain_numerator", "MISSING_INT_A_DPiM_DOMAIN_JH"],
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles_present": yesno(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


JH_NORM_AUDIT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "audit_id": "JHN1719_0_definition",
        "ingredient": "J_H source-current definition",
        "mathematical_form": "J_H[tau]=star(T_obs(tau,.)); T_obs^{mu nu}=2/sqrt(-g_obs) delta S_matter/delta g_obs_munu",
        "source_anchor": "449 W0;942 SEL942_2;943 DER943_3",
        "current_status": "CONDITIONAL_DEFINITION_ONLY",
        "norm_ready": no(),
        "missing": "parent matter functor; observed coframe descent; tau/source normal lock",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "JHN1719_1_Ward_conservation",
        "ingredient": "Ward conservation of Hilbert current",
        "mathematical_form": "nabla_mu T_m^{mu nu}=0 on matter equations if no explicit nonmetric/source arguments",
        "source_anchor": "449 W2;449 Ward_conservation_limit",
        "current_status": "CONDITIONAL_STANDARD_IDENTITY_NOT_MASS_NORM",
        "norm_ready": no(),
        "missing": "zero hidden exchange; absolute calibration; compact support norm",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "JHN1719_2_norm_choice",
        "ingredient": "norm convention for J_H on A_ext",
        "mathematical_form": "||J_H||_A must declare L1/L2/sup/dual-current norm, volume form, tau, frame and units",
        "source_anchor": "1718 NDB1718_0;1359 ISI1359_2;1360 MSI1360_6",
        "current_status": "MISSING_NORM_CONVENTION",
        "norm_ready": no(),
        "missing": "norm type; annulus measure; source current units; source path",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "JHN1719_3_verdict",
        "ingredient": "claim-safe Hilbert source-current norm",
        "mathematical_form": "||J_H||_A is source-backed or theorem-bounded in the same observed coframe and tau",
        "source_anchor": "449;942;943;1718",
        "current_status": "JH_NORM_NOT_SOURCED",
        "norm_ready": no(),
        "missing": "numeric/theorem bound; units; same-frame matter source proof; compact annulus",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


DPIM_OPERATOR_AUDIT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "audit_id": "DPO1719_0_operator_definition",
        "ingredient": "domain derivative of Pi_M",
        "mathematical_form": "(dPi_M)_domain := D_D Pi_M[delta W_M,delta A_ext,delta[S2]_M]",
        "source_anchor": "1718 NDB1718_0;1357 ICP1357_0;1358 IFR1358_0",
        "current_status": "FORMAL_SPLIT_ONLY",
        "operator_ready": no(),
        "missing": "functional derivative of Pi_M with respect to domain/linking data",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "DPO1719_1_zero_route",
        "ingredient": "operator theorem-zero",
        "mathematical_form": "if delta W_M=delta A_ext=delta[S2]_M=0 then D_D Pi_M=0",
        "source_anchor": "1717 CDT1717_1;1718 WST1718_1",
        "current_status": "CONDITIONAL_ONLY",
        "operator_ready": no(),
        "missing": "parent-fixed support and surface homology theorem",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "DPO1719_2_bound_route",
        "ingredient": "operator norm bound",
        "mathematical_form": "||D_D Pi_M||_{A<-H} <= C_DPiM for declared current/domain norm pair",
        "source_anchor": "1187/1191 style operator-bound debts;1718 NDB1718_0",
        "current_status": "MISSING_OPERATOR_NORM",
        "operator_ready": no(),
        "missing": "domain geometry; boundary conditions; regularity; norm pair; source path",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "DPO1719_3_domain_variation_amplitude",
        "ingredient": "domain variation amplitude",
        "mathematical_form": "||delta_D|| = ||(delta W_M,delta A_ext,delta[S2]_M)|| under allowed metric/readout/orbit variations",
        "source_anchor": "941 RWT941_1;942 WTR942_0-WTR942_2;1360 MSI1360_3",
        "current_status": "MISSING_DOMAIN_VARIATION_BOUND",
        "operator_ready": no(),
        "missing": "surface pair; homology certificate; allowed variation class; numeric/theorem bound",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "audit_id": "DPO1719_4_verdict",
        "ingredient": "claim-safe dPiM domain operator factor",
        "mathematical_form": "C_DPiM ||delta_D|| is source-backed or theorem-zero",
        "source_anchor": "1718;1358;1359;1360",
        "current_status": "DPIM_DOMAIN_OPERATOR_NOT_SOURCED",
        "operator_ready": no(),
        "missing": "operator norm or zero theorem; domain variation amplitude; annulus geometry",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


NUMERATOR_FACTOR_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "factor_id": "NF1719_0_factorized_bound",
        "quantity": "N_domain",
        "factorized_formula": "abs(N_domain) <= C_DPiM * ||delta_D|| * ||J_H||_A",
        "factor_C_DPiM": "MISSING_OPERATOR_NORM_OR_ZERO_THEOREM",
        "factor_delta_D": "MISSING_DOMAIN_VARIATION_AMPLITUDE_OR_ZERO_THEOREM",
        "factor_JH_norm": "MISSING_SOURCE_CURRENT_NORM",
        "factor_annulus": "MISSING_ANNULUS_MEASURE_AND_SURFACE_PAIR",
        "units_status": "MISSING_NUMERATOR_UNITS",
        "current_status": "BOUND_FORM_DERIVED_INPUTS_MISSING",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "factor_id": "NF1719_1_zero_route",
        "quantity": "N_domain",
        "factorized_formula": "N_domain=0 if C_DPiM=0 or ||delta_D||=0 on the parent-owned local branch",
        "factor_C_DPiM": "CONDITIONAL_DPiM_ZERO_ONLY",
        "factor_delta_D": "CONDITIONAL_FIXED_DOMAIN_ONLY",
        "factor_JH_norm": "not needed if operator/domain factor theorem-zero",
        "factor_annulus": "still must define source-free exterior annulus",
        "units_status": "not_applicable_if_zero_theorem_signed",
        "current_status": "ZERO_ROUTE_NOT_PARENT_SIGNED",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


FIRST_INGREDIENT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "ING1719_0_JH_norm_candidate",
        "ingredient": "J_H_norm",
        "definition": "norm of observed Hilbert source current on A_ext",
        "formula": "||J_H||_A = norm_A[star(T_obs(tau,.))]",
        "required_fields": "system_id;A_ext;norm_type;volume_form;e_obs_id;tau_id;T_obs_source;J_H_norm;units;source_path;equation_ref;valid_for_claim",
        "current_value": "MISSING_SOURCE_CURRENT_NORM",
        "source_path": ";".join(
            str(item["source_path"])
            for item in SOURCES
            if item["source_key"] in {"449_doc", "942_doc", "943_doc", "943_contract"}
        ),
        "equation_ref": "449 W0/W2/W4;942 SEL942_2;943 DER943_3;CFC943_2",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "row_id": "ING1719_1_DPiM_operator_norm_candidate",
        "ingredient": "C_DPiM",
        "definition": "operator norm of domain/linking-surface derivative of Pi_M",
        "formula": "C_DPiM = ||D_D Pi_M||_{A<-H}",
        "required_fields": "system_id;Pi_M_definition;domain_rule;surface_pair;norm_pair;boundary_conditions;regularity_class;C_DPiM;units;source_path;equation_ref;valid_for_claim",
        "current_value": "MISSING_OPERATOR_NORM_OR_PARENT_ZERO",
        "source_path": ";".join(
            str(item["source_path"])
            for item in SOURCES
            if item["source_key"] in {"1718_numerator_contract", "1357_profiles", "1358_doc", "1358_schema", "1359_intake"}
        ),
        "equation_ref": "1718 NDB1718_0;1357 ICP1357_0;1358 IFR1358_0;1359 ISI1359_2",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "row_id": "ING1719_2_delta_D_candidate",
        "ingredient": "delta_D",
        "definition": "allowed source-support/exterior/linking-surface variation amplitude",
        "formula": "||delta_D|| = ||(delta W_M,delta A_ext,delta[S2]_M)||",
        "required_fields": "system_id;W_rule;S1;S2;homology_class;allowed_variations;delta_D;units;source_path;equation_ref;valid_for_claim",
        "current_value": "MISSING_DOMAIN_VARIATION_AMPLITUDE_OR_ZERO_THEOREM",
        "source_path": ";".join(
            str(item["source_path"])
            for item in SOURCES
            if item["source_key"] in {"941_template", "942_worldtube_rows", "1360_intake"}
        ),
        "equation_ref": "941 RWT941_1;942 WTR942_0-WTR942_2;1360 MSI1360_3",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1719_0_JH_norm",
        "quantity": "Hilbert source-current norm",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_NORM_TYPE;MISSING_SOURCE_CURRENT_VALUE;MISSING_UNITS;MISSING_PARENT_MATTER_FUNCTOR;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1719_1_DPiM_operator_norm",
        "quantity": "domain derivative operator norm",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_PIM_DOMAIN_DERIVATIVE;MISSING_NORM_PAIR;MISSING_BOUNDARY_CONDITIONS;MISSING_NUMERIC_OPERATOR_NORM;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1719_2_N_domain_bound",
        "quantity": "factorized N_domain bound",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "JH_NORM_MISSING;DPIM_OPERATOR_NORM_MISSING;DELTA_D_MISSING;ANNULUS_MEASURE_MISSING",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1719_3_Newton_GR",
        "quantity": "Newton/local-GR source-normalization reopening",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "N_DOMAIN_UNBOUNDED;M_H_REF_MISSING;R_EQ_MISSING;PPN_VECTOR_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1719_0_primary",
        "next_target": "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
        "script": "scripts/Y5_R2FR_observed_Hilbert_current_norm_source_row_or_matter_functor_signature.py",
        "objective": "try to parent-sign the observed matter functor/coframe/tau definition that makes J_H real; if not, fill the first Hilbert-current norm source row as nonclaim",
        "selection_status": "selected",
        "success_condition": "either J_H norm is theorem-owned/source-backed, or a complete nonclaim source row names norm type, units, frame, tau and source paths",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1719_1_parallel_operator",
        "next_target": "1720b-Y5-R2FR-dPiM-domain-operator-norm-or-fixed-domain-zero-theorem.md",
        "script": "scripts/Y5_R2FR_dPiM_domain_operator_norm_or_fixed_domain_zero_theorem.py",
        "objective": "parallel route for the domain-operator norm or fixed-domain zero theorem",
        "selection_status": "held_parallel",
        "success_condition": "C_DPiM theorem-zero/source-backed or explicit blocker row",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1719_0_JH_norm",
        "claim": "Hilbert source-current norm is source-backed or theorem-bounded",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "observed matter functor, norm convention, units and source-current value are missing",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1719_1_DPiM_operator",
        "claim": "domain derivative operator norm is sourced or theorem-zero",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "domain derivative, norm pair, boundary conditions and fixed-domain theorem are unsigned",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1719_2_N_domain",
        "claim": "N_domain has a finite source-backed bound",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "J_H norm, C_DPiM, delta_D and annulus measure remain missing",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1719_3_Newton_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "N_domain, M_H_ref, R_eq, Pi_M_H and PPN residual vector remain open",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_SOURCE_REGISTER.csv",
    "jh_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_JH_SOURCE_CURRENT_NORM_AUDIT.csv",
    "dpim_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_DPIM_DOMAIN_OPERATOR_AUDIT.csv",
    "factor_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NDOMAIN_FACTOR_BOUND_CONTRACT.csv",
    "ingredient_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_RUNNER_REFUSAL.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1719_VALIDATION.csv",
}


COPY_MAP = {
    "jh_audit": "R2FR_JH_source_current_norm_audit_1719.csv",
    "dpim_audit": "R2FR_DPiM_domain_operator_audit_1719.csv",
    "factor_bound": "R2FR_Ndomain_factor_bound_contract_1719.csv",
    "ingredient_rows": "R2FR_numerator_ingredient_source_rows_1719.csv",
    "runner_refusal": "R2FR_runner_refusal_1719.csv",
    "next_target": "R2FR_next_target_1719.csv",
    "claim_gate": "R2FR_claim_gate_1719.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "jh_audit": JH_NORM_AUDIT_ROWS,
        "dpim_audit": DPIM_OPERATOR_AUDIT_ROWS,
        "factor_bound": NUMERATOR_FACTOR_ROWS,
        "ingredient_rows": FIRST_INGREDIENT_ROWS,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "next_target": NEXT_TARGET_ROWS,
        "claim_gate": CLAIM_GATE_ROWS,
    }


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1719_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1719_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "norm_ready", "operator_ready"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def ingredient_source_paths_exist() -> bool:
    for row in FIRST_INGREDIENT_ROWS:
        paths = [Path(item) for item in row["source_path"].split(";") if item]
        if not paths or any(not path.exists() for path in paths):
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1719_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1719_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1719*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_rows = rows_map["source_register"]
    jh_rows = rows_map["jh_audit"]
    dpim_rows = rows_map["dpim_audit"]
    factor_rows = rows_map["factor_bound"]
    ingredient_rows = rows_map["ingredient_rows"]
    runner_rows = rows_map["runner_refusal"]
    claim_rows = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]
    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1719_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1719_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1719_2_JH_norm_not_sourced",
            any(row["audit_id"] == "JHN1719_3_verdict" and row["current_status"] == "JH_NORM_NOT_SOURCED" for row in jh_rows),
            "Hilbert source-current norm remains unsourced",
            "JH norm verdict missing or promoted",
        ),
        check(
            "VAL1719_3_DPiM_operator_not_sourced",
            any(row["audit_id"] == "DPO1719_4_verdict" and row["current_status"] == "DPIM_DOMAIN_OPERATOR_NOT_SOURCED" for row in dpim_rows),
            "dPiM domain operator factor remains unsourced",
            "dPiM operator verdict missing or promoted",
        ),
        check(
            "VAL1719_4_factor_bound_present",
            any(row["factor_id"] == "NF1719_0_factorized_bound" and row["current_status"] == "BOUND_FORM_DERIVED_INPUTS_MISSING" for row in factor_rows),
            "factorized N_domain bound is present with missing inputs",
            "factorized N_domain bound missing or score-ready",
        ),
        check(
            "VAL1719_5_ingredient_rows_nonclaim",
            len(ingredient_rows) == 3 and all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in ingredient_rows),
            "three numerator ingredient rows exist and remain nonclaim",
            "ingredient rows missing or claim-enabled",
        ),
        check(
            "VAL1719_6_ingredient_source_paths_exist",
            ingredient_source_paths_exist(),
            "all source paths listed in ingredient rows exist",
            "one or more source paths listed in ingredient rows missing",
        ),
        check(
            "VAL1719_7_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses JH norm, dPiM norm, N_domain and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1719_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check(
            "VAL1719_9_next_selected",
            any(row["route_id"] == "NEXT1719_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects observed Hilbert current norm or matter-functor signature",
            "next target missing selected primary route",
        ),
        check("VAL1719_10_csv_parse", parsed_ok, "all generated 1719 CSVs parse", "one or more generated 1719 CSVs failed to parse"),
        check("VAL1719_11_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1719_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1719_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1719_14_formalization_untouched", formalization_untouched(), "no 1719 outputs found under formalization-workbench", "1719 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1719_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1719 JH source-current norm and dPiM domain-operator validation" if overall else "one or more 1719 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1719 tries to make the `N_domain` numerator calculable rather than symbolic.",
        "- The Hilbert current definition is available conditionally, but `||J_H||_A` is not source-backed because the observed matter functor, coframe descent, tau/source lock, norm convention, units, and compact annulus are unsigned.",
        "- The domain-operator side is also not source-backed: `(dPi_M)_domain` has a clean zero route if the domain is fixed, but current MTS lacks the fixed-domain theorem and lacks an operator norm.",
        "- The useful output is the factorized nonclaim bound `abs(N_domain) <= C_DPiM ||delta_D|| ||J_H||_A`, with each missing ingredient split into its own source row.",
        "- No Newton, local-GR, R10, PPN, clock, orbital, source-normalization or `q_loc`-zero claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## JH Source-Current Norm Audit",
        markdown_table(rows_map["jh_audit"], ["audit_id", "ingredient", "mathematical_form", "current_status", "norm_ready", "missing"]),
        "",
        "## dPiM Domain Operator Audit",
        markdown_table(rows_map["dpim_audit"], ["audit_id", "ingredient", "mathematical_form", "current_status", "operator_ready", "missing"]),
        "",
        "## N_domain Factor Bound",
        markdown_table(rows_map["factor_bound"], ["factor_id", "quantity", "factorized_formula", "factor_C_DPiM", "factor_delta_D", "factor_JH_norm", "current_status", "score_ready"]),
        "",
        "## Numerator Ingredient Rows",
        markdown_table(rows_map["ingredient_rows"], ["row_id", "ingredient", "formula", "current_value", "equation_ref", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1719 does not close the local-GR route, but it prevents a hidden normalization cheat. The numerator is now split into exactly three source debts: `J_H` norm, `dPiM` domain-operator norm, and domain-variation amplitude. The best next derivation route is the observed Hilbert-current side, because if the matter functor/coframe/tau owner is signed it also helps worldtube support, source measure, WEP, clocks, and Newton normalization.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1719-Y5-R2FR-JH-source-current-norm-or-dPiM-domain-operator-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1719_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1719 validation FAIL")
    print("1719 validation PASS")


if __name__ == "__main__":
    main()
