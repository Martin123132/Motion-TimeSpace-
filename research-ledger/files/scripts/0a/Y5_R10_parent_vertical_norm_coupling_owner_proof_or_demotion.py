from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_parent_vertical_norm_coupling_owner_proof_or_demotion.py"
DOC_PATH = ROOT / "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md"

STATUS = "Y5_R10_parent_vertical_norm_theorem_written_but_current_corpus_cannot_sign_subblock_inheritance_zero_route_demoted"
CLAIM_CEILING = "conditional_vertical_norm_theorem_and_rescaling_counterexample_only_no_kappa_alpha_zero_no_EM_or_local_claim"
NEXT_TARGET = "645-Y5-R10-finite-kappa-alpha-bound-input-fill-and-prior-discipline.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S644_0", "checkpoint_643_doc", ROOT / "643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md", "immediate prior owner hunt"),
        ("S644_1", "validation_643", OUT / "P8_Y5_BRR545_643_VALIDATION.csv", "prior validation"),
        ("S644_2", "vertical_norm_contract_643", OUT / "P8_Y5_R10_643_PARENT_VERTICAL_NORM_CONTRACT.csv", "proof contract input"),
        ("S644_3", "rescaling_no_go_643", OUT / "P8_Y5_R10_643_RESCALING_NO_GO.csv", "rescaling/free-coupling blocker input"),
        ("S644_4", "owner_candidate_matrix_643", OUT / "P8_Y5_R10_643_OWNER_CANDIDATE_MATRIX.csv", "owner candidate comparison"),
        ("S644_5", "GK_parent_metric_Ward_211", ROOT / "211-GK-parent-metric-Ward-identity-attempt.md", "partial parent norm precedent; full composite metric not derived"),
        ("S644_6", "X_constraint_parent_223", ROOT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "constraint algebra and constitutive owner blockers"),
        ("S644_7", "boundary_symplectic_metric_233", ROOT / "233-boundary-symplectic-metric-or-local-EH-operator.md", "boundary Hodge/DeWitt metric candidate but not parent-derived"),
        ("S644_8", "Hamiltonian_trace_current_332", ROOT / "332-parent-Hamiltonian-trace-current-gate.md", "same unit-inheritance vs lambda-rescaling pattern"),
        ("S644_9", "generator_script_644", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def conditional_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CVN644",
            "name": "conditional parent vertical norm alpha-silence theorem",
            "statement": "If EM is the projection of a compact parent vertical generator T_Q with fixed parent norm, unique curvature-norm subblock, same-owner current, observed coframe descent, and no independent F_Q^2 invariant, then local vertical Xhat variations give D_v ln(alpha_EM)=0.",
            "proof_status": "proved_as_conditional_template",
            "corpus_status": "premises_unsigned",
            "valid_for_claim": "false",
        }
    ]


def proof_step_rows() -> list[dict[str, object]]:
    return [
        {
            "step_id": "PS644_0_parent_bundle",
            "required_premise": "Parent state carries a compact vertical charge fibre with generator T_Q.",
            "derivation_attempt": "Use 642 compact U1 result as the fibre template.",
            "logical_result_if_true": "charge labels can be representation/winding labels",
            "corpus_result": "partial_template_only",
            "blocking_gap": "T_Q is not yet a field/generator in the parent action",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PS644_1_fixed_vertical_norm",
            "required_premise": "The parent metric/symplectic/lattice form fixes N_Q=<T_Q,T_Q> and forbids T_Q -> s T_Q.",
            "derivation_attempt": "Borrow the Hodge/DeWitt and GK parent-norm pattern as the candidate norm owner.",
            "logical_result_if_true": "the charge generator cannot be renormalized away",
            "corpus_result": "not_derived",
            "blocking_gap": "211/233 give candidates and partial flow ownership, but not a parent-fixed charge-generator norm",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PS644_2_connection_projection",
            "required_premise": "Observed A_mu is the projection of the parent connection on T_Q.",
            "derivation_attempt": "Write Omega_Q = A_Q T_Q and F_Q = dA_Q for the charge subblock.",
            "logical_result_if_true": "EM curvature is parent-owned rather than inserted",
            "corpus_result": "missing",
            "blocking_gap": "no source maps the MTS parent connection/coframe to the observed EM connection",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PS644_3_unique_curvature_subblock",
            "required_premise": "The F_Q^2 term is a literal piece of the already-normalized parent curvature norm.",
            "derivation_attempt": "Use the Hamiltonian subblock inheritance pattern: unit coefficient is owned only if the term is not separately addable.",
            "logical_result_if_true": "1/g_EM^2 is inherited from the parent coefficient and N_Q",
            "corpus_result": "failed_current_corpus",
            "blocking_gap": "the current corpus does not forbid an independent lambda_A F_Q^2 invariant",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PS644_4_same_owner_current",
            "required_premise": "The Noether/boundary current couples to A_Q with charge unit Q_star fixed by T_Q normalization.",
            "derivation_attempt": "Use 287/288/109/110 charge-unit ladders as the same-owner current route.",
            "logical_result_if_true": "charge unit and Maxwell source normalization have one owner",
            "corpus_result": "failed_current_corpus",
            "blocking_gap": "Q_star, level/index theorem, and EM current identification remain missing",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PS644_5_measure_coframe_descent",
            "required_premise": "Parent measure and Hodge star descend to the observed local coframe used by matter.",
            "derivation_attempt": "Use the boundary Hodge/DeWitt metric candidate and universal-coupling discipline.",
            "logical_result_if_true": "no hidden frame/clock factor can reopen alpha pressure",
            "corpus_result": "candidate_not_parent_derived",
            "blocking_gap": "boundary metric and local coframe descent are still candidates, not parent variation results",
            "valid_for_claim": "false",
        },
        {
            "step_id": "PS644_6_vertical_alpha_silence",
            "required_premise": "D_v N_Q = D_v C_parent = D_v hbar = D_v c = 0 and no alpha_EM(Xhat) vertex exists.",
            "derivation_attempt": "Differentiate the inherited coupling formula along local vertical variations.",
            "logical_result_if_true": "kappa_alpha = D_v ln(alpha_EM) = 0",
            "corpus_result": "conditional_only",
            "blocking_gap": "depends on all previous unsigned premises",
            "valid_for_claim": "false",
        },
    ]


def formula_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "formula_id": "FL644_0_parent_norm",
            "formula": "S_parent ⊃ -C_P/4 ∫ dμ_parent <F,F>_V",
            "meaning": "parent curvature norm with already-owned coefficient C_P",
            "owned_if": "C_P and the vertical metric are fixed by the parent action",
            "current_status": "template_only",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FL644_1_charge_projection",
            "formula": "F = F_Q T_Q + F_perp,  <T_Q,T_Q>_V = N_Q",
            "meaning": "projection of the parent curvature onto the charge generator",
            "owned_if": "T_Q is a parent generator with fixed norm N_Q",
            "current_status": "not_parent_signed",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FL644_2_Maxwell_coefficient",
            "formula": "S_Q = -(C_P N_Q)/4 ∫ dμ_obs F_Q^{μν}F^Q_{μν}",
            "meaning": "observed Maxwell coefficient inherited from parent norm after measure/coframe descent",
            "owned_if": "dμ_parent,*_parent descend to dμ_obs,*_obs and no extra λ_A F_Q² is allowed",
            "current_status": "blocked_by_subblock_and_coframe_gaps",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FL644_3_coupling_readout",
            "formula": "g_EM^{-2} = C_P N_Q,  alpha_EM = g_EM²/(4π ħ c)",
            "meaning": "alpha is fixed if C_P, N_Q, ħ, and c are quotient-fixed",
            "owned_if": "all four readout factors are parent-owned and locally vertical-silent",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "FL644_4_alpha_silence",
            "formula": "D_v ln(alpha_EM) = -D_v ln(C_P N_Q ħ c)",
            "meaning": "local alpha response vanishes only if the inherited factors are vertical-silent",
            "owned_if": "D_v C_P = D_v N_Q = D_v ħ = D_v c = 0",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
        },
    ]


def rescaling_counterexample_rows() -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "RC644_0_free_lambda_A",
            "construction": "Add ΔS = -λ_A/4 ∫ dμ_obs F_Q^{μν}F^Q_{μν}.",
            "why_allowed_by_current_corpus": "It is gauge-invariant, covariant, and not forbidden by any parent uniqueness theorem currently in the files.",
            "effect": "g_EM^{-2} -> C_P N_Q + λ_A, so alpha_EM is not fixed by the parent norm alone.",
            "defeats_claim": "kappa_alpha_zero",
            "blocked_only_if": "literal subblock inheritance plus no-independent-invariant theorem is proved",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "RC644_1_generator_rescale",
            "construction": "Rescale T_Q -> s T_Q and A_Q -> A_Q/s while preserving the same formal connection product A_Q T_Q.",
            "why_allowed_by_current_corpus": "No parent lattice/norm theorem currently fixes the absolute normalization of T_Q.",
            "effect": "relative integer labels survive but Q_star and g_EM shift.",
            "defeats_claim": "charge_unit_and_alpha_owner",
            "blocked_only_if": "fixed generator norm/lattice theorem is proved",
            "valid_for_claim": "false",
        },
        {
            "counterexample_id": "RC644_2_coframe_factor",
            "construction": "Let the projection from parent Hodge star to observed Hodge star carry a local factor ζ_X.",
            "why_allowed_by_current_corpus": "Measure/coframe descent is candidate-level, not parent-derived.",
            "effect": "g_EM^{-2} -> ζ_X C_P N_Q and D_v ln(alpha_EM) can be nonzero.",
            "defeats_claim": "local_vertical_silence",
            "blocked_only_if": "observed coframe descent and vertical ζ_X silence are proved",
            "valid_for_claim": "false",
        },
    ]


def evidence_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "evidence_id": "EA644_0_GK_norm",
            "source": "211-GK-parent-metric-Ward-identity-attempt.md",
            "support": "ADM/DeWitt-style norm gives partial geometric ownership for a flow block.",
            "limit": "full composite metric and charge-generator norm are not parent-derived",
            "supports_proof": "partial",
            "valid_for_claim": "false",
        },
        {
            "evidence_id": "EA644_1_boundary_metric",
            "source": "233-boundary-symplectic-metric-or-local-EH-operator.md",
            "support": "boundary Hodge/DeWitt metric candidate can orthogonalize/project sectors",
            "limit": "metric candidate is not varied from parent action and does not include EM charge subblock",
            "supports_proof": "partial",
            "valid_for_claim": "false",
        },
        {
            "evidence_id": "EA644_2_Hamiltonian_pattern",
            "source": "332-parent-Hamiltonian-trace-current-gate.md",
            "support": "correct unit route is literal inherited subblock; lambda-rescaling no-go already identified",
            "limit": "pattern transfers conceptually but does not prove EM subblock inheritance",
            "supports_proof": "strong_analogy_only",
            "valid_for_claim": "false",
        },
        {
            "evidence_id": "EA644_3_charge_current",
            "source": "287/288/109/110 charge-unit attempts",
            "support": "relative current and index/level route are identified",
            "limit": "Q_star, level/index theorem, and EM current identification remain missing",
            "supports_proof": "partial",
            "valid_for_claim": "false",
        },
    ]


def demotion_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG644_0_conditional_theorem",
            "gate": "conditional vertical-norm theorem written",
            "result": "pass",
            "consequence": "we know exactly what a future parent action must prove",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG644_1_parent_signed_premises",
            "gate": "all theorem premises signed by existing corpus",
            "result": "fail",
            "consequence": "zero-coupling route cannot be promoted",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG644_2_rescaling_counterexample_closed",
            "gate": "λ_A F_Q² and T_Q rescaling counterexamples are forbidden",
            "result": "fail",
            "consequence": "alpha_EM remains a possible finite coupling",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG644_3_demote_zero_route",
            "gate": "demote kappa_alpha=0 route to closure contract in the current corpus",
            "result": "pass",
            "consequence": "next work should fill finite-coupling inputs unless a new parent-action source appears",
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC644_0",
            "next_target": NEXT_TARGET,
            "work_item": "Define finite kappa_alpha prior rows with explicit units/status rather than theorem-zero language.",
            "acceptance_condition": "no finite row is valid_for_claim until Xhat unit, tau maps, and sensitivity coefficients exist",
        },
        {
            "contract_id": "NC644_1",
            "next_target": NEXT_TARGET,
            "work_item": "Fill the easiest real bound input first: clocks/spectroscopy alpha sensitivity or WEP composition sensitivity.",
            "acceptance_condition": "source path, unit, observable, and projection formula are present",
        },
        {
            "contract_id": "NC644_2",
            "next_target": NEXT_TARGET,
            "work_item": "Keep parent vertical norm as a dormant theorem contract, not an active claim.",
            "acceptance_condition": "any future proof must explicitly defeat λ_A F_Q², T_Q rescaling, and coframe-factor counterexamples",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D644_0",
            "route": "parent_vertical_norm_zero_theorem",
            "result": "conditional_theorem_written_but_not_parent_signed",
            "decision": "demote_to_closure_contract",
            "why": "existing corpus does not prove fixed T_Q norm, connection projection, unique F_Q² subblock, or same-owner charge current",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D644_1",
            "route": "finite_kappa_alpha_branch",
            "result": "required_next_for_empirical_discipline",
            "decision": "move_to_bound_input_fill",
            "why": "rescaling counterexamples keep alpha_EM as a finite-coupling channel until the parent action forbids them",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "conditional_theorem_written": "true",
            "kappa_alpha_zero_claim": "false",
            "zero_route_demoted": "true",
            "numeric_score_allowed": "false",
            "strongest_positive_result": "we now have the exact theorem and exact counterexamples; this is no longer a vague coupling worry",
            "hardest_blocker": "current corpus does not forbid an independent lambda_A F_Q^2 term or generator/coframe rescaling",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    formula_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    evidence_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V644_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_643_VALIDATION.csv")
    checks.append(("V644_1_prior_643_validation_clean", all(row.get("result") == "pass" for row in prior), "643 validation remains clean"))
    checks.append(("V644_2_conditional_theorem_written", theorem_rows[0]["proof_status"] == "proved_as_conditional_template", "conditional theorem is written"))
    checks.append(("V644_3_unsigned_premises_explicit", any(row["corpus_result"] in {"not_derived", "missing", "failed_current_corpus"} for row in proof_rows), "unsigned premises are explicit"))
    checks.append(("V644_4_formula_ledger_nonclaim", all(row["valid_for_claim"] == "false" for row in formula_rows), "formula rows are nonclaim"))
    checks.append(("V644_5_rescaling_counterexamples_present", len(counter_rows) >= 3 and any(("lambda_A" in row["construction"] or "λ_A" in row["construction"]) for row in counter_rows), "lambda/generator/coframe counterexamples are present"))
    checks.append(("V644_6_evidence_audit_nonclaim", all(row["valid_for_claim"] == "false" for row in evidence_rows), "evidence audit remains nonclaim"))
    checks.append(("V644_7_demote_gate_passes", any(row["gate_id"] == "DG644_3_demote_zero_route" and row["result"] == "pass" for row in demotion_rows), "zero route is demoted in current corpus"))
    checks.append(("V644_8_next_contract_points_to_finite", all(row["next_target"] == NEXT_TARGET for row in next_rows), "next contract points to finite bound input fill"))
    checks.append(("V644_9_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows do not claim pass"))
    checks.append(("V644_10_summary_nonclaim", summary[0]["kappa_alpha_zero_claim"] == "false" and summary[0]["zero_route_demoted"] == "true", "summary marks demotion and no zero claim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V644_11_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    formula_rows: list[dict[str, object]],
    counter_rows: list[dict[str, object]],
    evidence_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 644 Y5/R10 Parent Vertical Norm Coupling Owner Proof or Demotion",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The proof succeeds only as a conditional theorem: if a parent fixed vertical norm and unique curvature subblock exist, then local `kappa_alpha=0` follows.",
        "- The current corpus cannot sign the premises. In particular it does not forbid an independent `lambda_A F_Q^2` term, generator rescaling, or coframe-factor leakage.",
        "- Therefore the theorem-zero route is demoted to a dormant closure contract, and the next disciplined route is finite-coupling bound-input fill.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Conditional Theorem",
        "",
        markdown_table(theorem_rows, ["theorem_id", "name", "proof_status", "corpus_status", "statement"]),
        "",
        "## Proof Step Audit",
        "",
        markdown_table(proof_rows, ["step_id", "required_premise", "corpus_result", "blocking_gap", "logical_result_if_true"]),
        "",
        "## Coupling Formula Ledger",
        "",
        markdown_table(formula_rows, ["formula_id", "formula", "meaning", "owned_if", "current_status"]),
        "",
        "## Rescaling Counterexamples",
        "",
        markdown_table(counter_rows, ["counterexample_id", "construction", "effect", "blocked_only_if"]),
        "",
        "## Evidence Audit",
        "",
        markdown_table(evidence_rows, ["evidence_id", "source", "support", "limit", "supports_proof"]),
        "",
        "## Demotion Gate",
        "",
        markdown_table(demotion_rows, ["gate_id", "gate", "result", "consequence"]),
        "",
        "## Next Contract",
        "",
        markdown_table(next_rows, ["contract_id", "work_item", "acceptance_condition"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "result", "decision", "why"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is a good failure, not a collapse. We now know the exact theorem that would win and the exact counterexamples that block it.",
        "- The local-zero route is not dead forever; it is dormant until a parent action proves literal charge subblock inheritance.",
        "- Until then, treating `kappa_alpha` as finite and bounded is the honest engineering path.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "conditional_theorem_written", "kappa_alpha_zero_claim", "zero_route_demoted", "numeric_score_allowed", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    theorem_rows = conditional_theorem_rows()
    proof_rows = proof_step_rows()
    formula_rows = formula_ledger_rows()
    counter_rows = rescaling_counterexample_rows()
    evidence_rows = evidence_audit_rows()
    demotion_rows = demotion_gate_rows()
    next_rows = next_contract_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(
        source_rows,
        theorem_rows,
        proof_rows,
        formula_rows,
        counter_rows,
        evidence_rows,
        demotion_rows,
        next_rows,
        decision,
        summary,
    )

    write_csv(OUT / "P8_Y5_R10_644_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_644_CONDITIONAL_THEOREM.csv", theorem_rows)
    write_csv(OUT / "P8_Y5_R10_644_PROOF_STEP_AUDIT.csv", proof_rows)
    write_csv(OUT / "P8_Y5_R10_644_COUPLING_FORMULA_LEDGER.csv", formula_rows)
    write_csv(OUT / "P8_Y5_R10_644_RESCALING_COUNTEREXAMPLES.csv", counter_rows)
    write_csv(OUT / "P8_Y5_R10_644_EVIDENCE_AUDIT.csv", evidence_rows)
    write_csv(OUT / "P8_Y5_R10_644_DEMOTION_GATE.csv", demotion_rows)
    write_csv(OUT / "P8_Y5_R10_644_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_644_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_644_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_644_VALIDATION.csv", validation)
    write_doc(source_rows, theorem_rows, proof_rows, formula_rows, counter_rows, evidence_rows, demotion_rows, next_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"proof_steps={len(proof_rows)}")
    print(f"counterexamples={len(counter_rows)}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
