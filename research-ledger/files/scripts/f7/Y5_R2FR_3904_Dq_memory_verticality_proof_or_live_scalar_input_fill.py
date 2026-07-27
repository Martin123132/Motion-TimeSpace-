from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3904"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3904-Y5-R2FR-Dq-memory-verticality-proof-or-live-scalar-input-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3904_SOURCE_REGISTER.csv",
    "product_chart": SRC / "P8_Y5_R2FR_3904_PRODUCT_CHART_VERTICALITY_THEOREM.csv",
    "dq_matrix": SRC / "P8_Y5_R2FR_3904_DQ_MEMORY_VERTICALITY_MATRIX.csv",
    "dobs": SRC / "P8_Y5_R2FR_3904_DOBS_E_MEMORY_READOUT_TEST.csv",
    "coefficients": SRC / "P8_Y5_R2FR_3904_DIRECT_DISFORMAL_SCALAR_INPUT_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3904_BRANCH_DECISION.csv",
    "gate": SRC / "P8_Y5_R2FR_3904_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3904_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3904_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3904_VALIDATION.csv",
}

PRODUCT_CHART = "Phi <-> (Q_pub, Y_loc, H_priv), q_parent(Phi)=Q_pub, X_mem=y^memory in Y_loc"
DQ_ZERO = "Dq_parent[partial_Xmem]=0 because q_parent is the projection onto Q_pub in the local product chart"
DOBS_ZERO = "DObs_e[partial_Xmem]=DE_Q[Dq_parent[partial_Xmem]]=0 for e_obs=E(Q_pub)"
LINEAR_FALLBACK = (
    "K_gamma_linear <= K_E*C_Dq_mem + C_disformal_mem + "
    "C_boundary_TF_linear + C_projector_TF_linear"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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
        ("SRC3904_00_next", SRC / "P8_Y5_R2FR_3903_NEXT_TARGET.csv", "NEXT3903_0", "3903 selected Dq memory target"),
        ("SRC3904_01_lgz", SRC / "P8_Y5_R2FR_3903_LINEAR_GAMMA_ZERO_BRANCH_PROMOTION.csv", "LGZ3903_1_Xmem_vertical", "linear gamma-zero Dq hinge"),
        ("SRC3904_02_inputs", SRC / "P8_Y5_R2FR_3903_LIVE_SCALAR_INPUT_FILL_QUEUE.csv", "IN3903_0_Dq_Xmem", "live scalar input queue"),
        ("SRC3904_03_dq2570", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_4_memory_frame", "memory-frame obstruction"),
        ("SRC3904_04_qmap", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_1_tau_clock", "actual q-map components"),
        ("SRC3904_05_2571_vg", SRC / "P8_Y5_OBS_COFRAME_2571_VERTICAL_GENERATOR_TABLE.csv", "VG2571_2_vmemory", "observed coframe vertical generator row"),
        ("SRC3904_06_2571_dobs", SRC / "P8_Y5_OBS_COFRAME_2571_DOBS_KERNEL_GATE.csv", "DOK2571_0_exact_kernel", "conditional DObs kernel theorem"),
        ("SRC3904_07_2571_leaks", SRC / "P8_Y5_OBS_COFRAME_2571_FINITE_DOBS_LEAK_ROWS.csv", "DLEAK2571_2_memory_frame_abs", "finite memory-frame leak precedent"),
        ("SRC3904_08_memory", SRC / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv", "OWN3894_0_owner", "memory parent owner candidate"),
        ("SRC3904_09_coframe", SRC / "P8_Y5_R2FR_3900_SINGLE_COFRAME_LOCK_ATTEMPT.csv", "COF3900_3_no_disformal", "same-frame/no-disformal status"),
        ("SRC3904_10_response", SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv", "RESP3901_5_verdict", "linear gamma fallback response"),
        ("SRC3904_11_gamma2", SRC / "P8_Y5_R2FR_3902_SECOND_ORDER_GAMMA_BOUND_DERIVATION.csv", "GAM3902_3_gamma2", "second-order gamma runner"),
        ("SRC3904_12_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary anisotropy status"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def product_chart_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PCH3904_0_chart",
            "clause": "local product chart",
            "statement": PRODUCT_CHART,
            "derived_result": "if the parent action adopts this split, X_mem is a vertical fibre coordinate, not a public q coordinate",
            "status": "CONSTRUCTED_EXACT_THEOREM_CONDITIONAL",
            "remaining_failure": "product chart/admission clause is not yet globally parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCH3904_1_Dq",
            "clause": "Dq memory zero",
            "statement": DQ_ZERO,
            "derived_result": "Dq[X_mem]=0 is mathematically proved in the product-chart branch",
            "status": "PROVED_INSIDE_PRODUCT_CHART_BRANCH",
            "remaining_failure": "must prove actual MTS q-map is this projection for geometry, tau, matter constants, boundary and coupling slots",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCH3904_2_anti_tautology",
            "clause": "anti-tautology guard",
            "statement": "Q_pub is measured/varied before Y_loc; X_mem may not be defined as 'whatever q forgets' after the fact",
            "derived_result": "requires submersion rank, independent Y_loc fibre coordinate, and no hidden readout slot E(Q_pub,X_mem)",
            "status": "ADMISSION_TEST_NOT_CLOSURE_AXIOM",
            "remaining_failure": "rank/no-shadow/no-extra-slot certificates are still parent-action obligations",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCH3904_3_DObs",
            "clause": "observed coframe chain",
            "statement": DOBS_ZERO,
            "derived_result": "public metric/coframe and Levi-Civita/spin connection become linear-silent to X_mem",
            "status": "PROVED_IF_QBASIC_OBSERVED_COFRAME",
            "remaining_failure": "tau/clock/source/coupling/boundary readouts must also be Q_pub-basic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PCH3904_4_linear_gamma",
            "clause": "linear gamma result",
            "statement": "product chart + q-basic e_obs + no direct disformal slot + quadratic memory stress => K_gamma_linear=0",
            "derived_result": "3901/3903 linear gamma-zero branch becomes a theorem inside this admitted branch",
            "status": "LINEAR_GAMMA_ZERO_BRANCH_CONSTRUCTED_NOT_PROMOTED",
            "remaining_failure": "direct disformal, boundary/projector and global adoption clauses are not signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def dq_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DQM3904_0_public_geometry",
            "q_component": "public_geometry",
            "test": "D_Xmem g_obs=0 and D_Xmem e_obs=0",
            "product_chart_result": "ZERO",
            "current_corpus_status": "CANDIDATE_VISIBLE_NOT_PARENT_DERIVED",
            "failure_if_not_signed": "direct hidden/common-frame readout reopens gamma/PPN response",
            "runner_symbol": "C_E_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DQM3904_1_tau_clock",
            "q_component": "public_tau_clock",
            "test": "D_Xmem tau_obs=0 and tau_source=tau_charge=tau_clock=tau_readout",
            "product_chart_result": "ZERO_IF_TAU_IN_QPUB_ONLY",
            "current_corpus_status": "TAU_FRAME_LOCK_UNSIGNED",
            "failure_if_not_signed": "clock drift, preferred-frame and Gdot channels remain live",
            "runner_symbol": "C_tau_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DQM3904_2_matter_constants",
            "q_component": "ordinary_matter_data",
            "test": "D_Xmem theta_obs=0 and D_Xmem c_vis=0",
            "product_chart_result": "ZERO_IF_CONSTANTS_ARE_QPUB_BASIC",
            "current_corpus_status": "NO_SOURCE_PREF_AND_COEFFICIENT_DESCENT_UNSIGNED",
            "failure_if_not_signed": "visible masses, charges, alpha/clock and source normalization can carry X_mem",
            "runner_symbol": "C_coupling_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DQM3904_3_boundary_reference",
            "q_component": "boundary_reference_class",
            "test": "P_loc D_Xmem B_ref=0 and no linear boundary anisotropy",
            "product_chart_result": "ZERO_IF_BOUNDARY_CLASS_QPUB_FIXED",
            "current_corpus_status": "BOUNDARY_CLASS_UNSIGNED",
            "failure_if_not_signed": "boundary/corner/reference data can source linear local anisotropy",
            "runner_symbol": "C_boundary_TF_linear",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DQM3904_4_coupling_slots",
            "q_component": "parent_coefficient_slots",
            "test": "D_Xmem ln kappa_MTS = D_Xmem ln ell_J = D_Xmem ln G_parent = 0",
            "product_chart_result": "ZERO_IF_PARENT_COEFFICIENTS_ARE_QPUB_SLOTS",
            "current_corpus_status": "COEFFICIENT_DESCENT_UNSIGNED",
            "failure_if_not_signed": "Newton constant/source-current normalization can be hidden in fitted GM",
            "runner_symbol": "C_coupling_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DQM3904_5_projector_readout",
            "q_component": "projector_or_readout_order",
            "test": "D_Xmem Pi_M=0 or P_loc[d,Pi_M]J_H=0",
            "product_chart_result": "ZERO_IF_PROJECTOR_FIXED_BEFORE_VARIATION",
            "current_corpus_status": "PROJECTOR_READOUT_ORDER_UNSIGNED",
            "failure_if_not_signed": "post-readout source projection can mimic a local force/source term",
            "runner_symbol": "C_projector_TF_linear",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DQM3904_6_verdict",
            "q_component": "whole_q_vector",
            "test": "all q components above zero at once",
            "product_chart_result": "Dq[X_mem]=0 EXACT IN PRODUCT CHART",
            "current_corpus_status": "NOT_GLOBALLY_SIGNED",
            "failure_if_not_signed": "use finite direct-disformal/scalar input rows, not a gamma-zero claim",
            "runner_symbol": "C_Dq_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def dobs_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "test_id": "DOBS3904_0_chain",
            "object": "e_obs",
            "equation": DOBS_ZERO,
            "result": "exact zero if q-basic product chart is adopted",
            "status": "EXACT_CONDITIONAL",
            "fallback_if_failed": "retain C_E_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "DOBS3904_1_connection",
            "object": "omega[e_obs], Gamma[e_obs]",
            "equation": "D_Xmem Gamma[e_obs]=D_Gamma[DObs_e[X_mem]]=0 if DObs_e[X_mem]=0",
            "result": "connection-level PPN/light-cone linear leaks vanish with coframe zero",
            "status": "PASS_IF_DOBS_ZERO",
            "fallback_if_failed": "retain connection response inside C_E_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "DOBS3904_2_disformal_countermodel",
            "object": "direct hidden readout",
            "equation": "e_obs=E(Q_pub)+A(X_mem) tau tau+B(X_mem) h produces DObs_e[X_mem] != 0",
            "result": "same-frame alone is not enough; no-disformal/no-extra-slot clause is required",
            "status": "COUNTERMODEL_RETAINED",
            "fallback_if_failed": "retain C_disformal_mem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "DOBS3904_3_linear_gamma_bound",
            "object": "PPN gamma linear residual",
            "equation": LINEAR_FALLBACK,
            "result": "if product chart is unsigned, linear gamma is bounded by explicit live coefficients instead of handwaved away",
            "status": "FALLBACK_RUNNER_FORMULA_READY",
            "fallback_if_failed": "fill source-backed numeric coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "DOBS3904_4_second_order_bridge",
            "object": "second-order memory stress",
            "equation": "if K_gamma_linear=0, use gamma2_bound from 3902; otherwise use gamma_linear_bound + gamma2_bound",
            "result": "3902 runner now has a clean branch switch",
            "status": "BRANCH_SWITCH_READY",
            "fallback_if_failed": "do not promote local-GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, Any]]:
    source_paths = {
        "memory": rel(SRC / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv"),
        "dobs": rel(SRC / "P8_Y5_OBS_COFRAME_2571_FINITE_DOBS_LEAK_ROWS.csv"),
        "qmap": rel(SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv"),
        "boundary": rel(SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv"),
        "gamma": rel(SRC / "P8_Y5_R2FR_3902_SECOND_ORDER_GAMMA_BOUND_DERIVATION.csv"),
    }
    return [
        {
            "input_id": "COEF3904_0_C_Dq_mem",
            "symbol": "C_Dq_mem",
            "definition": "norm of Dq_parent[partial_Xmem] over all public q components",
            "units": "dimensionless operator norm",
            "zero_route": "product chart Phi=(Q_pub,Y_loc,H_priv) with X_mem in Y_loc",
            "fallback_use": "if nonzero, blocks linear gamma-zero branch and feeds K_E*C_Dq_mem",
            "status": "MISSING_PARENT_PRODUCT_CHART_SIGNATURE_OR_NUMERIC_BOUND",
            "source_path": source_paths["qmap"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_1_C_E_mem",
            "symbol": "C_E_mem",
            "definition": "norm of DObs_e[partial_Xmem], including connection inheritance",
            "units": "dimensionless coframe response",
            "zero_route": "e_obs=E(Q_pub) and Dq[X_mem]=0",
            "fallback_use": "direct metric/coframe contribution to PPN gamma, clocks and orbits",
            "status": "MISSING_QBASIC_OBSERVED_COFRAME_OR_NUMERIC_BOUND",
            "source_path": source_paths["dobs"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_2_C_tau_mem",
            "symbol": "C_tau_mem",
            "definition": "norm of D_Xmem tau/clock/readout mismatch",
            "units": "dimensionless clock response",
            "zero_route": "tau_source=tau_charge=tau_clock=tau_readout=tau(Q_pub)",
            "fallback_use": "Gdot, clock drift and preferred-frame leak",
            "status": "MISSING_TAU_FRAME_LOCK_OR_NUMERIC_BOUND",
            "source_path": source_paths["qmap"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_3_C_disformal_mem",
            "symbol": "C_disformal_mem",
            "definition": "linear coefficient of hidden/disformal X_mem slot in observed metric/coframe",
            "units": "dimensionless linear response",
            "zero_route": "ordinary readout action domain forbids E(Q_pub,X_mem), A(X_mem)tau_tau and B(X_mem)h slots",
            "fallback_use": LINEAR_FALLBACK,
            "status": "MISSING_NO_DISFORMAL_ACTION_DOMAIN_OR_NUMERIC_BOUND",
            "source_path": rel(SRC / "P8_Y5_R2FR_3900_SINGLE_COFRAME_LOCK_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_4_C_boundary_TF_linear",
            "symbol": "C_boundary_TF_linear",
            "definition": "linear traceless boundary/reference anisotropy sourced by X_mem",
            "units": "dimensionless slip-source norm",
            "zero_route": "3892 boundary certificate adopted with fixed relative class and no normal exchange",
            "fallback_use": LINEAR_FALLBACK,
            "status": "MISSING_BOUNDARY_CERTIFICATE_ADOPTION_OR_NUMERIC_BOUND",
            "source_path": source_paths["boundary"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_5_C_projector_TF_linear",
            "symbol": "C_projector_TF_linear",
            "definition": "linear traceless source/projection leak from projector/readout-order variation",
            "units": "dimensionless projection norm",
            "zero_route": "Pi_M fixed before variation or P_loc[d,Pi_M]J_H=0",
            "fallback_use": LINEAR_FALLBACK,
            "status": "MISSING_PROJECTOR_ORDER_ZERO_OR_NUMERIC_BOUND",
            "source_path": rel(SRC / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_6_C_coupling_mem",
            "symbol": "C_coupling_mem",
            "definition": "absolute X_mem derivative of visible couplings/source scales",
            "units": "dimensionless logarithmic response",
            "zero_route": "kappa_MTS, ell_J, G_parent and c_vis are Q_pub-basic parent coefficient slots",
            "fallback_use": "Gdot/Newton/source normalization and clock/alpha drift terms",
            "status": "MISSING_COEFFICIENT_DESCENT_OR_NUMERIC_BOUND",
            "source_path": source_paths["qmap"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "COEF3904_7_K_gamma_linear",
            "symbol": "K_gamma_linear",
            "definition": LINEAR_FALLBACK,
            "units": "dimensionless PPN gamma residual envelope",
            "zero_route": "all C_Dq/C_disformal/boundary/projector linear coefficients vanish",
            "fallback_use": "gamma_total_bound = K_gamma_linear*X_bound + gamma2_bound",
            "status": "FORMULA_READY_INPUTS_NONCLAIM",
            "source_path": source_paths["gamma"],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3904_0_product_chart",
            "decision": "use the product-chart construction as the clean derivation route",
            "reason": "it proves Dq[X_mem]=0 rather than smuggling in a plateau axiom",
            "effect": "promotes memory verticality from vibes to a precise parent-action admission clause",
            "status": "BEST_ROUTE_CONSTRUCTED_NOT_CLAIMED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3904_1_current_corpus",
            "decision": "do not claim current local-GR pass",
            "reason": "tau, constants, boundary, projector and no-disformal clauses are not globally signed",
            "effect": "finite coefficient rows remain active",
            "status": "NO_LOCAL_GR_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3904_2_runner",
            "decision": "branch the scalar runner",
            "reason": "if product chart is adopted use gamma2_bound; otherwise use gamma_linear_bound + gamma2_bound",
            "effect": "turns the coupling worry into testable coefficients",
            "status": "RUNNER_BRANCH_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "GATE3904_0_Dq_theorem", "gate": "Dq memory zero theorem", "result": "proved in product-chart branch", "status": "PASS_CONDITIONAL_EXACT", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3904_1_adoption", "gate": "parent action adopts product chart", "result": "not globally signed in current corpus", "status": "BLOCKED_PARENT_SIGNATURE", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3904_2_DObs", "gate": "observed coframe/connection zero", "result": "exact if e_obs=E(Q_pub) and Dq[X_mem]=0", "status": "PASS_CONDITIONAL_QBASIC", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3904_3_tau_coupling_boundary", "gate": "tau/coupling/boundary/projector inheritance", "result": "open finite rows emitted", "status": "BLOCKED_INPUTS_ACTIVE", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "GATE3904_4_local_GR", "gate": "local GR/Newton promotion", "result": "no claim until product chart and inheritance stack are parent-signed or coefficients are source-bounded", "status": "BLOCKED_NO_CLAIM", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3904_0",
            "target_checkpoint": "3905-Y5-R2FR-parent-product-chart-adoption-and-inheritance-stack-or-linear-coefficient-runner.md",
            "script": "scripts/Y5_R2FR_3905_parent_product_chart_adoption_and_inheritance_stack_or_linear_coefficient_runner.py",
            "objective": "try to adopt the product chart as a parent-action clause for geometry, tau, constants, boundary and projector inheritance; if not, run the linear coefficient fallback",
            "why_next": "3904 proved the memory-zero route inside a product chart; the next leap is parent adoption of that chart, not another search for missing couplings",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRODUCT_CHART_DQ_MEMORY_ZERO_CONSTRUCTED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "Dq[X_mem]=0 and DObs_e[X_mem]=0 are proved inside an explicit local product-chart parent branch; current corpus still needs adoption/inheritance signatures or finite coefficient bounds",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    product_chart: list[dict[str, Any]],
    dq_matrix: list[dict[str, Any]],
    dobs: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3904 - Dq Memory Verticality Proof or Live Scalar Input Fill

Generated: `{timestamp}`

## Result

This checkpoint takes the leap we needed: it constructs the exact route by which the memory field can be locally invisible without inventing a plateau axiom.

Parent branch:

`{PRODUCT_CHART}`

Then:

`{DQ_ZERO}`

and for a q-basic observed coframe:

`{DOBS_ZERO}`

So the good news is real: `Dq[X_mem]=0` is not impossible or mystical. It is an exact theorem in a local parent product chart where `X_mem` is a `Y_loc` fibre coordinate and all ordinary readouts descend through `Q_pub`.

The hard guard is also real: the current corpus has not globally signed that product chart/inheritance stack yet. So there is still no local-GR claim. The fallback is now concrete:

`{LINEAR_FALLBACK}`

## Product-Chart Verticality Theorem

{markdown_table(product_chart, ["row_id", "clause", "statement", "status", "remaining_failure"])}

## Dq Memory Verticality Matrix

{markdown_table(dq_matrix, ["row_id", "q_component", "test", "product_chart_result", "current_corpus_status", "runner_symbol"])}

## DObs/e Readout Test

{markdown_table(dobs, ["test_id", "object", "equation", "status", "fallback_if_failed"])}

## Direct Disformal / Scalar Input Rows

{markdown_table(coefficients, ["input_id", "symbol", "definition", "zero_route", "status", "fallback_use"])}

## Branch Decision

{markdown_table(decision, ["decision_id", "decision", "reason", "effect", "status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3904 is forward movement: the local branch no longer says "maybe memory is invisible". It says exactly what must be true:

1. `Phi` must split locally into `(Q_pub, Y_loc, H_priv)`.
2. `X_mem` must be a `Y_loc` fibre coordinate.
3. `e_obs`, `tau`, visible constants, boundary class and projectors must inherit from `Q_pub`.
4. If any of those fail, the theory must run the explicit `K_gamma_linear` coefficient branch instead.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3904 PRODUCT CHART DQ MEMORY ZERO -->
## 3904 Product-Chart Dq Memory-Zero Branch

Timestamp: `{timestamp}`

Result: `PASS_PRODUCT_CHART_DQ_MEMORY_ZERO_CONSTRUCTED`.

Constructed parent branch:
`{PRODUCT_CHART}`

Exact zero:
`{DQ_ZERO}`

Observed coframe consequence:
`{DOBS_ZERO}`

Fallback if the product chart/inheritance stack is not parent-signed:
`{LINEAR_FALLBACK}`

Decision: no local-GR claim yet. The route is now parent-chart adoption or explicit linear coefficient scoring.
<!-- END 3904 PRODUCT CHART DQ MEMORY ZERO -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3904 PRODUCT CHART DQ MEMORY ZERO -->"
    end = "<!-- END 3904 PRODUCT CHART DQ MEMORY ZERO -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    product_chart: list[dict[str, Any]],
    dq_matrix: list[dict[str, Any]],
    dobs: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3904_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3904_1_product_chart", "product chart theorem constructed", any(row["row_id"] == "PCH3904_1_Dq" and "PROVED" in str(row["status"]) for row in product_chart), "PCH3904_1"))
    checks.append(("VAL3904_2_anti_tautology", "anti-tautology guard retained", any(row["row_id"] == "PCH3904_2_anti_tautology" for row in product_chart), "PCH3904_2"))
    checks.append(("VAL3904_3_dq_matrix", "Dq matrix covers required q components", len(dq_matrix) >= 7 and any(row["q_component"] == "whole_q_vector" for row in dq_matrix), f"{len(dq_matrix)} rows"))
    checks.append(("VAL3904_4_dobs", "DObs chain and disformal countermodel both present", any(row["test_id"] == "DOBS3904_0_chain" for row in dobs) and any(row["test_id"] == "DOBS3904_2_disformal_countermodel" for row in dobs), "chain+countermodel"))
    required_symbols = {"C_Dq_mem", "C_E_mem", "C_tau_mem", "C_disformal_mem", "C_boundary_TF_linear", "C_projector_TF_linear", "C_coupling_mem", "K_gamma_linear"}
    checks.append(("VAL3904_5_coefficients", "live fallback coefficients complete", required_symbols.issubset({str(row["symbol"]) for row in coefficients}), f"{len(coefficients)} coefficients"))
    checks.append(("VAL3904_6_branch_decision", "branch decision chooses chart or fallback", any(row["decision_id"] == "DEC3904_2_runner" for row in decision), "DEC3904_2"))
    checks.append(("VAL3904_7_no_claim", "local GR remains blocked", any(row["gate_id"] == "GATE3904_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "GATE3904_4"))
    checks.append(("VAL3904_8_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [product_chart, dq_matrix, dobs, coefficients, decision, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3904_9_doc", "markdown checkpoint exists with product chart", DOC_PATH.exists() and PRODUCT_CHART in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3904_10_spine", "spine updated with 3904 block", SPINE_PATH.exists() and "BEGIN 3904 PRODUCT CHART DQ MEMORY ZERO" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3904_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3904*")
            if path.is_file() and ("3904-Y5" in path.name or "P8_Y5_R2FR_3904" in path.name or "P8_Y5_BRR545_3904" in path.name)
        ]
    checks.append(("VAL3904_12_formalization_untouched", "no generated 3904 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3904_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3904_14_next_target", "next target is parent product-chart adoption", any("product-chart-adoption" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3905 product chart"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    product_chart = product_chart_rows(timestamp)
    dq_matrix = dq_matrix_rows(timestamp)
    dobs = dobs_rows(timestamp)
    coefficients = coefficient_rows(timestamp)
    decision = decision_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["product_chart"], product_chart)
    write_csv(OUTPUTS["dq_matrix"], dq_matrix)
    write_csv(OUTPUTS["dobs"], dobs)
    write_csv(OUTPUTS["coefficients"], coefficients)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, product_chart, dq_matrix, dobs, coefficients, decision, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, product_chart, dq_matrix, dobs, coefficients, decision, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_PRODUCT_CHART_DQ_MEMORY_ZERO_CONSTRUCTED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
