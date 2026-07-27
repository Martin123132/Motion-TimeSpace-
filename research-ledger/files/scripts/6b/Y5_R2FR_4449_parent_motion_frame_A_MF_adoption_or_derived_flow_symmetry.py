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

from a_mf_adoption_gate import evaluate_contract_rows, evaluate_evidence_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4449"
CLAIM_ID = "L-291"
MARKER = "PPC4161_PARENT_MOTION_FRAME_A_MF_PRIVATE_ADOPTION_4449"
PACKET_MARKER = "PPC4161_PACKET_A_MF_PRIVATE_ADOPTION_4449"
DECISION = "A_MF_ADOPTED_AS_EXPLICIT_PRIVATE_PARENT_AXIOM_CANDIDATE_OLDER_PRIMITIVE_DERIVATION_NOT_FOUND_IR_SELECTOR_REMAINS_NONCLAIM"
NEXT_TARGET = "4450-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"

FORMAL_PATH = FORMAL / "465-PPC4161-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md"
DOC_PATH = POST / "4449-Y5-R2FR-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4449_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4449_SOURCE_REGISTER.csv"
EVIDENCE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4449_A_MF_EVIDENCE_INPUT.csv"
EVIDENCE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4449_A_MF_EVIDENCE_OUTPUT.csv"
CONTRACT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4449_A_MF_PRIVATE_ADOPTION_CONTRACT_INPUT.csv"
CONTRACT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4449_A_MF_PRIVATE_ADOPTION_CONTRACT_OUTPUT.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4449_DERIVATION_ROWS.csv"
CONSEQUENCE_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4449_CONSEQUENCE_LINKS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4449_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4449_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4449_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4449_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "a_mf_adoption_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4449_parent_motion_frame_A_MF_adoption_or_derived_flow_symmetry.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4448 = SOURCE_DIR / "P8_Y5_R2FR_4448_NEXT_TARGET.csv"
FORMAL_464 = FORMAL / "464-PPC4161-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"
POST_4070 = POST / "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md"
POST_4071 = POST / "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md"
POST_4072 = POST / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md"
FORMAL_179 = FORMAL / "179-PPC4048-local-parent-packet-candidate.md"
FORMAL_198 = FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md"
FORMAL_199 = FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md"
FORMAL_200 = FORMAL / "200-PPC4161-Palatini-IR-normal-form-selector-under-AMF.md"
PROOF_19 = FORMAL / "19-proof-obligations.md"
SPINE_07 = FORMAL / "07-unification-spine.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUND_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
OUT_4182_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4182_EFFECTIVE_GR_LABEL_DECISION.csv"
OUT_4182_SWEEP = SOURCE_DIR / "P8_Y5_R2FR_4182_PARENT_SYMMETRY_EVIDENCE_SWEEP.csv"
OUT_4182_FORCING = SOURCE_DIR / "P8_Y5_R2FR_4182_COMPENSATOR_FORCING_DERIVATION.csv"
OUT_4183_FORK = SOURCE_DIR / "P8_Y5_R2FR_4183_FORK_DECISION.csv"
OUT_4183_CONSEQ = SOURCE_DIR / "P8_Y5_R2FR_4183_A_MF_ADOPTION_CONSEQUENCE_MATRIX.csv"
OUT_4184_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4184_BRANCH_DECISION.csv"
OUT_4184_SELECTOR = SOURCE_DIR / "P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv"
OUT_4184_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv"


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
        {"source_id": "SRC4449_00_next4448", "path": NEXT_4448, "needle": "4449-Y5-R2FR-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md", "role": "4448 selected A_MF target."},
        {"source_id": "SRC4449_01_formal464", "path": FORMAL_464, "needle": "Actual derivation blocker: A_MF", "role": "4448 ranking map."},
        {"source_id": "SRC4449_02_4070", "path": POST_4070, "needle": "exact scalar gradients alone do **not** derive local GR", "role": "flatness obstruction."},
        {"source_id": "SRC4449_03_4071", "path": POST_4071, "needle": "If MTS owns local internal motion-frame symmetry", "role": "conditional compensator forcing."},
        {"source_id": "SRC4449_04_4072", "path": POST_4072, "needle": "motion_frame_gauge_action = formal_private_candidate", "role": "formal private candidate action."},
        {"source_id": "SRC4449_05_formal179", "path": FORMAL_179, "needle": "PPC4048_4070_4072_motion_frame_gauge_candidate = true", "role": "packet candidate record."},
        {"source_id": "SRC4449_06_formal198", "path": FORMAL_198, "needle": "The internal motion-frame labels of X^A=L_* Psi^A are local gauge redundancies", "role": "A_MF adoption-ready axiom."},
        {"source_id": "SRC4449_07_4182_decision", "path": OUT_4182_DECISION, "needle": "current_MTS_local_GR_derivation", "role": "older derivation not found."},
        {"source_id": "SRC4449_08_4182_sweep", "path": OUT_4182_SWEEP, "needle": "EV4182_7_current_verdict", "role": "source sweep verdict."},
        {"source_id": "SRC4449_09_4182_forcing", "path": OUT_4182_FORCING, "needle": "FD4182_4_covariant_coframe", "role": "compensator forcing theorem."},
        {"source_id": "SRC4449_10_formal199", "path": FORMAL_199, "needle": "A_MF_ADOPTION_CONTRACT_WRITTEN", "role": "A_MF consequences formal note."},
        {"source_id": "SRC4449_11_4183_fork", "path": OUT_4183_FORK, "needle": "A_MF_adoption_contract_written", "role": "machine adoption contract status."},
        {"source_id": "SRC4449_12_4183_consequence", "path": OUT_4183_CONSEQ, "needle": "AC4183_0_A_MF_adoption", "role": "A_MF consequence matrix."},
        {"source_id": "SRC4449_13_formal200", "path": FORMAL_200, "needle": "if `A_MF` is adopted", "role": "IR selector under A_MF."},
        {"source_id": "SRC4449_14_4184_selector", "path": OUT_4184_SELECTOR, "needle": "SEL4184_0_A_MF", "role": "A_MF owned as candidate in selector."},
        {"source_id": "SRC4449_15_4184_decision", "path": OUT_4184_DECISION, "needle": "selector_assumptions_parent_derived", "role": "IR selector still parent debt."},
        {"source_id": "SRC4449_16_4184_residual", "path": OUT_4184_RESIDUAL, "needle": "RB4184_3_cGamma", "role": "residual coefficient ledger."},
        {"source_id": "SRC4449_17_proof_obligations", "path": PROOF_19, "needle": "parent-sign local motion-frame Lorentz + translation gauge symmetry", "role": "proof obligation."},
        {"source_id": "SRC4449_18_spine", "path": SPINE_07, "needle": "motion_frame_gauge_parent_candidate = true", "role": "spine candidate status."},
        {"source_id": "SRC4449_19_core_action", "path": CORE_ACTION, "needle": "The fundamental object is a scalar motion field", "role": "older primitive scalar source."},
        {"source_id": "SRC4449_20_fund_action", "path": FUND_ACTION, "needle": "gradients encode directional flow of curvature information", "role": "flow clue but not A_MF proof."},
        {"source_id": "SRC4449_21_gate", "path": GATE_PATH, "needle": "def evaluate_evidence_row", "role": "4449 A_MF gate."},
        {"source_id": "SRC4449_22_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4449"', "role": "4449 generator."},
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


def evidence_input_rows() -> List[Dict[str, object]]:
    return [
        {"row_id": "AMF4449_0_scalar_motion_field", "evidence_class": "older_primitive", "claim_piece": "scalar motion field exists", "source_path": str(CORE_ACTION), "supports_A_MF": True, "proves_A_MF": False, "counterevidence": False, "adoption_ready": False, "public_claim_false": True},
        {"row_id": "AMF4449_1_flow_curvature_clue", "evidence_class": "older_primitive", "claim_piece": "flow gradients encode directional curvature information", "source_path": str(FUND_ACTION), "supports_A_MF": True, "proves_A_MF": False, "counterevidence": False, "adoption_ready": False, "public_claim_false": True},
        {"row_id": "AMF4449_2_flatness_obstruction", "evidence_class": "countermodel", "claim_piece": "exact scalar gradient route cannot derive curved local GR", "source_path": str(POST_4070), "supports_A_MF": True, "proves_A_MF": False, "counterevidence": True, "adoption_ready": False, "public_claim_false": True},
        {"row_id": "AMF4449_3_compensator_forcing", "evidence_class": "conditional_theorem", "claim_piece": "local motion-frame symmetry forces omega and B", "source_path": str(OUT_4182_FORCING), "supports_A_MF": True, "proves_A_MF": False, "counterevidence": False, "adoption_ready": True, "public_claim_false": True},
        {"row_id": "AMF4449_4_source_sweep_verdict", "evidence_class": "sweep", "claim_piece": "older MTS derivation of A_MF not found", "source_path": str(OUT_4182_SWEEP), "supports_A_MF": False, "proves_A_MF": False, "counterevidence": True, "adoption_ready": False, "public_claim_false": True},
        {"row_id": "AMF4449_5_adoption_contract", "evidence_class": "adoption_contract", "claim_piece": "A_MF contract and Noether consequences written", "source_path": str(OUT_4183_FORK), "supports_A_MF": True, "proves_A_MF": False, "counterevidence": False, "adoption_ready": True, "public_claim_false": True},
        {"row_id": "AMF4449_6_ir_selector", "evidence_class": "downstream_selector", "claim_piece": "A_MF enters IR selector but does not force Palatini alone", "source_path": str(OUT_4184_DECISION), "supports_A_MF": True, "proves_A_MF": False, "counterevidence": False, "adoption_ready": True, "public_claim_false": True},
    ]


def contract_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "CON4449_0_private_A_MF_adoption",
            "clause": "Inside PPC4161 private local branch, treat internal motion-frame labels X^A=L_*Psi^A as local affine/Lorentz gauge redundancies; use e^A=D_omega X^A+B^A and g_obs=eta_AB e^A e^B before matter/EM readout.",
            "source_path": str(FORMAL_199),
            "clause_signed_private": True,
            "consequences_written": True,
            "ir_selector_needed": True,
            "public_claim_false": True,
        },
        {
            "contract_id": "CON4449_1_no_older_derivation_claim",
            "clause": "Do not claim older motion/flow primitives already derive A_MF; they motivate/admit the axiom but do not prove local gauge redundancy.",
            "source_path": str(OUT_4182_DECISION),
            "clause_signed_private": True,
            "consequences_written": True,
            "ir_selector_needed": True,
            "public_claim_false": True,
        },
    ]


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "D4449_0_failed_older_derivation",
            "claim": "The older scalar/flow corpus does not derive A_MF by itself.",
            "derivation": "The scalar motion field and directional-flow language motivate a motion-frame branch, but 4070 proves exact scalar coframes are locally flat and 4182's sweep finds no parent-owned local affine/Lorentz gauge redundancy. Therefore an older-primitive derivation is not currently available.",
            "consequence": "No public local-GR derivation claim is allowed from old scalar/flow text alone.",
            "status": "OLDER_DERIVATION_NOT_FOUND",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4449_1_private_adoption",
            "claim": "A_MF can be adopted explicitly as a private parent-branch axiom candidate.",
            "derivation": "4071/4182 prove that if A_MF is real, omega and B are forced compensators. 4183 writes the adoption contract and Noether identities. 4184 already uses A_MF as an owned candidate in the IR selector. 4449 therefore signs A_MF only inside the private PPC4161 parent-branch candidate.",
            "consequence": "The coframe/connection variables become branch-owned for downstream private tests, while public proof remains blocked by IR selector assumptions and residual coefficients.",
            "status": "A_MF_PRIVATE_BRANCH_ADOPTED_AS_AXIOM_CANDIDATE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "D4449_2_next_problem",
            "claim": "A_MF adoption does not finish local GR.",
            "derivation": "4183 shows A_MF constrains variables and Noether identities but does not uniquely select the Palatini/EH action. 4184 writes a conditional IR selector and residual ledger for extra invariant terms.",
            "consequence": "The next problem is coefficient/scale law or bound rows for c_T, c_R2, c_D, c_Gamma, c_bdy, and delta_kappa.",
            "status": "IR_SELECTOR_AND_RESIDUAL_LEDGER_REMAIN",
            "valid_for_claim": False,
        },
    ]


def consequence_rows() -> List[Dict[str, object]]:
    return [
        {"link_id": "LINK4449_0", "if_A_MF_private_adopted": "omega^AB and B^A are forced compensators", "downstream_source": str(OUT_4182_FORCING), "remaining_gate": "torsion/nonmetricity and IR normal form", "valid_for_claim": False},
        {"link_id": "LINK4449_1", "if_A_MF_private_adopted": "Noether identities explain Bianchi-compatible total source conservation", "downstream_source": str(OUT_4183_CONSEQ), "remaining_gate": "same-coframe matter/EM and boundary routing", "valid_for_claim": False},
        {"link_id": "LINK4449_2", "if_A_MF_private_adopted": "EC/Palatini is selected only under extra IR assumptions", "downstream_source": str(OUT_4184_SELECTOR), "remaining_gate": "residual coefficient map or parent scale law", "valid_for_claim": False},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [{
        "decision_id": "DEC4449_0",
        "decision": DECISION,
        "summary": "4449 adopts A_MF as an explicit private PPC4161 parent-branch axiom candidate. It does not claim A_MF is derived from older scalar/flow primitives: the exact-gradient route fails and the source sweep found no older parent-owned local gauge redundancy. The adoption is useful because it gives branch-owned Cartan variables and Noether identities; the next blocker is the IR selector/residual coefficient ledger.",
        "next_target": NEXT_TARGET,
        "public_claim": False,
        "valid_for_claim": False,
    }]


def status_rows() -> List[Dict[str, object]]:
    return [{
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "claim_id": CLAIM_ID,
        "decision": DECISION,
        "A_MF_private_adopted": True,
        "older_MTS_derivation_found": False,
        "omega_B_forced_if_A_MF": True,
        "Noether_consequences_available": True,
        "Palatini_forced_by_A_MF_alone": False,
        "remaining": "IR selector assumptions and residual coefficient/scale/bound ledger",
        "next_target": NEXT_TARGET,
        "public_claim": False,
        "valid_for_claim": False,
        "generated_utc": STAMP,
    }]


def next_rows() -> List[Dict[str, object]]:
    return [{
        "next_id": "NT4449_0",
        "target": NEXT_TARGET,
        "objective": "Map every extra A_MF-invariant residual coefficient to parent-zero, parent-scale, screening, or source-backed local bounds.",
        "derive_first": "try parent scale/zero laws for c_T, c_R2, c_D, c_Gamma, c_bdy, and delta_kappa",
        "fallback": "build PPN/R10/WEP/clock/orbital bound rows for each coefficient",
        "risk": "pretending A_MF adoption alone selects Einstein-Hilbert/Palatini",
        "valid_for_claim": False,
    }]


def claim_gate_rows(evidence_outputs: Sequence[Mapping[str, str]], contract_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    evidence = {row["row_id"]: row for row in evidence_outputs}
    contracts = {row["contract_id"]: row for row in contract_outputs}
    sources = rows_from(SOURCE_REGISTER)
    no_claim = not any(row.get("valid_for_claim") == "True" for row in evidence_outputs)
    return [
        {"gate_id": "CG4449_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in sources), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4449_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in sources), "valid_for_claim": False, "detail": "A_MF decision is source-backed."},
        {"gate_id": "CG4449_2_older_derivation_not_found", "claim": "older scalar/flow derivation is not claimed", "passed": evidence["AMF4449_4_source_sweep_verdict"].get("current_status") == "COUNTEREVIDENCE_BLOCKS_PUBLIC_DERIVATION", "valid_for_claim": False, "detail": "Prevents magic roof-ladder move."},
        {"gate_id": "CG4449_3_compensator_forcing_ready", "claim": "compensator theorem supports adoption", "passed": evidence["AMF4449_3_compensator_forcing"].get("current_status") == "ADOPTION_READY_PRIVATE_AXIOM_INPUT", "valid_for_claim": False, "detail": "omega/B are forced if A_MF is signed."},
        {"gate_id": "CG4449_4_private_adoption_contract", "claim": "A_MF private branch contract is adopted", "passed": contracts["CON4449_0_private_A_MF_adoption"].get("current_status") == "A_MF_ADOPTED_PRIVATE_BRANCH_IR_SELECTOR_STILL_REQUIRED", "valid_for_claim": False, "detail": "Adopted only as private parent-branch axiom candidate."},
        {"gate_id": "CG4449_5_no_older_public_claim", "claim": "contract blocks older-derivation public claim", "passed": contracts["CON4449_1_no_older_derivation_claim"].get("current_status") == "A_MF_ADOPTED_PRIVATE_BRANCH_IR_SELECTOR_STILL_REQUIRED", "valid_for_claim": False, "detail": "No public local-GR proof from old scalar flow text."},
        {"gate_id": "CG4449_6_ir_selector_remains", "claim": "IR selector remains next blocker", "passed": "IR_SELECTOR_AND_RESIDUAL_LEDGER_REMAIN" in text(DERIVATION_ROWS), "valid_for_claim": False, "detail": "A_MF alone does not force EH."},
        {"gate_id": "CG4449_7_no_public_claim", "claim": "4449 emits no public local-GR claim", "passed": no_claim, "valid_for_claim": False, "detail": "Every evidence row remains nonclaim."},
        {"gate_id": "CG4449_8_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def build_doc(sources: Sequence[Mapping[str, object]], evidence_outputs: Sequence[Mapping[str, object]], contract_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 465 PPC4161 parent motion-frame A_MF adoption or derived flow symmetry

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4449 takes the clean route:

```text
Older scalar/flow primitives motivate A_MF but do not prove it.
A_MF is now adopted only as an explicit private PPC4161 parent-branch axiom candidate.
```

That means the branch can use the Cartan variables `omega`, `B`, `e`, and `g_obs` as owned candidate variables for private work. It still cannot claim public local GR, because `A_MF` alone does not select the Einstein-Cartan/Palatini normal form or kill all extra invariant coefficients.

## Source Register

{table(sources)}

## Evidence Gate

{table(evidence_outputs)}

## Private Adoption Contract

{table(contract_outputs)}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Consequence Links

{table(rows_from(CONSEQUENCE_ROWS))}

## Claim Gates

{table(gates)}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4449 Y5 R2FR parent motion-frame A_MF adoption or derived flow symmetry

Private checkpoint generated at `{STAMP}`.

Summary:
- Older scalar/flow material does not prove `A_MF`.
- `A_MF` is adopted as an explicit private PPC4161 parent-branch axiom candidate.
- This owns the Cartan variables for private derivation work, but leaves the IR selector/residual coefficient problem open.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "4449 adopts A_MF as an explicit private PPC4161 parent-branch axiom candidate while rejecting any claim that older scalar/flow primitives already derive it. The branch gains owned candidate Cartan variables, but public local GR remains blocked by IR selector and residual coefficient gates.",
        "current_evidence": "4449 source register, evidence gate, private adoption contract, derivation rows, consequence links, claim gates, decision, status, next target and validation CSV.",
        "status": "A_MF_private_parent_axiom_candidate_adopted_older_derivation_false_IR_selector_open_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating A_MF adoption as a public derivation or as sufficient to select EH/Palatini.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4449 source register, evidence gate, private adoption contract, derivation rows, consequence links, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Treating A_MF adoption as a public derivation or as sufficient to select EH/Palatini.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Parent-Derivation Update - A_MF Private Adoption

Marker: `{MARKER}`  
Source checkpoint: `4449-Y5-R2FR-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md`  
Claim register row: `{CLAIM_ID}`

`A_MF` is now adopted only as an explicit private PPC4161 parent-branch axiom candidate. Older scalar/flow primitives motivate the move but do not prove it. The branch can use `omega`, `B`, `e`, and `g_obs` as owned candidate Cartan variables for private derivation, while the public theorem remains blocked by IR selector assumptions and residual coefficients.
"""
    packet_section = f"""## PPC4161 Packet Addendum - A_MF Private Adoption

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4449-Y5-R2FR-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md`

Inside the private packet, `A_MF` is signed as a branch axiom candidate, not as a recovered theorem from old scalar motion-field text. The next packet work is the residual coefficient/scale-law ledger, not another proof that `omega` and `B` are forced if `A_MF` holds.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    evidence = {row["row_id"]: row for row in rows_from(EVIDENCE_OUTPUT)}
    contracts = {row["contract_id"]: row for row in rows_from(CONTRACT_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    checks = [
        ("VAL4449_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4449_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4449_2_older_not_derived", evidence["AMF4449_4_source_sweep_verdict"].get("current_status") == "COUNTEREVIDENCE_BLOCKS_PUBLIC_DERIVATION", "older derivation not claimed"),
        ("VAL4449_3_adoption_ready", evidence["AMF4449_5_adoption_contract"].get("current_status") == "ADOPTION_READY_PRIVATE_AXIOM_INPUT", "adoption contract is ready"),
        ("VAL4449_4_private_contract", contracts["CON4449_0_private_A_MF_adoption"].get("current_status") == "A_MF_ADOPTED_PRIVATE_BRANCH_IR_SELECTOR_STILL_REQUIRED", "A_MF private contract adopted"),
        ("VAL4449_5_no_public_contract", contracts["CON4449_1_no_older_derivation_claim"].get("current_status") == "A_MF_ADOPTED_PRIVATE_BRANCH_IR_SELECTOR_STILL_REQUIRED", "no older public derivation claim"),
        ("VAL4449_6_all_claim_gates", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4449_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-291"),
        ("VAL4449_8_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4449_9_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4449_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4449_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4449_12_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target written"),
        ("VAL4449_13_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(EVIDENCE_INPUT, evidence_input_rows())
    write_csv(EVIDENCE_OUTPUT, evaluate_evidence_rows(EVIDENCE_INPUT))
    write_csv(CONTRACT_INPUT, contract_input_rows())
    write_csv(CONTRACT_OUTPUT, evaluate_contract_rows(CONTRACT_INPUT))
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(CONSEQUENCE_ROWS, consequence_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    evidence_outputs = rows_from(EVIDENCE_OUTPUT)
    contract_outputs = rows_from(CONTRACT_OUTPUT)
    gates = claim_gate_rows(evidence_outputs, contract_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), evidence_outputs, contract_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
