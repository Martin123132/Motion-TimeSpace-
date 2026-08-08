from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_889_parent_spine_repair_contract_written_conditional_theorem_not_parent_signed_finite_runner_dryrun_blocked_nonclaim"
CLAIM_CEILING = "conditional_boundary_quotient_repair_contract_and_runner_blocker_dryrun_only_no_readout_promotion_no_cT_zero_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "890-Y5-R10-boundary-quotient-no-tail-signature-or-finite-trace-coefficient-acquisition.md"


SOURCE_SPECS = [
    {
        "source_id": "888_doc",
        "path": ROOT / "888-Y5-R10-parent-spine-readout-clause-integration-or-finite-trace-carrier-runner.md",
        "needle": "compatible with the parent-spine discipline but not integrated as a theorem",
        "role": "immediate integration/fallback handoff",
    },
    {
        "source_id": "888_validation",
        "path": OUT / "P8_Y5_BRR545_888_VALIDATION.csv",
        "needle": "V888_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "888_runner_skeleton",
        "path": OUT / "P8_Y5_R10_888_FINITE_TRACE_RUNNER_SKELETON.csv",
        "needle": "RUN888_5_runner_verdict",
        "role": "finite trace runner skeleton to dry-run",
    },
    {
        "source_id": "887_readout_clause",
        "path": OUT / "P8_Y5_R10_887_READOUT_BOUNDARY_CLAUSE.csv",
        "needle": "RO887_6_clause_verdict",
        "role": "readout-only boundary-support clause to repair",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "local trace zero-return route now has a real conditional theorem",
        "role": "conditional rank-zero/no-pole/source-cokernel implication",
    },
    {
        "source_id": "177_parent_action",
        "path": ROOT / "177-parent-action-perturbation-local-GR-contract.md",
        "needle": "S_parent =",
        "role": "parent action slot and local-GR contract",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "Projection is applied only to observables/current readout.",
        "role": "exact parent readout rule",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero != physical spurion",
        "role": "source-at-zero/no-spurion discipline",
    },
    {
        "source_id": "446_no_cheat",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "readout variables enter only after variation and cannot backreact",
        "role": "readout-after-variation no-cheat rule",
    },
    {
        "source_id": "870_nohair",
        "path": ROOT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        "needle": "support(J_trace) is only FLRW zero-mode/global boundary support",
        "role": "boundary support/no-tail blocker",
    },
    {
        "source_id": "873_charge_zero",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "Q_T^A=0 follows by chain rule",
        "role": "matter trace-charge zero lemma",
    },
    {
        "source_id": "874_verticality",
        "path": ROOT / "874-Y5-R10-parent-qloc-verticality-signature-or-cT-coefficient-fill.md",
        "needle": "q_loc[U] is a compact-domain restriction/jet quotient",
        "role": "compact q_loc verticality contract",
    },
    {
        "source_id": "654_local_gr_spine",
        "path": ROOT / "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md",
        "needle": "local_GR_claim | hardest_next_blocker",
        "role": "broader local-GR stack status",
    },
    {
        "source_id": "437_R10_contract",
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needle": "Anything else remains symbolic and blocks R10 promotion.",
        "role": "finite-carrier R10 claim discipline",
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
            "what_changed": "wrote an exact boundary-quotient repair contract that would integrate the 887 readout clause if signed, then dry-ran the finite trace runner as a blocker ledger",
            "best_partial_result": "the derivation path is now a sharp sufficient theorem: if the parent configuration splits into compact local jets plus boundary cohomology, the trace direction has no compact jet/tail, matter descends through q_loc with no marker constants, and readout sources are set to zero after variation, then P_tr has zero local rank and the 886 zero-pole/source-cokernel theorem can fire",
            "hard_blockers": "the boundary/no-tail cohomology signature and parent q_loc/matter no-marker signatures are still not proved inside an actual MTS parent action; finite branch still lacks Z_tr, lambda_tr, Q_tr/m, PPN, clock/WEP, orbital coefficients, and sourced bounds",
            "what_is_not_claimed": "readout-only theorem, v_tr in ker(Dq_loc), P_tr rank zero, c_T=0, finite carrier pass, R10/PPN/WEP/clock/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def repair_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "RC889_0_parent_configuration_split",
            "repair_clause": "Parent configuration space splits locally into compact jet data and boundary/cohomology class data before scoring/readout.",
            "mathematical_form": "Phi -> (q_loc[U](Phi), b_partial(Phi)); q_loc[U]=[j^k Phi|_U]_gauge and b_partial in H_boundary/relative class for compact U away from cosmological boundary.",
            "proof_role": "makes local variables and boundary trace readout different quotient coordinates rather than separate patched sectors",
            "current_status": "sufficient_contract_written_not_parent_signed",
            "if_signed": "q_loc has a parent-owned definition and the trace endpoint can be globally visible while locally vertical",
            "if_failed": "trace variable may be a physical local scalar/conformal mode requiring bounds",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RC889_1_trace_vertical_generator",
            "repair_clause": "The trace/readout generator v_tr is vertical for q_loc but not necessarily for the FLRW/global readout.",
            "mathematical_form": "Dq_loc[U][v_tr]=[j^k v_tr|_U]_gauge=0 while Dq_FLRW[v_tr] may be nonzero.",
            "proof_role": "turns local trace silence into a quotient statement rather than a fitted small coupling",
            "current_status": "conditional_from_874_not_parent_signed",
            "if_signed": "local matter sees no trace endpoint through compact rods/clocks",
            "if_failed": "finite c_T branch stays legal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RC889_2_boundary_no_tail",
            "repair_clause": "Boundary/exact trace current has no compact local tail, flux, scalar gradient, vector hair, or tensor hair.",
            "mathematical_form": "P_loc J_trace|_U=0 and P_loc dB_trace|_U=0 through tested order; all local relative fluxes vanish.",
            "proof_role": "prevents a boundary readout from leaking back into local fifth-force/PPN/clock channels",
            "current_status": "hardest_unsigned_clause",
            "if_signed": "P_loc P_tr P_loc^dagger has zero compact rank for the trace endpoint",
            "if_failed": "local trace leakage maps to R10/PPN/clock/orbital residual vector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RC889_3_variation_order",
            "repair_clause": "All physical fields are varied before the trace readout/probe source is applied, and the probe source is set to zero.",
            "mathematical_form": "delta(S_parent+s_tr R_tr)/delta Phi at s_tr=0 equals delta S_parent/delta Phi; R_tr is an observable map on Sol(S_parent).",
            "proof_role": "blocks readout-after-variation backreaction and spurion cheating",
            "current_status": "policy_supported_by_337_338_446_not_trace_parent_signed",
            "if_signed": "R_tr cannot create a physical local source term",
            "if_failed": "readout source is a physical spurion and must be bounded",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RC889_4_matter_stack_no_marker",
            "repair_clause": "Matter measure, coframe/metric, connection, derivative operator, masses, alpha_EM, species labels, and clock constants factor through q_loc and carry no trace marker.",
            "mathematical_form": "S_matter=Sbar[q_loc(Phi),Psi,theta] with partial_{v_tr}theta=0 and no reduced EFT operator O_loc(Q_trace).",
            "proof_role": "lets the 873 chain-rule charge-zero theorem kill Q_tr^A for local matter",
            "current_status": "conditional_from_873_not_parent_signed",
            "if_signed": "J_tr source-cokernel vanishes for local matter",
            "if_failed": "WEP/clock/EM/species source coefficients must be filled",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RC889_5_local_GR_scope_guard",
            "repair_clause": "Trace-branch closure is only one local-GR subgate; EH operator, source normalization, PPN vector, and other residual channels remain separate requirements.",
            "mathematical_form": "trace_zero_return != local_GR; local_GR requires EH + Newtonian source law + PPN residual vector + all retained q_loc channels zeroed/bounded.",
            "proof_role": "prevents a real trace success from being over-promoted to full GR/Newton",
            "current_status": "guard_active",
            "if_signed": "trace branch can contribute to the GR derivation spine without overstating it",
            "if_failed": "project becomes another isolated fifth-force/MOND-like patch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "RC889_6_repair_verdict",
            "repair_clause": "RC889_0 through RC889_5 must be signed by one parent action/spine to integrate the readout route.",
            "mathematical_form": "boundary quotient split + vertical generator + no-tail + source-at-zero variation + matter no-marker + local-GR scope guard",
            "proof_role": "exact contract for a future parent action to close the trace branch",
            "current_status": "conditional_contract_complete_but_not_parent_signed",
            "if_signed": "the 886 zero-pole/source-cokernel theorem can be promoted for the trace branch in a later checkpoint",
            "if_failed": "finite trace carrier coefficient acquisition remains mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def conditional_proof_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "proof_id": "CP889_0_local_quotient_derivative",
            "claim": "If q_loc[U]=[j^k Phi|_U]_gauge and j^k v_tr|_U is zero/gauge-exact, then Dq_loc[U][v_tr]=0.",
            "derivation": "Dq_loc[U][v_tr]=D([j^k Phi|_U]_gauge)[v_tr]=[j^k v_tr|_U]_gauge=0.",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "q_loc_and_support_not_parent_signed",
            "what_it_buys": "trace endpoint becomes locally vertical instead of small-coupled",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "CP889_1_no_tail_to_rank_zero",
            "claim": "If v_tr has only boundary/FLRW class support and no local tail, P_loc P_tr P_loc^dagger has zero compact local rank.",
            "derivation": "for every compact test mode eta_U, P_tr P_loc^dagger eta_U has no gauge-invariant image in the trace quotient; hence all local trace matrix elements vanish",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "boundary_no_tail_signature_missing",
            "what_it_buys": "feeds the exact rank-zero premise of 886",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "CP889_2_matter_chain_rule",
            "claim": "If matter descends through q_loc and constants have no trace marker, local matter trace charge is zero.",
            "derivation": "partial_{v_tr}S_matter=(delta Sbar/dq_loc)Dq_loc[v_tr]+(partial Sbar/partial theta)partial_{v_tr}theta=0",
            "proof_status": "conditional_theorem_valid",
            "parent_status": "matter_stack_no_marker_not_parent_signed",
            "what_it_buys": "kills direct R10/WEP/clock source charge on the trace branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "CP889_3_readout_source_zero",
            "claim": "If R_tr is post-variation/source-at-zero, it cannot generate a local force in the parent Euler equations.",
            "derivation": "physical equations use s_tr=0, so delta(s_tr R_tr)/delta Phi contributes no on-shell source term",
            "proof_status": "conditional_rule_valid",
            "parent_status": "readout_policy_supported_trace_clause_not_integrated",
            "what_it_buys": "prevents the readout from becoming a spurion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "CP889_4_zero_return_corollary",
            "claim": "If CP889_0 through CP889_3 are parent-signed, the trace branch has no local source-coupled pole or source-cokernel.",
            "derivation": "rank-zero P_tr plus matter descent satisfies the 886 hypotheses, so H_tr has no source-coupled local pole and J_tr has zero local cokernel",
            "proof_status": "conditional_corollary_valid",
            "parent_status": "premises_not_jointly_signed",
            "what_it_buys": "a derivation route to trace zero-return without tuning a coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "CP889_5_verdict",
            "claim": "889 repairs the clause as an exact sufficient theorem but does not close it as physics.",
            "derivation": "the proof is mathematically valid under explicit boundary quotient/no-tail/matter descent premises; current corpus supplies contracts and lemmas, not one parent-signed action proof",
            "proof_status": "conditional_theorem_valid_not_promoted",
            "parent_status": "missing_parent_signature",
            "what_it_buys": "the next derivation target is no longer vague: sign boundary quotient/no-tail first, or fill finite trace coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def premise_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "premise_id": "PA889_0_parent_configuration_split",
            "required_for": "RC889_0 and CP889_0",
            "current_evidence": "177 has parent action slot; 874 writes q_loc compact quotient contract",
            "audit_result": "contract_present_not_action_derived",
            "next_action": "write/sign parent bundle map Phi -> (q_loc,boundary class)",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "premise_id": "PA889_1_boundary_no_tail",
            "required_for": "RC889_2 and CP889_1",
            "current_evidence": "870 identifies support/no-tail theorem as open",
            "audit_result": "hard_fail_open",
            "next_action": "prove relative cohomology/no local flux theorem or demote to finite coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "premise_id": "PA889_2_matter_no_marker",
            "required_for": "RC889_4 and CP889_2",
            "current_evidence": "873 gives valid chain-rule theorem but parent signature remains missing",
            "audit_result": "conditional_not_parent_signed",
            "next_action": "sign full measure/coframe/connection/constants descent through q_loc",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "premise_id": "PA889_3_readout_source_zero",
            "required_for": "RC889_3 and CP889_3",
            "current_evidence": "337/338/446 support post-variation source-at-zero readout discipline",
            "audit_result": "policy_pass_not_trace_parent_signed",
            "next_action": "embed R_tr as a source-at-zero observable map on Sol(S_parent), not as a local field",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "premise_id": "PA889_4_finite_coefficients",
            "required_for": "finite branch if repair fails",
            "current_evidence": "888 runner skeleton lists missing Z_tr/lambda_tr/Q_tr and arena response coefficients",
            "audit_result": "missing_all_numeric_parent_inputs",
            "next_action": "acquire coefficients only if no-tail/zero route fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "premise_id": "PA889_5_local_GR_scope",
            "required_for": "full GR/Newton derivation",
            "current_evidence": "654/346 keep EH/source-normalization/PPN stack open",
            "audit_result": "outside_trace_branch_still_open",
            "next_action": "do not promote trace progress to full local-GR claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def finite_runner_dryrun_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "dryrun_id": "DR889_0_input_load",
            "arena": "runner_schema",
            "loaded_from": "P8_Y5_R10_888_FINITE_TRACE_RUNNER_SKELETON.csv",
            "required_inputs": "P_tr,H_tr,Z_tr,lambda_tr,J_tr,Q_tr/m,bounds,responses",
            "dryrun_result": "BLOCKED_SCHEMA_ONLY",
            "reason": "runner can load schema but no row contains numeric sourced parent coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DR889_1_zero_branch",
            "arena": "conditional_zero",
            "loaded_from": "RC889/CP889 theorem rows",
            "required_inputs": "parent-signed boundary quotient, no-tail, matter no-marker, source-at-zero",
            "dryrun_result": "BLOCKED_PREMISES_UNSIGNED",
            "reason": "conditional theorem exists but parent signature is missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DR889_2_R10",
            "arena": "R10_alpha_lambda",
            "loaded_from": "437_R10_contract and 888 runner skeleton",
            "required_inputs": "Z_tr, lambda_tr, Q_tr^source/m, Q_tr^test/m, full alpha_bound(lambda)",
            "dryrun_result": "BLOCKED_MISSING_COEFFICIENTS_AND_BOUND_CURVE",
            "reason": "symbolic alpha(lambda) cannot be compared or claimed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DR889_3_PPN",
            "arena": "PPN_gamma_beta_preferred_frame",
            "loaded_from": "654 local-GR spine and 888 runner skeleton",
            "required_inputs": "C_T_gamma,C_T_beta,C_T_alpha_i and source normalization",
            "dryrun_result": "BLOCKED_MISSING_RESPONSE_OPERATOR",
            "reason": "no PPN residual vector is derived for finite trace leakage",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DR889_4_clocks_WEP",
            "arena": "clock_WEP_EM_species",
            "loaded_from": "873 matter no-marker theorem and 888 runner skeleton",
            "required_inputs": "clock trace charges, Delta(Q_tr/m)_AB, alpha_EM/mass marker audit",
            "dryrun_result": "BLOCKED_NO_MARKER_UNSIGNED",
            "reason": "conditional charge-zero theorem is not enough and finite coefficients are absent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DR889_5_orbital",
            "arena": "orbital_GM_Newton",
            "loaded_from": "177/654 local-GR/source-normalization contracts",
            "required_inputs": "orbital Yukawa response, GM absorption theorem, Gdot/deltaGM bounds",
            "dryrun_result": "BLOCKED_SOURCE_NORMALIZATION_OPEN",
            "reason": "trace branch cannot be folded into Newtonian source law without a theorem or coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DR889_6_dryrun_verdict",
            "arena": "all",
            "loaded_from": "889 repair theorem plus 888 skeleton",
            "required_inputs": "either parent-signed zero branch or fully sourced finite branch",
            "dryrun_result": "BLOCKED_NO_PHYSICAL_RUN",
            "reason": "dry-run proves the refusal logic works: no local claim is emitted from missing inputs",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def blocker_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BL889_0_boundary_no_tail",
            "blocker": "prove boundary/relative-cohomology trace current has no compact local tail or flux",
            "why_it_matters": "this is the shortest derivation-first route to rank(P_loc P_tr P_loc^dagger)=0",
            "if_not_solved": "finite c_T/H_tr branch must be coefficient-filled",
            "priority": "highest",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL889_1_parent_qloc_bundle",
            "blocker": "define parent-owned q_loc[U] and boundary class map in one action-level bundle",
            "why_it_matters": "without this, verticality is a coordinate choice rather than a theorem",
            "if_not_solved": "local trace field remains legal",
            "priority": "high",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL889_2_matter_stack_no_marker",
            "blocker": "sign matter stack descent and no trace marker constants",
            "why_it_matters": "otherwise R10/WEP/clock/EM channels can reintroduce the coupling",
            "if_not_solved": "Q_tr/m coefficients required",
            "priority": "high",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL889_3_finite_coefficients",
            "blocker": "derive or source Z_tr, lambda_tr, Q_tr/m, PPN, clock/WEP, and orbital response coefficients",
            "why_it_matters": "needed if the zero route fails",
            "if_not_solved": "finite branch remains untestable",
            "priority": "fallback",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL889_4_full_local_GR",
            "blocker": "EH operator, source normalization, PPN vector, and other q_loc residual branches",
            "why_it_matters": "trace closure is not full GR/Newton derivation",
            "if_not_solved": "framework remains short of local GR",
            "priority": "parallel_after_trace",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG889_0_repair_contract",
            "promotion_target": "readout-only trace branch is parent integrated",
            "required_to_pass": "RC889_0 through RC889_4 parent-signed by one action/spine",
            "current_evidence": "sufficient contract written; signatures missing",
            "gate_result": "fail_for_claim",
            "next_action": "attack boundary no-tail/quotient signature first",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG889_1_zero_return",
            "promotion_target": "c_T trace branch zero-returns locally",
            "required_to_pass": "CP889 theorem premises plus 886 rank-zero/no-pole/source-cokernel",
            "current_evidence": "conditional theorem only",
            "gate_result": "fail_for_claim",
            "next_action": "do not claim c_T=0",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG889_2_finite_runner",
            "promotion_target": "finite trace carrier can be scored against local arenas",
            "required_to_pass": "no missing coefficients and sourced R10/PPN/clock/orbital rows",
            "current_evidence": "dry-run blocker ledger only",
            "gate_result": "fail_for_claim",
            "next_action": "acquire coefficients only if no-tail proof fails",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG889_3_local_GR",
            "promotion_target": "MTS derives local GR/Newton",
            "required_to_pass": "trace branch plus all EH/source-normalization/PPN/q_loc channels closed",
            "current_evidence": "trace branch still not closed",
            "gate_result": "fail_for_claim",
            "next_action": "keep deriving; no local-GR claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC889_0_selected",
            "route": "boundary_quotient_no_tail_signature_or_finite_trace_coefficient_acquisition",
            "status": "selected",
            "reason": "889 converted the vague parent-spine gap into one hard mathematical target: prove no compact local tail/flux for the boundary quotient trace direction; if that fails, finite coefficients must be acquired",
            "include": "relative cohomology/no-tail proof attempt, parent q_loc bundle signature, coefficient fallback ledger",
            "exclude": "R10/PPN/local-GR claim, GitHub action, formalization-workbench edits, fitted tiny coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG889_0_no_parent_integration_claim",
            "forbidden_claim": "readout route is parent-integrated",
            "status": "forbidden",
            "reason": "889 writes a sufficient contract but does not sign it inside a concrete parent action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG889_1_no_cT_zero",
            "forbidden_claim": "c_T=0 or trace branch has no local carrier",
            "status": "forbidden",
            "reason": "no-tail and q_loc/matter signatures remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG889_2_no_finite_pass",
            "forbidden_claim": "finite trace carrier passes tests",
            "status": "forbidden",
            "reason": "dry-run has missing coefficients and bound curves",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG889_3_no_local_GR",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "broader EH/source-normalization/PPN stack remains open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG889_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "889 gives a sharper derivation target and a working blocker dry-run",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D889_0",
            "finding": "conditional_repair_theorem_written",
            "reason": "the exact boundary-quotient/source-at-zero/matter-no-marker premises now imply the 886 trace zero-return route",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D889_1",
            "finding": "not_parent_signed",
            "reason": "boundary no-tail, q_loc bundle, and matter no-marker signatures are still not derived from one parent action",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D889_2",
            "finding": "finite_runner_dryrun_blocked",
            "reason": "dry-run confirms no local arena can be scored without parent coefficients or a zero theorem",
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
            "objective": "try to sign the boundary-quotient/no-tail premise that would make the readout clause locally invisible; if it fails, begin finite trace coefficient acquisition with no claims",
            "include": "relative cohomology support theorem, compact local flux test, q_loc boundary bundle map, finite coefficient fallback",
            "exclude": "claiming c_T=0, claiming R10/PPN/local-GR pass, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_888_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_888_VALIDATION.csv"
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
    summary_rows: list[dict[str, object]],
    repair_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    premise_rows: list[dict[str, object]],
    dryrun_rows: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    repair_ids = {row["clause_id"] for row in repair_rows}
    proof_ids = {row["proof_id"] for row in proof_rows}
    dryrun_results = [str(row["dryrun_result"]) for row in dryrun_rows]
    row_groups = [
        source_rows,
        summary_rows,
        repair_rows,
        proof_rows,
        premise_rows,
        dryrun_rows,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    ]
    checks = [
        {
            "check_id": "V889_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all 889 source paths exist and needles are present",
        },
        {
            "check_id": "V889_1_prior_888_clean",
            "result": "pass" if prior_888_clean() else "fail",
            "detail": "P8_Y5_BRR545_888_VALIDATION.csv clean",
        },
        {
            "check_id": "V889_2_repair_contract_complete",
            "result": "pass" if {"RC889_0_parent_configuration_split", "RC889_1_trace_vertical_generator", "RC889_2_boundary_no_tail", "RC889_3_variation_order", "RC889_4_matter_stack_no_marker", "RC889_5_local_GR_scope_guard", "RC889_6_repair_verdict"}.issubset(repair_ids) else "fail",
            "detail": "all repair clauses present",
        },
        {
            "check_id": "V889_3_conditional_theorem_not_promoted",
            "result": "pass" if "CP889_5_verdict" in proof_ids and any(row["proof_id"] == "CP889_5_verdict" and row["parent_status"] == "missing_parent_signature" for row in proof_rows) else "fail",
            "detail": "conditional theorem exists but remains not parent-signed",
        },
        {
            "check_id": "V889_4_premise_audit_identifies_no_tail_as_hard_fail",
            "result": "pass" if any(row["premise_id"] == "PA889_1_boundary_no_tail" and row["audit_result"] == "hard_fail_open" for row in premise_rows) else "fail",
            "detail": "boundary/no-tail premise is identified as the main open derivation target",
        },
        {
            "check_id": "V889_5_finite_runner_dryrun_blocked",
            "result": "pass" if dryrun_rows and all(result.startswith("BLOCKED") for result in dryrun_results) else "fail",
            "detail": "finite runner dry-run refuses every arena",
        },
        {
            "check_id": "V889_6_blocker_ledger_ready",
            "result": "pass" if len(blocker_rows) >= 5 and any(row["blocker_id"] == "BL889_0_boundary_no_tail" for row in blocker_rows) else "fail",
            "detail": "blocker ledger includes boundary/no-tail, q_loc, matter, finite coefficients, local GR",
        },
        {
            "check_id": "V889_7_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V889_8_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V889_9_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V889_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V889_11_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V889_12_validation_rows_ready",
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
    repair_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    premise_rows: list[dict[str, object]],
    dryrun_rows: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 889 - Y5/R10 Finite Trace Carrier Runner Dry-Run or Parent-Spine Clause Repair",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **889 turns the readout route into an exact conditional repair theorem, but still not a claim**. If the parent action supplies a boundary-quotient split, a trace generator with no compact local jet/tail, source-at-zero post-variation readout, and matter/no-marker descent through `q_loc`, then the 886 zero-pole/source-cokernel theorem can close the trace branch. The current corpus does not yet sign the boundary/no-tail and matter/q_loc premises, so the finite trace runner dry-run correctly blocks every local arena.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Parent-Spine Repair Contract",
        md_table(repair_rows),
        "",
        "## Conditional Proof",
        md_table(proof_rows),
        "",
        "## Premise Audit",
        md_table(premise_rows),
        "",
        "## Finite Runner Dry-Run",
        md_table(dryrun_rows),
        "",
        "## Blocker Ledger",
        md_table(blocker_rows),
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
    repair_rows = repair_contract_rows(generated_utc)
    proof_rows = conditional_proof_rows(generated_utc)
    premise_rows = premise_audit_rows(generated_utc)
    dryrun_rows = finite_runner_dryrun_rows(generated_utc)
    blocker_rows = blocker_ledger_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows,
        summary_rows,
        repair_rows,
        proof_rows,
        premise_rows,
        dryrun_rows,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    )

    outputs = {
        "P8_Y5_R10_889_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_889_PARENT_SPINE_REPAIR_CONTRACT.csv": repair_rows,
        "P8_Y5_R10_889_CONDITIONAL_PROOF.csv": proof_rows,
        "P8_Y5_R10_889_PREMISE_AUDIT.csv": premise_rows,
        "P8_Y5_R10_889_FINITE_RUNNER_DRYRUN.csv": dryrun_rows,
        "P8_Y5_R10_889_BLOCKER_LEDGER.csv": blocker_rows,
        "P8_Y5_R10_889_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_889_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_889_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_889_DECISION.csv": decision_rows_,
        "P8_Y5_R10_889_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_889_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_889_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "889-Y5-R10-finite-trace-carrier-runner-dryrun-or-parent-spine-clause-repair.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        repair_rows,
        proof_rows,
        premise_rows,
        dryrun_rows,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_889_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
