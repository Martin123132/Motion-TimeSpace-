from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "985-Y5-R10-WEP-imported-basis-screening-runner-MICROSCOPE-TiPt.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)
ETA_BOUND = 6.992e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "984_doc",
            "path": "984-Y5-R10-source-charge-basis-derivation-or-phenomenological-basis-import.md",
            "role": "handoff selecting WEP imported-basis runner",
            "needle": "DEC984_2_best_next",
        },
        {
            "source_id": "984_imported_basis",
            "path": "source-intake/mts_residuals/P8_Y5_R10_984_IMPORTED_PHENOMENOLOGICAL_BASIS.csv",
            "role": "imported nonclaim charge basis",
            "needle": "IMP984_2_electromagnetic_Coulomb",
        },
        {
            "source_id": "984_basis_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_984_BASIS_TO_MTS_SLOT_MAP.csv",
            "role": "basis-to-MTS-slot map showing missing b_kappa route",
            "needle": "BMAP984_3_basis_to_bkappa",
        },
        {
            "source_id": "983_delta_vector",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv",
            "role": "MICROSCOPE alloy proxy deltas",
            "needle": "DEL983_coulomb_proxy",
        },
        {
            "source_id": "983_identity_bounds",
            "path": "source-intake/mts_residuals/P8_Y5_R10_983_IDENTITY_DEBUG_BOUNDS.csv",
            "role": "identity debug bounds for single-proxy sanity",
            "needle": "IB983_coulomb_proxy",
        },
        {
            "source_id": "981_candidates",
            "path": "source-intake/mts_residuals/P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv",
            "role": "eta screening envelope source row",
            "needle": "CP981_0_b_kappa_species_split_WEP",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def delta_lookup() -> dict[str, float]:
    rows = read_csv(OUT / "P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv")
    return {row["feature"]: float(row["delta_value"]) for row in rows}


def identity_lookup() -> dict[str, float]:
    rows = read_csv(OUT / "P8_Y5_R10_983_IDENTITY_DEBUG_BOUNDS.csv")
    return {row["feature"]: float(row["identity_debug_bound"]) for row in rows}


def coefficient_vector_template() -> list[dict[str, str]]:
    return [
        {
            "coefficient_id": "C985_0_C_Ye",
            "symbol": "C_Ye",
            "basis_feature": "Y_e_proxy",
            "MTS_slot_candidate": "b_theta_or_b_m",
            "status": "MISSING_PHENOMENOLOGICAL_COEFFICIENT",
            "value": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C985_1_C_N",
            "symbol": "C_N",
            "basis_feature": "neutron_excess_proxy",
            "MTS_slot_candidate": "b_theta_or_b_kappa_after_source_projection",
            "status": "MISSING_PHENOMENOLOGICAL_COEFFICIENT",
            "value": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C985_2_C_C",
            "symbol": "C_C",
            "basis_feature": "coulomb_proxy",
            "MTS_slot_candidate": "b_theta_alpha_EM_first",
            "status": "MISSING_PHENOMENOLOGICAL_COEFFICIENT",
            "value": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C985_3_C_A",
            "symbol": "C_A",
            "basis_feature": "A_bar_proxy",
            "MTS_slot_candidate": "b_m_or_nonstandard_source_marker",
            "status": "MISSING_PHENOMENOLOGICAL_COEFFICIENT",
            "value": "MISSING",
            "valid_for_claim": "false",
        },
        {
            "coefficient_id": "C985_4_S_source",
            "symbol": "S_source",
            "basis_feature": "source_normalization",
            "MTS_slot_candidate": "b_kappa",
            "status": "MISSING_CI_TO_MTS_SLOT_MAP",
            "value": "MISSING",
            "valid_for_claim": "false",
        },
    ]


def runner_scenarios(deltas: dict[str, float], identities: dict[str, float]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    zero_coeffs = {"Y_e_proxy": 0.0, "neutron_excess_proxy": 0.0, "coulomb_proxy": 0.0, "A_bar_proxy": 0.0}
    rows.append(make_scenario("SCEN985_0_parent_zero_debug", "all imported coefficients set to zero", zero_coeffs, deltas, "parent_zero_debug_only", "universal Hilbert source would imply this only if parent gates are signed"))
    for feature, bound in identities.items():
        coeffs = {"Y_e_proxy": 0.0, "neutron_excess_proxy": 0.0, "coulomb_proxy": 0.0, "A_bar_proxy": 0.0}
        coeffs[feature] = bound
        rows.append(make_scenario(f"SCEN985_1_identity_{feature}", f"single proxy coefficient saturates eta envelope: {feature}", coeffs, deltas, "identity_debug_only", "single-proxy dominance is not an MTS source-charge projection"))
    for scale in [0.1, 0.01]:
        coeffs = {feature: scale * identities.get(feature, 0.0) for feature in ["Y_e_proxy", "neutron_excess_proxy", "coulomb_proxy", "A_bar_proxy"]}
        rows.append(make_scenario(f"SCEN985_2_multiaxis_{scale:g}x_identity", f"all proxy coefficients set to {scale:g} times their identity debug bound", coeffs, deltas, "multi_axis_debug_only", "simultaneous coefficients can add or cancel; no C_i-to-MTS map supplied"))
    return rows


def make_scenario(
    scenario_id: str,
    description: str,
    coeffs: dict[str, float],
    deltas: dict[str, float],
    scenario_type: str,
    why_not_claim: str,
) -> dict[str, str]:
    eta_pred = sum(deltas.get(feature, 0.0) * coeffs.get(feature, 0.0) for feature in coeffs)
    ratio = abs(eta_pred) / ETA_BOUND if ETA_BOUND > 0 else float("inf")
    return {
        "scenario_id": scenario_id,
        "description": description,
        "scenario_type": scenario_type,
        "C_Ye": f"{coeffs.get('Y_e_proxy', 0.0):.9e}",
        "C_N": f"{coeffs.get('neutron_excess_proxy', 0.0):.9e}",
        "C_C": f"{coeffs.get('coulomb_proxy', 0.0):.9e}",
        "C_A": f"{coeffs.get('A_bar_proxy', 0.0):.9e}",
        "eta_pred": f"{eta_pred:.9e}",
        "eta_bound": f"{ETA_BOUND:.9e}",
        "abs_eta_over_bound": f"{ratio:.9e}",
        "screen_result": "screen_pass_debug" if ratio <= 1.0 + 1e-12 else "screen_fail_debug",
        "why_not_claim": why_not_claim,
        "valid_for_claim": "false",
    }


def hard_gate_rows(scenarios: list[dict[str, str]]) -> list[dict[str, str]]:
    debug_screens_parse = all(row["screen_result"] in {"screen_pass_debug", "screen_fail_debug"} for row in scenarios)
    return [
        {
            "gate_id": "HG985_0_runner_executes",
            "requirement": "screening runner produces eta_pred and ratio rows",
            "gate_result": "pass" if debug_screens_parse else "fail",
            "claim_allowed": "false",
            "detail": "runner arithmetic works but scenarios are debug-only",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "HG985_1_parent_zero_claim",
            "requirement": "parent-zero branch can be claimed",
            "gate_result": "blocked_parent_gates_unsigned",
            "claim_allowed": "false",
            "detail": "universal source theorem is relative, not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "HG985_2_imported_basis_claim",
            "requirement": "imported C_i basis bounds MTS coefficients",
            "gate_result": "blocked_missing_Ci_to_MTS_map",
            "claim_allowed": "false",
            "detail": "C_i are phenomenological placeholders, not b_kappa/b_theta values",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "HG985_3_WEP_pass",
            "requirement": "MICROSCOPE WEP pass for MTS local branch",
            "gate_result": "blocked_no_claim",
            "claim_allowed": "false",
            "detail": "no scored MTS coefficient row exists",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC985_0_runner",
            "topic": "imported-basis WEP runner",
            "result": "screening_runner_operational_nonclaim",
            "reason": "eta prediction arithmetic now exists for zero, identity, and multi-axis debug scenarios",
            "next_action": "do not treat debug screen pass/fail as theory evidence",
        },
        {
            "decision_id": "DEC985_1_theory",
            "topic": "MTS coefficient status",
            "result": "Ci_to_MTS_map_missing",
            "reason": "imported phenomenological coefficients are not b_kappa or b_theta without a parent coupling map",
            "next_action": "derive or explicitly choose a Ci-to-slot map before any WEP scoring",
        },
        {
            "decision_id": "DEC985_2_best_next",
            "topic": "next checkpoint",
            "result": "derive_Ci_to_MTS_slot_map_or_parent_zero_theorem",
            "reason": "the runner exists; the remaining physics is the map or the parent zero theorem",
            "next_action": "write 986 Ci-to-MTS slot map attempt, prioritizing alpha_EM/Coulomb to b_theta and source-normalization to b_kappa",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "986-Y5-R10-Ci-to-MTS-slot-map-or-parent-zero-theorem.md",
            "objective": "derive the map from phenomenological WEP coefficients C_i to MTS slots b_theta/b_kappa/b_m, or prove the parent universal-source zero theorem instead",
            "include": "Coulomb-to-alpha_EM route, nuclear-binding-to-matter-constant route, source-normalization-to-b_kappa route, hard claim gates",
            "exclude": "WEP pass, invented C_i values, theorem-zero promotion without parent signatures, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    coefficients_nonclaim_ok = all(row["valid_for_claim"] == "false" and row["value"] == "MISSING" for row in coefficients)
    scenarios_nonclaim_ok = all(row["valid_for_claim"] == "false" for row in scenarios)
    runner_arithmetic_ok = all(float(row["abs_eta_over_bound"]) >= 0.0 for row in scenarios)
    gates_safe_ok = all(row["claim_allowed"] == "false" for row in gates)
    decision_ok = any(row["decision_id"] == "DEC985_2_best_next" and row["result"] == "derive_Ci_to_MTS_slot_map_or_parent_zero_theorem" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V985_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all source files exist and needles are found"},
        {"check_id": "V985_1_coefficients_nonclaim", "result": "pass" if coefficients_nonclaim_ok else "fail", "detail": "C_i coefficient template rows remain missing/nonclaim"},
        {"check_id": "V985_2_scenarios_nonclaim", "result": "pass" if scenarios_nonclaim_ok else "fail", "detail": "all runner scenarios remain nonclaim"},
        {"check_id": "V985_3_runner_arithmetic", "result": "pass" if runner_arithmetic_ok else "fail", "detail": "eta_pred ratios parse and are nonnegative"},
        {"check_id": "V985_4_hard_gates_safe", "result": "pass" if gates_safe_ok else "fail", "detail": "hard gates block WEP/MTS coefficient claims"},
        {"check_id": "V985_5_next_decision", "result": "pass" if decision_ok else "fail", "detail": "986 C_i-to-MTS map or parent-zero theorem selected"},
        {"check_id": "V985_6_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V985_7_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {"check_id": "V985_READY", "result": "pass" if ready else "fail", "detail": "985 checkpoint pack validation summary", "generated_utc": stamp()}
    ]


def write_doc(
    sources: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    scenarios: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 985 Y5 R10: WEP Imported-Basis Screening Runner MICROSCOPE TiPt",
        "",
        "Status: `Y5_R10_985_WEP_imported_basis_screening_runner_operational_nonclaim_Ci_to_MTS_map_missing`",
        "",
        "Claim ceiling: no WEP pass, no `b_kappa` bound, no `b_theta` bound, no source-charge theorem-zero promotion, and no local-GR claim.",
        "",
        "## Readout",
        "",
        "985 makes the imported-basis branch runnable without making it claimable. The runner computes:",
        "",
        "`eta_pred = DeltaY_e*C_Ye + Deltaq_N*C_N + Deltaq_C*C_C + DeltaAbar*C_A`.",
        "",
        "The zero branch, identity branch, and multi-axis debug branches are all useful for scale discipline. None of them is MTS evidence until either the parent universal-source zero theorem is signed or the `C_i -> b_theta/b_kappa/b_m` map is derived.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Coefficient Vector Template",
        "",
        md_table(coefficients, ["coefficient_id", "symbol", "basis_feature", "MTS_slot_candidate", "status", "value", "valid_for_claim"]),
        "",
        "## Screening Scenarios",
        "",
        md_table(scenarios, ["scenario_id", "description", "scenario_type", "eta_pred", "eta_bound", "abs_eta_over_bound", "screen_result", "why_not_claim", "valid_for_claim"]),
        "",
        "## Hard Gates",
        "",
        md_table(gates, ["gate_id", "requirement", "gate_result", "claim_allowed", "detail", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    deltas = delta_lookup()
    identities = identity_lookup()
    coefficients = coefficient_vector_template()
    scenarios = runner_scenarios(deltas, identities)
    gates = hard_gate_rows(scenarios)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, coefficients, scenarios, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_985_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_985_COEFFICIENT_VECTOR_TEMPLATE.csv", coefficients)
    write_csv(OUT / "P8_Y5_R10_985_SCREENING_SCENARIOS.csv", scenarios)
    write_csv(OUT / "P8_Y5_R10_985_HARD_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_985_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_985_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_985_VALIDATION.csv", validation)
    write_doc(sources, coefficients, scenarios, gates, decisions, validation, next_target)


if __name__ == "__main__":
    main()
