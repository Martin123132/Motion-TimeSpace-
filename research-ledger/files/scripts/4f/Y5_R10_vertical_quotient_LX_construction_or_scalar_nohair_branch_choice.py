from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1022_0_1021_next", "source-intake/mts_residuals/P8_Y5_R10_1021_NEXT_TARGET.csv", "vertical-quotient", "1021 handoff to quotient/vertical or scalar no-hair choice."),
        ("SRC1022_1_1021_routes", "source-intake/mts_residuals/P8_Y5_R10_1021_ROUTE_VERDICTS.csv", "R1021_3_verdict", "1021 route split verdict."),
        ("SRC1022_2_1021_scalar", "source-intake/mts_residuals/P8_Y5_R10_1021_SCALAR_BRANCH_SEPARATION.csv", "SB1021_3_scalar_verdict", "1021 scalar/noether separation."),
        ("SRC1022_3_669_candidates", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_0_absent_quotient_variable", "669 L_X candidate ranking."),
        ("SRC1022_4_669_vertical", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_1_vertical_constraint", "669 vertical constraint route."),
        ("SRC1022_5_669_scalar", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_2_positive_sourcefree_massive", "669 scalar source-free route."),
        ("SRC1022_6_669_residuals", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_0_Z_X", "669 residual coefficient vector."),
        ("SRC1022_7_669_gates", "source-intake/mts_residuals/P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv", "G669_5_no_pole_quotient", "669 no-pole and positive operator gates."),
        ("SRC1022_8_670_no_pole", "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv", "NQ670_8_no_pole_result", "670 no-pole quotient chain."),
        ("SRC1022_9_670_sourcefree", "source-intake/mts_residuals/P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv", "PSF670_6_zero_profile_result", "670 positive source-free chain."),
        ("SRC1022_10_581_chain", "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv", "QVT581_7_alpha_result", "581 quotient/vertical theorem chain."),
        ("SRC1022_11_581_certificate", "source-intake/mts_residuals/P8_Y5_R10_581_NO_POLE_CERTIFICATE_TEMPLATE.csv", "NPC581_6_claim_gate", "581 no-pole certificate template."),
        ("SRC1022_12_637_qmap", "source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv", "QM637_2_vertical_kernel", "637 quotient map derivation."),
        ("SRC1022_13_637_obs", "source-intake/mts_residuals/P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv", "OF637_1_chain_rule", "637 observed functor and matter descent."),
        ("SRC1022_14_590_map", "source-intake/mts_residuals/P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv", "DVM590_3_precise_map", "590 DCdagger-to-vertical map."),
        ("SRC1022_15_590_gate", "source-intake/mts_residuals/P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv", "MCG590_6_matter_quotient", "590 mapping closure gates."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def branch_decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "branch_id": "BDM1022_0_absent_quotient",
            "candidate": "X absent from physical quotient before variation",
            "core_test": "S_parent=S_red[q(Phi)] and Dq[v_X]=0 before local equations or readout",
            "scrutiny_level": "lowest_if_constructed",
            "current_status": "best_route_partial_conditional",
            "missing": "actual X equals parent null/relative-exact generator; action descent; matter descent; boundary silence",
            "decision": "attempt_first",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BDM1022_1_vertical_constraint",
            "candidate": "X is first-class vertical constraint direction",
            "core_test": "delta G_X=Omega(delta Phi,v_X), bracket closure, degree count, Q_X=0/proper/exact",
            "scrutiny_level": "low_if_first_class_boundary_silent",
            "current_status": "best_active_theorem_route_unsigned",
            "missing": "parent Omega, v_X on every field, differentiable boundary charge, reduced nondegeneracy",
            "decision": "attempt_with_absent_quotient",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BDM1022_2_scalar_positive_nohair",
            "candidate": "X is physical scalar-like positive source-free mode",
            "core_test": "Z_X>0, M_X^2>0, J_X=0, boundary_flux_X=0 => X=0 in compact exterior",
            "scrutiny_level": "medium_and_coefficient_sensitive",
            "current_status": "conditional_theorem_only",
            "missing": "Z_X, M_X^2, J_X=0, self-adjoint domain, boundary_flux_X=0",
            "decision": "fallback_if_quotient_fails",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BDM1022_3_scalar_sourced_residual",
            "candidate": "X is physical sourced finite-range residual",
            "core_test": "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT scored against R10/R11",
            "scrutiny_level": "highest_empirical_pressure",
            "current_status": "schema_ready_no_values",
            "missing": "all coefficients, units, source paths, bound curve linkage, no-cancellation envelope",
            "decision": "last_resort_scoreable_branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BDM1022_4_memory_nonlocal",
            "candidate": "X is local face of memory/nonlocal kernel",
            "core_test": "causal positive kernel or auxiliary-field lift with source silence/bounds",
            "scrutiny_level": "high_until_kernel_spectrum_owned",
            "current_status": "retained_unowned_extension",
            "missing": "kernel, spectrum, local lift, source terms, boundary history injection",
            "decision": "defer_until_local_branch_choice",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "BDM1022_5_verdict",
            "candidate": "1022 branch choice",
            "core_test": "prefer theorem-zero before coefficient scoring, but never mix proof languages",
            "scrutiny_level": "route_hygiene_gate",
            "current_status": "choose_quotient_vertical_next",
            "missing": "parent-signed q/v_X/action/matter/boundary package",
            "decision": "1023 constructs quotient/vertical certificate; scalar no-hair remains fallback",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def vertical_quotient_rows() -> list[dict[str, str]]:
    rows = [
        {
            "clause_id": "VQC1022_0_q_map",
            "required_clause": "canonical parent quotient map",
            "mathematical_form": "q: Conf_parent -> Q_obs=Conf_parent/N_X with Dq[v_X]=0",
            "current_status": "conditional_math_not_parent_signed",
            "missing_for_claim": "identify actual local X variations with integrable parent null distribution N_X",
            "if_signed": "X is representative data, not a physical local pole",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_1_action_descent",
            "required_clause": "bulk action descends before variation",
            "mathematical_form": "S_bulk[Phi]=S_red[q(Phi)] + fixed boundary/topological terms",
            "current_status": "conditional_only",
            "missing_for_claim": "parent Lagrangian and boundary/domain terms must be explicit and invariant along v_X",
            "if_signed": "no independent X Hessian or local Green function",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_2_matter_descent",
            "required_clause": "ordinary matter sees quotient observables only",
            "mathematical_form": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] with L_vX theta_A=0",
            "current_status": "conditional_chain_rule_only",
            "missing_for_claim": "constant/material-marker ownership and no hidden conformal/disformal X channel",
            "if_signed": "qbar_XT=0 or matter source term vanishes by chain rule",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_3_vertical_generator",
            "required_clause": "field-by-field vertical action",
            "mathematical_form": "v_X[Phi^A] given for metric/coframe, matter readout, memory/projector/domain, and boundary fields",
            "current_status": "missing",
            "missing_for_claim": "590 lists candidates but no MTS parent transformation law on all fields",
            "if_signed": "DCdagger/Omega-flat map becomes executable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_4_momentum_map",
            "required_clause": "first-class differentiable generator",
            "mathematical_form": "delta G_X[epsilon]=Omega(delta Phi,v_epsilon), G_X=int epsilon C_X+Q_X",
            "current_status": "not_derived",
            "missing_for_claim": "parent theta/Omega, DC_X, Q_X differentiability, and bracket closure",
            "if_signed": "vertical constraint route can remove physical X degrees",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_5_boundary_silence",
            "required_clause": "no local edge charge or central cocycle",
            "mathematical_form": "Q_X=0/proper/exact and K_boundary[epsilon,eta]=0 on compact local branch",
            "current_status": "blocked_by_1019_1021",
            "missing_for_claim": "B_X primitive/exactness, projector orthogonality, and boundary cocycle calculation",
            "if_signed": "Qbar_XH=0 and edge alpha branch inactive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_6_degree_count",
            "required_clause": "rank and reduced nondegeneracy",
            "mathematical_form": "primary+secondary first-class pair removes X pair; reduced Omega nondegenerate modulo ordinary gauge",
            "current_status": "not_checked",
            "missing_for_claim": "constraint rank, no proper stabilizer, and reduced phase-space count",
            "if_signed": "zero Hessian means gauge, not under-specified dynamics",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "VQC1022_7_verdict",
            "required_clause": "quotient/vertical no-pole theorem",
            "mathematical_form": "VQC1022_0 through VQC1022_6 imply K_X=qbar_XT=Qbar_XH=0 and no active R10 X alpha row",
            "current_status": "fail_current_claim_but_best_next_target",
            "missing_for_claim": "full q/v_X/action/matter/boundary/degree certificate",
            "if_signed": "strongest path to local-GR-like silence without tuning",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def scalar_nohair_rows() -> list[dict[str, str]]:
    rows = [
        {
            "clause_id": "SNH1022_0_operator",
            "required_clause": "self-adjoint positive local operator",
            "mathematical_form": "O_X=-nabla_i(Z_X nabla^i)+M_X^2 on compact source-free exterior",
            "current_status": "template_only",
            "missing_for_claim": "parent Hessian, field units, domain, and self-adjoint boundary conditions",
            "if_signed": "energy identity becomes legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "SNH1022_1_positive_kinetic",
            "required_clause": "Z_X>0",
            "mathematical_form": "quadratic kinetic Hessian positive in the local branch",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "second variation and normalization",
            "if_signed": "no ghost/anti-elliptic leakage",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "SNH1022_2_positive_mass_gap",
            "required_clause": "M_X^2>0 and lambda_X fixed",
            "mathematical_form": "lambda_X=sqrt(Z_X/M_X^2) with units",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "mass-gap derivation or sourced range row",
            "if_signed": "no tachyon/zero-mode long-range scalar hair",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "SNH1022_3_source_zero",
            "required_clause": "J_X=0 channel-by-channel",
            "mathematical_form": "delta_X S_matter + hidden/source/domain terms vanish",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "missing_for_claim": "matter quotient/no-marker theorem or explicit source-current cancellation",
            "if_signed": "no ordinary matter source excites X",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "SNH1022_4_boundary_flux_zero",
            "required_clause": "boundary_flux_X=0",
            "mathematical_form": "int_boundary X Z_X n.grad X=0 or exact/proper boundary term",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "missing_for_claim": "boundary class/no-hair/projector silence from parent action",
            "if_signed": "energy identity forces X=0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "SNH1022_5_energy_identity",
            "required_clause": "positive no-hair identity",
            "mathematical_form": "int_A(Z_X|grad X|^2+M_X^2 X^2)=int_A XJ_X+boundary_flux_X",
            "current_status": "conditional_math_valid",
            "missing_for_claim": "SNH1022_0 through SNH1022_4 together",
            "if_signed": "X=0 in local exterior",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "SNH1022_6_verdict",
            "required_clause": "scalar source-free local silence",
            "mathematical_form": "SNH1022_0 through SNH1022_5 imply no active scalar profile, but not a Noether edge primitive",
            "current_status": "fallback_not_next_best",
            "missing_for_claim": "all operator/source/boundary inputs",
            "if_signed": "R10/R11 scalar profile can be silenced, but edge/source substitutes still audited",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def fallback_rows() -> list[dict[str, str]]:
    rows = [
        {
            "row_id": "FBR1022_0_quotient_certificate",
            "quantity": "q_vX_action_matter_boundary_certificate",
            "required_columns": "q_id;vX_id;action_descent;matter_descent;boundary_silence;degree_count;source_path;valid_for_claim",
            "current_status": "MISSING_CERTIFICATE",
            "used_if": "quotient/vertical route pursued in 1023",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FBR1022_1_scalar_operator_pack",
            "quantity": "Z_X;M_X2;J_X;boundary_flux_X;lambda_X",
            "required_columns": "system_id;Z_X;M_X2;J_X;boundary_flux_X;lambda_X;units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "used_if": "scalar no-hair route selected or quotient fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FBR1022_2_sourced_alpha_pack",
            "quantity": "K_X;Qbar_XH;qbar_XT;alpha_X(lambda)",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_X;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "used_if": "scalar/source route remains nonzero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FBR1022_3_edge_bound_pack",
            "quantity": "EDGEBOUND1020 terms",
            "required_columns": "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_BOUND_TERMS",
            "used_if": "boundary/edge charge route remains nonzero or unproved",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "FBR1022_4_total_guard",
            "quantity": "absolute no-cancellation local residual envelope",
            "required_columns": "abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_R11;component_sum_abs;bound_curve;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "used_if": "any theorem-zero branch fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def route_rows() -> list[dict[str, str]]:
    rows = [
        {
            "route_id": "R1022_0_selected_next",
            "route": "attempt quotient/vertical construction first",
            "status": "selected_as_least_scrutiny_but_not_claimed",
            "because": "it removes X before variation instead of fitting coefficients after the fact",
            "next_action": "build q/v_X/action/matter/boundary certificate in 1023",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1022_1_scalar_fallback",
            "route": "scalar positive no-hair",
            "status": "fallback_if_quotient_fails",
            "because": "it is mathematically honest but coefficient/source/boundary intensive",
            "next_action": "fill Z_X, M_X2, J_X=0, boundary_flux_X=0 only if quotient route fails",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1022_2_sourced_fallback",
            "route": "finite residual scoring",
            "status": "last_resort_scoreable",
            "because": "nonzero source/coupling must be tested against R10/R11 instead of hidden",
            "next_action": "source K_X, Qbar_XH, qbar_XT, lambda_X, and edge-bound rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1022_3_verdict",
            "route": "branch-choice checkpoint",
            "status": "no_claim_but_next_route_selected",
            "because": "quotient/vertical is the cleanest route if constructible; scalar remains fallback, not mixed",
            "next_action": "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    rows = [
        ("CG1022_0_sources_registered", "1022 source chain exists", True, "all cited route-choice ledgers are found", False),
        ("CG1022_1_branch_choice_written", "branch decision matrix written", True, "quotient, vertical, scalar no-hair, sourced residual, and memory branches are separated", False),
        ("CG1022_2_quotient_claim", "quotient/vertical no-pole claim", False, "q/v_X/action/matter/boundary/degree certificate is missing", False),
        ("CG1022_3_scalar_nohair_claim", "scalar source-free no-hair claim", False, "Z_X, M_X2, J_X=0, and boundary_flux_X=0 are missing", False),
        ("CG1022_4_source_residual_claim", "finite residual R10/R11 pass", False, "coefficient rows and no-cancellation envelope are missing", False),
        ("CG1022_5_route_mixing_forbidden", "route-mixing guardrail", True, "scalar no-hair is not allowed to masquerade as Noether edge exactness", False),
        ("CG1022_6_local_GR_claim", "local GR/Newton reduction", False, "no local branch has theorem-zero or valid source-bound closure", False),
        ("CG1022_7_next_target_ready", "1023 target selected", True, "1023 will attempt q/v_X/action descent certificate first", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": str(gate_pass).lower(),
            "reason": reason,
            "claim_allowed": str(claim_allowed).lower(),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1022_0_branch_choice",
            "decision": "Attempt the quotient/vertical construction first.",
            "because": "It is the least post-hoc local-GR route: if X is absent/vertical before variation, no local pole needs hiding.",
            "next_action": "construct q, v_X, action descent, matter descent, boundary silence, and degree count as one certificate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1022_1_no_scalar_mixing",
            "decision": "Do not use scalar no-hair language to claim edge-charge exactness.",
            "because": "A scalar positive operator can give X=0 only under source-free/boundary conditions; it is not automatically a Noether boundary primitive.",
            "next_action": "keep scalar no-hair as fallback branch with separate inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1022_2_empirical_fallback",
            "decision": "If both theorem routes fail, score the residual instead of soft-closing it.",
            "because": "Nonzero coupling/source terms belong in alpha/lambda and R11 coefficient rows.",
            "next_action": "fill FBR1022 source packs with units and source paths",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1022_3_next_target",
            "decision": "The next target is the q/v_X/action descent certificate.",
            "because": "This is the first object that can genuinely remove the local X branch before variation.",
            "next_action": "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            "objective": "build a single certificate for q, v_X, action descent, matter descent, boundary silence, and degree count; if it fails, formally demote to scalar no-hair/source-coefficient inputs",
            "include": "q map, N_X null distribution, Dq[v_X]=0, S_parent=S_red[q(Phi)], matter quotient functor, constants/no-marker, G_X momentum map, Q_X boundary silence, degree count",
            "exclude": "post-readout quotient, scalar no-hair as edge exactness, source-free by assertion, cancellation between unknowns, R10/R11 pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    branches: list[dict[str, str]],
    vertical: list[dict[str, str]],
    scalar: list[dict[str, str]],
    fallback: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    branch_required = {"BDM1022_0_absent_quotient", "BDM1022_1_vertical_constraint", "BDM1022_2_scalar_positive_nohair", "BDM1022_3_scalar_sourced_residual", "BDM1022_4_memory_nonlocal", "BDM1022_5_verdict"}
    vertical_required = {"VQC1022_0_q_map", "VQC1022_1_action_descent", "VQC1022_2_matter_descent", "VQC1022_3_vertical_generator", "VQC1022_4_momentum_map", "VQC1022_5_boundary_silence", "VQC1022_6_degree_count", "VQC1022_7_verdict"}
    scalar_required = {"SNH1022_0_operator", "SNH1022_1_positive_kinetic", "SNH1022_2_positive_mass_gap", "SNH1022_3_source_zero", "SNH1022_4_boundary_flux_zero", "SNH1022_5_energy_identity", "SNH1022_6_verdict"}
    fallback_required = {"FBR1022_0_quotient_certificate", "FBR1022_1_scalar_operator_pack", "FBR1022_2_sourced_alpha_pack", "FBR1022_3_edge_bound_pack", "FBR1022_4_total_guard"}
    checks = [
        ("V1022_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1022_1_branch_matrix_complete", branch_required.issubset({row["branch_id"] for row in branches}), "branch matrix covers quotient, vertical, scalar no-hair, sourced residual, memory, and verdict"),
        ("V1022_2_branch_choice_selected", any(row["branch_id"] == "BDM1022_5_verdict" and row["decision"].startswith("1023 constructs quotient") for row in branches), "quotient/vertical is selected as next route without claim"),
        ("V1022_3_vertical_clauses_complete", vertical_required.issubset({row["clause_id"] for row in vertical}), "vertical quotient construction clauses are complete"),
        ("V1022_4_vertical_nonclaim", any(row["clause_id"] == "VQC1022_7_verdict" and row["current_status"] == "fail_current_claim_but_best_next_target" for row in vertical), "vertical no-pole theorem is not promoted"),
        ("V1022_5_scalar_clauses_complete", scalar_required.issubset({row["clause_id"] for row in scalar}), "scalar no-hair clauses are complete"),
        ("V1022_6_scalar_nonclaim", any(row["clause_id"] == "SNH1022_6_verdict" and row["current_status"] == "fallback_not_next_best" for row in scalar), "scalar no-hair remains fallback and nonclaim"),
        ("V1022_7_fallback_rows_complete", fallback_required.issubset({row["row_id"] for row in fallback}), "fallback source rows cover quotient certificate, scalar pack, sourced alpha, edge bound, and total guard"),
        ("V1022_8_fallback_rows_nonclaim", all(row["valid_for_claim"] == "false" and ("MISSING" in row["current_status"] or "NOT_COMPUTED" in row["current_status"]) for row in fallback), "fallback rows remain nonclaim"),
        ("V1022_9_route_verdict_selected", any(row["route_id"] == "R1022_3_verdict" and row["status"] == "no_claim_but_next_route_selected" for row in routes), "route verdict selects 1023 and blocks claim"),
        ("V1022_10_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "all claim gates are nonclaim"),
        ("V1022_11_route_mixing_guardrail", any(row["gate_id"] == "CG1022_5_route_mixing_forbidden" and flag(row["gate_pass"]) for row in gates), "route-mixing guardrail is installed"),
        ("V1022_12_decision_written", any(row["decision_id"] == "DEC1022_3_next_target" for row in decisions), "1023 decision row is written"),
        ("V1022_13_next_target_written", len(next_target) == 1 and "1023-Y5-R10-q-vX-action" in next_target[0]["next_target"], "1023 next target row is present"),
        ("V1022_14_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1022_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1022 branch-choice validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    branches: list[dict[str, str]],
    vertical: list[dict[str, str]],
    scalar: list[dict[str, str]],
    fallback: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1022 Y5 R10 vertical quotient L_X construction or scalar nohair branch choice",
            "",
            "**Status:** The branch fork is now explicit. The quotient/vertical route is selected as the next least-scrutiny attempt because it can remove `X` before variation if `q`, `v_X`, action descent, matter descent, boundary silence, and degree count close together. Scalar no-hair remains a fallback, not an edge-charge proof.",
            "",
            "**Claim ceiling:** no quotient no-pole theorem, scalar no-hair theorem, R10/R11 pass, PPN pass, Newton limit, or local-GR reduction is allowed from 1022.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Branch decision matrix",
            md_table(branches, ["branch_id", "candidate", "core_test", "scrutiny_level", "current_status", "missing", "decision", "claim_allowed"]),
            "## Vertical quotient construction",
            md_table(vertical, ["clause_id", "required_clause", "mathematical_form", "current_status", "missing_for_claim", "if_signed", "valid_for_claim"]),
            "## Scalar no-hair construction",
            md_table(scalar, ["clause_id", "required_clause", "mathematical_form", "current_status", "missing_for_claim", "if_signed", "valid_for_claim"]),
            "## Fallback source rows",
            md_table(fallback, ["row_id", "quantity", "required_columns", "current_status", "used_if", "valid_for_claim"]),
            "## Route verdicts",
            md_table(routes, ["route_id", "route", "status", "because", "next_action", "claim_allowed", "valid_for_claim"]),
            "## Claim gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    branches = branch_decision_rows()
    vertical = vertical_quotient_rows()
    scalar = scalar_nohair_rows()
    fallback = fallback_rows()
    routes = route_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, branches, vertical, scalar, fallback, routes, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1022_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1022_BRANCH_DECISION_MATRIX.csv", branches)
    write_csv(OUT / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv", vertical)
    write_csv(OUT / "P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv", scalar)
    write_csv(OUT / "P8_Y5_R10_1022_FALLBACK_SOURCE_ROWS.csv", fallback)
    write_csv(OUT / "P8_Y5_R10_1022_ROUTE_VERDICTS.csv", routes)
    write_csv(OUT / "P8_Y5_R10_1022_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1022_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1022_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1022_VALIDATION.csv", validations)
    write_doc(sources, branches, vertical, scalar, fallback, routes, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
