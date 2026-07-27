from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md"
NEXT_TARGET = "786-Y5-R10-parent-action-metric-map-ownership-or-bg-bound-source-pack.md"
STATUS = "Y5_R10_785_psi_metric_to_coframe_connection_contract_conditional_bg_cg_residual_locked_nonclaim"
CLAIM_CEILING = "conditional_metric_to_matter_stack_only_no_covariant_psi_metric_parent_action_no_GR_Newton_local_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_785_SOURCE_REGISTER.csv"
COFRAME_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv"
CONNECTION_STACK_PATH = RESIDUALS / "P8_Y5_R10_785_CONNECTION_DERIVATIVE_STACK_GATE.csv"
BG_RESIDUAL_LOCK_PATH = RESIDUALS / "P8_Y5_R10_785_BG_RESIDUAL_LOCK.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_785_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_785_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_785_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_OWNER_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_785_COFRAME_CONNECTION_CLOSED_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_785_COUPLING_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_785_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    COFRAME_CONTRACT_PATH,
    CONNECTION_STACK_PATH,
    BG_RESIDUAL_LOCK_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "784_doc": {
        "path": POST_CHECKPOINT / "784-Y5-R10-observed-metric-from-psi-map-or-coupling-owner-demotion.md",
        "needles": ["Current result", "psi -> g_obs -> e_obs -> omega/D_m"],
        "role": "immediate 785 handoff",
    },
    "784_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_784_VALIDATION.csv",
        "needles": ["V784_5_covariance_blocked", "V784_6_owner_not_promoted"],
        "role": "prior validation guard",
    },
    "784_metric_gate": {
        "path": RESIDUALS / "P8_Y5_R10_784_OBSERVED_METRIC_FROM_PSI_GATE.csv",
        "needles": ["OMG784_4_coframe", "OMG784_5_connection"],
        "role": "metric-to-coframe open gates",
    },
    "784_coframe_requirements": {
        "path": RESIDUALS / "P8_Y5_R10_784_COFRAME_CONNECTION_REQUIREMENTS.csv",
        "needles": ["CCR784_1_tetrad_branch", "CCR784_5_action_derivation"],
        "role": "coframe/connection acceptance requirements",
    },
    "783_field_map": {
        "path": RESIDUALS / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
        "needles": ["FM783_2_e_obs", "strongest_partial_alignment"],
        "role": "metric partial-anchor source",
    },
    "ledger_14": {
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": ["Working repaired metric ansatz", "Metric normalization scale"],
        "role": "metric ansatz and dimensions",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["emergent or effective metric", "MTS parent theory -> effective GR"],
        "role": "unification spine and GR/Newton chain",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["Einstein-Equation Convention", "T_total"],
        "role": "Einstein convention and exchange postulates",
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


def coframe_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PMC785_0_metric_candidate",
            "object": "g_obs[psi]",
            "condition_or_theorem": "g_obs = eta + L_*^2 <partial psi partial psi> is dimensionless and symmetric, so it can be used as a candidate metric field.",
            "status": "pass_formal_from_784",
            "what_is_derived": "a symmetric metric candidate, not a dynamical spacetime metric",
            "missing_before_claim": "covariant construction, Lorentz signature theorem, parent action ownership",
            "fallback_residual": "b_g/c_g",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_1_covariant_metric_functional",
            "object": "G_mu_nu[psi]",
            "condition_or_theorem": "The psi metric map must be a diffeomorphism-covariant tensor functional; fixed eta and coordinate smoothing are not enough for a parent field theory.",
            "status": "blocked",
            "what_is_derived": "no covariant owner yet",
            "missing_before_claim": "covariant kernel/bitensor/EFT operator or a declared background-EFT route",
            "fallback_residual": "b_g/c_g remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_2_local_coframe_existence",
            "object": "e_obs",
            "condition_or_theorem": "If g_obs is smooth, nondegenerate, Lorentzian, orientable, and time-orientable on a patch U, then a local orthonormal coframe e_obs exists with g_obs = eta_ab e^a e^b.",
            "status": "pass_conditional",
            "what_is_derived": "standard local tetrad existence once metric admissibility is assumed",
            "missing_before_claim": "signature/nondegeneracy domain from psi and local Lorentz gauge handling",
            "fallback_residual": "b_g/c_g if matter frame is not unique/owned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_3_coframe_gauge_blindness",
            "object": "local Lorentz frame",
            "condition_or_theorem": "Matter observables must be invariant under e_obs -> Lambda(x) e_obs, so tetrad representative choices cannot become new physical couplings.",
            "status": "conditional",
            "what_is_derived": "a no-spurion condition for the frame branch",
            "missing_before_claim": "explicit matter action and spin/gauge representation proof",
            "fallback_residual": "W_Ic and b_g/c_g",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_4_connection_from_coframe",
            "object": "omega[e_obs]",
            "condition_or_theorem": "If torsion and nonmetricity are absent or parent-owned, omega can be the Levi-Civita/spin connection of e_obs.",
            "status": "pass_conditional",
            "what_is_derived": "a clean derivative stack is possible in the metric-only branch",
            "missing_before_claim": "parent proof that torsion/nonmetricity vanish or are independently bounded",
            "fallback_residual": "connection-leakage component of b_g/c_g",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_5_matter_metric_only_coupling",
            "object": "S_matter[Psi,e_obs,omega,theta]",
            "condition_or_theorem": "Ordinary matter must couple only through e_obs, omega[e_obs], owned gauge fields, and constants theta; no direct dependence on psi gradients, Gamma_mem, chi, q_loc, or representative data.",
            "status": "blocked_missing_parent_signature",
            "what_is_derived": "the exact contract for matter-frame blindness",
            "missing_before_claim": "parent-signed matter action/coupling ledger",
            "fallback_residual": "b_g, b_theta, C_qmu",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_6_parent_action_metric_ownership",
            "object": "S_parent",
            "condition_or_theorem": "The parent action must derive g_obs[psi] either as an Euler equation, a constraint, or an induced effective metric after integrating out fast fields.",
            "status": "not_derived",
            "what_is_derived": "nothing claimable; this is the next hard theorem",
            "missing_before_claim": "action term/constraint multiplier/induced gravity derivation with correct sign and universality",
            "fallback_residual": "b_g/c_g locked as empirical interface",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PMC785_7_GR_Newton_reduction",
            "object": "MTS -> GR -> Newton",
            "condition_or_theorem": "After metric ownership, the effective equations must reduce to Einstein/GR locally and then to the Newtonian weak-field limit.",
            "status": "not_closed",
            "what_is_derived": "the required reduction chain is now sharply localized",
            "missing_before_claim": "Einstein equation, stress map, conservation/Bianchi identity, PPN vector, Newtonian limit",
            "fallback_residual": "local-GR branch remains nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def connection_stack_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CDS785_0_tetrad_domain",
            "stack_layer": "metric-to-coframe",
            "required_input": "smooth Lorentzian g_obs[psi] with det(g_obs) nonzero",
            "result": "conditional_open_domain",
            "leak_if_missing": "no physical matter frame",
            "next_evidence": "signature/nondegeneracy theorem or perturbative domain bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CDS785_1_lc_connection",
            "stack_layer": "coframe-to-spin-connection",
            "required_input": "torsion-free, metric-compatible connection",
            "result": "pass_conditional",
            "leak_if_missing": "torsion/nonmetricity can act as hidden coupling",
            "next_evidence": "parent connection equation setting T^a=0 and nabla g=0, or sourced/bounded deviations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CDS785_2_torsion_nonmetricity",
            "stack_layer": "connection residuals",
            "required_input": "T^a=0 and Q_{lambda mu nu}=0 or owned residual equations",
            "result": "blocked",
            "leak_if_missing": "extra local force/PPN response beyond GR",
            "next_evidence": "connection variation or empirical response bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CDS785_3_matter_derivative",
            "stack_layer": "D_m",
            "required_input": "D_m uses omega[e_obs] and owned gauge connections only",
            "result": "blocked_missing_matter_action",
            "leak_if_missing": "direct psi/Gamma/q_loc derivative couplings",
            "next_evidence": "S_matter signature and no-marker audit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CDS785_4_boundary_projection",
            "stack_layer": "local projection",
            "required_input": "boundary/source-measure terms do not change the local matter frame",
            "result": "blocked",
            "leak_if_missing": "B_obs/source-measure can mimic residual coupling",
            "next_evidence": "source-measure coefficient rows or theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CDS785_5_stack_verdict",
            "stack_layer": "psi -> g_obs -> e_obs -> omega -> D_m",
            "required_input": "all CDS785_0..4 gates close",
            "result": "conditional_skeleton_only",
            "leak_if_missing": "b_g/c_g must stay explicit",
            "next_evidence": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bg_residual_lock_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "BGL785_0_definition",
            "coefficient": "b_g/c_g",
            "lock_rule": "activate whenever the observed metric/coframe/connection stack is not parent-derived and matter-visible only",
            "why_locked": "otherwise a metric ansatz is being mistaken for a coupling theorem",
            "bound_or_derivation_needed": "derive parent action ownership or provide finite PPN/clock/orbital response bounds",
            "status": "active_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "BGL785_1_covariance_trigger",
            "coefficient": "b_g/c_g",
            "lock_rule": "remain active while eta/background smoothing is not replaced by a covariant psi metric functional",
            "why_locked": "fixed-background leakage can be observable in local frames",
            "bound_or_derivation_needed": "covariant coarse-graining or declared background-EFT error budget",
            "status": "active_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "BGL785_2_connection_trigger",
            "coefficient": "b_g/c_g",
            "lock_rule": "remain active while torsion/nonmetricity and spin-connection ownership are unsigned",
            "why_locked": "derivative couplings are where hidden local-gravity violations can hide",
            "bound_or_derivation_needed": "connection Euler equation or response coefficients",
            "status": "active_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "BGL785_3_matter_blindness_trigger",
            "coefficient": "b_g/c_g",
            "lock_rule": "remain active until ordinary matter is proved blind to psi/Gamma_mem/chi/q_loc except through e_obs",
            "why_locked": "direct field dependence would violate the equivalence principle branch",
            "bound_or_derivation_needed": "parent-signed S_matter plus no-spurion audit",
            "status": "active_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lock_id": "BGL785_4_observable_interface",
            "coefficient": "b_g/c_g",
            "lock_rule": "feed this residual into PPN, clock, orbital, and R10 source-measure rows until theorem-zero closes",
            "why_locked": "local GR safety needs either zero theorem or bounded residual vector",
            "bound_or_derivation_needed": "PPN residual vector, clock redshift residual, orbital ephemeris residual, R10 alpha(lambda) response",
            "status": "active_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D785_0_keep_conditional_stack",
            "decision": "keep the psi metric-to-matter stack as a conditional theorem route",
            "reason": "coframe and Levi-Civita connection are standard once a good Lorentzian metric is owned",
            "result": "conditional_route_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D785_1_lock_bg",
            "decision": "lock b_g/c_g as an active residual",
            "reason": "covariance, parent action ownership, torsion/nonmetricity, and matter blindness are not proved",
            "result": "residual_locked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D785_2_no_owner_adoption",
            "decision": "do not adopt the coupling owner action",
            "reason": "785 gives a clean contract but not the parent derivation that would make it physical",
            "result": "not_adopted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D785_3_next_target",
            "decision": "try parent-action metric-map ownership before giving up to pure bound-sourcing",
            "reason": "derivability is still the best route; if it fails, b_g/c_g already has a source-ready lock",
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
            "main_result": "coframe and connection are conditionally available from a Lorentzian g_obs[psi], but the psi metric map is not yet covariant or parent-action-owned; b_g/c_g is therefore locked as an active residual",
            "hard_blocker": "parent action must derive the psi metric functional and prove ordinary matter sees only e_obs/omega, otherwise local GR remains nonclaim",
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
    stack: list[dict[str, Any]],
    bg_lock: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_784_clean = all(validation_clean(number) for number in range(665, 785))
    contract_complete = len(contract) == 8
    tetrad_conditional = any(row["contract_id"] == "PMC785_2_local_coframe_existence" and row["status"] == "pass_conditional" for row in contract)
    covariance_blocked = any(row["contract_id"] == "PMC785_1_covariant_metric_functional" and row["status"] == "blocked" for row in contract)
    parent_action_not_derived = any(row["contract_id"] == "PMC785_6_parent_action_metric_ownership" and row["status"] == "not_derived" for row in contract)
    stack_complete = len(stack) == 6
    lc_conditional = any(row["gate_id"] == "CDS785_1_lc_connection" and row["result"] == "pass_conditional" for row in stack)
    torsion_blocked = any(row["gate_id"] == "CDS785_2_torsion_nonmetricity" and row["result"] == "blocked" for row in stack)
    bg_lock_complete = len(bg_lock) == 5
    bg_lock_active = all(row["status"] == "active_nonclaim" for row in bg_lock)
    not_adopted = any(row["decision_id"] == "D785_2_no_owner_adoption" and row["result"] == "not_adopted" for row in decisions)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D785_3_next_target" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, contract, stack, bg_lock, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V785_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V785_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V785_2_prior_665_784_clean", prior_665_784_clean, "665-784 validation rows have no failures"),
        ("V785_3_contract_complete", contract_complete, "psi metric/coframe contract rows complete"),
        ("V785_4_tetrad_conditional_recorded", tetrad_conditional, "local coframe existence theorem recorded as conditional"),
        ("V785_5_covariance_blocked", covariance_blocked, "covariant psi metric functional still missing"),
        ("V785_6_parent_action_not_derived", parent_action_not_derived, "parent action ownership still missing"),
        ("V785_7_stack_complete", stack_complete, "connection derivative stack rows complete"),
        ("V785_8_lc_connection_conditional", lc_conditional, "Levi-Civita/spin connection only conditional"),
        ("V785_9_torsion_nonmetricity_blocked", torsion_blocked, "torsion/nonmetricity gate blocks claim"),
        ("V785_10_bg_lock_complete", bg_lock_complete, "b_g/c_g residual lock rows complete"),
        ("V785_11_bg_lock_active", bg_lock_active, "all b_g/c_g locks active nonclaim"),
        ("V785_12_owner_not_adopted", not_adopted, "coupling owner not adopted"),
        ("V785_13_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V785_14_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V785_15_claim_artifacts_absent", claim_artifacts_absent, "no coframe/owner/zero/local-GR claim artifact fabricated"),
        ("V785_16_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V785_17_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V785_18_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    stack: list[dict[str, Any]],
    bg_lock: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 785 - Y5 R10 Psi Metric Coframe Connection Contract Or Bg Residual Lock

Current result: **the `psi -> g_obs -> e_obs -> omega -> D_m` route survives only as a conditional skeleton**. There is a real mathematical foothold here: if `g_obs[psi]` is a smooth Lorentzian metric, the local coframe and Levi-Civita/spin-connection stack can be built. But that is not yet the same as deriving local GR, because the `psi` metric map is still not covariant/action-owned and ordinary matter has not been proved blind to the underlying fields. So `b_g/c_g` is now explicitly locked as an active residual.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Psi Metric Coframe Contract

{markdown_table(contract, ["contract_id", "object", "condition_or_theorem", "status", "what_is_derived", "missing_before_claim", "fallback_residual", "valid_for_claim"])}

## Connection Derivative Stack Gate

{markdown_table(stack, ["gate_id", "stack_layer", "required_input", "result", "leak_if_missing", "next_evidence", "valid_for_claim"])}

## Bg/Cg Residual Lock

{markdown_table(bg_lock, ["lock_id", "coefficient", "lock_rule", "why_locked", "bound_or_derivation_needed", "status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is not grim, but it is strict. The nice result is that the metric branch is not mathematically nonsense: once a Lorentzian `g_obs` is owned, a local coframe and compatible matter derivative stack are standard. The hard missing piece is upstream: the parent action must make `g_obs[psi]` real rather than a repair ansatz, and it must prove matter sees only that metric/coframe. Until that theorem exists, the local-GR branch carries `b_g/c_g`.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    contract = coframe_contract_rows(generated_utc)
    stack = connection_stack_rows(generated_utc)
    bg_lock = bg_residual_lock_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, contract, stack, bg_lock, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(COFRAME_CONTRACT_PATH, contract, ["contract_id", "object", "condition_or_theorem", "status", "what_is_derived", "missing_before_claim", "fallback_residual", "valid_for_claim", "generated_utc"])
    write_csv(CONNECTION_STACK_PATH, stack, ["gate_id", "stack_layer", "required_input", "result", "leak_if_missing", "next_evidence", "valid_for_claim", "generated_utc"])
    write_csv(BG_RESIDUAL_LOCK_PATH, bg_lock, ["lock_id", "coefficient", "lock_rule", "why_locked", "bound_or_derivation_needed", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, contract, stack, bg_lock, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"785 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
