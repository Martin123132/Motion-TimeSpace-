from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2694"
BRANCH_ID = "Y5_R2FR_SECTOR_POSITIVE_OPERATOR_SILENCE_CERTIFICATES_OR_RESIDUAL_VALUES_2694"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2694-Y5-R2FR-sector-positive-operator-silence-certificates-or-residual-values.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2694_SOURCE_REGISTER.csv",
    "sector_priority": RESIDUALS / "P8_Y5_R2FR_2694_SECTOR_PRIORITY_AND_DEPENDENCY_MATRIX.csv",
    "certificate_attempt": RESIDUALS / "P8_Y5_R2FR_2694_SECTOR_CERTIFICATE_ATTEMPT_MATRIX.csv",
    "operator_trials": RESIDUALS / "P8_Y5_R2FR_2694_FIELD_SPECIFIC_OPERATOR_TRIALS.csv",
    "residual_requirements": RESIDUALS / "P8_Y5_R2FR_2694_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM.csv",
    "local_gr_gate": RESIDUALS / "P8_Y5_R2FR_2694_LOCAL_GR_IMPACT_GATE.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2694_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2694_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2694_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2694_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2694_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2694_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2694_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_sector_priority": LOCAL_BOUNDS / "sector_priority_and_dependency_matrix_2694_NONCLAIM.csv",
    "local_certificate_attempt": LOCAL_BOUNDS / "sector_certificate_attempt_matrix_2694_NONCLAIM.csv",
    "local_residual_requirements": LOCAL_BOUNDS / "residual_value_requirements_2694_NONCLAIM.csv",
    "wep_residual_requirements": WEP_RESIDUALS / "residual_value_requirements_2694_NONCLAIM.csv",
    "source_weight_residual_requirements": SOURCE_WEIGHT / "SECTOR_RESIDUAL_VALUE_REQUIREMENTS_2694_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2694_KAPPA_TOPOLOGICAL_SUPERSELECTION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2694_2693_DOC",
        "relative_path": "2693-Y5-R2FR-Lovelock-hypothesis-prover-or-left-hand-operator-residual-acquisition.md",
        "required_needles": ["NEXT2693_0_selected", "SCR2693_9_verdict", "VAL2693_OVERALL"],
        "purpose": "imports selected 2694 sector-certificate target",
    },
    {
        "source_id": "SRC2694_2693_REQUIREMENTS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2693_SECTOR_CERTIFICATE_REQUIREMENTS_NONCLAIM.csv",
        "required_needles": ["SCR2693_0_higher_derivative", "SCR2693_8_worldtube_gauss", "CERTIFICATE_SET_INCOMPLETE"],
        "purpose": "imports sector certificate queue from 2693",
    },
    {
        "source_id": "SRC2694_2693_ACQUISITION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2693_OPERATOR_RESIDUAL_ACQUISITION_ROWS_NONCLAIM.csv",
        "required_needles": ["ACQ2693_0_c_HD", "ACQ2693_9_total_abs", "MISSING_COMPONENT_VALUES_AND_KERNELS"],
        "purpose": "imports residual acquisition rows from 2693",
    },
    {
        "source_id": "SRC2694_2621_VARIATION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SECTOR_VARIATION_GATE_2621_SECTOR_VARIATION_DERIVATION_ATTEMPT.csv",
        "required_needles": ["VAR2621_2_higher_derivative", "VAR2621_6_nonlocal_history", "NONCLAIM_BOUND_REQUIRED"],
        "purpose": "imports prior sector variation formulas",
    },
    {
        "source_id": "SRC2694_2621_SCALING",
        "relative_path": "source-intake/mts_residuals/P8_Y5_SECTOR_VARIATION_GATE_2621_LOCAL_SCALING_ESTIMATE_PACK.csv",
        "required_needles": ["SCL2621_2_higher", "SCL2621_6_nonlocal", "MISSING_KERNEL_BOUND"],
        "purpose": "imports prior local scaling estimates",
    },
    {
        "source_id": "SRC2694_507_QUEUE",
        "relative_path": "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
        "required_needles": ["kappa_Geff_source_normalization", "508-constant-kappa-superselection-or-drift-residual.md", "G507_0_theorem_zero"],
        "purpose": "imports field-specific silence priority queue",
    },
    {
        "source_id": "SRC2694_508_KAPPA",
        "relative_path": "508-constant-kappa-superselection-or-drift-residual.md",
        "required_needles": ["T508_1_topological_zeroform", "KR508_0_time_drift", "V508_4_local_GR_claim_blocked"],
        "purpose": "imports kappa topological superselection route and residuals",
    },
    {
        "source_id": "SRC2694_1508_LX",
        "relative_path": "1508-Y5-R10-RAB-field-specific-LX-operator-certificate-or-alpha-prior-source-pack.md",
        "required_needles": ["LXA1508_8_verdict", "TRIAL1508_8_acceptance", "VAL1508_14_overall"],
        "purpose": "imports field-specific L_X certificate gate",
    },
    {
        "source_id": "SRC2694_CONSTANT_GM",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "required_needles": ["Z1_global_coupling_superselection", "Z8_second_order_source_stability"],
        "purpose": "imports measured-GM/kappa/source-normalization blockers",
    },
    {
        "source_id": "SRC2694_CONSTANT_KAPPA",
        "relative_path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "required_needles": ["CU1_global_coupling_status", "CU8_retained_residual_fallback"],
        "purpose": "imports universal kappa contract",
    },
    {
        "source_id": "SRC2694_DOMAIN",
        "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
        "required_needles": ["P2_domain_selector_no_vector", "P5_R11_operator_vector"],
        "purpose": "imports domain/projector no-vector blockers",
    },
    {
        "source_id": "SRC2694_MEMORY",
        "relative_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_DECISION.csv",
        "required_needles": ["D0_double_zero_requirement", "D4_promotion"],
        "purpose": "imports memory double-zero status",
    },
    {
        "source_id": "SRC2694_YLOC",
        "relative_path": "source-intake/mts_residuals/P8_YLOC_SOURCE_DEBT_LEDGER.csv",
        "required_needles": ["S0_boundary_source", "S4_Bianchi_stress_current"],
        "purpose": "imports local motion/source-current debts",
    },
    {
        "source_id": "SRC2694_BOUNDARY",
        "relative_path": "source-intake/mts_residuals/P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv",
        "required_needles": ["R4_flux_zero", "R5_constant_monopole_derivative_silence"],
        "purpose": "imports boundary no-flux repair ledger",
    },
    {
        "source_id": "SRC2694_R11_QUEUE",
        "relative_path": "source-intake/mts_residuals/R11_OPERATOR_VECTOR_FILL_QUEUE.csv",
        "required_needles": ["source_normalization_operator", "vector_preferred_frame", "boundary_topological_terms"],
        "purpose": "imports R11 operator-vector fill priorities",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def sector_priority_rows() -> list[dict[str, Any]]:
    rows = [
        (1, "kappa_Geff_source_normalization", "measured GM, Gdot, radial hair, source/range/frame/domain dependence all depend on constant universal kappa", "derive topological/global coupling superselection or retain drift/source/range residuals", "508 topological zero-form route", "2695_kappa_topological_superselection"),
        (2, "source_measure_and_Meff_flux", "constant kappa is not enough unless M_eff is the conserved Hilbert/worldtube/Gauss charge", "derive source-measure flux closure or retain mass flux residuals", "parallel source/Gauss branch", "held_after_kappa"),
        (3, "higher_derivative_public_metric", "second-order Lovelock hypothesis fails if higher operators survive", "forbid/topological/redundant proof or source-backed high-scale coefficient", "2621 scaling rows; R11 queue", "operator_basis_after_kappa"),
        (4, "domain_projector_selector", "preferred-frame/location and source-normalization rows are severe", "derive topological no-vector/no-stress projector or fill coefficient products", "domain alpha3 premise ledger", "domain_projector_after_kappa"),
        (5, "memory_coframe_nonlocal", "cosmology-friendly memory cannot leak into compact local systems", "derive stable local memory/frame-lock silence or kernel bounds", "double-zero memory; 1508 L_X gate", "memory_after_kappa"),
        (6, "motion_time_flow_modes", "Yloc route needs actual source-current zero, not closure language", "derive field-specific operator/no-source/no-boundary current or retain source rows", "YLOC source debt ledger", "motion_flow_after_kappa"),
        (7, "boundary_topological_terms", "boundary flux can become mass/PPN/clock hair", "derive fixed-before-readout zero flux/reference lock or retain boundary coefficients", "boundary scalar repair ledger", "boundary_after_core_sectors"),
        (8, "metric_EH_operator_core", "final local GR needs EH-only or executable non-EH vector", "derive metric-only second-order EH operator or fill R11 operator vector", "Lovelock/EH branch", "after_source_and_sector_silence"),
    ]
    return [
        {
            "priority": row[0],
            "sector": row[1],
            "why_here": row[2],
            "required_next_certificate": row[3],
            "evidence_anchor": row[4],
            "selected_next_target_hint": row[5],
            "sector_claim_status": "open_nonclaim",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def certificate_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("CERT2694_0_kappa", "kappa_Geff_source_normalization", "topological/global zero-form route", "S_kappa_top=int kappa_eff dA_3 -> d kappa_eff=0", "CONDITIONAL_ROUTE_EXISTS_NOT_PARENT_ADOPTED", "not a local positive operator; global/topological superselection route is cleaner", "source/Gauss Newton branch remains blocked", "residual_if_missing"),
        ("CERT2694_1_source_measure", "source_measure_and_Meff_flux", "Noether/Hilbert/worldtube charge closure", "M_eff=M_Hilbert=M_Gauss before orbital readout", "NOT_ATTEMPTED_HERE_PARALLEL_HELD", "depends on kappa and Pi_M/source-chain proofs", "measured Newton cannot be claimed", "residual_if_missing"),
        ("CERT2694_2_higher", "higher_derivative_public_metric", "operator exclusion or high-scale suppression", "DeltaE_HD=sum c_i O_i with eta_i~|c_i|/L^p", "FAIL_NO_OPERATOR_BASIS_UNITS_SCALE", "no parent-sourced basis/coefficient hierarchy", "Lovelock second-order clause fails", "nonclaim_bound_required"),
        ("CERT2694_3_aux", "auxiliary_private_vertical_fields", "positive source-free local operator", "L_X X=0 and int<X,L_X X>=positive+flux", "FAIL_FIELD_SPECIFIC_LX_NOT_INSTANTIATED", "1508 blocks generic positive-operator substitution", "metric-only clause fails", "nonclaim_bound_required"),
        ("CERT2694_4_projector", "domain_projector_selector", "chain-map/projector commutator zero", "[nabla,Pi_M]J_H=0 and delta_g Pi_M=0 in local branch", "FAIL_PROJECTOR_CHAIN_MAP_UNSIGNED", "domain no-vector/no-stress theorem not parent-derived", "source/PPN/WEP contamination remains", "nonclaim_bound_required"),
        ("CERT2694_5_boundary", "boundary_topological_terms", "fixed-before-readout zero flux", "int_boundary B_X=0 with reference/subtraction fixed before readout", "FAIL_ZERO_FLUX_REFERENCE_LOCK_UNSIGNED", "Ward ownership is not absence of force/flux", "mass/radial/PPN hair remains", "nonclaim_bound_required"),
        ("CERT2694_6_nonminimal", "nonminimal_source_geometry", "forbid or reclassify direct matter-MTS coupling", "no f(X,Phi)L_m or A(X)J_m unless universal/bounded", "FAIL_FORBID_THEOREM_UNSIGNED", "direct coupling would produce WEP/clock/R10 channels", "minimal coupling Lovelock source clause fails", "nonclaim_bound_required"),
        ("CERT2694_7_memory", "memory_coframe_preferred_frame", "stable local memory/frame-lock silence", "memory kernel becomes constant universal or positive-source-free silent locally", "FAIL_MEMORY_KERNEL_FRAME_LOCK_UNSIGNED", "double-zero is a requirement not a parent derivation", "preferred-frame/Gdot/clock channels remain", "nonclaim_bound_required"),
        ("CERT2694_8_nonlocal", "nonlocal_history_kernel", "locality reduction or kernel bound", "int K(t,t')O(t') -> local auxiliary or bounded tail", "FAIL_LOCALITY_REDUCTION_UNSIGNED", "no kernel decay/support bound", "locality Lovelock clause fails", "nonclaim_bound_required"),
        ("CERT2694_9_EH_core", "metric_EH_operator_core", "dominant EH normalization", "E_EH=a_EH(G+Lambda g) with parent a_EH/kappa owner", "DOMINANT_TEMPLATE_NOT_PARENT_NORMALIZED", "a_EH/G/source normalization remain open", "GR shape exists only conditionally", "normalization_required"),
        ("CERT2694_10_verdict", "all_sectors", "sector certificate pass", "all sectors theorem-zero, positive-silent, source-backed bounded, or reclassified", "CERTIFICATE_PASS_FAILS_CURRENT_CORPUS", "no sector is claim-ready; kappa has the cleanest next derivation route", "local GR/Newton remains blocked", "continue_derivation_queue"),
    ]
    return [
        {
            "certificate_id": row[0],
            "sector": row[1],
            "certificate_type": row[2],
            "formal_attempt": row[3],
            "current_status": row[4],
            "why_not_closed": row[5],
            "local_gr_effect": row[6],
            "fallback_class": row[7],
            "operator_written": "false" if row[0] not in {"CERT2694_0_kappa", "CERT2694_9_EH_core"} else "conditional_template",
            "sign_or_gap_known": "false",
            "source_charge_zero": "false",
            "boundary_flux_zero": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def operator_trial_rows() -> list[dict[str, Any]]:
    rows = [
        ("TRIAL2694_0_field_id", "field_id(X_a)", "name the parent field/component varied by the action", "MISSING_FOR_ALL_EXTRA_SECTORS_EXCEPT_CONDITIONAL_KAPPA_TEMPLATE", "blocks positive-operator zero"),
        ("TRIAL2694_1_euler_operator", "L_X", "extract operator from Euler equation or second variation", "MISSING_FIELD_SPECIFIC_OPERATOR", "generic Helmholtz/vector templates cannot pass"),
        ("TRIAL2694_2_domain_norm", "domain_and_inner_product", "positive self-adjoint domain after gauge/quotient", "MISSING_SIGNED_DOMAIN", "energy identity cannot be closed"),
        ("TRIAL2694_3_source_charge", "Q_X_source", "prove zero exterior source charge or provide value", "MISSING_ZERO_OR_VALUE", "nonzero source creates hair/fifth force"),
        ("TRIAL2694_4_test_readout", "q_test_X", "prove zero test/readout coupling or provide value", "MISSING_ZERO_OR_VALUE", "R10/PPN/clock readout cannot be set to zero"),
        ("TRIAL2694_5_boundary_flux", "boundary_flux/history", "prove zero boundary/history injection", "MISSING_SILENCE_PROOF", "positive identity still has surface/history leakage"),
        ("TRIAL2694_6_projection", "PiM_H_QX", "prove measured-G projection zero or provide coefficient", "MISSING_PROJECTION", "source normalization remains blocked"),
        ("TRIAL2694_7_acceptance", "sector_zero", "all field-specific trial clauses close", "BLOCKED", "no sector silence claim"),
    ]
    return [
        {
            "trial_id": row[0],
            "symbol": row[1],
            "requirement": row[2],
            "current_status": row[3],
            "effect": row[4],
            "accepted_now": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def residual_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ2694_0_kappa_drift", "delta_kappa_source", "dln_Geff_dt;partial_r_ln_Geff;partial_A_ln_Geff;alpha_kappa(lambda);frame/domain split", "kappa topological/global clause not parent adopted", "R1;R4;R9;R10;R11", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_VALUES"),
        ("REQ2694_1_source_measure", "delta_worldtube_Gauss", "Hilbert mass;worldtube charge;Gauss flux;orbital readout without backfill", "source-measure flux not closed", "Newton;orbital;Cavendish;PPN", "MISSING_CHARGE_GAUSS_EQUALITY"),
        ("REQ2694_2_higher", "c_HD_vector", "operator basis;coefficient units;local length scale;R10/PPN kernel", "higher derivative sector not zeroed", "R10;PPN;waves", "MISSING_OPERATOR_BASIS_UNITS_SCALE"),
        ("REQ2694_3_aux", "c_aux_private", "field id;L_X;Z_X;M_X^2;Q_X;boundary flux;projection", "field-specific positive operator not instantiated", "local_GR;PPN;clock", "MISSING_FIELD_SPECIFIC_CERTIFICATE"),
        ("REQ2694_4_projector", "c_projector_operator", "Pi_M chain map;commutator norm;delta_g Pi_M;source-measure kernel", "projector/domain theorem not signed", "WEP;Newton;PPN;orbital", "MISSING_PROJECTOR_NORM"),
        ("REQ2694_5_boundary", "c_boundary_reference", "boundary action;reference subtraction;flux integral;mass/PPN kernel", "zero flux/reference lock not signed", "Newton;clock;orbital;PPN", "MISSING_BOUNDARY_ZERO_OR_BOUND"),
        ("REQ2694_6_nonminimal", "c_nonminimal", "forbid theorem or coupling function;composition derivative;WEP/clock/R10 map", "nonminimal coupling not forbidden", "WEP;clock;PPN;R10", "MISSING_FORBID_OR_COUPLING_BOUND"),
        ("REQ2694_7_memory_frame", "c_memory_frame", "memory kernel;local frame lock;alpha_i projection;clock map", "memory/frame lock not derived", "PPN_alpha_i;clock;orbital", "MISSING_FRAME_LOCK_KERNEL"),
        ("REQ2694_8_nonlocal", "K_history", "kernel form;decay/support;locality limit;orbital/clock kernel", "nonlocal tail not reduced", "clock;orbital;cosmology", "MISSING_LOCALITY_REDUCTION"),
        ("REQ2694_9_total", "Delta_LHS_GR_abs", "absolute no-cancellation sum over all retained sector residuals", "component values and kernels missing", "all local arenas", "MISSING_COMPONENT_VALUES_AND_KERNELS"),
    ]
    return [
        {
            "requirement_id": row[0],
            "symbol": row[1],
            "required_inputs": row[2],
            "why_required": row[3],
            "observable_link": row[4],
            "current_status": row[5],
            "numeric_value_present": "false",
            "source_path_present": "true",
            "units_declared": "false",
            "kernel_declared": "false",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def local_gr_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("LGG2694_0_kappa", "constant universal kappa/G_eff", "CONDITIONAL_ROUTE_NOT_PARENT_ADOPTED", "kappa can be cleanly derived if topological/global sector is adopted, but current MTS has not earned it", "BLOCKS_MEASURED_GM_NEWTON"),
        ("LGG2694_1_sector_silence", "all non-EH sectors silent/bounded", "FAIL_CERTIFICATE_SET_INCOMPLETE", "sector certificates and residual values missing", "BLOCKS_LOVELOCK_METRIC_ONLY_SECOND_ORDER"),
        ("LGG2694_2_source_measure", "Hilbert/worldtube/Gauss source equality", "PARALLEL_HELD_BLOCKER", "source normalization remains required before Newton", "BLOCKS_INVERSE_SQUARE_NEWTON"),
        ("LGG2694_3_residual_envelope", "Delta_LHS_GR_abs has values/kernels", "FAIL_NONCLAIM_REQUIREMENTS", "absolute residual envelope is only symbolic", "BLOCKS_LOCAL_TEST_SCORING"),
        ("LGG2694_4_verdict", "local GR/Newton branch", "CLAIM_BLOCKED", "no sector has sufficient theorem-zero/value evidence", "MOVE_TO_KAPPA_FIRST"),
    ]
    return [
        {
            "gate_id": row[0],
            "gate": row[1],
            "current_status": row[2],
            "detail": row[3],
            "effect": row[4],
            "gate_pass": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2694_0_all_closed", "true", "true", "true", "true", "false", "false", "THEOREM_READY_IF_PARENT_SIGNED"),
        ("DRY2694_1_kappa_missing", "false", "true", "true", "true", "false", "false", "REJECT_KAPPA_OPEN"),
        ("DRY2694_2_sector_missing", "true", "false", "true", "true", "false", "false", "REJECT_SECTOR_CERTIFICATES_OPEN"),
        ("DRY2694_3_source_measure_missing", "true", "true", "false", "true", "false", "false", "REJECT_SOURCE_GAUSS_OPEN"),
        ("DRY2694_4_values_missing", "false", "false", "false", "false", "false", "false", "REJECT_NO_THEOREM_AND_NO_VALUES"),
        ("DRY2694_5_cancellation_only", "false", "false", "true", "true", "true", "false", "REJECT_CANCELLATION_ONLY_PASS"),
        ("DRY2694_6_fitted_gm", "true", "true", "false", "true", "false", "true", "REJECT_FITTED_GM_BACKFILL"),
    ]
    return [
        {
            "case_id": row[0],
            "kappa_closed": row[1],
            "sector_certificates_closed": row[2],
            "source_gauss_closed": row[3],
            "residual_values_or_zeros_present": row[4],
            "cancellation_only": row[5],
            "fitted_gm_backfill": row[6],
            "expected_status": row[7],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in cases
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["cancellation_only"] == "true":
        return "REJECT_CANCELLATION_ONLY_PASS"
    if case["fitted_gm_backfill"] == "true":
        return "REJECT_FITTED_GM_BACKFILL"
    if case["kappa_closed"] != "true" and case["residual_values_or_zeros_present"] != "true":
        return "REJECT_NO_THEOREM_AND_NO_VALUES"
    if case["kappa_closed"] != "true":
        return "REJECT_KAPPA_OPEN"
    if case["sector_certificates_closed"] != "true":
        return "REJECT_SECTOR_CERTIFICATES_OPEN"
    if case["source_gauss_closed"] != "true":
        return "REJECT_SOURCE_GAUSS_OPEN"
    return "THEOREM_READY_IF_PARENT_SIGNED"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        computed = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "computed_status": computed,
                "expected_status": case["expected_status"],
                "status_match": as_bool(computed == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2694_0_kappa", "constant kappa/G_eff parent-owned or residual values filled", "FAIL_KAPPA_PARENT_ADOPTION_UNSIGNED", "CERT2694_0_kappa;REQ2694_0_kappa_drift", "false"),
        ("CG2694_1_sector_certificates", "non-EH sectors have silence certificates", "FAIL_SECTOR_CERTIFICATE_PASS_FAILED", "CERT2694_10_verdict", "false"),
        ("CG2694_2_residual_values", "failed sectors have values, units, kernels and source paths", "FAIL_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM", "REQ2694_9_total", "false"),
        ("CG2694_3_source_gauss", "source-measure/worldtube/Gauss chain closed", "FAIL_PARALLEL_SOURCE_GAUSS_HELD", "CERT2694_1_source_measure", "false"),
        ("CG2694_4_no_cancellation", "absolute no-cancellation guard active", "PASS_GUARD_ONLY", "DRY2694_5_cancellation_only", "true"),
        ("CG2694_5_no_gm_backfill", "fitted orbital GM backfill refused", "PASS_GUARD_ONLY", "DRY2694_6_fitted_gm", "true"),
        ("CG2694_6_verdict", "local GR/Newton branch can claim pass", "CLAIM_BLOCKED", "CG2694_0 through CG2694_5", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "source_anchor": row[3],
            "gate_pass": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2694_0_sector_pass",
            "decision": "SECTOR_CERTIFICATE_PASS_BUILT_NOT_CLOSED",
            "reason": "Every retained sector now has a theorem-zero/value requirement, but no sector is claim-ready in the current corpus.",
            "status": "NONCLAIM_PROGRESS",
            "next_dependency": "prove or adopt the kappa topological/global parent clause first",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2694_1_kappa_first",
            "decision": "KAPPA_GEFF_IS_FIRST_REAL_STRIKE",
            "reason": "If kappa/G_eff is not constant and source-blind, measured GM, Newton, R10, Gdot and local GR remain contaminated regardless of EH operator work.",
            "status": "NEXT_ROUTE_SELECTED",
            "next_dependency": "2695 kappa topological superselection parent adoption or drift residual values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2694_2_topological_route",
            "decision": "TOPOLOGICAL_ZERO_FORM_ROUTE_IS_CLEAN_BUT_UNSIGNED",
            "reason": "The 508 route can derive d kappa=0 without a plateau axiom, but current MTS has not shown that this sector is in the parent action.",
            "status": "CONDITIONAL_DERIVATION_AVAILABLE",
            "next_dependency": "parent-action adoption/signature or drift/source/range residual rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2694_3_no_overview_loop",
            "decision": "DO_NOT_REOPEN_BROAD_LOVELOCK_OVERVIEW_NEXT",
            "reason": "2692 and 2693 already wrote the exact bridge; the forward move is closing the first sector in the queue.",
            "status": "ANTI_CIRCLING_GUARD",
            "next_dependency": "run 2695 kappa branch",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2694_0_selected",
            "kind": "selected",
            "target_doc": "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md",
            "target_script": "scripts/Y5_R2FR_kappa_topological_superselection_parent_adoption_or_drift_residual_values_2695.py",
            "purpose": "attempt to parent-sign the topological/global kappa sector that derives d kappa_eff=0; if not, fill explicit kappa drift/source/range/frame/domain residual value requirements",
            "acceptance_gate": "either kappa_eff is parent-owned as a global/topological superselection label with no local/source/range/frame/domain dependence, or drift residual rows remain explicit nonclaim inputs with units/kernels/source paths",
            "forbidden_shortcuts": "absorbing kappa drift into fitted GM; treating constant G as convention; cancellation-only pass; source-side cleanup as GR proof; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "target_id": "NEXT2694_1_held",
            "kind": "held_after_kappa",
            "target_doc": "2695b-Y5-R2FR-source-measure-Meff-flux-closure-after-kappa-gate.md",
            "target_script": "scripts/Y5_R2FR_source_measure_Meff_flux_closure_after_kappa_gate_2695b.py",
            "purpose": "after kappa is controlled, derive whether M_eff is the conserved parent source charge mapped to exterior Gauss flux",
            "acceptance_gate": "Hilbert source mass, parent charge, Pi_M flux and Gauss mass match before orbital readout",
            "forbidden_shortcuts": "using orbital GM as premise; hiding mu_extra/source flux",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2694_0_sectors", "sector certificates", "QUEUE_RESOLVED_TO_PRIORITIES", "each retained sector has explicit zero/bound/value requirements"),
        ("STATUS2694_1_kappa", "kappa/G_eff", "FIRST_TARGET_SELECTED", "topological global route exists conditionally but is not current parent proof"),
        ("STATUS2694_2_lovelock", "Lovelock/EH route", "STILL_BLOCKED_BY_SECTORS", "metric-only/second-order/local clauses remain unsigned"),
        ("STATUS2694_3_newton", "Newton/Poisson", "BLOCKED_BY_KAPPA_AND_SOURCE_GAUSS", "constant G and source mass equality both still required"),
        ("STATUS2694_4_claims", "claim status", "ALL_LOCAL_CLAIMS_BLOCKED", "no local-GR/Newton/PPN/R10/clock/orbital claim"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2695 kappa topological superselection or drift residual values",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2694_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    operator_trials: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    local_gr_gate: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    kappa_first = priority[0]["sector"] == "kappa_Geff_source_normalization" and priority[0]["priority"] == 1
    sector_attempts_cover = len(certificates) >= 10 and any(row["certificate_id"] == "CERT2694_10_verdict" and row["current_status"] == "CERTIFICATE_PASS_FAILS_CURRENT_CORPUS" for row in certificates)
    no_sector_promoted = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in certificates)
    operator_trials_block = any(row["trial_id"] == "TRIAL2694_7_acceptance" and row["current_status"] == "BLOCKED" for row in operator_trials)
    residuals_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["score_ready"] == "false"
        and row["numeric_value_present"] == "false"
        for row in residuals
    )
    local_gr_blocked = any(row["gate_id"] == "LGG2694_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in local_gr_gate)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2694_6_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2695" in read_text(OUTPUTS["next_target"]) and "kappa" in read_text(OUTPUTS["next_target"]).lower()
    checks = [
        ("VAL2694_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2694_kappa_first_selected", kappa_first, "kappa/G_eff is the first sector target"),
        ("VAL2694_sector_attempts_cover_queue", sector_attempts_cover and no_sector_promoted, "all sector attempts are represented and none are promoted"),
        ("VAL2694_field_specific_operator_trials_block", operator_trials_block, "field-specific L_X acceptance remains blocked"),
        ("VAL2694_residual_requirements_nonclaim", residuals_nonclaim, "residual value requirements remain nonclaim/not score-ready"),
        ("VAL2694_local_gr_gate_blocks", local_gr_blocked, "local-GR/Newton impact gate blocks promotion"),
        ("VAL2694_dryrun_refusals", dryrun_ok, "dry-run refuses open kappa, open sectors, source/Gauss gap, missing values, cancellation and fitted GM"),
        ("VAL2694_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2694_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2694_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2694_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2694_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2694_next_target_selected", next_target_ok, "2695 kappa topological superselection/drift residual target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2694_OVERALL",
            "passed": as_bool(overall),
            "detail": "2694 resolves the sector certificate queue into priorities, keeps all claims blocked, and selects kappa/G_eff as the first derivation target",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    operator_trials: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    local_gr_gate: list[dict[str, Any]],
    dry_cases: list[dict[str, Any]],
    dry_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2694 - Y5/R2FR Sector Positive-Operator Silence Certificates or Residual Values",
                "",
                "## Private Verdict",
                "",
                "This checkpoint stops the sector work from becoming a fog bank. Every retained local-GR blocker is forced into a certificate lane: theorem-zero, positive/source-free/zero-flux silence, source-backed bound, or explicit nonclaim residual value requirement.",
                "",
                "The sector pass does not close local GR. The only clean derivation lead is `kappa/G_eff`: 508 already gave a non-cheat topological zero-form route that would derive `d kappa_eff=0`, but current MTS has not parent-signed or adopted that sector. Because measured `GM`, Gdot, R10/range hair, source dependence, and Newton normalization all depend on this, 2694 selects kappa as the first real strike.",
                "",
                "No sector is promoted. No local-GR, Newton, PPN, WEP, clock, orbital, R10, GitHub, or public claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Sector Priority And Dependency Matrix",
                "",
                markdown_table(priority),
                "",
                "## Sector Certificate Attempt Matrix",
                "",
                markdown_table(certificates),
                "",
                "## Field-Specific Operator Trials",
                "",
                markdown_table(operator_trials),
                "",
                "## Residual Value Requirements",
                "",
                markdown_table(residuals),
                "",
                "## Local GR Impact Gate",
                "",
                markdown_table(local_gr_gate),
                "",
                "## Dry-Run Cases",
                "",
                markdown_table(dry_cases),
                "",
                "## Dry-Run Results",
                "",
                markdown_table(dry_results),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    for path in [RESIDUALS, LOCAL_BOUNDS, WEP_RESIDUALS, SOURCE_WEIGHT, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    priority = sector_priority_rows()
    certificates = certificate_attempt_rows()
    operator_trials = operator_trial_rows()
    residuals = residual_requirement_rows()
    local_gr_gate = local_gr_gate_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["sector_priority"], priority)
    write_csv(OUTPUTS["certificate_attempt"], certificates)
    write_csv(OUTPUTS["operator_trials"], operator_trials)
    write_csv(OUTPUTS["residual_requirements"], residuals)
    write_csv(OUTPUTS["local_gr_gate"], local_gr_gate)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_sector_priority"], priority)
    write_csv(BRANCH_OUTPUTS["local_certificate_attempt"], certificates)
    write_csv(BRANCH_OUTPUTS["local_residual_requirements"], residuals)
    write_csv(BRANCH_OUTPUTS["wep_residual_requirements"], residuals)
    write_csv(BRANCH_OUTPUTS["source_weight_residual_requirements"], residuals)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_target)

    branch_rows = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validation = validation_rows(
        source_rows=source_rows,
        priority=priority,
        certificates=certificates,
        operator_trials=operator_trials,
        residuals=residuals,
        local_gr_gate=local_gr_gate,
        dryrun_results=dry_results,
        claim_gates=claim_gates,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_document(
        source_rows=source_rows,
        priority=priority,
        certificates=certificates,
        operator_trials=operator_trials,
        residuals=residuals,
        local_gr_gate=local_gr_gate,
        dry_cases=dry_cases,
        dry_results=dry_results,
        claim_gates=claim_gates,
        decisions=decisions,
        next_target=next_target,
        status=status,
        validation=validation,
    )


if __name__ == "__main__":
    main()
