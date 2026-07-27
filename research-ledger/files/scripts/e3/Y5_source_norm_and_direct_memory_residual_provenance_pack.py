from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1544_doc": ROOT / "1544-Y5-Cqm-zero-theorem-or-finite-provenance-runner.md",
    "1544_validation": OUT / "P8_Y5_BRR545_1544_VALIDATION.csv",
    "1544_provenance": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_FINITE_PROVENANCE_REQUIREMENTS.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "1543_inputs": OUT / "P8_Y5_PARENT_QLOC_1543_FINITE_INPUT_PROVENANCE_PACK.csv",
    "1543_arenas": OUT / "P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv",
    "1542_cqm": OUT / "P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv",
    "1539_inputs": OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv",
    "source_current": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1545_SOURCE_REGISTER.csv"
SOURCE_NORM_GATE = OUT / "P8_Y5_PARENT_QLOC_1545_TSOURCE_NORM_GATE.csv"
DIRECT_GATE = OUT / "P8_Y5_PARENT_QLOC_1545_DIRECT_MEMORY_RESIDUAL_GATE.csv"
SOURCE_EXTRA_GATE = OUT / "P8_Y5_PARENT_QLOC_1545_SOURCE_NORMALIZATION_EXTRA_GATE.csv"
BOUNDARY_GATE = OUT / "P8_Y5_PARENT_QLOC_1545_BOUNDARY_MEMORY_RESIDUAL_GATE.csv"
SCG_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_1545_SCG_ENVELOPE_STATUS_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1545_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1545_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1545_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1545_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1545"
QUAR_TSOURCE = QUARANTINE / "TSOURCE_NORM_GATE_NONCLAIM.csv"
QUAR_DIRECT = QUARANTINE / "DIRECT_MEMORY_RESIDUAL_GATE_NONCLAIM.csv"
QUAR_EXTRA = QUARANTINE / "SOURCE_NORMALIZATION_EXTRA_GATE_NONCLAIM.csv"
QUAR_BOUNDARY = QUARANTINE / "BOUNDARY_MEMORY_RESIDUAL_GATE_NONCLAIM.csv"
QUAR_SCG = QUARANTINE / "SCG_ENVELOPE_STATUS_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_TSOURCE = BRANCH_RESIDUALS / "Tsource_norm_gate_nonclaim_1545.csv"
BRANCH_DIRECT = BRANCH_RESIDUALS / "direct_memory_residual_gate_nonclaim_1545.csv"
BRANCH_EXTRA = BRANCH_RESIDUALS / "source_normalization_extra_gate_nonclaim_1545.csv"
BRANCH_BOUNDARY = BRANCH_RESIDUALS / "boundary_memory_residual_gate_nonclaim_1545.csv"
BRANCH_SCG = BRANCH_RESIDUALS / "Scg_envelope_status_nonclaim_1545.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "source_residual_decision_nonclaim_1545.csv"


def flags() -> dict[str, bool]:
    return {
        "theorem_zero_adopted": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1545_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for source norm and direct memory residual provenance gates",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def source_norm_rows() -> list[dict[str, Any]]:
    rows = [
        ("TS1545_0_definition", "T_source_norm", "T_source_norm=||delta S_matter/delta q||_source", "DEFINITION", "ordinary compact matter source norm; not expected to be zero"),
        ("TS1545_1_Hilbert_current", "Hilbert/Noether source current", "tau_a^mu=det(e)^-1 delta S_m/delta e_mu^a in same observed coframe", "CONDITIONAL_STANDARD_NOT_NUMERIC", "source-current definition exists but compact-body norm not sourced"),
        ("TS1545_2_compact_profile", "compact source/worldtube profile", "local worldtube/source profile and norm domain for the body used in R10/PPN/orbit tests", "MISSING_SOURCE_PROFILE", "needed before C_qm*T_source_norm can be evaluated"),
        ("TS1545_3_units", "units/norm", "source norm units and dual pairing must match S_cg_norm E* convention", "MISSING_UNITS_AND_NORM", "prevents hiding magnitude in normalization"),
        ("TS1545_4_verdict", "T_source_norm verdict", "not zero; not numeric; provenance required", "MISSING_PROVENANCE", "finite source norm remains a live input"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "item": item,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1543_inputs", "source_current", "source_measure_flux"),
            **flags(),
        }
        for row_id, item, statement, status, reason in rows
    ]


def direct_rows() -> list[dict[str, Any]]:
    rows = [
        ("DIR1545_0_definition", "S_direct_m", "S_direct_m=||(partial_m S_matter + partial_m S_source_norm)_q||_{E*}", "DEFINITION", "direct memory dependence not included in q pullback"),
        ("DIR1545_1_zero_route", "no-direct-memory action domain", "ordinary matter/source action excludes direct m, L_cg, Pi_B, support marker, or memory coefficient arguments", "UNSIGNED_ZERO_ROUTE", "would zero S_direct_m only if parent object language is signed"),
        ("DIR1545_2_counterroute", "direct coupling finite route", "if any direct memory/source argument remains, source a finite residual coefficient", "FINITE_ROUTE_REQUIRED_IF_UNSIGNED", "cannot be hidden inside C_qm or T_source_norm"),
        ("DIR1545_3_units", "units/source row", "finite S_direct_m needs units, source path, equation row, and derivation status", "MISSING_PROVENANCE", "placeholder direct residual is refused"),
        ("DIR1545_4_verdict", "S_direct_m verdict", "no-direct theorem not proved and finite value absent", "BLOCKED_NONCLAIM", "direct residual remains active"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "item": item,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1543_inputs", "1544_projection", "source_owner", "source_current"),
            **flags(),
        }
        for row_id, item, statement, status, reason in rows
    ]


def source_extra_rows() -> list[dict[str, Any]]:
    rows = [
        ("EXTRA1545_0_definition", "S_source_norm_extra", "extra memory leakage in source calibration beyond Hilbert q-pullback", "DEFINITION", "protects measured-GM/source normalization from hiding the coupling"),
        ("EXTRA1545_1_zero_route", "source-normalization descent", "G_eff, M_eff, Pi_M J_H, and calibration constants descend through q or are fixed constants", "UNSIGNED_ZERO_ROUTE", "source-normalization owner theorem is not parent-derived"),
        ("EXTRA1545_2_finite_route", "finite calibration residual", "retain partial_m S_source_norm beyond Hilbert q-pullback as a separate positive envelope term", "FINITE_ROUTE_REQUIRED_IF_UNSIGNED", "no cancellation against C_qm or direct terms"),
        ("EXTRA1545_3_verdict", "S_source_norm_extra verdict", "zero not proved and finite value absent", "BLOCKED_NONCLAIM", "source-calibration residual remains active"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "item": item,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1543_inputs", "source_normalization_owner", "source_measure_flux"),
            **flags(),
        }
        for row_id, item, statement, status, reason in rows
    ]


def boundary_rows() -> list[dict[str, Any]]:
    rows = [
        ("BND1545_0_definition", "S_boundary_m", "S_boundary_m <= C_inner |Q_m^H| + domain/support boundary terms", "DEFINITION", "compact-source boundary/domain leakage term"),
        ("BND1545_1_zero_route", "boundary/source silence", "Q_m^H=0, no-flux boundary, domain support silence, and zero-mode certificate all parent-signed", "UNSIGNED_ZERO_ROUTE", "1529/positive nohair show this is not automatic"),
        ("BND1545_2_finite_route", "finite boundary norm", "source C_inner, Q_m^H, domain/support terms, and boundary-dual norm", "FINITE_ROUTE_REQUIRED_IF_UNSIGNED", "finite boundary term must be absolute-valued"),
        ("BND1545_3_verdict", "S_boundary_m verdict", "boundary zero not proved and finite boundary norm absent", "BLOCKED_NONCLAIM", "boundary leakage remains active"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "item": item,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1543_inputs", "1539_inputs", "positive_nohair", "boundary_certificate"),
            **flags(),
        }
        for row_id, item, statement, status, reason in rows
    ]


def scg_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCG1545_0_formula", "S_cg_norm", "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m", "SCHEMA_READY", "no-cancellation envelope"),
        ("SCG1545_1_current_inputs", "all envelope inputs", "C_qm, T_source_norm, S_direct_m, S_source_norm_extra, S_boundary_m", "NOT_COMPUTABLE", "every finite input is missing or unsigned"),
        ("SCG1545_2_Npair", "N_pair insertion", "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|", "NOT_COMPUTABLE", "S_cg_norm and first-pair inputs missing"),
        ("SCG1545_3_local_claim", "local GR/Newton", "requires full N_lock and arena projections after source envelope closes", "BLOCKED_NO_CLAIM", "no local claim from source envelope"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1544_projection", "1543_arenas", "1542_cqm"),
            **flags(),
        }
        for row_id, quantity, formula, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1545_0_Tsource", "T_source_norm gate written", "PASS_NONCLAIM", "definition/provenance requirements explicit"),
        ("GATE1545_1_direct", "direct/source/boundary residual gates written", "PASS_NONCLAIM", "all residual terms have zero/finite routes"),
        ("GATE1545_2_Scg", "S_cg_norm computable", "BLOCKED", "envelope inputs missing"),
        ("GATE1545_3_R10_PPN", "R10/PPN/clock/orbital score", "BLOCKED", "S_cg/N_pair/N_lock/projections missing"),
        ("GATE1545_4_local_GR", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "source envelope remains nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1545_0_progress", "All non-C_qm source envelope terms now have provenance gates.", "SOURCE_RESIDUAL_GATES_WRITTEN", "the S_cg envelope cannot hide unsourced direct/source/boundary terms"),
        ("DEC1545_1_priority", "Prioritize T_source_norm worldtube normalization next.", "TSOURCE_FIRST", "T_source_norm is physically nonzero and needed for any finite C_qm product"),
        ("DEC1545_2_no_claim", "Keep local claims blocked.", "CLAIM_BLOCKED", "S_cg_norm is still not computable"),
        ("DEC1545_3_next", "Next target is compact source/worldtube normalization.", "NEXT_1546_TSOURCE_WORLDTUBE", "define the source norm, units, and profile before arena tests"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1545_0_1546",
            "next_target": "1546-Y5-Tsource-worldtube-normalization-or-source-profile-acquisition.md",
            "script": "scripts/Y5_Tsource_worldtube_normalization_or_source_profile_acquisition.py",
            "objective": "define or source T_source_norm with same-frame Hilbert/Noether current, compact-source/worldtube profile, units, norm, and local arena compatibility",
            "do_not": "do not import orbital GM as the source norm; do not use placeholder profiles; do not claim local GR or arena passes",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (SOURCE_NORM_GATE, QUAR_TSOURCE),
        (DIRECT_GATE, QUAR_DIRECT),
        (SOURCE_EXTRA_GATE, QUAR_EXTRA),
        (BOUNDARY_GATE, QUAR_BOUNDARY),
        (SCG_ENVELOPE, QUAR_SCG),
        (DECISION, QUAR_DECISION),
        (SOURCE_NORM_GATE, BRANCH_TSOURCE),
        (DIRECT_GATE, BRANCH_DIRECT),
        (SOURCE_EXTRA_GATE, BRANCH_EXTRA),
        (BOUNDARY_GATE, BRANCH_BOUNDARY),
        (SCG_ENVELOPE, BRANCH_SCG),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    tsource = read_csv(SOURCE_NORM_GATE)
    direct = read_csv(DIRECT_GATE)
    extra = read_csv(SOURCE_EXTRA_GATE)
    boundary = read_csv(BOUNDARY_GATE)
    scg = read_csv(SCG_ENVELOPE)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1545_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1545 source paths exist"),
        ("VAL1545_1_Tsource_gate", any(row["row_id"] == "TS1545_4_verdict" and row["current_status"] == "MISSING_PROVENANCE" for row in tsource), "T_source_norm provenance gate written"),
        ("VAL1545_2_direct_gate", any(row["row_id"] == "DIR1545_4_verdict" and row["current_status"] == "BLOCKED_NONCLAIM" for row in direct), "direct memory residual gate written"),
        ("VAL1545_3_extra_gate", any(row["row_id"] == "EXTRA1545_3_verdict" and row["current_status"] == "BLOCKED_NONCLAIM" for row in extra), "source-normalization extra gate written"),
        ("VAL1545_4_boundary_gate", any(row["row_id"] == "BND1545_3_verdict" and row["current_status"] == "BLOCKED_NONCLAIM" for row in boundary), "boundary memory residual gate written"),
        ("VAL1545_5_scg_not_computable", any(row["row_id"] == "SCG1545_1_current_inputs" and row["current_status"] == "NOT_COMPUTABLE" for row in scg), "S_cg envelope remains noncomputable"),
        ("VAL1545_6_claim_gates_block", any(row["gate_id"] == "GATE1545_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1545_7_decision_next", any(row["result"] == "NEXT_1546_TSOURCE_WORLDTUBE" for row in decisions), "decision selects T_source worldtube target next"),
        ("VAL1545_8_next_target", any("1546-Y5-Tsource" in row["next_target"] for row in next_rows), "next target is T_source worldtube normalization"),
        ("VAL1545_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1545 CSVs parse cleanly"),
        ("VAL1545_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1545_11_branch_copies", all(path.exists() for path in [QUAR_TSOURCE, QUAR_DIRECT, QUAR_EXTRA, QUAR_BOUNDARY, QUAR_SCG, QUAR_DECISION, BRANCH_TSOURCE, BRANCH_DIRECT, BRANCH_EXTRA, BRANCH_BOUNDARY, BRANCH_SCG, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1545_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1545_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1545_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1545 installs provenance gates for T_source_norm, direct memory, source-normalization extra, and boundary memory residuals, keeps S_cg noncomputable, and selects T_source worldtube normalization next"
            if overall
            else "1545 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    tsource: list[dict[str, Any]],
    direct: list[dict[str, Any]],
    extra: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    scg: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1545 - Source Norm and Direct Memory Residual Provenance Pack",
                "",
                "## Verdict",
                "- The full finite source envelope is now guarded term-by-term.",
                "- `T_source_norm` is explicitly not assumed zero; it needs same-frame Hilbert/Noether source current, compact worldtube profile, units, and norm.",
                "- `S_direct_m`, `S_source_norm_extra`, and `S_boundary_m` each have zero-theorem and finite-provenance routes, but none closes yet.",
                "- `S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m` remains schema-ready but noncomputable.",
                "- No local GR/Newton/PPN/R10/clock/orbital claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## T_source_norm Gate",
                md_table(tsource, ["row_id", "item", "statement", "current_status", "reason"]),
                "",
                "## Direct Memory Residual Gate",
                md_table(direct, ["row_id", "item", "statement", "current_status", "reason"]),
                "",
                "## Source-Normalization Extra Gate",
                md_table(extra, ["row_id", "item", "statement", "current_status", "reason"]),
                "",
                "## Boundary Memory Residual Gate",
                md_table(boundary, ["row_id", "item", "statement", "current_status", "reason"]),
                "",
                "## S_cg Envelope Status",
                md_table(scg, ["row_id", "quantity", "formula", "current_status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    tsource = source_norm_rows()
    direct = direct_rows()
    extra = source_extra_rows()
    boundary = boundary_rows()
    scg = scg_envelope_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SOURCE_NORM_GATE, tsource)
    write_csv(DIRECT_GATE, direct)
    write_csv(SOURCE_EXTRA_GATE, extra)
    write_csv(BOUNDARY_GATE, boundary)
    write_csv(SCG_ENVELOPE, scg)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        SOURCE_NORM_GATE,
        DIRECT_GATE,
        SOURCE_EXTRA_GATE,
        BOUNDARY_GATE,
        SCG_ENVELOPE,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, tsource, direct, extra, boundary, scg, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
