from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "758-Y5-R10-full-residual-vector-parent-action-contract-or-component-input-acquisition.md"
NEXT_TARGET = "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md"
STATUS = "Y5_R10_758_full_residual_vector_parent_action_contract_written_not_parent_signed_component_input_acquisition_ledger_opened"
CLAIM_CEILING = "parent_action_contract_and_acquisition_ledger_only_no_q_loc_zero_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_758_SOURCE_REGISTER.csv"
PARENT_ACTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_758_PARENT_ACTION_CONTRACT_ATTEMPT.csv"
LOCK_GATE_PATH = RESIDUALS / "P8_Y5_R10_758_FULL_RESIDUAL_VECTOR_LOCK_GATE.csv"
ACQUISITION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_758_COMPONENT_INPUT_ACQUISITION_LEDGER.csv"
EXIT_CRITERIA_PATH = RESIDUALS / "P8_Y5_R10_758_CHANNEL_EXIT_CRITERIA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_758_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_758_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_758_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_758_VALIDATION.csv"

QLOC_COMPONENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv"
PFLUX_PROJECTOR_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_PFLUX_PROJECTOR_INPUT.csv"
ALPHA3_RESPONSE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_RESPONSE_OPERATOR_INPUT.csv"
ALPHA3_PRODUCT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_755_ALPHA3_PRODUCT_INPUT.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "757_doc": {
        "path": POST_CHECKPOINT / "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
        "needles": [
            "Current result: **the physical lock is not proved**",
            "758-Y5-R10-full-residual-vector-parent-action-contract-or-component-input-acquisition.md",
        ],
        "role": "immediate 758 handoff",
    },
    "757_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_757_VALIDATION.csv",
        "needles": ["V757_16_validation_rows_ready", "V757_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "757_contract": {
        "path": RESIDUALS / "P8_Y5_R10_757_PHYSICAL_LOCK_CONTRACT.csv",
        "needles": ["PLC757_0_physical_residual_bundle", "PLC757_5_zero_theorem"],
        "role": "full residual-vector lock contract",
    },
    "757_basis": {
        "path": RESIDUALS / "P8_Y5_R10_757_RESIDUAL_VECTOR_BASIS.csv",
        "needles": ["RVB757_0_q_loc_vector", "RVB757_5_matter_coupling"],
        "role": "physical residual basis",
    },
    "757_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_757_PHYSICAL_LOCK_ATTEMPT.csv",
        "needles": ["PLA757_6_verdict", "physical_lock_not_proved"],
        "role": "formal Z route rejection",
    },
    "757_component_decision": {
        "path": RESIDUALS / "P8_Y5_R10_757_QLOC_COMPONENT_INPUT_DECISION.csv",
        "needles": ["QCI757_0_no_q_loc_candidate_written", "do not fabricate component rows"],
        "role": "component-input fallback guard",
    },
    "518_doc": {
        "path": POST_CHECKPOINT / "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "needles": ["Y5O_8_owner_theorem", "theorem_written_current_MTS_does_not_satisfy_premises"],
        "role": "Y5 owner theorem premises",
    },
    "519_doc": {
        "path": POST_CHECKPOINT / "519-fill-Y5-bound-runner-or-source-owner-clause.md",
        "needles": ["UOC519_4_diffeomorphism_Ward_identity", "D519_3_source_measure"],
        "role": "same-coframe coupling clause and remaining source-measure gap",
    },
    "520_doc": {
        "path": POST_CHECKPOINT / "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "needles": ["WB520_6_conditional_closure_theorem", "WO520_5_ad_hoc_multiplier"],
        "role": "Ward source-current closure and ad hoc multiplier warning",
    },
    "750_component_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
        "needles": ["QIN750_3_q_loc_components", "component-resolved q_loc field/profile"],
        "role": "q_loc component input schema",
    },
    "750_hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "Hodge/alpha3 component runner schema",
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


def parent_action_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PAC758_0_action_skeleton",
            "clause": "Write a parent action whose variables are the observed geometry, matter, and residual-sector fields before local readout.",
            "mathematical_form": "S_parent = S_EH[g_obs] + S_matter[g_obs/e_obs,Psi] + S_res[g_obs,R_phys,U] + S_boundary + S_gauge",
            "acceptance_test": "R_phys is derived from variations/noether maps of owned fields, not inserted after the fact as a fitted readout residual.",
            "current_status": "skeleton_written_not_parent_signed",
            "risk_if_missing": "residual norm becomes closure machinery rather than a field theory",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC758_1_residual_norm",
            "clause": "The residual sector must be coercive on the full physical residual vector.",
            "mathematical_form": "S_res contains 1/2 int sqrt(-g) R_phys^I G_IJ R_phys^J with G_IJ positive after gauge/constraint quotient.",
            "acceptance_test": "c_- ||R_phys||^2 <= R_phys^I G_IJ R_phys^J and every q_loc/Y5/Y6/PPN/boundary/coupling channel has nonzero weight or theorem-zero owner.",
            "current_status": "contract_written_not_derived",
            "risk_if_missing": "one channel can hide in the nullspace while the action looks quiet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC758_2_Euler_no_source_work",
            "clause": "Compact-local Euler equations must have no source or boundary work in the residual directions.",
            "mathematical_form": "L_IJ R_phys^J = J_I + B_I, with J_I=0 and B_I=0 by parent Ward/charge/boundary identities.",
            "acceptance_test": "Y5 source current, Y6 extra stress, q_H boundary flux, and matter-coupling terms are each zero-owned or carried as bounded residuals.",
            "current_status": "not_parent_signed",
            "risk_if_missing": "positive norm does not force zero if sources/boundaries drive it",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC758_3_universal_coupling_owner",
            "clause": "The parent action must own the single observed coupling/readout structure.",
            "mathematical_form": "S_matter = Sbar[e_obs,Psi] and S_readout = S_readout[e_obs,source,orbit,clock,photon] with no hidden conformal/disformal/species/source-frame maps.",
            "acceptance_test": "same coframe plus quotient-invariant matter/source/readout descent closes species, clock, photon, source, and orbit coupling residuals.",
            "current_status": "partial_same_coframe_only",
            "risk_if_missing": "this is the coupling leak: a good-looking gravity sector can still fail WEP, clocks, source GM, EM/readout, or PPN",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC758_4_no_ad_hoc_constraint",
            "clause": "Do not add a Lagrange multiplier or penalty solely to impose the target GR residual equation.",
            "mathematical_form": "S_parent must not contain arbitrary lambda_I R_phys^I or lambda_M d(Pi_M J_H) unless lambda_I is gauge/topological/Ward-owned by the parent structure.",
            "acceptance_test": "the zero follows from symmetry, positive energy, owned charge closure, or sourced field equations; not from a bolt-on zero condition.",
            "current_status": "guardrail_active",
            "risk_if_missing": "the derivation becomes a disguised plateau axiom",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC758_5_verdict",
            "clause": "Promote full residual-vector parent action to current MTS proof.",
            "mathematical_form": "PAC758_0..PAC758_4 close and validate against PLC757_0..PLC757_5.",
            "acceptance_test": "R_phys=0 theorem follows for the measured channels and all source paths are parent-owned.",
            "current_status": "not_promoted_current_corpus",
            "risk_if_missing": "must use component/residual acquisition path",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def lock_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "FLG758_0_q_loc",
            "physical_channel": "q_loc vector / alpha3-sensitive leakage",
            "parent_action_requirement": "Gamma_eff/K_hat/P_loc arise from owned action variables and give component q_loc^nu in observed frame.",
            "status_after_758": "not_closed",
            "required_evidence_or_input": "theorem-zero q_loc or P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv with sourced q0..q3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "FLG758_1_Y5",
            "physical_channel": "source-normalization / measured GM",
            "parent_action_requirement": "source current closure, no extra mass projection, Gauss/orbital calibration, and PPN source stability.",
            "status_after_758": "not_closed",
            "required_evidence_or_input": "parent-signed Y5O_1..Y5O_8 or channelwise source-normalization residual rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "FLG758_2_Y6",
            "physical_channel": "extra stress / local exterior metric",
            "parent_action_requirement": "all non-EH stress is either topological/improvement-invisible or included in the residual norm with positive control.",
            "status_after_758": "not_closed",
            "required_evidence_or_input": "Y6 stress decomposition and PPN beta/gamma/lensing response operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "FLG758_3_PPN",
            "physical_channel": "full weak-field coefficient vector",
            "parent_action_requirement": "linear response from R_phys to {gamma,beta,alpha_i,xi,zeta_i,Gdot,R11} is sourced and full-rank or theorem-zero.",
            "status_after_758": "not_closed",
            "required_evidence_or_input": "PPN response matrix W_A_I with source convention and bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "FLG758_4_boundary",
            "physical_channel": "boundary/harmonic flux",
            "parent_action_requirement": "boundary and Hodge pieces are included in K_gamma/residual norm or killed by a compact no-flux theorem.",
            "status_after_758": "not_closed",
            "required_evidence_or_input": "P_flux/Hodge projector, boundary operator, or no-flux theorem certificate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "FLG758_5_coupling",
            "physical_channel": "matter/source/readout coupling",
            "parent_action_requirement": "one parent-owned e_obs/g_obs descends to matter, clocks, photons, source charge, orbit readout, and EM/charge interface.",
            "status_after_758": "partial_only",
            "required_evidence_or_input": "quotient-invariant matter action plus source/readout descent and coupling residual rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def acquisition_ledger_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "acquisition_id": "AIL758_0_q_loc_components",
            "artifact_or_dataset": str(QLOC_COMPONENT_CANDIDATE_PATH),
            "required_columns_or_source": "sample_id;domain_id;weight_dV;frame_convention;u0..u3;q0..q3;boundary_tag;boundary_condition;source_path",
            "purpose": "compute or theorem-check q_loc vector and alpha3-sensitive component fractions",
            "current_status": f"missing_exists={bool_string(QLOC_COMPONENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "AIL758_1_Hodge_flux_projector",
            "artifact_or_dataset": str(PFLUX_PROJECTOR_CANDIDATE_PATH),
            "required_columns_or_source": "projector_id;domain_id;boundary_operator;P_flux_formula;normalization;q_proxy_denominator;units;source_path",
            "purpose": "separate gradient/transverse/harmonic q_loc and produce f_qV without scalar proxy cheating",
            "current_status": f"missing_exists={bool_string(PFLUX_PROJECTOR_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "AIL758_2_alpha3_response_operator",
            "artifact_or_dataset": str(ALPHA3_RESPONSE_CANDIDATE_PATH),
            "required_columns_or_source": "operator_id;G_PPN_source_to_g0i;Pi_alpha3_extraction;gauge;frame;units;source_path",
            "purpose": "map q_loc component fractions to alpha3 in the same frame/gauge convention",
            "current_status": f"missing_exists={bool_string(ALPHA3_RESPONSE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "AIL758_3_Y5_source_normalization",
            "artifact_or_dataset": "future_Y5_source_normalization_residual_rows",
            "required_columns_or_source": "Gdot;Mdot;radial_flux;species_charge;range_dependence;frame_split;mu_extra;PPN_source_terms;source_path",
            "purpose": "bound or derive source-normalized Newton rather than hiding measured GM in calibration",
            "current_status": "source_rows_needed_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "AIL758_4_Y6_extra_stress",
            "artifact_or_dataset": "future_Y6_extra_stress_response_rows",
            "required_columns_or_source": "stress_component;conservation_status;topological_or_bulk;PPN_beta_gamma_response;lensing_response;source_path",
            "purpose": "prevent conserved exchange-even stress from bypassing q_loc while changing the metric",
            "current_status": "source_rows_needed_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "acquisition_id": "AIL758_5_coupling_descent",
            "artifact_or_dataset": "future_coupling_descent_residual_rows",
            "required_columns_or_source": "sector;matter_species;clock;photon;source_charge;orbit;EM_charge_interface;frame_map;source_path",
            "purpose": "turn the coupling gut-feel into a source-backed descent/violation ledger",
            "current_status": "source_rows_needed_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def exit_criteria_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "exit_id": "EX758_0_theorem_route",
            "route": "parent-action proof",
            "exit_condition": "PAC758_0..PAC758_5 and FLG758_0..FLG758_5 close with source paths and no ad hoc closure terms",
            "if_met": "promote to a local silence theorem candidate for q_loc/Y5/Y6/PPN/coupling",
            "if_not_met": "continue acquisition ledger",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "exit_id": "EX758_1_component_route",
            "route": "real residual input route",
            "exit_condition": "AIL758_0..AIL758_5 receive sourced rows with units, conventions, and no placeholder markers",
            "if_met": "run q_loc/Hodge/PPN/source-normalization comparator instead of theorem promotion",
            "if_not_met": "all local claims remain blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "exit_id": "EX758_2_alpha3_gate",
            "route": "preferred-frame product",
            "exit_condition": f"P_flux P_Hodge q_loc=0 theorem or abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g} from sourced rows",
            "if_met": "alpha3 branch can be scored but still not full local GR by itself",
            "if_not_met": "alpha3 remains blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D758_0_parent_action",
            "decision": "full residual-vector parent action contract is written but not parent-signed",
            "reason": "the contract is mathematically clean, but current corpus has not derived the residual fields, coupling descent, positivity, no-source work, or no-boundary work",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D758_1_no_ad_hoc_closure",
            "decision": "reject bolt-on residual multipliers as a derivation",
            "reason": "a multiplier that imposes d(Pi_M J_H)=0 or R_phys=0 solely to recover GR is a closure axiom unless Ward/topological/gauge-owned",
            "claim_status": "guardrail_active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D758_2_acquisition",
            "decision": "open component/residual acquisition ledger",
            "reason": "if the theorem route cannot close immediately, the honest next move is sourced local residual inputs and response operators",
            "claim_status": "acquisition_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU758_0_allowed",
            "allowed_after_758": "use PAC758 as the stricter parent-action contract for derived local GR",
            "forbidden_after_758": "treat the contract itself as a proof",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU758_1_allowed",
            "allowed_after_758": "say the coupling problem is now a concrete action/descent requirement",
            "forbidden_after_758": "hide matter/source/readout coupling residuals behind gravity-sector silence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU758_2_allowed",
            "allowed_after_758": "start acquiring real component/residual inputs under AIL758 if theorem rows remain unsigned",
            "forbidden_after_758": "create placeholder q_loc, alpha3, Y5, Y6, or coupling rows marked valid_for_claim=true",
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
            "main_result": "parent-action contract sharpened; not proved; component/residual acquisition ledger opened",
            "hard_blocker": "no parent-signed full residual vector, no universal coupling descent, no real q_loc component/operator inputs",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    parent_action: list[dict[str, Any]],
    lock_gate: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    exits: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V758_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V758_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_757 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_757_VALIDATION.csv")
    validation.append({"check_id": "V758_2_prior_757_clean", "result": "pass" if prior_757 and all(row.get("result") == "pass" for row in prior_757) else "fail", "detail": "757 validation has no failures"})
    validation.append({"check_id": "V758_3_parent_action_contract_written", "result": "pass" if len(parent_action) == 6 and any(row["contract_id"] == "PAC758_5_verdict" for row in parent_action) else "fail", "detail": "PAC758 contract rows present"})
    validation.append({"check_id": "V758_4_parent_action_not_promoted", "result": "pass" if any(row["contract_id"] == "PAC758_5_verdict" and row["current_status"] == "not_promoted_current_corpus" for row in parent_action) else "fail", "detail": "contract is nonclaim"})
    validation.append({"check_id": "V758_5_no_ad_hoc_closure_guard", "result": "pass" if any(row["contract_id"] == "PAC758_4_no_ad_hoc_constraint" for row in parent_action) and any(row["decision_id"] == "D758_1_no_ad_hoc_closure" for row in decisions) else "fail", "detail": "bolt-on closure terms rejected"})
    validation.append({"check_id": "V758_6_full_lock_gates_present", "result": "pass" if len(lock_gate) == 6 and all(row["status_after_758"] in {"not_closed", "partial_only"} for row in lock_gate) else "fail", "detail": "six physical lock gates retained"})
    validation.append({"check_id": "V758_7_acquisition_ledger_open", "result": "pass" if len(acquisition) == 6 and all(row["valid_for_claim"] == "false" for row in acquisition) else "fail", "detail": "component/residual acquisition rows are nonclaim"})
    validation.append({"check_id": "V758_8_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in [QLOC_COMPONENT_CANDIDATE_PATH, PFLUX_PROJECTOR_CANDIDATE_PATH, ALPHA3_RESPONSE_CANDIDATE_PATH, ALPHA3_PRODUCT_CANDIDATE_PATH]) else "fail", "detail": "no claim-input artifacts fabricated"})
    validation.append({"check_id": "V758_9_exit_criteria_nonclaim", "result": "pass" if len(exits) == 3 and all(row["valid_for_claim"] == "false" for row in exits) else "fail", "detail": "exit routes recorded without claim promotion"})
    all_generated = parent_action + lock_gate + acquisition + exits + decisions + routes + summary
    validation.append({"check_id": "V758_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V758_11_no_local_arena_claim", "result": "pass" if "no_q_loc_zero_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local claims remain blocked"})
    validation.append({"check_id": "V758_12_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PARENT_ACTION_CONTRACT_PATH,
        LOCK_GATE_PATH,
        ACQUISITION_LEDGER_PATH,
        EXIT_CRITERIA_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V758_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V758_14_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V758_15_coupling_descent_explicit", "result": "pass" if any(row["contract_id"] == "PAC758_3_universal_coupling_owner" for row in parent_action) and any(row["acquisition_id"] == "AIL758_5_coupling_descent" for row in acquisition) else "fail", "detail": "coupling owner and acquisition lane explicit"})
    validation.append({"check_id": "V758_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    parent_action: list[dict[str, Any]],
    lock_gate: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    exits: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 758 - Y5 R10 Full Residual-Vector Parent Action Contract Or Component Input Acquisition

Start point: 757 showed that the response-doublet cannot be promoted unless it controls the whole measured residual vector.

Current result: **the stronger parent-action contract can be written, but it is not yet parent-signed**. The least-cheaty route is a full residual-vector action/descent theorem: `R_phys=0` must follow from owned fields, universal coupling, positive/coercive residual norm, and no source/boundary work. A bolt-on multiplier that simply enforces the desired GR limit is rejected as closure-only. Because the theorem route is not closed here, 758 opens the component/residual acquisition ledger.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Parent-Action Contract Attempt

{markdown_table(parent_action, ["contract_id", "clause", "mathematical_form", "acceptance_test", "current_status", "risk_if_missing", "valid_for_claim"])}

## Full Residual-Vector Lock Gate

{markdown_table(lock_gate, ["gate_id", "physical_channel", "parent_action_requirement", "status_after_758", "required_evidence_or_input", "valid_for_claim"])}

## Component / Residual Acquisition Ledger

{markdown_table(acquisition, ["acquisition_id", "artifact_or_dataset", "required_columns_or_source", "purpose", "current_status", "valid_for_claim"])}

## Exit Criteria

{markdown_table(exits, ["exit_id", "route", "exit_condition", "if_met", "if_not_met", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_758", "forbidden_after_758", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a narrowing in the good sense. The theory route is now stricter: a parent action must own the residual vector and the coupling/readout map, not just make an auxiliary field quiet. That makes the target harder, but also less vulnerable to scrutiny. If the coupling owner can be derived, we have a serious route. If not, the next honest move is acquisition: source-backed component `q_loc`, Hodge/flux operator, PPN response, Y5/Y6 residuals, and coupling descent rows.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    parent_action = parent_action_contract_rows(generated_utc)
    lock_gate = lock_gate_rows(generated_utc)
    acquisition = acquisition_ledger_rows(generated_utc)
    exits = exit_criteria_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, parent_action, lock_gate, acquisition, exits, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_ACTION_CONTRACT_PATH, parent_action, ["contract_id", "clause", "mathematical_form", "acceptance_test", "current_status", "risk_if_missing", "valid_for_claim", "generated_utc"])
    write_csv(LOCK_GATE_PATH, lock_gate, ["gate_id", "physical_channel", "parent_action_requirement", "status_after_758", "required_evidence_or_input", "valid_for_claim", "generated_utc"])
    write_csv(ACQUISITION_LEDGER_PATH, acquisition, ["acquisition_id", "artifact_or_dataset", "required_columns_or_source", "purpose", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(EXIT_CRITERIA_PATH, exits, ["exit_id", "route", "exit_condition", "if_met", "if_not_met", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_758", "forbidden_after_758", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, parent_action, lock_gate, acquisition, exits, decisions, routes, summary, validation)

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
