from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3538-Y5-R2FR-observed-flow-coframe-stationary-branch-ownership-or-PPN-vector-bounds.md"
CANONICAL_STATUS = OUT / "P8_local_GR_observed_flow_stationary_branch_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3538": {"path": Path(__file__).resolve(), "role": "3538 generator"},
    "doc_3537": {
        "path": ROOT / "3537-Y5-R2FR-Qcoh-parent-action-or-Noether-load-tensor-STF-zero.md",
        "role": "3537 Qcoh deformation tensor handoff",
    },
    "next_3537": {
        "path": OUT / "P8_Y5_R2FR_3537_NEXT_TARGET.csv",
        "role": "3537 selected observed-flow target",
    },
    "qcoh_zero_3537": {
        "path": OUT / "P8_Y5_R2FR_3537_QCOH_NOETHER_ZERO_PROOF.csv",
        "role": "Qcoh Noether/geometric zero proof",
    },
    "stress_audit_3537": {
        "path": OUT / "P8_Y5_R2FR_3537_STRESS_BIANCHI_AUDIT.csv",
        "role": "Qcoh stress/Bianchi caveats",
    },
    "fallbacks_3537": {
        "path": OUT / "P8_Y5_R2FR_3537_COEFFICIENT_FALLBACKS.csv",
        "role": "Qcoh fallback coefficient rows",
    },
    "min_parent_blocks": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "minimal local-GR action blocks",
    },
    "symbol_map": {
        "path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "MTS symbol to local-GR action map",
    },
    "first_variation_gates": {
        "path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "MTS symbol first-variation gates",
    },
    "domain_novector": {
        "path": OUT / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
        "role": "domain no-vector theorem attempt",
    },
    "domain_alpha3": {
        "path": OUT / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
        "role": "domain alpha3 no-leak attempt",
    },
    "local_zero_requirements": {
        "path": OUT / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv",
        "role": "local-zero extra premise requirements",
    },
    "prediction_template": {
        "path": OUT / "MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "local residual prediction template",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical bounds",
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


def flow_ownership_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "FLO3538_0_quotient_coframe",
            "object": "g_obs/e_obs/tau_obs",
            "definition": "Observed coframe and time flow are quotient/readout objects: u^mu=tau_obs^mu, h_mn=g_obs_mn+u_m u_n.",
            "zero_or_bound": "parent-owned if all matter, clocks, EM Hodge, Hilbert stress and Hamiltonian charge use the same g_obs/tau_obs",
            "current_status": "CONDITIONAL_SAME_VISIBLE_STACK",
            "residual_if_failed": "R_frame; Delta_Hodge_EM; clock/source/PPN frame mismatch",
            "valid_for_claim": "False",
        },
        {
            "route_id": "FLO3538_1_stationary_Killing",
            "object": "compact local stationary branch",
            "definition": "Local isolated branch has a parent-owned timelike generator k with L_k g_obs=0 and u=k/sqrt(-k^2).",
            "zero_or_bound": "L_u h_ij=0, expansion X=0, shear Q_STF=0 and Qcoh deformation zero",
            "current_status": "EXACT_CONDITIONAL_NOT_GLOBAL_LOCAL_GR",
            "residual_if_failed": "X, Q_STF, V_domain and preferred-frame PPN rows",
            "valid_for_claim": "False",
        },
        {
            "route_id": "FLO3538_2_no_flux_domain",
            "object": "domain representative/no-flux branch",
            "definition": "Compact local domain representative is exact/trivial and carries no coherent FLRW/domain memory class locally.",
            "zero_or_bound": "P_loc^i_mu F_D^mu=0 and epsilon_domain_flux=0 only if parent domain selector owns the representative",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "residual_if_failed": "alpha3 domain flux and R11 source-normalization rows",
            "valid_for_claim": "False",
        },
        {
            "route_id": "FLO3538_3_dynamic_PPN_branch",
            "object": "nonstationary/moving-source branch",
            "definition": "If L_u h is not zero, it is a real local residual, not a failure to be ignored.",
            "zero_or_bound": "report X, Q_STF, V_domain and flux components with PPN/R11 maps",
            "current_status": "BOUND_BRANCH_REQUIRED",
            "residual_if_failed": "R5/R6/R7/R8/R11 coefficient products",
            "valid_for_claim": "False",
        },
    ]


def stationary_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "OSP3538_0_same_stack",
            "target": "observed stack ownership",
            "statement": "Use one quotient coframe for matter rods/clocks, Maxwell Hodge star, Hilbert stress and Hamiltonian charge.",
            "mathematical_form": "S_matter[g_obs,psi]+S_EM[g_obs,A]+S_EH[g_obs]; tau_obs fixed before source readout",
            "derived_result": "This would make u/h/tau_obs parent-owned rather than post-selected fit objects.",
            "current_status": "CONDITIONAL_FROM_LOCAL_EH_KERNEL",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "OSP3538_1_Killing_Qzero",
            "target": "Qcoh zero",
            "statement": "If tau_obs is a Killing flow of the compact local branch, Qcoh vanishes geometrically.",
            "mathematical_form": "L_tau g_obs=0 and h=g_obs+u u => L_u h=0 => Qcoh_ij=0",
            "derived_result": "X=0 and Q_STF=0 exactly for the stationary branch.",
            "current_status": "EXACT_BRANCH_THEOREM_IF_KILLING_PREMISE_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "OSP3538_2_no_vector_spurion",
            "target": "PPN preferred-frame vector silence",
            "statement": "Stationary scalar branch has no independent local vector/marker if u is only the observed time generator and no domain normal/velocity is introduced.",
            "mathematical_form": "epsilon_D^i=P_loc^i_mu V_D^mu=0 if V_D^mu is absent and D_i chi_D=0",
            "derived_result": "alpha1/alpha2 vector leakage can be zeroed only under the no-spurion/domain-selector premises.",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "OSP3538_3_alpha3_flux_warning",
            "target": "domain alpha3 flux",
            "statement": "Stationarity of u/h does not automatically kill domain momentum flux alpha3.",
            "mathematical_form": "Qcoh=0 does not imply P_loc^i_mu F_D^mu=0",
            "derived_result": "alpha3 still needs trivial representative/no-flux/domain R11 silence or coefficient bounds.",
            "current_status": "SCOPE_GUARD_ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "OSP3538_4_dynamic_branch",
            "target": "nonstationary residuals",
            "statement": "For moving-source or time-dependent local systems, L_u h must be treated as a residual vector.",
            "mathematical_form": "Q_ij=1/2 L_u h_ij; residual vector={X,Q_STF,V_domain,F_D}",
            "derived_result": "No universal local-GR promotion follows from the stationary branch alone.",
            "current_status": "BOUND_BRANCH_STAGED",
            "valid_for_claim": "False",
        },
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "OFB3538_0_X_expansion",
            "residual": "X=tr(Qcoh)=nabla_mu u^mu",
            "observable_map": "Gdot/source drift; clock drift; scalar expansion source",
            "bound_requirement": "numeric or theorem-zero X with units tied to tau_obs; if time drift, compare to Gdot rows",
            "current_status": "MISSING_NUMERIC_OR_PARENT_ZERO",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "OFB3538_1_Q_STF_shear",
            "residual": "Q_STF_ij",
            "observable_map": "gamma/beta/xi anisotropy and R11 shear/operator rows",
            "bound_requirement": "W_QSTF_gamma_beta_xi products or theorem-zero no-shear certificate",
            "current_status": "MISSING_COEFFICIENT_PRODUCTS",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "OFB3538_2_domain_vector",
            "residual": "epsilon_domain_vector=P_loc^i_mu V_D^mu",
            "observable_map": "alpha1 and alpha2 preferred-frame rows",
            "bound_requirement": "abs(alpha1_domain)<=1e-4 and abs(alpha2_domain)<=2e-9 with sourced products or theorem-zero",
            "current_status": "DOMAIN_VECTOR_PRODUCTS_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "OFB3538_3_domain_flux",
            "residual": "epsilon_domain_flux=P_loc^i_mu F_D^mu",
            "observable_map": "alpha3 preferred-momentum/nonconservation row",
            "bound_requirement": "abs(W_domain_alpha3*epsilon_domain_flux)<=4e-20 or theorem-zero no-flux certificate",
            "current_status": "HIGHEST_PRESSURE_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "OFB3538_4_domain_anisotropy",
            "residual": "epsilon_domain_anisotropy=STF(P_loc T_D P_loc)",
            "observable_map": "xi preferred-location and anisotropic stress rows",
            "bound_requirement": "abs(xi_domain)<=4e-9 or theorem-zero scalar/topological stress certificate",
            "current_status": "NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "OFB3538_5_R11_unfactored",
            "residual": "unfactored local operator family independent of Qcoh/Sigma_loc",
            "observable_map": "R2/R3/R4/R9/R10/R11",
            "bound_requirement": "complete R11 vector with coefficients, units, normalization and weak-field maps",
            "current_status": "R11_VECTOR_HAS_MISSING_ROWS",
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "OFG3538_0_same_visible_stack",
            "gate": "same observed coframe/tau in matter, clocks, EM, Hilbert stress and Hamiltonian charge",
            "current_result": "not fully parent-signed",
            "blocks": "frame/source/readout mismatch",
            "claim_allowed": "False",
        },
        {
            "gate_id": "OFG3538_1_local_Killing_branch",
            "gate": "parent action/boundary conditions select a compact local stationary branch with L_tau g=0",
            "current_result": "conditional branch only",
            "blocks": "Qcoh zero promotion beyond stationary systems",
            "claim_allowed": "False",
        },
        {
            "gate_id": "OFG3538_2_no_domain_spurion",
            "gate": "domain selector introduces no independent vector, normal, velocity, material marker or anisotropy",
            "current_result": "not parent-derived",
            "blocks": "alpha1/alpha2/xi and alpha3",
            "claim_allowed": "False",
        },
        {
            "gate_id": "OFG3538_3_no_flux_trivial_representative",
            "gate": "compact local domain representative is exact/trivial and carries no local coherent memory flux",
            "current_result": "conditional not parent-derived",
            "blocks": "alpha3 <= 4e-20",
            "claim_allowed": "False",
        },
        {
            "gate_id": "OFG3538_4_R11_silence",
            "gate": "every local non-EH/source operator is Sigma_loc factored, topological/exact or bounded",
            "current_result": "fails current R11 vector",
            "blocks": "local GR/PPN/Maxwell stress promotion",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3538_0_stationary_branch_use",
            "decision": "Use the stationary/Killing branch only as an exact conditional local-zero theorem.",
            "rationale": "It cleanly gives L_u h=0 and Qcoh=0, but it does not cover all local PPN dynamics or domain flux.",
            "effect": "Qcoh route becomes sharper without overclaiming local GR.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3538_1_dynamic_residuals",
            "decision": "For nonstationary or unowned-flow cases, retain explicit PPN/vector/domain-flux residual rows.",
            "rationale": "Moving-source local tests need a residual vector, not a stationary shortcut.",
            "effect": "X, Q_STF, vector, flux, anisotropy and R11 rows remain bound targets.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3538_2_next",
            "decision": "Attack q_loc/Gamma-Khat Ward/no-flux residual next.",
            "rationale": "Observed-flow stationarity narrows Qcoh, but the true local force residual q_loc and boundary/domain flux remain the live local-GR hinge.",
            "effect": "next target moves to Ward residual ownership rather than another flow restatement.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3538_0_flow",
            "quantity": "observed_flow_coframe",
            "value": "conditional_same_stack_owner",
            "meaning": "u/h/tau_obs are clean if inherited from the same g_obs quotient used by matter, EM, stress and charge",
            "claim_effect": "not fully parent-signed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3538_1_stationary",
            "quantity": "stationary_Killing_Qcoh_zero",
            "value": "exact_conditional_branch",
            "meaning": "L_u h=0 gives Qcoh=0 on compact stationary branch",
            "claim_effect": "does not prove full local GR or dynamic PPN branch",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3538_2_bounds",
            "quantity": "PPN_vector_domain_flux_bounds",
            "value": "required_if_flow_or_no_flux_premises_fail",
            "meaning": "X/Q_STF/vector/flux/anisotropy/R11 rows must be filled or theorem-zeroed",
            "claim_effect": "keeps local-GR claim blocked",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3538_3_next",
            "quantity": "next_best_target",
            "value": "q_loc_Gamma_Khat_Ward_residual_no_flux_or_bounds",
            "meaning": "the remaining local-force residual must be derived as an on-shell Ward exact term or bounded",
            "claim_effect": "direct route to local GR/Newton PPN residual vector",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3539-Y5-R2FR-qloc-Gamma-Khat-Ward-residual-no-flux-or-PPN-bound-vector.md",
            "next_script": "scripts/Y5_R2FR_3539_qloc_Gamma_Khat_Ward_residual_no_flux_or_PPN_bound_vector.py",
            "objective": "Try to derive q_loc^nu=P_loc(nabla^nu Gamma_eff-div K_hat) as an on-shell Ward/exact boundary residual that vanishes on the compact local branch, or emit PPN/local-bound rows for the surviving force/flux vector.",
            "success_gate": "Either q_loc is parent-owned and theorem-zero under the same observed-flow/no-flux branch, or every surviving component maps to WEP/PPN/Gdot/R10/R11 coefficient rows.",
            "why_next": "3538 sharpens observed-flow stationarity but leaves the actual local force residual and boundary/domain flux as the hinge.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    flows: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3538_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_1_flow_routes_present", "passed": bool_text({"FLO3538_0_quotient_coframe", "FLO3538_1_stationary_Killing", "FLO3538_3_dynamic_PPN_branch"} <= {row["route_id"] for row in flows}), "detail": "quotient, stationary and dynamic branches present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_2_Killing_Qzero_present", "passed": bool_text(any(row["proof_id"] == "OSP3538_1_Killing_Qzero" and "Qcoh" in row["target"] for row in proofs)), "detail": "Killing-flow Qcoh zero proof present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_3_alpha3_scope_guard", "passed": bool_text(any(row["proof_id"] == "OSP3538_3_alpha3_flux_warning" for row in proofs) and any(row["bound_id"] == "OFB3538_3_domain_flux" for row in bounds)), "detail": "domain alpha3 flux guard and bound row present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_4_bound_rows_cover_vector_flux_R11", "passed": bool_text({"OFB3538_1_Q_STF_shear", "OFB3538_2_domain_vector", "OFB3538_3_domain_flux", "OFB3538_5_R11_unfactored"} <= {row["bound_id"] for row in bounds}), "detail": "Q_STF, vector, flux and R11 fallback rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_5_gates_retained", "passed": bool_text(all(row["claim_allowed"] == "False" for row in gates)), "detail": "promotion gates retained rather than passed", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_6_no_false_claims", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + flows + proofs + bounds + status) and all(row["claim_allowed"] == "False" for row in gates + decisions + next_rows)), "detail": "no local-GR/Newton/PPN claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3539-Y5-R2FR-qloc")), "detail": "3539 qloc/Gamma-Khat target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3538_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3538_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3538_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    flows: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3538 - Observed Flow/Coframe Stationary Branch Ownership Or PPN Vector Bounds

## Summary
- **Observed-flow route:** `u/h/tau_obs` are clean only if they descend from the same `g_obs` quotient used by matter, clocks, EM, Hilbert stress and Hamiltonian charge.
- **Exact conditional win:** on a parent-owned compact stationary branch, `L_u h=0`, so `Qcoh=0`, `X=0`, and `Q_STF=0`.
- **No overclaim:** stationarity does not automatically kill domain flux, boundary flux, unfactored R11 towers, or dynamic PPN residuals.
- **Bound branch staged:** if the flow/no-flux premises fail, `X`, `Q_STF`, domain vector, domain flux, anisotropy, and R11 coefficients must be filled or theorem-zeroed.
- **Next hinge:** `q_loc^nu=P_loc(nabla^nu Gamma_eff-div K_hat)` must be derived as a Ward/exact residual or bounded.

## Core Local Branch
If the parent action gives a single observed quotient stack and a compact local time generator with

`L_tau g_obs = 0`,

then with `u=tau/sqrt(-tau^2)` and `h=g_obs+u u`,

`L_u h = 0`,

so

`Qcoh_ij=1/2 L_u h_ij=0`.

That is useful, but it is a stationary-branch theorem, not a universal local-GR pass.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Flow Ownership Routes
{markdown_table(flows, ["route_id", "object", "definition", "zero_or_bound", "current_status", "residual_if_failed", "valid_for_claim"])}

## Stationary Proof
{markdown_table(proofs, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])}

## Residual Bound Rows
{markdown_table(bounds, ["bound_id", "residual", "observable_map", "bound_requirement", "current_status", "valid_for_claim"])}

## Promotion Gates
{markdown_table(gates, ["gate_id", "gate", "current_result", "blocks", "claim_allowed"])}

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
    flows = flow_ownership_rows()
    proofs = stationary_proof_rows()
    bounds = residual_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3538_SOURCE_REGISTER.csv",
        "flow_routes": OUT / "P8_Y5_R2FR_3538_FLOW_OWNERSHIP_ROUTES.csv",
        "stationary_proof": OUT / "P8_Y5_R2FR_3538_STATIONARY_BRANCH_PROOF.csv",
        "residual_bounds": OUT / "P8_Y5_R2FR_3538_PPN_VECTOR_BOUND_ROWS.csv",
        "promotion_gates": OUT / "P8_Y5_R2FR_3538_PROMOTION_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3538_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3538_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3538_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3538_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["flow_routes"], flows, ["route_id", "object", "definition", "zero_or_bound", "current_status", "residual_if_failed", "valid_for_claim"])
    write_csv(outputs["stationary_proof"], proofs, ["proof_id", "target", "statement", "mathematical_form", "derived_result", "current_status", "valid_for_claim"])
    write_csv(outputs["residual_bounds"], bounds, ["bound_id", "residual", "observable_map", "bound_requirement", "current_status", "valid_for_claim"])
    write_csv(outputs["promotion_gates"], gates, ["gate_id", "gate", "current_result", "blocks", "claim_allowed"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, flows, proofs, bounds, gates, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, flows, proofs, bounds, gates, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
