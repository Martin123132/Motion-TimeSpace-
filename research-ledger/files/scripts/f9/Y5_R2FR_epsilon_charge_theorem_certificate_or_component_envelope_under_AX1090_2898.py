from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2898-Y5-R2FR-epsilon-charge-theorem-certificate-or-component-envelope-under-AX1090.md"

SRC_2897_DOC = ROOT / "2897-Y5-R2FR-source-normalization-operator-first-fill-or-measured-GM-current-closure-under-AX1090.md"
SRC_2897_NEXT = RESIDUALS / "P8_Y5_R2FR_2897_NEXT_TARGET.csv"
SRC_2897_CLOSURE = RESIDUALS / "P8_Y5_R2FR_2897_MEASURED_GM_CLOSURE_ATTEMPT.csv"
SRC_2897_RESIDUALS = RESIDUALS / "P8_Y5_R2FR_2897_SOURCE_RESIDUAL_FIRST_FILL_ROWS.csv"
SRC_532_DOC = ROOT / "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md"
SRC_533_DOC = ROOT / "533-Y5-epsilon-charge-first-row-runner-or-source-current-theorem.md"
SRC_520_DOC = ROOT / "520-Y5-source-current-Ward-closure-or-bound-row.md"
SRC_522_DOC = ROOT / "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md"
SRC_499_DOC = ROOT / "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md"
SRC_505_DOC = ROOT / "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md"
SRC_SOURCE_SCORE = RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"
SRC_WARD_BRIDGE = RESIDUALS / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv"
SRC_WARD_OBSTRUCTION = RESIDUALS / "P8_Y5_WARD_TO_MASS_FLUX_OBSTRUCTION.csv"
SRC_MEFF_UPDATE = RESIDUALS / "P8_Y5_MEFF_FLUX_BOUND_UPDATE.csv"
SRC_PIM_INPUT = RESIDUALS / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"
SRC_EXTRA_MASS = RESIDUALS / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv"
SRC_PG_CONTRACT = RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"
SRC_SN_STACK = RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2898_SOURCE_REGISTER.csv",
    "denominator": RESIDUALS / "P8_Y5_R2FR_2898_DENOMINATOR_CONVENTION_GATE.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2898_EPSILON_CHARGE_THEOREM_AUDIT.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_2898_COMPONENT_ENVELOPE_ROWS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2898_EPSILON_CHARGE_EVALUATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2898_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2898_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2898_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2898_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2898_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2898_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "components_copy": BETA_DOCS / "RAB_EPSILON_CHARGE_COMPONENT_ENVELOPE_2898_NONCLAIM.csv",
    "evaluator_copy": BETA_DOCS / "RAB_EPSILON_CHARGE_EVALUATOR_2898_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2898_PiM_equality_commutator_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2898_0_2897_doc", SRC_2897_DOC, "epsilon_charge = (B_xi/G_eff - M_H[Pi_M J_H]) / M_H;NEXT2897_0_2898", "2897 selects epsilon_charge as first denominator lock"),
        ("SRC2898_1_2897_next", SRC_2897_NEXT, "NEXT2897_0_2898;component-envelope input row", "machine-readable 2898 handoff"),
        ("SRC2898_2_2897_closure", SRC_2897_CLOSURE, "GM2897_2_charge_current_equality;not_parent_derived", "latest measured-GM closure status"),
        ("SRC2898_3_2897_residuals", SRC_2897_RESIDUALS, "SRC2897_0_epsilon_charge;primary_next", "latest source residual first-fill queue"),
        ("SRC2898_4_532_doc", SRC_532_DOC, "epsilon_charge = (B_xi/G_eff - M_H[Pi_M J_H]) / M_H.;SC532_6_absolute_normalization", "source-current closure attempt and six required premises"),
        ("SRC2898_5_533_doc", SRC_533_DOC, "epsilon_charge = (B_xi/G_eff - M_H[Pi_M J_H]) / M_H[Pi_M J_H].;Pi_M equality/commutator is the next bottleneck", "older epsilon-charge runner and denominator-warning source"),
        ("SRC2898_6_520_doc", SRC_520_DOC, "d(Pi_M J_H)=0.;Ward conservation alone does not prove that", "Ward bridge and projected current obstruction"),
        ("SRC2898_7_522_doc", SRC_522_DOC, "Pi_M dJ_extra = 0.;not_derived_not_filled", "extra projected mass-channel obstruction"),
        ("SRC2898_8_499_doc", SRC_499_DOC, "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent.;I_parent_radial", "exact source identity split"),
        ("SRC2898_9_505_doc", SRC_505_DOC, "T505_conditional_Noether_mass_charge_closure;premises_not_yet_parent_derived", "conditional Noether closure route"),
        ("SRC2898_10_source_score", SRC_SOURCE_SCORE, "SRC523_0_charge_current_normalization;unfilled", "canonical source-normalization scorecard"),
        ("SRC2898_11_ward_bridge", SRC_WARD_BRIDGE, "WB520_6_conditional_closure_theorem;conditional_theorem_written_not_MTS_derived", "machine-readable Ward closure conditions"),
        ("SRC2898_12_ward_obstruction", SRC_WARD_OBSTRUCTION, "WO520_1_PiM_not_parent_owned;WO520_5_ad_hoc_multiplier", "machine-readable obstruction ledger"),
        ("SRC2898_13_meff_update", SRC_MEFF_UPDATE, "Y5B_1_Meff_conservation;Y5B_5_extra_mass_projection", "M_eff source-flux bound rows"),
        ("SRC2898_14_pim_input", SRC_PIM_INPUT, "PI521_1_commutator_profile;template_from_499_not_filled", "Pi_M equality and commutator input slots"),
        ("SRC2898_15_extra_mass", SRC_EXTRA_MASS, "EX522_0_boundary_improvement;EX522_8_absolute_calibration", "extra mass channelwise inputs"),
        ("SRC2898_16_pg_contract", SRC_PG_CONTRACT, "PG1_charge_equals_projected_Hilbert_source;PG3_EH_to_Poisson_coefficient", "charge-to-Poisson contract"),
        ("SRC2898_17_sn_stack", SRC_SN_STACK, "SN3_charge_equals_Hilbert_mass_current;SN4_closed_Meff_flux", "source-normalized Newton stack"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def denominator_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "DEN2898_0_detected_convention_split",
            "issue": "532/2897 write epsilon_charge with denominator M_H, while 533 writes denominator M_H[Pi_M J_H]",
            "risk": "a source-normalization residual can appear smaller/larger by convention unless the denominator is fixed before scoring",
            "canonical_resolution": "use M_ref := M_H[Pi_M J_H] for the evaluator, and allow M_H only when explicitly defined as the same projected Hilbert source mass",
            "status": "PASS_GUARD_CONVENTION_CANONICALIZED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "gate_id": "DEN2898_1_canonical_definition",
            "issue": "epsilon_charge must be dimensionless and relative to the parent projected source mass",
            "risk": "measured-GM absorption or source-unity shortcut could hide the very coupling residual being tested",
            "canonical_resolution": "epsilon_charge := (B_xi/G_eff - M_ref)/M_ref, M_ref := M_H[Pi_M J_H]",
            "status": "CANONICAL_FOR_2898_RUNNER_ONLY",
            "valid_for_claim": False,
        },
        {
            "gate_id": "DEN2898_2_equivalence_condition",
            "issue": "older M_H notation can be harmless only if M_H == M_H[Pi_M J_H] is parent-defined",
            "risk": "otherwise the notation assumes the charge-current equality it is supposed to prove",
            "canonical_resolution": "require a source path proving the equality before using denominator aliases as claim evidence",
            "status": "EQUIVALENCE_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
        },
    ]
    return [add_common(row) for row in rows]


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        ("ECT2898_0_observed_time_charge", "SC532_0_observed_time_charge", "source-backed observed-time Hamiltonian charge with normalized xi", "conditional_not_parent_derived", "H_xi=B_xi on shell with xi normalized in observed frame", "MISSING_PARENT_OBSERVED_TIME_CHARGE_CERTIFICATE"),
        ("ECT2898_1_Hilbert_source_current", "SC532_1_Hilbert_source_current", "same-frame Hilbert/source current defined before orbital fitting", "conditional_source_current_defined_not_mass_flux_closed", "J_H[tau]=T_m^{mu nu}[e_obs] tau_nu dSigma_mu", "NEEDS_MASS_FLUX_CLOSURE_NOT_JUST_WARD_CURRENT"),
        ("ECT2898_2_charge_current_variation_identity", "SC532_2_charge_current_variation_identity", "delta B_xi equals delta integral of Pi_M J_H and fixes absolute normalization", "missing_certificate", "B_xi/G_eff = M_H[Pi_M J_H]", "MISSING_VARIATION_IDENTITY_AND_ABSOLUTE_NORMALIZATION"),
        ("ECT2898_3_parent_owned_PiM", "SC532_3_parent_owned_PiM", "Pi_M is parent-owned/topological/Hamiltonian charge projector, not readout mask", "missing_certificate", "Pi_M J = ell_M(J) omega_M_top or equivalent parent charge projector", "MISSING_PARENT_PROJECTOR_SOURCE"),
        ("ECT2898_4_zero_projector_commutator", "SC532_4_zero_projector_commutator", "[d,Pi_M]J_H=0 or bounded commutator integral", "missing_certificate_or_bound", "int_A [d,Pi_M]J_H = 0 or below source-normalization lock", "MISSING_COMMUTATOR_ZERO_OR_PROFILE"),
        ("ECT2898_5_zero_extra_projection", "SC532_5_zero_extra_projection", "Pi_M dJ_extra=0 channelwise or all channels bounded", "missing_certificate_or_channel_bounds", "Pi_M dJ_extra_i=0 for each boundary/domain/bulk/nonEH/coupling/frame/projector/anomaly channel", "MISSING_CHANNELWISE_ZERO_OR_NUMERIC_BOUNDS"),
        ("ECT2898_6_absolute_normalization", "SC532_6_absolute_normalization", "G_eff normalization is constant/universal/source-blind before measured-GM fitting", "missing_certificate", "partial_{t,r,A,lambda,frame,domain} G_eff = 0", "MISSING_CONSTANT_COUPLING_CERTIFICATE"),
        ("ECT2898_7_verdict", "SC532_0..SC532_6", "epsilon_charge=0 theorem certificate", "FAIL_CURRENT_MTS_THEOREM_NOT_PROVED", "all six claim rungs are parent-signed and denominator convention is fixed", "THEOREM_ZERO_REFUSED"),
    ]
    return [
        add_common(
            {
                "certificate_id": certificate_id,
                "rung_id": rung_id,
                "required_certificate": required_certificate,
                "math_form": math_form,
                "current_status": current_status,
                "blocking_marker": blocking_marker,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for certificate_id, rung_id, required_certificate, current_status, math_form, blocking_marker in specs
    ]


def component_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ECE2898_0_epsilon_Hamiltonian_norm",
            "epsilon_Hamiltonian_norm",
            "(B_xi/G_eff - Q_parent)/M_ref",
            "Hamiltonian/boundary charge normalization error relative to parent source units",
            "SC532_0;SC532_2;PG0;PG1",
            "MISSING_BXI_OVER_GEFF_AND_Q_PARENT_SOURCE_ROWS",
            "dimensionless",
            "blocks epsilon_charge theorem and measured-GM denominator",
        ),
        (
            "ECE2898_1_epsilon_PiM_equality",
            "epsilon_PiM_equality",
            "(Q_parent - M_H[Pi_M J_H])/M_ref",
            "failure of the parent charge to equal the projected Hilbert source mass",
            "SC532_2;SC532_3;PI521_3;PG1",
            "MISSING_PARENT_PIM_EQUALITY_CERTIFICATE_OR_R_EQ_INTEGRAL",
            "dimensionless",
            "central bottleneck inside epsilon_charge",
        ),
        (
            "ECE2898_2_epsilon_commutator",
            "epsilon_commutator",
            "M_ref^-1 * int_A [d,Pi_M]J_H",
            "finite-shell product-rule leakage from the mass projector",
            "SC532_4;WB520_4;PI521_1;S499_0",
            "MISSING_COMMUTATOR_ZERO_THEOREM_OR_I_COMMUTATOR_PROFILE",
            "dimensionless_or_integral_units_divided_by_M_ref",
            "creates radial source hair/projector stress if open",
        ),
        (
            "ECE2898_3_epsilon_extra_projection",
            "epsilon_extra_projection",
            "M_ref^-1 * sum_i |int_A Pi_M dJ_extra_i|",
            "non-Hilbert sectors projected into the source charge",
            "SC532_5;EM522;EX522_0..EX522_8",
            "MISSING_CHANNELWISE_ZERO_OR_NUMERIC_EXTRA_PROJECTION_ROWS",
            "dimensionless",
            "prevents hidden boundary/domain/bulk/nonEH/coupling/source mass shifts",
        ),
        (
            "ECE2898_4_epsilon_boundary_anomaly",
            "epsilon_boundary_anomaly",
            "M_ref^-1 * (int_boundary Pi_M K_owner + int_A A_parent)",
            "boundary improvement, reference, multiplier, or anomaly offset in source charge",
            "SC532_5;WO520_4;WO520_5;D505_3;T499_0",
            "MISSING_BOUNDARY_NO_FLUX_OR_ANOMALY_ZERO_CERTIFICATE",
            "dimensionless",
            "rejects closure-only multiplier or finite boundary charge hiding",
        ),
        (
            "ECE2898_5_epsilon_Geff_abs",
            "epsilon_Geff_abs",
            "|delta ln G_eff| + derivative/range/source/frame/domain coupling terms",
            "absolute coupling normalization and drift inside B_xi/G_eff",
            "SC532_6;SRC523_5;EX522_4;EX522_8",
            "MISSING_CONSTANT_UNIVERSAL_COUPLING_THEOREM_OR_DERIVATIVE_ROWS",
            "dimensionless_or_derivative_units_declared_before_scoring",
            "keeps source-normalization from being absorbed into measured GM",
        ),
        (
            "ECE2898_6_total_no_cancellation",
            "epsilon_charge_abs_envelope",
            "sum_abs(ECE2898_0..ECE2898_5)",
            "strict no-cancellation envelope for the charge-current normalization row",
            "SRC523_0;532;533;2897",
            "NOT_COMPUTED_COMPONENTS_UNFILLED",
            "dimensionless",
            "claim only if every component is theorem-zero or sourced numeric below lock",
        ),
    ]
    return [
        add_common(
            {
                "component_id": component_id,
                "component_symbol": component_symbol,
                "formula": formula,
                "meaning": meaning,
                "mapped_source_rows": mapped_source_rows,
                "current_value": current_value,
                "units": units,
                "claim_effect": claim_effect,
                "normalization": "M_ref := M_H[Pi_M J_H]; no measured-GM absorption; no source-unity shortcut",
                "source_path": str(DOC),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for component_id, component_symbol, formula, meaning, mapped_source_rows, current_value, units, claim_effect in specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "eval_id": "EVAL2898_0_current_MTS_epsilon_charge",
                "mode": "strict_claim",
                "formula": "epsilon_charge_abs_envelope = sum_abs(epsilon_Hamiltonian_norm, epsilon_PiM_equality, epsilon_commutator, epsilon_extra_projection, epsilon_boundary_anomaly, epsilon_Geff_abs)",
                "required_inputs": "all six components numeric/source-backed or theorem-zero; fixed M_ref denominator",
                "computed_value": "NOT_EVALUATED",
                "bound_or_target": "below adopted source-normalization/local lock after units and normalization are source-backed",
                "result": "REFUSED_MISSING_COMPONENTS",
                "reason": "no theorem-zero certificate and no numeric component rows for current MTS",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "eval_id": "EVAL2898_1_GR_reference_control",
                "mode": "reference_control_not_evidence",
                "formula": "(1-1)/1",
                "required_inputs": "reference GR equality only",
                "computed_value": 0.0,
                "bound_or_target": "zero by reference definition",
                "result": "DENIED_AS_MTS_EVIDENCE",
                "reason": "reference GR does not source current MTS parent coefficients or Pi_M ownership",
                "runner_ready": False,
            }
        ),
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2898_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2898_1_denominator_convention", "epsilon_charge denominator is fixed before scoring", "PASS_GUARD", "M_ref canonical denominator selected and alias condition stated", False),
        ("GATE2898_2_theorem_zero", "epsilon_charge=0 is parent-signed", "FAIL", "SC532_0..SC532_6 are not all parent-signed", False),
        ("GATE2898_3_component_envelope", "six-piece absolute component envelope is staged", "PASS_NONCLAIM", "all six numerator channels plus total row are present but unfilled", False),
        ("GATE2898_4_numeric_evaluation", "current MTS epsilon_charge can be scored", "FAIL", "no numeric or theorem-zero components exist", False),
        ("GATE2898_5_no_GR_import", "GR reference zero is not used as MTS evidence", "PASS_GUARD", "reference control row is denied for claim credit", False),
        ("GATE2898_6_no_absorption", "measured-GM/source-unity absorption shortcut is forbidden", "PASS_GUARD", "denominator convention requires parent equality, not fitting", False),
        ("GATE2898_7_next_target", "next bottleneck selects Pi_M equality/commutator", "PASS_NONCLAIM", "2899 target selected", False),
        ("GATE2898_8_local_GR", "local Newton/GR branch closes", "FAIL_CLOSED", "epsilon_charge remains unfilled and downstream Poisson/Gauss/beta rows are held", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": gate_passed,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason, gate_passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2898_0_theorem_certificate",
                "status": "REFUSED_MISSING_CERTIFICATES",
                "required_components": "SC532_0..SC532_6 all parent-signed",
                "components_evaluable": 0,
                "reason": "observed-time charge, charge-current identity, Pi_M ownership, commutator silence, extra projection silence, and constant coupling are not all derived",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "runner_id": "RUN2898_1_component_envelope",
                "status": "STAGED_NONCLAIM_SCHEMA",
                "required_components": "six absolute components plus total no-cancellation row",
                "components_evaluable": 0,
                "reason": "schema is parseable but all live values are missing or theorem-unproved",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "runner_id": "RUN2898_2_next_PiM",
                "status": "NEXT_TARGET_SELECTED",
                "required_components": "epsilon_PiM_equality and epsilon_commutator theorem/numeric rows",
                "components_evaluable": 0,
                "reason": "533 and 2898 both identify Pi_M equality/commutator as the sharpest next bottleneck",
                "runner_ready": False,
            }
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2898_0_theorem", "REFUSE_EPSILON_CHARGE_ZERO_THEOREM_FOR_CURRENT_MTS", "the required SC532 certificates are not parent-signed", "do not promote measured GM/Newton/local GR"),
        ("DEC2898_1_denominator", "CANONICALIZE_DENOMINATOR_TO_M_REF", "532/2897 and 533 used different shorthand denominators; scoring needs one convention", "use M_ref=M_H[Pi_M J_H] until an alias theorem exists"),
        ("DEC2898_2_envelope", "STAGE_SIX_COMPONENT_ABSOLUTE_ENVELOPE", "a failed proof must become a finite testable object rather than an assertion", "fill or theorem-zero each component"),
        ("DEC2898_3_GR_reference", "DENY_REFERENCE_GR_ZERO_AS_EVIDENCE", "GR tells us the target shape, not the MTS coefficient or projector ownership", "keep reference controls nonclaim"),
        ("DEC2898_4_next", "SELECT_PIM_EQUALITY_COMMUTATOR_BOTTLENECK", "epsilon_PiM_equality and epsilon_commutator are the first two components likely to move the whole denominator lock", "build 2899 Pi_M parent-owned projector/equality or commutator envelope"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2898_0_2899",
                "status": "selected_primary",
                "target_doc": "2899-Y5-R2FR-PiM-parent-owned-projector-equality-or-commutator-envelope-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_PiM_parent_owned_projector_equality_or_commutator_envelope_under_AX1090_2899.py",
                "mission": "try to derive a parent-owned/topological Pi_M that equals the Hilbert source mass and has [d,Pi_M]J_H=0; if proof fails, stage strict epsilon_PiM_equality and epsilon_commutator rows with source paths, units, and no-cancellation guards",
                "forbidden": "readout-mask Pi_M; Hodge metric projector without stress row; closure multiplier; source-unity shortcut; cancellation; local-GR/Newton/beta claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2898_1_held_extra_projection",
                "status": "held_after_PiM",
                "target_doc": "2899b-Y5-R2FR-extra-projection-channelwise-zero-or-source-envelope.md",
                "target_script": "scripts/Y5_R2FR_extra_projection_channelwise_zero_or_source_envelope_2899b.py",
                "mission": "attack Pi_M dJ_extra channelwise after Pi_M ownership/commutator convention is fixed",
                "forbidden": "cancellation between channels; measured-GM absorption; local-GR claim",
                "selected": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("BR2898_0_components_copy", OUTPUTS["components"], BRANCH_OUTPUTS["components_copy"], "beta-source copy of epsilon_charge component envelope"),
        ("BR2898_1_evaluator_copy", OUTPUTS["evaluator"], BRANCH_OUTPUTS["evaluator_copy"], "beta-source copy of epsilon_charge evaluator"),
        ("BR2898_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_ts = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= start_ts:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    denominator_rows_ = all_rows["denominator"]
    theorem_rows_ = all_rows["theorem"]
    component_rows_ = all_rows["components"]
    evaluator_rows_ = all_rows["evaluator"]
    gate_rows_ = all_rows["gates"]
    next_rows_ = all_rows["next"]
    branch_rows = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]

    required_components = {
        "epsilon_Hamiltonian_norm",
        "epsilon_PiM_equality",
        "epsilon_commutator",
        "epsilon_extra_projection",
        "epsilon_boundary_anomaly",
        "epsilon_Geff_abs",
    }
    found_components = {row["component_symbol"] for row in component_rows_}

    checks = [
        ("VAL2898_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2898_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2898_2_denominator_guard", any(row["gate_id"] == "DEN2898_0_detected_convention_split" for row in denominator_rows_), "denominator convention split is registered"),
        ("VAL2898_3_theorem_refused", any(row["certificate_id"] == "ECT2898_7_verdict" and "FAIL" in row["current_status"] for row in theorem_rows_), "epsilon_charge theorem-zero is refused"),
        ("VAL2898_4_required_components_present", required_components <= found_components, "six epsilon_charge component rows are present"),
        ("VAL2898_5_components_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in component_rows_), "all component rows remain nonclaim"),
        ("VAL2898_6_evaluator_refuses_current_MTS", any(row["eval_id"] == "EVAL2898_0_current_MTS_epsilon_charge" and row["result"] == "REFUSED_MISSING_COMPONENTS" for row in evaluator_rows_), "current MTS evaluator refuses missing components"),
        ("VAL2898_7_GR_reference_denied", any(row["eval_id"] == "EVAL2898_1_GR_reference_control" and row["result"] == "DENIED_AS_MTS_EVIDENCE" for row in evaluator_rows_), "GR reference zero denied as MTS evidence"),
        ("VAL2898_8_absorption_guard", any(row["gate_id"] == "GATE2898_6_no_absorption" and row["result"] == "PASS_GUARD" for row in gate_rows_), "measured-GM absorption remains forbidden"),
        ("VAL2898_9_local_gr_fail_closed", any(row["gate_id"] == "GATE2898_8_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_), "local Newton/GR branch remains fail-closed"),
        ("VAL2898_10_next_target_2899", any(row["next_id"] == "NEXT2898_0_2899" and row["selected"] for row in next_rows_), "2899 PiM target selected"),
        ("VAL2898_11_branch_copies_exist", all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2898_12_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2898_13_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2898_OVERALL", overall, "2898 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2898 - Y5 R2FR Epsilon-Charge Theorem Certificate or Component Envelope Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-epsilon-charge-theorem-certificate-or-component-envelope-under-AX1090`",
        "Status: `Y5_R2FR_2898_epsilon_charge_zero_refused_denominator_canonicalized_component_envelope_staged_PiM_2899_next`",
        "Claim ceiling: `epsilon_charge_component_envelope_only_no_measured_GM_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "The 2898 proof attempt does not close `epsilon_charge=0` for current MTS. The useful result is sharper: the row is now a six-component no-cancellation envelope with a fixed denominator convention.",
        "",
        "Canonical scoring convention:",
        "",
        "`M_ref := M_H[Pi_M J_H]`",
        "",
        "`epsilon_charge := (B_xi/G_eff - M_ref)/M_ref`.",
        "",
        "Earlier notes used both `/M_H` and `/M_H[Pi_M J_H]`. That is harmless only if `M_H` is explicitly defined as the projected Hilbert source mass. Until that alias is parent-signed, the evaluator uses `M_ref` and refuses claim credit.",
        "",
        "The theorem route fails because observed-time charge, charge-current variation identity, parent-owned `Pi_M`, commutator silence, zero extra projection, and constant coupling are not all parent-signed. The fallback is not a defeat; it is the engineering shape we need: six named residuals that can each be proved zero or bounded.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Denominator Convention Gate",
        "",
        md_table(all_rows["denominator"], ["gate_id", "issue", "risk", "canonical_resolution", "status", "valid_for_claim"]),
        "",
        "## Theorem Certificate Audit",
        "",
        md_table(all_rows["theorem"], ["certificate_id", "rung_id", "required_certificate", "math_form", "current_status", "blocking_marker", "valid_for_claim"]),
        "",
        "## Component Envelope Rows",
        "",
        md_table(all_rows["components"], ["component_id", "component_symbol", "formula", "meaning", "current_value", "units", "claim_effect", "valid_for_claim"]),
        "",
        "## Epsilon-Charge Evaluator",
        "",
        md_table(all_rows["evaluator"], ["eval_id", "mode", "computed_value", "result", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        md_table(all_rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is the first real tightening of the coupling problem: the source-current row is no longer a single foggy missing variable. It has split into six places where the theory must pay its bill. The biggest next prize is `Pi_M`: if it becomes parent-owned/topological and commutator-silent, the denominator route gets much cleaner. If it does not, the commutator/equality rows become honest residuals rather than hidden failure modes.",
        "",
        "## Forbidden Claims From 2898",
        "",
        "- MTS has proved `epsilon_charge=0`.",
        "- MTS has a claim-valid numeric `epsilon_charge` row.",
        "- The GR reference equality proves the MTS source-current equality.",
        "- `/M_H` and `/M_H[Pi_M J_H]` are interchangeable before the parent alias is proved.",
        "- MTS has derived measured `GM`, source-normalized Newton, beta, PPN, R10, or local GR.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["denominator"] = denominator_rows()
    all_rows["theorem"] = theorem_rows()
    all_rows["components"] = component_rows()
    all_rows["evaluator"] = evaluator_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "denominator", "theorem", "components", "evaluator", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2898_OVERALL")
    print(f"2898 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
