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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1819"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1819_0_1818_doc",
        "source_key": "1818_handoff_doc",
        "source_path": ROOT / "1818-Y5-R2FR-Hilbert-worldtube-charge-identity-or-R-Hsrc-bound-row.md",
        "needles": ["DEC1818_3_best_next", "NEXT1818_0_primary"],
        "role": "1818 selects local EH symplectic charge inheritance as the next target.",
    },
    {
        "source_id": "SRC1819_1_1818_validation",
        "source_key": "1818_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1818_VALIDATION.csv",
        "needles": ["VAL1818_OVERALL", "PASS"],
        "role": "confirms 1818 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1819_2_1818_identity",
        "source_key": "1818_charge_identity",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv",
        "needles": ["HCI1818_1_noether_charge", "PARENT_LAGRANGIAN_THETA_Q_NOT_DERIVED"],
        "role": "1818 identifies missing parent L/theta/Q_tau package.",
    },
    {
        "source_id": "SRC1819_3_1818_residual",
        "source_key": "1818_R_Hsrc_residual",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1818_R_HSRC_RESIDUAL_ROWS.csv",
        "needles": ["RHS1818_3_extra_charge", "MISSING_EXTRA_SECTOR_CHARGE_SILENCE_OR_BOUND"],
        "role": "R_Hsrc decomposition exposes extra-sector and calibration residuals.",
    },
    {
        "source_id": "SRC1819_4_505_theorem",
        "source_key": "505_noether_closure",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "needles": ["T505_conditional_Noether_mass_charge_closure", "premises_not_yet_parent_derived"],
        "role": "conditional Noether mass-charge closure theorem.",
    },
    {
        "source_id": "SRC1819_5_505_chain",
        "source_key": "505_derivation_chain",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        "needles": ["D505_3_exterior_derivative", "C_EH"],
        "role": "C-term derivative identity for exterior charge closure.",
    },
    {
        "source_id": "SRC1819_6_505_cterms",
        "source_key": "505_C_term_ledger",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_C_TERM_LEDGER.csv",
        "needles": ["C505_extra", "C505_projector"],
        "role": "four named C-term families for charge leakage.",
    },
    {
        "source_id": "SRC1819_7_505_decision",
        "source_key": "505_decision",
        "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DECISION.csv",
        "needles": ["DEC505_1_MTS_status", "no_local_GR_claim"],
        "role": "prior decision keeps Noether closure conditional only.",
    },
    {
        "source_id": "SRC1819_8_506_theorem",
        "source_key": "506_local_EH_reduction",
        "source_path": RESIDUALS / "P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv",
        "needles": ["T506_EH_plus_silent_reduction", "conditional_theorem_not_MTS_promotion"],
        "role": "local EH plus silent-sector theorem is conditional, not MTS promotion.",
    },
    {
        "source_id": "SRC1819_9_506_requirements",
        "source_key": "506_EH_requirements",
        "source_path": RESIDUALS / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv",
        "needles": ["EH505_0_operator_reduction", "not_parent_derived"],
        "role": "EH reduction requirements remain parent-unsigned.",
    },
    {
        "source_id": "SRC1819_10_1512_selection",
        "source_key": "1512_EH_selection",
        "source_path": RESIDUALS / "P8_Y5_PARENT_EH_1512_SELECTION_THEOREM_ATTEMPT.csv",
        "needles": ["THM1512_2_current_verdict", "NON_EH_VECTOR_REQUIRED"],
        "role": "EH selection theorem shape exists but non-EH vector is required.",
    },
    {
        "source_id": "SRC1819_11_1512_premises",
        "source_key": "1512_premise_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
        "needles": ["PRE1512_7_acceptance", "BLOCKED"],
        "role": "EH operator claim is blocked by unsigned premises.",
    },
    {
        "source_id": "SRC1819_12_1512_vector",
        "source_key": "1512_non_EH_vector",
        "source_path": RESIDUALS / "P8_Y5_PARENT_EH_1512_NON_EH_RESIDUAL_VECTOR.csv",
        "needles": ["R11_1512_01", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"],
        "role": "R2/fR and other non-EH rows remain retained and unfilled.",
    },
    {
        "source_id": "SRC1819_13_1708_result",
        "source_key": "1708_EH_result",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1708_EH_THEOREM_RESULT.csv",
        "needles": ["EHT1708_3_verdict", "NO_EH_CLAIM"],
        "role": "latest EH theorem result still refuses promotion.",
    },
    {
        "source_id": "SRC1819_14_1708_priority",
        "source_key": "1708_R11_priority",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1708_R11_PRIORITY_FILL_CONTRACT.csv",
        "needles": ["R11F1708_0_R2_fR", "HIGHEST_FIRST"],
        "role": "R2/fR no-higher-derivative/minimality is the first operator-side target.",
    },
    {
        "source_id": "SRC1819_15_1770_dominance",
        "source_key": "1770_EH_dominance",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
        "needles": ["EHD1770_4_current_verdict", "FAIL_CURRENT_PARENT_PROOF"],
        "role": "EH dominance is sharp but not parent-proven.",
    },
    {
        "source_id": "SRC1819_16_555_cterm",
        "source_key": "555_radial_Cterm_theorem",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_RADIAL_CTERM_THEOREM_ATTEMPT.csv",
        "needles": ["RCT555_6_verdict", "fail_current_claim"],
        "role": "radial C-term closure fails current claim.",
    },
    {
        "source_id": "SRC1819_17_555_decomp",
        "source_key": "555_Cterm_decomposition",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_RADIAL_CTERM_DECOMPOSITION.csv",
        "needles": ["CTD555_5_total", "unfilled"],
        "role": "radial C-term decomposition is explicit but unfilled.",
    },
    {
        "source_id": "SRC1819_18_1787_extra",
        "source_key": "1787_extra_sector_silence",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_EXTRA_SECTOR_SILENCE_MATRIX.csv",
        "needles": ["ESM1787_0_R2_fR_scalar", "RELATIVE_ZERO_THEOREM_AVAILABLE_PARENT_PREMISE_UNSIGNED"],
        "role": "extra-sector silence matrix keeps R2/fR as first unresolved local risk.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_SOURCE_REGISTER.csv",
    "eh_charge_inheritance_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_LOCAL_EH_SYMPLECTIC_CHARGE_INHERITANCE_THEOREM.csv",
    "cterm_clause_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_CTERM_CLAUSE_AUDIT.csv",
    "cterm_residual_vector": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_CTERM_RESIDUAL_VECTOR.csv",
    "r11_priority_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_R11_PRIORITY_GATE.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1819_VALIDATION.csv",
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


def eh_charge_inheritance_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_0_target",
            "claim": "MTS local exterior inherits the EH covariant-phase-space mass charge",
            "mathematical_statement": "On a compact source-free annulus A, if the MTS local exterior action is EH plus Lambda/background subtraction plus topological/exact/silent sectors, then Q_MTS[tau]=Q_EH[tau;G_ref]+Q_top+Q_silent+Q_residual and dQ_MTS[tau]=C_EH+C_extra+C_projector+C_boundary+C_ref.",
            "proof_status": "EXACT_CONDITIONAL_DECOMPOSITION",
            "current_corpus_status": "C_TERMS_NOT_ZERO",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_1_EH_reference",
            "claim": "EH covariant-phase-space charge is the reference branch",
            "mathematical_statement": "For EH with fixed tau, integrable boundary conditions and source-free exterior constraints, the CPS charge is radially closed between linked surfaces.",
            "proof_status": "KNOWN_CONDITIONAL_REFERENCE",
            "current_corpus_status": "MTS_EH_INHERITANCE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_2_operator_selection",
            "claim": "MTS local operator is EH plus harmless terms",
            "mathematical_statement": "The EH selection route fires only under local 4D, metric-only, Levi-Civita, second-order, no-extra-field and no-flux premises; otherwise DeltaE_R11 remains in the charge and PPN equations.",
            "proof_status": "EXACT_LOVELOCK_STYLE_CONDITIONAL",
            "current_corpus_status": "EH_PREMISES_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_3_Cterm_zero_condition",
            "claim": "radial charge closure follows from C-term silence",
            "mathematical_statement": "If C_EH=C_extra=C_projector=C_boundary=C_ref=0, then int_S2 Q_MTS[tau]-int_S1 Q_MTS[tau]=0 and the radial mass-hair numerator vanishes.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "C_TERM_ZERO_CLAUSES_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_4_bianchi_noether_guard",
            "claim": "dropping residual sectors must preserve Noether/Bianchi identity",
            "mathematical_statement": "The complete parent variation guarantees the Noether identity; deleting DeltaE_R11 by assumption would violate the bookkeeping unless each deleted sector is theorem-zero or bounded.",
            "proof_status": "GUARDRAIL",
            "current_corpus_status": "SECTOR_CERTIFICATES_INCOMPLETE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_5_Newton_GR_limit",
            "claim": "charge inheritance plus source identity gives Newton/GR source bridge",
            "mathematical_statement": "If EH charge inheritance, R_Hsrc=0, and weak-field Poisson/Gauss calibration all close, the same parent charge controls Newtonian source mass and the local PPN source side.",
            "proof_status": "CONDITIONAL_COROLLARY",
            "current_corpus_status": "R_HSRC_AND_WEAK_FIELD_STACK_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EHC1819_6_verdict",
            "claim": "1819 proves local EH symplectic charge inheritance in current MTS",
            "mathematical_statement": "EHC1819_0 through EHC1819_5 close only if EH operator selection, fixed tau/reference, extra-sector silence, projector constancy, boundary zero-flux and source calibration are all signed together.",
            "proof_status": "CONDITIONAL_CHARGE_INHERITANCE_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_CTERM_RESIDUAL_VECTOR",
            "valid_for_claim": False,
        },
    ]


def cterm_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CTA1819_0_C_EH",
            "cterm": "C_EH",
            "needed_clause": "local exterior satisfies EH constraints with fixed kappa/G_ref and allowed Lambda/background subtraction",
            "source_anchor": "C505_EH; RCT555_2_C_EH_zero; THM1512_2_current_verdict",
            "current_status": "EH_OPERATOR_SELECTION_NOT_PARENT_SIGNED",
            "failure_if_missing": "standard GR charge closure is not inherited",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CTA1819_1_C_extra",
            "cterm": "C_extra",
            "needed_clause": "non-EH, motion/time/domain/memory/source-normalization sectors are silent or topological",
            "source_anchor": "C505_extra; RCT555_3_C_extra_zero; ESM1787 matrix",
            "current_status": "EXTRA_SECTOR_SILENCE_NOT_PARENT_SIGNED",
            "failure_if_missing": "extra sectors carry local mass/PPN/fifth-force charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CTA1819_2_C_projector",
            "cterm": "C_projector",
            "needed_clause": "Pi_M or Q_M readout is parent-fixed and covariantly constant through the annulus",
            "source_anchor": "C505_projector; RCT555_4_C_projector_zero; RHS1818_1_PiM_commutator",
            "current_status": "PROJECTOR_COMMUTATOR_NOT_ZERO",
            "failure_if_missing": "mass drift can be produced by projector/readout hair",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CTA1819_3_C_boundary",
            "cterm": "C_boundary",
            "needed_clause": "topological/exact/boundary improvements have zero linking-sphere flux",
            "source_anchor": "C505_boundary; RCT555_5_C_boundary_ref_zero; RHS1818_2_boundary_reference",
            "current_status": "BOUNDARY_NOFLUX_NOT_PARENT_SIGNED",
            "failure_if_missing": "divergence terms produce finite mass, alpha3, xi or Gdot hair",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CTA1819_4_C_ref",
            "cterm": "C_ref",
            "needed_clause": "reference subtraction is fixed once and cannot absorb source, radius, time or frame changes",
            "source_anchor": "CTD555_4_C_ref; HCI554_3_reference_lock",
            "current_status": "REFERENCE_SUBTRACTION_LOCK_OPEN",
            "failure_if_missing": "background bookkeeping can fake radial/source stability",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CTA1819_5_verdict",
            "cterm": "all",
            "needed_clause": "all C terms zero or source-backed below locks",
            "source_anchor": "EHC1819_0 through EHC1819_5",
            "current_status": "FAIL_CURRENT_ZERO_PROOF",
            "failure_if_missing": "retain C-term residual vector and no local GR/Newton promotion",
            "valid_for_claim": False,
        },
    ]


def cterm_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CTV1819_0_C_EH",
            "quantity": "epsilon_C_EH_abs",
            "definition": "EH constraint/operator mismatch contribution to Hamiltonian charge closure",
            "formal_expression": "abs(int_A C_EH)/M_H_ref",
            "zero_condition": "local exterior EH equations hold with fixed kappa/G_ref and valid Lambda/reference subtraction",
            "required_inputs": "EH operator theorem or R11 coefficients; kappa/G_ref lock; subtraction rule; source_path",
            "current_status": "MISSING_EH_CONSTRAINT_ZERO_OR_SOURCE_BACKED_BOUND",
            "units": "dimensionless_charge_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_MH_REF_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CTV1819_1_C_extra",
            "quantity": "epsilon_C_extra_abs",
            "definition": "non-EH/domain/memory/range/motion/source-normalization charge leakage",
            "formal_expression": "abs(int_A C_extra)/M_H_ref",
            "zero_condition": "each extra sector has theorem-zero silence or source-backed channel bound",
            "required_inputs": "extra-sector matrix; channel coefficients; source norms; units; source paths",
            "current_status": "MISSING_EXTRA_SECTOR_ZERO_OR_CHANNEL_VECTOR",
            "units": "dimensionless_charge_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_EXTRA_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CTV1819_2_C_projector",
            "quantity": "epsilon_C_projector_abs",
            "definition": "Pi_M/projector/readout commutator leakage through the annulus",
            "formal_expression": "abs(int_A C_projector)/M_H_ref",
            "zero_condition": "Pi_M is parent-owned, covariantly fixed and equal to source/readout mass map",
            "required_inputs": "Pi_M theorem or commutator bound; source norm; units; source_path",
            "current_status": "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND",
            "units": "dimensionless_projector_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_PROJECTOR_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CTV1819_3_C_boundary",
            "quantity": "epsilon_C_boundary_abs",
            "definition": "boundary/exact/topological side-flux leakage",
            "formal_expression": "abs(int_A C_boundary)/M_H_ref",
            "zero_condition": "boundary/cohomology/no-hair and zero side-flux theorem holds for local branch",
            "required_inputs": "boundary theorem or flux bound; linking surface convention; units; source_path",
            "current_status": "MISSING_BOUNDARY_NOFLUX_ZERO_OR_BOUND",
            "units": "dimensionless_boundary_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_BOUNDARY_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CTV1819_4_C_ref",
            "quantity": "epsilon_C_ref_abs",
            "definition": "reference/background/subtraction dependence across source, radius, time or frame",
            "formal_expression": "abs(int_A C_ref)/M_H_ref",
            "zero_condition": "B_ref and subtraction branch are fixed/superselected and derivative-silent",
            "required_inputs": "reference lock theorem or bound; subtraction convention; units; source_path",
            "current_status": "MISSING_REFERENCE_SUBTRACTION_ZERO_OR_BOUND",
            "units": "dimensionless_reference_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_REFERENCE_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "CTV1819_5_total",
            "quantity": "epsilon_Cterm_total_abs",
            "definition": "strict no-cancellation C-term envelope for local EH charge inheritance",
            "formal_expression": "abs(CTV1819_0)+abs(CTV1819_1)+abs(CTV1819_2)+abs(CTV1819_3)+abs(CTV1819_4)",
            "zero_condition": "all C terms individually theorem-zero or source-backed below local locks",
            "required_inputs": "all CTV1819 components; common normalizers; units; source paths; local tolerances",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "units": "absolute_no_cancellation_envelope",
            "source_path": "",
            "common_normalizer": "MISSING_TOTAL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def r11_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "priority_id": "R11P1819_0_R2_fR",
            "operator_family": "R2_fR_scalar_mode",
            "why_first": "highest-priority direct violation of second-order EH operator selection and maps to PPN/R10/fifth-force channels",
            "current_status": "MISSING_MINIMALITY_OR_SCALAR_MODE_COEFFICIENT",
            "next_target_if_selected": "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "R11P1819_1_torsion_nonmetricity",
            "operator_family": "torsion_nonmetricity",
            "why_first": "Levi-Civita premise is also high-priority but depends on connection/matter-interface branch",
            "current_status": "LEVI_CIVITA_GATE_NOT_CLOSED",
            "next_target_if_selected": "held_parallel_connection_silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "R11P1819_2_boundary",
            "operator_family": "boundary_topological_terms",
            "why_first": "feeds C_boundary/C_ref and alpha3/xi/Gdot, but prior route has multiple failed no-flux gates",
            "current_status": "BOUNDARY_NOFLUX_NOT_PARENT_SIGNED",
            "next_target_if_selected": "held_parallel_boundary_flux",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "R11P1819_3_projector",
            "operator_family": "projector_domain_stress",
            "why_first": "essential for R_Hsrc but depends on Pi_M/Hilbert identity branch",
            "current_status": "PROJECTOR_COMMUTATOR_NOT_ZERO",
            "next_target_if_selected": "held_parallel_projector_identity",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "priority_id": "R11P1819_4_verdict",
            "operator_family": "C_EH_first",
            "why_first": "the next derivation should attack the operator-side EH selection gate before empirical C-term filling",
            "current_status": "SELECT_R2_FR_MINIMALITY_FIRST",
            "next_target_if_selected": "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1819_0_imported_EH",
            "countermodel": "Einstein equations are inserted as the local left-hand side rather than selected from MTS",
            "why_it_defeats_claim": "local GR is assumed rather than derived",
            "blocked_by": "parent-signed EH operator selection or explicit C_EH bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1819_1_R2_fR_scalar",
            "countermodel": "higher-curvature R2/fR scalar mode survives in the local exterior",
            "why_it_defeats_claim": "adds fifth-force/PPN/source charge tails and changes CPS charge",
            "blocked_by": "minimality/no-higher-derivative theorem or scalar-mode coefficient bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1819_2_extra_sector_charge",
            "countermodel": "memory/domain/motion/time/range sector carries Hamiltonian mass charge",
            "why_it_defeats_claim": "C_extra remains nonzero and radial source hair survives",
            "blocked_by": "sector-specific silence theorem or source-backed channel vector",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1819_3_projector_stress",
            "countermodel": "Pi_M varies with domain/readout/metric and generates C_projector",
            "why_it_defeats_claim": "mass-channel closure becomes projector-dependent",
            "blocked_by": "parent-owned fixed Pi_M theorem or commutator bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1819_4_boundary_flux",
            "countermodel": "boundary/reference/exact term has nonzero linking-sphere flux",
            "why_it_defeats_claim": "a divergence term becomes observable mass/PPN hair",
            "blocked_by": "boundary zero-flux/reference-lock theorem or source-backed bound",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1819_0_if_charge_inheritance_closes",
            "if_closed": "C_EH=C_extra=C_projector=C_boundary=C_ref=0",
            "would_buy": "local exterior charge closure becomes derivable rather than plateau-style",
            "still_missing": "R_Hsrc source equality, weak-field Poisson/Gauss calibration and PPN second-order stability",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1819_1_if_C_EH_closes",
            "if_closed": "EH operator selection/minimality closes",
            "would_buy": "the main left-hand GR operator is no longer imported by hand",
            "still_missing": "C_extra, C_projector, C_boundary, R_Hsrc and source calibration remain open",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1819_2_Newton_bridge",
            "if_closed": "C terms close plus source identity and Gauss calibration close",
            "would_buy": "source-normalized Newton becomes a serious derived route",
            "still_missing": "slow-particle readout, constant G_ref and residual source-charge tests",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1819_3_verdict",
            "if_closed": "1819 alone proves local GR",
            "would_buy": "nothing claimable alone; 1819 is an EH charge-inheritance subgate",
            "still_missing": "current corpus keeps C-term vector unfilled and nonclaim",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1819_0_charge_contract",
            "gate": "local EH charge inheritance theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "EHC1819 writes exact EH/C-term decomposition and zero conditions",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1819_1_Cterm_zero",
            "gate": "all C terms theorem-zero",
            "current_status": "BLOCKED",
            "reason": "EH operator, extra-sector, projector, boundary and reference clauses are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1819_2_residual_values",
            "gate": "C-term residual vector source-backed",
            "current_status": "BLOCKED",
            "reason": "CTV1819 rows have missing component values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1819_3_Newton_bridge",
            "gate": "source-normalized Newton promotion allowed",
            "current_status": "REFUSED",
            "reason": "C-term vector, R_Hsrc and Poisson/Gauss calibration are not closed",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1819_4_local_GR",
            "gate": "PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "R11/operator vector and PPN second-order source stability remain unfilled",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1819_0_EH_charge_inheritance",
            "claim": "MTS inherits EH CPS charge in the local branch",
            "status": "BLOCKED",
            "reason": "EH operator and silent-sector premises are not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1819_1_Cterm_zero",
            "claim": "C-term residual vector is zero",
            "status": "BLOCKED",
            "reason": "C_EH/C_extra/C_projector/C_boundary/C_ref are unzeroed or unbounded",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1819_2_Newton",
            "claim": "Newton source-normalized limit follows",
            "status": "REFUSED",
            "reason": "charge inheritance is not enough without R_Hsrc and Gauss/Poisson calibration",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1819_3_local_GR_PPN",
            "claim": "local GR/PPN follows",
            "status": "REFUSED",
            "reason": "operator residual vector and second-order PPN stability are not derived or scored",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1819_0_theorem_result",
            "decision": "EH_CHARGE_INHERITANCE_CONTRACT_ONLY",
            "reason": "the EH/C-term charge decomposition is exact, but C terms are not zero for current MTS",
            "next_action": "retain C-term residual vector and do not promote Newton/GR",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1819_1_core_blocker",
            "decision": "C_EH_OPERATOR_SELECTION_FIRST",
            "reason": "without EH operator/minimality, no local GR source-charge route can claim derivation",
            "next_action": "attack R2/fR/no-higher-derivative minimality before empirical C-term scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1819_2_residual_status",
            "decision": "CTERM_VECTOR_READY_NONCLAIM",
            "reason": "C_EH/C_extra/C_projector/C_boundary/C_ref are named but unfilled",
            "next_action": "fill no row without source paths, units, normalizers and no-cancellation guard",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1819_3_best_next",
            "decision": "EH_OPERATOR_SELECTION_MINIMALITY_NEXT",
            "reason": "the least empirical and highest-priority next derivation is the R2/fR/no-higher-derivative minimality gate",
            "next_action": "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1819_0_primary",
            "next_target": "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md",
            "script": "scripts/Y5_R2FR_EH_operator_selection_minimality_or_R11_C_EH_first_row.py",
            "objective": "derive local EH operator selection/minimality by excluding R2/fR and higher-curvature scalar modes; if not, emit the first C_EH/R11 scalar-mode residual row",
            "selection_status": "selected",
            "success_condition": "R2/fR scalar-mode theorem-zero, or a source-backed C_EH/R11 first row remains nonclaim until gates pass",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1819_1_parallel",
            "next_target": "1820b-Y5-R2FR-Cterm-source-backed-bound-fill-pack.md",
            "script": "scripts/Y5_R2FR_Cterm_source_backed_bound_fill_pack.py",
            "objective": "fill C-term components with theorem-zero certificates or numeric bounds if derivation route stalls",
            "selection_status": "held_parallel",
            "success_condition": "C-term rows parse, cite source paths, carry units and remain nonclaim until gates pass",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "eh_charge_inheritance_theorem": eh_charge_inheritance_rows(),
        "cterm_clause_audit": cterm_clause_rows(),
        "cterm_residual_vector": cterm_residual_rows(),
        "r11_priority_gate": r11_priority_rows(),
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
    allowed_gate_pass = {"AC1819_0_charge_contract"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1819_0_charge_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1819_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1819_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1819_2_charge_contract_written",
            any(row["theorem_id"] == "EHC1819_0_target" and row["proof_status"] == "EXACT_CONDITIONAL_DECOMPOSITION" for row in rows_map["eh_charge_inheritance_theorem"]),
            "local EH symplectic charge inheritance decomposition is written",
        ),
        (
            "VAL1819_3_Cterm_zero_blocked",
            any(row["theorem_id"] == "EHC1819_3_Cterm_zero_condition" and row["current_corpus_status"] == "C_TERM_ZERO_CLAUSES_OPEN" for row in rows_map["eh_charge_inheritance_theorem"]),
            "C-term zero clauses remain open",
        ),
        (
            "VAL1819_4_theorem_not_promoted",
            any(row["theorem_id"] == "EHC1819_6_verdict" and row["proof_status"] == "CONDITIONAL_CHARGE_INHERITANCE_NOT_CURRENT_PROOF" for row in rows_map["eh_charge_inheritance_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["eh_charge_inheritance_theorem"]),
            "1819 theorem is not promoted as current proof",
        ),
        (
            "VAL1819_5_clause_audit_blocked",
            any(row["clause_id"] == "CTA1819_5_verdict" and row["current_status"] == "FAIL_CURRENT_ZERO_PROOF" for row in rows_map["cterm_clause_audit"]),
            "C-term clause audit remains blocked",
        ),
        (
            "VAL1819_6_residual_rows_nonclaim",
            any(row["residual_id"] == "CTV1819_5_total" for row in rows_map["cterm_residual_vector"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["cterm_residual_vector"]),
            "C-term residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1819_7_R11_priority_selected",
            any(row["priority_id"] == "R11P1819_4_verdict" and row["current_status"] == "SELECT_R2_FR_MINIMALITY_FIRST" for row in rows_map["r11_priority_gate"]),
            "R2/fR minimality is selected as first C_EH/R11 target",
        ),
        (
            "VAL1819_8_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1819_9_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1819_10_acceptance_blocks",
            any(row["gate_id"] == "AC1819_0_charge_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1819_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all EH/Newton/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1819_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1819_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1819_14_decision_next",
            any(row["decision_id"] == "DEC1819_3_best_next" and row["decision"] == "EH_OPERATOR_SELECTION_MINIMALITY_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects EH operator selection/minimality next",
        ),
        (
            "VAL1819_15_next_selected",
            any(row["route_id"] == "NEXT1819_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1819_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1819 CSVs parse"),
        ("VAL1819_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1819_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1819_19_formalization_untouched", formalization_untouched(), "no 1819 outputs found under formalization-workbench"),
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
            "check_id": "VAL1819_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1819 local EH symplectic charge inheritance or C-term residual vector checkpoint",
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
            "# 1819 Y5 R2FR local EH symplectic charge inheritance or Cterm residual vector",
            "",
            "**Progress:** 1819 turns the local-GR/Newton bridge into a precise charge-inheritance equation. In a compact source-free annulus, MTS must inherit the EH covariant-phase-space charge or keep the residual vector `C_EH + C_extra + C_projector + C_boundary + C_ref` explicit.",
            "",
            "**Current verdict:** exact conditional decomposition, not current proof. The present corpus still has open EH operator selection, extra-sector silence, projector commutator, boundary/reference zero-flux, and source-calibration gates. So no local GR/Newton promotion is allowed.",
            "",
            "**Claim ceiling:** no EH charge-inheritance claim, no C-term zero claim, no derived Newton source mass, no PPN/local-GR pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1819.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Local EH Symplectic Charge Inheritance Theorem",
            markdown_table(rows_map["eh_charge_inheritance_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Cterm Clause Audit",
            markdown_table(rows_map["cterm_clause_audit"], ["clause_id", "cterm", "needed_clause", "source_anchor", "current_status", "failure_if_missing", "valid_for_claim"]),
            "",
            "## Cterm Residual Vector",
            markdown_table(rows_map["cterm_residual_vector"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
            "",
            "## R11 Priority Gate",
            markdown_table(rows_map["r11_priority_gate"], ["priority_id", "operator_family", "why_first", "current_status", "next_target_if_selected", "valid_for_claim"]),
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
            "This is useful pressure. We are no longer saying vaguely “reduce to GR”; we have the exact local charge inheritance debt. The next cleanest derivation is operator-side: kill the R2/fR scalar-mode/higher-derivative leak by parent minimality, or admit the first `C_EH/R11` row. That is a better next attack than trying to score WEP/R10/PPN before the left-hand operator is owned.",
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
    print(f"1819 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
