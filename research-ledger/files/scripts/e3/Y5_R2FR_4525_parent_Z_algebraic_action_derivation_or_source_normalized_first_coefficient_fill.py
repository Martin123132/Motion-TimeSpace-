from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4525"
CLAIM_ID = "L-367"
MARKER = "PPC4161_PARENT_Z_ALGEBRAIC_ACTION_DERIVATION_OR_SOURCE_NORMALIZED_FIRST_COEFFICIENT_FILL_4525"
PACKET_MARKER = "PPC4161_PACKET_PARENT_Z_ALGEBRAIC_ACTION_DERIVATION_OR_SOURCE_NORMALIZED_FIRST_COEFFICIENT_FILL_4525"
DECISION = "QUOTIENT_EVEN_MORSE_BOTT_PARENT_Z_MECHANISM_DERIVED_SOURCE_SIGNATURE_NOT_FOUND_COEFFICIENT_FILL_ROUTE_DEFINED"
NEXT_TARGET = "4526-Y5-R2FR-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md"

FORMAL_PATH = FORMAL / "541-PPC4161-parent-Z-algebraic-action-derivation-or-source-normalized-first-coefficient-fill.md"
DOC_PATH = POST / "4525-Y5-R2FR-parent-Z-algebraic-action-derivation-or-source-normalized-first-coefficient-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4525_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv"
PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_Z_PROOF_STEPS.csv"
SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_SOURCE_NORMALIZED_COEFFICIENT_FILL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_DECISION.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4525_NEXT_TARGET.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4525_VALIDATION.csv"

DOC_4524 = POST / "4524-Y5-R2FR-first-finite-residual-alpha-smoke-runner-or-parent-Z-action-signature.md"
FORMAL_4524 = FORMAL / "540-PPC4161-first-finite-residual-alpha-smoke-runner-or-parent-Z-action-signature.md"
VALIDATION_4524 = SOURCE_DIR / "P8_Y5_BRR545_4524_VALIDATION.csv"
LAW_4524 = SOURCE_DIR / "P8_Y5_R2FR_4524_FINITE_RESIDUAL_ALPHA_LAW.csv"
INPUTS_4524 = SOURCE_DIR / "P8_Y5_R2FR_4524_RESIDUAL_ALPHA_INPUT_CONTRACT.csv"
PARENT_Z_4524 = SOURCE_DIR / "P8_Y5_R2FR_4524_PARENT_Z_ACTION_SIGNATURE_HUNT.csv"
PARENT_ACTION_4523 = SOURCE_DIR / "P8_Y5_R2FR_4523_RANK_ZERO_PARENT_ACTION_CONTRACT.csv"
FORMAL_190 = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
FORMAL_196 = FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md"
MUC_2537 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2537_MINIMAL_UNIVERSAL_MATTER_COUPLING_SIGNATURE.csv"
MCA_2587 = SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ADOPTION_GATE.csv"
NOTOWER_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_INTEGRATED_OUT_TOWER_AUDIT.csv"
NOMARKER_2623 = SOURCE_DIR / "P8_Y5_PRIMITIVE_QUOTIENT_GATE_2623_NO_NATURAL_MARKER_AUDIT.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def line_of(path: Path, needle: str) -> int:
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, body: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as handle:
        if current and not current.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + body.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4525_00_formal4524", "4524 formal handoff", FORMAL_4524, "PPC4161_FIRST_FINITE_RESIDUAL_ALPHA_SMOKE_RUNNER_OR_PARENT_Z_ACTION_SIGNATURE_4524", "finite-residual alpha bridge"),
        ("SRC4525_01_post4524", "4524 post handoff", DOC_4524, "4525-Y5-R2FR-parent-Z-algebraic-action-derivation-or-source-normalized-first-coefficient-fill.md", "declared 4525 target"),
        ("SRC4525_02_val4524", "4524 validation", VALIDATION_4524, "VAL4524_OVERALL", "previous validation pass"),
        ("SRC4525_03_law4524", "4524 finite alpha law", LAW_4524, "FRA4524_3_R10_alpha_projection", "alpha projection formula"),
        ("SRC4525_04_inputs4524", "4524 input contract", INPUTS_4524, "RAI4524_0_mmin", "coefficient inputs"),
        ("SRC4525_05_parentZ4524", "4524 parent Z hunt", PARENT_Z_4524, "PZA4524_0_action_form", "parent Z action signature"),
        ("SRC4525_06_action4523", "4523 parent action contract", PARENT_ACTION_4523, "RZPA4523_0_total_branch", "rank-zero parent action contract"),
        ("SRC4525_07_selector190", "190 parent selector", FORMAL_190, "PPC4161_PARENT_ACTION_SELECTOR_OR_LOCAL_QUARANTINE", "selector/local branch quarantine"),
        ("SRC4525_08_adoption196", "196 minimal parent adoption", FORMAL_196, "PPC4161_MINIMAL_PARENT_ACTION_ADOPTION_MATRIX", "adoption matrix"),
        ("SRC4525_09_muc2537", "minimal universal matter coupling", MUC_2537, "MUC2537_6_verdict", "matter coupling not parent-signed"),
        ("SRC4525_10_mca2587", "minimum parent matter gate", MCA_2587, "AD2587_0_action_adoption", "matter action adoption gate"),
        ("SRC4525_11_notower2623", "no integrated-out tower audit", NOTOWER_2623, "TOW2623_4_overall", "tower countermodels"),
        ("SRC4525_12_nomarker2623", "no marker audit", NOMARKER_2623, "MRK2623_6_overall", "marker countermodels"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, path, needle, note in specs:
        body = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "QEZ4525_0_field_space_split",
            "name": "quotient collar normal form",
            "statement": "Let pi:F_loc -> Q be the parent-to-quotient map. In a local collar around a chosen GR/Newton branch section s(Q), write parent fields as Phi=s(q)+z with z vertical, Dpi(z)=0.",
            "formula": "Phi = s(q) + z, z in ker(Dpi), q=pi(Phi)",
            "proof_status": "SETUP",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QEZ4525_1_even_involution",
            "name": "vertical reflection kills first force",
            "statement": "If the parent action, measure, matter coupling, readout and boundary conditions are invariant under a vertical involution I_q:z->-z, then every odd vertical Taylor coefficient vanishes at z=0.",
            "formula": "S[q,z,Psi]=S[q,-z,Psi] => delta S/dz|_{z=0}=0 and cubic/odd source vertices vanish",
            "proof_status": "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QEZ4525_2_rank_zero_from_auxiliary_verticality",
            "name": "no vertical kinetic term gives rank zero",
            "statement": "If z is an auxiliary vertical coordinate and the parent Lagrangian contains no nabla z nabla z term on the physical quotient, the z principal symbol is zero and the local branch is algebraic.",
            "formula": "partial L/partial(nabla_mu z^A)=0 => Z_AB=0 in the z principal block",
            "proof_status": "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QEZ4525_3_M_lock_from_Morse_Bott_Hessian",
            "name": "transverse Morse-Bott lock",
            "statement": "If the even vertical Hessian M_AB is positive/coercive on the reduced vertical complement, z=0 is an isolated transverse extremum and M_AB z^B=0 implies z=0.",
            "formula": "delta^2_z S|_0 = int sqrt(-g) z^A M_AB z^B, M>=m_min I, m_min>0",
            "proof_status": "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QEZ4525_4_source_silence",
            "name": "q-basic Hilbert matter plus evenness kills retained source",
            "statement": "If matter and Maxwell/Poynting sectors are q-basic Hilbert-owned and respect the same vertical involution, their vertical first variation at z=0 is zero. Radiative boundary flux is silent only if the no-flux boundary is also invariant; otherwise it is a finite residual.",
            "formula": "delta_z S_matter[q,Psi]|_0=0; B_A^EM=0 only for owned no-flux, else B_A^EM retained",
            "proof_status": "DERIVED_CONDITIONAL_WITH_Poynting_CAVEAT",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QEZ4525_5_local_GR_closure_mechanism",
            "name": "parent Z closure theorem",
            "statement": "Under QEZ4525_1-4 in one same branch, the 4523 parent Z-action contract is satisfied: rank(Z_AB)=0, M_AB locks z, retained sources vanish, and the local rank-zero residual closes without an alpha claim.",
            "formula": "even + auxiliary + Morse-Bott + q-basic/no-flux => M_AB z^B=0 => z=0",
            "proof_status": "MECHANISM_DERIVED_PARENT_SIGNATURE_NOT_FOUND",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QEZ4525_6_symmetry_breaking_fallback",
            "name": "if any clause fails, fill coefficients",
            "statement": "Any odd vertical source, kinetic leakage, boundary flux, marker, tower, calibration or readout asymmetry becomes a source-normalized finite coefficient for 4524 scoring rather than being set to zero.",
            "formula": "epsilon_odd, K_kin, B_flux, J_marker, J_tower, J_cal -> alpha/PPN/clock/orbit residual rows",
            "proof_status": "DERIVED_FALLBACK",
            "valid_for_claim": False,
        },
    ]


def proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PROOF4525_0_Taylor",
            "step": "Taylor expand the local parent density in vertical coordinates around z=0.",
            "expression": "L=L0(q,Psi)+L_A z^A+1/2 M_AB z^A z^B+K_AB^{mu nu} nabla_mu z^A nabla_nu z^B+O(z^3)",
            "result": "identifies the exact objects that 4523 named Z_AB, M_AB and retained source terms",
        },
        {
            "step_id": "PROOF4525_1_evenness",
            "step": "Apply I_q:z->-z invariance to the Taylor expansion.",
            "expression": "L(q,z)=L(q,-z)",
            "result": "L_A=0 and all odd retained source vertices vanish at the section",
        },
        {
            "step_id": "PROOF4525_2_auxiliary",
            "step": "Demand auxiliary verticality rather than a propagating hidden field.",
            "expression": "K_AB^{mu nu}=0 on Q_phys",
            "result": "rank(Z_AB)=0; if K_AB is nonzero the route becomes finite-range alpha scoring",
        },
        {
            "step_id": "PROOF4525_3_Morse_Bott",
            "step": "Use a positive transverse Hessian to lock the vertical coordinate.",
            "expression": "M_AB >= m_min h_AB, m_min>0",
            "result": "Euler equation M_AB z^B+O(z^3)=0 has the small-branch solution z=0",
        },
        {
            "step_id": "PROOF4525_4_sources",
            "step": "Route matter, Poynting, boundary and readout through the same symmetry.",
            "expression": "delta_z(S_Hilbert[q]+S_EM[q]+S_readout_post[q])|_0=0",
            "result": "source silence follows only if these sectors are q-basic/even/no-flux in the same branch",
        },
        {
            "step_id": "PROOF4525_5_verdict",
            "step": "Compare to current corpus signatures.",
            "expression": "explicit parent involution + auxiliary verticality + Morse-Bott Hessian + source-even matter",
            "result": "mechanism is mathematically clean but not yet parent-signed in the corpus",
        },
    ]


def signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "SIG4525_0_vertical_involution",
            "needed_parent_signature": "I_q exists with I_q^2=1, pi∘I_q=pi and I_q fixes the GR/Newton section",
            "current_status": "NOT_FOUND_IN_SOURCES",
            "if_found": "kills F_1/J_retained by symmetry",
            "if_not_found": "odd coefficient epsilon_odd must be filled and scored",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4525_1_auxiliary_vertical_coordinate",
            "needed_parent_signature": "z has no independent kinetic/principal term on Q_phys",
            "current_status": "NOT_FOUND_IN_SOURCES",
            "if_found": "rank(Z_AB)=0 is derived",
            "if_not_found": "finite-range branch with lambda_X and alpha_X is required",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4525_2_Morse_Bott_Hessian",
            "needed_parent_signature": "positive transverse Hessian M_AB with m_min>0 or constraint-owned nulls",
            "current_status": "NOT_FOUND_IN_SOURCES",
            "if_found": "M_AB lock is derived",
            "if_not_found": "m_min row remains blocked and residual bound cannot score",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4525_3_source_evenness",
            "needed_parent_signature": "matter, EM/Poynting, source calibration, worldtube, marker, memory and readout are q-basic/even or postprocess-only",
            "current_status": "NOT_FOUND_IN_SOURCES",
            "if_found": "retained current and boundary/readout tails vanish",
            "if_not_found": "finite source-normalized coefficients must be filled",
            "valid_for_claim": False,
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "COF4525_0_epsilon_odd",
            "quantity": "epsilon_odd := ||delta_z S_parent|_{z=0}||",
            "alpha_runner_role": "numerator residual if vertical evenness fails",
            "source_needed": "parent action first vertical derivative in local collar",
            "current_value": "MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4525_1_Kkin",
            "quantity": "K_AB^{mu nu}",
            "alpha_runner_role": "finite-range/principal leakage if auxiliary verticality fails",
            "source_needed": "parent kinetic/principal symbol in vertical directions",
            "current_value": "MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4525_2_mmin",
            "quantity": "m_min(M_AB)",
            "alpha_runner_role": "denominator lock for no-cancellation residual bound",
            "source_needed": "Morse-Bott Hessian or Schur complement lower eigenvalue",
            "current_value": "MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4525_3_source_even_break",
            "quantity": "J_A^source-even-break",
            "alpha_runner_role": "retained source-current numerator",
            "source_needed": "source/worldtube/calibration/marker/memory/readout vertical first variation",
            "current_value": "MISSING",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4525_4_Poynting_flux",
            "quantity": "B_A^EM = int_boundary v_A^nu T^EM_{mu nu} n^mu dSigma",
            "alpha_runner_role": "boundary or wave-flux numerator if no-flux fails",
            "source_needed": "local EM flux boundary condition or radiative profile",
            "current_value": "ROUTED_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COF4525_5_K_R10",
            "quantity": "K_R10_X/(G_N M_S m_T)",
            "alpha_runner_role": "projection from residual amplitude to alpha",
            "source_needed": "arena transfer operator and calibration convention",
            "current_value": "MISSING",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4525_0",
            "decision": DECISION,
            "meaning": "There is now a clean derivation route: a quotient-even Morse-Bott vertical parent action would prove F_1=0, rank(Z)=0, M-lock and source silence together. The current corpus does not yet source the required vertical involution/auxiliary/Hessian signatures, so no local-GR claim is made.",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG4525_0_mechanism",
            "gate": "quotient-even Morse-Bott mechanism derived",
            "status": "PASS_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4525_1_parent_signature",
            "gate": "explicit parent vertical involution and auxiliary Z action found",
            "status": "BLOCKED_NOT_FOUND",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4525_2_local_GR",
            "gate": "same-branch local GR claim",
            "status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4525_3_alpha_fallback",
            "gate": "source-normalized coefficient rows claim-ready",
            "status": "BLOCKED_PENDING_VALUES",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "claim_status": "private_conditional_nonclaim_derivation_mechanism",
            "created_at_utc": now(),
            "next_target": NEXT_TARGET,
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "hunt for explicit vertical involution/auxiliary parent Z action first; if absent, fill first source-normalized coefficient row",
            "why": "This is the strongest route under scrutiny: prove local GR from symmetry/Hessian, otherwise score the exact symmetry-breaking residual.",
            "valid_for_claim": False,
        }
    ]


def validate(sources: list[dict[str, Any]], claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        PROOF_CSV,
        SIGNATURE_CSV,
        COEFFICIENT_CSV,
        DECISION_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parse_issues: list[str] = []
    for path in csv_paths:
        try:
            rows = read_csv(path)
            if not rows:
                parse_issues.append(f"{path.name}:empty")
        except Exception as error:
            parse_issues.append(f"{path.name}:{error}")
    theorem_ids = {row.get("theorem_id") for row in read_csv(THEOREM_CSV)}
    proof_ids = {row.get("step_id") for row in read_csv(PROOF_CSV)}
    rows = [
        {
            "validation_id": "VAL4525_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all source paths exist and source needles are found",
        },
        {
            "validation_id": "VAL4525_01_mechanism",
            "status": "PASS" if "QEZ4525_5_local_GR_closure_mechanism" in theorem_ids else "FAIL",
            "detail": "local GR closure mechanism theorem row present",
        },
        {
            "validation_id": "VAL4525_02_proof",
            "status": "PASS" if "PROOF4525_5_verdict" in proof_ids else "FAIL",
            "detail": "proof verdict row present",
        },
        {
            "validation_id": "VAL4525_03_signature_not_claimed",
            "status": "PASS" if any(row.get("current_status") == "NOT_FOUND_IN_SOURCES" for row in read_csv(SIGNATURE_CSV)) else "FAIL",
            "detail": "parent signature absence is explicit",
        },
        {
            "validation_id": "VAL4525_04_coefficients",
            "status": "PASS" if any(row.get("coefficient_id") == "COF4525_0_epsilon_odd" for row in read_csv(COEFFICIENT_CSV)) else "FAIL",
            "detail": "first source-normalized coefficient rows exist",
        },
        {
            "validation_id": "VAL4525_05_claims_blocked",
            "status": "PASS" if all(str(row.get("valid_for_claim", "")).lower() == "false" for row in claims) else "FAIL",
            "detail": "all claim gates remain blocked",
        },
        {
            "validation_id": "VAL4525_06_csv_parse",
            "status": "PASS" if not parse_issues else "FAIL",
            "detail": ";".join(parse_issues) if parse_issues else "all generated CSV files parse and have rows",
        },
        {
            "validation_id": "VAL4525_07_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append({"validation_id": "VAL4525_OVERALL", "status": overall, "detail": "4525 parent Z mechanism derivation"})
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    signatures: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4525 — Parent Z Algebraic Action Derivation Or Source-Normalized First Coefficient Fill

Marker: `{MARKER}`  
Packet marker: `{PACKET_MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}`  
Status: private conditional non-claim; derivation mechanism found, parent signature not found.

## Result In Plain Terms

This is the best derivation route so far for the local-GR branch:

```text
Parent field collar: Phi = s(q) + z, z vertical
Vertical symmetry: z -> -z
Auxiliary verticality: no nabla z nabla z term
Morse-Bott Hessian: M_AB >= m_min I
q-basic/even matter and no-flux boundary
=> F_1 = 0, rank(Z_AB)=0, M_AB z^B=0, z=0
```

So the theory does not need to smuggle a plateau axiom if a parent-owned vertical reflection / quotient-even principle exists. That is the real hinge. If the symmetry is not in the parent theory, its breaking coefficients are exactly what 4524 must score as alpha/PPN/clock/orbit residuals.

## Quotient-Even Morse-Bott Z Theorem

{table(theorem)}

## Proof Steps

{table(proof)}

## Required Parent Signatures

{table(signatures)}

## First Coefficient Fill Rows If The Signature Fails

{table(coefficients)}

## Decision

{table(decisions)}

## Claim Gates

{table(gates)}

## Sources

{table(sources)}

## Validation

{table(validation)}

## Next

`{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    current = text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in current:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_parent_Z_mechanism",
        "claim": "4525 derives a quotient-even Morse-Bott vertical parent-action mechanism that would prove F_1=0, rank(Z_AB)=0, M-lock and retained-source silence together if parent-signed.",
        "current_evidence": "Generated theorem QEZ4525_0-6, proof steps, parent signature requirements, coefficient fallback rows and validation P8_Y5_BRR545_4525_VALIDATION.csv.",
        "status": "conditional_internal_nonclaim_parent_signature_needed",
        "next_test": NEXT_TARGET,
        "key_risk": "The required vertical involution, auxiliary verticality and positive Hessian are not yet sourced from the parent MTS corpus.",
        "sector": "local_gr_newton",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Mistaking a clean conditional mechanism for a parent-derived local-GR proof; if symmetry is absent, alpha/residual coefficients must be filled instead.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    proof = proof_rows()
    signatures = signature_rows()
    coefficients = coefficient_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    status = status_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(PROOF_CSV, proof)
    write_csv(SIGNATURE_CSV, signatures)
    write_csv(COEFFICIENT_CSV, coefficients)
    write_csv(DECISION_CSV, decisions)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, proof, signatures, coefficients, decisions, gates, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4525 Parent Z Algebraic Action Derivation Or Source-Normalized First Coefficient Fill

Marker: `{MARKER}`  
The local branch now has a concrete derivation mechanism: a quotient-even Morse-Bott vertical parent action, with auxiliary vertical coordinates and q-basic/even matter, would prove `F_1=0`, `rank(Z_AB)=0`, `M_AB` lock and retained-source silence in one stroke. Current corpus sources do not yet sign the vertical involution/Hessian, so the result remains private conditional and the coefficient-fill fallback is explicit.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4525 Packet Integration

Marker: `{PACKET_MARKER}`  
The PPC4161 packet now has a serious parent-action route rather than only closure language: find a vertical reflection/quotient-even principle, or score its breaking coefficients. Poynting/wave flux remains included as a symmetry-breaking boundary/source coefficient unless no-flux is parent-owned. Next target: `{NEXT_TARGET}`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
