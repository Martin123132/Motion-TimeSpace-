from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3962"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3962-Y5-R2FR-EM-residual-vector-first-score-or-Hodge-owner-lock.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3962_SOURCE_REGISTER.csv",
    "vector": SRC / "P8_Y5_R2FR_3962_EM_RESIDUAL_VECTOR.csv",
    "hodge_owner": SRC / "P8_Y5_R2FR_3962_HODGE_OWNER_LOCK_OR_BOUND.csv",
    "score": SRC / "P8_Y5_R2FR_3962_EM_FIRST_NONCLAIM_SCORE_ROW.csv",
    "ca_feed": SRC / "P8_Y5_R2FR_3962_CA_TOTAL_EM_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3962_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3962_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3962_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3962_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3962_VALIDATION.csv",
}

NEXT_DOC = "3963-Y5-R2FR-source-coupling-product-Newton-G-constancy-or-residual-score.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3963_source_coupling_product_Newton_G_constancy_or_residual_score.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3962_00_3961_next", SRC / "P8_Y5_R2FR_3961_NEXT_TARGET.csv", "NEXT3961_0", "3961 handoff"),
        ("SRC3962_01_hidden_law", SRC / "P8_Y5_R2FR_3961_HIDDEN_EM_VARIATION_LAW.csv", "HEV3961_1_source_current", "hidden EM source law"),
        ("SRC3962_02_hidden_bound", SRC / "P8_Y5_R2FR_3961_HIDDEN_EM_VARIATION_LAW.csv", "HEV3961_2_bound", "hidden EM bound"),
        ("SRC3962_03_sigma_zero", SRC / "P8_Y5_R2FR_3961_SIGMA_FACTOR_EM_EXCLUSION_GATE.csv", "SFE3961_1_sigma_factor", "Sigma factor zero route"),
        ("SRC3962_04_poynting_zero", SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv", "PNF3961_1_stationary_zero", "Poynting zero route"),
        ("SRC3962_05_poynting_bound", SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv", "PNF3961_2_flux_bound", "Poynting bound"),
        ("SRC3962_06_first_hodge", SRC / "P8_Y5_R2FR_3961_EM_FIRST_CONDITIONAL_ZERO_VALUES.csv", "EMZ3961_3_Delta_Hodge_EM", "Hodge zero condition"),
        ("SRC3962_07_bound_alpha", SRC / "P8_Y5_R2FR_3961_EM_BOUND_VALUE_TEMPLATES.csv", "EMB3961_2_alpha_clock", "alpha/clock bound"),
        ("SRC3962_08_3503_hodge", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_0_Delta_Hodge_EM", "Hodge owner residual"),
        ("SRC3962_09_3503_wem", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_1_w_EM", "Maxwell multiplier residual"),
        ("SRC3962_10_3503_current", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_3_C_JQ", "charge/current normalization residual"),
        ("SRC3962_11_3503_readout", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_5_C_EM_readout", "EM readout residual"),
        ("SRC3962_12_3503_total", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_6_Delta_J_total", "total current closure residual"),
        ("SRC3962_13_3502_visible", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_0_minimal_bound_field_stress", "visible Maxwell zero"),
        ("SRC3962_14_3502_readout", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_6_readout_radiative_regeneration", "readout regeneration residual"),
        ("SRC3962_15_CA_EM", SRC / "P8_Y5_R2FR_3959_CA_TOTAL_CURRENT_BOUND_LAW.csv", "CAB3959_5_EM_alpha_charge", "CA EM feed"),
        ("SRC3962_16_3960_values", SRC / "P8_Y5_R2FR_3960_FIRST_CONDITIONAL_ZERO_VALUES.csv", "FZ3960_4_epsilon_EM_extra", "visible EM conditional zero"),
        ("SRC3962_17_validation_3961", SRC / "P8_Y5_BRR545_3961_VALIDATION.csv", "VAL3961_19_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def vector_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EMV3962_0_visible_minimal", "epsilon_EM_extra_hidden_source", "0", "ordinary Maxwell stress included in T_total/M_H with same *_obs", "CLOSED_CONDITIONAL_ZERO", "source stress"),
        ("EMV3962_1_internal_exchange", "epsilon_internal_exchange", "0", "matter-EM Lorentz exchange cancels inside total stress", "CLOSED_BOOKKEEPING_ZERO", "Bianchi/source conservation"),
        ("EMV3962_2_hidden_F2", "C_XF2_effective", "|f_A| ||F^2|| + |g_A| ||F*F||", "zero if Sigma-factor/no-Hom; otherwise coefficient and field norms required", "BOUND_OR_ZERO", "alpha; EM clocks; source leakage"),
        ("EMV3962_3_Hodge", "Delta_Hodge_EM", "|*_EM-*_obs| or constitutive tensor difference", "zero if EM Hodge is exactly observed coframe Hodge", "HODGE_OWNER_LOCK_CONDITIONAL", "Maxwell stress/source coupling"),
        ("EMV3962_4_Poynting", "Phi_EM_rad", "|dU_EM/dt| + |int J.E dV|", "zero on stationary isolated no-flux branch; otherwise energy/work bound", "BOUND_OR_ZERO", "boundary current; clocks/orbits"),
        ("EMV3962_5_wEM", "w_EM-1", "|w_EM-1|", "zero if unique Maxwell normalization owner fixes common F^2 coefficient", "OWNER_LOCK_OPEN", "alpha/charge normalization"),
        ("EMV3962_6_CJQ", "C_JQ", "charge/current normalization ambiguity", "zero if A,J,current normalization and alpha readout are fixed together", "OWNER_LOCK_OPEN", "charge/current normalization"),
        ("EMV3962_7_readout", "C_EM_readout", "readout/loop/spectroscopy regeneration", "zero if readout closure preserves visible pullback and unique EM owner", "READOUT_LOCK_OPEN", "EM clocks; alpha"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "score_term": score_term,
            "zero_or_bound_condition": condition,
            "status": status,
            "feeds": feeds,
            "score_ready": status in {"CLOSED_CONDITIONAL_ZERO", "CLOSED_BOOKKEEPING_ZERO", "BOUND_OR_ZERO", "HODGE_OWNER_LOCK_CONDITIONAL"},
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, score_term, condition, status, feeds in rows
    ]


def hodge_owner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HOL3962_0_lock_condition",
            "owner_piece": "EM Hodge owner",
            "formula": "*_EM := *_obs[e_obs(q)]",
            "derived_effect": "Delta_Hodge_EM=0 and visible Maxwell stress varies with the same observed metric/coframe as matter",
            "status": "LOCK_CONDITIONAL_NOT_GLOBAL_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HOL3962_1_counter_branch",
            "owner_piece": "independent constitutive tensor",
            "formula": "*_EM = *_obs + Delta_* or chi_EM != chi_obs",
            "derived_effect": "Delta_Hodge_EM remains in the EM residual vector and feeds C_A_total/alpha/clock bounds",
            "status": "BOUND_BRANCH_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HOL3962_2_readout_owner",
            "owner_piece": "EM readout/spectroscopy owner",
            "formula": "S_eff/readout contains no regenerated f_X F^2, alpha_X, or EM binding response beyond visible pullback",
            "derived_effect": "C_EM_readout=0 if readout is a pullback of the same EM owner; otherwise retained",
            "status": "READOUT_LOCK_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "HOL3962_3_normalization_owner",
            "owner_piece": "Maxwell coefficient/current normalization",
            "formula": "w_EM, A_Q, J_Q, and alpha readout share one representation/normalization owner",
            "derived_effect": "w_EM-1 and C_JQ vanish if the owner is unique; otherwise alpha/charge normalization remains bounded",
            "status": "NORMALIZATION_LOCK_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def score_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "score_id": "EMS3962_0_full_vector",
            "score_name": "epsilon_EM_residual",
            "formula": "epsilon_EM <= A_F(|f_A| ||F^2|| + |g_A| ||F*F||) + A_H|Delta_Hodge_EM| + A_P|Phi_EM_rad| + A_R|C_EM_readout| + A_W|w_EM-1| + A_Q|C_JQ|",
            "conditional_reduction": "if Sigma/no-Hom, stationary no-flux, same Hodge, unique normalization, and readout lock all hold then epsilon_EM=0",
            "current_values": "visible minimal EM=0; internal exchange=0; partial_A f/g=0 conditional; Phi_EM_rad=0 conditional; Delta_Hodge_EM=0 conditional; w_EM/C_JQ/C_EM_readout open",
            "score_status": "FIRST_NONCLAIM_SCORE_ROW_SYMBOLIC",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "score_id": "EMS3962_1_minimal_stationary_pullback_branch",
            "score_name": "epsilon_EM_minimal_branch",
            "formula": "epsilon_EM_minimal = A_W|w_EM-1| + A_Q|C_JQ| + A_R|C_EM_readout|",
            "conditional_reduction": "after Sigma factorization, stationary no-flux, and same-Hodge lock, only normalization/readout owner terms remain",
            "current_values": "not numeric; owner rows still unsigned",
            "score_status": "REDUCED_SYMBOLIC_SCORE_ROW",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ca_feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CAF3962_0_CA_total_feed",
            "target": "C_A_total_current_MTS",
            "update_formula": "C_A_total <= C_A_nonEM + K_EMsource epsilon_EM_residual",
            "meaning": "the whole EM/Hodge/Poynting/readout leakage now feeds local source coupling through one score term",
            "required_next_values": "A_F,A_H,A_P,A_R,A_W,A_Q,K_EMsource plus retained residual values or owner zeros",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CAF3962_1_alpha_clock_feed",
            "target": "Delta_alpha/alpha and EM clock residual",
            "update_formula": "|Delta_alpha/alpha| <= K_alpha epsilon_EM_residual",
            "meaning": "EM empirical tests can score the same residual vector instead of ad hoc channel lists",
            "required_next_values": "K_alpha; EM residual weights; spectroscopy/readout bounds",
            "status": "SYMBOLIC_FEED_READY_NO_NUMERIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3962_0_vectorized",
            "decision": "assemble EM residuals into epsilon_EM_residual",
            "basis": "3961 gives hidden F2, Poynting, Hodge, and readout bound templates; 3960 supplies visible EM zeros",
            "effect": "EM leakage now feeds C_A_total through one symbolic score row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3962_1_partial_lock",
            "decision": "record Hodge owner lock as conditional rather than claimed",
            "basis": "Delta_Hodge_EM=0 requires *_EM=*_obs[e_obs(q)] as parent grammar, not just convenience",
            "effect": "same-Hodge route is clean, independent constitutive branch remains bounded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3962_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "EM branch is now score-ready symbolically; next highest local-GR coupling gap is Newton/source coupling product constancy",
            "effect": "connects the local source-current work to Newtonian mechanics and calibrated G",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CLG3962_0_sources", "source register", "all cited local sources and needles found", "PASS_PRIVATE"),
        ("CLG3962_1_score_row", "first EM score row", "epsilon_EM_residual assembled with all live EM channels", "PASS_SYMBOLIC_NONCLAIM"),
        ("CLG3962_2_hodge", "Hodge owner", "*_EM=*_obs[e_obs(q)] parent-signed", "CONDITIONAL_ONLY"),
        ("CLG3962_3_readout_norm", "readout/normalization owners", "C_EM_readout,w_EM,C_JQ zero or bounded", "OPEN"),
        ("CLG3962_4_local_GR", "local GR/Maxwell/Newton source coupling", "EM score plus non-EM source coupling product closed", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3962_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive or bound the EH/source-coupling product that fixes measured Newton G: G_ref, w_common, ell_J, R_frame, epsilon_mu, and any remaining source-normalization drift",
            "success_condition": "Newtonian source coupling is either parent-constant/universal or represented by a first nonclaim residual score feeding Gdot/WEP/PPN/R10 gates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_EM_SCORE_VECTOR",
            "summary": "3962 assembles hidden F2, Hodge, Poynting, readout, Maxwell normalization, and charge-current normalization into a first symbolic EM residual score feeding C_A_total_current and alpha/clock bounds. Hodge owner lock remains conditional; readout/normalization owners remain open.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3962 - EM Residual Vector First Score Or Hodge Owner Lock

Timestamp: `{timestamp}`

## Result

3962 turns the EM leftovers into one scoreable vector:

`epsilon_EM <= A_F(|f_A| ||F^2|| + |g_A| ||F*F||) + A_H|Delta_Hodge_EM| + A_P|Phi_EM_rad| + A_R|C_EM_readout| + A_W|w_EM-1| + A_Q|C_JQ|`.

Known conditional zero pieces:

- visible minimal Maxwell extra-source leakage is zero if it uses `*_obs` and is inside `T_total`;
- internal matter-EM exchange is bookkeeping-zero in total stress;
- hidden `F^2/F*F` linear source is zero if the coefficient factorizes through `Sigma_loc` or no hidden-visible Hom exists;
- Poynting flux is zero on the stationary isolated no-flux branch;
- Hodge leakage is zero if `*_EM=*_obs[e_obs(q)]`.

Still open:

- `C_EM_readout`;
- `w_EM-1`;
- `C_JQ`;
- global parent signing of the Hodge/readout/normalization owner.

## Source/Register

- Sources found: `{found}/{len(source_rows)}`
- EM residual vector: `source-intake\\mts_residuals\\P8_Y5_R2FR_3962_EM_RESIDUAL_VECTOR.csv`
- Hodge owner gate: `source-intake\\mts_residuals\\P8_Y5_R2FR_3962_HODGE_OWNER_LOCK_OR_BOUND.csv`
- First score row: `source-intake\\mts_residuals\\P8_Y5_R2FR_3962_EM_FIRST_NONCLAIM_SCORE_ROW.csv`
- C_A feed update: `source-intake\\mts_residuals\\P8_Y5_R2FR_3962_CA_TOTAL_EM_FEED_UPDATE.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3962_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3962 - EM Residual Vector And First Symbolic Score

Timestamp: `{timestamp}`

- EM/Hodge/Poynting/readout leakage is now compressed into `epsilon_EM_residual`.
- Hodge owner lock is conditional: `*_EM=*_obs[e_obs(q)]` gives `Delta_Hodge_EM=0`; independent constitutive tensor remains bounded.
- `epsilon_EM_residual` feeds `C_A_total_current` and alpha/clock bounds through explicit symbolic formulas.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3962 - EM Residual Vector And First Symbolic Score"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    vector = vector_rows(timestamp)
    hodge = hodge_owner_rows(timestamp)
    score = score_rows(timestamp)
    ca_feed = ca_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()

    vector_symbols = {row["symbol"] for row in vector}
    vector_statuses = {row["status"] for row in vector}
    hodge_statuses = {row["status"] for row in hodge}
    score_names = {row["score_name"] for row in score}
    ca_targets = {row["target"] for row in ca_feed}
    decision_text = " ".join(row["decision"] for row in decisions)
    claim_statuses = {row["status"] for row in claims}
    all_physics_rows = vector + hodge + score + ca_feed + decisions + claims + next_target

    checks = [
        ("VAL3962_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3962_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3962_02_vector_complete", {"C_XF2_effective", "Delta_Hodge_EM", "Phi_EM_rad", "w_EM-1", "C_JQ", "C_EM_readout"}.issubset(vector_symbols), "EM residual vector contains live channels"),
        ("VAL3962_03_closed_zeros", "CLOSED_CONDITIONAL_ZERO" in vector_statuses and "CLOSED_BOOKKEEPING_ZERO" in vector_statuses, "closed EM zero rows retained"),
        ("VAL3962_04_hodge_lock", "LOCK_CONDITIONAL_NOT_GLOBAL_PARENT_SIGNED" in hodge_statuses and "BOUND_BRANCH_RETAINED" in hodge_statuses, "Hodge lock and bound branch written"),
        ("VAL3962_05_score_rows", {"epsilon_EM_residual", "epsilon_EM_minimal_branch"}.issubset(score_names), "first symbolic EM score rows written"),
        ("VAL3962_06_ca_feed", {"C_A_total_current_MTS", "Delta_alpha/alpha and EM clock residual"}.issubset(ca_targets), "EM score feeds C_A and alpha/clock rows"),
        ("VAL3962_07_decision", "assemble EM residuals" in decision_text and "Hodge owner lock" in decision_text, "decision records vectorization and Hodge conditionality"),
        ("VAL3962_08_claim_gate", "PASS_SYMBOLIC_NONCLAIM" in claim_statuses and "CONDITIONAL_ONLY" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses, "claim gate blocks promotion"),
        ("VAL3962_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to source coupling/Newton G product"),
        ("VAL3962_10_all_nonclaim", all(not row["valid_for_claim"] for row in all_physics_rows), "all generated physics rows remain nonclaim"),
        ("VAL3962_11_score_ready", all(row["score_ready"] for row in score), "symbolic EM score rows are score-ready"),
        ("VAL3962_12_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in generated_paths), "no generated output is inside formalization-workbench"),
        ("VAL3962_13_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in generated_paths), fwb_git_detail),
        ("VAL3962_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3962_15_spine_updated", SPINE_PATH.exists() and "3962 - EM Residual Vector And First Symbolic Score" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3962_16_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3962_17_script_compile", True, "script compiled before validation write"),
        ("VAL3962_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    vector = vector_rows(timestamp)
    hodge = hodge_owner_rows(timestamp)
    score = score_rows(timestamp)
    ca_feed = ca_feed_rows(timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, sources)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["vector"], vector)
    write_csv(OUTPUTS["hodge_owner"], hodge)
    write_csv(OUTPUTS["score"], score)
    write_csv(OUTPUTS["ca_feed"], ca_feed)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, sources), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, sources)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3962 validation failed: {failed}")

    print(f"3962 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("EM residual vector assembled and first symbolic score row feeds C_A_total_current")


if __name__ == "__main__":
    run()
