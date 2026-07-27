from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


CHECKPOINT = "3853"
BRANCH = "MTS_R2FR_Y5_RADIAL_CELL_CONSTRAINT_ORIGIN_FROM_MTS_COFRAME_OR_EXPLICIT_CLOSURE_3853"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3853-Y5-R2FR-radial-cell-constraint-origin-from-MTS-coframe-or-explicit-closure.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_01_ROUTE = PCW / "01-motion-load-route-contract.md"
P_02_REDUCTION = PCW / "02-motion-load-local-GR-reduction.md"
P_07_CONSTRAINT = PCW / "07-nonpropagating-reciprocity-constraint.md"
P_08_PHASE = PCW / "08-phase-volume-reciprocity-origin.md"
P_09_HAMILTONIAN = PCW / "09-hamiltonian-radial-cell-derivation.md"
P_10_OBSERVER = PCW / "10-observer-map-symplectic-contract.md"
P_11_CURRENT = PCW / "11-cell-current-origin-attempt.md"

CSV_3852_SIGNATURE = OUT / "P8_Y5_R2FR_3852_PARENT_NEUTRALITY_SIGNATURE_THEOREM.csv"
CSV_3852_ACTION = OUT / "P8_Y5_R2FR_3852_AUXILIARY_CONSTRAINT_ACTION_CANDIDATE.csv"
CSV_3852_PROOF = OUT / "P8_Y5_R2FR_3852_RAB_ZERO_PROOF_STATUS.csv"
CSV_3852_FINITE = OUT / "P8_Y5_R2FR_3852_FINITE_HAIR_REQUIRED_SOURCE_ROW.csv"
CSV_3852_VALIDATION = OUT / "P8_Y5_BRR545_3852_VALIDATION.csv"
CSV_3851_BUDGET = OUT / "P8_Y5_R2FR_3851_RAB_BUDGET_FROM_CASSINI_NEAR_LIMB.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3853_SOURCE_REGISTER.csv",
    "coframe": OUT / "P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv",
    "action": OUT / "P8_Y5_R2FR_3853_COFRAME_CELL_ACTION_CANDIDATE.csv",
    "closure": OUT / "P8_Y5_R2FR_3853_EXPLICIT_CLOSURE_ORIGIN_LEDGER.csv",
    "proof": OUT / "P8_Y5_R2FR_3853_RAB_ZERO_FROM_CELL_LOCK_STATUS.csv",
    "finite_row": OUT / "P8_Y5_R2FR_3853_FINITE_HAIR_FALLBACK_ROW.csv",
    "gates": OUT / "P8_Y5_R2FR_3853_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3853_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3853_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3853_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3853_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3853_0_01_route", P_01_ROUTE, "c^2 = v_space^2 + v_clock^2 + v_load^2"),
    ("SRC3853_1_02_reduction", P_02_REDUCTION, "the lost clock capacity is reciprocally carried as spatial routing"),
    ("SRC3853_2_07_constraint", P_07_CONSTRAINT, "S_constraint = integral lambda_R R_AB"),
    ("SRC3853_3_08_phase", P_08_PHASE, "T sqrt(S) = 1"),
    ("SRC3853_4_09_hamiltonian", P_09_HAMILTONIAN, "J_tr = T sqrt(S)"),
    ("SRC3853_5_10_observer", P_10_OBSERVER, "theta_0 = T c dt"),
    ("SRC3853_6_11_current", P_11_CURRENT, "ordinary cell-current conservation does not close"),
    ("SRC3853_7_3852_signature", CSV_3852_SIGNATURE, "PNS3852_5_current_verdict"),
    ("SRC3853_8_3852_action", CSV_3852_ACTION, "lambda_R ln(T^2 S)=2 lambda_R ln(T sqrt(S))"),
    ("SRC3853_9_3852_proof", CSV_3852_PROOF, "NOT_PROVED_FOR_STRICT_CURRENT_CORPUS"),
    ("SRC3853_10_3852_finite", CSV_3852_FINITE, "6.102178699076298E-11"),
    ("SRC3853_11_3852_validation", CSV_3852_VALIDATION, "PASS"),
    ("SRC3853_12_3851_budget", CSV_3851_BUDGET, "6.102178699076298e-11"),
]

OMEGA_DEF = "Omega_tr=(theta^0/c) wedge theta^1=T*sqrt(S) dt wedge dr"
OMEGA_LOCK = "Omega_tr=Omega_ref=dt wedge dr"
CELL_ZERO = "Omega_tr=Omega_ref => T*sqrt(S)=1 => ln(T^2 S)=0 => R_AB=0"
COFRAME_ACTION = "S_cell=int_U Lambda_J (Omega_tr-Omega_ref)"
REDUCED_ACTION = "S_cell -> int dr lambda_J ln(T*sqrt(S)) = (1/2) int dr lambda_J ln(T^2 S)"
FINITE_HAIR_FORMULA = "B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|)"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def budget_value() -> Decimal:
    for row in read_csv_rows(CSV_3851_BUDGET):
        if row.get("budget_id") == "RBC3851_0_near_limb_scalar_budget":
            return Decimal(row["exact_log_bound"])
    raise RuntimeError("3851 R_AB budget row missing")


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_radial_cell_coframe_origin_or_explicit_closure",
                "claim_use": "nonclaim_derivation_candidate_and_closure_ledger",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coframe_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "derivation_id": "RCD3853_0_observer_coframe",
            "step": "static radial observer coframe",
            "formula": "theta^0=T c dt; theta^1=sqrt(S) dr",
            "source": rel(P_10_OBSERVER),
            "result": "local radial clock and routing units are explicit coframe legs",
            "status": "PASS_FROM_EXISTING_OBSERVER_MAP",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RCD3853_1_radial_cell_two_form",
            "step": "construct radial observer-cell two-form",
            "formula": OMEGA_DEF,
            "source": "theta^0/c and theta^1",
            "result": "the desired scalar cell factor is exactly J_tr=T*sqrt(S)",
            "status": "PASS_EXACT_COFRAME_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RCD3853_2_parent_cell_lock",
            "step": "candidate parent origin",
            "formula": OMEGA_LOCK,
            "source": "motion/time/space radial cell invariance candidate",
            "result": CELL_ZERO,
            "status": "PASS_IF_PARENT_CELL_TWO_FORM_LOCK_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RCD3853_3_relation_to_3852_lambda",
            "step": "coframe action reduces to lambda_R constraint",
            "formula": REDUCED_ACTION,
            "source": rel(CSV_3852_ACTION),
            "result": "3852 lambda_R ln(T^2S) is the scalar radial reduction of a coframe two-form lock",
            "status": "PASS_EXACT_REWRITE_OF_CANDIDATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "derivation_id": "RCD3853_4_rejected_shortcuts",
            "step": "not generic volume, Liouville, null, or current conservation",
            "formula": "generic phase volume and ordinary cell current do not imply Omega_tr=Omega_ref",
            "source": rel(P_09_HAMILTONIAN) + ";" + rel(P_11_CURRENT),
            "result": "the missing premise is specifically parent-fixed radial observer-cell two-form",
            "status": "SHORTCUTS_REJECTED_MISSING_CLAUSE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def action_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "action_id": "CCA3853_0_two_form_cell_lock",
            "candidate_action": COFRAME_ACTION,
            "variation": "delta_Lambda_J S_cell=0 => Omega_tr=Omega_ref",
            "reduced_static_result": CELL_ZERO,
            "forbidden_interpretation": "not Schwarzschild AB=1; not Einstein vacuum equation; not generic determinant/volume preservation",
            "adoption_status": "CANDIDATE_PARENT_COFRAME_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "CCA3853_1_scalar_reduction",
            "candidate_action": REDUCED_ACTION,
            "variation": "delta_lambda_J enforces ln(T*sqrt(S))=0",
            "reduced_static_result": "equivalent to (1/2) lambda_R ln(T^2 S)",
            "forbidden_interpretation": "do not call this derived unless the two-form lock is parent-owned",
            "adoption_status": "EQUIVALENT_TO_3852_AUXILIARY_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def closure_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "ECO3853_0_exact_closure_axiom_if_needed",
            "closure_statement": "The parent MTS radial observer-cell two-form is fixed: (theta^0/c) wedge theta^1 = dt wedge dr on the local exterior branch.",
            "mathematical_effect": CELL_ZERO,
            "why_not_smuggled_if_labelled": "it is stated as a parent closure/selection rule, not advertised as derived from GR or tests",
            "what_would_derivate_it": "a deeper MTS coframe action, gauge redundancy, or topological cell charge proving Omega_tr-Omega_ref=0",
            "current_status": "EXPLICIT_CLOSURE_IF_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "closure_id": "ECO3853_1_finite_hair_fallback",
            "closure_statement": "If no cell lock is adopted, retain finite R_AB hair.",
            "mathematical_effect": FINITE_HAIR_FORMULA,
            "why_not_smuggled_if_labelled": "finite hair is test-facing and must beat Cassini/gamma budget",
            "what_would_derivate_it": "source-backed Pi_R/J_R/boundary rows or parent zero theorem",
            "current_status": "FALLBACK_SEVERE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def proof_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "proof_id": "RZC3853_0_if_cell_lock_signed",
            "premise": "parent signs Omega_tr=Omega_ref as a radial observer-cell two-form constraint",
            "chain": OMEGA_DEF + "; " + OMEGA_LOCK + "; " + CELL_ZERO,
            "result": "R_AB=0 and 3852 no-hair mechanism closes",
            "proof_status": "PROVED_CONDITIONAL_ON_PARENT_CELL_LOCK",
            "claim_allowed": False,
            "reason_nonclaim": "cell lock is candidate parent principle, not yet derived from deeper MTS object language",
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "RZC3853_1_strict_current_corpus",
            "premise": "existing 01-11 sources plus 3852 candidate, without adopting the two-form lock",
            "chain": "observer coframe exists; radial cell identity exists; generic derivations fail",
            "result": "R_AB=0 remains an explicit closure or finite source-bound branch",
            "proof_status": "NOT_STRICT_CURRENT_PROOF",
            "claim_allowed": False,
            "reason_nonclaim": "no source currently proves Omega_tr=Omega_ref",
            "timestamp_utc": timestamp,
        },
    ]


def finite_hair_rows(timestamp: str) -> list[dict[str, object]]:
    budget = budget_value()
    return [
        {
            "fallback_id": "FHF3853_0_no_cell_lock_finite_hair",
            "quantity": "B_RAB",
            "required_bound": f"B_RAB <= {budget} before other gamma residuals",
            "source_formula": FINITE_HAIR_FORMULA,
            "required_inputs": "C_W;Pi_R;Pi_R_ct;JR_L1;Delta_R_boundary;Delta_W;B_other;full_Cassini_kernel",
            "status": "BLOCKED_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3853_0_coframe_identity",
            "gate": "radial cell coframe identity",
            "status": "PASS_EXACT_IDENTITY",
            "claim_allowed": False,
            "reason": "theta^0/c wedge theta^1 gives T sqrt(S) dt wedge dr",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3853_1_parent_cell_lock",
            "gate": "Omega_tr=Omega_ref parent origin",
            "status": "BLOCKED_PARENT_TWO_FORM_LOCK_REQUIRED",
            "claim_allowed": False,
            "reason": "the exact coframe lock is identified but not parent-derived by current sources",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3853_2_no_smuggling",
            "gate": "closure honesty",
            "status": "PASS_EXPLICIT_IF_USED_AS_CLOSURE",
            "claim_allowed": False,
            "reason": "if adopted without deeper proof, it is labelled as a parent closure, not as a derived theorem",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3853_3_finite_fallback",
            "gate": "finite R_AB hair fallback",
            "status": "BLOCKED_VALUES_MISSING_SEVERE_BUDGET",
            "claim_allowed": False,
            "reason": "fallback requires B_RAB below 3851 Cassini pressure and full kernel/gauge rows",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3853_4_local_GR_scope",
            "gate": "full local GR",
            "status": "BLOCKED_BETA_NEWTON_SOURCE_EM_SEPARATE",
            "claim_allowed": False,
            "reason": "R_AB/gamma throat is only one part of the local-GR route",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3853_0",
            "decision": "3852 lambda_R origin can be rewritten as a coframe two-form cell lock",
            "consequence": "the missing theorem is now Omega_tr=Omega_ref, not a vague lambda source",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3853_1",
            "decision": "current corpus still does not derive the two-form lock",
            "consequence": "no strict local-GR claim opens; closure must be labelled if used",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3853_2",
            "decision": "next route should test gauge/topological origin of the cell lock",
            "consequence": "a true observer-splitting gauge redundancy or topological cell charge would make the closure less ad hoc",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3853_0",
            "next_checkpoint": "3854-Y5-R2FR-observer-cell-gauge-or-topological-charge-origin.md",
            "script": "scripts/Y5_R2FR_3854_observer_cell_gauge_or_topological_charge_origin.py",
            "objective": "test whether Omega_tr=Omega_ref follows from observer-splitting gauge redundancy or a topological radial-cell charge; otherwise freeze it as explicit closure and move to beta/source consistency",
            "reason": "3853 sharpened lambda_R origin to a coframe two-form lock, but did not prove the lock from current MTS sources",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_COFRAME_CELL_LOCK_CANDIDATE_OR_EXPLICIT_CLOSURE",
            "claim": "no strict-current R_AB zero, gamma, PPN, Newton, beta, EM, or local-GR claim",
            "result": "lambda_R origin sharpened to parent radial-cell two-form lock; current corpus still needs gauge/topological derivation or explicit closure label",
            "next": "3854 observer-cell gauge/topological origin",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    coframe: list[dict[str, object]],
    action: list[dict[str, object]],
    closure: list[dict[str, object]],
    proof: list[dict[str, object]],
    finite_row: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    budget = budget_value()
    text = f"""# 3853 - Radial Cell Constraint Origin From MTS Coframe Or Explicit Closure

Private checkpoint. This tries to derive the 3852 `lambda_R ln(T^2 S)` constraint from the MTS observer coframe, not merely rename it.

Generated: `{timestamp}`

## Result

The strongest non-GR origin found is a radial observer-cell two-form lock.

From the existing observer coframe:

`theta^0 = T c dt`

`theta^1 = sqrt(S) dr`

construct:

`{OMEGA_DEF}`.

If the parent MTS theory fixes the radial observer-cell two-form:

`{OMEGA_LOCK}`,

then:

`{CELL_ZERO}`.

So the 3852 scalar multiplier is not arbitrary in this route. It is the radial scalar reduction of:

`{COFRAME_ACTION}`,

which reduces in the static branch to:

`{REDUCED_ACTION}`.

This is a real sharpening: the missing object is now a concrete coframe/two-form principle, not a vague `lambda_R` handwave.

But it is not yet a strict-current proof. Current sources define the coframe and show that the lock would work; they do not yet prove why the parent MTS object language must impose `Omega_tr=Omega_ref`. Therefore this checkpoint keeps the route nonclaim and writes the exact closure axiom that would be needed if the gauge/topological derivation fails.

Finite-hair fallback remains severe:

`B_RAB <= {budget}` before other gamma residuals.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Coframe Derivation

{markdown_table(coframe, ["derivation_id", "step", "formula", "status", "result"])}

## Coframe Cell Action Candidate

{markdown_table(action, ["action_id", "candidate_action", "variation", "reduced_static_result", "adoption_status"])}

## Explicit Closure Origin Ledger

{markdown_table(closure, ["closure_id", "closure_statement", "mathematical_effect", "current_status"])}

## R_AB Zero From Cell Lock Status

{markdown_table(proof, ["proof_id", "premise", "result", "proof_status", "reason_nonclaim"])}

## Finite Hair Fallback

{markdown_table(finite_row, ["fallback_id", "quantity", "required_bound", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3853 moves the missing theorem one level deeper and makes it more respectable: `lambda_R ln(T^2S)` can be read as a coframe two-form cell lock, `(theta^0/c) wedge theta^1 = dt wedge dr`. That is much less arbitrary than raw `AB=1`, but it is still a parent-cell closure unless 3854 can derive it from observer-splitting gauge redundancy or a topological cell charge.

Next target: `3854-Y5-R2FR-observer-cell-gauge-or-topological-charge-origin.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    budget = budget_value()
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3852", "Current State After 3853", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3853 at ")
    )
    paragraph = (
        "`3853` sharpens the origin of the 3852 auxiliary constraint from a scalar `lambda_R ln(T^2S)` into a concrete coframe two-form lock. "
        "With `theta^0=T c dt` and `theta^1=sqrt(S)dr`, the radial observer-cell form is `Omega_tr=(theta^0/c) wedge theta^1=T sqrt(S) dt wedge dr`. "
        "If the parent MTS theory signs `Omega_tr=Omega_ref=dt wedge dr`, then `T sqrt(S)=1`, `ln(T^2S)=0`, and `R_AB=0`. "
        "This gives a cleaner parent-action candidate `S_cell=int Lambda_J(Omega_tr-Omega_ref)`, whose static scalar reduction is the 3852 multiplier term. "
        f"Current sources do not yet derive the two-form lock, so it remains nonclaim/explicit closure unless a gauge or topological origin is found; finite hair still faces `B_RAB <= {budget}` before other gamma residuals.\n\n"
    )
    anchor = "`3852` constructs"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3853-Y5-R2FR-radial-cell-constraint-origin-from-MTS-coframe-or-explicit-closure.md`

Target: derive `lambda_R ln(T^2 S)` from motion/time/space coframe or radial observer-cell invariance; if this cannot be derived, mark it as an explicit parent closure rather than a hidden theorem.

This is the best next move because 3852 closes the no-hair mechanism inside a candidate action, but the parent origin of the constraint is now the real missing derivation."""
    new_gate = """`3854-Y5-R2FR-observer-cell-gauge-or-topological-charge-origin.md`

Target: test whether `Omega_tr=Omega_ref` follows from observer-splitting gauge redundancy or a topological radial-cell charge; otherwise freeze it as explicit closure and move to beta/source consistency.

This is the best next move because 3853 sharpened lambda_R origin to a coframe two-form lock, but did not prove the lock from current MTS sources."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3853_COFRAME_CELL_ACTION_CANDIDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3853_EXPLICIT_CLOSURE_ORIGIN_LEDGER.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3853_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3853_RADIAL_CELL_COFRAME_DERIVATION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3853 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    coframe: list[dict[str, object]],
    action: list[dict[str, object]],
    closure: list[dict[str, object]],
    proof: list[dict[str, object]],
    finite_row: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    budget = budget_value()
    all_text = " ".join(str(row) for row in coframe + action + closure + proof + finite_row + gates)
    add(
        "VAL3853_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add("VAL3853_1_coframe_identity", "Omega_tr identity is present", OMEGA_DEF in all_text, "coframe identity present")
    add("VAL3853_2_cell_lock", "Omega_tr lock implies R_AB zero", CELL_ZERO in all_text, "cell lock chain present")
    add("VAL3853_3_action_candidate", "coframe action candidate is present", COFRAME_ACTION in all_text and REDUCED_ACTION in all_text, "two-form action and scalar reduction present")
    add("VAL3853_4_closure_label", "explicit closure ledger is present", "EXPLICIT_CLOSURE_IF_NOT_PARENT_DERIVED" in all_text, "closure label retained")
    add("VAL3853_5_nonclaim", "all 3853 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in coframe + action + closure + proof + finite_row + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3853_6_budget_propagated", "finite hair budget is propagated", str(budget) in all_text and budget < Decimal("1e-9"), str(budget))
    add("VAL3853_7_next", "next target is 3854", DOC_PATH.exists() and "3854-Y5-R2FR-observer-cell-gauge-or-topological-charge-origin" in read_text(DOC_PATH), "3854 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3853_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3853_9_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "coframe two-form cell lock" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3853*", "P8_Y5_BRR545_3853*", "*Y5_R2FR_3853*", "3853-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3853_10_formalization_clean", "formalization-workbench has no generated 3853 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3853 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3853_11_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    coframe = coframe_rows(timestamp)
    action = action_rows(timestamp)
    closure = closure_rows(timestamp)
    proof = proof_rows(timestamp)
    finite_row = finite_hair_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["coframe"], coframe)
    write_csv(OUTPUTS["action"], action)
    write_csv(OUTPUTS["closure"], closure)
    write_csv(OUTPUTS["proof"], proof)
    write_csv(OUTPUTS["finite_row"], finite_row)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, coframe, action, closure, proof, finite_row, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, coframe, action, closure, proof, finite_row, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_COFRAME_CELL_LOCK_CANDIDATE_OR_EXPLICIT_CLOSURE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
