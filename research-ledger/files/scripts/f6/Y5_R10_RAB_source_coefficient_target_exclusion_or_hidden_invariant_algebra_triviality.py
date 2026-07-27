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
DOC = ROOT / "1490-Y5-R10-RAB-source-coefficient-target-exclusion-or-hidden-invariant-algebra-triviality.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1489_next": OUT / "P8_Y5_R10_1489_NEXT_TARGET.csv",
    "1489_validation": OUT / "P8_Y5_BRR545_1489_VALIDATION.csv",
    "1489_hom": OUT / "P8_Y5_R10_1489_NO_SOURCE_ONLY_HOM_EXCLUSION_THEOREM_ATTEMPT.csv",
    "1489_targets": OUT / "P8_Y5_R10_1489_TYPED_COEFFICIENT_TARGET_AUDIT.csv",
    "1489_countermodels": OUT / "P8_Y5_R10_1489_HOM_COUNTERMODEL_LEDGER.csv",
    "1489_delta_interface": OUT / "P8_Y5_R10_1489_DELTA_W_BOUND_INTERFACE_NONCLAIM.csv",
    "1489_calibration": OUT / "P8_Y5_R10_1489_COMMON_CALIBRATION_RULE.csv",
    "1051_invariant_obstruction": OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "1051_no_mixed": OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1066_operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "1066_delta_import": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv",
    "1451_operator_grammar": OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv",
    "1451_slot_matrix": OUT / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv",
    "1451_bound_requirements": OUT / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv",
    "1479_hom_audit": OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv",
    "1488_delta_lock": OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
}

C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1490_SOURCE_REGISTER.csv"
TARGET_EXCLUSION = OUT / "P8_Y5_R10_1490_SOURCE_COEFFICIENT_TARGET_EXCLUSION_ATTEMPT.csv"
INVARIANT_TRIVIALITY = OUT / "P8_Y5_R10_1490_HIDDEN_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv"
COMMON_CALIBRATION = OUT / "P8_Y5_R10_1490_COMMON_CALIBRATION_EXCEPTION_GATE.csv"
SPECIES_READOUT = OUT / "P8_Y5_R10_1490_SPECIES_READOUT_DEPENDENCY_AUDIT.csv"
DELTA_REQUIREMENTS = OUT / "P8_Y5_R10_1490_DELTA_W_REAL_INPUT_REQUIREMENTS.csv"
PROMOTION_GATES = OUT / "P8_Y5_R10_1490_PROMOTION_GATES.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1490_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1490_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1490_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1490_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1490_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1490_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1490"
QUAR_TARGET = QUARANTINE / "SOURCE_COEFFICIENT_TARGET_EXCLUSION_ATTEMPT_NONCLAIM.csv"
QUAR_INV = QUARANTINE / "HIDDEN_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT_NONCLAIM.csv"
QUAR_DELTA = QUARANTINE / "DELTA_W_REAL_INPUT_REQUIREMENTS_NONCLAIM.csv"
BRANCH_TARGET = BRANCH_RESIDUALS / "source_coefficient_target_exclusion_attempt_nonclaim_1490.csv"
BRANCH_INV = BRANCH_RESIDUALS / "hidden_invariant_algebra_triviality_attempt_nonclaim_1490.csv"
BRANCH_DELTA = BRANCH_RESIDUALS / "delta_w_real_input_requirements_nonclaim_1490.csv"


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


def false_flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_rows() -> list[dict[str, Any]]:
    usage = {
        "1489_next": "authoritative 1490 handoff",
        "1489_validation": "previous validation state",
        "1489_hom": "Hom theorem failure state",
        "1489_targets": "typed coefficient target audit",
        "1489_countermodels": "live Hom countermodels",
        "1489_delta_interface": "delta_w nonclaim bound-interface skeleton",
        "1489_calibration": "common calibration guard",
        "1051_invariant_obstruction": "hidden invariant scalar obstruction",
        "1051_no_mixed": "no-mixed morphism lemma attempt",
        "1066_source_scalar": "source-scalar exclusion lemma",
        "1066_operator_domain": "operator-domain exclusion audit",
        "1066_delta_import": "older delta_w bound input scaffold",
        "1451_operator_grammar": "operator grammar theorem attempt",
        "1451_slot_matrix": "source-only slot reduction matrix",
        "1451_bound_requirements": "epsilon/delta_w bound requirements",
        "1479_hom_audit": "Hom channel audit",
        "1488_delta_lock": "delta_w symbolic residual lock",
    }
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1490_{index}_{key}",
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage[key],
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def target_exclusion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SCT1490_0_target",
            "source-only coefficient target exclusion",
            "R_+^active_source_prefactor is not an admissible target object of the parent coefficient functor, except one guarded common calibration mode",
            "CTA1489_6;ODR1066_4;OG1451_1",
            "TARGET_EXACT",
            "derive parent coefficient functor and target category from MTS primitives",
            "This would close the hidden-invariant route without needing to list every invariant.",
        ),
        (
            "SCT1490_1_positive_rule",
            "allowed visible coefficient ring",
            "Coeff(O_vis) subset Alg[q_loc, theta_rep, Level_EM] for visible/readout operators",
            "ODR1066_0;CTA1489_0..3",
            "POWERFUL_IF_SIGNED",
            "the same rule remains a contract rather than a theorem",
            "Good skeleton; not enough to promote.",
        ),
        (
            "SCT1490_2_source_target_gap",
            "active source target is continuous",
            "if R_+^source is legal, any surviving scalar can feed w=w0+epsilon I",
            "ODR1066_1;HET1489_3",
            "OBSTRUCTION_SURVIVES",
            "exclude R_+^source as a target or trivialise hidden invariant algebra",
            "This is the central fork.",
        ),
        (
            "SCT1490_3_action_scale_gap",
            "action-scale target",
            "w_A S_A is a variational/action-scale coefficient, not just a measured matter parameter",
            "ODR1066_3;SSE1066_4",
            "REQUIRES_PARENT_MEASURE_OWNER",
            "common measure/current/action-scale normalization must be parent-owned",
            "No theorem-zero coupling without this.",
        ),
        (
            "SCT1490_4_readout_gap",
            "readout target reentry",
            "post-variation readout/source-worldtube maps can create effective source coefficients",
            "SSE1066_2;HOM1479_5;HET1489_5",
            "READOUT_CLOSURE_UNSIGNED",
            "derive readout closure or keep readout delta_w residual",
            "Stops detector modelling from becoming a hidden axiom.",
        ),
        (
            "SCT1490_5_verdict",
            "target exclusion verdict",
            "source-only R_+ target exclusion is not derived in current corpus",
            "1490 synthesis",
            "NOT_DERIVED_BOUND_INPUT_ROUTE_SELECTED",
            "move to real source-backed delta_w bound inputs unless a deeper parent grammar source appears",
            "No universal-coupling claim is allowed from target exclusion.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim_piece": claim_piece,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "route_note": route_note,
            **false_flags(),
        }
        for attempt_id, claim_piece, formal_statement, source_anchor, current_status, missing_for_claim, route_note in rows
    ]


def invariant_triviality_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HIA1490_0_target",
            "hidden invariant algebra triviality",
            "O(C_hid)^inv = R for source-coefficient purposes",
            "NMM1051_1;ISO1051_0",
            "TARGET_EXACT",
            "prove all local hidden scalars are gauge/quotient/boundary-silent or non-admissible",
            "This would kill hidden-to-source coefficients directly.",
        ),
        (
            "HIA1490_1_conditional_theorem",
            "trivial algebra implies no hidden coefficient",
            "if O(C_hid)^inv=R, any natural scalar coefficient C_hid->R is constant",
            "NMM1051_1",
            "EXACT_CONDITIONAL_THEOREM",
            "current corpus has not proved invariant algebra triviality",
            "The mathematics is fine; the premise is the problem.",
        ),
        (
            "HIA1490_2_scalar_counterexample",
            "generic hidden scalar",
            "I_hid with dI != 0 permits c_I=c0+epsilon I_hid",
            "NMM1051_2;ISO1051_0",
            "COUNTEREXAMPLE_PROVED_IF_I_SURVIVES",
            "forbid the target or prove no such I survives",
            "This is live and blocks theorem-zero.",
        ),
        (
            "HIA1490_3_Xhat_value",
            "Xhat amplitude invariant",
            "f_X(Xhat) can feed source/EM/mass/clock coefficients if product functor is unsigned",
            "ISO1051_1",
            "LIVE_UNLESS_PRODUCT_FUNCTOR_SIGNED",
            "exact shift/sequester/product functor or Xhat=0 theorem",
            "Still live as an invariant candidate.",
        ),
        (
            "HIA1490_4_gradient_norm",
            "gradient/profile norm invariant",
            "f((nabla Xhat)^2) can feed coefficient channels with even parity",
            "ISO1051_2",
            "EVEN_PARITY_SURVIVOR",
            "positive no-hair/profile-zero theorem or product functor",
            "Evenness means sign tricks do not save us.",
        ),
        (
            "HIA1490_5_marker_domain",
            "domain/material marker invariant",
            "theta_A(marker) or kappa_A(marker) can feed source/test couplings",
            "ISO1051_3;SM1451_3",
            "LIVE_LABEL_OBSTRUCTION",
            "source-label forgetting and no-marker functor theorem",
            "Composition labels can sneak back in by another name.",
        ),
        (
            "HIA1490_6_verdict",
            "hidden invariant algebra verdict",
            "hidden invariant algebra triviality is not proved",
            "1490 synthesis",
            "NOT_TRIVIALITY_PROVED",
            "keep delta_w bound interface and require real source-backed rows",
            "This is why the empirical fallback is now the honest route.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim_piece": claim_piece,
            "formal_statement": formal_statement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "route_note": route_note,
            **false_flags(),
        }
        for attempt_id, claim_piece, formal_statement, source_anchor, current_status, missing_for_claim, route_note in rows
    ]


def common_calibration_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CCG1490_0_exception",
            "common calibration exception",
            "one universal w_star/kappa_univ common mode may be allowed",
            "ALLOWED_ONLY_IF_SILENT",
            "prove no species/time/range/frame/source-body dependence",
        ),
        (
            "CCG1490_1_delta_definition",
            "delta_w_A definition",
            "delta_w_A := w_A - w_star is the WEP-sensitive residual",
            "DEFINITION_LOCKED",
            "component/source basis needed before numerical scoring",
        ),
        (
            "CCG1490_2_absorption_guard",
            "absorb into G_N/GM",
            "w_star can be absorbed into measured G only after readout/source convention is fixed",
            "GUARDED_NOT_CLAIMED",
            "source/readout transfer and orbital/GM convention remain needed",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "rule": rule,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, rule, current_status, missing_for_claim in rows
    ]


def species_readout_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SRD1490_0_species_components",
            "species/component labels",
            "Nat(C_disconnected,R_+) admits independent constants",
            "ODR1066_2;HCM1489_0",
            "OPEN",
            "connected common action-measure owner and label forgetting before coupling",
        ),
        (
            "SRD1490_1_current_norm",
            "current normalization",
            "J_A -> c_A J_A or beta_source,A can mimic source weights",
            "HCM1489_3;SM1451_2;SM1451_4",
            "OPEN",
            "current owner and Hilbert/non-Hilbert split",
        ),
        (
            "SRD1490_2_marker_spurion",
            "marker/domain/boundary labels",
            "material/domain/boundary/readout marker prefactors can undo label forgetting",
            "HCM1489_2;SM1451_3",
            "OPEN",
            "no-marker/no-spurion closure and boundary/domain silence",
        ),
        (
            "SRD1490_3_readout_transfer",
            "readout/source-worldtube transfer",
            "post-variation source selector can create active source weights",
            "HCM1489_4;HOM1479_5",
            "OPEN",
            "variation-before-readout and official/source-worldtube transfer",
        ),
        (
            "SRD1490_4_verdict",
            "species/readout dependency verdict",
            "source-label dependencies remain live and must be either derived away or bounded",
            "1490 synthesis",
            "OPEN_DEPENDENCIES_RETAINED",
            "move to real source-backed delta_w bound input pack",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "dependency": dependency,
            "formal_risk": formal_risk,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "required_to_close": required_to_close,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, dependency, formal_risk, source_anchor, current_status, required_to_close in rows
    ]


def delta_requirements_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DWR1490_0_core",
            "core_delta_w_model",
            "eta_AB ~= sum_i DeltaQ_i(AB) delta_w_i tau_i",
            "dimensionless",
            "material/source charge basis; tau_i; readout transfer; experimental bound",
            "MISSING_SOURCE_BACKED_INPUTS",
        ),
        (
            "DWR1490_1_MICROSCOPE",
            "MICROSCOPE_TiPt",
            "delta_w_TiPt source-weight contrast",
            "dimensionless",
            "official Ti/Pt/PtRh/TA6V material vector; Earth/source kernel; accepted readout; tau_eff",
            "MISSING_SOURCE_BACKED_INPUTS",
        ),
        (
            "DWR1490_2_EotWash",
            "EotWash_WEP",
            "delta_w_AB torsion-balance material/source contrast",
            "dimensionless",
            "experiment composition vectors; source attractor vector; range/profile transfer; published eta bounds",
            "MISSING_SOURCE_BACKED_INPUTS",
        ),
        (
            "DWR1490_3_R10",
            "R10_short_range",
            "delta_w_R10 contribution to alpha(lambda)",
            "dimensionless",
            "real alpha(lambda) bound curve; source/test composition; lambda/range map; parent profile",
            "MISSING_SOURCE_BACKED_INPUTS",
        ),
        (
            "DWR1490_4_clock",
            "clock_alpha_mass",
            "delta_w_clock / constant-leakage product",
            "dimensionless",
            "clock sensitivity matrix; tau_clock; alpha/mass split; source-coefficient target map",
            "MISSING_SOURCE_BACKED_INPUTS",
        ),
        (
            "DWR1490_5_orbital",
            "orbital_GM",
            "active source calibration residual",
            "dimensionless",
            "body composition model; measured GM convention; orbital residual projection",
            "MISSING_SOURCE_BACKED_INPUTS",
        ),
        (
            "DWR1490_6_claim_gate",
            "claim_gate",
            "no delta_w row can claim until every numeric value has source path, units, and arena projection",
            "dimensionless",
            "source-backed rows plus runner acceptance gates",
            "NONCLAIM_REQUIREMENTS_ONLY",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "arena": arena,
            "quantity": quantity,
            "units": units,
            "required_inputs": required_inputs,
            "current_status": current_status,
            "numeric_value": "MISSING_SOURCE_BACKED_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for requirement_id, arena, quantity, units, required_inputs, current_status in rows
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PG1490_0_target_exclusion", "source-only R_+ target absent", "FAIL", "target exclusion remains a contract not a theorem"),
        ("PG1490_1_invariant_triviality", "hidden invariant algebra trivial", "FAIL", "generic/Xhat/gradient/marker invariants remain live"),
        ("PG1490_2_Hom_zero", "no-source-only Hom theorem-zero", "FAIL", "either target exclusion or invariant triviality would be needed"),
        ("PG1490_3_delta_w_numeric", "delta_w numeric bound", "FAIL_NONCLAIM_REQUIREMENTS_ONLY", "real source-backed inputs are missing"),
        ("PG1490_4_Cparent", "C_parent theorem-zero import", "FAIL_FORBIDDEN", "universal coupling still not derived"),
        ("PG1490_5_local_GR", "local GR/Newton/WEP claim", "FAIL", "coupling/source-weight branch remains open"),
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
            "refusal_id": "CPR1490_0_live_import",
            "forbidden_object": rel(C_PARENT_IMPORT),
            "exists": C_PARENT_IMPORT.exists(),
            "current_status": "ABSENT_OK" if not C_PARENT_IMPORT.exists() else "ERROR_LIVE_IMPORT_PRESENT",
            "reason": "source coefficient target exclusion and hidden invariant triviality both remain unsigned",
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
            "LRS1490_0_universal_coupling",
            "universal matter coupling",
            "no admissible relative active-source coefficient target",
            "NOT_DERIVED",
            "source-only target and invariant algebra routes both unsigned",
            "universal coupling not claimable",
        ),
        (
            "LRS1490_1_WEP",
            "WEP/source universality",
            "delta_w_A=0 modulo common calibration",
            "BLOCKED_MOVE_TO_BOUNDS",
            "delta_w must be bounded unless a new derivation source appears",
            "WEP theorem-zero blocked",
        ),
        (
            "LRS1490_2_Newton",
            "Newtonian source",
            "unique active Hilbert source without relative weights",
            "CONDITIONAL_ONLY",
            "species/readout/source-weight channels remain live",
            "Newton reduction still conditional",
        ),
        (
            "LRS1490_3_GR",
            "local GR matter limit",
            "universal observed metric/coframe coupling",
            "CONDITIONAL_ONLY",
            "ordinary matter coupling owner remains unsigned",
            "GR reduction not yet claimable",
        ),
        (
            "LRS1490_4_verdict",
            "local GR/Newton status",
            "derivation path did not close; empirical residual branch is now the honest next move",
            "NOT_CLOSED_NEXT_REAL_DELTA_W_INPUTS",
            "source-backed delta_w bound input pack",
            "no local-GR/Newton/WEP/R10 claim from 1490",
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
            **false_flags(),
        }
        for status_id, target, required_statement, current_status, missing_for_claim, claim_effect in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1490_0_target", "SOURCE_COEFFICIENT_TARGET_NOT_EXCLUDED", "R_+ active-source coefficient target is not parent-forbidden"),
        ("REJ1490_1_invariant", "HIDDEN_INVARIANT_ALGEBRA_NOT_TRIVIAL", "generic/Xhat/gradient/marker invariant channels remain live"),
        ("REJ1490_2_action_scale", "PARENT_ACTION_SCALE_OWNER_MISSING", "w_A S_A action-scale target not ruled out"),
        ("REJ1490_3_readout", "READOUT_REENTRY_UNSIGNED", "post-variation source/readout transfer can reintroduce weights"),
        ("REJ1490_4_species", "SPECIES_COMPONENT_DEPENDENCIES_OPEN", "label-visible components can retain independent constants"),
        ("REJ1490_5_delta", "DELTA_W_REAL_INPUTS_MISSING", "bound branch lacks source-backed numeric inputs"),
        ("REJ1490_6_Cparent", "C_PARENT_IMPORT_FORBIDDEN", "universal coupling owner not signed"),
        ("REJ1490_7_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton/R10 claim allowed"),
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
            "DEC1490_0_no_target_promotion",
            "do not promote source target exclusion",
            "the coefficient target category remains a contract rather than derived parent grammar",
            "retain target exclusion as a theorem candidate only",
        ),
        (
            "DEC1490_1_no_invariant_triviality",
            "do not claim hidden invariant algebra triviality",
            "multiple explicit invariant countermodels survive",
            "retain hidden-invariant delta_w channels",
        ),
        (
            "DEC1490_2_move_to_bounds",
            "move to real source-backed delta_w inputs",
            "derivation-first route has localized the missing theorem without closing it",
            "build WEP/R10/clock/orbital input pack before any score",
        ),
        (
            "DEC1490_3_no_public_claim",
            "keep local-GR/Newton/WEP private and nonclaim",
            "universal coupling is not yet derived",
            "no C_parent import or claim promotion",
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
            "next_id": "NEXT1490_0_1491",
            "next_target": "1491-Y5-R10-RAB-real-delta-w-bound-input-pack-WEP-R10-clock-orbital.md",
            "script": "scripts/Y5_R10_RAB_real_delta_w_bound_input_pack_WEP_R10_clock_orbital.py",
            "objective": "build source-backed nonclaim delta_w bound inputs for WEP/MICROSCOPE, EotWash, R10, clocks, and orbital/GM channels before any scoring or claim promotion",
            "include": "material/source charge vectors; tau/projection placeholders; official bound paths; units; missing-input gates; common calibration guard",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; theorem-zero coupling claim; numeric WEP claim without source-backed inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        TARGET_EXCLUSION,
        INVARIANT_TRIVIALITY,
        COMMON_CALIBRATION,
        SPECIES_READOUT,
        DELTA_REQUIREMENTS,
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
    shutil.copyfile(TARGET_EXCLUSION, QUAR_TARGET)
    shutil.copyfile(INVARIANT_TRIVIALITY, QUAR_INV)
    shutil.copyfile(DELTA_REQUIREMENTS, QUAR_DELTA)
    shutil.copyfile(TARGET_EXCLUSION, BRANCH_TARGET)
    shutil.copyfile(INVARIANT_TRIVIALITY, BRANCH_INV)
    shutil.copyfile(DELTA_REQUIREMENTS, BRANCH_DELTA)


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
    target = read_csv(TARGET_EXCLUSION)
    invariant = read_csv(INVARIANT_TRIVIALITY)
    calibration = read_csv(COMMON_CALIBRATION)
    species = read_csv(SPECIES_READOUT)
    delta = read_csv(DELTA_REQUIREMENTS)
    gates = read_csv(PROMOTION_GATES)
    c_parent = read_csv(C_PARENT_REFUSAL)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    next_target = read_csv(NEXT_TARGET)

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1490_0_sources",
            all(row["exists_or_resolved"].lower() == "true" for row in source_register),
            "all cited local source paths exist",
        ),
        (
            "VAL1490_1_target_not_derived",
            any(row["current_status"] == "NOT_DERIVED_BOUND_INPUT_ROUTE_SELECTED" for row in target),
            "source coefficient target exclusion is not derived",
        ),
        (
            "VAL1490_2_invariant_not_trivial",
            any(row["current_status"] == "NOT_TRIVIALITY_PROVED" for row in invariant),
            "hidden invariant algebra triviality is not proved",
        ),
        (
            "VAL1490_3_common_calibration_guarded",
            any(row["current_status"] == "GUARDED_NOT_CLAIMED" for row in calibration),
            "common calibration exception is guarded",
        ),
        (
            "VAL1490_4_species_readout_open",
            any(row["current_status"] == "OPEN_DEPENDENCIES_RETAINED" for row in species),
            "species/readout dependencies remain open",
        ),
        (
            "VAL1490_5_delta_requirements_nonclaim",
            all(row["numeric_value"] == "MISSING_SOURCE_BACKED_VALUE" and row["claim_allowed"].lower() == "false" for row in delta),
            "delta_w real input rows remain source-requirement nonclaim rows",
        ),
        (
            "VAL1490_6_promotion_gates_fail",
            all(row["claim_allowed"].lower() == "false" for row in gates),
            "all promotion gates block claims",
        ),
        (
            "VAL1490_7_no_Cparent_import",
            (not C_PARENT_IMPORT.exists()) and all(row["claim_allowed"].lower() == "false" for row in c_parent),
            "live C_parent import remains absent and refused",
        ),
        (
            "VAL1490_8_local_blocked",
            any(row["current_status"] == "NOT_CLOSED_NEXT_REAL_DELTA_W_INPUTS" for row in local),
            "local GR/Newton/WEP remains blocked and moves to real delta_w inputs",
        ),
        (
            "VAL1490_9_rejections",
            len(rejections) >= 8 and all(row["claim_allowed"].lower() == "false" for row in rejections),
            "rejection ledger blocks claim promotion",
        ),
        (
            "VAL1490_10_decisions",
            any(row["decision_id"] == "DEC1490_2_move_to_bounds" for row in decisions),
            "decision ledger selects real source-backed delta_w inputs next",
        ),
        (
            "VAL1490_11_next",
            len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1490_0_1491",
            "1491 handoff written",
        ),
        (
            "VAL1490_12_csv_parse",
            all(parse_csv(path) for path in generated_csvs()),
            "all generated 1490 CSVs parse cleanly",
        ),
        (
            "VAL1490_13_branch_copies",
            all(path.exists() for path in [QUAR_TARGET, QUAR_INV, QUAR_DELTA, BRANCH_TARGET, BRANCH_INV, BRANCH_DELTA]),
            "branch/quarantine nonclaim copies written",
        ),
    ]
    remove_pycache()
    checks.append(
        (
            "VAL1490_14_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent after run",
        )
    )
    modified_count = formalization_modified_count()
    checks.append(
        (
            "VAL1490_15_formalization_untouched",
            modified_count == 0,
            f"formalization modified-file count since start={modified_count}",
        )
    )
    claim_paths = generated_csvs() + [QUAR_TARGET, QUAR_INV, QUAR_DELTA, BRANCH_TARGET, BRANCH_INV, BRANCH_DELTA]
    claim_flags_false = True
    for path in claim_paths:
        for row in read_csv(path):
            for flag in ("valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if flag in row and row[flag].lower() != "false":
                    claim_flags_false = False
    checks.append(("VAL1490_16_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"))
    overall = all(result for _, result, _ in checks)
    checks.append(
        (
            "VAL1490_17_overall",
            overall,
            "1490 rejects theorem-zero coupling promotion and hands off to real source-backed delta_w bound inputs",
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
    target = read_csv(TARGET_EXCLUSION)
    invariant = read_csv(INVARIANT_TRIVIALITY)
    calibration = read_csv(COMMON_CALIBRATION)
    species = read_csv(SPECIES_READOUT)
    delta = read_csv(DELTA_REQUIREMENTS)
    gates = read_csv(PROMOTION_GATES)
    local = read_csv(LOCAL_STATUS)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION_LEDGER)
    validation = read_csv(VALIDATION)
    next_target = read_csv(NEXT_TARGET)

    lines = [
        "# 1490 - Source Coefficient Target Exclusion Or Hidden Invariant Algebra Triviality",
        "",
        "## Verdict",
        "- The source-only `R_+` coefficient target is not parent-excluded in the current corpus.",
        "- Hidden invariant algebra triviality is also not proved: generic hidden scalars, `Xhat`, gradient norms, and marker/domain labels remain live counterchannels.",
        "- The derivation-first coupling route therefore remains blocked, and the honest next move is a real source-backed `delta_w` bound input pack.",
        "",
        "## Source Coefficient Target Exclusion",
        markdown_table(target, ["attempt_id", "current_status", "missing_for_claim"]),
        "",
        "## Hidden Invariant Algebra",
        markdown_table(invariant, ["attempt_id", "current_status", "missing_for_claim"]),
        "",
        "## Common Calibration Exception",
        markdown_table(calibration, ["gate_id", "current_status", "missing_for_claim"]),
        "",
        "## Species And Readout Dependencies",
        markdown_table(species, ["audit_id", "dependency", "current_status", "required_to_close"]),
        "",
        "## Delta w Real Input Requirements",
        markdown_table(delta, ["requirement_id", "arena", "current_status", "numeric_value", "source_path"]),
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
    write_csv(TARGET_EXCLUSION, target_exclusion_rows())
    write_csv(INVARIANT_TRIVIALITY, invariant_triviality_rows())
    write_csv(COMMON_CALIBRATION, common_calibration_rows())
    write_csv(SPECIES_READOUT, species_readout_rows())
    write_csv(DELTA_REQUIREMENTS, delta_requirements_rows())
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
