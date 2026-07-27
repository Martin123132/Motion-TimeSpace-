from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md"
SCRIPT_REL = "scripts/Y5_R10_parent_matter_sector_contract_or_residual_prior_runner.py"
STATUS = "Y5_R10_parent_matter_sector_contract_written_residual_prior_runner_blocks_all_local_claims"
CLAIM_CEILING = "private_contract_and_smoke_runner_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md"


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
        ("621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md", "immediate handoff: normal form contract not parent-derived"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_621_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_621_NORMAL_FORM_THEOREM_ATTEMPT.csv", "621 normal-form theorem clauses"),
        ("source-intake/mts_residuals/P8_Y5_R10_621_PARENT_CLAUSE_LEDGER.csv", "621 parent clause obligations"),
        ("source-intake/mts_residuals/P8_Y5_R10_621_COMPONENT_STATUS_MATRIX.csv", "621 residual component status"),
        ("source-intake/mts_residuals/P8_Y5_R10_621_COEFFICIENT_PRIOR_TEMPLATE.csv", "621 coefficient prior template"),
        ("source-intake/mts_residuals/P8_Y5_R10_621_ARENA_PRIOR_SCHEMA.csv", "621 arena prior schema"),
        ("620-Y5-R10-qbarXT-residual-envelope-after-no-marker-failure.md", "on-shell residual vector derivation"),
        ("619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md", "no-marker failure and residual routing"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "selector theorem conditional source"),
        ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "constant/source current source"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "coframe pullback source"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_parent_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "PMC622_0_parent_split",
            "contract_clause": "S_parent[Phi,Psi]=S_MTS[Phi]+sum_A S_A[Psi_A,e_obs(q(Phi)),theta_A]+S_constraints",
            "required_owner": "parent action",
            "what_it_would_prove": "ordinary matter is coupled through the observed MTS geometry and representation labels only",
            "current_status": "contract_written_not_signed",
            "zero_if_signed": "organizes route to qbarXT_vec zero",
            "fallback_if_unsigned": "use residual prior runner",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_1_domain_covariance",
            "contract_clause": "ordinary matter fields are local covariant/Lorentz representations over the observed coframe bundle",
            "required_owner": "parent matter category",
            "what_it_would_prove": "defines allowed matter functors before adding markers",
            "current_status": "admissible_but_not_parent_constructed",
            "zero_if_signed": "supports all later normal-form clauses",
            "fallback_if_unsigned": "extra structures remain legal",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_2_unique_observed_geometry",
            "contract_clause": "there is a unique matter-visible geometry functor Obs_e:Q_MTS->coframe and dq(v_X)=0 implies Lie_vX(e_obs)=0",
            "required_owner": "parent quotient/functor theorem",
            "what_it_would_prove": "no common metric/coframe X mode",
            "current_status": "not_signed",
            "zero_if_signed": "b_g=0",
            "fallback_if_unsigned": "common_frame_log_derivative prior",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_3_marker_taxonomy",
            "contract_clause": "every matter-visible marker is absent, pure gauge, source-independent auxiliary, or retained as a real field",
            "required_owner": "parent variation and gauge taxonomy",
            "what_it_would_prove": "no hidden material marker can be zeroed without classification",
            "current_status": "not_signed",
            "zero_if_signed": "b_m=0 only for absent/gauge/auxiliary cases",
            "fallback_if_unsigned": "marker_coupling_projection prior",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_4_constant_superselection",
            "contract_clause": "theta_A are selector-trivial representation/superselection labels with Lie_vX(theta_A)=0",
            "required_owner": "parent representation theorem",
            "what_it_would_prove": "ordinary constants do not source the local X branch",
            "current_status": "not_signed",
            "zero_if_signed": "b_theta=0",
            "fallback_if_unsigned": "alpha_EM and mass-ratio derivative priors",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_5_universal_source",
            "contract_clause": "one Hilbert/coframe source current and one universal kappa source all ordinary matter",
            "required_owner": "parent Ward/Noether identity",
            "what_it_would_prove": "no species-weighted source charge",
            "current_status": "not_signed",
            "zero_if_signed": "b_kappa=0",
            "fallback_if_unsigned": "species_source_weight_splitting prior",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_6_nonHilbert_current",
            "contract_clause": "non-Hilbert local currents are absent, exact, zero-flux, or separately retained",
            "required_owner": "parent current decomposition plus boundary certificate",
            "what_it_would_prove": "spin/torsion/topological current cannot be hidden in qbarXT",
            "current_status": "not_signed",
            "zero_if_signed": "b_NH=0 where absent/exact/zero-flux",
            "fallback_if_unsigned": "nonHilbert_current_projection prior",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_7_branch_purity",
            "contract_clause": "post-readout EFT counterterms are absent from the parent-derived branch",
            "required_owner": "private branch policy until parent derivation exists",
            "what_it_would_prove": "phenomenological patches cannot count as parent theory evidence",
            "current_status": "policy_signed_not_positive_zero_theorem",
            "zero_if_signed": "b_EFT excluded from parent-branch scoring",
            "fallback_if_unsigned": "phenomenology-only branch",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PMC622_8_contract_verdict",
            "contract_clause": "PMC622_0..PMC622_7 jointly sign the parent matter sector",
            "required_owner": "full parent action",
            "what_it_would_prove": "qbarXT_vec ordinary-matter source zero before edge/range gates",
            "current_status": "not_signed",
            "zero_if_signed": "qbarXT_vec=0 for this matter branch",
            "fallback_if_unsigned": "residual prior runner remains active",
            "valid_for_claim": "false",
        },
    ]


def build_contract_to_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "map_id": "MAP622_0_geometry",
            "contract_clause": "PMC622_2_unique_observed_geometry",
            "component": "b_g",
            "fallback_prior": "common_frame_log_derivative",
            "smoke_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocked_until_derive_zero_or_numeric_bound",
            "first_derivation_target": "unique observed coframe functor",
        },
        {
            "map_id": "MAP622_1_constants_alpha",
            "contract_clause": "PMC622_4_constant_superselection",
            "component": "b_theta",
            "fallback_prior": "d_ln_alpha_EM_dXhat",
            "smoke_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocked_until_derive_zero_or_numeric_bound",
            "first_derivation_target": "constant superselection or EM charge normal form",
        },
        {
            "map_id": "MAP622_2_constants_mass",
            "contract_clause": "PMC622_4_constant_superselection",
            "component": "b_theta",
            "fallback_prior": "d_ln_mass_ratio_dXhat",
            "smoke_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocked_until_derive_zero_or_numeric_bound",
            "first_derivation_target": "mass-ratio representation theorem",
        },
        {
            "map_id": "MAP622_3_marker",
            "contract_clause": "PMC622_3_marker_taxonomy",
            "component": "b_m",
            "fallback_prior": "marker_coupling_projection",
            "smoke_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocked_until_marker_classified_or_bound",
            "first_derivation_target": "marker classifier",
        },
        {
            "map_id": "MAP622_4_source_weight",
            "contract_clause": "PMC622_5_universal_source",
            "component": "b_kappa",
            "fallback_prior": "species_source_weight_splitting",
            "smoke_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocked_until_universal_source_or_bound",
            "first_derivation_target": "universal source current",
        },
        {
            "map_id": "MAP622_5_nonHilbert",
            "contract_clause": "PMC622_6_nonHilbert_current",
            "component": "b_NH",
            "fallback_prior": "nonHilbert_current_projection",
            "smoke_value": "MISSING_PARENT_INPUT",
            "claim_gate": "blocked_until_current_decomposition_or_bound",
            "first_derivation_target": "local current decomposition",
        },
        {
            "map_id": "MAP622_6_EFT",
            "contract_clause": "PMC622_7_branch_purity",
            "component": "b_EFT",
            "fallback_prior": "post_readout_counterterm_projection",
            "smoke_value": "absent_from_parent_branch",
            "claim_gate": "not_used_for_positive_theorem_claim",
            "first_derivation_target": "none; keep absent unless parent-derived",
        },
    ]


def build_runner_schema_rows() -> list[dict[str, object]]:
    return [
        {
            "schema_field": "parameter",
            "required": "true",
            "allowed_values": "common_frame_log_derivative,d_ln_alpha_EM_dXhat,d_ln_mass_ratio_dXhat,marker_coupling_projection,species_source_weight_splitting,nonHilbert_current_projection,post_readout_counterterm_projection,P_A_qbarXT_vec",
            "claim_rule": "must match a known prior parameter",
        },
        {
            "schema_field": "component",
            "required": "true",
            "allowed_values": "b_g,b_theta,b_m,b_kappa,b_NH,b_EFT,qbarXT_vec",
            "claim_rule": "must map to a known residual component",
        },
        {
            "schema_field": "status",
            "required": "true",
            "allowed_values": "derive_zero,numeric_bound,symbolic_placeholder,absent_from_parent_branch,phenomenology_only",
            "claim_rule": "claim-ready only for derive_zero or numeric_bound with source_path and no MISSING markers",
        },
        {
            "schema_field": "value",
            "required": "true",
            "allowed_values": "0 for derive_zero; finite numeric for numeric_bound; MISSING_PARENT_INPUT for placeholder; absent_from_parent_branch for branch exclusion",
            "claim_rule": "MISSING_PARENT_INPUT blocks every arena claim",
        },
        {
            "schema_field": "units",
            "required": "true",
            "allowed_values": "dimensionless unless a later schema explicitly introduces units",
            "claim_rule": "units must be recognized before numeric scoring",
        },
        {
            "schema_field": "source_path",
            "required": "true",
            "allowed_values": "local source path for theorem/numeric bound, N/A only for absent_from_parent_branch",
            "claim_rule": "source path must exist for claim-ready theorem or numeric row",
        },
        {
            "schema_field": "valid_for_claim",
            "required": "true",
            "allowed_values": "false until all schema and arena gates pass",
            "claim_rule": "runner never promotes valid_for_claim from placeholders",
        },
    ]


def build_smoke_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "prior_id": "SP622_0_common_frame",
            "parameter": "common_frame_log_derivative",
            "component": "b_g",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_1_alpha_EM",
            "parameter": "d_ln_alpha_EM_dXhat",
            "component": "b_theta",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_2_mass_ratio",
            "parameter": "d_ln_mass_ratio_dXhat",
            "component": "b_theta",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_3_marker",
            "parameter": "marker_coupling_projection",
            "component": "b_m",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_4_source_weight",
            "parameter": "species_source_weight_splitting",
            "component": "b_kappa",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_5_nonHilbert",
            "parameter": "nonHilbert_current_projection",
            "component": "b_NH",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_6_EFT",
            "parameter": "post_readout_counterterm_projection",
            "component": "b_EFT",
            "status": "absent_from_parent_branch",
            "value": "absent_from_parent_branch",
            "units": "dimensionless",
            "source_path": "N/A",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "SP622_7_projection",
            "parameter": "P_A_qbarXT_vec",
            "component": "qbarXT_vec",
            "status": "symbolic_placeholder",
            "value": "MISSING_PARENT_INPUT",
            "units": "dimensionless",
            "source_path": "MISSING_PARENT_SOURCE",
            "valid_for_claim": "false",
        },
    ]


def row_has_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def build_smoke_result_rows(smoke_prior_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    results = []
    for row in smoke_prior_rows:
        status = str(row["status"])
        missing = row_has_missing_marker(row)
        if status == "absent_from_parent_branch":
            runner_result = "accepted_as_branch_exclusion_nonclaim"
            blocks_claim = "false_for_EFT_only"
            reason = "branch purity keeps post-readout EFT out of parent-derived scoring"
        elif missing:
            runner_result = "blocked_missing_parent_input"
            blocks_claim = "true"
            reason = "placeholder value or source path present"
        else:
            runner_result = "not_claim_ready_in_smoke"
            blocks_claim = "true"
            reason = "smoke runner does not promote claim rows"
        results.append(
            {
                "prior_id": row["prior_id"],
                "parameter": row["parameter"],
                "component": row["component"],
                "status": status,
                "missing_marker_present": str(missing).lower(),
                "runner_result": runner_result,
                "blocks_claim": blocks_claim,
                "reason": reason,
                "valid_for_claim": "false",
            }
        )
    return results


def build_arena_result_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "AR622_0_R10",
            "arena": "R10 inverse-square",
            "required_inputs": "K_X,Qbar_XH,lambda_X,P_R10,common_frame,marker,source_weight,nonHilbert,bound_curve",
            "smoke_runner_status": "blocked",
            "block_reason": "parent residual priors and K/Q/lambda inputs are placeholders",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AR622_1_WEP",
            "arena": "WEP/composition",
            "required_inputs": "mass-ratio derivatives, marker projection, source-weight splitting, composition charges",
            "smoke_runner_status": "blocked",
            "block_reason": "component priors and composition projection are placeholders",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AR622_2_PPN",
            "arena": "PPN/local gravity",
            "required_inputs": "common-frame coupling, range suppression, PPN projection matrix",
            "smoke_runner_status": "blocked",
            "block_reason": "geometry functor and range/projection inputs are not sourced",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AR622_3_clocks_EM",
            "arena": "clocks/EM/fine structure",
            "required_inputs": "alpha_EM derivative, mass-ratio derivative, clock sensitivity matrix, environment profile",
            "smoke_runner_status": "blocked",
            "block_reason": "constant-sector priors are placeholders",
            "claim_allowed": "false",
        },
        {
            "arena_id": "AR622_4_orbital",
            "arena": "orbital/binary",
            "required_inputs": "common-frame coupling, source-weight splitting, non-Hilbert current, range/radiation channel",
            "smoke_runner_status": "blocked",
            "block_reason": "local matter and range/radiation inputs are placeholders",
            "claim_allowed": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D622_0_main_verdict",
            "status": STATUS,
            "decision": "parent matter-sector contract written; not signed by parent derivation",
            "meaning": "the clean local matter route now has exact clauses, but the residual-prior runner remains active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D622_1_runner",
            "status": "smoke_runner_blocks_placeholders",
            "decision": "runner blocks every local arena while MISSING_PARENT_INPUT rows remain",
            "meaning": "no R10/WEP/PPN/clock/orbital scoring can be treated as evidence yet",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D622_2_best_next_derivation",
            "status": "geometry_functor_first",
            "decision": "attack unique observed coframe functor first",
            "meaning": "b_g touches R10, PPN, clocks, and orbital arenas, so it is the highest-leverage first clause",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D622_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no local-gravity claim",
            "meaning": "contract and runner only; all claim flags remain false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU622_0_allowed",
            "allowed_after_622": "use the parent matter contract as the required signature checklist",
            "forbidden_after_622": "treat the checklist as already signed",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU622_1_allowed",
            "allowed_after_622": "run residual-prior smoke rows to verify blockers",
            "forbidden_after_622": "score local tests with MISSING_PARENT_INPUT priors",
            "next_action": "derive or source one prior at a time",
        },
        {
            "route_id": "RU622_2_allowed",
            "allowed_after_622": "attack b_g first via unique observed coframe functor",
            "forbidden_after_622": "jump to broad local-GR claims before b_g/geometry ownership",
            "next_action": NEXT_TARGET,
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "parent_contract_written": "true",
            "parent_contract_signed": "false",
            "residual_prior_runner_written": "true",
            "runner_blocks_placeholders": "true",
            "b_g_zero_promoted": "false",
            "b_theta_zero_promoted": "false",
            "b_m_zero_promoted": "false",
            "b_kappa_zero_promoted": "false",
            "b_NH_zero_promoted": "false",
            "qbarXT_vec_zero_promoted": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    smoke_prior_rows: list[dict[str, object]],
    smoke_result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_621_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]
    contract_ids = {row["contract_id"] for row in contract_rows}
    required_contracts = {
        "PMC622_2_unique_observed_geometry",
        "PMC622_3_marker_taxonomy",
        "PMC622_4_constant_superselection",
        "PMC622_5_universal_source",
        "PMC622_6_nonHilbert_current",
        "PMC622_7_branch_purity",
        "PMC622_8_contract_verdict",
    }
    contract_complete = required_contracts.issubset(contract_ids)
    contract_not_signed = any(row["contract_id"] == "PMC622_8_contract_verdict" and row["current_status"] == "not_signed" for row in contract_rows)
    map_complete = len(map_rows) >= 7 and all(row["fallback_prior"] for row in map_rows)
    schema_fields = {row["schema_field"] for row in schema_rows}
    required_schema_fields = {"parameter", "component", "status", "value", "units", "source_path", "valid_for_claim"}
    schema_complete = required_schema_fields.issubset(schema_fields)
    smoke_has_missing = any(row_has_missing_marker(row) for row in smoke_prior_rows)
    smoke_nonclaim = all(not parse_bool(row["valid_for_claim"]) for row in smoke_prior_rows)
    runner_blocks = all(row["valid_for_claim"] == "false" for row in smoke_result_rows) and any(row["runner_result"] == "blocked_missing_parent_input" for row in smoke_result_rows)
    arenas_blocked = all(row["smoke_runner_status"] == "blocked" and row["claim_allowed"] == "false" for row in arena_rows)
    all_nonclaim = all(
        not parse_bool(row.get("valid_for_claim", "false"))
        for row in contract_rows + smoke_prior_rows + smoke_result_rows + decision_rows
    )
    nonclaim = nonclaim_rows[0]

    return [
        {
            "check_id": "V622_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V622_1_prior_621_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V622_2_contract_complete_not_signed",
            "result": "pass" if contract_complete and contract_not_signed else "fail",
            "detail": f"contract_complete={contract_complete};contract_not_signed={contract_not_signed}",
        },
        {
            "check_id": "V622_3_contract_to_prior_map_complete",
            "result": "pass" if map_complete else "fail",
            "detail": f"map_rows={len(map_rows)}",
        },
        {
            "check_id": "V622_4_runner_schema_complete",
            "result": "pass" if schema_complete else "fail",
            "detail": f"schema_fields={','.join(sorted(schema_fields))}",
        },
        {
            "check_id": "V622_5_smoke_priors_nonclaim_with_missing",
            "result": "pass" if smoke_has_missing and smoke_nonclaim else "fail",
            "detail": f"smoke_has_missing={smoke_has_missing};smoke_nonclaim={smoke_nonclaim}",
        },
        {
            "check_id": "V622_6_runner_blocks_placeholders",
            "result": "pass" if runner_blocks else "fail",
            "detail": f"runner_blocks={runner_blocks}",
        },
        {
            "check_id": "V622_7_arenas_blocked",
            "result": "pass" if arenas_blocked else "fail",
            "detail": f"arena_rows={len(arena_rows)};all_blocked={arenas_blocked}",
        },
        {
            "check_id": "V622_8_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V622_9_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["qbarXT_vec_zero_promoted"] == "false"
            else "fail",
            "detail": "qbarXT_vec_zero=false;R10=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_doc(
    source_register: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    map_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    smoke_prior_rows: list[dict[str, object]],
    smoke_result_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 622 Y5 R10 parent matter sector contract or residual prior runner

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- 622 writes the exact parent matter-sector contract needed to turn the 621 normal form into a real derivation.
- The contract is not signed by the current parent action. Only the branch-purity rule for post-readout EFT is accepted as private policy, and that is not positive evidence for local GR.
- The residual-prior smoke runner is now in place and it correctly blocks all local-test claims while `MISSING_PARENT_INPUT` rows remain.
- Highest-leverage next target is `b_g`: prove a unique observed coframe/metric functor, or fill the common-frame prior. That one touches R10, PPN, clocks, and orbital tests, so it is the next clean punch.

## Parent Matter-Sector Contract
The desired parent branch has the schematic form:

```text
S_parent[Phi,Psi] =
  S_MTS[Phi]
  + sum_A S_A[Psi_A, e_obs(q(Phi)), theta_A]
  + S_constraints
```

with no extra matter-visible geometry, no unclassified marker, no selector-dependent constants, no species-weighted source current, no independent non-Hilbert local current, and no post-readout EFT counterterm. If the parent action signs all of that, the ordinary-matter part of `qbarXT_vec` can be zeroed. Until then, the runner treats each unsigned clause as a prior slot.

## Source Register
{md_table(source_register)}

## Contract Clauses
{md_table(contract_rows)}

## Contract To Prior Map
{md_table(map_rows)}

## Runner Schema
{md_table(schema_rows)}

## Smoke Prior Rows
{md_table(smoke_prior_rows)}

## Smoke Runner Results
{md_table(smoke_result_rows)}

## Arena Smoke Results
{md_table(arena_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is the right kind of annoying. We now have a contract a future parent action must satisfy, and a runner that refuses to let placeholders cosplay as evidence. The next move is to try deriving the geometry clause first: unique observed coframe/metric functor, or `b_g` becomes the first real prior to fill.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    contract_rows = build_parent_contract_rows()
    map_rows = build_contract_to_prior_rows()
    schema_rows = build_runner_schema_rows()
    smoke_prior_rows = build_smoke_prior_rows()
    smoke_result_rows = build_smoke_result_rows(smoke_prior_rows)
    arena_rows = build_arena_result_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        contract_rows,
        map_rows,
        schema_rows,
        smoke_prior_rows,
        smoke_result_rows,
        arena_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_622_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv", contract_rows),
        ("P8_Y5_R10_622_CONTRACT_TO_PRIOR_MAP.csv", map_rows),
        ("P8_Y5_R10_622_RESIDUAL_PRIOR_RUNNER_SCHEMA.csv", schema_rows),
        ("P8_Y5_R10_622_SMOKE_PRIOR_ROWS.csv", smoke_prior_rows),
        ("P8_Y5_R10_622_PRIOR_RUNNER_SMOKE_RESULTS.csv", smoke_result_rows),
        ("P8_Y5_R10_622_ARENA_SMOKE_RESULTS.csv", arena_rows),
        ("P8_Y5_BRR545_622_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_622_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_622_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_622_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        contract_rows,
        map_rows,
        schema_rows,
        smoke_prior_rows,
        smoke_result_rows,
        arena_rows,
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
