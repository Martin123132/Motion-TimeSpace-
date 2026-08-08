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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2899-Y5-R2FR-PiM-parent-owned-projector-equality-or-commutator-envelope-under-AX1090.md"

SRC_2898_DOC = ROOT / "2898-Y5-R2FR-epsilon-charge-theorem-certificate-or-component-envelope-under-AX1090.md"
SRC_2898_NEXT = RESIDUALS / "P8_Y5_R2FR_2898_NEXT_TARGET.csv"
SRC_2898_COMPONENTS = RESIDUALS / "P8_Y5_R2FR_2898_COMPONENT_ENVELOPE_ROWS.csv"
SRC_534_DOC = ROOT / "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md"
SRC_2584_DOC = ROOT / "2584-Y5-R2FR-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md"
SRC_2585_DOC = ROOT / "2585-Y5-R2FR-PiM-chainmap-commutator-zero-or-Icommutator-bound-fill.md"
SRC_455_DOC = ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md"
SRC_450_DOC = ROOT / "450-Hilbert-source-to-measured-monopole-calibration-gate.md"
SRC_PIM_RADIAL = RESIDUALS / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"
SRC_2584_AUDIT = RESIDUALS / "P8_Y5_PIM_JH_FLUX_2584_CLOSURE_DERIVATION_AUDIT.csv"
SRC_2584_VECTOR = RESIDUALS / "P8_Y5_PIM_JH_FLUX_2584_EXACT_OBSTRUCTION_VECTOR.csv"
SRC_2585_AUDIT = RESIDUALS / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv"
SRC_2585_BOUND = RESIDUALS / "P8_Y5_PIM_CHAINMAP_2585_ICOMMUTATOR_BOUND_ROWS.csv"
SRC_WARD_BRIDGE = RESIDUALS / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv"
SRC_WARD_OBSTRUCTION = RESIDUALS / "P8_Y5_WARD_TO_MASS_FLUX_OBSTRUCTION.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2899_SOURCE_REGISTER.csv",
    "route": RESIDUALS / "P8_Y5_R2FR_2899_PIM_ROUTE_GATE.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2899_PIM_THEOREM_AUDIT.csv",
    "rows": RESIDUALS / "P8_Y5_R2FR_2899_PIM_EQUALITY_COMMUTATOR_ROWS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2899_PIM_EVALUATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2899_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2899_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2899_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2899_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2899_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2899_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "rows_copy": LOCAL_BOUNDS / "PiM_equality_commutator_rows_2899_NONCLAIM.csv",
    "evaluator_copy": BETA_DOCS / "RAB_PIM_EQUALITY_COMMUTATOR_EVALUATOR_2899_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2899_source_worldtube_current_complex_NEXT.csv",
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
        ("SRC2899_0_2898_doc", SRC_2898_DOC, "NEXT2898_0_2899;M_ref := M_H[Pi_M J_H]", "2898 selects PiM equality/commutator as first denominator sublock"),
        ("SRC2899_1_2898_next", SRC_2898_NEXT, "NEXT2898_0_2899;parent-owned/topological Pi_M", "machine-readable 2899 handoff"),
        ("SRC2899_2_2898_components", SRC_2898_COMPONENTS, "ECE2898_1_epsilon_PiM_equality;ECE2898_2_epsilon_commutator", "epsilon_charge component rows to fill"),
        ("SRC2899_3_534_doc", SRC_534_DOC, "Pi_M J_H = J_M_top + dB_zero;Current MTS does not yet prove this", "older PiM equality/commutator certificate"),
        ("SRC2899_4_2584_doc", SRC_2584_DOC, "Omega_GM = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent;PIM_JH_FLUX_CLOSURE_NOT_DERIVED_CURRENT_CORPUS", "current R2FR PiM flux obstruction"),
        ("SRC2899_5_2585_doc", SRC_2585_DOC, "FIXED_CHAINMAP_ZERO_IS_MATHEMATICALLY_CLEAN;CURRENT_MTS_DOES_NOT_PROVE_CHAINMAP_ANTECEDENTS", "current R2FR chainmap/commutator audit"),
        ("SRC2899_6_455_doc", SRC_455_DOC, "topological_projector_not_mass_current;mass_flux_closure_parent_derived", "Ward/topological route limits"),
        ("SRC2899_7_450_doc", SRC_450_DOC, "HM1_parent_defined_mass_projector;measured_GM_parent_derived", "Hilbert-source to measured-monopole calibration gate"),
        ("SRC2899_8_pim_radial", SRC_PIM_RADIAL, "PI521_1_commutator_profile;PI521_3_topological_equality_residual", "PiM equality/commutator input slots"),
        ("SRC2899_9_2584_audit", SRC_2584_AUDIT, "FCA2584_4_chainmap_commutator_zero;PIM_JH_FLUX_CLOSURE_NOT_DERIVED_CURRENT_CORPUS", "R2FR closure audit rows"),
        ("SRC2899_10_2584_vector", SRC_2584_VECTOR, "OBS2584_1_PiM_chainmap_commutator;OBS2584_3_topological_equality_residual", "R2FR exact obstruction vector"),
        ("SRC2899_11_2585_audit", SRC_2585_AUDIT, "CMA2585_1_fixed_chainmap_theorem;PIM_CHAINMAP_COMMUTATOR_ZERO_NOT_DERIVED_CURRENT_CORPUS", "R2FR chainmap theorem audit"),
        ("SRC2899_12_2585_bound", SRC_2585_BOUND, "IC2585_0_I_commutator_abs;IC2585_4_R_eq_guard", "R2FR I_commutator/R_eq nonclaim rows"),
        ("SRC2899_13_ward_bridge", SRC_WARD_BRIDGE, "WB520_4_exact_product_obstruction;WB520_6_conditional_closure_theorem", "Ward bridge product-rule source"),
        ("SRC2899_14_ward_obstruction", SRC_WARD_OBSTRUCTION, "WO520_1_PiM_not_parent_owned;WO520_2_projector_commutator", "Ward-to-mass obstruction ledger"),
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


def route_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROUTE2899_0_fixed_chainmap", "preferred_conditional_route", "Pi_M is a parent-selected fixed chain map on the physical compact-exterior Hilbert-current complex", "would give [d,Pi_M]J_H=0", "conditional_clean_not_parent_signed", "keep, but do not claim"),
        ("ROUTE2899_1_topological_same_object", "required_guard", "Pi_M J_H = J_M_top + dB_zero with zero compact boundary flux and common M_ref", "prevents closed wrong conserved object", "R_eq_and_B_zero_unfilled", "attack source-worldtube/current-complex antecedent"),
        ("ROUTE2899_2_Hodge_metric_projector", "danger_route", "Pi_M depends on metric/domain/Hodge data", "creates delta_g Pi_M stress and commutator leakage", "retained_residual_unless_stress_mapped", "forbid claim without stress row"),
        ("ROUTE2899_3_readout_mask", "forbidden_route", "Pi_M chosen after orbital GM or PPN fitting", "assumes the source normalization it should derive", "forbidden_as_derivation", "no claim credit"),
        ("ROUTE2899_4_closure_multiplier", "forbidden_route", "lambda_M imposes d(Pi_M J_H)=0 without independent gauge/topological/Ward origin", "closure axiom masquerades as derivation", "forbidden_as_derivation", "only allowed as explicit closure"),
        ("ROUTE2899_5_no_repeat_algebra", "work_policy", "product rule and fixed-chainmap conditional theorem are already clean", "future work should not circle this algebra unless new parent action evidence appears", "pass_policy", "move to parent-owned current-complex antecedents"),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route_type": route_type,
                "statement": statement,
                "effect": effect,
                "current_status": current_status,
                "next_action": next_action,
            }
        )
        for route_id, route_type, statement, effect, current_status, next_action in specs
    ]


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        ("PIM2899_0_parent_selector", "mass/source selector exists before readout", "chi_M or equivalent parent mass-channel selector independent of orbital GM, PPN score, or source normalization", "NOT_PARENT_SIGNED", "Pi_M may otherwise be a post-readout mask"),
        ("PIM2899_1_fixed_domain_worldtube", "source worldtube, compact exterior, linking surfaces, and orientation are fixed before readout", "W_source, A_ext, S_link, orientation fixed and not metric/fitting dependent", "NOT_PARENT_SIGNED", "domain motion contributes D_D Pi_M and source-hair leakage"),
        ("PIM2899_2_physical_current_complex", "observed Hilbert current lives in the same parent complex used by Pi_M", "J_H[e_obs,tau] in C_H(A_ext), with clocks/rods/orbits and source variation using the same current", "NOT_PARENT_SIGNED", "Pi_M can act on a surrogate current rather than measured source mass"),
        ("PIM2899_3_fixed_chainmap_commutator", "fixed chainmap theorem gives commutator zero if antecedents close", "Pi_M d = d Pi_M on C_H(A_ext) and delta_m Pi_M=0 imply [d,Pi_M]J_H=0", "EXACT_CONDITIONAL_THEOREM_NOT_CURRENT_CLAIM", "antecedents PIM2899_0..2 plus no-stress/equality guards unsigned"),
        ("PIM2899_4_topological_Hilbert_equality", "closed topological current is the same object as projected Hilbert source mass", "Pi_M J_H = J_M_top + dB_zero, int_boundary dB_zero=0, common M_ref", "NOT_DERIVED_R_EQ_UNFILLED", "closed wrong current cannot prove epsilon_PiM_equality"),
        ("PIM2899_5_projector_stress_silence", "Pi_M variation creates no independent stress", "delta_g Pi_M=delta_domain Pi_M=0 or projector stress is source-backed below local locks", "NOT_PARENT_SIGNED", "Hodge/domain projector route keeps R11/PPN stress residuals"),
        ("PIM2899_6_no_multiplier_or_readout_cheat", "no late closure multiplier or readout-defined projector is used", "Pi_M appears in parent/source-normalization structure before scoring", "PASS_GUARD_NONCLAIM", "protects derivation from fitted closure"),
        ("PIM2899_7_verdict", "current MTS proves PiM equality and commutator zero", "all preceding theorem rows parent-signed and no missing R_eq/I_commutator/projector stress rows", "FAIL_CURRENT_MTS_PIM_LOCK_NOT_DERIVED", "epsilon_PiM_equality and epsilon_commutator remain explicit nonclaim rows"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "formal_statement": formal_statement,
                "result": result,
                "blocking_gap": blocking_gap,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for audit_id, claim_piece, formal_statement, result, blocking_gap in specs
    ]


def row_pack() -> list[dict[str, Any]]:
    specs = [
        ("PIMROW2899_0_epsilon_PiM_equality", "epsilon_PiM_equality", "R_eq_integral/M_ref", "R_eq_integral = int_A(Pi_M J_H - J_M_top - dB_zero)", "MISSING_TOPOLOGICAL_HILBERT_EQUALITY_OR_VALUE", "dimensionless_after_M_ref_normalization", "ECE2898_1;SRC523_0;Newton;R11"),
        ("PIMROW2899_1_epsilon_commutator_abs", "epsilon_commutator_abs", "M_ref^-1 * abs(int_A [d,Pi_M]J_H)", "finite-shell product-rule leakage from non-fixed Pi_M", "MISSING_CHAINMAP_ZERO_OR_I_COMMUTATOR_VALUE", "dimensionless_after_M_ref_normalization_or_GM_flux_before_normalization", "ECE2898_2;radial_Meff_hair;PPN;R10;R11"),
        ("PIMROW2899_2_projector_variation_stress", "projector_stress_beta_equiv", "weak-field map of -2/sqrt(-g) delta S_PiM/delta g_munu", "stress generated if Pi_M uses metric/Hodge/domain data", "MISSING_PROJECTOR_STRESS_MAP_OR_VALUE", "PPN_or_operator_units", "gamma;beta;preferred_frame;local_GR;R11"),
        ("PIMROW2899_3_domain_motion", "D_domain_PiM", "domain/worldtube/linking-surface derivative contribution", "domain movement or fitted surface choice shifts the source current", "MISSING_DOMAIN_LOCK_OR_OPERATOR_BOUND", "operator_norm_or_dimensionless_flux", "radial_Meff_hair;R10;orbital"),
        ("PIMROW2899_4_zero_boundary_flux", "B_zero_flux", "int_boundary dB_zero/M_ref", "exact primitive/reference subtraction flux in topological-Hilbert equality", "MISSING_ZERO_BOUNDARY_FLUX_THEOREM_OR_VALUE", "dimensionless_after_M_ref_normalization", "epsilon_PiM_equality;boundary_monopole;orbital"),
        ("PIMROW2899_5_total_no_cancellation", "PiM_equality_commutator_envelope", "sum_abs(PIMROW2899_0..PIMROW2899_4)", "strict no-cancellation envelope over PiM equality/commutator/stress/domain/boundary rows", "NOT_COMPUTED_COMPONENTS_UNFILLED", "dimensionless_after_common_denominator", "epsilon_charge_abs_envelope;source_normalized_Newton"),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "definition": definition,
                "current_value": current_value,
                "units": units,
                "observable_link": observable_link,
                "source_path": str(DOC),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, formula, definition, current_value, units, observable_link in specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "eval_id": "EVAL2899_0_current_MTS_PiM_lock",
                "mode": "strict_claim",
                "formula": "PiM_equality_commutator_envelope = sum_abs(epsilon_PiM_equality, epsilon_commutator_abs, projector_stress_beta_equiv, D_domain_PiM, B_zero_flux)",
                "computed_value": "NOT_EVALUATED",
                "result": "REFUSED_MISSING_COMPONENTS",
                "reason": "R_eq, I_commutator, projector stress, domain derivative, and boundary flux rows lack theorem-zero or numeric source-backed values",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "eval_id": "EVAL2899_1_fixed_chainmap_conditional",
                "mode": "conditional_theorem_control",
                "formula": "if parent fixed chainmap antecedents and physical current complex close, epsilon_commutator_abs=0",
                "computed_value": "CONDITIONAL_ZERO_ONLY",
                "result": "USEFUL_NOT_CLAIM",
                "reason": "algebra is clean but parent selector/domain/current-complex antecedents are unsigned",
                "runner_ready": False,
            }
        ),
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2899_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2899_1_fixed_chainmap", "fixed-chainmap commutator zero theorem is conditionally clean", "PASS_NONCLAIM", "2585 already establishes the algebraic conditional theorem", False),
        ("GATE2899_2_parent_antecedents", "parent selector/domain/current-complex antecedents are signed", "FAIL", "parent source complex and fixed worldtube are still unsigned", False),
        ("GATE2899_3_same_object", "closed topological current equals observed Hilbert source mass", "FAIL", "R_eq and B_zero_flux remain unfilled", False),
        ("GATE2899_4_projector_stress", "PiM stress/variation is zero or bounded", "FAIL", "Hodge/domain route keeps projector stress without a source-backed bound", False),
        ("GATE2899_5_rows_staged", "PiM equality/commutator residual rows are staged", "PASS_NONCLAIM", "R_eq/I_commutator/stress/domain/boundary rows are explicit and nonclaim", False),
        ("GATE2899_6_no_magic", "readout masks and closure multipliers are forbidden", "PASS_GUARD", "route gate rejects fitted PiM and lambda_M magic wand", False),
        ("GATE2899_7_next", "next target moves to source-worldtube/current-complex owner", "PASS_NONCLAIM", "do not circle product-rule algebra again", False),
        ("GATE2899_8_local_GR", "source-normalized Newton/local GR branch closes", "FAIL_CLOSED", "PiM lock and epsilon_charge denominator remain blocked", False),
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
                "runner_id": "RUN2899_0_PiM_theorem_runner",
                "status": "REFUSED_UNSIGNED_ANTECEDENTS",
                "required_components": "parent selector; fixed worldtube/domain; physical Hilbert-current complex; same-object equality; no projector stress",
                "components_evaluable": 0,
                "reason": "fixed-chainmap algebra is conditional, not current MTS evidence",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "runner_id": "RUN2899_1_residual_envelope_runner",
                "status": "STAGED_NONCLAIM_ROWS",
                "required_components": "R_eq_integral; I_commutator; projector_stress; D_domain_PiM; B_zero_flux",
                "components_evaluable": 0,
                "reason": "rows are explicit but missing numeric/theorem-zero values and source-backed units",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "runner_id": "RUN2899_2_next_source_complex",
                "status": "NEXT_TARGET_SELECTED",
                "required_components": "source worldtube/current complex ownership",
                "components_evaluable": 0,
                "reason": "this is the narrow antecedent needed before the clean chainmap theorem can be used",
                "runner_ready": False,
            }
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2899_0_keep_conditional", "KEEP_FIXED_CHAINMAP_ZERO_AS_CONDITIONAL_THEOREM", "the product-rule algebra is clean if PiM is a parent fixed chainmap on the physical current complex", "do not re-litigate this algebra without new parent evidence"),
        ("DEC2899_1_reject_claim", "REJECT_CURRENT_PIM_ZERO_CLAIM", "parent selector, domain/worldtube, physical current complex, R_eq, B_zero and M_ref locks are unsigned", "keep epsilon_PiM_equality and epsilon_commutator nonclaim"),
        ("DEC2899_2_prefer_topological", "PREFER_TOPOLOGICAL_PARENT_PIM_OVER_HODGE_ROUTE", "a metric/Hodge projector creates variation stress unless separately bounded", "treat Hodge/domain PiM as residual route"),
        ("DEC2899_3_no_magic", "FORBID_READOUT_MASK_AND_CLOSURE_MULTIPLIER", "those routes impose Newton/source-normalization instead of deriving it", "allow only explicit closure labels, no derivation credit"),
        ("DEC2899_4_next", "SELECT_SOURCE_WORLDTUBE_CURRENT_COMPLEX", "the missing antecedent is not the product rule but ownership of W_source/A_ext/S_link/J_H/tau in one parent complex", "build 2900 source-worldtube/current-complex owner or J_domain bound fill"),
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
                "next_id": "NEXT2899_0_2900",
                "status": "selected_primary",
                "target_doc": "2900-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_worldtube_current_complex_owner_or_Jdomain_bound_fill_under_AX1090_2900.py",
                "mission": "prove W_source, A_ext, S_link, J_H[e_obs,tau] and tau are parent-owned before readout and live in the same Hilbert-current complex used by Pi_M; if proof fails, fill J_domain/current-escape bound rows with units and source paths",
                "forbidden": "source worldtube chosen after fitting; observed-GM normalization; Noether conservation alone as source equality; closed wrong charge; local-GR/Newton/beta claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2899_1_held_extra_projection",
                "status": "held_after_current_complex",
                "target_doc": "2900b-Y5-R2FR-extra-projection-channelwise-zero-or-source-envelope.md",
                "target_script": "scripts/Y5_R2FR_extra_projection_channelwise_zero_or_source_envelope_2900b.py",
                "mission": "attack Pi_M dJ_extra channelwise only after PiM/current-complex ownership is explicit",
                "forbidden": "channel cancellation; measured-GM absorption; local-GR claim",
                "selected": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("BR2899_0_rows_copy", OUTPUTS["rows"], BRANCH_OUTPUTS["rows_copy"], "local-bounds copy of PiM equality/commutator rows"),
        ("BR2899_1_evaluator_copy", OUTPUTS["evaluator"], BRANCH_OUTPUTS["evaluator_copy"], "beta-source copy of PiM evaluator"),
        ("BR2899_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue copy of next target"),
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
    route_rows_ = all_rows["route"]
    theorem_rows_ = all_rows["theorem"]
    row_pack_ = all_rows["rows"]
    evaluator_rows_ = all_rows["evaluator"]
    gate_rows_ = all_rows["gates"]
    next_rows_ = all_rows["next"]
    branch_rows = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]

    required_symbols = {
        "epsilon_PiM_equality",
        "epsilon_commutator_abs",
        "projector_stress_beta_equiv",
        "D_domain_PiM",
        "B_zero_flux",
    }
    found_symbols = {row["symbol"] for row in row_pack_}

    checks = [
        ("VAL2899_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2899_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2899_2_fixed_chainmap_conditional", any(row["route_id"] == "ROUTE2899_0_fixed_chainmap" and "conditional" in row["current_status"] for row in route_rows_), "fixed chainmap is kept as conditional route"),
        ("VAL2899_3_theorem_refused", any(row["audit_id"] == "PIM2899_7_verdict" and "FAIL" in row["result"] for row in theorem_rows_), "current PiM lock is refused"),
        ("VAL2899_4_required_rows_present", required_symbols <= found_symbols, "PiM equality/commutator row pack contains required symbols"),
        ("VAL2899_5_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in row_pack_), "all row-pack rows remain nonclaim"),
        ("VAL2899_6_evaluator_refuses", any(row["eval_id"] == "EVAL2899_0_current_MTS_PiM_lock" and row["result"] == "REFUSED_MISSING_COMPONENTS" for row in evaluator_rows_), "current PiM evaluator refuses missing components"),
        ("VAL2899_7_no_magic_guard", any(row["gate_id"] == "GATE2899_6_no_magic" and row["result"] == "PASS_GUARD" for row in gate_rows_), "readout masks and closure multipliers remain forbidden"),
        ("VAL2899_8_local_gr_fail_closed", any(row["gate_id"] == "GATE2899_8_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_), "local GR/Newton remains fail-closed"),
        ("VAL2899_9_next_target_2900", any(row["next_id"] == "NEXT2899_0_2900" and row["selected"] for row in next_rows_), "2900 source-worldtube/current-complex target selected"),
        ("VAL2899_10_branch_copies_exist", all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2899_11_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2899_12_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2899_OVERALL", overall, "2899 validation overall"))
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
        "# 2899 - Y5 R2FR PiM Parent-Owned Projector Equality or Commutator Envelope Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-PiM-parent-owned-projector-equality-or-commutator-envelope-under-AX1090`",
        "Status: `Y5_R2FR_2899_PiM_lock_not_derived_fixed_chainmap_conditional_retained_source_complex_2900_next`",
        "Claim ceiling: `PiM_equality_commutator_envelope_only_no_epsilon_charge_measured_GM_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2899 does not prove the PiM lock. It does something more useful than another lap around the same cone: it separates the already-clean algebra from the missing parent-action antecedents.",
        "",
        "The clean conditional theorem is:",
        "",
        "`if Pi_M:C_H(A_ext)->C_M(A_ext) is parent-selected before readout, fixed on the compact exterior domain, and J_H[e_obs,tau] lives in that same parent current complex, then [d,Pi_M]J_H=0`.",
        "",
        "Current MTS does not yet own those antecedents. It also does not prove the same-object guard `Pi_M J_H = J_M_top + dB_zero` with zero boundary flux and common `M_ref`. Therefore `epsilon_PiM_equality` and `epsilon_commutator_abs` stay as explicit nonclaim residuals.",
        "",
        "The next target is not to re-derive the product rule again. It is to prove or bound the source-worldtube/current-complex owner: `W_source`, `A_ext`, `S_link`, `J_H[e_obs,tau]`, and `tau` must all be parent-owned before readout and live in the same complex.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## PiM Route Gate",
        "",
        md_table(all_rows["route"], ["route_id", "route_type", "statement", "effect", "current_status", "next_action", "valid_for_claim"]),
        "",
        "## PiM Theorem Audit",
        "",
        md_table(all_rows["theorem"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "valid_for_claim"]),
        "",
        "## Equality/Commutator Rows",
        "",
        md_table(all_rows["rows"], ["row_id", "symbol", "formula", "definition", "current_value", "units", "observable_link", "valid_for_claim"]),
        "",
        "## Evaluator",
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
        "This is a genuine narrowing. The PiM algebra is no longer the fog. The fog is whether MTS owns the source current, worldtube, exterior domain, linking surfaces, and time generator in one parent complex before readout. That is exactly the kind of missing structure a real GR-reduction proof needs.",
        "",
        "## Forbidden Claims From 2899",
        "",
        "- MTS has proved `Pi_M J_H = J_M_top + dB_zero`.",
        "- MTS has proved `[d,Pi_M]J_H=0` for the current local branch.",
        "- A Hodge/metric/domain `Pi_M` is harmless without a projector-stress row.",
        "- A readout mask or closure multiplier counts as derivation.",
        "- MTS has derived `epsilon_charge=0`, measured `GM`, source-normalized Newton, beta, PPN, R10, or local GR.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["route"] = route_rows()
    all_rows["theorem"] = theorem_rows()
    all_rows["rows"] = row_pack()
    all_rows["evaluator"] = evaluator_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "route", "theorem", "rows", "evaluator", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2899_OVERALL")
    print(f"2899 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
