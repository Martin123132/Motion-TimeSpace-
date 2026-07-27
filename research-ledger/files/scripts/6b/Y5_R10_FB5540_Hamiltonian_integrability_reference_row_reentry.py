from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "769-Y5-R10-FB554-0-Hamiltonian-integrability-reference-row-reentry.md"
NEXT_TARGET = "770-Y5-R10-Hamiltonian-integrability-parent-action-clause-or-FB5540-component-fill.md"
STATUS = "Y5_R10_769_FB5540_reentry_theorem_contract_written_prior_chain_collapsed_to_parent_action_coupling_owner_nonclaim"
CLAIM_CEILING = "FB5540_reentry_contract_only_no_HPiM_integrability_no_Newton_no_PPN_no_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_769_SOURCE_REGISTER.csv"
THEOREM_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_769_FB5540_REENTRY_THEOREM_CONTRACT.csv"
COMPONENT_STATUS_PATH = RESIDUALS / "P8_Y5_R10_769_COMPONENT_STATUS_AFTER_REENTRY.csv"
CHAIN_COLLAPSE_PATH = RESIDUALS / "P8_Y5_R10_769_PRIOR_CHAIN_COLLAPSE_MAP.csv"
OBSTRUCTION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_769_SURVIVING_OBSTRUCTION_LEDGER.csv"
NEXT_PROOF_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_769_NEXT_PROOF_QUEUE.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_769_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_769_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_769_VALIDATION.csv"

CANDIDATE_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_769_FB5540_PARENT_ACTION_CERTIFICATE_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_769_DELTA_H_TAU_COMPONENT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_769_DELTA_REF_COMPONENT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_769_SYMPLECTIC_BOUNDARY_COMPONENT_INPUT_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_769_TAU_MHREF_COMPONENT_INPUT_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    THEOREM_CONTRACT_PATH,
    COMPONENT_STATUS_PATH,
    CHAIN_COLLAPSE_PATH,
    OBSTRUCTION_LEDGER_PATH,
    NEXT_PROOF_QUEUE_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "768_doc": {
        "path": POST_CHECKPOINT / "768-Y5-R10-local-GR-EH-or-R11-reentry-after-alpha-WEP-quarantine.md",
        "needles": [
            "local-GR route re-enters through Hamiltonian PiM source-charge integrability",
            "769-Y5-R10-FB554-0-Hamiltonian-integrability-reference-row-reentry.md",
        ],
        "role": "immediate reentry selecting FB5540 as live edge",
    },
    "768_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_768_VALIDATION.csv",
        "needles": ["V768_8_FB554_0_live_edge_selected", "pass"],
        "role": "prior 768 validation guard",
    },
    "665_doc": {
        "path": POST_CHECKPOINT / "665-Y5-R10-fill-or-prove-FB554-0-Hamiltonian-integrability-reference-row.md",
        "needles": ["FB554_0 = abs(delta_H_tau_nonintegrable_over_MH)", "not proved zero"],
        "role": "direct FB5540 proof/fill attempt",
    },
    "665_component_audit": {
        "path": RESIDUALS / "P8_Y5_R10_665_FB5540_COMPONENT_AUDIT.csv",
        "needles": ["delta_H_tau_nonintegrable_over_MH", "symplectic_boundary_flux_over_MH"],
        "role": "FB5540 component audit",
    },
    "666_source_hunt": {
        "path": RESIDUALS / "P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
        "needles": ["MISSING_PARENT_THETA_QTAU_AND_FIELD_SPACE_CURL_ZERO", "MISSING_PARENT_REFERENCE_LOCK"],
        "role": "FB5540 source-value hunt ledger",
    },
    "667_doc": {
        "path": POST_CHECKPOINT / "667-Y5-R10-explicit-parent-boundary-action-ansatz-and-variation-ledger.md",
        "needles": ["delta H_tau[S] = int_S(delta Q_tau^MTS - i_tau Theta_total)", "does **not** yet prove `FB554_0=0`"],
        "role": "parent boundary action ansatz and variation ledger",
    },
    "667_term_map": {
        "path": RESIDUALS / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
        "needles": ["TM667_0_delta_H_tau", "TM667_2_symplectic_boundary_flux"],
        "role": "FB5540 term map",
    },
    "668_doc": {
        "path": POST_CHECKPOINT / "668-Y5-R10-sector-Lagrangian-owner-and-boundary-condition-lock.md",
        "needles": ["L_X, Theta_X, Q_X", "`FB554_0=0` is still not proved"],
        "role": "sector Lagrangian owner and boundary condition lock",
    },
    "668_impact": {
        "path": RESIDUALS / "P8_Y5_R10_668_FB5540_IMPACT_MAP.csv",
        "needles": ["missing_LX_and_boundary_conditions", "missing_observed_tau_functor"],
        "role": "FB5540 impact map after sector-owner audit",
    },
    "669_doc": {
        "path": POST_CHECKPOINT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["No signed minimal L_X owner yet", "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md"],
        "role": "minimal L_X owner attempt",
    },
    "670_doc": {
        "path": POST_CHECKPOINT / "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md",
        "needles": ["quotient/no-pole branch has a real conditional spine", "full no-pole proof is blocked"],
        "role": "no-pole/source-free L_X continuation",
    },
    "673_doc": {
        "path": POST_CHECKPOINT / "673-Y5-R10-edge-coefficient-source-acquisition-or-Hamiltonian-PiM-orthogonality-proof.md",
        "needles": ["Hamiltonian `Pi_M^H`", "integrability, fixed reference, same-frame source measure"],
        "role": "Hamiltonian PiM orthogonality blocker",
    },
    "684_doc": {
        "path": POST_CHECKPOINT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
        "needles": ["tau_obs", "not yet constructed as the same stationary/clock/Hamiltonian generator"],
        "role": "observed-frame tau/coframe lock attempt",
    },
    "742_doc": {
        "path": POST_CHECKPOINT / "742-Y5-R10-observed-tau-owner-or-q_loc-free-coefficient-pack.md",
        "needles": ["observed `tau` is not parent-owned for the current chain", "NO_PARENT_SIGNED_TAU_LOCK"],
        "role": "later tau-owner rejection",
    },
    "759_doc": {
        "path": POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        "needles": ["coupling owner action is not parent-signed yet", "quotient matter descent clause"],
        "role": "coupling owner action audit",
    },
    "759_coupling": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
        "needles": ["COA759_6_verdict", "coupling_owner_not_parent_signed"],
        "role": "coupling owner action rows",
    },
    "760_doc": {
        "path": POST_CHECKPOINT / "760-Y5-R10-quotient-matter-descent-or-coupling-residual-source-pack.md",
        "needles": ["quotient matter descent is not parent-signed", "`c_g=0` is not claimed"],
        "role": "quotient matter descent audit",
    },
    "760_descent": {
        "path": RESIDUALS / "P8_Y5_R10_760_QUOTIENT_DESCENT_PROOF_ATTEMPT.csv",
        "needles": ["QMD760_6_verdict", "quotient_matter_descent_not_parent_signed"],
        "role": "quotient descent proof attempt rows",
    },
    "763_doc": {
        "path": POST_CHECKPOINT / "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md",
        "needles": ["no-marker/no-spurion theorem is only a classification theorem shape", "qbar_XT_vec"],
        "role": "no-marker/no-spurion classification",
    },
    "764_doc": {
        "path": POST_CHECKPOINT / "764-Y5-R10-constant-superselection-and-charge-normalization-or-source-fill.md",
        "needles": ["constant/charge descent gate is now exact enough to use", "does not close"],
        "role": "constant and charge descent gate",
    },
    "767_doc": {
        "path": POST_CHECKPOINT / "767-Y5-R10-parent-matter-functor-no-alpha-vertex-or-WEP-closure.md",
        "needles": ["parent matter functor/no-alpha-vertex theorem is still not signed", "WEP safety remains an explicit quarantined closure"],
        "role": "WEP/no-alpha quarantine before 768 reentry",
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


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def theorem_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "FBR769_0_definition",
            "statement": "FB5540 is zero if all normalized Hamiltonian-integrability, reference, and symplectic-boundary components are zero with positive same-frame denominator",
            "mathematical_form": "FB554_0=|delta_H_tau_nonintegrable|/M_H_ref+|Delta_ref|/M_H_ref+|symplectic_boundary_flux|/M_H_ref",
            "proof_step": "nonnegative sum; no cancellation credit allowed",
            "current_status": "definition_imported_not_zero",
            "claim_effect_if_signed": "opens Hamiltonian PiM source-charge route; does not alone prove source equality, Gauss, PPN, or local GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "FBR769_1_integrability_curl",
            "statement": "Hamiltonian variation is field-space exact when the local parent action supplies theta, Q_tau, fixed tau, and zero boundary symplectic flux",
            "mathematical_form": "delta H_tau=int_S(delta Q_tau-i_tau theta); curl(delta H_tau)=int_S i_tau omega(delta_1 Phi,delta_2 Phi)+tau/reference/domain terms",
            "proof_step": "covariant phase-space identity reduces the curl to symplectic flux and variation of the generator/reference/surface",
            "current_status": "conditional_identity_written_not_parent_signed",
            "claim_effect_if_signed": "kills delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "FBR769_2_reference_silence",
            "statement": "reference subtraction contributes no physical source residual if the same parent branch fixes B_ref before readout",
            "mathematical_form": "partial_{source,r,t,frame,lambda}Delta_ref=0 and delta H_ref=0 on allowed local variations",
            "proof_step": "fixed reference/counterterm convention cannot depend on the source, radial shell, clock, frame, or R10 range being tested",
            "current_status": "conditional_clause_not_parent_owned",
            "claim_effect_if_signed": "kills Delta_ref_over_MH",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "FBR769_3_boundary_flux_silence",
            "statement": "extra boundary/projector/non-EH symplectic flux vanishes only when the retained sectors are exact/proper gauge, source-free no-pole, or explicitly bounded",
            "mathematical_form": "int_boundary(delta Q_tau^extra-i_tau theta_extra)+delta B_class+projector/domain terms=0",
            "proof_step": "edge, projector, L_X, and boundary no-hair channels must be killed by the same parent action, not by notation",
            "current_status": "failed_for_current_corpus_retained_residuals_active",
            "claim_effect_if_signed": "kills symplectic_boundary_flux_over_MH and removes one FB5540 channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "FBR769_4_same_frame_denominator",
            "statement": "M_H_ref can normalize FB5540 only when it is positive, fixed, and read in the same observed source/clock/boundary frame",
            "mathematical_form": "M_H_ref=G_ref^-1 int_S Q_tau^MTS > 0 with tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit",
            "proof_step": "denominator, time generator, and source measure cannot be imported from orbital GM before Poisson/Gauss/source equality",
            "current_status": "blocked_by_tau_and_MHref_chain",
            "claim_effect_if_signed": "makes the FB5540 bound meaningful and prevents circular normalization",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "FBR769_5_total_verdict",
            "statement": "Current MTS does not yet prove FB5540=0",
            "mathematical_form": "FBR769_1 through FBR769_4 are not jointly signed",
            "proof_step": "665-768 collapse to missing parent action/coupling/source ownership rather than a hidden algebraic contradiction",
            "current_status": "theorem_contract_only_nonclaim",
            "claim_effect_if_signed": "next work should attempt the parent-action clause first, then source-fill components if it fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def component_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "FBC769_0_delta_H_tau_nonintegrable",
            "component": "delta_H_tau_nonintegrable_over_MH",
            "current_status": "blocked_not_zero_not_numeric",
            "exact_reentry_condition": "explicit L_parent, theta_total, Q_tau^MTS, fixed tau, field-space curl zero, and owned L_X/no-pole or retained residual vector",
            "best_prior_evidence": "665 component audit; 667 variation ledger; 668/669 L_X owner failure; 670 no-pole partial failure; 759 coupling owner not signed",
            "why_not_closed": "theta/Q_tau cannot be computed for all retained sectors and the coupling owner action is not parent-signed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "FBC769_1_Delta_ref",
            "component": "Delta_ref_over_MH",
            "current_status": "blocked_not_zero_not_numeric",
            "exact_reentry_condition": "B_ref/reference branch fixed before source, radius, time, frame, range, and boundary-counterterm choices",
            "best_prior_evidence": "665/666 reference rows; 667 reference rule; 668 boundary reference owner missing; 673 PiM orthogonality blocker",
            "why_not_closed": "reference subtraction can still absorb or imitate the tested source calibration",
            "next_action": "include B_ref derivative-silence in parent-action certificate or source-fill Delta_ref",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "FBC769_2_symplectic_boundary_flux",
            "component": "symplectic_boundary_flux_over_MH",
            "current_status": "blocked_not_zero_not_numeric",
            "exact_reentry_condition": "boundary class/no-hair, projector silence, edge charge zero, and L_X boundary flux zero are parent-owned",
            "best_prior_evidence": "667 term map; 670 no-pole proof blocked; 671-679 edge channel retained; 681 demotes B_X to closure support",
            "why_not_closed": "edge/projector/boundary channels can carry physical residuals unless killed or bounded",
            "next_action": "either prove exact/proper boundary class in parent action or source-fill boundary flux component",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "FBC769_3_tau_lock",
            "component": "time_generator_lock",
            "current_status": "blocked_with_one_pruned_skew_component",
            "exact_reentry_condition": "same tau_obs controls source variation, Hamiltonian charge, clocks, boundary reference, and orbital readout with delta tau=0",
            "best_prior_evidence": "684-689 tau chain; 742 observed tau owner rejected; 743 antisymmetric tau component pruned only",
            "why_not_closed": "symmetric tau strain, role mismatch, denominator, and observed generator ownership remain open",
            "next_action": "carry tau lock as explicit parent-action clause; do not use the skew pruning theorem as full tau proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "FBC769_4_MHref_denominator",
            "component": "M_H_ref",
            "current_status": "blocked_positive_same_frame_denominator_missing",
            "exact_reentry_condition": "Hamiltonian charge equals same-frame source mass before orbital fitting, with Poisson/Gauss calibration downstream",
            "best_prior_evidence": "683/697 M_H_ref denominator missing; 698/699 Poisson-Gauss bridge nonclaim; 702/703 coupling lock missing",
            "why_not_closed": "no claim-ready M_H_ref row exists and orbital GM cannot backfill the denominator",
            "next_action": "keep M_H_ref as guardrail denominator only until Hamiltonian/source equality and PG calibration close",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "FBC769_5_matter_and_constant_descent",
            "component": "ordinary matter/constants coupling silence",
            "current_status": "blocked_closure_only",
            "exact_reentry_condition": "matter functor, measure/coframe/connection, constants, charge normalization, and no-marker clauses descend through q(Phi)",
            "best_prior_evidence": "760-767 quotient matter, geometry stack, no-marker, constants, alpha, and WEP closure audits",
            "why_not_closed": "WEP/no-alpha/common-frame safety remains explicit closure, not parent derivation",
            "next_action": "treat coupling descent as a clause in the parent-action certificate; otherwise retain residual source pack",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def chain_collapse_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "PCC769_0_665_direct_FB5540",
            "checkpoint_range": "665-666",
            "what_was_tried": "prove or source-fill FB5540 directly",
            "result": "component audit and source-value hunt staged; no theorem-zero or claim-valid numeric rows",
            "collapse_to": "need parent theta/Q_tau, reference lock, boundary flux silence, tau lock",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_1_667_669_parent_action_LX",
            "checkpoint_range": "667-669",
            "what_was_tried": "write parent boundary action ansatz and identify L_X owner",
            "result": "variation ledger exists, but L_X, theta_X, Q_X, boundary class, tau, and M_H_ref remain unsigned",
            "collapse_to": "explicit parent Lagrangian/current owner or retained L_X residual vector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_2_670_679_no_pole_edge",
            "checkpoint_range": "670-679",
            "what_was_tried": "kill L_X/edge branch through quotient no-pole, boundary exactness, PiM orthogonality, or first source row",
            "result": "conditional zero shapes exist; edge coefficients and Qbar rows remain nonclaim",
            "collapse_to": "boundary/edge proper-gauge proof or source-backed edge coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_3_680_703_denominator_tau_PG_coupling",
            "checkpoint_range": "680-703",
            "what_was_tried": "derive B_X/Qbar/M_H_ref/tau/Poisson-Gauss/coupling normalization",
            "result": "M_H_ref denominator, tau lock, EH prefactor/coupling, and Poisson coefficient remain conditional or unfilled",
            "collapse_to": "fixed same-frame Hamiltonian source charge plus parent coupling prefactor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_4_704_724_scalar_affine_edge",
            "checkpoint_range": "704-724",
            "what_was_tried": "remove scalar/class prefactor, source scalar coefficients, affine no-pole branch, and edge alpha envelope",
            "result": "scalar zero demoted to closure; retained finite/edge coefficient pack remains active and nonclaim",
            "collapse_to": "descent/quotient theorem or sourced retained coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_5_725_758_q_loc_residual_vector",
            "checkpoint_range": "725-758",
            "what_was_tried": "derive q_loc residual zero through parent Omega/DC, hybrid quotient, Ward owner, and alpha3 response",
            "result": "three narrow representative zeros prune fake channels, but observed q_loc/Y5/Y6/PPN residual vector remains open",
            "collapse_to": "full residual-vector parent action or component/source acquisition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_6_759_767_coupling_descent",
            "checkpoint_range": "759-767",
            "what_was_tried": "prove coupling owner action, quotient matter descent, geometry stack descent, no-marker constants, and no-alpha/WEP closure",
            "result": "coupling route gives useful conditional zeros but is not parent-signed; WEP/alpha stays quarantined",
            "collapse_to": "parent action/coupling owner clause must be signed before local-GR use",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "chain_id": "PCC769_7_768_reentry",
            "checkpoint_range": "768",
            "what_was_tried": "re-enter local-GR spine after alpha/WEP quarantine",
            "result": "FB5540 selected as live edge because source-charge integrability must precede source equality, Gauss, PPN, and R10",
            "collapse_to": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def obstruction_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "OBS769_0_parent_current_owner",
            "missing_object": "one explicit parent current owner for theta_total, Q_tau^MTS, C_tau, and mu_X",
            "why_decisive": "without it the Hamiltonian curl is not computable and delta_H_tau remains a placeholder component",
            "blocks_components": "delta_H_tau_nonintegrable;C_extra;symplectic_boundary_flux",
            "repair_or_bound": "derive from parent Lagrangian or source-fill curl/flux terms with units",
            "priority": "P0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "OBS769_1_fixed_reference",
            "missing_object": "parent-selected B_ref/counterterm convention with derivative silence",
            "why_decisive": "reference freedom can hide source normalization or boundary residuals",
            "blocks_components": "Delta_ref;M_H_ref;symplectic_boundary_flux",
            "repair_or_bound": "prove source/range/frame/time derivative zero or fill Delta_ref profile",
            "priority": "P1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "OBS769_2_boundary_edge_silence",
            "missing_object": "edge/proper-gauge/no-hair/projector-silence theorem or sourced edge coefficients",
            "why_decisive": "extra boundary charge can be invisible in prose but visible in R10/PPN/source normalization",
            "blocks_components": "symplectic_boundary_flux;R10;R11;PPN preferred-frame",
            "repair_or_bound": "prove Q_edge=0 and projector orthogonality, or source K_edge/Qbar/qbar rows",
            "priority": "P1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "OBS769_3_tau_and_MHref",
            "missing_object": "same observed tau and positive same-frame M_H_ref",
            "why_decisive": "FB5540 cannot be normalized or compared if the generator/denominator changes between source, clock, charge, boundary, and orbit",
            "blocks_components": "tau_lock;M_H_ref;Delta_ref;delta_H_tau_nonintegrable",
            "repair_or_bound": "derive tau_obs/M_H_ref from parent action and source measure, or source mismatch bounds",
            "priority": "P1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "OBS769_4_coupling_descent",
            "missing_object": "quotient matter/geometry/constants/charge descent",
            "why_decisive": "even a formal Hamiltonian charge does not prove local GR if ordinary matter, constants, or charge units feel representative variables",
            "blocks_components": "matter_constants_descent;WEP;clock;R10;PPN;source equality",
            "repair_or_bound": "sign quotient descent stack or keep coupling residual acquisition rows",
            "priority": "P2",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_proof_queue_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "NPQ769_0_parent_action_certificate",
            "next_target": NEXT_TARGET,
            "task": "attempt a minimal Hamiltonian-integrability parent-action certificate before numeric fill",
            "acceptance_gate": "explicit L_parent, theta_total, Q_tau, tau owner, B_ref rule, boundary flux policy, and valid/failing component flags",
            "if_passes": "FB5540 theorem-zero route becomes serious enough to move to source equality FB5541",
            "if_fails": "stage component input rows for delta_H_tau, Delta_ref, symplectic boundary flux, tau mismatch, and M_H_ref",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "NPQ769_1_no_cancellation_policy",
            "next_target": NEXT_TARGET,
            "task": "preserve no-cancellation scoring for FB5540 components",
            "acceptance_gate": "each term individually zero or individually source-bounded before FB5540 can pass",
            "if_passes": "prevents hiding edge/reference/coupling terms in a tuned sum",
            "if_fails": "local-GR reduction becomes patchwork rather than field-theoretic",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "NPQ769_2_source_fill_fallback",
            "next_target": NEXT_TARGET,
            "task": "if the parent-action certificate fails, write source-fill rows instead of closure prose",
            "acceptance_gate": "numeric values have units, source paths, assumptions, source/reference frame, and valid_for_claim flags",
            "if_passes": "turns FB5540 into an empirical residual gate",
            "if_fails": "FB5540 remains a blocked closure condition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D769_0_reentry_not_duplicate",
            "decision": "do not duplicate 665-669; treat them as prior failed proof/fill attempts",
            "reason": "the current state already narrows FB5540 to parent action, L_X/no-pole, B_ref, tau/MHref, and coupling descent",
            "claim_status": "nonclaim_reentry",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D769_1_best_route",
            "decision": "try the parent-action certificate before numeric component fill",
            "reason": "the user's priority is derivability; numeric rows are fallback if the theorem route fails",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D769_2_no_claim",
            "decision": "do not claim FB5540=0, EH, Newton, PPN, R10, R11, or local GR",
            "reason": "none of the required parent-action/coupling/reference/tau clauses is jointly signed in the current corpus",
            "claim_status": "blocked_for_claim_not_for_work",
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
            "main_result": "FB5540 now has an exact reentry theorem contract: it can be killed by a parent-owned Hamiltonian current, fixed reference, zero boundary flux, same tau/MHref, and quotient matter/constant descent; current MTS has not signed those clauses",
            "hard_blocker": "one parent action must own theta_total/Q_tau/B_ref/tau/L_X/boundary/coupling before FB5540 can be theorem-zero",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_claim_rows_false(row_groups: list[list[dict[str, Any]]]) -> bool:
    rows_with_claim_field = [
        row
        for row_group in row_groups
        for row in row_group
        if "valid_for_claim" in row
    ]
    return bool(rows_with_claim_field) and all(str(row["valid_for_claim"]).lower() == "false" for row in rows_with_claim_field)


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    components: list[dict[str, Any]],
    collapse: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_768_clean = all(validation_clean(number) for number in range(665, 769))
    theorem_contract_written = len(theorem) >= 6 and any(row["theorem_id"] == "FBR769_5_total_verdict" for row in theorem)
    component_status_complete = {
        row["component"]
        for row in components
    } >= {
        "delta_H_tau_nonintegrable_over_MH",
        "Delta_ref_over_MH",
        "symplectic_boundary_flux_over_MH",
        "time_generator_lock",
        "M_H_ref",
    }
    chain_collapse_complete = len(collapse) >= 8 and any(row["checkpoint_range"] == "759-767" for row in collapse)
    parent_action_selected = any(row["queue_id"] == "NPQ769_0_parent_action_certificate" and row["next_target"] == NEXT_TARGET for row in queue)
    no_duplicate_decision = any(row["decision_id"] == "D769_0_reentry_not_duplicate" for row in decisions)
    candidate_artifacts_not_faked = all(not path.exists() for path in CANDIDATE_ARTIFACTS)
    all_nonclaim = all_claim_rows_false([sources, theorem, components, collapse, obstructions, queue, decisions, summary])
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D769_1_best_route" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V769_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V769_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V769_2_prior_665_768_clean", prior_665_768_clean, "665-768 validation rows have no failures"),
        ("V769_3_theorem_contract_written", theorem_contract_written, "FB5540 reentry theorem contract written"),
        ("V769_4_component_status_complete", component_status_complete, "FB5540 components and guards mapped"),
        ("V769_5_chain_collapse_complete", chain_collapse_complete, "prior 665-768 chain collapsed into live obstructions"),
        ("V769_6_parent_action_selected_first", parent_action_selected, "derivation-first parent-action certificate selected"),
        ("V769_7_no_duplicate_reentry", no_duplicate_decision, "665-669 not duplicated as new proof"),
        ("V769_8_candidate_artifacts_not_faked", candidate_artifacts_not_faked, "no claim-input artifacts fabricated"),
        ("V769_9_no_claim_rows_promoted", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V769_10_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V769_11_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V769_12_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V769_13_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    components: list[dict[str, Any]],
    collapse: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    queue: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 769 - Y5 R10 FB554-0 Hamiltonian Integrability Reference Row Reentry

Start point: 768 selected `FB554_0_HPiM_integrability_reference_bound` as the live edge for local-GR/Newton reentry. This checkpoint does not restart the old 665 proof attempt as if nothing happened. It folds the full 665-768 chain back into one exact contract.

Current result: **`FB554_0=0` is now an exact parent-action/coupling ownership target, not a vague missing number**. It would close if one parent action owns the Hamiltonian current, fixed reference, boundary silence, same time/denominator, and quotient matter/constant descent. Current MTS does not yet sign that stack, so no Hamiltonian PiM, Newton, PPN, R10, R11, or local-GR claim is promoted.

## Status

| field | value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | {summary[0]["main_result"]} |
| Hard blocker | `{summary[0]["hard_blocker"]}` |
| Next target | `{NEXT_TARGET}` |

## FB5540 Reentry Theorem Contract

{markdown_table(theorem, ["theorem_id", "statement", "mathematical_form", "proof_step", "current_status", "claim_effect_if_signed", "valid_for_claim"])}

## Component Status After Reentry

{markdown_table(components, ["component_id", "component", "current_status", "exact_reentry_condition", "best_prior_evidence", "why_not_closed", "next_action", "valid_for_claim"])}

## Prior Chain Collapse Map

{markdown_table(collapse, ["chain_id", "checkpoint_range", "what_was_tried", "result", "collapse_to", "valid_for_claim"])}

## Surviving Obstruction Ledger

{markdown_table(obstructions, ["obstruction_id", "missing_object", "why_decisive", "blocks_components", "repair_or_bound", "priority", "valid_for_claim"])}

## Next Proof Queue

{markdown_table(queue, ["queue_id", "next_target", "task", "acceptance_gate", "if_passes", "if_fails", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is good news in the unglamorous way. The work did not magically prove local GR, but it did remove fog. The first real bottleneck is not a galaxy fit, not an R10 number, and not an alpha patch. It is this: can MTS write one parent action whose covariant Hamiltonian current owns the local source charge without leaking through reference choice, boundary/edge channels, tau normalization, or matter/constants coupling? If yes, `FB554_0` can fall. If no, it must become an empirical residual row.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    theorem = theorem_contract_rows(generated_utc)
    components = component_status_rows(generated_utc)
    collapse = chain_collapse_rows(generated_utc)
    obstructions = obstruction_rows(generated_utc)
    queue = next_proof_queue_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, theorem, components, collapse, obstructions, queue, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(THEOREM_CONTRACT_PATH, theorem, ["theorem_id", "statement", "mathematical_form", "proof_step", "current_status", "claim_effect_if_signed", "valid_for_claim", "generated_utc"])
    write_csv(COMPONENT_STATUS_PATH, components, ["component_id", "component", "current_status", "exact_reentry_condition", "best_prior_evidence", "why_not_closed", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(CHAIN_COLLAPSE_PATH, collapse, ["chain_id", "checkpoint_range", "what_was_tried", "result", "collapse_to", "valid_for_claim", "generated_utc"])
    write_csv(OBSTRUCTION_LEDGER_PATH, obstructions, ["obstruction_id", "missing_object", "why_decisive", "blocks_components", "repair_or_bound", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_PROOF_QUEUE_PATH, queue, ["queue_id", "next_target", "task", "acceptance_gate", "if_passes", "if_fails", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, theorem, components, collapse, obstructions, queue, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"769 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
