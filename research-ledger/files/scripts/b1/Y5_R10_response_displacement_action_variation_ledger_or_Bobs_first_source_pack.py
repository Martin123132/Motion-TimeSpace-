from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "776-Y5-R10-response-displacement-action-variation-ledger-or-Bobs-first-source-pack.md"
NEXT_TARGET = "777-Y5-R10-physical-residual-lock-map-or-Bobs-source-measure-first-pack.md"
STATUS = "Y5_R10_776_response_displacement_variation_ledger_written_formal_double_zero_not_physical_lock_Bobs_first_source_pack_staged_nonclaim"
CLAIM_CEILING = "response_displacement_variation_ledger_and_Bobs_first_source_pack_only_no_owner_certificate_no_Bobs_zero_no_deltaH_zero_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_776_SOURCE_REGISTER.csv"
VARIATION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_776_RESPONSE_DISPLACEMENT_VARIATION_LEDGER.csv"
KGAMMA_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv"
OWNER_VERDICT_PATH = RESIDUALS / "P8_Y5_R10_776_OWNER_VERDICT_GATE.csv"
BOBS_FIRST_PACK_PATH = RESIDUALS / "P8_Y5_R10_776_BOBS_FIRST_SOURCE_PACK.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_776_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_776_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_776_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_776_RESPONSE_DISPLACEMENT_OWNER_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_776_PHYSICAL_RESIDUAL_LOCK_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_776_BOBS_FIRST_SOURCE_NUMERIC_INPUT.csv",
    RESIDUALS / "P8_Y5_R10_776_BOBS_ZERO_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_776_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    VARIATION_LEDGER_PATH,
    KGAMMA_LEDGER_PATH,
    OWNER_VERDICT_PATH,
    BOBS_FIRST_PACK_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "775_doc": {
        "path": POST_CHECKPOINT / "775-Y5-R10-observed-boundary-flux-source-acquisition-or-response-displacement-owner.md",
        "needles": ["RDO775_0_response_displacement_ansatz", "BSA775_5_total_Bobs"],
        "role": "immediate 776 handoff",
    },
    "775_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_775_VALIDATION.csv",
        "needles": ["V775_3_owner_attempt_complete", "pass"],
        "role": "prior validation guard",
    },
    "775_owner": {
        "path": RESIDUALS / "P8_Y5_R10_775_RESPONSE_DISPLACEMENT_OWNER_ATTEMPT.csv",
        "needles": ["RDO775_3_no_source_or_boundary_work", "fail_current_corpus"],
        "role": "owner attempt clauses",
    },
    "775_bobs_ledger": {
        "path": RESIDUALS / "P8_Y5_R10_775_BOBS_SOURCE_ACQUISITION_LEDGER.csv",
        "needles": ["BSA775_2_source_measure_flux", "BSA775_5_total_Bobs"],
        "role": "B_obs source acquisition ledger",
    },
    "775_readiness": {
        "path": RESIDUALS / "P8_Y5_R10_775_BOBS_CLAIM_READINESS_GATE.csv",
        "needles": ["BCR775_0_owner_certificate", "BCR775_4_local_claim"],
        "role": "claim readiness blockers",
    },
    "517_doc": {
        "path": POST_CHECKPOINT / "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
        "needles": ["AV517_2_first_variation_Z", "MR517_3_boundary_terms"],
        "role": "older response-doublet variation and boundary work blocker",
    },
    "757_doc": {
        "path": POST_CHECKPOINT / "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
        "needles": ["physical_lock_not_proved", "real q_loc^nu field/profile or theorem-zero certificate"],
        "role": "formal double-zero does not imply observed residual zero",
    },
    "758_contract": {
        "path": RESIDUALS / "P8_Y5_R10_758_PARENT_ACTION_CONTRACT_ATTEMPT.csv",
        "needles": ["PAC758_1_residual_norm", "PAC758_3_universal_coupling_owner"],
        "role": "full residual-vector parent-action contract",
    },
    "758_lock_gate": {
        "path": RESIDUALS / "P8_Y5_R10_758_FULL_RESIDUAL_VECTOR_LOCK_GATE.csv",
        "needles": ["FLG758_0_q_loc", "FLG758_5_coupling"],
        "role": "physical residual lock gates",
    },
    "759_coupling_audit": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
        "needles": ["COA759_0_single_observed_geometry", "COA759_6_verdict"],
        "role": "coupling owner action audit",
    },
    "774_runner": {
        "path": RESIDUALS / "P8_Y5_R10_774_BOBS_INPUT_RUNNER_SCHEMA.csv",
        "needles": ["BIR774_0_bulk_Euler_flux", "BIR774_5_total_Bobs"],
        "role": "previous B_obs runner schema",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


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


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def variation_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "variation_id": "RAV776_0_action_density",
            "object": "response-displacement action",
            "formula": "S_R = 1/2 int_M sqrt(-g) R^A G_AB(g,U,D) R^B + int_boundary B_R",
            "variation_result": "delta S_R = int sqrt(-g) E_A delta R^A - 1/2 int sqrt(-g) T_R^{mu nu} delta g_{mu nu} + int_boundary Theta_R",
            "derivation_status": "formal_variation_shape_written",
            "claim_effect": "gives a candidate parent form but not current-MTS ownership",
            "missing": "explicit R^A field definitions, G_AB units, U/domain data, and source paths",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "variation_id": "RAV776_1_euler_equation",
            "object": "response Euler equation",
            "formula": "E_A = G_AB R^B + 1/2 R^B (partial_A G_BC) R^C - nabla_mu(partial L_R/partial nabla_mu R^A) - J_A",
            "variation_result": "local silence requires E_A=0 with J_A=0 and no boundary work",
            "derivation_status": "formal_only",
            "claim_effect": "positive operator could force R=0 only after source/boundary/coupling silence is signed",
            "missing": "J_A=0, B_A=0, source current closure, coupling descent, boundary no-flux",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "variation_id": "RAV776_2_formal_double_zero",
            "object": "quadratic gamma response",
            "formula": "gamma_R = 1/2 R^A G_AB R^B; partial_C gamma_R|R=0 = 0 if G_AB finite and no linear J_A R^A term is present",
            "variation_result": "F_1=0 for the auxiliary response variables",
            "derivation_status": "pass_formal_auxiliary_only",
            "claim_effect": "useful double-zero structure retained",
            "missing": "proof that R=0 is equivalent to observed q_loc/Y5/Y6/PPN/boundary/coupling residuals vanishing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "variation_id": "RAV776_3_boundary_variation",
            "object": "boundary and integration-by-parts terms",
            "formula": "Theta_R + delta B_R + domain/projector variations contribute B_obs_boundary and corner/edge pieces",
            "variation_result": "bulk double-zero does not kill finite boundary/source flux",
            "derivation_status": "open_current_corpus",
            "claim_effect": "B_obs boundary pack remains necessary",
            "missing": "fixed-reference/no-flux theorem or sourced boundary/corner flux rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "variation_id": "RAV776_4_source_measure_coupling",
            "object": "source/readout/coupling work",
            "formula": "J_A delta R^A + B_source_measure + delta O_source[e_obs,Psi,R] can feed B_obs_source_measure",
            "variation_result": "coupling/source-measure leak is a first-class obstruction, not a side note",
            "derivation_status": "blocked_by_759_coupling_owner",
            "claim_effect": "B_obs_source_measure_over_MH must be derived zero or sourced",
            "missing": "quotient-invariant matter/source/readout descent or coefficient bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def kgamma_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "kgamma_id": "KGL776_0_volume_piece",
            "metric_response_piece": "volume response of gamma_R",
            "formal_expression": "delta sqrt(-g) gamma_R gives gamma_R g^{mu nu} contribution to T_R^{mu nu}",
            "status": "formal_known",
            "blocks_if_missing": "sign convention mismatch in T_GK=Gamma g-Khat",
            "required_before_claim": "fixed sign/volume convention matching 514/733",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kgamma_id": "KGL776_1_G_metric_dependence",
            "metric_response_piece": "delta_g G_AB(g,U,D)",
            "formal_expression": "K_G^{mu nu} ~ R^A (delta G_AB/delta g_{mu nu}) R^B plus derivative terms",
            "status": "not_computable_without_GAB",
            "blocks_if_missing": "K_hat cannot be compared to K_gamma",
            "required_before_claim": "explicit G_AB and tensor-slot comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kgamma_id": "KGL776_2_derivative_terms",
            "metric_response_piece": "terms from nabla R, connections, Hodge/domain operators",
            "formal_expression": "delta_g(nabla R, star, domain metric) creates derivative/projector stress",
            "status": "open",
            "blocks_if_missing": "hidden Khat_unmatched and P_loc commutator leakage",
            "required_before_claim": "Helmholtz/integrability ledger including derivative and projector terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kgamma_id": "KGL776_3_boundary_reference_terms",
            "metric_response_piece": "delta B_R, reference subtraction, and corner terms",
            "formal_expression": "surface metric response contributes B_obs_boundary_improvement_over_MH unless exact/fixed",
            "status": "open",
            "blocks_if_missing": "observed B_obs zero theorem",
            "required_before_claim": "fixed-reference no-flux theorem or source-backed boundary row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "kgamma_id": "KGL776_4_current_Khat_match",
            "metric_response_piece": "K_hat - K_gamma comparison",
            "formal_expression": "Delta K^{mu nu} := K_hat^{mu nu} - K_gamma^{mu nu}",
            "status": "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH",
            "blocks_if_missing": "reduced GK owner and local-GR route",
            "required_before_claim": "Delta K row zero/theorem or retained residual coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def owner_verdict_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "OVG776_0_formal_variation",
            "gate": "response action variation written",
            "result": "pass_formal",
            "evidence": "RAV776_0 through RAV776_2",
            "why_not_claim": "formal variation does not identify current MTS symbols or physical residual lock",
            "next_requirement": "explicit R^A map and Khat/Kgamma comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OVG776_1_physical_lock",
            "gate": "R^A full-rank locks to observed residual vector",
            "result": "fail_current_corpus",
            "evidence": "757/758 gates keep q_loc,Y5,Y6,PPN,boundary,coupling channels open",
            "why_not_claim": "auxiliary R=0 can be an internal shadow zero",
            "next_requirement": "physical residual lock map or component source rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OVG776_2_source_boundary_silence",
            "gate": "J_A=0 and B_A=0 in compact exterior",
            "result": "fail_current_corpus",
            "evidence": "Y5/Y6/boundary/coupling/source-measure rows remain active",
            "why_not_claim": "positive norm does not force zero when driven by source or boundary work",
            "next_requirement": "B_obs first source pack and coupling descent proof/bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OVG776_3_metric_response_match",
            "gate": "K_hat equals K_gamma",
            "result": "fail_current_corpus",
            "evidence": "KGL776_4 missing explicit gamma/Kgamma match",
            "why_not_claim": "T_GK is not yet a Hilbert stress for current MTS",
            "next_requirement": "metric response tensor-slot ledger",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OVG776_4_verdict",
            "gate": "response-displacement owner certificate",
            "result": "not_promoted",
            "evidence": "formal double-zero yes; physical owner no",
            "why_not_claim": "no owner certificate, no B_obs source rows, no local-GR reentry",
            "next_requirement": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bobs_first_pack_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "BFP776_0_priority_source_measure",
            "target_quantity": "B_obs_source_measure_over_MH",
            "why_first": "coupling/source-measure leakage can mimic measured-GM/orbit/clock/EM readout even if the geometry sector looks clean",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_776_BOBS_SOURCE_MEASURE_FIRST_PACK_CANDIDATE.csv"),
            "required_columns": "system_id;source_channel;coupling_descent_status;C_qmu;flux_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_COUPLING_DESCENT_OR_NUMERIC_SOURCE",
            "claim_gate": "quotient matter/source/readout descent or coefficient bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BFP776_1_boundary_reference",
            "target_quantity": "B_obs_boundary_improvement_over_MH",
            "why_first": "response variation produces boundary/reference pieces even when the bulk quadratic double-zero is formal",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_776_BOBS_BOUNDARY_REFERENCE_FIRST_PACK_CANDIDATE.csv"),
            "required_columns": "system_id;surface_id;boundary_class;B_GK_component;B_ref_component;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_REFERENCE_SOURCE",
            "claim_gate": "fixed-reference theorem or finite-boundary flux source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BFP776_2_bulk_Euler",
            "target_quantity": "B_obs_bulk_Euler_over_MH",
            "why_first": "positive response action cannot silence the bulk unless E_A=0 is source-free",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_776_BOBS_BULK_EULER_FIRST_PACK_CANDIDATE.csv"),
            "required_columns": "system_id;annulus;field_A;E_A;nabla_Phi_A;P_loc_component;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_REDUCED_EULER_SOURCE",
            "claim_gate": "explicit Euler/no-source theorem or numeric compact-exterior profile",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BFP776_3_projector_commutator",
            "target_quantity": "B_obs_projector_commutator_over_MH",
            "why_first": "P_loc/Pi_M can create leakage by product rule after the Ward identity",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_776_BOBS_PROJECTOR_FIRST_PACK_CANDIDATE.csv"),
            "required_columns": "system_id;projector_id;commutator_value;domain_dependence;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_PROJECTOR_DESCENT_SOURCE",
            "claim_gate": "parent projector theorem or finite commutator bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "BFP776_4_total_guard",
            "target_quantity": "B_observed_reduced_flux_over_MH",
            "why_first": "total B_obs cannot use cancellation credit between unknown components",
            "candidate_artifact": str(RESIDUALS / "P8_Y5_R10_776_BOBS_TOTAL_FIRST_PACK_CANDIDATE.csv"),
            "required_columns": "component_id;value;units;source_path;zero_theorem_or_bound;no_cancellation_flag;valid_for_claim",
            "current_status": "MISSING_COMPONENTS",
            "claim_gate": "all component packs valid before total can be valid",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D776_0_formal_double_zero_retained",
            "decision": "retain the quadratic response action as a formal double-zero mechanism",
            "reason": "delta gamma_R is linear in R and vanishes at R=0 if no linear source term is present",
            "claim_status": "formal_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D776_1_owner_not_promoted",
            "decision": "do not accept response-displacement owner for current MTS",
            "reason": "physical lock, source/boundary silence, Khat metric response, and projector/readout descent are missing",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D776_2_first_source_pack_staged",
            "decision": "stage the first B_obs source pack with source-measure/coupling as priority",
            "reason": "coupling/readout leakage is the fastest way for a clean-looking geometry branch to fail Newton/local-GR recovery",
            "claim_status": "source_pack_schema_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D776_3_next_target",
            "decision": "attack physical residual lock map or build B_obs source-measure first pack",
            "reason": "that decides whether the formal R=0 theorem is physical or whether the source-measure residual must be bounded",
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
            "main_result": "quadratic response-displacement variation gives a formal auxiliary double-zero, but not a physical local-GR proof; B_obs first source pack is staged",
            "hard_blocker": "R^A is not yet full-rank locked to observed q_loc/Y5/Y6/PPN/boundary/coupling residuals and source/boundary/coupling work is not zero",
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
    variation: list[dict[str, Any]],
    kgamma: list[dict[str, Any]],
    verdict: list[dict[str, Any]],
    bobs_pack: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_variation_ids = {
        "RAV776_0_action_density",
        "RAV776_1_euler_equation",
        "RAV776_2_formal_double_zero",
        "RAV776_3_boundary_variation",
        "RAV776_4_source_measure_coupling",
    }
    expected_kgamma_ids = {
        "KGL776_0_volume_piece",
        "KGL776_1_G_metric_dependence",
        "KGL776_2_derivative_terms",
        "KGL776_3_boundary_reference_terms",
        "KGL776_4_current_Khat_match",
    }
    expected_pack_ids = {
        "BFP776_0_priority_source_measure",
        "BFP776_1_boundary_reference",
        "BFP776_2_bulk_Euler",
        "BFP776_3_projector_commutator",
        "BFP776_4_total_guard",
    }

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_775_clean = all(validation_clean(number) for number in range(665, 776))
    variation_complete = expected_variation_ids.issubset({row["variation_id"] for row in variation})
    formal_double_zero_recorded = any(row["variation_id"] == "RAV776_2_formal_double_zero" and row["derivation_status"] == "pass_formal_auxiliary_only" for row in variation)
    kgamma_complete = expected_kgamma_ids.issubset({row["kgamma_id"] for row in kgamma})
    owner_not_promoted = any(row["gate_id"] == "OVG776_4_verdict" and row["result"] == "not_promoted" for row in verdict)
    bobs_pack_complete = expected_pack_ids.issubset({row["pack_id"] for row in bobs_pack})
    bobs_pack_missing = all("MISSING" in row["current_status"] for row in bobs_pack)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, variation, kgamma, verdict, bobs_pack, decisions, summary)
    )
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D776_3_next_target" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V776_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V776_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V776_2_prior_665_775_clean", prior_665_775_clean, "665-775 validation rows have no failures"),
        ("V776_3_variation_ledger_complete", variation_complete, "response-displacement variation rows complete"),
        ("V776_4_formal_double_zero_recorded", formal_double_zero_recorded, "formal auxiliary F1=0 row recorded"),
        ("V776_5_Kgamma_ledger_complete", kgamma_complete, "metric-response pieces enumerated"),
        ("V776_6_owner_not_promoted", owner_not_promoted, "response owner remains nonclaim"),
        ("V776_7_Bobs_first_pack_complete", bobs_pack_complete, "B_obs first source pack rows complete"),
        ("V776_8_Bobs_pack_missing_markers", bobs_pack_missing, "B_obs source pack rows remain MISSING_*"),
        ("V776_9_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V776_10_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V776_11_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no owner/Bobs/local-GR claim artifacts fabricated"),
        ("V776_12_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V776_13_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V776_14_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    kgamma: list[dict[str, Any]],
    verdict: list[dict[str, Any]],
    bobs_pack: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 776 - Y5 R10 Response Displacement Action Variation Ledger Or Bobs First Source Pack

Current result: **the response-displacement action gives a real formal double-zero, but not a physical local-GR proof yet**. For a quadratic response action, `partial_A gamma_R|R=0=0` if there is no linear source term. That is useful. But the current corpus still does not prove `R^A` is full-rank locked to observed `q_loc/Y5/Y6/PPN/boundary/coupling` residuals, nor that source/boundary/coupling work vanishes. So the owner route stays nonclaim and the first `B_obs` source pack is staged.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Response-Displacement Variation Ledger

{markdown_table(variation, ["variation_id", "object", "formula", "variation_result", "derivation_status", "claim_effect", "missing", "valid_for_claim"])}

## Kgamma Metric-Response Ledger

{markdown_table(kgamma, ["kgamma_id", "metric_response_piece", "formal_expression", "status", "blocks_if_missing", "required_before_claim", "valid_for_claim"])}

## Owner Verdict Gate

{markdown_table(verdict, ["gate_id", "gate", "result", "evidence", "why_not_claim", "next_requirement", "valid_for_claim"])}

## Bobs First Source Pack

{markdown_table(bobs_pack, ["pack_id", "target_quantity", "why_first", "candidate_artifact", "required_columns", "current_status", "claim_gate", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a genuine derivation win but not a victory lap. We now have a clean reason the response route is attractive: it can kill first variations formally. We also have the exact reason it is not enough: the formal zero must be glued to the physical residual vector and protected from source, boundary, projector, and coupling work. Next we either build that physical lock map or start the `B_obs_source_measure` pack.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    variation = variation_rows(generated_utc)
    kgamma = kgamma_rows(generated_utc)
    verdict = owner_verdict_rows(generated_utc)
    bobs_pack = bobs_first_pack_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, variation, kgamma, verdict, bobs_pack, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(VARIATION_LEDGER_PATH, variation, ["variation_id", "object", "formula", "variation_result", "derivation_status", "claim_effect", "missing", "valid_for_claim", "generated_utc"])
    write_csv(KGAMMA_LEDGER_PATH, kgamma, ["kgamma_id", "metric_response_piece", "formal_expression", "status", "blocks_if_missing", "required_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(OWNER_VERDICT_PATH, verdict, ["gate_id", "gate", "result", "evidence", "why_not_claim", "next_requirement", "valid_for_claim", "generated_utc"])
    write_csv(BOBS_FIRST_PACK_PATH, bobs_pack, ["pack_id", "target_quantity", "why_first", "candidate_artifact", "required_columns", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, variation, kgamma, verdict, bobs_pack, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"776 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
