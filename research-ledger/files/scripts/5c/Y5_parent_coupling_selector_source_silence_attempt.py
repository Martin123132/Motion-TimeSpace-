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
DOC = ROOT / "1540-Y5-parent-coupling-selector-source-silence-attempt.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1539_doc": ROOT / "1539-Y5-source-support-power-and-inner-charge-input-acquisition.md",
    "1539_validation": OUT / "P8_Y5_BRR545_1539_VALIDATION.csv",
    "1539_input_ledger": OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv",
    "1539_lemmas": OUT / "P8_Y5_PARENT_QLOC_1539_CONDITIONAL_BOUND_LEMMAS.csv",
    "1539_schema": OUT / "P8_Y5_PARENT_QLOC_1539_PAIR_BOUND_SCHEMA_NONCLAIM.csv",
    "1538_Nsrc": OUT / "P8_Y5_PARENT_QLOC_1538_N_SRC_THEOREM_OR_BOUND.csv",
    "1538_Ninner": OUT / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1540_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv"
VARIATION_CHAIN = OUT / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv"
PAYOFF = OUT / "P8_Y5_PARENT_QLOC_1540_SOURCE_SILENCE_PAYOFF.csv"
FAILURE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_FAILURE_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1540_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1540_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1540_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1540_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1540"
QUAR_THEOREM = QUARANTINE / "COUPLING_SELECTOR_THEOREM_ATTEMPT_NONCLAIM.csv"
QUAR_CHAIN = QUARANTINE / "VARIATION_CHAIN_AUDIT_NONCLAIM.csv"
QUAR_PAYOFF = QUARANTINE / "SOURCE_SILENCE_PAYOFF_NONCLAIM.csv"
QUAR_FAILURE = QUARANTINE / "COUPLING_FAILURE_LEDGER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "parent_coupling_selector_theorem_attempt_nonclaim_1540.csv"
BRANCH_CHAIN = BRANCH_RESIDUALS / "parent_coupling_variation_chain_audit_nonclaim_1540.csv"
BRANCH_PAYOFF = BRANCH_RESIDUALS / "parent_coupling_source_silence_payoff_nonclaim_1540.csv"
BRANCH_FAILURE = BRANCH_RESIDUALS / "parent_coupling_failure_ledger_nonclaim_1540.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "parent_coupling_decision_nonclaim_1540.csv"


def flags() -> dict[str, bool]:
    return {
        "premise_signed": False,
        "theorem_closed": False,
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
        "premise_signed",
        "theorem_closed",
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
            "source_id": f"SRC1540_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for parent coupling selector/source-silence proof attempt",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CSEL1540_0_candidate_theorem",
            "candidate selector theorem",
            "If S_matter and S_source_norm depend only on q(Phi), matter fields, and calibrated constants, and the local memory/cg variation v_m is vertical with Dq[v_m]=0, then matter/source action has no active memory source.",
            "S_cg_norm=0 and no matter-owned contribution to Q_m^H",
            "CANDIDATE_THEOREM_FORMULATED",
            "all premises below must be parent-signed together",
        ),
        (
            "CSEL1540_1_matter_descent",
            "matter action descent",
            "S_matter=sum_A S_A[Psi_A, q(Phi), omega[q(Phi)], theta_A] with no direct m, L_cg, Pi_B, class, or source-support marker argument",
            "kills direct partial_m S_matter",
            "UNSIGNED",
            "SC0 is conditional and A6 is not parent-derived",
        ),
        (
            "CSEL1540_2_vertical_memory_generator",
            "vertical generator condition",
            "v_m in ker(Dq), so Dq[v_m]=0 for the memory/cg direction being tested",
            "kills stress-mediated coupling through observed geometry",
            "MISSING_CORE_Q_MAP",
            "the quotient map q and actual vertical generator are not signed here",
        ),
        (
            "CSEL1540_3_source_norm_descent",
            "source normalization descent",
            "S_source_norm[kappa,G_eff,M_eff,Pi_M J_H(q)] contains no memory-sector or selector-dependent source coefficient",
            "kills source-normalization contribution to S_cg and Q_m^H",
            "UNSIGNED",
            "A4/A5 and Y5O_3..Y5O_6 remain not parent-derived",
        ),
        (
            "CSEL1540_4_boundary_silence",
            "boundary/excision silence",
            "S_boundary is class-only/topological or q-only and carries no memory boundary flux through compact inner boundary",
            "kills Q_m^H from boundary symplectic/source flux",
            "FAIL_OPEN",
            "SC5 and the 1529 boundary certificate remain open",
        ),
        (
            "CSEL1540_5_no_retained_current",
            "no retained source current",
            "q_retained^nu=0 or owned divergence has no non-Hilbert memory/source current",
            "prevents a hidden source-current bypass",
            "UNSIGNED",
            "SC4/A1/A2 are not parent-derived",
        ),
        (
            "CSEL1540_6_current_verdict",
            "selector theorem verdict",
            "the algebraic theorem is valid as a conditional route but current MTS inputs do not sign the premises",
            "do not set S_cg_norm=0 or Q_m^H=0",
            "THEOREM_NOT_CLOSED",
            "next proof target is the actual quotient map q and Dq[v_m] certificate",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_row_id": row_id,
            "clause": clause,
            "required_statement": statement,
            "would_close": would_close,
            "current_status": status,
            "missing_or_reason": missing,
            "source_paths": source_list("1539_lemmas", "source_owner", "ward_universality", "source_normalization_owner"),
            **flags(),
        }
        for row_id, clause, statement, would_close, status, missing in rows
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VAR1540_0_matter_variation",
            "memory/cg variation of matter action",
            "delta_v S_matter = <delta S_matter/delta q, Dq[v_m]> + (partial_m S_matter)_q delta m",
            "both Dq[v_m]=0 and direct partial_m S_matter=0 are required",
            "DERIVED_IDENTITY_CONDITIONAL",
        ),
        (
            "VAR1540_1_stress_not_zero",
            "stress term cannot be ignored",
            "delta S_matter/delta q is the Hilbert stress/current and is nonzero for ordinary matter",
            "one cannot use matter equations of motion to kill the stress-mediated Dq[v_m] term",
            "NO_SHORTCUT",
        ),
        (
            "VAR1540_2_source_norm_variation",
            "memory/cg variation of source normalization",
            "delta_v S_source_norm = <delta S_source_norm/delta Pi_M J_H, delta_v(Pi_M J_H)> + direct memory/source-coefficient terms",
            "source normalization must also descend through q-only Hilbert current",
            "DERIVED_IDENTITY_CONDITIONAL",
        ),
        (
            "VAR1540_3_boundary_charge",
            "inner memory charge",
            "Q_m^H is the inner boundary flux/symplectic charge induced by the same variation",
            "Q_m^H=0 needs no direct memory boundary term plus no q-dependent memory flux through v_m",
            "BOUNDARY_OPEN",
        ),
        (
            "VAR1540_4_payoff_identity",
            "first-pair silence identity",
            "direct_m S=0, Dq[v_m]=0, and boundary memory flux=0 imply S_cg_norm=0 and Q_m^H=0",
            "then N_pair=0 for the source/inner pair",
            "CONDITIONAL_NOT_ADOPTED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "chain_id": chain_id,
            "step": step,
            "identity": identity,
            "implication": implication,
            "current_status": status,
            "source_paths": source_list("1539_input_ledger", "source_owner", "ward_universality", "boundary_certificate"),
            **flags(),
        }
        for chain_id, step, identity, implication, status in rows
    ]


def payoff_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PAY1540_0_if_closed",
            "if coupling selector closes",
            "S_cg_norm=0; Q_m^H=0; N_src=0; N_inner=0; N_pair=0",
            "would remove first-pair source/inner obstruction",
            "CONDITIONAL_PAYOFF_ONLY",
        ),
        (
            "PAY1540_1_current_Nsrc",
            "current N_src",
            "S_cg_norm remains missing; U_B_max irrelevant only if S_cg_norm=0 is proved",
            "N_src remains unfilled",
            "BLOCKED_NONCLAIM",
        ),
        (
            "PAY1540_2_current_Ninner",
            "current N_inner",
            "Q_m^H remains missing; C_inner irrelevant only if Q_m^H=0 is proved",
            "N_inner remains unfilled",
            "BLOCKED_NONCLAIM",
        ),
        (
            "PAY1540_3_current_local_GR",
            "current local GR branch",
            "first-pair silence not proved; full N_lock and Kmetric conversion still absent",
            "local GR/Newton/PPN remains blocked",
            "BLOCKED_NO_CLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "payoff_id": payoff_id,
            "case": case,
            "result": result,
            "implication": implication,
            "current_status": status,
            **flags(),
        }
        for payoff_id, case, result, implication, status in rows
    ]


def failure_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FAIL1540_0_Dq_leak",
            "observed geometry depends on memory/cg",
            "If Dq[v_m] != 0, ordinary matter stress sources the memory/cg equation.",
            "retain S_cg_norm finite-bound branch",
        ),
        (
            "FAIL1540_1_direct_memory_argument",
            "matter/source action has direct memory argument",
            "If partial_m S_matter or source-normalization coefficients are nonzero, selector silence fails.",
            "source S_cg_norm directly or rewrite parent action",
        ),
        (
            "FAIL1540_2_boundary_flux",
            "compact inner boundary carries memory flux",
            "If Q_m^H is a real compact-source charge, no exterior vacuum wording can erase it.",
            "retain C_inner |Q_m^H| in the local bound",
        ),
        (
            "FAIL1540_3_retained_current",
            "retained non-Hilbert current",
            "If q_retained^nu survives, source-current silence can fail even when matter action descends.",
            "derive owned current decomposition or retain residual vector",
        ),
        (
            "FAIL1540_4_frame_split",
            "matter/source readout uses a split observed frame",
            "If clocks/photons/sources use different q maps, the coupling can reappear as calibration hair.",
            "derive single observed coframe or keep frame residual rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "failure_id": failure_id,
            "failure_mode": mode,
            "why_it_matters": why,
            "fallback": fallback,
            "source_paths": source_list("source_owner", "ward_universality", "source_measure_flux", "boundary_certificate"),
            **flags(),
        }
        for failure_id, mode, why, fallback in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1540_0_variation_identity", "coupling variation identity written", "PASS_NONCLAIM", "chain rule exposes direct term plus Dq[v_m] stress term"),
        ("GATE1540_1_selector_theorem", "parent selector theorem closed", "BLOCKED", "q map, vertical generator, source-normalization, and boundary flux premises unsigned"),
        ("GATE1540_2_Scg_zero", "S_cg_norm=0", "BLOCKED", "Dq[v_m]=0 and direct matter/source silence not proved"),
        ("GATE1540_3_QmH_zero", "Q_m^H=0", "BLOCKED", "inner boundary/source charge silence not proved"),
        ("GATE1540_4_Npair_zero", "N_pair=0", "BLOCKED", "requires both S_cg_norm=0 and Q_m^H=0"),
        ("GATE1540_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "local source/inner pair remains open"),
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
            "DEC1540_0_progress",
            "Keep the selector theorem as a clean conditional route.",
            "CONDITIONAL_THEOREM_WRITTEN",
            "it gives the exact algebraic conditions for killing S_cg_norm and Q_m^H",
        ),
        (
            "DEC1540_1_core_blocker",
            "The core missing object is q and Dq[v_m].",
            "QUOTIENT_KERNEL_BLOCKER_IDENTIFIED",
            "matter stress is nonzero, so verticality of the memory generator is not optional",
        ),
        (
            "DEC1540_2_no_claim",
            "Do not promote source silence or local GR.",
            "CLAIM_BLOCKED",
            "the theorem is conditional and premises are unsigned",
        ),
        (
            "DEC1540_3_next",
            "Next target is the quotient map/kernel certificate.",
            "NEXT_1541_Q_MAP_VERTICAL_GENERATOR",
            "prove Dq[v_m]=0 or admit a finite coupling branch",
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
            "next_id": "NEXT1540_0_1541",
            "next_target": "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md",
            "script": "scripts/Y5_quotient_map_vertical_generator_kernel_certificate.py",
            "objective": "define the parent quotient map q, the local memory/cg vertical generator v_m, and either prove Dq[v_m]=0 or produce the finite coupling leakage row that sources S_cg_norm",
            "do_not": "do not rely on matter equations of motion to kill stress; do not assume verticality; do not claim source silence/local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (THEOREM_ATTEMPT, QUAR_THEOREM),
        (VARIATION_CHAIN, QUAR_CHAIN),
        (PAYOFF, QUAR_PAYOFF),
        (FAILURE_LEDGER, QUAR_FAILURE),
        (DECISION, QUAR_DECISION),
        (THEOREM_ATTEMPT, BRANCH_THEOREM),
        (VARIATION_CHAIN, BRANCH_CHAIN),
        (PAYOFF, BRANCH_PAYOFF),
        (FAILURE_LEDGER, BRANCH_FAILURE),
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
    theorem = read_csv(THEOREM_ATTEMPT)
    chain = read_csv(VARIATION_CHAIN)
    payoff = read_csv(PAYOFF)
    failures = read_csv(FAILURE_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1540_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1540 input source paths exist"),
        ("VAL1540_1_candidate_theorem", any(row["theorem_row_id"] == "CSEL1540_0_candidate_theorem" for row in theorem), "candidate selector theorem written"),
        ("VAL1540_2_kernel_blocker", any(row["theorem_row_id"] == "CSEL1540_2_vertical_memory_generator" and row["current_status"] == "MISSING_CORE_Q_MAP" for row in theorem), "Dq[v_m] kernel blocker identified"),
        ("VAL1540_3_variation_identity", any(row["chain_id"] == "VAR1540_0_matter_variation" and "Dq[v_m]" in row["identity"] for row in chain), "variation chain includes Dq[v_m] stress term"),
        ("VAL1540_4_no_stress_shortcut", any(row["chain_id"] == "VAR1540_1_stress_not_zero" and row["current_status"] == "NO_SHORTCUT" for row in chain), "matter stress shortcut rejected"),
        ("VAL1540_5_payoff_blocked", any(row["payoff_id"] == "PAY1540_3_current_local_GR" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in payoff), "payoff remains nonclaim"),
        ("VAL1540_6_failure_ledger", any(row["failure_id"] == "FAIL1540_0_Dq_leak" for row in failures), "Dq leakage failure mode recorded"),
        ("VAL1540_7_claim_gates_block", any(row["gate_id"] == "GATE1540_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1540_8_decision_next", any(row["result"] == "NEXT_1541_Q_MAP_VERTICAL_GENERATOR" for row in decisions), "decision selects q-map/vertical-generator target next"),
        ("VAL1540_9_next_target", any("1541-Y5-quotient-map" in row["next_target"] for row in next_rows), "next target is quotient map vertical generator kernel certificate"),
        ("VAL1540_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1540 CSVs parse cleanly"),
        ("VAL1540_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1540_12_branch_copies", all(path.exists() for path in [QUAR_THEOREM, QUAR_CHAIN, QUAR_PAYOFF, QUAR_FAILURE, QUAR_DECISION, BRANCH_THEOREM, BRANCH_CHAIN, BRANCH_PAYOFF, BRANCH_FAILURE, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1540_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1540_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1540_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1540 writes the parent coupling selector theorem attempt, proves the required variation identity, rejects the stress shortcut, keeps source silence nonclaim, and selects the q-map kernel certificate next"
            if overall
            else "1540 validation failed; inspect failed rows before continuing",
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
    theorem: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    payoff: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1540 - Parent Coupling Selector Source-Silence Attempt",
                "",
                "## Verdict",
                "- A clean conditional selector theorem now exists: if matter/source action descends only through the observed quotient `q(Phi)` and the memory/cg variation is vertical, then the first source pair can vanish.",
                "- The decisive identity is `delta_v S_matter = <delta S_matter/delta q, Dq[v_m]> + (partial_m S_matter)_q delta m`.",
                "- Ordinary matter stress is not zero, so the `Dq[v_m]` term cannot be waved away by matter equations of motion.",
                "- Current MTS state does not prove `Dq[v_m]=0`, direct memory/source silence, source-normalization descent, or compact boundary charge silence.",
                "- Therefore `S_cg_norm=0`, `Q_m^H=0`, `N_pair=0`, and local GR/Newton/PPN remain blocked/nonclaim.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Coupling Selector Theorem Attempt",
                md_table(theorem, ["theorem_row_id", "clause", "required_statement", "would_close", "current_status", "missing_or_reason"]),
                "",
                "## Variation Chain Audit",
                md_table(chain, ["chain_id", "step", "identity", "implication", "current_status"]),
                "",
                "## Source Silence Payoff",
                md_table(payoff, ["payoff_id", "case", "result", "implication", "current_status"]),
                "",
                "## Failure Ledger",
                md_table(failures, ["failure_id", "failure_mode", "why_it_matters", "fallback"]),
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
    theorem = theorem_attempt_rows()
    chain = variation_chain_rows()
    payoff = payoff_rows()
    failures = failure_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_ATTEMPT, theorem)
    write_csv(VARIATION_CHAIN, chain)
    write_csv(PAYOFF, payoff)
    write_csv(FAILURE_LEDGER, failures)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        THEOREM_ATTEMPT,
        VARIATION_CHAIN,
        PAYOFF,
        FAILURE_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, chain, payoff, failures, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
