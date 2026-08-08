from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md"
SCRIPT_REL = "scripts/Y5_R10_cg_bound_source_acquisition_or_local_geometry_zero_proof.py"
STATUS = "Y5_R10_cg_zero_proof_attempt_failed_source_ready_bound_ledger_written_no_local_claim"
CLAIM_CEILING = "private_cg_zero_or_bound_input_checkpoint_only_no_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md", "immediate handoff: c_g zero not signed, bound inputs written"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_626_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv", "descent/signature attempt"),
        ("source-intake/mts_residuals/P8_Y5_R10_626_SIGNATURE_LEDGER.csv", "signature ledger"),
        ("source-intake/mts_residuals/P8_Y5_R10_626_CG_BOUND_INPUT_TEMPLATE.csv", "bound input template"),
        ("source-intake/mts_residuals/P8_Y5_R10_626_ARENA_BOUND_EQUATIONS.csv", "arena bound equations"),
        ("source-intake/mts_residuals/P8_Y5_R10_626_SMOKE_RESULTS.csv", "blocked smoke results"),
        ("625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md", "representative Weyl/disformal exclusion attempt"),
        ("624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md", "b_g runner"),
        ("623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md", "coframe factorization lemma"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "conditional coframe pullback theorem"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor attempt"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_zero_proof_rows() -> list[dict[str, object]]:
    return [
        {
            "proof_id": "ZCG627_0_parent_quotient_map",
            "zero_clause": "parent quotient map q:Phi_parent -> Q_MTS exists before matter coupling",
            "mathematical_test": "q defined and representative fibres identified for local branch",
            "current_status": "contract_only",
            "if_signed": "descent criterion has a parent domain",
            "if_unsigned": "Z_cg cannot be evaluated as a parent theorem",
            "Z_cg_support": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZCG627_1_local_verticality",
            "zero_clause": "v_X in ker(Dq) on the local matter branch",
            "mathematical_test": "Dq[v_X]=0 and vertical action is defined before variation",
            "current_status": "conditional_not_parent_signed",
            "if_signed": "representative Weyl factors become quotient-invariance violations",
            "if_unsigned": "X can remain physical local geometry data",
            "Z_cg_support": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZCG627_2_matter_action_descent",
            "zero_clause": "S_matter = Sbar_matter[q(Phi),Psi,theta]",
            "mathematical_test": "Lie_v S_matter=0 for every v in ker(Dq), up to owned gauge/boundary terms",
            "current_status": "not_parent_signed",
            "if_signed": "representative A_g(X)^2 matter frame is forbidden",
            "if_unsigned": "c_g must be source-acquired or left blocked",
            "Z_cg_support": "central_clause",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZCG627_3_measure_coframe_connection_descent",
            "zero_clause": "matter measure, coframe, connection, and derivative operator descend to Q_MTS",
            "mathematical_test": "det(e_m), e_m, omega[e_m], D[e_m] are functions of q(Phi)",
            "current_status": "not_parent_signed",
            "if_signed": "no representative c_g leakage through measure or connection",
            "if_unsigned": "c_g can re-enter through local rods/clocks geometry",
            "Z_cg_support": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZCG627_4_no_representative_coefficients",
            "zero_clause": "no fixed representative Weyl/disformal coefficients enter matter geometry",
            "mathematical_test": "A_g, B_g, U_a are Q-data, gauge/auxiliary/retained fields, or absent",
            "current_status": "not_parent_signed",
            "if_signed": "fixed c_g and disformal spurion channels close",
            "if_unsigned": "c_g and d_g_Pi_disformal acquisition rows remain required",
            "Z_cg_support": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZCG627_5_boundary_projection_silence",
            "zero_clause": "vertical boundary/exact terms have zero local projection and zero relevant flux",
            "mathematical_test": "boundary contribution to Lie_v S_matter is exact/gauge or routed to non-Hilbert residual",
            "current_status": "not_parent_signed",
            "if_signed": "descent criterion is not spoiled by edge current",
            "if_unsigned": "boundary/non-Hilbert residual remains open",
            "Z_cg_support": "necessary_not_sufficient",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZCG627_6_zero_verdict",
            "zero_clause": "Z_cg=true",
            "mathematical_test": "ZCG627_0..ZCG627_5 jointly signed",
            "current_status": "not_passed",
            "if_signed": "c_g=0 can be promoted and local geometry common-frame branch closes",
            "if_unsigned": "source-ready c_g acquisition ledger selected",
            "Z_cg_support": "false",
            "valid_for_claim": "false",
        },
    ]


def build_acquisition_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "acquisition_id": "ACQ627_0_Z_cg",
            "parameter": "Z_cg",
            "definition": "true iff the local geometry zero proof is parent-signed",
            "units": "boolean",
            "required_for": "all local geometry zero claims",
            "current_value": "false",
            "source_path": "this_checkpoint",
            "source_status": "not_signed",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_1_c_g",
            "parameter": "c_g",
            "definition": "d ln A_g/dXhat for representative Weyl common-frame coupling",
            "units": "dimensionless",
            "required_for": "R10,PPN,clock,orbital if Z_cg=false",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_status": "needed_numeric_bound_or_theorem_zero",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_2_tau_R10",
            "parameter": "tau_R10",
            "definition": "R10 material/source-test projection of stress trace/common-frame response",
            "units": "dimensionless",
            "required_for": "R10",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "source_status": "needed_projection",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_3_tau_PPN",
            "parameter": "tau_PPN",
            "definition": "PPN/local-gravity projection of common-frame response",
            "units": "dimensionless",
            "required_for": "PPN",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "source_status": "needed_projection",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_4_tau_clock",
            "parameter": "tau_clock",
            "definition": "clock/redshift/environment projection of common-frame response",
            "units": "dimensionless",
            "required_for": "clock",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "source_status": "needed_projection",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_5_tau_orbital",
            "parameter": "tau_orbital",
            "definition": "orbital/binary projection of common-frame response",
            "units": "dimensionless",
            "required_for": "orbital",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": "MISSING_ARENA_SOURCE",
            "source_status": "needed_projection",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_6_K_X",
            "parameter": "K_X",
            "definition": "local exchange/kernel factor for common-frame geometry source branch",
            "units": "schema_required",
            "required_for": "R10,PPN,orbital if exchange branch used",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_status": "needed_parent_kernel",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_7_Qbar_XH",
            "parameter": "Qbar_XH",
            "definition": "source/edge/Hamiltonian projection for X-channel coupling",
            "units": "schema_required",
            "required_for": "R10 and local source coupling",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_status": "needed_parent_projection",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_8_lambda_X",
            "parameter": "lambda_X",
            "definition": "range of local X/common-frame exchange branch",
            "units": "length",
            "required_for": "R10,PPN,orbital range suppression",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_status": "needed_parent_range",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_9_alpha_bound_lambda",
            "parameter": "alpha_bound_lambda",
            "definition": "experimental R10/Yukawa alpha_bound(lambda) curve or source-backed nonclaim anchor",
            "units": "dimensionless",
            "required_for": "R10",
            "current_value": "MISSING_ARENA_SOURCE",
            "source_path": "MISSING_ARENA_SOURCE",
            "source_status": "needed_real_bound_curve_before_R10_scoring",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ627_10_d_g_Pi_disformal",
            "parameter": "d_g_Pi_disformal",
            "definition": "combined disformal coefficient/projection stub pending fuller schema",
            "units": "dimensionless_after_schema_fix",
            "required_for": "disformal branch",
            "current_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "source_status": "stub_blocks_disformal_scoring",
            "valid_for_claim": "false",
        },
    ]


def build_arena_blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "AB627_0_R10",
            "arena": "R10 inverse-square",
            "equation": "alpha_bg(lambda)=K_X(lambda)*Qbar_XH*tau_R10*c_g",
            "required_inputs": "c_g,tau_R10,K_X,Qbar_XH,lambda_X,alpha_bound_lambda",
            "blocking_markers": "MISSING_PARENT_INPUT,MISSING_ARENA_PROJECTION,MISSING_ARENA_SOURCE",
            "current_status": "blocked",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AB627_1_PPN",
            "arena": "PPN/local gravity",
            "equation": "r_PPN_bg=M_PPN(lambda_X,profile)*tau_PPN*c_g",
            "required_inputs": "c_g,tau_PPN,lambda_X,profile,M_PPN",
            "blocking_markers": "MISSING_PARENT_INPUT,MISSING_ARENA_PROJECTION",
            "current_status": "blocked",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AB627_2_clock",
            "arena": "clock/redshift",
            "equation": "r_clock_bg=S_clock(environment)*tau_clock*c_g",
            "required_inputs": "c_g,tau_clock,environment_profile,clock_sensitivity",
            "blocking_markers": "MISSING_PARENT_INPUT,MISSING_ARENA_PROJECTION",
            "current_status": "blocked",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AB627_3_orbital",
            "arena": "orbital/binary",
            "equation": "r_orbital_bg=M_orbital(lambda_X,source_profile)*tau_orbital*c_g",
            "required_inputs": "c_g,tau_orbital,lambda_X,source_profile,orbital_projection",
            "blocking_markers": "MISSING_PARENT_INPUT,MISSING_ARENA_PROJECTION",
            "current_status": "blocked",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AB627_4_disformal",
            "arena": "disformal extension",
            "equation": "b_g_disformal=d_g_Pi_disformal",
            "required_inputs": "d_g_Pi_disformal plus arena-specific projection schema",
            "blocking_markers": "MISSING_PARENT_INPUT",
            "current_status": "blocked_stub",
            "claim_allowed": "false",
        },
    ]


def build_source_requirement_rows() -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "SRC627_0_zero_proof_source",
            "source_type": "parent theorem",
            "needed_item": "quotient-invariant matter action proof",
            "minimum_acceptance": "local path proving q, v_X verticality, matter descent, measure/coframe/connection descent, no representative coefficients, and boundary projection silence",
            "claim_effect_if_found": "Z_cg=true possible",
            "status": "missing",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "SRC627_1_cg_bound_source",
            "source_type": "parent coefficient or empirical bound",
            "needed_item": "numeric or theorem-zero c_g",
            "minimum_acceptance": "finite signed dimensionless value or zero theorem with existing source_path",
            "claim_effect_if_found": "allows arena-specific blocker checks, not automatic pass",
            "status": "missing",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "SRC627_2_arena_projection_source",
            "source_type": "arena projection",
            "needed_item": "tau_R10, tau_PPN, tau_clock, tau_orbital",
            "minimum_acceptance": "dimensionless projection definitions with source paths and no MISSING markers",
            "claim_effect_if_found": "allows arena equations to be evaluated",
            "status": "missing",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "SRC627_3_kernel_source",
            "source_type": "parent/local kernel",
            "needed_item": "K_X, Qbar_XH, lambda_X",
            "minimum_acceptance": "units and source-backed values or theorem-zero rows",
            "claim_effect_if_found": "allows local exchange/range scoring",
            "status": "missing",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "SRC627_4_R10_bound_source",
            "source_type": "experimental bound",
            "needed_item": "alpha_bound_lambda",
            "minimum_acceptance": "real curve/table or explicitly nonclaim source-backed anchor rows",
            "claim_effect_if_found": "allows R10 comparison only if all other inputs are sourced",
            "status": "missing",
            "valid_for_claim": "false",
        },
    ]


def build_smoke_rows(acquisition_rows: list[dict[str, object]], arena_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in acquisition_rows:
        missing = has_missing_marker(row)
        rows.append(
            {
                "smoke_id": "SMK_" + str(row["acquisition_id"]),
                "object_type": "acquisition_input",
                "object_id": row["acquisition_id"],
                "missing_marker_present": str(missing).lower(),
                "runner_result": "blocked_missing_source_or_value" if missing else "nonclaim_zero_or_checkpoint_row",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    for row in arena_rows:
        rows.append(
            {
                "smoke_id": "SMK_" + str(row["arena_id"]),
                "object_type": "arena_blocker",
                "object_id": row["arena_id"],
                "missing_marker_present": "true",
                "runner_result": row["current_status"],
                "claim_allowed": row["claim_allowed"],
                "valid_for_claim": "false",
            }
        )
    return rows


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D627_0_main_verdict",
            "status": STATUS,
            "decision": "local geometry zero proof does not close",
            "meaning": "Z_cg remains false because parent quotient, verticality, matter descent, coefficient exclusion, and boundary clauses are unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D627_1_acquisition_ledger",
            "status": "source_ready_cg_acquisition_ledger_written",
            "decision": "write source-ready bound ledger for c_g and arena projections",
            "meaning": "next implementation can source real inputs without guessing schema",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D627_2_next_route",
            "status": "real_bound_input_sources_next",
            "decision": "next target is real local bound input sources or a stronger Z_cg proof",
            "meaning": "the local branch is ready for source acquisition, but still not for claims",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D627_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no local test pass",
            "meaning": "all R10/WEP/PPN/clock/orbital/local-GR claims remain blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU627_0_allowed",
            "allowed_after_627": "cite Z_cg=false and the exact unsigned zero-proof clauses",
            "forbidden_after_627": "promote c_g=0 or local GR from the descent criterion alone",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU627_1_allowed",
            "allowed_after_627": "source c_g, tau_A, K_X, Qbar_XH, lambda_X, and alpha_bound_lambda one by one",
            "forbidden_after_627": "score any local arena while acquisition rows contain MISSING markers",
            "next_action": "acquire real bound/source rows or prove Z_cg=true",
        },
        {
            "route_id": "RU627_2_allowed",
            "allowed_after_627": "keep disformal branch as a blocked stub until c_g is resolved",
            "forbidden_after_627": "hide disformal leakage inside conformal c_g scoring",
            "next_action": "defer disformal expansion unless c_g source path forces it",
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "zero_proof_attempted": "true",
            "Z_cg": "false",
            "c_g_zero_promoted": "false",
            "acquisition_ledger_written": "true",
            "bound_inputs_sourced": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "clock_pass": "false",
            "orbital_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    source_requirement_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_626_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]

    required_zero_ids = {
        "ZCG627_0_parent_quotient_map",
        "ZCG627_1_local_verticality",
        "ZCG627_2_matter_action_descent",
        "ZCG627_3_measure_coframe_connection_descent",
        "ZCG627_4_no_representative_coefficients",
        "ZCG627_5_boundary_projection_silence",
        "ZCG627_6_zero_verdict",
    }
    zero_ids = {row["proof_id"] for row in zero_rows}
    zero_audit_complete = required_zero_ids.issubset(zero_ids)
    zero_not_passed = any(row["proof_id"] == "ZCG627_6_zero_verdict" and row["current_status"] == "not_passed" for row in zero_rows)

    required_params = {"Z_cg", "c_g", "tau_R10", "tau_PPN", "tau_clock", "tau_orbital", "K_X", "Qbar_XH", "lambda_X", "alpha_bound_lambda"}
    acquisition_params = {row["parameter"] for row in acquisition_rows}
    acquisition_complete = required_params.issubset(acquisition_params)
    acquisition_safe = acquisition_complete and all(not parse_bool(row["valid_for_claim"]) for row in acquisition_rows) and any(has_missing_marker(row) for row in acquisition_rows)
    arenas_blocked = all(row["claim_allowed"] == "false" and str(row["current_status"]).startswith("blocked") for row in arena_rows)
    source_requirements_safe = all(not parse_bool(row["valid_for_claim"]) and row["status"] == "missing" for row in source_requirement_rows)
    smoke_blocks = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in smoke_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in zero_rows + acquisition_rows + source_requirement_rows + smoke_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V627_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V627_1_prior_626_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V627_2_zero_proof_audit_complete_not_passed",
            "result": "pass" if zero_audit_complete and zero_not_passed else "fail",
            "detail": f"zero_audit_complete={zero_audit_complete};zero_not_passed={zero_not_passed}",
        },
        {
            "check_id": "V627_3_acquisition_ledger_complete_safe",
            "result": "pass" if acquisition_safe else "fail",
            "detail": f"params={','.join(sorted(acquisition_params))};safe={acquisition_safe}",
        },
        {
            "check_id": "V627_4_arenas_blocked",
            "result": "pass" if arenas_blocked else "fail",
            "detail": f"arena_rows={len(arena_rows)};arenas_blocked={arenas_blocked}",
        },
        {
            "check_id": "V627_5_source_requirements_missing_nonclaim",
            "result": "pass" if source_requirements_safe else "fail",
            "detail": f"source_requirement_rows={len(source_requirement_rows)};safe={source_requirements_safe}",
        },
        {
            "check_id": "V627_6_smoke_blocks_claims",
            "result": "pass" if smoke_blocks else "fail",
            "detail": f"smoke_rows={len(smoke_rows)};blocks={smoke_blocks}",
        },
        {
            "check_id": "V627_7_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V627_8_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["clock_pass"] == "false"
            and nonclaim["orbital_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["c_g_zero_promoted"] == "false"
            else "fail",
            "detail": "c_g_zero=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def write_doc(
    source_register: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    source_requirement_rows: list[dict[str, object]],
    smoke_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 627 Y5 R10 c_g bound source acquisition or local geometry zero proof

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- 627 tries the local geometry zero proof first.
- The proof does not close: the parent quotient map, local `X` verticality, matter action descent, measure/coframe/connection descent, no representative coefficients, and boundary projection silence are not jointly parent-signed.
- Therefore `Z_cg=false` and `c_g=0` is not promoted.
- The fallback is now source-ready: the acquisition ledger names every input needed before R10, PPN, clock, or orbital scoring can even start.

## Zero-Proof Target

```text
Z_cg=true only if:
q: Phi_parent -> Q_MTS is parent-owned
v_X in ker(Dq)
S_matter = Sbar_matter[q(Phi),Psi,theta]
det(e_m), e_m, omega[e_m], D[e_m] descend to Q_MTS
no fixed representative Weyl/disformal coefficient enters matter geometry
boundary/exact vertical terms have zero local projection
```

Current result:

```text
Z_cg=false
c_g=0 not promoted
```

## Source Register
{md_table(source_register)}

## Zero-Proof Audit
{md_table(zero_rows)}

## c_g Acquisition Ledger
{md_table(acquisition_rows)}

## Arena Blocker Matrix
{md_table(arena_rows)}

## Source Requirements
{md_table(source_requirement_rows)}

## Smoke Results
{md_table(smoke_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is the right handoff to data without surrendering derivation discipline. If a future parent proof signs `Z_cg=true`, the common-frame branch collapses cleanly. If not, the next checkpoint must acquire real source-backed values or bounds for `c_g`, `tau_R10`, `tau_PPN`, `tau_clock`, `tau_orbital`, `K_X`, `Qbar_XH`, `lambda_X`, and the R10 bound curve before any local claim is allowed.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    zero_rows = build_zero_proof_rows()
    acquisition_rows = build_acquisition_ledger_rows()
    arena_rows = build_arena_blocker_rows()
    source_requirement_rows = build_source_requirement_rows()
    smoke_rows = build_smoke_rows(acquisition_rows, arena_rows)
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        zero_rows,
        acquisition_rows,
        arena_rows,
        source_requirement_rows,
        smoke_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_627_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_627_ZERO_PROOF_AUDIT.csv", zero_rows),
        ("P8_Y5_R10_627_CG_ACQUISITION_LEDGER.csv", acquisition_rows),
        ("P8_Y5_R10_627_ARENA_BLOCKER_MATRIX.csv", arena_rows),
        ("P8_Y5_R10_627_SOURCE_REQUIREMENTS.csv", source_requirement_rows),
        ("P8_Y5_R10_627_SMOKE_RESULTS.csv", smoke_rows),
        ("P8_Y5_BRR545_627_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_627_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_627_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_627_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        zero_rows,
        acquisition_rows,
        arena_rows,
        source_requirement_rows,
        smoke_rows,
        decision_rows,
        route_rows,
        nonclaim_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
