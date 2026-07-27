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
DOC = ROOT / "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1540_doc": ROOT / "1540-Y5-parent-coupling-selector-source-silence-attempt.md",
    "1540_validation": OUT / "P8_Y5_BRR545_1540_VALIDATION.csv",
    "1540_theorem": OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
    "1540_chain": OUT / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv",
    "1540_failure": OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_FAILURE_LEDGER.csv",
    "1539_input_ledger": OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1045_doc": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
    "1029_doc": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "1030_doc": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1541_SOURCE_REGISTER.csv"
QMAP_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1541_QMAP_CANDIDATE_LEDGER.csv"
VGEN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1541_VERTICAL_GENERATOR_AUDIT.csv"
KERNEL_TEST = OUT / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv"
FINITE_COUPLING = OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1541_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1541_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1541_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1541_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1541"
QUAR_QMAP = QUARANTINE / "QMAP_CANDIDATE_LEDGER_NONCLAIM.csv"
QUAR_VGEN = QUARANTINE / "VERTICAL_GENERATOR_AUDIT_NONCLAIM.csv"
QUAR_KERNEL = QUARANTINE / "KERNEL_TEST_NONCLAIM.csv"
QUAR_COUPLING = QUARANTINE / "DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_QMAP = BRANCH_RESIDUALS / "qmap_candidate_ledger_nonclaim_1541.csv"
BRANCH_VGEN = BRANCH_RESIDUALS / "vertical_generator_audit_nonclaim_1541.csv"
BRANCH_KERNEL = BRANCH_RESIDUALS / "qmap_kernel_test_nonclaim_1541.csv"
BRANCH_COUPLING = BRANCH_RESIDUALS / "Dqvm_finite_coupling_row_nonclaim_1541.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "qmap_kernel_decision_nonclaim_1541.csv"


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
            "source_id": f"SRC1541_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for q-map/v_m kernel certificate and finite Dq[v_m] coupling fallback",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def qmap_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QMAP1541_0_parent_quotient",
            "q_loc: Phi_parent -> Q_obs/Q_loc",
            "q_loc is a parent-owned quotient/reduction map, not a post-readout projection",
            "CONDITIONAL_PRIOR_CONTRACT",
            "1023/1045 carry conditional q_loc contracts but not a parent-signed current MTS q map",
        ),
        (
            "QMAP1541_1_observed_coframe",
            "e_obs=Obs_e(q_loc(Phi)); g_obs=eta(e_obs,e_obs)",
            "ordinary matter stress couples to this observed coframe/metric",
            "CONDITIONAL_PRIOR_CONTRACT",
            "1045/1030 make this exact if signed; no terminal public metric theorem is current",
        ),
        (
            "QMAP1541_2_memory_membership",
            "membership of m/L_cg/cg data in q_loc",
            "the local memory/cg direction must be absent from q_loc to satisfy Dq[v_m]=0",
            "UNDECIDED",
            "current files do not define whether local m changes q, e_obs, calibration, or source readout",
        ),
        (
            "QMAP1541_3_shadow_frame_guard",
            "no hidden Weyl/disformal/readout frame",
            "if any A_m(m) or B_m(m) frame slot exists outside q, Dq[v_m] or direct source coupling reappears",
            "GUARD_ACTIVE_UNSIGNED",
            "1029/1030 reject covariance/WEP/Ward shortcuts; no-shadow frame remains unsigned",
        ),
        (
            "QMAP1541_4_current_verdict",
            "q map verdict",
            "q_loc is usable as a conditional theorem object, not as a signed kernel certificate",
            "QMAP_NOT_SIGNED",
            "cannot claim Dq[v_m]=0 from current q evidence",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "qmap_id": row_id,
            "object": obj,
            "required_statement": statement,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1023_doc", "1045_doc", "1029_doc", "1030_doc", "1540_doc"),
            **flags(),
        }
        for row_id, obj, statement, status, reason in rows
    ]


def vertical_generator_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VGEN1541_0_target",
            "v_m",
            "local memory/cg vertical generator tested by 1540",
            "delta_v m != 0 with declared variations of L_cg, Pi_B, e_obs, source normalization, boundary data, and matter lift",
            "FIELD_BY_FIELD_ACTION_MISSING",
            "the current branch has a symbol for the direction, not a complete parent transformation law",
        ),
        (
            "VGEN1541_1_clean_vertical_option",
            "v_m",
            "pure hidden representative direction",
            "delta_v m != 0 while delta_v q_loc=0, delta_v e_obs=0, delta_v theta=0, and boundary flux is exact/zero",
            "EXACT_ROUTE_UNSIGNED",
            "would close Dq[v_m]=0 and remove stress-mediated source coupling if parent-signed",
        ),
        (
            "VGEN1541_2_physical_memory_option",
            "v_m",
            "physical local memory direction",
            "delta_v m changes e_obs, G_eff/source normalization, constants, L_cg, boundary charge, or domain data",
            "FINITE_COUPLING_ROUTE_ACTIVE",
            "then Dq[v_m] or direct terms source S_cg_norm",
        ),
        (
            "VGEN1541_3_current_verdict",
            "v_m",
            "v_m verdict",
            "current MTS has not proven v_m is a kernel/null/gauge direction of q_loc",
            "KERNEL_NOT_PROVED",
            "must stage C_qm/Dq[v_m] finite row unless 1542 signs q and v_m",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "vgen_id": row_id,
            "object": obj,
            "role": role,
            "required_action": action,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1540_chain", "1539_input_ledger", "1023_doc", "1045_doc"),
            **flags(),
        }
        for row_id, obj, role, action, status, reason in rows
    ]


def kernel_test_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KTEST1541_0_Dq_kernel",
            "Dq[v_m]=0",
            "requires q_loc field definition plus v_m field-by-field action",
            "FAIL_CURRENT_CERTIFICATE",
            "q_loc and v_m are not jointly signed",
        ),
        (
            "KTEST1541_1_DObs_kernel",
            "DObs_e[Dq[v_m]]=0",
            "requires observed coframe functor and no shadow-frame/readout slot",
            "FAIL_CURRENT_CERTIFICATE",
            "terminal public metric/no-extra-frame theorem not derived",
        ),
        (
            "KTEST1541_2_direct_memory",
            "(partial_m S_matter)_q=0",
            "requires matter/source action domain excluding m, L_cg, Pi_B, support markers, and memory coefficients",
            "FAIL_CURRENT_CERTIFICATE",
            "parent object-language exclusion is a contract, not a derivation",
        ),
        (
            "KTEST1541_3_boundary_memory",
            "Q_m^H=0 under v_m",
            "requires compact inner boundary memory charge/no-flux theorem",
            "FAIL_CURRENT_CERTIFICATE",
            "boundary certificate remains open",
        ),
        (
            "KTEST1541_4_kernel_verdict",
            "full source-silence kernel",
            "KTEST1541_0 through KTEST1541_3 all pass together",
            "KERNEL_NOT_PROVED",
            "source-silence and local-GR claims remain blocked",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_test_id": row_id,
            "test": test,
            "pass_condition": condition,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1540_theorem", "1540_chain", "1023_doc", "1030_doc", "boundary_certificate"),
            **flags(),
        }
        for row_id, test, condition, status, reason in rows
    ]


def finite_coupling_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DQC1541_0_C_qm_definition",
            "C_qm",
            "observed-quotient derivative norm",
            "C_qm := ||DObs_e[Dq[v_m]]|| in the local weak-field/source norm",
            "MISSING_QMAP_DERIVATIVE",
            "dimension depends on v_m normalization",
            "finite coupling row if Dq[v_m] is nonzero or unknown",
        ),
        (
            "DQC1541_1_stress_coupling",
            "S_geom_m",
            "stress-mediated geometry coupling",
            "S_geom_m <= 1/2 ||T||_source C_qm",
            "FORMULA_ONLY_INPUTS_MISSING",
            "E* forcing units",
            "captures the term <delta S/delta q,Dq[v_m]> from 1540",
        ),
        (
            "DQC1541_2_direct_coupling",
            "S_direct_m",
            "direct memory/source action coupling",
            "S_direct_m := ||(partial_m S_matter + partial_m S_source_norm)_q||_{E*}",
            "MISSING_ACTION_DOMAIN_EXCLUSION",
            "E* forcing units",
            "retained if matter/source action has direct m or support-marker dependence",
        ),
        (
            "DQC1541_3_boundary_coupling",
            "S_boundary_m",
            "boundary/source-memory coupling",
            "S_boundary_m := C_inner |Q_m^H| or a stronger source-backed boundary norm",
            "MISSING_BOUNDARY_CHARGE",
            "E* forcing units",
            "retained if compact inner memory charge is not zero",
        ),
        (
            "DQC1541_4_Scg_envelope",
            "S_cg_norm",
            "absolute no-cancellation envelope",
            "S_cg_norm <= 1/2 ||T||_source C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "NONCLAIM_SCHEMA_READY_INPUTS_MISSING",
            "E* forcing units",
            "this is the finite fallback if q-kernel proof fails",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "coupling_id": row_id,
            "symbol": symbol,
            "meaning": meaning,
            "formula": formula,
            "current_status": status,
            "units": units,
            "role": role,
            "source_paths": source_list("1540_chain", "1539_input_ledger", "1029_doc", "1030_doc"),
            **flags(),
        }
        for row_id, symbol, meaning, formula, status, units, role in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1541_0_qmap_ledger", "q-map candidate ledger written", "PASS_NONCLAIM", "conditional q evidence collected"),
        ("GATE1541_1_vgen_audit", "v_m vertical generator audited", "PASS_NONCLAIM", "field-by-field action gap exposed"),
        ("GATE1541_2_Dq_kernel", "Dq[v_m]=0", "BLOCKED", "q map and v_m are not jointly parent-signed"),
        ("GATE1541_3_Scg_zero", "S_cg_norm=0", "BLOCKED", "Dq kernel, direct action silence, and boundary silence all fail current certificate"),
        ("GATE1541_4_finite_value", "finite C_qm/S_cg score", "BLOCKED", "finite row is schema-only with missing q derivative and source norms"),
        ("GATE1541_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "source coupling remains open"),
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
            "DEC1541_0_kernel_result",
            "Do not claim Dq[v_m]=0.",
            "KERNEL_NOT_PROVED",
            "the old q_loc contracts are conditional and do not define the current memory/cg vertical action",
        ),
        (
            "DEC1541_1_finite_fallback",
            "Retain a finite Dq[v_m] coupling envelope.",
            "C_QM_ROW_STAGED",
            "if q-kernel proof fails, S_cg_norm must be bounded through C_qm and direct/boundary source terms",
        ),
        (
            "DEC1541_2_best_next",
            "Try one final q-definition/source-pack split.",
            "NEXT_1542_Q_DEFINITION_OR_CQM_BOUND",
            "either define q/v_m from MTS primitives as a parent object or move to finite coefficient acquisition",
        ),
        (
            "DEC1541_3_no_claim",
            "No source-silence or local-GR promotion.",
            "CLAIM_BLOCKED",
            "Dq[v_m], S_cg_norm, and Q_m^H remain unclosed",
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
            "next_id": "NEXT1541_0_1542",
            "next_target": "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
            "script": "scripts/Y5_q_definition_or_Dqvm_coupling_coefficient_source_pack.py",
            "objective": "make the fork explicit: either define q_loc and v_m from MTS primitives strongly enough to sign Dq[v_m]=0, or fill a finite C_qm/S_cg_norm source-pack for local tests",
            "do_not": "do not define q by post-hoc deletion of failed couplings; do not use WEP/covariance/Ward shortcuts; do not claim local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (QMAP_LEDGER, QUAR_QMAP),
        (VGEN_AUDIT, QUAR_VGEN),
        (KERNEL_TEST, QUAR_KERNEL),
        (FINITE_COUPLING, QUAR_COUPLING),
        (DECISION, QUAR_DECISION),
        (QMAP_LEDGER, BRANCH_QMAP),
        (VGEN_AUDIT, BRANCH_VGEN),
        (KERNEL_TEST, BRANCH_KERNEL),
        (FINITE_COUPLING, BRANCH_COUPLING),
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
    qmap = read_csv(QMAP_LEDGER)
    vgen = read_csv(VGEN_AUDIT)
    kernel = read_csv(KERNEL_TEST)
    coupling = read_csv(FINITE_COUPLING)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1541_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1541 source paths exist"),
        ("VAL1541_1_qmap_verdict", any(row["qmap_id"] == "QMAP1541_4_current_verdict" and row["current_status"] == "QMAP_NOT_SIGNED" for row in qmap), "q-map remains conditional/not signed"),
        ("VAL1541_2_vgen_gap", any(row["vgen_id"] == "VGEN1541_0_target" and row["current_status"] == "FIELD_BY_FIELD_ACTION_MISSING" for row in vgen), "v_m field-by-field action gap recorded"),
        ("VAL1541_3_kernel_not_proved", any(row["kernel_test_id"] == "KTEST1541_4_kernel_verdict" and row["current_status"] == "KERNEL_NOT_PROVED" for row in kernel), "Dq[v_m] kernel not proved"),
        ("VAL1541_4_Cqm_row", any(row["coupling_id"] == "DQC1541_0_C_qm_definition" and row["symbol"] == "C_qm" for row in coupling), "finite C_qm coupling row staged"),
        ("VAL1541_5_Scg_envelope", any(row["coupling_id"] == "DQC1541_4_Scg_envelope" and "C_qm" in row["formula"] for row in coupling), "S_cg finite envelope includes C_qm"),
        ("VAL1541_6_claim_gates_block", any(row["gate_id"] == "GATE1541_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1541_7_decision_next", any(row["result"] == "NEXT_1542_Q_DEFINITION_OR_CQM_BOUND" for row in decisions), "decision selects q-definition or C_qm source-pack target"),
        ("VAL1541_8_next_target", any("1542-Y5-q-definition" in row["next_target"] for row in next_rows), "next target is q-definition or Dqvm coupling coefficient source pack"),
        ("VAL1541_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1541 CSVs parse cleanly"),
        ("VAL1541_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1541_11_branch_copies", all(path.exists() for path in [QUAR_QMAP, QUAR_VGEN, QUAR_KERNEL, QUAR_COUPLING, QUAR_DECISION, BRANCH_QMAP, BRANCH_VGEN, BRANCH_KERNEL, BRANCH_COUPLING, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1541_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1541_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1541_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1541 audits q_loc and v_m, refuses an unsigned Dq[v_m]=0 claim, stages the finite C_qm/S_cg coupling envelope, and selects q-definition-or-C_qm source-pack next"
            if overall
            else "1541 validation failed; inspect failed rows before continuing",
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
    qmap: list[dict[str, Any]],
    vgen: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1541 - Quotient Map / Vertical Generator Kernel Certificate",
                "",
                "## Verdict",
                "- The current corpus has a strong conditional `q_loc`/matter-functor spine, but it does not sign the current local memory/cg direction `v_m` as a true kernel direction.",
                "- Therefore `Dq[v_m]=0` is not proved, and the coupling-selector theorem from 1540 cannot yet set `S_cg_norm=0`.",
                "- The finite fallback is now explicit: define `C_qm := ||DObs_e[Dq[v_m]]||` and bound the stress-mediated source contribution by `S_geom_m <= 1/2 ||T||_source C_qm`.",
                "- The no-cancellation envelope is `S_cg_norm <= 1/2 ||T||_source C_qm + S_direct_m + S_source_norm_extra + S_boundary_m`.",
                "- No source-silence, local lock, local GR/Newton/PPN, R10, WEP, clock, or orbital claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Q-Map Candidate Ledger",
                md_table(qmap, ["qmap_id", "object", "required_statement", "current_status", "reason"]),
                "",
                "## Vertical Generator Audit",
                md_table(vgen, ["vgen_id", "object", "role", "required_action", "current_status", "reason"]),
                "",
                "## Kernel Test",
                md_table(kernel, ["kernel_test_id", "test", "pass_condition", "current_status", "reason"]),
                "",
                "## Finite Dq[v_m] Coupling Row",
                md_table(coupling, ["coupling_id", "symbol", "meaning", "formula", "current_status", "units", "role"]),
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
    qmap = qmap_rows()
    vgen = vertical_generator_rows()
    kernel = kernel_test_rows()
    coupling = finite_coupling_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QMAP_LEDGER, qmap)
    write_csv(VGEN_AUDIT, vgen)
    write_csv(KERNEL_TEST, kernel)
    write_csv(FINITE_COUPLING, coupling)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        QMAP_LEDGER,
        VGEN_AUDIT,
        KERNEL_TEST,
        FINITE_COUPLING,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, qmap, vgen, kernel, coupling, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
