from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md"
NEXT_TARGET = "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md"
STATUS = "Y5_R10_789_palatini_tetrad_GR_Newton_limit_contract_written_MTS_exchange_residuals_explicit_nonclaim"
CLAIM_CEILING = "conditional_GR_Newton_limit_contract_only_no_parent_derivation_of_tetrad_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_789_SOURCE_REGISTER.csv"
GR_LIMIT_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_789_PALATINI_TETRAD_GR_LIMIT_CONTRACT.csv"
VARIATION_WARD_PATH = RESIDUALS / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv"
NEWTON_PPN_PATH = RESIDUALS / "P8_Y5_R10_789_NEWTON_PPN_RESIDUAL_VECTOR.csv"
MTS_INPUTS_PATH = RESIDUALS / "P8_Y5_R10_789_MTS_EXCHANGE_INPUT_REQUIREMENTS.csv"
BRANCH_DECISION_PATH = RESIDUALS / "P8_Y5_R10_789_BRANCH_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_789_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_789_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_789_LOCAL_GR_PROOF_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_789_NEWTON_LIMIT_PROOF_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_789_ADOPTED_TETRAD_ACTION.csv",
    RESIDUALS / "P8_Y5_R10_789_PPN_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    GR_LIMIT_CONTRACT_PATH,
    VARIATION_WARD_PATH,
    NEWTON_PPN_PATH,
    MTS_INPUTS_PATH,
    BRANCH_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "788_doc": {
        "path": POST_CHECKPOINT / "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md",
        "needles": ["Current result", "Palatini/tetrad"],
        "role": "immediate 789 handoff",
    },
    "788_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_788_VALIDATION.csv",
        "needles": ["V788_5_palatini_selected", "V788_12_next_target_selected"],
        "role": "prior validation guard",
    },
    "788_contracts": {
        "path": RESIDUALS / "P8_Y5_R10_788_PARENT_ACTION_CONTRACT_CANDIDATES.csv",
        "needles": ["PAC788_0_palatini_tetrad_contract", "least_suspicious_local_GR_route"],
        "role": "selected action contract input",
    },
    "785_contract": {
        "path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_4_connection_from_coframe", "PMC785_7_GR_Newton_reduction"],
        "role": "coframe/connection and GR/Newton requirement",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["Einstein-Equation Convention", "Q^"],
        "role": "Einstein and exchange convention",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["MTS parent theory -> effective GR", "GR weak field -> Newtonian gravity"],
        "role": "unification spine limit chain",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "local GR-limit demand",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def gr_limit_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PTG789_0_field_content",
            "statement": "Use coframe e^a, spin connection omega^{ab}, MTS fields Phi_MTS, matter fields Psi, and owned gauge fields.",
            "condition": "e is invertible and Lorentzian; omega is independent before variation",
            "derived_if_condition_holds": "metric g_mu_nu = eta_ab e^a_mu e^b_nu and a standard local frame for matter",
            "missing_before_claim": "parent derivation or justified adoption of e/Phi_MTS field content",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PTG789_1_action_form",
            "statement": "S = (1/2 kappa_GR) integral epsilon_abcd e^a wedge e^b wedge R^{cd}[omega] + S_MTS[e,omega,Phi_MTS] + S_matter[e,omega,Psi] + S_boundary.",
            "condition": "all non-EH terms are covariant and their variations define stress, spin, and exchange currents",
            "derived_if_condition_holds": "a local GR-compatible variational arena",
            "missing_before_claim": "explicit S_MTS and source/boundary terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PTG789_2_connection_equation",
            "statement": "delta_omega S gives torsion equation; if spin/MTS torsion sources vanish locally, T^a=0 and omega=omega[e].",
            "condition": "tau_spin + tau_MTS_torsion -> 0 or is bounded below local tests",
            "derived_if_condition_holds": "Levi-Civita/spin connection and no hidden torsion force",
            "missing_before_claim": "MTS torsion-source calculation or empirical bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PTG789_3_coframe_equation",
            "statement": "delta_e S gives Einstein equation G_mu_nu = kappa_GR (T_matter_mu_nu + T_MTS_mu_nu + T_boundary_mu_nu) after omega=omega[e].",
            "condition": "stress tensors are symmetric/equivalent after spin terms and boundary pieces are handled",
            "derived_if_condition_holds": "GR with explicit MTS effective stress",
            "missing_before_claim": "T_MTS decomposition and local suppression theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PTG789_4_GR_recovery",
            "statement": "Local GR is recovered when T_MTS, torsion source, nonmetricity source, boundary source, and matter-frame leakage are zero or below local bounds.",
            "condition": "R_local = {T_MTS, Q_nu, torsion, boundary, b_g/c_g, W_Ic} -> 0 in the local regime",
            "derived_if_condition_holds": "Einstein equation for ordinary matter in the tested local domain",
            "missing_before_claim": "component-by-component suppression or bound rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PTG789_5_Newton_recovery",
            "statement": "In the weak-field, slow-motion, quasi-static limit of the recovered GR equation, Poisson/Newton follows.",
            "condition": "g_00 = -1 - 2 Phi_N/c^2, pressure/stress small, v << c, residual vector below PPN/orbital bounds",
            "derived_if_condition_holds": "GR -> Newton link is standard once PTG789_4 closes",
            "missing_before_claim": "PPN residual vector and local source model",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def variation_ward_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "VWI789_0_local_Lorentz",
            "identity_or_variation": "local Lorentz invariance",
            "result": "requires spin/torsion accounting",
            "meaning": "antisymmetric stress and spin current must be zero, improved, or carried by torsion",
            "missing": "spin/torsion source ledger for MTS and matter",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VWI789_1_diffeomorphism",
            "identity_or_variation": "diffeomorphism invariance",
            "result": "total conservation conditional",
            "meaning": "nabla_mu(T_matter+T_MTS+T_boundary)^mu_nu=0 when field equations hold",
            "missing": "explicit covariant S_MTS and boundary variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VWI789_2_exchange_current",
            "identity_or_variation": "matter/MTS split",
            "result": "Q_nu_allowed_but_must_cancel_total",
            "meaning": "nabla T_matter = Q and nabla T_MTS = -Q is allowed, but Q must vanish or be bounded for local GR matter conservation",
            "missing": "Q_nu decomposition connected to q_loc/Gamma_eff/K_hat",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VWI789_3_Bianchi",
            "identity_or_variation": "Bianchi identity",
            "result": "blocks_arbitrary_source_terms",
            "meaning": "any added MTS stress must be divergence-compatible; otherwise the metric equation is inconsistent",
            "missing": "T_MTS construction with Ward identity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VWI789_4_boundary",
            "identity_or_variation": "boundary/source variation",
            "result": "must_be_silent_or_explicit",
            "meaning": "source-measure and boundary terms cannot be hidden if they affect local equations",
            "missing": "B_obs/source-measure coefficient or theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def newton_ppn_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "NPR789_0_torsion",
            "quantity": "tau_torsion",
            "local_GR_requirement": "zero or below spin/torsion local bounds",
            "Newton_PPN_effect_if_nonzero": "extra spin/precession/contact force channels",
            "status": "missing_bound_or_theorem_zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "NPR789_1_T_MTS",
            "quantity": "T_MTS_mu_nu / T_matter_mu_nu",
            "local_GR_requirement": "suppressed in Solar/lab/orbital local regime or absorbed into measured matter source",
            "Newton_PPN_effect_if_nonzero": "effective dark/source correction and PPN gamma/beta shifts",
            "status": "missing_decomposition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "NPR789_2_Q_nu",
            "quantity": "Q_nu or q_loc_nu",
            "local_GR_requirement": "matter exchange current vanishes or is bounded in local regime",
            "Newton_PPN_effect_if_nonzero": "non-geodesic force or nonconservation signal",
            "status": "missing_q_loc_suppression",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "NPR789_3_boundary",
            "quantity": "B_obs/source-measure",
            "local_GR_requirement": "boundary/source-measure terms silent in local patch or explicitly bounded",
            "Newton_PPN_effect_if_nonzero": "apparent fifth-force/source-renormalization",
            "status": "missing_source_measure_bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "NPR789_4_frame",
            "quantity": "b_g/c_g and W_Ic",
            "local_GR_requirement": "ordinary matter sees only e, omega[e], and owned gauge fields",
            "Newton_PPN_effect_if_nonzero": "equivalence-principle/PPN/readout violation",
            "status": "active_from_785_786",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def mts_input_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "MIR789_0_T_MTS_decomposition",
            "needed_object": "T_MTS_mu_nu",
            "why_needed": "tells whether MTS acts as stress, cosmological term, boundary term, or local force",
            "acceptance_gate": "covariant variation of S_MTS with divergence-compatible stress",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "MIR789_1_exchange_current",
            "needed_object": "Q_nu / q_loc_nu",
            "why_needed": "local GR requires ordinary matter conservation or a bound below experiments",
            "acceptance_gate": "derive Q from Ward identity and show local suppression",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "MIR789_2_torsion_spin",
            "needed_object": "MTS spin/torsion source",
            "why_needed": "Palatini connection equation must reduce to Levi-Civita locally",
            "acceptance_gate": "zero theorem or torsion bound",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "MIR789_3_boundary_source",
            "needed_object": "B_obs/source-measure",
            "why_needed": "boundary terms can spoil local equations if hidden",
            "acceptance_gate": "explicit boundary variation and local silence theorem/bound",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "MIR789_4_matter_universality",
            "needed_object": "S_matter[e,omega,Psi] no direct Phi_MTS",
            "why_needed": "equivalence principle and PPN safety",
            "acceptance_gate": "no-spurion/no-direct-coupling audit",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D789_0_contract_written",
            "decision": "keep Palatini/tetrad as the explicit local-GR reduction contract",
            "reason": "it gives a clear route from action variation to GR and then Newton under named residual gates",
            "result": "contract_retained_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D789_1_no_local_GR_claim",
            "decision": "do not claim MTS derives local GR yet",
            "reason": "T_MTS, Q_nu/q_loc, torsion, boundary, and frame leakage are not decomposed or bounded",
            "result": "claim_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D789_2_next_target",
            "decision": "decompose MTS exchange stress and local suppression gates next",
            "reason": "this is now the smallest missing step for GR/Newton recovery",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "a conditional Palatini/tetrad contract now states exactly how MTS reduces to GR and then Newton: torsion/nonmetricity, T_MTS, Q_nu/q_loc, boundary terms, and frame leakage must vanish or be bounded locally",
            "hard_blocker": "derive or bound the MTS exchange stress/current/source-measure residual vector; tetrad ownership from MTS remains deeper work",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_788_clean = all(validation_clean(number) for number in range(665, 789))
    contract_complete = len(contract) == 6
    connection_gate = any(row["contract_id"] == "PTG789_2_connection_equation" for row in contract)
    coframe_gate = any(row["contract_id"] == "PTG789_3_coframe_equation" for row in contract)
    gr_recovery_gate = any(row["contract_id"] == "PTG789_4_GR_recovery" for row in contract)
    newton_gate = any(row["contract_id"] == "PTG789_5_Newton_recovery" for row in contract)
    ward_complete = len(ward) == 5
    exchange_current_recorded = any(row["gate_id"] == "VWI789_2_exchange_current" for row in ward)
    residuals_complete = len(residuals) == 5
    residuals_all_missing_or_active = all(row["status"].startswith("missing") or row["status"].startswith("active") for row in residuals)
    inputs_complete = len(inputs) == 5
    inputs_missing = all(row["status"] == "missing" for row in inputs)
    no_local_gr_claim = any(row["decision_id"] == "D789_1_no_local_GR_claim" and row["result"] == "claim_blocked" for row in decisions)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D789_2_next_target" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, contract, ward, residuals, inputs, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V789_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V789_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V789_2_prior_665_788_clean", prior_665_788_clean, "665-788 validation rows have no failures"),
        ("V789_3_contract_complete", contract_complete, "Palatini/tetrad contract rows complete"),
        ("V789_4_connection_gate", connection_gate, "connection/torsion gate recorded"),
        ("V789_5_coframe_gate", coframe_gate, "coframe Einstein equation gate recorded"),
        ("V789_6_GR_recovery_gate", gr_recovery_gate, "GR recovery residual gate recorded"),
        ("V789_7_Newton_gate", newton_gate, "Newton weak-field gate recorded"),
        ("V789_8_ward_complete", ward_complete, "variation/Ward identity rows complete"),
        ("V789_9_exchange_current_recorded", exchange_current_recorded, "Q_nu exchange current gate recorded"),
        ("V789_10_residuals_complete", residuals_complete, "Newton/PPN residual vector rows complete"),
        ("V789_11_residuals_missing_or_active", residuals_all_missing_or_active, "residual rows remain missing/active nonclaim"),
        ("V789_12_inputs_complete", inputs_complete, "MTS exchange input requirement rows complete"),
        ("V789_13_inputs_missing", inputs_missing, "all MTS exchange inputs still missing"),
        ("V789_14_no_local_GR_claim", no_local_gr_claim, "local GR claim remains blocked"),
        ("V789_15_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V789_16_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V789_17_claim_artifacts_absent", claim_artifacts_absent, "no local-GR/Newton/adopted-action/PPN claim artifact fabricated"),
        ("V789_18_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V789_19_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V789_20_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    ward: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 789 - Y5 R10 Palatini Tetrad GR Limit With MTS Exchange Contract

Current result: **we now have a clean conditional contract for `MTS -> GR -> Newton`, but not a claim that MTS has satisfied it**. The Palatini/tetrad route says exactly what has to happen: the connection equation must reduce to Levi-Civita, the coframe equation must reduce to Einstein with ordinary matter, MTS stress/exchange/boundary/frame residuals must vanish or be bounded locally, and only then the usual GR weak-field limit gives Newton.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Palatini Tetrad GR Limit Contract

{markdown_table(contract, ["contract_id", "statement", "condition", "derived_if_condition_holds", "missing_before_claim", "valid_for_claim"])}

## Variation Ward Identity Gate

{markdown_table(ward, ["gate_id", "identity_or_variation", "result", "meaning", "missing", "valid_for_claim"])}

## Newton PPN Residual Vector

{markdown_table(residuals, ["residual_id", "quantity", "local_GR_requirement", "Newton_PPN_effect_if_nonzero", "status", "valid_for_claim"])}

## MTS Exchange Input Requirements

{markdown_table(inputs, ["input_id", "needed_object", "why_needed", "acceptance_gate", "status", "valid_for_claim"])}

## Branch Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is the most useful local-GR checkpoint so far. It stops the work from drifting: MTS does not need to beat GR locally; it needs to become GR locally, then Newton in the weak-field limit, with every extra MTS term either silent or explicitly bounded. The next job is therefore not more philosophy about the metric. It is to decompose `T_MTS`, `Q_nu/q_loc`, torsion, boundary/source-measure, and frame leakage into concrete gates.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    contract = gr_limit_contract_rows(generated_utc)
    ward = variation_ward_rows(generated_utc)
    residuals = newton_ppn_rows(generated_utc)
    inputs = mts_input_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, contract, ward, residuals, inputs, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(GR_LIMIT_CONTRACT_PATH, contract, ["contract_id", "statement", "condition", "derived_if_condition_holds", "missing_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(VARIATION_WARD_PATH, ward, ["gate_id", "identity_or_variation", "result", "meaning", "missing", "valid_for_claim", "generated_utc"])
    write_csv(NEWTON_PPN_PATH, residuals, ["residual_id", "quantity", "local_GR_requirement", "Newton_PPN_effect_if_nonzero", "status", "valid_for_claim", "generated_utc"])
    write_csv(MTS_INPUTS_PATH, inputs, ["input_id", "needed_object", "why_needed", "acceptance_gate", "status", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, contract, ward, residuals, inputs, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"789 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
