from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3746"
BRANCH_ID = "MTS_R2FR_Y5_EXPLICIT_PARENT_ACTION_ANSATZ_AND_VARIATION_TEST_3746"
DOC = ROOT / "3746-Y5-R2FR-explicit-parent-action-ansatz-and-variation-test.md"

DOC_3744 = ROOT / "3744-Y5-R2FR-local-safe-S-closure-variant-and-PPN-test-stub.md"
DOC_3745 = ROOT / "3745-Y5-R2FR-parent-legitimacy-of-local-safe-S-closure.md"
CONTRACT_3745 = RESIDUALS / "P8_Y5_R2FR_3745_PARENT_THEOREM_CONTRACT.csv"
PROOF_3745 = RESIDUALS / "P8_Y5_R2FR_3745_CONDITIONAL_PROOF_STEPS.csv"
GATES_3745 = RESIDUALS / "P8_Y5_R2FR_3745_CLAIM_GATES.csv"
VALIDATION_3745 = RESIDUALS / "P8_Y5_BRR545_3745_VALIDATION.csv"
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
        ("doc_3744_projected_s", DOC_3744, "sigma_phi_local*epsilon_phi_raw", "explicit projected local-safe S formula"),
        ("doc_3745_status", DOC_3745, "CONDITIONAL_PROJECTOR_THEOREM_READY_PARENT_SIGNATURE_MISSING", "parent legitimacy handoff"),
        ("doc_3745_action_split", DOC_3745, "S_parent=S_GR+S_L[P_L Phi]+S_M[P_M Phi]+S_matter[q_L(Phi),psi]", "parent action split target"),
        ("contract_3745_commutator", CONTRACT_3745, "[nabla,P_L] terms are zero or budgeted", "commutator clause"),
        ("contract_3745_boundary", CONTRACT_3745, "B_LM=0 or |B_LM|<=epsilon_boundary", "boundary clause"),
        ("proof_3745_budget", PROOF_3745, "S_eff=epsilon_K+epsilon_grad+epsilon_boundary", "conditional local budget conclusion"),
        ("gates_3745_local_block", GATES_3745, "CG3745_6_local_claim", "local claim remains blocked"),
        ("validation_3745_clean", VALIDATION_3745, "next_target_3746", "3745 validation handoff"),
        ("redteam_projector_warning", RED_TEAM, "P_loc, P_gal, and P_cos could become arbitrary sector switches.", "projector anti-cheat warning"),
        ("spine_projector_route", SPINE, "exact cancellation/projector theorem", "projector route in spine"),
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


def parent_action_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("ACT3746_0_metric", "S_GR[g]", "calibrated Einstein-Hilbert/local GR baseline", "local metric/coframe", "kept calibrated; not a G_N derivation"),
        ("ACT3746_1_local_kinetic", "S_L[P_L Phi]", "local smooth K/gradK sector", "P_L Phi", "allowed to feed epsilon_K and epsilon_grad"),
        ("ACT3746_2_morphology", "S_M[P_M Phi_S]", "morphology/nonlocal Phi_S sector", "P_M Phi_S", "must be silent in local PPN or bounded"),
        ("ACT3746_3_matter", "S_matter[g_L(P_L Phi), psi]", "ordinary matter coupling through local quotient only", "q_L(Phi), g_L, psi", "must not couple to P_M Phi_S"),
        ("ACT3746_4_boundary", "B_LM[P_L Phi,P_M Phi]", "boundary/transition term", "branch interface", "must vanish or be budgeted"),
        ("ACT3746_5_total", "S_parent=S_GR+S_L+S_M+S_matter+B_LM", "minimal explicit parent ansatz for the test", "all sectors", "variation decides whether projected S is derived or only closure"),
    ]
    return [
        {
            **base(timestamp),
            "term_id": term_id,
            "action_term": action_term,
            "role": role,
            "arguments": arguments,
            "local_ppn_requirement": local_ppn_requirement,
            "claim_allowed": False,
        }
        for term_id, action_term, role, arguments, local_ppn_requirement in specs
    ]


def variation_identity_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "VAR3746_0_morphology_variation",
            "delta_L S_M",
            "<E_M, delta_L(P_M Phi_S)> + B_M",
            "local morphology response before assumptions",
            "not automatically zero",
        ),
        (
            "VAR3746_1_projector_expand",
            "delta_L(P_M Phi_S)",
            "P_M P_L delta Phi_S + (delta_L P_M) Phi_S",
            "splits ideal orthogonal zero from field-dependent projector leakage",
            "zero only if P_M P_L=0 and delta_L P_M=0",
        ),
        (
            "VAR3746_2_derivative_expand",
            "delta_L nabla(P_M Phi_S)",
            "nabla(P_M P_L delta Phi_S) + [nabla,P_M]P_L delta Phi_S + nabla((delta_L P_M)Phi_S)",
            "shows derivative/projector commutator hazard",
            "zero only if commutator and deltaP terms vanish or are bounded",
        ),
        (
            "VAR3746_3_matter_expand",
            "delta_L S_matter",
            "<T_matter, delta g_L(P_L Phi)> + <J_M, delta_L(P_M Phi_S)>",
            "tests whether local matter sees morphology",
            "requires J_M=0 by matter descent",
        ),
        (
            "VAR3746_4_boundary_expand",
            "delta_L B_LM",
            "B_LM_local + B_comm + B_deltaP",
            "tests whether integration by parts moves leakage to boundary",
            "requires zero or epsilon_boundary bound",
        ),
        (
            "VAR3746_5_total_local_residual",
            "R_local_morph",
            "R_orth + R_deltaP + R_comm + R_matter_M + R_boundary",
            "named residual vector feeding the next bound/test runner",
            "all components must vanish or be bounded before local claim",
        ),
    ]
    return [
        {
            **base(timestamp),
            "identity_id": identity_id,
            "object": obj,
            "variation_identity": identity,
            "meaning": meaning,
            "zero_condition": zero_condition,
            "claim_allowed": False,
        }
        for identity_id, obj, identity, meaning, zero_condition in specs
    ]


def ideal_zero_proof_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("ZP3746_0_local_variation", "delta_L Phi = P_L delta Phi", "local weak-field variations are in im(P_L)", "assumption"),
        ("ZP3746_1_orthogonal_projectors", "P_M P_L=0", "kills the algebraic morphology variation term", "assumption"),
        ("ZP3746_2_fixed_projector", "delta_L P_M=0", "kills field-dependent/projector-moving leakage", "assumption"),
        ("ZP3746_3_commuting_derivative", "[nabla,P_M]P_L=0", "kills derivative leakage into local equations", "assumption"),
        ("ZP3746_4_matter_descent", "J_M=delta S_matter/d(P_M Phi_S)=0", "prevents ordinary matter from sourcing morphology locally", "assumption"),
        ("ZP3746_5_boundary_silence", "B_LM=0", "prevents integration-by-parts leakage", "assumption"),
        ("ZP3746_6_conclusion", "R_local_morph=0", "under ZP3746_0 through ZP3746_5 the morphology sector is locally silent", "conditional_theorem"),
    ]
    return [
        {
            **base(timestamp),
            "proof_id": proof_id,
            "condition": condition,
            "effect": effect,
            "step_type": step_type,
            "signed_in_current_corpus": False if step_type != "conditional_theorem" else False,
            "claim_allowed": False,
        }
        for proof_id, condition, effect, step_type in specs
    ]


def residual_term_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("RES3746_0_R_orth", "R_orth", "<E_M, P_M P_L delta Phi_S>", "algebraic non-orthogonality leakage", "P_M P_L=0", "MISSING_PARENT_PROJECTOR_IDEMPOTENCE_ORTHOGONALITY"),
        ("RES3746_1_R_deltaP", "R_deltaP", "<E_M, (delta_L P_M) Phi_S>", "field-dependent projector leakage", "delta_L P_M=0 or bound", "MISSING_FIXED_PROJECTOR_OR_DELTA_PROJECTOR_BOUND"),
        ("RES3746_2_R_comm", "R_comm", "<E_M^nabla, [nabla,P_M]P_L delta Phi_S>", "covariant derivative/projector commutator leakage", "[nabla,P_M]P_L=0 or bound", "MISSING_COMMUTATOR_THEOREM_OR_BOUND"),
        ("RES3746_3_R_matter_M", "R_matter_M", "<J_M, delta_L(P_M Phi_S)>", "ordinary matter coupling to morphology", "J_M=0 by matter descent or bound", "MISSING_MATTER_DESCENT_THEOREM_OR_COUPLING_BOUND"),
        ("RES3746_4_R_boundary", "R_boundary", "B_LM_local+B_comm+B_deltaP", "boundary/interface leakage", "B_LM=0 or epsilon_boundary bound", "MISSING_BOUNDARY_NO_FLUX_THEOREM_OR_BOUND"),
        ("RES3746_5_R_total", "R_local_morph", "R_orth+R_deltaP+R_comm+R_matter_M+R_boundary", "total local morphology residual", "all residuals zero or bounded below PPN tolerance", "LOCAL_CLAIM_BLOCKED_UNTIL_COMPONENTS_CLOSE"),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "formula": formula,
            "physical_meaning": meaning,
            "zero_or_bound_condition": condition,
            "status": status,
            "claim_allowed": False,
        }
        for residual_id, symbol, formula, meaning, condition, status in specs
    ]


def ppn_bound_interface_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("BND3746_0_sigma_phi", "sigma_phi_local", "||P_L response from P_M Phi_S|| / ||Phi_S||", "dimensionless", "feeds epsilon_phi_eff=sigma_phi_local*epsilon_phi_raw", "MISSING_ZERO_OR_BOUND"),
        ("BND3746_1_deltaP", "epsilon_deltaP", "||R_deltaP||", "operator_or_dimensionless_profile", "adds to S_eff if projector depends on local fields", "MISSING_BOUND"),
        ("BND3746_2_comm", "epsilon_comm", "||R_comm||", "operator_or_dimensionless_profile", "adds derivative/projector leakage", "MISSING_BOUND"),
        ("BND3746_3_matter", "epsilon_matter_M", "||R_matter_M||", "source_or_metric_response_units", "feeds fifth-force/PPN/source-coupling residual", "MISSING_MATTER_COUPLING_BOUND"),
        ("BND3746_4_boundary", "epsilon_boundary_LM", "||R_boundary||", "boundary_profile_units", "extends prior epsilon_boundary budget", "MISSING_BOUNDARY_BOUND"),
        ("BND3746_5_total_ppn", "S_eff_3746", "epsilon_K+epsilon_grad+epsilon_boundary+epsilon_phi_eff+epsilon_deltaP+epsilon_comm+epsilon_matter_M+epsilon_boundary_LM", "dimensionless_budget_after_normalization", "must satisfy gamma/beta/Newton tolerance gate", "BOUND_INTERFACE_READY_VALUES_MISSING"),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "observable_link": observable_link,
            "status": status,
            "claim_allowed": False,
        }
        for bound_id, quantity, definition, units, observable_link, status in specs
    ]


def theorem_verdict_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("THM3746_0_variation_identity", "DERIVED_FORMAL_IDENTITY", "Local variation of the morphology action decomposes into R_orth, R_deltaP, R_comm, R_matter_M, and R_boundary."),
        ("THM3746_1_conditional_zero", "CONDITIONAL_ZERO_THEOREM", "If projectors are fixed orthogonal, derivative-compatible, matter-descended, and boundary-silent, then R_local_morph=0."),
        ("THM3746_2_current_result", "UNSIGNED_IN_CURRENT_CORPUS", "The current corpus does not sign the conditions, so the theorem does not yet produce a local GR/PPN claim."),
        ("THM3746_3_real_progress", "RESIDUAL_VECTOR_EXTRACTED", "The next work is no longer vague: fill or prove five named residuals."),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "status": status,
            "statement": statement,
            "claim_allowed": False,
        }
        for theorem_id, status, statement in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3746_0_sources", "3746 source handoff complete", True, "source paths and needles found"),
        ("CG3746_1_action_ansatz", "explicit parent action ansatz written", True, "S_GR+S_L+S_M+S_matter+B_LM rows emitted"),
        ("CG3746_2_variation_identity", "local morphology variation identity derived", True, "residual decomposition emitted"),
        ("CG3746_3_conditional_zero", "conditional zero theorem stated", True, "ideal assumptions imply R_local_morph=0"),
        ("CG3746_4_conditions_signed", "zero theorem assumptions signed by corpus", False, "fixed projector, matter descent, commutator, and boundary clauses remain unsigned"),
        ("CG3746_5_residuals_bounded", "all residual components bounded", False, "no numeric/source bounds yet"),
        ("CG3746_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "conditional theorem and residual vector only"),
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
        ("DEC3746_0_progress", "VARIATION_TEST_COMPLETED_SYMBOLICALLY", "The local-safe projector route now has an explicit action ansatz and variation residual decomposition."),
        ("DEC3746_1_best_next", "ATTACK_DELTA_PROJECTOR_AND_COMMUTATOR_FIRST", "R_deltaP and R_comm decide whether the projector is a real parent structure or an arena switch."),
        ("DEC3746_2_fallback", "IF_DELTA_PROJECTOR_OR_COMMUTATOR_SURVIVES_BUILD_BOUND_RUNNER", "If zero cannot be proved, the residuals must be fed into the PPN/Newton tolerance interface from 3744."),
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
        "status_id": "STATUS3746_0",
        "status": "VARIATION_IDENTITY_AND_CONDITIONAL_ZERO_DERIVED_RESIDUALS_REMAIN",
        "summary": "3746 writes the minimal parent action ansatz, varies the morphology sector against local PPN variations, derives the conditional zero theorem, and extracts the residual vector that must be proved zero or bounded.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3746_0",
        "target_doc": "3747-Y5-R2FR-projector-fixedness-commutator-zero-or-bound.md",
        "target_script": "scripts/Y5_R2FR_3747_projector_fixedness_commutator_zero_or_bound.py",
        "objective": "try to prove delta_L P_M=0 and [nabla,P_M]P_L=0 for the local parent projector; if not, create explicit epsilon_deltaP and epsilon_comm bound rows for the PPN/Newton gate",
        "success_gate": "either R_deltaP and R_comm vanish by parent geometry, or they enter S_eff_3746 as bounded nonclaim residuals",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3746 - Explicit Parent Action Ansatz and Variation Test",
        "",
        "## Status",
        "- `VARIATION_IDENTITY_AND_CONDITIONAL_ZERO_DERIVED_RESIDUALS_REMAIN`",
        "- This checkpoint does the algebraic leap from a projector contract to a concrete parent-action variation test.",
        "- Result: the local morphology sector is silent only under explicit fixed-projector, commutator, matter-descent, and boundary assumptions.",
        "",
        "## Parent Action Ansatz",
    ]
    for row in grouped["action"]:
        lines.append(f"- `{row['term_id']}`: `{row['action_term']}` | {row['local_ppn_requirement']}")
    lines.extend(["", "## Variation Identity"])
    for row in grouped["variation"]:
        lines.append(f"- `{row['identity_id']}` `{row['object']}`: {row['variation_identity']} | {row['zero_condition']}")
    lines.extend(["", "## Conditional Zero Proof"])
    for row in grouped["zero_proof"]:
        lines.append(f"- `{row['proof_id']}` `{row['step_type']}`: {row['condition']} -> {row['effect']}")
    lines.extend(["", "## Residual Vector"])
    for row in grouped["residuals"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}` `{row['status']}`: {row['formula']}")
    lines.extend(["", "## PPN/Newton Bound Interface"])
    for row in grouped["bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['quantity']}` `{row['status']}`: {row['definition']}")
    lines.extend(["", "## Theorem Verdicts"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}` | {row['statement']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
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
    action = parse_csv(paths["action"])
    variation = parse_csv(paths["variation"])
    zero_proof = parse_csv(paths["zero_proof"])
    residuals = parse_csv(paths["residuals"])
    bounds = parse_csv(paths["bounds"])
    theorems = parse_csv(paths["theorems"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3746*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("action_complete", "minimal parent action ansatz has six terms", len(action) == 6 and "S_parent=S_GR+S_L+S_M+S_matter+B_LM" in read_text(paths["action"])),
        ("variation_identity", "variation residual decomposition emitted", len(variation) == 6 and "R_orth + R_deltaP + R_comm + R_matter_M + R_boundary" in read_text(paths["variation"])),
        ("zero_proof_conditional", "conditional zero proof has assumptions and conclusion", len(zero_proof) == 7 and "R_local_morph=0" in read_text(paths["zero_proof"])),
        ("residual_vector", "five component residuals plus total residual emitted", len(residuals) == 6 and all(token in read_text(paths["residuals"]) for token in ["R_deltaP", "R_comm", "R_matter_M", "R_boundary", "R_local_morph"])),
        ("bound_interface", "S_eff_3746 bound interface emitted", len(bounds) == 6 and "epsilon_deltaP+epsilon_comm+epsilon_matter_M" in read_text(paths["bounds"])),
        ("theorem_status", "theorem verdicts distinguish identity, conditional zero, and unsigned corpus", all(token in read_text(paths["theorems"]) for token in ["DERIVED_FORMAL_IDENTITY", "CONDITIONAL_ZERO_THEOREM", "UNSIGNED_IN_CURRENT_CORPUS"])),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3746_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("claim_allowed_false", "all gate rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records variation test and residual vector", all(token in read_text(paths["doc"]) for token in ["Variation Identity", "Conditional Zero Proof", "Residual Vector"])),
        ("next_target_3747", "next target attacks projector fixedness and commutator", next_target[0]["target_doc"] == "3747-Y5-R2FR-projector-fixedness-commutator-zero-or-bound.md"),
        ("no_formalization_leak", "no 3746 files in formalization-workbench", len(formalization_leaks) == 0),
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
        "source_register": RESIDUALS / "P8_Y5_R2FR_3746_SOURCE_REGISTER.csv",
        "action": RESIDUALS / "P8_Y5_R2FR_3746_PARENT_ACTION_ANSATZ.csv",
        "variation": RESIDUALS / "P8_Y5_R2FR_3746_VARIATION_IDENTITIES.csv",
        "zero_proof": RESIDUALS / "P8_Y5_R2FR_3746_CONDITIONAL_ZERO_PROOF.csv",
        "residuals": RESIDUALS / "P8_Y5_R2FR_3746_RESIDUAL_VECTOR.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3746_PPN_BOUND_INTERFACE.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3746_THEOREM_VERDICTS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3746_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3746_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3746_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3746_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3746_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(timestamp),
        "action": parent_action_rows(timestamp),
        "variation": variation_identity_rows(timestamp),
        "zero_proof": ideal_zero_proof_rows(timestamp),
        "residuals": residual_term_rows(timestamp),
        "bounds": ppn_bound_interface_rows(timestamp),
        "theorems": theorem_verdict_rows(timestamp),
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
        raise SystemExit(f"3746 validation failed: {failures}")
    print("wrote 3746 checkpoint: parent action variation identity derived; residual vector extracted")


if __name__ == "__main__":
    main()
