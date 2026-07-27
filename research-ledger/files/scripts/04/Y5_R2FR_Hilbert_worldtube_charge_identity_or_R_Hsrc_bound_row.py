from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1818"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1818-Y5-R2FR-Hilbert-worldtube-charge-identity-or-R-Hsrc-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1818_0_1817_doc",
        "source_key": "1817_handoff_doc",
        "source_path": ROOT / "1817-Y5-R2FR-source-worldtube-transfer-kernel-or-post-current-cA-bound-row.md",
        "needles": ["DEC1817_3_best_next", "NEXT1817_0_primary"],
        "role": "1817 selects the Hilbert-worldtube charge identity as the next target.",
    },
    {
        "source_id": "SRC1818_1_1817_validation",
        "source_key": "1817_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1817_VALIDATION.csv",
        "needles": ["VAL1817_OVERALL", "PASS"],
        "role": "confirms 1817 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1818_2_1817_theorem",
        "source_key": "1817_transfer_kernel_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_SOURCE_WORLDTUBE_TRANSFER_KERNEL_THEOREM.csv",
        "needles": ["KWT1817_3_charge_source_identity", "KEY_IDENTITY_MISSING"],
        "role": "identifies exterior charge/projected Hilbert source equality as the key missing identity.",
    },
    {
        "source_id": "SRC1818_3_1817_residual",
        "source_key": "1817_R_Hsrc_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1817_K_ARENA_RESIDUAL_ROWS.csv",
        "needles": ["KAR1817_3_R_Hsrc", "MISSING_HILBERT_WORLDTUBE_CHARGE_IDENTITY"],
        "role": "R_Hsrc is the explicit residual row inherited from 1817.",
    },
    {
        "source_id": "SRC1818_4_1778_worldtube_current",
        "source_key": "1778_worldtube_current_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_WORLDTUBE_CURRENT_MAP.csv",
        "needles": ["WCM1778_1_chain_identity", "MISSING_CHAIN_IDENTITY"],
        "role": "latest source-chain map says the charge identity is missing.",
    },
    {
        "source_id": "SRC1818_5_536_theorem",
        "source_key": "536_hilbert_worldtube_glue",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "not_derived"],
        "role": "older Hilbert/worldtube attempt names the unproved Pi_M charge map.",
    },
    {
        "source_id": "SRC1818_6_535_certificate",
        "source_key": "535_hilbert_worldtube_certificate",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
        "needles": ["HWG535_4_commutator_zero", "missing_certificate_or_bound"],
        "role": "certificate ledger keeps Pi_M commutator and exact boundary terms open.",
    },
    {
        "source_id": "SRC1818_7_537_contract",
        "source_key": "537_parent_action_contract",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "needles": ["PAC537_5_Hilbert_topological_charge_equality", "not_derived"],
        "role": "parent action contract states the needed Hilbert/topological charge equality.",
    },
    {
        "source_id": "SRC1818_8_501_attempt",
        "source_key": "501_topological_hilbert_equality",
        "source_path": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "needles": ["EH501_0_equality_statement", "Pi_M J_H = J_M_top + dB_zero + R_eq"],
        "role": "topological/Hilbert equality target and residual shape.",
    },
    {
        "source_id": "SRC1818_9_501_obstructions",
        "source_key": "501_topological_hilbert_obstructions",
        "source_path": RESIDUALS / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
        "needles": ["OB501_0_independent_topological_label", "not_parent_derived"],
        "role": "wrong-conserved-object obstruction remains active.",
    },
    {
        "source_id": "SRC1818_10_499_identity",
        "source_key": "499_parent_source_identity",
        "source_path": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv",
        "needles": ["I499_3_parent_source_identity", "derived_as_decomposition_not_zero"],
        "role": "parent source identity supplies an exact decomposition, not a zero proof.",
    },
    {
        "source_id": "SRC1818_11_499_residuals",
        "source_key": "499_source_identity_residuals",
        "source_path": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "needles": ["S499_0_projector_commutator", "not_parent_derived"],
        "role": "residual decomposition lists the active source-identity failure modes.",
    },
    {
        "source_id": "SRC1818_12_509_theorem",
        "source_key": "509_source_measure_flux",
        "source_path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "needles": ["T509_0_charge_identity_needed", "not_parent_derived"],
        "role": "source measure/exterior flux equality is required and not parent-derived.",
    },
    {
        "source_id": "SRC1818_13_554_integrability",
        "source_key": "554_hamiltonian_integrability",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
        "needles": ["HCI554_2_parent_Lagrangian_theta_Q", "not_derived"],
        "role": "explicit Lagrangian, symplectic potential and Q_tau are not yet derived for current MTS.",
    },
    {
        "source_id": "SRC1818_14_505_noether",
        "source_key": "505_parent_noether_closure",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "needles": ["T505_source_measure_matching", "core_glue_not_yet_parent_derived"],
        "role": "Noether closure theorem is conditional and source matching remains the core glue.",
    },
    {
        "source_id": "SRC1818_15_newton_stack",
        "source_key": "source_normalized_newton_stack",
        "source_path": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
        "needles": ["SN3_charge_equals_Hilbert_mass_current", "not_parent_derived"],
        "role": "Newton stack blocks source-normalized Newton until charge equals Hilbert mass current.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_SOURCE_REGISTER.csv",
    "charge_identity_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv",
    "identity_clause_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_IDENTITY_CLAUSE_AUDIT.csv",
    "R_Hsrc_residual_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_R_HSRC_RESIDUAL_ROWS.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1818_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for path in {RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "pass", "passed"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        text = read_text(path)
        exists = path.exists()
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def charge_identity_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_0_target",
            "claim": "Hilbert-worldtube charge identity connects parent source to Newton/GR mass",
            "mathematical_statement": "G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc, with R_Hsrc=0, is the needed bridge between exterior Hamiltonian charge and the projected observed Hilbert source.",
            "proof_status": "TARGET_EXACT",
            "current_corpus_status": "R_HSRC_NOT_ZERO",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_1_noether_charge",
            "claim": "parent covariant phase space defines Q_tau",
            "mathematical_statement": "If delta L=E_A delta Phi^A+dTheta and tau is fixed, then on shell J_tau=Theta(Phi,L_tau Phi)-i_tau L=dQ_tau+C_tau; this gives a candidate exterior Hamiltonian mass charge.",
            "proof_status": "EXACT_IF_PARENT_L_THETA_Q_SIGNED",
            "current_corpus_status": "PARENT_LAGRANGIAN_THETA_Q_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_2_hilbert_source",
            "claim": "same observed matter action defines J_H",
            "mathematical_statement": "J_H is the Hilbert/coframe source current from the same observed matter action and same tau used by the exterior charge.",
            "proof_status": "CONDITIONAL_SOURCE_OWNER",
            "current_corpus_status": "SAME_FRAME_SOURCE_MEASURE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_3_worldtube_support",
            "claim": "compact worldtube support is fixed before readout",
            "mathematical_statement": "W_source=closure(supp J_H[tau]) and linking surfaces enclose that same support, so source selection is not an orbital/readout fit.",
            "proof_status": "CONDITIONAL_LEMMA",
            "current_corpus_status": "WORLDTUBE_SUPPORT_OWNER_NOT_PROVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_4_identity_equality",
            "claim": "Q_tau equals the Pi_M-projected Hilbert source up to exact zero-flux terms",
            "mathematical_statement": "The conserved exterior charge must be the same object as the measured source current, not a separate topological label or boundary bookkeeping variable.",
            "proof_status": "KEY_EQUALITY_MISSING",
            "current_corpus_status": "WRONG_CONSERVED_OBJECT_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_5_residual_decomposition",
            "claim": "R_Hsrc has a finite no-cancellation decomposition",
            "mathematical_statement": "R_Hsrc is bounded by source equality mismatch, Pi_M commutator/projector stress, boundary/reference flux, extra-sector charge, frame mismatch, and calibration mismatch components.",
            "proof_status": "DECOMPOSITION_READY_NOT_ZERO",
            "current_corpus_status": "R_HSRC_COMPONENTS_UNFILLED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_6_newton_corollary",
            "claim": "identity plus EH/Poisson limit gives Newton source mass",
            "mathematical_statement": "If HCI1818_0 closes and the local exterior is EH with standard weak-field normalization, then the same source charge controls the Newton/Gauss monopole.",
            "proof_status": "CONDITIONAL_COROLLARY",
            "current_corpus_status": "EH_POISSON_PPN_STACK_STILL_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HCI1818_7_verdict",
            "claim": "1818 proves the Hilbert-worldtube charge identity in the current corpus",
            "mathematical_statement": "The identity closes only if parent Lagrangian/theta/Q_tau, same-frame Hilbert source, worldtube support, exact boundary zero, Pi_M constancy, extra-sector silence and calibration are signed together.",
            "proof_status": "CONDITIONAL_IDENTITY_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_R_HSRC_RESIDUAL_ROWS",
            "valid_for_claim": False,
        },
    ]


def identity_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_0_parent_L_theta_Q",
            "needed_clause": "explicit parent Lagrangian, symplectic potential and Hamiltonian charge",
            "source_anchor": "HCI554_2_parent_Lagrangian_theta_Q; PAC537_0_covariant_parent_action",
            "current_status": "NOT_DERIVED_FOR_CURRENT_MTS",
            "failure_if_missing": "Q_tau is a candidate charge rather than a derived parent object",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_1_tau_lock",
            "needed_clause": "same observed time generator in source variation, charge and readout",
            "source_anchor": "HCI554_4_time_generator_lock; WTO1718_2_tau_lock",
            "current_status": "TAU_SOURCE_READOUT_LOCK_OPEN",
            "failure_if_missing": "charge/source equality can be frame/time dependent",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_2_same_frame_Hilbert_source",
            "needed_clause": "matter source, clocks, rods and orbital readout use the same observed coframe",
            "source_anchor": "HWT536_1_observed_Hilbert_measure_owned; SN0_same_observed_frame",
            "current_status": "SAME_FRAME_SOURCE_MEASURE_NOT_PARENT_SIGNED",
            "failure_if_missing": "Hilbert source and orbital/Newton source can live in different frames",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_3_PiM_owned_projector",
            "needed_clause": "Pi_M is parent-owned, fixed and covariantly constant on the local source-current space",
            "source_anchor": "HWG535_4_commutator_zero; S499_0_projector_commutator",
            "current_status": "PROJECTOR_COMMUTATOR_NOT_ZERO",
            "failure_if_missing": "Pi_M can create source hair through product-rule/projector stress",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_4_boundary_reference_zero",
            "needed_clause": "exact improvement, reference and symplectic-boundary terms have zero compact flux",
            "source_anchor": "HWG535_3_exact_term_zero; HCI554_5_symplectic_boundary_flux",
            "current_status": "BOUNDARY_REFERENCE_FLUX_OPEN",
            "failure_if_missing": "surface charge equality can shift by bookkeeping terms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_5_extra_sector_silence",
            "needed_clause": "motion/time/domain/memory/range/connection/non-EH sectors carry no independent mass charge",
            "source_anchor": "HWT536_7_extra_sector_charge_silence; C505_extra",
            "current_status": "FIELD_SPECIFIC_SILENCE_QUEUE_OPEN",
            "failure_if_missing": "MTS extra sectors can repair fits while breaking local GR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_6_gauss_newton_calibration",
            "needed_clause": "dressed charge normalizes to the weak-field inverse-square coefficient",
            "source_anchor": "PG1_charge_equals_projected_Hilbert_source; SN3_charge_equals_Hilbert_mass_current",
            "current_status": "NEWTON_GAUSS_CALIBRATION_NOT_DERIVED",
            "failure_if_missing": "closed charge may not be measured Newtonian mass",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "ICA1818_7_verdict",
            "needed_clause": "all charge identity clauses close",
            "source_anchor": "HCI1818_0 through HCI1818_6",
            "current_status": "FAIL_CURRENT_ZERO_PROOF",
            "failure_if_missing": "retain R_Hsrc and source-normalized Newton blockers",
            "valid_for_claim": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RHS1818_0_source_equality",
            "quantity": "epsilon_HPiM_source_equality_abs",
            "definition": "mismatch between exterior Hamiltonian charge and projected Hilbert source",
            "formal_expression": "||G_ref^-1 Q_tau - Pi_M^H J_H^dress||/||Pi_M^H J_H^dress||",
            "zero_condition": "Hilbert-worldtube charge identity closes with same-frame source and tau",
            "required_inputs": "Q_tau; Pi_M_H; J_H_dress; source_norm; tau_lock; source_path",
            "current_status": "MISSING_SOURCE_EQUALITY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_source_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_HSRC_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RHS1818_1_PiM_commutator",
            "quantity": "epsilon_PiM_commutator_abs",
            "definition": "mass-projector product-rule or stress mismatch",
            "formal_expression": "||[d,Pi_M]J_H||/||Pi_M J_H||",
            "zero_condition": "Pi_M is parent-owned, fixed and covariantly constant on the exterior source-current space",
            "required_inputs": "Pi_M definition; commutator theorem or value; source_norm; units; source_path",
            "current_status": "MISSING_PIM_COMMUTATOR_ZERO_OR_BOUND",
            "units": "dimensionless_projector_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_PIM_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RHS1818_2_boundary_reference",
            "quantity": "epsilon_boundary_reference_abs",
            "definition": "exact improvement, reference and symplectic-boundary flux mismatch",
            "formal_expression": "||dB_H + Delta_ref + Delta_symp||/||source charge||",
            "zero_condition": "exact terms have zero linking-sphere flux and reference is fixed once",
            "required_inputs": "B_H; reference term; symplectic flux; boundary theorem or value; units; source_path",
            "current_status": "MISSING_BOUNDARY_REFERENCE_ZERO_OR_BOUND",
            "units": "dimensionless_boundary_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_BOUNDARY_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RHS1818_3_extra_charge",
            "quantity": "epsilon_extra_charge_abs",
            "definition": "non-EH/domain/memory/range/connection/source-normalization mass charge",
            "formal_expression": "||Delta_nonEH + Delta_extra + Delta_frame + Delta_domain||/||source charge||",
            "zero_condition": "all extra sectors are silent/topological or individually bounded below local locks",
            "required_inputs": "channel matrix; source norms; theorem-zero certificates or numeric bounds; source paths",
            "current_status": "MISSING_EXTRA_SECTOR_CHARGE_SILENCE_OR_BOUND",
            "units": "dimensionless_extra_charge_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_EXTRA_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RHS1818_4_frame_calibration",
            "quantity": "epsilon_frame_calibration_abs",
            "definition": "same-frame and Gauss/Newton calibration mismatch",
            "formal_expression": "abs(Delta_frame_source)+abs(Delta_cal_Gauss)+abs(Delta_Gref)",
            "zero_condition": "observed source frame and weak-field Gauss/Poisson calibration are derived from the same parent charge",
            "required_inputs": "frame certificate; Gauss calibration; G_ref lock; units; source_path",
            "current_status": "MISSING_FRAME_CALIBRATION_THEOREM_OR_BOUND",
            "units": "dimensionless_calibration_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_CALIBRATION_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RHS1818_5_total",
            "quantity": "epsilon_R_Hsrc_total_abs",
            "definition": "total no-cancellation envelope for Hilbert-worldtube charge identity failure",
            "formal_expression": "abs(RHS1818_0)+abs(RHS1818_1)+abs(RHS1818_2)+abs(RHS1818_3)+abs(RHS1818_4)",
            "zero_condition": "all charge/source equality, projector, boundary, extra-sector and calibration terms theorem-zero or source-backed",
            "required_inputs": "all RHS1818 components; common normalizers; units; source paths; local locks",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "units": "absolute_no_cancellation_envelope",
            "source_path": "",
            "common_normalizer": "MISSING_TOTAL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1818_0_wrong_conserved_object",
            "countermodel": "Q_tau or J_M_top is closed but not equal to the observed Hilbert source charge",
            "why_it_defeats_claim": "Newton/GR source mass would be a conserved wrong object",
            "blocked_by": "Hilbert-worldtube charge identity or R_Hsrc bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1818_1_projector_commutator",
            "countermodel": "Pi_M depends on metric/domain/readout so [d,Pi_M]J_H is nonzero",
            "why_it_defeats_claim": "projector stress creates radial/source hair",
            "blocked_by": "parent-owned covariantly constant Pi_M theorem or bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1818_2_boundary_reference_shift",
            "countermodel": "exact/reference/symplectic boundary term has nonzero compact flux",
            "why_it_defeats_claim": "surface charge equality shifts by bookkeeping terms",
            "blocked_by": "zero-flux boundary/reference theorem or source-backed bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1818_3_extra_sector_mass_charge",
            "countermodel": "motion/time/domain/memory/range/connection sector carries Pi_M mass charge",
            "why_it_defeats_claim": "extra sectors can create non-GR monopole or PPN source residues",
            "blocked_by": "field-specific silence theorem or residual coefficient map",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1818_4_orbital_GM_smuggling",
            "countermodel": "orbital GM is used to define the source charge rather than derived from it",
            "why_it_defeats_claim": "Newton recovery becomes calibration, not derivation",
            "blocked_by": "Gauss/Poisson calibration theorem after charge identity",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1818_0_if_identity_closes",
            "if_closed": "R_Hsrc is theorem-zero",
            "would_buy": "exterior Hamiltonian charge and observed Hilbert source become the same parent object",
            "still_missing": "EH/Poisson coefficient, constant G_ref, slow-particle readout and second-order PPN stability",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1818_1_Newton_bridge",
            "if_closed": "R_Hsrc=0 plus EH weak-field Gauss calibration closes",
            "would_buy": "source-normalized Newton becomes derivable rather than orbital-GM backfilled",
            "still_missing": "local EH symplectic charge inheritance and extra-sector silence remain unsigned",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1818_2_local_GR",
            "if_closed": "charge identity and Newton bridge close through second order",
            "would_buy": "PPN/local-GR source side becomes a serious derived branch",
            "still_missing": "gamma/beta/preferred-frame residual vector and non-EH operator ledger",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1818_3_verdict",
            "if_closed": "1818 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone; it is the source-mass identity subgate",
            "still_missing": "current corpus keeps R_Hsrc as an unfilled nonclaim residual",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1818_0_identity_contract",
            "gate": "Hilbert-worldtube charge identity written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "HCI1818 writes the exact source-mass bridge and the R_Hsrc decomposition",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1818_1_identity_zero",
            "gate": "R_Hsrc theorem-zero",
            "current_status": "BLOCKED",
            "reason": "charge/source equality, Pi_M, boundary/reference and extra-sector clauses are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1818_2_residual_values",
            "gate": "R_Hsrc residual rows source-backed",
            "current_status": "BLOCKED",
            "reason": "RHS1818 rows have missing component values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1818_3_newton_bridge",
            "gate": "source-normalized Newton promotion allowed",
            "current_status": "REFUSED",
            "reason": "R_Hsrc is not zero and EH/Poisson/Gauss calibration is not derived",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1818_4_local_gr",
            "gate": "PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "1818 is a source-mass identity subgate and second-order PPN stability is not reached",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1818_0_R_Hsrc_zero",
            "claim": "R_Hsrc=0",
            "status": "BLOCKED",
            "reason": "Hilbert-worldtube charge identity is not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1818_1_Newton_source_mass",
            "claim": "Newtonian source mass is derived",
            "status": "BLOCKED",
            "reason": "charge identity and Gauss/Poisson calibration are incomplete",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1818_2_orbital_GM",
            "claim": "orbital GM can be used as derived source identity",
            "status": "REFUSED",
            "reason": "orbital GM is calibration/readout unless the charge identity and weak-field bridge are proven first",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1818_3_local_GR_PPN",
            "claim": "local GR/PPN follows",
            "status": "REFUSED",
            "reason": "second-order source/operator residual vector is not derived or scored",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1818_0_identity_result",
            "decision": "R_HSRC_IDENTITY_CONTRACT_ONLY",
            "reason": "the exact identity is now stated, but the corpus has only decompositions and conditional routes, not a zero proof",
            "next_action": "retain R_Hsrc as nonclaim until charge identity components are signed or sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1818_1_core_blocker",
            "decision": "EXPLICIT_LOCAL_CPS_CHARGE_PACKAGE_MISSING",
            "reason": "without parent L, theta, Q_tau, tau lock and EH-plus-silent exterior, the identity cannot be derived",
            "next_action": "attack local EH symplectic charge inheritance rather than orbital calibration",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1818_2_residual_status",
            "decision": "R_HSRC_ROWS_READY_NONCLAIM",
            "reason": "R_Hsrc components are named with units/normalizers but unfilled",
            "next_action": "no row can be scored without theorem-zero certificate or source-backed values",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1818_3_best_next",
            "decision": "LOCAL_EH_SYMPLECTIC_CHARGE_INHERITANCE_NEXT",
            "reason": "the least empirical next derivation is to show MTS local exterior inherits the EH covariant-phase-space charge plus explicit C-term residuals",
            "next_action": "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1818_0_primary",
            "next_target": "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
            "script": "scripts/Y5_R2FR_local_EH_symplectic_charge_inheritance_or_Cterm_residual_vector.py",
            "objective": "derive the local exterior MTS charge as EH covariant-phase-space charge plus silent/topological sectors; if not, emit C_EH/C_extra/C_projector/C_boundary residual rows",
            "selection_status": "selected",
            "success_condition": "EH symplectic charge inheritance theorem-zero, or C-term residual vector becomes source-backed and remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1818_1_parallel",
            "next_target": "1819b-Y5-R2FR-R-Hsrc-source-backed-bound-fill-pack.md",
            "script": "scripts/Y5_R2FR_R_Hsrc_source_backed_bound_fill_pack.py",
            "objective": "fill R_Hsrc components with source-backed theorem-zero certificates or numeric bounds if derivation route stalls",
            "selection_status": "held_parallel",
            "success_condition": "R_Hsrc components parse, cite source paths, carry units and remain nonclaim until gates pass",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "charge_identity_theorem": charge_identity_theorem_rows(),
        "identity_clause_audit": identity_clause_rows(),
        "R_Hsrc_residual_rows": residual_rows(),
        "countermodel_ledger": countermodel_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output, target_dir / output.name)


def branch_copies_exist() -> bool:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            if not (target_dir / output.name).exists():
                return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    names = {DOC_PATH.name, OUTPUTS["validation"].name} | {path.name for path in generated_csvs()}
    return not any(path.name in names for path in FORMALIZATION.rglob("*") if path.is_file())


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_gate_pass = {"AC1818_0_identity_contract"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed_now", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if field == "gate_pass" and row.get("gate_id") in allowed_gate_pass:
                        continue
                    return False
    return True


def missing_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text and (
                boolish(row.get("score_ready", False))
                or boolish(row.get("valid_for_claim", False))
                or boolish(row.get("claim_allowed", False))
                or boolish(row.get("claim_allowed_now", False))
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1818_0_identity_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1818_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1818_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1818_2_identity_contract_written",
            any(row["theorem_id"] == "HCI1818_0_target" and row["proof_status"] == "TARGET_EXACT" for row in rows_map["charge_identity_theorem"]),
            "Hilbert-worldtube charge identity target is written",
        ),
        (
            "VAL1818_3_key_equality_missing",
            any(row["theorem_id"] == "HCI1818_4_identity_equality" and row["proof_status"] == "KEY_EQUALITY_MISSING" for row in rows_map["charge_identity_theorem"]),
            "key charge/source equality remains missing",
        ),
        (
            "VAL1818_4_theorem_not_promoted",
            any(row["theorem_id"] == "HCI1818_7_verdict" and row["proof_status"] == "CONDITIONAL_IDENTITY_NOT_CURRENT_PROOF" for row in rows_map["charge_identity_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["charge_identity_theorem"]),
            "1818 identity is not promoted as current proof",
        ),
        (
            "VAL1818_5_clause_audit_blocked",
            any(row["clause_id"] == "ICA1818_7_verdict" and row["current_status"] == "FAIL_CURRENT_ZERO_PROOF" for row in rows_map["identity_clause_audit"]),
            "identity clause audit remains blocked",
        ),
        (
            "VAL1818_6_residual_rows_nonclaim",
            any(row["residual_id"] == "RHS1818_5_total" for row in rows_map["R_Hsrc_residual_rows"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["R_Hsrc_residual_rows"]),
            "R_Hsrc residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1818_7_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1818_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1818_9_acceptance_blocks",
            any(row["gate_id"] == "AC1818_0_identity_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1818_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all source/Newton/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1818_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1818_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1818_13_decision_next",
            any(row["decision_id"] == "DEC1818_3_best_next" and row["decision"] == "LOCAL_EH_SYMPLECTIC_CHARGE_INHERITANCE_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects local EH symplectic charge inheritance next",
        ),
        (
            "VAL1818_14_next_selected",
            any(row["route_id"] == "NEXT1818_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1818_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1818 CSVs parse"),
        ("VAL1818_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1818_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1818_18_formalization_untouched", formalization_untouched(), "no 1818 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1818_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1818 Hilbert-worldtube charge identity or R_Hsrc bound row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1818 Y5 R2FR Hilbert-worldtube charge identity or R_Hsrc bound row",
            "",
            "**Progress:** 1818 writes the exact bridge MTS needs for derivable Newton/GR source mass: `G_ref^-1 Q_tau = Pi_M^H J_H^dress + dB_H + R_Hsrc`. If `R_Hsrc=0`, the exterior Hamiltonian charge and observed Hilbert source are the same parent object. If not, the difference is now an explicit residual vector.",
            "",
            "**Current verdict:** exact identity contract, not current proof. The current corpus still lacks parent `L, Theta, Q_tau`, tau lock, same-frame Hilbert source ownership, Pi_M commutator silence, boundary/reference zero, extra-sector mass-charge silence, and Gauss/Newton calibration.",
            "",
            "**Claim ceiling:** no `R_Hsrc=0`, no derived Newton source mass, no orbital-GM shortcut, no PPN/local-GR pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1818.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Hilbert Worldtube Charge Identity Theorem",
            markdown_table(rows_map["charge_identity_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Identity Clause Audit",
            markdown_table(rows_map["identity_clause_audit"], ["clause_id", "needed_clause", "source_anchor", "current_status", "failure_if_missing", "valid_for_claim"]),
            "",
            "## R_Hsrc Residual Rows",
            markdown_table(rows_map["R_Hsrc_residual_rows"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "why_it_defeats_claim", "blocked_by", "retained", "valid_for_claim"]),
            "",
            "## GR Newton Impact Ledger",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a big conceptual tightening. The project is not stuck at `K_arena`; it is stuck at the source-mass identity. To get Newton/GR derivably, the next route should not be more empirical readout first. It should be local EH covariant-phase-space charge inheritance: show MTS gives the EH charge plus named silent/topological residuals, or fill the C-term vector honestly.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1818 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
