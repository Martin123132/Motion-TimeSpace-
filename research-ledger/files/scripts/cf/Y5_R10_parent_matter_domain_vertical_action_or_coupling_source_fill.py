from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "761-Y5-R10-parent-matter-domain-vertical-action-or-coupling-source-fill.md"
NEXT_TARGET = "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md"
STATUS = "Y5_R10_761_parent_matter_domain_vertical_action_contract_written_not_parent_signed_coupling_source_fill_schema_retained"
CLAIM_CEILING = "parent_matter_domain_vertical_action_contract_only_no_quotient_descent_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

COUPLING_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_COUPLING_DESCENT_INPUT_CANDIDATE.csv"
CG_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_CG_COUPLING_BOUND_INPUT_CANDIDATE.csv"
EM_INTERFACE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_EM_CHARGE_INTERFACE_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_761_SOURCE_REGISTER.csv"
VERTICAL_ACTION_PATH = RESIDUALS / "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv"
EVALUABILITY_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_761_LIEV_SMATTER_EVALUABILITY_AUDIT.csv"
COUNTEREXAMPLE_PATH = RESIDUALS / "P8_Y5_R10_761_VERTICAL_ACTION_COUNTEREXAMPLE_LEDGER.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_761_COUPLING_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_761_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_761_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_761_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_761_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "760_doc": {
        "path": POST_CHECKPOINT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
        "needles": [
            "Current result: **quotient matter descent is not parent-signed**",
            "761-Y5-R10-parent-matter-domain-vertical-action-or-coupling-source-fill.md",
        ],
        "role": "immediate 761 handoff",
    },
    "760_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_760_VALIDATION.csv",
        "needles": ["V760_15_validation_rows_ready", "V760_12_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "760_descent_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_760_QUOTIENT_DESCENT_PROOF_ATTEMPT.csv",
        "needles": ["QMD760_2_vertical_matter_action", "not_parent_signed"],
        "role": "vertical matter action blocker",
    },
    "760_gate": {
        "path": RESIDUALS / "P8_Y5_R10_760_DESCENT_SIGNATURE_GATE.csv",
        "needles": ["DSG760_2_matter_descent", "not_signed"],
        "role": "descent gate handoff",
    },
    "760_source_pack": {
        "path": RESIDUALS / "P8_Y5_R10_760_COUPLING_RESIDUAL_SOURCE_PACK_SCHEMA.csv",
        "needles": ["CSP760_0_coupling_descent_candidate", "schema_only_candidate_missing=true"],
        "role": "source-fill fallback",
    },
    "626_signature_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
        "needles": ["QIM626_1_parent_matter_domain", "cannot evaluate quotient invariance of S_matter"],
        "role": "prior parent matter-domain clause",
    },
    "622_contract": {
        "path": RESIDUALS / "P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
        "needles": ["PMC622_1_domain_covariance", "PMC622_8_contract_verdict"],
        "role": "parent matter-sector contract",
    },
    "621_doc": {
        "path": POST_CHECKPOINT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
        "needles": ["NMF621_0_parent_matter_domain", "not_closed_contract_only"],
        "role": "normal-form theorem contract",
    },
    "565_doc": {
        "path": POST_CHECKPOINT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
        "needles": ["VT565_0_vertical_observation_theorem", "factorization_not_parent_derived"],
        "role": "conditional vertical observation theorem",
    },
    "410_doc": {
        "path": POST_CHECKPOINT / "410-quotient-matter-functor-theorem-attempt.md",
        "needles": ["matter action factorization", "sufficient_axiom_not_parent_derived"],
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


def vertical_action_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "MVA761_0_domain_category",
            "vertical_action_clause": "Ordinary matter fields are sections of parent-owned bundles over the observed geometry.",
            "mathematical_form": "Psi_A in Gamma(E_A[e_obs(q(Phi))]); S_A=S_A[Psi_A,e_obs(q(Phi)),theta_A]",
            "derives_if_signed": "the matter domain on which Lie_v acts is defined before coupling tests",
            "current_status": "admissible_contract_not_parent_constructed",
            "blocker": "the parent action has not constructed the ordinary matter category as the only allowed matter domain",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MVA761_1_fixed_Psi_vertical_action",
            "vertical_action_clause": "For representative vertical v in ker(Dq), ordinary matter variables are held fixed when only parent representative data moves.",
            "mathematical_form": "delta_v Phi=v, Dq[v]=0, delta_v Psi_A=0, delta_v theta_A=0",
            "derives_if_signed": "Lie_v S_matter reduces to geometry/constant/boundary dependence; if those descend too, Lie_v S_matter=0",
            "current_status": "clean_option_not_parent_signed",
            "blocker": "fixed-Psi choice is a convention unless parent says v is a redundancy of the matter bundle, not a physical matter transformation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MVA761_2_gauge_lift_action",
            "vertical_action_clause": "If v induces a pure gauge/local Lorentz/diffeomorphism lift on Psi, that lift must be owned and observable-trivial.",
            "mathematical_form": "delta_v Psi_A = rho_A(lambda_v) Psi_A or L_xi Psi_A, with delta_v S_A = boundary/gauge and all observables invariant",
            "derives_if_signed": "gauge vertical motion can be quotient-trivial without freezing Psi by hand",
            "current_status": "standard_form_allowed_not_parent_signed",
            "blocker": "no parent map currently assigns v to a specific gauge/representation lift for every ordinary matter species",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MVA761_3_no_physical_species_lift",
            "vertical_action_clause": "A vertical representative motion may not change species constants, charge normalization, mass ratios, or material markers unless those are retained residual fields.",
            "mathematical_form": "delta_v theta_A=0 or theta_A is moved into R_phys/coupling residual source pack",
            "derives_if_signed": "direct species/clock/EM/source marker spurions cannot fake quotient descent",
            "current_status": "not_parent_signed",
            "blocker": "constant-superselection/no-marker theorem remains open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MVA761_4_boundary_of_matter_domain",
            "vertical_action_clause": "Vertical action on matter domain must specify compact-support, boundary, and edge-current behaviour.",
            "mathematical_form": "delta_v S_matter = bulk_v + dB_v, with B_v owned gauge/topological or zero projected",
            "derives_if_signed": "Lie_v S_matter can be evaluated without hiding edge coupling residuals",
            "current_status": "not_parent_signed",
            "blocker": "boundary projection silence is still a separate open descent gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "MVA761_5_evaluability_verdict",
            "vertical_action_clause": "Can we evaluate Lie_v S_matter for current MTS ordinary matter?",
            "mathematical_form": "MVA761_0..MVA761_4 jointly sign a matter-domain action of ker(Dq)",
            "derives_if_signed": "the quotient descent test becomes well-defined",
            "current_status": "parent_matter_vertical_action_not_signed",
            "blocker": "matter category, fixed/gauge lift choice, constants/markers, and boundary action are unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def evaluability_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "LEV761_0_fixed_Psi_chain_rule",
            "test": "Assume delta_v Psi=0 and delta_v theta=0.",
            "result": "conditional_evaluable",
            "what_follows": "Lie_v S_matter = (delta S/d e_m) Lie_v e_m + connection/measure/boundary terms",
            "what_remains": "geometry stack descent and boundary silence still required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "LEV761_1_gauge_lift_chain_rule",
            "test": "Assume delta_v Psi is a parent-owned gauge/representation lift.",
            "result": "conditional_evaluable",
            "what_follows": "matter variation is E_Psi delta_v Psi plus gauge/boundary terms, zero on matter EOM if lift is true gauge",
            "what_remains": "parent must specify lift for every ordinary species and prove observables invariant",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "LEV761_2_physical_lift",
            "test": "Allow delta_v Psi to change physical species, charge, phase, marker, or source labels.",
            "result": "not_descent",
            "what_follows": "v is no longer invisible to ordinary matter; coupling residual/source-pack row is required",
            "what_remains": "classify as retained physical field, bounded coefficient, or forbidden branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "LEV761_3_current_corpus",
            "test": "Evaluate Lie_v S_matter using current corpus alone.",
            "result": "not_evaluable_as_parent_theorem",
            "what_follows": "descent cannot be promoted because the vertical action on matter is not parent-signed",
            "what_remains": "write source-fill schema and move next to geometry stack descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def counterexample_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "VCE761_0_marker_lift",
            "legal_if_unsigned": "theta_A or material marker m_A transforms along v",
            "mathematical_form": "delta_v theta_A != 0 while e_obs is quotient-blind",
            "effect": "Lie_v S_matter returns through constants/readout markers",
            "blocks": "direct species/clock/EM/source coupling zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "VCE761_1_common_Weyl_frame",
            "legal_if_unsigned": "matter metric contains representative A_g(X)^2 factor",
            "mathematical_form": "g_matter=A_g(X)^2 g_obs with Dq[v_X]=0 but Lie_v A_g != 0",
            "effect": "common c_g source survives even for universal matter",
            "blocks": "c_g=0 and R10/PPN/clock/orbital coupling silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "VCE761_2_species_dependent_lift",
            "legal_if_unsigned": "different matter species carry different vertical representation weights",
            "mathematical_form": "delta_v Psi_A = rho_A(v) Psi_A with rho_A not pure gauge/universal",
            "effect": "WEP/composition residual is a real coupling channel",
            "blocks": "universal source and species charge zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "counterexample_id": "VCE761_3_edge_current",
            "legal_if_unsigned": "vertical matter variation is exact in bulk but carries boundary projection",
            "mathematical_form": "Lie_v S_matter = int_boundary B_v with nonzero local projection",
            "effect": "bulk quotient silence does not imply local source/readout silence",
            "blocks": "boundary/harmonic coupling and q_H silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "CSF761_0_vertical_action_source",
            "artifact": "future_parent_matter_vertical_action_certificate.csv",
            "required_columns": "species_or_sector;bundle_owner;vertical_rule;fixed_or_gauge_lift;observable_invariant;source_path;valid_for_claim",
            "claim_gate": "every ordinary matter sector has a parent-signed vertical action rule",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF761_1_coupling_descent_candidate",
            "artifact": str(COUPLING_DESCENT_CANDIDATE_PATH),
            "required_columns": "sector;functional;uses_e_obs;uses_q_of_Phi;hidden_frame_map;species_label_dependence;source_path;valid_for_claim",
            "claim_gate": "vertical action plus q/e_obs descent proves no hidden coupling map",
            "current_status": f"schema_only_candidate_missing={bool_string(not COUPLING_DESCENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF761_2_cg_bound_input",
            "artifact": str(CG_SOURCE_CANDIDATE_PATH),
            "required_columns": "coefficient_id;arena;c_g_or_equivalent;lambda_or_scale;bound_value;units;source_path;valid_for_claim",
            "claim_gate": "c_g theorem-zero from descent or sourced numeric bound",
            "current_status": f"schema_only_candidate_missing={bool_string(not CG_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF761_3_EM_charge_interface",
            "artifact": str(EM_INTERFACE_CANDIDATE_PATH),
            "required_columns": "sector;charge_current_owner;metric_or_coframe_used;normalization;alpha_or_charge_response;source_path;valid_for_claim",
            "claim_gate": "charge/current variables have parent-signed vertical rule and no hidden X-dependent normalization",
            "current_status": f"schema_only_candidate_missing={bool_string(not EM_INTERFACE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "CSF761_4_marker_constant_source",
            "artifact": "future_marker_constant_vertical_source_rows.csv",
            "required_columns": "marker_or_constant;sector;vertical_derivative;classification;bound_or_zero_certificate;source_path;valid_for_claim",
            "claim_gate": "theta/marker channels are selector-trivial, pure gauge, retained, or bounded",
            "current_status": "schema_only_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D761_0_best_route",
            "decision": "attack parent matter-domain vertical action before bound rows",
            "reason": "without a vertical action on Psi/theta, Lie_v S_matter cannot be evaluated as a theorem",
            "claim_status": "best_route_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D761_1_contract",
            "decision": "write fixed-Psi/gauge-lift vertical action contract",
            "reason": "these are the only clean non-cheat ways for representative motion to be matter-invisible",
            "claim_status": "contract_written_not_parent_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D761_2_promotion",
            "decision": "do not promote quotient descent or c_g=0",
            "reason": "matter-domain vertical action remains unsigned and counterexamples remain legal",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU761_0_allowed",
            "allowed_after_761": "say fixed-Psi or owned gauge-lift are the clean vertical-action options",
            "forbidden_after_761": "evaluate Lie_v S_matter as parent theorem without signing one of those options",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU761_1_allowed",
            "allowed_after_761": "move to geometry-stack descent because vertical action is now contract-shaped",
            "forbidden_after_761": "claim c_g=0 before measure/coframe/connection descent and no-marker clauses close",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU761_2_allowed",
            "allowed_after_761": "keep coupling source-fill rows schema-only until sourced",
            "forbidden_after_761": "mark vertical-action, coupling, c_g, marker, or EM rows valid_for_claim from placeholders",
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
            "main_result": "best route chosen; vertical-action contract written but not parent-signed",
            "hard_blocker": "ordinary matter bundle action/fixed-Psi or gauge-lift rule is not derived from parent action",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    vertical: list[dict[str, Any]],
    evaluability: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V761_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V761_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_760 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_760_VALIDATION.csv")
    validation.append({"check_id": "V761_2_prior_760_clean", "result": "pass" if prior_760 and all(row.get("result") == "pass" for row in prior_760) else "fail", "detail": "760 validation has no failures"})
    validation.append({"check_id": "V761_3_vertical_contract_written", "result": "pass" if len(vertical) == 6 and any(row["contract_id"] == "MVA761_5_evaluability_verdict" for row in vertical) else "fail", "detail": "vertical action contract rows present"})
    validation.append({"check_id": "V761_4_vertical_not_parent_signed", "result": "pass" if any(row["contract_id"] == "MVA761_5_evaluability_verdict" and row["current_status"] == "parent_matter_vertical_action_not_signed" for row in vertical) else "fail", "detail": "vertical action remains nonclaim"})
    validation.append({"check_id": "V761_5_evaluability_blocked", "result": "pass" if any(row["audit_id"] == "LEV761_3_current_corpus" and row["result"] == "not_evaluable_as_parent_theorem" for row in evaluability) else "fail", "detail": "Lie_v S_matter not theorem-evaluable"})
    validation.append({"check_id": "V761_6_counterexamples_retained", "result": "pass" if len(counterexamples) == 4 and all(row["valid_for_claim"] == "false" for row in counterexamples) else "fail", "detail": "counterexamples remain legal while unsigned"})
    validation.append({"check_id": "V761_7_source_fill_schema_written", "result": "pass" if len(source_fill) == 5 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    validation.append({"check_id": "V761_8_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in [COUPLING_DESCENT_CANDIDATE_PATH, CG_SOURCE_CANDIDATE_PATH, EM_INTERFACE_CANDIDATE_PATH]) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = vertical + evaluability + counterexamples + source_fill + decisions + routes + summary
    validation.append({"check_id": "V761_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V761_10_no_local_arena_claim", "result": "pass" if "no_quotient_descent_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V761_11_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        VERTICAL_ACTION_PATH,
        EVALUABILITY_AUDIT_PATH,
        COUNTEREXAMPLE_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V761_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V761_13_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V761_14_geometry_stack_next", "result": "pass" if "geometry-stack-descent" in NEXT_TARGET else "fail", "detail": "next attacks measure/coframe/connection descent"})
    validation.append({"check_id": "V761_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    vertical: list[dict[str, Any]],
    evaluability: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 761 - Y5 R10 Parent Matter-Domain Vertical Action Or Coupling Source Fill

Start point: 760 showed that quotient matter descent cannot be evaluated until the parent says what a vertical representative motion does to ordinary matter variables.

Current result: **the best route is the parent matter-domain vertical-action contract, but it is not parent-signed yet**. The clean options are narrow: either `Psi_A` and `theta_A` are fixed while only representative parent geometry moves, or `Psi_A` is lifted by an owned gauge/representation action that is observable-trivial. Any physical species, marker, charge, boundary, or readout change is a coupling residual, not quotient descent.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Parent Matter Vertical-Action Contract

{markdown_table(vertical, ["contract_id", "vertical_action_clause", "mathematical_form", "derives_if_signed", "current_status", "blocker", "valid_for_claim"])}

## Lie_v S_matter Evaluability Audit

{markdown_table(evaluability, ["audit_id", "test", "result", "what_follows", "what_remains", "valid_for_claim"])}

## Vertical-Action Counterexample Ledger

{markdown_table(counterexamples, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "blocks", "valid_for_claim"])}

## Coupling Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_761", "forbidden_after_761", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is the right route because it attacks the first evaluability problem. We now know what the parent must say before quotient descent can be tested. But it is still a contract, not a proof. The next clean target is geometry-stack descent: even with a fixed/gauge-lifted `Psi`, rods, clocks, measure, coframe, connection, and derivative operator must also factor through the quotient.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    vertical = vertical_action_rows(generated_utc)
    evaluability = evaluability_rows(generated_utc)
    counterexamples = counterexample_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, vertical, evaluability, counterexamples, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(VERTICAL_ACTION_PATH, vertical, ["contract_id", "vertical_action_clause", "mathematical_form", "derives_if_signed", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(EVALUABILITY_AUDIT_PATH, evaluability, ["audit_id", "test", "result", "what_follows", "what_remains", "valid_for_claim", "generated_utc"])
    write_csv(COUNTEREXAMPLE_PATH, counterexamples, ["counterexample_id", "legal_if_unsigned", "mathematical_form", "effect", "blocks", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_761", "forbidden_after_761", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, vertical, evaluability, counterexamples, source_fill, decisions, routes, summary, validation)

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
