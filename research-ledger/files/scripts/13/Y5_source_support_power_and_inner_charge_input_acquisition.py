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
DOC = ROOT / "1539-Y5-source-support-power-and-inner-charge-input-acquisition.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1538_doc": ROOT / "1538-Y5-source-support-and-inner-charge-theorem-or-bound.md",
    "1538_validation": OUT / "P8_Y5_BRR545_1538_VALIDATION.csv",
    "1538_Nsrc": OUT / "P8_Y5_PARENT_QLOC_1538_N_SRC_THEOREM_OR_BOUND.csv",
    "1538_Ninner": OUT / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv",
    "1538_pair": OUT / "P8_Y5_PARENT_QLOC_1538_PAIR_NORM_RUNNER.csv",
    "1538_rejection": OUT / "P8_Y5_PARENT_QLOC_1538_REJECTION_LEDGER.csv",
    "1537_norm_pack": OUT / "P8_Y5_PARENT_QLOC_1537_COMPONENT_NORM_INPUT_PACK.csv",
    "1536_jeff": OUT / "P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv",
    "1536_bm": OUT / "P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv",
    "gamma_expansion": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "parent_source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1539_SOURCE_REGISTER.csv"
INPUT_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv"
CONDITIONAL_LEMMAS = OUT / "P8_Y5_PARENT_QLOC_1539_CONDITIONAL_BOUND_LEMMAS.csv"
PAIR_BOUND_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1539_PAIR_BOUND_SCHEMA_NONCLAIM.csv"
INPUT_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1539_INPUT_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1539_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1539_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1539_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1539_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1539"
QUAR_LEDGER = QUARANTINE / "FIRST_PAIR_INPUT_ACQUISITION_LEDGER_NONCLAIM.csv"
QUAR_LEMMAS = QUARANTINE / "CONDITIONAL_BOUND_LEMMAS_NONCLAIM.csv"
QUAR_SCHEMA = QUARANTINE / "PAIR_BOUND_SCHEMA_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "INPUT_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_LEDGER = BRANCH_RESIDUALS / "source_support_power_inner_charge_input_acquisition_nonclaim_1539.csv"
BRANCH_LEMMAS = BRANCH_RESIDUALS / "source_inner_conditional_bound_lemmas_nonclaim_1539.csv"
BRANCH_SCHEMA = BRANCH_RESIDUALS / "source_inner_pair_bound_schema_nonclaim_1539.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "source_inner_input_runner_nonclaim_1539.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "source_inner_input_decision_nonclaim_1539.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "parent_signed": False,
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
        "parent_signed",
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
            "source_id": f"SRC1539_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for U_B_max, S_cg_norm, C_inner, and Q_m^H acquisition",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def input_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "INPUT1539_0_U_B_max",
            "U_B_max",
            "dimensionless local source-support leakage amplitude",
            "U_B=1-Pi_B; U_B_max=sup_{local exterior} |U_B|",
            "dimensionless",
            "MISSING_PARENT_PROJECTOR_VALUE",
            "Need Pi_B definition, range, local exterior branch, and proof/bound that Pi_B is close to 1 or exactly 1.",
            "derive projector support theorem; or source an empirical upper bound from local fifth-force/PPN residual pipeline",
            "gamma_expansion; parent_source_owner",
        ),
        (
            "INPUT1539_1_S_cg_norm",
            "S_cg_norm",
            "dual norm of compact-source forcing into memory/cg sector",
            "S_cg_norm=||P_E*(S_cg)||_{E*}",
            "E* forcing units",
            "MISSING_SOURCE_CURRENT_PROJECTION",
            "Need parent source-current selector, matter action variation target, and the projection map into the local memory equation.",
            "derive selector-blind coupling theorem; or define a sourced compact-body norm from Hilbert/Noether current",
            "ward_universality; source_normalization_owner",
        ),
        (
            "INPUT1539_2_C_inner",
            "C_inner",
            "boundary-to-energy trace/Green constant for compact inner charge",
            "||B_inner||_{E*} <= C_inner |Q_m^H|",
            "boundary-dual per charge unit",
            "SYMBOLIC_CONDITIONAL_ONLY",
            "A generic Lax-Milgram/trace constant exists only after the operator, domain, boundary norm, and charge normalization are fixed.",
            "derive exterior elliptic trace lemma for the selected local memory operator and excision geometry",
            "positive_nohair; boundary_certificate",
        ),
        (
            "INPUT1539_3_Q_mH",
            "Q_m^H",
            "compact-source inner memory charge or monopole flux through the excision boundary",
            "Q_m^H=int_{partial H} n_i K_m^i dS or equivalent parent-owned memory charge",
            "model-defined charge/flux",
            "MISSING_PARENT_CHARGE_OR_ZERO_THEOREM",
            "Need source silence, no extra mass-channel theorem, or a finite compact-source memory charge bound.",
            "derive Q_m^H=0 from coupling selector; or retain finite sourced row for local tests",
            "positive_nohair; source_measure_flux; boundary_certificate",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "symbol": symbol,
            "meaning": meaning,
            "definition": definition,
            "units": units,
            "current_status": status,
            "blocking_detail": blocking,
            "acquisition_route": route,
            "primary_sources": source_names,
            **flags(),
        }
        for input_id, symbol, meaning, definition, units, status, blocking, route, source_names in rows
    ]


def conditional_lemma_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LEMMA1539_0_Nsrc_product_bound",
            "source product bound",
            "If U_B in L^inf(Omega_loc) and projected S_cg in E*, then ||U_B S_cg||_{E*} <= U_B_max S_cg_norm.",
            "holder/dual multiplication bound in the chosen local exterior Banach pair",
            "CONDITIONAL_DERIVED_SCHEMA",
            "U_B_max and S_cg_norm missing; function spaces not parent-fixed",
        ),
        (
            "LEMMA1539_1_Ninner_boundary_bound",
            "inner charge boundary bound",
            "For a coercive exterior operator L_m=-D_m Delta+M_scr^2 with weak boundary functional b_H(phi)=Q_m^H h_H(phi), ||B_inner||_{E*} <= ||h_H||_{E*} |Q_m^H|.",
            "Lax-Milgram plus trace theorem; identify C_inner=||h_H||_{E*}",
            "CONDITIONAL_DERIVED_SCHEMA",
            "operator coefficients, domain, h_H normalization, and Q_m^H definition missing",
        ),
        (
            "LEMMA1539_2_pair_no_cancellation",
            "first-pair absolute envelope",
            "N_pair <= U_B_max S_cg_norm + C_inner |Q_m^H|.",
            "triangle inequality applied to source and inner-boundary forcing",
            "CONDITIONAL_DERIVED_SCHEMA",
            "all four input values missing",
        ),
        (
            "LEMMA1539_3_exact_selector_payoff",
            "coupling selector payoff",
            "If the parent matter action is independent of the memory variable and compact-source boundary memory flux, then S_cg_norm=0 and Q_m^H=0, so the first pair vanishes even without numeric bounds.",
            "Euler variation and Gauss/source-flux closure",
            "PREFERRED_PROOF_ROUTE_UNSIGNED",
            "selector-blind matter action and boundary charge silence not signed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "lemma_id": lemma_id,
            "lemma": lemma,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1538_Nsrc", "1538_Ninner", "positive_nohair", "ward_universality"),
            **flags(),
        }
        for lemma_id, lemma, statement, derivation, status, missing in rows
    ]


def pair_bound_schema_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SCHEMA1539_0_exact_first_pair",
            "exact first-pair silence",
            "If S_cg_norm=0 and Q_m^H=0, then N_pair=0 regardless of U_B_max and C_inner.",
            "BLOCKED_UNSIGNED",
            "requires parent coupling selector and boundary charge silence",
        ),
        (
            "SCHEMA1539_1_finite_first_pair",
            "finite first-pair leakage",
            "N_pair <= U_B_max*S_cg_norm + C_inner*QmH_abs",
            "SCHEMA_READY_INPUTS_MISSING",
            "requires four nonnegative sourced inputs",
        ),
        (
            "SCHEMA1539_2_local_residual_insertion",
            "local residual insertion",
            "PPN_residual_first_pair <= K_metric*(U_B_max*S_cg_norm + C_inner*QmH_abs) plus hidden-kernel terms",
            "BLOCKED_NO_NUMERIC_KMETRIC",
            "requires Kmetric conversion and hidden-kernel gate",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": schema_id,
            "schema": schema,
            "formula": formula,
            "current_status": status,
            "missing_to_promote": missing,
            **flags(),
        }
        for schema_id, schema, formula, status, missing in rows
    ]


def input_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1539_0_U_B_max", "U_B_max", "MISSING", "no numeric/projector theorem row found"),
        ("RUN1539_1_S_cg_norm", "S_cg_norm", "MISSING", "no source-current projection or selector theorem row found"),
        ("RUN1539_2_C_inner", "C_inner", "SYMBOLIC_ONLY", "conditional trace constant exists but no domain/operator normalization"),
        ("RUN1539_3_Q_mH", "Q_m^H", "MISSING", "no compact-source memory charge or zero theorem row found"),
        ("RUN1539_4_N_pair", "N_pair", "NOT_COMPUTABLE", "first-pair formula has missing nonnegative inputs"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "quantity": quantity,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, quantity, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1539_0_four_inputs_named", "four first-pair inputs are explicit", "PASS_NONCLAIM", "U_B_max, S_cg_norm, C_inner, and Q_m^H have acquisition rows"),
        ("GATE1539_1_product_bound", "N_src product bound schema", "PASS_NONCLAIM", "valid symbolic inequality; inputs missing"),
        ("GATE1539_2_boundary_bound", "N_inner boundary bound schema", "PASS_NONCLAIM", "valid symbolic trace/Lax-Milgram schema; operator/domain missing"),
        ("GATE1539_3_numeric_pair", "numeric N_pair bound", "BLOCKED", "four inputs not numeric/parent-signed"),
        ("GATE1539_4_exact_pair", "exact N_pair=0", "BLOCKED", "coupling selector and boundary charge silence not proven"),
        ("GATE1539_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "N_pair, full N_lock, and Kmetric conversion remain nonclaim"),
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
            "DEC1539_0_progress",
            "Keep the finite first-pair formula.",
            "SCHEMA_SHARPENED",
            "the first leakage term is now a four-input acquisition problem, not a vague coupling worry",
        ),
        (
            "DEC1539_1_Cinner",
            "Treat C_inner as conditionally derived but not numeric.",
            "TRACE_CONSTANT_SYMBOLIC_ONLY",
            "functional analysis gives the shape, but the actual operator/domain constant is still missing",
        ),
        (
            "DEC1539_2_coupling",
            "Attack the parent coupling selector next.",
            "BEST_NEXT_PROOF_BRANCH",
            "one selector theorem could set S_cg_norm and Q_m^H to zero together, which is stronger than chasing loose bounds",
        ),
        (
            "DEC1539_3_no_claim",
            "Do not promote local GR or PPN.",
            "CLAIM_BLOCKED",
            "the first-pair runner is not computable and exact silence is unsigned",
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
            "next_id": "NEXT1539_0_1540",
            "next_target": "1540-Y5-parent-coupling-selector-source-silence-attempt.md",
            "script": "scripts/Y5_parent_coupling_selector_source_silence_attempt.py",
            "objective": "try to prove the parent matter/source action is selector-blind to the local memory/cg variable so S_cg_norm=0 and Q_m^H=0; if it fails, retain the four-input finite-bound branch",
            "do_not": "do not assume coupling silence; do not set compact-source charge to zero by exterior-vacuum wording; do not claim local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (INPUT_LEDGER, QUAR_LEDGER),
        (CONDITIONAL_LEMMAS, QUAR_LEMMAS),
        (PAIR_BOUND_SCHEMA, QUAR_SCHEMA),
        (INPUT_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (INPUT_LEDGER, BRANCH_LEDGER),
        (CONDITIONAL_LEMMAS, BRANCH_LEMMAS),
        (PAIR_BOUND_SCHEMA, BRANCH_SCHEMA),
        (INPUT_RUNNER, BRANCH_RUNNER),
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
    inputs = read_csv(INPUT_LEDGER)
    lemmas = read_csv(CONDITIONAL_LEMMAS)
    schema = read_csv(PAIR_BOUND_SCHEMA)
    runner = read_csv(INPUT_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    input_symbols = {row["symbol"] for row in inputs}
    required_inputs = {"U_B_max", "S_cg_norm", "C_inner", "Q_m^H"}
    checks = [
        ("VAL1539_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1539 input source paths exist"),
        ("VAL1539_1_four_inputs", required_inputs.issubset(input_symbols), "all four first-pair inputs have acquisition rows"),
        ("VAL1539_2_Cinner_symbolic", any(row["symbol"] == "C_inner" and row["current_status"] == "SYMBOLIC_CONDITIONAL_ONLY" for row in inputs), "C_inner is symbolic only, not numeric"),
        ("VAL1539_3_product_bound_lemma", any(row["lemma_id"] == "LEMMA1539_0_Nsrc_product_bound" for row in lemmas), "N_src product bound lemma written"),
        ("VAL1539_4_boundary_bound_lemma", any(row["lemma_id"] == "LEMMA1539_1_Ninner_boundary_bound" for row in lemmas), "N_inner boundary trace lemma written"),
        ("VAL1539_5_pair_schema", any(row["schema_id"] == "SCHEMA1539_1_finite_first_pair" and "U_B_max*S_cg_norm" in row["formula"] for row in schema), "finite pair schema written"),
        ("VAL1539_6_runner_blocked", any(row["runner_id"] == "RUN1539_4_N_pair" and row["current_status"] == "NOT_COMPUTABLE" for row in runner), "first-pair runner remains noncomputable"),
        ("VAL1539_7_claim_gates_block", any(row["gate_id"] == "GATE1539_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1539_8_decision_coupling_next", any(row["result"] == "BEST_NEXT_PROOF_BRANCH" for row in decisions), "decision selects coupling selector as best next proof branch"),
        ("VAL1539_9_next_target", any("1540-Y5-parent-coupling-selector" in row["next_target"] for row in next_rows), "next target is parent coupling selector source-silence attempt"),
        ("VAL1539_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1539 CSVs parse cleanly"),
        ("VAL1539_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1539_12_branch_copies", all(path.exists() for path in [QUAR_LEDGER, QUAR_LEMMAS, QUAR_SCHEMA, QUAR_RUNNER, QUAR_DECISION, BRANCH_LEDGER, BRANCH_LEMMAS, BRANCH_SCHEMA, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1539_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1539_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1539_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1539 converts the first-pair source/inner-charge obstruction into four explicit nonclaim inputs, writes conditional product/trace lemmas, keeps N_pair noncomputable, and selects coupling selector proof next"
            if overall
            else "1539 validation failed; inspect failed rows before continuing",
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
    inputs: list[dict[str, Any]],
    lemmas: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1539 - Source Support Power and Inner Charge Input Acquisition",
                "",
                "## Verdict",
                "- The source/inner first-pair obstruction has been reduced to four explicit inputs: `U_B_max`, `S_cg_norm`, `C_inner`, and `Q_m^H`.",
                "- `C_inner` has a conditional functional-analysis shape: a boundary trace/Green constant for the selected coercive local memory operator, but it is not numeric yet.",
                "- The finite leakage schema is now `N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|`; this is a no-cancellation envelope, not a claim.",
                "- The stronger route is a parent coupling-selector theorem: if matter/source action is blind to the local memory/cg variable, then `S_cg_norm=0` and `Q_m^H=0` together.",
                "- Current status remains nonclaim: no exact source silence, no numeric leakage bound, no local GR/Newton/PPN promotion.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## First-Pair Input Acquisition Ledger",
                md_table(inputs, ["input_id", "symbol", "meaning", "definition", "units", "current_status", "blocking_detail", "acquisition_route"]),
                "",
                "## Conditional Bound Lemmas",
                md_table(lemmas, ["lemma_id", "lemma", "statement", "derivation", "status", "missing_to_promote"]),
                "",
                "## Pair Bound Schema",
                md_table(schema, ["schema_id", "schema", "formula", "current_status", "missing_to_promote"]),
                "",
                "## Input Runner",
                md_table(runner, ["runner_id", "quantity", "current_status", "reason"]),
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
    inputs = input_ledger_rows()
    lemmas = conditional_lemma_rows()
    schema = pair_bound_schema_rows()
    runner = input_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INPUT_LEDGER, inputs)
    write_csv(CONDITIONAL_LEMMAS, lemmas)
    write_csv(PAIR_BOUND_SCHEMA, schema)
    write_csv(INPUT_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        INPUT_LEDGER,
        CONDITIONAL_LEMMAS,
        PAIR_BOUND_SCHEMA,
        INPUT_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, inputs, lemmas, schema, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
