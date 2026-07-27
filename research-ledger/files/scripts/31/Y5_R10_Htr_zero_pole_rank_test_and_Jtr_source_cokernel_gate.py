from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_886_Htr_zero_pole_implication_theorem_written_parent_signatures_missing_finite_carrier_branch_retained_nonclaim"
CLAIM_CEILING = "conditional_Htr_rank_zero_no_pole_source_cokernel_theorem_only_no_parent_signed_zero_return_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "887-Y5-R10-readout-only-boundary-support-action-clause-or-finite-trace-carrier-source-pack.md"


SOURCE_SPECS = [
    {
        "source_id": "885_doc",
        "path": ROOT / "885-Y5-R10-parent-charge-lattice-or-Htr-P0-zero-pole-source-fill.md",
        "needle": "the charge-unit route was attempted in its cleanest form",
        "role": "immediate H_tr zero-pole/source-cokernel handoff",
    },
    {
        "source_id": "885_validation",
        "path": OUT / "P8_Y5_BRR545_885_VALIDATION.csv",
        "needle": "V885_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "885_htr_fill",
        "path": OUT / "P8_Y5_R10_885_HTR_ZERO_POLE_SOURCE_FILL.csv",
        "needle": "HZ885_2_zero_pole",
        "role": "zero-pole/source-cokernel rows to refine",
    },
    {
        "source_id": "878_projector",
        "path": ROOT / "878-Y5-R10-Ptr-parent-projector-definition-and-constraint-rank-test.md",
        "needle": "`P_tr` is now a precise parent-geometry object",
        "role": "formal P_tr/rank test predecessor",
    },
    {
        "source_id": "877_htr_skeleton",
        "path": ROOT / "877-Y5-R10-parent-trace-Hessian-source-hunt-and-minimal-action-skeleton.md",
        "needle": "minimal future action object",
        "role": "minimal H_tr skeleton",
    },
    {
        "source_id": "876_trace_hessian",
        "path": ROOT / "876-Y5-R10-trace-sector-ZT-lambdaT-parent-input-or-zero-return.md",
        "needle": "principal-symbol normalization of the projected trace Hessian",
        "role": "Z_tr/lambda_tr no-pole contract",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "verticality proof has a clean mathematical shape",
        "role": "q_loc compact restriction/support lemma",
    },
    {
        "source_id": "873_charge_zero",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "chain-rule zero theorem is valid as mathematics",
        "role": "matter trace-charge source zero lemma",
    },
    {
        "source_id": "870_nohair",
        "path": ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needle": "the first local `q_loc` channel is conditionally clean but not derived",
        "role": "P_loc J_trace no-hair/support debt",
    },
    {
        "source_id": "421_fibre_decoupling",
        "path": ROOT / "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "needle": "finite-fibre/local-GR checkpoint",
        "role": "nonpropagating/gapped finite-fibre analogy",
    },
    {
        "source_id": "446_zero_conditions",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "q-retained Zero Conditions",
        "role": "legal zero-route/no-cheat policy",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout-after-variation/no-spurion rule",
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
        lines.append("| " + " | ".join(stringify(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
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
            "what_changed": "wrote the conditional implication theorem from local rank-zero/readout-only P_tr to no H_tr pole and zero J_tr source-cokernel, then kept it nonclaim because parent signatures are missing",
            "best_partial_result": "if P_tr is a boundary/readout-only direction with zero compact local jet rank, then the local trace branch has no source-coupled pole and no local matter charge by rank/source-cokernel pairing; this would zero-return c_T without fitting it",
            "hard_blockers": "P_tr is still closure-only, q_loc compact restriction is not parent-owned, boundary support/no-tail is not proved, H_tr is not computed, J_tr source-cokernel is not signed, matter-stack/no-marker descent is incomplete",
            "what_is_not_claimed": "rank-zero, no physical trace pole, J_tr=0, c_T=0, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def zero_pole_implication_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "ZP886_0_local_rank_definition",
            "statement": "local trace rank is the rank of P_loc P_tr P_loc^dagger on compact lab/solar-system domains",
            "derivation": "if q_loc[U] is a compact k-jet quotient, this rank tests whether the trace direction has any local representative after gauge/exact quotienting",
            "proof_status": "definition_ready",
            "parent_status": "P_tr_and_q_loc_not_parent_signed",
            "what_it_buys": "turns vague local silence into a concrete finite-rank test",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "ZP886_1_rank_zero_implication",
            "statement": "if rank(P_loc P_tr P_loc^dagger)=0, then the trace projector has no physical compact-local image",
            "derivation": "for any local variation eta_U, P_tr P_loc^dagger eta_U is gauge/exact-zero or outside the local quotient; hence local matrix elements of P_tr vanish",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "needs boundary/readout support signature",
            "what_it_buys": "no local trace carrier is introduced by endpoint/readout algebra",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "ZP886_2_rank_zero_no_pole",
            "statement": "rank-zero P_tr implies no source-coupled local H_tr pole",
            "derivation": "H_tr=P_tr^dagger Hess(S_parent) P_tr has no local source-coupled domain if the projected local trace subspace is zero-dimensional; a Green-function pole requires a nonzero local source-coupled image",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "H_tr not computed and rank-zero not signed",
            "what_it_buys": "lambda_tr is not a physical local range on the zero branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "ZP886_3_source_cokernel_zero",
            "statement": "rank-zero plus matter descent gives zero J_tr source-cokernel",
            "derivation": "if J_parent is compact-local and descends through q_loc, then <P_tr u,J_parent>=0 for all physical local modes u; equivalently J_tr=P_tr^dagger J_parent has zero projection on local cokernel modes",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "matter descent and no-marker clauses remain unsigned",
            "what_it_buys": "kills R10/WEP/clock/orbital trace source amplitudes without tuning a small coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "ZP886_4_readout_source_at_zero",
            "statement": "if P_tr is only a post-variation readout/source-at-zero observable, it cannot backreact as a local spurion",
            "derivation": "338-style readout discipline permits measuring q_trace after solving the parent equations, but forbids inserting the readout as a local source term in S_parent",
            "proof_status": "conditional_rule_valid",
            "parent_status": "readout-only status not signed for the trace endpoint",
            "what_it_buys": "separates cosmological readout from local fifth-force carrier",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "ZP886_5_zero_return_corollary",
            "statement": "rank-zero/no-pole/source-cokernel jointly imply the retained trace branch zero-returns locally",
            "derivation": "no local image + no Green-function pole + no source-cokernel means no finite alpha(lambda), no PPN trace scalar, no clock/WEP trace charge, and no orbital trace force from this branch",
            "proof_status": "conditional_corollary_valid",
            "parent_status": "premises not parent-signed",
            "what_it_buys": "a real path to c_T=0 rather than a fitted tiny coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "ZP886_6_verdict",
            "statement": "the implication theorem is valid, but the current corpus does not prove its premises",
            "derivation": "885/878/874/873/870 supply exact contracts and conditional lemmas, not parent-owned P_tr, q_loc, support/no-tail, H_tr, or source-cokernel signatures",
            "proof_status": "conditional_not_promoted",
            "parent_status": "missing_parent_signatures",
            "what_it_buys": "the next target is now one specific parent action clause: readout-only boundary support, otherwise finite-carrier source pack",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def parent_signature_debt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "debt_id": "PSD886_0_Ptr_owner",
            "needed_signature": "P_tr is a parent-owned boundary/readout trace direction or a defined quotient projector",
            "current_status": "closure_only",
            "if_signed": "rank test can be applied to a real object",
            "if_failed": "finite local trace carrier branch remains legal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "debt_id": "PSD886_1_q_loc_compact_restriction",
            "needed_signature": "q_loc[U] is a compact restriction/jet quotient of local observed geometry",
            "current_status": "not_parent_defined",
            "if_signed": "boundary/global endpoint directions can be tested for local verticality",
            "if_failed": "q_loc may see Q_trace as local scalar/conformal data",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "debt_id": "PSD886_2_boundary_support_no_tail",
            "needed_signature": "j^k v_tr|_U=0 or pure gauge/exact-zero and P_loc dB_trace=0 on compact U",
            "current_status": "open_nohair_clause",
            "if_signed": "local trace rank is zero",
            "if_failed": "boundary tail/source flux activates c_T",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "debt_id": "PSD886_3_matter_descent_no_marker",
            "needed_signature": "matter measure/coframe/connection/constants descend through q_loc with no Q_trace marker",
            "current_status": "not_parent_signed",
            "if_signed": "J_tr source-cokernel vanishes for local matter",
            "if_failed": "WEP/clock/R10 matter charge rows must be filled",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "debt_id": "PSD886_4_Htr_constraint_rank",
            "needed_signature": "H_tr reduced inverse has no local source-coupled pole, or H_tr never exists because P_tr is readout-only",
            "current_status": "not_tested",
            "if_signed": "no finite local lambda_tr branch",
            "if_failed": "Z_tr, mu_tr^2, lambda_tr, and alpha(lambda) branch become mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "debt_id": "PSD886_5_other_q_loc_channels",
            "needed_signature": "other local residual channels besides trace are also zeroed or bounded",
            "current_status": "outside_886_scope_but_required_for_local_GR",
            "if_signed": "trace closure can contribute to full local GR branch",
            "if_failed": "even a trace zero-return is not a full GR/Newton derivation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def finite_carrier_branch_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "FC886_0_local_conformal_scalar",
            "legal_if_unsigned": "P_tr has nonzero local jet support and H_tr has a reduced inverse",
            "damage": "finite trace scalar can mediate R10/orbital force and shift PPN gamma/beta",
            "required_response": "derive Z_tr, mu_tr^2, lambda_tr, J_tr, and metric/source response before testing",
            "current_status": "retained_nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "FC886_1_boundary_tail",
            "legal_if_unsigned": "P_loc dB_trace or P_loc J_trace has a compact-domain tail",
            "damage": "cosmological endpoint current leaks into local source terms",
            "required_response": "prove no-tail/support theorem or map tail to c_T residual vector",
            "current_status": "retained_nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "FC886_2_matter_marker",
            "legal_if_unsigned": "matter constants, clocks, binding energy, or EM carry Q_trace marker dependence",
            "damage": "WEP/clock/EM channels activate even if geometry rank appears zero",
            "required_response": "derive no-marker matter descent or fill species/clock coefficients",
            "current_status": "retained_nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "FC886_3_finite_fibre_trace",
            "legal_if_unsigned": "trace is quotient-invariant but not decoupled/gapped/source-blind",
            "damage": "basis-free trace class can still be a local scalar marker",
            "required_response": "prove source-independent stationary/gapped auxiliary theorem or bound it",
            "current_status": "retained_nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "FC886_4_bound_pack_required",
            "legal_if_unsigned": "any FC886_0 through FC886_3 remains open",
            "damage": "no local-GR claim; finite carrier/source rows must be sourced",
            "required_response": "build minimum source pack for Z_tr, lambda_tr, Q_tr/m, PPN/clock/orbital response with valid_for_claim=false until numeric and sourced",
            "current_status": "next_if_readout_clause_fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def source_pack_queue_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "SP886_0_Ztr",
            "quantity": "Z_tr",
            "needed_if": "finite local trace carrier survives zero-pole gate",
            "required_source": "principal symbol of parent H_tr",
            "current_status": "MISSING_PARENT_SYMBOL",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "SP886_1_lambda_tr",
            "quantity": "lambda_tr",
            "needed_if": "finite local trace carrier has a mass pole",
            "required_source": "m_tr^2=mu_tr^2/Z_tr from parent H_tr",
            "current_status": "MISSING_MASS_GAP",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "SP886_2_Qtr_over_m",
            "quantity": "Q_tr^A/m_A",
            "needed_if": "J_tr source-cokernel is nonzero",
            "required_source": "matter-source projection or body response functional",
            "current_status": "MISSING_SOURCE_PROJECTION",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "SP886_3_species_clock",
            "quantity": "Delta(Q_tr/m)_AB and clock trace response",
            "needed_if": "matter/no-marker descent fails",
            "required_source": "species/clock constants response to trace direction",
            "current_status": "MISSING_NO_MARKER_OR_COEFFICIENTS",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "SP886_4_metric_response",
            "quantity": "C_T_gamma, C_T_beta, source-normalization response",
            "needed_if": "finite trace carrier modifies observed metric/source",
            "required_source": "weak-field solution and measured-GM absorption audit",
            "current_status": "MISSING_RESPONSE_OPERATOR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG886_0_rank_zero",
            "promotion_target": "rank(P_loc P_tr P_loc^dagger)=0",
            "required_to_pass": "parent P_tr plus q_loc compact restriction plus boundary/readout support/no-tail",
            "current_evidence": "conditional implication theorem only",
            "gate_result": "fail_for_claim",
            "next_action": "derive readout-only boundary support action clause",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG886_1_no_pole",
            "promotion_target": "no local source-coupled H_tr pole",
            "required_to_pass": "rank-zero or computed reduced H_tr inverse with no physical pole",
            "current_evidence": "H_tr not computed; rank-zero not signed",
            "gate_result": "fail_for_claim",
            "next_action": "readout-only route first, finite-carrier source pack if it fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG886_2_source_cokernel",
            "promotion_target": "J_tr source-cokernel projection vanishes",
            "required_to_pass": "matter descent/no-marker plus P_tr local rank zero or explicit cokernel pairing",
            "current_evidence": "conditional chain-rule zero only",
            "gate_result": "fail_for_claim",
            "next_action": "derive matter/readout source silence or fill Q_tr/m rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG886_3_cT_zero_return",
            "promotion_target": "local trace branch zero-returns",
            "required_to_pass": "rank-zero, no-pole, source-cokernel, and no-tail all signed",
            "current_evidence": "valid implication chain, unsigned premises",
            "gate_result": "fail_for_claim",
            "next_action": "do not score R10/PPN as pass; continue proof or source pack",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG886_4_local_GR",
            "promotion_target": "MTS locally reduces to GR/Newton",
            "required_to_pass": "trace branch zero-return plus all other q_loc residual/source-normalization channels controlled",
            "current_evidence": "trace branch still conditional and other channels remain open",
            "gate_result": "fail_for_claim",
            "next_action": "keep full local GR gate blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC886_0_selected",
            "route": "readout_only_boundary_support_action_clause_or_finite_trace_carrier_source_pack",
            "status": "selected",
            "reason": "the zero-pole implication theorem is now clean; the least-scrutiny derivation path is to parent-sign P_tr as readout-only/boundary-supported, otherwise immediately build the finite-carrier source pack",
            "include": "readout-after-variation status, boundary support/no-tail action clause, q_loc compact restriction, source-at-zero rule, finite trace carrier fallback source pack",
            "exclude": "rank-zero claim, c_T zero claim, local-GR/Newton pass, R10/PPN pass, fitted coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG886_0_no_rank_zero_claim",
            "forbidden_claim": "local trace rank is zero",
            "status": "forbidden",
            "reason": "rank-zero implication is conditional; parent P_tr/q_loc/support signatures are missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG886_1_no_no_pole_claim",
            "forbidden_claim": "H_tr has no physical local pole",
            "status": "forbidden",
            "reason": "H_tr is not computed and rank-zero is not parent-signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG886_2_no_source_zero_claim",
            "forbidden_claim": "J_tr source-cokernel vanishes",
            "status": "forbidden",
            "reason": "matter descent/no-marker/source pairing remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG886_3_no_local_GR_claim",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace zero-return is conditional and other local residual channels are not closed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG886_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "886 proves the conditional zero-pole/source-cokernel implication and names the exact parent signatures still required",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D886_0",
            "finding": "zero_pole_implication_theorem_valid",
            "reason": "rank-zero/readout-only P_tr would remove the local trace image, pole, and source-cokernel together",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D886_1",
            "finding": "premises_not_parent_signed",
            "reason": "P_tr/q_loc/support/no-tail/H_tr/J_tr/matter descent signatures remain missing or conditional",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D886_2",
            "finding": "next_route_readout_clause_or_finite_pack",
            "reason": "either make P_tr a true source-at-zero boundary readout, or stop trying to zero it and source the finite carrier branch",
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
            "objective": "try to parent-sign P_tr as a readout-only/boundary-supported source-at-zero direction; if that fails, build the finite trace carrier source pack without claiming local GR",
            "include": "readout-after-variation clause, boundary support/no-tail certificate, q_loc compact restriction, no-spurion rule, finite-carrier Z_tr/lambda_tr/J_tr/Q_tr source pack",
            "exclude": "public claim, fitted coupling, R10/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_885_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_885_VALIDATION.csv"
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


def all_nonclaim(row_groups: Iterable[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)) != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    debt_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    zero_ids = {row["theorem_id"] for row in zero_rows}
    debt_ids = {row["debt_id"] for row in debt_rows}
    queue_statuses = [str(row["current_status"]) for row in queue_rows]
    row_groups = [
        source_rows,
        zero_rows,
        debt_rows,
        finite_rows,
        queue_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    checks = [
        {
            "check_id": "V886_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V886_1_prior_885_clean",
            "result": "pass" if prior_885_clean() else "fail",
            "detail": "P8_Y5_BRR545_885_VALIDATION.csv clean",
        },
        {
            "check_id": "V886_2_zero_implication_written",
            "result": "pass" if {"ZP886_1_rank_zero_implication", "ZP886_2_rank_zero_no_pole", "ZP886_3_source_cokernel_zero", "ZP886_5_zero_return_corollary"}.issubset(zero_ids) else "fail",
            "detail": "rank-zero/no-pole/source-cokernel implication rows present",
        },
        {
            "check_id": "V886_3_zero_not_promoted",
            "result": "pass" if any(row["theorem_id"] == "ZP886_6_verdict" and row["proof_status"] == "conditional_not_promoted" for row in zero_rows) else "fail",
            "detail": "zero-return verdict remains conditional_not_promoted",
        },
        {
            "check_id": "V886_4_parent_debts_complete",
            "result": "pass" if {"PSD886_0_Ptr_owner", "PSD886_1_q_loc_compact_restriction", "PSD886_2_boundary_support_no_tail", "PSD886_3_matter_descent_no_marker", "PSD886_4_Htr_constraint_rank"}.issubset(debt_ids) else "fail",
            "detail": "required parent signature debts recorded",
        },
        {
            "check_id": "V886_5_finite_carrier_retained",
            "result": "pass" if finite_rows and all(row["current_status"] in {"retained_nonclaim", "next_if_readout_clause_fails"} for row in finite_rows) else "fail",
            "detail": "finite-carrier counterbranch remains retained/nonclaim",
        },
        {
            "check_id": "V886_6_source_pack_missing_markers",
            "result": "pass" if queue_statuses and all("MISSING" in status for status in queue_statuses) else "fail",
            "detail": "finite-carrier source pack rows stay missing/nonclaim",
        },
        {
            "check_id": "V886_7_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V886_8_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V886_9_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V886_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V886_11_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V886_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return [{**row, "generated_utc": generated_utc} for row in checks]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    debt_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 886 - Y5/R10 Htr Zero-Pole Rank Test and Jtr Source-Cokernel Gate",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the local trace zero-return route now has a real conditional theorem, but not a parent-signed proof**. If `P_tr` is genuinely a readout-only/boundary-supported direction with zero compact-local rank, then `H_tr` has no source-coupled local pole and `J_tr` has zero source-cokernel against local matter. That would kill the retained trace coupling without tuning. The catch is exactly where it should be: the corpus still has to parent-sign `P_tr`, `q_loc`, boundary support/no-tail, matter descent/no-marker, and the readout-after-variation rule. So no local-GR or R10/PPN pass is claimed.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Zero-Pole Implication Theorem",
        md_table(zero_rows),
        "",
        "## Parent Signature Debts",
        md_table(debt_rows),
        "",
        "## Finite-Carrier Counterbranch",
        md_table(finite_rows),
        "",
        "## Source-Pack Queue",
        md_table(queue_rows),
        "",
        "## Promotion Gates",
        md_table(promotion_rows),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guards",
        md_table(guard_rows),
        "",
        "## Decisions",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    zero_rows = zero_pole_implication_rows(generated_utc)
    debt_rows = parent_signature_debt_rows(generated_utc)
    finite_rows = finite_carrier_branch_rows(generated_utc)
    queue_rows = source_pack_queue_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows,
        zero_rows,
        debt_rows,
        finite_rows,
        queue_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_886_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_886_ZERO_POLE_IMPLICATION_THEOREM.csv": zero_rows,
        "P8_Y5_R10_886_PARENT_SIGNATURE_DEBTS.csv": debt_rows,
        "P8_Y5_R10_886_FINITE_CARRIER_COUNTERBRANCH.csv": finite_rows,
        "P8_Y5_R10_886_SOURCE_PACK_QUEUE.csv": queue_rows,
        "P8_Y5_R10_886_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_886_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_886_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_886_DECISION.csv": decision_rows_,
        "P8_Y5_R10_886_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_886_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_886_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        zero_rows,
        debt_rows,
        finite_rows,
        queue_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_886_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
