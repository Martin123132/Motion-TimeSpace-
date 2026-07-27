from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md"
NEXT_TARGET = "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md"
STATUS = "Y5_R10_759_coupling_owner_action_not_parent_signed_partial_coupling_theorem_contract_written_residual_acquisition_runner_opened"
CLAIM_CEILING = "coupling_owner_action_audit_and_residual_acquisition_runner_only_no_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_759_SOURCE_REGISTER.csv"
COUPLING_OWNER_PATH = RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv"
PARTIAL_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_759_PARTIAL_COUPLING_THEOREM_CONTRACT.csv"
ACQUISITION_RUNNER_PATH = RESIDUALS / "P8_Y5_R10_759_COUPLING_RESIDUAL_ACQUISITION_RUNNER.csv"
IMPACT_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_759_RESIDUAL_VECTOR_IMPACT_MATRIX.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_759_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_759_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_759_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_759_VALIDATION.csv"

COUPLING_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_COUPLING_DESCENT_INPUT_CANDIDATE.csv"
CG_SOURCE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_CG_COUPLING_BOUND_INPUT_CANDIDATE.csv"
EM_INTERFACE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_EM_CHARGE_INTERFACE_INPUT_CANDIDATE.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "758_doc": {
        "path": POST_CHECKPOINT / "758-Y5-R10-full-residual-vector-parent-action-contract-or-component-input-acquisition.md",
        "needles": [
            "Current result: **the stronger parent-action contract can be written, but it is not yet parent-signed**",
            "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        ],
        "role": "immediate 759 handoff",
    },
    "758_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_758_VALIDATION.csv",
        "needles": ["V758_16_validation_rows_ready", "V758_14_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "758_parent_action": {
        "path": RESIDUALS / "P8_Y5_R10_758_PARENT_ACTION_CONTRACT_ATTEMPT.csv",
        "needles": ["PAC758_3_universal_coupling_owner", "PAC758_4_no_ad_hoc_constraint"],
        "role": "universal coupling owner and anti-closure guard",
    },
    "758_acquisition": {
        "path": RESIDUALS / "P8_Y5_R10_758_COMPONENT_INPUT_ACQUISITION_LEDGER.csv",
        "needles": ["AIL758_5_coupling_descent", "turn the coupling gut-feel into a source-backed descent/violation ledger"],
        "role": "coupling acquisition handoff",
    },
    "757_basis": {
        "path": RESIDUALS / "P8_Y5_R10_757_RESIDUAL_VECTOR_BASIS.csv",
        "needles": ["RVB757_5_matter_coupling", "same-coframe clause is partial"],
        "role": "matter-coupling residual vector basis",
    },
    "519_doc": {
        "path": POST_CHECKPOINT / "519-fill-Y5-bound-runner-or-source-owner-clause.md",
        "needles": ["UOC519_0_single_coframe_field", "UOC519_5_no_conformal_disformal_shadow_frame"],
        "role": "same-coframe coupling clause",
    },
    "520_doc": {
        "path": POST_CHECKPOINT / "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "needles": ["WB520_0_same_frame_source_current", "WO520_3_extra_mass_projection"],
        "role": "source-current and mass-projection obstruction",
    },
    "627_doc": {
        "path": POST_CHECKPOINT / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md",
        "needles": ["S_matter = Sbar_matter[q(Phi),Psi,theta]", "c_g=0 not promoted"],
        "role": "quotient matter descent and c_g blocker",
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


def coupling_owner_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "COA759_0_single_observed_geometry",
            "coupling_clause": "One observed coframe/metric carries matter, clocks, photons, source current, orbit readout, and local residual response.",
            "mathematical_form": "e_obs := e_matter := e_source := e_clock := e_photon := e_orbit; g_obs=e_obs^T eta e_obs",
            "what_it_would_close": "frame-split source/readout residuals",
            "current_status": "conditional_from_519_not_current_MTS_derived",
            "blocker": "single coframe is a clause, not yet a parent-signed descent theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "COA759_1_quotient_matter_descent",
            "coupling_clause": "Matter action descends through the parent quotient, not through representative Weyl/disformal/local labels.",
            "mathematical_form": "S_matter[Phi_parent,Psi] = Sbar_matter[q(Phi_parent),Psi,theta] and Lie_v S_matter=0 for v in ker(Dq)",
            "what_it_would_close": "direct representative c_g/b_g/Weyl/disformal matter leakage",
            "current_status": "not_parent_signed_627_failed",
            "blocker": "quotient map, verticality, measure/coframe/connection descent, and boundary projection silence are not jointly proved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "COA759_2_species_constants",
            "coupling_clause": "Species constants in the matter action are not functions of local MTS/domain/source fields.",
            "mathematical_form": "partial_{Phi,D,kappa_local} m_A = partial_{Phi,D,kappa_local} q_A = 0 at fixed e_obs",
            "what_it_would_close": "direct nonmetric species source charge",
            "current_status": "conditional_from_519_not_dressed_source_proof",
            "blocker": "binding, field dressing, EM charge interface, and source-measure projection remain separate channels",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "COA759_3_source_current",
            "coupling_clause": "Hilbert/source current is defined before orbital measured-GM calibration.",
            "mathematical_form": "T_m^{mu nu}:=2/sqrt(-g_obs) delta S_matter/delta g_obs_mu_nu; J_H[tau]=T_m^{mu nu} tau_nu dSigma_mu",
            "what_it_would_close": "source current not being phenomenological",
            "current_status": "conditional_source_current_exists",
            "blocker": "Ward conservation does not close Pi_M J_H or measured GM without mass generator, Pi_M owner, zero commutator, zero exchange, and Gauss calibration",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "COA759_4_readout_descent",
            "coupling_clause": "Clock, photon, orbit, EM/charge, and source readouts are all functionals of the same observed structure.",
            "mathematical_form": "O_clock,O_photon,O_orbit,O_EM,O_source = O_A[e_obs,Psi_A,owned charges] with no hidden C(Phi), D(Phi), or source-frame map",
            "what_it_would_close": "clock/EM/orbit/readout coupling residuals",
            "current_status": "not_parent_signed",
            "blocker": "EM/charge interface and orbit/source calibration descent have not been written as parent-owned maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "COA759_5_no_ad_hoc_coupling_zero",
            "coupling_clause": "Do not set coupling residuals to zero by constraint unless the constraint is gauge/topological/Ward-owned.",
            "mathematical_form": "No arbitrary lambda_C Delta_coupling term may be used solely to recover WEP/clocks/Newton/PPN.",
            "what_it_would_close": "nothing by itself; it protects the proof standard",
            "current_status": "guardrail_active",
            "blocker": "without this guard, the coupling action becomes a disguised fit-to-GR axiom",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "COA759_6_verdict",
            "coupling_clause": "Promote universal coupling owner action to current MTS theorem.",
            "mathematical_form": "COA759_0..COA759_5 all close",
            "what_it_would_close": "direct coupling residual vector and c_g-like representative leakage",
            "current_status": "coupling_owner_not_parent_signed",
            "blocker": "central quotient matter descent and readout/source/EM descent remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def partial_theorem_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PCT759_0_frame_split",
            "conditional_statement": "If one parent-owned e_obs is used by source, clocks, photons, and orbit readout, then direct frame-split residuals vanish.",
            "mathematical_form": "e_source=e_clock=e_photon=e_orbit=e_obs => delta_frame_source=0",
            "status": "conditional_not_parent_signed",
            "not_enough_for": "M_eff closure, mu_extra=0, Gauss calibration, PPN stability",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PCT759_1_direct_species_charge",
            "conditional_statement": "If matter species pull back only through e_obs and fixed constants, direct MTS species charge is absent.",
            "mathematical_form": "partial_{Phi,D} S_A|e_obs = 0 => eta_source_AB^direct=0",
            "status": "conditional_not_dressed_source_proof",
            "not_enough_for": "binding/dressed source universality or WEP as a full source theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PCT759_2_representative_cg",
            "conditional_statement": "If matter action descends through q(Phi), representative Weyl/disformal coefficients do not enter matter rods/clocks.",
            "mathematical_form": "Lie_v S_matter=0 for v in ker(Dq) => c_g^rep=0 on vertical representative directions",
            "status": "not_parent_signed_627_blocked",
            "not_enough_for": "R10/PPN/clock/orbital pass unless descent, measure/coframe/connection, and boundary clauses are all signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PCT759_3_source_current",
            "conditional_statement": "Same-frame matter action gives a Hilbert source current and ordinary Ward conservation.",
            "mathematical_form": "delta_xi S_m=0 and E_psi=0 => nabla_mu T_m^{mu nu}=0",
            "status": "standard_conditional",
            "not_enough_for": "closed projected mass current d(Pi_M J_H)=0 or measured GM",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PCT759_4_EM_charge_interface",
            "conditional_statement": "EM/charge readout must descend through the same observed structure if charge is to be part of the unified coupling owner.",
            "mathematical_form": "S_EM and charge readout use e_obs and owned charge/current variables with no hidden MTS-dependent charge normalization",
            "status": "open",
            "not_enough_for": "fine-structure/charge/magnetic residual claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "PCT759_5_verdict",
            "conditional_statement": "Coupling route currently gives useful conditional zeros, not a full local-GR reduction.",
            "mathematical_form": "PCT759_0..PCT759_4 are not jointly parent-signed",
            "status": "partial_contract_only_no_claim",
            "not_enough_for": "c_g zero, q_loc zero, alpha3, PPN, Newton, or local GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def acquisition_runner_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "CAR759_0_coupling_descent_input",
            "artifact": str(COUPLING_DESCENT_CANDIDATE_PATH),
            "required_columns": "sector;functional;uses_e_obs;uses_q_of_Phi;hidden_frame_map;species_label_dependence;source_path;valid_for_claim",
            "claim_gate": "all sectors descend through e_obs/q(Phi); no hidden frame/species/readout map; source paths real",
            "current_status": f"candidate_missing_exists={bool_string(COUPLING_DESCENT_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "CAR759_1_cg_bound_input",
            "artifact": str(CG_SOURCE_CANDIDATE_PATH),
            "required_columns": "coefficient_id;arena;c_g_or_equivalent;lambda_or_scale;bound_value;units;source_path;valid_for_claim",
            "claim_gate": "c_g theorem-zero or sourced numeric bound input; no representative descent claim without 627 clauses",
            "current_status": f"candidate_missing_exists={bool_string(CG_SOURCE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "CAR759_2_EM_charge_interface",
            "artifact": str(EM_INTERFACE_CANDIDATE_PATH),
            "required_columns": "sector;charge_current_owner;metric_or_coframe_used;normalization;alpha_or_charge_response;source_path;valid_for_claim",
            "claim_gate": "EM/charge/fine-structure interface descends through same observed structure or is explicitly bounded",
            "current_status": f"candidate_missing_exists={bool_string(EM_INTERFACE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "CAR759_3_source_orbit_coupling",
            "artifact": "future_source_orbit_coupling_residual_rows",
            "required_columns": "source_current_owner;Pi_M_owner;orbit_readout_owner;Gauss_calibration;mu_extra_channel;source_path;valid_for_claim",
            "claim_gate": "same-frame source current plus closed projected mass channel and orbital calibration",
            "current_status": "source_rows_needed_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "CAR759_4_clock_photon_readout",
            "artifact": "future_clock_photon_readout_residual_rows",
            "required_columns": "clock_functional;photon_functional;frame_map;redshift_or_speed_response;source_path;valid_for_claim",
            "claim_gate": "clock/photon observables use e_obs with no independent local MTS frame map",
            "current_status": "source_rows_needed_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "CAR759_5_PPN_coupling_response",
            "artifact": "future_PPN_coupling_response_rows",
            "required_columns": "PPN_coefficient;coupling_channel;linear_response;gauge;frame;source_path;valid_for_claim",
            "claim_gate": "coupling residuals map to beta/gamma/alpha_i/xi/zeta_i/Gdot/R11 or are theorem-zero",
            "current_status": "source_rows_needed_not_claim_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def impact_matrix_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IM759_0_Y5",
            "residual_channel": "source-normalization Y5",
            "what_coupling_owner_can_help": "same e_obs defines source current before orbital fitting and kills direct frame split",
            "what_remains_open": "Pi_M owner, mass generator, commutator, extra projection, Gauss calibration, PPN stability",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "IM759_1_cg_R10",
            "residual_channel": "c_g / representative geometry coupling",
            "what_coupling_owner_can_help": "quotient matter descent would make representative Weyl/disformal coefficients invisible to matter",
            "what_remains_open": "627 descent clauses not parent-signed; bounds still source-needed",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "IM759_2_alpha3_q_loc",
            "residual_channel": "q_loc / alpha3",
            "what_coupling_owner_can_help": "same observed frame prevents frame-split hiding of preferred-frame terms",
            "what_remains_open": "q_loc component theorem/input, Hodge projector, PPN alpha3 operator",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "IM759_3_EM_charge",
            "residual_channel": "EM/charge interface",
            "what_coupling_owner_can_help": "forces EM/charge readout to declare whether it descends through e_obs and owned currents",
            "what_remains_open": "charge normalization/fine-structure response not in parent-signed coupling action",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "IM759_4_local_GR",
            "residual_channel": "full local GR",
            "what_coupling_owner_can_help": "removes a large class of hidden readout/coupling loopholes if signed",
            "what_remains_open": "Y5/Y6/PPN/q_loc/boundary residual gates remain unless full residual-vector action closes",
            "claim_status": "blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D759_0_coupling_owner",
            "decision": "coupling owner action is not parent-signed",
            "reason": "same-coframe clauses are useful but quotient matter descent, c_g silence, source/readout descent, and EM/charge interface remain unsigned",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D759_1_partial_theorem",
            "decision": "retain partial conditional coupling zeros as theorem contracts",
            "reason": "they are real derivation targets, but none are current MTS claims until parent-signed",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D759_2_acquisition_runner",
            "decision": "open coupling residual acquisition runner",
            "reason": "if quotient descent cannot be proved next, coupling residuals need source-backed rows, not prose",
            "claim_status": "acquisition_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU759_0_allowed",
            "allowed_after_759": "say coupling is now a concrete parent-action/descent gate",
            "forbidden_after_759": "claim universal coupling, c_g=0, or source-normalized Newton from same-coframe alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU759_1_allowed",
            "allowed_after_759": "attack quotient matter descent as the central next theorem",
            "forbidden_after_759": "hide representative Weyl/disformal coupling behind notation",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU759_2_allowed",
            "allowed_after_759": "if descent fails, fill coupling residual rows as nonclaim inputs",
            "forbidden_after_759": "mark coupling, c_g, EM, source, or PPN rows valid_for_claim without theorem/source backing",
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
            "main_result": "coupling owner action not parent-signed; partial theorem contracts retained; acquisition runner opened",
            "hard_blocker": "quotient matter descent and source/readout/EM coupling descent are unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V759_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V759_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_758 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_758_VALIDATION.csv")
    validation.append({"check_id": "V759_2_prior_758_clean", "result": "pass" if prior_758 and all(row.get("result") == "pass" for row in prior_758) else "fail", "detail": "758 validation has no failures"})
    validation.append({"check_id": "V759_3_coupling_owner_not_signed", "result": "pass" if any(row["audit_id"] == "COA759_6_verdict" and row["current_status"] == "coupling_owner_not_parent_signed" for row in owner) else "fail", "detail": "coupling owner remains nonclaim"})
    validation.append({"check_id": "V759_4_partial_theorem_nonclaim", "result": "pass" if any(row["theorem_id"] == "PCT759_5_verdict" and row["status"] == "partial_contract_only_no_claim" for row in theorem) else "fail", "detail": "conditional coupling zeros not promoted"})
    validation.append({"check_id": "V759_5_quotient_descent_next", "result": "pass" if NEXT_TARGET.startswith("760-Y5-R10-quotient-matter-descent") else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V759_6_acquisition_runner_open", "result": "pass" if len(acquisition) == 6 and all(row["valid_for_claim"] == "false" for row in acquisition) else "fail", "detail": "coupling acquisition rows nonclaim"})
    validation.append({"check_id": "V759_7_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in [COUPLING_DESCENT_CANDIDATE_PATH, CG_SOURCE_CANDIDATE_PATH, EM_INTERFACE_CANDIDATE_PATH]) else "fail", "detail": "no coupling claim-input artifacts fabricated"})
    validation.append({"check_id": "V759_8_cg_zero_not_claimed", "result": "pass" if any(row["theorem_id"] == "PCT759_2_representative_cg" and row["status"] == "not_parent_signed_627_blocked" for row in theorem) else "fail", "detail": "c_g remains blocked"})
    validation.append({"check_id": "V759_9_impact_matrix_blocks_claims", "result": "pass" if len(impact) == 5 and all(row["claim_status"] == "blocked" for row in impact) else "fail", "detail": "all impact rows blocked"})
    all_generated = owner + theorem + acquisition + impact + decisions + routes + summary
    validation.append({"check_id": "V759_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V759_11_no_local_arena_claim", "result": "pass" if "no_cg_zero_q_loc_zero_alpha3_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local/coupling claims remain blocked"})
    validation.append({"check_id": "V759_12_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        COUPLING_OWNER_PATH,
        PARTIAL_THEOREM_PATH,
        ACQUISITION_RUNNER_PATH,
        IMPACT_MATRIX_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V759_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V759_14_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V759_15_no_ad_hoc_coupling_zero", "result": "pass" if any(row["audit_id"] == "COA759_5_no_ad_hoc_coupling_zero" for row in owner) else "fail", "detail": "coupling zero cannot be bolted on"})
    validation.append({"check_id": "V759_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 759 - Y5 R10 Coupling Owner Action Or Residual Vector Acquisition Runner

Start point: 758 made coupling descent the central hard gate for the full residual-vector parent action.

Current result: **the coupling owner action is not parent-signed yet**. The same-coframe route is useful and gives real conditional zeros, but it does not by itself prove quotient matter descent, `c_g=0`, closed source mass, EM/charge descent, PPN silence, or local GR. The next theorem target is the quotient matter descent clause; if that does not close, the coupling residual acquisition runner is ready.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Coupling Owner Action Audit

{markdown_table(owner, ["audit_id", "coupling_clause", "mathematical_form", "what_it_would_close", "current_status", "blocker", "valid_for_claim"])}

## Partial Coupling Theorem Contract

{markdown_table(theorem, ["theorem_id", "conditional_statement", "mathematical_form", "status", "not_enough_for", "valid_for_claim"])}

## Coupling Residual Acquisition Runner

{markdown_table(acquisition, ["runner_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Residual Vector Impact Matrix

{markdown_table(impact, ["impact_id", "residual_channel", "what_coupling_owner_can_help", "what_remains_open", "claim_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_759", "forbidden_after_759", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a good narrowing. The coupling idea is not handwavy anymore: it has a theorem target. Same coframe gets us part of the way, but the real lock is quotient matter descent: matter, rods, clocks, source charge, orbit readout, and EM/charge must all be functions of the same observed quotient structure. If that signs, a lot of ugly coupling channels collapse. If it does not, we do not bluff; we acquire residual rows.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    owner = coupling_owner_rows(generated_utc)
    theorem = partial_theorem_rows(generated_utc)
    acquisition = acquisition_runner_rows(generated_utc)
    impact = impact_matrix_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, owner, theorem, acquisition, impact, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(COUPLING_OWNER_PATH, owner, ["audit_id", "coupling_clause", "mathematical_form", "what_it_would_close", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(PARTIAL_THEOREM_PATH, theorem, ["theorem_id", "conditional_statement", "mathematical_form", "status", "not_enough_for", "valid_for_claim", "generated_utc"])
    write_csv(ACQUISITION_RUNNER_PATH, acquisition, ["runner_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(IMPACT_MATRIX_PATH, impact, ["impact_id", "residual_channel", "what_coupling_owner_can_help", "what_remains_open", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_759", "forbidden_after_759", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, owner, theorem, acquisition, impact, decisions, routes, summary, validation)

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
