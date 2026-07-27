from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3006"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3006-Y5-R2FR-parent-theta-Qtau-Htau-extraction-or-Hamiltonian-current-owner-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3006_SOURCE_REGISTER.csv",
    "current_chain": RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv",
    "sectors": RESIDUALS / "P8_Y5_R2FR_3006_SECTOR_CHARGE_OWNER_ROWS.csv",
    "htau": RESIDUALS / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_3006_DENOMINATOR_REENTRY_AFTER_THETA_QTAU.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3006_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3006_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3006_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3006_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3006_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "current_owner_copy": PARENT_ACTION / "parent_theta_Qtau_Htau_current_owner_3006_NOT_SIGNED.csv",
    "sector_rows_copy": LOCAL_BOUNDS / "Hamiltonian_current_sector_charge_rows_3006_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3006_MINIMAL_PARENT_ACTION_SECTOR_GRAMMAR_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3006_00_3005_next",
        RESIDUALS / "P8_Y5_R2FR_3005_NEXT_TARGET.csv",
        ["NEXT3005_0_3006", "theta_MTS"],
        "3005 selects parent theta/Q_tau/H_tau extraction next.",
    ),
    (
        "SRC3006_01_3005_doc",
        ROOT / "3005-Y5-R2FR-Mref-denominator-ownership-or-Bv-envelope-scoreability-under-AX1090.md",
        ["Current MTS does not yet sign that stack", "parent `theta_MTS/Q_tau/H_tau` owner"],
        "3005 identifies parent Hamiltonian-current ownership as the upstream denominator blocker.",
    ),
    (
        "SRC3006_02_1008_doc",
        ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        ["PVA1008_6_verdict", "fail_current_claim"],
        "1008 attempted theta/Q_tau extraction and refused current claim.",
    ),
    (
        "SRC3006_03_1008_variation",
        RESIDUALS / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
        ["PVA1008_0_parent_action", "PVA1008_6_verdict"],
        "1008 parent variation audit: formal current-chain shape exists but is not extracted.",
    ),
    (
        "SRC3006_04_1008_pieces",
        RESIDUALS / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
        ["QTA1008_1_theta_total", "QTA1008_8_Q_total"],
        "1008 charge piece ledger names theta_MTS and Q_tau^MTS missing pieces.",
    ),
    (
        "SRC3006_05_1009_sector_contract",
        RESIDUALS / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
        ["PCS1009_0_EH_core", "PCS1009_8_worldtube_source_glue"],
        "1009 sector contract lists retained sectors and current owner status.",
    ),
    (
        "SRC3006_06_993_decomposition",
        RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
        ["QDEC993_0_EH", "QDEC993_5_total"],
        "993 Q_tau decomposition shows EH reference is not total MTS charge.",
    ),
    (
        "SRC3006_07_1646_owner",
        RESIDUALS / "P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        ["TQ1646_0_parent_variation", "TQ1646_5_owner_verdict"],
        "1646 current-owner audit refuses Theta_total/Q_tau promotion.",
    ),
    (
        "SRC3006_08_771_owner",
        RESIDUALS / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
        ["TQ771_0_parent_variation", "TQ771_6_owner_verdict"],
        "771 older owner audit records same parent-current blockers.",
    ),
    (
        "SRC3006_09_2552_contract",
        RESIDUALS / "P8_Y5_NO_SHADOW_2552_CURRENT_CHAIN_PROMOTION_CONTRACT.csv",
        ["PCC2552_0_single_action_source", "PCC2552_7_source_bridge"],
        "2552 current-chain promotion contract gives required reopen clauses.",
    ),
    (
        "SRC3006_10_2552_verdict",
        RESIDUALS / "P8_Y5_NO_SHADOW_2552_THETA_QTAU_PROMOTION_VERDICT.csv",
        ["TQV2552_0_conditional_sum", "TQV2552_1_current_promotion"],
        "2552 says the sector-sum theorem is conditional only and not current evidence.",
    ),
    (
        "SRC3006_11_2552_material",
        RESIDUALS / "P8_Y5_NO_SHADOW_2552_REOPEN_MATERIAL_SPEC.csv",
        ["MAT2552_0_action_source", "MAT2552_5_reference_pack"],
        "2552 material spec states what is required to reopen denominator/current-chain promotion.",
    ),
    (
        "SRC3006_12_2551_requirements",
        RESIDUALS / "P8_Y5_NO_SHADOW_2551_CHARGE_POSITIVITY_PACK_REQUIREMENTS.csv",
        ["REQ2551_0_parent_action", "REQ2551_6_no_shortcuts"],
        "2551 charge positivity pack requirements remain unsatisfied.",
    ),
    (
        "SRC3006_13_2504_chain",
        RESIDUALS / "P8_Y5_NO_SHADOW_2504_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
        ["NHC2504_0_variation", "NHC2504_4_PiM_identification"],
        "2504 gives exact conditional Noether/Hamiltonian charge chain.",
    ),
    (
        "SRC3006_14_BZTC552",
        RESIDUALS / "P8_Y5_BRR545_PARENT_ACTION_ZERO_THEOREM_CONTRACT.csv",
        ["BZTC552_0_covariant_phase_space_parent", "BZTC552_7_no_cancellation_envelope_identity"],
        "552 parent-action zero theorem contract names current-chain and no-cancellation requirements.",
    ),
    (
        "SRC3006_15_583_momentum",
        RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        ["NMC583_0_symplectic_potential", "NMC583_5_boundary_zero"],
        "583 momentum-map contract keeps parent symplectic potential and boundary zero missing.",
    ),
    (
        "SRC3006_16_HC_contract",
        RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        ["HC2_differentiable_integrable_Hxi", "HC5_no_extra_hidden_charge"],
        "Hamiltonian boundary-charge contract keeps integrability and hidden-charge channels unowned.",
    ),
    (
        "SRC3006_17_HCI554",
        RESIDUALS / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
        ["HCI554_2_parent_Lagrangian_theta_Q", "HCI554_6_integrability_verdict"],
        "Hamiltonian charge attempt says explicit L/theta/Q_tau not derived.",
    ),
    (
        "SRC3006_18_charge_current",
        RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        ["CC0_parent_phase_space_start", "CC7_closed_flux_and_Gauss_calibration"],
        "charge-current equality attempt keeps parent symplectic current and Gauss calibration unproved.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def current_chain_rows() -> list[dict[str, Any]]:
    data = [
        (
            "CCA3006_0_single_action",
            "one explicit diffeomorphism-covariant S_parent source",
            "delta L_parent = E_A delta Phi^A + d theta_MTS",
            "MISSING_SINGLE_PARENT_ACTION_SOURCE",
            "CSV contracts are not a substitute for a varied parent action",
            "PCC2552_0_single_action_source;PVA1008_0_parent_action",
        ),
        (
            "CCA3006_1_field_list",
            "complete retained field and variation list",
            "Phi={g_obs,coframe,tau,matter,Gamma/Khat/q_loc,projector,boundary,reference,source worldtube,...}",
            "MISSING_COMPLETE_FIELD_VARIATION_LIST",
            "unlisted fields can carry hidden current or stress",
            "PCC2552_1_field_list;PCS1009 sector table",
        ),
        (
            "CCA3006_2_sector_variations",
            "each retained sector has first variation",
            "delta S_i=E_i delta Phi_i + d theta_i plus stress/source/boundary terms",
            "MISSING_SECTOR_FIRST_VARIATION_PACK",
            "theta_MTS=sum theta_i is only legal after every retained sector is varied or demoted",
            "PCC2552_2_sector_variations;TQV2552_0_conditional_sum",
        ),
        (
            "CCA3006_3_theta_sum",
            "theta_MTS=sum_i theta_i is explicit",
            "theta_MTS=theta_EH+theta_matter+theta_boundary+theta_extra+theta_projector+theta_memory+...",
            "MISSING_THETA_MTS_EXTRACTION",
            "theta_EH alone cannot normalize MTS residuals",
            "PVA1008_1_theta_MTS;QTA1008_1_theta_total",
        ),
        (
            "CCA3006_4_Noether_current",
            "observed tau Noether current is parent-owned",
            "J_tau=theta_MTS(Phi,L_tau Phi)-i_tau L_parent",
            "FORMAL_SHAPE_AVAILABLE_NOT_OWNER",
            "tau action across metric, matter, representative, boundary/reference fields is unsigned",
            "PVA1008_2_J_tau;TQ771_3_tau_action",
        ),
        (
            "CCA3006_5_Qtau_sum",
            "J_tau=dQ_tau^MTS+C_tau with all pieces owned",
            "Q_tau^MTS=sum(Q_EH,Q_boundary,Q_extra,Q_projector,Q_matter,...)",
            "MISSING_QTAU_MTS_EXTRACTION",
            "only Q_EH is a conditional reference; total MTS charge is not promoted",
            "PVA1008_3_Q_tau_piece_split;QDEC993_5_total",
        ),
        (
            "CCA3006_6_constraints",
            "C_tau constraint/exchange terms are zero, bounded, or sourced",
            "C_tau=C_EH+C_extra+C_projector+C_boundary+C_ref+C_matter",
            "MISSING_CONSTRAINT_COMPONENT_LEDGER",
            "hidden bulk/exchange terms prevent H_tau from becoming a clean surface source charge",
            "NHC2504_2_charge_decomposition;HC3_constraints_and_boundary_conditions",
        ),
        (
            "CCA3006_7_integrable_Htau",
            "H_tau exists as an integrable state function with fixed reference",
            "delta H_tau=int_S(delta Q_tau-i_tau theta_MTS), delta^2 H_tau=0",
            "MISSING_HTAU_INTEGRABILITY_CERTIFICATE",
            "without curl control H_tau cannot feed M_H_ref",
            "HCI554_6_integrability_verdict;HC2_differentiable_integrable_Hxi",
        ),
        (
            "CCA3006_8_source_bridge",
            "Hamiltonian charge equals the same source/current used by matter and later Gauss readout",
            "M_source[W]=H_tau[S]-H_ref and Pi_M J_H maps to same charge",
            "MISSING_SOURCE_BRIDGE",
            "Hamiltonian charge can be well-defined but still be the wrong measured source",
            "NHC2504_3_source_measure;NHC2504_4_PiM_identification;CC7_closed_flux_and_Gauss_calibration",
        ),
        (
            "CCA3006_9_verdict",
            "theta_MTS/Q_tau/H_tau owner for current MTS",
            "CCA3006_0 through CCA3006_8 all pass",
            "CURRENT_OWNER_NOT_DERIVED_ROWS_STAGED",
            "conditional covariant phase-space route is good, but current corpus lacks the parent action/sector variation pack",
            "all rows above",
        ),
    ]
    return [
        base(
            {
                "audit_id": audit_id,
                "current_chain_clause": current_chain_clause,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "failure_mode": failure_mode,
                "source_anchors": source_anchors,
                "parent_signed_now": False,
                "theorem_promoted_now": False,
            }
        )
        for audit_id, current_chain_clause, mathematical_form, current_status, failure_mode, source_anchors in data
    ]


def sector_rows() -> list[dict[str, Any]]:
    data = [
        (
            "SEC3006_0_EH_core",
            "EH core",
            "theta_EH and Q_tau^EH",
            "CONDITIONAL_BASELINE_NOT_TOTAL_PARENT",
            "valid GR reference shape, but cannot carry MTS extra/projector/boundary/matter coupling sectors",
            "PCS1009_0_EH_core;QDEC993_0_EH",
        ),
        (
            "SEC3006_1_kappa_topological",
            "kappa/topological coupling sector",
            "theta_kappa and Q_tau^kappa or constant-superselection proof",
            "CANDIDATE_NOT_ADOPTED",
            "variation of A3/kappa and no source/species/range drift not parent-signed",
            "PCS1009_1_kappa_topological;HC7_constant_universal_Geff",
        ),
        (
            "SEC3006_2_universal_matter",
            "ordinary matter/source sector",
            "Hilbert current J_H and universal matter coupling descent",
            "MISSING_MATTER_DESCENT_AND_SOURCE_WARD",
            "source current can differ from Hamiltonian charge or carry species/frame leakage",
            "PCS1009_2_universal_matter;TQ771_5_matter_coupling",
        ),
        (
            "SEC3006_3_boundary_reference",
            "boundary/reference/improvement sector",
            "theta_boundary, Q_tau^boundary, fixed H_ref/B_ref and no fitted subtraction",
            "MISSING_FIXED_REFERENCE_BEFORE_READOUT",
            "boundary/reference can shift mass normalization or absorb residuals",
            "PCS1009_3_boundary_reference;QDEC993_1_boundary_reference",
        ),
        (
            "SEC3006_4_Gamma_Khat_q_loc",
            "Gamma/Khat/q_loc extra sector",
            "S_GK, theta_GK, Q_tau^GK or explicit retained residual policy",
            "MISSING_S_GK_HELMHOLTZ_EULER_DOUBLE_ZERO",
            "hard local sector cannot be silently included in EH charge",
            "PCS1009_4_Gamma_Khat_extra;TQV2552_2_hardest_block",
        ),
        (
            "SEC3006_5_domain_selector",
            "domain/projector/local selector sector",
            "selector stress zero theorem or retained domain residual rows",
            "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
            "domain selection and metric stress can become readout masks",
            "PCS1009_5_domain_projector_selector",
        ),
        (
            "SEC3006_6_mass_projector_PiM",
            "Pi_M/source-measure projector sector",
            "Pi_M chain map, variation owner, flux closure and source mass equality",
            "MISSING_PIM_SOURCE_BRIDGE",
            "projector can select wrong charge or carry commutator/stress residuals",
            "PCS1009_6_mass_projector_PiM;QDEC993_3_projector",
        ),
        (
            "SEC3006_7_memory_response",
            "memory/response doublet sector",
            "theta_memory, Q_tau^memory or double-zero/no-source theorem",
            "PARTIAL_CANDIDATE_NOT_MATCHED",
            "memory can carry local source-normalization or PPN leakage",
            "PCS1009_7_memory_response_doublet;QDEC993_2_extra",
        ),
        (
            "SEC3006_8_worldtube_source_glue",
            "worldtube/source-measure glue",
            "M_source[W]=int_S Q_M[tau] before orbital fitting",
            "CORE_MISSING_PIECE",
            "source mass denominator cannot be connected to observed matter without this bridge",
            "PCS1009_8_worldtube_source_glue;NHC2504_3_source_measure",
        ),
        (
            "SEC3006_9_total",
            "total parent Hamiltonian current",
            "theta_MTS=sum theta_i and Q_tau^MTS=sum Q_i with every C_tau zero/bounded/sourced",
            "TOTAL_CURRENT_NOT_PROMOTED",
            "sector rows above are partial, conditional, blocked or source-acquisition only",
            "QTA1008_8_Q_total;TQV2552_1_current_promotion",
        ),
    ]
    return [
        base(
            {
                "sector_id": sector_id,
                "sector": sector,
                "needed_current_piece": needed_current_piece,
                "current_status": current_status,
                "failure_mode": failure_mode,
                "source_anchors": source_anchors,
                "theta_contribution_owned": sector_id == "SEC3006_0_EH_core",
                "Qtau_contribution_owned": sector_id == "SEC3006_0_EH_core",
                "promote_sector": False,
            }
        )
        for sector_id, sector, needed_current_piece, current_status, failure_mode, source_anchors in data
    ]


def htau_rows() -> list[dict[str, Any]]:
    data = [
        ("HTE3006_0_theta", "theta_MTS", "theta_MTS=sum_i theta_i", "MISSING_THETA_MTS_EXTRACTION", "PVA1008_1_theta_MTS;PCC2552_3_theta_sum"),
        ("HTE3006_1_Jtau", "J_tau", "theta_MTS(Phi,L_tau Phi)-i_tau L_parent", "FORMAL_SHAPE_AVAILABLE_NOT_OWNER", "PVA1008_2_J_tau;NHC2504_1_Noether_current"),
        ("HTE3006_2_Qtau", "Q_tau^MTS", "J_tau=dQ_tau^MTS+C_tau", "MISSING_QTAU_MTS_EXTRACTION", "PVA1008_3_Q_tau_piece_split;PCC2552_4_Qtau_sum"),
        ("HTE3006_3_constraints", "C_tau_total", "C_EH+C_extra+C_projector+C_boundary+C_ref+C_matter", "MISSING_CONSTRAINT_COMPONENT_LEDGER", "NHC2504_2_charge_decomposition;HC3_constraints_and_boundary_conditions"),
        ("HTE3006_4_Htau_variation", "delta H_tau", "int_S(delta Q_tau^MTS-i_tau theta_MTS)", "MISSING_PARENT_HTAU_VARIATION", "HC2_differentiable_integrable_Hxi;HCI554_0_target"),
        ("HTE3006_5_integrability", "delta_H_tau_curl", "delta^2 H_tau=0 or source-backed curl bound", "MISSING_HTAU_INTEGRABILITY_CERTIFICATE", "HCI554_6_integrability_verdict"),
        ("HTE3006_6_Href", "H_ref", "fixed reference selected before source/readout fitting", "MISSING_FIXED_REFERENCE_BEFORE_READOUT", "HCI554_3_reference_lock;PCC2552_5_fixed_reference"),
        ("HTE3006_7_MHref_feed", "M_H_ref_feed", "H_tau[S_outer]-H_ref with positive same-frame source bridge", "MISSING_POSITIVE_SAME_FRAME_MHREF", "REQ2551_5_positivity;NHC2504_3_source_measure"),
        ("HTE3006_8_verdict", "H_tau_current_owner", "all HTE3006_0..7 pass", "HTAU_NOT_DERIVED_ROWS_STAGED", "TQV2552_3_denominator_availability"),
    ]
    return [
        base(
            {
                "row_id": row_id,
                "quantity": quantity,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "source_anchors": source_anchors,
                "current_value": "MISSING_PARENT_INPUT",
                "finite_value_present": False,
                "theorem_zero_now": False,
            }
        )
        for row_id, quantity, mathematical_form, current_status, source_anchors in data
    ]


def reentry_rows() -> list[dict[str, Any]]:
    data = [
        ("DENR3006_0_theta_Qtau", "theta_MTS/Q_tau^MTS", "MISSING_PARENT_CURRENT_OWNER", "M_H_ref cannot be derived until parent current owner closes"),
        ("DENR3006_1_Htau", "H_tau", "MISSING_HTAU_INTEGRABILITY_CERTIFICATE", "Hamiltonian charge is not a state-function denominator"),
        ("DENR3006_2_Href", "H_ref/B_ref", "MISSING_FIXED_REFERENCE_BEFORE_READOUT", "reference can still absorb source/readout residuals"),
        ("DENR3006_3_MHref", "M_H_ref", "MISSING_POSITIVE_SAME_FRAME_MHREF", "denominator cannot normalize Bv or PiM rows"),
        ("DENR3006_4_Bv_envelope", "epsilon_Bv_ambiguity_abs_envelope", "NOT_SCOREABLE", "Bv remains explicit residual closure"),
        ("DENR3006_5_local_GR", "local_GR_Newton_PPN", "BLOCKED_NONCLAIM", "current-chain owner is upstream of GR/Newton reduction"),
    ]
    return [
        base({"reentry_id": reentry_id, "object": obj, "status": status, "effect": effect})
        for reentry_id, obj, status, effect in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE3006_0_sources", "3006 source anchors exist", "PASS", True, False, "all required source anchors are present"),
        ("GATE3006_1_conditional_sum", "theta_MTS/Q_tau sector sum is mathematically legal if every sector is owned", "PASS_AS_CONTRACT_ONLY", True, False, "TQV2552_0 gives conditional route, not current proof"),
        ("GATE3006_2_current_owner", "theta_MTS/Q_tau/H_tau are parent-signed now", "FAIL_CLOSED", False, False, "single action, field list, sector variations, theta/Q pieces and constraints are missing"),
        ("GATE3006_3_EH_only_import", "EH charge imports total MTS charge", "REJECTED_SHORTCUT_PASS", True, False, "EH anchor is baseline only and not a total MTS parent charge"),
        ("GATE3006_4_MHref_reentry", "M_H_ref denominator reopens", "BLOCKED_NONCLAIM", False, False, "H_tau/current owner remains missing"),
        ("GATE3006_5_local_claims", "local GR/Newton/PPN/WEP/R10 claim allowed", "FAIL_CLOSED", False, False, "parent current-chain and sector grammar are not derived"),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": gate_status,
                "condition_passed": condition_passed,
                "promotion_allowed_now": promotion_allowed_now,
                "reason": reason,
            }
        )
        for gate_id, gate, gate_status, condition_passed, promotion_allowed_now, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3006_0_conditional_route",
            "Keep the covariant phase-space route.",
            "The route is the correct GR-like mechanism: action variation gives theta, Noether current, surface charge and constraints.",
            "retain as the parent-current contract",
        ),
        (
            "DEC3006_1_no_promotion",
            "Do not promote theta_MTS/Q_tau/H_tau.",
            "Current MTS has contracts and EH baseline, but not a single varied parent action with all retained sectors.",
            "sector charge owner rows remain nonclaim",
        ),
        (
            "DEC3006_2_EH_guard",
            "Do not use EH-only current as total MTS charge.",
            "That would hide extra/projector/boundary/matter-coupling channels inside a GR import.",
            "EH stays a reference anchor only",
        ),
        (
            "DEC3006_3_next",
            "Move to minimal parent action sector grammar.",
            "The current-chain owner can only close if the field list, sector action blocks and first variations are written or omitted sectors are demoted.",
            "3007 should build a source-ready parent action grammar/variation ledger",
        ),
    ]
    return [
        base({"decision_id": decision_id, "decision": decision, "rationale": rationale, "next_effect": next_effect})
        for decision_id, decision, rationale, next_effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3006_0_3007",
                "priority": "selected_primary",
                "target_doc": "3007-Y5-R2FR-minimal-parent-action-sector-grammar-or-sector-variation-ledger-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_minimal_parent_action_sector_grammar_or_sector_variation_ledger_under_AX1090_3007.py",
                "mission": "Build the minimal parent action sector grammar: declare retained fields, action blocks, dimensions, first-variation targets, theta_i/Q_i outputs, and explicitly demote or residualize omitted sectors.",
                "success_condition": "a sector grammar/variation ledger exists that can feed theta_MTS/Q_tau/H_tau extraction without EH-only import or hidden omitted sectors",
                "fallback_if_fail": "keep Hamiltonian-current route closure-only and attack a direct local residual bound path instead",
                "guardrails": "no EH-only charge import; no orbital-GM denominator; no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "path": str(path),
                "path_exists": path.exists(),
                "row_count": len(rows(path)),
                "csv_parse_ok": csv_ok(path),
                "claim_flags_present": any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in rows(path)),
            }
        )
        for copy_id, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    current_chain: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    htau: list[dict[str, Any]],
    reentry: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    generated_rows = sources + current_chain + sectors + htau + reentry + gates + decisions + next_target + branches
    targeted_formalization_hits = []
    if FORMALIZATION.exists():
        patterns = [
            "*Y5_R2FR_3006*",
            "*3006-Y5-R2FR*",
            "*parent_theta_Qtau_Htau_current_owner_3006*",
            "*Hamiltonian_current_sector_charge_rows_3006*",
            "*JR3006_MINIMAL_PARENT_ACTION*",
        ]
        for pattern in patterns:
            targeted_formalization_hits.extend(FORMALIZATION.rglob(pattern))

    checks = [
        ("VAL3006_00_sources_exist", all(boolish(row["path_exists"]) for row in sources), "every cited source path exists", True),
        ("VAL3006_01_source_anchors", all(boolish(row["anchors_found"]) for row in sources), "every source has required anchors", True),
        ("VAL3006_02_current_owner_not_promoted", any(row["audit_id"] == "CCA3006_9_verdict" for row in current_chain) and not any(boolish(row["theorem_promoted_now"]) for row in current_chain), "parent current owner remains not promoted", True),
        ("VAL3006_03_missing_current_clauses", all(expected in {row["current_status"] for row in current_chain} for expected in {"MISSING_SINGLE_PARENT_ACTION_SOURCE", "MISSING_SECTOR_FIRST_VARIATION_PACK", "MISSING_THETA_MTS_EXTRACTION", "MISSING_QTAU_MTS_EXTRACTION", "MISSING_HTAU_INTEGRABILITY_CERTIFICATE", "MISSING_SOURCE_BRIDGE"}), "current-chain audit preserves missing parent clauses", True),
        ("VAL3006_04_sector_rows_nonclaim", len(sectors) == 10 and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) and not boolish(row["promote_sector"]) for row in sectors), "sector charge rows are staged and nonclaim", True),
        ("VAL3006_05_EH_not_total", any(row["sector_id"] == "SEC3006_0_EH_core" and row["current_status"] == "CONDITIONAL_BASELINE_NOT_TOTAL_PARENT" for row in sectors), "EH core is baseline only, not total MTS charge", True),
        ("VAL3006_06_Htau_rows_nonclaim", len(htau) == 9 and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in htau), "H_tau extraction rows are nonclaim", True),
        ("VAL3006_07_denominator_still_blocked", any(row["object"] == "M_H_ref" and row["status"] == "MISSING_POSITIVE_SAME_FRAME_MHREF" for row in reentry), "M_H_ref remains blocked after theta/Q_tau audit", True),
        ("VAL3006_08_local_claims_blocked", all(row["promotion_allowed_now"] is False for row in gates), "no local GR/Newton/PPN/WEP/R10 promotion allowed", True),
        ("VAL3006_09_next_target_sector_grammar", len(next_target) == 1 and "parent action sector grammar" in next_target[0]["mission"], "3007 selects minimal parent action sector grammar next", True),
        ("VAL3006_10_branch_copies", len(branches) == 3 and all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) for row in branches) and not any(boolish(row["claim_flags_present"]) for row in branches), "branch copies exist, parse, and carry no claim flags", True),
        ("VAL3006_11_csv_parse", all(csv_ok(path) for path in OUTPUTS.values() if path.suffix == ".csv"), "all 3006 CSV outputs parse cleanly", True),
        ("VAL3006_12_paths_under_post_checkpoint", all(under(path, ROOT) for path in output_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL3006_13_formalization_untouched", len(targeted_formalization_hits) == 0, "no targeted 3006 files exist under formalization-workbench", True),
        ("VAL3006_14_no_claim_flags", not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in generated_rows), "all generated rows remain valid_for_claim=false and claim_allowed=false", True),
    ]
    preliminary = [
        base({"validation_id": validation_id, "passed": passed, "detail": detail, "required": required})
        for validation_id, passed, detail, required in checks
    ]
    overall = all(boolish(row["passed"]) for row in preliminary if boolish(row["required"]))
    preliminary.append(
        base(
            {
                "validation_id": "VAL3006_OVERALL",
                "passed": overall,
                "detail": "3006 refuses theta_MTS/Q_tau/H_tau promotion, stages sector current-owner rows, and selects minimal parent action sector grammar next",
                "required": True,
            }
        )
    )
    return preliminary


def write_doc(
    sources: list[dict[str, Any]],
    current_chain: list[dict[str, Any]],
    sectors: list[dict[str, Any]],
    htau: list[dict[str, Any]],
    reentry: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 3006 - Y5/R2FR Parent theta-Qtau-Htau Extraction Or Hamiltonian Current Owner Under AX1090

Status: `Y5_R2FR_3006_parent_current_owner_conditional_route_kept_not_promoted_sector_rows_staged_3007_next`

Generated: `{RUN_UTC}`

## Current Verdict

3006 goes upstream of the denominator. The correct GR-like route is not mysterious: vary one parent action, get `theta_MTS`, build `J_tau=theta_MTS(Phi,L_tau Phi)-i_tau L_parent`, decompose `J_tau=dQ_tau^MTS+C_tau`, then integrate `delta H_tau=int_S(delta Q_tau^MTS-i_tau theta_MTS)`.

The conditional theorem is good. If every retained sector supplies its first variation and charge/constraint piece, then `theta_MTS=sum theta_i` and `Q_tau^MTS=sum Q_i` are legitimate. That is exactly the kind of mechanism that could eventually give the GR-to-Newton style reduction.

Current MTS does not yet promote it. EH gives a baseline charge shape, but boundary/reference, Gamma/Khat/q_loc, projector/PiM, matter/source glue, memory/response, coupling and worldtube sectors are not jointly varied and signed. So 3006 refuses `theta_MTS/Q_tau/H_tau` promotion and stages the sector charge-owner rows instead.

## Source Register

{md_table(sources, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Parent Current-Chain Audit

{md_table(current_chain, ["audit_id", "current_chain_clause", "mathematical_form", "current_status", "failure_mode", "source_anchors"])}

## Sector Charge-Owner Rows

{md_table(sectors, ["sector_id", "sector", "needed_current_piece", "current_status", "failure_mode", "source_anchors"])}

## H_tau Extraction Rows

{md_table(htau, ["row_id", "quantity", "mathematical_form", "current_status", "current_value", "source_anchors"])}

## Denominator Reentry After 3006

{md_table(reentry, ["reentry_id", "object", "status", "effect"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branches, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is the first point where the work stops being mostly boundary hygiene and becomes the actual skeleton of a field theory. The route is exactly the right kind of route: parent action -> symplectic potential -> Noether charge -> Hamiltonian source mass. The problem is not the idea; the problem is that the parent action is still distributed across contracts, sector ledgers and conditional clauses rather than one signed variational object.

## Forbidden Claims From 3006

- `theta_MTS` is extracted from a complete parent action.
- `Q_tau^MTS` is the promoted total MTS Hamiltonian charge.
- `H_tau` is integrable and fixed-reference in current MTS.
- EH charge alone is the total MTS charge.
- `M_ref/M_H_ref` reopens as a denominator.
- `epsilon_Bv_ambiguity` or `epsilon_kernel_charge_public_SRNG` is zero.
- Local GR/Newton/PPN/WEP/R10 pass.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    sources = source_rows()
    current_chain = current_chain_rows()
    sectors = sector_rows()
    htau = htau_rows()
    reentry = reentry_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["current_chain"], current_chain)
    write_csv(OUTPUTS["sectors"], sectors)
    write_csv(OUTPUTS["htau"], htau)
    write_csv(OUTPUTS["reentry"], reentry)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    shutil.copyfile(OUTPUTS["current_chain"], BRANCH_OUTPUTS["current_owner_copy"])
    shutil.copyfile(OUTPUTS["sectors"], BRANCH_OUTPUTS["sector_rows_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)
    validation = validation_rows(sources, current_chain, sectors, htau, reentry, gates, decisions, next_target, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, current_chain, sectors, htau, reentry, gates, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL3006_OVERALL")
    if not boolish(overall["passed"]):
        raise SystemExit("3006 validation failed; see P8_Y5_BRR545_3006_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"validation {overall['passed']}: {overall['detail']}")


if __name__ == "__main__":
    main()
