from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2761-Y5-R2FR-first-same-branch-coupling-product-row-balpha-clock-or-deltaw-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2761_SOURCE_REGISTER.csv",
    "candidates": MTS / "P8_Y5_R2FR_2761_SAME_BRANCH_PRODUCT_CANDIDATE_MATRIX.csv",
    "contract": MTS / "P8_Y5_R2FR_2761_PRODUCT_CONTRACT_LEDGER.csv",
    "transfer": MTS / "P8_Y5_R2FR_2761_TRANSFER_GATE_MATRIX.csv",
    "delta": MTS / "P8_Y5_R2FR_2761_DELTA_W_FALLBACK_AUDIT.csv",
    "arena": MTS / "P8_Y5_R2FR_2761_LOCAL_RESIDUAL_INSERTION_MAP.csv",
    "decisions": MTS / "P8_Y5_R2FR_2761_DECISION_LEDGER.csv",
    "gates": MTS / "P8_Y5_R2FR_2761_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2761_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2761_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2761_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2761_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidates_queue": RAB_QUEUE / "JR2761_FIRST_SAME_BRANCH_COUPLING_PRODUCT_CANDIDATES_NONCLAIM.csv",
    "contract_queue": RAB_QUEUE / "JR2761_PRODUCT_CONTRACT_LEDGER_NONCLAIM.csv",
    "transfer_beta": BETA_DOCS / "FIRST_SAME_BRANCH_COUPLING_PRODUCT_TRANSFER_GATES_2761_NONCLAIM.csv",
    "arena_local": LOCAL_BOUNDS / "first_same_branch_coupling_product_local_residual_map_2761_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2761_TAU_WEP_BETA_SOURCE_NEXT_TARGET.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            cells.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2761_00_2760_doc", "2760_doc", WORK / "2760-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior-under-AX1090.md", ["NEXT2760_0_2761", "FCP2760_0_b_alpha", "FCP2760_3_delta_w_A"], "2760 handoff to first same-branch finite product"),
        ("SRC2761_01_2760_validation", "2760_validation", MTS / "P8_Y5_BRR545_2760_VALIDATION.csv", ["VAL2760_OVERALL"], "2760 validation"),
        ("SRC2761_02_2319_rows", "2319_source_backed_rows", MTS / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv", ["FCR2319_0_clock_product_best", "FCR2319_3_delta_w_missing_prediction"], "first source-backed nonclaim rows"),
        ("SRC2761_03_1052_doc", "1052_tau_projection_doc", WORK / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md", ["TCN1052_4_verdict", "AWP1052_0_alpha_Coulomb", "RAP1052_0_product_law"], "tau clock and alpha WEP/R10 projection precedent"),
        ("SRC2761_04_1052_clock_bound", "1052_clock_bound_csv", MTS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", ["ACB1052_2"], "source-backed clock product bound"),
        ("SRC2761_05_1052_tau", "1052_tau_csv", MTS / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv", ["TCN1052_4_verdict"], "tau/Xhat normalization blockage"),
        ("SRC2761_06_1052_WEP", "1052_wep_csv", MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", ["AWP1052_0_alpha_Coulomb"], "WEP alpha pressure target"),
        ("SRC2761_07_1052_R10", "1052_r10_csv", MTS / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", ["RAP1052_0_product_law"], "R10 product law requirements"),
        ("SRC2761_08_1092_doc", "1092_hidden_triviality_doc", WORK / "1092-Y5-R10-hidden-invariant-algebra-triviality-or-balpha-tau-projection.md", ["BTP1092_0_best_clock_product", "TRG1092_2_clock_to_WEP"], "clock fallback and transfer gates"),
        ("SRC2761_09_1053_doc", "1053_beta_tau_doc", WORK / "1053-Y5-R10-beta-source-alpha-and-tau-WEP-R10-source-chain.md", ["BSA1053_2_alpha_Coulomb_bound_target", "TPR1053_4_verdict"], "beta_source_alpha/tau_WEP/R10 source chain"),
        ("SRC2761_10_1490_doc", "1490_delta_w_doc", WORK / "1490-Y5-R10-RAB-source-coefficient-target-exclusion-or-hidden-invariant-algebra-triviality.md", ["DWR1490_6_claim_gate", "LRS1490_4_verdict"], "delta_w requirements and local block"),
        ("SRC2761_11_local_bounds", "local_bounds", WORK / "source-intake" / "local_bounds" / "local_bound_claims.csv", ["R1_WEP_source_charge"], "MICROSCOPE comparator bound"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        needles_found = exists and all(needle in text for needle in needles)
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": needles_found,
            "source_role": role,
        }))
    return rows


def load_inputs() -> dict[str, dict[str, str]]:
    return {
        "clock_2319": find_row(read_csv_rows(MTS / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv"), "row_id", "FCR2319_0_clock_product_best"),
        "delta_2319": find_row(read_csv_rows(MTS / "P8_Y5_PARENT_QLOC_2319_SOURCE_BACKED_FINITE_COUPLING_ROWS_NONCLAIM.csv"), "row_id", "FCR2319_3_delta_w_missing_prediction"),
        "clock_1052": find_row(read_csv_rows(MTS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"), "bound_id", "ACB1052_2"),
        "tau_1052": find_row(read_csv_rows(MTS / "P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv"), "tau_id", "TCN1052_4_verdict"),
        "wep_1052": find_row(read_csv_rows(MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"), "projection_id", "AWP1052_0_alpha_Coulomb"),
        "r10_1052": find_row(read_csv_rows(MTS / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"), "projection_id", "RAP1052_0_product_law"),
        "wep_bound": find_row(read_csv_rows(WORK / "source-intake" / "local_bounds" / "local_bound_claims.csv"), "row_id", "R1_WEP_source_charge"),
    }


def build_candidate_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    clock_2319 = inputs["clock_2319"]
    clock_1052 = inputs["clock_1052"]
    wep_1052 = inputs["wep_1052"]
    r10_1052 = inputs["r10_1052"]
    delta_2319 = inputs["delta_2319"]
    return [
        nonclaim({
            "row_id": "SBC2761_0_clock_product_admitted",
            "candidate": "b_alpha*tau_clock_time",
            "sector": "clock_alpha_product",
            "numeric_value": clock_2319.get("numeric_value", clock_1052.get("product_bound_1sigma_yr_inv", "MISSING")),
            "units": clock_2319.get("units", "yr^-1"),
            "source_path": clock_2319.get("source_path", str(MTS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv")),
            "source_row_id": clock_2319.get("source_row_id", "ACB1052_2"),
            "same_branch_status": "CLOCK_PRODUCT_BRANCH_LOCKED_NONCLAIM",
            "local_residual_status": "NOT_INSERTABLE_IN_LOCAL_GR_VECTOR",
            "score_ready": False,
            "reason": "source-backed product bound exists, but it is clock-only and not standalone b_alpha",
        }),
        nonclaim({
            "row_id": "SBC2761_1_H0_diagnostic_only",
            "candidate": "b_alpha*dchi_X/dN",
            "sector": "clock_alpha_diagnostic",
            "numeric_value": clock_1052.get("H0_normalized_diagnostic", "MISSING"),
            "units": "dimensionless if tau_clock_time=H0*dchi_X/dN is assumed",
            "source_path": str(MTS / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"),
            "source_row_id": "ACB1052_2",
            "same_branch_status": "DIAGNOSTIC_ONLY_NOT_PARENT_DERIVED",
            "local_residual_status": "FORBIDDEN_AS_THEORY_INPUT",
            "score_ready": False,
            "reason": "H0-normalized value depends on an unsigned tau-clock/Xhat identification",
        }),
        nonclaim({
            "row_id": "SBC2761_2_WEP_alpha_pressure_target",
            "candidate": "beta_source_alpha*b_alpha*tau_WEP",
            "sector": "WEP_alpha_source_product",
            "numeric_value": wep_1052.get("required_abs_beta_source_max", "MISSING"),
            "units": "dimensionless normalized product ceiling",
            "source_path": str(MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"),
            "source_row_id": "AWP1052_0_alpha_Coulomb",
            "same_branch_status": "TARGET_ONLY_NOT_MTS_PREDICTION",
            "local_residual_status": "NEEDS_BETA_SOURCE_ALPHA_AND_TAU_WEP",
            "score_ready": False,
            "reason": "WEP supplies a pressure target, not beta_source_alpha or tau_WEP",
        }),
        nonclaim({
            "row_id": "SBC2761_3_delta_w_missing",
            "candidate": "delta_w_A",
            "sector": "source_weight",
            "numeric_value": delta_2319.get("numeric_value", "MISSING_SOURCE_BACKED_VALUE"),
            "units": delta_2319.get("units", "dimensionless"),
            "source_path": delta_2319.get("source_path", str(MTS / "P8_Y5_R10_1490_DELTA_W_REAL_INPUT_REQUIREMENTS.csv")),
            "source_row_id": delta_2319.get("source_row_id", "DWR1490_6_claim_gate"),
            "same_branch_status": "PREDICTION_MISSING",
            "local_residual_status": "NOT_INSERTABLE_IN_LOCAL_GR_VECTOR",
            "score_ready": False,
            "reason": "delta_w has comparator/requirements only; no material/source/tau projection value",
        }),
        nonclaim({
            "row_id": "SBC2761_4_R10_product_missing",
            "candidate": "K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "sector": "R10_finite_range_product",
            "numeric_value": "MISSING_LAMBDA_KX_BETA_TAU_R10",
            "units": "dimensionless alpha(lambda)",
            "source_path": str(MTS / "P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv"),
            "source_row_id": "RAP1052_0_product_law",
            "same_branch_status": "SCHEMA_ONLY",
            "local_residual_status": "R10_SCORE_BLOCKED",
            "score_ready": False,
            "reason": r10_1052.get("missing_inputs", "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; promoted bound curve"),
        }),
    ]


def build_contract_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    tau_1052 = inputs["tau_1052"]
    return [
        nonclaim({"row_id": "CON2761_0_clock_observable", "contract_piece": "clock product definition", "mathematical_form": "d ln R_ij/dt = DeltaK_alpha^ij * b_alpha * tau_clock_time + retained mass/nuclear terms", "status": "PRODUCT_CONSTRAINT_SOURCE_BACKED", "current_value": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1", "missing_for_claim": "standalone b_alpha and parent tau_clock_time"}),
        nonclaim({"row_id": "CON2761_1_tau_clock", "contract_piece": "tau_clock_time ownership", "mathematical_form": tau_1052.get("mathematical_form", "tau_clock_time := d chi_X/dt"), "status": tau_1052.get("derivation_status", "DEFINED_PRODUCT_MAP_NOT_PARENT_DERIVED"), "current_value": "clock product usable only as product", "missing_for_claim": tau_1052.get("blocking_gap", "chi_X parent state and local time projection are not derived")}),
        nonclaim({"row_id": "CON2761_2_same_branch_lock", "contract_piece": "same-branch export rule", "mathematical_form": "clock, WEP, R10, PPN, and local residual rows may share b_alpha only if Xhat/chi_X normalization and projection taus are one parent map", "status": "EXPORT_BLOCKED", "current_value": "clock product branch locked; WEP/R10 products target-only", "missing_for_claim": "shared tau_clock/tau_WEP/tau_R10 theorem or independent theorem-zero rows"}),
        nonclaim({"row_id": "CON2761_3_delta_w_contract", "contract_piece": "source-weight product definition", "mathematical_form": "eta_AB ~= sum_i DeltaQ_i(AB) delta_w_i tau_i with readout/source transfer", "status": "REQUIRED_INPUTS_MISSING", "current_value": "no numeric delta_w_A prediction row", "missing_for_claim": "material/source charge basis, tau_i, readout transfer, no-cancellation group"}),
        nonclaim({"row_id": "CON2761_4_local_insertion_contract", "contract_piece": "local residual insertion", "mathematical_form": "local residual vector may receive only theorem-zero or same-branch finite products with source paths/units/projection", "status": "NOT_SATISFIED", "current_value": "clock product does not insert into local GR vector", "missing_for_claim": "tau_WEP/beta_source_alpha or delta_w material vector tied to j_q/local residual"}),
    ]


def build_transfer_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    wep_1052 = inputs["wep_1052"]
    r10_1052 = inputs["r10_1052"]
    return [
        nonclaim({"row_id": "TR2761_0_clock_internal", "transfer": "clock product used in clock arena", "gate_status": "PASS_NONCLAIM_ONLY", "reason": "source-backed clock product exists", "needed_to_promote": "tau_clock_time parent derivation; alpha owner; mass/nuclear split", "claim_allowed": False}),
        nonclaim({"row_id": "TR2761_1_clock_to_balpha", "transfer": "clock product gives standalone b_alpha", "gate_status": "FAIL", "reason": "tau_clock_time and Xhat/chi_X normalization are not derived", "needed_to_promote": "parent-owned tau_clock_time or independent b_alpha source", "claim_allowed": False}),
        nonclaim({"row_id": "TR2761_2_clock_to_WEP", "transfer": "clock product exports to WEP alpha/source charge", "gate_status": "FAIL", "reason": "requires beta_source_alpha, tau_WEP, material model, and shared domain rule", "needed_to_promote": wep_1052.get("missing_for_claim", "beta_source_alpha theorem/prior; tau_WEP; shared domain rule; full material model"), "claim_allowed": False}),
        nonclaim({"row_id": "TR2761_3_clock_to_R10", "transfer": "clock product exports to R10 alpha(lambda)", "gate_status": "FAIL", "reason": "R10 product has its own source/test/profile/readout projection", "needed_to_promote": r10_1052.get("missing_inputs", "lambda_X; Z_X; K_X(lambda); beta_s; beta_t; alpha projection; promoted bound curve"), "claim_allowed": False}),
        nonclaim({"row_id": "TR2761_4_delta_to_local", "transfer": "delta_w comparator bound gives local source-weight prediction", "gate_status": "FAIL", "reason": "comparator bound is not an MTS delta_w prediction", "needed_to_promote": "official material/source vector, tau_eff, readout transfer, source path, no-cancellation group", "claim_allowed": False}),
        nonclaim({"row_id": "TR2761_5_mixed_branch_guard", "transfer": "mix R2/f(R) clock product with R10/WEP branch placeholders", "gate_status": "FAIL_GUARD", "reason": "branch IDs, projection taus, and operator normalizations differ", "needed_to_promote": "single parent branch map or explicit bridge theorem", "claim_allowed": False}),
    ]


def build_delta_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    wep_bound = inputs["wep_bound"]
    return [
        nonclaim({"row_id": "DW2761_0_MICROSCOPE_bound", "quantity": "eta_WEP_source_charge_bound", "arena": "MICROSCOPE_TiPt", "current_value": wep_bound.get("upper_bound", "2.8e-15"), "units": wep_bound.get("units", "dimensionless"), "source_basis": wep_bound.get("reference_path_or_url", "local_bound_claims.csv"), "usable_as": "comparator bound only", "missing_for_prediction": "delta_w_A source/material projection"}),
        nonclaim({"row_id": "DW2761_1_delta_w_prediction", "quantity": "delta_w_A", "arena": "WEP/Newton/source", "current_value": "MISSING_SOURCE_BACKED_VALUE", "units": "dimensionless", "source_basis": "DWR1490_6_claim_gate", "usable_as": "acquisition target", "missing_for_prediction": "material/source vector, tau_eff, readout transfer"}),
        nonclaim({"row_id": "DW2761_2_clock_vs_delta", "quantity": "clock product vs delta_w", "arena": "cross_arena_policy", "current_value": "not comparable", "units": "n/a", "source_basis": "2760/1052/1490 gates", "usable_as": "branch guard", "missing_for_prediction": "shared parent normalization theorem"}),
        nonclaim({"row_id": "DW2761_3_verdict", "quantity": "delta_w first product row", "arena": "all local source-weight arenas", "current_value": "NOT_READY", "units": "n/a", "source_basis": "1490 plus 2319", "usable_as": "next acquisition route", "missing_for_prediction": "first numeric/source-backed delta_w or theorem-zero"}),
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "ARENA2761_0_clock", "arena": "clock", "inserted_row": "SBC2761_0_clock_product_admitted", "status": "SOURCE_BACKED_NONCLAIM_PRODUCT", "residual_effect": "bounds clock alpha drift product only", "score_ready": False}),
        nonclaim({"row_id": "ARENA2761_1_WEP", "arena": "WEP/MICROSCOPE", "inserted_row": "SBC2761_2_WEP_alpha_pressure_target", "status": "TARGET_ONLY_NO_MTS_VALUE", "residual_effect": "sets pressure target for beta_source_alpha*b_alpha*tau_WEP", "score_ready": False}),
        nonclaim({"row_id": "ARENA2761_2_R10", "arena": "R10 short range", "inserted_row": "SBC2761_4_R10_product_missing", "status": "SCHEMA_ONLY", "residual_effect": "no alpha(lambda) prediction", "score_ready": False}),
        nonclaim({"row_id": "ARENA2761_3_PPN_local", "arena": "PPN/local GR", "inserted_row": "none", "status": "NO_LOCAL_COMPONENT_INSERTION", "residual_effect": "clock product cannot be used as local-GR residual component", "score_ready": False}),
        nonclaim({"row_id": "ARENA2761_4_Newton_orbital", "arena": "Newton/orbital source normalization", "inserted_row": "SBC2761_3_delta_w_missing", "status": "SOURCE_WEIGHT_PREDICTION_MISSING", "residual_effect": "observed GM/source-weight channel remains open", "score_ready": False}),
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2761_0_clock_product", "decision": "admit b_alpha*tau_clock_time as first source-backed finite product row", "because": "it has positive numeric bound, units, source rows, and a clear product definition", "next_action": "keep it clock-only until tau_clock_time is parent-owned"}),
        nonclaim({"row_id": "DEC2761_1_no_export", "decision": "do not export the clock product into WEP/R10/local GR", "because": "tau_WEP, tau_R10, beta_source_alpha, source/test charges, and shared normalization are missing", "next_action": "build a same-branch WEP/source projection row"}),
        nonclaim({"row_id": "DEC2761_2_delta_w", "decision": "delta_w is not ready as the first product row", "because": "comparator bounds exist but the MTS prediction row is missing", "next_action": "use delta_w as acquisition target, not score input"}),
        nonclaim({"row_id": "DEC2761_3_best_route", "decision": "the best next attack is tau_WEP/material-source projection or beta_source_alpha zero/prior", "because": "this is the shortest bridge from clock product evidence to local source-current tests without cheating", "next_action": "derive zero or source first numeric product beta_source_alpha*b_alpha*tau_WEP"}),
        nonclaim({"row_id": "DEC2761_4_next", "decision": "NEXT_2762_TAU_WEP_MATERIAL_SOURCE_OR_BETA_SOURCE_ALPHA_ZERO", "because": "2761 gives a real product row but not a local residual insertion", "next_action": "target tau_WEP/material/source tensor or beta_source_alpha theorem-zero under AX1090"}),
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2761_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2761_1_clock_product_numeric", "gate": "clock product row has positive numeric bound", "passed": True, "claim_effect": "first finite product row can be retained as nonclaim"}),
        nonclaim({"row_id": "CG2761_2_standalone_balpha", "gate": "standalone b_alpha derived", "passed": False, "claim_effect": "clock product cannot become coefficient claim"}),
        nonclaim({"row_id": "CG2761_3_WEP_product", "gate": "beta_source_alpha*b_alpha*tau_WEP same-branch product sourced", "passed": False, "claim_effect": "WEP/local source-current score blocked"}),
        nonclaim({"row_id": "CG2761_4_R10_product", "gate": "R10 alpha(lambda) product sourced", "passed": False, "claim_effect": "R10 score blocked"}),
        nonclaim({"row_id": "CG2761_5_delta_w_prediction", "gate": "delta_w_A prediction sourced", "passed": False, "claim_effect": "Newton/source-weight score blocked"}),
        nonclaim({"row_id": "CG2761_6_local_GR_Newton", "gate": "local GR/Newton residual vector complete", "passed": False, "claim_effect": "no local-GR/Newton claim from 2761"}),
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2761_0_standalone_balpha", "claim": "clock row gives standalone b_alpha", "allowed": False, "reason": "the row bounds only b_alpha*tau_clock_time and tau_clock_time is not parent-derived", "blocking_rows": "CON2761_1_tau_clock;TR2761_1_clock_to_balpha"}),
        nonclaim({"row_id": "REF2761_1_clock_export", "claim": "clock product can be used directly in WEP/R10/local tests", "allowed": False, "reason": "projection taus and source/test/material factors are missing", "blocking_rows": "TR2761_2_clock_to_WEP;TR2761_3_clock_to_R10;TR2761_5_mixed_branch_guard"}),
        nonclaim({"row_id": "REF2761_2_delta_w_bound", "claim": "MICROSCOPE comparator bound supplies delta_w_A", "allowed": False, "reason": "comparator bound is not an MTS prediction and lacks material/source/tau transfer", "blocking_rows": "DW2761_1_delta_w_prediction;TR2761_4_delta_to_local"}),
        nonclaim({"row_id": "REF2761_3_local_GR", "claim": "MTS derives local GR/Newton after 2761", "allowed": False, "reason": "2761 adds a clock-only product row, not a complete local residual vector", "blocking_rows": "ARENA2761_3_PPN_local;CG2761_6_local_GR_Newton"}),
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2761_0_2762",
            "next_target": "2762-Y5-R2FR-tau-WEP-material-source-projection-or-beta-source-alpha-zero-under-AX1090.md",
            "script": "scripts/Y5_R2FR_tau_WEP_material_source_projection_or_beta_source_alpha_zero_under_AX1090_2762.py",
            "why": "2761 admits the real clock product but blocks all transfers. The next useful step is either derive beta_source_alpha=0/no-alpha coefficient silence, or build the WEP material/source/tau product beta_source_alpha*b_alpha*tau_WEP with source paths and no-cancellation grouping.",
            "include": "tau_WEP definition attempt, MICROSCOPE material/source tensor requirements, beta_source_alpha zero theorem attempt, normalized WEP product target, branch lock",
            "exclude": "clock-to-WEP export by assumption, tau unity shortcut, pair cancellation, local-GR/R10/WEP claim, GitHub, formalization edits",
        })
    ]


def copy_branch_outputs(candidates: list[dict[str, Any]], contract: list[dict[str, Any]], transfer: list[dict[str, Any]], arena: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("BR2761_0_candidates_queue", "candidates", candidates, OUTPUTS["candidates"], BRANCH_OUTPUTS["candidates_queue"], "RAB queue for first finite coupling product candidates"),
        ("BR2761_1_contract_queue", "contract", contract, OUTPUTS["contract"], BRANCH_OUTPUTS["contract_queue"], "RAB queue for product contract obligations"),
        ("BR2761_2_transfer_beta", "transfer", transfer, OUTPUTS["transfer"], BRANCH_OUTPUTS["transfer_beta"], "beta/source transfer gates"),
        ("BR2761_3_arena_local", "arena", arena, OUTPUTS["arena"], BRANCH_OUTPUTS["arena_local"], "local residual insertion map"),
        ("BR2761_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next WEP/beta source target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    candidates = rows_by_name["candidates"]
    contract = rows_by_name["contract"]
    transfer = rows_by_name["transfer"]
    delta = rows_by_name["delta"]
    arena = rows_by_name["arena"]
    gates = rows_by_name["gates"]
    refusal = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]

    clock_row = next((row for row in candidates if row["row_id"] == "SBC2761_0_clock_product_admitted"), {})
    try:
        clock_positive = float(clock_row.get("numeric_value", "nan")) > 0
    except ValueError:
        clock_positive = False

    checks = [
        ("VAL2761_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2761_1_clock_product_numeric", clock_positive and clock_row.get("units") == "yr^-1", "clock product row has positive numeric yr^-1 bound"),
        ("VAL2761_2_clock_only_nonclaim", clock_row.get("same_branch_status") == "CLOCK_PRODUCT_BRANCH_LOCKED_NONCLAIM" and clock_row.get("score_ready") is False, "clock product admitted only as nonclaim clock product"),
        ("VAL2761_3_tau_contract_blocks_standalone", any(row["row_id"] == "CON2761_1_tau_clock" and ("NOT_PARENT_DERIVED" in row["status"] or "TAU_NOT_DERIVED" in row["status"]) for row in contract), "tau/Xhat normalization blocks standalone b_alpha"),
        ("VAL2761_4_transfer_gates_block", all(row["claim_allowed"] is False for row in transfer), "all transfer gates deny claims"),
        ("VAL2761_5_delta_missing", any(row["row_id"] == "DW2761_1_delta_w_prediction" and row["current_value"] == "MISSING_SOURCE_BACKED_VALUE" for row in delta), "delta_w prediction remains explicitly missing"),
        ("VAL2761_6_arena_blocks", all(row["score_ready"] is False for row in arena), "all local arenas remain blocked/nonclaim"),
        ("VAL2761_7_claim_gates_block", any(row["row_id"] == "CG2761_6_local_GR_Newton" and row["passed"] is False for row in gates), "local GR/Newton gate remains blocked"),
        ("VAL2761_8_refusals_block", all(row["allowed"] is False for row in refusal), "refusal runner blocks premature claims"),
        ("VAL2761_9_next", any(row["row_id"] == "NEXT2761_0_2762" and "tau-WEP-material-source" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2761_10_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2761_11_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2761_12_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true or claim_allowed=true"),
        ("VAL2761_13_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2761_14_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2761_15_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append({
        "validation_id": "VAL2761_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2761 admits the source-backed b_alpha*tau_clock_time bound as the first finite coupling product row, but keeps it clock-only and nonclaim. Standalone b_alpha, clock-to-WEP/R10 transfer, delta_w prediction, and local-GR/Newton scoring remain blocked. The next target is tau_WEP/material-source projection or beta_source_alpha zero/prior.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2761 - Y5 R2/f(R): First Same-Branch Coupling Product Row b_alpha Clock Or delta_w Under AX1090",
        "## Private Verdict\n\nWe got one real piece on the board: `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1` is a source-backed finite coupling product row. That is useful and not embarrassing. But it is not a standalone `b_alpha`, and it does not enter WEP, R10, PPN, Newton, or local-GR scoring until the parent branch owns `tau_clock_time` and the WEP/R10 projection taus.\n\nSo 2761 is a partial win: the first finite product row is admitted as clock-only discipline, while every attempted transfer is blocked. The next route is sharper: derive/source `tau_WEP` and `beta_source_alpha`, or prove `beta_source_alpha=0` from the parent coefficient-domain theorem.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Same-Branch Product Candidate Matrix\n\n" + markdown_table(rows_by_name["candidates"], ["row_id", "candidate", "sector", "numeric_value", "units", "source_path", "source_row_id", "same_branch_status", "local_residual_status", "score_ready", "reason", "valid_for_claim"]),
        "## Product Contract Ledger\n\n" + markdown_table(rows_by_name["contract"], ["row_id", "contract_piece", "mathematical_form", "status", "current_value", "missing_for_claim", "valid_for_claim"]),
        "## Transfer Gate Matrix\n\n" + markdown_table(rows_by_name["transfer"], ["row_id", "transfer", "gate_status", "reason", "needed_to_promote", "claim_allowed", "valid_for_claim"]),
        "## delta_w Fallback Audit\n\n" + markdown_table(rows_by_name["delta"], ["row_id", "quantity", "arena", "current_value", "units", "source_basis", "usable_as", "missing_for_prediction", "valid_for_claim"]),
        "## Local Residual Insertion Map\n\n" + markdown_table(rows_by_name["arena"], ["row_id", "arena", "inserted_row", "status", "residual_effect", "score_ready", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decisions"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThe coupling hunt did not go in circles here: it separated a real clock product from illegal cross-arena exports. The work now has a nonclaim product row we can keep, and a precise next missing object: the WEP/source projection `beta_source_alpha*b_alpha*tau_WEP`, or a theorem that sets `beta_source_alpha=0` before we ever need that product.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    candidates = build_candidate_rows(inputs)
    contract = build_contract_rows(inputs)
    transfer = build_transfer_rows(inputs)
    delta = build_delta_rows(inputs)
    arena = build_arena_rows()
    decisions = build_decision_rows()
    gates = build_gate_rows()
    refusal = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["candidates"], candidates)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["transfer"], transfer)
    write_csv(OUTPUTS["delta"], delta)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(candidates, contract, transfer, arena, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "candidates": candidates,
        "contract": contract,
        "transfer": transfer,
        "delta": delta,
        "arena": arena,
        "decisions": decisions,
        "gates": gates,
        "refusal": refusal,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2761_OVERALL")
    print(f"2761 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
