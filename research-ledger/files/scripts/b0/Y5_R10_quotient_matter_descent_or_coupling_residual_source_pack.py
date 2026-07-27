from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md"
NEXT_TARGET = "761-Y5-R10-parent-matter-domain-vertical-action-or-coupling-source-fill.md"
STATUS = "Y5_R10_760_quotient_matter_descent_not_parent_signed_coupling_residual_source_pack_schema_written"
CLAIM_CEILING = "quotient_matter_descent_attempt_and_source_pack_schema_only_no_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_760_SOURCE_REGISTER.csv"
DESCENT_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_760_QUOTIENT_DESCENT_PROOF_ATTEMPT.csv"
SIGNATURE_GATE_PATH = RESIDUALS / "P8_Y5_R10_760_DESCENT_SIGNATURE_GATE.csv"
SOURCE_PACK_PATH = RESIDUALS / "P8_Y5_R10_760_COUPLING_RESIDUAL_SOURCE_PACK_SCHEMA.csv"
CG_DECISION_PATH = RESIDUALS / "P8_Y5_R10_760_CG_BOUND_DECISION.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_760_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_760_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_760_VALIDATION.csv"

COUPLING_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_COUPLING_DESCENT_INPUT_CANDIDATE.csv"
CG_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_CG_COUPLING_BOUND_INPUT_CANDIDATE.csv"
EM_INTERFACE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_EM_CHARGE_INTERFACE_INPUT_CANDIDATE.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "759_doc": {
        "path": POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        "needles": [
            "Current result: **the coupling owner action is not parent-signed yet**",
            "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
        ],
        "role": "immediate 760 handoff",
    },
    "759_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_759_VALIDATION.csv",
        "needles": ["V759_16_validation_rows_ready", "V759_14_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "759_owner": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
        "needles": ["COA759_1_quotient_matter_descent", "not_parent_signed_627_failed"],
        "role": "current quotient matter descent blocker",
    },
    "759_theorem": {
        "path": RESIDUALS / "P8_Y5_R10_759_PARTIAL_COUPLING_THEOREM_CONTRACT.csv",
        "needles": ["PCT759_2_representative_cg", "not_parent_signed_627_blocked"],
        "role": "representative c_g conditional theorem",
    },
    "759_acquisition": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_RESIDUAL_ACQUISITION_RUNNER.csv",
        "needles": ["CAR759_0_coupling_descent_input", "CAR759_1_cg_bound_input"],
        "role": "coupling residual acquisition handoff",
    },
    "627_doc": {
        "path": POST_CHECKPOINT / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md",
        "needles": ["S_matter = Sbar_matter[q(Phi),Psi,theta]", "c_g=0 not promoted"],
        "role": "latest c_g zero proof failure",
    },
    "626_doc": {
        "path": POST_CHECKPOINT / "626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md",
        "needles": ["The descent criterion is clean", "the signature is not parent-signed"],
        "role": "quotient-invariant matter action signature attempt",
    },
    "626_signature_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
        "needles": ["QIM626_0_descent_equivalence", "QIM626_5_signature_verdict"],
        "role": "prior descent clause audit",
    },
    "626_signature_ledger": {
        "path": RESIDUALS / "P8_Y5_R10_626_SIGNATURE_LEDGER.csv",
        "needles": ["QMS626_2_matter_descent", "QMS626_5_total_signature"],
        "role": "prior signature ledger",
    },
    "626_cg_template": {
        "path": RESIDUALS / "P8_Y5_R10_626_CG_BOUND_INPUT_TEMPLATE.csv",
        "needles": ["CGB626_1_cg_value", "MISSING_PARENT_INPUT"],
        "role": "existing c_g source-pack template",
    },
    "565_doc": {
        "path": POST_CHECKPOINT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
        "needles": ["VT565_0_vertical_observation_theorem", "factorization_not_parent_derived"],
        "role": "conditional vertical observation theorem",
    },
    "410_doc": {
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": ["quotient_matter_functor_parent_derived", "fail"],
        "role": "older quotient matter functor attempt",
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


def descent_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "QMD760_0_descent_equivalence",
            "target": "matter action descends to Q_MTS",
            "mathematical_test": "S_matter[Phi_parent,Psi] = Sbar_matter[q(Phi_parent),Psi,theta] iff Lie_v S_matter=0 for every v in ker(Dq), up to owned gauge/boundary terms",
            "result": "valid_conditional_descent_criterion",
            "missing_parent_signature": "criterion is known, but parent has not supplied all objects needed to evaluate it",
            "if_signed": "representative Weyl/disformal c_g-like leakage is forbidden in ordinary matter",
            "if_unsigned": "c_g/disformal/coupling residual source pack remains required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "QMD760_1_parent_quotient_object",
            "target": "q:Phi_parent -> Q_MTS before matter coupling",
            "mathematical_test": "q is defined on the parent configuration space, and representative fibres are identified before ordinary matter is varied",
            "result": "contract_only",
            "missing_parent_signature": "parent quotient construction is not yet a signed action-level object",
            "if_signed": "vertical/descent test has a domain",
            "if_unsigned": "representative directions may be physical local geometry data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "QMD760_2_vertical_matter_action",
            "target": "vertical action on matter domain",
            "mathematical_test": "for v in ker(Dq), either Psi is fixed or lifted by an owned gauge/representation action that leaves observables invariant",
            "result": "not_parent_signed",
            "missing_parent_signature": "ordinary matter variables and their vertical transformation rule are not fully specified",
            "if_signed": "Lie_v S_matter is well-defined",
            "if_unsigned": "descent cannot be tested without choosing a closure convention",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "QMD760_3_measure_coframe_connection",
            "target": "matter measure/coframe/connection descent",
            "mathematical_test": "det(e_m), e_m, omega[e_m], and D[e_m] are functions of q(Phi) rather than representative fibre data",
            "result": "not_parent_signed",
            "missing_parent_signature": "the matter geometry stack is not jointly shown to factor through Q_MTS",
            "if_signed": "representative c_g leakage through rods/clocks/derivatives is excluded",
            "if_unsigned": "A_g(X) or disformal terms can re-enter through measure or connection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "QMD760_4_no_marker_coefficients",
            "target": "no representative matter constants or marker labels",
            "mathematical_test": "theta_A, m_A, q_A, frame factors, and source/readout couplings are Q-data, representation data, or retained fields; not hidden fibre functions",
            "result": "not_parent_signed",
            "missing_parent_signature": "marker/class/constant-sector leakage remains a legal counterexample",
            "if_signed": "direct species and frame spurion leakage closes",
            "if_unsigned": "coupling residual rows must include species/marker dependence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "QMD760_5_boundary_projection",
            "target": "vertical boundary/exact terms have zero local projection",
            "mathematical_test": "boundary contribution to Lie_v S_matter is owned gauge/exact/topological or has zero local force/source/clock projection",
            "result": "not_parent_signed",
            "missing_parent_signature": "boundary and non-Hilbert residual projection silence is not derived",
            "if_signed": "descent is not spoiled by edge currents",
            "if_unsigned": "boundary/harmonic coupling residual must be sourced or bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "QMD760_6_verdict",
            "target": "promote quotient matter descent",
            "mathematical_test": "QMD760_0..QMD760_5 jointly sign S_matter=Sbar_matter[q(Phi),Psi,theta]",
            "result": "quotient_matter_descent_not_parent_signed",
            "missing_parent_signature": "parent quotient, vertical matter action, geometry stack descent, no-marker clause, and boundary silence are unsigned",
            "if_signed": "c_g=0 candidate and coupling-descent theorem can be promoted for ordinary matter",
            "if_unsigned": "write coupling residual source-pack schema and keep c_g/local claims blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def signature_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "DSG760_0_q_object",
            "required_clause": "parent quotient q exists before matter variation",
            "current_status": "contract_only",
            "blocks": "descent criterion domain",
            "next_evidence": "parent q map source or closure-only demotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DSG760_1_vertical_kernel",
            "required_clause": "local representative direction v_X belongs to ker(Dq)",
            "current_status": "conditional_not_signed",
            "blocks": "representative-frame exclusion and c_g theorem-zero",
            "next_evidence": "local branch theorem for Dq[v_X]=0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DSG760_2_matter_descent",
            "required_clause": "S_matter=Sbar_matter[q(Phi),Psi,theta]",
            "current_status": "not_signed",
            "blocks": "all ordinary coupling zero claims",
            "next_evidence": "parent matter action or source-pack rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DSG760_3_geometry_stack_descent",
            "required_clause": "measure, coframe, connection, and derivative operator descend",
            "current_status": "not_signed",
            "blocks": "rod/clock/derivative c_g leakage",
            "next_evidence": "geometry stack factorization proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DSG760_4_no_marker_spurion",
            "required_clause": "no representative species/source/readout constants",
            "current_status": "not_signed",
            "blocks": "species, WEP, clock, EM, and source-charge coupling zeros",
            "next_evidence": "no-marker/no-class-charge parent theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DSG760_5_boundary_silence",
            "required_clause": "vertical boundary/exact terms have zero local projection",
            "current_status": "not_signed",
            "blocks": "boundary/harmonic coupling and q_H leakage",
            "next_evidence": "boundary projection certificate or residual source row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_pack_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "CSP760_0_coupling_descent_candidate",
            "artifact": str(COUPLING_DESCENT_CANDIDATE_PATH),
            "required_columns": "sector;functional;uses_e_obs;uses_q_of_Phi;hidden_frame_map;species_label_dependence;source_path;valid_for_claim",
            "claim_gate": "all ordinary sectors descend through e_obs/q(Phi), no hidden frame/species/readout map, source paths real",
            "current_status": f"schema_only_candidate_missing={bool_string(not COUPLING_DESCENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CSP760_1_cg_bound_input",
            "artifact": str(CG_SOURCE_CANDIDATE_PATH),
            "required_columns": "coefficient_id;arena;c_g_or_equivalent;lambda_or_scale;bound_value;units;source_path;valid_for_claim",
            "claim_gate": "c_g theorem-zero or sourced numeric bound input; no representative descent claim without QMD760_6 closure",
            "current_status": f"schema_only_candidate_missing={bool_string(not CG_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CSP760_2_disformal_projection_input",
            "artifact": "future_disformal_projection_input_candidate.csv",
            "required_columns": "coefficient_id;arena;d_g_or_equivalent;projector;bound_value;units;source_path;valid_for_claim",
            "claim_gate": "disformal representative leakage is theorem-zero or bounded with arena projection",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CSP760_3_EM_charge_interface",
            "artifact": str(EM_INTERFACE_CANDIDATE_PATH),
            "required_columns": "sector;charge_current_owner;metric_or_coframe_used;normalization;alpha_or_charge_response;source_path;valid_for_claim",
            "claim_gate": "EM/charge/fine-structure interface descends through same observed quotient structure or is explicitly bounded",
            "current_status": f"schema_only_candidate_missing={bool_string(not EM_INTERFACE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CSP760_4_source_orbit_coupling",
            "artifact": "future_source_orbit_coupling_residual_rows.csv",
            "required_columns": "source_current_owner;Pi_M_owner;orbit_readout_owner;Gauss_calibration;mu_extra_channel;source_path;valid_for_claim",
            "claim_gate": "source current and orbit readout descend before measured-GM calibration",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CSP760_5_boundary_marker_residual",
            "artifact": "future_boundary_marker_coupling_residual_rows.csv",
            "required_columns": "residual_id;boundary_or_marker_type;projection;bound_or_zero_certificate;units;source_path;valid_for_claim",
            "claim_gate": "boundary/marker leakage is theorem-zero or explicitly bounded in the local arena",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def cg_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "CGD760_0_zero_certificate",
            "quantity": "Z_cg",
            "status": "false_not_parent_signed",
            "reason": "quotient matter descent did not close",
            "claim_effect": "c_g=0 cannot be promoted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "CGD760_1_bound_route",
            "quantity": "c_g and disformal equivalents",
            "status": "source_pack_required",
            "reason": "representative Weyl/disformal coupling remains a possible residual if descent is unsigned",
            "claim_effect": "R10/PPN/clock/orbital arenas remain blocked until numeric/theorem rows exist",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "CGD760_2_local_claims",
            "quantity": "local-GR / PPN / alpha3 / Newton",
            "status": "blocked",
            "reason": "coupling descent alone is not signed, and q_loc/Y5/Y6 gates remain independently open",
            "claim_effect": "no local arena pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU760_0_allowed",
            "allowed_after_760": "say quotient matter descent has a valid conditional criterion",
            "forbidden_after_760": "say current MTS has parent-signed matter descent or c_g=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU760_1_allowed",
            "allowed_after_760": "attack parent matter-domain vertical action next",
            "forbidden_after_760": "evaluate Lie_v S_matter without specifying how matter variables transform vertically",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU760_2_allowed",
            "allowed_after_760": "use coupling residual source-pack schema if descent remains unsigned",
            "forbidden_after_760": "mark coupling, c_g, disformal, EM, boundary, or source-orbit rows valid_for_claim with placeholders",
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
            "main_result": "quotient matter descent not parent-signed; coupling residual source-pack schema written",
            "hard_blocker": "parent matter-domain vertical action plus geometry stack/no-marker/boundary descent are unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    cg_decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V760_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V760_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_759 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_759_VALIDATION.csv")
    validation.append({"check_id": "V760_2_prior_759_clean", "result": "pass" if prior_759 and all(row.get("result") == "pass" for row in prior_759) else "fail", "detail": "759 validation has no failures"})
    validation.append({"check_id": "V760_3_descent_not_parent_signed", "result": "pass" if any(row["attempt_id"] == "QMD760_6_verdict" and row["result"] == "quotient_matter_descent_not_parent_signed" for row in attempts) else "fail", "detail": "descent remains nonclaim"})
    validation.append({"check_id": "V760_4_signature_gates_retained", "result": "pass" if len(gates) == 6 and all(row["valid_for_claim"] == "false" for row in gates) else "fail", "detail": "six descent gates retained"})
    validation.append({"check_id": "V760_5_source_pack_schema_written", "result": "pass" if len(pack) == 6 and all(row["valid_for_claim"] == "false" for row in pack) else "fail", "detail": "coupling source-pack schema is nonclaim"})
    validation.append({"check_id": "V760_6_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in [COUPLING_DESCENT_CANDIDATE_PATH, CG_SOURCE_CANDIDATE_PATH, EM_INTERFACE_CANDIDATE_PATH]) else "fail", "detail": "no claim-input artifacts fabricated"})
    validation.append({"check_id": "V760_7_cg_zero_not_promoted", "result": "pass" if any(row["decision_id"] == "CGD760_0_zero_certificate" and row["status"] == "false_not_parent_signed" for row in cg_decisions) else "fail", "detail": "c_g zero remains blocked"})
    all_generated = attempts + gates + pack + cg_decisions + routes + summary
    validation.append({"check_id": "V760_8_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V760_9_no_local_arena_claim", "result": "pass" if "no_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V760_10_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        DESCENT_ATTEMPT_PATH,
        SIGNATURE_GATE_PATH,
        SOURCE_PACK_PATH,
        CG_DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V760_11_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V760_12_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V760_13_matter_domain_next", "result": "pass" if "parent-matter-domain-vertical-action" in NEXT_TARGET else "fail", "detail": "next attacks first evaluability blocker"})
    validation.append({"check_id": "V760_14_no_placeholder_claim_inputs", "result": "pass" if all("schema_only" in row["current_status"] for row in pack) else "fail", "detail": "source pack is schema only"})
    validation.append({"check_id": "V760_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    cg_decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 760 - Y5 R10 Quotient Matter Descent Or Coupling Residual Source Pack

Start point: 759 selected quotient matter descent as the central coupling theorem target.

Current result: **quotient matter descent is not parent-signed**. The descent criterion is clean and worth keeping: `S_matter` descends to `Sbar_matter[q(Phi),Psi,theta]` exactly when vertical representative variations leave the matter action invariant, up to owned gauge/boundary terms. But the current corpus still lacks the parent matter-domain vertical action, geometry-stack descent, no-marker/no-spurion theorem, and boundary projection silence. Therefore `c_g=0` is not claimed, and 760 writes the coupling residual source-pack schema.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Quotient Descent Proof Attempt

{markdown_table(attempts, ["attempt_id", "target", "mathematical_test", "result", "missing_parent_signature", "if_signed", "if_unsigned", "valid_for_claim"])}

## Descent Signature Gate

{markdown_table(gates, ["gate_id", "required_clause", "current_status", "blocks", "next_evidence", "valid_for_claim"])}

## Coupling Residual Source-Pack Schema

{markdown_table(pack, ["pack_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## c_g / Local Claim Decision

{markdown_table(cg_decisions, ["decision_id", "quantity", "status", "reason", "claim_effect", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_760", "forbidden_after_760", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is not grim; it is exact. The theorem we want has a clean mathematical door, but the key is not yet cut: before `Lie_v S_matter=0` can be evaluated, the parent has to say what `v` does to the matter domain. That is the next best target. If that fails, the source-pack lane is ready and still private/nonclaim.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    attempts = descent_attempt_rows(generated_utc)
    gates = signature_gate_rows(generated_utc)
    pack = source_pack_rows(generated_utc)
    cg_decisions = cg_decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, attempts, gates, pack, cg_decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(DESCENT_ATTEMPT_PATH, attempts, ["attempt_id", "target", "mathematical_test", "result", "missing_parent_signature", "if_signed", "if_unsigned", "valid_for_claim", "generated_utc"])
    write_csv(SIGNATURE_GATE_PATH, gates, ["gate_id", "required_clause", "current_status", "blocks", "next_evidence", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_PACK_PATH, pack, ["pack_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(CG_DECISION_PATH, cg_decisions, ["decision_id", "quantity", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_760", "forbidden_after_760", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, attempts, gates, pack, cg_decisions, routes, summary, validation)

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
