from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3530-Y5-R2FR-kappa-G-source-normalization-and-Newtonian-limit-gate.md"
CANONICAL_STATUS = OUT / "P8_local_GR_kappa_G_Newtonian_gate_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3530": {"path": Path(__file__).resolve(), "role": "3530 generator"},
    "doc_3529": {
        "path": ROOT / "3529-Y5-R2FR-calibrated-alpha-to-local-GR-source-coupling-interface.md",
        "role": "calibrated alpha to local GR source interface",
    },
    "next_3529": {
        "path": OUT / "P8_Y5_R2FR_3529_NEXT_TARGET.csv",
        "role": "3529-selected kappa/G source-normalization target",
    },
    "status_3529": {
        "path": OUT / "P8_local_GR_calibrated_alpha_source_interface_status.csv",
        "role": "3529 canonical local source interface status",
    },
    "eh_coupling_2483": {
        "path": OUT / "P8_Y5_EH_COUPLING_2483_ORIGIN_AUDIT.csv",
        "role": "EH coupling origin and kappa owner audit",
    },
    "eh_route_2483": {
        "path": OUT / "P8_Y5_EH_COUPLING_2483_ROUTE_MATRIX.csv",
        "role": "routes to EH leading operator",
    },
    "kappa_residual_2483": {
        "path": OUT / "P8_Y5_EH_COUPLING_2483_COUPLING_RESIDUAL_ROW.csv",
        "role": "kappa/G residual rows",
    },
    "kappa_lock_3511": {
        "path": OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_ACTION_LINE_LOCK_THEOREM.csv",
        "role": "kappa/Gref action-line and product-lock theorem",
    },
    "kappa_bound_3511": {
        "path": OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_BOUND_INPUT_TEMPLATE.csv",
        "role": "kappa/Gref finite bound input template",
    },
    "local_gr_2633": {
        "path": OUT / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "role": "conditional local GR/Newton theorem",
    },
    "residual_map_2633": {
        "path": OUT / "P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_RESIDUAL_VECTOR_MAP.csv",
        "role": "public equation, source normalization and PPN residual map",
    },
    "newton_score_2921": {
        "path": OUT / "P8_Y5_R2FR_2921_SOURCE_NORMALIZED_NEWTON_SCORECARD_ROWS.csv",
        "role": "source-normalized Newton scorecard rows",
    },
    "newton_gates_2921": {
        "path": OUT / "P8_Y5_R2FR_2921_CLAIM_GATES.csv",
        "role": "source-normalized Newton claim gates",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bounds including Gdot, PPN and WEP anchors",
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


def kappa_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "KG3530_0_EH_coefficient",
            "piece": "EH leading coefficient",
            "classification": "DERIVABLE_CONDITIONAL_OR_CALIBRATED",
            "mathematical_form": "S_EH=(1/(2*kappa_eff)) int sqrt(-g) R",
            "current_result": "standard variation and candidate branch are valid templates; MTS parent origin and coefficient owner are not derived",
            "allowed_use": "use kappa_0=8*pi*G_N/c^4 as calibrated local constant in the effective branch",
            "forbidden_use": "claim MTS derives Newton's constant or the EH coefficient value",
            "source_path": str(SOURCES["eh_coupling_2483"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KG3530_1_topological_constancy",
            "piece": "kappa local constancy",
            "classification": "POSSIBLE_DERIVATION_ROUTE_NOT_ADOPTED",
            "mathematical_form": "S_top=int kappa_eff dA_3 => d kappa_eff=0 under fixed topological boundary variation",
            "current_result": "3511 constructs a topological route for constancy, but the sector is not adopted as the active MTS parent signature",
            "allowed_use": "retain as future parent derivation option for d kappa=0",
            "forbidden_use": "claim kappa value or source product is derived",
            "source_path": str(SOURCES["kappa_lock_3511"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KG3530_2_calibrated_GN",
            "piece": "measured local gravitational coupling",
            "classification": "CALIBRATED_CONSTANT",
            "mathematical_form": "G_N=G_ref in the local effective branch; kappa_0=8*pi*G_ref/c^4",
            "current_result": "calibration allowed only after anti-circular guard: measured GM cannot define source mass and coupling simultaneously",
            "allowed_use": "set the baseline strength of local Einstein/Poisson equations",
            "forbidden_use": "hide source-denominator, M_H_ref or fitted-GM residuals",
            "source_path": str(SOURCES["kappa_lock_3511"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "KG3530_3_product_lock",
            "piece": "local Newton coefficient product",
            "classification": "EXACT_BOOKKEEPING_IDENTITY",
            "mathematical_form": "D_X ln G_eff = D_X ln G_ref + D_X ln w_common + D_X ln ell_J + D_X ln R_frame + retained source terms",
            "current_result": "kappa constancy alone does not close Newton/local GR; the product lock is unsigned",
            "allowed_use": "defines the finite residuals that must vanish or be bounded",
            "forbidden_use": "claim Newton recovery from kappa/G calibration alone",
            "source_path": str(SOURCES["kappa_lock_3511"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def poisson_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PNG3530_0_public_equation",
            "gate": "public Einstein equation with residuals",
            "mathematical_contract": "G_mn+Lambda g_mn=kappa_0 T_H_mn + DeltaE_res_mn",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "needed_for_pass": "DeltaE_res=0 or source-backed bounds; parent normal form and EH leading operator hypotheses",
            "source_path": str(SOURCES["local_gr_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3530_1_source_denominator",
            "gate": "Hilbert source denominator/source mass",
            "mathematical_contract": "rho_H and M_H_ref are fixed before orbital/GM readout",
            "current_status": "MISSING_SOURCE_NORMALIZATION",
            "needed_for_pass": "M_H_ref, ell_J, worldtube/source-current owner and no fitted-GM transfer",
            "source_path": str(SOURCES["newton_score_2921"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3530_2_Newton_Poisson",
            "gate": "Newtonian Poisson limit",
            "mathematical_contract": "nabla^2 U=4*pi*G_ref rho_H + residual_source_terms",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "needed_for_pass": "G_eff product lock; residual source terms zero/bounded; boundary/reference branch fixed",
            "source_path": str(SOURCES["local_gr_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3530_3_no_GM_smuggling",
            "gate": "anti-circular fitted-GM guard",
            "mathematical_contract": "mu_obs=G_ref w_common M_H(1+epsilon_mu); epsilon_mu must be zero/bounded before Newton recovery is claimed",
            "current_status": "ANTI_CIRCULAR_GUARD_EXACT",
            "needed_for_pass": "epsilon_mu row and independent source denominator",
            "source_path": str(SOURCES["kappa_lock_3511"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3530_4_full_PPN",
            "gate": "full PPN/Newton residual vector",
            "mathematical_contract": "gamma,beta,preferred-frame,source,endpoint,readout,q_loc/Khat and non-EH operator residuals are zero/bounded componentwise",
            "current_status": "FULL_VECTOR_OPEN",
            "needed_for_pass": "Cassini/LLR/pulsar/WEP/R10/Gdot mappings and no-cancellation envelope",
            "source_path": str(SOURCES["residual_map_2633"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PNG3530_5_live_verdict",
            "gate": "local GR/Newton claim",
            "mathematical_contract": "PNG3530_0 through PNG3530_4 all pass together",
            "current_status": "BLOCKED_NONCLAIM",
            "needed_for_pass": "all source-normalization and PPN/Newton residuals theorem-zero or numeric source-backed",
            "source_path": str(SOURCES["newton_gates_2921"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "KB3530_0_Gdot_product",
            "residual": "D_t ln G_eff product",
            "arena": "LLR/Gdot",
            "formula": "D_t ln(G_ref w_common ell_J R_frame ...)",
            "bound_value": "9.6e-15",
            "units": "yr^-1",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R9_Gdot",
            "prediction_status": "MISSING_DTLN_GREF_WCOMMON_ELLJ_RFRAME",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "KB3530_1_WEP_source_charge",
            "residual": "source charge universality / eta_source_AB",
            "arena": "MICROSCOPE/WEP",
            "formula": "eta_AB from source/test Hilbert charge mismatch and source current weights",
            "bound_value": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R1_WEP_source_charge",
            "prediction_status": "MISSING_SOURCE_CHARGE_UNIVERSALITY",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "KB3530_2_gamma",
            "residual": "PPN gamma_minus_1",
            "arena": "Cassini/Shapiro",
            "formula": "gamma residual from metric/source/readout/non-EH vector",
            "bound_value": "2.3e-05",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R3_gamma",
            "prediction_status": "MISSING_FULL_PPN_VECTOR_PROJECTION",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "KB3530_3_beta",
            "residual": "PPN beta_minus_1 / nonlinear source residue",
            "arena": "planetary ephemerides/LLR",
            "formula": "delta_beta_source plus non-EH nonlinear residuals",
            "bound_value": "7.8e-05",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R4_beta",
            "prediction_status": "MISSING_B_SOURCE_A_SOURCE_SQUARE_LAW",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "KB3530_4_fifth_force_R10",
            "residual": "range dependence / Yukawa alpha(lambda)",
            "arena": "R10 inverse-square",
            "formula": "alpha(lambda) from residual scalar/source range and source charge product",
            "bound_value": "alpha(lambda)",
            "units": "range-dependent",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R10_fifth_force",
            "prediction_status": "MISSING_RANGE_CURVE_OR_NO_RANGE_THEOREM",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "KB3530_5_total_guard",
            "residual": "source-normalized Newton total absolute residual",
            "arena": "Newton/PPN/R10/WEP/Gdot",
            "formula": "Delta_SN_total_abs=sum_abs(all source/kappa/frame/operator residual components)",
            "bound_value": "componentwise",
            "units": "mixed_declared_per_component",
            "source_path": str(SOURCES["newton_score_2921"]["path"]),
            "source_row": "SN2921_9_total_guard",
            "prediction_status": "TOTAL_SOURCE_NORMALIZED_NEWTON_NOT_SCORE_READY",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3530_0_calibrate_GN",
            "decision": "use G_N/kappa_0 as calibrated local constant in the baseline branch",
            "rationale": "parent kappa value is not derived; calibration is honest and GR-standard",
            "effect": "does not solve source normalization or Newton recovery by itself",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3530_1_product_lock_required",
            "decision": "treat local Newton recovery as a product-lock problem",
            "rationale": "local tests see G_ref*w_common*ell_J*frame/source normalization, not kappa alone",
            "effect": "prevents fitted-GM smuggling",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3530_2_next_source_denominator",
            "decision": "target M_H_ref/ell_J/source denominator before claiming Poisson",
            "rationale": "Poisson coefficient is meaningless unless rho_H is the same Hilbert source object used by the field equation",
            "effect": "next step attacks source normalization directly",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3530_0_kappa",
            "quantity": "kappa_GN",
            "value": "calibrated_baseline_not_derived",
            "meaning": "G_N/kappa is a measured local constant unless a parent coefficient owner is later derived",
            "claim_effect": "no derived Newton constant claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3530_1_product",
            "quantity": "G_eff_product_lock",
            "value": "exact_bookkeeping_identity_unsigned",
            "meaning": "Newton recovery depends on G_ref*w_common*ell_J*frame/source normalization",
            "claim_effect": "kappa constancy alone is insufficient",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3530_2_Newton",
            "quantity": "Newtonian_Poisson_limit",
            "value": "exact_conditional_not_claimed",
            "meaning": "Poisson target is written but source denominator and residual vector remain open",
            "claim_effect": "no Newton/local-GR pass",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3530_3_next",
            "quantity": "next_best_target",
            "value": "Hilbert_source_denominator_MHref_ellJ_owner",
            "meaning": "derive or bound the source mass/current normalization entering rho_H and M_H_ref",
            "claim_effect": "moves into source normalization rather than constants",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3531-Y5-R2FR-Hilbert-source-denominator-MHref-ellJ-owner-or-Newton-bound-row.md",
            "next_script": "scripts/Y5_R2FR_3531_Hilbert_source_denominator_MHref_ellJ_owner_or_Newton_bound_row.py",
            "objective": "Attack the source side of the Newtonian limit: derive or bound the common Hilbert source denominator, M_H_ref, ell_J and no fitted-GM transfer that define rho_H before Poisson/PPN scoring.",
            "success_gate": "Either M_H_ref/ell_J/source current are parent-owned and same-frame, or finite Newton/PPN/Gdot/WEP bound rows receive explicit prediction-side coefficients and units.",
            "why_next": "3530 shows calibrated G_N is not enough; the next missing object is the Hilbert source denominator.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3530_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_1_kappa_calibrated_not_derived", "passed": bool_text(any(row["contract_id"] == "KG3530_2_calibrated_GN" for row in contracts) and any(row["quantity"] == "kappa_GN" and row["value"] == "calibrated_baseline_not_derived" for row in status)), "detail": "G_N/kappa is calibrated baseline, not derived claim", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_2_product_lock_present", "passed": bool_text(any(row["contract_id"] == "KG3530_3_product_lock" and "w_common" in row["mathematical_form"] for row in contracts)), "detail": "G_eff product-lock identity is present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_3_no_GM_smuggling_gate", "passed": bool_text(any(row["gate_id"] == "PNG3530_3_no_GM_smuggling" and row["current_status"] == "ANTI_CIRCULAR_GUARD_EXACT" for row in gates)), "detail": "anti-circular fitted-GM guard is active", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_4_bounds_staged", "passed": bool_text(any(row["bound_id"] == "KB3530_0_Gdot_product" and row["bound_value"] == "9.6e-15" for row in bounds) and any(row["bound_id"] == "KB3530_5_total_guard" for row in bounds)), "detail": "Gdot and total source-normalized Newton bound rows staged", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_5_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + contracts + gates + bounds + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no Newton/local-GR/kappa claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3531-Y5-R2FR-Hilbert-source-denominator")), "detail": "3531 source-denominator target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3530_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3530_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3530_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3530 - Kappa/G Source Normalization And Newtonian Limit Gate

## Summary
- **G_N/kappa handled honestly:** like alpha, `G_N` is a calibrated local constant in the baseline branch unless a parent coefficient owner is later derived.
- **Important distinction:** calibrating `G_N` does not derive Newtonian recovery. Local tests see the product `G_ref * w_common * ell_J * R_frame * M_H`, not kappa alone.
- **Anti-smuggling guard:** observed orbital `GM` may calibrate an already-fixed branch, but cannot define both the coupling and the source mass.
- **Poisson target written:** `nabla^2 U = 4*pi*G_ref*rho_H + residual_source_terms`, still nonclaim until the source denominator and PPN/Newton residual vector close.
- **Next hard throat:** `M_H_ref`, `ell_J`, common Hilbert source current and no fitted-GM transfer.

## Newtonian Target
`G_mn + Lambda g_mn = kappa_0 T_H_mn + DeltaE_res_mn`

`nabla^2 U = 4*pi*G_ref rho_H + residual_source_terms`

where `rho_H` must come from the same Hilbert source branch before any orbital `GM` readout is used.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Kappa/G Contract
{markdown_table(contracts, ["contract_id", "piece", "classification", "mathematical_form", "current_result", "allowed_use", "forbidden_use", "source_path", "valid_for_claim"])}

## Poisson/PPN Gates
{markdown_table(gates, ["gate_id", "gate", "mathematical_contract", "current_status", "needed_for_pass", "source_path", "valid_for_claim"])}

## Bound Rows
{markdown_table(bounds, ["bound_id", "residual", "arena", "formula", "bound_value", "units", "source_path", "source_row", "prediction_status", "score_ready", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    contracts = kappa_contract_rows()
    gates = poisson_gate_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3530_SOURCE_REGISTER.csv",
        "kappa_contract": OUT / "P8_Y5_R2FR_3530_KAPPA_G_CONTRACT.csv",
        "poisson_gates": OUT / "P8_Y5_R2FR_3530_POISSON_PPN_GATES.csv",
        "bound_rows": OUT / "P8_Y5_R2FR_3530_NEWTON_PPN_BOUND_ROWS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3530_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3530_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3530_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3530_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["kappa_contract"], contracts, ["contract_id", "piece", "classification", "mathematical_form", "current_result", "allowed_use", "forbidden_use", "source_path", "valid_for_claim"])
    write_csv(outputs["poisson_gates"], gates, ["gate_id", "gate", "mathematical_contract", "current_status", "needed_for_pass", "source_path", "valid_for_claim"])
    write_csv(outputs["bound_rows"], bounds, ["bound_id", "residual", "arena", "formula", "bound_value", "units", "source_path", "source_row", "prediction_status", "score_ready", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, contracts, gates, bounds, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, contracts, gates, bounds, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
