from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4827"
CLAIM_ID = "L-669"
MARKER = "PPC4161_PROJECTOR_STRESS_ZERO_OR_FIRST_TPIM_BOUND_ROW_4827"
PACKET_MARKER = "PPC4161_PACKET_PROJECTOR_STRESS_ZERO_OR_FIRST_TPIM_BOUND_ROW_4827"
DECISION = "PROJECTOR_STRESS_ZERO_UNSIGNED_FIRST_TPIM_BOUND_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4828-Y5-R2FR-topological-Hilbert-equality-or-first-Req-Bzero-row.md"

DOC_PATH = POST / "4827-Y5-R2FR-projector-stress-zero-or-first-TPiM-bound-row.md"
FORMAL_PATH = FORMAL / "843-PPC4161-projector-stress-zero-or-first-TPiM-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "projector_stress_TPiM_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4827_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4827_PROJECTOR_STRESS_ZERO_AUDIT.csv"
BOUND_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4827_TPIM_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4827_TPIM_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4827_TPIM_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4827_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4827_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4827_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4827_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4827_VALIDATION.csv"

SOURCE_PATHS = {
    "resume": RESUME_PATH,
    "4826_doc": POST / "4826-Y5-R2FR-PiM-commutator-zero-or-first-Icommutator-bound-row.md",
    "1014_doc": POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1013_doc": POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "stress_contract": SOURCE_DIR / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "obstruction_vector": SOURCE_DIR / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "radial_input": SOURCE_DIR / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
    "fill_template": SOURCE_DIR / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
    "flux_residual": SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "worldtube_runner": SOURCE_DIR / "P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4827_00_resume", SOURCE_PATHS["resume"], "4827-Y5-R2FR-projector-stress-zero-or-first-TPiM-bound-row.md", "4826 selected projector stress as next obstruction."),
        ("SRC4827_01_4826_doc", SOURCE_PATHS["4826_doc"], "PIMZ4826_6_projector_stress_silence", "4826 leaves projector-stress silence open."),
        ("SRC4827_02_1014_doc", SOURCE_PATHS["1014_doc"], "PCC1014_3_projector_stress_beta_equiv", "1014 names projector stress beta equivalent."),
        ("SRC4827_03_1013_doc", SOURCE_PATHS["1013_doc"], "OBS1013_5_projector_stress", "1013 names T_PiM obstruction."),
        ("SRC4827_04_stress_contract_PV0", SOURCE_PATHS["stress_contract"], "PV0_product_variation_included", "product variation cannot be dropped."),
        ("SRC4827_05_stress_contract_PV2", SOURCE_PATHS["stress_contract"], "PV2_Hodge_DeWitt_metric_dependence_retained", "Hodge/DeWitt metric dependence must be varied."),
        ("SRC4827_06_stress_contract_PV6", SOURCE_PATHS["stress_contract"], "PV6_modified_exterior_residual_map", "retained stress maps into PPN/source-normalization rows."),
        ("SRC4827_07_stress_contract_PV7", SOURCE_PATHS["stress_contract"], "PV7_readout_masks_after_variation_only", "readout masks cannot enter parent variation."),
        ("SRC4827_08_obstruction_vector", SOURCE_PATHS["obstruction_vector"], "OBS1013_5_projector_stress", "machine obstruction vector."),
        ("SRC4827_09_radial_input", SOURCE_PATHS["radial_input"], "PI521_2_projector_stress_vector", "projector-stress vector input template."),
        ("SRC4827_10_fill_template", SOURCE_PATHS["fill_template"], "PIF537_3_projector_stress_beta_equiv", "beta-equivalent fill template."),
        ("SRC4827_11_flux_residual", SOURCE_PATHS["flux_residual"], "SMR509_1_Delta_PiM", "source-measure residual map."),
        ("SRC4827_12_worldtube_runner", SOURCE_PATHS["worldtube_runner"], "MR510_3_projector_hair", "worldtube projector-hair blocker."),
        ("SRC4827_13_runner", SOURCE_PATHS["runner"], "def evaluate_row", "4827 executable runner."),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("TPZ4827_0_variation_included", "full Pi_M product/metric variation", "delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H and delta_g Pi_M terms are carried", "WRITTEN_GATE", "dropping projector stress is forbidden"),
        ("TPZ4827_1_topological_route", "metric-independent topological Pi_M", "delta_g Pi_M=0 on the compact exterior branch", "CONDITIONAL_NOT_PARENT_SIGNED", "direct T_PiM row"),
        ("TPZ4827_2_Hodge_route", "Hodge/DeWitt route retained", "delta_g star, Delta, Green operator and boundary metric dependence produce T_PiM", "RETAINED_IF_USED", "component stress bound"),
        ("TPZ4827_3_domain_homology_fixed", "domain/homology selector fixed or varied", "delta Sigma_ext, chi_D, n_mu and L_cg are zero/topological or retained", "NOT_PARENT_DERIVED", "domain-motion stress row"),
        ("TPZ4827_4_boundary_wall_silent", "boundary wall/improvement has no source tail", "T_PiM boundary term is zero-flux, class-only, monopole-only and derivative-silent", "FAIL_OPEN", "boundary_wall_stress row"),
        ("TPZ4827_5_denominator_reference_silent", "no hidden denominator/reference stress", "M_H_ref and projector denominator do not vary with source/range/frame/readout", "FAIL_OPEN", "denominator_reference_stress row"),
        ("TPZ4827_6_Bianchi_owned", "total stress is Bianchi-compatible", "nabla_mu(T_matter+T_PiM+T_extra)^mu_nu=0 with no dropped exchange force", "NOT_CLOSED", "PPN/source residual vector"),
        ("TPZ4827_7_no_readout_mask", "anti-circularity", "post-readout Pi_M and measured GM never source a theorem zero", "POLICY_GUARD", "forbidden-source guard"),
    ]
    return [
        {
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "math_form": math_form,
            "current_result": current_result,
            "finite_fallback": finite_fallback,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, claim_piece, math_form, current_result, finite_fallback in rows
    ]


def bound_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("TPC4827_0_zero", "T_PiM_norm_abs=0", "all projector-stress zero clauses parent-signed in the same branch", "conditional_only"),
        ("TPC4827_1_direct", "T_PiM_norm_abs", "direct weak-field/PPN equivalent norm of metric/domain projector stress", "runner_ready_values_missing"),
        ("TPC4827_2_components", "sum six stress components", "metric + domain + Hodge/Green + wall + denominator/reference + source/readout stress", "runner_ready_values_missing"),
        ("TPC4827_3_PPN", "C_i_TPiM*T_PiM", "maps retained projector stress into beta, gamma, alpha3 and xi rows", "runner_ready_values_missing"),
        ("TPC4827_4_BY5", "tau_BY5_TPiM*T_PiM", "feeds projector stress into source-normalization/BY5 finite branch", "runner_ready_values_missing"),
    ]
    return [
        {
            "contract_id": contract_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, quantity, definition, status in rows
    ]


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    doc_1014 = str(SOURCE_PATHS["1014_doc"])
    stress_contract = str(SOURCE_PATHS["stress_contract"])
    base_flags = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero_flags = {
        "parent_variation_includes_PiM_signed": "true",
        "PiM_parent_owned_signed": "true",
        "metric_independent_topological_signed": "true",
        "domain_homology_fixed_signed": "true",
        "boundary_wall_silent_signed": "true",
        "denominator_reference_silent_signed": "true",
        "Bianchi_total_stress_owned_signed": "true",
        "Hilbert_current_compatibility_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    return [
        {
            "row_id": "RUN4827_0_live_zero_missing",
            "route_type": "stress_zero",
            "route": "live zero audit",
            "source_path": doc_1014,
            "equation_ref": "CG1014_1_projector_stress",
            "notes": "physical branch has unsigned projector stress clauses",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_1_conditional_zero_pass",
            "route_type": "stress_zero",
            "route": "conditional parent-signed zero",
            "source_path": stress_contract,
            "equation_ref": "PV1/PV2/PV6 projector-stress route",
            "notes": "nonclaim theorem-shape smoke row",
            **base_flags,
            **zero_flags,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_2_forbidden_dropped_stress",
            "route_type": "stress_zero",
            "route": "forbidden dropped stress",
            "source_path": stress_contract,
            "equation_ref": "PV0_product_variation_included",
            "notes": "DROP_PROJECTOR_STRESS is not a derivation",
            **base_flags,
            **zero_flags,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_3_live_direct_bound_missing",
            "route_type": "direct_bound",
            "route": "live T_PiM value missing",
            "source_path": str(SOURCE_PATHS["radial_input"]),
            "equation_ref": "PI521_2_projector_stress_vector",
            "T_PiM_norm_abs": "MISSING_PROJECTOR_STRESS_MAP",
            "tau_BY5_TPiM_abs": "MISSING_TAU",
            "notes": "no physical source-backed T_PiM value yet",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_4_direct_TPiM_smoke_pass",
            "route_type": "direct_bound",
            "route": "direct finite T_PiM smoke",
            "source_path": str(SOURCE_PATHS["fill_template"]),
            "equation_ref": "PIF537_3_projector_stress_beta_equiv",
            "T_PiM_norm_abs": "0.02",
            "C_beta_TPiM_abs": "0.50",
            "C_gamma_TPiM_abs": "0.25",
            "C_alpha3_TPiM_abs": "0.10",
            "C_xi_TPiM_abs": "0.05",
            "tau_BY5_TPiM_abs": "2.0",
            "notes": "nonclaim direct PPN/source-feed smoke row",
            **base_flags,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_5_component_TPiM_smoke_pass",
            "route_type": "component_bound",
            "route": "component finite T_PiM smoke",
            "source_path": stress_contract,
            "equation_ref": "PV6_modified_exterior_residual_map",
            "metric_projector_stress_abs": "0.01",
            "domain_motion_stress_abs": "0.02",
            "hodge_green_stress_abs": "0.03",
            "boundary_wall_stress_abs": "0.01",
            "denominator_reference_stress_abs": "0.02",
            "source_readout_stress_abs": "0.01",
            "C_beta_TPiM_abs": "0.40",
            "C_gamma_TPiM_abs": "0.20",
            "C_alpha3_TPiM_abs": "0.10",
            "C_xi_TPiM_abs": "0.05",
            "tau_BY5_TPiM_abs": "1.5",
            "notes": "nonclaim component stress smoke row",
            **base_flags,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_6_forbidden_reference_zero",
            "route_type": "direct_bound",
            "route": "forbidden reference row zero",
            "source_path": doc_1014,
            "equation_ref": "PRS1014_5_reference_zero",
            "T_PiM_norm_abs": "0.0",
            "C_beta_TPiM_abs": "1.0",
            "tau_BY5_TPiM_abs": "1.0",
            "notes": "REFERENCE_ROW_AS_ZERO cannot zero physical T_PiM",
            **base_flags,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_7_forbidden_measured_GM_source",
            "route_type": "component_bound",
            "route": "forbidden measured GM source",
            "source_path": doc_1014,
            "equation_ref": "measured GM readout",
            "metric_projector_stress_abs": "0.0",
            "domain_motion_stress_abs": "0.0",
            "hodge_green_stress_abs": "0.0",
            "boundary_wall_stress_abs": "0.0",
            "denominator_reference_stress_abs": "0.0",
            "source_readout_stress_abs": "0.0",
            "C_beta_TPiM_abs": "1.0",
            "tau_BY5_TPiM_abs": "1.0",
            "notes": "MEASURED_GM_AS_SOURCE cannot source projector stress silence",
            **base_flags,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4827_8_forbidden_cancellation",
            "route_type": "component_bound",
            "route": "forbidden cancellation",
            "source_path": stress_contract,
            "equation_ref": "component cancellation",
            "metric_projector_stress_abs": "0.01",
            "domain_motion_stress_abs": "0.01",
            "hodge_green_stress_abs": "0.01",
            "boundary_wall_stress_abs": "0.01",
            "denominator_reference_stress_abs": "0.01",
            "source_readout_stress_abs": "0.01",
            "C_beta_TPiM_abs": "1.0",
            "tau_BY5_TPiM_abs": "1.0",
            "notes": "CANCEL_UNKNOWN_COMPONENTS is not a theorem zero",
            **base_flags,
            "timestamp_utc": timestamp,
        },
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)


def build_decision(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4827_0",
            "decision": DECISION,
            "basis": "live projector-stress zero clauses and live T_PiM values are missing; direct/component smoke routes execute; dropped-stress/reference/measured-GM shortcuts fail closed",
            "zero_claim": False,
            "finite_bound_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def build_claim_gates(timestamp: str, outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    return [
        {
            "gate_id": "CG4827_0_zero",
            "claim": "projector stress is zero/gauge-only/boundary-silent",
            "passed": by_id["RUN4827_0_live_zero_missing"]["runner_status"] == "PROJECTOR_STRESS_ZERO_PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "live topological/metric-independent, domain, boundary, denominator and Bianchi clauses remain unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CG4827_1_TPiM_bound",
            "claim": "source-backed T_PiM PPN/source-normalization row exists",
            "passed": by_id["RUN4827_3_live_direct_bound_missing"]["runner_status"] == "PROJECTOR_STRESS_DIRECT_BOUND_PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "live T_PiM remains missing; smoke rows only check arithmetic",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CG4827_2_anti_circularity",
            "claim": "projector stress is not dropped or hidden in measured GM/reference rows",
            "passed": by_id["RUN4827_2_forbidden_dropped_stress"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE"
            and by_id["RUN4827_6_forbidden_reference_zero"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE"
            and by_id["RUN4827_7_forbidden_measured_GM_source"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
            "claim_allowed": False,
            "reason": "forbidden routes fail closed",
            "timestamp_utc": timestamp,
        },
    ]


def build_status(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "claim_allowed": False,
            "physics_status": "projector-stress zero remains unsigned; T_PiM finite PPN/source-normalization contract is executable but nonclaim",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def build_next_target(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "reason": "once projector stress is retained as a real gate, the next root source-coupling problem is whether the closed topological current equals the observed Hilbert projected current",
            "success_condition": "derive Pi_M J_H = J_M_top + dB_zero with zero compact boundary flux, or produce first R_eq/B_zero source-backed bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validate(timestamp: str, outputs: list[dict[str, str]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    checks = [
        ("VAL4827_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4827_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4827_02_live_zero_blocked", by_id["RUN4827_0_live_zero_missing"]["runner_status"] == "BLOCKED_PROJECTOR_STRESS_ZERO_CLAUSES", "live stress zero remains blocked"),
        ("VAL4827_03_conditional_zero_pass", by_id["RUN4827_1_conditional_zero_pass"]["runner_status"] == "PROJECTOR_STRESS_ZERO_PASS_NONCLAIM", "conditional stress zero computes"),
        ("VAL4827_04_dropped_stress_fails", by_id["RUN4827_2_forbidden_dropped_stress"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "dropped stress route fails closed"),
        ("VAL4827_05_live_bound_blocked", by_id["RUN4827_3_live_direct_bound_missing"]["runner_status"] == "BLOCKED_PROJECTOR_STRESS_DIRECT_BOUND_INPUTS", "live T_PiM row missing"),
        ("VAL4827_06_direct_smoke_pass", by_id["RUN4827_4_direct_TPiM_smoke_pass"]["runner_status"] == "PROJECTOR_STRESS_DIRECT_BOUND_PASS_NONCLAIM", "direct T_PiM smoke passes"),
        ("VAL4827_07_component_smoke_pass", by_id["RUN4827_5_component_TPiM_smoke_pass"]["runner_status"] == "PROJECTOR_STRESS_COMPONENT_BOUND_PASS_NONCLAIM", "component T_PiM smoke passes"),
        ("VAL4827_08_reference_zero_fails", by_id["RUN4827_6_forbidden_reference_zero"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "reference-zero shortcut fails closed"),
        ("VAL4827_09_measured_GM_fails", by_id["RUN4827_7_forbidden_measured_GM_source"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "measured-GM shortcut fails closed"),
        ("VAL4827_10_cancellation_fails", by_id["RUN4827_8_forbidden_cancellation"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "cancellation shortcut fails closed"),
        ("VAL4827_11_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in outputs), "no runner row allows a claim"),
    ]
    return [
        {
            "validation_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "details": details,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, details in checks
    ]


def build_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4827 - Projector Stress Zero Or First TPiM Bound Row

Marker: `{MARKER}`

## Summary

4827 attacks the stress-energy cost of using `Pi_M`:

```text
T_PiM^{{mu nu}} = -2/sqrt(-g) delta S_PiM / delta g_mu_nu
T_PiM_bound = |T_metric|+|T_domain|+|T_Hodge|+|T_wall|+|T_ref|+|T_readout|
PPN_i = C_i_TPiM T_PiM_bound
BY5_TPiM = tau_BY5_TPiM T_PiM_bound
```

The exact-zero route is attractive but still unsigned. It requires `Pi_M` to be parent-owned, metric-independent/topological or fully varied, domain/homology fixed, wall/reference/denominator terms silent, and the total Bianchi stress ledger owned in the same branch. The finite route is now executable: direct `T_PiM` or component stress rows feed PPN and source-normalization without dropping projector stress or hiding it in measured `GM`.

## Source register

{md_table(sources, ['source_id', 'exists', 'needle_found', 'role'])}

## Zero audit

{md_table(audit, ['clause_id', 'claim_piece', 'current_result', 'finite_fallback'])}

## Bound contract

{md_table(contract, ['contract_id', 'quantity', 'definition', 'status'])}

## Runner output

{md_table(outputs, ['row_id', 'runner_status', 'T_PiM_norm_abs', 'projector_stress_beta_equiv_abs', 'projector_stress_gamma_equiv_abs', 'BY5_projector_stress_feed_abs', 'missing_for_claim'])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`

## Validation

{md_table(validations, ['validation_id', 'result', 'details'])}
"""
    formal = f"""# 843 - PPC4161 projector stress zero or first TPiM bound row

Marker: `{MARKER}`

4827 makes `T_PiM` an explicit local-GR/Newton source-coupling gate. The live branch does **not** prove projector-stress silence. A metric-independent topological `Pi_M` could zero the stress, but the current corpus has not parent-signed the topological/domain/boundary/Bianchi clauses in one branch. Therefore any Hodge/DeWitt/domain/readout implementation must retain:

```text
T_PiM_bound = |T_metric|+|T_domain|+|T_Hodge|+|T_wall|+|T_ref|+|T_readout|
PPN_i = C_i_TPiM T_PiM_bound
BY5_TPiM = tau_BY5_TPiM T_PiM_bound
```

Smoke rows verify direct and component arithmetic. Dropped-stress, reference-zero, cancellation-only and measured-`GM` routes fail closed. No local-GR/Newton/source-normalization claim is allowed from this checkpoint.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "projector_stress_zero_or_first_TPiM_bound_row",
        "current_evidence": "4827 converts the PiM projector-stress problem into an executable zero-or-finite T_PiM/PPN/BY5 runner; live zero and source-backed T_PiM values remain missing.",
        "status": "projector_stress_TPiM_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "metric-independent topological PiM, domain/homology silence, boundary/reference silence, Bianchi ownership, and source-backed T_PiM values remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live projector-stress rows are not source-backed",
        "title": "Projector stress zero or first TPiM bound row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIMS_PATH.exists():
        rows = read_csv(CLAIMS_PATH)
        if any(existing.get("claim_id") == CLAIM_ID for existing in rows):
            return
        fields = list(rows[0].keys()) if rows else list(row.keys())
        for key in row:
            if key not in fields:
                fields.append(key)
        rows.append(row)
        with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def update_spine_and_packet(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4827 projector-stress TPiM runner

`{MARKER}`. Projector stress is now an explicit local source-coupling gate: either `Pi_M` is parent-owned and metric-independent/topological with silent domain/boundary/Bianchi clauses, or `T_PiM` is retained and mapped into PPN/source-normalization rows. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4827 projector stress zero-or-bound runner

`{MARKER}` turns hidden projector stress into a calculable obstruction. Conditional zero requires parent-signed topological/domain/boundary/Bianchi clauses; finite direct/component rows compute PPN and BY5 feeds; dropped-stress, reference-zero, cancellation and measured-GM shortcuts fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4827-Y5-R2FR-projector-stress-zero-or-first-TPiM-bound-row.md`
Marker: `{MARKER}`

## Where we are

4827 made the hidden projector-stress cost executable:

```text
T_PiM^{{mu nu}} = -2/sqrt(-g) delta S_PiM / delta g_mu_nu
T_PiM_bound = |T_metric|+|T_domain|+|T_Hodge|+|T_wall|+|T_ref|+|T_readout|
PPN_i = C_i_TPiM T_PiM_bound
BY5_TPiM = tau_BY5_TPiM T_PiM_bound
```

## Live blockers

- Projector-stress zero is not parent-signed.
- Metric-independent/topological `Pi_M`, domain/homology silence, boundary/wall silence, denominator/reference silence, and Bianchi ownership remain open.
- No source-backed physical `T_PiM` row exists yet.
- Dropping projector stress, reference-zero rows, measured `GM`, and cancellation-only routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(__file__, doraise=True)

    sources = source_register(timestamp)
    audit = zero_audit(timestamp)
    contract = bound_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT, audit)
    write_csv(BOUND_CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)

    run_runner()
    outputs = read_csv(RUNNER_OUTPUT)
    decisions = build_decision(timestamp)
    gates = build_claim_gates(timestamp, outputs)
    status = build_status(timestamp)
    next_rows = build_next_target(timestamp)
    validations = validate(timestamp, outputs, sources)

    write_csv(DECISION_CSV, decisions)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    write_csv(VALIDATION_CSV, validations)

    build_docs(timestamp, sources, audit, contract, outputs, validations)
    update_claims(timestamp)
    update_spine_and_packet(timestamp)
    update_resume(timestamp)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["result"] != "PASS"]
    if failed:
        raise RuntimeError(f"4827 validation failed: {failed}")
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
