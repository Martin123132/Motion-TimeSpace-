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
DOC = ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1541_doc": ROOT / "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md",
    "1541_validation": OUT / "P8_Y5_BRR545_1541_VALIDATION.csv",
    "1541_qmap": OUT / "P8_Y5_PARENT_QLOC_1541_QMAP_CANDIDATE_LEDGER.csv",
    "1541_vgen": OUT / "P8_Y5_PARENT_QLOC_1541_VERTICAL_GENERATOR_AUDIT.csv",
    "1541_kernel": OUT / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv",
    "1541_coupling": OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv",
    "1540_chain": OUT / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv",
    "1539_inputs": OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1045_doc": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
    "1029_doc": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "1030_doc": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1542_SOURCE_REGISTER.csv"
Q_DEFINITION_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1542_Q_DEFINITION_AUDIT.csv"
VM_DEFINITION_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1542_VM_DEFINITION_AUDIT.csv"
FORK_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1542_FORK_DECISION_MATRIX.csv"
CQM_SOURCE_PACK = OUT / "P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv"
SCG_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1542_SCG_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1542_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1542_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1542_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1542_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1542"
QUAR_QDEF = QUARANTINE / "Q_DEFINITION_AUDIT_NONCLAIM.csv"
QUAR_VMDEF = QUARANTINE / "VM_DEFINITION_AUDIT_NONCLAIM.csv"
QUAR_FORK = QUARANTINE / "FORK_DECISION_MATRIX_NONCLAIM.csv"
QUAR_CQM = QUARANTINE / "CQM_SOURCE_PACK_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "SCG_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_QDEF = BRANCH_RESIDUALS / "q_definition_audit_nonclaim_1542.csv"
BRANCH_VMDEF = BRANCH_RESIDUALS / "vm_definition_audit_nonclaim_1542.csv"
BRANCH_FORK = BRANCH_RESIDUALS / "q_or_Cqm_fork_decision_nonclaim_1542.csv"
BRANCH_CQM = BRANCH_RESIDUALS / "Cqm_source_pack_nonclaim_1542.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "Scg_runner_nonclaim_1542.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "q_definition_or_Cqm_decision_nonclaim_1542.csv"


def flags() -> dict[str, bool]:
    return {
        "kernel_proved": False,
        "finite_value_present": False,
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
        "kernel_proved",
        "finite_value_present",
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
            "source_id": f"SRC1542_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for q-definition or Dq[v_m] finite coupling source pack",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def q_definition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QDEF1542_0_pretest_rule",
            "pre-test parent quotient rule",
            "q_loc must be declared from the parent field domain, equivalence relation, observed functor, source/readout functors, and boundary data before local tests are scored.",
            "LEGAL_REQUIREMENT",
            "prevents defining q by deleting whichever coupling failed",
            "parent field domain; equivalence relation; observed functor; source/readout functor; boundary class",
        ),
        (
            "QDEF1542_1_minimal_visible_candidate",
            "minimal visible quotient candidate",
            "q_loc(Phi)=(e_obs,g_obs,omega_obs,theta_vis,Pi_M J_H,calibration constants,allowed topological classes)",
            "CANDIDATE_ONLY",
            "would make memory/cg invisible only if m,L_cg,Pi_B and boundary charge are not in these visible objects",
            "proof memory/cg does not change e_obs, theta_vis, Pi_M J_H, calibration, or boundary class",
        ),
        (
            "QDEF1542_2_illegal_deletion",
            "illegal q definition",
            "q_loc := all parent data except the variables that produce local fifth-force/source residuals",
            "REJECTED",
            "this is post-hoc quotient surgery, not a derivation",
            "replace with parent equivalence relation or finite residual rows",
        ),
        (
            "QDEF1542_3_memory_membership_test",
            "memory/cg membership test",
            "Dq[v_m]=0 requires delta_v of every q_loc component to vanish, including source normalization and readout calibration.",
            "FAIL_CURRENT_EVIDENCE",
            "1541 found membership undecided and no field-by-field v_m action",
            "field-by-field derivative of q_loc along v_m",
        ),
        (
            "QDEF1542_4_q_verdict",
            "q definition verdict",
            "current corpus has conditional q contracts but no parent-signed q_loc/v_m definition strong enough to prove Dq[v_m]=0.",
            "EXACT_KERNEL_NOT_AVAILABLE",
            "must keep finite C_qm branch alive",
            "future parent action may reopen this",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "qdef_id": row_id,
            "audit_item": item,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "missing_to_promote": missing,
            "source_paths": source_list("1541_qmap", "1541_kernel", "1023_doc", "1045_doc", "1030_doc"),
            **flags(),
        }
        for row_id, item, statement, status, reason, missing in rows
    ]


def vm_definition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VMDEF1542_0_required_vector",
            "field-by-field v_m",
            "v_m must specify variations of m, L_cg, Pi_B, e_obs/q components, source normalization, matter lift, domain, and boundary data.",
            "REQUIRED_NOT_AVAILABLE",
            "without this, Dq[v_m] is not a calculable object",
        ),
        (
            "VMDEF1542_1_clean_kernel_vector",
            "clean kernel option",
            "delta_v m != 0 while delta_v q_loc=0, delta_v source/readout=0, and delta_v boundary charge=0.",
            "UNSIGNED_OPTION",
            "would prove source silence if a parent symmetry/null direction supplies it",
        ),
        (
            "VMDEF1542_2_physical_memory_vector",
            "physical coupling option",
            "delta_v m induces delta_v e_obs, source calibration, direct matter/source terms, domain/support motion, or boundary memory charge.",
            "FINITE_BRANCH_ACTIVE",
            "then the theory must score or bound C_qm/S_cg_norm instead of claiming zero",
        ),
        (
            "VMDEF1542_3_vm_verdict",
            "v_m definition verdict",
            "current v_m is a named direction, not a parent-owned null/gauge generator with a closed algebra and boundary action.",
            "KERNEL_NOT_PROVED",
            "finite branch is mandatory unless a future parent action supplies the vector",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "vmdef_id": row_id,
            "audit_item": item,
            "statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1541_vgen", "1540_chain", "source_owner", "boundary_certificate"),
            **flags(),
        }
        for row_id, item, statement, status, reason in rows
    ]


def fork_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FORK1542_0_exact_kernel",
            "exact source-silence route",
            "Dq[v_m]=0, direct_m S=0, source-normalization descent, and Q_m^H=0",
            "FAIL_CURRENT_EVIDENCE",
            "would give S_cg_norm=0 and Q_m^H=0",
            "not selected for claim",
        ),
        (
            "FORK1542_1_finite_Cqm",
            "finite coupling route",
            "C_qm, T_source_norm, S_direct_m, S_source_norm_extra, and S_boundary_m are sourced or bounded",
            "SELECTED_NONCLAIM_WORK_ROUTE",
            "turns coupling leak into a testable residual envelope",
            "selected for next work",
        ),
        (
            "FORK1542_2_public_claim",
            "public/local-GR route",
            "exact kernel or finite envelope must beat local bounds with full N_lock/Kmetric projection",
            "BLOCKED_NO_CLAIM",
            "prevents using a conditional q story as a GR-reduction proof",
            "not selected",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "fork_id": fork_id,
            "route": route,
            "condition": condition,
            "current_status": status,
            "effect_if_closed": effect,
            "decision": decision,
            "source_paths": source_list("1541_coupling", "1541_kernel", "1540_chain"),
            **flags(),
        }
        for fork_id, route, condition, status, effect, decision in rows
    ]


def cqm_source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CQM1542_0_C_qm",
            "C_qm",
            "observed quotient derivative norm",
            "C_qm=||DObs_e[Dq[v_m]]||_{loc}",
            "dimension depends on v_m normalization",
            "MISSING_DQVM_DERIVATIVE",
            "derive q_loc and v_m derivatives; or introduce sourced finite coefficient with units/provenance",
        ),
        (
            "CQM1542_1_T_source_norm",
            "T_source_norm",
            "active compact-source stress/current norm in the same local dual space",
            "T_source_norm=||delta S_matter/delta q||_{source}",
            "stress/current norm",
            "MISSING_SOURCE_NORM",
            "define from Hilbert/Noether source current and local compact-source profile",
        ),
        (
            "CQM1542_2_S_direct_m",
            "S_direct_m",
            "direct memory dependence in matter/source action",
            "S_direct_m=||(partial_m S_matter + partial_m S_source_norm)_q||_{E*}",
            "E* forcing units",
            "MISSING_ACTION_DOMAIN_EXCLUSION_OR_VALUE",
            "derive no-direct-memory theorem or source the residual coefficient",
        ),
        (
            "CQM1542_3_S_source_norm_extra",
            "S_source_norm_extra",
            "extra source-normalization/source-calibration memory leakage",
            "S_source_norm_extra=||partial_m S_source_norm beyond Hilbert q-pullback||_{E*}",
            "E* forcing units",
            "MISSING_SOURCE_NORMALIZATION_RESIDUAL",
            "derive source-normalization descent or retain finite coefficient",
        ),
        (
            "CQM1542_4_S_boundary_m",
            "S_boundary_m",
            "compact inner/domain/boundary memory leakage",
            "S_boundary_m <= C_inner |Q_m^H| + domain/support boundary terms",
            "E* forcing units",
            "MISSING_BOUNDARY_CHARGE_AND_DOMAIN_NORM",
            "derive Q_m^H=0/domain silence or source boundary norm",
        ),
        (
            "CQM1542_5_Scg_envelope",
            "S_cg_norm",
            "finite no-cancellation source-coupling envelope",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "E* forcing units",
            "SCHEMA_READY_INPUTS_MISSING",
            "runner input once rows CQM1542_0 through CQM1542_4 are numeric or theorem-zero",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "symbol": symbol,
            "meaning": meaning,
            "definition_or_bound": definition,
            "units": units,
            "current_status": status,
            "acquisition_route": route,
            "source_paths": source_list("1541_coupling", "1539_inputs", "ward_universality", "source_normalization_owner", "source_measure_flux"),
            **flags(),
        }
        for input_id, symbol, meaning, definition, units, status, route in rows
    ]


def scg_runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1542_0_exact",
            "exact S_cg silence",
            "S_cg_norm=0 if Dq[v_m]=0, direct_m S=0, source-normalization descent, and Q_m^H=0",
            "BLOCKED",
            "exact kernel route failed current evidence",
        ),
        (
            "RUN1542_1_finite",
            "finite S_cg envelope",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "NOT_COMPUTABLE",
            "all finite source-pack inputs are missing",
        ),
        (
            "RUN1542_2_Npair",
            "first-pair insertion",
            "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "NOT_COMPUTABLE",
            "S_cg_norm, U_B_max, C_inner, and Q_m^H are not sourced",
        ),
        (
            "RUN1542_3_local_projection",
            "local residual projection",
            "PPN/R10/clock/orbital residual <= K_metric/source_projection * N_lock",
            "BLOCKED_NO_CLAIM",
            "N_lock and local projection coefficients remain unfilled",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "quantity": quantity,
            "formula": formula,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, quantity, formula, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1542_0_q_rules", "legal q-definition rules written", "PASS_NONCLAIM", "post-hoc quotient deletion is explicitly rejected"),
        ("GATE1542_1_exact_kernel", "Dq[v_m]=0 exact kernel", "BLOCKED", "q_loc/v_m are not jointly parent-signed"),
        ("GATE1542_2_finite_pack", "finite C_qm source pack staged", "PASS_NONCLAIM", "all needed finite inputs named but missing"),
        ("GATE1542_3_Scg_numeric", "S_cg_norm computable", "BLOCKED", "finite inputs are not numeric/theorem-zero"),
        ("GATE1542_4_Npair", "N_pair computable", "BLOCKED", "S_cg_norm plus first-pair inputs remain missing"),
        ("GATE1542_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "no exact kernel and no finite bound pass"),
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
        (
            "DEC1542_0_q_result",
            "Do not define q by deleting couplings.",
            "POSTHOC_Q_REJECTED",
            "a legal quotient has to be parent-owned before empirical/local gates are judged",
        ),
        (
            "DEC1542_1_exact_result",
            "Do not claim the exact Dq[v_m]=0 route.",
            "EXACT_KERNEL_FAILS_CURRENT_EVIDENCE",
            "q_loc and v_m are still conditional contracts, not a signed parent kernel",
        ),
        (
            "DEC1542_2_work_route",
            "Move to finite C_qm/S_cg input acquisition.",
            "FINITE_SOURCE_PACK_SELECTED",
            "this is the testable route unless a future parent action signs the kernel",
        ),
        (
            "DEC1542_3_no_claim",
            "Keep local GR/Newton/PPN nonclaim.",
            "CLAIM_BLOCKED",
            "finite S_cg and N_pair are not computable yet",
        ),
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
            "next_id": "NEXT1542_0_1543",
            "next_target": "1543-Y5-Cqm-source-norm-local-projection-pack.md",
            "script": "scripts/Y5_Cqm_source_norm_local_projection_pack.py",
            "objective": "fill or bound the finite inputs C_qm, T_source_norm, S_direct_m, S_source_norm_extra, and S_boundary_m, then map the resulting S_cg_norm into R10/PPN/clock/orbital local projections without claiming a pass",
            "do_not": "do not insert placeholder numeric values; do not use cancellations; do not claim local GR or q-kernel silence",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (Q_DEFINITION_AUDIT, QUAR_QDEF),
        (VM_DEFINITION_AUDIT, QUAR_VMDEF),
        (FORK_MATRIX, QUAR_FORK),
        (CQM_SOURCE_PACK, QUAR_CQM),
        (SCG_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (Q_DEFINITION_AUDIT, BRANCH_QDEF),
        (VM_DEFINITION_AUDIT, BRANCH_VMDEF),
        (FORK_MATRIX, BRANCH_FORK),
        (CQM_SOURCE_PACK, BRANCH_CQM),
        (SCG_RUNNER, BRANCH_RUNNER),
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
    qdef = read_csv(Q_DEFINITION_AUDIT)
    vmdef = read_csv(VM_DEFINITION_AUDIT)
    fork = read_csv(FORK_MATRIX)
    cqm = read_csv(CQM_SOURCE_PACK)
    runner = read_csv(SCG_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_cqm = {"C_qm", "T_source_norm", "S_direct_m", "S_source_norm_extra", "S_boundary_m", "S_cg_norm"}
    cqm_symbols = {row["symbol"] for row in cqm}
    checks = [
        ("VAL1542_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1542 source paths exist"),
        ("VAL1542_1_posthoc_q_rejected", any(row["qdef_id"] == "QDEF1542_2_illegal_deletion" and row["current_status"] == "REJECTED" for row in qdef), "post-hoc q deletion is rejected"),
        ("VAL1542_2_exact_kernel_unavailable", any(row["qdef_id"] == "QDEF1542_4_q_verdict" and row["current_status"] == "EXACT_KERNEL_NOT_AVAILABLE" for row in qdef), "exact q/v_m kernel not available"),
        ("VAL1542_3_vm_gap", any(row["vmdef_id"] == "VMDEF1542_3_vm_verdict" and row["current_status"] == "KERNEL_NOT_PROVED" for row in vmdef), "v_m remains not kernel-proved"),
        ("VAL1542_4_fork_selects_finite", any(row["fork_id"] == "FORK1542_1_finite_Cqm" and row["current_status"] == "SELECTED_NONCLAIM_WORK_ROUTE" for row in fork), "finite C_qm route selected as nonclaim work route"),
        ("VAL1542_5_cqm_inputs_complete", required_cqm.issubset(cqm_symbols), "finite C_qm/S_cg source pack has all required rows"),
        ("VAL1542_6_scg_runner_blocked", any(row["runner_id"] == "RUN1542_1_finite" and row["current_status"] == "NOT_COMPUTABLE" for row in runner), "S_cg finite runner remains noncomputable"),
        ("VAL1542_7_claim_gates_block", any(row["gate_id"] == "GATE1542_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1542_8_decision_finite", any(row["result"] == "FINITE_SOURCE_PACK_SELECTED" for row in decisions), "decision selects finite source-pack acquisition"),
        ("VAL1542_9_next_target", any("1543-Y5-Cqm-source-norm" in row["next_target"] for row in next_rows), "next target is C_qm source-norm local projection pack"),
        ("VAL1542_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1542 CSVs parse cleanly"),
        ("VAL1542_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1542_12_branch_copies", all(path.exists() for path in [QUAR_QDEF, QUAR_VMDEF, QUAR_FORK, QUAR_CQM, QUAR_RUNNER, QUAR_DECISION, BRANCH_QDEF, BRANCH_VMDEF, BRANCH_FORK, BRANCH_CQM, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1542_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1542_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1542_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1542 rejects post-hoc q deletion, keeps exact Dq[v_m]=0 unproved, stages the finite C_qm/S_cg source pack, keeps claims blocked, and selects C_qm source-norm projection next"
            if overall
            else "1542 validation failed; inspect failed rows before continuing",
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
    qdef: list[dict[str, Any]],
    vmdef: list[dict[str, Any]],
    fork: list[dict[str, Any]],
    cqm: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1542 - q Definition or Dq[v_m] Coupling Coefficient Source Pack",
                "",
                "## Verdict",
                "- A legal `q_loc` must be parent-owned before local tests; defining `q` by deleting whichever coupling failed is explicitly rejected.",
                "- The exact route still does not close: current evidence does not define `q_loc` and `v_m` strongly enough to prove `Dq[v_m]=0`.",
                "- The work route is now the finite source pack: `S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m`.",
                "- This is useful because it turns the coupling problem into sourceable inputs rather than a vague philosophical gap.",
                "- No source-silence, local lock, local GR/Newton/PPN, R10, WEP, clock, or orbital claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## q Definition Audit",
                md_table(qdef, ["qdef_id", "audit_item", "statement", "current_status", "reason", "missing_to_promote"]),
                "",
                "## v_m Definition Audit",
                md_table(vmdef, ["vmdef_id", "audit_item", "statement", "current_status", "reason"]),
                "",
                "## Fork Decision Matrix",
                md_table(fork, ["fork_id", "route", "condition", "current_status", "effect_if_closed", "decision"]),
                "",
                "## C_qm Source Pack",
                md_table(cqm, ["input_id", "symbol", "meaning", "definition_or_bound", "units", "current_status", "acquisition_route"]),
                "",
                "## S_cg Runner",
                md_table(runner, ["runner_id", "quantity", "formula", "current_status", "reason"]),
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
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    qdef = q_definition_rows()
    vmdef = vm_definition_rows()
    fork = fork_matrix_rows()
    cqm = cqm_source_pack_rows()
    runner = scg_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(Q_DEFINITION_AUDIT, qdef)
    write_csv(VM_DEFINITION_AUDIT, vmdef)
    write_csv(FORK_MATRIX, fork)
    write_csv(CQM_SOURCE_PACK, cqm)
    write_csv(SCG_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        Q_DEFINITION_AUDIT,
        VM_DEFINITION_AUDIT,
        FORK_MATRIX,
        CQM_SOURCE_PACK,
        SCG_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, qdef, vmdef, fork, cqm, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
