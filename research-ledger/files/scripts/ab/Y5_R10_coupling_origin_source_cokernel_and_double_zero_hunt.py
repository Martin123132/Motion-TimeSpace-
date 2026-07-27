from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_897_coupling_origin_hunt_completed_source_cokernel_and_double_zero_conditional_not_parent_signed_residual_vector_required"
CLAIM_CEILING = "conditional_coupling_silence_contract_only_no_Jtr_zero_no_Ctr_double_zero_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "898-Y5-R10-trace-vertical-generator-matter-descent-signature-or-residual-vector.md"

SOURCE_COKERNEL_FORMULA = "J_tr=P_tr^dagger J_parent=0 if matter descends through q_loc and P_tr/v_tr is local-vertical or rank-zero"
DOUBLE_ZERO_FORMULA = "C_tr(Phi0)=0 and partial_A C_tr(Phi0)=0 if C_tr=F(R_tr), R_tr=G_AB Z_tr^A Z_tr^B, F(0)=0"

SOURCE_SPECS = [
    {
        "source_id": "896_doc",
        "path": ROOT / "896-Y5-R10-trace-action-parent-adoption-gate-and-zero-vs-finite-branch-register.md",
        "needle": "coupling ownership",
        "role": "immediate coupling bottleneck handoff",
    },
    {
        "source_id": "896_validation",
        "path": OUT / "P8_Y5_BRR545_896_VALIDATION.csv",
        "needle": "V896_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "896_coupling_register",
        "path": OUT / "P8_Y5_R10_896_COUPLING_BOTTLENECK_REGISTER.csv",
        "needle": "CB896_0_Jtr_zero",
        "role": "selected J_tr/double-zero bottleneck rows",
    },
    {
        "source_id": "873_trace_charge",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "chain-rule zero theorem",
        "role": "conditional local matter trace-charge zero theorem",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "Dq_loc[U][v_T]=0",
        "role": "local verticality lemma and support debts",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "A real trace projector requires a parent trace covector",
        "role": "P_tr/v_tr construction and rank/source-cokernel tests",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "source-cokernel",
        "role": "rank-zero no-pole/source-cokernel conditional theorem",
    },
    {
        "source_id": "407_matter_functor",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needle": "S_matter_quotient_functor",
        "role": "matter quotient/descent sketch",
    },
    {
        "source_id": "511_fixed_point",
        "path": ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "needle": "FP511_1_double_zero_nonEH_coupling",
        "role": "local fixed-point double-zero criterion",
    },
    {
        "source_id": "488_selector",
        "path": ROOT / "488-double-zero-R11-selector-parent-clause-or-demotion.md",
        "needle": "Sigma_loc = G_AB",
        "role": "composite squared selector mechanism",
    },
    {
        "source_id": "608_normsquare",
        "path": ROOT / "608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md",
        "needle": "NS608_1_no_linear_marker",
        "role": "norm-square/no-linear-marker double-zero theorem attempt",
    },
    {
        "source_id": "801_fixed_point",
        "path": ROOT / "801-Y5-R10-double-zero-fixed-point-parent-mechanism-or-local-branch-closure-ledger.md",
        "needle": "DZ801_1_norm_evenness",
        "role": "fixed-point norm-evenness double-zero theorem",
    },
    {
        "source_id": "654_local_gr_spine",
        "path": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needle": "R10_fifth_force",
        "role": "local-GR/R10 fifth-force gate",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "merged the J_tr source-cokernel and C_tr double-zero routes into one coupling-origin gate",
            "best_partial_result": "the silence path is exact if P_tr/v_tr is local-vertical, matter descends through q_loc with no markers, and trace metric couplings are norm-square/even functions at the fixed point",
            "hard_blockers": "P_tr/v_tr not parent-owned, q_loc matter descent not signed, source-cokernel not proved, trace double-zero not parent-specialized, boundary no-tail still open",
            "what_is_not_claimed": "J_tr=0, alpha_tr=0, C_tr double zero, no local trace pole, R10 pass, PPN pass, clock/WEP/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def source_cokernel_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "SCA897_0_definition",
            "object": "J_tr",
            "math_statement": "J_tr=P_tr^dagger J_parent; local silence means <u_tr,J_parent>=0 for every physical local trace test mode u_tr",
            "current_status": "definition_ready",
            "parent_gap": "P_tr/v_tr and physical trace test modes are not parent-owned",
            "if_closed": "local trace matter coupling is zero without tuning",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "SCA897_1_chain_rule_descent",
            "object": "matter action descent",
            "math_statement": "S_matter=Sbar[Obs(q_loc(Phi)),Psi,theta] and Dq_loc[v_tr]=0 imply partial_{v_tr}S_matter=0",
            "current_status": "conditional_theorem_valid",
            "parent_gap": "q_loc, geometry stack descent, and no-marker theta are not signed",
            "if_closed": "ordinary matter has Q_tr^A=0 for R10/WEP/clock/orbital source tests",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "SCA897_2_rank_zero_route",
            "object": "P_tr local rank",
            "math_statement": "rank(P_loc P_tr P_loc^dagger)=0 implies no local source-coupled trace image",
            "current_status": "conditional_theorem_valid",
            "parent_gap": "rank-zero/readout-only/boundary support and no-tail are not signed",
            "if_closed": "no finite local trace pole and J_tr source-cokernel zero",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "SCA897_3_boundary_tail_watch",
            "object": "boundary/exact trace current",
            "math_statement": "P_loc J_trace=0 and P_loc dB_trace=0 on compact local U",
            "current_status": "not_proved",
            "parent_gap": "relative cohomology/no-tail certificate missing",
            "if_closed": "endpoint/cosmology trace readout cannot leak into local fifth-force hair",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "SCA897_4_verdict",
            "object": "source-cokernel route",
            "math_statement": SOURCE_COKERNEL_FORMULA,
            "current_status": "conditional_not_parent_signed",
            "parent_gap": "same missing signatures recur: P_tr/v_tr, q_loc, matter descent, no-marker constants, boundary no-tail",
            "if_closed": "this is the cleanest coupling-zero route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def double_zero_origin_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "origin_id": "DZO897_0_fixed_point_requirement",
            "object": "C_tr",
            "math_statement": "local GR needs C_tr(Phi0)=0 and partial_A C_tr(Phi0)=0 for any trace coupling altering metric/source charge",
            "current_status": "criterion_ready",
            "parent_gap": "criterion not specialized to trace sector from parent action",
            "if_closed": "first-order PPN/source-normalization leakage is theorem-zero",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "DZO897_1_norm_evenness",
            "object": "norm-square trace leakage",
            "math_statement": DOUBLE_ZERO_FORMULA,
            "current_status": "conditional_theorem_valid",
            "parent_gap": "Z_tr^A/G_AB/evenness symmetry not parent-owned for this trace branch",
            "if_closed": "linear leakage coefficient F_1 is killed by geometry rather than tuning",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "DZO897_2_composite_selector",
            "object": "Sigma_tr",
            "math_statement": "Sigma_tr=G_AB Y_tr^A Y_tr^B gives Sigma_tr=0 and delta Sigma_tr=0 when Y_tr=0",
            "current_status": "sufficient_mechanism",
            "parent_gap": "parent Euler equations do not yet force a trace-specific Y_tr=0 multiplet",
            "if_closed": "R11-style non-EH families can be factorized by a genuine double-zero selector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "DZO897_3_no_linear_marker",
            "object": "forbidden linear trace marker",
            "math_statement": "a linear term ell_A Z_tr^A is illegal only if no parent covector/marker exists in the trace leakage fibre",
            "current_status": "not_eliminated",
            "parent_gap": "no-marker theorem still has legal counterexamples",
            "if_closed": "leading scalar trace activation starts at quadratic order",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "origin_id": "DZO897_4_verdict",
            "object": "double-zero route",
            "math_statement": "double-zero is mathematically clean but not parent-signed for trace coupling",
            "current_status": "conditional_not_parent_signed",
            "parent_gap": "needs trace leakage variable, fibre metric, evenness/no-marker, gradient control, and branch selectivity",
            "if_closed": "local-GR coupling silence moves from closure to theorem target",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def coupling_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "CC897_0_zero_coupling_contract",
            "contract": "J_tr zero by source-cokernel",
            "required_parent_signature": "P_tr/v_tr local-vertical or rank-zero, q_loc matter descent, no-marker constants, boundary no-tail",
            "current_status": "not_signed",
            "promotion_effect": "alpha_tr source charge zero",
            "fallback_if_failed": "fill Q_tr/m, clock/species, and source-normalization residual rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC897_1_metric_leakage_contract",
            "contract": "C_tr double zero at local fixed point",
            "required_parent_signature": "C_tr=F(G_AB Z_tr^A Z_tr^B) or C_tr=Sigma_tr Cbar with parent-owned Z/Y/G and F(0)=0",
            "current_status": "not_signed",
            "promotion_effect": "first-order PPN/source-normalization leakage zero",
            "fallback_if_failed": "fill C_tr_gamma, C_tr_beta, C_tr_source, C_tr_clock residual vector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC897_2_no_pole_contract",
            "contract": "no local trace carrier",
            "required_parent_signature": "rank-zero/readout-only or constrained reduced inverse with no source-coupled pole",
            "current_status": "not_signed",
            "promotion_effect": "lambda_tr absent locally",
            "fallback_if_failed": "source Z_tr, mu_tr^2, lambda_tr from parent H_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "CC897_3_joint_GR_safe_contract",
            "contract": "trace sector cannot disturb local GR to first order",
            "required_parent_signature": "CC897_0 + CC897_1 + boundary no-tail, with EH same-frame limit",
            "current_status": "not_signed",
            "promotion_effect": "trace-sector q_loc contribution can be zero-returned",
            "fallback_if_failed": "construct residual vector and compare to local bounds later",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def counterexample_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "counterexample_id": "CE897_0_universal_conformal_trace",
            "legal_if_unsigned": "matter metric uses A_tr(phi_tr)^2 g_obs with universal A_tr",
            "damage": "WEP may survive while R10/orbital/PPN scalar force remains",
            "blocked_by": "source-cokernel descent or no local phi_tr pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE897_1_linear_marker_covector",
            "legal_if_unsigned": "parent action contains ell_A Z_tr^A O_matter",
            "damage": "double-zero fails and first-order source-normalization leakage returns",
            "blocked_by": "no-linear-marker/evenness theorem parent-signed for trace leakage bundle",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE897_2_species_constants_marker",
            "legal_if_unsigned": "masses, alpha_EM, binding energy, or clock transitions carry trace marker dependence",
            "damage": "clock/WEP/species channels activate despite metric descent",
            "blocked_by": "no-marker constant-sector theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE897_3_boundary_tail",
            "legal_if_unsigned": "endpoint/exact current has compact-domain tail",
            "damage": "rank-zero/readout route leaks into local fifth-force or orbital residuals",
            "blocked_by": "relative cohomology/support/no-tail theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "CE897_4_gradient_reentry",
            "legal_if_unsigned": "amplitude double-zero holds but gradients scale too sharply in transition region",
            "damage": "q_loc residual can reappear through nabla C_tr or boundary layer terms",
            "blocked_by": "gradient power-control theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def residual_vector_fallback_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "RV897_0_Qtr_over_m",
            "quantity": "Q_tr^A/m_A",
            "needed_if": "source-cokernel fails",
            "current_value": "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "arena": "R10,WEP,orbital",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RV897_1_Ztr_lambdatr",
            "quantity": "Z_tr,mu_tr^2,lambda_tr",
            "needed_if": "finite local trace carrier survives",
            "current_value": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "arena": "R10,orbital,PPN",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RV897_2_metric_PPN",
            "quantity": "C_tr_gamma,C_tr_beta,C_tr_alpha_i",
            "needed_if": "double-zero metric leakage fails",
            "current_value": "MISSING_WEAK_FIELD_RESPONSE_OPERATOR",
            "arena": "PPN,solar_system",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RV897_3_clock_species",
            "quantity": "C_tr_clock_i,Delta_AB_Qtr_over_m",
            "needed_if": "no-marker constants fail",
            "current_value": "MISSING_CLOCK_AND_BINDING_FUNCTIONAL",
            "arena": "clocks,WEP",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "RV897_4_boundary_tail",
            "quantity": "B_tr_tail,K_perp_trace",
            "needed_if": "boundary no-tail fails",
            "current_value": "MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND",
            "arena": "orbital,PPN,local_GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def conditional_local_gr_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "CLG897_0_trace_coupling_silence",
            "conditional_statement": "If EH same-frame holds, P_tr is local-vertical/rank-zero, matter descends through q_loc with no markers, C_tr has a parent double zero, and boundary trace tails vanish, then the trace sector contributes no first-order local force/source-normalization/PPN residual.",
            "proof_status": "conditional_valid",
            "parent_status": "not_signed",
            "unsigned_premises": "P_tr/v_tr, q_loc, matter descent, no-marker constants, double-zero origin, boundary no-tail",
            "claim_effect": "cannot promote local GR yet",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "CLG897_1_residual_fallback",
            "conditional_statement": "If any premise fails, the trace sector must be carried as an explicit residual vector rather than hidden inside a closure phrase.",
            "proof_status": "policy_gate_valid",
            "parent_status": "active_fallback",
            "unsigned_premises": "same as CLG897_0",
            "claim_effect": "future empirical testing must use sourced rows only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG897_0_Jtr_zero",
            "promotion_target": "J_tr=0/source-cokernel",
            "required_to_pass": "P_tr/v_tr local-vertical or rank-zero plus q_loc matter descent/no-marker/boundary no-tail",
            "current_evidence": "conditional theorem only",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG897_1_Ctr_double_zero",
            "promotion_target": "C_tr double-zero leakage silence",
            "required_to_pass": "parent-owned trace leakage variable, fibre metric, norm/evenness or composite selector factorization",
            "current_evidence": "criterion and conditional mechanisms only",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG897_2_no_pole",
            "promotion_target": "no local trace pole",
            "required_to_pass": "rank-zero/readout-only boundary support or reduced inverse no-pole theorem",
            "current_evidence": "conditional from 886/878",
            "gate_result": "fail_for_claim",
            "next_action": "carry no-pole as linked but unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG897_3_residual_vector",
            "promotion_target": "explicit residual vector executable later",
            "required_to_pass": "fallback rows have numeric/sourced values or theorem-zero entries",
            "current_evidence": "all fallback rows contain MISSING markers",
            "gate_result": "fail_for_claim",
            "next_action": "898 decides proof vs residual vector source fill",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG897_4_local_GR",
            "promotion_target": "local GR/Newton reduction",
            "required_to_pass": "trace coupling silence plus other q_loc residual channels controlled",
            "current_evidence": "trace coupling route conditional only",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC897_0_selected",
            "route": "trace_vertical_generator_matter_descent_signature_or_residual_vector",
            "status": "selected",
            "reason": "the source-cokernel and double-zero routes both reduce to the same parent signatures: actual vertical generator/readout status plus matter descent/no-marker; if those fail, a residual vector is mandatory",
            "include": "P_tr/v_tr ownership, Dq_loc[v_tr], matter descent stack, no-marker constants, source-cokernel pairing, residual vector fallback",
            "exclude": "claiming J_tr=0, claiming C_tr double-zero, numeric alpha pass, endpoint transfer, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG897_0_no_Jtr_zero_claim",
            "forbidden_claim": "J_tr=0 or source-cokernel is parent-derived",
            "status": "forbidden",
            "reason": "proof remains conditional on P_tr/q_loc/matter descent/no-tail signatures",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG897_1_no_double_zero_claim",
            "forbidden_claim": "trace C_tr double zero is parent-derived",
            "status": "forbidden",
            "reason": "norm-square/composite selector mechanisms are not specialized and parent-signed for trace coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG897_2_no_alpha_claim",
            "forbidden_claim": "alpha_tr or local residual vector is known",
            "status": "forbidden",
            "reason": "fallback rows are missing theorem-zero or numeric source-backed entries",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG897_3_no_local_GR_claim",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace coupling is only one conditional branch and remains unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG897_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "897 compresses the coupling problem into exact parent signatures and a fallback residual vector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D897_0",
            "finding": "source_cokernel_conditional_not_signed",
            "reason": "J_tr=0 follows only after P_tr/q_loc/matter descent/no-marker/no-tail signatures close",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D897_1",
            "finding": "double_zero_conditional_not_signed",
            "reason": "norm-square/composite selector mechanisms exist but are not trace-parent-owned",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D897_2",
            "finding": "residual_vector_required_if_signatures_fail",
            "reason": "without proof, the theory must expose Q_tr, Z_tr, lambda_tr, metric, clock, and boundary residual rows",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to parent-sign the actual trace vertical generator and matter-descent source-cokernel; if that fails, build the explicit residual vector rows needed for later R10/PPN/clock/orbital bounds",
            "include": "ell_tr/K_parent/v_tr ownership, Dq_loc[v_tr], S_matter descent, no-marker constants, boundary no-tail watch, residual vector schema",
            "exclude": "R10/PPN/local-GR pass, fitted tiny coupling, endpoint transfer, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_896_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_896_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    source_cokernel_rows_: list[dict[str, object]],
    double_zero_rows_: list[dict[str, object]],
    contract_rows_: list[dict[str, object]],
    counterexample_rows_: list[dict[str, object]],
    residual_rows_: list[dict[str, object]],
    local_gr_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        source_rows_,
        summary_rows_,
        source_cokernel_rows_,
        double_zero_rows_,
        contract_rows_,
        counterexample_rows_,
        residual_rows_,
        local_gr_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V897_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V897_1_prior_896_clean",
            "result": "pass" if prior_896_clean() else "fail",
            "detail": "P8_Y5_BRR545_896_VALIDATION.csv clean",
        },
        {
            "check_id": "V897_2_source_cokernel_not_promoted",
            "result": "pass"
            if any(row["attempt_id"] == "SCA897_4_verdict" and row["current_status"] == "conditional_not_parent_signed" for row in source_cokernel_rows_)
            else "fail",
            "detail": "J_tr source-cokernel remains conditional",
        },
        {
            "check_id": "V897_3_double_zero_not_promoted",
            "result": "pass"
            if any(row["origin_id"] == "DZO897_4_verdict" and row["current_status"] == "conditional_not_parent_signed" for row in double_zero_rows_)
            else "fail",
            "detail": "trace double-zero route remains conditional",
        },
        {
            "check_id": "V897_4_coupling_contract_complete",
            "result": "pass" if len(contract_rows_) == 4 else "fail",
            "detail": "zero coupling, metric leakage, no-pole, and joint GR-safe contracts recorded",
        },
        {
            "check_id": "V897_5_counterexamples_recorded",
            "result": "pass" if len(counterexample_rows_) == 5 else "fail",
            "detail": "linear marker, conformal trace, species marker, boundary tail, and gradient re-entry counterexamples recorded",
        },
        {
            "check_id": "V897_6_residual_vector_missing_nonclaim",
            "result": "pass"
            if all("MISSING" in str(row["current_value"]) and not bool(row["valid_for_claim"]) for row in residual_rows_)
            else "fail",
            "detail": "fallback residual vector rows remain missing/nonclaim",
        },
        {
            "check_id": "V897_7_conditional_GR_nonclaim",
            "result": "pass" if all(not bool(row["valid_for_claim"]) for row in local_gr_rows_) else "fail",
            "detail": "conditional local-GR coupling lemma remains nonclaim",
        },
        {
            "check_id": "V897_8_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V897_9_claim_allowed_false",
            "result": "pass" if all(not bool(row["claim_allowed"]) for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V897_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V897_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V897_12_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V897_13_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    source_cokernel_rows_: list[dict[str, object]],
    double_zero_rows_: list[dict[str, object]],
    contract_rows_: list[dict[str, object]],
    counterexample_rows_: list[dict[str, object]],
    residual_rows_: list[dict[str, object]],
    local_gr_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 897 - Y5/R10 Coupling-Origin Source-Cokernel And Double-Zero Hunt

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the coupling bottleneck is now written as two exact but unsigned routes**:

1. `{SOURCE_COKERNEL_FORMULA}`
2. `{DOUBLE_ZERO_FORMULA}`

Neither is parent-signed yet. The good news is that this is not vague anymore: the local-GR-safe path needs actual `P_tr/v_tr` verticality or rank-zero, matter descent through `q_loc`, no marker constants, trace double-zero/evenness, and boundary no-tail. If any of these fail, the theory must expose a residual vector instead of hiding the coupling.

## Exact 897 Finding
The trace branch is not dead, but it is not free. To reduce to GR/Newton in the serious sense, MTS needs either a theorem-zero coupling route or a sourced residual vector. The best theorem-zero route is now: `J_tr=0` by source-cokernel plus `C_tr` double-zero by norm/evenness/composite-selector structure. The current corpus supplies valid conditional mathematics for both, but not the parent signatures. Therefore no local-GR, R10, PPN, clock, WEP, or orbital pass is claimed.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Source-Cokernel Proof Attempt
{md_table(source_cokernel_rows_)}

## Double-Zero Origin Audit
{md_table(double_zero_rows_)}

## Coupling Contract
{md_table(contract_rows_)}

## Counterexample Ledger
{md_table(counterexample_rows_)}

## Residual Vector Fallback
{md_table(residual_rows_)}

## Conditional Local-GR Lemma
{md_table(local_gr_rows_)}

## Promotion Gate
{md_table(promotion_rows_)}

## Route Choice
{md_table(route_rows_)}

## Claim Guard
{md_table(claim_rows_)}

## Decision
{md_table(decision_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    source_cokernel_rows_ = source_cokernel_attempt_rows(generated_utc)
    double_zero_rows_ = double_zero_origin_rows(generated_utc)
    contract_rows_ = coupling_contract_rows(generated_utc)
    counterexample_rows_ = counterexample_rows(generated_utc)
    residual_rows_ = residual_vector_fallback_rows(generated_utc)
    local_gr_rows_ = conditional_local_gr_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        source_cokernel_rows_,
        double_zero_rows_,
        contract_rows_,
        counterexample_rows_,
        residual_rows_,
        local_gr_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_897_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_897_SOURCE_COKERNEL_PROOF_ATTEMPT.csv": source_cokernel_rows_,
        "P8_Y5_R10_897_DOUBLE_ZERO_ORIGIN_AUDIT.csv": double_zero_rows_,
        "P8_Y5_R10_897_COUPLING_CONTRACT.csv": contract_rows_,
        "P8_Y5_R10_897_COUNTEREXAMPLE_LEDGER.csv": counterexample_rows_,
        "P8_Y5_R10_897_RESIDUAL_VECTOR_FALLBACK.csv": residual_rows_,
        "P8_Y5_R10_897_CONDITIONAL_LOCAL_GR_LEMMA.csv": local_gr_rows_,
        "P8_Y5_R10_897_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_897_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_897_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_897_DECISION.csv": decision_rows_,
        "P8_Y5_R10_897_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_897_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_897_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "897-Y5-R10-coupling-origin-source-cokernel-and-double-zero-hunt.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        source_cokernel_rows_,
        double_zero_rows_,
        contract_rows_,
        counterexample_rows_,
        residual_rows_,
        local_gr_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_897_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
