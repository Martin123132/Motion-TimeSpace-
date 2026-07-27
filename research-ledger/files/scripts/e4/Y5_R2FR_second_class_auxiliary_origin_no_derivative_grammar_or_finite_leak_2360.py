from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_SECOND_CLASS_AUXILIARY_NO_DERIVATIVE_GRAMMAR_OR_FINITE_LEAK_2360"
SOURCE_BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2360-Y5-R2FR-second-class-auxiliary-origin-no-derivative-grammar-or-finite-leak.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def false_claim_columns(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "numeric_value_present": "false",
        "source_backed": "false",
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC2360_2359_selector",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2359_NOPOLE_SELECTOR_GATE.csv",
            "needle": "NPS2359_0_second_class_auxiliary",
            "role": "selects the second-class auxiliary/no-pole route as the next derivation target",
        },
        {
            "source_id": "SRC2360_2359_inputs",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2359_NEXT_INPUT_REQUIREMENTS.csv",
            "needle": "INP2359_0_parent_origin",
            "role": "lists parent origin, no-derivative grammar, zero-stress reaction, and boundary/readout stability as missing",
        },
        {
            "source_id": "SRC2360_1562_origin",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv",
            "needle": "ORG1562_3_second_class_auxiliary",
            "role": "identifies the algebraic auxiliary route as the best conditional repair target",
        },
        {
            "source_id": "SRC2360_1562_stress",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_ZERO_STRESS_VARIATION_GATE.csv",
            "needle": "STR1562_2_aux_E_R",
            "role": "records the E_R reaction equation and source-zero condition",
        },
        {
            "source_id": "SRC2360_1576_constraint",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
            "needle": "CNP1576_5_verdict",
            "role": "shows that current no-pole/local-GR claim remains blocked",
        },
        {
            "source_id": "SRC2360_1576_fallback",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1576_RAB_FINITE_FALLBACK_COMPONENT_ROWS.csv",
            "needle": "FF1576_0_constraint_origin",
            "role": "defines the fallback finite component rows when no-pole is unsigned",
        },
        {
            "source_id": "SRC2360_1621_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1621_NO_POLE_THEOREM_AUDIT.csv",
            "needle": "NPA1621_0_conditional_theorem",
            "role": "records the earlier conditional no-pole theorem but keeps it unclaimed",
        },
        {
            "source_id": "SRC2360_1268_candidate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
            "needle": "CAC1268_5_conditional_theorem",
            "role": "gives the second-class compatibility action candidate and theorem clauses",
        },
        {
            "source_id": "SRC2360_1268_variation",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1268_VARIATIONAL_ELIMINATION_AUDIT.csv",
            "needle": "VAR1268_1_E_R",
            "role": "states Lambda_R plus source, boundary, and readout terms in the R_AB variation",
        },
        {
            "source_id": "SRC2360_1248_dirac",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1248_DIRAC_CHECK.csv",
            "needle": "DIR1248_2_preservation",
            "role": "shows the older lambda_R ansatz still lacks Hamiltonian/bracket closure",
        },
        {
            "source_id": "SRC2360_1561_variation",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1561_EULER_VARIATION_GATE.csv",
            "needle": "EUL1561_2_lambda_stress",
            "role": "flags lambda_R metric stress silence as unsigned",
        },
    ]
    for row in sources:
        path = POST_ROOT / str(row["source_path"])
        row["path_exists"] = bool_text(path.exists())
        row["needle_found"] = bool_text(contains(path, str(row["needle"])))
        row["valid_for_claim"] = "false"
    return sources


def theorem_audit() -> list[dict[str, object]]:
    base = {
        "branch_id": BRANCH_ID,
        "source_branch_id": SOURCE_BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    return [
        {
            **base,
            "row_id": "SCA2360_0_conditional_theorem",
            "clause": "exact auxiliary no-pole theorem",
            "statement": "If the parent action contains S_R=int mu_parent Lambda_R [R_AB-C_AB(q(Phi),theta,top)], R_AB and Lambda_R are algebraic auxiliaries, no derivative or kinetic pole is legal, matter descends through q, boundary/readout terms do not re-enter R_AB, and E_R sets Lambda_R=0, then the R_AB sector is eliminated before local readout and carries no local Yukawa/source pole.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_WRITTEN",
            "missing": "parent origin; parent field sort; no-derivative operator exclusion; source-zero descent; boundary/readout silence",
            "effect": "this is the cleanest local-GR route if every clause can be parent-signed",
        },
        {
            **base,
            "row_id": "SCA2360_1_parent_origin",
            "clause": "parent origin of Lambda_R/C_R",
            "statement": "Lambda_R C_R must arise from a phase-cell/current-chain/compatibility identity in the parent action rather than being inserted to force R_AB=0.",
            "current_status": "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "missing": "source-backed derivation of C_R and variation class",
            "effect": "without this the construction is closure, not derivation",
        },
        {
            **base,
            "row_id": "SCA2360_2_no_derivative_grammar",
            "clause": "operator grammar",
            "statement": "The parent operator grammar must exclude D R_AB, D Lambda_R, a vertical kinetic metric, Green kernels, and boundary derivative operators for this sector.",
            "current_status": "MISSING_OPERATOR_SIGNATURE",
            "missing": "operator-exhaustion theorem or parent sort that forbids those terms",
            "effect": "if a kinetic channel is legal, finite q_R/R10/PPN leak rows remain live",
        },
        {
            **base,
            "row_id": "SCA2360_3_E_lambda",
            "clause": "E_Lambda equation",
            "statement": "delta_{Lambda_R} S_R gives R_AB-C_AB(q(Phi),theta,top)=0 inside the candidate action.",
            "current_status": "FORMAL_PASS_WITHIN_CANDIDATE",
            "missing": "candidate block must still be parent-owned",
            "effect": "sets compatibility only after the candidate is accepted",
        },
        {
            **base,
            "row_id": "SCA2360_4_E_R_zero_stress",
            "clause": "E_R reaction stress",
            "statement": "delta_{R_AB} S_total gives Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0, so Lambda_R=0 only if direct matter source, boundary tail, and readout regeneration vanish.",
            "current_status": "PASS_ONLY_IF_SOURCES_ZERO",
            "missing": "matter descent, boundary zero, and readout stability",
            "effect": "lambda_R stress silence is not a free consequence of R_AB=0",
        },
        {
            **base,
            "row_id": "SCA2360_5_matter_boundary_readout",
            "clause": "descent and boundary silence",
            "statement": "S_matter, clocks, photons, orbital readouts, and boundary terms must factor through q(Phi), theta, and public geometry with no direct R_AB slot.",
            "current_status": "MISSING_DESCENT_AND_BOUNDARY_CERTIFICATE",
            "missing": "source map, edge mode map, readout EFT closure",
            "effect": "observables can regenerate the same local residual the theorem tries to remove",
        },
        {
            **base,
            "row_id": "SCA2360_6_verdict",
            "clause": "2360 verdict",
            "statement": "The derivation route is sharpened into an exact contract, but the current corpus does not yet parent-sign the origin/no-derivative/source-boundary clauses.",
            "current_status": "CONDITIONAL_THEOREM_NOT_CLOSED_FOR_CLAIM",
            "missing": "parent origin remains the first lock",
            "effect": "move next to deriving C_R from phase-cell/current-chain structure or keep finite q_R rows",
        },
    ]


def no_derivative_grammar_gate() -> list[dict[str, object]]:
    rows = [
        ("NDG2360_0_DRAB_bulk", "bulk derivative terms", "D_mu R_AB and D_mu Lambda_R are forbidden", "MISSING_OPERATOR_EXCLUSION_PROOF", "would create a propagating or Yukawa-like reciprocal mode"),
        ("NDG2360_1_vertical_metric", "vertical metric channel", "no G_vert^{ABCD} D R_AB D R_CD exists in the auxiliary branch", "MISSING_VERTICAL_NULL_THEOREM", "would make Z_R a real parameter needing bounds"),
        ("NDG2360_2_hessian_rank", "Hessian/Dirac rank", "R_AB and Lambda_R have no invertible kinetic Hessian and form an eliminable auxiliary pair", "MISSING_HESSIAN_RANK_CERTIFICATE", "would leave a local pole or hidden degree of freedom"),
        ("NDG2360_3_boundary_derivatives", "boundary derivative terms", "corner/edge action contains no normal derivative charge for R_AB", "MISSING_BOUNDARY_OPERATOR_EXCLUSION", "would leave Q_R/Pi_R boundary hair"),
        ("NDG2360_4_direct_source", "direct matter/source slot", "matter has no direct R_AB coupling before readout", "MISSING_MATTER_DESCENT", "would make J_R nonzero"),
        ("NDG2360_5_readout_regen", "readout regeneration", "effective readout cannot regenerate Z_R, J_R, or B_R after elimination", "MISSING_READOUT_STABILITY", "would reintroduce the local residual downstream"),
        ("NDG2360_6_verdict", "operator grammar verdict", "no-derivative grammar is necessary and not yet parent-signed", "BLOCKS_NO_POLE_CLAIM", "finite leak rows remain required"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "required_signature": required,
            "current_status": status,
            "failure_effect": effect,
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, required, status, effect in rows
    ]


def zero_stress_reaction_gate() -> list[dict[str, object]]:
    rows = [
        ("ZSR2360_0_E_lambda", "delta_{Lambda_R} S_R", "R_AB-C_AB(q,theta,top)=0", "FORMAL_PASS_WITHIN_CANDIDATE", "not enough without parent origin"),
        ("ZSR2360_1_E_R", "delta_{R_AB} S_total", "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0", "EXACT_CONDITIONAL_ONLY", "Lambda_R=0 follows only if every source term vanishes"),
        ("ZSR2360_2_metric_stress", "delta_g S_R", "constraint stress must vanish after auxiliary elimination", "MISSING_REACTION_STRESS_THEOREM", "unowned stress could spoil local GR"),
        ("ZSR2360_3_source_zero", "direct source variation", "J_R=0 from matter descent", "MISSING_SOURCE_DESCENT", "finite source-current amplitude remains live"),
        ("ZSR2360_4_boundary_zero", "boundary/corner variation", "delta B_R/delta R_AB=0 or exact/proper with no local charge", "MISSING_BOUNDARY_SILENCE", "boundary tail remains live"),
        ("ZSR2360_5_readout_zero", "post-elimination readout", "readout_regen=0", "MISSING_READOUT_STABILITY", "downstream EFT can regenerate the residual"),
        ("ZSR2360_6_verdict", "zero-stress verdict", "lambda_R is stress silent only inside the full auxiliary contract", "BLOCKS_LOCAL_GR_CLAIM", "local PPN branch still needs derivation or finite bounds"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "variation": variation,
            "required_result": result,
            "current_status": status,
            "failure_effect": effect,
            "parent_signed": "false" if "FORMAL" not in status else "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, variation, result, status, effect in rows
    ]


def finite_leak_rows() -> list[dict[str, object]]:
    rows = [
        ("FL2360_0_C_lambda_origin", "C_R/Lambda_R parent origin", "derive C_R from parent phase-cell/current-chain identity", "MISSING_PARENT_CONSTRAINT_ORIGIN", "chooses theorem route versus closure"),
        ("FL2360_1_Z_R", "Z_R kinetic coefficient", "prove theorem-zero or source numeric value, unit, and source path", "MISSING_OPERATOR_SIGNATURE", "sets local pole strength if kinetic route survives"),
        ("FL2360_2_M_R2", "M_R^2 algebraic mass/stiffness", "source positive finite value or prove auxiliary elimination", "MISSING_MASS_STIFFNESS_INPUT", "sets lambda_R/range if no-pole fails"),
        ("FL2360_3_J_R", "direct source current", "prove J_R=0 by matter descent or source finite beta values", "MISSING_SOURCE_CHARGE_RESOLUTION", "sets R10/PPN bulk amplitude"),
        ("FL2360_4_B_R", "boundary/corner tail", "prove exact/proper/zero boundary charge or source finite tail", "MISSING_BOUNDARY_RESOLUTION", "sets long-range exterior leakage"),
        ("FL2360_5_Dq_leak", "observable projection leak", "prove Dq_R=0 or source projection norm", "MISSING_ARENA_PROJECTION", "sets clock, orbital, EM, and PPN readout residuals"),
        ("FL2360_6_tau_arena", "arena transfer coefficients", "source tau_R10, tau_PPN, tau_clock, tau_orbital", "MISSING_ARENA_TRANSFER_INPUTS", "needed for any empirical local-branch comparison"),
        ("FL2360_7_public_claim_state", "claim readiness", "all finite rows numeric, sourced, unit-checked, and below bounds", "NOT_SCORE_READY", "no local-GR/R10/WEP/PPN/clock/orbital pass is allowed"),
    ]
    return [
        {
            **false_claim_columns(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "required_resolution": required,
            "current_status": status,
            "score_effect": effect,
        }
        for row_id, quantity, required, status, effect in rows
    ]


def route_decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2360_0_exact_contract", "second-class auxiliary/no-pole route", 1, "KEEP_AS_BEST_THEOREM_ROUTE", "it removes the local residual before matter coupling instead of calling it gauge"),
        ("DEC2360_1_parent_origin", "derive C_R/Lambda_R origin", 1, "SELECT_NEXT_ATTACK", "the source register shows parent origin is the first repeated missing clause"),
        ("DEC2360_2_operator_grammar", "no-derivative operator exclusion", 2, "NEXT_AFTER_ORIGIN", "the operator ban only has force once the parent sort and C_R origin exist"),
        ("DEC2360_3_finite_rows", "finite q_R/source-current leak branch", 3, "KEEP_NONCLAIM_FALLBACK", "needed if the parent origin or no-derivative grammar fails"),
        ("DEC2360_4_public_status", "local-GR claim status", 0, "DO_NOT_CLAIM_LOCAL_GR_PASS", "the route is disciplined but still unsigned"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("GATE2360_0_parent_origin", "parent origin signed", "blocked", "C_R/Lambda_R not derived from parent phase-cell/current-chain identity"),
        ("GATE2360_1_operator_grammar", "no derivative grammar signed", "blocked", "D R_AB / kinetic / boundary derivative exclusion is not parent-proved"),
        ("GATE2360_2_zero_stress", "reaction stress silence proved", "blocked", "Lambda_R=0 needs source, boundary, and readout zero"),
        ("GATE2360_3_matter_descent", "matter/readout descent proved", "blocked", "observable sectors can still source or regenerate R_AB"),
        ("GATE2360_4_finite_bounds", "fallback rows numeric and sourced", "blocked", "finite leak rows are placeholders only"),
        ("GATE2360_5_verdict", "R10/WEP/PPN/local-GR pass", "blocked", "no public pass from 2360"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "status": status.upper(),
            "reason": reason,
            "passes_public_claim": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2360_0_magic_multiplier", "refuse S_lambda=int lambda_R R_AB as a derivation by itself", "PASS_REFUSAL", "formal variation is not parent origin"),
        ("REF2360_1_GR_import", "refuse importing Schwarzschild AB=1 or Einstein vacuum equations as proof", "PASS_REFUSAL", "would replace MTS derivation with GR result"),
        ("REF2360_2_hidden_kinetic", "refuse no-pole claim while a legal kinetic/counterterm channel is unsigned", "PASS_REFUSAL", "keeps finite branch live"),
        ("REF2360_3_hidden_source", "refuse local-GR pass while matter/readout can source R_AB", "PASS_REFUSAL", "protects PPN/R10/clock/orbital gates"),
        ("REF2360_4_public_claim", "refuse public R10/WEP/local-GR claim from this checkpoint", "PASS_REFUSAL", "2360 is a derivation contract plus blocker ledger"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "refusal": refusal,
            "status": status,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, refusal, status, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2360_0_selected",
            "next_file": "2361-Y5-R2FR-parent-origin-of-CR-from-phase-cell-current-chain-or-finite-qR-row.md",
            "next_script": "scripts/Y5_R2FR_parent_origin_of_CR_from_phase_cell_current_chain_or_finite_qR_row_2361.py",
            "selected_reason": "parent origin is the first repeated missing clause across 1561, 1562, 1576, 1621, and 2359",
            "success_condition": "derive C_R/Lambda_R from parent phase-cell/current-chain/compatibility structure without importing GR or inserting a closure multiplier",
            "fallback_condition": "if parent origin fails, promote finite q_R source/current rows as the honest branch",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
    ]


def branch_copies() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "COPY2360_0_source_branch",
            "copied_from": SOURCE_BRANCH_ID,
            "branch_role": "local residual/R10/WEP finite-source branch retained as source context",
            "copy_type": "nonclaim_reference",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "COPY2360_1_route_branch",
            "copied_from": "MTS_R2FR_PARENT_Q_FIELD_CHART_EQUIV_OR_NOPOLE_SELECTOR_2359",
            "branch_role": "inherits selector decision that the second-class auxiliary route is the next derivation attack",
            "copy_type": "nonclaim_route_continuation",
            "valid_for_claim": "false",
        },
    ]


def formalization_status() -> tuple[str, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return "PASS", "formalization-workbench path does not exist; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return "PASS", f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        if not changed:
            return "PASS", "git modified-file count for formalization-workbench is 0"
        return "FAIL", f"formalization-workbench has {len(changed)} git status rows"
    return "PASS", "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    forbidden_pairs = [
        ("valid_for_claim", "true"),
        ("claim_allowed", "true"),
        ("passes_public_claim", "true"),
        ("score_ready", "true"),
        ("valid_prediction_row", "true"),
        ("parent_signed", "true"),
        ("source_backed", "true"),
        ("numeric_value_present", "true"),
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            for key, bad_value in forbidden_pairs:
                if row.get(key, "").strip().lower() == bad_value:
                    offenders.append(f"{rel(path)}:{row.get('row_id', row.get('source_id', '?'))}:{key}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def write_markdown(outputs: dict[str, Path]) -> None:
    theorem_rows = read_csv(outputs["theorem"])
    ndg_rows = read_csv(outputs["grammar"])
    zsr_rows = read_csv(outputs["stress"])
    finite_rows = read_csv(outputs["finite"])
    decision_rows = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    def table(headers: list[str], rows: list[dict[str, str]]) -> str:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
        return "\n".join(lines)

    md = f"""# 2360 — Second-Class Auxiliary Origin, No-Derivative Grammar, Or Finite Leak

## Result

The best local-GR/R10 route is now sharpened into a precise conditional theorem, not promoted into a claim.  The clean route is:

`S_R = int mu_parent Lambda_R [R_AB - C_AB(q(Phi), theta, top)]`

If this block is parent-owned, purely algebraic, source-silent, boundary-silent, and readout-stable, then `R_AB` and `Lambda_R` can be eliminated before local readout and no reciprocal local pole remains.  Current MTS does not yet sign those clauses.  The first missing lock is the parent origin of `C_R/Lambda_R`.

## Theorem Audit

{table(["row_id", "clause", "current_status", "missing", "effect"], theorem_rows)}

## No-Derivative Grammar Gate

{table(["row_id", "gate", "current_status", "failure_effect"], ndg_rows)}

## Zero-Stress Reaction Gate

{table(["row_id", "variation", "current_status", "failure_effect"], zsr_rows)}

## Finite Leak Rows

{table(["row_id", "quantity", "current_status", "score_effect"], finite_rows)}

## Route Decision

{table(["row_id", "route", "rank", "decision", "reason"], decision_rows)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["theorem"])}`
- `{rel(outputs["grammar"])}`
- `{rel(outputs["stress"])}`
- `{rel(outputs["finite"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["gates"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["copies"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is good news structurally but not a victory lap.  The route is no longer vague: it says exactly what a parent action must do.  It also blocks the cheap move: a multiplier alone is not enough.  Next we attack `C_R` itself and ask whether it comes from a phase-cell/current-chain/compatibility identity, or whether the honest branch is a finite residual to be bounded.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "row_id": row_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2360_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2360_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2360_02_outputs_exist", all(path.exists() for path in generated), "all 2360 output files written")

    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2360_03_csv_parse", parse_ok, parse_detail)

    theorem_statuses = {row["row_id"]: row["current_status"] for row in read_csv(outputs["theorem"])}
    add(
        "VAL2360_04_conditional_theorem_recorded",
        theorem_statuses.get("SCA2360_0_conditional_theorem") == "EXACT_CONDITIONAL_THEOREM_WRITTEN",
        "conditional auxiliary no-pole theorem recorded",
    )
    add(
        "VAL2360_05_no_pole_not_promoted",
        theorem_statuses.get("SCA2360_6_verdict") == "CONDITIONAL_THEOREM_NOT_CLOSED_FOR_CLAIM",
        "verdict keeps no-pole/local-GR route unclaimed",
    )

    finite = read_csv(outputs["finite"])
    finite_nonclaim = all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in finite)
    add("VAL2360_06_finite_rows_nonclaim", finite_nonclaim, "all finite leak rows remain nonclaim and not score-ready")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2360_07_no_positive_claim_flags", flag_ok, flag_detail)

    next_selected = read_csv(outputs["next"])[0].get("row_id") == "NEXT2360_0_selected"
    add("VAL2360_08_next_selected", next_selected, "2361 parent-origin target selected")

    formal_status, formal_detail = formalization_status()
    add("VAL2360_09_formalization_untouched", formal_status == "PASS", formal_detail)

    gates_blocked = all(row.get("passes_public_claim") == "false" for row in read_csv(outputs["gates"]))
    add("VAL2360_10_claim_gates_blocked", gates_blocked, "all public claim gates remain blocked")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2360_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2360 checkpoint valid: derivation contract written, no claims promoted, next target selected" if overall else "one or more validation gates failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_SOURCE_REGISTER.csv",
        "theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_SECOND_CLASS_AUXILIARY_THEOREM_AUDIT.csv",
        "grammar": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_NO_DERIVATIVE_GRAMMAR_GATE.csv",
        "stress": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_ZERO_STRESS_REACTION_GATE.csv",
        "finite": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_FINITE_LEAK_ROWS.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_ROUTE_DECISION_LEDGER.csv",
        "gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_NEXT_TARGET.csv",
        "copies": RESIDUALS / "P8_Y5_PARENT_QLOC_2360_BRANCH_COPIES.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2360_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["theorem"], theorem_audit())
    write_csv(outputs["grammar"], no_derivative_grammar_gate())
    write_csv(outputs["stress"], zero_stress_reaction_gate())
    write_csv(outputs["finite"], finite_leak_rows())
    write_csv(outputs["decision"], route_decision_ledger())
    write_csv(outputs["gates"], claim_gates())
    write_csv(outputs["refusal"], refusal_runner())
    write_csv(outputs["next"], next_target())
    write_csv(outputs["copies"], branch_copies())

    validation = validation_rows(outputs, sources)
    write_csv(outputs["validation"], validation)
    write_markdown(outputs)

    for row in validation:
        print(f"{row['row_id']},{row['status']},{row['detail']}")
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
