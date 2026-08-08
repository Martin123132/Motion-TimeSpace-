from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3512-Y5-R2FR-product-lock-factor-vector-ellJ-Rframe-or-Gdot-runner.md"
CANONICAL_PRODUCT_VECTOR = OUT / "P8_EM_product_lock_factor_vector_ellJ_Rframe.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3512": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3511": {
        "path": ROOT / "3511-Y5-R2FR-fixed-kappa-Gref-action-line-lock-or-Gdot-Newton-bound.md",
        "role": "3511 kappa/Gref product-lock handoff",
    },
    "residual_3511": {
        "path": OUT / "P8_EM_fixed_kappa_Gref_action_line_lock.csv",
        "role": "3511 product-lock residual vector",
    },
    "theorem_3511": {
        "path": OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_ACTION_LINE_LOCK_THEOREM.csv",
        "role": "3511 kappa/Gref theorem stack",
    },
    "ellj_audit_2932": {
        "path": OUT / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv",
        "role": "kappa/ellJ constant proof audit",
    },
    "ellj_source_audit_2934": {
        "path": OUT / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv",
        "role": "ellJ owner/source-current audit",
    },
    "ellj_theorem_2937": {
        "path": OUT / "P8_Y5_R2FR_2937_ELLJ_OWNER_THEOREM_ATTEMPT.csv",
        "role": "ellJ owner theorem attempt",
    },
    "ellj_reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "MHref/ellJ/reference lock contract",
    },
    "frame_audit_1519": {
        "path": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "role": "observed coframe/tau source frame audit",
    },
    "coframe_theorem_1739": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_THEOREM_ATTEMPT.csv",
        "role": "parent coframe ownership theorem attempt",
    },
    "frame_readout_1926": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1926_OBSERVED_FRAME_READOUT_CONTRACT.csv",
        "role": "observed frame readout contract",
    },
    "frame_split_row": {
        "path": OUT / "P8_frame_source_split_residual_or_zero.csv",
        "role": "frame/source split residual row",
    },
    "reference_lock_3427": {
        "path": OUT / "P8_Y5_R2FR_3427_REFERENCE_LOCK_THEOREM.csv",
        "role": "reference lock theorem",
    },
    "reference_attempt_548": {
        "path": OUT / "P8_Y5_BRR545_REFERENCE_LOCK_THEOREM_ATTEMPT.csv",
        "role": "reference lock theorem attempt",
    },
    "reference_audit": {
        "path": OUT / "P8_Y5_BOUNDARY_REFERENCE_THEOREM_ZERO_AUDIT.csv",
        "role": "boundary reference theorem-zero audit",
    },
    "integrability_reference_910": {
        "path": OUT / "P8_Y5_R10_910_INTEGRABILITY_REFERENCE_CONTRACT.csv",
        "role": "integrability/reference contract",
    },
    "gdot_gate_2933": {
        "path": OUT / "P8_Y5_R2FR_2933_DOTG_KAPPA_PROJECTION_GATE.csv",
        "role": "finite dotG/kappa projection gate",
    },
    "kappa_bound_3511": {
        "path": OUT / "P8_Y5_R2FR_3511_KAPPA_GREF_BOUND_INPUT_TEMPLATE.csv",
        "role": "3511 kappa/Gref bound input template",
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


def factor_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PLF3512_0_product_identity",
            "claim_piece": "full local coupling product",
            "statement": "The local Newton/Gdot/source coupling gate is the logarithmic derivative of the whole product, not any single factor.",
            "mathematical_form": "D_X ln G_eff = D_X ln G_ref + D_X ln w_common + D_X ln ell_J + D_X ln R_frame + D_X ln C_extra",
            "derivation": "Linearized EH supplies the left coupling; ordinary matter/action scale supplies w_common; the Hilbert/worldtube source current supplies ell_J; same-frame/reference/readout supplies R_frame; retained extra sectors supply C_extra.",
            "payoff": "prevents closing local GR by proving only kappa or only Ward conservation",
            "gap": "each product factor still needs parent signature or numeric bound rows",
            "status": "EXACT_PRODUCT_BOOKKEEPING_IDENTITY",
            "source_path": str(SOURCES["theorem_3511"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PLF3512_1_ellJ_zero_route",
            "claim_piece": "ell_J source-current normalization",
            "statement": "ell_J is zero-derivative only if the same Hilbert/worldtube source current is extracted from the same matter action before readout and used by stress, H_tau, Pi_M and Newton source mass.",
            "mathematical_form": "J_H := delta S_matter/delta e_obs . L_tau e_obs; D_X ln ell_J=0 if J_H,T_H,H_tau,Pi_M all use this pre-readout branch",
            "derivation": "A single variational source-current owner leaves no later scale slot for ell_J; otherwise measured GM or reference choices can absorb source-current drift.",
            "payoff": "would remove delta_ellJ from Gdot/Newton/PPN source coupling",
            "gap": "matter descent, Pi_M commutator, H_ref lock and source worldtube glue are not jointly parent-signed",
            "status": "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "source_path": str(SOURCES["ellj_theorem_2937"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PLF3512_2_Rframe_zero_route",
            "claim_piece": "same-frame/reference readout normalization",
            "statement": "R_frame is zero-derivative only if matter, source support, clocks, orbit/readout, boundary reference and Hamiltonian time generator all use the same observed coframe/tau branch fixed before readout.",
            "mathematical_form": "R_frame=1 and D_X ln R_frame=0 if e_obs=E(q(Phi)), tau=tau(q(Phi)), H_ref=H_ref[boundary_class] and no shadow/source frame enters",
            "derivation": "A common observed frame functor kills representative-frame drift, but only after parent q, coframe ownership, tau lock, and reference rule are signed.",
            "payoff": "would remove frame/source calibration split from Gdot/Newton/clock rows",
            "gap": "parent coframe/tau/reference ownership remains conditional",
            "status": "CONDITIONAL_FRAME_LOCK_NOT_LIVE",
            "source_path": str(SOURCES["frame_audit_1519"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PLF3512_3_reference_no_laundering",
            "claim_piece": "reference anti-absorption",
            "statement": "H_ref and boundary/reference subtraction must be fixed by the parent branch; it may not absorb source-current, frame or measured-GM drift.",
            "mathematical_form": "partial_{source,r,t,frame,lambda} H_ref = 0, with H_ref selected before source/readout fitting",
            "derivation": "A fixed reference functional contributes no source derivative; a chosen-after-fit reference is just another hidden calibration knob.",
            "payoff": "blocks measured-GM laundering of ell_J/R_frame residuals",
            "gap": "reference rule and integrability/phase-space boundary conditions are not fully parent-owned",
            "status": "EXACT_IF_REFERENCE_BRANCH_SIGNED",
            "source_path": str(SOURCES["reference_lock_3427"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PLF3512_4_finite_runner_interface",
            "claim_piece": "Gdot product runner",
            "statement": "If product factors are not zero-derived, use finite Gdot/Newton/clock comparators as non-claim runner rows.",
            "mathematical_form": "|D_t ln(G_ref*w_common*ell_J*R_frame*C_extra)| <= 4.0e-14 yr^-1 for the carried Gdot comparator",
            "derivation": "The bound side exists, but prediction rows remain blocked until each factor has a sourced value/projection.",
            "payoff": "turns the product-lock problem into an executable non-claim pipeline",
            "gap": "prediction values for ell_J, R_frame and C_extra are missing",
            "status": "BOUND_INTERFACE_READY_PREDICTION_BLOCKED",
            "source_path": str(SOURCES["gdot_gate_2933"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "PLF3512_5_verdict",
            "claim_piece": "3512 status",
            "statement": "The product-lock route is now factorized: kappa/G_ref, w_common, ell_J, R_frame and C_extra are separate no-cancellation factors.",
            "mathematical_form": "Z_product_X := z_G + z_w + z_ellJ + z_R + z_extra; claim requires each term zero-owned or bound-scored without cancellation credit",
            "derivation": "Combine 3511 product identity with ellJ owner, coframe/tau, reference-lock and Gdot projection evidence.",
            "payoff": "local GR/Newton coupling closure becomes a finite factor list, not a vague missing coupling",
            "gap": "ell_J and R_frame are now the highest-pressure unsolved factors",
            "status": "FACTOR_VECTOR_CONSTRUCTED_NOT_CLAIMED",
            "source_path": str(SOURCES["residual_3511"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def factor_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PLFV3512_0_z_G",
            "factor": "z_G",
            "definition": "D_X ln G_ref or D_X ln kappa_eff",
            "status": "conditional zero from superselection/topological route if parent-adopted",
            "zero_condition": "fixed parent kappa/Gref sector",
            "observable_links": "Gdot; Newton; R10; PPN",
            "next_action": "keep 3511 kappa route or bound delta_kappa",
            "claim_allowed": "False",
        },
        {
            "row_id": "PLFV3512_1_z_w",
            "factor": "z_w",
            "definition": "D_X ln w_common",
            "status": "universal action/source scale residual from 3510",
            "zero_condition": "fixed common action-density line/hbar/measure owner",
            "observable_links": "Gdot; Newton_GM; clocks",
            "next_action": "derive common action line or bound universal source scale",
            "claim_allowed": "False",
        },
        {
            "row_id": "PLFV3512_2_z_ellJ",
            "factor": "z_ellJ",
            "definition": "D_X ln ell_J",
            "status": "source-current normalization factor retained",
            "zero_condition": "same Hilbert/worldtube source current before readout",
            "observable_links": "Newton; WEP; PPN; orbital_GM; Gdot",
            "next_action": "derive ellJ owner via J_H/H_tau/Pi_M/H_ref chain",
            "claim_allowed": "False",
        },
        {
            "row_id": "PLFV3512_3_z_Rframe",
            "factor": "z_Rframe",
            "definition": "D_X ln R_frame",
            "status": "same-frame/reference/readout factor retained",
            "zero_condition": "observed coframe/tau/source/orbit/clock/reference all fixed by same q branch",
            "observable_links": "clock; PPN; orbital_GM; Gdot",
            "next_action": "derive common-frame/reference lock or bound frame split",
            "claim_allowed": "False",
        },
        {
            "row_id": "PLFV3512_4_z_extra",
            "factor": "z_extra",
            "definition": "D_X ln C_extra for boundary/projector/non-Hilbert/local MTS source terms",
            "status": "retained explicit extra-sector gate",
            "zero_condition": "extra-sector stress/source currents are exact zero-flux improvements or separately bounded",
            "observable_links": "PPN; R10; Newton; boundary_flux",
            "next_action": "keep no-cancellation residual rows",
            "claim_allowed": "False",
        },
        {
            "row_id": "PLFV3512_5_Z_product",
            "factor": "Z_product",
            "definition": "D_X ln(G_ref*w_common*ell_J*R_frame*C_extra)",
            "status": "no-cancellation product-lock residual",
            "zero_condition": "all factor rows are independently zero-owned or numerically below bounds",
            "observable_links": "Gdot; Newton; PPN; clocks; R10",
            "next_action": "make prediction-side product rows executable",
            "claim_allowed": "False",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PLBIN3512_0_Gdot_product",
            "arena": "Gdot/time drift",
            "factor": "Z_product",
            "predicted_value": "MISSING_Z_PRODUCT_TIME",
            "predicted_units": "yr^-1",
            "bound_value": "4.0e-14",
            "bound_units": "yr^-1",
            "source_path": str(SOURCES["gdot_gate_2933"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PLBIN3512_1_ellJ",
            "arena": "source-current normalization",
            "factor": "z_ellJ",
            "predicted_value": "MISSING_DLN_ELLJ",
            "predicted_units": "dimensionless_or_derivative",
            "bound_value": "MISSING_ELLJ_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["ellj_reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PLBIN3512_2_Rframe",
            "arena": "same-frame/reference readout",
            "factor": "z_Rframe",
            "predicted_value": "MISSING_DLN_RFRAME",
            "predicted_units": "dimensionless_or_derivative",
            "bound_value": "MISSING_FRAME_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["frame_split_row"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PLBIN3512_3_reference",
            "arena": "boundary/reference lock",
            "factor": "reference_derivative",
            "predicted_value": "MISSING_DLN_HREF_OR_DELTA_REF",
            "predicted_units": "dimensionless_or_charge_units",
            "bound_value": "MISSING_REFERENCE_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["integrability_reference_910"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PLBIN3512_4_clock_frame",
            "arena": "clock/frame product",
            "factor": "z_Rframe_or_clock",
            "predicted_value": "MISSING_CLOCK_FRAME_PROJECTION",
            "predicted_units": "yr^-1",
            "bound_value": "MISSING_CLOCK_FRAME_BOUND",
            "bound_units": "yr^-1",
            "source_path": str(SOURCES["frame_readout_1926"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def run_bound_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
            verdict = "PASS_NUMERIC_PRODUCT_LOCK_BOUND" if passes == "True" else "FAIL_NUMERIC_PRODUCT_LOCK_BOUND"
        results.append(
            {
                "row_id": row["row_id"].replace("PLBIN", "PLRUN"),
                "arena": row["arena"],
                "factor": row["factor"],
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
            "decision_id": "DEC3512_0_factorization_gain",
            "decision": "The local coupling gate is now a no-cancellation factor vector.",
            "rationale": "This prevents closing the theory by proving only kappa, only common action scale, or only Ward conservation.",
            "effect": "Each factor must be zero-owned or bounded independently.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3512_1_ellJ_priority",
            "decision": "ell_J is the next strongest derivation target.",
            "rationale": "It directly connects matter variation, Hilbert source, Hamiltonian mass, Pi_M and Newton normalization.",
            "effect": "Next work should try to close J_H/H_tau/Pi_M/H_ref as one source-current owner.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3512_2_Rframe_parallel_gate",
            "decision": "R_frame remains a parallel same-frame/reference gate.",
            "rationale": "Even a perfect ell_J proof can be laundered by frame/reference drift if e_obs/tau/H_ref are not parent-fixed.",
            "effect": "Frame/reference rows stay in the product vector and cannot be absorbed into measured GM.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3513-Y5-R2FR-ellJ-source-current-owner-JH-Htau-PiM-Href-or-bound.md",
            "next_script": "scripts/Y5_R2FR_3513_ellJ_source_current_owner_JH_Htau_PiM_Href_or_bound.py",
            "objective": "Try to derive ell_J=constant from one source-current owner linking J_H, T_H, H_tau, Pi_M, H_ref and M_H before readout; if not, make ell_J prediction-side bound rows executable.",
            "success_gate": "Either D_X ln ell_J=0 is parent-signed for source/orbit/clock frames, or ell_J gets sourced non-claim bound rows for Gdot/Newton/PPN/orbital arenas.",
            "forbidden_shortcuts": "Do not absorb ell_J into measured GM or H_ref; do not rely on Ward conservation without Pi_M/H_tau/reference ownership.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_ids = {row["theorem_id"] for row in theorem_rows}
    factor_names = {row["factor"] for row in factors}
    all_claim_false = all(
        row.get("valid_for_claim") == "False"
        for table in [sources, theorem_rows, bound_inputs, runner_results, decisions, next_rows]
        for row in table
    ) and all(row.get("claim_allowed") == "False" for row in factors)
    all_blocked = all("BLOCKED" in row["runner_verdict"] for row in runner_results)
    finite_gdot_bound = any(row["row_id"] == "PLBIN3512_0_Gdot_product" and parse_float(str(row["bound_value"])) for row in bound_inputs)
    validation = [
        {
            "check_id": "VAL3512_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_1_theorem_stack_present",
            "passed": bool_text({"PLF3512_0_product_identity", "PLF3512_1_ellJ_zero_route", "PLF3512_2_Rframe_zero_route"}.issubset(theorem_ids)),
            "detail": "product, ellJ, and Rframe theorem routes written",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_2_factor_vector_complete",
            "passed": bool_text({"z_G", "z_w", "z_ellJ", "z_Rframe", "z_extra", "Z_product"}.issubset(factor_names)),
            "detail": "product-lock factor vector complete",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_3_finite_Gdot_interface",
            "passed": bool_text(finite_gdot_bound),
            "detail": "finite Gdot bound carried as non-claim product interface",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_4_bound_runner_blocks_placeholders",
            "passed": bool_text(all_blocked),
            "detail": "all product factor rows remain blocked until prediction inputs are valid",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_5_no_claim_flags",
            "passed": bool_text(all_claim_false),
            "detail": "no 3512 output row is valid_for_claim=True or claim_allowed=True",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_6_next_target_ellJ",
            "passed": bool_text(next_rows[0]["next_doc"].startswith("3513") and "ell_J" in next_rows[0]["objective"]),
            "detail": "ellJ source-current owner selected next",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3512_7_formalization_workbench_not_targeted",
            "passed": bool_text(FORMALIZATION.exists() and str(DOC).startswith(str(ROOT))),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        },
    ]
    validation.append(
        {
            "check_id": "VAL3512_SUMMARY",
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
    theorem_rows: list[dict[str, Any]],
    factors: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3512 - Product-Lock Factor Vector: ellJ/Rframe Or Gdot Runner",
                "",
                "## Summary",
                "- **Derived gain:** the local coupling gate is now factorized as `D_X ln(G_ref*w_common*ell_J*R_frame*C_extra)`.",
                "- **ell_J route:** `ell_J` can be zero only if `J_H`, `T_H`, `H_tau`, `Pi_M`, `H_ref`, and `M_H` are one pre-readout source-current branch.",
                "- **R_frame route:** frame/reference drift is zero only if `e_obs`, `tau`, source support, clocks, orbit readout, and `H_ref` are fixed by the same observed branch.",
                "- **No claim yet:** finite `Gdot` is carried as a bound interface, but prediction rows remain blocked until factor values or zero theorems exist.",
                "",
                "## Product-Lock Theorem Stack",
                markdown_table(
                    theorem_rows,
                    ["theorem_id", "claim_piece", "statement", "mathematical_form", "payoff", "gap", "status"],
                ),
                "",
                "## Factor Vector",
                markdown_table(
                    factors,
                    ["row_id", "factor", "definition", "status", "zero_condition", "observable_links", "claim_allowed"],
                ),
                "",
                "## Bound Input Template",
                markdown_table(
                    bound_inputs,
                    ["row_id", "arena", "factor", "predicted_value", "bound_value", "source_path", "valid_for_claim"],
                ),
                "",
                "## Runner Results",
                markdown_table(
                    runner_results,
                    ["row_id", "arena", "factor", "pass_condition", "runner_verdict", "passes_bound", "claim_allowed"],
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
    theorem_rows = factor_theorem_rows()
    factors = factor_rows()
    bound_inputs = bound_input_rows()
    runner_results = run_bound_rows(bound_inputs)
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation_rows = validate(sources, theorem_rows, factors, bound_inputs, runner_results, decisions, next_rows)

    write_csv(OUT / "P8_Y5_R2FR_3512_SOURCE_REGISTER.csv", sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        OUT / "P8_Y5_R2FR_3512_PRODUCT_LOCK_THEOREM_STACK.csv",
        theorem_rows,
        ["theorem_id", "claim_piece", "statement", "mathematical_form", "derivation", "payoff", "gap", "status", "source_path", "valid_for_claim"],
    )
    factor_fields = [
        "row_id",
        "factor",
        "definition",
        "status",
        "zero_condition",
        "observable_links",
        "next_action",
        "claim_allowed",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3512_PRODUCT_LOCK_FACTOR_VECTOR.csv", factors, factor_fields)
    write_csv(CANONICAL_PRODUCT_VECTOR, factors, factor_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3512_PRODUCT_LOCK_BOUND_INPUT_TEMPLATE.csv",
        bound_inputs,
        ["row_id", "arena", "factor", "predicted_value", "predicted_units", "bound_value", "bound_units", "source_path", "valid_for_claim"],
    )
    runner_fields = [
        "row_id",
        "arena",
        "factor",
        "predicted_value",
        "bound_value",
        "pass_condition",
        "runner_verdict",
        "passes_bound",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3512_PRODUCT_LOCK_BOUND_RUNNER_RESULTS.csv", runner_results, runner_fields)
    write_csv(OUT / "P8_EM_product_lock_bound_runner_results.csv", runner_results, runner_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3512_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "rationale", "effect", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3512_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_BRR545_3512_VALIDATION.csv", validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(theorem_rows, factors, bound_inputs, runner_results, decisions, next_rows, validation_rows)


if __name__ == "__main__":
    main()
