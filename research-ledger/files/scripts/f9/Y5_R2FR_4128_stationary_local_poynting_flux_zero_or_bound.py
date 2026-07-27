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
DOC_PATH = ROOT / "4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_STATIONARY_LOCAL_POYNTING_FLUX_ZERO_OR_BOUND_4128"
CHECKPOINT_ID = "4128"
DECISION = "STATIONARY_LOCAL_PHI_EM_RAD_ZERO_DERIVED_RADIATIVE_BOUND_RETAINED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4128_00_4127_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4127_NEXT_TARGET.csv",
        "4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md",
        "4127 selected stationary Poynting flux zero or bound.",
    ),
    "SRC4128_01_4127_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4127_STATUS.csv",
        "POYNTING_DOUBLE_COUNT_SUBTERM_ELIMINATED_EM_SOURCE_RESIDUAL_REDUCED",
        "Current chain removed Poynting double-count subterm.",
    ),
    "SRC4128_02_4127_remaining": (
        SOURCE_DIR / "P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS.csv",
        "beta_Phi_EM_rad",
        "Live radiative/exterior Poynting residual.",
    ),
    "SRC4128_03_4127_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS.csv",
        "epsilon_Phi_EM_rad",
        "Flux-window bound target from 4127.",
    ),
    "SRC4128_04_4038_no_flux": (
        SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv",
        "LOCAL_NO_FLUX_THEOREM_DERIVED_CONDITIONALLY",
        "Strongest prior local no-flux theorem.",
    ),
    "SRC4128_05_3873_stationary": (
        SOURCE_DIR / "P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv",
        "EXACT_CONDITIONAL_ZERO_FOR_PHI_EM_BOUNDARY",
        "Stationary boundary flux zero theorem and circulation guard.",
    ),
    "SRC4128_06_3961_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv",
        "DERIVED_FLUX_BOUND_TEMPLATE",
        "Fallback bound template for nonstationary/radiative branch.",
    ),
    "SRC4128_07_3502_flux_vector": (
        SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
        "EMF3502_1_radiative_poynting_flux",
        "Poynting flux coefficient row.",
    ),
    "SRC4128_08_3597_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3597_EM_POYNTING_ONCE_THEOREM.csv",
        "Poynting balance",
        "Earlier Poynting balance statement.",
    ),
    "SRC4128_09_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4128_stationary_local_poynting_flux_zero_or_bound.py",
        "Reproducible generator for this 4128 checkpoint.",
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


def no_flux_theorem_rows() -> List[dict]:
    data = [
        (
            "NFT4128_0_poynting_identity",
            "Maxwell/Poynting identity",
            "d_t u_EM + div S_EM = -J.E",
            "integrating over exterior collar Omega gives Phi_EM_rad[S]=int_S S_EM.n dA = -d_t int_Omega u_EM dV - int_Omega J.E dV",
            "EXACT_OBSERVED_MAXWELL_IDENTITY",
        ),
        (
            "NFT4128_1_stationary_exterior",
            "stationary isolated exterior collar",
            "L_tau fields=0 up to fixed EM gauge; no current crosses the exterior collar; no imposed incoming/background radiation",
            "d_t int_Omega u_EM dV=0 and int_Omega J.E dV=0 in the source-free exterior, so Phi_EM_rad[S]=0",
            "STATIONARY_LOCAL_ZERO_DERIVED",
        ),
        (
            "NFT4128_2_bound_field_guard",
            "bound Coulomb/magnetostatic fields",
            "S_EM may circulate locally while int_S S_EM.n dA=0 on a closed stationary boundary",
            "do not set S_EM=0; set only net leakage Phi_EM_rad=0. EM stress remains inside M_H^dress.",
            "CIRCULATING_POYNTING_NOT_ERASED",
        ),
        (
            "NFT4128_3_radiative_fallback",
            "radiative or driven branch",
            "|Phi_EM_rad| <= |d_t U_EM[Omega]| + |int_Omega J.E dV| + |incoming/background flux| + |improvement flux|",
            "nonstationary systems keep a bound row instead of using the stationary zero",
            "FLUX_BOUND_TEMPLATE_RETAINED",
        ),
        (
            "NFT4128_4_scope_guard",
            "local not cosmological",
            "Phi_EM_rad=0 applies only to compact stationary isolated local source collars",
            "FLRW/cosmological memory, driven lab systems, radiating binaries, and external backgrounds keep the flux row live",
            "LOCAL_BRANCH_ONLY",
        ),
    ]
    rows: List[dict] = []
    for theorem_id, object_name, formula, derived_result, status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "object": object_name,
                "formula": formula,
                "derived_result": derived_result,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def branch_selector_rows() -> List[dict]:
    data = [
        (
            "PBS4128_0_static_local_source",
            "stationary_isolated_local",
            "compact source, fixed observed coframe, no exterior current crossing, no radiation/background flux, boundary improvements silent",
            "Phi_EM_rad=0",
            "USE_ZERO_ROW_FOR_LOCAL_STATIC_BRANCH",
        ),
        (
            "PBS4128_1_stationary_circulation",
            "stationary_with_internal_circulation",
            "S_EM nonzero inside the worldtube but closed-boundary net flux vanishes",
            "Phi_EM_rad=0 while T_EM and angular/momentum density remain in J_H_total",
            "ZERO_LEAKAGE_NOT_ZERO_STRESS",
        ),
        (
            "PBS4128_2_radiating_system",
            "radiative_or_nonstationary",
            "outgoing radiation, changing field energy, driven current, or open boundary",
            "retain epsilon_Phi_EM_rad bound",
            "BOUND_ROW_REQUIRED",
        ),
        (
            "PBS4128_3_external_background",
            "background_or_incoming_flux",
            "imposed EM background or cosmological/ambient flux crosses boundary",
            "retain signed incoming/outgoing flux row",
            "BOUND_ROW_REQUIRED",
        ),
    ]
    rows: List[dict] = []
    for selector_id, branch, conditions, result, status in data:
        row = row_base()
        row.update(
            {
                "selector_id": selector_id,
                "branch": branch,
                "conditions": conditions,
                "result": result,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def residual_update_rows() -> List[dict]:
    data = [
        (
            "RU4128_0_beta_Phi_EM_rad_static",
            "beta_Phi_EM_rad",
            "stationary_isolated_local",
            "0",
            "Poynting identity plus stationary source-free exterior collar",
            "ZERO_IN_SELECTED_LOCAL_BRANCH",
        ),
        (
            "RU4128_1_epsilon_Phi_EM_rad_static",
            "epsilon_Phi_EM_rad",
            "stationary_isolated_local",
            "0",
            "normalised leakage vanishes because numerator Phi_EM_rad vanishes",
            "ZERO_IN_SELECTED_LOCAL_BRANCH",
        ),
        (
            "RU4128_2_epsilon_EM_source_total_static_reduced",
            "epsilon_EM_source_total_static",
            "stationary_isolated_local",
            "epsilon_Hodge_EM + epsilon_ZQ + epsilon_JQ + epsilon_EM_readout + epsilon_DeltaJ + epsilon_dB_impr",
            "4127 removed double count; 4128 removes net radiative flux for the local stationary branch",
            "REDUCED_STATIC_EM_RESIDUAL_VECTOR",
        ),
        (
            "RU4128_3_epsilon_Phi_EM_rad_fallback",
            "epsilon_Phi_EM_rad",
            "radiative_or_background",
            "(|d_t U_EM| + |W_JE| + |Phi_incoming| + |Phi_improvement|)/|G_ref M_H| over declared window",
            "fallback row for nonstationary/radiative systems",
            "NONCLAIM_BOUND_TEMPLATE",
        ),
    ]
    rows: List[dict] = []
    for update_id, symbol, branch, result, reason, status in data:
        row = row_base()
        row.update(
            {
                "update_id": update_id,
                "symbol": symbol,
                "branch": branch,
                "result": result,
                "reason": reason,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def local_coupling_status_rows() -> List[dict]:
    data = [
        (
            "LCS4128_0_removed_terms",
            "EM/Poynting branch",
            "independent Poynting double-count; stationary local net Poynting leakage",
            "removed in 4127 and 4128 for the selected local branch",
            "TWO_EM_SOURCE_TERMS_REMOVED",
        ),
        (
            "LCS4128_1_remaining_terms",
            "EM/source owner branch",
            "Hodge ownership; Maxwell normalization; charge/current normalization; EM readout regeneration; total-current closure; boundary improvements",
            "still require parent zero or sourced bounds",
            "REMAINING_EM_COUPLING_TERMS_EXPLICIT",
        ),
        (
            "LCS4128_2_local_gr_status",
            "local GR/Newton branch",
            "source-normalization Ward zero remains unsigned because non-EM source terms and several EM owner terms remain",
            "no local GR pass, but coupling residual vector is smaller and sharper",
            "NO_CLAIM_PROGRESS_MADE",
        ),
    ]
    rows: List[dict] = []
    for row_id, branch, statement, consequence, status in data:
        row = row_base()
        row.update(
            {
                "row_id": row_id,
                "branch": branch,
                "statement": statement,
                "consequence": consequence,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4128_0_stationary_zero",
            "For compact stationary isolated local source collars, Phi_EM_rad=0 is derived from the observed Maxwell/Poynting identity.",
            "LOCAL_STATIONARY_FLUX_ZERO",
            "use zero only under the branch selector conditions",
        ),
        (
            "DEC4128_1_circulation_guard",
            "Stationary Poynting circulation is not erased; only net boundary leakage is zero.",
            "NO_STRESS_OVERKILL",
            "keep EM stress in J_H_total and do not set S_EM pointwise to zero",
        ),
        (
            "DEC4128_2_radiative_bound",
            "Radiative/background/driven systems keep epsilon_Phi_EM_rad as a bound row.",
            "BOUND_BRANCH_RETAINED",
            "no cosmology/lab/radiating-binary overclaim",
        ),
        (
            "DEC4128_3_next",
            "Next target is observed-Hodge/current owner, because flux and double-counting are no longer the first EM blockers in the stationary local branch.",
            "NEXT_HODGE_CURRENT_OWNER_SELECTED",
            "try to prove beta_Hodge_EM=beta_ZQ=beta_JQ=0 or fill coefficient bounds",
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
            "status_id": "STATUS4128_0",
            "result": DECISION,
            "summary": (
                "4128 imports and current-chain updates the stationary Poynting no-flux theorem. In a compact stationary "
                "isolated local exterior collar, the Maxwell/Poynting identity gives Phi_EM_rad=0; circulating bound-field "
                "Poynting stress may remain and is still counted in J_H_total. Radiative, driven, background, and cosmological "
                "branches retain a flux-window bound. This removes the stationary local Poynting leakage term after 4127 "
                "already removed Poynting double-counting."
            ),
            "stationary_flux_zero_derived": "True",
            "radiative_bound_retained": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM, Maxwell, or source-normalization pass",
            "next_target": "4129 observed-Hodge/current owner clause",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4128_0",
            "target_doc": "4129-Y5-R2FR-observed-hodge-current-owner-clause.md",
            "target_script": "scripts/Y5_R2FR_4129_observed_hodge_current_owner_clause.py",
            "objective": (
                "try to prove observed Hodge/current ownership for the local EM branch, targeting beta_Hodge_EM, beta_ZQ, "
                "and beta_JQ; if unsigned, stage coefficient-bound rows for EM Hodge, Maxwell normalization, and current normalization"
            ),
            "success_gate": "at least one of beta_Hodge_EM, beta_ZQ, beta_JQ is parent-signed zero, or all three get precise nonclaim bound schemas",
            "reason": "4127/4128 removed Poynting double-count and stationary local leakage; the next EM blockers are Hodge/current ownership.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4128_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4128_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4128_NO_FLUX_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4128_NO_FLUX_THEOREM.csv",
        "P8_Y5_R2FR_4128_BRANCH_SELECTOR": SOURCE_DIR / "P8_Y5_R2FR_4128_BRANCH_SELECTOR.csv",
        "P8_Y5_R2FR_4128_RESIDUAL_UPDATE": SOURCE_DIR / "P8_Y5_R2FR_4128_RESIDUAL_UPDATE.csv",
        "P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS.csv",
        "P8_Y5_R2FR_4128_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4128_DECISION_GATES.csv",
        "P8_Y5_R2FR_4128_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4128_STATUS.csv",
        "P8_Y5_R2FR_4128_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4128_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4128 - Stationary Local Poynting Flux Zero or Bound",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- For compact stationary isolated local systems, net exterior Poynting leakage `Phi_EM_rad` is zero.",
        "- This does not set the Poynting vector or EM stress to zero; bound-field EM stress remains in `J_H_total`.",
        "- Radiative, driven, external-background, and cosmological branches keep the flux-window bound.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## No-Flux Theorem", "", "| theorem_id | object | status |", "|---|---|---|"])
    for row in no_flux_theorem_rows():
        sections.append(f"| {row['theorem_id']} | {row['object']} | {row['status']} |")
    sections.extend(["", "## Branch Selector", "", "| branch | result | status |", "|---|---|---|"])
    for row in branch_selector_rows():
        sections.append(f"| {row['branch']} | {row['result']} | {row['status']} |")
    sections.extend(["", "## Residual Update", "", "| symbol | branch | result |", "|---|---|---|"])
    for row in residual_update_rows():
        sections.append(f"| {row['symbol']} | {row['branch']} | {row['result']} |")
    sections.extend(["", "## Claim Ceiling", "", f"- {status['claim_state']}.", "- This is a local stationary-branch simplification, not a full EM/local-GR claim.", "", "## Next Target", "", "- `4129-Y5-R2FR-observed-hodge-current-owner-clause.md`", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4128_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4128_NO_FLUX_THEOREM": no_flux_theorem_rows,
        "P8_Y5_R2FR_4128_BRANCH_SELECTOR": branch_selector_rows,
        "P8_Y5_R2FR_4128_RESIDUAL_UPDATE": residual_update_rows,
        "P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS": local_coupling_status_rows,
        "P8_Y5_R2FR_4128_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4128_STATUS": status_rows,
        "P8_Y5_R2FR_4128_NEXT_TARGET": next_target_rows,
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
        "VAL4128_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4128_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

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
    add("VAL4128_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4128_NO_FLUX_THEOREM"]])
    theorem_ok = all(token in theorem_text for token in ["Phi_EM_rad[S]=0", "CIRCULATING_POYNTING_NOT_ERASED", "FLUX_BOUND_TEMPLATE_RETAINED", "LOCAL_BRANCH_ONLY"])
    add("VAL4128_3_no_flux_theorem", "no-flux theorem includes zero, circulation guard, fallback, and local scope", theorem_ok, "theorem tokens checked")

    selector_text = flatten_rows([outputs["P8_Y5_R2FR_4128_BRANCH_SELECTOR"]])
    selector_ok = all(token in selector_text for token in ["stationary_isolated_local", "Phi_EM_rad=0", "radiative_or_nonstationary", "BOUND_ROW_REQUIRED"])
    add("VAL4128_4_branch_selector", "branch selector separates stationary zero from radiative bound", selector_ok, "selector tokens checked")

    update_text = flatten_rows([outputs["P8_Y5_R2FR_4128_RESIDUAL_UPDATE"]])
    update_ok = all(token in update_text for token in ["ZERO_IN_SELECTED_LOCAL_BRANCH", "epsilon_EM_source_total_static", "NONCLAIM_BOUND_TEMPLATE"])
    add("VAL4128_5_residual_update", "residual update zeroes stationary flux and retains fallback", update_ok, "update tokens checked")

    local_text = flatten_rows([outputs["P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS"]])
    local_ok = all(token in local_text for token in ["TWO_EM_SOURCE_TERMS_REMOVED", "REMAINING_EM_COUPLING_TERMS_EXPLICIT", "NO_CLAIM_PROGRESS_MADE"])
    add("VAL4128_6_local_status", "local coupling status records removed terms and remaining blockers", local_ok, "local status tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4128_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["LOCAL_STATIONARY_FLUX_ZERO", "NO_STRESS_OVERKILL", "BOUND_BRANCH_RETAINED", "NEXT_HODGE_CURRENT_OWNER_SELECTED"])
    add("VAL4128_7_decisions", "decision gates record zero, guards, bound branch, and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4128_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and status[0].get("stationary_flux_zero_derived") == "True" and status[0].get("radiative_bound_retained") == "True"
    add("VAL4128_8_status", "status records stationary zero and radiative bound retention", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4128_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4129-Y5-R2FR-observed-hodge-current-owner-clause.md"
    add("VAL4128_9_next_target", "next target is observed Hodge/current owner clause", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4128_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4128*")) or any(FORMALIZATION.rglob("4128-Y5-R2FR*"))
    add("VAL4128_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4128_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4128_VALIDATION.csv"
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
