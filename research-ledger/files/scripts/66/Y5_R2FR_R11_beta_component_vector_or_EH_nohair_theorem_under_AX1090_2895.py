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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2895-Y5-R2FR-R11-beta-component-vector-or-EH-nohair-theorem-under-AX1090.md"

SRC_2894_DOC = ROOT / "2894-Y5-R2FR-fill-A-B-source-coefficients-or-beta-vector-source-row-under-AX1090.md"
SRC_2894_NEXT = RESIDUALS / "P8_Y5_R2FR_2894_NEXT_TARGET.csv"
SRC_530_DOC = ROOT / "530-Y5-R11-beta-component-vector-or-EH-nohair-theorem.md"
SRC_529_DOC = ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md"
SRC_439_DOC = ROOT / "439-EH-only-exterior-parent-premise-ladder.md"
SRC_440_DOC = ROOT / "440-metric-only-second-order-sector-reduction-attempt.md"
SRC_1944_DOC = ROOT / "1944-Y5-R2FR-R11-weak-field-potential-equations-or-coefficient-placeholder-ledger.md"
SRC_1945_DOC = ROOT / "1945-Y5-R2FR-R11-traceless-spatial-zero-proof-or-Cassini-slip-bound.md"
SRC_R11_STATUS = RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv"
SRC_R11_SKELETON = RESIDUALS / "R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv"
SRC_R11_TEMPLATE = RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv"
SRC_PPN_R11 = RESIDUALS / "P8_Y5_PARENT_QLOC_1941_PPN_R11_RESIDUAL_VECTOR.csv"
SRC_EQ_R11 = RESIDUALS / "P8_Y5_PARENT_QLOC_1942_PPN_R11_EQUATION_MAP.csv"
SRC_1945_GATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1945_CLAIM_GATE.csv"
SRC_2894_ABROW = RESIDUALS / "P8_Y5_R2FR_2894_AB_COEFFICIENT_ROW_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2895_SOURCE_REGISTER.csv",
    "nohair": RESIDUALS / "P8_Y5_R2FR_2895_EH_NOHAIR_BETA_THEOREM_ATTEMPT.csv",
    "interface": RESIDUALS / "P8_Y5_R2FR_2895_GAMMA_SLIP_TO_BETA_INTERFACE.csv",
    "families": RESIDUALS / "P8_Y5_R2FR_2895_R11_BETA_OPERATOR_FAMILY_AUDIT.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_2895_R11_BETA_COMPONENT_ROWS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2895_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2895_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2895_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2895_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2895_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2895_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "nohair_copy": BETA_DOCS / "RAB_EH_NOHAIR_BETA_THEOREM_ATTEMPT_2895_NONCLAIM.csv",
    "components_copy": LOCAL_BOUNDS / "RAB_R11_BETA_COMPONENT_ROWS_2895_NONCLAIM.csv",
    "interface_copy": BETA_DOCS / "RAB_GAMMA_SLIP_TO_BETA_INTERFACE_2895_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2895_beta_envelope_or_first_R11_fill_NEXT.csv",
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
        ("SRC2895_0_2894_doc", SRC_2894_DOC, "Status: `Y5_R2FR_2894;NEXT2894_0_2895", "2894 A/B handoff and R11 fork"),
        ("SRC2895_1_2894_next", SRC_2894_NEXT, "NEXT2894_0_2895;R11 beta", "explicit 2895 target"),
        ("SRC2895_2_530_doc", SRC_530_DOC, "EHNH530_0_parent_frame;B530_0_source_AB;B530_11_readout_frame", "older R11 beta component vector"),
        ("SRC2895_3_529_doc", SRC_529_DOC, "SCEH529_1_EH_only_exterior;R11 Beta Fill Matrix", "source-calibrated EH proof stack"),
        ("SRC2895_4_439_doc", SRC_439_DOC, "P6_second_order_metric_equations;P9_weak_field_PPN_completion", "EH-only parent premise ladder"),
        ("SRC2895_5_440_doc", SRC_440_DOC, "R11 coefficient-vector data;current_policy", "metric-only sector reduction attempt"),
        ("SRC2895_6_1944_doc", SRC_1944_DOC, "delta_gamma_R11 ~=;P_TF[R11_ij]", "R11 weak-field gamma/slip reduction"),
        ("SRC2895_7_1945_doc", SRC_1945_DOC, "spherical symmetry alone does not kill;R11_ij=S(r)delta_ij", "R11 traceless-spatial zero attempt"),
        ("SRC2895_8_r11_status", SRC_R11_STATUS, "source_normalization_operator;template_only_retained_core_blocker", "current R11 family status"),
        ("SRC2895_9_r11_skeleton", SRC_R11_SKELETON, "R11_MTS_minimum_executable_vector;MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT", "minimum executable vector skeleton"),
        ("SRC2895_10_r11_template", SRC_R11_TEMPLATE, "R11_nonEH_operator_vector;fill_numeric_or_zero", "operator-vector template"),
        ("SRC2895_11_ppn_r11", SRC_PPN_R11, "PPN1941_2_beta_residual;MISSING_PPN_SOLVE", "PPN R11 residual vector"),
        ("SRC2895_12_eq_r11", SRC_EQ_R11, "EQ1942_2_beta;requires beta bound extraction", "PPN R11 equation map"),
        ("SRC2895_13_1945_gate", SRC_1945_GATE, "CG1945_3_parent_zero_theorem;FAIL_BLOCKED", "R11 TF zero claim gate"),
        ("SRC2895_14_2894_abrow", SRC_2894_ABROW, "ABR2894_0_current_MTS_AB_source_row;MISSING_A_SOURCE", "A/B row still missing"),
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


def nohair_rows() -> list[dict[str, Any]]:
    specs = [
        ("NH2895_0_observed_frame", "one observed metric/coframe through O(U^2)", "g_obs=g_matter=g_source=g_readout+O(U^3/c^6)", "would make R11 beta rows physical PPN rows", "UNSIGNED"),
        ("NH2895_1_metric_only", "no independent exterior scalar/vector/projector/domain/bulk/torsion/nonlocal hair", "Phi_extra=0/gauge/topological/no-stress in compact exterior", "would remove most R11 operator families", "UNSIGNED"),
        ("NH2895_2_second_order_operator", "surviving 4D local metric equation is second order and Lovelock-compatible", "E_munu=a G_munu+b g_munu only after parent rungs close", "would remove R2/f(R), Ricci/Weyl, nonlocal metric operators", "UNSIGNED"),
        ("NH2895_3_boundary_domain", "boundary/projector/domain class has no local stress, flux, dyad, or source shift", "delta_g S_boundary=0 locally and delta_mu_boundary=delta_beta_boundary=0", "would remove boundary/domain beta and preferred-frame rows", "UNSIGNED"),
        ("NH2895_4_source_mass", "measured mass/source normalization is constant and EH-owned", "mu_EH=mu_obs=G0 M_H, mu_extra=0, derivatives zero", "would make source A/B row meaningful", "UNSIGNED"),
        ("NH2895_5_beta_readout", "EH mass family is expanded in the observed PPN readout", "g00=-1+2U/c^2-2U^2/c^4+O(c^-6)", "would make beta=1 for the metric core", "CONDITIONAL_REFERENCE_ONLY"),
        ("NH2895_6_verdict", "EH/no-hair theorem for beta-relevant R11 rows", "all NH2895_0 through NH2895_5 parent-signed", "would set delta_beta_R11_i=0 and permit A/B square route", "NOT_DERIVED_CURRENT_CORPUS"),
    ]
    return [
        add_common(
            {
                "theorem_id": theorem_id,
                "required_clause": clause,
                "math_form": math_form,
                "if_signed": if_signed,
                "current_status": status,
                "condition_satisfied": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for theorem_id, clause, math_form, if_signed, status in specs
    ]


def interface_rows() -> list[dict[str, Any]]:
    specs = [
        ("GBI2895_0_gamma_target", "R11 gamma slip", "delta_gamma_R11 ~= -(kappa_R/(C_TF U)) nabla^{-2} P_TF[R11_ij]", "P_TF[R11_ij]=0 is sufficient for leading R11 gamma safety", "PASS_NONCLAIM"),
        ("GBI2895_1_spherical_guard", "spherical residual", "R_ij=A n_i n_j+B(delta_ij-n_i n_j) has P_TF=(A-B)(n_i n_j-delta_ij/3)", "spherical symmetry alone does not erase slip", "PASS_GUARD"),
        ("GBI2895_2_beta_not_gamma", "R11 beta", "g00=-1+2U/c^2-2(1+delta_beta_R11)U^2/c^4", "P_TF zero does not kill time-time/common nonlinear U2 beta residuals", "BETA_REMAINS_OPEN"),
        ("GBI2895_3_common_mode", "common R11 mode", "Phi_R11=Psi_R11 can make gamma safe while still shifting Newtonian/source/beta channels", "common mode needs ephemeris, inverse-square, measured-GM and beta checks", "OPEN_RESIDUAL"),
        ("GBI2895_4_no_overclaim", "local GR", "gamma-safe + beta-open + preferred-frame-open != local GR", "R11 TF/gamma progress cannot be promoted to PPN/local-GR", "CLAIM_BLOCKED"),
    ]
    return [
        add_common(
            {
                "interface_id": interface_id,
                "object": obj,
                "math_form": math_form,
                "meaning": meaning,
                "current_status": status,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for interface_id, obj, math_form, meaning, status in specs
    ]


def family_rows() -> list[dict[str, Any]]:
    specs = [
        ("FAM2895_0_source_norm", "source_normalization_operator", "delta_beta_source; epsilon_SN; Gdot; alpha(lambda)", "mu_extra/G_effM_eff and A/B source square law", "highest", "template_only_retained_core_blocker"),
        ("FAM2895_1_R2_fR", "R2_fR_scalar_mode", "delta_beta_R2_fR; gamma; alpha(lambda)", "coefficient, scalar mass, source coupling and weak-field PPN map", "high", "template_only"),
        ("FAM2895_2_scalar_class", "scalar_tensor_class_metric", "delta_beta_scalar_class; clock; Gdot; alpha(lambda)", "F(phi,C), scalar charge, source coupling and PPN/Gdot map", "high", "template_only"),
        ("FAM2895_3_boundary", "boundary_topological_terms", "delta_beta_boundary; alpha3; xi", "boundary coefficient or no-flux/no-stress theorem", "high", "template_only"),
        ("FAM2895_4_projector_domain", "projector_domain_stress", "delta_beta_projector_domain; alpha_i; xi", "projector/domain stress coefficient or metric-independent topological theorem", "high", "template_only"),
        ("FAM2895_5_nonlocal", "nonlocal_memory_kernel", "delta_beta_nonlocal; alpha3; Gdot; alpha(lambda)", "kernel norm/local compact silence proof", "medium", "template_only"),
        ("FAM2895_6_connection", "torsion_nonmetricity", "delta_beta_connection_readout; WEP; clock; lightcone", "Levi-Civita/no-independent-connection theorem or connection residual map", "medium", "template_only"),
        ("FAM2895_7_vector", "vector_preferred_frame", "alpha1; alpha2; alpha3; xi; beta cross-term", "vector absent/gauge/aligned theorem or preferred-frame coefficients", "medium", "template_only"),
        ("FAM2895_8_bulk_X", "bulk_X_force_law", "delta_beta_bulk_X; gamma; alpha(lambda)", "bulk source/test charge, mass gap and force-law map", "medium", "template_only"),
        ("FAM2895_9_Ricci_Weyl", "Ricci_Weyl_squared", "gamma; xi; possible beta/wave-sector response", "c_Ricci/c_Weyl, topological status and weak-field map", "medium", "template_only"),
    ]
    return [
        add_common(
            {
                "family_id": family_id,
                "operator_family": family,
                "beta_or_ppn_channels": channels,
                "required_real_input": required,
                "priority": priority,
                "current_status": status,
                "source_basis": "R11_EXECUTABLE_VECTOR_STATUS.csv;R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for family_id, family, channels, required, priority, status in specs
    ]


def component_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "R11B2895_0_source_normalization",
            "source_normalization_operator",
            "delta_beta_source_R11",
            "B_source/A_source^2-1 plus mu_extra/derivative source-normalization tails",
            "MISSING_A_B_SOURCE_ROW_OR_CONSTANT_MEASURED_GM_THEOREM",
            "dimensionless",
            "7.8e-05",
            "highest: controls A/B and measured mass",
        ),
        (
            "R11B2895_1_R2_fR_scalar",
            "R2_fR_scalar_mode",
            "delta_beta_R2_fR",
            "coefficient/scalar-mass/source-coupling -> beta/gamma/alpha(lambda) weak-field response",
            "MISSING_C_R2_OR_CF_R_SCALAR_MASS_SOURCE_COUPLING_MAP",
            "dimensionless plus range if finite-mass scalar",
            "7.8e-05 and gamma/R10 locks",
            "first metric-operator fill candidate",
        ),
        (
            "R11B2895_2_boundary_domain",
            "boundary_topological_terms;projector_domain_stress",
            "delta_beta_boundary_domain",
            "boundary/projector/domain stress and quadratic source shift -> beta/preferred-frame/location residuals",
            "MISSING_BOUNDARY_NOHAIR_OR_PROJECTOR_STRESS_MAP",
            "dimensionless or PPN-equivalent",
            "7.8e-05 with alpha3/xi guard",
            "tight because alpha3/xi can dominate",
        ),
        (
            "R11B2895_3_scalar_class",
            "scalar_tensor_class_metric",
            "delta_beta_scalar_class",
            "scalar/class source charge and nonlinear completion -> B/A^2 residual",
            "MISSING_SCALAR_SILENCE_OR_SCALAR_PPN_GDOT_RANGE_MAP",
            "dimensionless plus clock/Gdot/range maps",
            "7.8e-05 with clock/Gdot/R10 locks",
            "same-frame language is not enough",
        ),
        (
            "R11B2895_4_readout_connection",
            "torsion_nonmetricity;observed_readout_frame",
            "delta_beta_readout_connection",
            "connection/readout mismatch at O(U2) -> apparent beta shift",
            "MISSING_LEVI_CIVITA_OR_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "dimensionless/readout map",
            "7.8e-05 plus WEP/clock/lightcone locks",
            "prevents coordinate beta win",
        ),
        (
            "R11B2895_5_total_R11_beta_abs",
            "all_R11_beta_components",
            "sum_abs_delta_beta_R11_i",
            "sum absolute active R11 beta components with no cancellation",
            "ALL_COMPONENTS_MISSING_OR_TEMPLATE_ONLY",
            "dimensionless",
            "7.8e-05",
            "not executable until component rows are real",
        ),
    ]
    return [
        add_common(
            {
                "component_id": component_id,
                "operator_family": family,
                "symbol": symbol,
                "formal_map": formal_map,
                "missing_for_claim": missing,
                "units": units,
                "bound_or_gate": bound,
                "priority_note": note,
                "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
                "source_path": "MISSING_REAL_COMPONENT_SOURCE_PATH",
                "no_cancellation_policy": "sum absolute R11 beta components; no cancellation credit without parent identity",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for component_id, family, symbol, formal_map, missing, units, bound, note in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2895_0_nohair_attempt", "EH/no-hair beta theorem attempted", "PASS_NONCLAIM", "rungs and blockers are explicit"),
        ("GATE2895_1_nohair_parent_signed", "EH/no-hair rungs are parent-signed", "FAIL", "observed frame, metric-only, second-order, boundary, measured-mass and readout rungs remain unsigned"),
        ("GATE2895_2_gamma_beta_interface", "gamma-safe target is separated from beta-safe target", "PASS_NONCLAIM", "P_TF zero does not erase common/time-time beta residuals"),
        ("GATE2895_3_R11_component_rows", "R11 beta component rows exist", "PASS_NONCLAIM", "rows are staged but nonclaim"),
        ("GATE2895_4_component_values", "R11 beta components are numeric/source-backed or theorem-zero", "FAIL", "all current rows are missing/template-only"),
        ("GATE2895_5_total_R11_beta", "sum_abs_delta_beta_R11_i can be scored", "FAIL", "component rows are not executable"),
        ("GATE2895_6_local_gr", "local GR/PPN branch closes", "FAIL", "R11 beta, A/B, q_loc, boundary, readout and measured-GM gates remain open"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2895_0_R11_beta_nohair_or_component_runner",
                "status": "REFUSED_COMPONENTS_TEMPLATE_ONLY",
                "accepted_nohair_theorems": 0,
                "accepted_component_rows": 0,
                "staged_component_rows": 6,
                "reason": "EH/no-hair is not parent-signed and every R11 beta component row still lacks real coefficients, theorem-zero proof, units, normalization, and source path",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2895_0_nohair", "EH_NOHAIR_REMAINS_CONDITIONAL", "the theorem target is correct but current parent rungs are unsigned", "do not set R11 beta components to zero"),
        ("DEC2895_1_gamma_beta", "DO_NOT_PROMOTE_GAMMA_TF_PROGRESS_TO_BETA", "P_TF zero would help gamma but common/time-time U2 rows can still shift beta", "keep beta component vector active"),
        ("DEC2895_2_components", "KEEP_FIRST_R11_BETA_COMPONENT_ROWS", "the rows are the executable shape future source work must satisfy", "fill source_normalization_operator or R2/fR scalar first"),
        ("DEC2895_3_next", "MOVE_TO_BETA_ENVELOPE_OR_FIRST_REAL_R11_FILL", "R11 beta rows now exist but are not score-ready; the next useful object is the full beta envelope or first real component", "build 2896 source-normalized Newton/beta envelope with first-fill queue"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2895_0_2896",
                "status": "selected_primary",
                "target_doc": "2896-Y5-R2FR-source-normalized-Newton-beta-envelope-or-first-R11-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_normalized_Newton_beta_envelope_or_first_R11_fill_under_AX1090_2896.py",
                "mission": "combine A/B source, R11 beta, q_loc, boundary/domain, readout, and measured-GM terms into one no-cancellation beta envelope; if still blocked, select the first real R11 fill row",
                "forbidden_shortcuts": "no gamma-only promotion; no EH import; no cancellation; no placeholder coefficients; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2895_1_held_parent_conformal",
                "status": "held_until_new_parent_evidence",
                "target_doc": "2896b-Y5-R2FR-parent-conformal-descent-reentry-if-new-evidence.md",
                "target_script": "scripts/Y5_R2FR_parent_conformal_descent_reentry_if_new_evidence_2896b.py",
                "mission": "retry R11 conformal/no-dyad/no-Hessian zero theorem only if new parent action evidence appears",
                "forbidden_shortcuts": "do not repeat 1945/2895 nohair attempt without new source evidence",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2895_0_nohair_copy", OUTPUTS["nohair"], BRANCH_OUTPUTS["nohair_copy"], "beta-source copy of EH/no-hair beta theorem attempt"),
        ("BR2895_1_components_copy", OUTPUTS["components"], BRANCH_OUTPUTS["components_copy"], "local-bounds copy of R11 beta component rows"),
        ("BR2895_2_interface_copy", OUTPUTS["interface"], BRANCH_OUTPUTS["interface_copy"], "beta-source copy of gamma-to-beta interface guard"),
        ("BR2895_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in copy_specs:
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


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "condition_satisfied",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    nohair = rows_by_name["nohair"]
    interface = rows_by_name["interface"]
    families = rows_by_name["families"]
    components = rows_by_name["components"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    component_symbols = {row["symbol"] for row in components}
    required_symbols = {
        "delta_beta_source_R11",
        "delta_beta_R2_fR",
        "delta_beta_boundary_domain",
        "delta_beta_scalar_class",
        "delta_beta_readout_connection",
        "sum_abs_delta_beta_R11_i",
    }

    checks = [
        ("VAL2895_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2895_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2895_2_nohair_attempt", nohair[-1]["current_status"] == "NOT_DERIVED_CURRENT_CORPUS", "EH/no-hair theorem is attempted but not adopted"),
        ("VAL2895_3_gamma_beta_guard", any(row["interface_id"] == "GBI2895_2_beta_not_gamma" and row["current_status"] == "BETA_REMAINS_OPEN" for row in interface), "gamma TF progress is separated from beta"),
        ("VAL2895_4_family_audit", len(families) >= 10 and all(row["current_status"].startswith("template") for row in families), "R11 operator family audit remains template/nonclaim"),
        ("VAL2895_5_component_rows", required_symbols.issubset(component_symbols), "R11 beta component rows include required first-fill components"),
        ("VAL2895_6_components_missing", all(row["current_value"] == "MISSING_NUMERIC_OR_DERIVED_ZERO" for row in components), "no R11 beta component is fabricated"),
        ("VAL2895_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2895_8_runner_refused", runner[0]["status"] == "REFUSED_COMPONENTS_TEMPLATE_ONLY" and runner[0]["runner_ready"] is False, "runner refuses template-only components"),
        ("VAL2895_9_next_target_2896", next_target[0]["next_id"] == "NEXT2895_0_2896" and next_target[0]["selected"] is True, "2896 beta envelope target selected"),
        ("VAL2895_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2895_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2895_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2895_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2895_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2895_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2895_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2895_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2895 separated R11 gamma-slip progress from beta safety, refused EH/no-hair beta closure, staged first R11 beta component rows, and selected the full source-normalized beta envelope for 2896.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2895 - Y5 R2FR R11 Beta Component Vector Or EH Nohair Theorem Under AX1090

Status: `Y5_R2FR_2895_R11_beta_nohair_refused_gamma_beta_separated_components_staged_2896_next`

## Private Verdict

2895 takes the R11 fork without pretending the old gamma work solved beta.

The strongest useful inheritance is from 1944/1945: `delta_gamma_R11 ~= -(kappa_R/(C_TF U)) nabla^-2 P_TF[R11_ij]`, and `R11_ij=S delta_ij` would kill the leading traceless-spatial gamma slip source.

But that is not a beta theorem. `P_TF[R11_ij]=0` can make the R11 branch gamma-safe while common/time-time/nonlinear/source-normalization pieces still shift `g_00=-1+2U/c^2-2(1+delta_beta_R11)U^2/c^4`.

So 2895 refuses EH/no-hair beta closure, preserves the no-hair theorem target, and stages first R11 beta component rows. The current state remains nonclaim: every component is still missing a real coefficient, theorem-zero proof, units, normalization, and source path.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## EH Nohair Beta Theorem Attempt

{md_table(rows_by_name["nohair"], ["theorem_id", "required_clause", "math_form", "if_signed", "current_status", "condition_satisfied", "valid_for_claim"])}

## Gamma Slip To Beta Interface

{md_table(rows_by_name["interface"], ["interface_id", "object", "math_form", "meaning", "current_status", "valid_for_claim"])}

## R11 Beta Operator Family Audit

{md_table(rows_by_name["families"], ["family_id", "operator_family", "beta_or_ppn_channels", "required_real_input", "priority", "current_status", "valid_for_claim"])}

## R11 Beta Component Rows

{md_table(rows_by_name["components"], ["component_id", "operator_family", "symbol", "formal_map", "missing_for_claim", "bound_or_gate", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_nohair_theorems", "accepted_component_rows", "staged_component_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "nohair": nohair_rows(),
        "interface": interface_rows(),
        "families": family_rows(),
        "components": component_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2895_OVERALL")
    print(f"VAL2895_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
