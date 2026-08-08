from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from torsion_operator_invertibility_gate import evaluate_bound_row, evaluate_irrep_row, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4452"
CLAIM_ID = "L-294"
MARKER = "PPC4161_TORSION_OPERATOR_INVERTIBILITY_NO_ZERO_MODE_4452"
PACKET_MARKER = "PPC4161_PACKET_TORSION_OPERATOR_INVERTIBILITY_NO_ZERO_MODE_4452"
DECISION = "TORSION_OPERATOR_DIAGONALIZED_IN_LORENTZ_IRREPS_NO_ZERO_MODE_AND_CONTACT_BOUND_FORMULA_DERIVED_PARENT_POSITIVE_MARGIN_AND_NUMERIC_SPIN_BOUNDS_OPEN_NONCLAIM"
NEXT_TARGET = "4453-Y5-R2FR-parent-positive-torsion-margin-or-spin-contact-bound-source-row.md"

FORMAL_PATH = FORMAL / "468-PPC4161-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md"
DOC_PATH = POST / "4452-Y5-R2FR-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4452_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4452_SOURCE_REGISTER.csv"
IRREP_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4452_TORSION_IRREP_OPERATOR_INPUT.csv"
IRREP_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4452_TORSION_IRREP_OPERATOR_OUTPUT.csv"
BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4452_SPIN_CONTACT_BOUND_INPUT.csv"
BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4452_SPIN_CONTACT_BOUND_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4452_DERIVATION_ROWS.csv"
FORMULA_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4452_OPERATOR_FORMULA_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4452_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4452_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4452_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4452_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "torsion_operator_invertibility_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4452_torsion_operator_invertibility_no_zero_mode_or_spin_contact_bound.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4451 = SOURCE_DIR / "P8_Y5_R2FR_4451_NEXT_TARGET.csv"
THEOREM_4451 = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_THEOREM_OUTPUT.csv"
FORMAL_467 = FORMAL / "467-PPC4161-torsion-spin-residual-cT-zero-or-contact-bound.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
OUT_4184_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION.csv"
OUT_4184_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"
COEFF_4450 = SOURCE_DIR / "P8_Y5_R2FR_4450_COEFFICIENT_STATUS_OUTPUT.csv"


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4452_00_next4451", "path": NEXT_4451, "needle": "4452-Y5-R2FR-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md", "role": "4451 selected the operator target."},
        {"source_id": "SRC4452_01_theorem4451", "path": THEOREM_4451, "needle": "tau_spin=0 and ker L_T=0 => T=0", "role": "4451 spinless-zero theorem."},
        {"source_id": "SRC4452_02_formal467", "path": FORMAL_467, "needle": "L_T[e,c_T] T = kappa tau_spin", "role": "formal 4451 torsion equation."},
        {"source_id": "SRC4452_03_formal200", "path": FORMAL_200, "needle": "torsion squares -> coefficient `c_T`", "role": "torsion square residual term."},
        {"source_id": "SRC4452_04_formal295", "path": FORMAL_295, "needle": "c_T_spin", "role": "spin/torsion contact channel."},
        {"source_id": "SRC4452_05_4184_normal", "path": OUT_4184_NORMAL, "needle": "T^A wedge star T_A", "role": "torsion-square normal-form row."},
        {"source_id": "SRC4452_06_4184_ledger", "path": OUT_4184_LEDGER, "needle": "derive c_T=0/heavy from parent or fit upper bound", "role": "torsion residual evidence requirement."},
        {"source_id": "SRC4452_07_coeff4450", "path": COEFF_4450, "needle": "TORSION_MASS_OR_CONTACT_SCALE_MISSING", "role": "4450 missing torsion scale row."},
        {"source_id": "SRC4452_08_gate", "path": GATE_PATH, "needle": "def evaluate_irrep_row", "role": "4452 operator gate."},
        {"source_id": "SRC4452_09_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4452"', "role": "4452 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": spec["source_id"],
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line > 0,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def irrep_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "irrep_id": "IR4452_0_trace_vector",
            "irrep": "trace_vector",
            "torsion_component": "V_a = T^b{}_{ba}",
            "source_path": str(OUT_4184_NORMAL),
            "operator_eigenvalue": "lambda_V = lambda_V^EC + a_V(c_T)",
            "critical_surface": "lambda_V = 0",
            "diagonal_by_lorentz_parity": True,
            "eigenvalue_symbolic_written": True,
            "nonzero_contract_written": True,
            "positive_parent_signed": False,
            "numeric_margin_available": False,
            "public_claim_false": True,
        },
        {
            "irrep_id": "IR4452_1_axial_vector",
            "irrep": "axial_vector",
            "torsion_component": "A^a = epsilon^{abcd} T_bcd",
            "source_path": str(OUT_4184_NORMAL),
            "operator_eigenvalue": "lambda_A = lambda_A^EC + a_A(c_T)",
            "critical_surface": "lambda_A = 0",
            "diagonal_by_lorentz_parity": True,
            "eigenvalue_symbolic_written": True,
            "nonzero_contract_written": True,
            "positive_parent_signed": False,
            "numeric_margin_available": False,
            "public_claim_false": True,
        },
        {
            "irrep_id": "IR4452_2_tensor",
            "irrep": "tensor",
            "torsion_component": "Q_abc with Q^b{}_{ba}=0 and epsilon^{abcd} Q_bcd=0",
            "source_path": str(OUT_4184_NORMAL),
            "operator_eigenvalue": "lambda_Q = lambda_Q^EC + a_Q(c_T)",
            "critical_surface": "lambda_Q = 0",
            "diagonal_by_lorentz_parity": True,
            "eigenvalue_symbolic_written": True,
            "nonzero_contract_written": True,
            "positive_parent_signed": False,
            "numeric_margin_available": False,
            "public_claim_false": True,
        },
    ]


def bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "B4452_0_operator_norm",
            "arena": "operator_norm",
            "source_path": str(FORMAL_467),
            "bound_formula": "lambda_T,min = min(|lambda_V|,|lambda_A|,|lambda_Q|) > 0 => ||T|| <= kappa ||tau_spin||/lambda_T,min",
            "formula_written": True,
            "lambda_margin_symbolic": True,
            "spin_source_numeric": False,
            "experiment_bound_sourced": False,
            "public_claim_false": True,
        },
        {
            "bound_id": "B4452_1_contact_action",
            "arena": "spin_contact_action",
            "source_path": str(FORMAL_295),
            "bound_formula": "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)",
            "formula_written": True,
            "lambda_margin_symbolic": True,
            "spin_source_numeric": False,
            "experiment_bound_sourced": False,
            "public_claim_false": True,
        },
        {
            "bound_id": "B4452_2_spinless_local_tests",
            "arena": "spinless_PPN_R10_orbital",
            "source_path": str(THEOREM_4451),
            "bound_formula": "tau_spin=0 and lambda_T,min>0 => Delta_PPN_torsion = Delta_R10_torsion = 0",
            "formula_written": True,
            "lambda_margin_symbolic": True,
            "spin_source_numeric": False,
            "experiment_bound_sourced": False,
            "public_claim_false": True,
        },
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4452_0_irrep_decomposition",
            "claim": "The algebraic torsion operator splits into Lorentz irreducible channels.",
            "derivation": "In the parity-even no-DT branch, the trace vector V_a, axial vector A_a, and traceless tensor Q_abc are inequivalent Lorentz irreps. A local Lorentz scalar quadratic form cannot mix inequivalent irreps unless parity-odd or explicit mixing terms are added. Therefore L_T is block diagonal in V, A, and Q.",
            "consequence": "No-zero-mode is not vague: it is the three-channel condition lambda_V lambda_A lambda_Q != 0.",
            "status": "TORSION_OPERATOR_DIAGONALIZED_SYMBOLICALLY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4452_1_no_zero_mode_criterion",
            "claim": "The exact symbolic invertibility condition is lambda_T,min > 0.",
            "derivation": "Define lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|). If lambda_T,min > 0 then L_T has a bounded inverse and ||L_T^-1|| <= 1/lambda_T,min. If any lambda_i=0, the corresponding torsion irrep is a local zero mode and the branch reopens.",
            "consequence": "The previous open clause `ker L_T=0` is now an explicit eigenvalue/margin contract.",
            "status": "NO_ZERO_MODE_CONTRACT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4452_2_spin_contact_bound",
            "claim": "Finite spin torsion is bounded by the same margin.",
            "derivation": "Solving L_T T = kappa tau_spin gives T = kappa L_T^-1 tau_spin. Thus ||T|| <= kappa ||tau_spin||/lambda_T,min and integrating out torsion gives |Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min).",
            "consequence": "If parent positivity is not signed, 4453 must either source lambda_T,min and spin bounds or keep c_T_spin nonclaim.",
            "status": "SPIN_CONTACT_BOUND_FORMULA_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4452_3_spinless_closure",
            "claim": "Spinless local tests are conditionally clean.",
            "derivation": "For PPN/orbital/unpolarized R10 matter, tau_spin=0. With lambda_T,min>0, the solution is T=0 in all three irreps, so there is no long-range torsion contribution in those arenas.",
            "consequence": "The only remaining torsion risk is parent sign/margin or explicitly spin-polarized/contact experiments.",
            "status": "SPINLESS_BRANCH_CONDITIONALLY_CLEAN",
            "valid_for_claim": False,
        },
    ]


def formula_rows() -> List[Dict[str, object]]:
    return [
        {"formula_id": "F4452_0_decomposition", "formula": "T_abc = (trace V_a) + (axial A_a) + Q_abc", "meaning": "Lorentz irrep torsion split", "valid_for_claim": False},
        {"formula_id": "F4452_1_operator", "formula": "L_T = diag(lambda_V, lambda_A, lambda_Q)", "meaning": "parity-even no-DT algebraic torsion operator", "valid_for_claim": False},
        {"formula_id": "F4452_2_margin", "formula": "lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|)", "meaning": "operator no-zero-mode margin", "valid_for_claim": False},
        {"formula_id": "F4452_3_inverse", "formula": "||T|| <= kappa ||tau_spin||/lambda_T,min", "meaning": "torsion response bound", "valid_for_claim": False},
        {"formula_id": "F4452_4_contact", "formula": "|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)", "meaning": "spin-contact fallback bound", "valid_for_claim": False},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "irrep_diagonalization_written": True,
        "no_zero_mode_contract_written": True,
        "spin_contact_formula_written": True,
        "lambda_margin_numeric": False,
        "parent_positive_margin_signed": False,
        "public_claim": False,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "torsion_operator_irreps": "trace_vector;axial_vector;tensor",
        "lambda_T_min_contract": "min_abs(lambda_V,lambda_A,lambda_Q)>0",
        "spinless_torsion_long_range_clean_conditional": True,
        "spin_contact_bound_formula_ready": True,
        "numeric_spin_bound_ready": False,
        "local_GR_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4452_0",
        "target": NEXT_TARGET,
        "objective": "Either parent-sign a positive torsion margin lambda_T,min>0, or fill spin-contact bound source rows.",
        "derive_first": "prove parent IR selector supplies positive lambda_V, lambda_A, lambda_Q away from critical surfaces",
        "fallback": "source spin-clock/polarized-matter/contact bounds for kappa^2 tau_spin^2/(2 lambda_T,min)",
        "risk": "leaving lambda_T,min symbolic while treating torsion as closed",
        "valid_for_claim": False,
    }]


def claim_gate_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    irreps = rows_from(IRREP_OUTPUT)
    bounds = rows_from(BOUND_OUTPUT)
    return [
        {"gate_id": "CG4452_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in sources), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4452_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in sources), "valid_for_claim": False, "detail": "Operator target is source-backed."},
        {"gate_id": "CG4452_2_irrep_contract_ready", "claim": "all torsion irreps have symbolic nonzero contracts", "passed": all(row["current_status"] == "IRREP_SYMBOLIC_INVERTIBILITY_CONTRACT_READY_PARENT_MARGIN_MISSING" for row in irreps), "valid_for_claim": False, "detail": "V/A/Q channels diagonalized."},
        {"gate_id": "CG4452_3_bound_formula_ready", "claim": "spin-contact bound formulas are written", "passed": all(row["current_status"] == "SPIN_CONTACT_FORMULA_READY_NUMERIC_INPUTS_MISSING" for row in bounds), "valid_for_claim": False, "detail": "Numeric spin/source bounds remain missing."},
        {"gate_id": "CG4452_4_no_public_claim", "claim": "no public local-GR torsion claim emitted", "passed": all(row["claim_allowed"] == "False" for row in irreps) and all(row["claim_allowed"] == "False" for row in bounds), "valid_for_claim": False, "detail": "Parent margin/signature remains open."},
        {"gate_id": "CG4452_5_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc() -> str:
    return f"""# 468 PPC4161 torsion operator invertibility no zero mode or spin contact bound

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4452 closes the vague part of 4451. The condition `ker L_T=0` is now an explicit irreducible-channel contract:

```text
T_abc = V_a + A_a + Q_abc
L_T = diag(lambda_V, lambda_A, lambda_Q)
lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|)
```

The no-zero-mode condition is:

```text
lambda_T,min > 0.
```

Then:

```text
||T|| <= kappa ||tau_spin||/lambda_T,min
|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min).
```

So spinless local tests are conditionally clean, but the branch is not public until MTS parent-signs the positive torsion margin or supplies sourced spin-contact bounds.

## Source Register

{table(rows_from(SOURCE_REGISTER))}

## Torsion Irrep Operator Gate

{table(rows_from(IRREP_OUTPUT))}

## Spin Contact Bound Gate

{table(rows_from(BOUND_OUTPUT))}

## Formula Rows

{table(rows_from(FORMULA_ROWS))}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Claim Gates

{table(rows_from(CLAIM_GATES))}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4452 Y5 R2FR torsion operator invertibility no zero mode or spin contact bound

Private checkpoint generated at `{STAMP}`.

Summary:
- Replaced `ker L_T=0` with the exact symbolic condition `lambda_T,min = min(|lambda_V|, |lambda_A|, |lambda_Q|) > 0`.
- Derived the response bound `||T|| <= kappa ||tau_spin||/lambda_T,min`.
- Derived the contact fallback `|Delta L_contact| <= kappa^2 ||tau_spin||^2/(2 lambda_T,min)`.
- No public local-GR claim: parent positive margin and/or source-backed spin-contact bounds are still needed.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    row = {field: "" for field in fieldnames}
    payload = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "4452 diagonalizes the algebraic torsion operator into trace, axial, and tensor irreps, derives the exact no-zero-mode condition lambda_T,min>0, and writes the spin-contact fallback bound formula.",
        "current_evidence": "4452 source register, torsion irrep operator gate, spin-contact bound gate, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "status": "torsion_operator_no_zero_mode_contract_and_contact_bound_formula_ready_parent_margin_numeric_bounds_open_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Leaving lambda_T,min symbolic while treating torsion as fully closed.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4452 source register, torsion irrep operator gate, spin-contact bound gate, formula rows, derivation rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Leaving lambda_T,min symbolic while treating torsion as fully closed.",
    }
    for key, value in payload.items():
        if key in row:
            row[key] = value
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Parent-Derivation Update - Torsion Operator No-Zero-Mode Contract

Marker: `{MARKER}`  
Source checkpoint: `4452-Y5-R2FR-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md`  
Claim register row: `{CLAIM_ID}`

The torsion condition is now exact: decompose `T` into trace, axial, and tensor irreps, define `lambda_T,min=min(|lambda_V|,|lambda_A|,|lambda_Q|)`, and require `lambda_T,min>0`. This gives the response/contact bounds but still needs parent positive-margin signature or sourced spin-contact bounds.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Torsion Operator Contract

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4452-Y5-R2FR-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md`

Inside the private packet, `ker L_T=0` is no longer a black box. The packet now carries explicit `lambda_V`, `lambda_A`, `lambda_Q`, and `lambda_T,min` slots.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    irreps = rows_from(IRREP_OUTPUT)
    bounds = rows_from(BOUND_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    checks = [
        ("VAL4452_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4452_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4452_2_irrep_contracts", all(row["current_status"] == "IRREP_SYMBOLIC_INVERTIBILITY_CONTRACT_READY_PARENT_MARGIN_MISSING" for row in irreps), "all irreps have symbolic contracts"),
        ("VAL4452_3_bound_formulas", all(row["current_status"] == "SPIN_CONTACT_FORMULA_READY_NUMERIC_INPUTS_MISSING" for row in bounds), "all spin-contact formulas written"),
        ("VAL4452_4_formula_rows", FORMULA_ROWS.exists() and "lambda_T,min" in text(FORMULA_ROWS), "lambda_T,min formula row written"),
        ("VAL4452_5_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4452_6_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-294"),
        ("VAL4452_7_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4452_8_post_doc", DOC_PATH.exists() and "Private checkpoint" in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4452_9_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4452_10_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4452_11_next_target", NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4452_12_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(IRREP_INPUT, irrep_input_rows())
    write_csv(IRREP_OUTPUT, [evaluate_irrep_row(row) for row in rows_from(IRREP_INPUT)])
    write_csv(BOUND_INPUT, bound_input_rows())
    write_csv(BOUND_OUTPUT, [evaluate_bound_row(row) for row in rows_from(BOUND_INPUT)])
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(FORMULA_ROWS, formula_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_csv(CLAIM_GATES, claim_gate_rows())
    write_text(FORMAL_PATH, build_doc())
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows())


if __name__ == "__main__":
    main()
