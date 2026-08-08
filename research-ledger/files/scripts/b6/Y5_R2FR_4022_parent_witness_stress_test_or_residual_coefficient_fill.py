from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4022"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4022-Y5-R2FR-parent-witness-stress-test-or-residual-coefficient-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4022_SOURCE_REGISTER.csv",
    "operator_test": SRC / "P8_Y5_R2FR_4022_OPERATOR_CLASS_STRESS_TEST.csv",
    "admission": SRC / "P8_Y5_R2FR_4022_WITNESS_ADMISSION_MATRIX.csv",
    "survivors": SRC / "P8_Y5_R2FR_4022_SURVIVOR_PPN_ROUTE.csv",
    "priority": SRC / "P8_Y5_R2FR_4022_FIRST_RESIDUAL_PRIORITY.csv",
    "cases": SRC / "P8_Y5_R2FR_4022_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4022_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4022_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4022_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4022_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4022_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4022_VALIDATION.csv",
}

NEXT_DOC = "4023-Y5-R2FR-Gamma-Khat-variational-stress-action-or-q-loc-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4023_Gamma_Khat_variational_stress_action_or_q_loc_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4022_00_handoff", SRC / "P8_Y5_R2FR_4021_NEXT_TARGET.csv", "NEXT4021_0", "4021 handoff"),
        ("SRC4022_01_witness", SRC / "P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv", "WIT4021_2_no_extra_operators", "4021 no-extra witness"),
        ("SRC4022_02_lemma_q_loc", SRC / "P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv", "LEM4021_5_q_loc_vertical_kernel", "q_loc kernel lemma"),
        ("SRC4022_03_stress", SRC / "P8_Y5_R2FR_4021_WITNESS_STRESS_TEST_ROWS.csv", "STR4021_0_motion_time_space_terms", "4021 stress-test request"),
        ("SRC4022_04_R11_audit", SRC / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv", "R2_fR_scalar_mode", "R11 operator audit"),
        ("SRC4022_05_R11_mapping", SRC / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv", "R2_fR_scalar_mode", "double-zero R11 mapping"),
        ("SRC4022_06_R11_vector", SRC / "R11_nonEH_operator_vector_executable.csv", "R11_nonEH_operator_vector_executable", "executable R11 vector"),
        ("SRC4022_07_GK_contract", SRC / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv", "GK513_0_action_existence", "Gamma/Khat q_loc contract"),
        ("SRC4022_08_GK_decision", SRC / "P8_GAMMA_KHAT_QLOC_DECISION.csv", "D513_0", "Gamma/Khat decision"),
        ("SRC4022_09_domain_decision", SRC / "P8_DOMAIN_SELECTOR_PARENT_ACTION_DECISION.csv", "D0_parent_clause", "domain selector decision"),
        ("SRC4022_10_source_norm", SRC / "P8_R11_SOURCE_NORMALIZATION_DECISION.csv", "D0_minimum_fill", "source normalization R11 decision"),
        ("SRC4022_11_EM_once", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_1_Maxwell_Hilbert_stress", "EM/Poynting once-only"),
        ("SRC4022_12_Hodge", SRC / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv", "OHN4014_0_observed_Hodge_lock", "observed Hodge lock"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def operator_test_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "OP4022_0_boundary_topological",
            "operator_family": "boundary_topological_terms",
            "witness_gate": "admitted only as exact/topological with boundary-silent flux",
            "current_evidence": "old R11 audit retains missing coefficient/no-hair proof",
            "stress_result": "conditional_admit_else_score",
            "surviving_residual": "boundary_domain + beta/gamma/alpha3/xi maps",
            "route": "prove boundary no-flux/topological identity or fill R11 boundary coefficient",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_1_R2_fR",
            "operator_family": "R2_fR_scalar_mode",
            "witness_gate": "excluded unless auxiliary double-zero, vertical-only, or higher-than-2PN",
            "current_evidence": "retained with MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "delta_gamma_R11 + delta_beta_R11 + alpha(lambda)",
            "route": "derive double-zero curvature scalar coefficient or fill scalar mass/coupling map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_2_Ricci_Weyl",
            "operator_family": "Ricci_Weyl_squared",
            "witness_gate": "admitted only as topological Gauss-Bonnet/exact combination or double-zero",
            "current_evidence": "retained with missing coefficient/map",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "delta_gamma_R11 + xi + wave/slip sector",
            "route": "prove topological combination or compute weak-field projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_3_scalar_tensor",
            "operator_family": "scalar_tensor_class_metric",
            "witness_gate": "excluded unless scalar is locally fixed with zero derivatives or coupling is double-zero",
            "current_evidence": "retained in R11 vector with clock/Gdot/R10/PPN maps missing",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "Gdot/G + gamma/beta + clocks + alpha(lambda)",
            "route": "prove local scalar fixed point or fill scalar-tensor coefficient/bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_4_vector_preferred_frame",
            "operator_family": "vector_preferred_frame",
            "witness_gate": "excluded unless no-vector theorem or double-zero vector coefficient",
            "current_evidence": "domain/vector rows retained unfilled",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "alpha1 + alpha2 + alpha3 + xi",
            "route": "prove no local preferred selector or fill W_domain products",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_5_torsion_nonmetricity",
            "operator_family": "torsion_nonmetricity",
            "witness_gate": "excluded unless Levi-Civita observed branch or torsion/nonmetricity double-zero",
            "current_evidence": "retained with no coefficient/map",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "WEP + clock + lightcone + R11 ledger",
            "route": "prove observed connection is Levi-Civita through local branch or fill connection residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_6_bulk_X",
            "operator_family": "bulk_X_force_law",
            "witness_gate": "excluded unless bulk charge is vertical/source-silent or double-zero",
            "current_evidence": "retained with source charge and finite-range maps missing",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "R10 alpha(lambda) + WEP/source charge + gamma/beta",
            "route": "derive no source charge or fill finite-range bound coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_7_nonlocal_memory",
            "operator_family": "nonlocal_memory_kernel",
            "witness_gate": "excluded locally unless compact-local kernel is silent or norm is double-zero",
            "current_evidence": "retained with kernel norm/map missing",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "alpha3 + Gdot/G + R10 alpha(lambda)",
            "route": "prove local memory kernel vanishes in compact PPN branch or fill kernel norm",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_8_source_normalization",
            "operator_family": "source_normalization_operator",
            "witness_gate": "excluded unless same Hilbert source current and no extra mu/source prefactor",
            "current_evidence": "minimum fill written; zero claim-valid rows",
            "stress_result": "survivor_requires_score_or_excise",
            "surviving_residual": "delta_beta_source + alpha1/alpha2/alpha3/xi",
            "route": "derive same-source normalization or fill coefficient products",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_9_projector_domain",
            "operator_family": "projector_domain_stress",
            "witness_gate": "admitted only if metric-independent topological P_D with no bulk stress",
            "current_evidence": "conditional zero not parent-owned",
            "stress_result": "conditional_admit_else_score",
            "surviving_residual": "alpha1 + alpha2 + alpha3 + xi + R11",
            "route": "prove parent-owned metric-independent projector or score projector stress",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_10_Gamma_Khat_q_loc",
            "operator_family": "Gamma_eff/Khat/q_loc",
            "witness_gate": "admitted only if variational Hilbert stress, on-shell Euler closure, double-zero, projector-owned, and boundary-silent",
            "current_evidence": "513 decision says central residual reduced to variational stress problem; gates not passed",
            "stress_result": "highest_priority_survivor",
            "surviving_residual": "delta_beta_q_loc + alpha(lambda) + local force/source-exchange",
            "route": "construct S_GK or demote q_loc to residual bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "operator_id": "OP4022_11_EM_Hodge_Poynting",
            "operator_family": "EM_Hodge_Poynting_source",
            "witness_gate": "admitted if observed Hodge and same Hilbert variation once",
            "current_evidence": "4013/4014 provide conditional owner theorems",
            "stress_result": "admitted_under_witness_pending_corpus_adoption",
            "surviving_residual": "epsilon_EM_once + Delta_Hodge_EM if witness rejected",
            "route": "carry as witness-compatible; stress only if a constitutive/Hodge mismatch appears",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def admission_rows(operator_rows: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in operator_rows:
        result = row["stress_result"]
        if result == "admitted_under_witness_pending_corpus_adoption":
            admission = "admitted_by_WIT4021_if_corpus_adopts"
        elif result == "conditional_admit_else_score":
            admission = "conditional_admit_requires_extra_clause"
        elif result == "highest_priority_survivor":
            admission = "not_admitted_currently_primary_target"
        else:
            admission = "not_admitted_currently_score_or_excise"
        rows.append(
            {
                "admission_id": row["operator_id"].replace("OP", "ADM"),
                "operator_family": row["operator_family"],
                "witness_admission": admission,
                "why": row["witness_gate"],
                "current_status": row["current_evidence"],
                "resulting_route": row["route"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def survivor_rows(operator_rows: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in operator_rows:
        if row["stress_result"] == "admitted_under_witness_pending_corpus_adoption":
            continue
        priority = {
            "highest_priority_survivor": 1,
            "survivor_requires_score_or_excise": 2,
            "conditional_admit_else_score": 3,
        }.get(str(row["stress_result"]), 9)
        rows.append(
            {
                "route_id": row["operator_id"].replace("OP", "SURV"),
                "operator_family": row["operator_family"],
                "priority": priority,
                "surviving_residual": row["surviving_residual"],
                "coefficient_needed": coefficient_needed(str(row["operator_family"])),
                "target_score_rows": target_score_rows(str(row["operator_family"])),
                "next_derivation_or_bound": row["route"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coefficient_needed(operator_family: str) -> str:
    return {
        "Gamma_eff/Khat/q_loc": "T_GK action/integrability/double-zero witness or q_loc amplitude profile",
        "R2_fR_scalar_mode": "c_R2_or_c_fR plus scalar mass/coupling map",
        "Ricci_Weyl_squared": "c_Ricci_or_c_Weyl weak-field projection",
        "scalar_tensor_class_metric": "F_phi_C derivatives or double-zero coupling",
        "vector_preferred_frame": "W_domain_alpha_i * epsilon_domain_vector/flux/aniso products",
        "torsion_nonmetricity": "c_T/c_Q and connection-response map",
        "bulk_X_force_law": "q_X, m_X/lambda_X, source charge normalization",
        "nonlocal_memory_kernel": "local kernel norm and compact-branch support bound",
        "source_normalization_operator": "c_domain_source_normalization_operator or same-source theorem",
        "projector_domain_stress": "projector metric-variation stress coefficient or topological proof",
        "boundary_topological_terms": "boundary flux/no-hair coefficient or exact/topological proof",
    }.get(operator_family, "operator coefficient or theorem-zero witness")


def target_score_rows(operator_family: str) -> str:
    return {
        "Gamma_eff/Khat/q_loc": "WPS4021_3_delta_beta_q_loc; R10 alpha(lambda)",
        "R2_fR_scalar_mode": "WPS4021_0_delta_gamma_R11; WPS4021_2_delta_beta_R11; R10 alpha(lambda)",
        "Ricci_Weyl_squared": "WPS4021_0_delta_gamma_R11; WPS4021_2_delta_beta_R11; WPS4021_4_preferred_frame",
        "scalar_tensor_class_metric": "WPS4021_0_delta_gamma_R11; WPS4021_1_delta_beta_source; WPS4021_6_Gdot; R10/clocks",
        "vector_preferred_frame": "WPS4021_4_preferred_frame",
        "torsion_nonmetricity": "WEP/clocks/lightcone/R11 ledger",
        "bulk_X_force_law": "R10 alpha(lambda); WEP/source charge; WPS4021_0/2",
        "nonlocal_memory_kernel": "WPS4021_4_preferred_frame; WPS4021_6_Gdot; R10 alpha(lambda)",
        "source_normalization_operator": "WPS4021_1_delta_beta_source; WPS4021_4_preferred_frame",
        "projector_domain_stress": "WPS4021_4_preferred_frame; R11 ledger",
        "boundary_topological_terms": "WPS4021_0/2; boundary_domain; alpha3/xi",
    }.get(operator_family, "PPN/R10 residual rows")


def priority_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "priority_id": "PRI4022_0_first_target",
            "rank": 1,
            "target": "Gamma_eff/Khat/q_loc",
            "reason": "it is the only survivor already reduced to a crisp variational-stress contract; closing it directly attacks delta_beta_q_loc and local force exchange",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority_id": "PRI4022_1_second_target",
            "rank": 2,
            "target": "R11 curvature/source-normalization classes",
            "reason": "if q_loc closes, remaining local-GR pressure is non-EH operator coefficients and source prefactors",
            "next_doc": "after 4023: R11 curvature/source-normalization coefficient theorem-or-fill",
            "next_script": "deferred",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority_id": "PRI4022_2_parallel_guard",
            "rank": 3,
            "target": "domain/projector and nonlocal memory",
            "reason": "these are not allowed through witness unless topological/vertical/double-zero; keep them out of local 2PN or score them",
            "next_doc": "deferred unless 4023 closes",
            "next_script": "deferred",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4022_0_all_admitted",
            "assumption": "every operator class is admitted by WIT4021 or excluded from local 2PN",
            "expected_result": "4021 witness survives corpus stress test conditionally",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4022_1_current_evidence",
            "assumption": "old R11/q_loc/domain rows remain retained or conditional, not claim-valid",
            "expected_result": "witness is not yet corpus-adopted; q_loc/Gamma-Khat is first target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4022_2_q_loc_action_found",
            "assumption": "S_GK exists and satisfies integrability, Euler closure, double-zero, projector ownership, boundary silence",
            "expected_result": "delta_beta_q_loc theorem-zero under witness",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4022_3_q_loc_action_fails",
            "assumption": "Gamma_eff/Khat cannot be variational or double-zero",
            "expected_result": "q_loc becomes a residual-bound branch, no local-GR promotion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4022_0_all_admitted":
            verdict = "HYPOTHETICAL_WITNESS_SURVIVES"
            next_action = "would then adopt witness and promote conditional local-GR theorem"
        elif case_id == "CASE4022_1_current_evidence":
            verdict = "CURRENT_STRESS_TEST_FAILS_FULL_ADOPTION"
            next_action = "target Gamma_eff/Khat/q_loc variational stress first"
        elif case_id == "CASE4022_2_q_loc_action_found":
            verdict = "QLOC_ZERO_ROUTE_AVAILABLE_IF_CONSTRUCTED"
            next_action = "then return to R11 curvature/source-normalization survivors"
        else:
            verdict = "QLOC_BOUND_BRANCH_REQUIRED"
            next_action = "derive/source q_loc amplitude profile and local bounds"
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4022",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4022_0_stress_test",
            "decision": "stress-tested WIT4021 against actual retained operator families",
            "rationale": "the witness is only useful if every MTS local operator either enters through its gates or gets scored",
            "effect": "operator families are now admitted, conditionally admitted, or survivor-routed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4022_1_no_blanket_adoption",
            "decision": "do not adopt WIT4021 wholesale yet",
            "rationale": "R11/q_loc/domain/source-normalization evidence still contains retained and missing coefficient rows",
            "effect": "claim gates remain false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4022_2_first_target",
            "decision": "prioritize Gamma_eff/Khat/q_loc variational-stress action",
            "rationale": "it is the sharpest single survivor and directly hits the local PPN branch",
            "effect": "4023 targets S_GK construction or q_loc bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4022_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "constructing S_GK is the highest-leverage derivation-first attempt after the witness stress test",
            "effect": "either q_loc becomes theorem-zero or the local branch gets a concrete residual-bound route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4022_0_local_GR",
            "claim": "MTS locally reduces to GR/PPN",
            "allowed": False,
            "reason": "witness stress test leaves q_loc/R11/domain/source-normalization survivors",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4022_1_witness_adopted",
            "claim": "WIT4021 is adopted by the current corpus",
            "allowed": False,
            "reason": "operator-class evidence is not yet admitted/excluded/scored",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4022_2_q_loc_zero",
            "claim": "q_loc/Gamma-Khat is theorem-zero",
            "allowed": False,
            "reason": "variational stress action/integrability/double-zero/projector/boundary gates remain unproved",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4022_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "construct a variational Hilbert-stress action S_GK for Gamma_eff/Khat/q_loc satisfying integrability, Euler closure, double-zero, projector ownership and boundary silence; if it fails, demote q_loc to a sourced residual-bound branch",
            "success_condition": "q_loc is either theorem-zero under WIT4021 or converted into explicit amplitude/profile/bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "WIT4021 stress-tested against retained operator classes; Gamma/Khat/q_loc selected as first survivor target",
            "current_best_route": "construct S_GK or bound q_loc",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], operator_rows: list[dict[str, Any]], priority: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4022_1_current_evidence")
    survivor_count = sum(1 for row in operator_rows if row["stress_result"] in {"survivor_requires_score_or_excise", "highest_priority_survivor"})
    conditional_count = sum(1 for row in operator_rows if row["stress_result"] == "conditional_admit_else_score")
    admitted_count = sum(1 for row in operator_rows if row["stress_result"] == "admitted_under_witness_pending_corpus_adoption")
    first = priority[0]
    DOC_PATH.write_text(
        f"""# 4022 - Parent Witness Stress Test Or Residual Coefficient Fill

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

4021 gave a clean local parent-action witness. 4022 stress-tests it against the retained MTS operator families instead of pretending the witness is automatically adopted.

Operator-class outcome:

- Admitted under witness pending corpus adoption: `{admitted_count}`.
- Conditional-admit else score: `{conditional_count}`.
- Survivor requiring score or excision: `{survivor_count}`.
- Source needles found: `{source_hits}/{source_total}`.

Current evaluator result: `{current["verdict"]}`.

## Main Finding

The witness is strong, but the current corpus cannot adopt it wholesale yet. The retained pressure families are:

- `Gamma_eff/Khat/q_loc`;
- R11 curvature operators such as `R2/f(R)` and `Ricci/Weyl^2`;
- scalar/vector/source-normalization/domain projector rows;
- nonlocal memory and bulk force-law rows.

Only the EM/Hodge/Poynting source channel is cleanly compatible with WIT4021, and even that remains conditional on corpus adoption.

## First Target

Rank 1 target: `{first["target"]}`.

Reason: `{first["reason"]}`.

Next action: construct a variational Hilbert-stress action `S_GK` for `Gamma_eff/Khat/q_loc`, or demote q_loc to a residual-bound branch.

## Why This Is Progress

This turns the broad local-GR problem into a finite admission matrix:

`admitted by witness` / `conditional extra clause` / `surviving residual coefficient`.

The next step is not more circling. It is one concrete derivation attempt: does `Gamma_eff/Khat/q_loc` come from a real diffeomorphism-invariant stress action with double-zero local fixed point?

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4022 - Witness Stress Test Against Operator Classes"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: WIT4021 was stress-tested against retained local operator classes.
- Clean compatibility: EM/Hodge/Poynting is admitted under the witness pending corpus adoption.
- Conditional compatibility: boundary/topological and projector/domain terms need no-flux/topological/metric-independent ownership.
- Survivors: `R2/f(R)`, `Ricci/Weyl^2`, scalar-tensor, vector preferred-frame, torsion/nonmetricity, bulk force, nonlocal memory, source-normalization, and `Gamma_eff/Khat/q_loc`.
- First target: `Gamma_eff/Khat/q_loc`, because 513 already reduces it to a variational Hilbert-stress problem.
- No claim: WIT4021 is not adopted wholesale; local GR remains nonclaim.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4022 - Witness Stress Test Against Operator Classes" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    admission: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4022_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4022_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    required_ops = [
        "OP4022_0_boundary_topological",
        "OP4022_1_R2_fR",
        "OP4022_2_Ricci_Weyl",
        "OP4022_3_scalar_tensor",
        "OP4022_4_vector_preferred_frame",
        "OP4022_5_torsion_nonmetricity",
        "OP4022_6_bulk_X",
        "OP4022_7_nonlocal_memory",
        "OP4022_8_source_normalization",
        "OP4022_9_projector_domain",
        "OP4022_10_Gamma_Khat_q_loc",
        "OP4022_11_EM_Hodge_Poynting",
    ]
    for idx, op_id in enumerate(required_ops, start=2):
        add(f"VAL4022_{idx:02d}_operator", any(row["operator_id"] == op_id for row in operator_rows), f"{op_id} present")
    add("VAL4022_14_admission_matrix", len(admission) == len(operator_rows), "every operator has admission row")
    add("VAL4022_15_survivor_routes", any(row["operator_family"] == "Gamma_eff/Khat/q_loc" for row in survivors), "q_loc survivor routed")
    add("VAL4022_16_priority_q_loc", priority[0]["target"] == "Gamma_eff/Khat/q_loc", "q_loc selected first")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4022_17_current_case", result_lookup["CASE4022_1_current_evidence"]["verdict"] == "CURRENT_STRESS_TEST_FAILS_FULL_ADOPTION", "current evidence blocks full adoption")
    add("VAL4022_18_q_loc_case_found", result_lookup["CASE4022_2_q_loc_action_found"]["verdict"] == "QLOC_ZERO_ROUTE_AVAILABLE_IF_CONSTRUCTED", "q_loc action-found case defined")
    add("VAL4022_19_q_loc_case_fail", result_lookup["CASE4022_3_q_loc_action_fails"]["verdict"] == "QLOC_BOUND_BRANCH_REQUIRED", "q_loc failure case routes to bound")
    add("VAL4022_20_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4022_21_decision_first_target", any(row["decision_id"] == "DEC4022_2_first_target" and "Gamma_eff" in row["decision"] for row in decisions), "first target decision recorded")
    add("VAL4022_22_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        operator_rows,
        admission,
        survivors,
        priority,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4022_23_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4022_24_doc_exists", DOC_PATH.exists() and "finite admission matrix" in read_text(DOC_PATH), "document written with admission-matrix verdict")
    add("VAL4022_25_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4022_26_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4022_27_compile", compile_ok, "script compiles")
    add("VAL4022_28_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4022_29_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4022_30_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4022_31_em_admitted_only_conditional", any(row["operator_family"] == "EM_Hodge_Poynting_source" and row["stress_result"] == "admitted_under_witness_pending_corpus_adoption" for row in operator_rows), "EM channel compatibility recorded")
    add("VAL4022_32_no_wholesale_adoption", any(row["claim_id"] == "CLAIM4022_1_witness_adopted" and str(row["allowed"]).lower() == "false" for row in claims), "witness adoption overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    operators = operator_test_rows(timestamp)
    admission = admission_rows(operators, timestamp)
    survivors = survivor_rows(operators, timestamp)
    priority = priority_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["operator_test"], operators)
    write_csv(OUTPUTS["admission"], admission)
    write_csv(OUTPUTS["survivors"], survivors)
    write_csv(OUTPUTS["priority"], priority)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, operators, priority, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, operators, admission, survivors, priority, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4022 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
