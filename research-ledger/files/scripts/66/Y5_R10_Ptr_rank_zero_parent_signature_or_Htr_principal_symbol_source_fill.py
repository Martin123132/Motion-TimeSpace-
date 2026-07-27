from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_893_Ptr_rank_zero_parent_signature_audited_not_signed_Htr_principal_symbol_fill_staged_nonclaim"
CLAIM_CEILING = "Ptr_rank_zero_signature_audit_and_Htr_symbol_fill_staging_only_no_rank_zero_no_Ztr_lambdatr_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "894-Y5-R10-Htr-principal-symbol-and-mass-gap-source-fill.md"

SOURCE_SPECS = [
    {
        "source_id": "892_doc",
        "path": ROOT / "892-Y5-R10-trace-Hessian-Ztr-lambdatr-source-row-or-no-pole-theorem.md",
        "needle": "trace-Hessian branch has been sharpened into an exact fork",
        "role": "immediate 893 fork handoff",
    },
    {
        "source_id": "892_validation",
        "path": OUT / "P8_Y5_BRR545_892_VALIDATION.csv",
        "needle": "V892_13_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "892_trace_rows",
        "path": OUT / "P8_Y5_R10_892_TRACE_HESSIAN_SOURCE_ROWS.csv",
        "needle": "THS892_1_Ztr_principal_symbol",
        "role": "H_tr/Z_tr/lambda_tr source rows",
    },
    {
        "source_id": "892_no_pole",
        "path": OUT / "P8_Y5_R10_892_NO_POLE_THEOREM_ATTEMPT.csv",
        "needle": "NPT892_4_verdict",
        "role": "conditional no-pole theorem verdict",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "`P_tr` is now a precise parent-geometry object",
        "role": "P_tr construction and rank test",
    },
    {
        "source_id": "877_htr_skeleton",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "H_tr=P_tr^dagger Hess(S_parent) P_tr",
        "role": "minimal H_tr definition",
    },
    {
        "source_id": "887_doc",
        "path": ROOT / "887-Y5-R10-readout-only-boundary-support-action-clause-or-finite-trace-carrier-source-pack.md",
        "needle": "post-variation, source-at-zero boundary readout",
        "role": "readout-only boundary support clause",
    },
    {
        "source_id": "887_readout_clause",
        "path": OUT / "P8_Y5_R10_887_READOUT_BOUNDARY_CLAUSE.csv",
        "needle": "RO887_6_clause_verdict",
        "role": "readout clause rows",
    },
    {
        "source_id": "888_doc",
        "path": ROOT / "888-Y5-R10-parent-spine-readout-clause-integration-or-finite-trace-carrier-runner.md",
        "needle": "compatible with the parent-spine discipline but not integrated",
        "role": "parent-spine integration attempt",
    },
    {
        "source_id": "888_parent_integration",
        "path": OUT / "P8_Y5_R10_888_PARENT_SPINE_INTEGRATION.csv",
        "needle": "PSI888_5_integration_verdict",
        "role": "parent integration verdict",
    },
    {
        "source_id": "888_gates",
        "path": OUT / "P8_Y5_R10_888_COMPATIBILITY_GATES.csv",
        "needle": "G888_5_total_gate",
        "role": "readout compatibility gates",
    },
    {
        "source_id": "889_doc",
        "path": ROOT / "889-Y5-R10-finite-trace-carrier-runner-dryrun-or-parent-spine-clause-repair.md",
        "needle": "exact conditional repair theorem",
        "role": "parent-spine repair theorem",
    },
    {
        "source_id": "889_repair_contract",
        "path": OUT / "P8_Y5_R10_889_PARENT_SPINE_REPAIR_CONTRACT.csv",
        "needle": "RC889_6_repair_verdict",
        "role": "repair contract clauses",
    },
    {
        "source_id": "889_premise_audit",
        "path": OUT / "P8_Y5_R10_889_PREMISE_AUDIT.csv",
        "needle": "PA889_1_boundary_no_tail",
        "role": "premise audit and hard fail",
    },
    {
        "source_id": "890_no_tail",
        "path": OUT / "P8_Y5_R10_890_BOUNDARY_NO_TAIL_THEOREM_ATTEMPT.csv",
        "needle": "NT890_5_no_tail_corollary",
        "role": "boundary/no-tail corollary",
    },
    {
        "source_id": "891_coeff_rows",
        "path": OUT / "P8_Y5_R10_891_TRACE_COEFFICIENT_SOURCE_ROWS.csv",
        "needle": "TCSR891_1_lambda_tr",
        "role": "finite trace coefficient fallback rows",
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
            "what_changed": "audited the exact parent signatures required to promote P_tr rank-zero/readout-only status, and staged the finite H_tr principal-symbol/mass-gap source-fill fallback",
            "best_partial_result": "the shortest clean derivation path is now explicit: P_tr rank zero needs one parent-owned local/boundary quotient bundle plus no-tail, source-at-zero, and matter no-marker signatures; otherwise the finite branch must source H_tr symbols",
            "hard_blockers": "boundary/no-tail is still the hard fail, q_loc/boundary bundle is not parent-owned, readout source-at-zero is policy-compatible but not trace-parent-signed, matter no-marker is unsigned, and finite H_tr symbols are absent",
            "what_is_not_claimed": "P_tr parent ownership, rank(P_loc P_tr P_loc^dagger)=0, no H_tr pole, Z_tr, lambda_tr, R10 pass, PPN pass, clock/WEP/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def rank_zero_signature_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "RZS893_0_Ptr_owner",
            "signature": "P_tr parent ownership",
            "required_form": "P_tr=v_tr tensor ell_tr with ell_tr=DQ_trace and v_tr raised by a parent pairing/pseudo-inverse after gauge constraints",
            "current_evidence": "878 gives formal construction; 887/889 give a readout clause shape",
            "audit_result": "not_parent_signed",
            "if_signed": "rank tests refer to a real parent object rather than a symbolic closure",
            "if_failed": "H_tr=P_tr^dagger Hess(S_parent)P_tr remains undefined and finite source fill is mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "RZS893_1_qloc_boundary_bundle",
            "signature": "one parent bundle Phi -> (q_loc[U], boundary/FLRW class)",
            "required_form": "q_loc[U]=[j^k Phi|_U]_gauge while b_partial(Phi) carries Q_trace for U away from cosmological boundary",
            "current_evidence": "889 writes the sufficient contract; 888 says the slot exists but is not integrated",
            "audit_result": "contract_present_not_action_derived",
            "if_signed": "global trace visibility can coexist with local verticality without patching",
            "if_failed": "Q_trace may be part of local observed geometry and must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "RZS893_2_vtr_local_verticality",
            "signature": "Dq_loc[U][v_tr]=0",
            "required_form": "j^k v_tr|_U=0 or gauge/exact-zero on compact local domains, while Dq_FLRW[v_tr] may be nonzero",
            "current_evidence": "889 conditional theorem; 890 no-tail corollary not parent-signed",
            "audit_result": "conditional_not_parent_signed",
            "if_signed": "P_tr has no compact-local matrix elements from the trace endpoint",
            "if_failed": "a local conformal/trace scalar branch remains legal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "RZS893_3_boundary_no_tail",
            "signature": "no compact trace tail, flux, scalar gradient, vector hair, tensor hair, clock/WEP/species marker",
            "required_form": "P_loc J_trace=0 and P_loc dB_trace=0 through local arenas using the same domain/projector convention",
            "current_evidence": "889 premise audit marks boundary/no-tail as hard_fail_open; 890 corollary remains conditional",
            "audit_result": "hard_fail_open",
            "if_signed": "rank(P_loc P_tr P_loc^dagger)=0 can feed the 886/892 no-pole route",
            "if_failed": "finite H_tr and response coefficients must be filled and tested",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "RZS893_4_source_at_zero",
            "signature": "R_tr is post-variation/source-at-zero and absent as a physical spurion",
            "required_form": "delta(S_parent+s_tr R_tr)/delta Phi at s_tr=0 equals delta S_parent/delta Phi, with R_tr an observable on Sol(S_parent)",
            "current_evidence": "337/338/446 policy support via 887/888/889; trace-specific parent embedding still absent",
            "audit_result": "policy_pass_not_trace_parent_signed",
            "if_signed": "readout cannot create a local H_tr pole or local force term",
            "if_failed": "the readout source is a physical coupling and must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "RZS893_5_matter_no_marker",
            "signature": "ordinary matter descends through q_loc with no trace marker constants",
            "required_form": "S_matter=Sbar[q_loc(Phi),Psi,theta] with partial_{v_tr}theta=0 and no local EFT operator O_loc(Q_trace)",
            "current_evidence": "873/889 chain-rule theorem shape; no parent-signed measure/coframe/connection/constants descent",
            "audit_result": "conditional_not_parent_signed",
            "if_signed": "J_tr source-cokernel and Q_tr^A vanish for local matter",
            "if_failed": "R10/WEP/clock/EM/species coefficients must be acquired",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "RZS893_6_rank_zero_verdict",
            "signature": "rank(P_loc P_tr P_loc^dagger)=0",
            "required_form": "RZS893_0 through RZS893_5 signed by one parent action/spine with same U, quotient, gauge, and source-normalization conventions",
            "current_evidence": "sufficient theorem exists; parent signatures missing and boundary/no-tail is hard fail",
            "audit_result": "not_signed_do_not_promote",
            "if_signed": "trace branch can zero-return locally, still not full local GR by itself",
            "if_failed": "H_tr principal-symbol and mass-gap source fill becomes the next concrete route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def readout_domain_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "RDT893_0_variation_order",
            "domain_test": "variation before readout",
            "pass_condition": "physical field equations are computed with s_tr=0 before any trace readout is evaluated",
            "current_status": "policy_supported_not_trace_parent_signed",
            "failure_mode": "readout source backreacts as a spurion",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RDT893_1_compact_local_domain",
            "domain_test": "U is compact and away from cosmological boundary",
            "pass_condition": "same U is used for q_loc, P_loc, boundary class restriction, and matter readout",
            "current_status": "not_parent_locked",
            "failure_mode": "rank-zero follows from moving the domain convention",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RDT893_2_local_matrix_elements",
            "domain_test": "compact-local matrix elements of P_tr vanish",
            "pass_condition": "<eta_U,P_tr zeta_U>=0 for all compact local modes after gauge/exact quotienting",
            "current_status": "not_tested_parent_Ptr_missing",
            "failure_mode": "rank-one local trace carrier survives",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RDT893_3_boundary_flux",
            "domain_test": "no compact local boundary/exact flux",
            "pass_condition": "int_partialU B_trace=0 and P_loc dB_trace=0 through local arenas",
            "current_status": "hard_fail_open",
            "failure_mode": "boundary tail activates finite residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RDT893_4_source_cokernel",
            "domain_test": "J_tr pairs with no physical local cokernel mode",
            "pass_condition": "<u_tr,J_parent>=0 for all physical local trace modes or no such modes exist",
            "current_status": "matter_descent_unsigned",
            "failure_mode": "ordinary matter carries finite Q_tr/m",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "RDT893_5_domain_verdict",
            "domain_test": "rank-zero/readout route promotion",
            "pass_condition": "RDT893_0 through RDT893_4 pass together in one parent convention",
            "current_status": "fail_for_claim",
            "failure_mode": "finite H_tr symbol/source fill must proceed",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def htr_symbol_fill_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fill_id": "HSF893_0_define_Ptr_or_closure",
            "quantity": "P_tr",
            "source_target": "parent trace covector ell_tr, parent pairing K_parent, gauge/constraint pseudo-inverse",
            "formula_or_check": "P_tr=v_tr tensor ell_tr; v_tr=K_parent^-1 ell_tr/<ell_tr,K_parent^-1 ell_tr>",
            "current_status": "MISSING_PARENT_PROJECTOR",
            "required_before_claim": "real P_tr or explicit closure-only demotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF893_1_Htr_operator",
            "quantity": "H_tr",
            "source_target": "second variation of S_parent after P_tr is owned",
            "formula_or_check": "H_tr=P_tr^dagger Hess(S_parent) P_tr on the reduced quotient tangent space",
            "current_status": "MISSING_PARENT_HESSIAN",
            "required_before_claim": "operator domain, gauge reduction, and boundary conditions",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF893_2_principal_symbol",
            "quantity": "Z_tr",
            "source_target": "principal symbol of H_tr",
            "formula_or_check": "sigma_2(H_tr)=Z_tr g^{mu nu} k_mu k_nu on the physical scalar trace subspace",
            "current_status": "MISSING_PRINCIPAL_SYMBOL",
            "required_before_claim": "sign, units, canonical normalization, and provenance",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF893_3_mass_gap",
            "quantity": "mu_tr^2,m_tr,lambda_tr",
            "source_target": "zeroth-order H_tr symbol or no-pole theorem",
            "formula_or_check": "m_tr^2=mu_tr^2/Z_tr; lambda_tr=1/m_tr or hbar/(m_tr c) after units",
            "current_status": "MISSING_MASS_GAP_OR_NOPOLE",
            "required_before_claim": "positive/zero/tachyonic/constraint classification",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF893_4_reduced_inverse",
            "quantity": "source-coupled pole test",
            "source_target": "reduced inverse and physical local trace subspace",
            "formula_or_check": "pole exists only if H_tr^{-1} has a physical local scalar mode paired with J_tr",
            "current_status": "MISSING_REDUCED_INVERSE_TEST",
            "required_before_claim": "no-pole theorem or finite propagator certificate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF893_5_source_projection",
            "quantity": "J_tr,Q_tr/m",
            "source_target": "matter/source variation under trace direction",
            "formula_or_check": "J_tr=P_tr^dagger J_parent; Q_tr^A/m_A from local body response or zero by descent",
            "current_status": "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "required_before_claim": "universal/species/clock source rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "HSF893_6_arena_projection",
            "quantity": "R10,PPN,clock_WEP,orbital response",
            "source_target": "arena-specific response map after H_tr branch decision",
            "formula_or_check": "alpha_tr_AB, gamma/beta response, clock response, orbital Yukawa/GM absorption",
            "current_status": "MISSING_ARENA_PROJECTION",
            "required_before_claim": "source paths, units, bounds, and no MISSING markers",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def fork_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fork_id": "FD893_0_zero_route",
            "branch": "P_tr rank-zero/readout-only",
            "condition_to_take": "RZS893_0 through RZS893_6 parent-signed",
            "current_result": "blocked_not_parent_signed",
            "claim_policy": "do not claim no-pole or c_T zero",
            "next_action": "only reopen if boundary/no-tail and q_loc/matter signatures are newly supplied",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FD893_1_finite_Htr",
            "branch": "finite H_tr principal-symbol source fill",
            "condition_to_take": "any rank-zero signature remains unsigned",
            "current_result": "selected_next",
            "claim_policy": "source-fill only, no empirical pass",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "FD893_2_local_GR_scope",
            "branch": "local GR/Newton",
            "condition_to_take": "trace branch plus EH/source-normalization/PPN/q_loc residual branches all close",
            "current_result": "outside_trace_branch_still_blocked",
            "claim_policy": "trace progress is not a local-GR claim",
            "next_action": "keep GR gate blocked and derivation-first",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def blocker_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BL893_0_boundary_no_tail",
            "blocker": "boundary/relative-cohomology trace current no-tail remains hard_fail_open",
            "why_it_matters": "this is the direct route to rank(P_loc P_tr P_loc^dagger)=0",
            "next_action": "unless new parent evidence appears, proceed to H_tr symbol fill",
            "priority": "highest_zero_route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL893_1_Ptr_owner",
            "blocker": "P_tr is still not parent-owned",
            "why_it_matters": "H_tr and rank tests need a real projector",
            "next_action": "source ell_tr/K_parent or explicitly closure-only",
            "priority": "highest_finite_route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL893_2_Htr_symbols",
            "blocker": "Z_tr and mu_tr^2/lambda_tr are missing",
            "why_it_matters": "finite trace branch cannot be dimensioned or tested",
            "next_action": NEXT_TARGET,
            "priority": "next",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL893_3_matter_no_marker",
            "blocker": "matter descent/no-marker source-cokernel is unsigned",
            "why_it_matters": "local charges can reintroduce R10/WEP/clock/EM signals",
            "next_action": "after H_tr symbols, fill or zero J_tr/Q_tr rows",
            "priority": "high",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL893_4_arena_response",
            "blocker": "PPN, clock/WEP, orbital, and R10 response maps are not sourced",
            "why_it_matters": "no local empirical pass can be scored without observable projections",
            "next_action": "only after branch coefficients exist",
            "priority": "after_coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG893_0_Ptr_rank_zero",
            "promotion_target": "rank(P_loc P_tr P_loc^dagger)=0",
            "required_to_pass": "parent-owned P_tr, q_loc/boundary bundle, no-tail, source-at-zero, matter no-marker in one convention",
            "current_evidence": "conditional theorem only; boundary/no-tail hard fail",
            "gate_result": "fail_for_claim",
            "next_action": "do not promote zero route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG893_1_no_pole",
            "promotion_target": "no source-coupled local H_tr pole",
            "required_to_pass": "rank-zero/readout-only or reduced H_tr inverse no-pole certificate",
            "current_evidence": "not signed",
            "gate_result": "fail_for_claim",
            "next_action": "derive H_tr symbols if zero route remains unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG893_2_Htr_finite_branch",
            "promotion_target": "finite H_tr branch can be scored",
            "required_to_pass": "P_tr,H_tr,Z_tr,mu_tr^2,lambda_tr,J_tr,Q_tr/m,response maps,bounds all sourced",
            "current_evidence": "source-fill rows only with MISSING markers",
            "gate_result": "fail_for_claim",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG893_3_R10_PPN_local",
            "promotion_target": "R10/PPN/local-GR pass",
            "required_to_pass": "zero theorem or fully sourced finite branch plus local-GR residual stack",
            "current_evidence": "neither branch claim-ready",
            "gate_result": "fail_for_claim",
            "next_action": "no empirical/local-GR claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC893_0_selected",
            "route": "Htr_principal_symbol_and_mass_gap_source_fill",
            "status": "selected",
            "reason": "P_tr rank-zero/readout-only remains unsigned after a direct parent-signature audit, with boundary/no-tail still the hard fail; finite H_tr symbols are now the next concrete derivation/source target",
            "include": "P_tr owner or closure-only, H_tr second variation, Z_tr principal symbol, mu_tr^2/lambda_tr mass gap, reduced inverse sign/stability",
            "exclude": "R10/PPN/local-GR claim, fitted tiny coupling, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG893_0_no_rank_zero_claim",
            "forbidden_claim": "P_tr local rank is zero",
            "status": "forbidden",
            "reason": "rank-zero signatures are not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG893_1_no_no_pole_claim",
            "forbidden_claim": "H_tr has no local source-coupled pole",
            "status": "forbidden",
            "reason": "rank-zero and reduced-inverse no-pole routes are both unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG893_2_no_Zlambda_claim",
            "forbidden_claim": "Z_tr/lambda_tr are known",
            "status": "forbidden",
            "reason": "H_tr principal symbol and mass gap are missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG893_3_no_empirical_pass",
            "forbidden_claim": "R10/PPN/clock/WEP/orbital tests pass",
            "status": "forbidden",
            "reason": "no zero theorem and no finite coefficient/arena rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG893_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "893 cleanly selects finite H_tr symbol fill after direct rank-zero signature audit fails for claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D893_0",
            "finding": "rank_zero_signature_audited",
            "reason": "the exact parent signatures for P_tr rank-zero/readout-only were checked against 887-890 evidence",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D893_1",
            "finding": "rank_zero_not_parent_signed",
            "reason": "boundary/no-tail remains hard_fail_open and q_loc/matter/readout signatures are not jointly signed",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D893_2",
            "finding": "finite_Htr_symbol_fill_selected",
            "reason": "if zero route cannot be signed now, the next derivation-first route is to source H_tr principal symbol and mass gap without claiming a pass",
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
            "objective": "derive or source the finite trace Hessian principal symbol and mass gap, while keeping rank-zero as a conditional watch and making no local/R10/PPN claim",
            "include": "P_tr owner/closure decision, H_tr operator domain, sigma_2(H_tr), Z_tr sign, mu_tr^2/m_tr/lambda_tr, reduced inverse/no-pole fallback",
            "exclude": "R10/PPN/local-GR pass, fitted coupling, public prose, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_892_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_892_VALIDATION.csv"
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
    rank_rows_: list[dict[str, object]],
    domain_rows_: list[dict[str, object]],
    htr_rows_: list[dict[str, object]],
    fork_rows_: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    rank_verdict = next(row for row in rank_rows_ if row["audit_id"] == "RZS893_6_rank_zero_verdict")
    boundary_audit = next(row for row in rank_rows_ if row["audit_id"] == "RZS893_3_boundary_no_tail")
    htr_statuses = [str(row["current_status"]) for row in htr_rows_]
    row_groups = [
        source_rows_,
        summary_rows_,
        rank_rows_,
        domain_rows_,
        htr_rows_,
        fork_rows_,
        blocker_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V893_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows_) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V893_1_prior_892_clean",
            "result": "pass" if prior_892_clean() else "fail",
            "detail": "P8_Y5_BRR545_892_VALIDATION.csv clean",
        },
        {
            "check_id": "V893_2_rank_signature_audit_complete",
            "result": "pass" if len(rank_rows_) == 7 else "fail",
            "detail": "P_tr owner/q_loc/no-tail/source-at-zero/matter/verdict rows present",
        },
        {
            "check_id": "V893_3_rank_zero_not_promoted",
            "result": "pass" if rank_verdict["audit_result"] == "not_signed_do_not_promote" else "fail",
            "detail": "rank-zero verdict remains nonclaim",
        },
        {
            "check_id": "V893_4_boundary_no_tail_hard_fail_recorded",
            "result": "pass" if boundary_audit["audit_result"] == "hard_fail_open" else "fail",
            "detail": "boundary/no-tail remains the hard zero-route blocker",
        },
        {
            "check_id": "V893_5_domain_tests_block_claim",
            "result": "pass" if all(row["claim_allowed"] is False for row in domain_rows_) else "fail",
            "detail": "readout/domain tests all block claims",
        },
        {
            "check_id": "V893_6_Htr_symbol_fill_staged_missing",
            "result": "pass" if all("MISSING" in status for status in htr_statuses) else "fail",
            "detail": "finite H_tr fill rows remain missing/nonclaim",
        },
        {
            "check_id": "V893_7_finite_branch_selected_next",
            "result": "pass" if any(row["branch"] == "finite H_tr principal-symbol source fill" and row["current_result"] == "selected_next" for row in fork_rows_) else "fail",
            "detail": "finite H_tr source-fill branch selected as next target",
        },
        {
            "check_id": "V893_8_promotion_gates_blocked",
            "result": "pass" if all(row["gate_result"] == "fail_for_claim" for row in promotion_rows_) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V893_9_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V893_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V893_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V893_12_route_selected",
            "result": "pass" if route_rows_ and next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V893_13_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return [{**row, "generated_utc": generated_utc} for row in checks]


def write_markdown(
    path: Path,
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    rank_rows_: list[dict[str, object]],
    domain_rows_: list[dict[str, object]],
    htr_rows_: list[dict[str, object]],
    fork_rows_: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 893 - Y5/R10 P_tr Rank-Zero Parent Signature or Htr Principal-Symbol Source Fill",
        "",
        f"Status: `{STATUS}`",
        f"Claim ceiling: `{CLAIM_CEILING}`",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the direct `P_tr` rank-zero/readout-only audit still does not parent-sign the zero route, so the finite `H_tr` symbol-fill branch is now selected as the next concrete target**. The zero route remains mathematically live, but only as a watch: it needs one parent-owned local/boundary quotient bundle, no compact tail/flux, source-at-zero readout, and matter no-marker descent. Since those signatures are not jointly present, `Z_tr` and `lambda_tr` still cannot be claimed or tested.",
        "",
        "## Exact 893 Fork",
        "The clean theorem route is: parent-owned `P_tr` plus `rank(P_loc P_tr P_loc^dagger)=0` plus source-cokernel silence implies no local source-coupled `H_tr` pole. The audit finds the theorem shape is valid, but the parent signatures are unsigned. Therefore the next derivation-first move is not empirical scoring; it is the finite-symbol source fill: define or demote `P_tr`, construct the reduced `H_tr`, extract `sigma_2(H_tr)=Z_tr g^{mu nu}k_mu k_nu`, and derive the mass gap/range or a reduced-inverse no-pole certificate.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows_),
        "",
        "## Source Register",
        md_table(source_rows_),
        "",
        "## P_tr Rank-Zero Signature Audit",
        md_table(rank_rows_),
        "",
        "## Readout Domain Tests",
        md_table(domain_rows_),
        "",
        "## H_tr Principal-Symbol Fill Queue",
        md_table(htr_rows_),
        "",
        "## Fork Decision",
        md_table(fork_rows_),
        "",
        "## Blocker Ledger",
        md_table(blocker_rows_),
        "",
        "## Promotion Gates",
        md_table(promotion_rows_),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guards",
        md_table(claim_rows_),
        "",
        "## Decision",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    rank_rows_ = rank_zero_signature_audit_rows(generated_utc)
    domain_rows_ = readout_domain_test_rows(generated_utc)
    htr_rows_ = htr_symbol_fill_rows(generated_utc)
    fork_rows_ = fork_decision_rows(generated_utc)
    blocker_rows_ = blocker_ledger_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    claim_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        rank_rows_,
        domain_rows_,
        htr_rows_,
        fork_rows_,
        blocker_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_893_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_893_PTR_RANK_ZERO_SIGNATURE_AUDIT.csv": rank_rows_,
        "P8_Y5_R10_893_READOUT_DOMAIN_TESTS.csv": domain_rows_,
        "P8_Y5_R10_893_HTR_PRINCIPAL_SYMBOL_FILL.csv": htr_rows_,
        "P8_Y5_R10_893_FORK_DECISION.csv": fork_rows_,
        "P8_Y5_R10_893_BLOCKER_LEDGER.csv": blocker_rows_,
        "P8_Y5_R10_893_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_893_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_893_CLAIM_GUARD.csv": claim_rows_,
        "P8_Y5_R10_893_DECISION.csv": decision_rows_,
        "P8_Y5_R10_893_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_893_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_BRR545_893_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "893-Y5-R10-Ptr-rank-zero-parent-signature-or-Htr-principal-symbol-source-fill.md"
    write_markdown(
        doc_path,
        generated_utc,
        source_rows_,
        summary_rows_,
        rank_rows_,
        domain_rows_,
        htr_rows_,
        fork_rows_,
        blocker_rows_,
        promotion_rows_,
        route_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_893_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
