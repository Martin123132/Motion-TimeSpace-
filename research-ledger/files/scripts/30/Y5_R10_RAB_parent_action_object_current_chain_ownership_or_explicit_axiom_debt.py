from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1487-Y5-R10-RAB-parent-action-object-current-chain-ownership-or-explicit-axiom-debt.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1486_next": OUT / "P8_Y5_R10_1486_NEXT_TARGET.csv",
    "1486_validation": OUT / "P8_Y5_BRR545_1486_VALIDATION.csv",
    "1486_neighbourhood": OUT / "P8_Y5_R10_1486_NEIGHBOURHOOD_QUOTIENT_DESCENT_ATTEMPT.csv",
    "1486_moms_map": OUT / "P8_Y5_R10_1486_MOMS_PARENT_SIGNATURE_SOURCE_MAP.csv",
    "1486_clause_gates": OUT / "P8_Y5_R10_1486_CLAUSE_ADOPTION_GATES.csv",
    "1486_parent_action": OUT / "P8_Y5_R10_1486_PARENT_ACTION_OBJECT_AUDIT.csv",
    "1486_axiom_refusal": OUT / "P8_Y5_R10_1486_AXIOM_ADOPTION_REFUSAL.csv",
    "1486_local_reduction": OUT / "P8_Y5_R10_1486_LOCAL_GR_NEWTON_REDUCTION_STATUS.csv",
    "1486_rejections": OUT / "P8_Y5_R10_1486_REJECTION_LEDGER.csv",
    "1009_sector_contract": OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
    "1009_sector_variation": OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv",
    "1008_parent_variation": OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
    "1008_charge_piece": OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
    "1055_parent_contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1055_adoption_gates": OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
    "1090_missing_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1088_moms_clause": OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
    "1088_zero_theorem": OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv",
    "1478_single_action_line": OUT / "P8_Y5_R10_1478_SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT.csv",
    "1479_prefactor_typing": OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1487_SOURCE_REGISTER.csv"
PARENT_ACTION_AUDIT = OUT / "P8_Y5_R10_1487_PARENT_ACTION_OBJECT_CURRENT_CHAIN_AUDIT.csv"
SECTOR_CERTIFICATES = OUT / "P8_Y5_R10_1487_SECTOR_CERTIFICATE_GATE_MATRIX.csv"
THETA_QTAU_AUDIT = OUT / "P8_Y5_R10_1487_THETA_QTAU_OWNERSHIP_AUDIT.csv"
MATTER_OWNER = OUT / "P8_Y5_R10_1487_ORDINARY_MATTER_SUBACTION_OWNER.csv"
AXIOM_DEBT = OUT / "P8_Y5_R10_1487_EXPLICIT_AXIOM_DEBT_LEDGER.csv"
MOMS_UPDATE = OUT / "P8_Y5_R10_1487_MOMS_DEPENDENCY_UPDATE.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1487_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1487_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1487_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1487_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1487_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1487_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1487"
QUAR_PARENT = QUARANTINE / "PARENT_ACTION_OBJECT_CURRENT_CHAIN_AUDIT_NONCLAIM.csv"
QUAR_SECTORS = QUARANTINE / "SECTOR_CERTIFICATE_GATE_MATRIX_NONCLAIM.csv"
QUAR_DEBT = QUARANTINE / "EXPLICIT_AXIOM_DEBT_LEDGER_NONCLAIM.csv"
BRANCH_PARENT = BRANCH_COEFF / "parent_action_object_current_chain_audit_nonclaim_1487.csv"
BRANCH_DEBT = BRANCH_RESIDUALS / "explicit_axiom_debt_ledger_nonclaim_1487.csv"
BRANCH_LOCAL = BRANCH_RESIDUALS / "local_GR_Newton_status_nonclaim_1487.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for data_row in rows:
            writer.writerow(data_row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def common_flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_rows() -> list[dict[str, Any]]:
    usage = {
        "1486_next": "authoritative handoff into 1487",
        "1486_validation": "previous pass validation state",
        "1486_neighbourhood": "open-neighbourhood quotient descent target",
        "1486_moms_map": "MOMS clause source-map blockers",
        "1486_clause_gates": "blocked adoption gates inherited from 1486",
        "1486_parent_action": "immediate parent-action audit input",
        "1486_axiom_refusal": "closure-only axiom refusal input",
        "1486_local_reduction": "local GR/Newton status before 1487",
        "1486_rejections": "previous rejection ledger",
        "1009_sector_contract": "parent sector list and promotion requirements",
        "1009_sector_variation": "sector variation refusal matrix",
        "1008_parent_variation": "theta_MTS and Q_tau extraction audit",
        "1008_charge_piece": "Q_tau piece split and charge ownership gaps",
        "1055_parent_contract": "parent action contract candidate",
        "1055_adoption_gates": "contract-adoption blocks",
        "1090_missing_axioms": "explicit missing axiom ledger",
        "1090_synthesis": "MOMS synthesis failure mode",
        "1088_moms_clause": "minimal ordinary-matter signature clauses",
        "1088_zero_theorem": "conditional zero theorem route",
        "1478_single_action_line": "single ordinary action-density line attempt",
        "1479_prefactor_typing": "source-only prefactor typing attempt",
    }
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1487_{source_index}_{source_key}",
            "path_or_url": relative_path(source_path),
            "source_kind": "local_file",
            "exists_or_resolved": source_path.exists(),
            "usage": usage[source_key],
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items())
    ]


def parent_action_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PAO1487_0_parent_object",
            "one parent action object before readout",
            "S_parent[Phi;theta] owns geometry, EM, ordinary matter, boundary/reference, projector, source-measure, response/memory, and extra/domain sectors before fitting or readout",
            "PAO1486_0;PAC1055_6;PCS1009_9",
            "SCHEMA_WRITTEN_NOT_CURRENT_CHAIN_CLOSED",
            "write or source one L_parent whose variation covers every retained sector",
            "A clean schema exists, but current evidence does not prove one common action object.",
        ),
        (
            "PAO1487_1_delta_L",
            "first variation current chain",
            "delta L_parent = E_A delta Phi^A + d theta_MTS(Phi;delta Phi)",
            "PVA1008_0;PVA1008_1",
            "MISSING_EXPLICIT_CURRENT_CHAIN",
            "extract theta_MTS, Euler terms, boundary terms, and stress terms for all retained sectors",
            "This is the hard owner; without it, Noether identities remain templates rather than MTS theorems.",
        ),
        (
            "PAO1487_2_Q_tau",
            "tau Noether charge owner",
            "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent = d Q_tau^MTS + C_tau",
            "PVA1008_2;PVA1008_3;QTA1008_1..8",
            "FORMAL_SHAPE_NO_TOTAL_OWNER",
            "own Q_EH, Q_boundary, Q_extra, Q_projector, and Q_matter/source in one parent chain",
            "Q_EH can anchor the GR limit, but importing it alone would smuggle in the result.",
        ),
        (
            "PAO1487_3_sector_certificates",
            "retained-sector certificates",
            "each retained sector has action source, field list, variation equation, theta/Q contribution, stress, boundary, tau action, no-hidden-stress, and fixed-before-readout certificates",
            "SVR1009_0..6;PCS1009_0..9",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "close or explicitly demote every sector certificate",
            "This pass turns the blocker into a visible certificate matrix rather than letting it float as vibes.",
        ),
        (
            "PAO1487_4_ordinary_matter_route",
            "ordinary matter subaction owner",
            "S_ord descends through q on an open local neighbourhood with one observed coframe and fixed constants",
            "PCS1009_2;PAC1055_2;SAL1478;PREF1479;MOMS1088",
            "BEST_NARROW_ROUTE_NOT_PARENT_SIGNED",
            "derive matter bundle functor, single density line, fixed constants, and source-label forgetting",
            "This is the best next attack because it may prove the WEP/local-GR silence without finishing every extra sector.",
        ),
        (
            "PAO1487_5_verdict",
            "1487 parent action verdict",
            "current corpus supports an explicit action-object target and debt map, not a closed parent action theorem",
            "1486;1008;1009;1055;1090",
            "NOT_CLOSED_EXPLICIT_AXIOM_DEBT_WRITTEN",
            "pursue the ordinary-matter subaction owner first, then return to extra-sector certificates",
            "No C_parent import, WEP score, local-GR claim, or Newton claim is allowed from 1487.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": target_object,
            "required_statement": required_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "decision_note": decision_note,
            **common_flags(),
        }
        for audit_id, target_object, required_statement, source_anchor, current_status, missing_for_claim, decision_note in rows
    ]


def sector_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SCG1487_0_EH_core",
            "PCS1009_0_EH_core",
            "Einstein-Hilbert baseline",
            "S_EH[g_obs;kappa0,Lambda0]",
            "baseline_anchor_not_total_parent",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_PARTIAL_ANCHOR_ONLY",
            "EH anchor needs constant kappa0, fixed Lambda subtraction, same observed metric in matter/clocks, and MTS residual silence certificates",
        ),
        (
            "SCG1487_1_kappa_topological",
            "PCS1009_1_kappa_topological",
            "topological kappa sector",
            "S_kappa_top[kappa_eff,A_3]",
            "candidate_not_adopted",
            "NO_PARENT_VARIATION_RUNNER_ROW",
            "BLOCKED_NOT_ADOPTED",
            "variation of A_3/kappa_eff, boundary level convention, and no source/species/domain labels remain unsigned",
        ),
        (
            "SCG1487_2_universal_matter",
            "PCS1009_2_universal_matter",
            "ordinary/universal matter",
            "S_matter[psi,g_obs]",
            "conditional_source_input",
            "NO_DEDICATED_1009_VARIATION_ROW",
            "BLOCKED_BEST_NEXT_ROUTE",
            "same observed coframe, matter descent, source Ward identity, and no species-dependent extra coupling must be parent-owned",
        ),
        (
            "SCG1487_3_boundary_reference",
            "PCS1009_3_boundary_reference",
            "boundary/reference terms",
            "S_GHY + fixed exact/topological boundary/reference terms",
            "fixed_reference_missing",
            "NO_DEDICATED_1009_VARIATION_ROW",
            "BLOCKED_FIXED_REFERENCE_MISSING",
            "fixed-before-readout reference, improvement ambiguity certificate, and zero/fixed boundary flux remain unsigned",
        ),
        (
            "SCG1487_4_Gamma_Khat_extra",
            "PCS1009_4_Gamma_Khat_extra",
            "Gamma/Khat/q_loc extra sector",
            "S_GK[g,Phi] for Gamma_eff/K_hat/q_loc",
            "hard_fail_current_claim",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_HARD_FAIL",
            "action existence, Helmholtz integrability, Euler closure, double-zero residual, projector ownership, and boundary no-flux are not proved",
        ),
        (
            "SCG1487_5_domain_projector",
            "PCS1009_5_domain_projector_selector",
            "domain/projector/selector",
            "S_selector[u,h,X,Qcoh,chi_D]",
            "partial_clause_not_parent_closed",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_PARTIAL_CLAUSE",
            "metric-stress accounting, boundary flux, local/FLRW branch rule, and R11 silence remain open",
        ),
        (
            "SCG1487_6_mass_projector_PiM",
            "PCS1009_6_mass_projector_PiM",
            "mass/source-measure projector",
            "Pi_M/source-measure projector sector",
            "not_parent_derived",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_PROJECTOR_ORIGIN",
            "parent symplectic projector algebra, product variation, Ward/Euler flux closure, and measured-GM calibration are not derived",
        ),
        (
            "SCG1487_7_memory_response",
            "PCS1009_7_memory_response_doublet",
            "memory/response doublet",
            "response doublet / memory sector",
            "partial_candidate_not_matched",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_RESPONSE_CERTIFICATE",
            "component map, positive operator, zero odd source, PPN lock, and boundary no-flux remain unsigned",
        ),
        (
            "SCG1487_8_worldtube_source",
            "PCS1009_8_worldtube_source_glue",
            "worldtube/source glue",
            "source/worldtube matching and mass charge glue",
            "core_missing_piece",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_CORE_MASS_GLUE",
            "parent Noether identity, charge form, exterior closure, worldtube matching, and Poisson/Newton calibration remain unsigned",
        ),
        (
            "SCG1487_9_total_parent",
            "PCS1009_9_total_parent_contract",
            "total parent contract",
            "S_parent=sum owned sectors above",
            "not_promoted",
            "REFUSED_INCOMPLETE_PARENT_CURRENT_CHAIN_CONTRACT",
            "BLOCKED_TOTAL_SWITCH_UNSIGNED",
            "all retained sectors need action source/path, stress, Euler, boundary, tau action, sector certificate, no-hidden-stress, and fixed-before-readout certificates",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "sector_id": sector_id,
            "sector_name": sector_name,
            "action_block": action_block,
            "contract_status": contract_status,
            "variation_verdict": variation_verdict,
            "gate_status": gate_status,
            "missing_certificate": missing_certificate,
            **common_flags(),
        }
        for gate_id, sector_id, sector_name, action_block, contract_status, variation_verdict, gate_status, missing_certificate in rows
    ]


def theta_qtau_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TQO1487_0_Lparent",
            "L_parent",
            "delta L_parent = E_A delta Phi^A + d theta_MTS",
            "PVA1008_0",
            "MISSING_EXPLICIT_CURRENT_CHAIN",
            "write/source one current-chain Lagrangian before readout",
        ),
        (
            "TQO1487_1_theta_total",
            "theta_MTS",
            "theta_MTS = theta_EH + theta_boundary + theta_extra + theta_projector + theta_matter/source",
            "PVA1008_1",
            "TEMPLATE_AVAILABLE_NOT_EXTRACTED",
            "extract each sector contribution from a common variation",
        ),
        (
            "TQO1487_2_Jtau",
            "J_tau",
            "J_tau = theta_MTS(L_tau Phi) - i_tau L_parent",
            "PVA1008_2",
            "FORMAL_SHAPE_NO_OWNER",
            "define tau action across metric, matter, representative, boundary/reference fields",
        ),
        (
            "TQO1487_3_Qpieces",
            "Q_tau^MTS",
            "Q_tau^MTS = Q_EH + Q_boundary + Q_extra + Q_projector + Q_matter/source",
            "PVA1008_3;QTA1008_3..8",
            "PIECE_SPLIT_NOT_PROMOTED",
            "extract non-EH pieces or prove they vanish from the parent action",
        ),
        (
            "TQO1487_4_identity_limit",
            "Noether/Ward identity",
            "dJ_tau = -E_A L_tau Phi^A plus boundary terms",
            "PVA1008_4",
            "OWNERSHIP_NOT_ZERO_THEOREM",
            "show residual current silence rather than merely naming the identity",
        ),
        (
            "TQO1487_5_EH_guard",
            "EH import guard",
            "Q_tau^MTS -> Q_tau^EH only after parent reduction/silence/topological clauses are signed",
            "PVA1008_5",
            "REFERENCE_ONLY_GUARD_ACTIVE",
            "do not use GR charge as a shortcut for MTS parent closure",
        ),
        (
            "TQO1487_6_verdict",
            "theta/Q_tau ownership verdict",
            "all retained pieces are owned or proved silent",
            "PVA1008_6;SVR1009_6",
            "NOT_EXTRACTED",
            "continue with a narrower ordinary-matter owner before total action promotion",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": target_object,
            "required_equation": required_equation,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            **common_flags(),
        }
        for audit_id, target_object, required_equation, source_anchor, current_status, missing_for_claim in rows
    ]


def matter_owner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OMSO1487_0_action_form",
            "ordinary matter action form",
            "S_ord = integral L_ord(psi,Dpsi,e_obs(q(Phi)),theta_const)",
            "PCS1009_2;PAC1055_2;MOMS1088_0",
            "CANDIDATE_FORM_USEFUL_NOT_PARENT_SIGNED",
            "derive the parent matter bundle and quotient pullback before species/source readout",
            "This is the most promising narrow route because it targets the WEP silence directly.",
        ),
        (
            "OMSO1487_1_Hilbert_source",
            "Hilbert source owner",
            "T_ab = -2/sqrt(-g) delta S_ord/delta g_obs^ab with one observed coframe",
            "PCS1009_2;PVA1008_4",
            "CONDITIONAL_SOURCE_INPUT",
            "show source current comes from the same parent matter action line",
            "If this closes, Newtonian source universality gets a real derivation route.",
        ),
        (
            "OMSO1487_2_single_density",
            "single action-density line",
            "all ordinary species sit on one matter density line before source-label readout",
            "SAL1478",
            "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED",
            "complete the component vector or demote species weights to explicit residuals",
            "This is where source-only prefactors can still hide.",
        ),
        (
            "OMSO1487_3_no_source_prefactor",
            "no source-only weight slot",
            "there is no Hom(species/source-label -> gravitational-source prefactor) in the parent object language",
            "PREF1479;ADG1055_3",
            "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "derive the operator domain/category rule or retain finite w_A residuals",
            "This is the coupling bottleneck in its smallest form.",
        ),
        (
            "OMSO1487_4_fixed_constants",
            "fixed constants/representation data",
            "alpha, mass ratios, clock constants, and EM normalization are fixed representation data or explicitly retained residuals",
            "PAC1055_1..2;ADG1055_1..2;AX1090_3",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "derive fixed constant sector or keep residual coefficients live",
            "Do not hide charge/alpha/mass debt inside a fake WEP proof.",
        ),
        (
            "OMSO1487_5_neighbourhood_descent",
            "open-neighbourhood quotient descent",
            "S_ord factors through q on an open neighbourhood U, so vertical WEP flows leave ordinary matter action invariant",
            "NQD1486_0..5;ZERO1088",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "upgrade pointwise chain-rule blindness to parent-owned neighbourhood descent",
            "This is the prize: if closed, it buys C_parent double-zero without importing coefficients.",
        ),
        (
            "OMSO1487_6_verdict",
            "ordinary matter owner verdict",
            "ordinary matter subaction is the best 1488 target, but not a 1487 claim",
            "1487 synthesis",
            "BEST_NEXT_ROUTE_SELECTED_NOT_CLOSED",
            "build the 1488 ordinary-matter current-chain owner or lock explicit w_A residuals",
            "We have a sharper door to kick, not a theorem yet.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "owner_id": owner_id,
            "subtarget": subtarget,
            "required_statement": required_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "route_note": route_note,
            **common_flags(),
        }
        for owner_id, subtarget, required_statement, source_anchor, current_status, missing_for_claim, route_note in rows
    ]


def axiom_debt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AX1487_0_parent_object",
            "there exists one parent action object whose ordinary-matter domain is defined before every readout/projection/fitting choice",
            "separate contracts cannot derive each other without a common owner",
            "PAC1055_6;PCS1009_9;AX1090_0",
            "write/source L_parent or keep total-parent promotion blocked",
            "would look elegant but would be an inserted minimality principle",
        ),
        (
            "AX1487_1_current_chain",
            "delta L_parent = E_A delta Phi^A + d theta_MTS is extracted for all retained sectors",
            "Noether/Ward identities and Q_tau cannot be parent-owned without it",
            "PVA1008_0..6;QTA1008_0..8",
            "derive theta/Q pieces sector-by-sector or demote those sectors",
            "would smuggle in local GR charge ownership",
        ),
        (
            "AX1487_2_sector_certificates",
            "every retained sector has action, variation, stress, Euler, boundary, tau-action, and silence certificates",
            "uncertified sectors can carry hidden PPN/WEP residuals",
            "PCS1009;SVR1009",
            "complete certificate matrix or retain explicit residual vectors",
            "would erase live local-bound constraints",
        ),
        (
            "AX1487_3_no_hidden_visible_Hom",
            "the parent object language has no hidden-visible Hom to source, clock, EM, or metric coefficients",
            "blocks source-only prefactors and shadow readout reentry",
            "ADG1055_0;ADG1055_3;AX1090_1;PREF1479",
            "derive operator-domain exclusion or retain finite prefactor residuals",
            "too strong unless tied to real quotient/category construction",
        ),
        (
            "AX1487_4_common_measure_current_norm",
            "ordinary species share one action measure/current normalization before source readout",
            "needed to remove relative source weights w_A",
            "AX1090_2;SAL1478",
            "derive single action-density line and component vector",
            "imports quantum/statistical structure if not derived",
        ),
        (
            "AX1487_5_fixed_constants",
            "mass ratios, alpha, clock constants, and EM/gauge normalization are fixed representation data",
            "otherwise WEP/clock/alpha residuals can reenter",
            "PAC1055_1..2;ADG1055_1..2;AX1090_3",
            "derive fixed constant sector or keep coefficient rows nonclaim",
            "could hide real EM/mass coupling debt",
        ),
        (
            "AX1487_6_variation_before_readout",
            "all variation is performed before projection, calibration, detector readout, or source fitting",
            "otherwise readout terms can imitate a proof of silence",
            "PAC1055_5;ADG1055_4;AX1090_4",
            "derive readout closure theorem or retain readout residual priors",
            "may over-constrain detector/source physics",
        ),
        (
            "AX1487_7_boundary_reference",
            "boundary/reference terms are fixed before readout and contribute no fitted local source force",
            "needed for EH import and local charge/stress closure",
            "PCS1009_3;PVA1008_3;QTA1008_4",
            "prove fixed reference class and boundary no-flux",
            "could bury an adjustable subtraction",
        ),
        (
            "AX1487_8_worldtube_mass_glue",
            "source worldtube mass charge equals exterior Noether/Hilbert charge before orbital fitting",
            "needed for Newton/Poisson source universality",
            "PCS1009_8;SVR1009_4",
            "derive worldtube matching and measured-GM calibration",
            "would collapse a core empirical bridge by declaration",
        ),
        (
            "AX1487_9_memory_response_silence",
            "response/memory sectors are double-zero locally while allowed to activate cosmologically",
            "needed to keep cosmology branch without local PPN/WEP pollution",
            "PCS1009_7;SVR1009_5",
            "derive positive operator, zero odd source, PPN lock, and boundary no-flux",
            "could disguise the local/cosmology split as an axiom",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "axiom_id": axiom_id,
            "axiom_if_adopted": axiom_if_adopted,
            "why_needed": why_needed,
            "current_basis": current_basis,
            "debt_status": "EXPLICIT_DEBT_NOT_ADOPTED",
            "adoption_status": "REFUSED_CLOSURE_ONLY_AXIOM",
            "replacement_work": replacement_work,
            "danger_if_adopted": danger_if_adopted,
            **common_flags(),
        }
        for axiom_id, axiom_if_adopted, why_needed, current_basis, replacement_work, danger_if_adopted in rows
    ]


def moms_update_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MUP1487_0_action_form",
            "MOMS1088_0_action_form",
            "parent ordinary-matter action form",
            "AX1487_0;AX1487_1;AX1487_2",
            "BLOCKED_EXPLICIT_PARENT_ACTION_DEBT",
            "action form is now tied directly to L_parent/current-chain extraction rather than treated as a free clause",
        ),
        (
            "MUP1487_1_quotient_observables",
            "MOMS1088_1_quotient_observables",
            "q-neighbourhood and observed coframe functor",
            "AX1487_0;AX1487_3;OMSO1487_5",
            "BLOCKED_EXACT_CONDITIONAL_ONLY",
            "chain-rule lemma is kept, but parent selection of q/Obs_e on U is still unsigned",
        ),
        (
            "MUP1487_2_matter_bundle",
            "MOMS1088_2_matter_bundle",
            "parent matter bundle functor",
            "OMSO1487_0;OMSO1487_1;OMSO1487_2",
            "BLOCKED_BEST_1488_TARGET",
            "ordinary-matter subaction owner is selected as the next narrow attack",
        ),
        (
            "MUP1487_3_constants",
            "MOMS1088_3_constant_superselection",
            "fixed constant/representation sector",
            "AX1487_5;OMSO1487_4",
            "BLOCKED_CONSTANT_DEBT",
            "constants remain explicit debt, not hidden inside a WEP/local-GR claim",
        ),
        (
            "MUP1487_4_no_species_weights",
            "MOMS1088_4_no_species_weights",
            "no source-only/species weights",
            "AX1487_3;AX1487_4;OMSO1487_3",
            "BLOCKED_COUPLING_BOTTLENECK",
            "source-only prefactor exclusion remains the coupling bottleneck",
        ),
        (
            "MUP1487_5_variation_order",
            "MOMS1088_5_variation_order",
            "variation before readout",
            "AX1487_1;AX1487_6",
            "BLOCKED_READOUT_CLOSURE_DEBT",
            "readout closure cannot be treated as proof until current chain is owned",
        ),
        (
            "MUP1487_6_no_shadow_domain",
            "MOMS1088_6_no_shadow_domain",
            "no hidden/readout/domain reentry",
            "AX1487_3;SCG1487_5",
            "BLOCKED_OPERATOR_DOMAIN_DEBT",
            "operator-domain proof remains needed or finite residuals stay live",
        ),
        (
            "MUP1487_7_verdict",
            "MOMS1088_7_verdict",
            "minimal parent ordinary-matter signature",
            "1487 synthesis",
            "NOT_DERIVED_DEBT_MAP_LOCKED",
            "MOMS is sharpened into explicit debt plus a next target, not promoted",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": update_id,
            "moms_piece": moms_piece,
            "dependency": dependency,
            "new_1487_debt_links": new_debt_links,
            "updated_status": updated_status,
            "effect": effect,
            **common_flags(),
        }
        for update_id, moms_piece, dependency, new_debt_links, updated_status, effect in rows
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CPR1487_0_live_import",
            "forbidden_object": relative_path(C_PARENT_IMPORT),
            "exists": C_PARENT_IMPORT.exists(),
            "current_status": "ABSENT_OK" if not C_PARENT_IMPORT.exists() else "ERROR_LIVE_IMPORT_PRESENT",
            "reason": "C_parent_X remains conditional on parent-signed quotient descent/current-chain ownership",
            "action_taken": "no C_parent import written; branch remains nonclaim",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CPR1487_1_theorem_zero",
            "forbidden_object": "C_parent_X=0 and partial_A C_parent_X=0 as a live coefficient row",
            "exists": False,
            "current_status": "THEOREM_CONDITIONAL_ONLY",
            "reason": "the open-neighbourhood descent theorem route is exact but not parent-signed",
            "action_taken": "kept as local-status blocker, not a prediction row",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LRS1487_0_Cparent",
            "C_parent double-zero",
            "C_parent_X(Phi0)=0 and partial_A C_parent_X(Phi0)=0",
            "EXACT_CONDITIONAL_ONLY",
            "needs open-neighbourhood ordinary matter descent plus vertical q-fibre generator ownership",
            "blocks WEP/local-GR claim",
        ),
        (
            "LRS1487_1_Newton",
            "Newtonian source universality",
            "one Hilbert/source charge and no source-only relative weights",
            "CONDITIONAL_ONLY",
            "ordinary matter single action-density line and worldtube mass glue remain unsigned",
            "relative source weights remain residuals",
        ),
        (
            "LRS1487_2_GR",
            "GR local limit/equivalence principle",
            "same observed coframe and metric matter coupling with no hidden reentry",
            "CONDITIONAL_ONLY",
            "matter functor, constants, operator-domain no-shadow, and current-chain owner remain unsigned",
            "GR reduction not yet derived in MTS language",
        ),
        (
            "LRS1487_3_PPN",
            "PPN residual vector",
            "extra/projector/memory/boundary sectors vanish or are bounded locally",
            "OPEN_RETAINED_RESIDUALS",
            "sector certificate matrix has blocked extra/domain/PiM/memory/worldtube rows",
            "PPN tests remain required after derivation or finite residual selection",
        ),
        (
            "LRS1487_4_verdict",
            "local GR/Newton reduction",
            "parent action/current-chain ownership plus ordinary-matter descent",
            "NOT_CLOSED_BUT_SHARPER",
            "1488 should attack ordinary-matter subaction owner before numeric scoring",
            "no local-GR, Newton, WEP, or R10 pass is claimable from 1487",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "target": target,
            "required_statement": required_statement,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "claim_effect": claim_effect,
            **common_flags(),
        }
        for status_id, target, required_statement, current_status, missing_for_claim, claim_effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1487_0_parent_action", "MISSING_TOTAL_PARENT_ACTION_OBJECT", "one common S_parent/current chain is not closed"),
        ("REJ1487_1_current_chain", "MISSING_THETA_QTAU_EXTRACTION", "theta_MTS and Q_tau^MTS remain templates/piece-splits"),
        ("REJ1487_2_sector_cert", "INCOMPLETE_SECTOR_CERTIFICATES", "retained sectors still lack required action/variation/stress/boundary/tau certificates"),
        ("REJ1487_3_matter_owner", "ORDINARY_MATTER_SUBACTION_NOT_PARENT_SIGNED", "best narrow route is selected but not proved"),
        ("REJ1487_4_prefactor", "SOURCE_ONLY_WEIGHT_PREFACTOR_NOT_EXCLUDED", "coupling bottleneck remains live"),
        ("REJ1487_5_constants", "CONSTANT_SUPERSELECTION_UNSIGNED", "alpha/mass/clock constants remain explicit debt"),
        ("REJ1487_6_shadow", "NO_HIDDEN_VISIBLE_HOM_NOT_DERIVED", "operator-domain/shadow-readout reentry still blocks local claim"),
        ("REJ1487_7_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "no finite/theorem-zero C_parent row can be promoted"),
        ("REJ1487_8_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton/R10 claim allowed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": blocking_marker,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for rejection_id, blocking_marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1487_0_no_total_promotion",
            "do not promote S_parent",
            "the sector/current-chain audit still fails",
            "keep parent action object as explicit debt",
        ),
        (
            "DEC1487_1_no_Cparent_import",
            "do not import C_parent=0",
            "open-neighbourhood descent is exact conditional only",
            "keep WEP/local-GR branches blocked",
        ),
        (
            "DEC1487_2_best_next",
            "attack ordinary matter subaction owner",
            "it is narrower than all-sector closure and directly targets the coupling/source-weight bottleneck",
            "make 1488 the matter-current-chain owner or explicit w_A residual lock",
        ),
        (
            "DEC1487_3_empirical_wait",
            "delay numeric WEP/local scoring",
            "without the coupling owner, numeric rows would be nonclaim smoke only",
            "resume empirical runners after derivation or explicit residual branch selection",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1487_0_1488",
            "next_target": "1488-Y5-R10-RAB-ordinary-matter-subaction-current-chain-owner-or-explicit-wA-residual-lock.md",
            "script": "scripts/Y5_R10_RAB_ordinary_matter_subaction_current_chain_owner_or_explicit_wA_residual_lock.py",
            "objective": "try to close the ordinary-matter subaction current-chain owner before full extra-sector closure; if it cannot be derived, lock finite source-weight residuals w_A/delta_w_A explicitly",
            "include": "S_ord action form; Hilbert source owner; single action-density line; no-source-prefactor Hom gate; fixed constants; open-neighbourhood descent link",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; numeric WEP claim; closure-only axiom adoption",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_COEFF.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PARENT_ACTION_AUDIT, QUAR_PARENT)
    shutil.copyfile(SECTOR_CERTIFICATES, QUAR_SECTORS)
    shutil.copyfile(AXIOM_DEBT, QUAR_DEBT)
    shutil.copyfile(PARENT_ACTION_AUDIT, BRANCH_PARENT)
    shutil.copyfile(AXIOM_DEBT, BRANCH_DEBT)
    shutil.copyfile(LOCAL_STATUS, BRANCH_LOCAL)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    modified_count = 0
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and candidate.stat().st_mtime >= START_TS:
            modified_count += 1
    return modified_count


def all_generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        PARENT_ACTION_AUDIT,
        SECTOR_CERTIFICATES,
        THETA_QTAU_AUDIT,
        MATTER_OWNER,
        AXIOM_DEBT,
        MOMS_UPDATE,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def validation_rows() -> list[dict[str, Any]]:
    generated_csvs = all_generated_csvs()
    validation_checks: list[tuple[str, bool, str]] = []
    source_register = read_csv(SOURCE_REGISTER)
    parent_action = read_csv(PARENT_ACTION_AUDIT)
    sector_matrix = read_csv(SECTOR_CERTIFICATES)
    theta_qtau = read_csv(THETA_QTAU_AUDIT)
    matter_owner = read_csv(MATTER_OWNER)
    axiom_debt = read_csv(AXIOM_DEBT)
    moms_update = read_csv(MOMS_UPDATE)
    c_parent_refusal = read_csv(C_PARENT_REFUSAL)
    local_status = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_target = read_csv(NEXT_TARGET)

    validation_checks.append(
        (
            "VAL1487_0_sources",
            all(str(source_row["exists_or_resolved"]).lower() == "true" for source_row in source_register),
            "all cited local source paths exist",
        )
    )
    validation_checks.append(
        (
            "VAL1487_1_parent_not_closed",
            any(data_row["current_status"] == "NOT_CLOSED_EXPLICIT_AXIOM_DEBT_WRITTEN" for data_row in parent_action),
            "parent action object/current-chain remains not closed and debt is explicit",
        )
    )
    validation_checks.append(
        (
            "VAL1487_2_sector_gates_blocked",
            all(data_row["gate_status"].startswith("BLOCKED") for data_row in sector_matrix),
            "all retained sector certificates remain blocked/nonclaim",
        )
    )
    validation_checks.append(
        (
            "VAL1487_3_theta_qtau_not_extracted",
            any(data_row["current_status"] == "NOT_EXTRACTED" for data_row in theta_qtau),
            "theta_MTS/Q_tau ownership not extracted",
        )
    )
    validation_checks.append(
        (
            "VAL1487_4_matter_best_next_not_claim",
            any(data_row["current_status"] == "BEST_NEXT_ROUTE_SELECTED_NOT_CLOSED" for data_row in matter_owner),
            "ordinary matter owner selected as best next route but remains nonclaim",
        )
    )
    validation_checks.append(
        (
            "VAL1487_5_axiom_debt_not_adopted",
            all(data_row["debt_status"] == "EXPLICIT_DEBT_NOT_ADOPTED" and data_row["adoption_status"] == "REFUSED_CLOSURE_ONLY_AXIOM" for data_row in axiom_debt),
            "all axiom rows are explicit debt and refused as closure-only adoption",
        )
    )
    validation_checks.append(
        (
            "VAL1487_6_moms_dependency_blocked",
            all(data_row["updated_status"].startswith("BLOCKED") or data_row["updated_status"].startswith("NOT_DERIVED") for data_row in moms_update),
            "MOMS dependencies remain blocked/not derived",
        )
    )
    validation_checks.append(
        (
            "VAL1487_7_no_Cparent_import",
            (not C_PARENT_IMPORT.exists()) and all(str(data_row["claim_allowed"]).lower() == "false" for data_row in c_parent_refusal),
            "live C_parent import remains absent and refused",
        )
    )
    validation_checks.append(
        (
            "VAL1487_8_local_reduction_blocked",
            any(data_row["current_status"] == "NOT_CLOSED_BUT_SHARPER" for data_row in local_status),
            "local GR/Newton route is sharper but not closed",
        )
    )
    validation_checks.append(
        (
            "VAL1487_9_rejections_block_claim",
            len(rejections) >= 8 and all(str(data_row["claim_allowed"]).lower() == "false" for data_row in rejections),
            "rejection ledger blocks claim promotion",
        )
    )
    validation_checks.append(
        (
            "VAL1487_10_decisions",
            any(data_row["decision_id"] == "DEC1487_2_best_next" for data_row in decisions),
            "decision ledger selects ordinary-matter subaction owner as next target",
        )
    )
    validation_checks.append(
        (
            "VAL1487_11_next",
            len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1487_0_1488",
            "1488 handoff written",
        )
    )
    validation_checks.append(
        (
            "VAL1487_12_csv_parse",
            all(parse_csv(csv_path) for csv_path in generated_csvs),
            "all generated 1487 CSVs parse cleanly",
        )
    )
    validation_checks.append(
        (
            "VAL1487_13_branch_copies",
            all(copy_path.exists() for copy_path in [QUAR_PARENT, QUAR_SECTORS, QUAR_DEBT, BRANCH_PARENT, BRANCH_DEBT, BRANCH_LOCAL]),
            "branch/quarantine nonclaim copies written",
        )
    )
    remove_pycache()
    validation_checks.append(
        (
            "VAL1487_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent after run",
        )
    )
    modified_count = formalization_modified_count()
    validation_checks.append(
        (
            "VAL1487_15_formalization_untouched",
            modified_count == 0,
            f"formalization modified-file count since start={modified_count}",
        )
    )
    claim_flag_paths = generated_csvs + [QUAR_PARENT, QUAR_SECTORS, QUAR_DEBT, BRANCH_PARENT, BRANCH_DEBT, BRANCH_LOCAL]
    claim_flags_false = True
    for claim_flag_path in claim_flag_paths:
        for data_row in read_csv(claim_flag_path):
            for flag_name in ("valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if flag_name in data_row and str(data_row[flag_name]).lower() != "false":
                    claim_flags_false = False
    validation_checks.append(
        (
            "VAL1487_16_claim_flags_false",
            claim_flags_false,
            "all prediction/claim flags remain false",
        )
    )

    overall_pass = all(check_result for _, check_result, _ in validation_checks)
    validation_checks.append(
        (
            "VAL1487_17_overall",
            overall_pass,
            "1487 locks parent-action/current-chain debt and selects ordinary-matter owner as the next derivation target",
        )
    )
    return [
        {
            "check_id": check_id,
            "result": "PASS" if check_result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, check_result, detail in validation_checks
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for data_row in rows:
        body.append("| " + " | ".join(str(data_row.get(column, "")).replace("|", "/") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    parent_action = read_csv(PARENT_ACTION_AUDIT)
    sector_matrix = read_csv(SECTOR_CERTIFICATES)
    theta_qtau = read_csv(THETA_QTAU_AUDIT)
    matter_owner = read_csv(MATTER_OWNER)
    axiom_debt = read_csv(AXIOM_DEBT)
    moms_update = read_csv(MOMS_UPDATE)
    local_status = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_target = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)

    lines = [
        "# 1487 - Parent Action Object Current Chain Ownership Or Explicit Axiom Debt",
        "",
        "## Verdict",
        "- The parent action/current-chain route is sharpened, but not closed: `S_parent`, `theta_MTS`, and `Q_tau^MTS` remain unsigned across all retained sectors.",
        "- This pass does not adopt closure axioms; it writes the exact axiom debt and keeps every local-GR/Newton/WEP/R10 claim blocked.",
        "- The best next target is narrower: close the ordinary-matter subaction owner first, because that is where the coupling/source-weight bottleneck lives.",
        "",
        "## Parent Action Current Chain Audit",
        markdown_table(parent_action, ["audit_id", "current_status", "missing_for_claim"]),
        "",
        "## Sector Certificate Gate Matrix",
        markdown_table(sector_matrix, ["gate_id", "sector_id", "gate_status", "missing_certificate"]),
        "",
        "## Theta And Q Tau Ownership",
        markdown_table(theta_qtau, ["audit_id", "object", "current_status", "missing_for_claim"]),
        "",
        "## Ordinary Matter Subaction Owner",
        markdown_table(matter_owner, ["owner_id", "subtarget", "current_status", "missing_for_claim"]),
        "",
        "## Explicit Axiom Debt",
        markdown_table(axiom_debt, ["axiom_id", "debt_status", "replacement_work", "danger_if_adopted"]),
        "",
        "## MOMS Dependency Update",
        markdown_table(moms_update, ["update_id", "moms_piece", "updated_status", "effect"]),
        "",
        "## Local GR/Newton Status",
        markdown_table(local_status, ["status_id", "target", "current_status", "claim_effect"]),
        "",
        "## Rejection Ledger",
        markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]),
        "",
        "## Decision Ledger",
    ]
    for decision in decisions:
        lines.append(f"- `{decision['decision_id']}`: {decision['decision']} - {decision['next_action']}.")
    lines.extend(
        [
            "",
            "## Validation",
            markdown_table(validation, ["check_id", "result", "detail"]),
            "",
            "## Next Target",
            markdown_table(next_target, ["next_id", "next_target", "script", "objective"]),
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(PARENT_ACTION_AUDIT, parent_action_rows())
    write_csv(SECTOR_CERTIFICATES, sector_certificate_rows())
    write_csv(THETA_QTAU_AUDIT, theta_qtau_rows())
    write_csv(MATTER_OWNER, matter_owner_rows())
    write_csv(AXIOM_DEBT, axiom_debt_rows())
    write_csv(MOMS_UPDATE, moms_update_rows())
    write_csv(C_PARENT_REFUSAL, c_parent_refusal_rows())
    write_csv(LOCAL_STATUS, local_status_rows())
    write_csv(REJECTION_LEDGER, rejection_rows())
    write_csv(DECISION_LEDGER, decision_rows())
    write_csv(NEXT_TARGET, next_target_rows())
    copy_outputs()
    write_csv(VALIDATION, validation_rows())
    write_doc()
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {VALIDATION}")


if __name__ == "__main__":
    main()
