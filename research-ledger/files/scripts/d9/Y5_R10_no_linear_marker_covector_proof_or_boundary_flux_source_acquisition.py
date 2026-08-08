from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "975-Y5-R10-no-linear-marker-covector-proof-or-boundary-flux-source-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.timestamp()
    count = 0
    try:
        for directory, _subdirs, filenames in os.walk(FORMALIZATION):
            for filename in filenames:
                path = Path(directory) / filename
                try:
                    if path.stat().st_mtime > since:
                        count += 1
                except OSError:
                    return -2
    except OSError:
        return -2
    return count


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "974_doc",
            "path": "974-Y5-R10-zero-origin-evenness-theorem-or-boundary-flux-coefficient-fill.md",
            "role": "handoff selecting no-linear-marker covector or alpha3 coefficient source",
            "needle": "975-Y5-R10-no-linear-marker-covector-proof-or-boundary-flux-source-acquisition.md",
        },
        {
            "source_id": "974_marker_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv",
            "role": "current ell(X) and material/domain/readout marker counterexamples",
            "needle": "MCE974_0_linear_marker_covector",
        },
        {
            "source_id": "974_origin_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_974_PARENT_ORIGIN_ACCEPTANCE_GATE.csv",
            "role": "current missing no-linear-marker parent gate",
            "needle": "POA974_3_no_linear_marker",
        },
        {
            "source_id": "413_doc",
            "path": "413-no-marker-parent-action-theorem-attempt.md",
            "role": "fixed-spurion partial theorem and co-moving marker failure",
            "needle": "co_moving_marker_test",
        },
        {
            "source_id": "413_marker_defs",
            "path": "runs/20260602-063500-no-marker-parent-action-theorem-attempt/results/marker_definitions.csv",
            "role": "marker taxonomy from original no-marker theorem attempt",
            "needle": "co_moving_material_marker",
        },
        {
            "source_id": "413_chain",
            "path": "runs/20260602-063500-no-marker-parent-action-theorem-attempt/results/no_marker_theorem_chain.csv",
            "role": "no-marker theorem chain with material extension and invariant algebra blockers",
            "needle": "Material marker extension is also forbidden.",
        },
        {
            "source_id": "414_doc",
            "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
            "role": "local invariant algebra triviality condition and surviving generators",
            "needle": "strong_local_triviality",
        },
        {
            "source_id": "573_doc",
            "path": "573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md",
            "role": "primitive-minimal no-marker reduction to invariant algebra triviality",
            "needle": "PM573_3_local_invariant_algebra",
        },
        {
            "source_id": "573_chain",
            "path": "source-intake/mts_residuals/P8_Y5_R10_573_NO_MARKER_REDUCTION_CHAIN.csv",
            "role": "reduction chain: primitive domain, invariant algebra, qbar zero",
            "needle": "RC573_1_invariant_algebra",
        },
        {
            "source_id": "573_generator_debt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
            "role": "surviving local invariant generator debts",
            "needle": "IG573_3_memory_scalar",
        },
        {
            "source_id": "574_attack_order",
            "path": "source-intake/mts_residuals/P8_Y5_R10_574_GENERATOR_ATTACK_ORDER.csv",
            "role": "ranked generator elimination order",
            "needle": "post_readout_projector",
        },
        {
            "source_id": "575_readout_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_READOUT_LOCK_CONTRACT.csv",
            "role": "readout-after-variation no-cheat contract",
            "needle": "RL575_1_solution_space_readout",
        },
        {
            "source_id": "575_constant_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
            "role": "constant/source sector marker-dependence blockers",
            "needle": "CL575_1_trivial_MTS_action",
        },
        {
            "source_id": "608_counterexamples",
            "path": "source-intake/mts_residuals/P8_Y5_R10_608_COUNTEREXAMPLE_GATE.csv",
            "role": "linear marker covector and conformal matter counterexamples",
            "needle": "CE608_0_linear_marker_covector",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "alpha3/Gdot pressure anchors for coefficient acquisition fallback",
            "needle": "alpha3_flux",
        },
    ]
    rows = []
    for spec in specs:
        absolute_path = source_path(spec["path"])
        exists = absolute_path.exists()
        needle_found = spec["needle"] in read_text(absolute_path) if exists else False
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def no_linear_marker_theorem_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "step_id": "NLM975_0_problem",
            "claim_piece": "linear marker covector is the obstruction",
            "mathematical_form": "F(X)=F(0)+ell(X)+1/2 H_X(X,X)+...",
            "status": "OBSTRUCTION_IDENTIFIED",
            "proof_status": "ell in E_X* sources J_X(0) unless forbidden",
            "gap": "need a parent reason ell cannot exist",
        },
        {
            "step_id": "NLM975_1_fixed_spurion",
            "claim_piece": "fixed labelled covectors are not quotient functions",
            "mathematical_form": "ell_fixed(g.X) != ell_fixed(X), so ell_fixed is inadmissible on E_X/G_X",
            "status": "CONDITIONAL_PASS",
            "proof_status": "strict quotient parent action kills fixed non-orbit covectors",
            "gap": "strict quotient parent space still needs full parent signature for every local branch",
        },
        {
            "step_id": "NLM975_2_invariant_covector_lemma",
            "claim_piece": "no invariant dual vector means no linear scalar",
            "mathematical_form": "ell in (E_X*)^G_X; if (E_X*)^G_X=0 then ell=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "proof_status": "group-invariant parent scalar cannot contain a non-invariant linear functional",
            "gap": "current corpus has not parent-proved G_X, E_X, and no-trivial-dual-subrepresentation",
        },
        {
            "step_id": "NLM975_3_natural_marker_functor",
            "claim_piece": "material/domain covectors require an E_X*-valued natural marker functor",
            "mathematical_form": "m: I_loc(Q_MTS) -> E_X*; if I_loc=I_geom tensor Const and E_X has no trivial dual, then m=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "proof_status": "local invariant algebra triviality plus nontrivial fibre representation kills covector construction",
            "gap": "414/573 keep finite fibre, domain class, chi_D, memory scalar, species constants, and readout projector generators alive",
        },
        {
            "step_id": "NLM975_4_readout_after_variation",
            "claim_piece": "post-readout projector cannot source parent X",
            "mathematical_form": "R_read: Sol(S_parent)/G -> Obs and R_read notin Args(S_parent)",
            "status": "CONDITIONAL_NO_CHEAT_LOCK",
            "proof_status": "if readout is only after variation, delta_X S_parent has no readout marker term",
            "gap": "575 writes the contract but not a full parent-domain audit",
        },
        {
            "step_id": "NLM975_5_co_moving_marker_failure",
            "claim_piece": "co-moving material marker extension remains legal",
            "mathematical_form": "Q_tilde=(Q_MTS,m)/G_rel and ell_m(X) can descend as quotient data",
            "status": "FAIL_CURRENT_CORPUS",
            "proof_status": "quotient invariance alone does not forbid extended quotient objects",
            "gap": "requires primitive minimality/no-extension theorem not currently derived",
        },
        {
            "step_id": "NLM975_6_constant_sector_failure",
            "claim_piece": "matter constants/source weights can carry marker dependence",
            "mathematical_form": "theta_A=theta_A(I_Q,m) or kappa_A=kappa_A(I_Q,m)",
            "status": "FAIL_CURRENT_CORPUS",
            "proof_status": "constant-sector universality remains a separate parent theorem",
            "gap": "575 CL575_1/CL575_4 not parent-derived",
        },
        {
            "step_id": "NLM975_7_verdict",
            "claim_piece": "no-linear-marker covector theorem",
            "mathematical_form": "strict quotient + (E_X*)^G_X=0 + no E_X*-valued marker functor would force ell=0",
            "status": "REPRESENTATION_THEOREM_DERIVED_PARENT_UNSIGNED",
            "proof_status": "the exact theorem shape is now cleaner than a bare no-marker slogan",
            "gap": "not a local-GR claim because invariant algebra triviality/no-extension/constant universality remain unsigned",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def marker_classification() -> list[dict[str, str]]:
    specs = [
        {
            "marker_id": "MC975_0_fixed_spurion",
            "marker_type": "fixed active covector or labelled mask",
            "current_status": "CONDITIONAL_EXCLUDED",
            "reason": "not orbit-constant on the strict quotient",
            "remaining_work": "parent-sign strict quotient configuration space",
        },
        {
            "marker_id": "MC975_1_co_moving_material_marker",
            "marker_type": "m transforms with the system and descends to Q_tilde",
            "current_status": "NOT_EXCLUDED",
            "reason": "quotient invariance allows extended quotient data unless primitive minimality forbids it",
            "remaining_work": "derive parent no-extension/minimality theorem",
        },
        {
            "marker_id": "MC975_2_domain_class_marker",
            "marker_type": "relative boundary/domain class or chi_D selector",
            "current_status": "NOT_EXCLUDED",
            "reason": "414/573/574 keep domain class and selector generators alive",
            "remaining_work": "derive local trivial class and Bianchi-safe selector silence",
        },
        {
            "marker_id": "MC975_3_species_constant_marker",
            "marker_type": "theta_A(I_Q,m), q_A(I_Q), or kappa_A source weight",
            "current_status": "NOT_EXCLUDED",
            "reason": "constant-sector universality and universal source current are not parent-derived",
            "remaining_work": "prove constants are representation data with trivial MTS action",
        },
        {
            "marker_id": "MC975_4_post_readout_marker",
            "marker_type": "projector/readout selected reduced action",
            "current_status": "CONDITIONAL_NO_CHEAT_RULE",
            "reason": "readout-after-variation blocks it if enforced as parent-domain absence",
            "remaining_work": "audit that no reduced readout action is varied as parent source",
        },
        {
            "marker_id": "MC975_5_boundary_flux_source",
            "marker_type": "not an ell covector but still sources X through boundary/local projection",
            "current_status": "NOT_EXCLUDED",
            "reason": "417/974 keep alpha3/Gdot flux anchors but no K_boundary coefficient",
            "remaining_work": "derive boundary no-flux or source K_boundary_alpha3",
        },
        {
            "marker_id": "MC975_6_verdict",
            "marker_type": "all marker families",
            "current_status": "FIXED_SPURION_ONLY_PARTIALLY_KILLED",
            "reason": "material/domain/constant/readout/boundary routes survive as current legal alternatives",
            "remaining_work": "do not promote qbar_XT, J_X=0, p>=2, R10, PPN, or local-GR from this theorem yet",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def invariant_covector_gate() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "ICG975_0_parent_group_action",
            "required_input": "parent-defined local marker symmetry group G_X acting on E_X",
            "current_evidence": "inferred theorem target from 608/609/974, not parent-owned",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_GX_ACTION",
        },
        {
            "gate_id": "ICG975_1_nontrivial_dual",
            "required_input": "no invariant covector in the dual representation",
            "current_evidence": "representation-theoretic gate newly stated",
            "gate_pass": "false",
            "missing_input": "MISSING_PROOF_E_X_DUAL_INVARIANTS_ZERO",
        },
        {
            "gate_id": "ICG975_2_primitive_X",
            "required_input": "X is a primitive E_X amplitude, not a derived readout proxy",
            "current_evidence": "974/609 keep primitive ownership unsigned",
            "gate_pass": "false",
            "missing_input": "MISSING_PRIMITIVE_X_PARENT_OWNERSHIP",
        },
        {
            "gate_id": "ICG975_3_local_invariant_algebra",
            "required_input": "I_loc(Q_MTS)=I_geom tensor Const on compact local branch",
            "current_evidence": "414/573 reduce the problem here but leave generators alive",
            "gate_pass": "false",
            "missing_input": "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
        },
        {
            "gate_id": "ICG975_4_no_extension",
            "required_input": "co-moving material marker extension Q_tilde is inadmissible",
            "current_evidence": "413 and 573 say this is not derived",
            "gate_pass": "false",
            "missing_input": "MISSING_PARENT_NO_EXTENSION_THEOREM",
        },
        {
            "gate_id": "ICG975_5_readout_domain",
            "required_input": "readout-after-variation is enforced as parent-domain absence",
            "current_evidence": "575 gives formal no-cheat contract but not full parent audit",
            "gate_pass": "false",
            "missing_input": "MISSING_READOUT_PARENT_DOMAIN_AUDIT",
        },
        {
            "gate_id": "ICG975_6_boundary_silence",
            "required_input": "boundary flux does not source X or has sourced coefficient below bounds",
            "current_evidence": "974 writes non-scoreable alpha3/Gdot anchors",
            "gate_pass": "false",
            "missing_input": "MISSING_BOUNDARY_FLUX_ZERO_OR_K_ALPHA3",
        },
        {
            "gate_id": "ICG975_7_verdict",
            "required_input": "all invariant-covector gates close",
            "current_evidence": "relative theorem only",
            "gate_pass": "false",
            "missing_input": "MISSING_NO_LINEAR_MARKER_PARENT_CERTIFICATE",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def alpha3_coefficient_acquisition() -> list[dict[str, str]]:
    specs = [
        {
            "row_id": "ACQ975_0_prediction_formula",
            "arena": "PPN/preferred-frame",
            "quantity": "boundary-flux alpha3 prediction formula",
            "symbolic_form": "alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local",
            "bound_or_anchor": "abs(alpha3_MTS) <= 4.000e-20",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "status": "FORMULA_STUB_NON_SCOREABLE",
            "missing_inputs": "MISSING_K_BOUNDARY_ALPHA3;MISSING_PHI_BOUNDARY_LOCAL;MISSING_PROJECTION_NORMALIZATION",
        },
        {
            "row_id": "ACQ975_1_bound_anchor",
            "arena": "PPN/preferred-frame",
            "quantity": "alpha3 hard local pressure anchor",
            "symbolic_form": "alpha3_flux",
            "bound_or_anchor": "4.000e-20 dimensionless",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "status": "SOURCE_BACKED_BOUND_ANCHOR",
            "missing_inputs": "MISSING_CLAIM_GRADE_PARENT_COEFFICIENT",
        },
        {
            "row_id": "ACQ975_2_minimum_inputs",
            "arena": "coefficient acquisition",
            "quantity": "minimum executable inputs for scoring",
            "symbolic_form": "K_boundary_alpha3, Phi_boundary_local, units, sign, source path, projection map",
            "bound_or_anchor": "runner compares abs(predicted) to anchor",
            "source_path": "975-Y5-R10-no-linear-marker-covector-proof-or-boundary-flux-source-acquisition.md",
            "status": "INPUT_CONTRACT_WRITTEN",
            "missing_inputs": "MISSING_NUMERIC_VALUES_AND_UNITS",
        },
        {
            "row_id": "ACQ975_3_no_claim_rule",
            "arena": "all local",
            "quantity": "claim gate",
            "symbolic_form": "claim_allowed=false until theorem-zero or numeric pass",
            "bound_or_anchor": "G507_0 theorem-zero policy",
            "source_path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "status": "FORCED_FALSE",
            "missing_inputs": "MISSING_THEOREM_ZERO_OR_EXECUTABLE_BOUND_PASS",
        },
    ]
    return [
        {
            **spec,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def claim_gates() -> list[dict[str, str]]:
    specs = [
        {
            "gate_id": "CGATE975_0_invariant_covector_zero",
            "claim": "ell(X)=0 follows from parent representation symmetry",
            "current_evidence": "relative theorem derived, but G_X/E_X/no-dual-invariant parent signature missing",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE975_1_material_marker_absent",
            "claim": "co-moving material/domain/readout markers are absent",
            "current_evidence": "413/414/573/574/575 keep multiple generator routes alive",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE975_2_p2_normsquare_promotion",
            "claim": "p>=2 norm-square route can be promoted",
            "current_evidence": "no-linear-marker parent certificate is still absent",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE975_3_alpha3_bound_score",
            "claim": "boundary alpha3 coefficient row is executable and below bound",
            "current_evidence": "formula stub and source-backed anchor exist; K/Phi/projection units are missing",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE975_4_local_GR",
            "claim": "local GR/Newton reduction follows from no-marker route",
            "current_evidence": "no-marker theorem and boundary coefficient pass are both incomplete",
            "gate_pass": "false",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def decisions() -> list[dict[str, str]]:
    specs = [
        {
            "decision_id": "DEC975_0_theorem_shape",
            "topic": "no-linear-marker theorem",
            "result": "representation_covector_theorem_derived_parent_unsigned",
            "reason": "ell must be an invariant covector; if the parent dual invariant space is zero and no marker functor exists, ell=0",
            "next_action": "prove the parent G_X/E_X/no-trivial-dual and local invariant algebra clauses",
        },
        {
            "decision_id": "DEC975_1_fixed_vs_material",
            "topic": "marker taxonomy",
            "result": "fixed_spurion_conditionally_killed_material_markers_survive",
            "reason": "strict quotient removes fixed labels, but co-moving material markers and invariant class scalars descend as legal quotient data",
            "next_action": "attack parent no-extension/minimality or keep finite residuals",
        },
        {
            "decision_id": "DEC975_2_alpha3_fallback",
            "topic": "boundary alpha3 coefficient",
            "result": "formula_stub_written_nonclaim",
            "reason": "4e-20 alpha3 anchor is sourced, but K_boundary_alpha3 and Phi_boundary_local are not",
            "next_action": "derive boundary no-flux or acquire numeric coefficient inputs",
        },
        {
            "decision_id": "DEC975_3_best_next",
            "topic": "next checkpoint",
            "result": "generator_by_generator_elimination_or_K_boundary_alpha3_source",
            "reason": "no-marker proof now reduces to a finite generator list; if that route stalls, alpha3 coefficient acquisition is the honest fallback",
            "next_action": "start with the shortest live generator: readout-after-variation parent-domain audit, then constants/source universality",
        },
    ]
    return [
        {
            **spec,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for spec in specs
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "976-Y5-R10-readout-parent-domain-audit-or-K-boundary-alpha3-source.md",
            "objective": "turn readout-after-variation from a no-cheat rule into a parent-domain absence certificate, or source the first executable K_boundary_alpha3 coefficient",
            "include": "Args(S_parent) audit, reduced-action backreaction check, post-readout projector exclusion, K_boundary_alpha3/Phi_boundary inputs, alpha3 units",
            "exclude": "local-GR claim, qbar_XT theorem-zero, p>=2 promotion, invented alpha3 coefficient, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    marker_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V975_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_2_covector_theorem_written",
            "result": "pass"
            if any(row["step_id"] == "NLM975_7_verdict" and row["status"] == "REPRESENTATION_THEOREM_DERIVED_PARENT_UNSIGNED" for row in theorem_rows)
            else "fail",
            "detail": "representation/invariant-covector theorem written as parent-unsigned",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_3_material_markers_retained",
            "result": "pass"
            if any(row["marker_id"] == "MC975_1_co_moving_material_marker" and row["current_status"] == "NOT_EXCLUDED" for row in marker_rows)
            else "fail",
            "detail": "co-moving material marker remains legal until no-extension theorem exists",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_4_invariant_covector_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["valid_for_claim"] == "false" for row in gate_rows) else "fail",
            "detail": "parent invariant-covector acceptance gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_5_alpha3_rows_nonclaim",
            "result": "pass"
            if all(row["valid_for_claim"] == "false" and "MISSING_" in row["missing_inputs"] for row in alpha3_rows)
            else "fail",
            "detail": "alpha3 coefficient rows remain non-scoreable until numeric parent inputs exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_6_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all local-GR/R10/PPN claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_7_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_8_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "976 readout parent-domain audit or K_boundary_alpha3 source target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V975_9_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V975_READY",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "975 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    marker_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    alpha3_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 975 Y5 R10: No-Linear-Marker Covector Proof Or Boundary Flux Source Acquisition

Status: `Y5_R10_975_invariant_covector_theorem_derived_parent_unsigned_material_markers_survive_alpha3_formula_nonclaim`

Claim ceiling: no no-linear-marker parent theorem, no `p>=2` promotion, no `qbar_XT=0`, no scoreable alpha3 coefficient, no R10/PPN pass, and no EH/Newton/local-GR claim is made.

## Readout

975 sharpens the marker problem into the right mathematics.

A linear leakage term is not mysterious. It is a covector:

`F(X)=F(0)+ell(X)+1/2 H_X(X,X)+...`

So the proof target is: where can `ell in E_X*` come from?

The clean representation theorem is:

If the parent local memory variable `X` lives in a fibre `E_X` with parent symmetry `G_X`, and the parent action is `G_X` invariant, then a linear scalar term requires an invariant dual vector `ell in (E_X*)^G_X`. If `(E_X*)^G_X=0`, the linear term is impossible.

That is a real theorem shape. It is stronger and cleaner than saying "no marker" by taste. Fixed labelled spurions are also conditionally excluded by strict quotient logic: they are not orbit-constant parent functions.

But the current corpus still does not close the parent gate. A co-moving material marker, quotient-invariant domain/class scalar, marker-dependent species constant, or post-readout reduced-action marker can still manufacture an admissible covector unless primitive minimality, local invariant algebra triviality, constant-sector universality, and readout-after-variation are parent-signed. Boundary flux is not exactly an `ell` covector, but it remains a live source unless zeroed or coefficient-scored.

So 975 is progress but not a claim: the proof target is now a finite parent-certificate problem. The next shortest derivation route is to turn readout-after-variation from a no-cheat rule into a parent-domain absence certificate. If that fails, the honest fallback is sourcing `K_boundary_alpha3`.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## No-Linear-Marker Theorem Attempt

{md_table(theorem_rows, ["step_id", "claim_piece", "status", "proof_status", "gap"])}

## Marker Classification

{md_table(marker_rows, ["marker_id", "marker_type", "current_status", "reason", "remaining_work"])}

## Invariant-Covector Gate

{md_table(gate_rows, ["gate_id", "required_input", "current_evidence", "gate_pass", "missing_input"])}

## Alpha3 Coefficient Acquisition

{md_table(alpha3_rows, ["row_id", "arena", "quantity", "symbolic_form", "bound_or_anchor", "status", "missing_inputs", "valid_for_claim"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    theorem_rows = no_linear_marker_theorem_attempt()
    marker_rows = marker_classification()
    gate_rows = invariant_covector_gate()
    alpha3_rows = alpha3_coefficient_acquisition()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        theorem_rows,
        marker_rows,
        gate_rows,
        alpha3_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_975_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv",
        theorem_rows,
        ["step_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_MARKER_CLASSIFICATION.csv",
        marker_rows,
        ["marker_id", "marker_type", "current_status", "reason", "remaining_work", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_INVARIANT_COVECTOR_GATE.csv",
        gate_rows,
        ["gate_id", "required_input", "current_evidence", "gate_pass", "missing_input", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_ALPHA3_COEFFICIENT_ACQUISITION.csv",
        alpha3_rows,
        ["row_id", "arena", "quantity", "symbolic_form", "bound_or_anchor", "source_path", "status", "missing_inputs", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_975_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_975_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        theorem_rows,
        marker_rows,
        gate_rows,
        alpha3_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
