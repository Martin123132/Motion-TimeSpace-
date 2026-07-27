from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4127-Y5-R2FR-shortest-source-signature-clause-attack.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SHORTEST_SOURCE_SIGNATURE_CLAUSE_ATTACK_4127"
CHECKPOINT_ID = "4127"
DECISION = "POYNTING_DOUBLE_COUNT_SUBTERM_ELIMINATED_EM_SOURCE_RESIDUAL_REDUCED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4127_00_4126_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4126_NEXT_TARGET.csv",
        "4127-Y5-R2FR-shortest-source-signature-clause-attack.md",
        "4126 selected shortest source-signature clause attack.",
    ),
    "SRC4127_01_4126_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4126_STATUS.csv",
        "WARD_OBSTRUCTION_DERIVED_PARENT_ZERO_UNSIGNED_BETA_COMMON_BOUNDS_FILLED",
        "Current Ward obstruction and ten-term residual vector.",
    ),
    "SRC4127_02_4126_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4126_WARD_RESIDUAL_DECOMPOSITION.csv",
        "beta_source_EM",
        "4126 beta_source_EM term to reduce.",
    ),
    "SRC4127_03_4126_em": (
        SOURCE_DIR / "P8_Y5_R2FR_4126_EM_POYNTING_COUPLING_ROWS.csv",
        "POYNTING_ONCE_GUARD",
        "4126 Poynting once-only guard.",
    ),
    "SRC4127_04_3597_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3597_EM_POYNTING_ONCE_THEOREM.csv",
        "CONDITIONAL_ZERO_THEOREM_DERIVED",
        "Prior EM/Poynting once-only theorem scaffold.",
    ),
    "SRC4127_05_3597_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3597_EM_SOURCE_ACCOUNTING_RESIDUALS.csv",
        "EMR3597_8_double_count",
        "Prior double-count residual row.",
    ),
    "SRC4127_06_3597_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3597_EM_ONCE_BOUND_ROWS.csv",
        "EMB3597_8_epsilon_EM_double_count",
        "Prior double-count bound row.",
    ),
    "SRC4127_07_4096_em_interface": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE.csv",
        "EM4096_1_Poynting_exchange",
        "Poynting is source exchange inside Hilbert stress.",
    ),
    "SRC4127_08_4106_source_spine": (
        SOURCE_DIR / "P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE.csv",
        "SCS4106_6_EM_Poynting_once",
        "Current source-coupling spine includes EM/Poynting once.",
    ),
    "SRC4127_09_4112_em_spine": (
        SOURCE_DIR / "P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE.csv",
        "EMS4112_5_source_owner_packet",
        "EM owner packet remains live after once-only reduction.",
    ),
    "SRC4127_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4127_shortest_source_signature_clause_attack.py",
        "Reproducible generator for this 4127 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def poynting_theorem_rows() -> List[dict]:
    data = [
        (
            "POT4127_0_definition_lock",
            "single dressed source functional",
            "M_H^dress := N_G int_S Pi_M^H J_H_total with J_H_total=J_matter+J_EM+J_Poynting+J_binding+dB_impr",
            "The source charge is assembled once before orbital/readout calibration.",
            "DEFINITION_LOCK_IMPORTED_FROM_4126",
        ),
        (
            "POT4127_1_maxwell_balance",
            "Poynting theorem as stress conservation split",
            "D_tau E_EM[V] + int_boundary S_Poynting dot n dA = -int_V J dot E + improvements",
            "Poynting is the boundary/flux part of EM Hilbert stress exchange with matter, not a separate fifth source.",
            "POYNTING_IS_HILBERT_FLUX",
        ),
        (
            "POT4127_2_no_extra_coefficient",
            "extra Poynting source coefficient",
            "M_trial = ell_M(Pi_M J_H_total) + c_Poynt_extra int_boundary S_Poynting dot n dA",
            "Because the flux is already contained in J_H_total, consistency of one source functional forces c_Poynt_extra=0.",
            "EXTRA_POYNTING_COEFFICIENT_ZERO_BY_SINGLE_SOURCE_FUNCTIONAL",
        ),
        (
            "POT4127_3_double_count_zero",
            "epsilon_EM_double_count",
            "epsilon_EM_double_count := |M_matter^dress + M_EM^separate - M_source^dress[J_H_total]|/|M_H_ref|",
            "In the branch using only M_H^dress[J_H_total], M_EM^separate is not an allowed independent term, so the double-count subterm is eliminated.",
            "SUBTERM_ELIMINATED_BY_DEFINITION_LOCK",
        ),
        (
            "POT4127_4_remaining_not_zero",
            "beta_source_EM",
            "beta_source_EM -> beta_Hodge_EM + beta_ZQ + beta_JQ + beta_Phi_EM_rad + beta_EM_readout + beta_DeltaJ + beta_dB_impr",
            "The once-only result reduces the EM coupling space, but it does not prove observed Hodge/current/radiative/readout zero.",
            "FULL_EM_SOURCE_ZERO_UNSIGNED",
        ),
    ]
    rows: List[dict] = []
    for theorem_id, object_name, equation, derivation, status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "object": object_name,
                "equation": equation,
                "derivation": derivation,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def killed_subterm_rows() -> List[dict]:
    data = [
        (
            "KST4127_0_c_Poynt_extra",
            "c_Poynt_extra",
            "coefficient of an independent post-readout Poynting source term",
            "c_Poynt_extra=0",
            "If J_H_total already includes J_Poynting, an additional source term is double-counting, not new physics.",
            "EXACT_WITHIN_SINGLE_DRESSED_SOURCE_BRANCH",
        ),
        (
            "KST4127_1_epsilon_EM_double_count",
            "epsilon_EM_double_count",
            "double-count error from matter mass plus separate EM/Poynting patch",
            "epsilon_EM_double_count=0 for M_source^dress=ell_M(Pi_M J_H_total)",
            "The old 3597 missing certificate is replaced by the 4126 source functional definition lock.",
            "ELIMINATED_AS_INDEPENDENT_RESIDUAL",
        ),
        (
            "KST4127_2_beta_source_EM_reduced",
            "beta_source_EM_reduced",
            "EM source residual after removing independent Poynting double-count channel",
            "beta_source_EM_reduced=beta_Hodge_EM+beta_ZQ+beta_JQ+beta_Phi_EM_rad+beta_EM_readout+beta_DeltaJ+beta_dB_impr",
            "The remaining terms are real owner/flux/readout questions, not duplicate accounting.",
            "RESIDUAL_VECTOR_REDUCED_NOT_CLOSED",
        ),
    ]
    rows: List[dict] = []
    for kill_id, symbol, target, result, reason, status in data:
        row = row_base()
        row.update(
            {
                "kill_id": kill_id,
                "symbol": symbol,
                "target": target,
                "result": result,
                "reason": reason,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def remaining_residual_rows() -> List[dict]:
    data = [
        (
            "ERR4127_0_beta_Hodge_EM",
            "beta_Hodge_EM",
            "A_N ln star_obs or constitutive chi_EM drift",
            "observed-Hodge ownership by q/e_obs",
            "R10/EM/clock/fine-structure",
            "OPEN_OWNER_OR_BOUND_REQUIRED",
        ),
        (
            "ERR4127_1_beta_ZQ",
            "beta_ZQ",
            "A_N ln Z_Q or Maxwell action normalization drift",
            "unique Maxwell normalization and alpha/charge owner",
            "EM common mode, alpha drift, source mass",
            "OPEN_OWNER_OR_BOUND_REQUIRED",
        ),
        (
            "ERR4127_2_beta_JQ",
            "beta_JQ",
            "charge/current normalization drift",
            "same current normalization in Lorentz force and Maxwell stress",
            "Lorentz exchange, clocks, composition",
            "OPEN_OWNER_OR_BOUND_REQUIRED",
        ),
        (
            "ERR4127_3_beta_Phi_EM_rad",
            "beta_Phi_EM_rad",
            "net exterior Poynting flux over the stated window",
            "stationary isolated source theorem or explicit flux bound",
            "time-varying source mass, orbital/radiative systems",
            "OPEN_ZERO_OR_BOUND_REQUIRED",
        ),
        (
            "ERR4127_4_beta_EM_readout",
            "beta_EM_readout",
            "post-variation EM readout regeneration",
            "readout-after-variation closure",
            "Maxwell/source calibration",
            "OPEN_OWNER_OR_BOUND_REQUIRED",
        ),
        (
            "ERR4127_5_beta_DeltaJ",
            "beta_DeltaJ",
            "dJ_H_total closure failure",
            "total Hilbert current Ward closure including matter, EM, extra, boundary",
            "PPN/source conservation",
            "OPEN_CURRENT_CLOSURE_REQUIRED",
        ),
        (
            "ERR4127_6_beta_dB_impr",
            "beta_dB_impr",
            "boundary improvement flux",
            "boundary silence or explicit retained improvement row",
            "Hamiltonian/source equality",
            "OPEN_BOUNDARY_SILENCE_REQUIRED",
        ),
    ]
    rows: List[dict] = []
    for residual_id, symbol, definition, closure_needed, arena_link, status in data:
        row = row_base()
        row.update(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "definition": definition,
                "closure_needed": closure_needed,
                "arena_link": arena_link,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def bound_update_rows() -> List[dict]:
    data = [
        (
            "EUB4127_0_epsilon_EM_double_count",
            "epsilon_EM_double_count",
            "0 in the single dressed source functional branch",
            "dimensionless",
            "removed_from_bound_sum",
            "do not include a separate EM/Poynting patch after J_H_total has already been used",
        ),
        (
            "EUB4127_1_epsilon_EM_source_total_reduced",
            "epsilon_EM_source_total_reduced",
            "epsilon_Hodge_EM + epsilon_ZQ + epsilon_JQ + epsilon_Phi_EM_rad + epsilon_EM_readout + epsilon_DeltaJ + epsilon_dB_impr",
            "dimensionless_or_declared_component_norm",
            "reduced_nonclaim_bound_sum",
            "all remaining components still need parent zero or numeric/source-backed bounds",
        ),
        (
            "EUB4127_2_Poynting_flux_window",
            "epsilon_Phi_EM_rad",
            "abs(int_boundary S_Poynting dot n dA)/(abs(G_ref M_H) over stated window)",
            "time^-1_or_dimensionless_window",
            "critical_remaining_bound",
            "stationary isolated local branch can try zero; radiative/background branch needs flux bound",
        ),
    ]
    rows: List[dict] = []
    for bound_id, symbol, formula, units, status, next_input in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "status": status,
                "next_input": next_input,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4127_0_real_progress",
            "One coupling subterm is removed: an independent Poynting source coefficient is forbidden by the single dressed source functional.",
            "SUBTERM_KILLED_NOT_FULL_CLOSURE",
            "carry forward the reduced EM residual vector",
        ),
        (
            "DEC4127_1_no_overclaim",
            "This does not prove full EM source ownership, Maxwell limit, local GR, or beta_common=0.",
            "NO_LOCAL_GR_CLAIM",
            "keep Hodge, charge/current, radiative flux, readout, current closure, and boundary improvements live",
        ),
        (
            "DEC4127_2_best_next_clause",
            "The next clean target is the stationary local Poynting flux zero/bound, because it is now the sharpest remaining EM term.",
            "NEXT_PHI_EM_RAD_SELECTED",
            "derive Phi_EM_rad=0 for isolated stationary local systems or produce a flux-window bound row",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4127_0",
            "result": DECISION,
            "summary": (
                "4127 attacks one concrete coupling clause. Because 4126 defines the source mass as one dressed Hilbert "
                "functional M_H^dress[J_H_total], and J_H_total already includes EM/Poynting flux, a separate independent "
                "Poynting source coefficient is double-counting and is eliminated within this branch. Full EM/source "
                "ownership remains unsigned, but beta_source_EM is reduced to Hodge, Maxwell normalization, current, "
                "radiative flux, readout, current-closure, and boundary-improvement residuals."
            ),
            "subterm_eliminated": "True",
            "full_em_zero_signed": "False",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM, Maxwell, or source-normalization pass",
            "next_target": "4128 stationary local Poynting flux zero or flux-window bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4127_0",
            "target_doc": "4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md",
            "target_script": "scripts/Y5_R2FR_4128_stationary_local_poynting_flux_zero_or_bound.py",
            "objective": (
                "try to prove Phi_EM_rad=int_boundary S_Poynting dot n dA vanishes for stationary isolated local systems "
                "in the same observed coframe; if not, stage a flux-window bound row with units, surface, time window, and arena links"
            ),
            "success_gate": "Phi_EM_rad=0 is signed for the stationary isolated branch, or epsilon_Phi_EM_rad has a precise nonclaim bound schema",
            "reason": "4127 removed double-counting; the live Poynting term is now real exterior flux, not duplicate accounting.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4127_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4127_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM.csv",
        "P8_Y5_R2FR_4127_KILLED_SUBTERM_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4127_KILLED_SUBTERM_ROWS.csv",
        "P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS": SOURCE_DIR / "P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS.csv",
        "P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS.csv",
        "P8_Y5_R2FR_4127_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4127_DECISION_GATES.csv",
        "P8_Y5_R2FR_4127_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4127_STATUS.csv",
        "P8_Y5_R2FR_4127_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4127_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4127 - Shortest Source Signature Clause Attack",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- One subterm is actually removed: an extra independent Poynting source coefficient is double-counting.",
        "- This works only inside the single dressed source branch `M_H^dress[J_H_total]` from 4126.",
        "- Full EM source ownership is not solved; the remaining residual vector is smaller and sharper.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Poynting Once Theorem", "", "| theorem_id | object | status |", "|---|---|---|"])
    for row in poynting_theorem_rows():
        sections.append(f"| {row['theorem_id']} | {row['object']} | {row['status']} |")
    sections.extend(["", "## Killed Subterm", "", "| symbol | result | status |", "|---|---|---|"])
    for row in killed_subterm_rows():
        sections.append(f"| {row['symbol']} | {row['result']} | {row['status']} |")
    sections.extend(["", "## Remaining EM Residuals", "", "| symbol | closure_needed | status |", "|---|---|---|"])
    for row in remaining_residual_rows():
        sections.append(f"| {row['symbol']} | {row['closure_needed']} | {row['status']} |")
    sections.extend(["", "## Claim Ceiling", "", f"- {status['claim_state']}.", "- This is a coupling-space simplification, not a local-GR pass.", "", "## Next Target", "", "- `4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md`", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4127_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM": poynting_theorem_rows,
        "P8_Y5_R2FR_4127_KILLED_SUBTERM_ROWS": killed_subterm_rows,
        "P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS": remaining_residual_rows,
        "P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS": bound_update_rows,
        "P8_Y5_R2FR_4127_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4127_STATUS": status_rows,
        "P8_Y5_R2FR_4127_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4127_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4127_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4127_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM"]])
    theorem_ok = all(token in theorem_text for token in ["J_H_total", "c_Poynt_extra=0", "SUBTERM_ELIMINATED_BY_DEFINITION_LOCK", "FULL_EM_SOURCE_ZERO_UNSIGNED"])
    add("VAL4127_3_theorem", "Poynting once theorem removes only duplicate source coefficient", theorem_ok, "theorem tokens checked")

    killed_text = flatten_rows([outputs["P8_Y5_R2FR_4127_KILLED_SUBTERM_ROWS"]])
    killed_ok = all(token in killed_text for token in ["c_Poynt_extra", "epsilon_EM_double_count=0", "beta_source_EM_reduced"])
    add("VAL4127_4_killed_subterm", "killed-subterm rows include c_Poynt_extra, double-count zero, and reduced beta", killed_ok, "killed tokens checked")

    remaining_text = flatten_rows([outputs["P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS"]])
    remaining_ok = all(token in remaining_text for token in ["beta_Hodge_EM", "beta_ZQ", "beta_JQ", "beta_Phi_EM_rad", "beta_EM_readout", "beta_DeltaJ", "beta_dB_impr"])
    add("VAL4127_5_remaining_residuals", "remaining EM residual vector is explicit", remaining_ok, "remaining tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS"]])
    bound_ok = all(token in bound_text for token in ["removed_from_bound_sum", "epsilon_EM_source_total_reduced", "epsilon_Phi_EM_rad"])
    add("VAL4127_6_bound_update", "bound update removes double-count and selects flux window", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4127_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["SUBTERM_KILLED_NOT_FULL_CLOSURE", "NO_LOCAL_GR_CLAIM", "NEXT_PHI_EM_RAD_SELECTED"])
    add("VAL4127_7_decisions", "decision gates record progress without overclaim and select next flux target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4127_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and status[0].get("subterm_eliminated") == "True" and status[0].get("full_em_zero_signed") == "False"
    add("VAL4127_8_status", "status records subterm elimination and full EM no-claim", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4127_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md"
    add("VAL4127_9_next_target", "next target is stationary local Poynting flux zero or bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4127_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4127*")) or any(FORMALIZATION.rglob("4127-Y5-R2FR*"))
    add("VAL4127_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4127_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4127_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
