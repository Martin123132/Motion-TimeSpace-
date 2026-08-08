from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3529-Y5-R2FR-calibrated-alpha-to-local-GR-source-coupling-interface.md"
CANONICAL_STATUS = OUT / "P8_local_GR_calibrated_alpha_source_interface_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3529": {"path": Path(__file__).resolve(), "role": "3529 generator"},
    "doc_3528": {
        "path": ROOT / "3528-Y5-R2FR-unique-F2-parent-domain-inheritance-or-calibrated-alpha-constant-contract.md",
        "role": "calibrated alpha contract",
    },
    "next_3528": {
        "path": OUT / "P8_Y5_R2FR_3528_NEXT_TARGET.csv",
        "role": "3528-selected source-coupling interface target",
    },
    "status_3528": {
        "path": OUT / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
        "role": "3528 canonical alpha status",
    },
    "contract_3528": {
        "path": OUT / "P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv",
        "role": "calibrated alpha contract rows",
    },
    "composite_3524": {
        "path": OUT / "P8_Y5_R2FR_3524_COMPOSITE_THEOREMS.csv",
        "role": "shared owner theorem for local source coupling",
    },
    "kernel_req_3524": {
        "path": OUT / "P8_Y5_R2FR_3524_KERNEL_VALUE_REQUIREMENTS.csv",
        "role": "local kernel value requirements",
    },
    "em_owner_3503": {
        "path": OUT / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
        "role": "observed Hodge, Maxwell stress and total Hilbert current theorem",
    },
    "hilbert_gate_3503": {
        "path": OUT / "P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv",
        "role": "total Hilbert current closure gates",
    },
    "hodge_3504": {
        "path": OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
        "role": "Hodge uniqueness and conformal caveat",
    },
    "local_gr_2633": {
        "path": OUT / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "role": "conditional local GR/Newton theorem",
    },
    "normal_gate_2633": {
        "path": OUT / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PARENT_NORMAL_FORM_GATE.csv",
        "role": "parent normal form gate for local GR",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bounds for WEP, clocks, PPN, Gdot and R10",
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


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


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


def interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "SCI3529_0_calibrated_alpha",
            "piece": "alpha_EM baseline",
            "type": "CALIBRATED_CONSTANT",
            "mathematical_form": "alpha_EM=alpha_0; C_XF2=0 by calibration unless a nonzero branch is proposed",
            "role_in_source_coupling": "fixes local Maxwell normalization without claiming a derived alpha theorem",
            "remaining_gap": "nonzero alpha drift/source branches still need WEP/clock/R10 bounds",
            "source_path": str(SOURCES["contract_3528"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "interface_id": "SCI3529_1_calibrated_Maxwell_stress",
            "piece": "EM Hilbert stress",
            "type": "DERIVED_IDENTITY_GIVEN_CALIBRATED_ACTION",
            "mathematical_form": "T_EM^{mu nu}=lambda_0(F^{mu a}F^nu_a - 1/4 g_obs^{mu nu}F^2) plus only explicitly retained residual terms",
            "role_in_source_coupling": "places Poynting and EM binding energy inside the Hilbert source rather than as a separate force",
            "remaining_gap": "requires observed Hodge/coframe, same current owner and no readout backreaction",
            "source_path": str(SOURCES["em_owner_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "interface_id": "SCI3529_2_total_Hilbert_current",
            "piece": "matter plus EM source",
            "type": "DERIVED_CONDITIONAL_IDENTITY",
            "mathematical_form": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda; nabla_mu T_total^{mu nu}=0",
            "role_in_source_coupling": "internal Lorentz exchange cancels only in total Hilbert stress",
            "remaining_gap": "J_Q/source current and projector closure remain unsigned",
            "source_path": str(SOURCES["hilbert_gate_3503"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "interface_id": "SCI3529_3_kappa_G_calibration",
            "piece": "gravitational coupling",
            "type": "CALIBRATED_CONSTANT_OR_PARENT_OWNER",
            "mathematical_form": "kappa_0=8*pi*G_N/c^4 in the local effective branch unless a parent kappa owner is later derived",
            "role_in_source_coupling": "sets the overall Newtonian source strength after calibration",
            "remaining_gap": "MTS kappa/G_N source normalization and no fitted-GM transfer still need gates",
            "source_path": str(SOURCES["local_gr_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "interface_id": "SCI3529_4_local_field_equation",
            "piece": "local GR equation target",
            "type": "EXACT_CONDITIONAL_NOT_CLAIMED",
            "mathematical_form": "G_mn+Lambda g_mn = kappa_0(T_matter+T_EM)_mn + DeltaE_res_mn",
            "role_in_source_coupling": "separates the GR target from residual operators and source-normalization leaks",
            "remaining_gap": "DeltaE_res, source normalization, no-shadow coframe and PPN vector must be zero or bounded",
            "source_path": str(SOURCES["local_gr_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "interface_id": "SCI3529_5_Newtonian_limit",
            "piece": "Newton/Poisson readout",
            "type": "EXACT_CONDITIONAL_NOT_CLAIMED",
            "mathematical_form": "nabla^2 U = 4*pi*G_N*rho_H + residual_source_terms",
            "role_in_source_coupling": "defines the route by which GR reduces to Newton inside the MTS branch",
            "remaining_gap": "source denominator, M_H_ref, boundary class and PPN/Newton residual vector still missing values",
            "source_path": str(SOURCES["normal_gate_2633"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def constant_rows() -> list[dict[str, Any]]:
    return [
        {
            "constant_id": "CON3529_0_alpha",
            "symbol": "alpha_0",
            "status": "CALIBRATED_NOT_DERIVED",
            "allowed_use": "local Maxwell normalization and baseline EM stress",
            "forbidden_use": "claiming MTS predicts alpha or using alpha to cancel source residuals",
            "next_gate": "nonzero C_XF2 branches go to WEP/clock/R10 bounds",
            "valid_for_claim": "False",
        },
        {
            "constant_id": "CON3529_1_kappa_G",
            "symbol": "kappa_0 or G_N",
            "status": "CALIBRATED_UNLESS_PARENT_OWNER_DERIVED",
            "allowed_use": "local Einstein/Newton coupling after calibration",
            "forbidden_use": "claiming Newton's constant is derived before kappa/source-normalization owner exists",
            "next_gate": "kappa/G_N source-normalization and M_H_ref owner",
            "valid_for_claim": "False",
        },
        {
            "constant_id": "CON3529_2_c_clock",
            "symbol": "c and clock/ruler conventions",
            "status": "OBSERVED_READOUT_OR_UNIT_CONVENTION_WITH_CAVEATS",
            "allowed_use": "local units and Maxwell/GR expression matching",
            "forbidden_use": "using light-cone agreement to fix conformal/source scale",
            "next_gate": "clock/source/conformal scale owner",
            "valid_for_claim": "False",
        },
        {
            "constant_id": "CON3529_3_Lambda",
            "symbol": "Lambda_local",
            "status": "NEGLIGIBLE_OR_CALIBRATED_FOR_LOCAL_LIMIT",
            "allowed_use": "ignored in short-range Newtonian systems or carried as calibrated cosmological term",
            "forbidden_use": "hiding local residual curvature/source terms inside Lambda",
            "next_gate": "cosmology branch handles Lambda/memory separately",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RES3529_0_epsilon_J",
            "residual": "Hilbert current/source normalization",
            "formula_or_role": "epsilon_J measures mismatch between the physical source current and common Hilbert current",
            "arena": "Newton/PPN/orbital/source-normalization",
            "current_status": "MISSING_CURRENT_OWNER_OR_NUMERIC_BOUND",
            "source_path": str(SOURCES["kernel_req_3524"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES3529_1_Delta_w_label",
            "residual": "source-label/material prefactor",
            "formula_or_role": "Delta_w_label=P_perp w_source",
            "arena": "WEP/R10/PPN/clock/orbital",
            "current_status": "MISSING_VALUE_OR_THEOREM_ZERO",
            "source_path": str(SOURCES["kernel_req_3524"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES3529_2_Delta_Hodge_EM",
            "residual": "EM Hodge/constitutive mismatch",
            "formula_or_role": "*_EM-*_obs plus constitutive/readout components",
            "arena": "Maxwell limit/light-cone/Poynting/clock/PPN",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_CLAIMED",
            "source_path": str(SOURCES["hodge_3504"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES3529_3_epsilon_Poynting",
            "residual": "external/radiative EM flux leakage",
            "formula_or_role": "boundary integral of Poynting flux or stress-flux drift after total-current closure",
            "arena": "Gdot/clock/source drift/orbital",
            "current_status": "MISSING_POYNTING_PROJECTION_AND_FLUX_VALUE",
            "source_path": str(SOURCES["kernel_req_3524"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES3529_4_kappa_G_source",
            "residual": "kappa/G_N/source denominator",
            "formula_or_role": "a1=1/(2*kappa_MTS) and its measured G_N relation before fitted-GM transfer",
            "arena": "Newtonian Poisson/PPN/orbital",
            "current_status": "BLOCKED_COEFFICIENT_OWNER_UNSIGNED",
            "source_path": str(SOURCES["normal_gate_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES3529_5_DeltaE_res",
            "residual": "non-EH operator/residual field equation terms",
            "formula_or_role": "DeltaE_res_mn in the public field equation",
            "arena": "R11/local operator closure/PPN",
            "current_status": "BLOCKED_RESIDUAL_SECTOR_ZERO_OR_BOUNDS_MISSING",
            "source_path": str(SOURCES["normal_gate_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES3529_6_PPN_vector",
            "residual": "full local PPN vector",
            "formula_or_role": "gamma,beta,preferred-frame,source,endpoint,readout and q_loc/Khat residuals",
            "arena": "Cassini/LLR/pulsars/solar-system",
            "current_status": "BLOCKED_FULL_VECTOR_VALUES_MISSING",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3529_0_alpha",
            "quantity": "alpha_loop",
            "value": "closed_as_calibrated_baseline",
            "meaning": "alpha no longer blocks the local source spine unless a nonzero C_XF2 branch is proposed",
            "claim_effect": "not a derived-alpha claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3529_1_EM_stress",
            "quantity": "calibrated_Maxwell_stress",
            "value": "usable_conditional_identity",
            "meaning": "variation of calibrated Maxwell action gives EM Hilbert stress/Poynting bookkeeping on observed geometry",
            "claim_effect": "source interface clarified but Hodge/current gates remain",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3529_2_GR_Newton",
            "quantity": "local_GR_Newton_reduction",
            "value": "exact_conditional_not_claimed",
            "meaning": "Einstein/Poisson form is written with calibrated constants and explicit residuals",
            "claim_effect": "no local-GR pass until residuals and PPN vector close",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3529_3_next",
            "quantity": "next_best_target",
            "value": "kappa_G_source_normalization_and_Newtonian_limit_gate",
            "meaning": "the decisive next move is G_N/kappa/source denominator and Poisson/PPN residuals",
            "claim_effect": "moves project back to GR/Newton derivability",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3529_0_use_calibrated_alpha",
            "decision": "use calibrated alpha in the baseline local Maxwell stress",
            "rationale": "3528 labelled alpha honestly, so the source spine can proceed without deriving alpha first",
            "effect": "prevents alpha loop from stalling GR/Newton work",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3529_1_do_not_claim_GR",
            "decision": "do not claim local GR/Newton pass",
            "rationale": "G_N/kappa/source normalization, residual EH operator silence and PPN vector remain open",
            "effect": "keeps claim discipline while writing the correct interface",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3529_2_next_kappa_source",
            "decision": "target kappa/G_N and source normalization next",
            "rationale": "this is the Newton-constant analogue of the alpha decision and directly controls the Poisson limit",
            "effect": "next step attacks the GR-to-Newton reduction spine",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3530-Y5-R2FR-kappa-G-source-normalization-and-Newtonian-limit-gate.md",
            "next_script": "scripts/Y5_R2FR_3530_kappa_G_source_normalization_and_Newtonian_limit_gate.py",
            "objective": "Decide the G_N/kappa analogue of the alpha issue: derive or explicitly calibrate the gravitational coupling, then test whether the Hilbert source denominator and Newtonian Poisson limit can be closed or bounded without fitted-GM smuggling.",
            "success_gate": "A ledger separates derived kappa identities, calibrated G_N, source-denominator residuals and PPN/Newton bound rows; no Newton/local-GR claim is allowed without source normalization and full PPN vector gates.",
            "why_next": "3529 exposes kappa/G_N and source normalization as the next hard throat after calibrated alpha.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    interface: list[dict[str, Any]],
    constants: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3529_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_1_alpha_calibrated", "passed": bool_text(any(row["symbol"] == "alpha_0" and row["status"] == "CALIBRATED_NOT_DERIVED" for row in constants) and any(row["quantity"] == "alpha_loop" for row in status)), "detail": "alpha is used only as calibrated baseline", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_2_EM_stress_identity_present", "passed": bool_text(any(row["interface_id"] == "SCI3529_1_calibrated_Maxwell_stress" and "T_EM" in row["mathematical_form"] for row in interface)), "detail": "calibrated Maxwell Hilbert stress identity is present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_3_Einstein_and_Poisson_targets_present", "passed": bool_text(any(row["interface_id"] == "SCI3529_4_local_field_equation" and "DeltaE_res" in row["mathematical_form"] for row in interface) and any(row["interface_id"] == "SCI3529_5_Newtonian_limit" and "nabla^2" in row["mathematical_form"] for row in interface)), "detail": "Einstein and Newtonian target equations written with residuals", "valid_for_claim": "False"})
    required_residuals = {"RES3529_0_epsilon_J", "RES3529_4_kappa_G_source", "RES3529_5_DeltaE_res", "RES3529_6_PPN_vector"}
    checks.append({"check_id": "VAL3529_4_residuals_cover_GR_throat", "passed": bool_text({row["residual_id"] for row in residuals} >= required_residuals), "detail": "source normalization, kappa/G, DeltaE and PPN vector residuals present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_5_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + interface + constants + residuals + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/alpha claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3530-Y5-R2FR-kappa-G-source")), "detail": "3530 kappa/G/source-normalization target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3529_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3529_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3529_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    interface: list[dict[str, Any]],
    constants: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3529 - Calibrated Alpha To Local GR Source-Coupling Interface

## Summary
- **Alpha loop closed for baseline work:** `alpha_EM` is calibrated, not derived. That lets the local Maxwell stress be used without pretending MTS predicts alpha.
- **Source interface written:** calibrated Maxwell stress, matter Hilbert stress, total Hilbert current, `G_N/kappa`, Einstein target and Poisson/Newton target are now separated.
- **Key identity retained:** internal EM/matter Lorentz exchange cancels only in `T_total=T_matter+T_EM`; Poynting belongs inside EM Hilbert stress unless external/radiative flux is present.
- **No local-GR claim:** `G_N/kappa`, source normalization, residual EH operators and the full PPN vector are still open.
- **Next throat:** the Newton-constant analogue of alpha: derive or calibrate `G_N/kappa`, then close/bound the Hilbert source denominator and Poisson limit.

## Local Source Target
`G_mn + Lambda g_mn = kappa_0 (T_matter + T_EM)_mn + DeltaE_res_mn`

Weak static target:

`nabla^2 U = 4*pi*G_N*rho_H + residual_source_terms`

This is not claimed yet. It is the contract the remaining local branch has to satisfy.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Source-Coupling Interface
{markdown_table(interface, ["interface_id", "piece", "type", "mathematical_form", "role_in_source_coupling", "remaining_gap", "source_path", "valid_for_claim"])}

## Calibrated Constants
{markdown_table(constants, ["constant_id", "symbol", "status", "allowed_use", "forbidden_use", "next_gate", "valid_for_claim"])}

## Residual Ledger
{markdown_table(residuals, ["residual_id", "residual", "formula_or_role", "arena", "current_status", "source_path", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    interface = interface_rows()
    constants = constant_rows()
    residuals = residual_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3529_SOURCE_REGISTER.csv",
        "interface": OUT / "P8_Y5_R2FR_3529_SOURCE_COUPLING_INTERFACE.csv",
        "constants": OUT / "P8_Y5_R2FR_3529_CALIBRATED_CONSTANTS.csv",
        "residuals": OUT / "P8_Y5_R2FR_3529_RESIDUAL_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3529_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3529_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3529_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3529_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["interface"], interface, ["interface_id", "piece", "type", "mathematical_form", "role_in_source_coupling", "remaining_gap", "source_path", "valid_for_claim"])
    write_csv(outputs["constants"], constants, ["constant_id", "symbol", "status", "allowed_use", "forbidden_use", "next_gate", "valid_for_claim"])
    write_csv(outputs["residuals"], residuals, ["residual_id", "residual", "formula_or_role", "arena", "current_status", "source_path", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, interface, constants, residuals, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, interface, constants, residuals, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
