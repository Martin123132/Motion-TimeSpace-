from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md"
NEXT_TARGET = "791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md"
STATUS = "Y5_R10_790_MTS_exchange_stress_decomposition_and_local_suppression_gates_built_nonclaim"
CLAIM_CEILING = "decomposition_and_gate_ledger_only_no_TMTS_Q_torsion_boundary_frame_suppression_proof_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_790_SOURCE_REGISTER.csv"
STRESS_DECOMPOSITION_PATH = RESIDUALS / "P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv"
SUPPRESSION_GATES_PATH = RESIDUALS / "P8_Y5_R10_790_LOCAL_SUPPRESSION_GATES.csv"
ARENA_MAP_PATH = RESIDUALS / "P8_Y5_R10_790_RESIDUAL_TO_TEST_ARENA_MAP.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_790_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_790_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_790_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_790_LOCAL_GR_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_790_TMTS_SUPPRESSION_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_790_QLOC_ZERO_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_790_PPN_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    STRESS_DECOMPOSITION_PATH,
    SUPPRESSION_GATES_PATH,
    ARENA_MAP_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "789_doc": {
        "path": POST_CHECKPOINT / "789-Y5-R10-palatini-tetrad-GR-limit-with-MTS-exchange-contract.md",
        "needles": ["Current result", "T_MTS"],
        "role": "immediate 790 handoff",
    },
    "789_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_789_VALIDATION.csv",
        "needles": ["V789_6_GR_recovery_gate", "V789_14_no_local_GR_claim"],
        "role": "prior validation guard",
    },
    "789_gr_contract": {
        "path": RESIDUALS / "P8_Y5_R10_789_PALATINI_TETRAD_GR_LIMIT_CONTRACT.csv",
        "needles": ["PTG789_4_GR_recovery", "PTG789_5_Newton_recovery"],
        "role": "GR/Newton reduction contract",
    },
    "789_residual_vector": {
        "path": RESIDUALS / "P8_Y5_R10_789_NEWTON_PPN_RESIDUAL_VECTOR.csv",
        "needles": ["NPR789_1_T_MTS", "NPR789_2_Q_nu"],
        "role": "local residual vector",
    },
    "789_inputs": {
        "path": RESIDUALS / "P8_Y5_R10_789_MTS_EXCHANGE_INPUT_REQUIREMENTS.csv",
        "needles": ["MIR789_0_T_MTS_decomposition", "MIR789_1_exchange_current"],
        "role": "missing input ledger",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["Einstein-Equation Convention", "Q^"],
        "role": "Einstein/exchange convention",
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


def stress_decomposition_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "ESD790_0_trace_memory",
            "component": "trace/isotropic memory stress",
            "candidate_form": "T_trace_mu_nu = -Lambda_MTS(x) g_mu_nu / kappa_GR",
            "divergence_condition": "nabla_mu T_trace^mu_nu = -(1/kappa_GR) nabla_nu Lambda_MTS, so local GR requires nabla Lambda_MTS -> 0 or cancellation by another component",
            "local_suppression_condition": "|Lambda_MTS| L_local^2 and |nabla Lambda_MTS| L_local^3 below local-gravity bounds",
            "status": "decomposition_candidate_missing_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "ESD790_1_exchange_longitudinal",
            "component": "exchange-current stress",
            "candidate_form": "find T_Q_mu_nu such that nabla_mu T_Q^mu_nu = -Q_nu and nabla_mu T_matter^mu_nu = Q_nu",
            "divergence_condition": "total stress is Bianchi-compatible only if Q_matter + Q_MTS + Q_boundary = 0",
            "local_suppression_condition": "Q_nu or q_loc_nu must vanish or be bounded below PPN/orbital/nonconservation limits",
            "status": "primary_missing_derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "ESD790_2_anisotropic_memory",
            "component": "anisotropic/shear MTS stress",
            "candidate_form": "Pi_MTS_mu_nu = T_MTS_mu_nu - trace and longitudinal pieces",
            "divergence_condition": "must either be transverse or have divergence accounted in Q_nu",
            "local_suppression_condition": "|Pi_MTS|/rho_matter and PPN gamma/beta shifts below local bounds",
            "status": "missing_amplitude_and_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "ESD790_3_torsion_spin",
            "component": "spin/torsion/hyperstress source",
            "candidate_form": "tau_MTS_ab or Delta_omega S_MTS source in Palatini connection equation",
            "divergence_condition": "local Lorentz/Ward identities must carry antisymmetric stress into spin or set it zero",
            "local_suppression_condition": "tau_MTS -> 0 or torsion observables below local spin/precession bounds",
            "status": "missing_connection_variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "ESD790_4_boundary_source_measure",
            "component": "boundary/source-measure stress",
            "candidate_form": "T_boundary_mu_nu = -(2/sqrt(-g)) delta S_boundary/source / delta g^mu_nu",
            "divergence_condition": "boundary/source terms must be locally silent or included in total conservation",
            "local_suppression_condition": "B_obs/source-measure coefficient zero or bounded in R10/PPN/clock/orbital arenas",
            "status": "missing_boundary_variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "ESD790_5_frame_readout",
            "component": "matter-frame/readout leakage",
            "candidate_form": "not a stress alone: b_g/c_g and W_Ic encode direct matter/readout coupling outside e,omega",
            "divergence_condition": "cannot be hidden inside T_MTS without violating matter universality",
            "local_suppression_condition": "no-spurion theorem or PPN/clock/orbital response bounds",
            "status": "active_residual_from_785_789",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def suppression_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "LSG790_0_Ward_compatible_split",
            "gate": "T_total = T_matter + T_trace + T_Q + Pi_MTS + T_boundary must satisfy nabla_mu T_total^mu_nu = 0",
            "acceptance": "explicit covariant S_MTS or Ward identity produces every divergence term",
            "current_status": "blocked_missing_parent_variation",
            "failure_mode": "arbitrary MTS source violates Bianchi identity",
            "next_input": "derive Q_nu/q_loc and T_MTS split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_1_exchange_current_zero_or_bound",
            "gate": "Q_nu/q_loc_nu must vanish or be bounded locally",
            "acceptance": "Q_nu=0 theorem in local regime or numerical bound below PPN/orbital/matter-conservation limits",
            "current_status": "primary_next_gate",
            "failure_mode": "non-geodesic force or matter nonconservation",
            "next_input": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_2_trace_memory_local_silence",
            "gate": "Lambda_MTS must be locally constant/small or absorbed into measured cosmological background",
            "acceptance": "local gradient and amplitude below lab/Solar bounds",
            "current_status": "missing_projection",
            "failure_mode": "local fifth-force/source-renormalization",
            "next_input": "trace-memory projection from S_MTS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_3_anisotropic_PPN_suppression",
            "gate": "Pi_MTS must not shift gamma,beta,alpha_i beyond local bounds",
            "acceptance": "PPN residual vector computed or theorem-zero",
            "current_status": "missing_PPN_map",
            "failure_mode": "local metric deviates from GR/Newton",
            "next_input": "PPN response matrix for Pi_MTS and b_g/c_g",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_4_torsion_connection_silence",
            "gate": "MTS spin/torsion source must vanish or be bounded",
            "acceptance": "Palatini connection equation sets omega=omega[e] locally or torsion bounds pass",
            "current_status": "missing_connection_variation",
            "failure_mode": "spin/precession/contact-force deviations",
            "next_input": "delta_omega S_MTS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_5_boundary_source_silence",
            "gate": "boundary/source-measure terms must not alter local field equations",
            "acceptance": "B_obs/source-measure theorem-zero or sourced bound rows",
            "current_status": "missing_boundary_source_measure",
            "failure_mode": "hidden local force/source shift",
            "next_input": "boundary variation/source-measure coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_6_matter_frame_universality",
            "gate": "ordinary matter sees only e, omega[e], and owned gauge fields",
            "acceptance": "no direct Phi_MTS/psi/Gamma/q_loc dependence in S_matter",
            "current_status": "blocked_missing_matter_signature",
            "failure_mode": "equivalence-principle/readout violation",
            "next_input": "parent-signed S_matter/no-spurion audit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LSG790_7_Newton_limit_gate",
            "gate": "after all residuals close, weak-field GR gives Poisson/Newton",
            "acceptance": "g_00=-1-2Phi/c^2 and residual vector below bounds",
            "current_status": "conditional_on_LSG790_0_to_6",
            "failure_mode": "MTS remains modified gravity rather than GR limit",
            "next_input": "close suppression gates first",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def arena_map_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ATM790_0_PPN",
            "residuals": "Pi_MTS, T_trace gradients, Q_nu, b_g/c_g, torsion",
            "test_arena": "Solar-system PPN",
            "needed_output": "gamma,beta,alpha_i response vector or theorem-zero",
            "claim_status": "not_test_ready",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "ATM790_1_orbital",
            "residuals": "Q_nu/q_loc, boundary/source-measure, trace gradients",
            "test_arena": "planetary/lunar/binary orbital residuals",
            "needed_output": "extra acceleration vector and ephemeris bound map",
            "claim_status": "not_test_ready",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "ATM790_2_clocks",
            "residuals": "b_g/c_g, trace gradients, frame/readout leakage",
            "test_arena": "clock redshift/time dilation",
            "needed_output": "clock observable response to e/g mismatch and exchange fields",
            "claim_status": "not_test_ready",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "ATM790_3_R10",
            "residuals": "boundary/source-measure, frame leakage, trace/exchange projected fifth-force",
            "test_arena": "short-range inverse-square/fifth-force",
            "needed_output": "alpha(lambda) projection with real bound curve",
            "claim_status": "not_test_ready",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "ATM790_4_cosmology",
            "residuals": "T_trace, exchange/current, anisotropic stress",
            "test_arena": "FLRW/Pantheon/BAO/CMB/growth",
            "needed_output": "cosmological projection distinct from local suppression",
            "claim_status": "separate_empirical_pillar_not_local_GR_proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "ATM790_5_galaxy",
            "residuals": "anisotropic/memory stress and transport fields",
            "test_arena": "SPARC/ETG/rotation curves",
            "needed_output": "galaxy projection separate from Solar local-GR suppression",
            "claim_status": "separate_empirical_pillar_not_local_GR_proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D790_0_decomposition_retained",
            "decision": "retain six-component MTS residual decomposition",
            "reason": "it maps every 789 blocker to either a Ward-compatible stress/current, torsion source, boundary term, or frame coupling",
            "result": "decomposition_ready_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D790_1_Q_first",
            "decision": "derive or bound Q_nu/q_loc first",
            "reason": "exchange current is the Bianchi/matter-conservation gate that controls whether local GR can even be stated cleanly",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D790_2_no_local_claim",
            "decision": "do not claim local GR/Newton recovery",
            "reason": "no suppression theorem or bound is closed for T_MTS, Q, torsion, boundary, or frame leakage",
            "result": "claim_blocked",
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
            "main_result": "T_MTS has been decomposed into trace memory, exchange-current, anisotropic memory, torsion/spin, boundary/source-measure, and frame/readout residual channels with explicit local suppression gates",
            "hard_blocker": "Q_nu/q_loc is now the first gate because it controls Bianchi-compatible exchange and ordinary matter conservation in the local GR limit",
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
    stress: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_789_clean = all(validation_clean(number) for number in range(665, 790))
    stress_complete = len(stress) == 6
    exchange_component_present = any(row["component_id"] == "ESD790_1_exchange_longitudinal" for row in stress)
    frame_component_present = any(row["component_id"] == "ESD790_5_frame_readout" for row in stress)
    gates_complete = len(gates) == 8
    q_gate_primary = any(row["gate_id"] == "LSG790_1_exchange_current_zero_or_bound" and row["current_status"] == "primary_next_gate" for row in gates)
    newton_conditional = any(row["gate_id"] == "LSG790_7_Newton_limit_gate" and row["current_status"] == "conditional_on_LSG790_0_to_6" for row in gates)
    arenas_complete = len(arenas) == 6
    local_arenas_not_ready = all(row["claim_status"] != "ready" for row in arenas)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D790_1_Q_first" for row in decisions)
    no_local_claim = any(row["decision_id"] == "D790_2_no_local_claim" and row["result"] == "claim_blocked" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, stress, gates, arenas, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V790_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V790_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V790_2_prior_665_789_clean", prior_665_789_clean, "665-789 validation rows have no failures"),
        ("V790_3_stress_decomposition_complete", stress_complete, "six residual stress/current channels recorded"),
        ("V790_4_exchange_component_present", exchange_component_present, "Q_nu/q_loc channel recorded"),
        ("V790_5_frame_component_present", frame_component_present, "frame/readout leakage channel recorded"),
        ("V790_6_suppression_gates_complete", gates_complete, "local suppression gates complete"),
        ("V790_7_Q_gate_primary", q_gate_primary, "exchange current chosen as primary next gate"),
        ("V790_8_Newton_conditional", newton_conditional, "Newton gate conditional on residual closure"),
        ("V790_9_arenas_complete", arenas_complete, "test arena map rows complete"),
        ("V790_10_local_arenas_not_ready", local_arenas_not_ready, "no local arena marked ready"),
        ("V790_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V790_12_no_local_claim", no_local_claim, "local GR/Newton claim remains blocked"),
        ("V790_13_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V790_14_claim_artifacts_absent", claim_artifacts_absent, "no local-GR/TMTS/Qloc/PPN claim artifact fabricated"),
        ("V790_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V790_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V790_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 790 - Y5 R10 MTS Exchange Stress Decomposition And Local Suppression Gates

Current result: **the local-GR residual vector is now decomposed instead of being a blob**. `T_MTS` is split into trace memory, exchange-current, anisotropic memory, torsion/spin, boundary/source-measure, and frame/readout channels. This does not prove local GR, but it turns the problem into named gates. The first hard gate is `Q_nu/q_loc`: if the exchange current is not Ward-compatible and locally zero/bounded, the GR/Newton reduction cannot honestly close.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Exchange Stress Decomposition

{markdown_table(stress, ["component_id", "component", "candidate_form", "divergence_condition", "local_suppression_condition", "status", "valid_for_claim"])}

## Local Suppression Gates

{markdown_table(gates, ["gate_id", "gate", "acceptance", "current_status", "failure_mode", "next_input", "valid_for_claim"])}

## Residual To Test Arena Map

{markdown_table(arenas, ["arena_id", "residuals", "test_arena", "needed_output", "claim_status", "valid_for_claim"])}

## Derivation Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is useful because the next target is no longer vague. The local GR branch now lives or dies first on a Ward-compatible exchange-current theorem: derive `Q_nu/q_loc` from the parent action and prove it vanishes locally, or compute a bound that survives PPN/orbital/matter-conservation tests. Everything else is queued behind that.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    stress = stress_decomposition_rows(generated_utc)
    gates = suppression_gate_rows(generated_utc)
    arenas = arena_map_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, stress, gates, arenas, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(STRESS_DECOMPOSITION_PATH, stress, ["component_id", "component", "candidate_form", "divergence_condition", "local_suppression_condition", "status", "valid_for_claim", "generated_utc"])
    write_csv(SUPPRESSION_GATES_PATH, gates, ["gate_id", "gate", "acceptance", "current_status", "failure_mode", "next_input", "valid_for_claim", "generated_utc"])
    write_csv(ARENA_MAP_PATH, arenas, ["arena_id", "residuals", "test_arena", "needed_output", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, stress, gates, arenas, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"790 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
