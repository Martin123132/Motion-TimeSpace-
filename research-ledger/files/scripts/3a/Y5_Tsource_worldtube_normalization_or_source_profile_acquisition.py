from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1546-Y5-Tsource-worldtube-normalization-or-source-profile-acquisition.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1545_doc": ROOT / "1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md",
    "1545_validation": OUT / "P8_Y5_BRR545_1545_VALIDATION.csv",
    "1545_tsource": OUT / "P8_Y5_PARENT_QLOC_1545_TSOURCE_NORM_GATE.csv",
    "1545_scg": OUT / "P8_Y5_PARENT_QLOC_1545_SCG_ENVELOPE_STATUS_NONCLAIM.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "1543_arenas": OUT / "P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv",
    "source_current": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1546_SOURCE_REGISTER.csv"
WORLDTUBE_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1546_WORLDTUBE_REQUIREMENTS.csv"
TSOURCE_DEFINITION = OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_DEFINITION_CANDIDATES.csv"
PROVENANCE_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_PROVENANCE_RUNNER_NONCLAIM.csv"
ARENA_COMPATIBILITY = OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_ARENA_COMPATIBILITY.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1546_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1546_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1546_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1546_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1546"
QUAR_WORLD = QUARANTINE / "WORLDTUBE_REQUIREMENTS_NONCLAIM.csv"
QUAR_DEF = QUARANTINE / "TSOURCE_DEFINITION_CANDIDATES_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "TSOURCE_PROVENANCE_RUNNER_NONCLAIM.csv"
QUAR_ARENA = QUARANTINE / "TSOURCE_ARENA_COMPATIBILITY_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_WORLD = BRANCH_RESIDUALS / "Tsource_worldtube_requirements_nonclaim_1546.csv"
BRANCH_DEF = BRANCH_RESIDUALS / "Tsource_definition_candidates_nonclaim_1546.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "Tsource_provenance_runner_nonclaim_1546.csv"
BRANCH_ARENA = BRANCH_RESIDUALS / "Tsource_arena_compatibility_nonclaim_1546.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "Tsource_decision_nonclaim_1546.csv"


def flags() -> dict[str, bool]:
    return {
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
            "source_id": f"SRC1546_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for T_source_norm worldtube/source-profile normalization",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def worldtube_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WT1546_0_same_frame",
            "same observed frame",
            "source current, compact worldtube, clocks, photons, and orbital/readout maps must use the same e_obs/q_loc frame",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "SC0 and source-normalization owner rows remain conditional",
        ),
        (
            "WT1546_1_source_current",
            "Hilbert/Noether current",
            "tau_a^mu or T^{mu nu} is defined by variation of S_matter in the observed coframe before readout/scoring",
            "CONDITIONAL_DEFINITION_ONLY",
            "definition exists but not converted into compact source norm",
        ),
        (
            "WT1546_2_worldtube_domain",
            "compact worldtube W",
            "W must include support, boundary/excision convention, source profile, and exterior matching domain",
            "MISSING_WORLDTUBE_PROFILE",
            "no compact profile is source-backed here",
        ),
        (
            "WT1546_3_no_orbital_GM_import",
            "no orbital GM import",
            "T_source_norm cannot be set equal to fitted orbital GM or Kepler mass readout",
            "REJECTED_SHORTCUT",
            "orbital GM is an arena output/calibration target, not the source-side norm input",
        ),
        (
            "WT1546_4_norm_pairing",
            "local dual norm",
            "T_source_norm must be paired with C_qm so 1/2*T_source_norm*C_qm has E* forcing units",
            "MISSING_NORM_AND_UNITS",
            "cannot score until units and dual pairing are declared",
        ),
        (
            "WT1546_5_arena_compatibility",
            "arena compatibility",
            "one source profile must feed R10, PPN, clock, and orbital projections without retuning per arena",
            "MISSING_ARENA_PROFILE_MAP",
            "projection rows exist but profile-to-arena map is missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "requirement": requirement,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1545_tsource", "source_current", "source_measure_flux", "source_normalization_owner"),
            **flags(),
        }
        for requirement_id, requirement, statement, status, reason in rows
    ]


def tsource_definition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TDEF1546_0_abstract_norm",
            "abstract source-dual norm",
            "T_source_norm := ||delta S_matter/delta q||_{source,W}",
            "DEFINITION_CANDIDATE",
            "cleanest theory-side definition, but requires q/source norm and W profile",
        ),
        (
            "TDEF1546_1_Hilbert_worldtube",
            "Hilbert-current worldtube norm",
            "T_source_norm := ||T^{mu nu}[e_obs,psi]||_{W,E*} or equivalent tau_a^mu norm",
            "CONDITIONAL_CANDIDATE",
            "requires same-frame Hilbert current and compact-body profile",
        ),
        (
            "TDEF1546_2_Noether_charge",
            "Noether/Hamiltonian charge norm",
            "T_source_norm may be bounded by an owned source charge only if source measure and flux closure are parent-derived",
            "CONDITIONAL_NOT_CURRENTLY_AVAILABLE",
            "source-measure theorem says charge identity is not parent-derived",
        ),
        (
            "TDEF1546_3_orbital_GM",
            "orbital GM import",
            "T_source_norm := GM_orbit or fitted Kepler mass",
            "REJECTED",
            "would smuggle the Newtonian readout into the source-side proof",
        ),
        (
            "TDEF1546_4_current_verdict",
            "T_source_norm verdict",
            "definition candidates exist, but no numeric/source-backed T_source_norm is available",
            "NOT_SCORE_READY",
            "needs worldtube profile, units, norm, and source path",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "definition_id": definition_id,
            "candidate": candidate,
            "formula": formula,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1545_tsource", "source_current", "source_measure_flux"),
            **flags(),
        }
        for definition_id, candidate, formula, status, reason in rows
    ]


def provenance_runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TPR1546_0_source_current",
            "source_current_definition",
            "CONDITIONAL_AVAILABLE",
            "Hilbert/Noether current definition exists conditionally, but parent same-frame source theorem is unsigned",
        ),
        (
            "TPR1546_1_worldtube_profile",
            "compact_worldtube_profile",
            "MISSING",
            "no compact profile/support/domain/excision convention is sourced",
        ),
        (
            "TPR1546_2_units",
            "units_and_dual_norm",
            "MISSING",
            "T_source_norm units and pairing with C_qm are not declared",
        ),
        (
            "TPR1546_3_no_orbital_import",
            "no_orbital_GM_import",
            "PASS_GUARD",
            "orbital GM import is explicitly rejected",
        ),
        (
            "TPR1546_4_arena_map",
            "arena_profile_map",
            "MISSING",
            "R10/PPN/clock/orbit compatibility maps are not sourced",
        ),
        (
            "TPR1546_5_score_status",
            "T_source_norm_score",
            "REFUSED_NOT_SCORE_READY",
            "missing profile, units, norm, source path, and arena map",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, check, status, reason in rows
    ]


def arena_compatibility_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TARENA1546_0_R10",
            "R10",
            "source/test body convention, lambda profile, material/source profile, and T_source_norm norm must be mapped into Pi_R10",
            "MISSING_R10_PROFILE_MAP",
        ),
        (
            "TARENA1546_1_PPN",
            "PPN",
            "worldtube stress/current must map into weak-field source variables and PPN gauge response",
            "MISSING_PPN_PROFILE_MAP",
        ),
        (
            "TARENA1546_2_clock",
            "clock",
            "same source profile must coexist with clock/readout sensitivity and calibration convention",
            "MISSING_CLOCK_PROFILE_MAP",
        ),
        (
            "TARENA1546_3_orbital",
            "orbital",
            "orbital readout may compare against source norm but cannot define it",
            "MISSING_ORBITAL_PROFILE_MAP",
        ),
        (
            "TARENA1546_4_local_GR",
            "local GR",
            "source profile must enter N_lock/Kmetric projection without absorbing residuals into GM calibration",
            "BLOCKED_NO_CLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "compatibility_requirement": requirement,
            "current_status": status,
            "source_paths": source_list("1543_arenas", "1544_projection", "local_bound_claims"),
            **flags(),
        }
        for arena_id, arena, requirement, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1546_0_requirements", "worldtube requirements written", "PASS_NONCLAIM", "same-frame, current, profile, units, no-orbital-import, and arena map requirements are explicit"),
        ("GATE1546_1_definition", "T_source_norm definition candidate", "PASS_NONCLAIM", "definition candidates written but not score-ready"),
        ("GATE1546_2_no_orbital_import", "orbital GM import rejected", "PASS_GUARD", "source norm cannot be imported from orbital readout"),
        ("GATE1546_3_Tsource_score", "T_source_norm score-ready", "BLOCKED", "profile, units, norm, source path, and arena map missing"),
        ("GATE1546_4_Scg_score", "S_cg_norm computable", "BLOCKED", "T_source_norm and other envelope terms missing"),
        ("GATE1546_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "source/worldtube normalization remains nonclaim"),
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
        ("DEC1546_0_progress", "T_source_norm is now a legal worldtube/source-profile problem.", "WORLDTUBE_GATE_WRITTEN", "source strength cannot be a fitted orbital readout"),
        ("DEC1546_1_no_score", "Do not score T_source_norm yet.", "PROFILE_AND_UNITS_MISSING", "no source-backed compact profile or norm exists"),
        ("DEC1546_2_no_claim", "Keep local claims blocked.", "CLAIM_BLOCKED", "S_cg remains noncomputable"),
        ("DEC1546_3_next", "Next target is the compact profile template/acquisition pack.", "NEXT_1547_WORLD_PROFILE", "make profile rows fillable for R10/PPN/clock/orbit without retuning per arena"),
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
            "next_id": "NEXT1546_0_1547",
            "next_target": "1547-Y5-compact-worldtube-profile-template-and-arena-map.md",
            "script": "scripts/Y5_compact_worldtube_profile_template_and_arena_map.py",
            "objective": "create fillable compact-worldtube/source-profile rows for R10, PPN, clock, and orbital projections with units, support/domain conventions, and no per-arena retuning",
            "do_not": "do not use placeholder numeric profiles; do not import orbital GM as source norm; do not claim local GR or arena passes",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (WORLDTUBE_REQUIREMENTS, QUAR_WORLD),
        (TSOURCE_DEFINITION, QUAR_DEF),
        (PROVENANCE_RUNNER, QUAR_RUNNER),
        (ARENA_COMPATIBILITY, QUAR_ARENA),
        (DECISION, QUAR_DECISION),
        (WORLDTUBE_REQUIREMENTS, BRANCH_WORLD),
        (TSOURCE_DEFINITION, BRANCH_DEF),
        (PROVENANCE_RUNNER, BRANCH_RUNNER),
        (ARENA_COMPATIBILITY, BRANCH_ARENA),
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
    worldtube = read_csv(WORLDTUBE_REQUIREMENTS)
    definitions = read_csv(TSOURCE_DEFINITION)
    runner = read_csv(PROVENANCE_RUNNER)
    arenas = read_csv(ARENA_COMPATIBILITY)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_worldtube = {
        "same observed frame",
        "Hilbert/Noether current",
        "compact worldtube W",
        "no orbital GM import",
        "local dual norm",
        "arena compatibility",
    }
    worldtube_names = {row["requirement"] for row in worldtube}
    checks = [
        ("VAL1546_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1546 source paths exist"),
        ("VAL1546_1_worldtube_requirements", required_worldtube.issubset(worldtube_names), "all worldtube/source-profile requirements written"),
        ("VAL1546_2_orbital_import_rejected", any(row["requirement_id"] == "WT1546_3_no_orbital_GM_import" and row["current_status"] == "REJECTED_SHORTCUT" for row in worldtube), "orbital GM import rejected"),
        ("VAL1546_3_definition_candidates", any(row["definition_id"] == "TDEF1546_4_current_verdict" and row["current_status"] == "NOT_SCORE_READY" for row in definitions), "definition candidates remain nonclaim/not score-ready"),
        ("VAL1546_4_runner_refuses_score", any(row["runner_id"] == "TPR1546_5_score_status" and row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in runner), "T_source_norm runner refuses scoring"),
        ("VAL1546_5_arena_maps", len(arenas) >= 5 and any(row["current_status"] == "BLOCKED_NO_CLAIM" for row in arenas), "arena compatibility rows written"),
        ("VAL1546_6_claim_gates_block", any(row["gate_id"] == "GATE1546_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1546_7_decision_next", any(row["result"] == "NEXT_1547_WORLD_PROFILE" for row in decisions), "decision selects compact worldtube profile template next"),
        ("VAL1546_8_next_target", any("1547-Y5-compact-worldtube-profile" in row["next_target"] for row in next_rows), "next target is compact worldtube profile template and arena map"),
        ("VAL1546_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1546 CSVs parse cleanly"),
        ("VAL1546_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1546_11_branch_copies", all(path.exists() for path in [QUAR_WORLD, QUAR_DEF, QUAR_RUNNER, QUAR_ARENA, QUAR_DECISION, BRANCH_WORLD, BRANCH_DEF, BRANCH_RUNNER, BRANCH_ARENA, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1546_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1546_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1546_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1546 defines the legal T_source_norm worldtube/source-profile requirements, rejects orbital GM import, keeps T_source non-score-ready, and selects compact profile template next"
            if overall
            else "1546 validation failed; inspect failed rows before continuing",
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
    worldtube: list[dict[str, Any]],
    definitions: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1546 - T_source Worldtube Normalization or Source Profile Acquisition",
                "",
                "## Verdict",
                "- `T_source_norm` is now defined as a legal source/worldtube normalization problem, not a fitted orbital-GM input.",
                "- The clean candidate is `T_source_norm := ||delta S_matter/delta q||_{source,W}` or an equivalent same-frame Hilbert/Noether worldtube norm.",
                "- Orbital `GM` import is explicitly rejected because it would smuggle the Newtonian readout into the source-side proof.",
                "- No numeric/source-backed compact profile, units, dual norm, or arena profile map exists yet.",
                "- No local GR/Newton/PPN/R10/clock/orbital claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Worldtube Requirements",
                md_table(worldtube, ["requirement_id", "requirement", "statement", "current_status", "reason"]),
                "",
                "## T_source Definition Candidates",
                md_table(definitions, ["definition_id", "candidate", "formula", "current_status", "reason"]),
                "",
                "## Provenance Runner",
                md_table(runner, ["runner_id", "check", "current_status", "reason"]),
                "",
                "## Arena Compatibility",
                md_table(arenas, ["arena_id", "arena", "compatibility_requirement", "current_status"]),
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
    worldtube = worldtube_rows()
    definitions = tsource_definition_rows()
    runner = provenance_runner_rows()
    arenas = arena_compatibility_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(WORLDTUBE_REQUIREMENTS, worldtube)
    write_csv(TSOURCE_DEFINITION, definitions)
    write_csv(PROVENANCE_RUNNER, runner)
    write_csv(ARENA_COMPATIBILITY, arenas)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        WORLDTUBE_REQUIREMENTS,
        TSOURCE_DEFINITION,
        PROVENANCE_RUNNER,
        ARENA_COMPATIBILITY,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, worldtube, definitions, runner, arenas, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
