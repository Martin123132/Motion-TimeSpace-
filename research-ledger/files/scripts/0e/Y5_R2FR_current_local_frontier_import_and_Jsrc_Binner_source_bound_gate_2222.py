from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2222-Y5-R2FR-current-local-frontier-import-and-Jsrc-Binner-source-bound-gate.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_SOURCE_BOUNDARY_FRONTIER_2222"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2221_doc": ROOT / "2221-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md",
    "2221_validation": OUT / "P8_Y5_BRR545_2221_VALIDATION.csv",
    "2221_next": OUT / "P8_Y5_PARENT_QLOC_2221_NEXT_TARGET.csv",
    "1537_doc": ROOT / "1537-Y5-Jeff-Bm-component-norm-input-pack.md",
    "1537_validation": OUT / "P8_Y5_BRR545_1537_VALIDATION.csv",
    "1537_norm_pack": OUT / "P8_Y5_PARENT_QLOC_1537_COMPONENT_NORM_INPUT_PACK.csv",
    "1537_first_priority": OUT / "P8_Y5_PARENT_QLOC_1537_FIRST_PRIORITY_NORM_ROWS.csv",
    "1538_doc": ROOT / "1538-Y5-source-support-and-inner-charge-theorem-or-bound.md",
    "1538_validation": OUT / "P8_Y5_BRR545_1538_VALIDATION.csv",
    "1538_nsrc": OUT / "P8_Y5_PARENT_QLOC_1538_N_SRC_THEOREM_OR_BOUND.csv",
    "1538_ninner": OUT / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv",
    "1538_pair": OUT / "P8_Y5_PARENT_QLOC_1538_PAIR_NORM_RUNNER.csv",
    "1539_doc": ROOT / "1539-Y5-source-support-power-and-inner-charge-input-acquisition.md",
    "1539_validation": OUT / "P8_Y5_BRR545_1539_VALIDATION.csv",
    "1539_inputs": OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv",
    "1539_lemmas": OUT / "P8_Y5_PARENT_QLOC_1539_CONDITIONAL_BOUND_LEMMAS.csv",
    "1539_schema": OUT / "P8_Y5_PARENT_QLOC_1539_PAIR_BOUND_SCHEMA_NONCLAIM.csv",
    "1540_doc": ROOT / "1540-Y5-parent-coupling-selector-source-silence-attempt.md",
    "1540_validation": OUT / "P8_Y5_BRR545_1540_VALIDATION.csv",
    "1540_theorem": OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
    "1540_variation": OUT / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv",
    "1540_payoff": OUT / "P8_Y5_PARENT_QLOC_1540_SOURCE_SILENCE_PAYOFF.csv",
    "1540_next": OUT / "P8_Y5_PARENT_QLOC_1540_NEXT_TARGET.csv",
    "1541_doc": ROOT / "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2222_SOURCE_REGISTER.csv"
FRONTIER_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2222_FRONTIER_IMPORT_AUDIT.csv"
FIRST_PAIR_STATUS = OUT / "P8_Y5_PARENT_QLOC_2222_FIRST_PAIR_INPUT_STATUS.csv"
PAIR_BOUND_GATE = OUT / "P8_Y5_PARENT_QLOC_2222_NPAIR_BOUND_GATE.csv"
COUPLING_GATE = OUT / "P8_Y5_PARENT_QLOC_2222_COUPLING_SELECTOR_IMPORT_GATE.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2222_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2222_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2222_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2222_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2222_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2222_SOURCE_BOUNDARY_FIRST_PAIR_FRONTIER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "source_boundary_first_pair_frontier_nonclaim_2222.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_SOURCE_BOUNDARY_FIRST_PAIR_FRONTIER_2222_NONCLAIM.csv",
}


def flags() -> dict[str, bool]:
    return {
        "premise_signed": False,
        "theorem_closed": False,
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


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "premise_signed",
        "theorem_closed",
        "numeric_value_present",
        "parent_signed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2222_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2222" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "input evidence"
        if key.startswith("2221"):
            role = "current R2FR handoff selecting first source-boundary targets"
        elif key.startswith("1537"):
            role = "component norm slot frontier"
        elif key.startswith("1538"):
            role = "first-pair theorem-or-bound frontier"
        elif key.startswith("1539"):
            role = "four-input acquisition frontier"
        elif key.startswith("1540"):
            role = "coupling selector theorem attempt and failure"
        elif key.startswith("1541"):
            role = "known next quotient-map target to avoid duplicate next work"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2222_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def frontier_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "FRONT2222_0_1537",
            "1537 component norm pack",
            "all J_eff/B_m pieces receive nonclaim norm slots; N_src and N_inner marked first priority",
            "IMPORTED_VALID_FRONTIER",
            "no component norm is numeric or theorem-zero",
        ),
        (
            "FRONT2222_1_1538",
            "1538 first-pair theorem-or-bound",
            "N_src exact-zero routes and finite product bound written; N_inner exact-zero routes and finite charge bound written",
            "IMPORTED_VALID_FRONTIER",
            "zero routes unsigned and finite route lacks U_B_max, S_cg_norm, C_inner, Q_mH",
        ),
        (
            "FRONT2222_2_1539",
            "1539 four-input acquisition",
            "first-pair obstruction reduced to U_B_max, S_cg_norm, C_inner, and Q_m^H",
            "IMPORTED_VALID_FRONTIER",
            "C_inner only symbolic; other three inputs missing; N_pair not computable",
        ),
        (
            "FRONT2222_3_1540",
            "1540 coupling selector attempt",
            "conditional theorem identifies how S_cg_norm and Q_m^H could vanish together",
            "IMPORTED_FAILURE_AS_NEXT_PROOF_GUIDE",
            "q map, vertical generator, source-normalization descent and boundary silence unsigned",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "frontier_id": frontier_id,
            "checkpoint": checkpoint,
            "imported_result": result,
            "current_2222_status": status,
            "remaining_blocker": blocker,
            **flags(),
        }
        for frontier_id, checkpoint, result, status, blocker in entries
    ]


def first_pair_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "PAIR2222_0_U_B_max",
            "U_B_max",
            "source-support leakage amplitude",
            "MISSING_PARENT_PROJECTOR_VALUE",
            "cannot bound N_src without Pi_B/support theorem or external conservative bound",
            "derive projector support theorem or retain finite residual input",
        ),
        (
            "PAIR2222_1_S_cg_norm",
            "S_cg_norm",
            "dual norm of compact-source forcing into memory/cg sector",
            "MISSING_SOURCE_CURRENT_PROJECTION",
            "the selector theorem would set this to zero, but Dq[v_m] and direct/source-normalization silence are unsigned",
            "prove coupling selector or source compact-body current norm",
        ),
        (
            "PAIR2222_2_C_inner",
            "C_inner",
            "boundary-to-energy trace/Green constant",
            "SYMBOLIC_CONDITIONAL_ONLY",
            "functional-analysis shape exists after operator/domain/boundary normalization but no numeric value is present",
            "derive trace lemma for selected local memory operator and excision geometry",
        ),
        (
            "PAIR2222_3_Q_mH",
            "Q_m^H",
            "compact-source inner memory charge/monopole flux",
            "MISSING_PARENT_CHARGE_OR_ZERO_THEOREM",
            "selector theorem or boundary/no-flux theorem could zero it, but neither is signed",
            "prove charge silence or retain finite compact-source charge row",
        ),
        (
            "PAIR2222_4_N_pair",
            "N_pair",
            "first source-boundary leakage pair",
            "SCHEMA_READY_NOT_COMPUTABLE",
            "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|, with all nonnegative inputs unsourced",
            "fill at least one exact-zero theorem or four finite inputs",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "meaning": meaning,
            "current_status": status,
            "reason": reason,
            "next_action": next_action,
            **flags(),
        }
        for row_id, symbol, meaning, status, reason, next_action in entries
    ]


def pair_bound_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "NPAIR2222_0_exact_source",
            "N_src=0",
            "U_B=0, projected S_cg=0, or selector-blind matter/source action",
            "BLOCKED",
            "no parent support/projector or selector theorem is closed",
        ),
        (
            "NPAIR2222_1_exact_inner",
            "N_inner=0",
            "Q_m^H=0, source/projection silence, or parent no-flux boundary condition",
            "BLOCKED",
            "inner charge and boundary certificate remain open",
        ),
        (
            "NPAIR2222_2_finite_pair",
            "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "absolute first-pair leakage bound",
            "FORMULA_ONLY_NOT_NUMERIC",
            "U_B_max, S_cg_norm, C_inner, Q_m^H missing or symbolic",
        ),
        (
            "NPAIR2222_3_selector_payoff",
            "selector theorem payoff",
            "if Dq[v_m]=0 plus direct/source/boundary silence, then S_cg_norm=0 and Q_m^H=0",
            "CONDITIONAL_NOT_LIVE",
            "matter stress term makes Dq[v_m]=0 unavoidable",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "object": obj,
            "condition_or_formula": formula,
            "status": status,
            "blocker": blocker,
            **flags(),
        }
        for gate_id, obj, formula, status, blocker in entries
    ]


def coupling_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "CSEL2222_0_identity",
            "delta_v S_matter=<delta S_matter/delta q,Dq[v_m]>+(partial_m S_matter)_q delta m",
            "PASS_CONDITIONAL_IDENTITY",
            "shows why ordinary matter stress cannot be ignored",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv",
        ),
        (
            "CSEL2222_1_selector_theorem",
            "q-only matter/source descent plus v_m in ker(Dq) plus boundary silence",
            "THEOREM_ATTEMPT_NOT_CLOSED",
            "would zero S_cg_norm and Q_m^H together",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
        ),
        (
            "CSEL2222_2_core_blocker",
            "define q and prove Dq[v_m]=0",
            "NEXT_CORE_OBJECT",
            "without verticality, nonzero Hilbert stress sources the memory/cg channel",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1540_NEXT_TARGET.csv",
        ),
        (
            "CSEL2222_3_fallback",
            "finite coupling leakage row",
            "RETAIN_IF_KERNEL_FAILS",
            "if Dq[v_m] is nonzero, S_cg_norm must be bounded rather than zeroed",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1540_COUPLING_FAILURE_LEDGER.csv",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "selector_id": selector_id,
            "statement": statement,
            "status": status,
            "meaning": meaning,
            "source_path": source_path,
            **flags(),
        }
        for selector_id, statement, status, meaning, source_path in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2222_0_frontier_import", "1537-1540 frontier imported", "PASS_NONCLAIM", "validated old frontier is connected to current R2FR numbering"),
        ("CG2222_1_Nsrc", "N_src zero or finite bound", "BLOCKED_NONCLAIM", "U_B_max and S_cg_norm missing; selector theorem unsigned"),
        ("CG2222_2_Ninner", "N_inner zero or finite bound", "BLOCKED_NONCLAIM", "C_inner symbolic and Q_m^H missing; boundary silence unsigned"),
        ("CG2222_3_Npair", "first-pair leakage computable", "BLOCKED_NONCLAIM", "formula exists but nonnegative inputs missing"),
        ("CG2222_4_selector", "coupling selector closes", "BLOCKED_NONCLAIM", "q map and Dq[v_m] certificate missing"),
        ("CG2222_5_local_lock", "local memory locking/no-hair or score-ready leakage", "BLOCKED_NONCLAIM", "N_lock cannot be computed from first pair"),
        ("CG2222_6_local_GR", "derived local GR/Newton/PPN recovery", "BLOCKED_NO_CLAIM", "source-boundary, hidden Kmetric and projection gates remain open"),
        ("CG2222_7_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private branch remains mid-proof"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2222_0_progress",
            "Import 1537-1540 rather than duplicate them.",
            "FRONTIER_CONNECTED",
            "the source-boundary branch already reached a four-input obstruction and a coupling-selector attempt",
        ),
        (
            "DEC2222_1_first_pair",
            "Do not claim N_src or N_inner zero/bounded.",
            "FIRST_PAIR_BLOCKED",
            "the finite formula is sharp, but every exact-zero/numeric input remains unsigned or symbolic",
        ),
        (
            "DEC2222_2_coupling",
            "The coupling selector is the best proof route.",
            "Q_MAP_KERNEL_IS_CORE",
            "one theorem for q-only descent plus Dq[v_m]=0 could remove both S_cg_norm and Q_m^H",
        ),
        (
            "DEC2222_3_guardrail",
            "Do not use matter equations of motion to hide the stress term.",
            "STRESS_SHORTCUT_REJECTED",
            "ordinary matter stress is nonzero, so verticality is a real requirement",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2222_0_2223",
            "target_file": "2223-Y5-R2FR-quotient-map-vertical-generator-frontier-import-or-finite-coupling-row.md",
            "target_script": "scripts/Y5_R2FR_quotient_map_vertical_generator_frontier_import_or_finite_coupling_row_2223.py",
            "objective": "inspect/import the existing 1541 quotient-map vertical-generator certificate and decide whether Dq[v_m]=0 closes or whether a finite coupling leakage row must be retained for S_cg_norm",
            "success_condition": "Dq[v_m]=0 is parent-signed in the same branch, or a finite nonclaim coupling residual row is emitted with all missing clauses explicit",
            "do_not": "do not rely on matter equations of motion to kill stress; do not assume verticality; do not claim source silence, local lock, or local GR",
            **flags(),
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for copy_id, destination in COPY_TARGETS.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIRST_PAIR_STATUS, destination)
        copied.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(FIRST_PAIR_STATUS),
                "target_path": rel(destination),
                "copied": destination.exists(),
                "parse_ok": parse_csv(destination),
                **flags(),
            }
        )
    return copied


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    frontier = read_csv(FRONTIER_IMPORT)
    first_pair = read_csv(FIRST_PAIR_STATUS)
    pair_gate = read_csv(PAIR_BOUND_GATE)
    coupling = read_csv(COUPLING_GATE)
    claims = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    copies = read_csv(BRANCH_COPIES)
    required_symbols = {"U_B_max", "S_cg_norm", "C_inner", "Q_m^H", "N_pair"}
    checks = [
        ("VAL2222_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited 2222 source paths exist"),
        ("VAL2222_01_prior_validations", all(row["validation_overall_pass"] in {"", "True"} for row in sources), "all imported validation files pass overall"),
        ("VAL2222_02_frontier_import", len(frontier) == 4 and any(row["checkpoint"].startswith("1540") for row in frontier), "1537-1540 frontier imported"),
        ("VAL2222_03_four_inputs", required_symbols.issubset({row["symbol"] for row in first_pair}), "four first-pair inputs plus N_pair recorded"),
        ("VAL2222_04_Cinner_symbolic", any(row["symbol"] == "C_inner" and row["current_status"] == "SYMBOLIC_CONDITIONAL_ONLY" for row in first_pair), "C_inner remains symbolic, not numeric"),
        ("VAL2222_05_Npair_blocked", any(row["object"] == "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|" and row["status"] == "FORMULA_ONLY_NOT_NUMERIC" for row in pair_gate), "N_pair finite formula is nonnumeric"),
        ("VAL2222_06_selector_blocker", any(row["selector_id"] == "CSEL2222_2_core_blocker" and row["status"] == "NEXT_CORE_OBJECT" for row in coupling), "q-map/Dq[v_m] core blocker selected"),
        ("VAL2222_07_claims_blocked", any(row["gate_id"] == "CG2222_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in claims), "local GR claim remains blocked"),
        ("VAL2222_08_decision", any(row["result"] == "Q_MAP_KERNEL_IS_CORE" for row in decisions), "decision identifies q-map kernel as core route"),
        ("VAL2222_09_next_target", any("2223-Y5-R2FR-quotient-map" in row["target_file"] for row in next_target), "next target imports quotient-map frontier"),
        ("VAL2222_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2222 CSVs parse cleanly"),
        ("VAL2222_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated flags remain nonclaim"),
        ("VAL2222_12_branch_copies", all(row["copied"] == "True" and row["parse_ok"] == "True" for row in copies), "branch copies written and parse"),
        ("VAL2222_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2222_14_formalization_no_2222", formalization_2222_artifacts_absent(), "formalization-workbench has no 2222 artifacts"),
        ("VAL2222_15_formalization_untouched", formalization_untouched_since_start(), "formalization-workbench untouched during 2222 run"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            **flags(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2222_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "2222 imports the 1537-1540 source-boundary frontier, keeps N_src/N_inner/N_pair nonclaim, identifies q and Dq[v_m] as the next core coupling object, and preserves local-GR blockage"
            if overall
            else "2222 validation failed; inspect failed rows before continuing",
            **flags(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    frontier: list[dict[str, Any]],
    first_pair: list[dict[str, Any]],
    pair_gate: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2222 - Y5/R2FR Current Local Frontier Import And Jsrc/Binner Source-Bound Gate",
                "",
                "## Verdict",
                "- 2222 imports the existing `1537-1540` local source-boundary frontier into the current R2FR numbering.",
                "- The first-pair obstruction is sharp: `N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|`.",
                "- It is not score-ready: `U_B_max`, `S_cg_norm`, and `Q_m^H` are missing, while `C_inner` is symbolic only.",
                "- The best proof route is the coupling-selector theorem, but 1540 shows the hard condition is real: define `q` and prove `Dq[v_m]=0`.",
                "- Local lock, local GR, Newton, PPN, R10, WEP, clocks, and orbital claims remain blocked/nonclaim.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
                "",
                "## Frontier Import Audit",
                md_table(frontier, ["frontier_id", "checkpoint", "imported_result", "current_2222_status", "remaining_blocker"]),
                "",
                "## First Pair Input Status",
                md_table(first_pair, ["row_id", "symbol", "meaning", "current_status", "reason", "next_action"]),
                "",
                "## N Pair Bound Gate",
                md_table(pair_gate, ["gate_id", "object", "condition_or_formula", "status", "blocker"]),
                "",
                "## Coupling Selector Import Gate",
                md_table(coupling, ["selector_id", "statement", "status", "meaning", "source_path"]),
                "",
                "## Claim Gate",
                md_table(claims, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision Ledger",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Next Target",
                md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
                "",
                "## Branch Copies",
                md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Working Interpretation",
                "",
                "The coupling worry was not a side issue; it is now the central local-GR obstruction. The good news is that it has a clean mathematical contract. The bad news is that the contract requires the real quotient map and vertical generator, not wording. That is exactly the next pressure point.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    frontier = frontier_rows()
    first_pair = first_pair_rows()
    pair_gate = pair_bound_rows()
    coupling = coupling_rows()
    claims = claim_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FRONTIER_IMPORT, frontier)
    write_csv(FIRST_PAIR_STATUS, first_pair)
    write_csv(PAIR_BOUND_GATE, pair_gate)
    write_csv(COUPLING_GATE, coupling)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_outputs()
    write_csv(BRANCH_COPIES, copies)
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        FRONTIER_IMPORT,
        FIRST_PAIR_STATUS,
        PAIR_BOUND_GATE,
        COUPLING_GATE,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
        BRANCH_COPIES,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, frontier, first_pair, pair_gate, coupling, claims, decisions, next_target, copies, validation)


if __name__ == "__main__":
    main()
