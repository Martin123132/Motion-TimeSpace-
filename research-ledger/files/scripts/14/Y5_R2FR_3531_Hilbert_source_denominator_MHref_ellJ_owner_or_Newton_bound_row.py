from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3531-Y5-R2FR-Hilbert-source-denominator-MHref-ellJ-owner-or-Newton-bound-row.md"
CANONICAL_STATUS = OUT / "P8_local_GR_Hilbert_source_denominator_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3531": {"path": Path(__file__).resolve(), "role": "3531 generator"},
    "doc_3530": {
        "path": ROOT / "3530-Y5-R2FR-kappa-G-source-normalization-and-Newtonian-limit-gate.md",
        "role": "kappa/G Newtonian gate handoff",
    },
    "next_3530": {
        "path": OUT / "P8_Y5_R2FR_3530_NEXT_TARGET.csv",
        "role": "3530-selected Hilbert source denominator target",
    },
    "status_3530": {
        "path": OUT / "P8_local_GR_kappa_G_Newtonian_gate_status.csv",
        "role": "3530 canonical kappa/G Newtonian status",
    },
    "ellj_zero_3513": {
        "path": OUT / "P8_Y5_R2FR_3513_ELLJ_ZERO_PROOF_ATTEMPT.csv",
        "role": "ell_J zero proof and residual law",
    },
    "ellj_square_3513": {
        "path": OUT / "P8_Y5_R2FR_3513_ELLJ_SOURCE_CURRENT_COMMUTING_SQUARE.csv",
        "role": "source-current commuting square",
    },
    "ellj_residual_3513": {
        "path": OUT / "P8_Y5_R2FR_3513_ELLJ_RESIDUAL_LAW.csv",
        "role": "ell_J residual decomposition",
    },
    "mhref_lock_3433": {
        "path": OUT / "P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv",
        "role": "M_H_ref tau/source lock theorem",
    },
    "mhref_audit_3433": {
        "path": OUT / "P8_Y5_R2FR_3433_SAME_FRAME_MHREF_TAU_AUDIT.csv",
        "role": "same-frame M_H_ref tau audit",
    },
    "poisson_3434": {
        "path": OUT / "P8_Y5_R2FR_3434_SOURCE_NORMALIZED_POISSON_LIMIT_THEOREM.csv",
        "role": "source-normalized Poisson limit theorem",
    },
    "mhref_bounds_3446": {
        "path": OUT / "P8_Y5_R2FR_3446_MHREF_DENOMINATOR_BOUND_ROWS.csv",
        "role": "M_H_ref denominator component bound rows",
    },
    "source_norm_3377": {
        "path": OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv",
        "role": "weak-field source normalization theorem",
    },
    "newton_chain_3382": {
        "path": OUT / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
        "role": "Newton source normalization chain",
    },
    "newton_score_2921": {
        "path": OUT / "P8_Y5_R2FR_2921_SOURCE_NORMALIZED_NEWTON_SCORECARD_ROWS.csv",
        "role": "source-normalized Newton scorecard rows",
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


def denominator_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HSD3531_0_definition",
            "claim_piece": "Hilbert source denominator definition",
            "statement": "The Newtonian source mass must be M_H_ref=c^-2(H_tau[S_outer]-H_ref) evaluated with one tau, one observed frame, one fixed reference and no orbital-GM input.",
            "mathematical_form": "rho_H integrates to M_H_ref; mu_obs=G_ref M_H_ref(1+epsilon_mu)",
            "current_status": "DEFINITION_LOCK_CANDIDATE",
            "remaining_gap": "tau/surface/reference/units/source path must be fixed in one source row",
            "source_path": str(SOURCES["mhref_lock_3433"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HSD3531_1_ellJ_commuting_square",
            "claim_piece": "ell_J zero theorem",
            "statement": "If matter variation, Hilbert current, Hamiltonian charge, Pi_M projection, worldtube support and readout form one pre-readout functorial chain, then ell_J has no branch-dependent scale freedom.",
            "mathematical_form": "S_m -> J_H -> H_tau-H_ref -> Pi_M^H(H_tau-H_ref)=M_H_ref -> J_readout",
            "current_status": "CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "remaining_gap": "Pi_M/H_tau/reference/worldtube square is not parent-signed",
            "source_path": str(SOURCES["ellj_zero_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HSD3531_2_residual_identity",
            "claim_piece": "ell_J denominator obstruction vector",
            "statement": "When the square does not close, z_ellJ is the sum of named normalized obstruction terms and no cancellation is credited.",
            "mathematical_form": "z_ellJ=R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units",
            "current_status": "EXACT_RESIDUAL_DECOMPOSITION_READY",
            "remaining_gap": "component zero proofs or numeric bounds remain absent",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HSD3531_3_source_normalized_poisson",
            "claim_piece": "Poisson source denominator",
            "statement": "In the public EH/Hilbert branch, Poisson's equation has the standard coefficient only when rho_H integrates to the same tau-normalized Hamiltonian/Hilbert denominator.",
            "mathematical_form": "nabla^2 Phi=4*pi*G0 rho_H + S_epsilon_mu + S_q_loc + S_domain + S_boundary + S_nonEH",
            "current_status": "CONDITIONAL_SOURCE_NORMALIZATION",
            "remaining_gap": "source-specific M_H_ref row and residual Green/source maps are missing",
            "source_path": str(SOURCES["poisson_3434"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "HSD3531_4_live_verdict",
            "claim_piece": "current MTS source denominator status",
            "statement": "Current MTS has a legitimate EH/Hilbert denominator route but not a full source-normalization lock.",
            "mathematical_form": "source_lock_current=false; epsilon_mu_residual_vector retained",
            "current_status": "DENOMINATOR_NOT_CLAIMED_BUT_NARROWED",
            "remaining_gap": "R_PiM and R_Htau are the highest-pressure algebraic rows",
            "source_path": str(SOURCES["ellj_zero_3513"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def residual_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "HSDR3531_0_M_H_ref",
            "residual": "M_H_ref positive same-frame denominator",
            "formula": "M_H_ref=H_tau[tau_obs,S_outer]-H_ref[S_outer]",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "zero_or_bound_condition": "source-specific row with tau/surface/reference/units/source path and no orbital GM",
            "observable_links": "Newton; orbital_GM; R10 denominator; local GR boundary",
            "source_path": str(SOURCES["mhref_bounds_3446"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "HSDR3531_1_R_PiM",
            "residual": "Pi_M/source-current commutator obstruction",
            "formula": "R_PiM=([D_X,Pi_M^H]J_H + Pi_M^H[D_X,J_H] - D_X Pi_M^H[J_H])/Pi_M^H[J_H]",
            "current_status": "RETAINED_PROJECTOR_OBSTRUCTION",
            "zero_or_bound_condition": "Pi_M fixed-variable list, source support and Hodge/domain data are parent-owned",
            "observable_links": "Newton source mass; PPN; R10 Qbar_XH; orbital_GM",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "HSDR3531_2_R_Htau",
            "residual": "H_tau non-integrability/source-charge curl",
            "formula": "R_Htau=normalized curl(delta H_tau)=normalized integral_S i_tau omega_total plus exact/boundary terms",
            "current_status": "INTEGRABILITY_CURL_NOT_CLAIM_READY",
            "zero_or_bound_condition": "parent L_X, theta_X, omega_X, tau/surface lock and boundary exactness are signed",
            "observable_links": "Gdot; Newton source mass; PPN; clocks",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "HSDR3531_3_R_ref",
            "residual": "source-blind reference failure",
            "formula": "R_ref=D_X H_ref/(H_tau-H_ref)",
            "current_status": "REFERENCE_SELECTOR_UNSIGNED",
            "zero_or_bound_condition": "H_ref depends only on boundary/topology/stationarity/asymptotic coframe data",
            "observable_links": "Gdot; orbital_GM; R10 denominator; local GR boundary",
            "source_path": str(SOURCES["mhref_lock_3433"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "HSDR3531_4_R_W",
            "residual": "worldtube support/domain selector drift",
            "formula": "R_W=D_X ln int_W_source rho_H dV_H - D_X ln int_closure(supp J_H[tau]) rho_H dV_H",
            "current_status": "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED",
            "zero_or_bound_condition": "W_source is exactly closure(supp J_H[tau]) on parent-owned Hamiltonian slice",
            "observable_links": "Newton source; R10 source support; WEP/source composition",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "HSDR3531_5_R_frame_units",
            "residual": "same-frame/readout/unit source mismatch",
            "formula": "R_frame+R_units from source readout frame and duplicate source-unit convention",
            "current_status": "PARALLEL_PRODUCT_FACTOR_RETAINED",
            "zero_or_bound_condition": "same observed coframe/tau/source/orbit/clock/reference branch fixed before readout",
            "observable_links": "clock; PPN; orbital_GM; Gdot",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "component_id": "HSDR3531_6_total",
            "residual": "epsilon_Htau_denominator_abs / z_ellJ total",
            "formula": "sum_abs(R_md,R_Ward,R_PiM,R_Htau,R_ref,R_W,R_frame,R_units plus H_tau denominator terms)",
            "current_status": "MISSING_COMPONENT_VALUES_TOTAL_NONCLAIM",
            "zero_or_bound_condition": "all components theorem-zero or source-backed numeric rows with no cancellation",
            "observable_links": "Newton; PPN; Gdot; R10; WEP",
            "source_path": str(SOURCES["mhref_bounds_3446"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def bound_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "HSDB3531_0_Gdot_denominator",
            "residual": "D_t ln M_H_ref or z_ellJ time component",
            "arena": "LLR/Gdot",
            "bound_value": "9.6e-15",
            "units": "yr^-1",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R9_Gdot",
            "prediction_needed": "D_t ln M_H_ref, D_t z_ellJ or theorem-zero of all time components",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HSDB3531_1_WEP_source_denominator",
            "residual": "species/source denominator mismatch",
            "arena": "MICROSCOPE/WEP",
            "bound_value": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R1_WEP_source_charge",
            "prediction_needed": "species/material projection of R_md, R_W, R_frame and source current mismatch",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HSDB3531_2_orbital_GM_guard",
            "residual": "epsilon_mu no-GM-laundering",
            "arena": "orbital/Newton source amplitude",
            "bound_value": "MISSING_NEWTON_PPN_MATCH_BOUND",
            "units": "dimensionless",
            "source_path": str(SOURCES["newton_score_2921"]["path"]),
            "source_row": "SN2921_9_total_guard",
            "prediction_needed": "epsilon_mu row with independent M_H_ref and G_ref calibration",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HSDB3531_3_R10_denominator",
            "residual": "range/source support denominator",
            "arena": "R10 inverse-square/fifth-force",
            "bound_value": "alpha(lambda)",
            "units": "range-dependent",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R10_fifth_force",
            "prediction_needed": "R_W/R_PiM source support and Qbar denominator projection",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "HSDB3531_4_PPN_source_vector",
            "residual": "PPN source-normalization vector",
            "arena": "Cassini/LLR/pulsar/planetary",
            "bound_value": "componentwise",
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]["path"]),
            "source_row": "R3_gamma;R4_beta;R5_alpha1;R6_alpha2;R8_xi",
            "prediction_needed": "map denominator residuals into full PPN vector, no gamma-only shortcut",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3531_0_denominator_not_claimed",
            "decision": "do not claim M_H_ref/ell_J/source denominator is owned",
            "rationale": "same-frame source row and Pi_M/H_tau/reference/worldtube commuting square are unsigned",
            "effect": "Newton/Poisson remains conditional",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3531_1_target_RPiM_RHtau",
            "decision": "attack R_PiM and R_Htau next",
            "rationale": "3513 identifies them as the algebraic heart of the denominator obstruction",
            "effect": "moves from broad source-normalization gap to two concrete proof/bound rows",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3531_2_no_GM_laundering",
            "decision": "keep orbital GM as readout/test only",
            "rationale": "using GM to define M_H_ref would hide the residual being tested",
            "effect": "preserves Newtonian derivation discipline",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3531_0_denominator",
            "quantity": "Hilbert_source_denominator",
            "value": "conditional_definition_not_claimed",
            "meaning": "M_H_ref is defined but not yet supplied as a positive same-frame source row",
            "claim_effect": "no Newton/Poisson pass",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3531_1_ellJ",
            "quantity": "ell_J",
            "value": "exact_residual_decomposition_ready",
            "meaning": "z_ellJ is reduced to named obstruction terms rather than a vague coupling gap",
            "claim_effect": "source-current owner not yet proven",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3531_2_next",
            "quantity": "next_best_target",
            "value": "PiM_Htau_commutator_and_integrability_gate",
            "meaning": "R_PiM and R_Htau should be proved zero or bounded first",
            "claim_effect": "moves toward actual Newton source denominator",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3532-Y5-R2FR-PiM-Htau-commutator-integrability-zero-or-denominator-bound.md",
            "next_script": "scripts/Y5_R2FR_3532_PiM_Htau_commutator_integrability_zero_or_denominator_bound.py",
            "objective": "Try to prove or bound the two algebraic heart rows of the Hilbert denominator: R_PiM and R_Htau. If they do not vanish, create explicit denominator bound inputs for Newton/PPN/Gdot/R10.",
            "success_gate": "Either Pi_M commutes with the source-current/H_tau chain and H_tau is integrable on the source branch, or both residuals receive source-backed units, components and arena projections.",
            "why_next": "3531 reduces source normalization to the Pi_M/H_tau/reference/worldtube square; R_PiM and R_Htau are the highest-pressure rows.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3531_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_1_denominator_defined_not_claimed", "passed": bool_text(any(row["theorem_id"] == "HSD3531_0_definition" for row in theorems) and any(row["quantity"] == "Hilbert_source_denominator" and row["value"] == "conditional_definition_not_claimed" for row in status)), "detail": "M_H_ref denominator defined but not claimed", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_2_ellJ_residual_decomposition", "passed": bool_text(any(row["theorem_id"] == "HSD3531_2_residual_identity" and "R_PiM" in row["mathematical_form"] for row in theorems)), "detail": "z_ellJ residual decomposition present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_3_RPiM_RHtau_present", "passed": bool_text({"HSDR3531_1_R_PiM", "HSDR3531_2_R_Htau"} <= {row["component_id"] for row in residuals}), "detail": "R_PiM and R_Htau component rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_4_bound_rows_staged", "passed": bool_text(any(row["bound_id"] == "HSDB3531_0_Gdot_denominator" and row["bound_value"] == "9.6e-15" for row in bounds) and any(row["bound_id"] == "HSDB3531_2_orbital_GM_guard" for row in bounds)), "detail": "Gdot denominator and no-GM-laundering rows staged", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_5_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + theorems + residuals + bounds + status) and all(row["claim_allowed"] == "False" for row in decisions + next_rows)), "detail": "no Newton/source-denominator claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_6_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3532-Y5-R2FR-PiM-Htau")), "detail": "3532 PiM-Htau target selected", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3531_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3531_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3531_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3531 - Hilbert Source Denominator, MHref/ellJ Owner, Or Newton Bound Row

## Summary
- **Denominator target:** Newton must use `M_H_ref=c^-2(H_tau[S_outer]-H_ref)` from the same Hilbert/Hamiltonian source branch, not an orbital `GM` backfill.
- **ell_J sharpened:** the source-current normalization gap is now `z_ellJ=R_md+R_Ward+R_PiM+R_Htau+R_ref+R_W+R_frame+R_units`.
- **Current verdict:** `M_H_ref` and `ell_J` are exact conditional routes, not live claims. The positive same-frame source row is still missing.
- **Highest-pressure rows:** `R_PiM` and `R_Htau`; these decide whether the projected Hilbert source and Hamiltonian charge denominator commute/integrate.
- **No Newton claim:** Poisson/Newton remains conditional until denominator, source support, reference, frame and PPN residual rows close.

## Denominator Target
`M_H_ref := c^-2 (H_tau[S_outer] - H_ref)`

`rho_H` must integrate to this same object before

`nabla^2 Phi = 4*pi*G_ref rho_H`

can be claimed.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Denominator Theorem
{markdown_table(theorems, ["theorem_id", "claim_piece", "statement", "mathematical_form", "current_status", "remaining_gap", "source_path", "valid_for_claim"])}

## Residual Components
{markdown_table(residuals, ["component_id", "residual", "formula", "current_status", "zero_or_bound_condition", "observable_links", "source_path", "valid_for_claim"])}

## Bound Rows
{markdown_table(bounds, ["bound_id", "residual", "arena", "bound_value", "units", "source_path", "source_row", "prediction_needed", "score_ready", "valid_for_claim"])}

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
    theorems = denominator_theorem_rows()
    residuals = residual_component_rows()
    bounds = bound_row_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3531_SOURCE_REGISTER.csv",
        "denominator_theorem": OUT / "P8_Y5_R2FR_3531_DENOMINATOR_THEOREM.csv",
        "residual_components": OUT / "P8_Y5_R2FR_3531_RESIDUAL_COMPONENTS.csv",
        "bound_rows": OUT / "P8_Y5_R2FR_3531_NEWTON_DENOMINATOR_BOUND_ROWS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3531_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3531_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3531_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3531_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["denominator_theorem"], theorems, ["theorem_id", "claim_piece", "statement", "mathematical_form", "current_status", "remaining_gap", "source_path", "valid_for_claim"])
    write_csv(outputs["residual_components"], residuals, ["component_id", "residual", "formula", "current_status", "zero_or_bound_condition", "observable_links", "source_path", "valid_for_claim"])
    write_csv(outputs["bound_rows"], bounds, ["bound_id", "residual", "arena", "bound_value", "units", "source_path", "source_row", "prediction_needed", "score_ready", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, theorems, residuals, bounds, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, theorems, residuals, bounds, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
