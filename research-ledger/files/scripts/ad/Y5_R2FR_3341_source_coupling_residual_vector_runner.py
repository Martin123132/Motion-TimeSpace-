from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3341-Y5-R2FR-source-coupling-residual-vector-runner-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3341_0_3340_doc",
        "path": ROOT / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
        "role": "3340 parent Hilbert clause and residual vector handoff",
    },
    {
        "source_id": "SRC3341_1_3340_clause",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv",
        "role": "parent clause rows",
    },
    {
        "source_id": "SRC3341_2_3340_evidence",
        "path": OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv",
        "role": "parent signature evidence score",
    },
    {
        "source_id": "SRC3341_3_3340_residual_schema",
        "path": OUT / "P8_Y5_R2FR_3340_FINITE_RESIDUAL_VECTOR_SCHEMA.csv",
        "role": "finite residual vector schema",
    },
    {
        "source_id": "SRC3341_4_3340_budget",
        "path": OUT / "P8_Y5_R2FR_3340_SOURCE_COUPLING_BUDGET_INTERFACE.csv",
        "role": "absolute source vector budget interface",
    },
    {
        "source_id": "SRC3341_5_3339_validation",
        "path": OUT / "P8_Y5_BRR545_3339_VALIDATION.csv",
        "role": "previous coupling decomposition validation",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3341_SOURCE_REGISTER.csv",
    "component_contract": OUT / "P8_Y5_R2FR_3341_COMPONENT_RUNNER_CONTRACT.csv",
    "candidate_rows": OUT / "P8_Y5_R2FR_3341_RESIDUAL_VECTOR_CANDIDATES.csv",
    "runner_results": OUT / "P8_Y5_R2FR_3341_RESIDUAL_VECTOR_RUNNER_RESULTS.csv",
    "aggregate": OUT / "P8_Y5_R2FR_3341_AGGREGATE_SOURCE_BUDGET.csv",
    "refusals": OUT / "P8_Y5_R2FR_3341_REFUSAL_LEDGER.csv",
    "requirements": OUT / "P8_Y5_R2FR_3341_NEXT_SOURCE_REQUIREMENTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3341_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3341_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3341_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3341_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
B_GAMMA = 2.3e-5
F_SOURCE = 0.30
B_SOURCE = F_SOURCE * B_GAMMA
COMPONENT_IDS = [
    "FRV3340_0_delta_kappa_common",
    "FRV3340_1_eta_species",
    "FRV3340_2_xi_tensor",
    "FRV3340_3_chi_spin_clock",
    "FRV3340_4_epsilon_EM",
    "FRV3340_5_epsilon_contact",
    "FRV3340_6_epsilon_boundary",
    "FRV3340_7_epsilon_bianchi",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def parse_float(value: str) -> float | None:
    try:
        if not value or value.startswith("MISSING"):
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def load_residual_schema() -> list[dict[str, str]]:
    schema_path = OUT / "P8_Y5_R2FR_3340_FINITE_RESIDUAL_VECTOR_SCHEMA.csv"
    if not schema_path.exists():
        return []
    return read_csv(schema_path)


def load_parent_evidence() -> list[dict[str, str]]:
    evidence_path = OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv"
    if not evidence_path.exists():
        return []
    return read_csv(evidence_path)


def parent_signature_closed() -> bool:
    evidence = load_parent_evidence()
    return bool(evidence) and all(row.get("passes_parent_signature") == "true" for row in evidence)


def component_contract_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    schema_by_id = {row.get("component_id", ""): row for row in load_residual_schema()}
    clause_map = {
        "FRV3340_0_delta_kappa_common": "HSC3340_2_common_kappa",
        "FRV3340_1_eta_species": "HSC3340_3_no_spurion_weights",
        "FRV3340_2_xi_tensor": "HSC3340_1_variation_target",
        "FRV3340_3_chi_spin_clock": "HSC3340_0_parent_action_form",
        "FRV3340_4_epsilon_EM": "HSC3340_4_public_Maxwell_Hodge",
        "FRV3340_5_epsilon_contact": "HSC3340_5_kernel_boundary_owner",
        "FRV3340_6_epsilon_boundary": "HSC3340_5_kernel_boundary_owner",
        "FRV3340_7_epsilon_bianchi": "HSC3340_6_bianchi_balance",
    }
    for component_id in COMPONENT_IDS:
        schema = schema_by_id.get(component_id, {})
        rows.append(
            {
                "component_id": component_id,
                "symbol": schema.get("symbol", ""),
                "required_zero_clause": clause_map[component_id],
                "numeric_required_columns": "component_value;response_factor;component_units;source_path;equation_ref;arena;no_cancellation_guard;valid_for_claim",
                "theorem_zero_rule": "allowed only if theorem_zero=true and zero_authority=PARENT_SIGNED_HSC3340",
                "numeric_rule": "finite component_value and response_factor; existing source_path; no_cancellation_guard=ABS_SUM_NO_CANCELLATION; valid_for_claim=true",
                "contribution_formula": "abs(component_value * response_factor)",
                "status": "RUNNER_CONTRACT_READY",
                "valid_for_claim": "false",
            }
        )
    return rows


def candidate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for component_id in COMPONENT_IDS:
        rows.append(
            {
                "candidate_id": f"CAND3341_missing_{component_id}",
                "component_id": component_id,
                "mode": "missing_live_placeholder",
                "theorem_zero": "false",
                "zero_authority": "MISSING_PARENT_SIGNATURE",
                "component_value": "MISSING_COMPONENT_VALUE",
                "response_factor": "MISSING_RESPONSE_FACTOR",
                "component_units": "MISSING_UNITS",
                "source_path": "MISSING_SOURCE_PATH",
                "equation_ref": "MISSING_EQUATION_REF",
                "arena": "MISSING_ARENA",
                "no_cancellation_guard": "MISSING_ABS_GUARD",
                "valid_for_claim": "false",
            }
        )
    for component_id in COMPONENT_IDS:
        rows.append(
            {
                "candidate_id": f"CAND3341_zero_unsigned_{component_id}",
                "component_id": component_id,
                "mode": "theorem_zero_switch_unsigned",
                "theorem_zero": "true",
                "zero_authority": "MISSING_PARENT_SIGNATURE",
                "component_value": "0",
                "response_factor": "1",
                "component_units": "dimensionless",
                "source_path": str(OUT / "P8_Y5_R2FR_3340_PARENT_CLAUSE_EVIDENCE_SCORE.csv"),
                "equation_ref": "EV3340_all_parent_signature_false",
                "arena": "local_source_coupling",
                "no_cancellation_guard": "ABS_SUM_NO_CANCELLATION",
                "valid_for_claim": "false",
            }
        )
    smoke_values = {
        "FRV3340_0_delta_kappa_common": 1.0e-8,
        "FRV3340_1_eta_species": 1.0e-13,
        "FRV3340_2_xi_tensor": 1.0e-8,
        "FRV3340_3_chi_spin_clock": 1.0e-9,
        "FRV3340_4_epsilon_EM": 2.0e-8,
        "FRV3340_5_epsilon_contact": 1.0e-8,
        "FRV3340_6_epsilon_boundary": 1.0e-8,
        "FRV3340_7_epsilon_bianchi": 1.0e-8,
    }
    for component_id, value in smoke_values.items():
        rows.append(
            {
                "candidate_id": f"CAND3341_smoke_nonclaim_{component_id}",
                "component_id": component_id,
                "mode": "numeric_schema_smoke_nonclaim",
                "theorem_zero": "false",
                "zero_authority": "NOT_THEOREM_ZERO",
                "component_value": f"{value:.6e}",
                "response_factor": "1.000000e+00",
                "component_units": "dimensionless",
                "source_path": str(OUT / "P8_Y5_R2FR_3340_FINITE_RESIDUAL_VECTOR_SCHEMA.csv"),
                "equation_ref": "FRV3340_schema_smoke_not_source_measurement",
                "arena": "local_source_coupling",
                "no_cancellation_guard": "ABS_SUM_NO_CANCELLATION",
                "valid_for_claim": "false",
            }
        )
    return rows


def evaluate_candidate(row: dict[str, Any]) -> dict[str, Any]:
    failure_reasons: list[str] = []
    source_path = Path(str(row.get("source_path", "")))
    theorem_zero = str(row.get("theorem_zero", "")).lower() == "true"
    zero_authority = str(row.get("zero_authority", ""))
    valid_for_claim = str(row.get("valid_for_claim", "")).lower() == "true"
    component_value = parse_float(str(row.get("component_value", "")))
    response_factor = parse_float(str(row.get("response_factor", "")))
    computed_abs = ""
    if theorem_zero:
        if zero_authority != "PARENT_SIGNED_HSC3340":
            failure_reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_HSC3340")
        if not parent_signature_closed():
            failure_reasons.append("PARENT_SIGNATURE_VECTOR_NOT_CLOSED")
        contribution = 0.0 if not failure_reasons else None
    else:
        if component_value is None:
            failure_reasons.append("MISSING_FINITE_COMPONENT_VALUE")
        if response_factor is None:
            failure_reasons.append("MISSING_FINITE_RESPONSE_FACTOR")
        if not str(row.get("component_units", "")) or str(row.get("component_units", "")).startswith("MISSING"):
            failure_reasons.append("MISSING_COMPONENT_UNITS")
        if not str(row.get("equation_ref", "")) or str(row.get("equation_ref", "")).startswith("MISSING"):
            failure_reasons.append("MISSING_EQUATION_REF")
        if not str(row.get("arena", "")) or str(row.get("arena", "")).startswith("MISSING"):
            failure_reasons.append("MISSING_ARENA")
        if str(row.get("no_cancellation_guard", "")) != "ABS_SUM_NO_CANCELLATION":
            failure_reasons.append("MISSING_ABSOLUTE_SUM_GUARD")
        if not source_path.exists():
            failure_reasons.append("MISSING_EXISTING_SOURCE_PATH")
        if not valid_for_claim:
            failure_reasons.append("VALID_FOR_CLAIM_FALSE")
        contribution = None
        if component_value is not None and response_factor is not None:
            contribution = abs(component_value * response_factor)
            computed_abs = f"{contribution:.6e}"
    score_ready = not failure_reasons
    return {
        "runner_id": f"RUN3341_{row['candidate_id']}",
        "candidate_id": row["candidate_id"],
        "component_id": row["component_id"],
        "mode": row["mode"],
        "score_ready": bool_str(score_ready),
        "claim_allowed": bool_str(score_ready and valid_for_claim),
        "computed_abs_contribution": computed_abs if computed_abs else ("0.000000e+00" if theorem_zero and score_ready else "NOT_SCORED"),
        "within_private_source_budget": bool_str((contribution or 0.0) <= B_SOURCE) if contribution is not None else "false",
        "failure_reasons": ";".join(failure_reasons) if failure_reasons else "",
        "valid_for_claim": "false",
    }


def runner_result_rows() -> list[dict[str, Any]]:
    return [evaluate_candidate(row) for row in candidate_rows()]


def aggregate_rows() -> list[dict[str, Any]]:
    results = runner_result_rows()
    smoke_results = [row for row in results if "smoke_nonclaim" in row["candidate_id"]]
    smoke_sum = 0.0
    for row in smoke_results:
        value = parse_float(row["computed_abs_contribution"])
        if value is not None:
            smoke_sum += value
    return [
        {
            "aggregate_id": "AGG3341_0_live_placeholders",
            "candidate_family": "missing_live_placeholder",
            "components": len([row for row in results if "missing_" in row["candidate_id"]]),
            "score_ready_count": sum(1 for row in results if "missing_" in row["candidate_id"] and row["score_ready"] == "true"),
            "claim_allowed": "false",
            "reason": "all live placeholders lack finite values, sources, units, equations, arenas, and valid_for_claim",
            "valid_for_claim": "false",
        },
        {
            "aggregate_id": "AGG3341_1_unsigned_zero_switches",
            "candidate_family": "theorem_zero_switch_unsigned",
            "components": len([row for row in results if "zero_unsigned" in row["candidate_id"]]),
            "score_ready_count": sum(1 for row in results if "zero_unsigned" in row["candidate_id"] and row["score_ready"] == "true"),
            "claim_allowed": "false",
            "reason": "theorem-zero switches are refused without PARENT_SIGNED_HSC3340",
            "valid_for_claim": "false",
        },
        {
            "aggregate_id": "AGG3341_2_smoke_vector",
            "candidate_family": "numeric_schema_smoke_nonclaim",
            "components": len(smoke_results),
            "private_abs_sum": f"{smoke_sum:.6e}",
            "private_budget": f"{B_SOURCE:.6e}",
            "within_private_budget": bool_str(smoke_sum <= B_SOURCE),
            "claim_allowed": "false",
            "reason": "smoke rows prove arithmetic/schema only; they point to schema, not source measurements, and valid_for_claim=false",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in runner_result_rows():
        if result["score_ready"] == "false":
            rows.append(
                {
                    "refusal_id": f"REF3341_{result['candidate_id']}",
                    "candidate_id": result["candidate_id"],
                    "component_id": result["component_id"],
                    "refusal": "REFUSED_MISSING_PROVENANCE_OR_PARENT_SIGNATURE",
                    "why": result["failure_reasons"],
                    "required_exit": "parent-signed theorem-zero or finite source-backed residual component with units, equation, arena, existing source path, absolute-sum guard, and valid_for_claim=true",
                    "claim_allowed": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "req_id": "REQ3341_0_eta_species_first",
            "target_component": "FRV3340_1_eta_species",
            "required_input": "eta_A-eta_B theorem-zero from no-spurion parent syntax or WEP/source-composition numeric bound",
            "why_first": "species/source weights are the cleanest common-kappa failure mode and map directly to WEP/material tests",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3341_1_epsilon_EM_second",
            "target_component": "FRV3340_4_epsilon_EM",
            "required_input": "b_alpha, delta_J, delta_star, EM stress readout, and Poynting flux closure from one public Hodge convention",
            "why_first": "EM/Poynting is a strong discriminator for whether coupling is truly universal Hilbert stress",
            "valid_for_claim": "false",
        },
        {
            "req_id": "REQ3341_2_parent_zero_bundle",
            "target_component": "all FRV3340",
            "required_input": "PARENT_SIGNED_HSC3340 for HSC3340_0..HSC3340_6",
            "why_first": "one parent clause would close the vector faster than filling eight empirical components",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    results = runner_result_rows()
    aggregate = aggregate_rows()
    return [
        {
            "gate_id": "GATE3341_0_runner_contract",
            "claim": "runner contract exists for every FRV3340 component",
            "passed": bool_str({row["component_id"] for row in component_contract_rows()} == set(COMPONENT_IDS)),
            "reason": "component contracts cover theorem-zero and finite numeric modes",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3341_1_unsigned_zero_refused",
            "claim": "unsigned theorem-zero switches are refused",
            "passed": bool_str(all(row["score_ready"] == "false" for row in results if "zero_unsigned" in row["candidate_id"])),
            "reason": "PARENT_SIGNED_HSC3340 is required",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3341_2_missing_rows_refused",
            "claim": "missing placeholder rows are refused",
            "passed": bool_str(all(row["score_ready"] == "false" for row in results if "missing_" in row["candidate_id"])),
            "reason": "finite values, units, sources, equations, arenas, and no-cancellation guards are mandatory",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3341_3_smoke_arithmetic",
            "claim": "nonclaim smoke vector computes an absolute sum",
            "passed": bool_str(any(row["aggregate_id"] == "AGG3341_2_smoke_vector" and row["within_private_budget"] == "true" for row in aggregate)),
            "reason": "arithmetic path works but remains nonclaim",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3341_4_local_GR_claim",
            "claim": "MTS local-GR source-coupling branch is claim-ready",
            "passed": "false",
            "reason": "no theorem-zero bundle or source-backed finite residual vector is currently score-ready",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3341_0",
            "question": "Did the residual vector runner allow a shortcut claim?",
            "answer": "no",
            "reason": "unsigned zero switches and missing placeholders are refused automatically",
            "next_action": "fill eta_species or epsilon_EM with a theorem-zero proof or source-backed bound",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3341_1",
            "question": "Did the runner improve the project?",
            "answer": "yes",
            "reason": "future coupling rows now have a hard interface and cannot silently pass without source/provenance",
            "next_action": "attack the highest leverage components rather than re-auditing the entire coupling stack",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3342-Y5-R2FR-eta-species-no-spurion-zero-or-WEP-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3342_eta_species_no_spurion_zero_or_WEP_bound.py",
            "objective": "try to prove eta_species=0 from parent no-spurion/Hilbert source syntax; if it fails, acquire/source a finite WEP/source-composition bound row for FRV3340_1",
            "must_include": "source-only weight exclusion, material constants, measured-G common mode, WEP observable map, no placeholder pass, no local-GR claim",
            "fallback_if_failed": "move to epsilon_EM public-Hodge/Poynting residual branch",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    contracts = component_contract_rows()
    candidates = candidate_rows()
    results = runner_result_rows()
    aggregate = aggregate_rows()
    refusals = refusal_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3341_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3341_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3341_2_outputs_parse",
            "check": "all 3341 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3341_3_contract_components",
            "check": "contracts cover all FRV3340 components",
            "passed": {row["component_id"] for row in contracts} == set(COMPONENT_IDS),
            "detail": "",
        },
        {
            "check_id": "VAL3341_4_candidate_families",
            "check": "candidate rows include missing, unsigned zero, and smoke families for every component",
            "passed": len(candidates) == len(COMPONENT_IDS) * 3,
            "detail": "",
        },
        {
            "check_id": "VAL3341_5_refuses_placeholders",
            "check": "missing placeholders and unsigned zero switches are refused",
            "passed": all(row["score_ready"] == "false" for row in results if "missing_" in row["candidate_id"] or "zero_unsigned" in row["candidate_id"]),
            "detail": "",
        },
        {
            "check_id": "VAL3341_6_smoke_nonclaim",
            "check": "smoke vector computes but remains nonclaim",
            "passed": any(row["aggregate_id"] == "AGG3341_2_smoke_vector" and row["within_private_budget"] == "true" and row["claim_allowed"] == "false" for row in aggregate),
            "detail": "",
        },
        {
            "check_id": "VAL3341_7_refusal_ledger",
            "check": "refusal ledger records failed rows",
            "passed": len(refusals) >= len(COMPONENT_IDS) * 2,
            "detail": "",
        },
        {
            "check_id": "VAL3341_8_no_claim",
            "check": "local-GR claim gate remains false",
            "passed": all(row["passed"] == "false" for row in gates if row["gate_id"] == "GATE3341_4_local_GR_claim"),
            "detail": "",
        },
        {
            "check_id": "VAL3341_9_next_3342",
            "check": "next target attacks eta_species no-spurion zero or WEP bound",
            "passed": any("eta_species=0" in row["objective"] and "WEP" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3341_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3341_11_overall",
            "check": "3341 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3341 - Source-coupling residual vector runner under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3341 makes the 3340 fallback executable.",
        "",
        "The runner accepts only two routes for each residual component:",
        "",
        "1. `theorem_zero=true` with `zero_authority=PARENT_SIGNED_HSC3340`, or",
        "2. a finite source-backed numeric row with units, equation reference, arena, existing source path, `ABS_SUM_NO_CANCELLATION`, and `valid_for_claim=true`.",
        "",
        "Current missing rows are refused. Current theorem-zero switches are refused because the parent Hilbert source clause is not signed.",
        "",
        "A tiny nonclaim smoke vector is computed only to prove the arithmetic path works; it is not evidence.",
        "",
        f"Private steering source budget remains `B_source = {B_SOURCE:.3e}`.",
        "",
        "No local-GR/PPN/Maxwell claim is made.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Component Runner Contract", component_contract_rows(), "component_id"),
        ("Residual Vector Candidates", candidate_rows(), "candidate_id"),
        ("Residual Vector Runner Results", runner_result_rows(), "runner_id"),
        ("Aggregate Source Budget", aggregate_rows(), "aggregate_id"),
        ("Refusal Ledger", refusal_rows(), "refusal_id"),
        ("Next Source Requirements", requirement_rows(), "req_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It is a strict runner scaffold: it refuses missing placeholders and unsigned theorem-zero switches.",
            "- It selects `eta_species` as the next highest-leverage coupling target, with `epsilon_EM` as the next fallback.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["component_contract"], component_contract_rows())
    write_csv(OUTPUTS["candidate_rows"], candidate_rows())
    write_csv(OUTPUTS["runner_results"], runner_result_rows())
    write_csv(OUTPUTS["aggregate"], aggregate_rows())
    write_csv(OUTPUTS["refusals"], refusal_rows())
    write_csv(OUTPUTS["requirements"], requirement_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
