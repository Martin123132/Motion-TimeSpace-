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
DOC = ROOT / "1538-Y5-source-support-and-inner-charge-theorem-or-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1537_doc": ROOT / "1537-Y5-Jeff-Bm-component-norm-input-pack.md",
    "1537_validation": OUT / "P8_Y5_BRR545_1537_VALIDATION.csv",
    "1537_first_priority": OUT / "P8_Y5_PARENT_QLOC_1537_FIRST_PRIORITY_NORM_ROWS.csv",
    "1537_norm_pack": OUT / "P8_Y5_PARENT_QLOC_1537_COMPONENT_NORM_INPUT_PACK.csv",
    "1536_doc": ROOT / "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md",
    "1536_jeff": OUT / "P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv",
    "1536_bm": OUT / "P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv",
    "1536_nlock": OUT / "P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
    "gamma_expansion": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "no_species_source_charge": OUT / "P8_no_species_source_charge_CONTRACT.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "parent_source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1538_SOURCE_REGISTER.csv"
N_SRC_GATE = OUT / "P8_Y5_PARENT_QLOC_1538_N_SRC_THEOREM_OR_BOUND.csv"
N_INNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv"
PAIR_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1538_PAIR_NORM_RUNNER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1538_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1538_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1538_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1538_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1538_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1538"
QUAR_N_SRC = QUARANTINE / "N_SRC_THEOREM_OR_BOUND_NONCLAIM.csv"
QUAR_N_INNER = QUARANTINE / "N_INNER_THEOREM_OR_BOUND_NONCLAIM.csv"
QUAR_PAIR = QUARANTINE / "PAIR_NORM_RUNNER_NONCLAIM.csv"
QUAR_REJECTION = QUARANTINE / "REJECTION_LEDGER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_N_SRC = BRANCH_RESIDUALS / "source_support_Nsrc_theorem_or_bound_nonclaim_1538.csv"
BRANCH_N_INNER = BRANCH_RESIDUALS / "inner_charge_Ninner_theorem_or_bound_nonclaim_1538.csv"
BRANCH_PAIR = BRANCH_RESIDUALS / "source_inner_pair_norm_runner_nonclaim_1538.csv"
BRANCH_REJECTION = BRANCH_RESIDUALS / "source_inner_rejection_ledger_nonclaim_1538.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "source_inner_decision_nonclaim_1538.csv"


def flags() -> dict[str, bool]:
    return {
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
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
        "promoted_to_theorem",
        "theorem_zero_adopted",
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
            "source_id": f"SRC1538_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for source-support and inner-charge theorem-or-bound gate",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def n_src_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NSRC1538_0_definition",
            "N_src",
            "J_src=U_B S_cg",
            "N_src=||U_B S_cg||_{E*}",
            "DEFINITION",
            "Exact first source forcing norm in the local memory-lock equation.",
            "none",
        ),
        (
            "NSRC1538_1_zero_by_UB",
            "U_B zero route",
            "U_B=0 on the local exterior/source-support branch",
            "N_src=0",
            "UNSIGNED_NOT_PROVED",
            "would kill the source term before it reaches the memory equation",
            "parent-signed projector/support theorem for U_B=0",
        ),
        (
            "NSRC1538_2_zero_by_projection",
            "S_cg projection zero route",
            "P_E*(S_cg)=0 or S_cg is orthogonal to the local exterior dual channel",
            "N_src=0",
            "UNSIGNED_NOT_PROVED",
            "would allow compact matter to exist while not sourcing the memory-lock mode",
            "parent-signed source-current selector and exterior projection theorem",
        ),
        (
            "NSRC1538_3_zero_by_selector_blindness",
            "matter action selector-blind route",
            "delta S_matter/delta m = 0 in the quotient-invariant local branch",
            "N_src=0",
            "UNSIGNED_NOT_PROVED",
            "would derive source silence from the parent matter action rather than postulate it",
            "signed matter-action descent with no representative Weyl/disformal memory coefficient",
        ),
        (
            "NSRC1538_4_finite_bound",
            "absolute finite bound",
            "N_src <= ||U_B||_inf ||S_cg||_{E*}",
            "N_src <= U_B_max S_cg_norm",
            "FORMULA_ONLY_INPUTS_MISSING",
            "safe no-cancellation bound; useful even if exact zero fails",
            "U_B_max; S_cg_norm; E* norm; projection convention; source support domain",
        ),
        (
            "NSRC1538_5_decision",
            "N_src verdict",
            "no source-support theorem or numeric bound is parent-signed yet",
            "N_src remains unfilled",
            "BLOCKED_NONCLAIM",
            "first N_lock input cannot be promoted",
            "derive/source U_B_max and S_cg_norm, or prove one exact-zero clause",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "condition_or_formula": condition,
            "bound_result": result,
            "status": status,
            "interpretation": interpretation,
            "missing_to_promote": missing,
            "source_paths": source_list(
                "1537_first_priority",
                "gamma_expansion",
                "ward_universality",
                "parent_source_owner",
                "source_normalization_owner",
            ),
            "theorem_zero_adopted": False,
            **flags(),
        }
        for row_id, route, condition, result, status, interpretation, missing in rows
    ]


def n_inner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NINNER1538_0_definition",
            "N_inner",
            "inner compact-source boundary forcing",
            "N_inner=||B_inner||_{boundary-dual}",
            "DEFINITION",
            "Exact first boundary forcing norm in the local memory-lock equation.",
            "none",
        ),
        (
            "NINNER1538_1_zero_by_QmH",
            "zero inner charge route",
            "Q_m^H=0 for the compact-source hole/excision boundary",
            "N_inner=0",
            "UNSIGNED_NOT_PROVED",
            "would eliminate the main compact-source hair channel",
            "parent-signed source charge/flux theorem proving Q_m^H=0",
        ),
        (
            "NINNER1538_2_zero_by_source_silence",
            "source/projection silence route",
            "matter carries no memory monopole into the local exterior boundary channel",
            "N_inner=0",
            "UNSIGNED_NOT_PROVED",
            "would let ordinary compact matter keep GR-like boundary data without memory hair",
            "source-current Ward universality plus no extra mass-channel theorem",
        ),
        (
            "NINNER1538_3_zero_by_boundary_no_flux",
            "boundary no-flux route",
            "inner boundary flux term vanishes in the parent local domain",
            "N_inner=0",
            "BLOCKED_BY_BOUNDARY_CERTIFICATE",
            "positive no-hair requires this; 1529 says the certificate is not signed",
            "parent domain, boundary, no-flux, and zero-mode certificate",
        ),
        (
            "NINNER1538_4_finite_bound",
            "absolute finite bound",
            "N_inner <= C_inner |Q_m^H|",
            "N_inner <= C_inner QmH_abs",
            "FORMULA_ONLY_INPUTS_MISSING",
            "safe no-cancellation bound if compact-source hair is nonzero",
            "C_inner; Q_m^H; boundary-dual norm; excision radius/domain convention",
        ),
        (
            "NINNER1538_5_decision",
            "N_inner verdict",
            "no zero charge theorem or numeric boundary bound is parent-signed yet",
            "N_inner remains unfilled",
            "BLOCKED_NONCLAIM",
            "second N_lock input cannot be promoted",
            "derive/source Q_m^H and C_inner, or prove one exact-zero clause",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "condition_or_formula": condition,
            "bound_result": result,
            "status": status,
            "interpretation": interpretation,
            "missing_to_promote": missing,
            "source_paths": source_list(
                "1537_first_priority",
                "positive_nohair",
                "no_species_source_charge",
                "ward_universality",
                "source_measure_flux",
                "boundary_certificate",
            ),
            "theorem_zero_adopted": False,
            **flags(),
        }
        for row_id, route, condition, result, status, interpretation, missing in rows
    ]


def pair_runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PAIR1538_0_exact_pair",
            "exact local source/boundary silence",
            "N_src=0 and N_inner=0",
            "BLOCKED",
            "no parent-signed U_B/S_cg silence and no parent-signed Q_m^H/no-flux theorem",
            "exact local no-hair theorem remains blocked",
        ),
        (
            "PAIR1538_1_finite_pair",
            "finite first-pair leakage",
            "N_pair <= U_B_max S_cg_norm + C_inner QmH_abs",
            "FORMULA_ONLY_INPUTS_MISSING",
            "U_B_max, S_cg_norm, C_inner, and Q_m^H are missing",
            "can become a calculable leakage bound once the four inputs are sourced",
        ),
        (
            "PAIR1538_2_Nlock_status",
            "N_lock first inputs",
            "N_lock >= N_src+N_inner before other nonnegative absolute components are added",
            "NOT_COMPUTABLE",
            "first source and boundary terms remain unfilled",
            "do not use cancellations against drift/history terms",
        ),
        (
            "PAIR1538_3_local_ppn_status",
            "local PPN residual vector",
            "PPN_residual ~ K_metric * N_lock plus hidden-kernel terms",
            "BLOCKED_NO_CLAIM",
            "N_lock and Kmetric conversion are not numeric",
            "local GR/Newton/PPN branch remains nonclaim",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "quantity": quantity,
            "formula": formula,
            "current_status": status,
            "missing_or_rule": missing,
            "implication": implication,
            **flags(),
        }
        for runner_id, quantity, formula, status, missing, implication in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "REJ1538_0_no_assumed_UB_zero",
            "Do not set U_B=0 by interpretation.",
            "U_B=0 must come from a parent support/projector theorem.",
        ),
        (
            "REJ1538_1_no_assumed_QmH_zero",
            "Do not set Q_m^H=0 by exterior vacuum language.",
            "positive no-hair explicitly says compact source inner boundary charge is not automatic zero.",
        ),
        (
            "REJ1538_2_no_cancellation",
            "Do not cancel source terms against drift/history/boundary terms.",
            "the leakage branch uses absolute nonnegative component envelopes.",
        ),
        (
            "REJ1538_3_no_GR_promotion",
            "Do not promote local GR/Newton/PPN.",
            "N_src, N_inner, N_lock, Kmetric conversion, and hidden kernels remain open.",
        ),
        (
            "REJ1538_4_no_numeric_placeholder",
            "Do not insert placeholder numeric bounds.",
            "the next pass must source or derive U_B_max, S_cg_norm, C_inner, and Q_m^H.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "rejected_shortcut": shortcut,
            "reason": reason,
            "source_paths": source_list("1537_first_priority", "positive_nohair", "boundary_certificate"),
            **flags(),
        }
        for rejection_id, shortcut, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1538_0_Nsrc_rows", "N_src exact-zero and finite-bound routes written", "PASS_NONCLAIM", "routes are explicit but unsigned"),
        ("GATE1538_1_Ninner_rows", "N_inner exact-zero and finite-bound routes written", "PASS_NONCLAIM", "routes are explicit but unsigned"),
        ("GATE1538_2_exact_zero", "N_src=0 or N_inner=0 theorem", "BLOCKED", "no parent-signed zero theorem"),
        ("GATE1538_3_finite_bound", "numeric first-pair bound", "BLOCKED", "U_B_max/S_cg_norm/C_inner/Q_m^H missing"),
        ("GATE1538_4_Nlock", "N_lock computable", "BLOCKED", "first-pair and remaining component norms missing"),
        ("GATE1538_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "local branch remains closure-only/nonclaim"),
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
            "DEC1538_0_progress",
            "Keep the source/inner-charge formulas.",
            "FIRST_PAIR_FORMULAS_WRITTEN",
            "N_src and N_inner now have exact-zero routes and absolute finite-bound routes.",
        ),
        (
            "DEC1538_1_no_zero",
            "Do not adopt source or inner-charge silence.",
            "ZERO_PROOF_FAILED_FOR_NOW",
            "every zero route needs a missing parent theorem.",
        ),
        (
            "DEC1538_2_no_claim",
            "Do not claim local locking or local GR.",
            "CLAIM_BLOCKED",
            "N_pair is formula-only and nonnumeric.",
        ),
        (
            "DEC1538_3_next",
            "Next target is source-support power and inner-charge input acquisition.",
            "NEXT_1539_SOURCE_SUPPORT_POWER_INNER_CHARGE_INPUTS",
            "the four concrete inputs are U_B_max, S_cg_norm, C_inner, and Q_m^H.",
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
            "next_id": "NEXT1538_0_1539",
            "next_target": "1539-Y5-source-support-power-and-inner-charge-input-acquisition.md",
            "script": "scripts/Y5_source_support_power_and_inner_charge_input_acquisition.py",
            "objective": "source, derive, or explicitly close the four first-pair inputs U_B_max, S_cg_norm, C_inner, and Q_m^H; keep all rows nonclaim until parent-signed or externally bounded",
            "do_not": "do not invent numeric placeholders; do not claim source silence or inner-charge silence by language alone; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (N_SRC_GATE, QUAR_N_SRC),
        (N_INNER_GATE, QUAR_N_INNER),
        (PAIR_RUNNER, QUAR_PAIR),
        (REJECTION_LEDGER, QUAR_REJECTION),
        (DECISION, QUAR_DECISION),
        (N_SRC_GATE, BRANCH_N_SRC),
        (N_INNER_GATE, BRANCH_N_INNER),
        (PAIR_RUNNER, BRANCH_PAIR),
        (REJECTION_LEDGER, BRANCH_REJECTION),
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
    n_src = read_csv(N_SRC_GATE)
    n_inner = read_csv(N_INNER_GATE)
    pair = read_csv(PAIR_RUNNER)
    rejected = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    nsrc_status = {row["row_id"]: row["status"] for row in n_src}
    ninner_status = {row["row_id"]: row["status"] for row in n_inner}
    exact_zero_statuses = [
        row["status"]
        for row in n_src + n_inner
        if "zero" in row["route"].lower() or row["bound_result"] == "N_src=0" or row["bound_result"] == "N_inner=0"
    ]
    checks = [
        ("VAL1538_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1538 input source paths exist"),
        ("VAL1538_1_Nsrc_exact_and_bound", "NSRC1538_1_zero_by_UB" in nsrc_status and "NSRC1538_4_finite_bound" in nsrc_status, "N_src exact-zero and finite-bound routes written"),
        ("VAL1538_2_Ninner_exact_and_bound", "NINNER1538_1_zero_by_QmH" in ninner_status and "NINNER1538_4_finite_bound" in ninner_status, "N_inner exact-zero and finite-bound routes written"),
        ("VAL1538_3_no_exact_zero_promoted", all(status != "THEOREM_ZERO_ADOPTED" for status in exact_zero_statuses), "no exact-zero shortcut promoted"),
        ("VAL1538_4_pair_runner_blocked", any(row["runner_id"] == "PAIR1538_2_Nlock_status" and row["current_status"] == "NOT_COMPUTABLE" for row in pair), "pair runner keeps N_lock noncomputable"),
        ("VAL1538_5_rejection_ledger", any(row["rejection_id"] == "REJ1538_2_no_cancellation" for row in rejected), "no-cancellation rejection recorded"),
        ("VAL1538_6_claim_gates_block", any(row["gate_id"] == "GATE1538_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1538_7_decision_next", any(row["result"] == "NEXT_1539_SOURCE_SUPPORT_POWER_INNER_CHARGE_INPUTS" for row in decisions), "decision selects concrete input acquisition next"),
        ("VAL1538_8_next_target", any("1539-Y5-source-support-power" in row["next_target"] for row in next_rows), "next target is source-support power and inner-charge input acquisition"),
        ("VAL1538_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1538 CSVs parse cleanly"),
        ("VAL1538_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1538_11_branch_copies", all(path.exists() for path in [QUAR_N_SRC, QUAR_N_INNER, QUAR_PAIR, QUAR_REJECTION, QUAR_DECISION, BRANCH_N_SRC, BRANCH_N_INNER, BRANCH_PAIR, BRANCH_REJECTION, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1538_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1538_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1538_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1538 derives the first-pair theorem-or-bound contract for N_src and N_inner, rejects unsigned zero shortcuts, keeps claims blocked, and selects concrete input acquisition next"
            if overall
            else "1538 validation failed; inspect failed rows before continuing",
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
    n_src: list[dict[str, Any]],
    n_inner: list[dict[str, Any]],
    pair: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1538 - Source Support and Inner Charge Theorem-or-Bound",
                "",
                "## Verdict",
                "- The first-pair local-lock blockers are now written as explicit theorem-or-bound contracts: `N_src=||U_B S_cg||_{E*}` and `N_inner=||B_inner||_{boundary-dual}`.",
                "- The cleanest exact route would prove either source-support silence (`U_B=0` or projected `S_cg=0`) and inner-charge silence (`Q_m^H=0` or no-flux), but every exact-zero clause is still unsigned.",
                "- The honest finite route is now sharp: `N_pair <= U_B_max S_cg_norm + C_inner |Q_m^H|`, with no cancellation allowed.",
                "- No numeric first-pair bound exists yet because `U_B_max`, `S_cg_norm`, `C_inner`, and `Q_m^H` are missing.",
                "- Local locking, local GR, Newton, PPN, R10, WEP, clock, and orbital claims remain blocked/nonclaim.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## N_src Theorem-or-Bound",
                md_table(n_src, ["row_id", "route", "condition_or_formula", "bound_result", "status", "missing_to_promote"]),
                "",
                "## N_inner Theorem-or-Bound",
                md_table(n_inner, ["row_id", "route", "condition_or_formula", "bound_result", "status", "missing_to_promote"]),
                "",
                "## Pair Norm Runner",
                md_table(pair, ["runner_id", "quantity", "formula", "current_status", "missing_or_rule", "implication"]),
                "",
                "## Rejection Ledger",
                md_table(rejected, ["rejection_id", "rejected_shortcut", "reason"]),
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
    n_src = n_src_rows()
    n_inner = n_inner_rows()
    pair = pair_runner_rows()
    rejected = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(N_SRC_GATE, n_src)
    write_csv(N_INNER_GATE, n_inner)
    write_csv(PAIR_RUNNER, pair)
    write_csv(REJECTION_LEDGER, rejected)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        N_SRC_GATE,
        N_INNER_GATE,
        PAIR_RUNNER,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, n_src, n_inner, pair, rejected, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
