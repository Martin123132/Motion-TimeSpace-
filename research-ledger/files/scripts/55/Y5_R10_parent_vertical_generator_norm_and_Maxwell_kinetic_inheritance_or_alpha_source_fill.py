from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md"
NEXT_TARGET = "766-Y5-R10-finite-alpha-source-fill-clock-first-or-parent-action-source-hunt.md"
STATUS = "Y5_R10_765_parent_vertical_generator_norm_theorem_reaudited_conditional_only_lambda_F2_escape_retained"
CLAIM_CEILING = "vertical_norm_Maxwell_inheritance_contract_only_no_kappa_alpha_zero_no_EM_R10_WEP_clock_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

PARENT_GENERATOR_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_765_PARENT_GENERATOR_NORM_INPUT_CANDIDATE.csv"
MAXWELL_SUBBLOCK_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_765_MAXWELL_SUBBLOCK_INPUT_CANDIDATE.csv"
CURRENT_OWNER_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_765_CHARGE_CURRENT_OWNER_INPUT_CANDIDATE.csv"
READOUT_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_765_READOUT_DESCENT_INPUT_CANDIDATE.csv"
FINITE_ALPHA_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_765_FINITE_ALPHA_SOURCE_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_765_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv"
KINETIC_GATE_PATH = RESIDUALS / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
COUNTEREXAMPLE_PATH = RESIDUALS / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_765_ALPHA_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_765_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_765_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_765_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_765_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "764_doc": {
        "path": POST_CHECKPOINT / "764-Y5-R10-constant-superselection-and-charge-normalization-or-source-fill.md",
        "needles": [
            "Current result: **the constant/charge descent gate is now exact enough to use, but it does not close**",
            "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md",
        ],
        "role": "immediate parent vertical-generator norm handoff",
    },
    "764_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_764_VALIDATION.csv",
        "needles": ["V764_15_validation_rows_ready", "V764_14_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "643_alpha_owner": {
        "path": POST_CHECKPOINT / "643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md",
        "needles": ["AO643_5_parent_vertical_norm", "PVC643_6_vertical_alpha_silence"],
        "role": "original alpha-owner hunt",
    },
    "644_vertical_norm": {
        "path": POST_CHECKPOINT / "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md",
        "needles": ["CVN644", "RC644_0_free_lambda_A"],
        "role": "prior vertical-norm theorem and lambda escape",
    },
    "642_charge_Maxwell": {
        "path": POST_CHECKPOINT / "642-Y5-R10-charge-unit-Maxwell-proof-extension-or-kappa-alpha-pressure-runner.md",
        "needles": ["TA642_4_coupling_normalization", "MD642_4_alpha_constant"],
        "role": "compact U1/Maxwell partial result",
    },
    "645_finite_alpha": {
        "path": POST_CHECKPOINT / "645-Y5-R10-finite-kappa-alpha-bound-input-fill-and-prior-discipline.md",
        "needles": ["KP645_0_zero_theorem_demoted", "AQ645_0_clock_alpha_sensitivity"],
        "role": "finite alpha fallback discipline",
    },
    "211_GK_norm_precedent": {
        "path": POST_CHECKPOINT / "211-GK-parent-metric-Ward-identity-attempt.md",
        "needles": ["GK_metric_Ward_identity_partial_flow_block_only_composite_metric_fixed_closure", "full composite metric still does not follow"],
        "role": "partial parent norm precedent",
    },
    "233_boundary_metric": {
        "path": POST_CHECKPOINT / "233-boundary-symplectic-metric-or-local-EH-operator.md",
        "needles": ["boundary_Hodge_DeWitt_metric_candidate_projectors_orthogonal_Lovelock_EH_gate_written_no_promotion", "parent boundary metric derived"],
        "role": "boundary Hodge/DeWitt candidate but not parent derivation",
    },
    "332_unit_inheritance": {
        "path": POST_CHECKPOINT / "332-parent-Hamiltonian-trace-current-gate.md",
        "needles": ["Hamiltonian_trace_current_unit_inheritance_conditional_lambda_rescaling_no_go_blocks_promotion", "lambda_mem"],
        "role": "unit-inheritance pattern and lambda no-go analogy",
    },
    "459B_phase_current": {
        "path": POST_CHECKPOINT / "459B-Andersen-charge-amplitude-phase-current-gate.md",
        "needles": ["PC2_quantized_charge_unit", "PC4_Maxwell_limit"],
        "role": "external phase/current clue, not proof",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
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


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
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
        for source_id, spec in SOURCES.items()
    ]


def theorem_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "VGN765_0_parent_charge_generator",
            "required_statement": "The parent configuration contains a compact vertical charge generator T_Q, not merely a closure-label charge.",
            "mathematical_form": "T_Q in Lie(G_parent) or lattice L_Q with exp(2*pi T_Q)=1, and A_Q is the connection along T_Q.",
            "if_signed": "charge labels can be representation/winding data rather than inserted matter constants",
            "current_status": "partial_template_only",
            "blocker": "T_Q is not yet supplied as a varied parent-action object in the current corpus",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "VGN765_1_fixed_norm",
            "required_statement": "The norm of T_Q is fixed by a parent metric/symplectic/lattice form and cannot be rescaled.",
            "mathematical_form": "N_Q=<T_Q,T_Q>_P is fixed; T_Q -> s T_Q is not an allowed representative transformation.",
            "if_signed": "charge connection normalization stops being a free convention",
            "current_status": "not_parent_signed",
            "blocker": "211/233 give norm analogies, but no parent-fixed EM charge-generator norm",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "VGN765_2_unique_curvature_subblock",
            "required_statement": "The observed Maxwell F_Q^2 term is the literal charge subblock of an already-normalized parent curvature norm.",
            "mathematical_form": "S_parent contains -C_P/4 int <F,F>_P, with <F_Q T_Q,F_Q T_Q>_P=N_Q F_Q^2; hence g_EM^{-2}=C_P N_Q.",
            "if_signed": "Maxwell kinetic coefficient is inherited rather than chosen",
            "current_status": "failed_current_corpus",
            "blocker": "no theorem forbids adding an independent lambda_A F_Q^2 invariant",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "VGN765_3_same_owner_current",
            "required_statement": "The current coupled to A_Q is the Noether/Ward current of the same parent generator and normalization.",
            "mathematical_form": "delta S_m/delta A_Q = J_Q and d*F_Q=g_EM^2 *J_Q, with Q_star fixed by T_Q and not by q_A(X).",
            "if_signed": "charge unit, source current, and Lorentz readout share one owner",
            "current_status": "not_parent_signed",
            "blocker": "Q_star, EM current identification, and matter derivative normalization remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "VGN765_4_readout_descent",
            "required_statement": "The Hodge star, hbar/c readout, and matter coframe descend or are pure quotient-fixed readout.",
            "mathematical_form": "Lie_v * = Lie_v ln(hbar c)=0 in the observed branch, or all changes cancel from dimensionless alpha_EM.",
            "if_signed": "no hidden clock/coframe factor reopens alpha pressure",
            "current_status": "not_parent_signed",
            "blocker": "geometry-stack/coframe/readout descent remains a separate open clause",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "VGN765_5_alpha_zero_conditional",
            "required_statement": "If VGN765_0..VGN765_4 all hold and no independent invariant is legal, then kappa_alpha=0.",
            "mathematical_form": "Lie_v ln alpha_EM = -Lie_v ln(C_P N_Q) - Lie_v ln(4*pi*hbar*c) = 0.",
            "if_signed": "alpha_EM is locally vertical-silent by parent inheritance",
            "current_status": "valid_conditional_theorem_not_parent_signed",
            "blocker": "VGN765_1..VGN765_4 are not all signed, and VGN765_2 currently fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "VGN765_6_verdict",
            "required_statement": "Parent vertical-generator norm route is the right theorem shape but not an active MTS claim.",
            "mathematical_form": "kappa_alpha=0 cannot be promoted while lambda_A F_Q^2, T_Q rescaling, current rescaling, or readout/coframe leakage remains legal.",
            "if_signed": "would close the alpha component of b_theta",
            "current_status": "not_parent_signed_retain_finite_alpha_source_fill",
            "blocker": "current corpus cannot defeat the rescaling counterexamples",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def kinetic_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MKI765_0_projection",
            "gate": "A_Q is a projection of a parent connection along T_Q.",
            "pass_condition": "A_parent=A_Q T_Q + A_perp and the projection is parent-defined before readout",
            "current_status": "template_only",
            "failure_if_missing": "observed EM connection can be appended after the parent action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MKI765_1_norm",
            "gate": "Parent norm fixes the T_Q length.",
            "pass_condition": "<T_Q,T_Q>_P=N_Q is fixed by a lattice/metric/symplectic form and invariant under vertical representatives",
            "current_status": "not_signed",
            "failure_if_missing": "rescale T_Q and compensate with charge/current units",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MKI765_2_unique_F2",
            "gate": "No independent Maxwell kinetic invariant exists.",
            "pass_condition": "there is no allowed Delta S=-lambda_A/4 int F_Q^2 beyond the parent curvature norm",
            "current_status": "failed_current_corpus",
            "failure_if_missing": "g_EM^{-2}=C_P N_Q + lambda_A remains free",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MKI765_3_same_current",
            "gate": "The matter current is normalized by the same T_Q owner.",
            "pass_condition": "J_Q is the Noether/Ward current of T_Q and matter charges are representation weights",
            "current_status": "not_signed",
            "failure_if_missing": "q_A(X) or kappa_A-style current weights reopen b_theta/b_kappa",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MKI765_4_readout",
            "gate": "The observed Hodge star and hbar/c readout are quotient-fixed.",
            "pass_condition": "the dimensionless alpha readout has no residual coframe/clock dependence",
            "current_status": "not_signed",
            "failure_if_missing": "clock and spectroscopy channels see alpha pressure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MKI765_5_total",
            "gate": "Maxwell kinetic inheritance can be promoted.",
            "pass_condition": "MKI765_0..MKI765_4 pass together",
            "current_status": "blocked",
            "failure_if_missing": "finite kappa_alpha source fill remains required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def counterexample_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "RCE765_0_lambda_F2",
            "legal_if_unsigned": "Add an independent Maxwell kinetic term.",
            "mathematical_form": "Delta S=-lambda_A/4 int dmu_obs F_Q^{mu nu}F^Q_{mu nu}",
            "effect": "g_EM^{-2}=C_P N_Q+lambda_A; alpha_EM is not fixed by parent norm alone",
            "blocks": "kappa_alpha=0, EM/charge descent, b_theta zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "RCE765_1_generator_rescale",
            "legal_if_unsigned": "Rescale the charge generator and compensate charge labels/current.",
            "mathematical_form": "T_Q -> s T_Q, A_Q -> A_Q/s, n_A -> s n_A where allowed by missing lattice/norm ownership",
            "effect": "charge unit and A normalization become convention/free parameter",
            "blocks": "unique Q_star, alpha normalization, current equality",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "RCE765_2_current_rescale",
            "legal_if_unsigned": "Matter current normalization is independent of the Maxwell kinetic owner.",
            "mathematical_form": "S_int=sum_A q_A(X) int A_Q J_A with d*F=g_EM^2 sum_A c_A J_A",
            "effect": "same F_Q^2 coefficient but different source/test charge response",
            "blocks": "WEP/R10/source-test charge and EM Lorentz readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "RCE765_3_coframe_Hodge_leak",
            "legal_if_unsigned": "Observed Hodge star or clock/ruler readout carries vertical representative data.",
            "mathematical_form": "*_obs = A_X^p *bar or hbar*c readout varies with Xhat",
            "effect": "dimensionless alpha readout changes despite a fixed abstract F_Q norm",
            "blocks": "clock/spectroscopy alpha silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "ASF765_0_parent_generator_norm",
            "artifact": str(PARENT_GENERATOR_CANDIDATE_PATH),
            "required_columns": "generator_id;parent_owner;compactness;norm_value_or_symbol;rescaling_forbidden_by;source_path;valid_for_claim",
            "claim_gate": "T_Q exists in the parent action and has a fixed non-rescalable norm",
            "current_status": f"schema_only_candidate_missing={bool_string(not PARENT_GENERATOR_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "ASF765_1_Maxwell_subblock",
            "artifact": str(MAXWELL_SUBBLOCK_CANDIDATE_PATH),
            "required_columns": "subblock_id;parent_curvature_norm;coefficient_owner;independent_F2_forbidden;source_path;valid_for_claim",
            "claim_gate": "F_Q^2 is inherited as a literal parent curvature subblock",
            "current_status": f"schema_only_candidate_missing={bool_string(not MAXWELL_SUBBLOCK_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "ASF765_2_charge_current_owner",
            "artifact": str(CURRENT_OWNER_CANDIDATE_PATH),
            "required_columns": "current_id;Noether_owner;charge_unit_owner;matter_coupling_owner;normalization;source_path;valid_for_claim",
            "claim_gate": "J_Q, Q_star, and matter charge coupling share the same T_Q owner",
            "current_status": f"schema_only_candidate_missing={bool_string(not CURRENT_OWNER_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "ASF765_3_readout_descent",
            "artifact": str(READOUT_DESCENT_CANDIDATE_PATH),
            "required_columns": "readout_id;Hodge_star_owner;hbar_c_status;coframe_descent_status;vertical_derivative;source_path;valid_for_claim",
            "claim_gate": "dimensionless alpha readout is quotient-fixed and coframe-silent",
            "current_status": f"schema_only_candidate_missing={bool_string(not READOUT_DESCENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "ASF765_4_finite_alpha_source",
            "artifact": str(FINITE_ALPHA_SOURCE_CANDIDATE_PATH),
            "required_columns": "component;kappa_alpha_or_bound;tau_clock;tau_WEP;tau_R10;tau_EM;source_path;valid_for_claim",
            "claim_gate": "if theorem route fails, finite alpha residual has sourced units, projections, and bounds",
            "current_status": f"schema_only_candidate_missing={bool_string(not FINITE_ALPHA_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D765_0_theorem_shape",
            "decision": "keep the parent vertical-generator norm theorem as the exact closure contract",
            "reason": "it is the only clean route that makes charge unit, A_Q, F2 coefficient, and current normalization one object",
            "claim_status": "conditional_contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D765_1_no_alpha_zero",
            "decision": "do not promote kappa_alpha=0",
            "reason": "lambda_A F_Q^2, generator rescaling, current rescaling, and readout/coframe leaks remain legal",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D765_2_next",
            "decision": "move to finite alpha source-fill unless a real parent-action source for T_Q appears",
            "reason": "the proof target is now sharp, but current corpus cannot sign it; empirical discipline needs finite alpha rows",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU765_0_allowed",
            "allowed_after_765": "cite the vertical-generator norm route as a dormant exact closure contract",
            "forbidden_after_765": "use it as evidence that alpha_EM is already silent",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU765_1_allowed",
            "allowed_after_765": "treat lambda_A F_Q^2 as the decisive counterexample unless forbidden by parent symmetry",
            "forbidden_after_765": "appeal to naturalness or compact U1 alone to set lambda_A=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU765_2_allowed",
            "allowed_after_765": "open finite alpha source-fill with clock-first priority",
            "forbidden_after_765": "score clocks, WEP, R10, or EM without tau maps and sensitivity coefficients",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "parent vertical-generator norm theorem is exact as a conditional contract but not parent-signed",
            "hard_blocker": "independent lambda_A F_Q^2 and generator/current/readout rescalings remain legal",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    kinetic: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V765_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V765_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_764 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_764_VALIDATION.csv")
    validation.append({"check_id": "V765_2_prior_764_clean", "result": "pass" if prior_764 and all(row.get("result") == "pass" for row in prior_764) else "fail", "detail": "764 validation has no failures"})
    validation.append({"check_id": "V765_3_theorem_contract_written", "result": "pass" if len(theorem) == 7 and any(row["theorem_id"] == "VGN765_6_verdict" for row in theorem) else "fail", "detail": "vertical-generator norm theorem rows present"})
    validation.append({"check_id": "V765_4_theorem_not_parent_signed", "result": "pass" if any(row["theorem_id"] == "VGN765_6_verdict" and row["current_status"] == "not_parent_signed_retain_finite_alpha_source_fill" for row in theorem) else "fail", "detail": "theorem remains nonclaim"})
    validation.append({"check_id": "V765_5_kinetic_gate_blocks", "result": "pass" if any(row["gate_id"] == "MKI765_2_unique_F2" and row["current_status"] == "failed_current_corpus" for row in kinetic) else "fail", "detail": "unique F2 inheritance gate records current failure"})
    validation.append({"check_id": "V765_6_counterexamples_present", "result": "pass" if len(counterexamples) == 4 and any(row["counterexample_id"] == "RCE765_0_lambda_F2" for row in counterexamples) else "fail", "detail": "lambda/generator/current/readout counterexamples retained"})
    validation.append({"check_id": "V765_7_source_fill_schema_written", "result": "pass" if len(source_fill) == 5 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    candidate_paths = [PARENT_GENERATOR_CANDIDATE_PATH, MAXWELL_SUBBLOCK_CANDIDATE_PATH, CURRENT_OWNER_CANDIDATE_PATH, READOUT_DESCENT_CANDIDATE_PATH, FINITE_ALPHA_SOURCE_CANDIDATE_PATH]
    validation.append({"check_id": "V765_8_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in candidate_paths) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = theorem + kinetic + counterexamples + source_fill + decisions + routes + summary
    validation.append({"check_id": "V765_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V765_10_no_local_or_EM_claim", "result": "pass" if "no_kappa_alpha_zero_no_EM_R10_WEP_clock_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha/EM/local claims remain blocked"})
    validation.append({"check_id": "V765_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        KINETIC_GATE_PATH,
        COUNTEREXAMPLE_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V765_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V765_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V765_14_finite_alpha_next", "result": "pass" if "finite-alpha-source-fill" in NEXT_TARGET else "fail", "detail": "next moves to finite alpha source-fill"})
    validation.append({"check_id": "V765_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    kinetic: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 765 - Y5 R10 Parent Vertical Generator Norm And Maxwell Kinetic Inheritance Or Alpha Source Fill

Start point: 764 isolated the live coupling problem. Compact `U(1)` can give integer charge labels, but it does not by itself own the continuous Maxwell kinetic normalization `g_EM` or the fine-structure strength `alpha_EM`.

Current result: **the parent vertical-generator norm route is the exact right theorem shape, but it is not parent-signed**. If `A_Q`, `F_Q^2`, charge unit, and current normalization are literal projections of one fixed parent generator `T_Q`, then `kappa_alpha=0` follows. But the current corpus still permits the counterpunch `lambda_A F_Q^2`, plus generator/current/readout rescalings. So this remains a dormant closure contract, not evidence.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Vertical-Generator Norm Theorem Attempt

{markdown_table(theorem, ["theorem_id", "required_statement", "mathematical_form", "if_signed", "current_status", "blocker", "valid_for_claim"])}

## Maxwell Kinetic Inheritance Gate

{markdown_table(kinetic, ["gate_id", "gate", "pass_condition", "current_status", "failure_if_missing", "valid_for_claim"])}

## Rescaling Counterexample Ledger

{markdown_table(counterexamples, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "blocks", "valid_for_claim"])}

## Alpha Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_765", "forbidden_after_765", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is the cleanest version of the coupling hunt. The win condition is beautifully sharp: make the EM connection, Maxwell kinetic term, charge unit, and source current one parent-owned object. The current corpus does not yet do that. The decisive hole is not vague; it is `lambda_A F_Q^2`. Until a parent symmetry forbids that independent invariant, alpha is a finite residual, not a derived zero.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    theorem = theorem_attempt_rows(generated_utc)
    kinetic = kinetic_gate_rows(generated_utc)
    counterexamples = counterexample_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, theorem, kinetic, counterexamples, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_ATTEMPT_PATH, theorem, ["theorem_id", "required_statement", "mathematical_form", "if_signed", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(KINETIC_GATE_PATH, kinetic, ["gate_id", "gate", "pass_condition", "current_status", "failure_if_missing", "valid_for_claim", "generated_utc"])
    write_csv(COUNTEREXAMPLE_PATH, counterexamples, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_765", "forbidden_after_765", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, theorem, kinetic, counterexamples, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
