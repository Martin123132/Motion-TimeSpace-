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
DOC = ROOT / "1489-Y5-R10-RAB-no-source-only-Hom-exclusion-or-delta-w-bound-interface.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1488_next": OUT / "P8_Y5_R10_1488_NEXT_TARGET.csv",
    "1488_validation": OUT / "P8_Y5_BRR545_1488_VALIDATION.csv",
    "1488_hom_gate": OUT / "P8_Y5_R10_1488_NO_SOURCE_ONLY_HOM_GATE.csv",
    "1488_delta_w_lock": OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
    "1488_current_chain": OUT / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv",
    "1479_typing": OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv",
    "1479_hom_audit": OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv",
    "1066_object_language": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1066_operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1066_delta_w_import": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv",
    "1051_invariant_scalar": OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "1055_adoption_gates": OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
    "1450_hilbert_forgetting": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1451_operator_grammar": OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv",
    "1451_bound_requirements": OUT / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv",
    "1416_current_rescaling": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
    "1416_countermodel": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv",
    "1333_prefactor_attempt": OUT / "P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv",
    "1333_countermodel": OUT / "P8_Y5_R10_1333_SOURCE_PREFACTOR_COUNTERMODEL_LEDGER.csv",
    "1229_source_clause": OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
    "1229_counterexample": OUT / "P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1489_SOURCE_REGISTER.csv"
HOM_THEOREM = OUT / "P8_Y5_R10_1489_NO_SOURCE_ONLY_HOM_EXCLUSION_THEOREM_ATTEMPT.csv"
COEFF_TARGETS = OUT / "P8_Y5_R10_1489_TYPED_COEFFICIENT_TARGET_AUDIT.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1489_HOM_COUNTERMODEL_LEDGER.csv"
DELTA_W_INTERFACE = OUT / "P8_Y5_R10_1489_DELTA_W_BOUND_INTERFACE_NONCLAIM.csv"
COMMON_CALIBRATION = OUT / "P8_Y5_R10_1489_COMMON_CALIBRATION_RULE.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1489_RESIDUAL_PROMOTION_GATES.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1489_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1489_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1489_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1489_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1489_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1489_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1489"
QUAR_HOM = QUARANTINE / "NO_SOURCE_ONLY_HOM_EXCLUSION_THEOREM_ATTEMPT_NONCLAIM.csv"
QUAR_COUNTER = QUARANTINE / "HOM_COUNTERMODEL_LEDGER_NONCLAIM.csv"
QUAR_DELTA = QUARANTINE / "DELTA_W_BOUND_INTERFACE_NONCLAIM.csv"
BRANCH_HOM = BRANCH_RESIDUALS / "no_source_only_Hom_exclusion_attempt_nonclaim_1489.csv"
BRANCH_COUNTER = BRANCH_RESIDUALS / "Hom_countermodel_ledger_nonclaim_1489.csv"
BRANCH_DELTA = BRANCH_RESIDUALS / "delta_w_bound_interface_nonclaim_1489.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
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
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def nonclaim() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_rows() -> list[dict[str, Any]]:
    usage = {
        "1488_next": "authoritative 1489 handoff",
        "1488_validation": "previous validation state",
        "1488_hom_gate": "no-source-only Hom gate source",
        "1488_delta_w_lock": "delta_w residual lock source",
        "1488_current_chain": "ordinary matter current-chain status",
        "1479_typing": "typing theorem attempt",
        "1479_hom_audit": "Hom channel audit",
        "1066_object_language": "object-language type status",
        "1066_operator_domain": "operator-domain source scalar exclusion",
        "1066_source_scalar": "source-scalar exclusion lemma",
        "1066_delta_w_import": "prior delta_w bound interface seed",
        "1051_invariant_scalar": "hidden invariant scalar obstruction",
        "1055_adoption_gates": "parent contract-adoption gates",
        "1450_hilbert_forgetting": "Hilbert source label-forgetting theorem attempt",
        "1451_operator_grammar": "no-source-only operator grammar theorem attempt",
        "1451_bound_requirements": "epsilon/delta_w bound input requirements",
        "1416_current_rescaling": "current rescaling ban attempt",
        "1416_countermodel": "source slot countermodel ledger",
        "1333_prefactor_attempt": "no source-prefactor derivation attempt",
        "1333_countermodel": "source prefactor countermodel ledger",
        "1229_source_clause": "universal source coupling clause audit",
        "1229_counterexample": "source-coupling counterexample ledger",
    }
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1489_{idx}_{key}",
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage[key],
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for idx, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def hom_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HET1489_0_target",
            "no source-only Hom theorem target",
            "Hom_parent(species_label, hidden_invariant, marker, current_label, readout_label -> R_+ active_source_prefactor) is empty or common-constant only",
            "HOMG1488_0;NST1479_0",
            "TARGET_EXACT",
            "derive this from parent object language, not from aesthetic minimality",
            "If signed, relative source weights collapse to theorem-zero modulo one common calibration.",
        ),
        (
            "HET1489_1_positive_typing_result",
            "candidate typing kills inert source scalar",
            "admissible arguments are geometry, matter fields, gauge/current data, representation constants, and universal constants; inert source-only w_A is rejected",
            "OLT1066_0..6;NST1479_1",
            "EXACT_CONDITIONAL_META_THEOREM",
            "typing restriction is still a parent grammar contract, not derived from MTS primitives",
            "This is the best proof-shaped piece, but still conditional.",
        ),
        (
            "HET1489_2_target_type_rule",
            "source coefficient target exclusion",
            "Coeff_source-only is not an object of the visible/readout coefficient ring except as common calibration",
            "ODR1066_0;ODR1066_4;NST1479_2",
            "POWERFUL_IF_SIGNED_NOT_REDUCED",
            "requires invariant algebra triviality/no-extension plus action-scale ownership",
            "This is the smallest formal lock we still lack.",
        ),
        (
            "HET1489_3_hidden_invariant_failure",
            "hidden invariant obstruction",
            "if a nonconstant invariant scalar I_hid exists and R_+ source coefficients are legal targets, w=w0+epsilon I_hid is a legal Hom",
            "ODR1066_1;HOM1479_2;ISO1051",
            "COUNTERMODEL_SURVIVES",
            "prove invariant algebra triviality or ban the source coefficient target",
            "This prevents the Hom theorem from closing.",
        ),
        (
            "HET1489_4_species_component_failure",
            "species/disconnected component obstruction",
            "if ordinary matter components remain label-visible, Nat(C_disconnected,R_+) admits independent constants",
            "ODR1066_2;HOM1479_1;HT1450_3",
            "COUNTERMODEL_SURVIVES",
            "prove connected common action-measure owner and label forgetting before source coupling",
            "Same-action Hilbert variation does not by itself kill this.",
        ),
        (
            "HET1489_5_readout_failure",
            "readout/source transfer obstruction",
            "post-variation readout/source-worldtube labels can feed active source weights unless variation-before-readout and transfer rules are parent-owned",
            "HOM1479_5;ADG1055_4",
            "READOUT_TRANSFER_UNSIGNED",
            "derive readout closure or retain readout delta_w residuals",
            "This keeps detector/source modelling honest.",
        ),
        (
            "HET1489_6_verdict",
            "Hom exclusion theorem verdict",
            "the theorem is exact as a conditional grammar rule but not derivable from current parent sources",
            "1489 synthesis",
            "NOT_DERIVED_DELTA_W_INTERFACE_BUILT",
            "keep delta_w bound interface nonclaim and target source-coefficient target/invariant algebra next",
            "A good miss: the problem is now mathematically localised.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "route_note": route_note,
            **nonclaim(),
        }
        for theorem_id, claim_piece, formal_statement, source_anchor, current_status, missing_for_claim, route_note in rows
    ]


def coefficient_target_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CTA1489_0_visible_geometry",
            "geometry/coframe coefficients",
            "Alg[q_loc, e_obs, g_obs, connection]",
            "ADMISSIBLE_IF_PARENT_Q_SIGNED",
            "does not by itself create species source weights",
            "MFS1045_0..1;OLT1066_0",
        ),
        (
            "CTA1489_1_matter_fields",
            "dynamical matter fields",
            "Psi_A and gauge/current fields inside S_ord",
            "ADMISSIBLE",
            "labels remain harmless only after source functor forgets them",
            "OLT1066_1;HT1450_0",
        ),
        (
            "CTA1489_2_representation_constants",
            "measured representation constants",
            "m_A, q_A, charges, spectra, interaction couplings",
            "ADMISSIBLE_IF_OBSERVABLE_NOT_SOURCE_ONLY",
            "can still be dangerous if converted into active source prefactor",
            "OLT1066_2;MFS1045_5",
        ),
        (
            "CTA1489_3_common_calibration",
            "universal source calibration",
            "one w_star/kappa_univ common mode",
            "CALIBRATION_ONLY_GUARDED",
            "not a WEP signal if species/time/range/frame silent",
            "OLT1066_3;HOM1479_0",
        ),
        (
            "CTA1489_4_inert_source_scalar",
            "relative source/action prefactor",
            "w_A multiplying only action/source strength",
            "REJECTED_BY_CANDIDATE_TYPING_NOT_PARENT_SIGNED",
            "live delta_w residual until object-language theorem is parent-derived",
            "OLT1066_4;NST1479_0",
        ),
        (
            "CTA1489_5_hidden_marker",
            "hidden/domain/material marker coefficient",
            "w(I_hid, D, material, boundary, readout)",
            "OBSTRUCTION_ACTIVE",
            "must be theorem-forbidden or explicitly bounded",
            "OLT1066_5;ODR1066_1;HOM1479_2..5",
        ),
        (
            "CTA1489_6_verdict",
            "typed coefficient target verdict",
            "source-only R_+ coefficient target is not parent-excluded yet",
            "EXACT_RULE_NOT_DERIVED",
            "derive coefficient-target exclusion or keep bound interface",
            "ODR1066_4;NST1479_4",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "target_id": target_id,
            "coefficient_target": coefficient_target,
            "formal_domain": formal_domain,
            "current_status": current_status,
            "effect_on_delta_w": effect_on_delta_w,
            "source_anchor": source_anchor,
            **nonclaim(),
        }
        for target_id, coefficient_target, formal_domain, current_status, effect_on_delta_w, source_anchor in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HCM1489_0_species_weight",
            "species label source prefactor",
            "S_ord=sum_A w_A S_A gives T_source=sum_A w_A T_A while preserving covariance/additivity inside each sector",
            "HT1450_3;NST1479_3;HOM1479_1",
            "LIVE_COUNTERMODEL",
            "common action-measure owner plus source-label forgetting before coupling",
        ),
        (
            "HCM1489_1_hidden_invariant",
            "hidden invariant source coefficient",
            "nonconstant I_hid feeding w=w0+epsilon I_hid if R_+ source target is legal",
            "ODR1066_1;HOM1479_2;1051 invariant scalar obstruction",
            "LIVE_COUNTERMODEL",
            "hidden invariant algebra triviality or target exclusion",
        ),
        (
            "HCM1489_2_material_marker",
            "material/domain/boundary marker prefactor",
            "w(marker_A, domain, boundary) reintroduces composition labels under another name",
            "HOM1479_3;OLT1066_5",
            "LIVE_COUNTERMODEL",
            "no-marker/no-spurion closure and boundary/domain silence",
        ),
        (
            "HCM1489_3_current_rescaling",
            "current-label normalization",
            "J_A -> c_A J_A or beta_source,A",
            "HOM1479_4;HT1450_5;1416 current rescaling",
            "LIVE_COUNTERMODEL",
            "current owner and Hilbert/non-Hilbert source split",
        ),
        (
            "HCM1489_4_readout_transfer",
            "readout/source-worldtube prefactor",
            "post-variation source/readout selector creates active source weight",
            "HOM1479_5;ADG1055_4",
            "LIVE_COUNTERMODEL",
            "variation-before-readout and source-worldtube transfer ownership",
        ),
        (
            "HCM1489_5_common_mode",
            "common universal calibration",
            "w_star common to all ordinary sources",
            "HOM1479_0",
            "NOT_WEP_SIGNAL_IF_SILENT",
            "prove no time/range/frame/species dependence before absorbing into G_N/GM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "construction": construction,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "required_to_close": required_to_close,
            "theorem_zero_allowed_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, construction, source_anchor, current_status, required_to_close in rows
    ]


def delta_w_interface_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DWI1489_0_core_formula",
            "core",
            "delta_w_AB",
            "eta_AB ~= sum_i DeltaQ_i(AB) * delta_w_i * tau_i",
            "dimensionless",
            "symbolic_interface",
            "material charge vector DeltaQ_i, arena tau_i, source/readout transfer, experimental bound",
        ),
        (
            "DWI1489_1_MICROSCOPE_WEP",
            "WEP_MICROSCOPE_TiPt",
            "delta_w_TiPt",
            "|eta_TiPt| <= |DeltaQ_TiPt dot delta_w| times tau_eff",
            "dimensionless",
            "source_ready_skeleton",
            "official readout, material vector, Earth/source kernel, tau_eff normalization",
        ),
        (
            "DWI1489_2_EotWash_WEP",
            "WEP_EotWash",
            "delta_w_material_pair",
            "|eta_AB| bound maps to source-weight contrast through material/source response",
            "dimensionless",
            "source_ready_skeleton",
            "experiment-specific composition vectors, source attractor vector, range/profile transfer",
        ),
        (
            "DWI1489_3_R10_short_range",
            "R10_short_range",
            "delta_w_R10",
            "alpha_pred(lambda) includes source/test source-weight leakage channel",
            "dimensionless",
            "source_ready_skeleton",
            "lambda profile, source/test composition response, real bound curve, parent range map",
        ),
        (
            "DWI1489_4_clock_alpha_mass",
            "clock_alpha_mass",
            "delta_w_clock",
            "clock ratio drifts constrain products of source-weight/constant leakage and clock sensitivity",
            "dimensionless",
            "source_ready_skeleton",
            "clock sensitivity matrix, tau_clock, alpha/mass owner split",
        ),
        (
            "DWI1489_5_orbital",
            "orbital_source_mass",
            "delta_w_orbital",
            "GM_source/readout residuals constrain active-source calibration and composition leakage",
            "dimensionless",
            "source_ready_skeleton",
            "source body composition, measured GM convention, orbital residual projection",
        ),
        (
            "DWI1489_6_claim_gate",
            "all_arenas",
            "delta_w_bound_claim",
            "no delta_w bound row is claimable until all source vectors, taus, units, and source paths are numeric and cited",
            "dimensionless",
            "NONCLAIM_INTERFACE_ONLY",
            "numeric source-backed rows and runner acceptance gates",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": interface_id,
            "arena": arena,
            "symbol": symbol,
            "bound_formula": bound_formula,
            "units": units,
            "status": status,
            "numeric_bound": "MISSING_SOURCE_BACKED_BOUND",
            "missing_for_claim": missing_for_claim,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for interface_id, arena, symbol, bound_formula, units, status, missing_for_claim in rows
    ]


def common_calibration_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CCR1489_0_common_mode_definition",
            "w_star",
            "one universal multiplicative calibration of all ordinary Hilbert sources",
            "COMMON_MODE_ALLOWED_IF_SILENT",
            "can be absorbed into measured G_N/GM only after silence guards",
        ),
        (
            "CCR1489_1_not_wEP_signal",
            "w_star_vs_delta_w",
            "WEP-sensitive residual is delta_w_A := w_A - w_star, not w_star itself",
            "DECOMPOSITION_RULE",
            "prevents confusing calibration with equivalence-principle violation",
        ),
        (
            "CCR1489_2_absorption_gate",
            "absorb_into_G",
            "w_star can be absorbed only if no time/range/frame/species/source-body dependence survives",
            "GUARDED_NOT_CLAIMED",
            "requires source/readout transfer and local-domain proof",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": rule_id,
            "object": object_name,
            "rule": rule,
            "status": status,
            "missing_for_claim": missing_for_claim,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rule_id, object_name, rule, status, missing_for_claim in rows
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PG1489_0_Hom_theorem", "Hom exclusion theorem", "FAIL", "hidden invariant/species/readout countermodels survive"),
        ("PG1489_1_delta_w_zero", "delta_w theorem-zero", "FAIL", "no-source-only prefactor channel is not parent-forbidden"),
        ("PG1489_2_delta_w_bound", "delta_w numeric bound", "FAIL_NONCLAIM_INTERFACE_ONLY", "source-backed vectors/tau/bounds are missing"),
        ("PG1489_3_Cparent", "C_parent import", "FAIL_FORBIDDEN", "ordinary matter/source-weight owner remains unsigned"),
        ("PG1489_4_local_GR", "local GR/Newton/WEP claim", "FAIL", "universal coupling is not derived"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "result": result,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, result, reason in rows
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CPR1489_0_live_import",
            "forbidden_object": rel(C_PARENT_IMPORT),
            "exists": C_PARENT_IMPORT.exists(),
            "current_status": "ABSENT_OK" if not C_PARENT_IMPORT.exists() else "ERROR_LIVE_IMPORT_PRESENT",
            "reason": "Hom exclusion theorem did not close; delta_w residual interface is nonclaim",
            "action_taken": "no C_parent import written",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LRS1489_0_coupling",
            "universal ordinary-matter coupling",
            "Hom(source labels -> active source prefactor)=empty/common-only",
            "NOT_DERIVED",
            "hidden invariant, species component, marker/current/readout Hom countermodels survive",
            "universal coupling not yet claimable",
        ),
        (
            "LRS1489_1_WEP",
            "WEP source universality",
            "delta_w_A=0 modulo common calibration",
            "BLOCKED_DELTA_W_RETAINED",
            "delta_w interface is symbolic and nonclaim",
            "WEP theorem-zero blocked",
        ),
        (
            "LRS1489_2_Newton",
            "Newtonian source",
            "one active Hilbert source with no relative source weights",
            "CONDITIONAL_ONLY",
            "same-action source is not enough without Hom exclusion",
            "Newton reduction still conditional",
        ),
        (
            "LRS1489_3_GR",
            "local GR matter coupling",
            "observed metric/coframe universal matter coupling",
            "CONDITIONAL_ONLY",
            "matter functor plus no-source-Hom grammar still unsigned",
            "GR reduction not yet claimable",
        ),
        (
            "LRS1489_4_verdict",
            "local GR/Newton status",
            "coupling bottleneck made testable but not derived",
            "NOT_CLOSED_NEXT_TARGET_SOURCE_TARGET_OR_INVARIANT_ALGEBRA",
            "derive source coefficient target exclusion or hidden invariant algebra triviality",
            "no local-GR/Newton/WEP/R10 claim from 1489",
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
            **nonclaim(),
        }
        for status_id, target, required_statement, current_status, missing_for_claim, claim_effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1489_0_Hom", "NO_SOURCE_ONLY_HOM_NOT_DERIVED", "Hom exclusion remains exact conditional only"),
        ("REJ1489_1_hidden", "HIDDEN_INVARIANT_COUNTERMODEL_SURVIVES", "nonconstant hidden invariant can feed continuous source coefficient"),
        ("REJ1489_2_species", "SPECIES_COMPONENT_COUNTERMODEL_SURVIVES", "disconnected/label-visible components permit independent constants"),
        ("REJ1489_3_readout", "READOUT_TRANSFER_UNSIGNED", "post-variation readout/source labels can reenter"),
        ("REJ1489_4_delta_w", "DELTA_W_INTERFACE_NONCLAIM", "bound interface has missing source-backed numeric inputs"),
        ("REJ1489_5_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "ordinary matter coupling owner not signed"),
        ("REJ1489_6_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton/R10 claim allowed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1489_0_Hom_not_promoted",
            "do not promote no-source-only Hom exclusion",
            "it remains a conditional grammar rule with live countermodels",
            "target source coefficient target exclusion or hidden invariant algebra next",
        ),
        (
            "DEC1489_1_delta_w_interface",
            "retain delta_w bound interface as nonclaim",
            "derivation failed honestly and empirical branch needs a clean input contract",
            "do not score until source vectors/tau/bounds are real",
        ),
        (
            "DEC1489_2_common_mode",
            "separate w_star common calibration from delta_w_A",
            "common calibration is not a WEP signal if truly universal and silent",
            "keep w_star guarded rather than claim-absorbed",
        ),
        (
            "DEC1489_3_next",
            "attack source coefficient target/invariant algebra",
            "one surviving scalar Hom is enough to keep coupling open",
            "1490 should prove target exclusion/triviality or fill real bound inputs",
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
            "next_id": "NEXT1489_0_1490",
            "next_target": "1490-Y5-R10-RAB-source-coefficient-target-exclusion-or-hidden-invariant-algebra-triviality.md",
            "script": "scripts/Y5_R10_RAB_source_coefficient_target_exclusion_or_hidden_invariant_algebra_triviality.py",
            "objective": "try to prove the source-only R_+ coefficient target is absent from the parent object language, or prove hidden invariant algebra triviality; if neither closes, move to real source-backed delta_w bound inputs",
            "include": "Coeff_source target; invariant scalar algebra; common calibration exception; species/readout Hom dependencies; delta_w interface gate",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; numeric WEP claim; closure-only axiom adoption",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        HOM_THEOREM,
        COEFF_TARGETS,
        COUNTERMODELS,
        DELTA_W_INTERFACE,
        COMMON_CALIBRATION,
        PROMOTION_GATES,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HOM_THEOREM, QUAR_HOM)
    shutil.copyfile(COUNTERMODELS, QUAR_COUNTER)
    shutil.copyfile(DELTA_W_INTERFACE, QUAR_DELTA)
    shutil.copyfile(HOM_THEOREM, BRANCH_HOM)
    shutil.copyfile(COUNTERMODELS, BRANCH_COUNTER)
    shutil.copyfile(DELTA_W_INTERFACE, BRANCH_DELTA)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows() -> list[dict[str, Any]]:
    source_register = read_csv(SOURCE_REGISTER)
    hom = read_csv(HOM_THEOREM)
    targets = read_csv(COEFF_TARGETS)
    countermodels = read_csv(COUNTERMODELS)
    delta = read_csv(DELTA_W_INTERFACE)
    calibration = read_csv(COMMON_CALIBRATION)
    gates = read_csv(PROMOTION_GATES)
    c_parent = read_csv(C_PARENT_REFUSAL)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_target = read_csv(NEXT_TARGET)

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1489_0_sources",
            all(row["exists_or_resolved"].lower() == "true" for row in source_register),
            "all cited local source paths exist",
        ),
        (
            "VAL1489_1_Hom_not_derived",
            any(row["current_status"] == "NOT_DERIVED_DELTA_W_INTERFACE_BUILT" for row in hom),
            "Hom exclusion theorem is not promoted and delta_w interface is built",
        ),
        (
            "VAL1489_2_targets_not_closed",
            any(row["current_status"] == "EXACT_RULE_NOT_DERIVED" for row in targets),
            "source-only coefficient target exclusion is not derived",
        ),
        (
            "VAL1489_3_countermodels_live",
            any(row["current_status"] == "LIVE_COUNTERMODEL" for row in countermodels),
            "live Hom countermodels remain explicit",
        ),
        (
            "VAL1489_4_delta_interface_nonclaim",
            all(row["numeric_bound"] == "MISSING_SOURCE_BACKED_BOUND" and row["claim_allowed"].lower() == "false" for row in delta),
            "delta_w bound interface rows are symbolic nonclaim rows",
        ),
        (
            "VAL1489_5_common_calibration_guarded",
            any(row["status"] == "GUARDED_NOT_CLAIMED" for row in calibration),
            "common calibration is guarded, not absorbed by claim",
        ),
        (
            "VAL1489_6_promotion_gates_fail",
            all(row["claim_allowed"].lower() == "false" for row in gates),
            "all promotion gates block claims",
        ),
        (
            "VAL1489_7_no_Cparent_import",
            (not C_PARENT_IMPORT.exists()) and all(row["claim_allowed"].lower() == "false" for row in c_parent),
            "live C_parent import remains absent and refused",
        ),
        (
            "VAL1489_8_local_blocked",
            any(row["current_status"] == "NOT_CLOSED_NEXT_TARGET_SOURCE_TARGET_OR_INVARIANT_ALGEBRA" for row in local),
            "local GR/Newton/WEP remains blocked by coupling target",
        ),
        (
            "VAL1489_9_rejections",
            len(rejections) >= 7 and all(row["claim_allowed"].lower() == "false" for row in rejections),
            "rejection ledger blocks claim promotion",
        ),
        (
            "VAL1489_10_decisions",
            any(row["decision_id"] == "DEC1489_3_next" for row in decisions),
            "decision ledger selects source coefficient target/invariant algebra next",
        ),
        (
            "VAL1489_11_next",
            len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1489_0_1490",
            "1490 handoff written",
        ),
        (
            "VAL1489_12_csv_parse",
            all(parse_csv(path) for path in generated_csvs()),
            "all generated 1489 CSVs parse cleanly",
        ),
        (
            "VAL1489_13_branch_copies",
            all(path.exists() for path in [QUAR_HOM, QUAR_COUNTER, QUAR_DELTA, BRANCH_HOM, BRANCH_COUNTER, BRANCH_DELTA]),
            "branch/quarantine nonclaim copies written",
        ),
    ]

    remove_pycache()
    checks.append(
        (
            "VAL1489_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent after run",
        )
    )
    modified_count = formalization_modified_count()
    checks.append(
        (
            "VAL1489_15_formalization_untouched",
            modified_count == 0,
            f"formalization modified-file count since start={modified_count}",
        )
    )
    claim_paths = generated_csvs() + [QUAR_HOM, QUAR_COUNTER, QUAR_DELTA, BRANCH_HOM, BRANCH_COUNTER, BRANCH_DELTA]
    claim_flags_false = True
    for path in claim_paths:
        for row in read_csv(path):
            for flag in ("valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if flag in row and row[flag].lower() != "false":
                    claim_flags_false = False
    checks.append(("VAL1489_16_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"))
    overall = all(result for _, result, _ in checks)
    checks.append(
        (
            "VAL1489_17_overall",
            overall,
            "1489 does not prove Hom exclusion, but creates the nonclaim delta_w bound interface and selects source-target/invariant algebra as next target",
        )
    )
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    hom = read_csv(HOM_THEOREM)
    targets = read_csv(COEFF_TARGETS)
    countermodels = read_csv(COUNTERMODELS)
    delta = read_csv(DELTA_W_INTERFACE)
    calibration = read_csv(COMMON_CALIBRATION)
    gates = read_csv(PROMOTION_GATES)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    validation = read_csv(VALIDATION)
    next_target = read_csv(NEXT_TARGET)

    lines = [
        "# 1489 - No Source Only Hom Exclusion Or Delta w Bound Interface",
        "",
        "## Verdict",
        "- The no-source-only `Hom` exclusion is exact as a conditional grammar theorem, but it is not parent-derived in the current corpus.",
        "- The decisive blockers are live: hidden invariant scalars, species/component labels, current normalization, marker/domain labels, and readout/source transfer can still feed `R_+` active-source prefactors.",
        "- 1489 therefore keeps `delta_w` nonclaim, builds the bound-interface skeleton, and points 1490 at source-coefficient target exclusion or hidden-invariant algebra triviality.",
        "",
        "## Hom Exclusion Attempt",
        markdown_table(hom, ["theorem_id", "current_status", "missing_for_claim"]),
        "",
        "## Typed Coefficient Targets",
        markdown_table(targets, ["target_id", "coefficient_target", "current_status", "effect_on_delta_w"]),
        "",
        "## Countermodel Ledger",
        markdown_table(countermodels, ["countermodel_id", "countermodel", "current_status", "required_to_close"]),
        "",
        "## Delta w Bound Interface",
        markdown_table(delta, ["interface_id", "arena", "symbol", "status", "numeric_bound", "missing_for_claim"]),
        "",
        "## Common Calibration Rule",
        markdown_table(calibration, ["rule_id", "object", "status", "missing_for_claim"]),
        "",
        "## Promotion Gates",
        markdown_table(gates, ["gate_id", "gate", "result", "reason"]),
        "",
        "## Local GR/Newton Status",
        markdown_table(local, ["status_id", "target", "current_status", "claim_effect"]),
        "",
        "## Rejection Ledger",
        markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]),
        "",
        "## Decision Ledger",
    ]
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['next_action']}.")
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
    write_csv(HOM_THEOREM, hom_theorem_rows())
    write_csv(COEFF_TARGETS, coefficient_target_rows())
    write_csv(COUNTERMODELS, countermodel_rows())
    write_csv(DELTA_W_INTERFACE, delta_w_interface_rows())
    write_csv(COMMON_CALIBRATION, common_calibration_rows())
    write_csv(PROMOTION_GATES, promotion_gate_rows())
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
