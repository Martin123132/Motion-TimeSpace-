from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_NOHYPERMOMENTUM_LEVICIVITA_OR_P4_ROW_2374"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2374-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2374_2373_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2373_NEXT_TARGET.csv", "NEXT2373_0_selected", "2373 selected no-hypermomentum/LC gate"),
        ("SRC2374_2373_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2373_VALIDATION.csv", "VAL2373_OVERALL", "2373 validation"),
        ("SRC2374_2333_proof", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2333_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv", "NHL2333_6_verdict", "no-hypermomentum/Levi-Civita proof audit"),
        ("SRC2374_2333_p4", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2333_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv", "P4R2333_0_hypermomentum_total", "P4 hypermomentum residual row"),
        ("SRC2374_2333_decision", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2333_CONNECTION_GATE_DECISION_LEDGER.csv", "CGD2333_1_best_next", "connection gate decision"),
        ("SRC2374_2333_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2333_NEXT_TARGET.csv", "NEXT2333_0", "no-Gamma slot next target"),
        ("SRC2374_2333_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2333_VALIDATION.csv", "VAL2333_OVERALL", "2333 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def proof_audit() -> list[dict[str, object]]:
    rows = [
        (
            "NHL2374_0_target",
            "no-hypermomentum / Levi-Civita source connection",
            "Gamma_obs=Gamma_LC[g_obs] and Delta_lambda^{mu nu}=delta S_ord/delta Gamma^lambda_{mu nu}=0 for matter, source, clock, light, orbit and readout sectors.",
            "TARGET_SHARPENED",
            "must be signed by parent variable selection or Palatini/no-hypermomentum theorem",
            "E_spin=0 and a major source-side GR coupling gate closes",
        ),
        (
            "NHL2374_1_metric_only_parent",
            "metric-only observed ordinary sector",
            "ordinary/source/readout configuration contains e_obs/g_obs and omega_LC[e_obs], but no independent Gamma argument",
            "EXACT_IF_PARENT_VARIABLE_LIST_SIGNED",
            "not signed for every matter/source/readout sector",
            "Delta_lambda^{mu nu}=0 by absence of variable",
        ),
        (
            "NHL2374_2_chain_rule_spin_connection",
            "coframe-owned spin connection",
            "spin connection is omega[e_obs], so spinor variation is counted through e_obs rather than an independent torsionful Gamma",
            "EXACT_CONDITIONAL_CLAUSE",
            "spinor and transport sectors need explicit coframe-owned connection clause",
            "ordinary spin does not create independent torsion source",
        ),
        (
            "NHL2374_3_palatini_route",
            "Palatini EH + no hypermomentum",
            "if independent Gamma enters only EH and Delta_lambda^{mu nu}=0, the Gamma equation gives Levi-Civita up to projective gauge",
            "CONDITIONAL_ROUTE_NOT_ACTIVE",
            "EH-only operator, no-Gamma matter/source/readout, and projective silence remain unsigned",
            "dynamic Levi-Civita compatibility rather than metric-only kinematics",
        ),
        (
            "NHL2374_4_source_readout_guard",
            "source/readout Gamma-slot exclusion",
            "delta S_source/delta Gamma = delta S_clock/delta Gamma = delta S_light/delta Gamma = delta S_orbit/delta Gamma = delta S_readout/delta Gamma = 0",
            "REQUIRED_GUARD_UNSIGNED",
            "source/worldtube/clock/light/orbit/readout Gamma-slot audit is not parent-signed",
            "connection cannot re-enter through measurement protocols",
        ),
        (
            "NHL2374_5_projective_caveat",
            "projective trace silence",
            "projective mode is gauge/fixed/unobservable in source charge, clocks, lightcones, spin transport and orbital readout",
            "UNSIGNED_OR_OPTIONAL_SOURCE_MISSING",
            "projective certificate/policy is not claim-grade in this branch",
            "Palatini route can avoid trace leakage",
        ),
        (
            "NHL2374_6_verdict",
            "promote Levi-Civita/no-hypermomentum",
            "current MTS corpus proves no independent connection source and no hypermomentum for all ordinary local tests",
            "NOT_DERIVED_RETAIN_P4_ROW",
            "metric-only parent, Palatini/EH, spin connection, source/readout Gamma-slot and projective clauses are unsigned",
            "use P4 hypermomentum residual row",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "formal_statement": statement,
            "status": status,
            "obstruction": obstruction,
            "effect_if_closed": effect,
        }
        for row_id, route, statement, status, obstruction, effect in rows
    ]


def p4_residual_row() -> list[dict[str, object]]:
    rows = [
        (
            "P4R2374_0_hypermomentum_total",
            "independent_connection_hypermomentum",
            "Delta_abs",
            "Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||",
            "WEP;clock;source_charge;orbital;PPN;local_GR",
            "hypermomentum units or normalized dimensionless envelope",
            "MISSING_DELTA_COMPONENT_VALUES",
            "Delta components; K_hyper; norm definition; weak-field projection; arena bounds; source path",
        ),
        (
            "P4R2374_1_no_gamma_switch",
            "zero-switch",
            "Delta_lambda^{mu nu}",
            "Delta_lambda^{mu nu}=0 only if no independent Gamma slot exists in ordinary/source/readout branch",
            "all local source-current arenas",
            "boolean/theorem",
            "REQUIRES_PARENT_VARIABLE_ABSENCE",
            "parent variable list; matter/source/readout no-Gamma audit",
        ),
        (
            "P4R2374_2_axial_torsion_guard",
            "axial_torsion_spin_coupling",
            "S_axial_abs",
            "S_axial_abs := ||c_A S_mu J5^mu|| or normalized spin-torsion response envelope",
            "spin_transport;clock;WEP;source_charge",
            "spin-current units or normalized dimensionless envelope",
            "MISSING_SPIN_TORSION_COEFFICIENT",
            "spinor action branch; torsion coefficient; fermion source density; clock_or_spin_bound; source path",
        ),
        (
            "P4R2374_3_mapping_contract",
            "P4 weak-field/arena map",
            "K_P4",
            "epsilon_P4 <= K_hyper * Delta_abs plus absolute envelopes for torsion/nonmetricity components",
            "R10;PPN;clock;WEP;orbital;lightcone",
            "arena-specific after projection",
            "MISSING_WEAK_FIELD_MAP_AND_UNIT_NORMALIZATION",
            "component basis; unit normalization; lab frame; observable kernel; no-cancellation policy",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "channel": channel,
            "residual_symbol": symbol,
            "residual_formula": formula,
            "affected_tests": tests,
            "units": units,
            "current_status": status,
            "required_inputs": inputs,
        }
        for row_id, channel, symbol, formula, tests, units, status, inputs in rows
    ]


def no_gamma_slot_audit_seed() -> list[dict[str, object]]:
    rows = [
        ("NGS2374_0_matter", "ordinary matter action", "no independent Gamma argument in L_A beyond omega_LC[e_obs]", "MISSING_SECTOR_AUDIT"),
        ("NGS2374_1_source", "source support/worldtube", "source profile and support use observed metric/coframe data, not independent connection response", "MISSING_SECTOR_AUDIT"),
        ("NGS2374_2_clock", "clock/readout standards", "clock protocols do not vary Gamma independently or create hypermomentum source", "MISSING_SECTOR_AUDIT"),
        ("NGS2374_3_light", "lightcone/EM optics", "light propagation branch uses metric/coframe observable structure or retains connection residual", "MISSING_SECTOR_AUDIT"),
        ("NGS2374_4_orbit", "orbit/Kepler readout", "orbital calibration uses observed connection determined by metric/coframe or finite residual", "MISSING_SECTOR_AUDIT"),
        ("NGS2374_5_readout", "PPN/local readout maps", "readout maps are downstream and no-source-codomain, not Gamma-source couplings", "MISSING_SECTOR_AUDIT"),
        ("NGS2374_6_verdict", "all local sectors", "Delta_lambda^{mu nu}=0 across matter/source/readout branch", "NOT_DERIVED_AUDIT_REQUIRED"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "sector": sector,
            "no_gamma_condition": condition,
            "status": status,
        }
        for row_id, sector, condition, status in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        (
            "CGD2374_0_route",
            "no-hypermomentum theorem not promoted",
            "all clean routes require parent-signed variable/action/readout clauses that are not currently active",
            "retain P4 hypermomentum row as mandatory fallback",
            "P4_ROW_REQUIRED_NONCLAIM",
        ),
        (
            "CGD2374_1_best_next",
            "attack no-Gamma slot audit next",
            "absence of independent Gamma is stronger and cleaner than bounding arbitrary connection residues",
            "if it fails, P4 row declares required inputs",
            "SELECT_NO_GAMMA_AUDIT_NEXT",
        ),
        (
            "CGD2374_2_public_policy",
            "do not publish as GR reduction",
            "Levi-Civita/no-hypermomentum is conditional and P4 rows are not score-ready",
            "private derivation/fallback checkpoint only",
            "NO_GITHUB_EVIDENCE_UPDATE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, decision, reason, consequence, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2374_0_sources", "source paths and needles valid", "PASS", "audit reproducible"),
        ("CG2374_1_metric_only_route", "metric-only observed connection parent-signed", "FAIL", "Levi-Civita not kinematically derived"),
        ("CG2374_2_palatini_route", "Palatini EH plus no hypermomentum closes", "FAIL", "dynamic LC route not active"),
        ("CG2374_3_no_gamma_source_readout", "source/readout Gamma-slot exclusion signed", "FAIL", "connection may re-enter via protocols"),
        ("CG2374_4_P4_score", "P4 hypermomentum residual score-ready", "FAIL", "values/maps/units missing"),
        ("CG2374_5_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "connection gate still open"),
        ("CG2374_6_github_public_update", "safe to push as public evidence", "FAIL", "private connection-gate checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2374_0_import_GR_connection", "use Levi-Civita because GR uses it", "false", "LC must be parent-signed or residualized"),
        ("REF2374_1_spinor_shortcut", "ordinary spinors imply no independent torsion source automatically", "false", "coframe-owned spin connection must be explicit"),
        ("REF2374_2_projective_ignore", "projective trace is harmless without proof", "false", "projective mode must be gauge/fixed/unobservable in every local arena"),
        ("REF2374_3_P4_claim", "P4 fallback row is an empirical pass", "false", "P4 row is schema only; component values, units and weak-field maps are missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2374_0_selected",
            "2375-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md",
            "scripts/Y5_R2FR_noGamma_slot_matter_source_readout_audit_2375.py",
            "prove ordinary matter, source support, clocks, light, orbit and readout have no independent Gamma argument",
            "if any sector has a Gamma slot, route it to P4 hypermomentum component map and units",
        ),
        (
            "NEXT2374_1_fallback",
            "2375b-Y5-R2FR-first-P4-hypermomentum-component-map-and-units.md",
            "scripts/Y5_R2FR_first_P4_hypermomentum_component_map_and_units_2375b.py",
            "fill Delta components, K_hyper, unit normalization, weak-field projection and arena bounds",
            "keep all values nonclaim until source-backed and same-frame",
        ),
        (
            "NEXT2374_2_parallel",
            "2375c-Y5-R2FR-projective-trace-certificate-or-residual-policy.md",
            "scripts/Y5_R2FR_projective_trace_certificate_or_residual_policy_2375c.py",
            "prove projective trace is gauge/fixed/unobservable across source, clocks, lightcones, spin transport and orbit readout",
            "otherwise retain projective residual policy",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_SOURCE_REGISTER.csv",
        "proof_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
        "p4_residual": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
        "no_gamma_seed": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_NO_GAMMA_SLOT_AUDIT_SEED.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_CONNECTION_GATE_DECISION_LEDGER.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2374_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False
    proof = read_csv(outputs["proof_audit"])
    p4 = read_csv(outputs["p4_residual"])
    seed = read_csv(outputs["no_gamma_seed"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    checks = [
        ("VAL2374_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2374_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2374_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2374 output files written"),
        ("VAL2374_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2374_04_nohyper_not_promoted",
            any(row["row_id"] == "NHL2374_6_verdict" and row["status"].startswith("NOT_DERIVED") for row in proof),
            "no-hypermomentum/LC not promoted",
        ),
        (
            "VAL2374_05_p4_row_exists",
            any(row["row_id"] == "P4R2374_0_hypermomentum_total" and row["current_status"] == "MISSING_DELTA_COMPONENT_VALUES" for row in p4),
            "P4 hypermomentum total row exists",
        ),
        (
            "VAL2374_06_no_gamma_audit_seeded",
            any(row["row_id"] == "NGS2374_6_verdict" and row["status"] == "NOT_DERIVED_AUDIT_REQUIRED" for row in seed),
            "no-Gamma slot audit seeded",
        ),
        (
            "VAL2374_07_claim_gates_block",
            any(row["row_id"] == "CG2374_5_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2374_08_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2374_09_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
        (
            "VAL2374_10_next_selected",
            any(row["row_id"] == "NEXT2374_0_selected" and "noGamma_slot" in row["next_script"] for row in next_rows),
            "2375 no-Gamma slot audit selected",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2374_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2374 valid: no-hypermomentum/LC not promoted, P4 residual row retained, no-Gamma slot audit selected"
            if overall_ok
            else "2374 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    proof = read_csv(outputs["proof_audit"])
    p4 = read_csv(outputs["p4_residual"])
    seed = read_csv(outputs["no_gamma_seed"])
    decision = read_csv(outputs["decision_ledger"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]
    text = f"""# 2374 - noHypermomentum LeviCivita Source Connection Or P4 Row

## Result

The Levi-Civita/no-hypermomentum route remains the cleanest way to collapse the spin/torsion head, but it is not yet derived.

The desired theorem is:

`Gamma_obs = Gamma_LC[g_obs]` and `Delta_lambda^{{mu nu}} = delta S_ord / delta Gamma^lambda_{{mu nu}} = 0`.

This cannot be imported from GR.  It must follow from either a parent variable list with no independent `Gamma` argument in matter/source/readout sectors, or a Palatini/EH route plus no-hypermomentum and projective silence.

Because those clauses are still unsigned, the P4 fallback remains live:

`Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||`.

Next target: audit each local sector for an independent `Gamma` slot.  If every sector is no-Gamma, `Delta_lambda^{{mu nu}}=0` by absence of variable.  If any sector has a Gamma slot, it must be routed into P4 residuals.

## noHypermomentum / Levi-Civita Proof Audit

{md_table(proof, ["row_id", "route", "status", "obstruction"])}

## P4 Hypermomentum Residual Row

{md_table(p4, ["row_id", "channel", "residual_symbol", "current_status", "required_inputs"])}

## no-Gamma Slot Audit Seed

{md_table(seed, ["row_id", "sector", "status", "no_gamma_condition"])}

## Connection Gate Decision Ledger

{md_table(decision, ["row_id", "decision", "status", "consequence"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is another useful narrowing.  The connection problem is no longer just "does it reduce to GR"; it is now a sector-by-sector variable ownership audit.  Either Gamma is absent from ordinary/source/readout sectors, or P4 becomes a real residual branch.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["proof_audit"], proof_audit())
    write_csv(outputs["p4_residual"], p4_residual_row())
    write_csv(outputs["no_gamma_seed"], no_gamma_slot_audit_seed())
    write_csv(outputs["decision_ledger"], decision_ledger())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()
