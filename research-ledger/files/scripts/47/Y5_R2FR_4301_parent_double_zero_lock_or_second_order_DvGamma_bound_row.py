from __future__ import annotations

import csv
import io
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4301"
CLAIM_ID = "L-142"
BRANCH = "MTS_R2FR_Y5_PARENT_DOUBLE_ZERO_LOCK_OR_SECOND_ORDER_DVGAMMA_BOUND_ROW_4301"
DECISION = "PARENT_DOUBLE_ZERO_LOCK_REDUCED_TO_POSITIVE_OPERATOR_NOHAIR_OR_SECOND_ORDER_DVGAMMA_BOUND_NONCLAIM"
MARKER = "PPC4161_PARENT_DOUBLE_ZERO_LOCK_OR_SECOND_ORDER_DVGAMMA_BOUND_4301"
PACKET_MARKER = "PPC4161_PACKET_PARENT_DOUBLE_ZERO_LOCK_OR_SECOND_ORDER_DVGAMMA_BOUND_4301"
NEXT_TARGET = "4302-Y5-R2FR-m-lock-positive-operator-inputs-or-DvGamma-quad-numeric-row.md"

FORMAL_PATH = FORMAL / "317-PPC4161-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md"
DOC_PATH = POST / "4301-Y5-R2FR-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4301_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4301_00_4300_formal": (
        FORMAL / "316-PPC4161-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md",
        "Next target: `4301-Y5-R2FR-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md`.",
        "4300 handoff: parent double-zero lock or quadratic residual bound.",
    ),
    "SRC4301_01_4300_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4300_VERTICAL_DOUBLE_ZERO_THEOREM.csv",
        "DZT4300_3_parent_lock_required",
        "4300 says the theorem fires only if parent lock is signed.",
    ),
    "SRC4301_02_4300_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4300_RESIDUAL_ORDER_REDUCTION.csv",
        "ROR4300_1_second_order_after_double_zero",
        "4300 second-order Gamma residual after double-zero lock.",
    ),
    "SRC4301_03_1533_contract": (
        POST / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
        "VAC1533_4_local_lock",
        "1533 parent double-zero contract and local lock requirement.",
    ),
    "SRC4301_04_1533_chain": (
        POST / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
        "DZD1533_4_chain_silence",
        "1533 chain-silence theorem for algebraic m/Lcg coefficients.",
    ),
    "SRC4301_05_1533_lock": (
        POST / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
        "LOCK1533_0_operator",
        "1533 positive-operator/no-hair lock target.",
    ),
    "SRC4301_06_124_extremality": (
        FORMAL / "124-fixed-point-extremality-origin.md",
        "double_zero_parent_derived = false",
        "Older fixed-point audit keeps scalar double-zero origin unsigned.",
    ),
    "SRC4301_07_79_fixed_point": (
        FORMAL / "79-local-fixed-point-mechanism.md",
        "local_fixed_point_mechanism_conditional_closure_not_parent_derived",
        "Local fixed-point mechanism exists as closure, not parent theorem.",
    ),
    "SRC4301_08_3534_origin": (
        POST / "3534-Y5-R2FR-MTS-variable-to-local-EH-quotient-map-and-double-zero-origin.md",
        "representation_norm_square_route_identified",
        "Best double-zero origin route: representation/norm-square, parent unsigned.",
    ),
    "SRC4301_09_3902_runner": (
        POST / "3902-Y5-R2FR-second-order-gamma-bound-and-stationary-Gdot-calibration.md",
        "GAM3902_3_gamma2",
        "Existing second-order gamma runner pattern.",
    ),
    "SRC4301_10_4293_requirements": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "4293 imported local precision gates.",
    ),
}

LOCK_CONTRACT_ROWS = [
    (
        "PLC4301_0_parent_variable",
        "m is a parent local memory/vacuum variable, not just a readout scalar",
        "S_parent contains or constrains m before projection/readout.",
        "Needed so m_* is a physical branch value.",
        "UNSIGNED",
    ),
    (
        "PLC4301_1_parent_potential",
        "there is a parent local potential/source functional V(m)",
        "V'(m_*)=0 and mu_m^2:=V''(m_*) is finite after gauge/constraint modes are removed.",
        "Gives the stationary part of F_m(m_*)=0.",
        "CONDITIONAL_FORM",
    ),
    (
        "PLC4301_2_vacuum_subtraction",
        "define F_vac(m)=V(m)-V(m_*) in the same local branch",
        "F_vac(m_*)=0 and F_vac'(m_*)=V'(m_*)=0.",
        "Gives the double zero without fitting local tests.",
        "CONDITIONAL_IDENTITY",
    ),
    (
        "PLC4301_3_local_lock_operator",
        "delta m obeys a positive local operator",
        "L_m delta m:=(-Z_m box + mu_m^2)delta m = J_m+B_m+N(delta m).",
        "Turns a stationary point into actual local locking/no-hair or a finite bound.",
        "MISSING_PARENT_OPERATOR",
    ),
    (
        "PLC4301_4_gap_and_boundary",
        "L_m has a positive gap and no unsuppressed boundary/source injection",
        "<delta m,L_m delta m> >= lambda_m ||delta m||^2 with lambda_m>0 and silent/bounded J_m,B_m.",
        "The exact zero branch requires J_m=B_m=N=0 with admissible boundary conditions.",
        "MISSING_GAP_SOURCE_BOUNDARY_INPUTS",
    ),
    (
        "PLC4301_5_verdict",
        "parent double-zero lock",
        "PLC4301_0..4 imply m=m_* and hence D_v Gamma_eff=0; otherwise use quadratic bound rows.",
        "The current corpus has the contract but not the live parent signatures.",
        "LOCK_NOT_PARENT_SIGNED",
    ),
]

EULER_ROWS = [
    (
        "EL4301_0_action_form",
        "candidate local parent sector",
        "S_m,loc = int sqrt(-g)[-1/2 Z_m nabla m nabla m - V(m) + J_m m] + B_m",
        "This is a minimal proof scaffold, not a discovered live parent action.",
        "SCAFFOLD_NONCLAIM",
    ),
    (
        "EL4301_1_vacuum_stationarity",
        "stationary vacuum",
        "V'(m_*)=0, F_vac(m)=V(m)-V(m_*), so F_vac(m_*)=F_vac'(m_*)=0",
        "This is the parent-action origin of the double zero if V is real.",
        "EXACT_IF_PARENT_V_EXISTS",
    ),
    (
        "EL4301_2_linearized_lock",
        "local perturbation equation",
        "(-Z_m box + mu_m^2)delta m = J_m + B_m + O(delta m^2), with mu_m^2=V''(m_*)",
        "This is the exact object that must be no-haired or bounded.",
        "DERIVED_CONTRACT",
    ),
    (
        "EL4301_3_exact_nohair",
        "zero source/boundary branch",
        "if lambda_m>0 and J_m=B_m=0 with no zero mode, then delta m=0 by the positive energy identity",
        "Then D_v Gamma_eff=0 in the Gamma trace channel.",
        "CONDITIONAL_ZERO_THEOREM",
    ),
    (
        "EL4301_4_finite_bound",
        "nonzero source/boundary fallback",
        "||delta m|| <= lambda_m^-1 (||J_m||+||B_m||+||N||)",
        "This feeds the second-order D_v Gamma residual.",
        "BOUND_TEMPLATE_MISSING_INPUTS",
    ),
    (
        "EL4301_5_vertical_bound",
        "vertical perturbation fallback",
        "||D_v delta m|| <= lambda_m^-1 (||D_v J_m||+||D_v B_m||+||D_v N||+||D_v L_m|| ||delta m||)",
        "Needed because D_v Gamma contains delta m D_v delta m after the double zero.",
        "BOUND_TEMPLATE_MISSING_INPUTS",
    ),
]

BOUND_ROWS = [
    (
        "BQ4301_0_delta_m",
        "delta_m_bound",
        "Delta_m <= (J_m_bound+B_m_bound+N_m_bound)/lambda_m",
        "lambda_m;J_m_bound;B_m_bound;N_m_bound",
        "MISSING_POSITIVE_OPERATOR_AND_SOURCE_BOUNDS",
    ),
    (
        "BQ4301_1_Dv_delta_m",
        "Dv_delta_m_bound",
        "Delta_Dv_m <= (DvJ_m_bound+DvB_m_bound+DvN_m_bound+DvL_m_bound*Delta_m)/lambda_m",
        "lambda_m;DvJ_m_bound;DvB_m_bound;DvN_m_bound;DvL_m_bound;Delta_m",
        "MISSING_VERTICAL_SOURCE_BOUNDS",
    ),
    (
        "BQ4301_2_Dv_ln_Lcg",
        "Dv_ln_Lcg_bound",
        "Delta_Dv_ln_Lcg is zero if L_cg is fixed/q-basic, otherwise it must be source-bounded.",
        "fixed-Lcg theorem or D_v ln L_cg source row",
        "MISSING_LCG_VERTICAL_BOUND",
    ),
    (
        "BQ4301_3_DvGamma_quad",
        "C4301_DVGAMMA_QUAD_BOUND",
        "C_quad <= N_P/a_ref * Lmin^-2*|F_2|*(Delta_m*Delta_Dv_m + Delta_m^2*Delta_Dv_ln_Lcg) + derivative/projector terms",
        "N_P;a_ref;Lmin;F_2;Delta_m;Delta_Dv_m;Delta_Dv_ln_Lcg;projector derivative terms",
        "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
    ),
]


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4301 turns the 4300 double-zero Gamma theorem into a parent-lock proof gate. A parent sector with "
                "F_vac(m)=V(m)-V(m_*), V'(m_*)=0 and a positive local operator "
                "L_m delta m=(-Z_m box+mu_m^2)delta m=J_m+B_m+N(delta m) gives an exact no-hair branch when the operator "
                "has a positive gap and source/boundary terms vanish. If not, 4301 provides the finite quadratic bound "
                "C_quad <= N_P/a_ref Lmin^-2 |F_2|(Delta_m Delta_Dv_m + Delta_m^2 Delta_Dv_ln_Lcg) plus derivative/projector terms."
            ),
            (
                "4301 source register, parent lock contract, Euler/no-hair derivation, second-order bound rows, "
                "coefficient-to-4293 gate, decision, firewall, status, next-target and validation CSV."
            ),
            "private_parent_double_zero_lock_reduced_to_positive_operator_or_quadratic_bound_nonclaim",
            (
                "Source or derive lambda_m, J_m/B_m silence, D_v source bounds, F_2, Lmin, projector norm and a_ref; otherwise the "
                "Gamma trace route remains conditional."
            ),
            (
                "Claiming the parent lock is signed, treating the scaffold action as the live action, scoring C_quad with missing inputs, "
                "or using Gamma trace no-hair to erase Khat/connection/boundary/matter residuals."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def requirement_rows() -> List[Dict[str, str]]:
    return csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def parent_lock_contract_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for clause_id, clause, formula, effect, status in LOCK_CONTRACT_ROWS:
        rows.append(
            {
                **common(),
                "clause_id": clause_id,
                "clause": clause,
                "formula_or_contract": formula,
                "effect": effect,
                "status": status,
                "parent_signed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def euler_lock_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for derivation_id, object_name, formula, interpretation, status in EULER_ROWS:
        rows.append(
            {
                **common(),
                "derivation_id": derivation_id,
                "object": object_name,
                "formula": formula,
                "interpretation": interpretation,
                "status": status,
                "fires_now": "False" if "MISSING" in status or status == "SCAFFOLD_NONCLAIM" else "conditional",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def second_order_bound_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for bound_id, name, formula, required_inputs, status in BOUND_ROWS:
        rows.append(
            {
                **common(),
                "bound_id": bound_id,
                "name": name,
                "formula": formula,
                "required_inputs": required_inputs,
                "current_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def coefficient_gate_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for requirement in requirement_rows():
        required_value = requirement.get("required_value", "MISSING_REQUIRED_VALUE")
        required_numeric = to_float(required_value)
        rows.append(
            {
                **common(),
                "gate_id": f"G4301_{len(rows):03d}",
                "coefficient_id": "C4301_DVGAMMA_QUAD_BOUND",
                "arena_requirement": requirement.get("requirement_id", ""),
                "arena": requirement.get("arena", ""),
                "observable": requirement.get("observable", ""),
                "required_value": required_value,
                "units": requirement.get("units", ""),
                "coefficient_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "required_value_positive_numeric": str(math.isfinite(required_numeric) and required_numeric > 0),
                "comparison_status": "NOT_RUN_MISSING_COEFFICIENT",
                "interpretation": "Use only after parent double-zero lock reduces the Gamma trace channel to quadratic order.",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4301_0",
            "decision": "PARENT_LOCK_NOT_SIGNED_BUT_REDUCED_TO_POSITIVE_OPERATOR_GATE",
            "why": "The missing object is no longer abstract: it is lambda_m plus source/boundary/vertical bounds for the m-lock operator.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4301_1",
            "decision": "SECOND_ORDER_BOUND_ROW_READY_NOT_SCORE_READY",
            "why": "C4301_DVGAMMA_QUAD_BOUND has the correct algebraic inputs but no numeric/source-backed values.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    forbidden = [
        ("FW4301_0", "Do not treat the scaffold S_m,loc as the live parent action without source ownership."),
        ("FW4301_1", "Do not fire the exact no-hair branch without lambda_m>0 and J_m=B_m=0/no-zero-mode proof."),
        ("FW4301_2", "Do not score C4301_DVGAMMA_QUAD_BOUND while any required input is missing."),
        ("FW4301_3", "Do not let a Gamma trace lock erase D_v K_hat, Delta_K, connection, boundary or matter-coupling residuals."),
        ("FW4301_4", "Do not claim local GR, Newton, PPN, WEP, clock, orbital, R10 or Gdot pass from 4301."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in forbidden
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STAT4301_0",
            "object": "parent_double_zero_lock",
            "status": "REDUCED_TO_POSITIVE_OPERATOR_NOHAIR_OR_BOUND",
            "effect": "The next proof object is lambda_m/source/boundary silence, not another broad missing-coupling note.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4301_1",
            "object": "D_v Gamma_eff",
            "status": "ZERO_IF_PARENT_LOCK_FIRES_ELSE_QUADRATIC_BOUND",
            "effect": "Linear Gamma leakage remains demoted only conditionally.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4301_2",
            "object": "C4301_DVGAMMA_QUAD_BOUND",
            "status": "TEMPLATE_NONCLAIM_MISSING_INPUTS",
            "effect": "Ready for source filling after lambda_m/J/B/F2/Lmin/projection/a_ref inputs exist.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4301_3",
            "object": "local_GR_claim",
            "status": "BLOCKED_NONCLAIM",
            "effect": "Khat, connection, boundary, matter descent and empirical gates remain open.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NT4301_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can lambda_m, source/boundary silence and vertical source bounds be derived or sourced for the m-lock operator?",
            "preferred_route": "prove positive operator/no-hair for delta m in the local exterior",
            "fallback_route": "fill C4301_DVGAMMA_QUAD_BOUND with sourced lambda_m, J_m, B_m, F_2, Lmin, projection norm and a_ref",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def markdown_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _column in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row.get(column, "").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def formal_doc() -> str:
    return f"""
# 317 PPC4161 parent double-zero lock or second-order DvGamma bound row

Marker: `{MARKER}`

## Decision

`{DECISION}`

4301 asks whether the 4300 double-zero can actually fire. The answer is: conditionally yes, if the local memory/vacuum perturbation has a parent positive-operator/no-hair theorem; not yet as a live MTS claim.

## Parent lock contract

{markdown_table(parent_lock_contract_rows(), ["clause_id", "clause", "status", "effect"])}

## Euler/no-hair derivation

The minimal proof scaffold is:

```text
S_m,loc = int sqrt(-g)[-1/2 Z_m nabla m nabla m - V(m) + J_m m] + B_m
F_vac(m) = V(m) - V(m_*)
V'(m_*) = 0
```

Then:

```text
F_vac(m_*) = 0,
F_vac'(m_*) = 0,
L_m delta m := (-Z_m box + mu_m^2)delta m = J_m + B_m + N(delta m).
```

{markdown_table(euler_lock_rows(), ["derivation_id", "object", "status", "interpretation"])}

## Second-order fallback

If exact no-hair fails but the double-zero form is still parent-accepted, the Gamma trace channel is bounded by:

```text
C_quad <= N_P/a_ref * Lmin^-2*|F_2|*(Delta_m*Delta_Dv_m + Delta_m^2*Delta_Dv_ln_Lcg)
          + derivative/projector terms.
```

{markdown_table(second_order_bound_rows(), ["bound_id", "name", "status", "required_inputs"])}

## Result

This checkpoint does not close local GR. It sharpens the next missing thing:

```text
lambda_m > 0,
J_m = 0 or bounded,
B_m = 0 or bounded,
D_v source/boundary terms bounded,
F_2, Lmin, projection norm, a_ref sourced.
```

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4301 Y5 R2FR parent double-zero lock or second-order DvGamma bound row

## Outcome

The parent double-zero lock is reduced to a positive-operator/no-hair gate:

```text
L_m delta m := (-Z_m box + mu_m^2)delta m = J_m + B_m + N(delta m).
```

If `lambda_m>0` and the source/boundary terms vanish with no zero mode, then `delta m=0` and the 4300 Gamma trace zero fires. If not, the fallback is the second-order bound:

```text
C_quad <= N_P/a_ref * Lmin^-2*|F_2|*(Delta_m*Delta_Dv_m + Delta_m^2*Delta_Dv_ln_Lcg)
```

## Status

Private nonclaim. The proof object is now concrete, but the required source/gap/boundary inputs are not yet signed or numeric.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    contract = csv_rows(paths["parent_lock_contract"])
    euler = csv_rows(paths["euler_lock_derivation"])
    bounds = csv_rows(paths["second_order_bound_rows"])
    gates = csv_rows(paths["coefficient_to_4293_gate"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4301_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4301_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4301_2_contract_verdict",
            any(row["clause_id"] == "PLC4301_5_verdict" and row["status"] == "LOCK_NOT_PARENT_SIGNED" for row in contract),
            "parent lock remains unsigned and not promoted",
        ),
        (
            "VAL4301_3_euler_nohair_gate",
            any(row["derivation_id"] == "EL4301_3_exact_nohair" and row["status"] == "CONDITIONAL_ZERO_THEOREM" for row in euler)
            and any(row["derivation_id"] == "EL4301_4_finite_bound" and row["status"] == "BOUND_TEMPLATE_MISSING_INPUTS" for row in euler),
            "Euler/no-hair exact branch and finite bound branch both exist",
        ),
        (
            "VAL4301_4_second_order_bound",
            any(row["bound_id"] == "BQ4301_3_DvGamma_quad" and row["name"] == "C4301_DVGAMMA_QUAD_BOUND" and row["status"] == "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW" for row in bounds),
            "second-order DvGamma bound row exists and remains unscored",
        ),
        (
            "VAL4301_5_4293_gate_links",
            bool(gates)
            and any(row["coefficient_id"] == "C4301_DVGAMMA_QUAD_BOUND" and row["arena_requirement"] == "REQ4293_WEP" for row in gates)
            and all(row["comparison_status"] == "NOT_RUN_MISSING_COEFFICIENT" for row in gates),
            "C4301 is linked to 4293 gates but not scored",
        ),
        (
            "VAL4301_6_required_values_positive",
            bool(gates) and all(row["required_value_positive_numeric"] == "True" for row in gates),
            "all imported 4293 required values are positive numeric",
        ),
        ("VAL4301_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4301_8_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4301_9_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-142 private nonclaim row",
        ),
        (
            "VAL4301_10_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4301_11_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4301_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4301_SOURCE_REGISTER.csv",
        "parent_lock_contract": SOURCE_DIR / "P8_Y5_R2FR_4301_PARENT_LOCK_CONTRACT.csv",
        "euler_lock_derivation": SOURCE_DIR / "P8_Y5_R2FR_4301_EULER_LOCK_DERIVATION.csv",
        "second_order_bound_rows": SOURCE_DIR / "P8_Y5_R2FR_4301_SECOND_ORDER_DVGAMMA_BOUND_ROWS.csv",
        "coefficient_to_4293_gate": SOURCE_DIR / "P8_Y5_R2FR_4301_COEFFICIENT_TO_4293_GATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4301_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4301_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4301_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4301_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["parent_lock_contract"], parent_lock_contract_rows())
    write_csv(paths["euler_lock_derivation"], euler_lock_rows())
    write_csv(paths["second_order_bound_rows"], second_order_bound_rows())
    write_csv(paths["coefficient_to_4293_gate"], coefficient_gate_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4301 parent double-zero lock or quadratic Gamma bound",
        (
            "4301 reduces the parent double-zero lock to a concrete positive-operator/no-hair gate for `delta m`: "
            "`L_m delta m=(-Z_m box+mu_m^2)delta m=J_m+B_m+N(delta m)`. Exact Gamma trace silence needs a positive gap and "
            "silent source/boundary terms; otherwise the live fallback is `C4301_DVGAMMA_QUAD_BOUND` against the 4293 gates."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4301 packet m-lock operator gate",
        (
            "Packet update: the double-zero is not hand-waved. The next evidence must be `lambda_m`, source/boundary silence, "
            "or real quadratic coefficient inputs. Khat/connection/boundary/matter residuals remain separate."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
