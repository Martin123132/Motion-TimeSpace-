from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3719"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_BATH_NORMALIZATION_AND_Z_PARITY_PROOF_3719"
DOC = ROOT / "3719-Y5-R2FR-parent-bath-normalization-and-z-parity-proof.md"

DOC_3718 = ROOT / "3718-Y5-R2FR-Fisher-fibre-gap-input-owner-Theta-IH-corrections.md"
NEXT_3718 = RESIDUALS / "P8_Y5_R2FR_3718_NEXT_TARGET.csv"
GAP_3718 = RESIDUALS / "P8_Y5_R2FR_3718_GAP_LAW_ROWS.csv"
OWNER_3718 = RESIDUALS / "P8_Y5_R2FR_3718_OWNER_CLAUSE_ROWS.csv"
CORR_3718 = RESIDUALS / "P8_Y5_R2FR_3718_CORRECTION_BUDGET_ROWS.csv"
FISHER_3717 = RESIDUALS / "P8_Y5_R2FR_3717_FISHER_KL_CORE_ROWS.csv"
DOC_3717 = ROOT / "3717-Y5-R2FR-fibre-normal-form-F1-zero-and-BQK-mixed-Hessian-owner.md"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(stamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": stamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(stamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3718", DOC_3718, "Xi_H:=Theta_min*iota_H-R_M_loss", "gap law handoff"),
        ("next_3718", NEXT_3718, "bath family, measure normalization", "3718 next target"),
        ("gap_3718", GAP_3718, "lambda_min(M_K,total) >= Theta_min*iota_H - R_M_loss", "gap inequality"),
        ("owner_3718", OWNER_3718, "Theta_H(q)>0", "owner clauses"),
        ("corr_3718", CORR_3718, "z -> -z", "parity route row"),
        ("fisher_3717", FISHER_3717, "p_z(xi|X_B,q)=p_0", "Fisher bath family"),
        ("doc_3717", DOC_3717, "F1_BQK_REDUCED_TO_ZERO_SECTION_FAMILY_AND_FISHER_KL_CORE_NONCLAIM", "zero-section family"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(stamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def bath_normalization_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "BATH3719_0_parent_bath_action",
            "A_B(q,z,xi)",
            "parent bath action/free-energy density for unresolved variables xi at fixed observed q and fibre z",
            "MISSING_PARENT_ACTION_TERM",
        ),
        (
            "BATH3719_1_gibbs_family",
            "p_z(xi|q)=exp[-A_B(q,z,xi)/Theta_H(q)]/Z(q,z)",
            "normalised parent-owned bath family; this is the concrete owner route for p_z",
            "DERIVED_TEMPLATE_NEEDS_PARENT_A_B_THETA",
        ),
        (
            "BATH3719_2_partition_function",
            "Z(q,z)=integral exp[-A_B(q,z,xi)/Theta_H(q)] dmu_H(xi;q)",
            "fixes normalization, measure, and the no-free-rescaling problem",
            "DERIVED_TEMPLATE_NEEDS_MU_H",
        ),
        (
            "BATH3719_3_normalization",
            "integral p_z(xi|q) dmu_H(xi;q)=1",
            "normalization implies the score has zero mean at z=0",
            "DERIVED_IF_MEASURE_OWNED",
        ),
        (
            "BATH3719_4_free_energy",
            "F_B(q,z)=-Theta_H(q) log Z(q,z)",
            "parent bath contribution whose Hessian supplies the Fisher gap",
            "DERIVED_TEMPLATE_NEEDS_THETA_UNITS",
        ),
    ]
    return [
        {
            **base(stamp),
            "bath_id": bath_id,
            "object": object_name,
            "definition": definition,
            "status": status,
            "claim_allowed": False,
        }
        for bath_id, object_name, definition, status in entries
    ]


def parity_proof_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "PAR3719_0_involution",
            "R_z:(z,xi)->(-z,R_xi xi), R_z^2=1",
            "parent fibre-reflection involution over the local q patch U",
            "MISSING_PARENT_INVARIANCE_MAP",
        ),
        (
            "PAR3719_1_action_evenness",
            "A_B(q,z,xi)=A_B(q,-z,R_xi xi)",
            "bath action is even under fibre reflection",
            "MISSING_PARENT_PARITY_SIGNATURE",
        ),
        (
            "PAR3719_2_measure_invariance",
            "dmu_H(xi;q)=dmu_H(R_xi xi;q)",
            "measure does not break the z parity",
            "MISSING_MEASURE_INVARIANCE",
        ),
        (
            "PAR3719_3_partition_evenness",
            "Z(q,z)=Z(q,-z)",
            "change variables xi->R_xi xi in the partition integral",
            "DERIVED_IF_PARITY_AND_MEASURE_HOLD",
        ),
        (
            "PAR3719_4_free_energy_evenness",
            "F_B(q,z)=F_B(q,-z)",
            "free energy inherits fibre evenness",
            "DERIVED_IF_Z_EVEN",
        ),
        (
            "PAR3719_5_force_zero",
            "partial_z F_B(q,z)|_{z=0}=0 for every q in U",
            "zero-section family is now derived from parity, not assumed",
            "DERIVED_EXACT_IF_PARENT_PARITY_SIGNED",
        ),
        (
            "PAR3719_6_mixed_zero",
            "partial_q partial_z F_B(q,z)|_{z=0}=partial_q 0=0",
            "B_QK core and odd correction mixed leakage vanish over U",
            "DERIVED_EXACT_IF_PARENT_PARITY_SIGNED",
        ),
    ]
    return [
        {
            **base(stamp),
            "parity_id": parity_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for parity_id, formula, meaning, status in entries
    ]


def fisher_identifiability_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "ID3719_0_score",
            "Y_A=partial_A log p_z|_{z=0}",
            "score variables generated by fibre displacement",
            "DERIVED_FROM_NORMALIZED_BATH",
        ),
        (
            "ID3719_1_score_mean",
            "E_0[Y_A]=0",
            "follows from differentiating integral p_z dmu=1",
            "DERIVED_IF_MEASURE_OWNED",
        ),
        (
            "ID3719_2_fisher_matrix",
            "I_AB=E_0[Y_A Y_B]",
            "positive semidefinite Fisher matrix",
            "DERIVED_IF_BATH_OWNED",
        ),
        (
            "ID3719_3_identifiability_floor",
            "a^A I_AB a^B=0 iff a^A Y_A=0 almost surely",
            "strict gap needs no nonzero fibre direction invisible to the bath",
            "MISSING_IDENTIFIABILITY_PROOF",
        ),
        (
            "ID3719_4_positive_floor",
            "iota_H:=inf_{q in U} lambda_min(I_H(q)) > 0",
            "finite local patch lower bound needed for Xi_H",
            "MISSING_LOCAL_EIGENVALUE_SOURCE",
        ),
    ]
    return [
        {
            **base(stamp),
            "ident_id": ident_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for ident_id, formula, meaning, status in entries
    ]


def theta_and_boundary_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "TB3719_0_theta_origin",
            "Theta_H(q)",
            "must be the parent action/temperature/coarse-grain scale appearing in exp[-A_B/Theta_H], not a fit knob inserted after the fact",
            "MISSING_PARENT_SCALE_OR_UNITS",
        ),
        (
            "TB3719_1_unit_map",
            "U_H: Hessian(F_B)->m^-2 operator",
            "same-basis unit map required before Xi_H can be compared to R10/PPN/clock/orbital bounds",
            "MISSING_UNIT_MAP",
        ),
        (
            "TB3719_2_boundary_parity",
            "S_boundary(q,z)=S_boundary(q,-z)",
            "boundary terms must share fibre parity or be explicitly bounded",
            "MISSING_BOUNDARY_PARITY",
        ),
        (
            "TB3719_3_odd_loss_zero",
            "R_odd=0 under parent fibre parity",
            "would collapse F_loss and QK_loss to boundary-only or zero",
            "CONDITIONAL_EXACT_ROUTE",
        ),
        (
            "TB3719_4_failure_fallback",
            "F_loss,QK_loss,R_M_loss remain finite nonclaim coefficients",
            "if any parity, scale, or boundary clause is unsigned, the local branch remains bounded not claimed",
            "NONCLAIM_FALLBACK",
        ),
    ]
    return [
        {
            **base(stamp),
            "theta_boundary_id": theta_boundary_id,
            "quantity": quantity,
            "clause": clause,
            "status": status,
            "claim_allowed": False,
        }
        for theta_boundary_id, quantity, clause, status in entries
    ]


def decision_rows(stamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "DEC3719_0_route",
            "PARENT_GIBBS_BATH_PLUS_FIBRE_PARITY_ROUTE_SELECTED",
            "This is the least hand-wavy way to own p_z, Theta_H, I_H, F_1=0, and B_QK=0 from one mechanism.",
        ),
        (
            "DEC3719_1_no_point_axiom",
            "ZERO_SECTION_FAMILY_DERIVED_IF_PARITY_HOLDS",
            "The force zero is generated over an open q patch by evenness, not imposed at one point.",
        ),
        (
            "DEC3719_2_gap",
            "STRICT_GAP_REQUIRES_IDENTIFIABILITY",
            "The Fisher gap is real only if every active fibre direction changes the bath distribution.",
        ),
        (
            "DEC3719_3_next",
            "ADVANCE_TO_CORPUS_HUNT_FOR_PARENT_A_B_THETA_MU_PARITY",
            "Next target should search the corpus for the actual parent action/measure/parity clauses instead of inventing them.",
        ),
    ]
    return [
        {
            **base(stamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in entries
    ]


def claim_gate_rows(stamp: str) -> list[dict[str, object]]:
    gates = [
        ("CG3719_0_parent_action", "BLOCKED", "A_B(q,z,xi) is present in the parent action with units"),
        ("CG3719_1_measure", "BLOCKED", "mu_H and Z(q,z) are parent-owned and normalized"),
        ("CG3719_2_theta", "BLOCKED", "Theta_H is parent scale with unit map U_H"),
        ("CG3719_3_parity", "BLOCKED", "R_z fibre involution and measure/action invariance are signed"),
        ("CG3719_4_identifiability", "BLOCKED", "I_H has positive lower eigenvalue on local patch U"),
        ("CG3719_5_boundary", "BLOCKED", "boundary terms are parity-even or bounded"),
        ("CG3719_6_local_claim", "BLOCKED", "local R10/PPN/clock/orbital claim allowed"),
    ]
    return [
        {
            **base(stamp),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(stamp: str) -> list[dict[str, object]]:
    return [{
        **base(stamp),
        "status_id": "STATUS3719_0",
        "status": "MECHANISM_CONSTRUCTED_NOT_PARENT_SIGNED",
        "summary": "3719 constructs the concrete route: a normalized parent Gibbs bath plus a fibre-reflection parity gives p_z, Fisher curvature, F_1=0, B_QK=0, and a possible positive gap if identifiability and Theta_H/unit map are owned.",
        "claim_allowed": False,
    }]


def next_target_rows(stamp: str) -> list[dict[str, object]]:
    return [{
        **base(stamp),
        "next_id": "NEXT3719_0",
        "target_doc": "3720-Y5-R2FR-corpus-hunt-parent-bath-scale-parity-clauses.md",
        "target_script": "scripts/Y5_R2FR_3720_corpus_hunt_parent_bath_scale_parity_clauses.py",
        "objective": "search post-checkpoint and source-intake text for parent action, bath measure, Theta_H scale, fibre parity, and boundary silence clauses that can sign the 3719 mechanism",
        "success_gate": "real source paths either support the Gibbs/parity route or force a clean demotion to finite nonclaim coefficient rows",
        "claim_allowed": False,
    }]


def validation_rows(stamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_files = list(FORMALIZATION.rglob("*3719*")) if FORMALIZATION.exists() else []
    formalization_files = [path for path in formalization_files if path.is_file()]
    checks = [
        ("sources_exist", "all cited local sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all generated outputs exist", all(path.exists() for path in generated_paths)),
        ("csv_parse", "all generated CSV files parse and are nonempty", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("bath_template", "Gibbs bath, partition function, and normalization rows exist", all(token in read_text(paths["bath"]) for token in ["p_z(xi|q)=exp", "Z(q,z)=integral", "integral p_z"])),
        ("parity_proof", "fibre involution proves force and mixed zero if signed", all(token in read_text(paths["parity"]) for token in ["A_B(q,z,xi)=A_B(q,-z,R_xi xi)", "partial_z F_B", "partial_q partial_z"])),
        ("identifiability", "Fisher positive floor condition exists", all(token in read_text(paths["identifiability"]) for token in ["E_0[Y_A]=0", "I_AB=E_0", "iota_H"])),
        ("theta_boundary", "Theta/unit/boundary rows retained", all(token in read_text(paths["theta_boundary"]) for token in ["Theta_H(q)", "U_H", "S_boundary"])),
        ("claim_gates_blocked", "all claim gates remain blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3720", "next target advances to corpus source hunt", "3720" in read_text(paths["next_target"])),
        ("doc_core_terms", "markdown contains mechanism statement", all(token in read_text(paths["doc"]) for token in ["normalized parent Gibbs bath", "fibre-reflection parity", "not claimed"])),
        ("no_formalization_leak", "no 3719 files written to formalization-workbench", len(formalization_files) == 0),
    ]
    return [
        {
            **base(stamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped_rows: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3719 — Parent Bath Normalization and z-Parity Proof",
        "",
        "## Status",
        "- `MECHANISM_CONSTRUCTED_NOT_PARENT_SIGNED`",
        "- This is an actual mechanism attempt, not another missing-list: a normalized parent Gibbs bath plus fibre-reflection parity can generate the bath family, Fisher matrix, `F_1=0`, and `B_QK=0` together.",
        "- It is still not claimed until the parent corpus signs the action, measure, scale, parity, identifiability, and boundary clauses.",
        "",
        "## Main Mechanism",
        "- Start with `p_z(xi|q)=exp[-A_B(q,z,xi)/Theta_H(q)]/Z(q,z)` and `Z(q,z)=integral exp[-A_B/Theta_H] dmu_H`.",
        "- Normalization gives `E_0[Y_A]=0`; the Fisher matrix is `I_AB=E_0[Y_A Y_B]`.",
        "- If a parent involution obeys `A_B(q,z,xi)=A_B(q,-z,R_xi xi)` and preserves `dmu_H`, then `Z(q,z)=Z(q,-z)` and `F_B(q,z)` is even.",
        "- Therefore `partial_z F_B|_{z=0}=0` for every `q` in the local patch and `partial_q partial_z F_B|_{z=0}=0`.",
        "- Positive local gap still needs identifiability: no nonzero active fibre direction may have zero score almost surely.",
        "",
        "## Bath Normalization",
    ]
    for row in grouped_rows["bath"]:
        lines.append(f"- `{row['bath_id']}` `{row['object']}` | {row['definition']} | {row['status']}")
    lines.extend(["", "## Parity Proof"])
    for row in grouped_rows["parity"]:
        lines.append(f"- `{row['parity_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Fisher Identifiability"])
    for row in grouped_rows["identifiability"]:
        lines.append(f"- `{row['ident_id']}` `{row['status']}`: `{row['formula']}` | {row['meaning']}")
    lines.extend(["", "## Theta and Boundary"])
    for row in grouped_rows["theta_boundary"]:
        lines.append(f"- `{row['theta_boundary_id']}` `{row['quantity']}` | {row['clause']} | {row['status']}")
    lines.extend(["", "## Decisions"])
    for row in grouped_rows["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped_rows["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Source Register"])
    for row in grouped_rows["source_register"]:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend([
        "",
        "## Next Target",
        "- `3720-Y5-R2FR-corpus-hunt-parent-bath-scale-parity-clauses.md`",
        "- Objective: search the corpus for real parent action, bath measure, `Theta_H`, fibre parity, and boundary silence clauses to sign or reject this mechanism.",
        "",
        "## Validation",
        f"- See `{paths['validation']}`.",
    ])
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    stamp = now_utc()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3719_SOURCE_REGISTER.csv",
        "bath": RESIDUALS / "P8_Y5_R2FR_3719_BATH_NORMALIZATION_ROWS.csv",
        "parity": RESIDUALS / "P8_Y5_R2FR_3719_PARITY_PROOF_ROWS.csv",
        "identifiability": RESIDUALS / "P8_Y5_R2FR_3719_FISHER_IDENTIFIABILITY_ROWS.csv",
        "theta_boundary": RESIDUALS / "P8_Y5_R2FR_3719_THETA_BOUNDARY_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3719_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3719_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3719_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3719_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3719_VALIDATION.csv",
        "doc": DOC,
    }
    grouped_rows = {
        "source_register": source_rows(stamp),
        "bath": bath_normalization_rows(stamp),
        "parity": parity_proof_rows(stamp),
        "identifiability": fisher_identifiability_rows(stamp),
        "theta_boundary": theta_and_boundary_rows(stamp),
        "decisions": decision_rows(stamp),
        "claim_gates": claim_gate_rows(stamp),
        "status": status_rows(stamp),
        "next_target": next_target_rows(stamp),
    }
    for name, rows in grouped_rows.items():
        write_csv(paths[name], rows)
    write_doc(paths, grouped_rows)
    write_csv(paths["validation"], validation_rows(stamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3719 validation failed: {failures}")
    print("wrote 3719 checkpoint: parent Gibbs bath plus z-parity mechanism constructed")


if __name__ == "__main__":
    main()
