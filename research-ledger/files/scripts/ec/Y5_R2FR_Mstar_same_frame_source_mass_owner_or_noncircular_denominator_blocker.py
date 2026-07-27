from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1644"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1644-Y5-R2FR-Mstar-same-frame-source-mass-owner-or-noncircular-denominator-blocker.md"

SOURCE_FILES = {
    "1643_doc": ROOT / "1643-Y5-R2FR-PiR-Mstar-source-acquisition-and-current-PPN-bound-runner.md",
    "1643_validation": OUT / "P8_Y5_BRR545_1643_VALIDATION.csv",
    "1643_next": OUT / "P8_Y5_PARENT_QLOC_1643_NEXT_TARGET.csv",
    "1643_inputs": OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_INPUT_STATUS.csv",
    "1643_blockers": OUT / "P8_Y5_PARENT_QLOC_1643_SOURCE_ACQUISITION_BLOCKERS.csv",
    "1006_denominator": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
    "1016_selector": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "449_ward": ROOT / "449-source-current-Ward-universality-theorem-attempt.md",
    "444_source_norm": ROOT / "444-source-normalization-residual-vector-refinement.md",
    "worldtube_clauses": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
    "hwt_attempt": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
    "boundary_first_status": OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
}

NEEDLES = {
    "1643_doc": ["M_star_same_frame", "RUN1643_0_input_gate", "Cassini: gamma"],
    "1643_validation": ["VAL1643_OVERALL", "PASS"],
    "1643_next": ["1644-Y5-R2FR-Mstar-same-frame-source-mass-owner-or-noncircular-denominator-blocker.md", "do not use orbital GM"],
    "1643_inputs": ["M_star_same_frame", "MISSING_SAME_FRAME_PARENT_SOURCE_MASS"],
    "1643_blockers": ["BLK1643_2_Mstar", "MISSING_NONCIRCULAR_DENOMINATOR"],
    "1006_denominator": ["positive same-frame M_H_ref", "orbital GM substitution is explicitly rejected"],
    "1016_selector": ["M_H_ref is a dressed source charge with fixed reference", "integrability/reference lock is not derived"],
    "449_ward": ["conditional_Hilbert_source_current_theorem", "measured Newtonian GM"],
    "444_source_norm": ["same_frame_source_calibration_gate", "conditional_open"],
    "worldtube_clauses": ["W504_4_worldtube_source_measure_glue", "not_yet_derived_core_missing_piece"],
    "hwt_attempt": ["HWT536_2_dressed_mass_charge_definition", "definition_guardrail_adopted_but_not_MTS_derived"],
    "boundary_first_status": ["M_H_ref", "missing_claim_valid_source_or_zero_theorem"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1644_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1644_MSTAR_THEOREM_ATTEMPT.csv"
CLAUSE_MAP = OUT / "P8_Y5_PARENT_QLOC_1644_SAME_FRAME_DENOMINATOR_CLAUSE_MAP.csv"
BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_1644_NONCIRCULAR_DENOMINATOR_BLOCKERS.csv"
INPUT_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1644_NORMALIZED_PPN_INPUT_UPDATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1644_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1644_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1644_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1644_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    THEOREM_ATTEMPT,
    CLAUSE_MAP,
    BLOCKERS,
    INPUT_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    THEOREM_ATTEMPT,
    CLAUSE_MAP,
    BLOCKERS,
    INPUT_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {"valid_for_claim", "valid_for_mts_claim", "claim_allowed", "score_allowed"}
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1644 same-frame source-mass denominator ownership audit",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, object]]:
    source_paths = ";".join(
        str(SOURCE_FILES[key])
        for key in ["1006_denominator", "1016_selector", "449_ward", "worldtube_clauses", "hwt_attempt"]
    )
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_0_candidate_definition",
            "statement": "M_* := M_H_ref := H_tau[S_outer] - H_ref is the only noncircular denominator candidate on this branch",
            "mathematical_form": "q_R = Q_R c^2/(2 G M_*); M_* = M_H_ref = H_tau[S_outer] - H_ref",
            "current_status": "DEFINITION_GUARDRAIL_PASS_NONCLAIM",
            "blocker": "definition exists but parent ownership, integrability, fixed reference, positivity, and calibration are unsigned",
            "source_paths": source_paths,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_1_parent_current_owner",
            "statement": "the parent action owns the Hilbert/Noether source current J_H[tau] in the observed coframe",
            "mathematical_form": "J_H[tau] := delta S_matter/delta e_obs contracted with tau",
            "current_status": "UNSIGNED_PARENT_ACTION_OWNER",
            "blocker": "single observed coframe and source-current ownership remain contract-level",
            "source_paths": ";".join([str(SOURCE_FILES["1016_selector"]), str(SOURCE_FILES["449_ward"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_2_integrability",
            "statement": "H_tau is an integrable Hamiltonian charge for the same tau and surface class",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau - i_tau Theta)",
            "current_status": "FAIL_CURRENT_CLAIM",
            "blocker": "integrability/reference lock is explicitly not derived",
            "source_paths": str(SOURCE_FILES["1016_selector"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_3_tau_coframe_lock",
            "statement": "the same tau/coframe controls source, clocks, boundary charge, orbital readout, and PPN projection",
            "mathematical_form": "tau_source = tau_clock = tau_orbit = tau_PPN; e_source = e_obs",
            "current_status": "UNSIGNED_SAME_FRAME_LOCK",
            "blocker": "frame or readout leakage could change the denominator",
            "source_paths": str(SOURCE_FILES["1016_selector"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_4_fixed_reference_boundary",
            "statement": "H_ref and boundary/improvement terms are fixed before the source is read",
            "mathematical_form": "M_H_ref = H_tau[S_outer] - H_ref with delta H_ref = 0 and zero hidden boundary shift",
            "current_status": "UNSIGNED_REFERENCE_LOCK",
            "blocker": "boundary/reference first-row status has no claim-valid M_H_ref row",
            "source_paths": ";".join([str(SOURCE_FILES["boundary_first_status"]), str(SOURCE_FILES["1016_selector"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_5_positivity_finiteness",
            "statement": "M_H_ref is finite and positive after reference subtraction",
            "mathematical_form": "0 < M_H_ref < infinity",
            "current_status": "UNSIGNED_POSITIVITY",
            "blocker": "no parent positive-energy/reference theorem is currently signed for this branch",
            "source_paths": str(SOURCE_FILES["1006_denominator"]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_6_poisson_gauss_orbital_bridge",
            "statement": "the same source charge becomes the measured Newtonian/orbital monopole only after a Poisson/Gauss bridge",
            "mathematical_form": "M_H_ref -> integral_S grad Phi . dS /(4 pi G_ref) -> GM_orbit/G_ref",
            "current_status": "MISSING_CALIBRATION_BRIDGE",
            "blocker": "measured orbital GM is not yet parent-derived from the Hilbert charge",
            "source_paths": ";".join([str(SOURCE_FILES["449_ward"]), str(SOURCE_FILES["worldtube_clauses"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_7_anti_circularity",
            "statement": "GM_orbit/G_ref cannot be imported as M_* before the above bridge is derived",
            "mathematical_form": "M_* != GM_orbit/G_ref unless M_H_ref -> Poisson/Gauss -> orbital readout is already proved",
            "current_status": "GUARDRAIL_PASS_NONCLAIM",
            "blocker": "using orbital GM now would borrow Newton/GR to prove the local Newton/GR normalization",
            "source_paths": ";".join([str(SOURCE_FILES["1006_denominator"]), str(SOURCE_FILES["1643_next"])]),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MST1644_8_verdict",
            "statement": "M_star_same_frame is parent-signed or source-backed for current MTS",
            "mathematical_form": "M_star_same_frame = M_H_ref with all ownership/certificates signed",
            "current_status": "FAIL_CURRENT_CLAIM",
            "blocker": "M_H_ref is structurally identified but not parent-signed, source-filled, or orbitally calibrated",
            "source_paths": source_paths,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def clause_map_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_0_parent_action",
            "required_clause": "explicit parent action and symplectic potential define the source current and charge",
            "mathematical_form": "delta L = E_A delta Phi^A + dTheta; J_H[tau], Q_tau owned by L",
            "current_status": "CONTRACT_ONLY",
            "failure_if_missing": "H_tau and M_H_ref are placeholders",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_1_same_frame_source",
            "required_clause": "matter, clocks, rods, photon/PPN readout, and source charge use one observed coframe",
            "mathematical_form": "S_matter = S_matter[e_obs, psi]; tau_source = tau_readout",
            "current_status": "UNSIGNED",
            "failure_if_missing": "frame leakage can masquerade as source mass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_2_worldtube_selector",
            "required_clause": "source worldtube is selected by parent Hilbert support before fitting",
            "mathematical_form": "W_source = closure(supp J_H[tau])",
            "current_status": "CONDITIONAL_SELECTOR_ONLY",
            "failure_if_missing": "source domain can be chosen post hoc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_3_charge_definition",
            "required_clause": "denominator is the dressed Hilbert/Noether source charge",
            "mathematical_form": "M_H_ref = H_tau[S_outer] - H_ref = integral_S Q_tau",
            "current_status": "DEFINITION_GUARDRAIL_ONLY",
            "failure_if_missing": "no noncircular denominator for q_R exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_4_integrability_reference",
            "required_clause": "H_tau is integrable and H_ref/counterterms are fixed once",
            "mathematical_form": "delta H_tau exact on phase space; delta H_ref = 0 under readout changes",
            "current_status": "NOT_DERIVED",
            "failure_if_missing": "boundary/reference bookkeeping can move the mass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_5_positivity",
            "required_clause": "reference-subtracted source charge is finite and positive",
            "mathematical_form": "0 < H_tau[S_outer] - H_ref < infinity",
            "current_status": "NOT_DERIVED",
            "failure_if_missing": "q_R normalization can be sign/scale ambiguous",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_6_poisson_gauss",
            "required_clause": "Hilbert/Noether mass calibrates to the Newtonian source monopole",
            "mathematical_form": "M_H_ref -> M_eff[J_H] -> Phi with nabla^2 Phi = 4 pi G rho",
            "current_status": "MISSING_BRIDGE",
            "failure_if_missing": "orbital GM cannot be used as an input denominator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_7_no_hidden_leakage",
            "required_clause": "hidden coupling/source/boundary sectors are theorem-zero or explicitly retained",
            "mathematical_form": "q_retained = 0 or enters absolute residual vector",
            "current_status": "NOT_DERIVED",
            "failure_if_missing": "denominator and numerator can hide source leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "MDC1644_8_anti_circularity",
            "required_clause": "no orbital-GM backfill until the parent bridge is proved",
            "mathematical_form": "M_* cannot be fit or imported from the same local orbit being explained",
            "current_status": "GUARDRAIL_INSTALLED",
            "failure_if_missing": "local-GR proof becomes circular",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1644_0_Mstar_same_frame",
            "quantity": "M_star_same_frame",
            "blocker_type": "MISSING_PARENT_SIGNED_MHREF_DENOMINATOR",
            "why_needed": "normalizes Q_R/Pi_R into dimensionless q_R through N_R = c^2/(2 G M_*)",
            "repair": "derive H_tau-H_ref integrability/reference/positivity in one observed frame or source a legitimate parent row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1644_1_Htau_integrability",
            "quantity": "H_tau",
            "blocker_type": "MISSING_INTEGRABILITY_CERTIFICATE",
            "why_needed": "turns the denominator from a symbol into a phase-space charge",
            "repair": "prove delta H_tau is exact on the allowed local branch with fixed surface class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1644_2_Href_reference_lock",
            "quantity": "H_ref",
            "blocker_type": "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "why_needed": "prevents the denominator from absorbing boundary/readout shifts",
            "repair": "derive fixed reference/counterterm rule and zero hidden boundary shift",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1644_3_positive_finite_mass",
            "quantity": "M_H_ref",
            "blocker_type": "MISSING_POSITIVITY_FINITE_CERTIFICATE",
            "why_needed": "q_R bound is meaningless if denominator can vanish, flip sign, or diverge",
            "repair": "prove positive finite source charge after reference subtraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1644_4_poisson_gauss_orbital_bridge",
            "quantity": "GM_orbit/G_ref",
            "blocker_type": "ORBITAL_GM_IMPORT_REJECTED",
            "why_needed": "external/local readout must be derived from the parent charge before use",
            "repair": "derive M_H_ref -> Poisson/Gauss monopole -> orbital GM bridge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "blocker_id": "BLK1644_5_absolute_residual_vector",
            "quantity": "absolute_local_residual_vector",
            "blocker_type": "MISSING_NO_CANCELLATION_COMPONENTS",
            "why_needed": "finite Pi_R scoring must not hide cancellations among source, boundary, frame, domain, and coupling terms",
            "repair": "source or zero each component before any local-PPN pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def input_update_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1644_0_PiR_boundary_abs",
            "quantity": "Pi_R_boundary_abs",
            "required_for_formula": "|q_R| = k_W |Pi_R| c^2/(2 G M_*)",
            "current_value": "MISSING_BOUND_VALUE",
            "source_status": "MISSING_PARENT_OR_EMPIRICAL_SOURCE_PATH",
            "runner_status": "BLOCKED",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1644_1_Mstar_same_frame",
            "quantity": "M_star_same_frame",
            "required_for_formula": "N_R = c^2/(2 G M_*)",
            "current_value": "MISSING_PARENT_SIGNED_MHREF_DENOMINATOR",
            "source_status": "MISSING_INTEGRABILITY_REFERENCE_POSITIVITY_AND_CALIBRATION",
            "runner_status": "BLOCKED_NONCIRCULAR_DENOMINATOR",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1644_2_kW_tail",
            "quantity": "k_W_tail",
            "required_for_formula": "maps boundary/tail coefficient into Pi_R contribution",
            "current_value": "CORPUS_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_status": "MISSING_PARENT_SIGNATURE",
            "runner_status": "BLOCKED",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1644_3_delta_gamma_bound",
            "quantity": "Delta_gamma_abs_max",
            "required_for_formula": "|q_R| <= |Delta gamma|max",
            "current_value": "6.7e-5",
            "source_status": "SOURCE_BACKED_BOUND_INPUT_ONLY_CASSINI",
            "runner_status": "AVAILABLE_AS_EXTERNAL_BOUND_ONLY",
            "valid_for_runner": True,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "IN1644_4_absolute_residual_vector",
            "quantity": "absolute_local_residual_vector",
            "required_for_formula": "no-cancellation denominator/numerator safety vector",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "source_status": "MISSING_NO_CANCELLATION_COMPONENTS",
            "runner_status": "BLOCKED",
            "valid_for_runner": False,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1644_0_Mstar_not_claimed",
            "decision": "do not claim M_star_same_frame/M_H_ref",
            "reason": "the same-frame denominator is structurally identified but not parent-signed or source-backed",
            "effect": "finite Pi_R PPN bound runner remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1644_1_candidate_retained",
            "decision": "retain M_* = M_H_ref = H_tau[S_outer] - H_ref as the legal candidate",
            "reason": "it is the only route that avoids fitting/importing the denominator from orbital GM",
            "effect": "next proof must sign integrability/reference/positivity/calibration clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1644_2_orbital_GM_refused",
            "decision": "reject GM_orbit/G_ref as a denominator input at this stage",
            "reason": "using orbital GM now would borrow Newton/GR to prove the local Newton/GR normalization",
            "effect": "no circular local-GR pass can be manufactured from the current branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1644_3_next_integrability_reference_lock",
            "decision": "move next to H_tau/M_H_ref integrability-reference lock",
            "reason": "this is the nearest upstream certificate that can convert the candidate denominator into a real parent charge",
            "effect": "1645 should attempt the charge theorem first, then stage Mstar source rows if it fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1644_0_Mstar_same_frame",
            "claim": "M_star_same_frame is a parent-signed source denominator",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_PARENT_SIGNED_MHREF_DENOMINATOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1644_1_normalized_PPN_runner",
            "claim": "finite Pi_R normalized PPN branch can be scored",
            "gate_pass": False,
            "status": "NOT_SCORED",
            "blocker": "missing Pi_R numerator and noncircular Mstar denominator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1644_2_orbital_GM_shortcut",
            "claim": "orbital GM can fill Mstar before parent bridge",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "ORBITAL_GM_SUBSTITUTION_REJECTED_AS_CIRCULAR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1644_3_local_GR_or_PPN_pass",
            "claim": "local GR/PPN/R10 pass follows from 1644",
            "gate_pass": False,
            "status": "NO_CLAIM",
            "blocker": "denominator, numerator, and absolute residual vector remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1644_4_guardrail",
            "claim": "noncircular denominator guardrail is installed",
            "gate_pass": True,
            "status": "PASS_AS_INTERNAL_GUARDRAIL_ONLY",
            "blocker": "guardrail is useful but not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md",
            "script": "scripts/Y5_R2FR_Htau_MHref_integrability_reference_lock_or_Mstar_source_row.py",
            "objective": "derive the integrable fixed-reference Hamiltonian charge M_H_ref=H_tau[S_outer]-H_ref in the observed frame, or stage explicit nonclaim Mstar source rows",
            "success_condition": "M_H_ref has parent-owned H_tau, fixed H_ref, same tau/coframe, finite positive value, no hidden boundary/source leakage, and no orbital-GM import",
            "guardrails": "do not use orbital GM; do not claim PPN/local-GR/R10; keep Cassini as bound input only; score no placeholders",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for path in GENERATED + [VALIDATION]:
        if path.exists():
            shutil.copy2(path, QUARANTINE / path.name)
            shutil.copy2(path, BRANCH_RESIDUALS / path.name)
    shutil.copy2(THEOREM_ATTEMPT, QUEUE / "JR1644_MSTAR_THEOREM_ATTEMPT_NONCLAIM.csv")
    shutil.copy2(BLOCKERS, QUEUE / "JR1644_NONCIRCULAR_DENOMINATOR_BLOCKERS_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1644_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, object]]:
    sources = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_ATTEMPT)
    clauses = csv_rows(CLAUSE_MAP)
    blockers = csv_rows(BLOCKERS)
    inputs = csv_rows(INPUT_UPDATE)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    generated_csvs_parse = all(len(csv_rows(path)) > 0 for path in GENERATED)
    no_missing_promoted = all(
        bool_string(row.get("valid_for_claim", row.get("valid_for_mts_claim", "false"))) == "false"
        for path in CLAIM_CHECKED
        for row in csv_rows(path)
    )
    checks = [
        (
            "VAL1644_0_sources_exist",
            all(bool_string(row["path_exists"]) == "true" and bool_string(row["needles_found"]) == "true" for row in sources),
            "all cited 1644 source paths exist and needles are present",
        ),
        (
            "VAL1644_1_candidate_definition_present",
            any(row["attempt_id"] == "MST1644_0_candidate_definition" for row in theorem),
            "Mstar candidate is written as M_H_ref=H_tau[S_outer]-H_ref",
        ),
        (
            "VAL1644_2_verdict_blocks_claim",
            any(row["attempt_id"] == "MST1644_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in theorem),
            "theorem attempt refuses to promote Mstar",
        ),
        (
            "VAL1644_3_orbital_GM_refused",
            any("ORBITAL_GM" in row["blocker_type"] for row in blockers)
            and any(row["decision_id"] == "DEC1644_2_orbital_GM_refused" for row in decisions),
            "orbital GM shortcut is refused as circular",
        ),
        (
            "VAL1644_4_denominator_clauses_blocked",
            any(row["clause_id"] == "MDC1644_4_integrability_reference" and row["current_status"] == "NOT_DERIVED" for row in clauses)
            and any(row["clause_id"] == "MDC1644_6_poisson_gauss" and row["current_status"] == "MISSING_BRIDGE" for row in clauses),
            "integrability/reference and Poisson/Gauss clauses remain blocked",
        ),
        (
            "VAL1644_5_input_update_blocks_runner",
            any(
                row["quantity"] == "M_star_same_frame"
                and row["runner_status"] == "BLOCKED_NONCIRCULAR_DENOMINATOR"
                and bool_string(row["valid_for_runner"]) == "false"
                for row in inputs
            ),
            "normalized PPN input update keeps Mstar invalid",
        ),
        (
            "VAL1644_6_cassini_bound_input_only",
            any(
                row["quantity"] == "Delta_gamma_abs_max"
                and bool_string(row["valid_for_runner"]) == "true"
                and bool_string(row["valid_for_mts_claim"]) == "false"
                for row in inputs
            ),
            "Cassini gamma remains an external bound input only",
        ),
        (
            "VAL1644_7_claim_gates_safe",
            any(row["gate_id"] == "CG1644_4_guardrail" and row["status"] == "PASS_AS_INTERNAL_GUARDRAIL_ONLY" for row in gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in gates),
            "all claim gates keep MTS claims false",
        ),
        (
            "VAL1644_8_next_target_selected",
            next_targets[0]["next_target"] == "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md",
            "next target selects Htau/MHref integrability-reference lock",
        ),
        (
            "VAL1644_9_csv_parse",
            generated_csvs_parse,
            "all generated 1644 CSVs parse",
        ),
        (
            "VAL1644_10_no_mts_claim_flags",
            all_claim_flags_false(CLAIM_CHECKED) and no_missing_promoted,
            "all 1644 generated rows keep MTS claim/no-score flags false",
        ),
        (
            "VAL1644_11_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1644_12_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1644_MSTAR_THEOREM_ATTEMPT_NONCLAIM.csv",
                    QUEUE / "JR1644_NONCIRCULAR_DENOMINATOR_BLOCKERS_NONCLAIM.csv",
                    QUEUE / "JR1644_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1644_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1644_14_formalization_untouched",
            not any(FORMALIZATION.rglob("*1644*")) if FORMALIZATION.exists() else True,
            "no 1644 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1644_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1644 Mstar same-frame denominator owner or noncircular blocker validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    sources = csv_rows(SOURCE_REGISTER)
    theorem = csv_rows(THEOREM_ATTEMPT)
    clauses = csv_rows(CLAUSE_MAP)
    blockers = csv_rows(BLOCKERS)
    inputs = csv_rows(INPUT_UPDATE)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_targets = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)
    content = f"""# 1644 - Mstar Same-Frame Source-Mass Owner Or Noncircular Denominator Blocker

**Private status:** nonclaim checkpoint. No PPN pass, local-GR pass, Newton pass, orbital pass, WEP pass, R10 pass, clock pass, or galaxy/cosmology claim is made here.

## Verdict

The finite reciprocal-hair branch needs a denominator before it can even be honestly compared to a PPN bound:

```text
q_R = Q_R c^2/(2 G M_*)
M_* := M_H_ref := H_tau[S_outer] - H_ref
```

That is the correct-looking object, but current MTS does not yet own it as a theorem. The parent route still needs:

```text
owned J_H[tau] + fixed tau/e_obs + integrable H_tau + fixed H_ref
+ positive finite M_H_ref + Poisson/Gauss calibration + no hidden source leakage
```

So the denominator is **not** claimed. `GM_orbit/G_ref` is explicitly refused as a shortcut because it would borrow the Newton/GR source normalization we are trying to derive. The win in this checkpoint is smaller but important: the legal target is now sharp, and the circular route is locked out.

## Source Register

{markdown_table(sources, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Mstar Theorem Attempt

{markdown_table(theorem, ["attempt_id", "statement", "mathematical_form", "current_status", "blocker"])}

## Same-Frame Denominator Clause Map

{markdown_table(clauses, ["clause_id", "required_clause", "mathematical_form", "current_status", "failure_if_missing"])}

## Noncircular Denominator Blockers

{markdown_table(blockers, ["blocker_id", "quantity", "blocker_type", "why_needed", "repair"])}

## Normalized PPN Input Update

{markdown_table(inputs, ["input_id", "quantity", "current_value", "source_status", "runner_status", "valid_for_runner"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "effect"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        THEOREM_ATTEMPT: theorem_attempt_rows(),
        CLAUSE_MAP: clause_map_rows(),
        BLOCKERS: blocker_rows(),
        INPUT_UPDATE: input_update_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)
    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
