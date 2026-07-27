from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_896_trace_action_parent_adoption_gate_run_no_parent_adoption_zero_route_unsigned_finite_branch_closure_only"
CLAIM_CEILING = "parent_adoption_gate_only_no_finite_trace_carrier_no_no_pole_theorem_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "897-Y5-R10-coupling-origin-source-cokernel-and-double-zero-hunt.md"

ACTION_ANSATZ = (
    "S_tr^(2)=1/2 int_U sqrt(-g_obs)[Z_tr g_obs^{mu nu} nabla_mu phi_tr nabla_nu phi_tr "
    "+ mu_tr^2 phi_tr^2 + 2 xi_tr R[g_obs] phi_tr^2] + int_U sqrt(-g_obs) phi_tr J_tr"
)

SOURCE_SPECS = [
    {
        "source_id": "895_doc",
        "path": ROOT / "895-Y5-R10-parent-quadratic-trace-action-ansatz-or-closure-demotion.md",
        "needle": "finite trace branch as an exact adoption contract",
        "role": "immediate adoption-gate handoff",
    },
    {
        "source_id": "895_validation",
        "path": OUT / "P8_Y5_BRR545_895_VALIDATION.csv",
        "needle": "V895_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "895_contract",
        "path": OUT / "P8_Y5_R10_895_QUADRATIC_TRACE_ACTION_CONTRACT.csv",
        "needle": "QTC895_8_parent_adoption_verdict",
        "role": "full trace-action adoption contract",
    },
    {
        "source_id": "895_symbol_readout",
        "path": OUT / "P8_Y5_R10_895_SYMBOL_READOUT_ROWS.csv",
        "needle": "SRR895_4_Jtr",
        "role": "blocked J_tr and alpha_tr source readouts",
    },
    {
        "source_id": "895_closure_rule",
        "path": OUT / "P8_Y5_R10_895_CLOSURE_DEMOTION_RULE.csv",
        "needle": "CDR895_0_contract_only",
        "role": "contract-only demotion rule",
    },
    {
        "source_id": "511_fixed_point",
        "path": ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "needle": "FP511_1_double_zero_nonEH_coupling",
        "role": "double-zero non-EH coupling target",
    },
    {
        "source_id": "382_local_action",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "S_X_auxiliary_or_mass_gap",
        "role": "parent local action auxiliary/mass-gap fallback",
    },
    {
        "source_id": "407_action_sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needle": "S_matter_quotient_functor",
        "role": "matter quotient/descent sketch",
    },
    {
        "source_id": "177_parent_action_contract",
        "path": ROOT / "177-parent-action-perturbation-local-GR-contract.md",
        "needle": "delta_g S_parent = 0",
        "role": "parent variation contract",
    },
    {
        "source_id": "877_htr_skeleton",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "H_tr=P_tr^dagger Hess(S_parent) P_tr",
        "role": "minimal trace Hessian skeleton",
    },
    {
        "source_id": "880_endpoint_action",
        "path": ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md",
        "needle": "K_endpoint=diag(6,6)",
        "role": "endpoint action and local transfer blocker",
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
            "what_changed": "ran the 895 trace-action parent-adoption gate against current parent-action sources and registered the zero-vs-finite branch decision",
            "best_partial_result": "the exact local-GR bottleneck is now isolated as coupling ownership: either J_tr/source-cokernel and double-zero leakage are parent-signed, or the trace branch cannot become a GR-safe local sector",
            "hard_blockers": "no source currently adopts the trace action as P_tr^dagger Hess(S_parent)P_tr, no source signs J_tr=0 or numeric J_tr, no trace-specific double-zero proof, no boundary no-tail theorem, no no-pole theorem",
            "what_is_not_claimed": "parent-adopted finite trace action, zero/no-pole trace theorem, numeric Z_tr, numeric lambda_tr, alpha_tr, R10/PPN/clock/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def adoption_clause_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "ACA896_0_parent_field_domain",
            "895_clause": "phi_tr=P_tr delta Phi",
            "adoption_test": "parent action names the quotient/gauge-reduced trace tangent direction and its source-domain projector",
            "current_evidence": "trace projector remains a contract/readout target",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "without a parent-owned trace direction, local extra hair cannot be compared to GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ACA896_1_parent_Hessian",
            "895_clause": "H_tr=P_tr^dagger Hess(S_parent)P_tr",
            "adoption_test": "written parent action is varied twice and projected onto trace sector",
            "current_evidence": "877 gives the skeleton but not a computed Hessian",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "GR reduction needs the extra-sector operator fixed by the same parent variational principle",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ACA896_2_Ztr_symbol",
            "895_clause": "Z_tr principal symbol",
            "adoption_test": "sigma_2(H_tr)(k)=Z_tr g_obs^{mu nu} k_mu k_nu with sign and units",
            "current_evidence": "missing; endpoint transfer rejected in 894",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "unknown kinetic normalization makes fifth-force amplitude and ghost sign unknowable",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ACA896_3_mass_gap",
            "895_clause": "mu_tr^2 and lambda_tr",
            "adoption_test": "zeroth-order symbol gives m_tr^2=mu_tr^2/Z_tr or no-pole theorem removes the range",
            "current_evidence": "missing mass gap and missing no-pole certificate",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "local tests need either a finite range/coupling or a theorem-zero local mode",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ACA896_4_double_zero",
            "895_clause": "C_tr(Phi0)=0 and partial_A C_tr(Phi0)=0",
            "adoption_test": "parent action proves trace-sector non-EH metric mixing has a double zero at the local fixed point",
            "current_evidence": "511 gives the exact criterion but not a trace-specific proof",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "this is the cleanest route to suppressing first-order PPN/source-normalization leakage",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ACA896_5_source_coupling",
            "895_clause": "J_tr=P_tr^dagger J_parent",
            "adoption_test": "matter descent/source-cokernel proves J_tr=0 or supplies arena charges",
            "current_evidence": "407 supplies a quotient-matter sketch; no trace-specific J_tr proof or charge exists",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "this is the coupling bottleneck; no source coupling means no honest alpha_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "ACA896_6_boundary_no_tail",
            "895_clause": "boundary/local projection silence",
            "adoption_test": "parent variational boundary term has no local tail or is fixed by admissible local-vacuum conditions",
            "current_evidence": "endpoint algebra exists but no local no-tail theorem",
            "gate_result": "fail_for_claim",
            "why_it_matters_for_GR": "boundary readouts must not re-enter as local fifth-force hair",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def parent_action_candidate_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "PAC896_0_177_parent_contract",
            "source": "177 parent-action perturbation contract",
            "what_it_supplies": "global variation checklist for metric, load tensor, domains, memory, and endpoint terms",
            "adopts_895_trace_action": False,
            "missing_for_adoption": "no trace projector, no trace Hessian, no Z_tr/mu_tr^2/J_tr readout",
            "best_use": "keeps full parent-action discipline in view",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAC896_1_382_local_action_contract",
            "source": "382 parent local action minimal contract",
            "what_it_supplies": "auxiliary/no-hair or alpha_X(lambda_X) fallback structure",
            "adopts_895_trace_action": False,
            "missing_for_adoption": "contract only; not varied into a trace-specific H_tr",
            "best_use": "maps finite-vs-no-hair alternatives",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAC896_2_407_relational_quotient_sketch",
            "source": "407 primitive relational quotient action sketch",
            "what_it_supplies": "matter quotient functor and same-frame action sketch",
            "adopts_895_trace_action": False,
            "missing_for_adoption": "quotient functor is sufficient-axiom/sketch level; no trace J_tr theorem",
            "best_use": "best current source for J_tr=0/source-cokernel hunt",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAC896_3_511_fixed_point_ansatz",
            "source": "511 minimal parent action local-GR fixed-point ansatz",
            "what_it_supplies": "S_extra template, double-zero criterion, positive mass-gap criterion",
            "adopts_895_trace_action": False,
            "missing_for_adoption": "criterion not specialized to phi_tr, P_tr, J_tr, or H_tr",
            "best_use": "best current double-zero/local-GR silence contract",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAC896_4_877_Htr_skeleton",
            "source": "877 parent trace Hessian skeleton",
            "what_it_supplies": "exact required form H_tr=P_tr^dagger Hess(S_parent) P_tr",
            "adopts_895_trace_action": False,
            "missing_for_adoption": "skeleton not populated by an actual S_parent variation",
            "best_use": "operator extraction law",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAC896_5_880_endpoint_action",
            "source": "880 endpoint Hessian/action contract",
            "what_it_supplies": "endpoint K block and K_parent extension target",
            "adopts_895_trace_action": False,
            "missing_for_adoption": "endpoint block is not a local spacetime trace operator",
            "best_use": "possible future pairing aid, not local Z_tr/lambda_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def branch_register_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BR896_0_parent_adopted_finite",
            "branch": "finite trace action adopted by S_parent",
            "required_signature": "P_tr,H_tr,Z_tr,mu_tr^2,J_tr,double-zero/boundary/provenance all source-backed",
            "current_status": "not_adopted",
            "decision": "demote_to_closure_only",
            "next_action": "do not score R10/PPN until adoption exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BR896_1_zero_no_pole",
            "branch": "trace is EH/gauge/constraint/readout-only",
            "required_signature": "rank-zero or constraint-null reduced inverse plus source-cokernel and boundary no-tail",
            "current_status": "not_signed",
            "decision": "watch_as_best_GR_safe_route",
            "next_action": "derive coupling/source-cokernel and double-zero clauses first",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BR896_2_coupling_origin",
            "branch": "source coupling/double-zero origin",
            "required_signature": "J_tr=0 by matter quotient descent or explicit small residual vector; C_tr double zero at Phi0",
            "current_status": "selected_next",
            "decision": "hunt_next",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def coupling_bottleneck_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coupling_id": "CB896_0_Jtr_zero",
            "object": "J_tr",
            "best_route": "prove P_tr lies in the matter-source cokernel induced by quotient-invariant matter descent",
            "current_status": "not_proved",
            "if_success": "finite trace branch can be source-silent even before numeric alpha_tr",
            "if_failure": "must source arena-specific charges and compare to R10/PPN/clocks/orbits",
            "selected_for_897": True,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coupling_id": "CB896_1_double_zero",
            "object": "C_tr(Phi0), partial_A C_tr(Phi0)",
            "best_route": "derive double zero from fixed-point/stationarity/symmetry rather than assuming it",
            "current_status": "criterion_exists_not_trace_signed",
            "if_success": "first-order PPN/source-normalization leakage is theorem-zero",
            "if_failure": "must build and bound a PPN residual vector",
            "selected_for_897": True,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coupling_id": "CB896_2_boundary_tail",
            "object": "boundary trace tail",
            "best_route": "show endpoint/readout variation is fixed, pure boundary, or source-cokernel silent in local exterior",
            "current_status": "not_proved",
            "if_success": "endpoint progress does not leak into local fifth-force hair",
            "if_failure": "boundary charge coefficients must be sourced",
            "selected_for_897": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "coupling_id": "CB896_3_numeric_alpha_fallback",
            "object": "alpha_tr(lambda_tr)",
            "best_route": "only after Z_tr, lambda_tr, and J_tr are source-backed",
            "current_status": "not_executable",
            "if_success": "empirical local comparison can begin",
            "if_failure": "remain closure-only",
            "selected_for_897": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def conditional_gr_reduction_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "CGR896_0_trace_silence_conditional",
            "conditional_statement": "If the EH same-frame limit holds, matter descends only through observed variables, P_tr is in the matter-source cokernel, non-EH trace metric couplings have a double zero, and boundary trace tails vanish, then q_loc^nu receives no first-order trace-sector source.",
            "current_truth_status": "conditional_only",
            "unsigned_premises": "EH same-frame proof, P_tr/source-cokernel, trace double-zero, boundary no-tail",
            "impact": "this is the GR-safe route: derive silence rather than tune a tiny coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "CGR896_1_finite_branch_conditional",
            "conditional_statement": "If the parent action adopts the finite trace Hessian and J_tr is nonzero, local GR requires the resulting PPN/R10 residual vector to sit below bounds without fitted silence.",
            "current_truth_status": "conditional_only",
            "unsigned_premises": "parent finite adoption, Z_tr, lambda_tr, J_tr, matter normalization",
            "impact": "finite branch remains possible but less GR-safe and more empirically exposed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG896_0_parent_adoption",
            "promotion_target": "895 contract adopted by S_parent",
            "required_to_pass": "a source-backed second variation produces every trace coefficient and coupling",
            "current_evidence": "all current parent sources are sketches/contracts/skeletons",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG896_1_zero_no_pole",
            "promotion_target": "trace no local pole",
            "required_to_pass": "constraint/readout-only reduced inverse plus source-cokernel plus boundary no-tail",
            "current_evidence": "unsigned",
            "gate_result": "fail_for_claim",
            "next_action": "prove coupling/source-cokernel first",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG896_2_coupling_silence",
            "promotion_target": "J_tr and first-order metric leakage vanish",
            "required_to_pass": "J_tr=0 and double-zero theorem for trace sector",
            "current_evidence": "criterion only",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG896_3_local_GR",
            "promotion_target": "local GR/Newton reduction",
            "required_to_pass": "EH same-frame limit plus trace/source/boundary silence or bounded residual vector",
            "current_evidence": "trace/coupling branch unresolved",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC896_0_selected",
            "route": "coupling_origin_source_cokernel_and_double_zero_hunt",
            "status": "selected",
            "reason": "parent adoption failed and zero/no-pole is unsigned; the shared bottleneck is coupling ownership, especially J_tr and trace double-zero leakage",
            "include": "matter quotient descent, source-cokernel, P_tr verticality/readout status, C_tr double-zero, boundary tail watch",
            "exclude": "numeric alpha claim, R10/PPN pass, endpoint transfer, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG896_0_no_parent_adoption_claim",
            "forbidden_claim": "895 trace action is parent-derived",
            "status": "forbidden",
            "reason": "adoption gate fails for every current parent-action candidate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG896_1_no_zero_route_claim",
            "forbidden_claim": "trace has no source-coupled local pole",
            "status": "forbidden",
            "reason": "source-cokernel and boundary no-tail are not signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG896_2_no_coupling_claim",
            "forbidden_claim": "J_tr=0, alpha_tr is known, or double-zero leakage is proved",
            "status": "forbidden",
            "reason": "coupling origin is selected as next target, not solved in 896",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG896_3_no_empirical_claim",
            "forbidden_claim": "R10/PPN/clock/orbital/local-GR branch passes",
            "status": "forbidden",
            "reason": "trace/coupling sector is not promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG896_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "896 narrows the missing GR bridge to coupling ownership without pretending it is solved",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D896_0",
            "finding": "parent_adoption_gate_failed",
            "reason": "current parent-action sources do not compute the 895 trace Hessian or source coupling",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D896_1",
            "finding": "finite_branch_closure_only",
            "reason": "a contract-only finite trace field cannot be used for R10/PPN/local-GR claims",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D896_2",
            "finding": "coupling_bottleneck_selected",
            "reason": "both the finite route and zero route require source-cokernel/double-zero control",
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
            "objective": "hunt the parent origin of trace-sector coupling: prove J_tr=0/source-cokernel and trace double-zero leakage, or produce explicit residual couplings for later bounds",
            "include": "matter quotient descent, P_tr source-cokernel, C_tr(Phi0)=0, partial_A C_tr(Phi0)=0, boundary no-tail watch, GR-safe conditional theorem",
            "exclude": "numeric alpha claim, empirical pass, endpoint transfer, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_895_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_895_VALIDATION.csv"
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
    adoption_rows_: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    coupling_rows_: list[dict[str, object]],
    gr_rows_: list[dict[str, object]],
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
        adoption_rows_,
        candidate_rows_,
        branch_rows_,
        coupling_rows_,
        gr_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V896_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V896_1_prior_895_clean",
            "result": "pass" if prior_895_clean() else "fail",
            "detail": "P8_Y5_BRR545_895_VALIDATION.csv clean",
        },
        {
            "check_id": "V896_2_adoption_clause_audit_complete",
            "result": "pass" if len(adoption_rows_) == 7 else "fail",
            "detail": "domain/Hessian/Z/mass/double-zero/source/boundary clauses audited",
        },
        {
            "check_id": "V896_3_no_candidate_adopts_trace_action",
            "result": "pass" if all(not bool(row["adopts_895_trace_action"]) for row in candidate_rows_) else "fail",
            "detail": "no current parent-action candidate adopts the 895 trace action",
        },
        {
            "check_id": "V896_4_finite_branch_closure_only",
            "result": "pass"
            if any(row["branch_id"] == "BR896_0_parent_adopted_finite" and row["decision"] == "demote_to_closure_only" for row in branch_rows_)
            else "fail",
            "detail": "finite trace branch demoted to closure-only",
        },
        {
            "check_id": "V896_5_zero_route_unsigned",
            "result": "pass"
            if any(row["branch_id"] == "BR896_1_zero_no_pole" and row["current_status"] == "not_signed" for row in branch_rows_)
            else "fail",
            "detail": "zero/no-pole route remains unsigned",
        },
        {
            "check_id": "V896_6_coupling_bottleneck_selected",
            "result": "pass"
            if route_rows_ and route_rows_[0]["route"] == "coupling_origin_source_cokernel_and_double_zero_hunt"
            else "fail",
            "detail": "J_tr/source-cokernel and double-zero selected as next target",
        },
        {
            "check_id": "V896_7_conditional_GR_rows_nonclaim",
            "result": "pass" if all(row["current_truth_status"] == "conditional_only" for row in gr_rows_) else "fail",
            "detail": "conditional GR reduction lemmas remain nonclaim",
        },
        {
            "check_id": "V896_8_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V896_9_claim_allowed_false",
            "result": "pass" if all(not bool(row["claim_allowed"]) for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V896_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V896_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V896_12_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V896_13_validation_rows_ready",
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
    adoption_rows_: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    coupling_rows_: list[dict[str, object]],
    gr_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 896 - Y5/R10 Trace-Action Parent-Adoption Gate And Zero-Vs-Finite Branch Register

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the 895 finite trace action is not parent-adopted by the current corpus**. The action contract remains:

`{ACTION_ANSATZ}`

The gate fails because no current parent-action source computes `P_tr`, `H_tr=P_tr^dagger Hess(S_parent)P_tr`, `Z_tr`, `mu_tr^2`, `J_tr`, trace-sector double-zero leakage, and boundary no-tail together. The finite branch is therefore closure-only. The zero/no-pole branch is still the cleaner GR-safe route, but it is also unsigned because the matter source-cokernel and boundary no-tail clauses are missing.

## Exact 896 Finding
The bottleneck has narrowed to **coupling ownership**. Both plausible routes need it: the finite route needs `J_tr` and `alpha_tr(lambda_tr)` sourced, while the GR-safe zero route needs `J_tr=0` plus double-zero metric leakage and no boundary tail. So the next best target is not another empirical run and not a fitted tiny coupling; it is a parent proof of source-cokernel/double-zero silence, or an honest residual vector if that proof fails.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Adoption Clause Audit
{md_table(adoption_rows_)}

## Parent Action Candidate Audit
{md_table(candidate_rows_)}

## Branch Register
{md_table(branch_rows_)}

## Coupling Bottleneck Register
{md_table(coupling_rows_)}

## Conditional GR Reduction Rows
{md_table(gr_rows_)}

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
    adoption_rows_ = adoption_clause_audit_rows(generated_utc)
    candidate_rows_ = parent_action_candidate_audit_rows(generated_utc)
    branch_rows_ = branch_register_rows(generated_utc)
    coupling_rows_ = coupling_bottleneck_rows(generated_utc)
    gr_rows_ = conditional_gr_reduction_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        adoption_rows_,
        candidate_rows_,
        branch_rows_,
        coupling_rows_,
        gr_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_896_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_896_ADOPTION_CLAUSE_AUDIT.csv": adoption_rows_,
        "P8_Y5_R10_896_PARENT_ACTION_CANDIDATE_AUDIT.csv": candidate_rows_,
        "P8_Y5_R10_896_BRANCH_REGISTER.csv": branch_rows_,
        "P8_Y5_R10_896_COUPLING_BOTTLENECK_REGISTER.csv": coupling_rows_,
        "P8_Y5_R10_896_CONDITIONAL_GR_REDUCTION_ROWS.csv": gr_rows_,
        "P8_Y5_R10_896_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_896_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_896_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_896_DECISION.csv": decision_rows_,
        "P8_Y5_R10_896_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_896_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_896_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "896-Y5-R10-trace-action-parent-adoption-gate-and-zero-vs-finite-branch-register.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        adoption_rows_,
        candidate_rows_,
        branch_rows_,
        coupling_rows_,
        gr_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_896_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
