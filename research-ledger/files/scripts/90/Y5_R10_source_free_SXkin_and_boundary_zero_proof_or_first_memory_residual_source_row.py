from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "973-Y5-R10-source-free-SXkin-and-boundary-zero-proof-or-first-memory-residual-source-row.md"
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
            "source_id": "972_doc",
            "path": "972-Y5-R10-parent-two-slot-memory-action-and-Bianchi-identity-or-residual-source-fill.md",
            "role": "handoff selecting source-free S_Xkin and boundary-zero proof",
            "needle": "973-Y5-R10-source-free-SXkin-and-boundary-zero-proof-or-first-memory-residual-source-row.md",
        },
        {
            "source_id": "972_zero_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_972_LOCAL_ZERO_THEOREM_GATE.csv",
            "role": "local memory zero blockers",
            "needle": "LZG972_7_verdict",
        },
        {
            "source_id": "972_residual_source_fill",
            "path": "source-intake/mts_residuals/P8_Y5_R10_972_RESIDUAL_SOURCE_FILL_LEDGER.csv",
            "role": "retained memory residual source-fill requirements",
            "needle": "RSF972_2_boundary_lift",
        },
        {
            "source_id": "967_memory_lemma",
            "path": "source-intake/mts_residuals/P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv",
            "role": "positive-operator local silence lemma",
            "needle": "MPO967_6_verdict",
        },
        {
            "source_id": "968_memory_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv",
            "role": "missing X/operator/source/boundary inputs",
            "needle": "MOI968_8_verdict",
        },
        {
            "source_id": "943_coframe_contract",
            "path": "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
            "role": "conditional matter blindness and source-current descent",
            "needle": "DER943_6_verdict",
        },
        {
            "source_id": "945_q_kernel",
            "path": "945-Y5-R10-parent-q-map-Obs-e-functor-construction-or-first-frame-leak-bound-pack.md",
            "role": "q-kernel and matter-invisibility gap",
            "needle": "KT945_6_total_kernel",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "boundary exchange, Bianchi, and numeric pressure anchors",
            "needle": "alpha3_flux",
        },
        {
            "source_id": "506_energy_identity",
            "path": "source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
            "role": "positive operator and boundary silence patterns",
            "needle": "E506_vector_tensor_positive_operator",
        },
        {
            "source_id": "507_acceptance_gates",
            "path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "role": "theorem-zero/numeric-bound acceptance standards",
            "needle": "G507_0_theorem_zero",
        },
        {
            "source_id": "963_no_tower",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-integrated-out tower blocker",
            "needle": "NES963_3_no_integrated_out_tower",
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


def source_free_sxkin_lemma() -> list[dict[str, str]]:
    specs = [
        {
            "lemma_id": "SFL973_0_homogeneous_quadratic",
            "claim_piece": "homogeneous-centered kinetic sector",
            "mathematical_form": "S_X^kin=1/2 <X,L_X X> with no linear term and origin X=0 fixed by parent variables",
            "status": "RELATIVE_LEMMA_VALID",
            "gap": "parent does not yet sign X=0 as the unique origin rather than a shifted calibration X0(q)",
        },
        {
            "lemma_id": "SFL973_1_variation",
            "claim_piece": "source-free variation",
            "mathematical_form": "delta_X S_X^kin=<delta X,L_X X>+boundary, so J_X^kin=0 when the action is homogeneous",
            "status": "RELATIVE_DERIVED",
            "gap": "requires no affine term, no hidden X0(q), and no matter/worldtube vertex outside C_obs",
        },
        {
            "lemma_id": "SFL973_2_evenness_guard",
            "claim_piece": "no linear source by symmetry",
            "mathematical_form": "X -> -X or norm-square construction forbids odd/linear X terms in S_X^kin",
            "status": "GOOD_ROUTE_NOT_PARENT_SIGNED",
            "gap": "no parent Z2/norm-square/evenness clause currently signs the memory variable",
        },
        {
            "lemma_id": "SFL973_3_matter_blindness",
            "claim_piece": "ordinary matter does not source X",
            "mathematical_form": "S_matter=Sbar[q(Phi),Psi,theta] and X vertical/null implies delta_X S_matter=0",
            "status": "CONDITIONAL_ONLY",
            "gap": "943/945 keep q-kernel, coframe descent, constants, and marker exclusion unsigned",
        },
        {
            "lemma_id": "SFL973_4_double_zero_observed_slot",
            "claim_piece": "observed/source slot is silent at chi_D=0",
            "mathematical_form": "delta_X[f(chi_D)C_obs]=f(0) delta_X C_obs=0",
            "status": "RELATIVE_DERIVED",
            "gap": "parent origin of f and ownership of C_obs slot remain unsigned",
        },
        {
            "lemma_id": "SFL973_5_hidden_source_counterexamples",
            "claim_piece": "counterexamples to source-free S_Xkin",
            "mathematical_form": "S_X^kin=1/2<X-X0(q),L(X-X0(q))> or A_g(X)e_obs or m_A(X) creates J_X != 0",
            "status": "COUNTEREXAMPLES_RETAINED",
            "gap": "must prove no shifted origin, no representative Weyl/disformal/mass marker, and no boundary tail",
        },
        {
            "lemma_id": "SFL973_6_verdict",
            "claim_piece": "source-free ungated memory kinetic sector",
            "mathematical_form": "homogeneous quadratic plus quotient blindness would give J_X^kin=0",
            "status": "RELATIVE_LEMMA_READY_PARENT_UNSIGNED",
            "gap": "no local-GR claim; source-free premise remains unsigned in current corpus",
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


def boundary_zero_attempt() -> list[dict[str, str]]:
    specs = [
        {
            "boundary_id": "BZA973_0_variation_boundary_term",
            "claim_piece": "boundary term in X variation",
            "mathematical_form": "delta S_X^kin boundary = int_partialD sqrt(h) n_i A^ij nabla_j X delta X + delta S_boundary",
            "status": "BOUNDARY_TERM_IDENTIFIED",
            "gap": "parent boundary condition not selected",
        },
        {
            "boundary_id": "BZA973_1_dirichlet_route",
            "claim_piece": "Dirichlet no-hair",
            "mathematical_form": "X|partialD=0 gives zero boundary lift and removes constant mode",
            "status": "CONDITIONAL_ROUTE",
            "gap": "not parent-selected; may be a closure boundary condition if imposed by hand",
        },
        {
            "boundary_id": "BZA973_2_neumann_zero_mean_route",
            "claim_piece": "zero-flux plus zero-mean/topological class",
            "mathematical_form": "n.A.grad X|partialD=0 plus int_D X=0 or m_X^2>0 removes constant hair",
            "status": "CONDITIONAL_ROUTE",
            "gap": "zero mean/topological class and positive gap not parent-signed",
        },
        {
            "boundary_id": "BZA973_3_exact_topological_route",
            "claim_piece": "boundary primitive exact/topological",
            "mathematical_form": "i_v Theta_parent=dB_v and Pi_local dB_v=0",
            "status": "CONDITIONAL_ROUTE_NOT_DERIVED",
            "gap": "417 says boundary primitive, Bianchi gate, projected flux, and secular drift fail",
        },
        {
            "boundary_id": "BZA973_4_no_wall_stress",
            "claim_piece": "no metric wall stress from boundary",
            "mathematical_form": "delta_g S_boundary has no compact local wall stress or is Ward-owned",
            "status": "NOT_DERIVED",
            "gap": "boundary polarization/local wall stress not parent-signed",
        },
        {
            "boundary_id": "BZA973_5_residual_if_fails",
            "claim_piece": "finite boundary residual",
            "mathematical_form": "boundary_lift_norm enters ||X|| <= (||J_X||+boundary_lift_norm)/lambda_gap",
            "status": "RETAINED_RESIDUAL_REQUIRED",
            "gap": "boundary_lift_norm has no value/source-backed coefficient",
        },
        {
            "boundary_id": "BZA973_6_verdict",
            "claim_piece": "boundary zero proof",
            "mathematical_form": "Dirichlet/zero-flux/exact-boundary routes are valid only as conditional contracts",
            "status": "BOUNDARY_ZERO_NOT_PARENT_DERIVED",
            "gap": "must source finite boundary residual rows or continue deriving no-hair",
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


def jx_decomposition_gate() -> list[dict[str, str]]:
    specs = [
        {
            "component_id": "JXD973_0_kinetic_affine",
            "component": "J_X^kin_affine",
            "zero_condition": "S_X^kin is centered homogeneous quadratic with no X0(q)",
            "current_status": "NOT_PARENT_SIGNED",
            "action": "derive zero-origin/evenness clause or retain shifted-source row",
        },
        {
            "component_id": "JXD973_1_matter",
            "component": "J_X^matter",
            "zero_condition": "ordinary matter depends only on q/e_obs/theta and X is quotient-null",
            "current_status": "CONDITIONAL_ONLY",
            "action": "close q-kernel/matter descent or retain frame/coupling leak rows",
        },
        {
            "component_id": "JXD973_2_observed_slot",
            "component": "J_X^obs",
            "zero_condition": "observed coupling is multiplied by f(chi_D) and f(0)=0",
            "current_status": "RELATIVE_ZERO_AT_LOCAL_BRANCH",
            "action": "parent-sign double-zero origin and C_obs slot",
        },
        {
            "component_id": "JXD973_3_chi_wall",
            "component": "J_X^chi_wall",
            "zero_condition": "f_prime(0)=0 and no domain wall/source tail",
            "current_status": "CONDITIONAL_ONLY",
            "action": "derive f origin and no wall stress",
        },
        {
            "component_id": "JXD973_4_boundary",
            "component": "J_X^boundary",
            "zero_condition": "Dirichlet/zero-flux/exact boundary primitive with zero local projection",
            "current_status": "NOT_DERIVED",
            "action": "prove boundary no-hair or source boundary_lift_norm",
        },
        {
            "component_id": "JXD973_5_history",
            "component": "J_X^history",
            "zero_condition": "memory kernel local, source-free, stable, no long tail",
            "current_status": "NOT_DERIVED",
            "action": "derive memory kernel silence or source finite history tail",
        },
        {
            "component_id": "JXD973_6_verdict",
            "component": "J_X_total",
            "zero_condition": "all components JXD973_0..5 vanish",
            "current_status": "JX_ZERO_NOT_PROVED",
            "action": "no theorem-zero; first residual source rows remain nonclaim",
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


def first_residual_source_rows() -> list[dict[str, str]]:
    specs = [
        {
            "residual_id": "FRS973_0_boundary_alpha3_flux",
            "arena": "PPN/preferred-frame",
            "quantity": "projected boundary/memory exchange flux",
            "bound_or_anchor_value": "4.000e-20",
            "units": "dimensionless alpha3-scale lock",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "missing_mts_input": "MISSING_BOUNDARY_FLUX_PROJECTION_COEFFICIENT;MISSING_JX_BOUNDARY_NORM",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "residual_id": "FRS973_1_boundary_Gdot_drift",
            "arena": "Gdot/time drift",
            "quantity": "secular boundary/domain/memory exchange drift",
            "bound_or_anchor_value": "9.600e-15",
            "units": "yr^-1",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "missing_mts_input": "MISSING_SECULAR_DRIFT_PROJECTION;MISSING_HISTORY_TAIL_NORM",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "residual_id": "FRS973_2_domain_vector_alpha2",
            "arena": "PPN/preferred-frame",
            "quantity": "vector boundary/projector representative residual",
            "bound_or_anchor_value": "2.000e-09",
            "units": "dimensionless alpha2-scale lock",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "missing_mts_input": "MISSING_DOMAIN_VECTOR_COEFFICIENT",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "residual_id": "FRS973_3_xi_anisotropy",
            "arena": "PPN/preferred-location",
            "quantity": "topology/preferred-location anisotropy residual",
            "bound_or_anchor_value": "4.000e-09",
            "units": "dimensionless xi-scale lock",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "missing_mts_input": "MISSING_XI_ANISOTROPY_PROJECTION",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "residual_id": "FRS973_4_gamma_beta_fifth_force_hair",
            "arena": "PPN/R10",
            "quantity": "scalar/radial boundary hair beyond source-normalized monopole",
            "bound_or_anchor_value": "2.300e-05",
            "units": "dimensionless gamma-scale lock",
            "source_path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "missing_mts_input": "MISSING_SCALAR_HAIR_ALPHA_LAMBDA;MISSING_K_R10_K_PPN",
            "row_status": "SOURCE_BACKED_BOUND_ANCHOR_NOT_SCOREABLE",
        },
        {
            "residual_id": "FRS973_5_score_gate",
            "arena": "all_local",
            "quantity": "valid_for_claim",
            "bound_or_anchor_value": "false",
            "units": "boolean",
            "source_path": "source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv",
            "missing_mts_input": "requires theorem-zero or numeric MTS coefficient with units/source path/bound comparison",
            "row_status": "FORCED_FALSE",
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
            "gate_id": "CGATE973_0_source_free_SXkin",
            "claim": "ungated S_X^kin is source-free",
            "current_evidence": "relative homogeneous-quadratic lemma only; parent zero-origin/evenness unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE973_1_boundary_zero",
            "claim": "X boundary flux/lift vanishes",
            "current_evidence": "conditional boundary routes only; 417 no-hair gates fail",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE973_2_JX_zero",
            "claim": "total J_X vanishes locally",
            "current_evidence": "matter, boundary, history, hidden-source components remain unsigned",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE973_3_memory_zero",
            "claim": "positive operator proves X=0",
            "current_evidence": "source and boundary premises not parent-signed",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE973_4_residual_score",
            "claim": "first retained memory residual rows are scoreable",
            "current_evidence": "bound anchors are source-backed but MTS projection coefficients are missing",
            "gate_pass": "false",
        },
        {
            "gate_id": "CGATE973_5_local_GR",
            "claim": "local GR/Newton reduction follows from the memory branch",
            "current_evidence": "no theorem-zero and no residual pass",
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
            "decision_id": "DEC973_0_source_free_lemma",
            "topic": "source-free S_Xkin",
            "result": "relative_lemma_ready_parent_unsigned",
            "reason": "homogeneous-centered quadratic action gives no source, but parent has not signed the zero-origin/evenness/no-hidden-source clauses",
            "next_action": "try to derive zero-origin/evenness or accept finite J_X residual",
        },
        {
            "decision_id": "DEC973_1_boundary_zero",
            "topic": "boundary no-hair",
            "result": "conditional_routes_fail_parent_gate",
            "reason": "Dirichlet, zero-flux, and exact/topological routes are known but not parent-selected; 417 gates remain failed",
            "next_action": "attack boundary primitive/local flux theorem or retain boundary_lift_norm",
        },
        {
            "decision_id": "DEC973_2_residual_rows",
            "topic": "first residual source rows",
            "result": "source_backed_bound_anchors_written_nonclaim",
            "reason": "417 gives hard local pressure anchors, but MTS projection/source coefficients are missing",
            "next_action": "derive or source the first coefficient: boundary flux projection or J_X boundary norm",
        },
        {
            "decision_id": "DEC973_3_best_next",
            "topic": "next checkpoint",
            "result": "zero_origin_evenness_or_boundary_flux_coefficient",
            "reason": "the proof now hinges on whether X=0 is a parent-centered origin and whether boundary flux is zero or finite",
            "next_action": "try zero-origin/evenness theorem first; if it fails, fill boundary flux coefficient row",
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
            "next_target": "974-Y5-R10-zero-origin-evenness-theorem-or-boundary-flux-coefficient-fill.md",
            "objective": "try to prove X=0 is the parent-centered even/homogeneous origin of the memory kinetic sector; if not, fill the first boundary flux projection coefficient row",
            "include": "X->-X or norm-square origin, no affine X0(q), no hidden matter marker, boundary flux coefficient, alpha3/Gdot pressure anchors",
            "exclude": "local-GR claim, invented coefficients, unsourced bound pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    source_free_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    jx_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    formalization_count = formalization_changed_after_start()
    rows = [
        {
            "check_id": "V973_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail",
            "detail": "all cited local source paths exist",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_1_source_needles_found",
            "result": "pass" if all(row["needle_found"] == "true" for row in sources) else "fail",
            "detail": "all source needles found",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_2_source_free_relative_lemma",
            "result": "pass"
            if any(row["lemma_id"] == "SFL973_6_verdict" and row["status"] == "RELATIVE_LEMMA_READY_PARENT_UNSIGNED" for row in source_free_rows)
            else "fail",
            "detail": "source-free S_Xkin lemma is relative and parent-unsigned",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_3_boundary_zero_not_derived",
            "result": "pass"
            if any(row["boundary_id"] == "BZA973_6_verdict" and row["status"] == "BOUNDARY_ZERO_NOT_PARENT_DERIVED" for row in boundary_rows)
            else "fail",
            "detail": "boundary zero proof remains unsigned",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_4_JX_zero_not_proved",
            "result": "pass"
            if any(row["component_id"] == "JXD973_6_verdict" and row["current_status"] == "JX_ZERO_NOT_PROVED" for row in jx_rows)
            else "fail",
            "detail": "J_X decomposition keeps total source zero unproved",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_5_first_residual_rows_nonclaim",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in residual_rows) else "fail",
            "detail": "first residual bound anchors written but not scoreable",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_6_claim_gates_false",
            "result": "pass" if all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows) else "fail",
            "detail": "all memory/local-GR claim gates remain false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_7_decisions_nonclaim",
            "result": "pass" if all(row["claim_allowed"] == "false" for row in decision_rows) else "fail",
            "detail": "decision ledger remains nonclaim",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_8_next_target_written",
            "result": "pass" if len(target_rows) == 1 and target_rows[0]["valid_for_claim"] == "false" else "fail",
            "detail": "974 zero-origin/evenness or boundary coefficient target selected",
            "generated_utc": stamp(),
        },
        {
            "check_id": "V973_9_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
            "generated_utc": stamp(),
        },
    ]
    rows.append(
        {
            "check_id": "V973_10_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "973 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    source_free_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    jx_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 973 Y5 R10: Source-Free S_Xkin And Boundary Zero Proof Or First Memory Residual Source Row

Status: `Y5_R10_973_source_free_SXkin_relative_lemma_boundary_zero_not_derived_first_residual_bound_anchors_nonclaim`

Claim ceiling: no source-free kinetic theorem, no boundary-zero theorem, no J_X zero, no memory theorem-zero, no residual bound pass, no R10/R11 pass, no EH/Newton/local-GR claim is made.

## Readout

973 gives a real but conditional proof shape:

If `S_X^kin = 1/2 <X,L_X X>` is a homogeneous quadratic sector centered at the parent origin `X=0`, then its variation is source-free:

`delta_X S_X^kin = <delta X,L_X X> + boundary`.

Together with the two-slot gate, `f(0)=0` kills the observed/source coupling at the local branch. So the local equation can become `L_X X=0`.

But the current corpus does not yet parent-sign the clauses that make this a theorem: `X=0` as the true centered origin, no affine `X0(q)`, no hidden matter/marker source, no boundary lift, and no history tail. The boundary side also does not close: Dirichlet/zero-flux/exact-topological routes are valid conditional routes, but 417 keeps boundary primitive, Bianchi gate, projected local flux, and secular drift unproved.

So 973 does not pass local GR. It makes the next choice brutally precise: prove zero-origin/evenness for `X`, or begin filling boundary/memory residual coefficients against the first hard local pressure anchors.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Source-Free S_Xkin Lemma

{md_table(source_free_rows, ["lemma_id", "claim_piece", "status", "gap"])}

## Boundary Zero Attempt

{md_table(boundary_rows, ["boundary_id", "claim_piece", "status", "gap"])}

## J_X Decomposition Gate

{md_table(jx_rows, ["component_id", "component", "zero_condition", "current_status", "action"])}

## First Residual Source Rows

{md_table(residual_rows, ["residual_id", "arena", "quantity", "bound_or_anchor_value", "units", "missing_mts_input", "row_status", "valid_for_claim"])}

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
    source_free_rows = source_free_sxkin_lemma()
    boundary_rows = boundary_zero_attempt()
    jx_rows = jx_decomposition_gate()
    residual_rows = first_residual_source_rows()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        source_free_rows,
        boundary_rows,
        jx_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_973_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_SOURCE_FREE_SXKIN_LEMMA.csv",
        source_free_rows,
        ["lemma_id", "claim_piece", "mathematical_form", "status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_BOUNDARY_ZERO_ATTEMPT.csv",
        boundary_rows,
        ["boundary_id", "claim_piece", "mathematical_form", "status", "gap", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv",
        jx_rows,
        ["component_id", "component", "zero_condition", "current_status", "action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_FIRST_RESIDUAL_SOURCE_ROWS.csv",
        residual_rows,
        ["residual_id", "arena", "quantity", "bound_or_anchor_value", "units", "source_path", "missing_mts_input", "row_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_973_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_973_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(
        sources,
        source_free_rows,
        boundary_rows,
        jx_rows,
        residual_rows,
        claim_rows,
        decision_rows,
        target_rows,
        validation_rows,
    )


if __name__ == "__main__":
    main()
