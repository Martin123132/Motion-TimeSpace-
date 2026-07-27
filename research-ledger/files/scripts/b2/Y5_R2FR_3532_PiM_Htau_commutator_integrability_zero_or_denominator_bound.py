from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3532-Y5-R2FR-PiM-Htau-commutator-integrability-zero-or-denominator-bound.md"
CANONICAL_STATUS = OUT / "P8_local_GR_PiM_Htau_zero_mechanism_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3532": {"path": Path(__file__).resolve(), "role": "3532 generator"},
    "doc_3531": {
        "path": ROOT / "3531-Y5-R2FR-Hilbert-source-denominator-MHref-ellJ-owner-or-Newton-bound-row.md",
        "role": "3531 Hilbert denominator handoff",
    },
    "status_3531": {
        "path": OUT / "P8_local_GR_Hilbert_source_denominator_status.csv",
        "role": "3531 canonical Hilbert denominator status",
    },
    "next_3531": {
        "path": OUT / "P8_Y5_R2FR_3531_NEXT_TARGET.csv",
        "role": "3531-selected PiM/Htau target",
    },
    "residuals_3531": {
        "path": OUT / "P8_Y5_R2FR_3531_RESIDUAL_COMPONENTS.csv",
        "role": "3531 denominator residual components",
    },
    "ellj_residual_3513": {
        "path": OUT / "P8_Y5_R2FR_3513_ELLJ_RESIDUAL_LAW.csv",
        "role": "ell_J residual decomposition",
    },
    "ellj_square_3513": {
        "path": OUT / "P8_Y5_R2FR_3513_ELLJ_SOURCE_CURRENT_COMMUTING_SQUARE.csv",
        "role": "source-current commuting square",
    },
    "min_local_gr_blocks": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "role": "minimal parent local-GR action blocks",
    },
    "min_local_gr_chain": {
        "path": OUT / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv",
        "role": "minimal local-GR derived chain",
    },
    "hilbert_worldtube_contract": {
        "path": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "role": "Hilbert/worldtube parent action contract",
    },
    "charge_current_direct": {
        "path": OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "role": "charge-current equality direct attempt",
    },
    "charge_current_residuals": {
        "path": OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "role": "charge-current residual decomposition",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "local empirical residual bounds",
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


def zero_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "ZC3532_0_parent_phase_space",
            "clause": "Parent action supplies covariant phase space and Hamiltonian variation.",
            "mathematical_form": "delta L = E_A delta phi^A + dTheta; delta H_tau = integral_boundary(delta Q_tau - tau dot Theta)",
            "needed_for": "R_Htau integrability; Hilbert charge equality",
            "current_status": "CONDITIONAL_FROM_PRIOR_CONTRACTS",
            "source_path": str(SOURCES["hilbert_worldtube_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_1_local_EH_quotient",
            "clause": "There is one observed metric/coframe quotient q(Phi)=g_obs and the compact local branch reduces to EH at leading order.",
            "mathematical_form": "S_parent -> S_EH[g_obs;kappa0,Lambda0] + S_m[g_obs,psi] + S_silent[Y] + dB",
            "needed_for": "standard Hamiltonian constraint; Poisson source denominator",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["min_local_gr_blocks"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_2_universal_matter_source",
            "clause": "Matter sees only the observed metric/coframe at leading local order; no direct species-dependent Y vertices.",
            "mathematical_form": "S_matter = S_matter[g_obs,psi]; D_Y S_matter|g_obs,psi = 0",
            "needed_for": "D_Y J_H=0; WEP/source charge silence",
            "current_status": "OPEN_NOT_PARENT_DERIVED",
            "source_path": str(SOURCES["min_local_gr_blocks"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_3_silent_extra_fixed_point",
            "clause": "Motion/time/domain/memory/range fields have a local fixed point with no linear stress, charge, or symplectic flux.",
            "mathematical_form": "Y=0; dV(Y0)=0; Hessian(V)>0; dC(Y0)=0; delta H_tau^Y=0",
            "needed_for": "R_Htau=0 and no non-EH source denominator hair",
            "current_status": "FIELD_MATCHING_OPEN",
            "source_path": str(SOURCES["min_local_gr_blocks"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_4_charge_identified_PiM",
            "clause": "Pi_M is not an adjustable empirical projector; it is the mass component of the same Hilbert/Hamiltonian charge.",
            "mathematical_form": "Pi_M^H[J_H] := c^-2 integral_Sigma n_mu tau_nu T_H^{mu nu} dSigma = c^-2(H_tau-H_ref)",
            "needed_for": "R_PiM=0 without GM laundering",
            "current_status": "NEW_BEST_ROUTE_CONTRACT",
            "source_path": str(SOURCES["charge_current_direct"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_5_fixed_worldtube_and_reference",
            "clause": "Worldtube, reference subtraction, units and readout frame are selected by the source current and observed time before fitting.",
            "mathematical_form": "W_source=closure(supp J_H[tau]); H_ref fixed; tau=tau_obs; units fixed once",
            "needed_for": "R_ref=R_W=R_frame=R_units=0",
            "current_status": "OPEN_NOT_PARENT_DERIVED",
            "source_path": str(SOURCES["hilbert_worldtube_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_6_Htau_integrability",
            "clause": "The observed time generator is Hamiltonian on the local branch; symplectic flux through the compact exterior boundary vanishes.",
            "mathematical_form": "curl(delta H_tau)=integral_boundary i_tau omega_total = 0",
            "needed_for": "R_Htau=0",
            "current_status": "OPEN_NO_PARENT_FLUX_CERTIFICATE",
            "source_path": str(SOURCES["charge_current_direct"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "contract_id": "ZC3532_7_second_order_PPN_survival",
            "clause": "The same source denominator survives the second-order weak-field expansion, not just Newtonian first order.",
            "mathematical_form": "gamma-1=0; beta-1=0; alpha_i=zeta_i=xi=0 plus bounded residual vector",
            "needed_for": "local GR promotion",
            "current_status": "NOT_REACHED",
            "source_path": str(SOURCES["charge_current_direct"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def zero_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "ZP3532_0_RPiM_kernel",
            "target": "R_PiM",
            "derivation_step": "Use the charge-identified route, so Pi_M is the EH/Hilbert mass functional built from g_obs, tau_obs, W_source and J_H before any orbital readout.",
            "mathematical_form": "Pi_M^H[J_H]=c^-2 integral_W n_mu tau_nu T_H^{mu nu} dSigma",
            "zero_result": "[D_Y,Pi_M^H]J_H=0 if D_Y g_obs=D_Y tau_obs=D_Y W_source=D_Y units=0 and D_Y J_H=0",
            "live_verdict": "CONDITIONAL_ZERO_MECHANISM_FOUND_NOT_PARENT_SIGNED",
            "remaining_obstruction": "ZC3532_1 through ZC3532_5 are not all current-parent theorems",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP3532_1_RPiM_no_GM_laundering",
            "target": "R_PiM",
            "derivation_step": "Do not define Pi_M from fitted orbital GM. Define the source charge first, then let orbital GM test G_ref M_H_ref.",
            "mathematical_form": "mu_obs=G_ref M_H_ref(1+epsilon_mu), not M_H_ref:=mu_obs/G_ref",
            "zero_result": "GM fitting cannot hide R_PiM because epsilon_mu remains an observable residual.",
            "live_verdict": "DISCIPLINE_LOCK_ACTIVE",
            "remaining_obstruction": "needs independent M_H_ref source row",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP3532_2_RHtau_integrability",
            "target": "R_Htau",
            "derivation_step": "For the EH quotient branch, H_tau is integrable when tau is a fixed observed time/Killing generator and all extra-sector symplectic fluxes vanish.",
            "mathematical_form": "curl(delta H_tau)=integral_boundary i_tau omega_EH + integral_boundary i_tau omega_extra = 0",
            "zero_result": "R_Htau=0 if EH boundary conditions hold and omega_extra has zero local boundary flux.",
            "live_verdict": "CONDITIONAL_ZERO_MECHANISM_FOUND_NOT_PARENT_SIGNED",
            "remaining_obstruction": "no parent flux certificate for motion/time/domain/memory/range sectors",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP3532_3_charge_current_equality",
            "target": "M_H_ref",
            "derivation_step": "With EH constraint and the same Hilbert source, boundary Hamiltonian variation equals projected source variation.",
            "mathematical_form": "delta(H_tau/G_ref)=delta int_W rho_H dV_H + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra",
            "zero_result": "M_H_ref=int_W rho_H dV_H follows if all Delta terms vanish and H_ref fixes the integration constant.",
            "live_verdict": "CONDITIONAL_STANDARD_GR_ROUTE",
            "remaining_obstruction": "Delta_nonEH/Delta_symp/Delta_extra and H_ref zero remain open",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP3532_4_zellJ_collapse",
            "target": "z_ellJ",
            "derivation_step": "If R_PiM and R_Htau are zero by the charge-identified EH route, the remaining ell_J pieces reduce to matter Ward identity, fixed reference, fixed worldtube, fixed frame and fixed units.",
            "mathematical_form": "z_ellJ=R_md+R_Ward+R_ref+R_W+R_frame+R_units after R_PiM=R_Htau=0",
            "zero_result": "full z_ellJ=0 only after the remaining source/readout clauses are also signed.",
            "live_verdict": "PARTIAL_COLLAPSE_ROUTE_NOT_FULL_ZERO",
            "remaining_obstruction": "R_ref/R_W/R_frame/R_units still need parent-owned selectors",
            "valid_for_claim": "False",
        },
    ]


def fallback_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PHTB3532_0_PiM_kernel_drift",
            "failed_zero_clause": "ZC3532_4_charge_identified_PiM",
            "residual": "C_PiM := norm([D_X,Pi_M^H]J_H)/norm(Pi_M^H[J_H])",
            "bound_route": "map to dln_Meff/dX, WEP source charge, R10 source-support charge and orbital epsilon_mu",
            "arena": "Newton/WEP/R10/orbital",
            "needed_source_row": "numeric or theorem-zero C_PiM with units, source support and source path",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PHTB3532_1_Htau_curl_flux",
            "failed_zero_clause": "ZC3532_6_Htau_integrability",
            "residual": "C_Htau := norm(integral_boundary i_tau omega_total)/norm(delta H_tau)",
            "bound_route": "map to Gdot, clock drift, PPN preferred-frame/conservation rows and boundary mass leakage",
            "arena": "Gdot/clocks/PPN/orbital",
            "needed_source_row": "numeric or theorem-zero symplectic flux certificate by sector",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PHTB3532_2_extra_mass_channel",
            "failed_zero_clause": "ZC3532_3_silent_extra_fixed_point",
            "residual": "C_extra_mass := Pi_M(Q_nonEH+Q_boundary+Q_domain+Q_memory+Q_range+Q_connection)",
            "bound_route": "R11 operator vector plus local fifth-force and PPN maps",
            "arena": "R10/R11/PPN",
            "needed_source_row": "executable non-EH operator coefficient vector or parent no-hair theorem",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PHTB3532_3_reference_worldtube_frame",
            "failed_zero_clause": "ZC3532_5_fixed_worldtube_and_reference",
            "residual": "C_selector := abs(R_ref)+abs(R_W)+abs(R_frame)+abs(R_units)",
            "bound_route": "same-frame source-readout audit against clocks, orbital GM and WEP source charge",
            "arena": "clock/WEP/orbital",
            "needed_source_row": "fixed selector theorem or bounded selector drift per observable",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3532_0_best_route",
            "decision": "Use charge-identified Pi_M as the best route.",
            "rationale": "An independent projector invites tuning; the EH/Hilbert charge route is the least suspicious path to Newton/GR.",
            "effect": "R_PiM becomes a concrete commutator theorem instead of a free closure coefficient.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3532_1_zero_not_live",
            "decision": "Do not claim R_PiM=R_Htau=0 yet.",
            "rationale": "The zero mechanism is sufficient but the current parent action has not signed universal matter, extra-sector silence, fixed worldtube/reference and no symplectic flux.",
            "effect": "local GR remains conditional, but the target is now sharply derivable.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3532_2_next_action",
            "decision": "Build the local EH quotient action kernel next.",
            "rationale": "Proving ZC3532_1-ZC3532_3 would kill the largest Pi_M/Htau obstructions at source rather than bounding them later.",
            "effect": "moves from ledger mode into a parent-action derivation attempt.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3532_0_RPiM",
            "quantity": "R_PiM",
            "value": "conditional_zero_mechanism_found",
            "meaning": "zero follows if Pi_M is the charge-identified EH/Hilbert source functional and vertical MTS fields do not move g_obs/J_H",
            "claim_effect": "not a live Newton/source claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3532_1_RHtau",
            "quantity": "R_Htau",
            "value": "conditional_zero_mechanism_found",
            "meaning": "zero follows if observed-time Hamiltonian integrability and extra-sector no-flux are parent-signed",
            "claim_effect": "not a live local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3532_2_best_route",
            "quantity": "next_best_route",
            "value": "local_EH_quotient_action_kernel",
            "meaning": "prove S_parent reduces locally to EH plus universal matter plus silent extra fields",
            "claim_effect": "routes toward derived GR/Newton rather than another phenomenological bound row",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3533-Y5-R2FR-local-EH-quotient-action-kernel-and-universal-matter-source.md",
            "next_script": "scripts/Y5_R2FR_3533_local_EH_quotient_action_kernel_and_universal_matter_source.py",
            "objective": "Try to write the minimal parent action kernel that makes D_Y g_obs=0, D_Y S_matter=0 and delta H_tau^extra=0 on compact local branches, then test whether it proves the 3532 Pi_M/H_tau double zero.",
            "success_gate": "A parent action clause derives EH plus universal matter plus silent extra fields without inserting local-GR as an axiom; otherwise produce explicit C_PiM/C_Htau bound inputs.",
            "why_next": "3532 found the best zero mechanism but it depends on the local EH quotient and universal-matter clauses.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3532_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_1_charge_identified_PiM_route", "passed": bool_text(any(row["contract_id"] == "ZC3532_4_charge_identified_PiM" for row in contracts) and any(row["decision_id"] == "DEC3532_0_best_route" for row in decisions)), "detail": "Pi_M is routed through EH/Hilbert charge, not an empirical projector", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_2_RPiM_zero_mechanism", "passed": bool_text(any(row["target"] == "R_PiM" and "CONDITIONAL_ZERO" in row["live_verdict"] for row in proofs)), "detail": "R_PiM conditional zero mechanism written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_3_RHtau_zero_mechanism", "passed": bool_text(any(row["target"] == "R_Htau" and "CONDITIONAL_ZERO" in row["live_verdict"] for row in proofs)), "detail": "R_Htau conditional zero mechanism written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_4_bound_fallbacks_exist", "passed": bool_text({"PHTB3532_0_PiM_kernel_drift", "PHTB3532_1_Htau_curl_flux"} <= {row["bound_id"] for row in bounds}), "detail": "Pi_M and H_tau fallback bound rows staged if zero proof fails", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_5_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + contracts + proofs + bounds + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no local-GR/Newton/PPN claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3533-Y5-R2FR-local-EH-quotient")), "detail": "3533 local EH quotient action kernel target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3532_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3532_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3532_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3532 - PiM/Htau Commutator, Integrability Zero, Or Denominator Bound

## Summary
- **Best route found:** make `Pi_M` the mass component of the same Hilbert/Hamiltonian charge, not a separate fitted projector.
- **Conditional double zero:** `R_PiM=0` and `R_Htau=0` follow if the parent action has a local EH quotient, universal matter coupling, silent extra fields, fixed worldtube/reference, and zero symplectic flux.
- **Important move:** this is not just another missing-input note; it gives the exact mechanism that would make the local source denominator behave like GR.
- **Current verdict:** not claim-ready. The mechanism is sufficient, but the current parent action has not signed the required clauses.
- **Next best attack:** build the local EH quotient action kernel and test whether MTS can derive those clauses without smuggling in local GR.

## Zero Mechanism In One Line
If

`S_parent -> S_EH[g_obs] + S_matter[g_obs,psi] + S_silent[Y] + dB`

with `D_Y g_obs=0`, `D_Y S_matter=0`, `delta H_tau^Y=0`, fixed `W_source`, fixed `H_ref`, and vanishing boundary symplectic flux, then

`[D_Y,Pi_M^H]J_H=0` and `curl(delta H_tau)=0`.

That is the cleanest local-GR route: not a plateau axiom, not a fitted GM trick, but a parent-action quotient theorem.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Zero Contract
{markdown_table(contracts, ["contract_id", "clause", "mathematical_form", "needed_for", "current_status", "source_path", "valid_for_claim"])}

## Zero Proof Attempt
{markdown_table(proofs, ["proof_id", "target", "derivation_step", "mathematical_form", "zero_result", "live_verdict", "remaining_obstruction", "valid_for_claim"])}

## Bound Fallbacks
{markdown_table(bounds, ["bound_id", "failed_zero_clause", "residual", "bound_route", "arena", "needed_source_row", "valid_for_claim"])}

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
    contracts = zero_contract_rows()
    proofs = zero_proof_rows()
    bounds = fallback_bound_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3532_SOURCE_REGISTER.csv",
        "zero_contract": OUT / "P8_Y5_R2FR_3532_ZERO_CONTRACT.csv",
        "zero_proof": OUT / "P8_Y5_R2FR_3532_PIM_HTAU_ZERO_PROOF.csv",
        "bound_fallbacks": OUT / "P8_Y5_R2FR_3532_DENOMINATOR_BOUND_FALLBACKS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3532_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3532_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3532_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3532_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["zero_contract"], contracts, ["contract_id", "clause", "mathematical_form", "needed_for", "current_status", "source_path", "valid_for_claim"])
    write_csv(outputs["zero_proof"], proofs, ["proof_id", "target", "derivation_step", "mathematical_form", "zero_result", "live_verdict", "remaining_obstruction", "valid_for_claim"])
    write_csv(outputs["bound_fallbacks"], bounds, ["bound_id", "failed_zero_clause", "residual", "bound_route", "arena", "needed_source_row", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, contracts, proofs, bounds, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, contracts, proofs, bounds, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
