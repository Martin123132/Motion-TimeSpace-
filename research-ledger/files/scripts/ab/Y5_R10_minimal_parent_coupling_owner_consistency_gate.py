from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "782-Y5-R10-minimal-parent-coupling-owner-consistency-gate.md"
NEXT_TARGET = "783-Y5-R10-coupling-owner-field-map-to-MTS-spine-or-residual-interface-runner.md"
STATUS = "Y5_R10_782_minimal_parent_coupling_owner_consistency_gate_run_candidate_viable_but_not_adopted_nonclaim"
CLAIM_CEILING = "consistency_gate_only_candidate_viable_not_adopted_no_coupling_zero_no_local_GR_Newton_PPN_R10_R11_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_782_SOURCE_REGISTER.csv"
CONSISTENCY_GATE_PATH = RESIDUALS / "P8_Y5_R10_782_CONSISTENCY_GATE.csv"
LIMIT_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_782_LIMIT_AND_PILLAR_COMPATIBILITY_MATRIX.csv"
RISK_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_782_OVERCONSTRAINT_RISK_LEDGER.csv"
ADOPTION_DECISION_PATH = RESIDUALS / "P8_Y5_R10_782_ADOPTION_DECISION.csv"
NEXT_INPUTS_PATH = RESIDUALS / "P8_Y5_R10_782_NEXT_INPUT_REQUIREMENTS.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_782_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_782_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_782_ADOPTED_PARENT_COUPLING_OWNER_ACTION.csv",
    RESIDUALS / "P8_Y5_R10_782_COUPLING_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_782_LOCAL_GR_REENTRY_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_782_NEWTON_LIMIT_CLAIM.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    CONSISTENCY_GATE_PATH,
    LIMIT_MATRIX_PATH,
    RISK_LEDGER_PATH,
    ADOPTION_DECISION_PATH,
    NEXT_INPUTS_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "781_doc": {
        "path": POST_CHECKPOINT / "781-Y5-R10-minimal-parent-coupling-owner-action-or-empirical-residual-interface.md",
        "needles": ["MPC781_7_contract_verdict", "782-Y5-R10-minimal-parent-coupling-owner-consistency-gate.md"],
        "role": "immediate 782 handoff",
    },
    "781_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_781_VALIDATION.csv",
        "needles": ["V781_3_action_contract_complete", "V781_7_adoption_not_claimed"],
        "role": "prior validation guard",
    },
    "781_action": {
        "path": RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
        "needles": ["MPC781_7_contract_verdict", "candidate_only_requires_782_consistency_gate"],
        "role": "candidate parent coupling owner action",
    },
    "781_interface": {
        "path": RESIDUALS / "P8_Y5_R10_781_EMPIRICAL_RESIDUAL_INTERFACE.csv",
        "needles": ["ERI781_3_C_qmu", "ERI781_5_W_Ic"],
        "role": "empirical residual fallback interface",
    },
    "780_triage": {
        "path": RESIDUALS / "P8_Y5_R10_780_LOCAL_GR_BRANCH_TRIAGE.csv",
        "needles": ["LGT780_4_local_GR_status", "not_derived_not_dead"],
        "role": "local-GR branch triage",
    },
    "777_lock_map": {
        "path": RESIDUALS / "P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv",
        "needles": ["PRL777_6_verdict", "physical_lock_not_proved"],
        "role": "full physical residual lock map",
    },
    "spine_03": {
        "path": FORMALIZATION / "03-unified-field-theory-programme.md",
        "needles": ["MTS microscopic dynamics -> emergent metric -> GR", "This is the central"],
        "role": "full programme and GR/Newton chain",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["Minimal Unification Spine", "motion/curvature-memory field theory"],
        "role": "unification spine",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "testing readiness and GR-limit demand",
    },
    "grossmann_148": {
        "path": FORMALIZATION / "148-fair-comparative-testing-and-grossmann-protocol.md",
        "needles": ["Grossmann mode", "same test where possible"],
        "role": "fair comparative testing discipline",
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


def consistency_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG782_0_spine_variable_map",
            "gate": "Map candidate Q/e_obs/R_phys variables to the MTS spine fields psi, Gamma_mem/Gamma_kappa, chi, g(z), and local q_loc.",
            "candidate_effect": "creates a clean quotient geometry layer for matter coupling",
            "result": "partial_open",
            "blocker": "Q=q(Phi_parent) is not yet mapped to the named MTS fields and sector variables",
            "adoption_effect": "cannot adopt until field-map exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_1_action_identity",
            "gate": "Show S_parent is a current-MTS parent action, not a retrofit added only to silence local coupling.",
            "candidate_effect": "proposes a coherent parent action skeleton",
            "result": "fail_current_corpus",
            "blocker": "781 explicitly marks action candidate_contract_not_adopted and 780 found no parent-signed owner",
            "adoption_effect": "must remain proposal, not theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_2_GR_Newton_chain",
            "gate": "Derive MTS -> GR -> Newton, not merely matter coupling silence.",
            "candidate_effect": "helps remove one local residual block",
            "result": "not_sufficient",
            "blocker": "q_loc, Y5/Y6, PPN, boundary, and residual-vector rank locks remain open",
            "adoption_effect": "no local-GR/Newton claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_3_conservation_Bianchi",
            "gate": "Check diffeomorphism covariance and conservation without hiding exchange terms.",
            "candidate_effect": "Hilbert matter current can be conserved if S_matter is same-frame and diffeo invariant",
            "result": "conditional_only",
            "blocker": "non-EH exchange, boundary/projector terms, and source-measure flux are not jointly owned",
            "adoption_effect": "Bianchi cannot erase residuals yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_4_empirical_pillar_preservation",
            "gate": "Preserve galaxy/cosmology/time/EM/matter work while adding universal coupling owner.",
            "candidate_effect": "could make local sector cleaner",
            "result": "open_overconstraint_risk",
            "blocker": "strong universal coupling may kill or reclassify phenomenological sectors unless residual separation is explicit",
            "adoption_effect": "requires sector-by-sector compatibility map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_5_readout_completeness",
            "gate": "Write clock, photon, orbit, EM/charge, source, and PPN readout maps.",
            "candidate_effect": "names the readout descent target",
            "result": "not_closed",
            "blocker": "readout functionals are not yet sourced; W_Ic, C_qmu, and B_SM remain missing",
            "adoption_effect": "empirical residual interface remains necessary",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_6_no_ad_hoc_repair",
            "gate": "Avoid adding a local-only coupling owner that cannot be motivated from the full theory.",
            "candidate_effect": "minimal action is disciplined but still a repair candidate",
            "result": "policy_guard_active",
            "blocker": "needs independent derivation from MTS ontology, not just local-GR pressure",
            "adoption_effect": "continue as candidate under consistency testing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CG782_7_verdict",
            "gate": "Adopt minimal parent coupling owner as current MTS?",
            "candidate_effect": "viable candidate route to coupling silence",
            "result": "not_adopted_viable_candidate",
            "blocker": "field-map, GR/Newton chain, empirical pillar preservation, and readout maps are incomplete",
            "adoption_effect": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def limit_matrix_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "limit_id": "LPM782_0_GR_Newton",
            "arena": "local GR/Newton limit",
            "candidate_support": "removes one coupling leakage channel if adopted",
            "remaining_gap": "does not derive Einstein equations, q_loc=0, PPN vector zero, or Newtonian source calibration",
            "compatibility_result": "not_enough_for_claim",
            "next_evidence": "full residual-vector lock plus PPN/Newton limit proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "LPM782_1_R10_short_range",
            "arena": "short-range/local force R10",
            "candidate_support": "could set representative matter-frame coupling to zero",
            "remaining_gap": "C_qmu, B_SM/M_H, source flux, and q_loc component profiles remain missing",
            "compatibility_result": "bound_interface_needed",
            "next_evidence": "numeric source-measure bound or parent zero certificate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "LPM782_2_PPN_R11",
            "arena": "PPN/R11",
            "candidate_support": "readout descent could remove hidden-frame PPN response",
            "remaining_gap": "W_Ic response matrix, gauge/frame certificate, q_loc preferred-frame block missing",
            "compatibility_result": "not_closed",
            "next_evidence": "PPN coupling response matrix or theorem-zero rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "LPM782_3_cosmology",
            "arena": "Pantheon/BAO/CMB/growth",
            "candidate_support": "same matter geometry may discipline source/readout calibration",
            "remaining_gap": "Q/e_obs action not mapped to cosmological memory variables or activation parameters",
            "compatibility_result": "field_map_needed",
            "next_evidence": "cosmology-sector projection of Q and matter calibration",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "LPM782_4_galaxy",
            "arena": "galaxy/rotation empirical pillar",
            "candidate_support": "could separate matter readout from geometry/residual fields",
            "remaining_gap": "must not erase the phenomenological memory/transport response used in galaxy fits",
            "compatibility_result": "overconstraint_check_needed",
            "next_evidence": "sector separation showing galaxy residuals live outside ordinary matter coupling spurions",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "limit_id": "LPM782_5_EM_clock_charge",
            "arena": "EM/clock/charge",
            "candidate_support": "theta_A and owned charges can be superselection/readout data",
            "remaining_gap": "alpha_EM, charge normalization, clock constants, magnetic/EM interface not derived",
            "compatibility_result": "superselection_source_needed",
            "next_evidence": "no-marker/no-spurion source paths or explicit residual coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def risk_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "risk_id": "ORL782_0_symbol_collision",
            "risk": "candidate Q/e_obs layer may collide with existing MTS field meanings",
            "impact": "could make the parent action look cleaner by renaming rather than deriving",
            "mitigation": "build explicit field map from Q to psi/Gamma/chi/g(z)/q_loc sectors",
            "severity": "high",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "risk_id": "ORL782_1_overconstraint",
            "risk": "universal coupling owner may suppress desired nonlocal/memory phenomenology",
            "impact": "could protect local GR by killing galaxy/cosmology/EM mechanisms",
            "mitigation": "separate ordinary matter coupling from residual/gravity sector dynamics",
            "severity": "high",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "risk_id": "ORL782_2_boundary_silence",
            "risk": "bulk vertical silence may not survive boundary/projector/source-measure terms",
            "impact": "B_obs_source_measure could remain finite even if matter action descends",
            "mitigation": "prove compact no-flux/projector descent or keep B_SM residual",
            "severity": "high",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "risk_id": "ORL782_3_frame_readout",
            "risk": "observable readouts may use hidden frame maps not present in S_matter",
            "impact": "clocks, photons, EM charge, or orbit calibration can leak coupling despite same matter action",
            "mitigation": "write readout functionals and W_Ic/C_qmu interface rows",
            "severity": "high",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "risk_id": "ORL782_4_retrofit",
            "risk": "candidate owner action is adopted because it solves local tests, not because MTS derives it",
            "impact": "turns derivation programme into post-hoc patch",
            "mitigation": "require independent spine compatibility and field-map proof before adoption",
            "severity": "medium",
            "status": "guard_active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def adoption_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "AD782_0_candidate_viability",
            "decision": "minimal parent coupling owner is viable as a candidate",
            "reason": "it directly targets the missing coupling/source-measure owner without adding arbitrary fit terms",
            "result": "viable_candidate",
            "claim_status": "nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "AD782_1_adoption",
            "decision": "do not adopt as current MTS yet",
            "reason": "field-map, local-GR chain, readout maps, and empirical pillar preservation are incomplete",
            "result": "not_adopted",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "AD782_2_empirical_fallback",
            "decision": "keep empirical residual interface active",
            "reason": "if the owner action cannot be derived, residual coefficients must enter tests explicitly",
            "result": "fallback_ready",
            "claim_status": "interface_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "AD782_3_next_target",
            "decision": "map candidate owner fields to the MTS spine or run residual interface",
            "reason": "this is the next fork between derivation and empirical-residual route",
            "result": "next_target_selected",
            "claim_status": "nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_input_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "NIR782_0_field_map",
            "required_input": "Q=q(Phi_parent) to MTS field map",
            "why_needed": "prevents symbol renaming from masquerading as derivation",
            "acceptance_gate": "psi/Gamma_mem/Gamma_kappa/chi/g(z)/q_loc roles mapped or explicitly separated",
            "if_missing": "candidate action remains external contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NIR782_1_readout_maps",
            "required_input": "clock/photon/orbit/EM/source/PPN readout functionals",
            "why_needed": "matter action descent alone does not prove observable descent",
            "acceptance_gate": "O_i[e_obs,Psi,theta,A_owned] rows with no hidden map or finite coefficients",
            "if_missing": "W_Ic and C_qmu residuals stay active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NIR782_2_boundary_projector",
            "required_input": "compact no-flux/projector descent theorem or B_SM rows",
            "why_needed": "bulk zero can leak through boundary/source-measure projection",
            "acceptance_gate": "B_SM=0 theorem or no-cancellation numeric bound",
            "if_missing": "local-GR recovery remains blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NIR782_3_sector_preservation",
            "required_input": "sector separation map for galaxy/cosmology/EM/matter",
            "why_needed": "universal coupling must not erase the broader theory",
            "acceptance_gate": "ordinary matter coupling separated from residual memory/transport dynamics",
            "if_missing": "overconstraint risk stays high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "NIR782_4_local_rank",
            "required_input": "full physical residual-vector rank/zero proof",
            "why_needed": "coupling zero alone is not GR/Newton reduction",
            "acceptance_gate": "q_loc/Y5/Y6/PPN/boundary/coupling vector locked or bounded",
            "if_missing": "no MTS -> GR -> Newton claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "candidate parent coupling owner is coherent enough to pursue, but fails adoption as current MTS until mapped to the spine and checked against limits/pillars",
            "hard_blocker": "Q/e_obs/S_parent candidate is not yet tied to existing MTS fields or full GR/Newton residual-vector closure",
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
    gates: list[dict[str, Any]],
    limits: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_781_clean = all(validation_clean(number) for number in range(665, 782))
    consistency_complete = len(gates) == 8
    not_adopted_verdict = any(row["gate_id"] == "CG782_7_verdict" and row["result"] == "not_adopted_viable_candidate" for row in gates)
    limits_complete = len(limits) == 6
    risks_complete = len(risks) == 5
    high_risks_open = sum(1 for row in risks if row["severity"] == "high" and row["status"] == "open") >= 3
    adoption_complete = len(adoption) == 4
    adoption_not_claimed = any(row["decision_id"] == "AD782_1_adoption" and row["result"] == "not_adopted" for row in adoption)
    next_inputs_complete = len(inputs) == 5
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, gates, limits, risks, adoption, inputs, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "AD782_3_next_target" for row in adoption)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V782_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V782_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V782_2_prior_665_781_clean", prior_665_781_clean, "665-781 validation rows have no failures"),
        ("V782_3_consistency_gate_complete", consistency_complete, "eight consistency gates written"),
        ("V782_4_not_adopted_verdict", not_adopted_verdict, "candidate viable but not adopted"),
        ("V782_5_limit_matrix_complete", limits_complete, "six limit/pillar arenas checked"),
        ("V782_6_risk_ledger_complete", risks_complete, "overconstraint risk ledger complete"),
        ("V782_7_high_risks_open", high_risks_open, "high-severity risks remain open"),
        ("V782_8_adoption_decision_complete", adoption_complete, "adoption decision rows complete"),
        ("V782_9_adoption_not_claimed", adoption_not_claimed, "candidate action not adopted"),
        ("V782_10_next_inputs_complete", next_inputs_complete, "next input requirements complete"),
        ("V782_11_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V782_12_claim_artifacts_absent", claim_artifacts_absent, "no adopted-action/zero/local-GR/Newton claim artifact fabricated"),
        ("V782_13_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V782_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V782_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V782_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    limits: list[dict[str, Any]],
    risks: list[dict[str, Any]],
    adoption: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 782 - Y5 R10 Minimal Parent Coupling Owner Consistency Gate

Current result: **the minimal parent coupling owner is a viable candidate, but it is not adopted**. It is coherent enough to keep pursuing because it targets the exact coupling/source-measure leak. It is not strong enough to claim because it has not been mapped to the existing MTS spine, does not by itself derive `MTS -> GR -> Newton`, and could overconstrain the broader galaxy/cosmology/EM programme if adopted blindly.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Consistency Gate

{markdown_table(gates, ["gate_id", "gate", "candidate_effect", "result", "blocker", "adoption_effect", "valid_for_claim"])}

## Limit And Pillar Compatibility Matrix

{markdown_table(limits, ["limit_id", "arena", "candidate_support", "remaining_gap", "compatibility_result", "next_evidence", "valid_for_claim"])}

## Overconstraint Risk Ledger

{markdown_table(risks, ["risk_id", "risk", "impact", "mitigation", "severity", "status", "valid_for_claim"])}

## Adoption Decision

{markdown_table(adoption, ["decision_id", "decision", "reason", "result", "claim_status", "next_target", "valid_for_claim"])}

## Next Input Requirements

{markdown_table(inputs, ["input_id", "required_input", "why_needed", "acceptance_gate", "if_missing", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is the right kind of pressure test. The candidate owner action is not rubbish; it is a plausible route. But it cannot be allowed to become a magic coupling eraser. The next move is to map its `Q`, `e_obs`, `R_phys`, and source/readout objects onto the existing MTS spine. If that map fails, use the empirical residual interface instead.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    gates = consistency_gate_rows(generated_utc)
    limits = limit_matrix_rows(generated_utc)
    risks = risk_rows(generated_utc)
    adoption = adoption_rows(generated_utc)
    inputs = next_input_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, gates, limits, risks, adoption, inputs, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CONSISTENCY_GATE_PATH, gates, ["gate_id", "gate", "candidate_effect", "result", "blocker", "adoption_effect", "valid_for_claim", "generated_utc"])
    write_csv(LIMIT_MATRIX_PATH, limits, ["limit_id", "arena", "candidate_support", "remaining_gap", "compatibility_result", "next_evidence", "valid_for_claim", "generated_utc"])
    write_csv(RISK_LEDGER_PATH, risks, ["risk_id", "risk", "impact", "mitigation", "severity", "status", "valid_for_claim", "generated_utc"])
    write_csv(ADOPTION_DECISION_PATH, adoption, ["decision_id", "decision", "reason", "result", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_INPUTS_PATH, inputs, ["input_id", "required_input", "why_needed", "acceptance_gate", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, gates, limits, risks, adoption, inputs, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"782 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
