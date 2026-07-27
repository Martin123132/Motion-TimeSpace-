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

from torsion_spin_residual_gate import evaluate_condition_row, evaluate_theorem_row, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4451"
CLAIM_ID = "L-293"
MARKER = "PPC4161_TORSION_SPIN_RESIDUAL_ZERO_OR_CONTACT_BOUND_4451"
PACKET_MARKER = "PPC4161_PACKET_TORSION_SPIN_RESIDUAL_ZERO_OR_CONTACT_BOUND_4451"
DECISION = "TORSION_SPIN_RESIDUAL_DEMOTED_FROM_LONG_RANGE_LOCAL_PPN_OBSTRUCTION_TO_CONDITIONAL_SPIN_CONTACT_CHANNEL_OPERATOR_INVERTIBILITY_AND_SPIN_BOUNDS_OPEN_NONCLAIM"
NEXT_TARGET = "4452-Y5-R2FR-torsion-operator-invertibility-no-zero-mode-or-spin-contact-bound.md"

FORMAL_PATH = FORMAL / "467-PPC4161-torsion-spin-residual-cT-zero-or-contact-bound.md"
DOC_PATH = POST / "4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4451_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4451_SOURCE_REGISTER.csv"
CONDITION_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_BRANCH_CONDITIONS_INPUT.csv"
CONDITION_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_BRANCH_CONDITIONS_OUTPUT.csv"
THEOREM_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_THEOREM_INPUT.csv"
THEOREM_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4451_TORSION_THEOREM_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4451_DERIVATION_ROWS.csv"
OUTCOME_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4451_OUTCOME_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4451_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4451_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4451_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4451_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "torsion_spin_residual_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4451_torsion_spin_residual_cT_zero_or_contact_bound.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4450 = SOURCE_DIR / "P8_Y5_R2FR_4450_NEXT_TARGET.csv"
COEFF_4450 = SOURCE_DIR / "P8_Y5_R2FR_4450_COEFFICIENT_STATUS_OUTPUT.csv"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
FORMAL_197 = FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md"
FORMAL_295 = FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md"
POST_4070 = POST / "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md"
OUT_4184_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4184_NORMAL_FORM_CLASSIFICATION.csv"
OUT_4184_LEDGER = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"


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
        {"source_id": "SRC4451_00_next4450", "path": NEXT_4450, "needle": "4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md", "role": "4450 selected the torsion-spin target."},
        {"source_id": "SRC4451_01_coeff4450", "path": COEFF_4450, "needle": "C4450_6_cT_spin", "role": "4450 coefficient row."},
        {"source_id": "SRC4451_02_formal200", "path": FORMAL_200, "needle": "If torsion/nonmetricity are algebraic", "role": "Palatini selector condition."},
        {"source_id": "SRC4451_03_formal197", "path": FORMAL_197, "needle": "torsion/nonmetricity and extra scalar/disformal modes are zero or bounded", "role": "EH origin gate."},
        {"source_id": "SRC4451_04_formal295", "path": FORMAL_295, "needle": "c_T_spin", "role": "survivor spin/torsion contact row."},
        {"source_id": "SRC4451_05_post4070", "path": POST_4070, "needle": "torsion-free or spinless branch", "role": "earlier torsion gate."},
        {"source_id": "SRC4451_06_4184_normal", "path": OUT_4184_NORMAL, "needle": "NFC4184_3_torsion_squares", "role": "torsion-square normal-form residual."},
        {"source_id": "SRC4451_07_4184_ledger", "path": OUT_4184_LEDGER, "needle": "RB4184_0_cT", "role": "torsion coefficient ledger."},
        {"source_id": "SRC4451_08_gate", "path": GATE_PATH, "needle": "def evaluate_theorem_row", "role": "4451 torsion gate."},
        {"source_id": "SRC4451_09_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4451"', "role": "4451 generator script."},
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


def condition_input_rows() -> List[Dict[str, object]]:
    return [
        {"condition_id": "TC4451_0_AMF", "condition": "A_MF gives private Cartan variables e and omega", "source_path": str(COEFF_4450), "private_ready": True, "parent_signed": False, "public_claim_false": True},
        {"condition_id": "TC4451_1_EC_principal", "condition": "Einstein-Cartan/Palatini principal block is selected only under the IR selector", "source_path": str(OUT_4184_NORMAL), "private_ready": True, "parent_signed": False, "public_claim_false": True},
        {"condition_id": "TC4451_2_no_torsion_kinetic", "condition": "torsion is auxiliary/algebraic: no independent D T kinetic term in the compact local IR branch", "source_path": str(FORMAL_200), "private_ready": True, "parent_signed": False, "public_claim_false": True},
        {"condition_id": "TC4451_3_spinless_source", "condition": "macroscopic local PPN/R10 bodies are treated as spinless or unpolarized in the bulk source channel", "source_path": str(POST_4070), "private_ready": True, "parent_signed": False, "public_claim_false": True},
        {"condition_id": "TC4451_4_operator_invertible", "condition": "torsion algebraic operator has no local zero mode or critical c_T tuning", "source_path": str(OUT_4184_LEDGER), "private_ready": False, "parent_signed": False, "public_claim_false": True},
        {"condition_id": "TC4451_5_contact_bound", "condition": "spin-polarized/contact channel has source-backed bound rows if not zero", "source_path": str(FORMAL_295), "private_ready": False, "parent_signed": False, "public_claim_false": True},
    ]


def theorem_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "TH4451_0_connection_variation",
            "claim_piece": "In the no-DT local IR branch, connection variation gives an algebraic torsion equation.",
            "source_path": str(FORMAL_200),
            "equation_form": "L_T[e,c_T] T = kappa tau_spin with no derivatives of T",
            "algebraic_no_derivatives": True,
            "spinless_zero": False,
            "long_range_zero": False,
            "contact_remaining": False,
            "open_parent_clause": True,
            "public_claim_false": True,
        },
        {
            "theorem_id": "TH4451_1_spinless_zero",
            "claim_piece": "If tau_spin=0 and ker L_T=0, then T=0 in the compact spinless local branch.",
            "source_path": str(FORMAL_197),
            "equation_form": "tau_spin=0 and ker L_T=0 => T=0",
            "algebraic_no_derivatives": True,
            "spinless_zero": True,
            "long_range_zero": True,
            "contact_remaining": False,
            "open_parent_clause": True,
            "public_claim_false": True,
        },
        {
            "theorem_id": "TH4451_2_contact_demote",
            "claim_piece": "After eliminating algebraic torsion, nonzero microscopic spin gives a local contact spin-spin term, not a long-range spinless PPN/R10 force.",
            "source_path": str(FORMAL_295),
            "equation_form": "S_eff = S_EH + O(tau_spin L_T^-1 tau_spin)",
            "algebraic_no_derivatives": True,
            "spinless_zero": True,
            "long_range_zero": True,
            "contact_remaining": True,
            "open_parent_clause": True,
            "public_claim_false": True,
        },
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4451_0_local_action",
            "claim": "The safe torsion branch is an auxiliary Cartan branch, not a propagating torsion theory.",
            "derivation": "Use the local private IR action S = S_EC[e,omega] + c_T int T^A wedge *T_A + S_m[e,psi] and explicitly exclude D T kinetic terms in this branch. Then varying omega cannot produce a wave equation for torsion; it produces an algebraic constraint.",
            "consequence": "A finite c_T is not automatically a new long-range force.",
            "status": "AUXILIARY_TORSION_BRANCH_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4451_1_connection_equation",
            "claim": "The torsion equation has the schematic form L_T T = kappa tau_spin.",
            "derivation": "The EC term contributes the usual e wedge T algebraic piece and c_T T wedge *T contributes a linear algebraic mass/contact operator. With no D T term, all terms are pointwise in T. Define L_T[e,c_T] as that algebraic operator.",
            "consequence": "If L_T has no kernel, spinless matter gives T=0 exactly.",
            "status": "ALGEBRAIC_TORSION_EQUATION_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4451_2_spinless_reduction",
            "claim": "For spinless/unpolarized macroscopic local tests, c_T_spin is demoted from long-range PPN obstruction to contact-channel issue.",
            "derivation": "Set tau_spin=0 for the bulk PPN/R10/orbital source. If ker L_T=0, then T=0. Substituting T back leaves no torsion-mediated long-range spinless potential; microscopic polarized spin produces only a local contact term tau_spin L_T^-1 tau_spin.",
            "consequence": "PPN spinless branch can proceed conditionally; spin-contact bound rows remain required.",
            "status": "SPINLESS_ZERO_CONTACT_CHANNEL_REMAINS",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4451_3_open_clause",
            "claim": "The theorem still needs an operator/no-zero-mode or source-backed contact bound.",
            "derivation": "MTS must parent-sign no propagating torsion kinetic term and no critical kernel of L_T, or else supply spin-clock/R10/contact bounds. Without that, local GR is improved but not publicly claimed.",
            "consequence": NEXT_TARGET,
            "status": "OPERATOR_INVERTIBILITY_OR_CONTACT_BOUND_NEXT",
            "valid_for_claim": False,
        },
    ]


def outcome_rows() -> List[Dict[str, object]]:
    return [
        {"outcome_id": "OUT4451_0_spinless_PPN", "arena": "PPN/orbital spinless macroscopic sources", "result": "conditional_zero", "meaning": "no torsion long-range correction if no-DT and ker L_T=0", "valid_for_claim": False},
        {"outcome_id": "OUT4451_1_R10_unpolarized", "arena": "R10 unpolarized ordinary matter", "result": "conditional_contact_suppression", "meaning": "torsion is not a Yukawa force unless a propagating torsion mode or finite contact source is introduced", "valid_for_claim": False},
        {"outcome_id": "OUT4451_2_spin_polarized", "arena": "spin clocks / polarized matter / microscopic contact", "result": "bound_required", "meaning": "remaining finite c_T_spin row lives here", "valid_for_claim": False},
        {"outcome_id": "OUT4451_3_failure_mode", "arena": "parent action with D T kinetic or ker L_T != 0", "result": "branch_reopens", "meaning": "then c_T is a real extra local mode and must be bounded, not hidden", "valid_for_claim": False},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "spinless_bulk_torsion_zero_conditional": True,
        "long_range_spinless_torsion_obstruction_removed_conditional": True,
        "contact_channel_remaining": True,
        "operator_invertibility_parent_signed": False,
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
        "torsion_equation_algebraic": True,
        "spinless_zero_conditional": True,
        "contact_bound_required": True,
        "operator_no_kernel_open": True,
        "local_GR_public_claim": False,
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4451_0",
        "target": NEXT_TARGET,
        "objective": "Close or bound the remaining torsion condition: no kinetic torsion and no algebraic zero mode, or spin-contact bound.",
        "derive_first": "prove parent IR selector makes L_T positive/invertible and excludes D T kinetic torsion in the compact local branch",
        "fallback": "source spin-clock/R10/contact limits for tau_spin L_T^-1 tau_spin",
        "risk": "claiming torsion is gone while leaving a critical algebraic kernel or spin-contact channel unsourced",
        "valid_for_claim": False,
    }]


def claim_gate_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    conditions = rows_from(CONDITION_OUTPUT)
    theorem = rows_from(THEOREM_OUTPUT)
    return [
        {"gate_id": "CG4451_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in sources), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4451_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in sources), "valid_for_claim": False, "detail": "Torsion target is source-backed."},
        {"gate_id": "CG4451_2_conditions_sourced", "claim": "all branch conditions have sources", "passed": all(row["source_exists"] == "True" for row in conditions), "valid_for_claim": False, "detail": "No unsourced torsion premise."},
        {"gate_id": "CG4451_3_algebraic_theorem_written", "claim": "algebraic torsion equation written", "passed": any(row["theorem_id"] == "TH4451_0_connection_variation" and row["algebraic_no_derivatives"] == "True" for row in theorem), "valid_for_claim": False, "detail": "L_T T = kappa tau_spin."},
        {"gate_id": "CG4451_4_spinless_zero_written", "claim": "spinless zero conditional written", "passed": any(row["theorem_id"] == "TH4451_1_spinless_zero" and row["spinless_zero"] == "True" and row["long_range_zero"] == "True" for row in theorem), "valid_for_claim": False, "detail": "tau_spin=0 and ker L_T=0 => T=0."},
        {"gate_id": "CG4451_5_contact_not_hidden", "claim": "spin contact channel remains explicit", "passed": any(row["theorem_id"] == "TH4451_2_contact_demote" and row["contact_remaining"] == "True" for row in theorem), "valid_for_claim": False, "detail": "Contact bound still required."},
        {"gate_id": "CG4451_6_no_public_claim", "claim": "no public local-GR claim emitted", "passed": all(row["claim_allowed"] == "False" for row in theorem) and all(row["claim_allowed"] == "False" for row in conditions), "valid_for_claim": False, "detail": "Operator/sign/source clauses remain open."},
        {"gate_id": "CG4451_7_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc() -> str:
    return f"""# 467 PPC4161 torsion spin residual cT zero or contact bound

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4451 takes the actual derivation shot at the torsion row selected by 4450.

The safe local branch is:

```text
S_loc = S_EC[e,omega] + c_T int T^A wedge *T_A + S_m[e,psi],
with no D T kinetic term in the compact local IR branch.
```

Varying the spin connection then gives the algebraic equation:

```text
L_T[e,c_T] T = kappa tau_spin.
```

Therefore, if `ker L_T = 0` and the macroscopic local source is spinless/unpolarized:

```text
tau_spin = 0  =>  T = 0.
```

This demotes `c_T_spin` from a generic long-range local PPN/R10 obstruction to a conditional spin-contact channel. It is not a public local-GR proof yet, because the parent action still has to sign no propagating torsion kinetic term, no critical algebraic kernel, and/or a source-backed spin-contact bound.

## Source Register

{table(rows_from(SOURCE_REGISTER))}

## Branch Conditions

{table(rows_from(CONDITION_OUTPUT))}

## Torsion Theorem Gate

{table(rows_from(THEOREM_OUTPUT))}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Outcome Rows

{table(rows_from(OUTCOME_ROWS))}

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
    return f"""# 4451 Y5 R2FR torsion spin residual cT zero or contact bound

Private checkpoint generated at `{STAMP}`.

Summary:
- Derived the conditional algebraic torsion equation `L_T T = kappa tau_spin` for the no-`D T` compact local branch.
- Spinless macroscopic local sources give `T=0` if `ker L_T=0`.
- The remaining problem is not generic long-range torsion; it is operator invertibility/no propagating torsion plus spin-contact bounds.

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
        "claim": "4451 derives the conditional torsion-spin reduction: in a no-kinetic-torsion Cartan branch, connection variation gives an algebraic torsion equation, so spinless local sources have T=0 if the torsion operator has no kernel; spin-contact bounds remain open.",
        "current_evidence": "4451 source register, branch conditions, torsion theorem gate, derivation rows, outcome rows, claim gates, decision, status, next target and validation CSV.",
        "status": "torsion_spin_residual_demoted_to_conditional_contact_channel_operator_invertibility_open_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Smuggling torsion away without proving no kinetic torsion/no operator kernel or sourcing spin-contact bounds.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4451 source register, branch conditions, torsion theorem gate, derivation rows, outcome rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Smuggling torsion away without proving no kinetic torsion/no operator kernel or sourcing spin-contact bounds.",
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
    spine_section = f"""## Local GR Parent-Derivation Update - Torsion Spin Residual

Marker: `{MARKER}`  
Source checkpoint: `4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md`  
Claim register row: `{CLAIM_ID}`

The selected `c_T_spin` row is now conditionally demoted: in the no-`D T` compact local branch, torsion is algebraic, `L_T T = kappa tau_spin`, so spinless local sources give `T=0` if `ker L_T=0`. Remaining work is operator invertibility/no propagating torsion or spin-contact bounds.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Torsion Spin Residual

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4451-Y5-R2FR-torsion-spin-residual-cT-zero-or-contact-bound.md`

Inside the private packet, `c_T_spin` is no longer treated as a generic long-range local force. It is a conditional contact-channel problem unless the parent action introduces propagating torsion or an algebraic zero mode.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows() -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    conditions = rows_from(CONDITION_OUTPUT)
    theorem = rows_from(THEOREM_OUTPUT)
    gates = rows_from(CLAIM_GATES)
    checks = [
        ("VAL4451_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4451_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4451_2_conditions_sourced", all(row["source_exists"] == "True" for row in conditions), "all branch conditions have source paths"),
        ("VAL4451_3_algebraic_theorem", any(row["theorem_id"] == "TH4451_0_connection_variation" and row["algebraic_no_derivatives"] == "True" for row in theorem), "algebraic torsion equation written"),
        ("VAL4451_4_spinless_zero", any(row["theorem_id"] == "TH4451_1_spinless_zero" and row["spinless_zero"] == "True" and row["long_range_zero"] == "True" for row in theorem), "spinless zero conditional written"),
        ("VAL4451_5_contact_explicit", any(row["theorem_id"] == "TH4451_2_contact_demote" and row["contact_remaining"] == "True" for row in theorem), "contact channel remains explicit"),
        ("VAL4451_6_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4451_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-293"),
        ("VAL4451_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4451_9_post_doc", DOC_PATH.exists() and "Private checkpoint" in text(DOC_PATH), "post checkpoint doc exists"),
        ("VAL4451_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4451_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4451_12_next_target", NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "next target written"),
        ("VAL4451_13_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(CONDITION_INPUT, condition_input_rows())
    write_csv(CONDITION_OUTPUT, [evaluate_condition_row(row) for row in rows_from(CONDITION_INPUT)])
    write_csv(THEOREM_INPUT, theorem_input_rows())
    write_csv(THEOREM_OUTPUT, [evaluate_theorem_row(row) for row in rows_from(THEOREM_INPUT)])
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(OUTCOME_ROWS, outcome_rows())
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
