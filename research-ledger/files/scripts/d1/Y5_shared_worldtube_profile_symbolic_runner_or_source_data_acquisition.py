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
DOC = ROOT / "1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1547_doc": ROOT / "1547-Y5-compact-worldtube-profile-template-and-arena-map.md",
    "1547_validation": OUT / "P8_Y5_BRR545_1547_VALIDATION.csv",
    "1547_next": OUT / "P8_Y5_PARENT_QLOC_1547_NEXT_TARGET.csv",
    "1547_profile": OUT / "P8_Y5_PARENT_QLOC_1547_COMPACT_PROFILE_TEMPLATE.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "1547_arena": OUT / "P8_Y5_PARENT_QLOC_1547_ARENA_MAP_REQUIREMENTS.csv",
    "1547_guard": OUT / "P8_Y5_PARENT_QLOC_1547_NO_RETUNING_GUARD.csv",
    "1546_worldtube": OUT / "P8_Y5_PARENT_QLOC_1546_WORLDTUBE_REQUIREMENTS.csv",
    "1546_tsource_def": OUT / "P8_Y5_PARENT_QLOC_1546_TSOURCE_DEFINITION_CANDIDATES.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "source_current": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1548_SOURCE_REGISTER.csv"
SYMBOLIC_PROFILE = OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv"
DIMENSION_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1548_DIMENSION_AND_NORMALIZATION_CONTRACT.csv"
ACQUISITION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1548_SOURCE_ACQUISITION_LEDGER.csv"
ARENA_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1548_ARENA_SYMBOLIC_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1548_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1548_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1548_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1548_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1548"
QUAR_SYMBOLIC = QUARANTINE / "SHARED_SYMBOLIC_PROFILE_CANDIDATES_NONCLAIM.csv"
QUAR_DIMENSION = QUARANTINE / "DIMENSION_AND_NORMALIZATION_CONTRACT_NONCLAIM.csv"
QUAR_LEDGER = QUARANTINE / "SOURCE_ACQUISITION_LEDGER_NONCLAIM.csv"
QUAR_ARENA = QUARANTINE / "ARENA_SYMBOLIC_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_SYMBOLIC = BRANCH_RESIDUALS / "shared_symbolic_profile_candidates_nonclaim_1548.csv"
BRANCH_DIMENSION = BRANCH_RESIDUALS / "dimension_normalization_contract_nonclaim_1548.csv"
BRANCH_LEDGER = BRANCH_RESIDUALS / "source_acquisition_ledger_nonclaim_1548.csv"
BRANCH_ARENA = BRANCH_RESIDUALS / "arena_symbolic_runner_nonclaim_1548.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "profile_decision_nonclaim_1548.csv"


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
            "source_id": f"SRC1548_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for shared symbolic worldtube profile runner and source-data acquisition ledger",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def symbolic_profile_candidate_rows() -> list[dict[str, Any]]:
    candidate_rows = [
        {
            "candidate_id": "SYM1548_0_smooth_bump_profile",
            "profile_family": "smooth compact bump",
            "symbolic_profile": "J_q^A(x;theta_src)=T_q n_q^A b(s;R_src,epsilon_reg)/N_b",
            "support_rule": "b has compact support in W_src and vanishes smoothly on the matching boundary",
            "normalization_rule": "N_b chosen symbolically so ||J_q||_{source,W_src,E*}=T_source_norm",
            "unit_hook": "requires dim(q_loc), dim(delta S_matter/delta q), dV_e_obs, and E* dual norm",
            "arena_reuse_rule": "same theta_src={T_q,n_q^A,R_src,epsilon_reg,boundary_rule} feeds every Pi_arena",
            "current_status": "CONDITIONAL_SYMBOLIC_NOT_SOURCE_BACKED",
            "blocker": "parent action has not fixed J_q^A, units, source charge, or regulator",
            "source_paths": source_list("1547_profile", "1547_support", "1546_tsource_def", "source_current"),
        },
        {
            "candidate_id": "SYM1548_1_distributional_limit",
            "profile_family": "regulated distributional compact source",
            "symbolic_profile": "J_q^A -> Q_q n_q^A delta_W after epsilon_reg -> 0 with finite norm bound",
            "support_rule": "distribution is only legal as limit of a declared regulator inside W_src",
            "normalization_rule": "Q_q and regulator must reproduce T_source_norm without importing orbital GM",
            "unit_hook": "requires source charge units and regulator scaling from parent measure",
            "arena_reuse_rule": "same Q_q, n_q^A, and regulator law must be used in all arenas",
            "current_status": "CONDITIONAL_REQUIRES_REGULATOR_AND_PARENT_CHARGE",
            "blocker": "source-measure/flux theorem has not closed the charge identity",
            "source_paths": source_list("1547_profile", "1547_support", "source_measure_flux", "source_normalization_owner"),
        },
        {
            "candidate_id": "SYM1548_2_Hilbert_stress_projected_profile",
            "profile_family": "Hilbert stress projected source",
            "symbolic_profile": "J_q^A=P^A_{mu_nu}[q,e_obs] T^{mu_nu}[e_obs,psi]",
            "support_rule": "support inherited from matter stress/current inside W_src",
            "normalization_rule": "T_source_norm=||P*T||_{source,W_src,E*}",
            "unit_hook": "requires dim(P^A_{mu_nu}) and same-frame Hilbert current normalization",
            "arena_reuse_rule": "same projector P and W_src feed the arena response maps",
            "current_status": "MISSING_PARENT_COUPLING_PROJECTOR",
            "blocker": "parent action has not supplied the q-matter projector P^A_{mu_nu}",
            "source_paths": source_list("source_current", "source_owner", "1546_tsource_def", "1547_profile"),
        },
        {
            "candidate_id": "SYM1548_3_Noether_charge_profile",
            "profile_family": "Noether or Hamiltonian source charge profile",
            "symbolic_profile": "J_q^A derived from a conserved source charge density rho_Q^A on W_src",
            "support_rule": "charge density must be compactly supported or have declared boundary flux",
            "normalization_rule": "T_source_norm bounded by owned source charge only after flux closure",
            "unit_hook": "requires parent Noether current, charge units, and boundary term sign",
            "arena_reuse_rule": "same charge density and flux law must project to all arenas",
            "current_status": "MISSING_SOURCE_MEASURE_AND_FLUX_CLOSURE",
            "blocker": "current source-measure theorem is conditional, not parent-derived",
            "source_paths": source_list("source_measure_flux", "source_normalization_owner", "1547_support"),
        },
        {
            "candidate_id": "SYM1548_4_current_verdict",
            "profile_family": "shared profile verdict",
            "symbolic_profile": "a shared symbolic profile is routable, but no source-backed accepted profile exists",
            "support_rule": "template support exists only as a contract",
            "normalization_rule": "no numeric or sourced T_source_norm is admitted",
            "unit_hook": "unit closure is the next required parent-level target",
            "arena_reuse_rule": "no arena is allowed to tune theta_src independently",
            "current_status": "NOT_SCORE_READY",
            "blocker": "missing parent source variation, q dimension, regulator, and arena kernels",
            "source_paths": source_list("1547_profile", "1547_guard", "1547_arena"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID, "symbolic_profile_present": True}, **row, **flags()} for row in candidate_rows]


def dimension_contract_rows() -> list[dict[str, Any]]:
    contract_rows = [
        ("DIM1548_0_q_dimension", "dim(q_loc)", "field dimension of q_loc or parent q required before J_q units are meaningful", "MISSING_PARENT_FIELD_DIMENSION"),
        ("DIM1548_1_source_variation", "dim(delta S_matter/delta q)", "source current must come from a parent variation, not a fitted observable", "MISSING_PARENT_VARIATION"),
        ("DIM1548_2_observed_measure", "dV_e_obs", "worldtube measure must descend to the observed frame and be shared by readouts", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("DIM1548_3_dual_norm", "||J_q||_{source,W_src,E*}", "norm must be paired with the C_qm norm so the S_cg envelope has legal units", "MISSING_NORM_PAIRING"),
        ("DIM1548_4_cqm_pairing", "T_source_norm*C_qm", "1/2*T_source_norm*C_qm must have the same units as source-coupling forcing in S_cg_norm", "MISSING_UNIT_CLOSURE"),
        ("DIM1548_5_projection_units", "Pi_arena output units", "each arena projection must convert N_lock/N_pair into its observable residual units", "MISSING_ARENA_KERNEL_UNITS"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dimension_id": dimension_id,
            "symbol_or_object": symbol_or_object,
            "requirement": requirement,
            "current_status": current_status,
            "source_paths": source_list("1546_tsource_def", "1547_support", "source_current", "source_owner"),
            **flags(),
        }
        for dimension_id, symbol_or_object, requirement, current_status in contract_rows
    ]


def source_acquisition_ledger_rows() -> list[dict[str, Any]]:
    ledger_rows = [
        ("ACQ1548_0_parent_q", "parent q or q_loc definition", "field definition, dimension, and observed-frame descent", "MISSING_PARENT_FIELD_INPUT"),
        ("ACQ1548_1_parent_action", "matter action dependence", "explicit S_matter[q(Phi),Psi,theta] term or coupling projector", "MISSING_PARENT_ACTION_TERM"),
        ("ACQ1548_2_source_variation", "source current variation", "delta S_matter/delta q in the same frame as local readouts", "MISSING_PARENT_VARIATION"),
        ("ACQ1548_3_worldtube_profile", "compact source profile", "W_src support, shape family, material/source label, and normalization", "MISSING_SOURCE_PROFILE"),
        ("ACQ1548_4_regulator", "regularization/excision", "finite regulator or proof that distributional limit has bounded norm", "MISSING_REGULATOR"),
        ("ACQ1548_5_boundary_flux", "boundary leakage", "flux/boundary term sign or finite bound for partial worldtubes", "MISSING_BOUNDARY_INPUT"),
        ("ACQ1548_6_unit_pairing", "C_qm/T_source norm pairing", "dual norm convention and unit conversion into S_cg_norm", "MISSING_UNIT_PAIRING"),
        ("ACQ1548_7_arena_kernels", "arena projection kernels", "Pi_R10, Pi_PPN, Pi_clock, Pi_orbital, and Pi_local maps from same profile", "MISSING_ARENA_PROJECTIONS"),
        ("ACQ1548_8_no_retuning_audit", "shared-profile audit", "evidence that theta_src is fixed before arena fits", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "needed_input": needed_input,
            "acceptance_requirement": acceptance_requirement,
            "current_status": current_status,
            "source_paths": source_list("1547_profile", "1547_support", "1547_guard", "source_owner"),
            **flags(),
        }
        for acquisition_id, needed_input, acceptance_requirement, current_status in ledger_rows
    ]


def arena_symbolic_runner_rows() -> list[dict[str, Any]]:
    runner_rows = [
        (
            "ARUN1548_0_R10",
            "R10",
            "smooth/shared symbolic W_src can be routed into Pi_R10(lambda) only after source/test geometry and projection kernel exist",
            "FORMALLY_ROUTABLE_NOT_SCORABLE",
            "missing Pi_R10(lambda;W_src), material profile, and valid claim-grade bound curve use",
        ),
        (
            "ARUN1548_1_PPN",
            "PPN",
            "shared W_src can be routed into weak-field response only after gauge-fixed source multipoles and metric map exist",
            "FORMALLY_ROUTABLE_NOT_SCORABLE",
            "missing Pi_PPN response matrix and parent Kmetric conversion",
        ),
        (
            "ARUN1548_2_clock",
            "clock",
            "shared W_src can be routed into clock residuals only after readout sensitivity and calibration split exist",
            "FORMALLY_ROUTABLE_NOT_SCORABLE",
            "missing Pi_clock and no-shadow-clock-frame proof",
        ),
        (
            "ARUN1548_3_orbital",
            "orbital",
            "shared W_src can be compared to orbital readouts only after source norm is independently derived",
            "FORMALLY_ROUTABLE_NOT_SCORABLE",
            "orbital GM remains forbidden as source input; source measure/flux closure missing",
        ),
        (
            "ARUN1548_4_local_GR",
            "local_GR",
            "shared W_src can enter local residual vector only after S_cg_norm and N_lock inputs close",
            "BLOCKED_NO_CLAIM",
            "missing source profile units, C_qm, boundary/direct residuals, and Pi_local",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "arena": arena,
            "symbolic_run_result": symbolic_run_result,
            "current_status": current_status,
            "blocker": blocker,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            "source_paths": source_list("1547_arena", "1547_profile", "1544_projection", "local_bound_claims"),
            **flags(),
        }
        for runner_id, arena, symbolic_run_result, current_status, blocker in runner_rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gate_rows = [
        ("GATE1548_0_symbolic_profile", "shared symbolic profile candidates written", "PASS_NONCLAIM", "several legal symbolic families are recorded"),
        ("GATE1548_1_acquisition_ledger", "source acquisition ledger written", "PASS_NONCLAIM", "missing parent inputs are now itemized"),
        ("GATE1548_2_no_retuning", "no per-arena retuning", "PASS_GUARD", "theta_src remains shared across arenas"),
        ("GATE1548_3_numeric_profile", "numeric/source-backed profile", "BLOCKED", "no parent-sourced W_src/J_q profile exists"),
        ("GATE1548_4_unit_closure", "unit/dimension closure", "BLOCKED", "dim(q_loc), delta S/delta q, norm pairing, and arena units remain missing"),
        ("GATE1548_5_arena_scores", "arena score readiness", "BLOCKED_NO_CLAIM", "symbolic routing is not scoring"),
        ("GATE1548_6_local_GR", "local GR/Newton reduction claim", "BLOCKED_NO_CLAIM", "source profile and local residual vector are not closed"),
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
        for gate_id, claim, status, reason in gate_rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    decision_items = [
        ("DEC1548_0_profile_attempt", "A shared symbolic profile can be written without retuning arenas.", "SYMBOLIC_ROUTE_EXISTS", "the branch is not nonsense structurally; it has a clean formal slot"),
        ("DEC1548_1_no_claim", "The symbolic profile is not yet evidence.", "SOURCE_AND_UNIT_CLOSURE_MISSING", "it lacks parent variation, field dimension, regulator, and sourced normalization"),
        ("DEC1548_2_best_next", "The best next target is parent source-current unit/dimension closure.", "NEXT_1549_PARENT_SOURCE_UNITS", "before R10/PPN/clock/orbit, derive what J_q and T_source_norm actually are"),
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
        for decision_id, decision, result, rationale in decision_items
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1548_0_1549",
            "next_target": "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
            "script": "scripts/Y5_Jq_unit_dimension_and_parent_source_variation_closure.py",
            "objective": "derive the source current units from the parent matter variation and q_loc dimension, then bind T_source_norm to the C_qm norm pairing or record the exact missing parent input",
            "do_not": "do not assign units by convenience; do not import orbital, PPN, clock, or R10 data as source normalization; do not claim local tests",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (SYMBOLIC_PROFILE, QUAR_SYMBOLIC),
        (DIMENSION_CONTRACT, QUAR_DIMENSION),
        (ACQUISITION_LEDGER, QUAR_LEDGER),
        (ARENA_RUNNER, QUAR_ARENA),
        (DECISION, QUAR_DECISION),
        (SYMBOLIC_PROFILE, BRANCH_SYMBOLIC),
        (DIMENSION_CONTRACT, BRANCH_DIMENSION),
        (ACQUISITION_LEDGER, BRANCH_LEDGER),
        (ARENA_RUNNER, BRANCH_ARENA),
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
    symbolic_rows = read_csv(SYMBOLIC_PROFILE)
    dimension_rows = read_csv(DIMENSION_CONTRACT)
    ledger_rows = read_csv(ACQUISITION_LEDGER)
    arena_rows = read_csv(ARENA_RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_arenas = {"R10", "PPN", "clock", "orbital", "local_GR"}
    arena_names = {row["arena"] for row in arena_rows}
    checks = [
        ("VAL1548_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1548 source paths exist"),
        ("VAL1548_1_symbolic_candidates", len(symbolic_rows) >= 5 and any(row["candidate_id"] == "SYM1548_0_smooth_bump_profile" for row in symbolic_rows), "shared symbolic profile candidates written"),
        ("VAL1548_2_no_candidate_scored", all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in symbolic_rows), "no symbolic candidate is score-ready or claim-valid"),
        ("VAL1548_3_dimension_contract", any(row["dimension_id"] == "DIM1548_0_q_dimension" and row["current_status"] == "MISSING_PARENT_FIELD_DIMENSION" for row in dimension_rows) and any(row["dimension_id"] == "DIM1548_4_cqm_pairing" for row in dimension_rows), "dimension and C_qm pairing blockers recorded"),
        ("VAL1548_4_acquisition_ledger", len(ledger_rows) >= 9 and any(row["acquisition_id"] == "ACQ1548_8_no_retuning_audit" for row in ledger_rows), "source acquisition ledger written"),
        ("VAL1548_5_arena_runner", required_arenas.issubset(arena_names) and all(row["accepted_for_scoring"] == "False" for row in arena_rows), "symbolic arena runner covers all local arenas without scoring"),
        ("VAL1548_6_claim_gates_block", any(row["gate_id"] == "GATE1548_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "local GR claim remains blocked"),
        ("VAL1548_7_decision_next", any(row["result"] == "NEXT_1549_PARENT_SOURCE_UNITS" for row in decision_items), "decision selects parent source-current unit/dimension closure next"),
        ("VAL1548_8_next_target", any("1549-Y5-Jq-unit-dimension" in row["next_target"] for row in next_rows), "next target is J_q unit/dimension and parent source variation closure"),
        ("VAL1548_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1548 CSVs parse cleanly"),
        ("VAL1548_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1548_11_branch_copies", all(path.exists() for path in [QUAR_SYMBOLIC, QUAR_DIMENSION, QUAR_LEDGER, QUAR_ARENA, QUAR_DECISION, BRANCH_SYMBOLIC, BRANCH_DIMENSION, BRANCH_LEDGER, BRANCH_ARENA, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1548_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1548_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1548_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1548 constructs a shared symbolic worldtube profile route, records exact missing source/current/unit inputs, and keeps all arena/local claims blocked"
            if overall
            else "1548 validation failed; inspect failed rows before continuing",
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
    symbolic_rows: list[dict[str, Any]],
    dimension_rows: list[dict[str, Any]],
    ledger_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1548 - Shared Worldtube Profile Symbolic Runner or Source Data Acquisition",
                "",
                "## Verdict",
                "- A shared symbolic worldtube profile route can be written cleanly without retuning R10, PPN, clock, orbital, or local-GR arenas.",
                "- This is structural progress, not evidence: no parent-sourced `J_q`, `q_loc` dimension, regulator, unit pairing, or arena kernel is closed.",
                "- The smooth compact bump, regulated distributional, Hilbert-projector, and Noether-charge routes are all conditional and nonclaim.",
                "- The next bottleneck is now sharper: derive `J_q := delta S_matter/delta q` and its units from the parent action, or explicitly close the route as a missing-input closure.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Shared Symbolic Profile Candidates",
                md_table(symbolic_rows, ["candidate_id", "profile_family", "symbolic_profile", "normalization_rule", "current_status", "blocker"]),
                "",
                "## Dimension and Normalization Contract",
                md_table(dimension_rows, ["dimension_id", "symbol_or_object", "requirement", "current_status"]),
                "",
                "## Source Acquisition Ledger",
                md_table(ledger_rows, ["acquisition_id", "needed_input", "acceptance_requirement", "current_status"]),
                "",
                "## Arena Symbolic Runner",
                md_table(arena_rows, ["runner_id", "arena", "symbolic_run_result", "current_status", "blocker"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "rationale"]),
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
    symbolic_rows = symbolic_profile_candidate_rows()
    dimension_rows = dimension_contract_rows()
    ledger_rows = source_acquisition_ledger_rows()
    arena_rows = arena_symbolic_runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SYMBOLIC_PROFILE, symbolic_rows)
    write_csv(DIMENSION_CONTRACT, dimension_rows)
    write_csv(ACQUISITION_LEDGER, ledger_rows)
    write_csv(ARENA_RUNNER, arena_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        SYMBOLIC_PROFILE,
        DIMENSION_CONTRACT,
        ACQUISITION_LEDGER,
        ARENA_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, symbolic_rows, dimension_rows, ledger_rows, arena_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
