from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3745"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_LEGITIMACY_OF_LOCAL_SAFE_S_CLOSURE_3745"
DOC = ROOT / "3745-Y5-R2FR-parent-legitimacy-of-local-safe-S-closure.md"

DOC_3741 = ROOT / "3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md"
DOC_3742 = ROOT / "3742-Y5-R2FR-local-S-budget-gate-etaPhi2-gradK-bound.md"
DOC_3743 = ROOT / "3743-Y5-R2FR-local-PhiS-projector-or-eta-zero-theorem.md"
DOC_3744 = ROOT / "3744-Y5-R2FR-local-safe-S-closure-variant-and-PPN-test-stub.md"
PROJECTOR_CONTRACT_3743 = RESIDUALS / "P8_Y5_R2FR_3743_PROJECTOR_CONTRACT_ROWS.csv"
CLOSURE_VARIANTS_3744 = RESIDUALS / "P8_Y5_R2FR_3744_CLOSURE_VARIANTS.csv"
DRY_RESULTS_3744 = RESIDUALS / "P8_Y5_R2FR_3744_PPN_DRY_RUN_RESULTS.csv"
VALIDATION_3744 = RESIDUALS / "P8_Y5_BRR545_3744_VALIDATION.csv"
RED_TEAM = FORMALIZATION / "06-consistency-red-team.md"
SPINE = FORMALIZATION / "07-unification-spine.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


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


def find_line(path: Path, needle: str) -> tuple[int, str]:
    for line_number, line in enumerate(read_lines(path), start=1):
        if needle in line:
            return line_number, line.strip()
    return 0, ""


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3741_conditional_ppn", DOC_3741, "For a calibrated GR baseline", "calibrated-GR perturbative closure theorem"),
        ("doc_3742_full_budget", DOC_3742, "S_epsilon = epsilon_K + epsilon_grad + epsilon_phi + epsilon_boundary", "full local S budget"),
        ("doc_3743_projector_failed", DOC_3743, "P_loc Phi_S=0 is not parent-derived", "failed unconditional projector theorem"),
        ("projector_contract_3743_kernel", PROJECTOR_CONTRACT_3743, "kernel condition", "machine-readable projector contract clause"),
        ("doc_3744_projected_preferred", DOC_3744, "PROJECTED_LOCAL_SAFE_S_IS_PREFERRED_REPAIR", "projected local-safe route selected as best repair candidate"),
        ("closure_3744_sigma", CLOSURE_VARIANTS_3744, "sigma_phi_local*epsilon_phi_raw", "explicit projected S formula"),
        ("dry_results_3744_projected", DRY_RESULTS_3744, "RES3744_1_projected_zero", "dry-run arithmetic for projected branch"),
        ("validation_3744_no_leak", VALIDATION_3744, "no_formalization_leak", "3744 validation clean"),
        ("redteam_projector_cheat", RED_TEAM, "P_loc, P_gal, and P_cos could become arbitrary sector switches.", "anti-cheat warning for sector projectors"),
        ("spine_projector_route", SPINE, "exact cancellation/projector theorem", "spine names projector theorem as route"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        line_number, line_text = find_line(path, needle) if exists else (0, "")
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "line_number": line_number,
            "line_text": line_text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def parent_contract_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "PLC3745_0_projector_domain",
            "fixed parent projector domain",
            "There is a parent state space E with covariant idempotent projectors P_L and P_M=1-P_L.",
            "P_L^2=P_L, P_M^2=P_M, P_L P_M=0",
            "prevents arena-label switches",
        ),
        (
            "PLC3745_1_variational_pairing",
            "orthogonal/self-adjoint pairing",
            "The variational pairing that defines local field equations makes local variations lie in im(P_L) and morphology terms in im(P_M).",
            "<delta_L Phi, P_M X>=0",
            "kills the local variation of morphology energy",
        ),
        (
            "PLC3745_2_action_split",
            "parent action split",
            "The parent action separates local and morphology contributions before gauge fixing.",
            "S_parent=S_GR+S_L[P_L Phi]+S_M[P_M Phi]+S_matter[q_L(Phi),psi]",
            "turns the repair from patch into theorem",
        ),
        (
            "PLC3745_3_matter_descent",
            "matter observes only the local quotient",
            "Ordinary local matter depends on q_L(Phi), metric/coframe, and matter fields, not on P_M Phi_S.",
            "delta S_matter / delta(P_M Phi_S)=0",
            "prevents fifth-force or PPN leakage through matter coupling",
        ),
        (
            "PLC3745_4_derivative_commutation",
            "covariant derivative compatibility",
            "P_L commutes with the derivative/connection operations needed in the weak-field local branch up to bounded terms.",
            "[nabla,P_L] terms are zero or budgeted",
            "prevents hidden grad-projector residuals",
        ),
        (
            "PLC3745_5_boundary_silence",
            "boundary and transition silence",
            "Integrations by parts and branch transitions do not create boundary flux from P_M into P_L.",
            "B_LM=0 or |B_LM|<=epsilon_boundary",
            "prevents projector proof from moving the problem to the boundary",
        ),
        (
            "PLC3745_6_global_non-erasure",
            "galaxy/cosmology non-erasure",
            "Removing P_M from local PPN observables must not erase the morphology sector in galaxy/cosmology observables.",
            "P_gal P_M and P_cos P_M are allowed nonzero",
            "keeps the unified route honest rather than MOND-by-switch",
        ),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "clause": clause,
            "requirement": requirement,
            "formal_condition": formal_condition,
            "why_it_matters": why_it_matters,
            "signed_status": "REQUIRED_UNSIGNED",
            "claim_allowed": False,
        }
        for contract_id, clause, requirement, formal_condition, why_it_matters in specs
    ]


def signedness_audit_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("SA3745_0_projector_domain", "PLC3745_0_projector_domain", "PARTIAL_CONCEPT_ONLY", "P_loc exists as a toy/red-team object, but not as a parent covariant idempotent.", "unsigned"),
        ("SA3745_1_pairing", "PLC3745_1_variational_pairing", "NOT_FOUND", "No parent variational inner product/signature proves im(P_L) orthogonal to morphology response.", "unsigned"),
        ("SA3745_2_action_split", "PLC3745_2_action_split", "NOT_FOUND", "No sourced parent action split S_L[P_L Phi]+S_M[P_M Phi] was found.", "unsigned"),
        ("SA3745_3_matter_descent", "PLC3745_3_matter_descent", "NOT_FOUND", "No local matter descent theorem excludes P_M Phi_S from matter coupling.", "unsigned"),
        ("SA3745_4_derivative_commutation", "PLC3745_4_derivative_commutation", "NOT_FOUND", "No [nabla,P_L]=0 or bounded commutator theorem was found.", "unsigned"),
        ("SA3745_5_boundary", "PLC3745_5_boundary_silence", "NOT_FOUND", "No no-flux boundary theorem for P_M -> P_L leakage was found.", "unsigned"),
        ("SA3745_6_non_erasure", "PLC3745_6_global_non-erasure", "PLAUSIBLE_BUT_NOT_PROVED", "The route intends galaxy/cosmology morphology to survive, but branch algebra is not signed.", "unsigned"),
    ]
    return [
        {
            **base(timestamp),
            "audit_id": audit_id,
            "contract_id": contract_id,
            "evidence_status": evidence_status,
            "finding": finding,
            "signedness": signedness,
            "claim_allowed": False,
        }
        for audit_id, contract_id, evidence_status, finding, signedness in specs
    ]


def conditional_proof_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("PRF3745_0_assume_split", "Assume the parent split S_parent=S_GR+S_L[P_L Phi]+S_M[P_M Phi]+S_matter[q_L(Phi),psi].", "hypothesis"),
        ("PRF3745_1_vary_local", "Take a local weak-field variation delta_L Phi in im(P_L).", "hypothesis"),
        ("PRF3745_2_pairing_zero", "By self-adjoint orthogonality, <delta_L Phi, delta S_M/d(P_M Phi)>=0.", "deduction"),
        ("PRF3745_3_matter_zero", "By matter descent, delta_L S_matter has no P_M Phi_S source term.", "deduction"),
        ("PRF3745_4_boundary_zero", "By no-flux boundary silence, integration-by-parts terms do not re-enter im(P_L).", "deduction"),
        ("PRF3745_5_local_budget", "Therefore the local PPN budget sees S_eff=epsilon_K+epsilon_grad+epsilon_boundary, or sigma_phi_local*epsilon_phi_raw if only bounded projection is proved.", "conditional_conclusion"),
        ("PRF3745_6_claim_limit", "Because the hypotheses are unsigned in the current corpus, this is a conditional theorem skeleton only.", "anti_overclaim"),
    ]
    return [
        {
            **base(timestamp),
            "proof_id": proof_id,
            "step": step,
            "step_type": step_type,
            "claim_allowed": False,
        }
        for proof_id, step, step_type in specs
    ]


def verdict_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("VER3745_0_conditional_theorem", "CONDITIONAL_PROJECTOR_THEOREM_BUILT", "If all parent-contract clauses are signed, the projected local-safe S closure is mathematically legitimate."),
        ("VER3745_1_unconditional_failure", "UNCONDITIONAL_PARENT_DERIVATION_NOT_PROVED", "The current corpus does not sign the projector domain, action split, matter descent, commutator, or boundary clauses."),
        ("VER3745_2_label", "CLOSURE_PATCH_LABEL_REQUIRED_FOR_NOW", "Until those clauses are signed, projected S is a disciplined closure patch, not a derived local-GR theorem."),
        ("VER3745_3_best_next", "BUILD_EXPLICIT_PARENT_ACTION_ANSATZ_AND_VARIATION_TEST", "The next non-circular move is to write the simplest parent action ansatz satisfying PLC3745 and vary it symbolically."),
    ]
    return [
        {
            **base(timestamp),
            "verdict_id": verdict_id,
            "verdict": verdict,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for verdict_id, verdict, rationale in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3745_0_sources", "3745 source sweep complete", True, "all source paths and needles are available"),
        ("CG3745_1_conditional_theorem", "conditional parent projector theorem is stated", True, "proof skeleton is exact enough to test"),
        ("CG3745_2_projector_domain_signed", "P_L/P_M parent projector domain signed", False, "not found as a parent theorem"),
        ("CG3745_3_action_split_signed", "parent action split signed", False, "not found"),
        ("CG3745_4_matter_descent_signed", "matter descent signed", False, "not found"),
        ("CG3745_5_commutator_boundary_signed", "commutator and boundary silence signed", False, "not found"),
        ("CG3745_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "conditional theorem hypotheses are unsigned"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3745_0_progress", "EXACT_PARENT_CONTRACT_WRITTEN", "The projected repair now has a precise parent action contract instead of a vague projector wish."),
        ("DEC3745_1_not_enough", "CURRENT_CORPUS_DOES_NOT_SIGN_IT", "The route is viable but not yet derived."),
        ("DEC3745_2_best_route", "DO_THE_VARIATION_TEST_NEXT", "Writing a minimal parent ansatz and varying it is the shortest path to either real progress or clean rejection."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3745_0",
        "status": "CONDITIONAL_PROJECTOR_THEOREM_READY_PARENT_SIGNATURE_MISSING",
        "summary": "3745 derives the exact conditional theorem needed to legitimize projected local-safe S, but the current corpus does not sign the parent projector/action/matter/boundary clauses.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3745_0",
        "target_doc": "3746-Y5-R2FR-explicit-parent-action-ansatz-and-variation-test.md",
        "target_script": "scripts/Y5_R2FR_3746_explicit_parent_action_ansatz_and_variation_test.py",
        "objective": "write the simplest parent action ansatz satisfying the 3745 projector contract and perform a symbolic variation test for whether the morphology sector is truly silent in local PPN",
        "success_gate": "either variation gives zero local morphology response under explicit assumptions, or it produces named residual terms for the next bound/test runner",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3745 - Parent Legitimacy of Local-Safe S Closure",
        "",
        "## Status",
        "- `CONDITIONAL_PROJECTOR_THEOREM_READY_PARENT_SIGNATURE_MISSING`",
        "- We now have the exact theorem contract the projected local-safe `S` branch must satisfy.",
        "- The theorem is conditional only: the current corpus does not yet sign the parent projector/action/matter/boundary clauses.",
        "",
        "## Parent Contract",
    ]
    for row in grouped["parent_contract"]:
        lines.append(f"- `{row['contract_id']}` `{row['signed_status']}`: {row['formal_condition']} | {row['why_it_matters']}")
    lines.extend(["", "## Conditional Proof Skeleton"])
    for row in grouped["proof"]:
        lines.append(f"- `{row['proof_id']}` `{row['step_type']}`: {row['step']}")
    lines.extend(["", "## Signedness Audit"])
    for row in grouped["signedness"]:
        lines.append(f"- `{row['audit_id']}` `{row['evidence_status']}`: {row['finding']}")
    lines.extend(["", "## Verdicts"])
    for row in grouped["verdicts"]:
        lines.append(f"- `{row['verdict_id']}` `{row['verdict']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` passed={row['passed']} claim_allowed={row['claim_allowed']} | {row['gate']}: {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    contract = parse_csv(paths["parent_contract"])
    signedness = parse_csv(paths["signedness"])
    proof = parse_csv(paths["proof"])
    verdicts = parse_csv(paths["verdicts"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3745*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("contract_complete", "seven parent contract clauses emitted", len(contract) == 7 and all(row["signed_status"] == "REQUIRED_UNSIGNED" for row in contract)),
        ("contract_has_action", "contract includes action split and matter descent", all(token in read_text(paths["parent_contract"]) for token in ["S_parent=S_GR+S_L", "delta S_matter / delta(P_M Phi_S)=0"])),
        ("signedness_blocks", "signedness audit blocks unconditional theorem", len(signedness) == 7 and all(row["signedness"] == "unsigned" for row in signedness)),
        ("proof_conditional", "conditional proof skeleton has conclusion and anti-overclaim", len(proof) == 7 and all(token in read_text(paths["proof"]) for token in ["conditional_conclusion", "anti_overclaim"])),
        ("verdicts_correct", "conditional theorem built but unconditional derivation not proved", all(token in read_text(paths["verdicts"]) for token in ["CONDITIONAL_PROJECTOR_THEOREM_BUILT", "UNCONDITIONAL_PARENT_DERIVATION_NOT_PROVED"])),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3745_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("claim_allowed_false", "all gate rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records parent signature missing", all(token in read_text(paths["doc"]) for token in ["CONDITIONAL_PROJECTOR_THEOREM_READY", "Parent Contract", "Signedness Audit"])),
        ("next_target_3746", "next target is explicit action variation test", next_target[0]["target_doc"] == "3746-Y5-R2FR-explicit-parent-action-ansatz-and-variation-test.md"),
        ("no_formalization_leak", "no 3745 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3745_SOURCE_REGISTER.csv",
        "parent_contract": RESIDUALS / "P8_Y5_R2FR_3745_PARENT_THEOREM_CONTRACT.csv",
        "signedness": RESIDUALS / "P8_Y5_R2FR_3745_SIGNEDNESS_AUDIT.csv",
        "proof": RESIDUALS / "P8_Y5_R2FR_3745_CONDITIONAL_PROOF_STEPS.csv",
        "verdicts": RESIDUALS / "P8_Y5_R2FR_3745_VERDICT_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3745_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3745_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3745_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3745_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3745_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "parent_contract": parent_contract_rows(timestamp),
        "signedness": signedness_audit_rows(timestamp),
        "proof": conditional_proof_rows(timestamp),
        "verdicts": verdict_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "status": status_rows(timestamp),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3745 validation failed: {failures}")
    print("wrote 3745 checkpoint: conditional parent projector theorem built; parent signature still missing")


if __name__ == "__main__":
    main()
