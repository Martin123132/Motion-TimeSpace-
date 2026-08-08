from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md"
NEXT_TARGET = "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md"
STATUS = "Y5_R10_756_Gamma_Khat_metric_response_symbol_match_failed_response_doublet_formal_only_q_loc_component_candidate_builder_schema_written"
CLAIM_CEILING = "metric_response_symbol_match_and_response_doublet_repair_audit_only_no_q_loc_zero_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_756_SOURCE_REGISTER.csv"
SYMBOL_MATCH_PATH = RESIDUALS / "P8_Y5_R10_756_METRIC_RESPONSE_SYMBOL_MATCH_AUDIT.csv"
RESPONSE_DOUBLET_PATH = RESIDUALS / "P8_Y5_R10_756_RESPONSE_DOUBLET_REPAIR_ATTEMPT.csv"
BUILDER_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_756_QLOC_COMPONENT_CANDIDATE_BUILDER_SCHEMA.csv"
DRYRUN_PATH = RESIDUALS / "P8_Y5_R10_756_QLOC_COMPONENT_CANDIDATE_DRYRUN.csv"
PRODUCT_DECISION_PATH = RESIDUALS / "P8_Y5_R10_756_ALPHA3_PRODUCT_DECISION.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_756_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_756_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_756_VALIDATION.csv"

QLOC_COMPONENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv"
PFLUX_PROJECTOR_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_PFLUX_PROJECTOR_INPUT.csv"
ALPHA3_RESPONSE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_RESPONSE_OPERATOR_INPUT.csv"
ALPHA3_PRODUCT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_PRODUCT_INPUT.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "755_doc": {
        "path": POST_CHECKPOINT / "755-Y5-R10-observed-q_loc-Ward-owner-or-alpha3-component-source-pack.md",
        "needles": [
            "the observed `q_loc` Ward-owner route is precise",
            "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
        ],
        "role": "immediate 756 handoff",
    },
    "755_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_755_VALIDATION.csv",
        "needles": ["V755_14_validation_rows_ready", "V755_11_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "755_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_755_GK_SYMBOL_MATCH_OBSTRUCTION_LEDGER.csv",
        "needles": ["GKO755_1_Khat_metric_response", "definition possible, existing match failed"],
        "role": "current Gamma/Khat obstruction",
    },
    "755_source_pack": {
        "path": RESIDUALS / "P8_Y5_R10_755_ALPHA3_COMPONENT_SOURCE_PACK_SCHEMA.csv",
        "needles": ["ACS755_0_q_loc_component_candidate", "blocked_until_zero_theorem_or_ACS755_0_to_2_filled"],
        "role": "component source-pack fallback",
    },
    "513_contract_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "needles": [
            "T_GK^{mu nu} := Gamma_eff g^{mu nu} - K_hat^{mu nu}",
            "q_loc^nu = P_loc nabla_mu T_GK^{mu nu}",
        ],
        "role": "first variation contract",
    },
    "514_candidate_doc": {
        "path": POST_CHECKPOINT / "514-construct-GK-stress-action-or-residual-bound.md",
        "needles": [
            "S_GK = - integral sqrt(-g) Gamma_eff",
            "K_hat = metric response of Gamma_eff",
        ],
        "role": "candidate action route",
    },
    "515_match_doc": {
        "path": POST_CHECKPOINT / "515-match-Gamma-eff-Khat-to-metric-response-action.md",
        "needles": [
            "No current corpus source proves that Gamma_eff is a covariant scalar action density.",
            "No current corpus source proves that K_hat is the metric variation of Gamma_eff.",
        ],
        "role": "metric-response no-match audit",
    },
    "516_owner_doc": {
        "path": POST_CHECKPOINT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
        "needles": [
            "Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)",
            "But it is still not a current MTS derivation.",
        ],
        "role": "response-doublet candidate owner",
    },
    "517_variation_doc": {
        "path": POST_CHECKPOINT / "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
        "needles": [
            "partial_A Gamma_eff|Z=0 = 0.",
            "Z^A must equal the actual local residual vector through PPN/source-normalization order.",
        ],
        "role": "formal double-zero and physical-lock blocker",
    },
    "metric_response_contract": {
        "path": RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "needles": ["MR514_0_scalar_density", "MR514_5_double_zero"],
        "role": "metric response acceptance contract",
    },
    "metric_response_audit": {
        "path": RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
        "needles": ["MA515_0_Gamma_scalar_density_owner", "MA515_1_Khat_metric_response"],
        "role": "previous symbol-match audit",
    },
    "gamma_owner_candidate": {
        "path": RESIDUALS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "needles": ["GO516_A_response_doublet_quadratic_density", "best_candidate_not_current_MTS_derived"],
        "role": "best formal repair candidate",
    },
    "response_doublet_variation": {
        "path": RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        "needles": ["AV517_2_first_variation_Z", "formal_double_zero_at_Z0"],
        "role": "formal double-zero ledger",
    },
    "response_doublet_obstructions": {
        "path": RESIDUALS / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
        "needles": ["OB517_0_Y5_even_scalar", "OB517_2_PPN_lock"],
        "role": "physical residual lock blockers",
    },
    "750_component_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
        "needles": ["QIN750_3_q_loc_components", "component-resolved q_loc field/profile"],
        "role": "real q_loc component input schema",
    },
    "750_hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "Hodge/component runner schema",
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


def symbol_match_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "match_id": "MRM756_0_variational_contract",
            "target": "define a reduced Hilbert-stress owner",
            "required_identity": "S_GK=-int sqrt(-g_obs) gamma; T_GK^{mu nu}=Gamma_eff g_obs^{mu nu}-K_hat^{mu nu}=2/sqrt(-g_obs) delta S_GK/delta g_obs_mu_nu",
            "current_evidence": "513/514 give the correct conditional contract and sign-convention target",
            "result": "formal_contract_only",
            "blocker_or_next": "must identify current Gamma_eff with gamma and current K_hat with its full metric response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "MRM756_1_Gamma_identification",
            "target": "Gamma_eff == gamma[g_obs,Phi,nablaPhi,D,...]",
            "required_identity": "Gamma_eff is a covariant scalar action density with declared units and no post-readout selector",
            "current_evidence": "515/MA515_0 says Gamma_eff appears as route/readout/relaxation/boundary-charge symbol, not as an action-owned scalar density",
            "result": "fail_for_current_corpus",
            "blocker_or_next": "write parent-owned gamma or demote Gamma_eff to residual bookkeeping",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "MRM756_2_Khat_identification",
            "target": "K_hat == K_gamma",
            "required_identity": "K_gamma^{mu nu}:=2 E_g^{mu nu}[gamma], including metric-derivative, projector, domain, and boundary terms under one sign convention",
            "current_evidence": "515/MA515_1 says Khat appears in q_loc identities and owner-current targets, but no derivation as delta[sqrt(-g)Gamma_eff]/delta g was found",
            "result": "fail_for_current_corpus",
            "blocker_or_next": "compute K_gamma from a proposed gamma and compare every tensor term with current K_hat",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "MRM756_3_Helmholtz_integrability",
            "target": "stress integrability",
            "required_identity": "delta(sqrt(-g)T_GK^{mu nu})/delta g_alpha_beta has the symmetric second-variation/Helmholtz structure up to allowed boundary improvements",
            "current_evidence": "513 records this as not checked; 756 finds no newer closure",
            "result": "not_checked_blocks_claim",
            "blocker_or_next": "cannot promote an arbitrary Gamma g - K tensor to an action stress without this check or an explicit action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "MRM756_4_boundary_projector_metric_terms",
            "target": "boundary, domain, P_loc, and readout metric variations",
            "required_identity": "metric variation of all domain/projector/boundary pieces is either included in K_gamma or theorem-zero in compact local vacuum",
            "current_evidence": "755 keeps P_loc ownership and observed boundary flux open",
            "result": "open_blocks_claim",
            "blocker_or_next": "proper representative boundary silence does not yet silence observed reduced q_loc flux",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "match_id": "MRM756_5_verdict",
            "target": "accept current Gamma/Khat metric-response symbol match",
            "required_identity": "MRM756_1..MRM756_4 all close",
            "current_evidence": "Gamma owner, Khat metric response, Helmholtz integrability, and boundary/projector terms remain unsigned",
            "result": "metric_response_symbol_match_not_accepted",
            "blocker_or_next": "response-doublet can be retained only as a formal parent-action contract; otherwise build real q_loc component input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def response_doublet_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "RDR756_0_response_doublet_parent_action",
            "route": "quadratic exchange-odd residual scalar density",
            "mathematical_form": "gamma = gamma0 + 1/2 M_AB(g_obs,R_even,D,...) Z^A Z^B + O(Z^4)",
            "what_it_derives": "delta gamma/delta Z^A = M_AB Z^B + O(Z^3), so the Z first variation vanishes at Z=0 if no J_A Z^A or boundary B_A Z^A term exists",
            "current_status": "formal_candidate_retained",
            "why_not_promoted": "Z^A is not yet proven equal to the actual physical q_loc/source-normalization/PPN residual vector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "RDR756_1_metric_response_of_doublet",
            "route": "K_gamma from gamma",
            "mathematical_form": "K_gamma^{mu nu}=2 E_g^{mu nu}[gamma]; after gamma0 subtraction, K_gamma and T_GK are O(Z^2) if M_AB/projectors have no hidden linear Z metric response",
            "what_it_derives": "a clean way to make F_1=0 for the auxiliary doublet sector",
            "current_status": "conditional_formal_pass",
            "why_not_promoted": "current K_hat has not been shown to equal this K_gamma term-by-term",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "RDR756_2_local_zero_limit",
            "route": "fixed-point double zero",
            "mathematical_form": "Z=0 and gamma0 subtracted => gamma-gamma0=0, partial_Z gamma=0, K_gamma=O(Z^2), T_GK=O(Z^2)",
            "what_it_derives": "linear local leakage can be killed inside the formal doublet model",
            "current_status": "formal_double_zero_only",
            "why_not_promoted": "does not yet kill exchange-even Y5 source strength, Y6 stress, PPN alpha_i, or observed boundary flux",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "RDR756_3_verdict",
            "route": "promote response-doublet to current MTS local-GR proof",
            "mathematical_form": "RDR756_0..RDR756_2 plus physical lock Z^A = {q_loc, epsilon_mu, Delta T_extra, PPN preferred-frame residuals} through weak-field order",
            "what_it_derives": "would become a serious parent-action route to derived local GR",
            "current_status": "not_promoted_physical_lock_missing",
            "why_not_promoted": "formal auxiliary zeros can erase a shadow variable without proving the measured local residuals vanish",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def builder_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "builder_id": "QCB756_0_builder_schema",
            "artifact": str(QLOC_COMPONENT_CANDIDATE_PATH),
            "required_columns": "sample_id;domain_id;weight_dV;frame_convention;u0;u1;u2;u3;q0;q1;q2;q3;boundary_tag;boundary_condition;source_path;valid_for_claim",
            "acceptance_gate": "real component-resolved q_loc data or a theorem-zero certificate; no scalar q_proxy-only substitution",
            "current_status": "candidate_input_absent_schema_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "builder_id": "QCB756_1_component_formula_owner",
            "artifact": "derived q_loc component formula",
            "required_columns": "Gamma_eff_component_owner;Khat_component_owner;P_loc_owner;covariant_derivative_convention;units;source_path",
            "acceptance_gate": "q_loc^nu=P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}) evaluated in observed frame with units",
            "current_status": "missing_current_symbol_match",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "builder_id": "QCB756_2_Hodge_flux_projector",
            "artifact": str(PFLUX_PROJECTOR_CANDIDATE_PATH),
            "required_columns": "projector_id;domain_id;boundary_operator;P_flux_formula;normalization;q_proxy_denominator;units;source_path;valid_for_claim",
            "acceptance_gate": "P_flux P_Hodge q_loc theorem-zero or computed from real component input and boundary operator",
            "current_status": "candidate_input_absent_schema_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "builder_id": "QCB756_3_alpha3_response_operator",
            "artifact": str(ALPHA3_RESPONSE_CANDIDATE_PATH),
            "required_columns": "operator_id;G_PPN_source_to_g0i;Pi_alpha3_extraction;gauge;frame;units;source_path;valid_for_claim",
            "acceptance_gate": "W_q_alpha3 derived in same frame/gauge convention as f_qV",
            "current_status": "candidate_input_absent_schema_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "builder_id": "QCB756_4_alpha3_product",
            "artifact": str(ALPHA3_PRODUCT_CANDIDATE_PATH),
            "required_columns": "W_q_alpha3;f_qV;q_proxy;alpha3_q;target_bound;source_paths;no_cancellation_flag;valid_for_claim",
            "acceptance_gate": f"abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g} and abs(alpha3_q)<=4e-20",
            "current_status": "blocked_until_theorem_zero_or_real_component_rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "builder_id": "QCB756_5_no_fake_data_guard",
            "artifact": "756 guardrail",
            "required_columns": "all claim rows must be sourced numeric/theorem rows",
            "acceptance_gate": "no MISSING_PARENT_INPUT, MISSING_ARENA_PROJECTION, placeholder Z, or q_proxy-only row may set valid_for_claim=true",
            "current_status": "guard_active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def dryrun_rows(generated_utc: str) -> list[dict[str, Any]]:
    candidate_exists = QLOC_COMPONENT_CANDIDATE_PATH.exists()
    projector_exists = PFLUX_PROJECTOR_CANDIDATE_PATH.exists()
    response_exists = ALPHA3_RESPONSE_CANDIDATE_PATH.exists()
    product_exists = ALPHA3_PRODUCT_CANDIDATE_PATH.exists()
    return [
        {
            "dryrun_id": "QCD756_0_schema_sources_present",
            "check": "component and Hodge schemas exist",
            "input_state": "750 schemas source-backed",
            "runner_action": "schema can be used for a future candidate file",
            "result": "pass_nonclaim",
            "claim_status": "dryrun_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QCD756_1_candidate_input_absent",
            "check": "real component candidate file",
            "input_state": f"exists={bool_string(candidate_exists)} path={QLOC_COMPONENT_CANDIDATE_PATH}",
            "runner_action": "do not integrate q_loc components and do not synthesize placeholder rows",
            "result": "blocked_as_expected",
            "claim_status": "no_component_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QCD756_2_projector_operator_absent",
            "check": "P_flux/Hodge projector input",
            "input_state": f"projector_exists={bool_string(projector_exists)} response_exists={bool_string(response_exists)}",
            "runner_action": "do not compute f_qV or W_q_alpha3",
            "result": "blocked_as_expected",
            "claim_status": "no_operator_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QCD756_3_product_input_absent",
            "check": "alpha3 product input",
            "input_state": f"exists={bool_string(product_exists)} path={ALPHA3_PRODUCT_CANDIDATE_PATH}",
            "runner_action": "retain product gate without scoring",
            "result": "blocked_as_expected",
            "claim_status": "not_scoreable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QCD756_4_claim_guard",
            "check": "claim promotion",
            "input_state": "metric-response theorem false; component/operator inputs absent",
            "runner_action": "keep alpha3, PPN, R10, Newton, and local-GR claims blocked",
            "result": "pass_nonclaim",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "A3D756_0_theorem_zero_route",
            "route": "P_flux P_Hodge q_loc = 0 by Ward/Hilbert-stress theorem",
            "status": "blocked",
            "reason": "Gamma_eff/K_hat metric-response symbol match not accepted",
            "gate": "MRM756_5 must close before theorem-zero promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "A3D756_1_numeric_component_route",
            "route": "compute f_qV and W_q_alpha3 from component/operator inputs",
            "status": "blocked",
            "reason": "real q_loc component candidate and response operator files are absent",
            "gate": "QCB756_0..QCB756_4 real sourced rows required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "A3D756_2_gate",
            "route": "alpha3 product acceptance",
            "status": "retained_not_scoreable",
            "reason": f"gate remains abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g}",
            "gate": "no model branch may pass alpha3 without theorem-zero or sourced numeric product",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "A3D756_3_claim_ceiling",
            "route": "local arena promotion",
            "status": "forbidden",
            "reason": "no q_loc zero, no alpha3 product, no local-GR proof",
            "gate": CLAIM_CEILING,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU756_0_allowed",
            "allowed_after_756": "state the exact parent-action contract for Gamma_eff/K_hat",
            "forbidden_after_756": "claim the current Gamma_eff/K_hat symbols already satisfy that contract",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU756_1_allowed",
            "allowed_after_756": "keep the response-doublet as the best formal construction route",
            "forbidden_after_756": "use formal Z=0 double-zero as proof that observed q_loc, Y5, Y6, or alpha3 vanish",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU756_2_allowed",
            "allowed_after_756": "either lock Z to the physical residual vector or build real q_loc component inputs",
            "forbidden_after_756": "fill component rows with placeholders or q_proxy-only smoke data",
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
            "main_result": "metric-response symbol match still fails; response-doublet is formal only; component builder schema/dry-run written",
            "hard_blocker": "physical lock from auxiliary Z^A to observed q_loc/source-normalization/PPN residuals is missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    symbol_match: list[dict[str, Any]],
    response_doublet: list[dict[str, Any]],
    builder: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V756_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V756_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_755 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_755_VALIDATION.csv")
    validation.append({"check_id": "V756_2_prior_755_clean", "result": "pass" if prior_755 and all(row.get("result") == "pass" for row in prior_755) else "fail", "detail": "755 validation has no failures"})
    validation.append({"check_id": "V756_3_symbol_match_failed_cleanly", "result": "pass" if any(row["match_id"] == "MRM756_5_verdict" and row["result"] == "metric_response_symbol_match_not_accepted" for row in symbol_match) else "fail", "detail": "symbol match remains nonclaim"})
    validation.append({"check_id": "V756_4_response_doublet_not_promoted", "result": "pass" if any(row["attempt_id"] == "RDR756_3_verdict" and row["current_status"] == "not_promoted_physical_lock_missing" for row in response_doublet) else "fail", "detail": "formal doublet not promoted to local-GR proof"})
    validation.append({"check_id": "V756_5_builder_schema_written", "result": "pass" if len(builder) == 6 and all(row["valid_for_claim"] == "false" for row in builder) else "fail", "detail": "q_loc component builder schema is nonclaim"})
    validation.append({"check_id": "V756_6_candidate_input_absent", "result": "pass" if not QLOC_COMPONENT_CANDIDATE_PATH.exists() else "fail", "detail": str(QLOC_COMPONENT_CANDIDATE_PATH)})
    validation.append({"check_id": "V756_7_dryrun_nonclaim", "result": "pass" if len(dryrun) == 5 and all(row["valid_for_claim"] == "false" for row in dryrun) else "fail", "detail": "dry-run blocks as expected without fake rows"})
    validation.append({"check_id": "V756_8_product_gate_retained", "result": "pass" if any(row["decision_id"] == "A3D756_2_gate" and row["status"] == "retained_not_scoreable" for row in product) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    all_generated = symbol_match + response_doublet + builder + dryrun + product + routes + summary
    validation.append({"check_id": "V756_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V756_10_no_local_arena_claim", "result": "pass" if "no_q_loc_zero_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V756_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        SYMBOL_MATCH_PATH,
        RESPONSE_DOUBLET_PATH,
        BUILDER_SCHEMA_PATH,
        DRYRUN_PATH,
        PRODUCT_DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V756_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V756_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V756_14_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in [QLOC_COMPONENT_CANDIDATE_PATH, PFLUX_PROJECTOR_CANDIDATE_PATH, ALPHA3_RESPONSE_CANDIDATE_PATH, ALPHA3_PRODUCT_CANDIDATE_PATH]) else "fail", "detail": "no claim-input artifacts fabricated"})
    validation.append({"check_id": "V756_15_route_forbids_formal_Z_overclaim", "result": "pass" if any("formal Z=0 double-zero" in row["forbidden_after_756"] for row in routes) else "fail", "detail": "formal auxiliary zero cannot be treated as observed residual zero"})
    validation.append({"check_id": "V756_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    symbol_match: list[dict[str, Any]],
    response_doublet: list[dict[str, Any]],
    builder: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    product: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 756 - Y5 R10 Gamma/Khat Metric-Response Symbol Match Or q_loc Component Candidate Builder

Start point: 755 left one precise hinge. The Ward identity can only suppress observed `q_loc` if the current symbols satisfy the parent Hilbert-stress contract:

```text
S_GK = - int sqrt(-g_obs) gamma
T_GK^{{mu nu}} = Gamma_eff g_obs^{{mu nu}} - K_hat^{{mu nu}}
              = 2/sqrt(-g_obs) delta S_GK / delta g_obs_mu_nu
q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}
```

Current result: **the metric-response symbol match still fails for the current corpus**. The response-doublet construction remains the best formal parent-action route, but it is not a local-GR proof until `Z^A` is physically locked to the observed residual vector. Therefore 756 also writes the no-fake-data `q_loc` component candidate builder schema and dry-run.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Metric-Response Symbol Match Audit

{markdown_table(symbol_match, ["match_id", "target", "required_identity", "current_evidence", "result", "blocker_or_next", "valid_for_claim"])}

## Response-Doublet Repair Attempt

{markdown_table(response_doublet, ["attempt_id", "route", "mathematical_form", "what_it_derives", "current_status", "why_not_promoted", "valid_for_claim"])}

## q_loc Component Candidate Builder Schema

{markdown_table(builder, ["builder_id", "artifact", "required_columns", "acceptance_gate", "current_status", "valid_for_claim"])}

## q_loc Component Candidate Dry-Run

{markdown_table(dryrun, ["dryrun_id", "check", "input_state", "runner_action", "result", "claim_status", "valid_for_claim"])}

## Alpha3 Product Decision

{markdown_table(product, ["decision_id", "route", "status", "reason", "gate", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_756", "forbidden_after_756", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a useful failure, not a dead-end failure. The clean derivation exists as a contract: make `Gamma_eff` a real scalar density, make `K_hat` its metric response, prove the boundary/projector pieces are owned, and the Ward route becomes serious. But the current symbols do not yet satisfy that contract. The response-doublet route gives us a mathematically neat double-zero, but the missing lock is physical: `Z^A` must be the actual observed residual vector, not an auxiliary shadow. Next target is therefore either to prove that lock or build the real component input pack.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    symbol_match = symbol_match_rows(generated_utc)
    response_doublet = response_doublet_rows(generated_utc)
    builder = builder_schema_rows(generated_utc)
    dryrun = dryrun_rows(generated_utc)
    product = product_decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, symbol_match, response_doublet, builder, dryrun, product, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SYMBOL_MATCH_PATH, symbol_match, ["match_id", "target", "required_identity", "current_evidence", "result", "blocker_or_next", "valid_for_claim", "generated_utc"])
    write_csv(RESPONSE_DOUBLET_PATH, response_doublet, ["attempt_id", "route", "mathematical_form", "what_it_derives", "current_status", "why_not_promoted", "valid_for_claim", "generated_utc"])
    write_csv(BUILDER_SCHEMA_PATH, builder, ["builder_id", "artifact", "required_columns", "acceptance_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DRYRUN_PATH, dryrun, ["dryrun_id", "check", "input_state", "runner_action", "result", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(PRODUCT_DECISION_PATH, product, ["decision_id", "route", "status", "reason", "gate", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_756", "forbidden_after_756", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, symbol_match, response_doublet, builder, dryrun, product, routes, summary, validation)

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
