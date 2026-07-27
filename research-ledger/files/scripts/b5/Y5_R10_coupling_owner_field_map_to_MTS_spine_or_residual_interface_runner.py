from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "783-Y5-R10-coupling-owner-field-map-to-MTS-spine-or-residual-interface-runner.md"
NEXT_TARGET = "784-Y5-R10-observed-metric-from-psi-map-or-coupling-owner-demotion.md"
STATUS = "Y5_R10_783_coupling_owner_field_map_runner_built_partial_metric_map_residual_interface_retained_nonclaim"
CLAIM_CEILING = "field_map_runner_only_partial_metric_alignment_no_adopted_parent_owner_no_coupling_zero_no_local_GR_Newton_PPN_R10_R11_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_783_SOURCE_REGISTER.csv"
FIELD_MAP_PATH = RESIDUALS / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv"
MAP_VERDICT_PATH = RESIDUALS / "P8_Y5_R10_783_FIELD_MAP_VERDICT_GATE.csv"
RESIDUAL_RUNNER_PATH = RESIDUALS / "P8_Y5_R10_783_RESIDUAL_INTERFACE_RUNNER.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_783_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_783_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_783_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_783_ADOPTED_PARENT_COUPLING_OWNER_ACTION.csv",
    RESIDUALS / "P8_Y5_R10_783_FULL_SPINE_FIELD_MAP_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_783_COUPLING_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_783_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    FIELD_MAP_PATH,
    MAP_VERDICT_PATH,
    RESIDUAL_RUNNER_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "782_doc": {
        "path": POST_CHECKPOINT / "782-Y5-R10-minimal-parent-coupling-owner-consistency-gate.md",
        "needles": ["CG782_0_spine_variable_map", "783-Y5-R10-coupling-owner-field-map-to-MTS-spine-or-residual-interface-runner.md"],
        "role": "immediate 783 handoff",
    },
    "782_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_782_VALIDATION.csv",
        "needles": ["V782_4_not_adopted_verdict", "V782_15_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "782_gate": {
        "path": RESIDUALS / "P8_Y5_R10_782_CONSISTENCY_GATE.csv",
        "needles": ["CG782_0_spine_variable_map", "not_adopted_viable_candidate"],
        "role": "field-map consistency gate",
    },
    "781_action": {
        "path": RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
        "needles": ["MPC781_7_contract_verdict", "S_parent=S_grav"],
        "role": "candidate owner action",
    },
    "781_interface": {
        "path": RESIDUALS / "P8_Y5_R10_781_EMPIRICAL_RESIDUAL_INTERFACE.csv",
        "needles": ["ERI781_0_b_g", "ERI781_5_W_Ic"],
        "role": "residual fallback interface",
    },
    "spine_03": {
        "path": FORMALIZATION / "03-unified-field-theory-programme.md",
        "needles": ["psi", "MTS microscopic dynamics -> emergent metric -> GR"],
        "role": "programme spine and GR/Newton chain",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["ψ", "Γ_mem", "g_μν", "χ", "g(z)"],
        "role": "minimal unification spine variables",
    },
    "ledger_14": {
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": ["g_μν = η_μν + L_*²", "Γ_mem"],
        "role": "field definitions and dimensional ledger",
    },
    "postulates_18": {
        "path": FORMALIZATION / "18-sign-conventions-and-field-postulates.md",
        "needles": ["G_μν + Γ_G g_μν", "Q^ν"],
        "role": "sign conventions and exchange postulates",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "GR-limit standard",
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


def field_map_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "map_id": "FM783_0_Phi_parent",
            "candidate_object": "Phi_parent",
            "spine_object": "{psi, Gamma_mem, g_mu_nu/e_obs, matter, chi, Gamma_G/Gamma_kappa, activation variables}",
            "proposed_map": "Phi_parent may be the full MTS field bundle, not a single new field",
            "map_status": "plausible_bundle_not_defined",
            "risk": "too broad unless the quotient map q is explicitly defined",
            "next_evidence": "define Phi_parent components and their gauge/quotient directions",
            "residual_if_unmapped": "candidate action remains external contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_1_Q",
            "candidate_object": "Q=q(Phi_parent)",
            "spine_object": "quotient data feeding observed geometry and matter variables",
            "proposed_map": "Q could be the ordinary-matter-visible quotient of the MTS field bundle",
            "map_status": "needed_but_not_owned",
            "risk": "renames the missing quotient theorem unless q and ker(Dq) are written",
            "next_evidence": "explicit q(Phi) and vertical generator basis",
            "residual_if_unmapped": "b_g,b_theta,b_kappa remain active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_2_e_obs",
            "candidate_object": "e_obs/g_obs",
            "spine_object": "g_mu_nu emergent/effective metric from psi",
            "proposed_map": "g_obs == g_mu_nu with g_mu_nu = eta_mu_nu + L_*^2 <partial_mu psi partial_nu psi>_smooth in the metric-repair branch",
            "map_status": "strongest_partial_alignment",
            "risk": "coframe, connection, and covariance/action ownership remain unproved",
            "next_evidence": "derive e_obs and compatible connection from psi metric ansatz",
            "residual_if_unmapped": "frame/readout residual b_g remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_3_Gamma_mem",
            "candidate_object": "residual/gravity sector in S_grav[g_obs,R_phys]",
            "spine_object": "Gamma_mem curvature-memory / irreversible exchange field",
            "proposed_map": "Gamma_mem belongs in S_grav/residual dynamics, not ordinary matter coupling",
            "map_status": "separation_rule_needed",
            "risk": "if matter sees Gamma_mem directly, coupling residual returns",
            "next_evidence": "show Gamma_mem affects matter only through g_obs or retained R_phys",
            "residual_if_unmapped": "exchange/coupling residual remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_4_Gamma_G_Gamma_kappa",
            "candidate_object": "cosmological/local curvature memory parameters",
            "spine_object": "Gamma_G and Gamma_kappa",
            "proposed_map": "Gamma_G/Gamma_kappa are sector projections of memory/exchange, not matter constants",
            "map_status": "partial_sector_projection",
            "risk": "direct dependence in matter/readout constants would violate coupling owner",
            "next_evidence": "projection equations and no direct theta_A dependence",
            "residual_if_unmapped": "b_theta or b_kappa residuals remain active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_5_chi",
            "candidate_object": "transport/galaxy support sector",
            "spine_object": "chi macroscopic transport-response field",
            "proposed_map": "chi should remain residual/transport sector, outside ordinary matter coupling quotient unless explicitly observable",
            "map_status": "must_be_separated",
            "risk": "universal coupling owner could erase galaxy phenomenology if chi is forced into ordinary matter quotient",
            "next_evidence": "sector separation showing chi affects dynamics without hidden matter readout coupling",
            "residual_if_unmapped": "galaxy residual interface remains separate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_6_gz",
            "candidate_object": "cosmological activation/readout",
            "spine_object": "g(z) cosmological activation fraction",
            "proposed_map": "g(z) is an emergent FLRW projection of memory/activation, not a local matter coupling variable",
            "map_status": "emergent_not_parent_mapped",
            "risk": "using g(z) inside Q would mix empirical cosmology fit variables into local matter action",
            "next_evidence": "FLRW projection from parent memory action",
            "residual_if_unmapped": "cosmology calibration residual stays outside local coupling owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_7_q_loc",
            "candidate_object": "R_phys local leakage component",
            "spine_object": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "proposed_map": "q_loc is a physical residual component, not part of the matter-visible quotient Q",
            "map_status": "residual_not_quotient",
            "risk": "putting q_loc into Q lets matter see the residual and reopens coupling",
            "next_evidence": "q_loc theorem-zero or component profile/bound",
            "residual_if_unmapped": "C_qmu and PPN alpha3 residuals remain active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "FM783_8_R_phys",
            "candidate_object": "R_phys",
            "spine_object": "{q_loc,Y5,Y6,PPN,boundary,coupling} residual vector",
            "proposed_map": "R_phys is the diagnostic/penalty vector for local-GR recovery, not an ordinary matter field",
            "map_status": "diagnostic_vector_not_action_owned",
            "risk": "candidate action may penalize residuals rather than derive them",
            "next_evidence": "derive R_phys from parent Euler/Ward identities or keep empirical residual interface",
            "residual_if_unmapped": "local-GR proof remains blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def map_verdict_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "MVG783_0_metric_alignment",
            "question": "Does e_obs/g_obs have a plausible MTS spine anchor?",
            "result": "partial_yes",
            "evidence": "formalization ledger gives g_mu_nu = eta_mu_nu + L_*^2 <partial psi partial psi>_smooth",
            "claim_effect": "supports next target focused on observed metric from psi",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "verdict_id": "MVG783_1_Q_alignment",
            "question": "Is Q=q(Phi_parent) already defined by the spine?",
            "result": "no",
            "evidence": "Q is a useful candidate quotient but q and ker(Dq) are not in the spine as owned objects",
            "claim_effect": "no adoption of parent coupling owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "verdict_id": "MVG783_2_residual_separation",
            "question": "Can Gamma_mem/chi/g(z)/q_loc be separated from ordinary matter coupling?",
            "result": "partial_policy_only",
            "evidence": "separation is logically required but not derived by current parent action",
            "claim_effect": "residual interface remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "verdict_id": "MVG783_3_field_map_verdict",
            "question": "Can the candidate owner action be adopted after this map?",
            "result": "not_adopted_partial_map_only",
            "evidence": "only e_obs/g_obs has a strong partial anchor; Q/R_phys/residual sectors are not fully owned",
            "claim_effect": "next target is observed metric from psi map or demotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def residual_runner_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RIR783_0_metric_frame_branch",
            "trigger": "FM783_2 e_obs/g_obs map remains partial",
            "route": "derive observed metric/coframe from psi or retain b_g/c_g as residual",
            "inputs_needed": "metric ansatz covariance, coframe square root/tetrad, compatible connection, no hidden frame map",
            "current_status": "derive_next",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RIR783_1_quotient_branch",
            "trigger": "FM783_1 Q not owned",
            "route": "define q(Phi_parent) and ker(Dq) or keep b_theta/b_kappa residuals",
            "inputs_needed": "quotient map, vertical generators, no-marker/no-spurion classification",
            "current_status": "blocked_missing_q",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RIR783_2_memory_transport_branch",
            "trigger": "Gamma_mem/chi/g(z) not ordinary matter coupling variables",
            "route": "separate residual dynamics from matter coupling or carry empirical sector residuals",
            "inputs_needed": "sector separation map and cosmology/galaxy projection equations",
            "current_status": "residual_interface_active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "RIR783_3_local_residual_branch",
            "trigger": "q_loc/R_phys not action-owned",
            "route": "derive q_loc/R_phys from Euler/Ward identities or keep C_qmu, B_SM, W_Ic as empirical coefficients",
            "inputs_needed": "q_loc component profile/theorem-zero, PPN response matrix, boundary/source-measure rows",
            "current_status": "local_GR_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D783_0_partial_map",
            "decision": "accept partial metric alignment only",
            "reason": "e_obs/g_obs can plausibly map to the emergent metric from psi, but this is not yet a coframe/action proof",
            "claim_status": "partial_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D783_1_no_adoption",
            "decision": "do not adopt candidate parent coupling owner",
            "reason": "Q, R_phys, memory/transport separation, and residual locks are not owned",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D783_2_residual_interface",
            "decision": "keep residual interface live",
            "reason": "unmapped fields must become explicit residual coefficients rather than hidden assumptions",
            "claim_status": "interface_active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D783_3_next_target",
            "decision": "derive observed metric/coframe from psi or demote owner route",
            "reason": "the metric map is the strongest partial anchor and the least arbitrary next derivation",
            "claim_status": "next_target_selected",
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
            "main_result": "field-map runner found strongest partial anchor at e_obs/g_obs from psi; Q/R_phys/residual sectors remain unmapped or diagnostic, so parent owner is not adopted",
            "hard_blocker": "no explicit q(Phi), ker(Dq), coframe/connection derivation, or residual-sector separation proof",
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
    field_map: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    residual_runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_782_clean = all(validation_clean(number) for number in range(665, 783))
    field_map_complete = len(field_map) == 9
    metric_partial_anchor = any(row["map_id"] == "FM783_2_e_obs" and row["map_status"] == "strongest_partial_alignment" for row in field_map)
    q_not_owned = any(row["map_id"] == "FM783_1_Q" and row["map_status"] == "needed_but_not_owned" for row in field_map)
    residual_not_quotient = any(row["map_id"] == "FM783_7_q_loc" and row["map_status"] == "residual_not_quotient" for row in field_map)
    verdicts_complete = len(verdicts) == 4
    not_adopted = any(row["verdict_id"] == "MVG783_3_field_map_verdict" and row["result"] == "not_adopted_partial_map_only" for row in verdicts)
    residual_runner_complete = len(residual_runner) == 4
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D783_3_next_target" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, field_map, verdicts, residual_runner, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V783_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V783_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V783_2_prior_665_782_clean", prior_665_782_clean, "665-782 validation rows have no failures"),
        ("V783_3_field_map_complete", field_map_complete, "candidate-to-spine map rows complete"),
        ("V783_4_metric_partial_anchor", metric_partial_anchor, "e_obs/g_obs has strongest partial alignment"),
        ("V783_5_Q_not_owned", q_not_owned, "Q quotient is not owned"),
        ("V783_6_q_loc_residual_not_quotient", residual_not_quotient, "q_loc kept as residual component"),
        ("V783_7_verdicts_complete", verdicts_complete, "field-map verdict rows complete"),
        ("V783_8_not_adopted", not_adopted, "candidate owner not adopted"),
        ("V783_9_residual_runner_complete", residual_runner_complete, "residual interface runner rows complete"),
        ("V783_10_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V783_11_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V783_12_claim_artifacts_absent", claim_artifacts_absent, "no adopted-action/field-map/zero/local-GR claim artifact fabricated"),
        ("V783_13_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V783_14_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V783_15_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    field_map: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    residual_runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 783 - Y5 R10 Coupling Owner Field Map To MTS Spine Or Residual Interface Runner

Current result: **the candidate coupling owner gets one strong partial anchor: `e_obs/g_obs` can plausibly map to the emergent/effective metric from `psi`**. Everything else is still too loose for adoption. `Q=q(Phi_parent)` is not owned, `R_phys` is diagnostic rather than derived, and `Gamma_mem/chi/g(z)/q_loc` must be separated from ordinary matter coupling or carried as explicit residuals. So this advances the derivation route without letting it cheat.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Coupling Owner Field Map

{markdown_table(field_map, ["map_id", "candidate_object", "spine_object", "proposed_map", "map_status", "risk", "next_evidence", "residual_if_unmapped", "valid_for_claim"])}

## Field Map Verdict Gate

{markdown_table(verdicts, ["verdict_id", "question", "result", "evidence", "claim_effect", "valid_for_claim"])}

## Residual Interface Runner

{markdown_table(residual_runner, ["runner_id", "trigger", "route", "inputs_needed", "current_status", "next_target", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This points to the least arbitrary next derivation: do not start with all of `Q`. Start with the piece the spine already knows how to talk about: the observed metric from `psi`. If we can derive a proper coframe/connection and show matter sees that metric only, the coupling owner route gains real teeth. If not, demote the owner route and run the empirical residual interface.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    field_map = field_map_rows(generated_utc)
    verdicts = map_verdict_rows(generated_utc)
    residual_runner = residual_runner_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, field_map, verdicts, residual_runner, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(FIELD_MAP_PATH, field_map, ["map_id", "candidate_object", "spine_object", "proposed_map", "map_status", "risk", "next_evidence", "residual_if_unmapped", "valid_for_claim", "generated_utc"])
    write_csv(MAP_VERDICT_PATH, verdicts, ["verdict_id", "question", "result", "evidence", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_RUNNER_PATH, residual_runner, ["runner_id", "trigger", "route", "inputs_needed", "current_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, field_map, verdicts, residual_runner, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"783 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
