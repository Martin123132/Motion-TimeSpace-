from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4314"
CLAIM_ID = "L-155"
BRANCH = "MTS_R2FR_Y5_RADIATIVE_POYNTING_NO_FLUX_OR_BOUNDARY_FLUX_ROW_4314"
DECISION = "RADIATIVE_POYNTING_CLOSED_COLLAR_ZERO_OR_DIMENSIONAL_BOUNDARY_FLUX_ROW_DERIVED_NONCLAIM"
MARKER = "PPC4161_RADIATIVE_POYNTING_NO_FLUX_OR_BOUNDARY_FLUX_ROW_4314"
PACKET_MARKER = "PPC4161_PACKET_RADIATIVE_POYNTING_NO_FLUX_OR_BOUNDARY_FLUX_ROW_4314"
NEXT_TARGET = "4315-Y5-R2FR-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md"

FORMAL_PATH = FORMAL / "330-PPC4161-radiative-Poynting-no-flux-or-boundary-flux-row.md"
DOC_PATH = POST / "4314-Y5-R2FR-radiative-Poynting-no-flux-or-boundary-flux-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4314_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4314_00_4313_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4313_NEXT_TARGET.csv",
        "4314-Y5-R2FR-radiative-Poynting-no-flux-or-boundary-flux-row.md",
        "4313 handoff selecting radiative Poynting no-flux or boundary-flux row.",
    ),
    "SRC4314_01_4313_defect": (
        SOURCE_DIR / "P8_Y5_R2FR_4313_DEFECT_REDUCTION.csv",
        "Delta_rad_Poynting",
        "4313 leaves radiative Poynting as the next EM frontier.",
    ),
    "SRC4314_02_4312_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv",
        "R_EM_Poynting <=",
        "4312 bound where Phi_rad feeds R_EM_Poynting and Eta_H.",
    ),
    "SRC4314_03_279_formal": (
        FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Phi_EM_rad = int_boundary S_Poynting dot n dA.",
        "4263 formal closed-collar theorem and radiative fallback.",
    ),
    "SRC4314_04_4263_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4263_CLOSED_COLLAR_THEOREM.csv",
        "CCT4263_1_closed_collar_flux",
        "closed-collar no-radiation clause.",
    ),
    "SRC4314_05_4263_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4263_BOUNDARY_FLUX_ORIENTATION_ROWS.csv",
        "abs(Phi_EM_rad)/(M_H*c^2/Delta_tau)",
        "4263 boundary-flux normalization row.",
    ),
    "SRC4314_06_192_noflux": (
        FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md",
        "F_rad[tau] != 0  =>  route as boundary charge",
        "local no-flux theorem: radiation routes as boundary charge if nonzero.",
    ),
    "SRC4314_07_191_guard": (
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Radiative EM is not erased.",
        "Maxwell-Hodge Poynting stress owner and radiative boundary guard.",
    ),
    "SRC4314_08_4311_SU": (
        FORMAL / "327-PPC4161-lambda-floor-source-row-or-collar-residual-first-bound.md",
        "S_U := R_U + N_N + N_boundary",
        "4311 residual numerator receiving boundary flux.",
    ),
    "SRC4314_09_309_precision": (
        FORMAL / "309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md",
        "order-one projection of epsilon_AJ_seed into local observables fails",
        "local precision guard forbidding unbounded boundary flux leakage.",
    ),
    "SRC4314_10_newton_guard": (
        POST / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md",
        "R_eq",
        "source-to-Newton equality gate remains open.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "em_local_gr",
        (
            "4314 derives the radiative Poynting no-flux or boundary-flux row needed after the 4313 EM current gate. "
            "It separates instantaneous boundary power P_rad_EM(tau)=int_partialW S_Poynting dot n dA from integrated "
            "radiated energy E_rad_EM=int_DeltaTau P_rad_EM d tau, so the dimensionless local leakage is "
            "epsilon_rad_EM=|E_rad_EM|/(M_H c^2) or equivalently |P_rad_EM|/(M_H c^2/DeltaTau) for a constant-power "
            "window. In the static/quasi-static closed-collar branch with fixed orientation and no-through EM flux, "
            "Delta_rad_Poynting=0. If flux survives, it is routed as N_boundary/Hamiltonian boundary flux and feeds "
            "R_EM_Poynting, Eta_H and S_U; it is not erased or counted as a hidden bulk source. No local GR/Newton/R10/PPN "
            "claim fires."
        ),
        (
            "4314 source register, radiative no-flux theorem, dimensional flux normalization, boundary flux bound row, "
            "collar residual update, runner, firewall, status, next-target and validation CSV."
        ),
        "private_radiative_Poynting_closed_collar_zero_or_boundary_flux_bound_nonclaim",
        (
            "Parent-sign closed-collar no-through-flux for the local test branch, or source Phi_rad/P_rad/E_rad with "
            "units and observation window and propagate it into N_boundary, Eta_H and S_U."
        ),
        (
            "Erasing real radiation, using time-averaged zero for instantaneous clock/PPN claims, counting Poynting as "
            "both Hilbert stress and separate source, or claiming local GR/Newton while lambda/source-equality gates remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def noflux_theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "NF4314_0_poynting_owner",
            "Poynting owner",
            "S_i=-T_EM(n,e_i) in the Maxwell-Hodge Hilbert branch",
            "Poynting is real Hilbert EM flux, not an extra source",
            "IMPORTED_EXACT_IDENTITY",
        ),
        (
            "NF4314_1_power_definition",
            "instantaneous boundary power",
            "P_rad_EM(tau) := int_partialW S_Poynting dot n dA",
            "power crossing the local collar at time tau",
            "DEFINITION_DERIVED",
        ),
        (
            "NF4314_2_energy_definition",
            "integrated radiated energy",
            "E_rad_EM[DeltaTau] := int_tau0^tau1 P_rad_EM(tau) d tau",
            "energy leakage over the local test window",
            "DEFINITION_DERIVED",
        ),
        (
            "NF4314_3_closed_collar_zero",
            "closed/static collar zero",
            "P_rad_EM(tau)=0 pointwise on the local test window plus fixed orientation/outward normal",
            "Delta_rad_Poynting=0 and Phi_rad=0",
            "EXACT_ZERO_IF_BRANCH_SIGNED",
        ),
        (
            "NF4314_4_average_zero_limit",
            "average-only zero",
            "E_rad_EM[DeltaTau]=0 but P_rad_EM(tau) not pointwise zero",
            "safe only for window-averaged source charge, not instantaneous clock/PPN claims",
            "LIMITED_ZERO_AVERAGE_BRANCH",
        ),
        (
            "NF4314_5_open_flux",
            "open radiative branch",
            "P_rad_EM or E_rad_EM nonzero",
            "route to N_boundary/Hamiltonian flux, not hidden bulk source",
            "BOUNDARY_BOUND_REQUIRED",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, clause, statement, result, status in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "statement": statement,
                "result": result,
                "status": status,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def dimensional_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DN4314_0_Prad",
            "P_rad_EM",
            "int_partialW S_Poynting dot n dA",
            "power",
            "W or energy/time",
            "instantaneous radiative crossing of the collar",
        ),
        (
            "DN4314_1_Erad",
            "E_rad_EM",
            "int_DeltaTau P_rad_EM d tau",
            "energy",
            "J or mass*length^2/time^2",
            "window-integrated radiative leakage",
        ),
        (
            "DN4314_2_epsilon_energy",
            "epsilon_rad_EM_energy",
            "|E_rad_EM|/(M_H c^2)",
            "dimensionless",
            "1",
            "fractional source-energy leakage over the window",
        ),
        (
            "DN4314_3_epsilon_power",
            "epsilon_rad_EM_power",
            "|P_rad_EM|/(M_H c^2/DeltaTau)",
            "dimensionless",
            "1",
            "constant-power or pointwise power-budget version",
        ),
        (
            "DN4314_4_Phi_rad",
            "Phi_rad",
            "use as E_rad_EM for integrated-energy rows, or P_rad_EM only when explicitly tagged as power",
            "tagged energy_or_power",
            "must declare",
            "prevents the 4263 Phi symbol from mixing dimensions",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for norm_id, symbol, definition, quantity_type, units, role in specs:
        row = base_row()
        row.update(
            {
                "norm_id": norm_id,
                "symbol": symbol,
                "definition": definition,
                "quantity_type": quantity_type,
                "units": units,
                "role": role,
                "source_path": "",
                "numeric_value": "",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def boundary_bound_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "BF4314_0_zero",
            "Delta_rad_Poynting",
            "P_rad_EM(tau)=0 pointwise on closed collar",
            "0",
            "removes radiative EM boundary term from R_EM_Poynting",
            "CONDITIONAL_ZERO_NOT_LIVE_GLOBALLY",
        ),
        (
            "BF4314_1_energy_bound",
            "epsilon_rad_EM_energy",
            "|int_DeltaTau int_partialW S dot n dA d tau|/(M_H c^2)",
            "missing numeric/source row",
            "feeds N_boundary and source-energy leakage",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "BF4314_2_power_bound",
            "epsilon_rad_EM_power",
            "|int_partialW S dot n dA|/(M_H c^2/DeltaTau)",
            "missing numeric/source row",
            "feeds instantaneous local clock/PPN power-budget checks",
            "BOUND_FORMULA_READY_VALUES_MISSING",
        ),
        (
            "BF4314_3_R_EM_update",
            "R_EM_Poynting",
            "R_EM_Poynting <= R_EM_noRad + |E_rad_EM| or source-normalized C_rad epsilon_rad_EM",
            "guarded update",
            "4312 EM residual with radiative term explicit",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "BF4314_4_EtaH_update",
            "Eta_H",
            "Eta_H >= Eta_H_noRad + C_rad epsilon_rad_EM",
            "guarded update",
            "lambda floor weakens if radiative boundary flux survives",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "BF4314_5_SU_update",
            "S_U",
            "S_U <= S_U_noRad + N_boundary_rad_EM",
            "guarded update",
            "collar residual numerator receives open EM radiation only through boundary row",
            "FORMULA_READY_VALUES_MISSING",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for bound_id, symbol, condition_or_law, value_or_bound, feeds, status in specs:
        row = base_row()
        row.update(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "condition_or_law": condition_or_law,
                "value_or_bound": value_or_bound,
                "feeds": feeds,
                "status": status,
                "source_path": "",
                "numeric_value": "",
                "units": "dimensionless after normalization or declared energy/power before normalization",
                "next_action": "prove closed-collar no-flux or fill sourced P_rad/E_rad values for the chosen test window",
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "RUN4314_0_current_corpus",
            "current corpus",
            "CONDITIONAL_ZERO_OR_BOUND",
            "4263 provides a closed-collar zero branch, but open radiation remains a retained finite boundary bound",
            "do not claim local tests from missing flux values",
        ),
        (
            "RUN4314_1_static_closed",
            "static/quasi-static closed collar with pointwise P_rad_EM=0",
            "ALLOW_DELTA_RAD_ZERO_CONDITIONAL",
            "radiative EM does not feed R_EM_Poynting, Eta_H or S_U in that branch",
            "still requires Hodge/constitutive and lambda/source-equality gates",
        ),
        (
            "RUN4314_2_average_zero",
            "window-integrated E_rad_EM=0 but nonzero instantaneous power",
            "ALLOW_AVERAGE_ONLY",
            "safe for averaged source charge only; not enough for instantaneous clock/PPN residuals",
            "keep power row for time-local observables",
        ),
        (
            "RUN4314_3_open_radiation",
            "nonzero P_rad_EM or E_rad_EM",
            "ROUTE_TO_BOUNDARY",
            "radiation contributes to N_boundary and Hamiltonian/source flux, not hidden bulk m-source",
            "fill energy/power bound row",
        ),
        (
            "RUN4314_4_local_claim",
            "claim local GR/Newton/R10/PPN now",
            "REJECT",
            "lambda components, Hodge/constitutive defects, source equality, I_commutator and projection gates remain open",
            "continue derivation chain",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, case, result, reason, next_action in specs:
        row = base_row()
        row.update(
            {
                "runner_id": runner_id,
                "case": case,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "score_ready": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "DEC4314_0_dimension",
            "PHI_RAD_DIMENSIONS_FIXED",
            "The radiative row now separates boundary power P_rad_EM from integrated energy E_rad_EM.",
            "use energy normalization for window leakage and power normalization for instantaneous checks",
        ),
        (
            "DEC4314_1_zero",
            "NO_FLUX_ZERO_IS_BRANCH_CONDITIONAL",
            "Pointwise no-through EM flux on a closed static/quasi-static collar can set Delta_rad_Poynting=0.",
            "do not apply to open radiative systems",
        ),
        (
            "DEC4314_2_bound",
            "OPEN_RADIATION_IS_BOUNDARY_FLUX",
            "Nonzero Poynting flux is physical boundary/Hamiltonian flux and feeds N_boundary, Eta_H and S_U.",
            "fill sourced flux values before scoring local arenas",
        ),
        (
            "DEC4314_3_frontier",
            "HODGE_CONSTITUTIVE_OWNER_NEXT",
            "After current and radiation are structured, the remaining EM defect with teeth is Delta_Hodge_EM/constitutive ownership.",
            NEXT_TARGET,
        ),
        (
            "DEC4314_4_claim",
            "NO_LOCAL_CLAIM",
            "This closes or bounds one EM boundary channel but not the full local-GR/Newton reduction.",
            "keep all claim flags false",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    rules = [
        "Do not erase nonzero EM radiation; route it as boundary/Hamiltonian flux.",
        "Do not use a time-averaged zero flux row for instantaneous clock or PPN claims.",
        "Do not mix power and energy dimensions under the same Phi_rad symbol without an explicit tag.",
        "Do not count Poynting both as Hilbert EM stress and as a standalone bulk source.",
        "Do not claim local GR/Newton/R10/PPN from the radiative flux gate alone.",
    ]
    rows: List[Dict[str, str]] = []
    for index, rule in enumerate(rules):
        row = base_row()
        row.update({"firewall_id": f"FW4314_{index}", "rule": rule, "status": "ACTIVE"})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4314_0_Prad", "P_rad_EM", "DEFINED", "instantaneous boundary power through the collar"),
        ("STAT4314_1_Erad", "E_rad_EM", "DEFINED", "integrated radiative energy over the test window"),
        ("STAT4314_2_zero", "Delta_rad_Poynting", "ZERO_OR_BOUND", "zero only for closed pointwise no-flux branch"),
        ("STAT4314_3_boundary", "N_boundary_rad_EM", "EXPLICIT", "open radiation feeds boundary flux, not hidden bulk source"),
        ("STAT4314_4_Hodge", "Delta_Hodge_EM", "NEXT_OPEN_GATE", "constitutive/Hodge owner still needs closure or bound"),
        ("STAT4314_5_local", "local GR/Newton", "BLOCKED", "source coupling sharper, full local reduction still open"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, item, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "item": item, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4314_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the observed Hodge/constitutive relation be parent-owned, or must Delta_Hodge_EM be bounded as the next EM residual?",
            "preferred_route": "derive same-Hodge constitutive ownership on the calibrated visible local branch",
            "fallback_route": "fill nonclaim Delta_Hodge_EM bound rows feeding R_EM_Poynting, Eta_H and local precision gates",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal_text = f"""# 330 PPC4161 radiative Poynting no-flux or boundary-flux row

Marker: `{MARKER}`

## Decision

`{DECISION}`

4314 tightens the radiative Poynting gate by separating power from energy:

```text
P_rad_EM(tau) := int_partialW S_Poynting dot n dA,
E_rad_EM[DeltaTau] := int_tau0^tau1 P_rad_EM(tau) d tau.
```

The dimensionless leakage rows are:

```text
epsilon_rad_EM_energy = |E_rad_EM|/(M_H c^2),
epsilon_rad_EM_power  = |P_rad_EM|/(M_H c^2/DeltaTau).
```

Closed-collar zero is honest only when:

```text
P_rad_EM(tau)=0 pointwise on the local test window,
orientation and outward normal fixed before variation.
```

Then:

```text
Delta_rad_Poynting = 0.
```

If the flux is nonzero, it is not deleted:

```text
N_boundary_rad_EM := |E_rad_EM|/(M_H c^2)
```

or the power-normalized analogue, and it feeds `R_EM_Poynting`, `Eta_H`, and `S_U`.

## Radiative No-Flux Theorem

{md_table(tables["noflux"], ["theorem_id", "clause", "statement", "result", "status"])}

## Dimensional Normalization

{md_table(tables["dimensional"], ["norm_id", "symbol", "definition", "quantity_type", "units", "role"])}

## Boundary Flux Bound Row

{md_table(tables["bounds"], ["bound_id", "symbol", "condition_or_law", "value_or_bound", "feeds", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "case", "result", "reason"])}

## Result

Radiative Poynting is now a clean zero-or-bound gate. Closed collars can set it to zero; open radiation becomes a declared boundary flux with dimensions and test-window normalization.

Next target: `{NEXT_TARGET}`.
"""
    doc_text = f"""# 4314 - radiative Poynting no-flux or boundary-flux row

## Verdict
- Derived separate power and energy rows: `P_rad_EM=int_partialW S dot n dA` and `E_rad_EM=int P_rad_EM d tau`.
- Fixed the dimensionless leakage normalization: `|E_rad_EM|/(M_H c^2)` or `|P_rad_EM|/(M_H c^2/DeltaTau)`.
- Closed-collar branch: pointwise no-through EM flux gives `Delta_rad_Poynting=0`.
- Open-radiation branch: flux feeds `N_boundary`, `R_EM_Poynting`, `Eta_H`, and `S_U`; it is not erased.
- No local-GR/Newton/R10/PPN claim fires.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Radiative No-Flux Theorem
{md_table(tables["noflux"], ["theorem_id", "clause", "statement", "result", "status"])}

## Dimensional Normalization
{md_table(tables["dimensional"], ["norm_id", "symbol", "definition", "quantity_type", "units", "role"])}

## Boundary Flux Bound Row
{md_table(tables["bounds"], ["bound_id", "symbol", "condition_or_law", "value_or_bound", "feeds", "status", "next_action"])}

## Runner
{md_table(tables["runner"], ["runner_id", "case", "result", "reason", "next_action"])}

## Claim Firewall
{md_table(tables["firewall"], ["firewall_id", "rule", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Status
{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal_text, encoding="utf-8")
    DOC_PATH.write_text(doc_text, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"{path.name} parses with {len(rows)} rows"
    except Exception as exc:
        return False, f"{path.name} parse failure: {exc}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4314_0_sources_exist", "all cited local source paths exist", all(Path(row["source_path"]).exists() for row in tables["sources"]), "source_register")
    add("VAL4314_1_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4314_2_power_energy_split", "power and energy rows are separated", any(row["symbol"] == "P_rad_EM" for row in tables["dimensional"]) and any(row["symbol"] == "E_rad_EM" for row in tables["dimensional"]), "dimensional")
    add("VAL4314_3_closed_zero", "closed collar zero theorem exists", any(row["theorem_id"] == "NF4314_3_closed_collar_zero" for row in tables["noflux"]), "noflux")
    add("VAL4314_4_average_guard", "average-only zero guard exists", any(row["theorem_id"] == "NF4314_4_average_zero_limit" for row in tables["noflux"]), "noflux")
    add("VAL4314_5_boundary_bound", "boundary flux bound row exists", any(row["bound_id"] == "BF4314_1_energy_bound" for row in tables["bounds"]), "bounds")
    add("VAL4314_6_runner_rejects_claim", "runner rejects local claim from flux gate alone", any(row["runner_id"] == "RUN4314_4_local_claim" and row["result"] == "REJECT" for row in tables["runner"]), "runner")
    add("VAL4314_7_next_selected", f"next target is {NEXT_TARGET}", tables["next"][0]["next_target"] == NEXT_TARGET, "next")
    add(
        "VAL4314_8_claim_flags_false",
        "all generated rows keep claim flags false",
        all(row.get("claim_allowed") == "False" and row.get("valid_for_claim") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    add(
        "VAL4314_9_score_flags_false",
        "all score rows remain unscored/nonclaim",
        all(row.get("score_ready", "False") == "False" for table in tables.values() for row in table),
        "generated_tables",
    )
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4314_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4314_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "generated_docs")
    add("VAL4314_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims_register")
    add("VAL4314_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "unification_spine")
    add("VAL4314_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "private_packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4314_SOURCE_REGISTER.csv",
        "noflux": SOURCE_DIR / "P8_Y5_R2FR_4314_RADIATIVE_NOFLUX_THEOREM.csv",
        "dimensional": SOURCE_DIR / "P8_Y5_R2FR_4314_DIMENSIONAL_FLUX_NORMALIZATION.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4314_BOUNDARY_FLUX_BOUND_ROW.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4314_COLLAR_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4314_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4314_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4314_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4314_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "noflux": noflux_theorem_rows(),
        "dimensional": dimensional_rows(),
        "bounds": boundary_bound_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4314 radiative Poynting no-flux or boundary-flux row

Marker: `{MARKER}`

4314 sharpens the EM radiative boundary gate. `P_rad_EM=int_partialW S_Poynting dot n dA` is power; `E_rad_EM=int_DeltaTau P_rad_EM d tau` is energy. The closed static/quasi-static collar branch sets `Delta_rad_Poynting=0` only when `P_rad_EM(tau)=0` pointwise with fixed orientation/normal. If radiation crosses the collar, it becomes `N_boundary_rad_EM` and feeds `R_EM_Poynting`, `Eta_H`, and `S_U`; it is not hidden as a bulk source or erased.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4314 packet radiative Poynting boundary flux

Marker: `{PACKET_MARKER}`

Packet update: radiative EM flux now has a dimensionally clean zero-or-bound row. Closed collars give `Delta_rad_Poynting=0`; open collars require sourced `P_rad_EM` or `E_rad_EM` values normalized by `M_H c^2` over the test window.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
