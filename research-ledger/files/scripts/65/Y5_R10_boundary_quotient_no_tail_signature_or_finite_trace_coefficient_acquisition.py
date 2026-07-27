from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_890_boundary_quotient_no_tail_theorem_attempt_conditional_only_transfer_rejected_finite_trace_coefficient_acquisition_plan_staged_nonclaim"
CLAIM_CEILING = "conditional_boundary_no_tail_theorem_and_coefficient_acquisition_plan_only_no_Ploc_Jtrace_zero_no_cT_zero_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "891-Y5-R10-finite-trace-coefficient-source-row-builder-with-zero-route-watch.md"


SOURCE_SPECS = [
    {
        "source_id": "889_doc",
        "path": ROOT / "889-Y5-R10-finite-trace-carrier-runner-dryrun-or-parent-spine-clause-repair.md",
        "needle": "exact conditional repair theorem",
        "role": "immediate boundary/no-tail handoff",
    },
    {
        "source_id": "889_validation",
        "path": OUT / "P8_Y5_BRR545_889_VALIDATION.csv",
        "needle": "V889_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "889_conditional_proof",
        "path": OUT / "P8_Y5_R10_889_CONDITIONAL_PROOF.csv",
        "needle": "CP889_5_verdict",
        "role": "conditional repair theorem to sharpen",
    },
    {
        "source_id": "889_blocker_ledger",
        "path": OUT / "P8_Y5_R10_889_BLOCKER_LEDGER.csv",
        "needle": "BL889_0_boundary_no_tail",
        "role": "boundary/no-tail blocker selected by 889",
    },
    {
        "source_id": "60_relative_contract",
        "path": ROOT / "60-relative-cohomology-boundary-contract.md",
        "needle": "relative_boundary_contract_written_not_derived",
        "role": "old relative cohomology local/FLRW split contract",
    },
    {
        "source_id": "231_Jrel_cohomology",
        "path": ROOT / "231-Jrel-cohomology-projector-or-local-EH-limit.md",
        "needle": "J_rel exactness has a cohomology theorem gate",
        "role": "real cohomology win for current/flux-like J_rel",
    },
    {
        "source_id": "273_Cperp_transfer_fail",
        "path": ROOT / "273-Cperp-relative-exactness-C-sector.md",
        "needle": "does not inherit the Jrel relative-cohomology",
        "role": "warning that cohomology transfer can fail for scalar representatives",
    },
    {
        "source_id": "549_boundary_certificate",
        "path": ROOT / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
        "needle": "boundary cohomology/no-hair certificate does not close",
        "role": "prior boundary cohomology/no-hair certificate failure",
    },
    {
        "source_id": "678_boundary_silence_stack",
        "path": ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md",
        "needle": "The corpus does **not** sign that stack",
        "role": "R10 boundary-class/nohair/projector silence stack failure",
    },
    {
        "source_id": "861_boundary_nohair_debt",
        "path": ROOT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        "needle": "boundary no-hair remain open",
        "role": "exact-readout/N5 branch keeps boundary no-hair open",
    },
    {
        "source_id": "863_trace_current",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "P_loc J_trace^mu = 0 while P_FLRW J_trace^mu may be nonzero",
        "role": "trace current local/global split target",
    },
    {
        "source_id": "864_local_global_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Boundary/exact trace currents have zero local projection",
        "role": "minimal local/global quotient and no-hair clause",
    },
    {
        "source_id": "882_ct_min_pack",
        "path": OUT / "P8_Y5_R10_882_RETAINED_CT_MINIMUM_SOURCE_PACK.csv",
        "needle": "MCP882_8_source_provenance",
        "role": "minimum retained c_T finite coefficient pack",
    },
    {
        "source_id": "485_no_flux_warning",
        "path": ROOT / "485-boundary-no-flux-and-R11-silence-from-local-zero.md",
        "needle": "scalar trace/volume statement",
        "role": "warning that scalar local zero does not kill vector/tensor boundary flux",
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
            "what_changed": "attempted to sign the boundary-quotient no-tail premise, audited whether the old J_rel cohomology theorem transfers to J_trace, and staged the finite trace coefficient acquisition plan",
            "best_partial_result": "a precise conditional no-tail theorem is now written: if J_trace is a parent-owned relative boundary current, its compact local relative class is zero, exact representatives have zero local flux, and scalar/vector/tensor/clock/species hair is absent, then P_loc J_trace=0 and the trace rank-zero route can fire",
            "hard_blockers": "the current corpus does not parent-sign the support class, no local flux certificate, vector/tensor/shear silence, or matter no-marker clauses; prior cohomology wins for J_rel do not automatically transfer to this trace endpoint current",
            "what_is_not_claimed": "P_loc J_trace=0, P_loc dB_trace=0, P_tr rank zero, c_T=0, R10/PPN/WEP/clock/orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def no_tail_theorem_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "NT890_0_parent_current_owner",
            "required_clause": "J_trace is a parent-owned Ward/exact current associated with a relative boundary class, not an inserted local field.",
            "mathematical_form": "J_trace=dB_trace+J_boundary with [J_boundary] in H_rel(boundary pair), defined before local readout.",
            "conditional_derivation": "only parent-owned currents can be quotient-tested; otherwise the current is a fitted residual source",
            "current_status": "candidate_shape_not_parent_signed",
            "if_signed": "trace current can be separated from ordinary matter/source flux",
            "if_failed": "retain finite local trace carrier/source rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NT890_1_compact_relative_zero",
            "required_clause": "For compact local domains U away from the cosmological boundary, the trace relative class restricts to zero.",
            "mathematical_form": "i_U^*[J_trace]=0 in H_rel(U,partial U) or is pure gauge/exact with zero local observable class.",
            "conditional_derivation": "if the class has no compact support on U, P_loc sees no trace charge/current",
            "current_status": "conditional_contract_available_not_parent_selected",
            "if_signed": "support(J_trace) cap U is empty/gauge-zero",
            "if_failed": "local endpoint tail remains legal",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NT890_2_exact_flux_zero",
            "required_clause": "Exact/improvement pieces have zero compact linked-surface flux and no local relative cohomology obstruction.",
            "mathematical_form": "int_{partial U} B_trace=0 and P_loc dB_trace|_U=0 for all lab/solar compact U.",
            "conditional_derivation": "Stokes kills exact pieces only after the boundary/reference class and local cycles are fixed",
            "current_status": "not_derived",
            "if_signed": "exact wording becomes a real no-tail mechanism",
            "if_failed": "exact boundary term can still carry a finite linked-surface charge",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NT890_3_multipole_nohair",
            "required_clause": "Boundary trace current has no scalar gradient, vector B_0i, trace-free/shear B_TF, radial/time, clock, WEP, or species marker hair.",
            "mathematical_form": "P_loc grad Q_trace=0; B_0i=0; B_TF=0; partial_r/time/frame Q_trace=0; partial_{Q_trace} theta_A=0.",
            "conditional_derivation": "a scalar or monopole boundary condition alone is insufficient; every local observable component must be silent",
            "current_status": "open",
            "if_signed": "PPN, clock, WEP, and orbital trace projections vanish",
            "if_failed": "finite coefficient vector must be sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NT890_4_projector_domain_lock",
            "required_clause": "The same parent-owned compact domain/projector convention is used for q_loc, boundary class, P_loc, and matter readout.",
            "mathematical_form": "Dq_loc[U][v_tr]=0 and P_loc J_trace=0 are evaluated on the same U, quotient, gauge convention, and source normalization.",
            "conditional_derivation": "prevents moving the boundary/projector convention between the theorem and the local test",
            "current_status": "not_parent_locked",
            "if_signed": "zero theorem and local arena readout use one frame",
            "if_failed": "the zero route can become a convention trick",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "NT890_5_no_tail_corollary",
            "required_clause": "NT890_0 through NT890_4 jointly hold.",
            "mathematical_form": "J_trace parent-owned + compact relative zero + exact flux zero + multipole/no-marker silence + same-domain lock.",
            "conditional_derivation": "then P_loc J_trace=0, P_loc dB_trace=0, rank(P_loc P_tr P_loc^dagger)=0, and 886 can zero-return the trace channel",
            "current_status": "conditional_theorem_valid_not_parent_signed",
            "if_signed": "trace branch can be promoted in a later checkpoint, still not full local GR by itself",
            "if_failed": "finite trace coefficient acquisition is mandatory",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def cohomology_transfer_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "CTA890_0_Jrel_success",
            "source": "231_Jrel_cohomology",
            "object": "J_rel projected memory current",
            "transfer_question": "does the shell cohomology success apply directly to J_trace",
            "audit_result": "supporting_analogy_only",
            "reason": "J_rel is current/flux-like and had ordinary mass flux explicitly separated; this gives a route shape, not a trace-current proof",
            "claim_effect": "no promotion",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CTA890_1_Cperp_failure_warning",
            "source": "273_Cperp_transfer_fail",
            "object": "scalar/representative Cperp",
            "transfer_question": "can cohomology exactness be moved to scalar or trace representatives by name",
            "audit_result": "transfer_rejected",
            "reason": "273 shows flux/current cohomology does not automatically make scalar residuals gauge or locally silent",
            "claim_effect": "blocks automatic P_loc J_trace zero",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CTA890_2_boundary_certificate_failure",
            "source": "549_boundary_certificate",
            "object": "boundary cohomology/no-hair certificate",
            "transfer_question": "has the boundary cohomology/no-hair certificate already closed",
            "audit_result": "prior_certificate_failed",
            "reason": "549 retains exact/improvement flux, vector/tensor hair, derivative hair, and projector boundary stress as unresolved",
            "claim_effect": "must keep no-tail nonclaim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CTA890_3_trace_current_specificity",
            "source": "863_trace_current;864_local_global_split",
            "object": "J_trace endpoint current",
            "transfer_question": "what extra is needed for trace current specifically",
            "audit_result": "specific_parent_signature_required",
            "reason": "J_trace must be parent-owned, FLRW-visible, locally vertical, no-tail, and matter-marker silent in one parent quotient stack",
            "claim_effect": "sets exact proof target",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "CTA890_4_verdict",
            "source": "all",
            "object": "boundary quotient no-tail route",
            "transfer_question": "can 890 sign P_loc J_trace=0 now",
            "audit_result": "not_signed_transfer_rejected",
            "reason": "old cohomology results are useful scaffolding, but the current trace boundary no-tail theorem still lacks a parent action signature",
            "claim_effect": "finite coefficient acquisition plan activates",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def local_projection_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "LPT890_0_compact_support",
            "local_test": "compact lab/R10 domain U",
            "required_zero": "support(J_trace) cap U = empty or pure gauge/exact-zero",
            "current_evidence": "contract only",
            "test_status": "not_verified",
            "failure_observable": "R10/fifth-force trace carrier",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "LPT890_1_linked_flux",
            "local_test": "linked sphere/worldtube around local source",
            "required_zero": "int_{partial U} B_trace=0 and no exact/improvement finite charge",
            "current_evidence": "prior boundary flux certificates failed",
            "test_status": "not_verified",
            "failure_observable": "GM drift, orbital/radial force, source normalization leakage",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "LPT890_2_vector_tensor_hair",
            "local_test": "weak-field solar-system exterior",
            "required_zero": "B_0i=B_TF=shear=preferred-frame trace projection=0",
            "current_evidence": "485 warns scalar local zero does not kill vector/tensor flux",
            "test_status": "not_verified",
            "failure_observable": "PPN gamma/beta/alpha1/alpha2/alpha3/xi residuals",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "LPT890_3_clock_WEP_marker",
            "local_test": "ordinary matter, clocks, EM, material species",
            "required_zero": "partial_{Q_trace} theta_A=0 and no local reduced EFT marker",
            "current_evidence": "873/889 conditional only",
            "test_status": "not_verified",
            "failure_observable": "clock drift, WEP/material charge, EM/fine-structure channel",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "LPT890_4_same_domain_lock",
            "local_test": "same U and projector convention across theorem and arena",
            "required_zero": "q_loc, P_loc, boundary class, and matter readout use one parent-owned domain convention",
            "current_evidence": "not locked",
            "test_status": "not_verified",
            "failure_observable": "apparent theorem-zero from changing representatives",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "test_id": "LPT890_5_projection_verdict",
            "local_test": "all local projection tests",
            "required_zero": "LPT890_0 through LPT890_4 pass",
            "current_evidence": "multiple open or failed certificates",
            "test_status": "fail_for_claim",
            "failure_observable": "finite trace coefficient route remains active",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def coefficient_acquisition_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "acquisition_id": "FCA890_0_Ztr",
            "quantity": "Z_tr",
            "needed_for": "kinetic normalization, ghost/no-pole decision, alpha(lambda) amplitude",
            "required_input": "positive numeric parent Hessian coefficient or zero-return certificate",
            "current_status": "MISSING_PARENT_HESSIAN",
            "first_source_target": "parent trace Hessian/action block, not observational fit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_1_lambda_tr",
            "quantity": "lambda_tr_or_m_tr",
            "needed_for": "R10/orbital finite-range profile",
            "required_input": "numeric mass/range from H_tr pole or theorem no physical pole",
            "current_status": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "first_source_target": "H_tr principal symbol/reduced inverse",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_2_Qtr_universal",
            "quantity": "Q_tr_over_m_universal",
            "needed_for": "R10/orbital common force and GM absorption audit",
            "required_input": "source projection J_tr onto ordinary matter per inertial mass or theorem zero",
            "current_status": "MISSING_SOURCE_PROJECTION",
            "first_source_target": "matter descent/no-marker theorem or source-cokernel computation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_3_Qtr_species",
            "quantity": "Delta_Q_tr_over_m_AB",
            "needed_for": "WEP/material/clock differential tests",
            "required_input": "species/material charge difference or no-marker theorem",
            "current_status": "MISSING_NO_MARKER_RESULT",
            "first_source_target": "matter constants, EM, binding energy, clock sector audit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_4_metric_response",
            "quantity": "C_T_gamma,C_T_beta,C_T_source",
            "needed_for": "PPN and Newtonian source normalization",
            "required_input": "weak-field response operator or EH/same-frame absorption theorem",
            "current_status": "MISSING_RESPONSE_OPERATOR",
            "first_source_target": "linearized metric/coframe response of finite trace branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_5_clock_response",
            "quantity": "C_T_clock",
            "needed_for": "clock/redshift/local constants tests",
            "required_input": "clock response or proof clock constants factor through q_loc",
            "current_status": "MISSING_CLOCK_RESPONSE",
            "first_source_target": "matter/EM/time sector descent audit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_6_R10_bound_curve",
            "quantity": "alpha_bound(lambda)_R10",
            "needed_for": "short-range fifth-force comparison after theory factors exist",
            "required_input": "full source-backed alpha(lambda) curve or explicitly nonclaim anchor-only rows",
            "current_status": "MISSING_FULL_CURVE_FOR_CLAIM",
            "first_source_target": "reuse existing R10 acquisition machinery only after theory row exists",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_7_arena_projection",
            "quantity": "tau_R10,tau_PPN,tau_clock_WEP,tau_orbital",
            "needed_for": "mapping c_T/Z_tr/lambda_tr/J_tr to observables",
            "required_input": "arena-dependent response maps with units and source paths",
            "current_status": "MISSING_ARENA_PROJECTION",
            "first_source_target": "runner schema, one arena at a time, no claim rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "FCA890_8_source_provenance",
            "quantity": "source_path_and_units_for_every_numeric_input",
            "needed_for": "claim hygiene and reproducibility",
            "required_input": "local path/DOI/URL, extraction method, confidence, units, valid_for_claim flag",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "first_source_target": "source register plus no MISSING markers before any comparison",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def blocker_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BL890_0_parent_trace_current",
            "blocker": "define J_trace as a parent-owned current with a support class",
            "why_it_matters": "without current ownership, no-tail is just a desired projection",
            "route_if_unsolved": "finite trace source projection rows",
            "priority": "highest_derivation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL890_1_compact_relative_zero",
            "blocker": "prove compact local restriction of the trace relative class is zero",
            "why_it_matters": "this is the direct P_loc J_trace=0 route",
            "route_if_unsolved": "R10/orbital finite range rows",
            "priority": "highest_derivation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL890_2_exact_flux_and_multipoles",
            "blocker": "prove exact flux, vector, tensor, shear, radial, time, clock, WEP, and species components vanish",
            "why_it_matters": "scalar no-tail alone is not enough for PPN/local GR",
            "route_if_unsolved": "PPN/clock/WEP/orbital coefficient vector",
            "priority": "high",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL890_3_Jrel_transfer_gap",
            "blocker": "show J_trace is the same kind of projected current object as J_rel, not a scalar/endpoint representative",
            "why_it_matters": "old cohomology theorem cannot be imported by analogy",
            "route_if_unsolved": "specific J_trace theorem or finite carrier branch",
            "priority": "high",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL890_4_finite_coefficient_rows",
            "blocker": "fill Z_tr, lambda_tr, Q_tr/m, response operators, and source-backed bound rows if no-tail remains unsigned",
            "why_it_matters": "needed for testable nonzero trace branch",
            "route_if_unsolved": "no local/R10 claim",
            "priority": "fallback_now_active",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG890_0_Ploc_Jtrace_zero",
            "promotion_target": "P_loc J_trace=0 and P_loc dB_trace=0",
            "required_to_pass": "NT890_0 through NT890_4 parent-signed",
            "current_evidence": "conditional theorem only; transfer rejected",
            "gate_result": "fail_for_claim",
            "next_action": "source/derive specific J_trace current or acquire finite coefficients",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG890_1_trace_rank_zero",
            "promotion_target": "rank(P_loc P_tr P_loc^dagger)=0",
            "required_to_pass": "P_loc J_trace zero plus same-domain q_loc/P_tr projector lock",
            "current_evidence": "not signed",
            "gate_result": "fail_for_claim",
            "next_action": "do not promote 886 zero-pole route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG890_2_finite_branch_claim",
            "promotion_target": "finite trace carrier can be tested as evidence",
            "required_to_pass": "all FCA890 rows numeric/sourced or theorem-zero with no MISSING markers",
            "current_evidence": "acquisition plan staged only",
            "gate_result": "fail_for_claim",
            "next_action": "build source-row runner in 891",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG890_3_local_GR",
            "promotion_target": "local GR/Newton derivation",
            "required_to_pass": "trace branch plus EH/source-normalization/PPN/q_loc/projector branches all closed",
            "current_evidence": "trace branch not closed",
            "gate_result": "fail_for_claim",
            "next_action": "keep local-GR gate blocked and derivation-first",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC890_0_selected",
            "route": "finite_trace_coefficient_source_row_builder_with_zero_route_watch",
            "status": "selected",
            "reason": "the no-tail theorem is now sharp but unsigned, and cohomology transfer by analogy is rejected; the honest next progress is source-row construction for the retained trace branch while watching for a real parent-current proof",
            "include": "Z_tr/lambda_tr/Q_tr/response/source provenance rows, claim guards, optional zero-route theorem input if found",
            "exclude": "R10/PPN/local-GR claim, fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG890_0_no_no_tail_claim",
            "forbidden_claim": "boundary quotient no-tail is proven",
            "status": "forbidden",
            "reason": "890 writes a conditional theorem but does not parent-sign the current/support/flux/multipole clauses",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG890_1_no_cohomology_transfer_claim",
            "forbidden_claim": "J_rel cohomology theorem automatically proves J_trace silence",
            "status": "forbidden",
            "reason": "transfer audit rejects automatic import; trace current needs its own parent signature",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG890_2_no_cT_zero",
            "forbidden_claim": "c_T=0 or trace branch has no local carrier",
            "status": "forbidden",
            "reason": "P_loc J_trace zero and rank-zero are not promoted",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG890_3_no_finite_pass",
            "forbidden_claim": "finite trace branch passes local tests",
            "status": "forbidden",
            "reason": "coefficient acquisition plan has missing parent inputs and no sourced bound rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG890_4_no_local_GR",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace branch and broader local-GR stack remain open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG890_5_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "890 creates a precise no-tail theorem target and activates finite coefficient acquisition honestly",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D890_0",
            "finding": "conditional_no_tail_theorem_written",
            "reason": "the exact clauses needed for P_loc J_trace=0 are now explicit and locally testable",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D890_1",
            "finding": "cohomology_transfer_rejected",
            "reason": "J_rel cohomology is a useful analogy but does not automatically prove trace endpoint current silence",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D890_2",
            "finding": "finite_coefficient_acquisition_plan_staged",
            "reason": "without a signed no-tail theorem, retained trace coefficients are the next testable nonclaim route",
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
            "objective": "build the first finite trace coefficient source-row runner while preserving an escape hatch for a real parent-signed no-tail theorem",
            "include": "Z_tr/lambda_tr/Q_tr response schema, source provenance, R10/PPN/clock/orbital blocker checks, no-tail theorem watch",
            "exclude": "claiming local silence, claiming local-GR/R10/PPN pass, using fitted tiny coupling, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_889_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_889_VALIDATION.csv"
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
    no_tail_rows: list[dict[str, object]],
    transfer_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    no_tail_ids = {row["theorem_id"] for row in no_tail_rows}
    transfer_results = [str(row["audit_result"]) for row in transfer_rows]
    acquisition_statuses = [str(row["current_status"]) for row in acquisition_rows]
    row_groups = [
        source_rows,
        summary_rows,
        no_tail_rows,
        transfer_rows,
        projection_rows,
        acquisition_rows,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    ]
    checks = [
        {
            "check_id": "V890_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all 890 source paths exist and needles are present",
        },
        {
            "check_id": "V890_1_prior_889_clean",
            "result": "pass" if prior_889_clean() else "fail",
            "detail": "P8_Y5_BRR545_889_VALIDATION.csv clean",
        },
        {
            "check_id": "V890_2_no_tail_theorem_complete",
            "result": "pass" if {"NT890_0_parent_current_owner", "NT890_1_compact_relative_zero", "NT890_2_exact_flux_zero", "NT890_3_multipole_nohair", "NT890_4_projector_domain_lock", "NT890_5_no_tail_corollary"}.issubset(no_tail_ids) else "fail",
            "detail": "all no-tail theorem clauses present",
        },
        {
            "check_id": "V890_3_no_tail_not_promoted",
            "result": "pass" if any(row["theorem_id"] == "NT890_5_no_tail_corollary" and row["current_status"] == "conditional_theorem_valid_not_parent_signed" for row in no_tail_rows) else "fail",
            "detail": "no-tail theorem remains conditional and unpromoted",
        },
        {
            "check_id": "V890_4_cohomology_transfer_rejected",
            "result": "pass" if "not_signed_transfer_rejected" in transfer_results and "transfer_rejected" in transfer_results else "fail",
            "detail": "J_rel analogy is not counted as J_trace proof",
        },
        {
            "check_id": "V890_5_projection_tests_block_claim",
            "result": "pass" if projection_rows and any(row["test_id"] == "LPT890_5_projection_verdict" and row["test_status"] == "fail_for_claim" for row in projection_rows) else "fail",
            "detail": "local projection tests remain unverified/fail for claim",
        },
        {
            "check_id": "V890_6_acquisition_plan_staged_missing",
            "result": "pass" if len(acquisition_rows) >= 9 and all(("MISSING" in status or "SCHEMA_READY" in status) for status in acquisition_statuses) else "fail",
            "detail": "finite trace coefficient acquisition plan staged with missing markers",
        },
        {
            "check_id": "V890_7_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V890_8_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V890_9_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V890_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V890_11_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V890_12_validation_rows_ready",
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
    no_tail_rows: list[dict[str, object]],
    transfer_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 890 - Y5/R10 Boundary-Quotient No-Tail Signature or Finite Trace Coefficient Acquisition",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the boundary/no-tail route is now a precise conditional theorem, but the proof is not signed**. The old `J_rel` cohomology result gives useful scaffolding for current/flux-like objects, but 890 rejects automatic transfer to the trace endpoint current. To claim local silence we would need a parent-owned `J_trace`, compact relative-zero support, exact zero flux, vector/tensor/shear/clock/species no-hair, and a same-domain `q_loc/P_loc` lock. Those are not present, so finite trace coefficient acquisition is staged as the next nonclaim route.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Boundary No-Tail Theorem Attempt",
        md_table(no_tail_rows),
        "",
        "## Cohomology Transfer Audit",
        md_table(transfer_rows),
        "",
        "## Local Projection Tests",
        md_table(projection_rows),
        "",
        "## Finite Trace Coefficient Acquisition Plan",
        md_table(acquisition_rows),
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
    no_tail_rows = no_tail_theorem_rows(generated_utc)
    transfer_rows = cohomology_transfer_rows(generated_utc)
    projection_rows = local_projection_test_rows(generated_utc)
    acquisition_rows = coefficient_acquisition_rows(generated_utc)
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
        no_tail_rows,
        transfer_rows,
        projection_rows,
        acquisition_rows,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    )

    outputs = {
        "P8_Y5_R10_890_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_890_BOUNDARY_NO_TAIL_THEOREM_ATTEMPT.csv": no_tail_rows,
        "P8_Y5_R10_890_COHOMOLOGY_TRANSFER_AUDIT.csv": transfer_rows,
        "P8_Y5_R10_890_LOCAL_PROJECTION_TESTS.csv": projection_rows,
        "P8_Y5_R10_890_FINITE_TRACE_COEFFICIENT_ACQUISITION_PLAN.csv": acquisition_rows,
        "P8_Y5_R10_890_BLOCKER_LEDGER.csv": blocker_rows,
        "P8_Y5_R10_890_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_890_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_890_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_890_DECISION.csv": decision_rows_,
        "P8_Y5_R10_890_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_890_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_890_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "890-Y5-R10-boundary-quotient-no-tail-signature-or-finite-trace-coefficient-acquisition.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        no_tail_rows,
        transfer_rows,
        projection_rows,
        acquisition_rows,
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
    print(f"wrote {OUT / 'P8_Y5_BRR545_890_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
