from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "781-Y5-R10-minimal-parent-coupling-owner-action-or-empirical-residual-interface.md"
NEXT_TARGET = "782-Y5-R10-minimal-parent-coupling-owner-consistency-gate.md"
STATUS = "Y5_R10_781_minimal_parent_coupling_owner_action_contract_written_empirical_residual_interface_ready_nonclaim"
CLAIM_CEILING = "candidate_parent_action_contract_and_residual_interface_only_no_adopted_parent_action_no_coupling_zero_no_source_measure_bound_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_781_SOURCE_REGISTER.csv"
OWNER_ACTION_PATH = RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv"
VERTICAL_PROOF_PATH = RESIDUALS / "P8_Y5_R10_781_VERTICAL_VARIATION_PROOF_LEDGER.csv"
ADOPTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_781_ACTION_ADOPTION_GATE.csv"
RESIDUAL_INTERFACE_PATH = RESIDUALS / "P8_Y5_R10_781_EMPIRICAL_RESIDUAL_INTERFACE.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_781_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_781_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_781_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_781_ADOPTED_PARENT_COUPLING_OWNER_ACTION.csv",
    RESIDUALS / "P8_Y5_R10_781_COUPLING_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_781_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    OWNER_ACTION_PATH,
    VERTICAL_PROOF_PATH,
    ADOPTION_GATE_PATH,
    RESIDUAL_INTERFACE_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "780_doc": {
        "path": POST_CHECKPOINT / "780-Y5-R10-parent-action-coupling-signature-search-or-local-GR-branch-triage.md",
        "needles": ["no parent-signed coupling owner", "781-Y5-R10-minimal-parent-coupling-owner-action-or-empirical-residual-interface.md"],
        "role": "immediate 781 handoff",
    },
    "780_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_780_VALIDATION.csv",
        "needles": ["V780_7_no_parent_signed_claim", "V780_9_local_GR_not_claimed"],
        "role": "prior validation guard",
    },
    "780_triage": {
        "path": RESIDUALS / "P8_Y5_R10_780_LOCAL_GR_BRANCH_TRIAGE.csv",
        "needles": ["LGT780_4_local_GR_status", "not_derived_not_dead"],
        "role": "local-GR branch triage",
    },
    "780_handoff": {
        "path": RESIDUALS / "P8_Y5_R10_780_EMPIRICAL_RESIDUAL_HANDOFF.csv",
        "needles": ["ERH780_3_C_qmu", "ERH780_5_W_PPN_coupling"],
        "role": "empirical residual handoff rows",
    },
    "621_normal_form": {
        "path": POST_CHECKPOINT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
        "needles": ["S_matter = sum_A int det(e_obs)", "not_parent_derived"],
        "role": "normal-form skeleton",
    },
    "759_coupling_owner": {
        "path": POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        "needles": ["COA759_1_quotient_matter_descent", "coupling_owner_not_parent_signed"],
        "role": "coupling owner audit",
    },
    "762_geometry_stack": {
        "path": POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needles": ["GSD762_1_measure_descent", "GSD762_5_stack_verdict"],
        "role": "geometry stack descent clauses",
    },
    "763_no_marker": {
        "path": POST_CHECKPOINT / "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md",
        "needles": ["NMS763_0_classification_theorem", "NMS763_6_verdict"],
        "role": "no-marker/no-spurion clauses",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
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


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_string(path.exists()),
                "needle_check": bool_string(text_contains(path, spec["needles"])),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def owner_action_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "action_id": "MPC781_0_parent_variables",
            "object": "parent variables and quotient",
            "minimal_form": "Phi_parent, Q=q(Phi_parent), v in ker(Dq), matter fields Psi_A, constants theta_A, owned gauge fields A_owned",
            "purpose": "separate physical quotient data from representative/local hidden labels",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "unclassified representative fields that ordinary matter can see",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_1_observed_geometry",
            "object": "observed coframe/metric",
            "minimal_form": "e_obs=E(Q,theta_g); g_obs=e_obs^T eta e_obs; Lie_v e_obs=Lie_v g_obs=0",
            "purpose": "one geometry for matter, source, clocks, photons, orbit readout, and EM interface",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "matter-frame A_g(X)^2 g_obs or B_g(X)U_muU_nu representative factors",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_2_geometry_stack",
            "object": "matter measure/coframe/connection/derivative stack",
            "minimal_form": "mu_m=Mu(Q); e_m=e_obs; omega_m=Omega[e_obs,A_owned]; D_m=D[e_obs,A_owned]",
            "purpose": "stop derivative/connection terms from reintroducing hidden representative data",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "torsion, nonmetricity, charge-normalization, or marker dependence outside Q or owned gauge fields",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_3_matter_action",
            "object": "ordinary matter action",
            "minimal_form": "S_matter=sum_A int Mu(Q) L_A(Psi_A,D_m Psi_A;theta_A) with Lie_v theta_A=0",
            "purpose": "make Lie_v S_matter vanish for quotient-vertical representative motion",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "species-dependent MTS charges, mass-ratio drift, alpha_EM drift, post-readout EFT terms",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_4_source_current",
            "object": "source current before measured-GM calibration",
            "minimal_form": "T_m^{mu nu}=2/sqrt(-g_obs) delta S_matter/delta g_obs_mu_nu; J_H[tau]=T_m^{mu nu}tau_nu dSigma_mu",
            "purpose": "avoid hiding coupling inside measured source mass or orbital calibration",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "non-Hilbert source charge, species source weights, unresolved Pi_M/Gauss calibration",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_5_readout_action",
            "object": "clock/photon/orbit/EM/PPN readouts",
            "minimal_form": "O_i=O_i[e_obs,Psi_i,theta_i,A_owned] and S_readout=sum_i R_i[O_i] with Lie_v O_i=0",
            "purpose": "keep observables from seeing hidden MTS frame/readout maps",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "hidden C(Phi), D(Phi), source-frame, clock-frame, or charge-normalization maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_6_boundary_and_projection",
            "object": "boundary/source-measure silence",
            "minimal_form": "delta_v(S_matter+S_readout)+B_source_measure=0 under compact-local boundary/projector conditions",
            "purpose": "make the zero theorem survive integration by parts and readout projection",
            "status": "candidate_contract_not_adopted",
            "must_exclude": "boundary, corner, projector, source-measure, or calibration leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "action_id": "MPC781_7_contract_verdict",
            "object": "minimal parent coupling owner action",
            "minimal_form": "S_parent=S_grav[g_obs,R_phys]+S_matter[Q,Psi,theta]+S_source[J_H]+S_readout[e_obs,Psi,theta,A_owned]+S_boundary",
            "purpose": "candidate action that would make the coupling branch derivable if adopted and consistency-tested",
            "status": "candidate_only_requires_782_consistency_gate",
            "must_exclude": "treating this candidate as already present in current MTS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def vertical_proof_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "VP781_0_quotient_verticality",
            "step": "take v in ker(Dq)",
            "variation": "Lie_v Q = Dq[v] = 0",
            "result_if_contract_holds": "all Q-only parent objects are vertical-silent",
            "current_status": "conditional_candidate_only",
            "missing_for_claim": "current-MTS q and vertical generator basis",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "VP781_1_geometry_stack",
            "step": "apply chain rule to matter geometry stack",
            "variation": "Lie_v mu_m=Lie_v e_m=Lie_v omega_m=Lie_v D_m=0 if each factors through Q and owned gauge fields",
            "result_if_contract_holds": "no representative Weyl/disformal/connection leakage",
            "current_status": "conditional_candidate_only",
            "missing_for_claim": "measure/coframe/connection/derivative descent source paths",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "VP781_2_matter_action",
            "step": "vary ordinary matter action at fixed Psi_A",
            "variation": "Lie_v S_matter = sum_A int [delta S/dmu Lie_v mu + delta S/de Lie_v e + delta S/dD Lie_v D + partial_theta L Lie_v theta_A] = 0",
            "result_if_contract_holds": "direct matter coupling residual vanishes",
            "current_status": "conditional_candidate_only",
            "missing_for_claim": "ordinary constants and charge/mass labels as superselection data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "VP781_3_source_and_readout",
            "step": "vary source current and readout functionals",
            "variation": "Lie_v J_H=0 and Lie_v O_i=0 if source/readouts are functionals only of e_obs, Psi, theta, and owned charges",
            "result_if_contract_holds": "source-measure and readout coupling leakage vanishes",
            "current_status": "conditional_candidate_only",
            "missing_for_claim": "source current closure, EM charge interface, orbit/clock/photon/PPN readout maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "VP781_4_boundary",
            "step": "integrate by parts and project to observed local arena",
            "variation": "B_source_measure + B_boundary + B_projector = 0 only with compact no-flux/projector descent theorem",
            "result_if_contract_holds": "B_obs_source_measure/M_H is theorem-zero",
            "current_status": "conditional_candidate_only",
            "missing_for_claim": "boundary/corner/projector no-flux proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "VP781_5_zero_theorem",
            "step": "combine vertical-silent matter/source/readout/boundary terms",
            "variation": "Lie_v(S_matter+S_source+S_readout)+B_obs_source_measure=0",
            "result_if_contract_holds": "DeltaCoupling_A=0 and source-measure block can be removed from local residual vector",
            "current_status": "candidate_zero_theorem_not_promoted",
            "missing_for_claim": "adopted parent action plus all consistency checks",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def adoption_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "AAG781_0_present_in_current_corpus",
            "gate": "Is the minimal parent coupling owner action already present as a sourced current-MTS action?",
            "result": "fail_current_corpus",
            "why": "780 found only conditional theorem shapes, not a parent-signed owner",
            "required_before_claim": "source path/equation adopting MPC781_0..MPC781_6",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AAG781_1_internal_consistency",
            "gate": "Does the candidate action preserve existing MTS gravity/cosmology/galaxy/EM structure?",
            "result": "not_tested",
            "why": "candidate action has not been checked against the current unification spine or empirical pillars",
            "required_before_claim": "782 consistency gate across field definitions, limits, and tests",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AAG781_2_GR_Newton_limit",
            "gate": "Does the candidate action derive local GR/Newton rather than impose it?",
            "result": "conditional_only",
            "why": "vertical coupling silence helps, but q_loc/Y5/Y6/PPN/boundary locks still need closure",
            "required_before_claim": "full residual-vector lock and PPN/Newton limit proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AAG781_3_overconstraint_risk",
            "gate": "Does the action accidentally kill desired MTS phenomenology?",
            "result": "open",
            "why": "strong universal coupling may overconstrain cosmology/galaxy/EM branches unless residual sectors are separated cleanly",
            "required_before_claim": "sector separation and empirical robustness pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "AAG781_4_adoption_verdict",
            "gate": "Adopt minimal parent coupling owner action as current MTS?",
            "result": "not_adopted_candidate_only",
            "why": "the action is a disciplined proposal, not yet source-backed current theory",
            "required_before_claim": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def residual_interface_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "ERI781_0_b_g",
            "coefficient": "b_g or c_g",
            "enters": "matter-frame/common Weyl/disformal response",
            "zero_route": "MPC781_1..MPC781_2 adopted with no hidden frame map",
            "bound_route": "R10/PPN/clock/orbit bound on frame response",
            "fit_role": "local coupling nuisance or derived-zero switch",
            "prior_status": "needs_source_or_zero_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "ERI781_1_b_theta",
            "coefficient": "b_theta",
            "enters": "constants, alpha_EM, charge normalization, mass ratios",
            "zero_route": "MPC781_3 plus no-marker/no-spurion superselection proof",
            "bound_route": "clock/EM/WEP residual priors",
            "fit_role": "clock/EM/WEP coupling nuisance",
            "prior_status": "needs_superselection_source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "ERI781_2_b_kappa",
            "coefficient": "b_kappa",
            "enters": "source current and measured-GM normalization",
            "zero_route": "MPC781_4 plus closed projected Hilbert current",
            "bound_route": "source-mass/orbit/Gauss calibration residual",
            "fit_role": "Newton/source normalization nuisance",
            "prior_status": "needs_source_current_owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "ERI781_3_C_qmu",
            "coefficient": "C_qmu",
            "enters": "q_loc/source-measure leakage",
            "zero_route": "MPC781_6 boundary/source-measure silence",
            "bound_route": "numeric C_qmu with units, q_loc component, M_H reference",
            "fit_role": "R10/PPN alpha3/local force coupling",
            "prior_status": "missing_numeric_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "ERI781_4_B_SM",
            "coefficient": "B_SM/M_H",
            "enters": "source-measure boundary/flux total",
            "zero_route": "compact no-flux theorem under MPC781_6",
            "bound_route": "no-cancellation sum over flux components",
            "fit_role": "local-GR recovery gate",
            "prior_status": "missing_flux_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "ERI781_5_W_Ic",
            "coefficient": "W_Ic",
            "enters": "PPN coupling response matrix",
            "zero_route": "MPC781_5 readout descent plus gauge/frame certificate",
            "bound_route": "linear PPN response matrix fitted or bounded",
            "fit_role": "PPN/R11 response gate",
            "prior_status": "missing_response_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D781_0_candidate_action_written",
            "decision": "write minimal parent coupling owner action as a candidate contract",
            "reason": "this is the least-scrutiny derivation route if it can be made consistent with current MTS",
            "claim_status": "candidate_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D781_1_zero_not_promoted",
            "decision": "do not promote the vertical zero theorem",
            "reason": "the candidate action is not adopted and boundary/source/readout closures are unproved",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D781_2_residual_interface_ready",
            "decision": "prepare empirical residual interface if the candidate action fails consistency",
            "reason": "the local branch can stay testable without pretending local GR is derived",
            "claim_status": "interface_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D781_3_next_target",
            "decision": "run the minimal parent coupling owner consistency gate",
            "reason": "we must test whether the candidate owner action breaks or supports the existing MTS spine",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "minimal parent coupling owner action contract written; vertical zero theorem is conditional; empirical residual interface is ready if adoption fails",
            "hard_blocker": "candidate action is not yet adopted or consistency-tested against the MTS spine and local-GR gates",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    interface: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_action_ids = {f"MPC781_{index}_{name}" for index, name in [
        (0, "parent_variables"),
        (1, "observed_geometry"),
        (2, "geometry_stack"),
        (3, "matter_action"),
        (4, "source_current"),
        (5, "readout_action"),
        (6, "boundary_and_projection"),
        (7, "contract_verdict"),
    ]}
    expected_proof_ids = {f"VP781_{index}_{name}" for index, name in [
        (0, "quotient_verticality"),
        (1, "geometry_stack"),
        (2, "matter_action"),
        (3, "source_and_readout"),
        (4, "boundary"),
        (5, "zero_theorem"),
    ]}
    expected_interface_ids = {f"ERI781_{index}_{name}" for index, name in [
        (0, "b_g"),
        (1, "b_theta"),
        (2, "b_kappa"),
        (3, "C_qmu"),
        (4, "B_SM"),
        (5, "W_Ic"),
    ]}

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_780_clean = all(validation_clean(number) for number in range(665, 781))
    action_complete = expected_action_ids.issubset({row["action_id"] for row in action})
    proof_complete = expected_proof_ids.issubset({row["proof_id"] for row in proof})
    zero_not_promoted = any(row["proof_id"] == "VP781_5_zero_theorem" and row["current_status"] == "candidate_zero_theorem_not_promoted" for row in proof)
    adoption_gate_complete = len(gates) == 5
    adoption_not_claimed = any(row["gate_id"] == "AAG781_4_adoption_verdict" and row["result"] == "not_adopted_candidate_only" for row in gates)
    interface_complete = expected_interface_ids.issubset({row["interface_id"] for row in interface})
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, action, proof, gates, interface, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D781_3_next_target" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V781_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V781_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V781_2_prior_665_780_clean", prior_665_780_clean, "665-780 validation rows have no failures"),
        ("V781_3_action_contract_complete", action_complete, "minimal parent coupling owner action clauses complete"),
        ("V781_4_vertical_proof_complete", proof_complete, "vertical variation proof ledger complete"),
        ("V781_5_zero_not_promoted", zero_not_promoted, "candidate vertical zero theorem not promoted"),
        ("V781_6_adoption_gate_complete", adoption_gate_complete, "action adoption gate complete"),
        ("V781_7_adoption_not_claimed", adoption_not_claimed, "candidate action not adopted as current MTS"),
        ("V781_8_residual_interface_complete", interface_complete, "empirical residual interface complete"),
        ("V781_9_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V781_10_claim_artifacts_absent", claim_artifacts_absent, "no adopted-action/zero/local-GR claim artifact fabricated"),
        ("V781_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V781_12_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V781_13_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V781_14_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    interface: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 781 - Y5 R10 Minimal Parent Coupling Owner Action Or Empirical Residual Interface

Current result: **the minimal parent coupling owner action is now explicit, but it is a candidate contract, not an adopted MTS theorem**. If adopted and consistency-tested, it gives the clean derivation route: quotient-vertical variations do not move `Q=q(Phi)`, `e_obs`, the matter geometry stack, source current, or readouts, so the coupling/source-measure block can vanish. If it cannot be adopted, the empirical residual interface below tells us exactly what coefficients must be carried into local tests.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Minimal Parent Coupling Owner Action

{markdown_table(action, ["action_id", "object", "minimal_form", "purpose", "status", "must_exclude", "valid_for_claim"])}

## Vertical Variation Proof Ledger

{markdown_table(proof, ["proof_id", "step", "variation", "result_if_contract_holds", "current_status", "missing_for_claim", "valid_for_claim"])}

## Action Adoption Gate

{markdown_table(gates, ["gate_id", "gate", "result", "why", "required_before_claim", "valid_for_claim"])}

## Empirical Residual Interface

{markdown_table(interface, ["interface_id", "coefficient", "enters", "zero_route", "bound_route", "fit_role", "prior_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is probably the sharpest formulation of the coupling fork so far. The derivation route is not mystical anymore: it is a concrete parent action contract. But it cannot simply be declared true. The next gate must check whether this contract is compatible with the existing MTS spine, cosmology/galaxy successes, EM ambitions, and local residual-vector locks. If it breaks too much, we demote gracefully to the empirical residual interface.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    action = owner_action_rows(generated_utc)
    proof = vertical_proof_rows(generated_utc)
    gates = adoption_gate_rows(generated_utc)
    interface = residual_interface_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, action, proof, gates, interface, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(OWNER_ACTION_PATH, action, ["action_id", "object", "minimal_form", "purpose", "status", "must_exclude", "valid_for_claim", "generated_utc"])
    write_csv(VERTICAL_PROOF_PATH, proof, ["proof_id", "step", "variation", "result_if_contract_holds", "current_status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(ADOPTION_GATE_PATH, gates, ["gate_id", "gate", "result", "why", "required_before_claim", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_INTERFACE_PATH, interface, ["interface_id", "coefficient", "enters", "zero_route", "bound_route", "fit_role", "prior_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, action, proof, gates, interface, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"781 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
