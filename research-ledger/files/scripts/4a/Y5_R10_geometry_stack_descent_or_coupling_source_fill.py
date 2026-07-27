from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md"
NEXT_TARGET = "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md"
STATUS = "Y5_R10_762_geometry_stack_descent_contract_written_not_parent_signed_coupling_source_fill_schema_retained"
CLAIM_CEILING = "geometry_stack_descent_contract_only_no_quotient_descent_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

COUPLING_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_COUPLING_DESCENT_INPUT_CANDIDATE.csv"
CG_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_CG_COUPLING_BOUND_INPUT_CANDIDATE.csv"
EM_INTERFACE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_EM_CHARGE_INTERFACE_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_762_SOURCE_REGISTER.csv"
GEOMETRY_STACK_PATH = RESIDUALS / "P8_Y5_R10_762_GEOMETRY_STACK_DESCENT_CONTRACT.csv"
CHAIN_RULE_PATH = RESIDUALS / "P8_Y5_R10_762_GEOMETRY_STACK_CHAIN_RULE_AUDIT.csv"
COUNTEREXAMPLE_PATH = RESIDUALS / "P8_Y5_R10_762_GEOMETRY_STACK_COUNTEREXAMPLE_LEDGER.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_762_COUPLING_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_762_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_762_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_762_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_762_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "761_doc": {
        "path": POST_CHECKPOINT / "761-Y5-R10-parent-matter-domain-vertical-action-or-coupling-source-fill.md",
        "needles": [
            "Current result: **the best route is the parent matter-domain vertical-action contract, but it is not parent-signed yet**",
            "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        ],
        "role": "immediate 762 handoff",
    },
    "761_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_761_VALIDATION.csv",
        "needles": ["V761_15_validation_rows_ready", "V761_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "761_evaluability": {
        "path": RESIDUALS / "P8_Y5_R10_761_LIEV_SMATTER_EVALUABILITY_AUDIT.csv",
        "needles": ["LEV761_0_fixed_Psi_chain_rule", "geometry stack descent and boundary silence still required"],
        "role": "chain-rule handoff to geometry stack",
    },
    "760_gate": {
        "path": RESIDUALS / "P8_Y5_R10_760_DESCENT_SIGNATURE_GATE.csv",
        "needles": ["DSG760_3_geometry_stack_descent", "not_signed"],
        "role": "geometry stack descent gate",
    },
    "626_signature_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
        "needles": ["QIM626_2_measure_and_connection_descent", "A_g(X) can still enter through measure or connection"],
        "role": "prior measure/connection descent blocker",
    },
    "624_doc": {
        "path": POST_CHECKPOINT / "624-Y5-R10-observed-coframe-factorization-parent-signature-or-bg-runner.md",
        "needles": ["SIG624_2_matter_geometry_factorization", "not_signed"],
        "role": "coframe factorization parent signature",
    },
    "623_doc": {
        "path": POST_CHECKPOINT / "623-Y5-R10-unique-observed-coframe-functor-or-bg-prior-fill.md",
        "needles": ["OCF623_0_factorization_lemma", "factorization_not_signed"],
        "role": "coframe factorization lemma",
    },
    "565_doc": {
        "path": POST_CHECKPOINT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
        "needles": ["CT565_1_matter_factorization_certificate", "not_parent_derived"],
        "role": "conditional coframe pullback certificate",
    },
    "622_contract": {
        "path": RESIDUALS / "P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
        "needles": ["PMC622_2_unique_observed_geometry", "common_frame_log_derivative prior"],
        "role": "parent matter-sector geometry contract",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def geometry_stack_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "GSD762_0_stack_definition",
            "stack_clause": "Declare the whole matter geometry stack before variation.",
            "mathematical_form": "G_matter(Phi):=(mu_m, e_m, g_m, omega_m, D_m) with S_A=S_A[Psi_A,mu_m,e_m,omega_m,D_m,theta_A]",
            "if_signed": "there is a definite object whose vertical derivative can be checked",
            "current_status": "contract_written_not_parent_signed",
            "blocker": "current parent action has not supplied this full stack as a unique ordinary-matter structure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "GSD762_1_measure_descent",
            "stack_clause": "The matter measure descends through Q_MTS.",
            "mathematical_form": "mu_m(Phi)=Mu(q(Phi)); Lie_v mu_m=0 for v in ker(Dq)",
            "if_signed": "no representative volume/Weyl coupling enters matter integration",
            "current_status": "not_parent_signed",
            "blocker": "det(e_m) can still carry A_g(X)^4 or disformal determinant factors",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "GSD762_2_coframe_metric_descent",
            "stack_clause": "The matter coframe/metric descends through Q_MTS.",
            "mathematical_form": "e_m(Phi)=E(q(Phi)); g_m=E(q)^T eta E(q); Lie_v e_m=Lie_v g_m=0",
            "if_signed": "common Weyl/disformal c_g-like geometry coupling is theorem-zero for vertical representative directions",
            "current_status": "not_parent_signed",
            "blocker": "representative A_g(X)^2 g_obs or B_g(X)U_mu U_nu remains a legal counterexample",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "GSD762_3_connection_descent",
            "stack_clause": "The matter connection descends through the quotient coframe.",
            "mathematical_form": "omega_m(Phi)=Omega(E(q(Phi))) plus owned gauge/torsion pieces; Lie_v omega_m is gauge/exact or zero",
            "if_signed": "derivative couplings cannot reintroduce representative geometry after coframe descent",
            "current_status": "not_parent_signed",
            "blocker": "spin/torsion/nonmetricity/disformal connection terms may carry representative data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "GSD762_4_derivative_operator_descent",
            "stack_clause": "The covariant derivative/operator used by matter descends.",
            "mathematical_form": "D_m(Phi)=D[E(q(Phi)),owned gauge fields]; Lie_v D_m is gauge/exact or zero on observables",
            "if_signed": "rods/clocks/waves/charges do not see hidden representative derivative data",
            "current_status": "not_parent_signed",
            "blocker": "matter derivative can contain marker, charge-normalization, torsion, or source-frame data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "GSD762_5_stack_verdict",
            "stack_clause": "Promote geometry-stack descent.",
            "mathematical_form": "GSD762_0..GSD762_4 jointly sign G_matter(Phi)=Gbar(q(Phi)) up to owned gauge/exact terms",
            "if_signed": "geometry-stack part of Lie_v S_matter vanishes; no c_g through rods/clocks/derivatives",
            "current_status": "geometry_stack_descent_not_parent_signed",
            "blocker": "measure, coframe/metric, connection, and derivative stack are unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def chain_rule_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "GCR762_0_stack_chain_rule",
            "test": "Evaluate fixed-Psi vertical variation through the matter geometry stack.",
            "mathematical_form": "Lie_v S_matter = (delta S/dmu_m)Lie_v mu_m + (delta S/de_m)Lie_v e_m + (delta S/domega_m)Lie_v omega_m + (delta S/dD_m)Lie_v D_m + theta/boundary terms",
            "result": "valid_conditional_identity",
            "claim_limit": "identity only kills matter coupling if every stack derivative is zero/gauge/exact and theta/boundary terms close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "GCR762_1_measure_coframe_partial",
            "test": "Assume mu_m and e_m factor through q.",
            "mathematical_form": "Lie_v mu_m=Lie_v e_m=0 when Dq[v]=0",
            "result": "conditional_partial_zero",
            "claim_limit": "connection, derivative, marker, and boundary terms can still carry representative data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "GCR762_2_connection_risk",
            "test": "Allow omega_m or D_m to include representative torsion/nonmetricity/disformal marker.",
            "mathematical_form": "Lie_v e_m=0 but Lie_v omega_m != 0 or Lie_v D_m != 0",
            "result": "descent_failure_channel",
            "claim_limit": "c_g-like coupling can re-enter through derivative terms even if the metric descends",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "GCR762_3_current_corpus",
            "test": "Evaluate geometry-stack descent from current corpus alone.",
            "mathematical_form": "G_matter(Phi)=Gbar(q(Phi))?",
            "result": "not_parent_signed",
            "claim_limit": "no c_g, R10, PPN, clock, EM, Newton, or local-GR claim follows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def counterexample_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "GCE762_0_measure_weyl",
            "legal_if_unsigned": "matter measure contains representative Weyl factor",
            "mathematical_form": "mu_m=A_g(X)^4 mu_obs",
            "effect": "trace/source coupling survives even if matter fields are fixed",
            "blocks": "c_g zero, R10/source coupling, clock/orbit common-frame silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "GCE762_1_coframe_disformal",
            "legal_if_unsigned": "matter metric has representative disformal component",
            "mathematical_form": "g_m=A(q)^2 g_obs + B_g(X) U_mu U_nu",
            "effect": "preferred-frame and anisotropic couplings survive quotient language",
            "blocks": "PPN alpha_i, alpha3, clock/orbital disformal silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "GCE762_2_connection_marker",
            "legal_if_unsigned": "spin connection or derivative operator contains representative torsion/marker",
            "mathematical_form": "omega_m=omega[E(q)] + C_X(X) K_marker",
            "effect": "spin/EM/wave propagation sees representative data despite coframe factorization",
            "blocks": "EM/charge, spin/current, clock/photon derivative coupling zeros",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "GCE762_3_charge_normalization_derivative",
            "legal_if_unsigned": "gauge derivative includes X-dependent charge/current normalization",
            "mathematical_form": "D_m=d+iq_A(X)A_mu dx^mu + omega[E(q)]",
            "effect": "fine-structure/charge residual survives even if metric descends",
            "blocks": "EM charge interface and alpha/fine-structure claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "GSF762_0_geometry_stack_certificate",
            "artifact": "future_geometry_stack_descent_certificate.csv",
            "required_columns": "stack_layer;parent_owner;factorizes_through_q;vertical_derivative;gauge_or_exact_status;source_path;valid_for_claim",
            "claim_gate": "measure, coframe, connection, and derivative operator all descend or are owned gauge/exact",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "GSF762_1_coupling_descent_candidate",
            "artifact": str(COUPLING_DESCENT_CANDIDATE_PATH),
            "required_columns": "sector;functional;uses_e_obs;uses_q_of_Phi;hidden_frame_map;species_label_dependence;source_path;valid_for_claim",
            "claim_gate": "all ordinary sectors use the descended stack and no hidden representative map",
            "current_status": f"schema_only_candidate_missing={bool_string(not COUPLING_DESCENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "GSF762_2_cg_bound_input",
            "artifact": str(CG_SOURCE_CANDIDATE_PATH),
            "required_columns": "coefficient_id;arena;c_g_or_equivalent;lambda_or_scale;bound_value;units;source_path;valid_for_claim",
            "claim_gate": "c_g theorem-zero from full stack descent or sourced numeric bound",
            "current_status": f"schema_only_candidate_missing={bool_string(not CG_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "GSF762_3_disformal_connection_input",
            "artifact": "future_disformal_connection_source_rows.csv",
            "required_columns": "coefficient_id;stack_layer;projector;arena;bound_value;units;source_path;valid_for_claim",
            "claim_gate": "disformal/connection representative leakage is theorem-zero or bounded with projection",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "GSF762_4_EM_charge_interface",
            "artifact": str(EM_INTERFACE_CANDIDATE_PATH),
            "required_columns": "sector;charge_current_owner;metric_or_coframe_used;normalization;alpha_or_charge_response;source_path;valid_for_claim",
            "claim_gate": "charge/current derivative operator descends or charge normalization residual is bounded",
            "current_status": f"schema_only_candidate_missing={bool_string(not EM_INTERFACE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D762_0_geometry_stack",
            "decision": "write geometry-stack descent contract",
            "reason": "fixed/gauge-lift matter verticality still leaves measure, coframe, connection, and derivative terms in Lie_v S_matter",
            "claim_status": "contract_written_not_parent_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D762_1_no_cg_promotion",
            "decision": "do not promote c_g=0 or quotient descent",
            "reason": "representative data can still enter through measure/coframe/connection/derivative stack",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D762_2_next",
            "decision": "attack no-marker/no-spurion clause next",
            "reason": "even a descended geometry stack can be bypassed by X-dependent constants, charge normalizations, or material markers",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU762_0_allowed",
            "allowed_after_762": "say geometry-stack descent is the required next layer after matter vertical action",
            "forbidden_after_762": "claim c_g=0 from fixed-Psi/gauge-lift alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU762_1_allowed",
            "allowed_after_762": "treat measure/coframe/connection/derivative as separate coupling gates",
            "forbidden_after_762": "collapse metric descent into full matter descent while derivative operators remain open",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU762_2_allowed",
            "allowed_after_762": "move to no-marker/no-spurion theorem next",
            "forbidden_after_762": "ignore X-dependent constants, charge normalization, or material markers",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "geometry-stack descent contract written but not parent-signed",
            "hard_blocker": "measure, coframe, connection, and derivative operator factorization through q(Phi) remains unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    stack: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V762_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V762_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_761 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_761_VALIDATION.csv")
    validation.append({"check_id": "V762_2_prior_761_clean", "result": "pass" if prior_761 and all(row.get("result") == "pass" for row in prior_761) else "fail", "detail": "761 validation has no failures"})
    validation.append({"check_id": "V762_3_stack_contract_written", "result": "pass" if len(stack) == 6 and any(row["contract_id"] == "GSD762_5_stack_verdict" for row in stack) else "fail", "detail": "geometry stack contract rows present"})
    validation.append({"check_id": "V762_4_stack_not_parent_signed", "result": "pass" if any(row["contract_id"] == "GSD762_5_stack_verdict" and row["current_status"] == "geometry_stack_descent_not_parent_signed" for row in stack) else "fail", "detail": "geometry stack remains nonclaim"})
    validation.append({"check_id": "V762_5_chain_rule_retains_open_terms", "result": "pass" if any(row["audit_id"] == "GCR762_3_current_corpus" and row["result"] == "not_parent_signed" for row in chain) else "fail", "detail": "current corpus cannot close stack descent"})
    validation.append({"check_id": "V762_6_counterexamples_retained", "result": "pass" if len(counterexamples) == 4 and all(row["valid_for_claim"] == "false" for row in counterexamples) else "fail", "detail": "geometry stack counterexamples retained"})
    validation.append({"check_id": "V762_7_source_fill_schema_written", "result": "pass" if len(source_fill) == 5 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    validation.append({"check_id": "V762_8_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in [COUPLING_DESCENT_CANDIDATE_PATH, CG_SOURCE_CANDIDATE_PATH, EM_INTERFACE_CANDIDATE_PATH]) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = stack + chain + counterexamples + source_fill + decisions + routes + summary
    validation.append({"check_id": "V762_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V762_10_no_local_arena_claim", "result": "pass" if "no_quotient_descent_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V762_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        GEOMETRY_STACK_PATH,
        CHAIN_RULE_PATH,
        COUNTEREXAMPLE_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V762_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V762_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V762_14_no_marker_next", "result": "pass" if "no-marker-spurion" in NEXT_TARGET else "fail", "detail": "next attacks constants/markers/spurions"})
    validation.append({"check_id": "V762_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    stack: list[dict[str, Any]],
    chain: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 762 - Y5 R10 Geometry-Stack Descent Or Coupling Source Fill

Start point: 761 made the matter-domain vertical action contract-shaped, but its fixed-`Psi` chain rule still leaves measure, coframe, connection, derivative, constants, and boundary terms.

Current result: **geometry-stack descent is not parent-signed**. The necessary contract is clear: the matter measure, coframe/metric, connection, and derivative operator must all factor through `q(Phi)` up to owned gauge/exact terms. Without that, representative coupling can leak through rods, clocks, waves, spin/connection, EM charge normalization, or disformal derivative terms even if `Psi` is fixed.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Geometry-Stack Descent Contract

{markdown_table(stack, ["contract_id", "stack_clause", "mathematical_form", "if_signed", "current_status", "blocker", "valid_for_claim"])}

## Geometry-Stack Chain-Rule Audit

{markdown_table(chain, ["audit_id", "test", "mathematical_form", "result", "claim_limit", "valid_for_claim"])}

## Geometry-Stack Counterexample Ledger

{markdown_table(counterexamples, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "blocks", "valid_for_claim"])}

## Coupling Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_762", "forbidden_after_762", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This keeps the route honest. We are not saying matter descends because the words look nice. We are saying every layer matter actually uses must descend: volume, rods/clocks, connection, derivative, and charge/current normalization. That is stricter, but it is the route that survives scrutiny. Next target is no-marker/no-spurion, because even a descended geometry stack can be bypassed by hidden constants or material labels.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    stack = geometry_stack_rows(generated_utc)
    chain = chain_rule_rows(generated_utc)
    counterexamples = counterexample_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, stack, chain, counterexamples, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(GEOMETRY_STACK_PATH, stack, ["contract_id", "stack_clause", "mathematical_form", "if_signed", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(CHAIN_RULE_PATH, chain, ["audit_id", "test", "mathematical_form", "result", "claim_limit", "valid_for_claim", "generated_utc"])
    write_csv(COUNTEREXAMPLE_PATH, counterexamples, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_762", "forbidden_after_762", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, stack, chain, counterexamples, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
