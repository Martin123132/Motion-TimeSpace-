from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_895_parent_quadratic_trace_action_contract_written_as_nonclaim_ansatz_closure_demotion_gate_open"
CLAIM_CEILING = "quadratic_trace_action_contract_only_no_parent_adoption_no_Ztr_lambdatr_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "896-Y5-R10-trace-action-parent-adoption-gate-and-zero-vs-finite-branch-register.md"

ACTION_ANSATZ = (
    "S_tr^(2)=1/2 int_U sqrt(-g_obs)[Z_tr g_obs^{mu nu} nabla_mu phi_tr nabla_nu phi_tr "
    "+ mu_tr^2 phi_tr^2 + 2 xi_tr R[g_obs] phi_tr^2] + int_U sqrt(-g_obs) phi_tr J_tr"
)

SOURCE_SPECS = [
    {
        "source_id": "894_doc",
        "path": ROOT / "894-Y5-R10-Htr-principal-symbol-and-mass-gap-source-fill.md",
        "needle": "parent quadratic trace-action ansatz/contract or demote the finite branch to closure-only",
        "role": "immediate handoff requiring either explicit trace action contract or closure demotion",
    },
    {
        "source_id": "894_validation",
        "path": OUT / "P8_Y5_BRR545_894_VALIDATION.csv",
        "needle": "V894_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "894_source_fill",
        "path": OUT / "P8_Y5_R10_894_SOURCE_FILL_ROWS.csv",
        "needle": "SFR894_2_Ztr",
        "role": "unsourced Z_tr/lambda_tr fill rows",
    },
    {
        "source_id": "894_branch",
        "path": OUT / "P8_Y5_R10_894_BRANCH_CLASSIFICATION.csv",
        "needle": "BCL894_3_new_parent_quadratic_trace_action",
        "role": "finite trace field branch not written in 894",
    },
    {
        "source_id": "894_endpoint_transfer",
        "path": OUT / "P8_Y5_R10_894_ENDPOINT_TRANSFER_AUDIT.csv",
        "needle": "ETA894_3_verdict",
        "role": "endpoint-to-local transfer rejection",
    },
    {
        "source_id": "511_fixed_point",
        "path": ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "needle": "A511_3_extra_field_silence",
        "role": "extra-field silence, double-zero, and positive mass-gap action template",
    },
    {
        "source_id": "382_local_action",
        "path": ROOT / "382-parent-local-action-minimal-contract.md",
        "needle": "S_X_auxiliary_or_mass_gap",
        "role": "parent local action contract and auxiliary/mass-gap fallback",
    },
    {
        "source_id": "407_action_sketch",
        "path": ROOT / "407-primitive-relational-quotient-action-sketch.md",
        "needle": "S_geom_same_frame",
        "role": "primitive relational quotient action sketch",
    },
    {
        "source_id": "177_parent_action_contract",
        "path": ROOT / "177-parent-action-perturbation-local-GR-contract.md",
        "needle": "S_parent =",
        "role": "early parent-action perturbation contract",
    },
    {
        "source_id": "877_htr_skeleton",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "H_tr=P_tr^dagger Hess(S_parent) P_tr",
        "role": "minimal parent trace Hessian skeleton",
    },
    {
        "source_id": "880_endpoint_action",
        "path": ROOT / "880-Y5-R10-minimal-Qtrace-Qstar-Kparent-action-contract-or-retained-cT-bound.md",
        "needle": "K_endpoint=diag(6,6)",
        "role": "endpoint Hessian candidate and K_parent blocker",
    },
    {
        "source_id": "880_minimal_action_contract",
        "path": OUT / "P8_Y5_R10_880_MINIMAL_ACTION_CONTRACT.csv",
        "needle": "MAC880_4_parent_pairing_extension",
        "role": "K_parent extension blocker",
    },
    {
        "source_id": "885_htr_fill",
        "path": OUT / "P8_Y5_R10_885_HTR_ZERO_POLE_SOURCE_FILL.csv",
        "needle": "HZ885_4_Ztr_mtr_lambda",
        "role": "prior H_tr zero-pole/source fill row",
    },
    {
        "source_id": "892_trace_rows",
        "path": OUT / "P8_Y5_R10_892_TRACE_HESSIAN_SOURCE_ROWS.csv",
        "needle": "THS892_1_Ztr_principal_symbol",
        "role": "trace Hessian source rows",
    },
    {
        "source_id": "893_htr_fill",
        "path": OUT / "P8_Y5_R10_893_HTR_PRINCIPAL_SYMBOL_FILL.csv",
        "needle": "HSF893_2_principal_symbol",
        "role": "finite H_tr principal-symbol fill rows",
    },
    {
        "source_id": "654_local_gr_spine",
        "path": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needle": "R10_fifth_force",
        "role": "local-GR/R10 fifth-force gate status",
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
            "what_changed": "wrote the exact finite trace quadratic action contract and the rule that demotes it to closure-only unless a parent action adopts every clause",
            "best_partial_result": "the finite branch now has a precise adoption target: P_tr, H_tr, Z_tr, mu_tr^2, xi_tr, J_tr, boundary/no-tail, units, and provenance must all be parent-owned before any R10/PPN/local-GR scoring",
            "hard_blockers": "ansatz not parent-adopted, P_tr still missing, parent Hessian still missing, Z_tr and mu_tr^2 still unsourced, J_tr/source-cokernel still unsigned, boundary/no-tail still unsigned",
            "what_is_not_claimed": "finite trace carrier, numeric Z_tr, numeric mu_tr^2, lambda_tr, source coupling, R10 pass, PPN pass, clock/WEP/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def quadratic_trace_action_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "QTC895_0_domain_projector",
            "object": "phi_tr=P_tr delta Phi",
            "required_parent_statement": "P_tr is a parent-owned quotient/gauge-reduced trace projector with source-domain selection and units",
            "current_895_status": "MISSING_PARENT_PROJECTOR",
            "failure_mode": "without P_tr the scalar trace field is not a defined local degree of freedom",
            "action_if_sourced": "use P_tr to form H_tr=P_tr^dagger Hess(S_parent) P_tr",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_1_quadratic_action",
            "object": "finite trace quadratic action",
            "required_parent_statement": ACTION_ANSATZ,
            "current_895_status": "ANSATZ_NOT_PARENT_ADOPTED",
            "failure_mode": "a written template is not a derivation from S_parent",
            "action_if_sourced": "vary twice and read principal/zeroth-order symbols before any empirical branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_2_kinetic_normalization",
            "object": "Z_tr",
            "required_parent_statement": "Z_tr is the coefficient of g_obs^{mu nu} k_mu k_nu in sigma_2(H_tr), after canonical normalization from parent G_AB/Hessian",
            "current_895_status": "MISSING_PRINCIPAL_SYMBOL",
            "failure_mode": "ghost sign, normalization, and alpha amplitude cannot be known",
            "action_if_sourced": "populate Z_tr and kinetic sign row with provenance",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_3_mass_gap",
            "object": "mu_tr^2 and lambda_tr",
            "required_parent_statement": "mu_tr^2 is the zeroth-order trace symbol from the same H_tr; m_tr^2=mu_tr^2/Z_tr and lambda_tr=1/m_tr in natural units",
            "current_895_status": "MISSING_ZEROTH_ORDER_SYMBOL",
            "failure_mode": "range cannot be bounded or compared to R10/local tests",
            "action_if_sourced": "populate mu_tr^2, m_tr, lambda_tr with units and source path",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_4_curvature_metric_mixing",
            "object": "xi_tr and non-EH metric mixing",
            "required_parent_statement": "all non-EH metric-coupling functions obey C_tr(Phi0)=0 and partial_A C_tr(Phi0)=0, or an explicit nonzero PPN/WEP residual is sourced",
            "current_895_status": "DOUBLE_ZERO_NOT_SIGNED_FOR_TRACE",
            "failure_mode": "first-order metric/source-normalization leakage would violate the local-GR target",
            "action_if_sourced": "route to zero leakage theorem or numeric PPN residual vector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_5_source_coupling",
            "object": "J_tr=P_tr^dagger J_parent",
            "required_parent_statement": "J_tr is either parent-zero by quotient-invariant matter descent/source-cokernel or source-backed with arena-specific charges",
            "current_895_status": "SOURCE_COKERNEL_NOT_SIGNED",
            "failure_mode": "a finite field with unknown source coupling cannot be scored or declared silent",
            "action_if_sourced": "derive alpha_tr(lambda_tr) or theorem-zero source projection",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_6_boundary_no_tail",
            "object": "boundary/local projection silence",
            "required_parent_statement": "boundary terms vanish, are fixed, or have no local tail in the trace sector under admissible local-vacuum boundary conditions",
            "current_895_status": "BOUNDARY_NO_TAIL_NOT_SIGNED",
            "failure_mode": "endpoint algebra may re-enter as local hair unless a no-tail theorem is signed",
            "action_if_sourced": "choose no-pole/readout-only route or add boundary charge coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_7_units_provenance",
            "object": "units and source paths",
            "required_parent_statement": "every coefficient has dimensions, sign convention, source file, and extraction path from the parent action",
            "current_895_status": "PROVENANCE_CONTRACT_ONLY",
            "failure_mode": "numbers would be closure knobs rather than theory outputs",
            "action_if_sourced": "promote only rows with no MISSING markers and valid units",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QTC895_8_parent_adoption_verdict",
            "object": "finite trace branch",
            "required_parent_statement": "the full contract is adopted as an actual second variation of S_parent, or the branch is closure-only",
            "current_895_status": "ansatz_not_parent_adopted",
            "failure_mode": "finite trace carrier remains nonclaim and cannot be used to pass R10/PPN/local GR",
            "action_if_sourced": "run 896 parent-adoption gate; otherwise keep closure-only register",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def variational_consistency_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "VCG895_0_parent_variation",
            "gate": "delta^2 S_parent projection",
            "required_test": "show the contract is literally P_tr^dagger Hess(S_parent)P_tr, not an added effective field",
            "current_status": "not_performed",
            "claim_effect": "blocks finite H_tr promotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VCG895_1_covariance",
            "gate": "covariant scalar operator",
            "required_test": "all terms use the same observed metric/coframe and have scalar density sqrt(-g_obs)",
            "current_status": "contract_specified_not_derived",
            "claim_effect": "covariance remains a checklist item",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VCG895_2_second_order_field_equation",
            "gate": "trace Euler-Lagrange equation",
            "required_test": "variation yields Z_tr box phi_tr - mu_tr^2 phi_tr - 2 xi_tr R phi_tr = J_tr plus signed boundary terms",
            "current_status": "template_only",
            "claim_effect": "operator readout not executable",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VCG895_3_ghost_tachyon",
            "gate": "positive kinetic and mass sector",
            "required_test": "Z_tr>0 and mu_tr^2>=0, or prove auxiliary/constraint no-pole instead",
            "current_status": "not_sourced",
            "claim_effect": "finite branch stability blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VCG895_4_double_zero",
            "gate": "local-GR leakage silence",
            "required_test": "C_tr(Phi0)=0 and partial_A C_tr(Phi0)=0 for every non-EH metric coupling touching trace",
            "current_status": "not_signed_for_trace",
            "claim_effect": "PPN/source-normalization blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VCG895_5_source_cokernel",
            "gate": "matter-source projection",
            "required_test": "J_tr=0 by descent/cokernel, or numeric J_tr charges are sourced for R10/PPN/clocks/orbits",
            "current_status": "not_signed",
            "claim_effect": "alpha_tr cannot be set to zero or scored",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "VCG895_6_boundary_no_tail",
            "gate": "boundary/local tail silence",
            "required_test": "integrations by parts leave no unsourced local boundary hair or endpoint tail",
            "current_status": "not_signed",
            "claim_effect": "endpoint readout can only be closure/watch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def symbol_readout_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "readout_id": "SRR895_0_Htr",
            "quantity": "H_tr",
            "readout_law": "H_tr=P_tr^dagger Hess(S_parent) P_tr",
            "current_value": "MISSING_PARENT_HESSIAN_AND_PROJECTOR",
            "parent_adoption_required": True,
            "claim_status": "blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "readout_id": "SRR895_1_Ztr",
            "quantity": "Z_tr",
            "readout_law": "coefficient of g_obs^{mu nu}k_mu k_nu in sigma_2(H_tr)",
            "current_value": "MISSING_PRINCIPAL_SYMBOL",
            "parent_adoption_required": True,
            "claim_status": "blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "readout_id": "SRR895_2_mutr2",
            "quantity": "mu_tr^2",
            "readout_law": "zeroth-order trace symbol from the same H_tr",
            "current_value": "MISSING_ZEROTH_ORDER_SYMBOL",
            "parent_adoption_required": True,
            "claim_status": "blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "readout_id": "SRR895_3_lambdatr",
            "quantity": "lambda_tr",
            "readout_law": "lambda_tr=1/sqrt(mu_tr^2/Z_tr), or absent by no-pole theorem",
            "current_value": "MISSING_MASS_GAP_OR_NOPOLE",
            "parent_adoption_required": True,
            "claim_status": "blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "readout_id": "SRR895_4_Jtr",
            "quantity": "J_tr",
            "readout_law": "J_tr=P_tr^dagger J_parent, or zero by quotient-invariant matter descent/source-cokernel",
            "current_value": "MISSING_SOURCE_COKERNEL_OR_CHARGE",
            "parent_adoption_required": True,
            "claim_status": "blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "readout_id": "SRR895_5_alpha_tr",
            "quantity": "alpha_tr(lambda_tr)",
            "readout_law": "arena coupling from Z_tr, lambda_tr, J_tr, and matter normalization",
            "current_value": "NOT_COMPUTABLE_FROM_CONTRACT_ONLY",
            "parent_adoption_required": True,
            "claim_status": "blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def closure_demotion_rule_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rule_id": "CDR895_0_contract_only",
            "condition": "quadratic trace action is written but not derived as parent Hessian",
            "classification": "closure_only_nonclaim",
            "required_next_action": "do not use finite branch for R10/PPN/local-GR pass; run 896 parent-adoption gate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "CDR895_1_parent_adopted_finite",
            "condition": "P_tr,H_tr,Z_tr,mu_tr^2,J_tr,boundary,units are all parent-signed",
            "classification": "finite_branch_executable_later",
            "required_next_action": "populate sourced coefficient rows, then compare against R10/PPN/clocks/orbits without edge/closure shortcuts",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "CDR895_2_no_pole_signed",
            "condition": "trace is EH/gauge/constraint/readout-only and has no source-coupled local inverse",
            "classification": "zero_route_replaces_finite_branch",
            "required_next_action": "write no-pole theorem and delete lambda_tr as a physical local range for this branch",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "CDR895_3_neither_signed",
            "condition": "neither parent finite branch nor no-pole branch is signed",
            "classification": "local_trace_branch_blocked",
            "required_next_action": "keep local-GR/R10 gates blocked and hunt the parent coupling/action origin",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD895_0_zero_route",
            "branch": "EH/gauge/constraint no-pole route",
            "current_status": "not_parent_signed",
            "evidence": "rank-zero/readout-only/boundary no-tail/source-cokernel clauses remain unsigned",
            "decision": "watch_not_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD895_1_finite_trace_action",
            "branch": "finite local trace carrier",
            "current_status": "contract_written_ansatz_not_parent_adopted",
            "evidence": ACTION_ANSATZ,
            "decision": "closure_only_until_adopted",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD895_2_boundary_endpoint",
            "branch": "endpoint/boundary readout",
            "current_status": "endpoint_transfer_rejected_by_894",
            "evidence": "K_endpoint may guide a future parent pairing but is not a local kinetic/mass operator",
            "decision": "do_not_transfer_to_Ztr_or_lambda",
            "next_action": "only revive after boundary no-tail or local field map is parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG895_0_parent_adoption",
            "promotion_target": "contract becomes S_parent second variation",
            "required_to_pass": "P_tr and every coefficient read from a written parent action with cited source paths",
            "current_evidence": "contract only",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG895_1_Ztr_source",
            "promotion_target": "Z_tr sourced",
            "required_to_pass": "local two-derivative trace principal symbol with sign/units",
            "current_evidence": "missing; 894 rejected endpoint transfer",
            "gate_result": "fail_for_claim",
            "next_action": "keep Z_tr row nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG895_2_lambda_source_or_absence",
            "promotion_target": "lambda_tr sourced or absent by theorem",
            "required_to_pass": "mu_tr^2/Z_tr mass gap or signed no-pole theorem",
            "current_evidence": "missing",
            "gate_result": "fail_for_claim",
            "next_action": "do not run finite-range local claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG895_3_source_coupling",
            "promotion_target": "J_tr/alpha_tr sourced or zero",
            "required_to_pass": "source-cokernel theorem or numeric charges and normalization",
            "current_evidence": "missing",
            "gate_result": "fail_for_claim",
            "next_action": "coupling hunt remains live",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG895_4_local_GR",
            "promotion_target": "local GR/Newton reduction",
            "required_to_pass": "EH limit plus trace/boundary/source silence plus PPN residual vector below bounds",
            "current_evidence": "trace branch closure-only",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG895_0_no_ansatz_as_derivation",
            "forbidden_claim": "the finite trace action is derived",
            "status": "forbidden",
            "reason": "895 writes a contract/adoption target only; no parent Hessian has adopted it",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG895_1_no_Ztr_lambda_claim",
            "forbidden_claim": "Z_tr, mu_tr^2, or lambda_tr is known",
            "status": "forbidden",
            "reason": "readout rows remain missing and endpoint transfer remains rejected",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG895_2_no_zero_route_claim",
            "forbidden_claim": "trace branch has no local pole",
            "status": "forbidden",
            "reason": "rank-zero/readout-only/source-cokernel/boundary no-tail clauses are not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG895_3_no_empirical_pass",
            "forbidden_claim": "R10, PPN, clocks, WEP, orbital, or local-GR gates pass",
            "status": "forbidden",
            "reason": "finite and zero routes are both nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG895_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "895 gives the exact future contract and demotion rule, which is useful internal theory discipline",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D895_0",
            "finding": "quadratic_trace_action_contract_written",
            "reason": "the finite branch now has an explicit parent-adoption target instead of an implicit free scalar",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D895_1",
            "finding": "contract_is_not_a_derivation",
            "reason": "no current source supplies P_tr, H_tr, Z_tr, mu_tr^2, or J_tr from the parent Hessian",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D895_2",
            "finding": "closure_demotion_gate_open",
            "reason": "unless 896 parent-adopts the action or signs no-pole, the local trace route stays closure-only",
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
            "objective": "decide whether the 895 trace-action contract is actually adopted by a parent action, or whether the zero/no-pole route wins and the finite branch is closure-only",
            "include": "parent Hessian adoption checklist, P_tr ownership, H_tr symbol readout, source-cokernel, double-zero leakage, boundary no-tail, finite-vs-zero branch register",
            "exclude": "R10/PPN/local-GR pass, numeric alpha claim, endpoint-to-local transfer, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_894_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_894_VALIDATION.csv"
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
    contract_rows_: list[dict[str, object]],
    variational_rows_: list[dict[str, object]],
    symbol_rows_: list[dict[str, object]],
    demotion_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    parent_verdict = next(row for row in contract_rows_ if row["contract_id"] == "QTC895_8_parent_adoption_verdict")
    demotion_rule = next(row for row in demotion_rows_ if row["rule_id"] == "CDR895_0_contract_only")
    row_groups = [
        source_rows_,
        summary_rows_,
        contract_rows_,
        variational_rows_,
        symbol_rows_,
        demotion_rows_,
        branch_rows_,
        promotion_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V895_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V895_1_prior_894_clean",
            "result": "pass" if prior_894_clean() else "fail",
            "detail": "P8_Y5_BRR545_894_VALIDATION.csv clean",
        },
        {
            "check_id": "V895_2_contract_rows_complete",
            "result": "pass" if len(contract_rows_) >= 9 else "fail",
            "detail": "domain/action/kinetic/mass/mixing/source/boundary/units/verdict rows written",
        },
        {
            "check_id": "V895_3_ansatz_not_parent_adopted",
            "result": "pass" if parent_verdict["current_895_status"] == "ansatz_not_parent_adopted" else "fail",
            "detail": "finite action is explicitly a nonclaim ansatz/contract",
        },
        {
            "check_id": "V895_4_variational_gates_present",
            "result": "pass" if len(variational_rows_) == 7 else "fail",
            "detail": "parent variation/covariance/operator/stability/double-zero/source/boundary gates present",
        },
        {
            "check_id": "V895_5_symbol_rows_blocked",
            "result": "pass"
            if all(row["claim_status"] == "blocked" and not bool(row["valid_for_claim"]) for row in symbol_rows_)
            else "fail",
            "detail": "H_tr, Z_tr, mu_tr^2, lambda_tr, J_tr, alpha_tr remain blocked",
        },
        {
            "check_id": "V895_6_closure_demotion_rule_blocks_claims",
            "result": "pass"
            if demotion_rule["classification"] == "closure_only_nonclaim" and not bool(demotion_rule["claim_allowed"])
            else "fail",
            "detail": "contract-only branch is demoted to closure-only",
        },
        {
            "check_id": "V895_7_branch_decisions_nonclaim",
            "result": "pass" if all(not bool(row["valid_for_claim"]) for row in branch_rows_) else "fail",
            "detail": "zero, finite, and endpoint branches remain nonclaim",
        },
        {
            "check_id": "V895_8_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V895_9_claim_allowed_false",
            "result": "pass" if all(not bool(row["claim_allowed"]) for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V895_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V895_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V895_12_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V895_13_validation_rows_ready",
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
    contract_rows_: list[dict[str, object]],
    variational_rows_: list[dict[str, object]],
    symbol_rows_: list[dict[str, object]],
    demotion_rows_: list[dict[str, object]],
    branch_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 895 - Y5/R10 Parent Quadratic Trace-Action Ansatz Or Closure Demotion

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **895 writes the finite trace branch as an exact adoption contract, not as a claim**. The candidate action is now explicit:

`{ACTION_ANSATZ}`

That is useful because it stops the trace sector being a foggy free scalar. But it is not yet derived from `S_parent`. Until a future checkpoint signs `P_tr`, `H_tr`, `Z_tr`, `mu_tr^2`, `J_tr`, double-zero leakage, and boundary/no-tail from the parent action, the finite branch is demoted to closure-only and cannot be used for R10, PPN, clock, WEP, orbital, or local-GR claims.

## Exact 895 Finding
The route is now a clean fork. Either the parent action adopts the quadratic trace contract as `H_tr=P_tr^dagger Hess(S_parent)P_tr`, giving source-backed `Z_tr`, `mu_tr^2`, `lambda_tr`, and `J_tr`; or the trace mode is proved to be EH/gauge/constraint/readout-only with no source-coupled local pole. If neither is signed, the local trace route is closure-only. This is not bad news: it is the coupling/action bottleneck finally written in a form we can attack.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Parent Quadratic Trace-Action Contract
{md_table(contract_rows_)}

## Variational Consistency Gates
{md_table(variational_rows_)}

## Symbol Readout Rows
{md_table(symbol_rows_)}

## Closure Demotion Rule
{md_table(demotion_rows_)}

## Branch Decision
{md_table(branch_rows_)}

## Promotion Gate
{md_table(promotion_rows_)}

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
    contract_rows_ = quadratic_trace_action_contract_rows(generated_utc)
    variational_rows_ = variational_consistency_gate_rows(generated_utc)
    symbol_rows_ = symbol_readout_rows(generated_utc)
    demotion_rows_ = closure_demotion_rule_rows(generated_utc)
    branch_rows_ = branch_decision_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        contract_rows_,
        variational_rows_,
        symbol_rows_,
        demotion_rows_,
        branch_rows_,
        promotion_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_895_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_895_QUADRATIC_TRACE_ACTION_CONTRACT.csv": contract_rows_,
        "P8_Y5_R10_895_VARIATIONAL_CONSISTENCY_GATES.csv": variational_rows_,
        "P8_Y5_R10_895_SYMBOL_READOUT_ROWS.csv": symbol_rows_,
        "P8_Y5_R10_895_CLOSURE_DEMOTION_RULE.csv": demotion_rows_,
        "P8_Y5_R10_895_BRANCH_DECISION.csv": branch_rows_,
        "P8_Y5_R10_895_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_895_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_895_DECISION.csv": decision_rows_,
        "P8_Y5_R10_895_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_895_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_895_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "895-Y5-R10-parent-quadratic-trace-action-ansatz-or-closure-demotion.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        contract_rows_,
        variational_rows_,
        symbol_rows_,
        demotion_rows_,
        branch_rows_,
        promotion_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_895_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
