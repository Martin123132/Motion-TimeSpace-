from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path


CHECKPOINT = "3852"
BRANCH = "MTS_R2FR_Y5_PARENT_NEUTRALITY_SIGNATURE_FOR_RAB_ZERO_OR_FINITE_HAIR_SOURCE_ROW_3852"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_04_CONTRACT = PCW / "04-vacuum-reciprocity-action-contract.md"
P_05_ATTEMPT = PCW / "05-reciprocity-theorem-attempt.md"
P_06_NEUTRALITY = PCW / "06-reciprocal-charge-source-neutrality.md"
P_07_CONSTRAINT = PCW / "07-nonpropagating-reciprocity-constraint.md"
P_08_PHASE = PCW / "08-phase-volume-reciprocity-origin.md"
P_09_HAMILTONIAN = PCW / "09-hamiltonian-radial-cell-derivation.md"

CSV_3849_NEUTRALITY = OUT / "P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv"
CSV_3849_HAIR = OUT / "P8_Y5_R2FR_3849_RAB_HAIR_SOURCE_ROW.csv"
CSV_3851_BUDGET = OUT / "P8_Y5_R2FR_3851_RAB_BUDGET_FROM_CASSINI_NEAR_LIMB.csv"
CSV_3851_DECISION = OUT / "P8_Y5_R2FR_3851_NEUTRALITY_VS_FINITE_HAIR_DECISION.csv"
CSV_3851_VALIDATION = OUT / "P8_Y5_BRR545_3851_VALIDATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3852_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_R2FR_3852_PARENT_NEUTRALITY_SIGNATURE_THEOREM.csv",
    "action": OUT / "P8_Y5_R2FR_3852_AUXILIARY_CONSTRAINT_ACTION_CANDIDATE.csv",
    "proof": OUT / "P8_Y5_R2FR_3852_RAB_ZERO_PROOF_STATUS.csv",
    "finite_row": OUT / "P8_Y5_R2FR_3852_FINITE_HAIR_REQUIRED_SOURCE_ROW.csv",
    "gates": OUT / "P8_Y5_R2FR_3852_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3852_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3852_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3852_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3852_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3852_0_04_contract", P_04_CONTRACT, "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R"),
    ("SRC3852_1_05_attempt", P_05_ATTEMPT, "conserved reciprocal charge"),
    ("SRC3852_2_06_neutrality", P_06_NEUTRALITY, "Q_R = -Pi_R"),
    ("SRC3852_3_07_constraint", P_07_CONSTRAINT, "S_constraint = integral lambda_R R_AB"),
    ("SRC3852_4_08_phase", P_08_PHASE, "T sqrt(S) = 1"),
    ("SRC3852_5_09_hamiltonian", P_09_HAMILTONIAN, "J_tr = T sqrt(S)"),
    ("SRC3852_6_3849_neutrality", CSV_3849_NEUTRALITY, "RNT3849_2_zero_chain"),
    ("SRC3852_7_3849_hair", CSV_3849_HAIR, "R_AB_hair_envelope"),
    ("SRC3852_8_3851_budget", CSV_3851_BUDGET, "6.102178699076298e-11"),
    ("SRC3852_9_3851_decision", CSV_3851_DECISION, "UNSIGNED_BUT_BEST_ROUTE"),
    ("SRC3852_10_3851_validation", CSV_3851_VALIDATION, "PASS"),
]

CONSTRAINT_ACTION = "S_R_aux=int_U dmu_r lambda_R ln(T^2 S)"
ZERO_VARIATION = "delta_{lambda_R} S_R_aux=0 => ln(T^2 S)=0 => R_AB=0 => T^2 S=1"
REACTION_EQUATION = "delta_{R_AB} S_parent=0 => lambda_R= - delta S_rest/delta R_AB, algebraic reaction not exterior hair"
FINITE_HAIR_FORMULA = "C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|) <= B_RAB_budget"


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
                "role": "input_for_parent_neutrality_signature_or_finite_hair_source_row",
                "claim_use": "nonclaim_action_signature_and_budget_contract",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def signature_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "PNS3852_0_variables",
            "claim_piece": "parent variables",
            "condition": "use independent clock/routing variables T,S and auxiliary multiplier lambda_R with R_AB=ln(T^2 S)",
            "derivation": "make reciprocal strain an auxiliary constrained direction, not a propagating exterior scalar",
            "result": "R_AB is varied through a multiplier constraint rather than a kinetic hair equation",
            "status": "PASS_SIGNATURE_COMPONENT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PNS3852_1_constraint_variation",
            "claim_piece": "R_AB zero",
            "condition": CONSTRAINT_ACTION,
            "derivation": ZERO_VARIATION,
            "result": "reciprocal routing T^2 S=1 follows inside this parent signature",
            "status": "PASS_EXACT_WITHIN_CANDIDATE_ACTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PNS3852_2_no_kinetic_charge",
            "claim_piece": "no Q_R hair",
            "condition": "no exterior term 0.5 W_R (partial_r R_AB)^2 and no normal-derivative boundary functional of R_AB",
            "derivation": "without a radial derivative term, there is no conserved W_R R_AB' charge and no Neumann hair channel",
            "result": "Q_R is not generated as a physical exterior integration constant",
            "status": "PASS_EXACT_WITHIN_CANDIDATE_ACTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PNS3852_3_source_reaction",
            "claim_piece": "source stress does not become J_R hair",
            "condition": "ordinary/source/readout terms may depend algebraically on R_AB only after the multiplier is present",
            "derivation": REACTION_EQUATION,
            "result": "source response is absorbed into lambda_R; it does not source a differential R_AB profile",
            "status": "PASS_REACTION_STRESS_MECHANISM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PNS3852_4_boundary_silence",
            "claim_piece": "Pi_R zero in hair sense",
            "condition": "boundary/reference terms are fixed before readout and contain no normal derivative of R_AB",
            "derivation": "R_AB is fixed by delta_lambda_R before boundary stationarity; algebraic boundary reactions shift lambda_R or fixed boundary stress, not Q_R",
            "result": "Pi_R cannot act as an exterior reciprocal momentum in the candidate signature",
            "status": "PASS_CONDITIONAL_BOUNDARY_MECHANISM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PNS3852_5_current_verdict",
            "claim_piece": "current MTS adoption",
            "condition": "parent must justify lambda_R ln(T^2 S) from motion/time/space radial cell rather than inserting it",
            "derivation": "07-09 motivate and sharpen the radial-cell route but do not derive its deeper origin",
            "result": "candidate mechanism closes the local hair problem if adopted; strict corpus still needs parent-origin derivation",
            "status": "CANDIDATE_SIGNATURE_NOT_STRICT_CURRENT_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def action_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "action_id": "ACA3852_0_minimal_auxiliary_constraint",
            "action_piece": CONSTRAINT_ACTION,
            "variation": ZERO_VARIATION,
            "forbidden_terms": "0.5*W_R*(partial_r R_AB)^2; J_R*R_AB as independent exterior source; boundary_normal_RAB_momentum",
            "allowed_terms": "ordinary matter/source stress; EM/binding stress; clock-load source terms; algebraic reaction into lambda_R",
            "derived_zero": "R_AB=0",
            "adoption_status": "CANDIDATE_PARENT_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "action_id": "ACA3852_1_phase_cell_reading",
            "action_piece": "lambda_R ln(T^2 S)=2 lambda_R ln(T sqrt(S))",
            "variation": "delta_lambda_R enforces radial t-r cell J_tr=T sqrt(S)=1",
            "forbidden_terms": "generic four-volume claim; generic Liouville claim; null-speed-only claim",
            "allowed_terms": "specific radial clock-routing cell principle",
            "derived_zero": "T sqrt(S)=1",
            "adoption_status": "MOTIVATED_BY_08_09_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def proof_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "proof_id": "RZP3852_0_with_candidate_signature",
            "route": "auxiliary constraint parent action",
            "premises": "ACA3852_0 adopted; no kinetic R_AB; no derivative boundary R_AB momentum",
            "result": "Pi_R=J_R=Pi_R_ct=Delta_R_boundary=Delta_W=0 as exterior hair sources; R_AB=0 by constraint",
            "proof_status": "PROVED_INSIDE_CANDIDATE_SIGNATURE",
            "claim_allowed": False,
            "reason_nonclaim": "candidate action is not yet derived from deeper MTS parent principle",
            "timestamp_utc": timestamp,
        },
        {
            "proof_id": "RZP3852_1_strict_current_corpus",
            "route": "existing corpus without adopting auxiliary constraint",
            "premises": "04-06 kinetic/hair route plus 07-09 motivation only",
            "result": "R_AB zero remains unsigned",
            "proof_status": "NOT_PROVED_FOR_STRICT_CURRENT_CORPUS",
            "claim_allowed": False,
            "reason_nonclaim": "radial-cell constraint origin is still open",
            "timestamp_utc": timestamp,
        },
    ]


def finite_hair_rows(timestamp: str) -> list[dict[str, object]]:
    budget = budget_value()
    return [
        {
            "row_id": "FHR3852_0_required_finite_hair_source_row",
            "quantity": "R_AB_hair_envelope",
            "source_formula": "B_RAB <= C_W*(|Pi_R|+|Pi_R_ct|+int|J_R|dr+|Delta_R_boundary|+|Delta_W|)",
            "required_for_Cassini_near_limb_zero_other": f"B_RAB <= {budget}",
            "strict_acceptance_formula": FINITE_HAIR_FORMULA,
            "required_columns": "system_id;C_W;Pi_R;Pi_R_ct;JR_L1;Delta_R_boundary;Delta_W;B_other;B_RAB;source_path;equation_ref;valid_for_claim",
            "current_status": "VALUES_MISSING_OR_PARENT_ZERO_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FHR3852_1_other_residual_guard",
            "quantity": "remaining_gamma_budget",
            "source_formula": "B_other=B_areal_to_PPN+B_domain+B_norm+B_higher_order+kernel_error",
            "required_for_Cassini_near_limb_zero_other": "B_other must be source-backed and theta_gamma>B_other",
            "strict_acceptance_formula": "B_RAB <= ln(1+2*phi_floor*T2_floor*(theta_gamma-B_other))",
            "required_columns": "B_areal_to_PPN;B_domain;B_norm;B_higher_order;kernel_error;theta_gamma;source_path;valid_for_claim",
            "current_status": "VALUES_MISSING_FULL_KERNEL_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3852_0_candidate_zero_mechanism",
            "gate": "auxiliary constraint kills R_AB hair",
            "status": "PASS_PROVED_WITHIN_CANDIDATE_ACTION",
            "claim_allowed": False,
            "reason": "delta lambda_R gives R_AB=0 and no kinetic term creates Q_R",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3852_1_parent_origin",
            "gate": "derive lambda_R ln(T^2 S) from MTS parent principle",
            "status": "BLOCKED_RADIAL_CELL_PARENT_ORIGIN_REQUIRED",
            "claim_allowed": False,
            "reason": "07-09 motivate the radial t-r cell but do not derive it from the deeper parent corpus",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3852_2_finite_hair_fallback",
            "gate": "finite hair source row meets Cassini pressure",
            "status": "BLOCKED_VALUES_MISSING_BUDGET_SEVERE",
            "claim_allowed": False,
            "reason": "B_RAB must be below the 3851 budget after other residuals; no source-backed row exists",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3852_3_no_smuggling_guard",
            "gate": "not a hidden Schwarzschild/GR import",
            "status": "PASS_SCOPE_GUARD_NONCLAIM",
            "claim_allowed": False,
            "reason": "constraint is labelled candidate until radial-cell origin is derived",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3852_4_local_GR_scope",
            "gate": "full local GR route",
            "status": "BLOCKED_GAMMA_COMPONENT_ONLY",
            "claim_allowed": False,
            "reason": "Newton source normalization, beta, full gamma no-slip/readout, and EM/source coupling remain open",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3852_0",
            "decision": "the clean technical mechanism is auxiliary-constrained R_AB, not kinetic R_AB hair",
            "consequence": "the work should now attack the origin of the radial t-r cell constraint",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3852_1",
            "decision": "finite hair remains a fallback only",
            "consequence": "the fallback must source B_RAB at or below the 6.1e-11 near-limb pressure before other residuals",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3852_2",
            "decision": "no public or strict-current local-GR claim opens from this checkpoint",
            "consequence": "candidate action is useful but still needs parent-origin derivation",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3852_0",
            "next_checkpoint": "3853-Y5-R2FR-radial-cell-constraint-origin-from-MTS-coframe-or-explicit-closure.md",
            "script": "scripts/Y5_R2FR_3853_radial_cell_constraint_origin_from_MTS_coframe_or_explicit_closure.py",
            "objective": "derive lambda_R ln(T^2 S) from motion/time/space coframe or radial observer-cell invariance; if this cannot be derived, mark it as an explicit parent closure rather than a hidden theorem",
            "reason": "3852 closes the no-hair mechanism inside a candidate action, but the parent origin of the constraint is now the real missing derivation",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_PARENT_NEUTRALITY_SIGNATURE_CANDIDATE",
            "claim": "no strict-current R_AB zero, gamma, PPN, Newton, beta, or local-GR claim",
            "result": "auxiliary constraint action proves R_AB=0 inside candidate signature; parent origin remains open",
            "next": "3853 radial-cell constraint origin or explicit closure",
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
    signature: list[dict[str, object]],
    action: list[dict[str, object]],
    proof: list[dict[str, object]],
    finite_row: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    budget = budget_value()
    text = f"""# 3852 - Parent Neutrality Signature For R_AB Zero Or Finite Hair Source Row

Private checkpoint. This attempts the derivation route first: build the exact parent-action signature that would make `R_AB=0` structural rather than a tuned finite hair.

Generated: `{timestamp}`

## Result

The clean technical mechanism is an auxiliary constraint, not kinetic reciprocal hair:

`{CONSTRAINT_ACTION}`.

Its multiplier variation gives:

`{ZERO_VARIATION}`.

The source variation becomes:

`{REACTION_EQUATION}`.

That is the important distinction. Matter/source stress can react into `lambda_R`, but it does not become a differential exterior `J_R` that generates `Q_R` hair. With no `partial_r R_AB` kinetic term and no normal-derivative boundary functional, there is no conserved `Q_R=W_R R_AB'` channel.

So 3852 does not merely say "missing". It constructs the candidate parent signature that would close the hair problem. The remaining missing derivation is sharper: why must the parent MTS action contain `lambda_R ln(T^2 S)`? The old 07-09 route says this is equivalent to preserving the radial `t-r` observer cell `T sqrt(S)=1`, but that origin is still not derived from deeper MTS variables.

If this parent signature is not adopted, the finite-hair fallback is severe:

`{FINITE_HAIR_FORMULA}`

with the 3851 near-limb budget:

`B_RAB_budget = {budget}`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Parent Neutrality Signature

{markdown_table(signature, ["theorem_id", "claim_piece", "condition", "status", "result"])}

## Auxiliary Constraint Action

{markdown_table(action, ["action_id", "action_piece", "variation", "derived_zero", "adoption_status"])}

## R_AB Zero Proof Status

{markdown_table(proof, ["proof_id", "route", "result", "proof_status", "reason_nonclaim"])}

## Finite Hair Required Source Row

{markdown_table(finite_row, ["row_id", "quantity", "required_for_Cassini_near_limb_zero_other", "current_status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3852 gives us the real fork. Either MTS derives the radial-cell auxiliary constraint, and `R_AB=0` is structural, or finite reciprocal hair must be sourced below about `6.1e-11` before other gamma residuals. The next best step is not another broad audit: derive the origin of `lambda_R ln(T^2 S)` from motion/time/space coframe structure, or explicitly demote it to a parent closure.

Next target: `3853-Y5-R2FR-radial-cell-constraint-origin-from-MTS-coframe-or-explicit-closure.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    budget = budget_value()
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3851", "Current State After 3852", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3852 at ")
    )
    paragraph = (
        "`3852` constructs the clean parent-neutrality mechanism for the reciprocal branch: make `R_AB=ln(T^2S)` an auxiliary constrained direction with `S_R_aux=int lambda_R ln(T^2S)` and no exterior `0.5 W_R(R_AB')^2` kinetic term. "
        "Then `delta_lambda_R` gives `R_AB=0`, while source stress reacts algebraically through `lambda_R=-delta S_rest/delta R_AB` instead of generating a differential `J_R` hair profile or conserved `Q_R`. "
        f"This proves no-hair inside the candidate signature but is not a strict-current claim because the deeper parent origin of `lambda_R ln(T^2S)`/radial `T sqrt(S)=1` remains open. "
        f"If the candidate is not adopted, the finite-hair row must satisfy the 3851 budget `B_RAB <= {budget}` before other gamma residuals.\n\n"
    )
    anchor = "`3851` fills"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row.md`

Target: derive the parent action/signature that sets `Pi_R=J_R=0` for the reciprocal exterior branch, or source a finite `B_RAB` row tight enough for the 3851 Cassini pressure budget.

This is the best next move because 3851 makes the finite-hair route quantitatively severe; no-hair neutrality is the clean path."""
    new_gate = """`3853-Y5-R2FR-radial-cell-constraint-origin-from-MTS-coframe-or-explicit-closure.md`

Target: derive `lambda_R ln(T^2 S)` from motion/time/space coframe or radial observer-cell invariance; if this cannot be derived, mark it as an explicit parent closure rather than a hidden theorem.

This is the best next move because 3852 closes the no-hair mechanism inside a candidate action, but the parent origin of the constraint is now the real missing derivation."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3852_PARENT_NEUTRALITY_SIGNATURE_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3852_AUXILIARY_CONSTRAINT_ACTION_CANDIDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3852_FINITE_HAIR_REQUIRED_SOURCE_ROW.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3852_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3852_PARENT_NEUTRALITY_SIGNATURE_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3852 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    signature: list[dict[str, object]],
    action: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in signature + action + proof + finite_row + gates)
    budget = budget_value()
    add(
        "VAL3852_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add("VAL3852_1_constraint_action", "auxiliary constraint action is present", CONSTRAINT_ACTION in all_text, "constraint action present")
    add("VAL3852_2_zero_variation", "delta lambda_R zero proof is present", "R_AB=0 => T^2 S=1" in all_text, "zero variation present")
    add("VAL3852_3_no_kinetic_charge", "no kinetic Q_R hair route is explicitly banned", "0.5*W_R*(partial_r R_AB)^2" in all_text and "Q_R" in all_text, "kinetic hair banned")
    add("VAL3852_4_reaction_stress", "source stress routed into lambda_R", "algebraic reaction" in all_text and "lambda_R" in all_text, "reaction stress mechanism present")
    add("VAL3852_5_finite_budget", "3851 finite hair budget is propagated", str(budget) in all_text and budget < Decimal("1e-9"), str(budget))
    add("VAL3852_6_nonclaim", "all 3852 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in signature + action + proof + finite_row + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3852_7_parent_origin_blocked", "parent origin remains blocked", "RADIAL_CELL_PARENT_ORIGIN_REQUIRED" in all_text and "CANDIDATE_SIGNATURE_NOT_STRICT_CURRENT_CLAIM" in all_text, "origin blocker retained")
    add("VAL3852_8_next", "next target is 3853", DOC_PATH.exists() and "3853-Y5-R2FR-radial-cell-constraint-origin-from-MTS-coframe-or-explicit-closure" in read_text(DOC_PATH), "3853 target visible")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3852_9_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3852_10_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "real fork" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3852*", "P8_Y5_BRR545_3852*", "*Y5_R2FR_3852*", "3852-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3852_11_formalization_clean", "formalization-workbench has no generated 3852 project files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3852 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3852_12_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    signature = signature_rows(timestamp)
    action = action_rows(timestamp)
    proof = proof_rows(timestamp)
    finite_row = finite_hair_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["signature"], signature)
    write_csv(OUTPUTS["action"], action)
    write_csv(OUTPUTS["proof"], proof)
    write_csv(OUTPUTS["finite_row"], finite_row)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, signature, action, proof, finite_row, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, signature, action, proof, finite_row, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_PARENT_NEUTRALITY_SIGNATURE_CANDIDATE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
