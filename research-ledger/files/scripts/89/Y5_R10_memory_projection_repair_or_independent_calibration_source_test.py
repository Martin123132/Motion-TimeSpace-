from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_856_SOURCE_REGISTER.csv"
SOURCE_TEST_PATH = RESIDUALS / "P8_Y5_R10_856_INDEPENDENT_RESPONSE_SOURCE_TEST.csv"
REPAIR_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_856_MEMORY_PROJECTION_REPAIR_CONTRACT.csv"
BRANCH_TARGET_PATH = RESIDUALS / "P8_Y5_R10_856_BRANCH_TARGET_CONSTRAINTS.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_856_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_856_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_856_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_856_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_856_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_856_VALIDATION.csv"

ESTIMATOR_PATH = RESIDUALS / "P8_Y5_R10_855_LINEAR_RESPONSE_ESTIMATOR.csv"
OBSERVED_PATH = RESIDUALS / "P8_Y5_R10_855_OBSERVED_CALIBRATION_VECTOR_CHECK.csv"
BRANCH_READOUT_PATH = RESIDUALS / "P8_Y5_R10_853_BRANCH_READOUT.csv"

STATUS = "Y5_R10_856_projection_repair_selected_no_independent_calibration_source_nonclaim"
CLAIM_CEILING = "route_selection_only_no_support_no_calibration_proof_no_parent_prediction"
NEXT_TARGET = "857-Y5-R10-branch-invariant-memory-projection-repair-contract.md"

SOURCE_SPECS = [
    {
        "source_id": "855_doc",
        "path": POST_CHECKPOINT / "855-Y5-R10-calibration-projection-response-estimator-dry-run.md",
        "needles": [
            "does not prove the SH0ES/no-SH0ES amplitude split",
            "independent_calibration_source_or_projection_repair",
            "856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md",
        ],
        "role": "calibration estimator handoff",
    },
    {
        "source_id": "855_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_855_VALIDATION.csv",
        "needles": [
            "V855_3_observed_vector_check_present,pass",
            "V855_6_route_selected,pass",
            "V855_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "855_estimator",
        "path": ESTIMATOR_PATH,
        "needles": ["used_in_sh0es_hf_indicator", "required_vector_mag_to_match_target", "finite_response"],
        "role": "linear response estimator rows",
    },
    {
        "source_id": "855_observed_vectors",
        "path": OBSERVED_PATH,
        "needles": ["insufficient_to_explain_target", "observed_MU_SH0ES_minus_m_b_corr"],
        "role": "observed calibration vector source test",
    },
    {
        "source_id": "853_branch_readout",
        "path": BRANCH_READOUT_PATH,
        "needles": ["competitive_nonclaim", "b_mem_fixed", "delta_BIC_vs_best_fit_baseline"],
        "role": "branch target amplitudes",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def finite_float(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: object) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def source_test_rows(estimator: list[dict[str, str]], observed: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    hf = next(row for row in estimator if row["branch"] == "sh0es" and row["vector_name"] == "used_in_sh0es_hf_indicator")
    lowz = next(row for row in estimator if row["branch"] == "sh0es" and row["vector_name"] == "low_z_lt_0p15_indicator")
    calibrator = next(row for row in estimator if row["branch"] == "sh0es" and row["vector_name"] == "calibrator_indicator")
    ceph = next(row for row in estimator if row["branch"] == "sh0es" and row["vector_name"] == "ceph_minus_mu_calibrator_residual")
    global_obs = next(row for row in observed if row["observed_vector"] == "observed_MU_SH0ES_minus_m_b_corr")
    ceph_obs = next(row for row in observed if row["observed_vector"] == "observed_CEPH_minus_MU_calibrator_only")
    return [
        {
            "test_id": "SRC856_0_global_offset",
            "candidate_source": "observed MU_SH0ES minus m_b_corr global offset",
            "required_effective_magnitude": "not_applicable",
            "observed_or_available_magnitude": global_obs["predicted_delta_b_from_observed_vector"],
            "target_delta_b": global_obs["target_delta_b"],
            "status": "fails_projected_out",
            "reason": "SN nuisance offset marginalization removes this mode",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "SRC856_1_observed_ceph_residual",
            "candidate_source": "observed CEPH minus MU calibrator residual",
            "required_effective_magnitude": ceph["required_vector_mag_to_match_target"],
            "observed_or_available_magnitude": ceph_obs["predicted_delta_b_from_observed_vector"],
            "target_delta_b": ceph_obs["target_delta_b"],
            "status": "fails_too_small",
            "reason": "observed residual predicts far less delta_b than required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "SRC856_2_hf_indicator",
            "candidate_source": "Hubble-flow indicator response",
            "required_effective_magnitude": hf["required_vector_mag_to_match_target"],
            "observed_or_available_magnitude": "MISSING_INDEPENDENT_SOURCE",
            "target_delta_b": hf["response_required_to_match_branch_target"],
            "status": "spans_but_unsourced",
            "reason": "finite required magnitude exists but is solved from target, not independently derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "SRC856_3_lowz_indicator",
            "candidate_source": "low-z indicator response",
            "required_effective_magnitude": lowz["required_vector_mag_to_match_target"],
            "observed_or_available_magnitude": "MISSING_INDEPENDENT_SOURCE",
            "target_delta_b": lowz["response_required_to_match_branch_target"],
            "status": "spans_but_unsourced",
            "reason": "finite required magnitude exists but is solved from target, not independently derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "SRC856_4_calibrator_indicator",
            "candidate_source": "calibrator-only indicator response",
            "required_effective_magnitude": calibrator["required_vector_mag_to_match_target"],
            "observed_or_available_magnitude": "MISSING_INDEPENDENT_SOURCE",
            "target_delta_b": calibrator["response_required_to_match_branch_target"],
            "status": "spans_but_unsourced_large",
            "reason": "requires a larger effective vector magnitude and no source is signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_target_rows(branch_readout: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in branch_readout:
        b_mem = float(row["b_mem_fixed"])
        rows.append(
            {
                "branch": row["branch"],
                "b_eff_target": fmt(b_mem),
                "eta1_aF_DeltaR_target": fmt(3.0 * b_mem),
                "delta_BIC_vs_best_fit_baseline": row["delta_BIC_vs_best_fit_baseline"],
                "role_in_repair": "anchor_parent_like_shape_branch" if row["branch"] == "no_sh0es" else "local_calibration_pressure_branch",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def repair_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "RPC856_0_invariant_limit",
            "requirement": "b_response -> 0 must reduce exactly to branch-invariant parent memory",
            "mathematical_form": "E2(z;B)=E2_LCDM + b_parent A_parent(z) + b_response[B] A_response(z;B)",
            "acceptance_gate": "no_SH0ES and SH0ES reduce to same b_parent when response source is absent",
            "status": "required_next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "RPC856_1_response_source",
            "requirement": "b_response[B] must be predicted by an independently sourced local/calibration response or set to zero",
            "mathematical_form": "b_response[B] = C_response * q_B, with q_B sourced before scoring",
            "acceptance_gate": "q_B path exists and does not use fitted b_eff target",
            "status": "required_next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "RPC856_2_BAO_guard",
            "requirement": "response term must not repair SN by silently breaking BAO",
            "mathematical_form": "Delta chi2_BAO(response) tracked separately from Delta chi2_SN(response)",
            "acceptance_gate": "BAO residual pressure table included in next dry-run",
            "status": "required_next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "RPC856_3_conservation_guard",
            "requirement": "if response is physical rather than observational, conservation accounting must be signed",
            "mathematical_form": "nabla_mu(T_parent^{mu nu}+T_response^{mu nu})=0 or response remains likelihood-level projection",
            "acceptance_gate": "physical response claims forbidden unless conservation row passes",
            "status": "required_next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC856_0_selected",
            "route": "branch_invariant_memory_projection_repair_contract",
            "status": "selected",
            "reason": "no independent calibration/local-response amplitude is currently sourced; response law cannot be promoted",
            "include": "two-channel projection contract, response source requirement, BAO/conservation guards",
            "exclude": "more scoring with free branch amplitudes, support claim, calibration proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC856_1_deferred",
            "route": "independent_calibration_source_search",
            "status": "deferred",
            "reason": "can be reopened if a real external/local source for q_B is supplied or derived",
            "include": "future sourced calibration/local-response amplitude",
            "exclude": "using fitted target as source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG856_0_no_calibration_source",
            "claim": "current data source calibration response amplitude",
            "status": "forbidden",
            "reason": "observed simple vectors are insufficient and indicator amplitudes are unsourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG856_1_no_projection_repair_done",
            "claim": "memory projection has been repaired",
            "status": "forbidden",
            "reason": "856 only writes the repair contract; no new projection is scored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG856_2_no_support",
            "claim": "positive fixed memory is support-grade",
            "status": "forbidden",
            "reason": "parent amplitude, response source, and robustness gates remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG856_3_allowed_route_selection",
            "claim": "projection repair is selected as the disciplined next route",
            "status": "allowed_private_nonclaim",
            "reason": "the independent source tests fail or remain unsourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D856_0",
            "finding": "no independent calibration/local-response amplitude is sourced yet",
            "reason": "global offset is projected out, observed calibrator residual is too small, and HF/low-z amplitudes are solved from target",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D856_1",
            "finding": "memory projection repair contract is selected before more scoring",
            "reason": "otherwise branch amplitudes become phenomenological knobs",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "write the branch-invariant/two-channel memory projection repair contract before any further scoring",
            "include": "A_parent, A_response, response-source gate, BAO residual guard, conservation status, no b_mem fitting",
            "exclude": "support claim, public evidence, formalization-workbench edits, fitted target as derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "tested independent calibration/local-response source status and selected projection repair",
            "selected_route": "branch_invariant_memory_projection_repair_contract",
            "what_is_not_claimed": "calibration proof, repaired projection, support, parent prediction, public evidence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    source_tests: list[dict[str, object]],
    repair_contract: list[dict[str, object]],
    branch_targets: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_855_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    tests_ok = len(source_tests) == 5 and any(row["status"] == "fails_too_small" for row in source_tests) and any(row["status"] == "spans_but_unsourced" for row in source_tests)
    repair_ok = len(repair_contract) == 4 and all(row["status"] == "required_next" for row in repair_contract)
    target_ok = len(branch_targets) == 2 and {row["branch"] for row in branch_targets} == {"no_sh0es", "sh0es"}
    route_ok = any(row["route_id"] == "RC856_0_selected" and row["route"] == "branch_invariant_memory_projection_repair_contract" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, source_tests, repair_contract, branch_targets, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V856_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V856_1_prior_855_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V856_2_source_tests_classified", "result": "pass" if tests_ok else "fail", "detail": "source tests include too-small and unsourced outcomes"},
        {"check_id": "V856_3_repair_contract_ready", "result": "pass" if repair_ok else "fail", "detail": "projection repair contract rows recorded"},
        {"check_id": "V856_4_branch_targets_present", "result": "pass" if target_ok else "fail", "detail": "no_sh0es and sh0es targets carried forward"},
        {"check_id": "V856_5_route_selected", "result": "pass" if route_ok else "fail", "detail": "branch-invariant projection repair contract selected"},
        {"check_id": "V856_6_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V856_7_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V856_8_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V856_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V856_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    source_tests: list[dict[str, object]],
    repair_contract: list[dict[str, object]],
    branch_targets: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 856 - Y5 R10 Memory Projection Repair Or Independent Calibration Source Test",
        "",
        "Current result: **no independent calibration/local-response amplitude is sourced strongly enough to explain the branch split**, so the disciplined next route is a branch-invariant memory-projection repair contract. The fair SN/BAO lead remains alive, but we cannot promote the SH0ES/no-SH0ES split to physics by solving for a response vector amplitude after the fact.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Independent Response Source Test",
        "",
        csv_table(source_tests, ["test_id", "candidate_source", "required_effective_magnitude", "observed_or_available_magnitude", "target_delta_b", "status", "reason", "valid_for_claim"]),
        "",
        "## Branch Target Constraints",
        "",
        csv_table(branch_targets, ["branch", "b_eff_target", "eta1_aF_DeltaR_target", "delta_BIC_vs_best_fit_baseline", "role_in_repair", "valid_for_claim"]),
        "",
        "## Memory Projection Repair Contract",
        "",
        csv_table(repair_contract, ["contract_id", "requirement", "mathematical_form", "acceptance_gate", "status", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    estimator = read_csv(ESTIMATOR_PATH)
    observed = read_csv(OBSERVED_PATH)
    branch_readout = read_csv(BRANCH_READOUT_PATH)
    source_tests = source_test_rows(estimator, observed, generated_utc)
    branch_targets = branch_target_rows(branch_readout, generated_utc)
    repair_contract = repair_contract_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, source_tests, repair_contract, branch_targets, routes, guards, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_TEST_PATH, source_tests, ["test_id", "candidate_source", "required_effective_magnitude", "observed_or_available_magnitude", "target_delta_b", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(REPAIR_CONTRACT_PATH, repair_contract, ["contract_id", "requirement", "mathematical_form", "acceptance_gate", "status", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_TARGET_PATH, branch_targets, ["branch", "b_eff_target", "eta1_aF_DeltaR_target", "delta_BIC_vs_best_fit_baseline", "role_in_repair", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, source_tests, repair_contract, branch_targets, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
