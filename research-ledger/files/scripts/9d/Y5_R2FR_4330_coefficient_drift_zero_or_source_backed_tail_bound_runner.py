from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4330"
CLAIM_ID = "L-171"
BRANCH = "MTS_R2FR_Y5_COEFFICIENT_DRIFT_ZERO_OR_SOURCE_BACKED_TAIL_BOUND_4330"
DECISION = "FIXED_PARENT_CALIBRATED_CONSTANT_BRANCH_DQ_COEFF_ZERO_IMPORTED_EPSILON_COEFF_REMOVED_NUMERIC_G_ALPHA_NOT_PREDICTED_NONCLAIM"
MARKER = "PPC4161_COEFFICIENT_DRIFT_ZERO_OR_SOURCE_BACKED_TAIL_BOUND_4330"
PACKET_MARKER = "PPC4161_PACKET_COEFFICIENT_DRIFT_ZERO_OR_SOURCE_BACKED_TAIL_BOUND_4330"
NEXT_TARGET = "4331-Y5-R2FR-readout-frame-terminal-tail-zero-or-explicit-projection-bound.md"

FORMAL_PATH = FORMAL / "346-PPC4161-coefficient-drift-zero-or-source-backed-tail-bound.md"
DOC_PATH = POST / "4330-Y5-R2FR-coefficient-drift-zero-or-source-backed-tail-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4330_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4330_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4329_NEXT_TARGET.csv",
        "coefficient drift epsilon_coeff",
        "4329 handoff selecting epsilon_coeff as the live geometry-tail target.",
    ),
    (
        "SRC4330_01_live_tail",
        FORMAL / "345-PPC4161-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md",
        "epsilon_coeff",
        "4329 reduced geometry core retains coefficient drift.",
    ),
    (
        "SRC4330_02_kappa_G",
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "G_N = c^4 kappa_eff/(8*pi)",
        "Kappa-to-Newton normalization and numeric-G firewall.",
    ),
    (
        "SRC4330_03_ZH_split",
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "Z_H = Z_0 exp(delta_ZH)",
        "Source-measure factor split into common normalization plus physical leak.",
    ),
    (
        "SRC4330_04_kappa_topological",
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "D_A ln kappa_* = 0",
        "Private packet topological kappa lock.",
    ),
    (
        "SRC4330_05_delta_ZH",
        FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md",
        "D_A delta_ZH = 0",
        "Hilbert source-measure descent closes physical ZH leakage.",
    ),
    (
        "SRC4330_06_calibrated_G",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi)",
        "Calibrated source-coupling law and Newton/Poisson coefficient.",
    ),
    (
        "SRC4330_07_Dq_coeff",
        FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md",
        "Dq_coeff = 0",
        "4267 Dq_coeff zero for fixed parent-action/calibrated-constant branch.",
    ),
    (
        "SRC4330_08_EM_readout",
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "D_X ln g_J = 0",
        "EM kinetic/current coefficient drift killed only in calibrated q-basic visible branch.",
    ),
    (
        "SRC4330_09_guard",
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "Dq_coeff = 0",
        "4277 lists Dq_coeff as a required field-rename/coupling escape blocker.",
    ),
    (
        "SRC4330_10_4328",
        FORMAL / "344-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md",
        "epsilon_coeff",
        "4328 first exposed coefficient drift as a full-geometry tail.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                "4330 imports the fixed-parent/calibrated-constant coefficient route into the 4329-reduced geometry core. In the PPC4161-TK-H calibrated local branch, the topological log-kappa sector gives D_A ln kappa_*=0, Hilbert source-measure descent gives delta_ZH=0 and D_A delta_ZH=0, and visible EM coefficients are q-basic calibrated readout data with D_X ln g_J=D_X ln lambda_A=0. Therefore the local drift coefficient Dq_coeff and Dq_coeff_C1 vanish in this branch, and the live epsilon_coeff tail drops out of the reduced geometry core. This is not a prediction of the numerical values of G_N, alpha_EM, charge normalization, particle masses, or hbar; dynamic hidden coefficient branches remain finite residual rows.",
                "4330 source register, coefficient owner audit, zero rows, coefficient-tail bound rows, geometry/source-readout update formulas, runner, firewall, decision, status, next-target and validation CSV.",
                "private_fixed_parent_calibrated_coefficient_drift_zero_nonclaim",
                "Attack readout-frame/terminal projection tails next, while keeping dynamic coefficient/source-backed residual rows for any nonstandard branch.",
                "Claiming numeric G_N or alpha_EM from coefficient drift zero; hiding source-measure leaks inside measured G; using Dq_coeff=0 when coefficients are hidden-field functions; treating calibrated constants as fundamental predictions; or claiming local GR/R10/PPN/clock pass while readout-frame/terminal/Xi gates remain open.",
            ]
        )


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, path, needle, role in SOURCES:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "line_number": find_line(path, needle),
                "role": role,
            }
        )
    return rows


def audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "AUD4330_0_kappa_star",
            "coefficient_slot": "kappa_*",
            "owner_clause": "parent-adopted topological log-kappa sector S_top^kappa=C_top int A_3 wedge d ln(kappa_*/kappa_0)",
            "drift_statement": "d ln kappa_*=0 => D_A ln kappa_*=0",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "not_claimed": "numeric value of kappa_* or G_N",
        },
        {
            "audit_id": "AUD4330_1_ZH",
            "coefficient_slot": "Z_H=Z_0 exp(delta_ZH)",
            "owner_clause": "Hilbert source-measure descent; common Z_0 is calibration gauge",
            "drift_statement": "delta_ZH=0 and D_A delta_ZH=0",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "not_claimed": "source-measure theorem outside private branch",
        },
        {
            "audit_id": "AUD4330_2_Gcal",
            "coefficient_slot": "G_cal=c^4 kappa_eff/(8*pi)",
            "owner_clause": "single calibrated EH/Hilbert coupling product",
            "drift_statement": "D_A ln G_cal=D_A ln(kappa_* Z_H)=0",
            "status": "STRUCTURAL_COUPLING_ZERO_NUMERIC_VALUE_CALIBRATED",
            "not_claimed": "numerical G_N prediction",
        },
        {
            "audit_id": "AUD4330_3_EM_coeff",
            "coefficient_slot": "g_J, lambda_A, alpha_EM",
            "owner_clause": "q-basic calibrated visible EM readout before variation",
            "drift_statement": "D_X ln g_J=0, D_X ln lambda_A=0, b_alpha=2D_X ln g_J-D_X ln lambda_A=0",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "not_claimed": "absolute alpha_EM or charge normalization derivation",
        },
        {
            "audit_id": "AUD4330_4_Dq_coeff",
            "coefficient_slot": "Dq_coeff",
            "owner_clause": "fixed parent-action/calibrated-constant branch",
            "drift_statement": "Dq_coeff=0 and Dq_coeff_C1=0",
            "status": "CONDITIONAL_ZERO_IMPORTED_INTO_4329_CORE",
            "not_claimed": "dynamic hidden coefficient branch",
        },
        {
            "audit_id": "AUD4330_5_nonstandard",
            "coefficient_slot": "hidden coefficient functions C_i(Phi)",
            "owner_clause": "not adopted in the reduced branch",
            "drift_statement": "epsilon_coeff <= sum_i |D_v ln C_i| + source/readout projection terms",
            "status": "BOUND_RETAINED_OUTSIDE_BRANCH",
            "not_claimed": "finite coefficient rows without source-backed values",
        },
    ]


def zero_rows() -> List[Dict[str, str]]:
    return [
        {
            "zero_id": "ZERO4330_0_kappa_star",
            "symbol": "D_A ln kappa_*",
            "zero_statement": "D_A ln kappa_*=0",
            "branch_conditions": "PPC4161-TK parent-adopted topological log-kappa sector with fixed boundary/superselection data",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4330_1_delta_ZH",
            "symbol": "D_A delta_ZH",
            "zero_statement": "delta_ZH=0 and D_A delta_ZH=0",
            "branch_conditions": "Hilbert source-measure descent with common source normalization Z_0 only",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4330_2_Gcal_drift",
            "symbol": "D_A ln G_cal",
            "zero_statement": "D_A ln G_cal=D_A ln(kappa_* Z_H)=0",
            "branch_conditions": "ZERO4330_0 + ZERO4330_1; G_cal is calibrated structural coupling",
            "status": "CONDITIONAL_ZERO_NUMERIC_VALUE_NOT_PREDICTED",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4330_3_EM_norm",
            "symbol": "b_alpha",
            "zero_statement": "b_alpha=2D_X ln g_J-D_X ln lambda_A=0",
            "branch_conditions": "q-basic calibrated visible EM constants fixed before variation",
            "status": "CONDITIONAL_ZERO_ALPHA_VALUE_NOT_PREDICTED",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4330_4_Dq_coeff",
            "symbol": "Dq_coeff",
            "zero_statement": "Dq_coeff=0 and Dq_coeff_C1=0",
            "branch_conditions": "fixed parent-action/calibrated-constant branch, no hidden coefficient function C_i(Phi)",
            "status": "CONDITIONAL_ZERO_IMPORTED_INTO_REDUCED_GEOMETRY_CORE",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4330_5_epsilon_coeff",
            "symbol": "epsilon_coeff",
            "zero_statement": "epsilon_coeff=0",
            "branch_conditions": "ZERO4330_4 plus no dynamic hidden coefficient branch",
            "status": "CONDITIONAL_ZERO_IMPORTED_INTO_4329_GEOMETRY_CORE",
            "valid_for_claim": "False",
        },
    ]


def tail_rows() -> List[Dict[str, str]]:
    return [
        {
            "tail_id": "TAIL4330_0_dynamic_kappa",
            "symbol": "D_A ln kappa_*",
            "meaning": "kappa_* promoted to a hidden/local field outside topological lock",
            "bound_contribution": "|D_A ln kappa_*|",
            "observable_links": "Gdot/G; PPN; orbital; R10/fifth-force if finite range",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4330_1_source_measure",
            "symbol": "D_A delta_ZH",
            "meaning": "source-measure leakage hidden inside measured G",
            "bound_contribution": "|D_A delta_ZH|",
            "observable_links": "WEP/species; frame/readout PPN; clock; range/environment",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4330_2_EM_coeff",
            "symbol": "b_alpha",
            "meaning": "EM kinetic/current normalization drift",
            "bound_contribution": "|2D ln g_J-D ln lambda_A|",
            "observable_links": "alpha variation; spectroscopy; clocks; EM material response",
            "status": "ZERO_IN_STANDARD_BRANCH_RETAINED_OUTSIDE",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4330_3_mass_clock",
            "symbol": "D_A ln m_A + D_A ln hbar + D_A ln c",
            "meaning": "visible mass/clock/unit coefficients are parent-active rather than calibrated q-basic data",
            "bound_contribution": "sum absolute log-derivatives",
            "observable_links": "clock comparisons; spectra; orbital units; source mass readout",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4330_4_operator_coefficients",
            "symbol": "sum_i |D_v c_i|",
            "meaning": "non-EH/EFT operator coefficients drift or enter local weak-field equations",
            "bound_contribution": "sum_i |D_v c_i| ||O_i||",
            "observable_links": "PPN gamma/beta/alpha_i/xi; R10; clocks; orbital residuals",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4330_0_kappa_lock",
            "name": "topological kappa lock",
            "formula": "S_top^kappa=C_top int A_3 wedge d ln(kappa_*/kappa_0), delta_A3 S=0 => d ln kappa_*=0 => D_A ln kappa_*=0",
            "status": "CONDITIONAL_ZERO_DERIVED",
        },
        {
            "formula_id": "F4330_1_source_measure",
            "name": "Hilbert source-measure closure",
            "formula": "Z_H=Z_0 exp(delta_ZH), Hilbert source-measure descent => delta_ZH=0 and D_A delta_ZH=0",
            "status": "CONDITIONAL_ZERO_DERIVED",
        },
        {
            "formula_id": "F4330_2_Gcal",
            "name": "calibrated Newton coupling drift",
            "formula": "G_cal=c^4 kappa_* Z_H/(8*pi), so D_A ln G_cal=D_A ln kappa_*+D_A delta_ZH=0",
            "status": "STRUCTURAL_COUPLING_ZERO_NUMERIC_VALUE_CALIBRATED",
        },
        {
            "formula_id": "F4330_3_EM_coeff",
            "name": "calibrated EM coefficient silence",
            "formula": "b_alpha=D_X ln alpha_eff=2D_X ln g_J-D_X ln lambda_A=0 in q-basic visible EM readout branch",
            "status": "CONDITIONAL_ZERO_DERIVED",
        },
        {
            "formula_id": "F4330_4_Dq_coeff",
            "name": "coefficient drift zero",
            "formula": "fixed parent-action/calibrated constants and no C_i(Phi) hidden coefficient slot => Dq_coeff=Dq_coeff_C1=epsilon_coeff=0",
            "status": "CONDITIONAL_ZERO_IMPORTED",
        },
        {
            "formula_id": "F4330_5_bound_fallback",
            "name": "dynamic coefficient fallback",
            "formula": "epsilon_coeff <= |D_A ln kappa_*| + |D_A delta_ZH| + |b_alpha| + sum_A |D_A ln unit/mass constants| + sum_i |D_v c_i| ||O_i||",
            "status": "BOUND_RETAINED_OUTSIDE_BRANCH",
        },
        {
            "formula_id": "F4330_6_geometry_core_update",
            "name": "geometry core after coefficient reduction",
            "formula": "epsilon_geom_core <= C_readout epsilon_readout_frame + C_terminal epsilon_terminal + C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + tail_guard_sum",
            "status": "REDUCED_BUT_OPEN",
        },
        {
            "formula_id": "F4330_7_source_readout_update",
            "name": "source-readout after coefficient reduction",
            "formula": "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_coeff + Xi_src_hidden",
            "status": "NONCLAIM_HANDOFF",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4330_0_fixed_calibrated_branch",
            "branch_input": "fixed parent-action/calibrated constants: kappa lock + Hilbert ZH closure + q-basic EM coefficients",
            "action": "ALLOW_EPSILON_COEFF_ZERO",
            "output": "Dq_coeff=Dq_coeff_C1=epsilon_coeff=0",
            "claim_policy": "private nonclaim; numeric constants not predicted",
        },
        {
            "runner_id": "RUN4330_1_dynamic_coefficients",
            "branch_input": "any coefficient is C_i(Phi), source-label dependent, or readout-regenerated",
            "action": "KEEP_COEFFICIENT_BOUND",
            "output": "epsilon_coeff_open no-cancellation envelope",
            "claim_policy": "source-backed values required before local tests",
        },
        {
            "runner_id": "RUN4330_2_numeric_G_alpha",
            "branch_input": "derive numeric G_N or alpha_EM from drift zero",
            "action": "REJECT",
            "output": "calibrated constants are stable but not numerically predicted",
            "claim_policy": "firewall",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4330_0_numeric_G",
            "forbidden_shortcut": "Dq_coeff=0 predicts numerical G_N",
            "reason": "a stable calibrated coupling is not a parent dimensionful scale prediction",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4330_1_numeric_alpha",
            "forbidden_shortcut": "b_alpha=0 predicts alpha_EM or charge normalization",
            "reason": "q-basic EM constants are locally fixed readout data, not derived values",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4330_2_source_measure_hide",
            "forbidden_shortcut": "absorb source-measure leaks into measured G",
            "reason": "only common Z_0 is a calibration gauge; delta_ZH leaks are physical",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4330_3_dynamic_branch",
            "forbidden_shortcut": "use epsilon_coeff=0 when coefficients are hidden-field functions",
            "reason": "dynamic C_i(Phi) branches require finite source-backed derivative rows",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4330_4_local_GR_claim",
            "forbidden_shortcut": "claim local GR/R10/PPN/clock pass from coefficient closure alone",
            "reason": "readout-frame, terminal projection, open EM and Xi_src_hidden gates remain",
            "status": "BLOCK",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "The coefficient drift tail is removed from the reduced geometry core only for the fixed parent-action/calibrated-constant branch. Dynamic hidden coefficient branches remain bounded, and no numerical G_N/alpha_EM prediction is claimed.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4330_0_coeff",
            "item": "epsilon_coeff",
            "status": "CONDITIONAL_ZERO_IN_FIXED_CALIBRATED_BRANCH",
            "notes": "removed from geometry core only when coefficients are fixed/q-basic and not hidden functions",
        },
        {
            "status_id": "STAT4330_1_G",
            "item": "G_cal",
            "status": "STABLE_CALIBRATED_COUPLING_NOT_NUMERIC_PREDICTION",
            "notes": "structural coupling and drift silence pass; absolute number remains empirical like GR",
        },
        {
            "status_id": "STAT4330_2_alpha",
            "item": "alpha_EM/g_J/lambda_A",
            "status": "QBASIC_READOUT_STABLE_NOT_DERIVED",
            "notes": "no alpha_EM prediction is claimed",
        },
        {
            "status_id": "STAT4330_3_geometry_core",
            "item": "epsilon_geom_core",
            "status": "REDUCED_BUT_OPEN",
            "notes": "readout-frame, terminal, open-EM and Xi tails remain",
        },
        {
            "status_id": "STAT4330_4_next",
            "item": "readout-frame/terminal",
            "status": "NEXT_TARGET",
            "notes": "remaining geometry tails are now projection/readout ownership rather than matter/EM/coefficient drift",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4330_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the readout-frame and terminal projection tails be zeroed by quotient/natural readout ownership, or must they become explicit projection-bound rows?",
            "preferred_route": "prove readout is pure postprocessing with no action-domain or effective-frame reentry, and terminal metric/coframe is not used as a shortcut for no-shadow",
            "fallback_route": "write explicit finite projection tails for epsilon_readout_frame, epsilon_terminal, local projection constants and Xi_src_hidden transfer",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 346 - PPC4161 coefficient drift zero or source-backed tail bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4330 does **not** predict the numerical values of `G_N`, `alpha_EM`, charge normalization, particle masses, `hbar`, or `c`. It does not claim public local GR, R10, PPN, WEP, clock, or orbital safety.

It closes a narrower but important leak: in the fixed parent-action/calibrated-constant branch, coefficient drift does not feed hidden local representative motion.

## Derived Branch Law

```text
S_top^kappa = C_top int A_3 wedge d ln(kappa_*/kappa_0)
=> D_A ln kappa_* = 0

Hilbert source-measure descent:
Z_H = Z_0 exp(delta_ZH), delta_ZH=0
=> D_A delta_ZH = 0

G_cal = c^4 kappa_* Z_H/(8*pi)
=> D_A ln G_cal = 0

q-basic visible EM readout:
D_X ln g_J = D_X ln lambda_A = 0
=> b_alpha = 0

fixed parent-action/calibrated constants and no hidden C_i(Phi) slot
=> Dq_coeff = Dq_coeff_C1 = epsilon_coeff = 0
```

The zero is branch-local. If any coefficient becomes a hidden-field/source/readout function, the finite no-cancellation tail rows remain live.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Owner Audit

{md_table(tables["audit"], ["audit_id", "coefficient_slot", "owner_clause", "drift_statement", "status", "not_claimed"])}

## Zero Rows

{md_table(tables["zeros"], ["zero_id", "symbol", "zero_statement", "branch_conditions", "status", "valid_for_claim"])}

## Retained Coefficient Tails

{md_table(tables["tails"], ["tail_id", "symbol", "meaning", "bound_contribution", "observable_links", "status"])}

## Formula Updates

{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4330 Y5-R2FR coefficient drift zero or source-backed tail bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

`epsilon_coeff` is now branch-resolved. In the fixed parent-action/calibrated-constant local branch, the coefficient drift vector is zero. In any dynamic coefficient branch, it remains an explicit finite tail.

## Reduced Geometry Core

{md_table(tables["formulas"], ["formula_id", "formula", "status"])}

## Remaining Tails

{md_table(tables["tails"], ["tail_id", "symbol", "observable_links", "status"])}

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4330_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4330_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4330_kappa_zero", "kappa drift zero row exists", any(r["symbol"] == "D_A ln kappa_*" for r in tables["zeros"]), "zeros")
    add("VAL4330_ZH_zero", "delta_ZH zero row exists", any(r["symbol"] == "D_A delta_ZH" for r in tables["zeros"]), "zeros")
    add("VAL4330_Gcal_zero", "G_cal drift zero without numeric prediction", any(r["symbol"] == "D_A ln G_cal" and "NOT_PREDICTED" in r["status"] for r in tables["zeros"]), "zeros")
    add("VAL4330_EM_zero", "EM coefficient drift zero row exists", any(r["symbol"] == "b_alpha" for r in tables["zeros"]), "zeros")
    add("VAL4330_Dq_coeff_zero", "Dq_coeff zero row exists", any(r["symbol"] == "Dq_coeff" for r in tables["zeros"]), "zeros")
    add("VAL4330_epsilon_coeff_zero", "epsilon_coeff zero imported into core", any(r["symbol"] == "epsilon_coeff" and "4329" in r["status"] for r in tables["zeros"]), "zeros")
    add("VAL4330_bound_fallback", "dynamic coefficient fallback formula retained", any("epsilon_coeff <=" in r["formula"] and "D_A delta_ZH" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4330_geometry_formula_reduced", "geometry formula no longer carries epsilon_coeff as live standard tail", any(r["formula_id"] == "F4330_6_geometry_core_update" and "epsilon_coeff_open" in r["formula"] and "epsilon_readout_frame" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4330_numeric_G_firewall", "numeric G prediction blocked", any("numerical G_N" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4330_numeric_alpha_firewall", "numeric alpha prediction blocked", any("alpha_EM" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4330_source_measure_firewall", "source-measure hiding blocked", any("source-measure" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4330_runner_modes", "runner has zero, bound and reject modes", {"ALLOW_EPSILON_COEFF_ZERO", "KEEP_COEFFICIENT_BOUND", "REJECT"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4330_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4330_next_readout", "next target is readout/terminal", any("readout-frame" in r["next_target"] and "terminal" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4330_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4330_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4330_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4330_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4330_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4330_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4330_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4330_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4330_COEFFICIENT_OWNER_AUDIT.csv",
        "zeros": SOURCE_DIR / "P8_Y5_R2FR_4330_COEFFICIENT_ZERO_ROWS.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4330_COEFFICIENT_TAIL_BOUND.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4330_GEOMETRY_UPDATE_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4330_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4330_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4330_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4330_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4330_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "zeros": zero_rows(),
        "tails": tail_rows(),
        "formulas": formula_rows(),
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
## PPC4161 4330 coefficient drift zero or source-backed tail bound

Marker: `{MARKER}`

4330 imports the fixed-parent/calibrated-constant route into the 4329-reduced geometry core. In the private PPC4161-TK-H calibrated branch, `D_A ln kappa_*=0`, `D_A delta_ZH=0`, `D_A ln G_cal=0`, `b_alpha=0`, and `Dq_coeff=Dq_coeff_C1=epsilon_coeff=0`. This closes the drift problem for stable local coefficients without pretending to predict the numerical values of `G_N`, `alpha_EM`, charge normalization, particle masses, or unit constants. Dynamic hidden coefficient branches remain explicit bound rows. The remaining geometry bottleneck is readout-frame/terminal projection plus `Xi_src_hidden`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4330 packet coefficient drift zero

Marker: `{PACKET_MARKER}`

Packet update: after ordinary matter, EM/Hodge, and coefficient drift reductions, the local branch no longer has to carry a generic `epsilon_coeff` tail in the fixed calibrated-constant sector. The numerical constants are calibrated/stable rather than predicted. Nonstandard coefficient functions remain finite residual rows.
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
