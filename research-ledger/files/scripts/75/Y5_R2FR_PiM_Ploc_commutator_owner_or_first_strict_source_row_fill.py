from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1654"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1654-Y5-R2FR-PiM-Ploc-commutator-owner-or-first-strict-source-row-fill.md"

SOURCE_FILES = {
    "1653_doc": ROOT / "1653-Y5-R2FR-Htau-Qtau-current-owner-or-source-measure-owner-first-row.md",
    "1653_validation": OUT / "P8_Y5_BRR545_1653_VALIDATION.csv",
    "1653_next": OUT / "P8_Y5_PARENT_QLOC_1653_NEXT_TARGET.csv",
    "1653_source_owner": OUT / "P8_Y5_PARENT_QLOC_1653_SOURCE_MEASURE_OWNER_GATE.csv",
    "1653_first_rows": OUT / "P8_Y5_PARENT_QLOC_1653_FIRST_SOURCE_ROW_LEDGER.csv",
    "1653_refusal": OUT / "P8_Y5_PARENT_QLOC_1653_OWNER_FIRST_ROW_REFUSAL_RUNNER.csv",
    "1652_mhref_gate": OUT / "P8_Y5_PARENT_QLOC_1652_MHREF_FIRST_ROW_GATE.csv",
    "1652_source_measure": OUT / "P8_Y5_PARENT_QLOC_1652_SOURCE_MEASURE_FLUX_CONTRACT.csv",
    "1647_hybrid": OUT / "P8_Y5_PARENT_QLOC_1647_HYBRID_CURRENT_OWNER_AUDIT.csv",
    "1648_flux_clause": OUT / "P8_Y5_PARENT_QLOC_1648_OBSERVED_FLUX_ZERO_CLAUSE_GATE.csv",
    "1648_component": OUT / "P8_Y5_PARENT_QLOC_1648_DELTAH_CURL_COMPONENT_FILL.csv",
    "ploc_1190": OUT / "P8_Y5_R10_1190_PLOC_PARENT_COMMUTATOR_GATE.csv",
    "ploc_1208_parallel": OUT / "P8_Y5_R10_1208_PLOC_PARALLEL_PROJECTOR_AUDIT.csv",
    "ploc_1208_bound": OUT / "P8_Y5_R10_1208_NABLAPLOC_BOUND_LAW.csv",
    "ploc_1208_row": OUT / "P8_Y5_R10_1208_SOURCE_READY_NABLAPLOC_ROW.csv",
    "ploc_1283": OUT / "P8_Y5_R10_1283_PLOC_PROJECTOR_OWNER_DERIVATION.csv",
    "pim_fork": OUT / "P8_Y5_PIM_PROJECTOR_OWNER_FORK.csv",
    "pim_contract": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
    "pim_flux_contract": OUT / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
    "pim_variation_contract": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "comm_zero_660": OUT / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
    "projector_stress_660": OUT / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
    "projector_913_zero": OUT / "P8_Y5_R10_913_PROJECTOR_ZERO_ROUTE_CLAUSES.csv",
    "projector_913_rows": OUT / "P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
    "projector_914_pack": OUT / "P8_Y5_R10_914_PROJECTOR_SOURCE_BOUND_PACK.csv",
    "r10_source_pack": OUT / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
    "queue_1653_owner": QUEUE / "JR1653_SOURCE_MEASURE_OWNER_GATE_NONCLAIM.csv",
    "queue_1653_first_rows": QUEUE / "JR1653_FIRST_SOURCE_ROW_LEDGER_NONCLAIM.csv",
}

NEEDLES = {
    "1653_doc": ["Pi_M/P_loc", "strict source row"],
    "1653_validation": ["VAL1653_OVERALL", "PASS"],
    "1653_next": ["1654-Y5-R2FR-PiM-Ploc-commutator-owner-or-first-strict-source-row-fill.md", "projector commutator ownership"],
    "1653_source_owner": ["SMO1653_3_commutator_closure", "NOT_PARENT_DERIVED"],
    "1653_first_rows": ["FSR1653_2_Bobs_zero_certificate", "FSR1653_3_Bobs_numeric_bound"],
    "1653_refusal": ["RUN1653_1_source_measure_owner", "REFUSE_SCORING"],
    "1652_mhref_gate": ["MHG1652_1_parent_current", "MISSING_PARENT_THETA_QTAU"],
    "1652_source_measure": ["SMF1652_1_PiM_Ploc_owner", "MISSING_PIM_PLOC_OWNER"],
    "1647_hybrid": ["HCO1647_6_source_projector_owner", "BLOCKED_BY_SOURCE_PROJECTOR_CHAIN"],
    "1648_flux_clause": ["OFC1648_5_projector_descent", "BLOCKED"],
    "1648_component": ["BCF1648_2_source_measure_flux", "MISSING_SOURCE_MEASURE_SILENCE_OR_NUMERIC"],
    "ploc_1190": ["PLC1190_2_derivative_commutator", "COMMUTATOR_RESIDUAL_RETAINED"],
    "ploc_1208_parallel": ["PPA1208_5_zero_verdict", "ZERO_NOT_CLAIMED_BOUND_ROUTE_SELECTED"],
    "ploc_1208_bound": ["NPL1208_2_fermi_curvature_bound", "BEST_NUMERIC_ROUTE_SOURCE_READY_NOT_CLAIM"],
    "ploc_1208_row": ["SRN1208_2_fermi_curvature_row", "BEST_SOURCE_ROW_FOR_NEXT_RUN_NONCLAIM"],
    "ploc_1283": ["POD1283_5_verdict", "PLOC_OWNER_NOT_CLOSED_BUT_BOUNDABLE"],
    "pim_fork": ["PF521_0_topological_absolute_PiM", "PF521_2_Hamiltonian_charge_PiM"],
    "pim_contract": ["PM6_flux_closure_requires_Ward_or_Euler", "not_parent_derived_next_target"],
    "pim_flux_contract": ["FC2_closed_mass_current_equation", "not_parent_derived"],
    "pim_variation_contract": ["PV0_product_variation_included", "PV8_retained_residual_fallback"],
    "comm_zero_660": ["CZ660_3_chain_map_property", "not_parent_derived"],
    "projector_stress_660": ["TPS660_0_commutator_integral", "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL"],
    "projector_913_zero": ["ZP913_4_chain_map_domain", "not_parent_derived"],
    "projector_913_rows": ["PSR913_4_projector_commutator", "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL"],
    "projector_914_pack": ["PSB914_4_I_commutator", "MISSING_CHAIN_MAP_DOMAIN_PROOF"],
    "r10_source_pack": ["BSM777_2_source_flux_value_input", "MISSING_SOURCE_FLUX_VALUE"],
    "queue_1653_owner": ["SMO1653_3_commutator_closure", "NOT_PARENT_DERIVED"],
    "queue_1653_first_rows": ["FSR1653_2_Bobs_zero_certificate", "FSR1653_3_Bobs_numeric_bound"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1654_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1654_INTAKE_SCAN.csv"
COMMUTATOR_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1654_PROJECTOR_COMMUTATOR_DERIVATION.csv"
OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1654_PIM_PLOC_OWNER_GATE.csv"
BOUND_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1654_PROJECTOR_BOUND_FORMULA_LEDGER.csv"
FIRST_ROW_FILL = OUT / "P8_Y5_PARENT_QLOC_1654_FIRST_STRICT_SOURCE_ROW_FILL_RUNNER.csv"
REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1654_COMMUTATOR_FIRST_ROW_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1654_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1654_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1654_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1654_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    COMMUTATOR_DERIVATION,
    OWNER_GATE,
    BOUND_LEDGER,
    FIRST_ROW_FILL,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    COMMUTATOR_DERIVATION,
    OWNER_GATE,
    BOUND_LEDGER,
    FIRST_ROW_FILL,
    REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    COMMUTATOR_DERIVATION: [
        QUARANTINE / "PROJECTOR_COMMUTATOR_DERIVATION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_projector_commutator_derivation_nonclaim_1654.csv",
        QUEUE / "JR1654_PROJECTOR_COMMUTATOR_DERIVATION_NONCLAIM.csv",
    ],
    OWNER_GATE: [
        QUARANTINE / "PIM_PLOC_OWNER_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_PiM_Ploc_owner_gate_nonclaim_1654.csv",
        QUEUE / "JR1654_PIM_PLOC_OWNER_GATE_NONCLAIM.csv",
    ],
    BOUND_LEDGER: [
        QUARANTINE / "PROJECTOR_BOUND_FORMULA_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_projector_bound_formula_ledger_nonclaim_1654.csv",
        QUEUE / "JR1654_PROJECTOR_BOUND_FORMULA_LEDGER_NONCLAIM.csv",
    ],
    FIRST_ROW_FILL: [
        QUARANTINE / "FIRST_STRICT_SOURCE_ROW_FILL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_first_strict_source_row_fill_runner_nonclaim_1654.csv",
        QUEUE / "JR1654_FIRST_STRICT_SOURCE_ROW_FILL_RUNNER_NONCLAIM.csv",
    ],
    REFUSAL_RUNNER: [
        QUARANTINE / "COMMUTATOR_FIRST_ROW_REFUSAL_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_commutator_first_row_refusal_runner_nonclaim_1654.csv",
        QUEUE / "JR1654_COMMUTATOR_FIRST_ROW_REFUSAL_RUNNER_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1654.csv",
        QUEUE / "JR1654_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, RAW, ACCEPTED, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "commutator_zero_claimed",
        "first_row_ready",
        "owner_ready",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
        "zero_claim_allowed",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1654 Pi_M/P_loc commutator owner or first strict source-row fill",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1654_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1654_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1654_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, role in scans:
        csv_count = len(list(folder.glob("*.csv"))) if folder.exists() else 0
        if folder == RAW and csv_count == 0:
            status = "NO_RAW_LIVE_ROWS"
        elif folder == ACCEPTED and csv_count == 0:
            status = "NO_ACCEPTED_LIVE_ROWS"
        elif folder == QUEUE and csv_count:
            status = "QUEUE_PRESENT_NONCLAIM"
        else:
            status = "LIVE_ROWS_REQUIRE_REVIEW"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_role": role,
                "folder_path": str(folder),
                "csv_count": csv_count,
                "status": status,
                "source_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def commutator_derivation_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PCD1654_0_product_rule",
            "d(Pi_M J_H)",
            "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "DERIVED_IDENTITY",
            "if dJ_H=0, only [d,Pi_M]J_H and boundary/domain terms remain",
            "does not prove [d,Pi_M]J_H=0",
        ),
        (
            "PCD1654_1_Ploc_divergence",
            "nabla_mu(P_loc K) split",
            "nabla_mu(P_loc^nu_rho K^{mu rho})=P_loc^nu_rho nabla_mu K^{mu rho}+(nabla_mu P_loc^nu_rho)K^{mu rho}",
            "DERIVED_IDENTITY",
            "projected local zero needs nabla P_loc silence or retained bound",
            "does not prove nabla_mu P_loc=0",
        ),
        (
            "PCD1654_2_parallel_projector_condition",
            "nabla P_loc zero condition",
            "P^2=P implies P(nabla P)P=0 and derivative leakage is off-diagonal; zero requires parallel image/kernel split",
            "DERIVED_CONDITION",
            "P_loc silence is reducible to parallel splitting/coframe/domain/connection input",
            "current corpus lacks parent-signed parallel splitting",
        ),
        (
            "PCD1654_3_finite_domain_bound",
            "finite-domain P_loc drift",
            "||nabla P_loc|| <= C_Fermi L_D||Riemann|| + C_Fermi2 L_D^2||nabla Riemann|| on a Fermi/local domain",
            "BOUND_ROUTE_SELECTED",
            "finite local domains can be bounded instead of axiomatically zeroed",
            "needs L_D, curvature norms, constants, and source path",
        ),
        (
            "PCD1654_4_PiM_chain_map",
            "Pi_M commutator zero condition",
            "[d,Pi_M]J_H=0 requires a parent-owned chain map on the allowed Hilbert/source-current complex",
            "NOT_PARENT_DERIVED",
            "Pi_M cannot be fitted/readout-selected after the fact",
            "current corpus has topological/Hamiltonian candidates only",
        ),
        (
            "PCD1654_5_verdict",
            "commutator owner theorem",
            "Pi_M/P_loc source-measure zero is claimable only if Pi_M chain-map, P_loc parallel/domain, boundary no-flux, and M_H_ref all close",
            "ZERO_NOT_CLAIMED",
            "the proof route is sharper but still incomplete",
            "convert to source-row bound if zero theorem fails",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "derivation_id": derivation_id,
            "object": object_name,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "progress": progress,
            "remaining_blocker": blocker,
            "commutator_zero_claimed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for derivation_id, object_name, mathematical_form, current_status, progress, blocker in rows
    ]


def owner_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "POG1654_0_parent_domain",
            "compact exterior/domain/S2 class selected before readout",
            "Sigma_ext, boundary, normal, annulus, and homology class are parent-owned",
            "MISSING_PARENT_DOMAIN_SELECTOR",
            "domain motion can generate source flux",
        ),
        (
            "POG1654_1_PiM_chain_map",
            "Pi_M is a chain map on allowed source currents",
            "[d,Pi_M]J_H=0 for J_H in domain(Pi_M)",
            "NOT_PARENT_DERIVED",
            "I_commutator remains a retained residual",
        ),
        (
            "POG1654_2_Hilbert_topological_equality",
            "closed mass current equals observed Hilbert Pi_M source current",
            "J_M_top = Pi_M J_H + dB_zero with zero boundary flux",
            "NOT_DERIVED_KEY_BLOCKER",
            "zeroing a topological current may zero the wrong current",
        ),
        (
            "POG1654_3_Ploc_parallel_owner",
            "P_loc image/kernel split is parallel in the same observed connection/domain",
            "nabla P_loc=0 or finite source-backed nabla P_loc bound is present",
            "ZERO_NOT_CLAIMED_BOUNDABLE",
            "P_loc derivative leakage stays live",
        ),
        (
            "POG1654_4_boundary_no_flux",
            "compact boundary/corner/projector flux vanishes or is source bounded",
            "integral_boundary Pi_M K_owner = 0 or explicit B_P_flux/M_H_ref row exists",
            "BOUNDARY_NO_FLUX_UNSIGNED",
            "boundary-only mass/source hair can survive",
        ),
        (
            "POG1654_5_MHref_join",
            "projector/source flux is normalized by same-frame M_H_ref",
            "all projector/source terms use the 1653/1654 Hamiltonian denominator",
            "BLOCKED_BY_MHREF",
            "no dimensionless local bound without denominator",
        ),
        (
            "POG1654_6_owner_verdict",
            "accept Pi_M/P_loc commutator owner",
            "POG1654_0 through POG1654_5 pass jointly",
            "OWNER_NOT_ACCEPTED",
            "projector owner route remains alive but nonclaim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "needed_clause": clause,
            "mathematical_test": test,
            "current_status": status,
            "blocker": blocker,
            "required_source_fields": "system_id;domain_id;Pi_M_owner;P_loc_owner;chain_map_status;nabla_Ploc_bound;I_commutator;B_P_flux;M_H_ref;units;source_path;valid_for_claim",
            "owner_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, clause, test, status, blocker in rows
    ]


def bound_ledger_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PBL1654_0_I_commutator",
            "I_commutator",
            "abs(integral_A [d,Pi_M]J_H)/M_H_ref",
            "chain-map theorem or sourced commutator integral",
            "MISSING_CHAIN_MAP_DOMAIN_PROOF_OR_NUMERIC_INTEGRAL",
        ),
        (
            "PBL1654_1_nabla_Ploc",
            "nabla_Ploc_Linf",
            "C_Fermi L_D||Riemann|| + C_Fermi2 L_D^2||nabla Riemann||",
            "finite-domain Fermi curvature row or parallel splitting theorem",
            "MISSING_LD_CURVATURE_CONSTANTS_SOURCE_PATH",
        ),
        (
            "PBL1654_2_projector_stress",
            "T_PiM or q_P",
            "P_loc nabla_mu T_projector^{mu nu} mapped to local response",
            "projector stress map or metric-independent no-stress theorem",
            "MISSING_PROJECTOR_STRESS_MAP",
        ),
        (
            "PBL1654_3_boundary_flux",
            "B_P_flux",
            "abs(integral_boundary Pi_M K_owner)/M_H_ref",
            "boundary no-flux theorem or sourced compact-boundary flux",
            "MISSING_BOUNDARY_NO_FLUX_INPUT",
        ),
        (
            "PBL1654_4_joined_bound",
            "B_obs_projector_source_over_MH",
            "C_comm I_commutator + C_P ||nabla P_loc||||K||/M_H_ref + B_P_flux/M_H_ref + readout terms",
            "all component rows with units, coefficients, source paths, no cancellation",
            "MISSING_MHREF_AND_COMPONENT_ROWS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "quantity": quantity,
            "formula": formula,
            "needed_input": needed_input,
            "current_status": status,
            "units": "dimensionless_after_M_H_ref_or_declared_projector_norm",
            "accepted_for_scoring": False,
            "valid_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bound_id, quantity, formula, needed_input, status in rows
    ]


def first_row_fill_rows() -> list[dict[str, object]]:
    raw_count = len(list(RAW.glob("*.csv"))) if RAW.exists() else 0
    accepted_count = len(list(ACCEPTED.glob("*.csv"))) if ACCEPTED.exists() else 0
    rows = [
        (
            "FRF1654_0_MHref",
            "M_H_ref source row",
            "system_id;tau_id;surface_outer;H_tau;H_ref;M_H_ref;uncertainty;units;reference_rule;same_frame_lock;source_path;valid_for_claim",
            "MISSING_H_TAU;MISSING_H_REF;MISSING_MHREF_VALUE;MISSING_UNITS;MISSING_SOURCE_PATH;NO_ORBITAL_GM_IMPORT",
        ),
        (
            "FRF1654_1_commutator_zero",
            "Pi_M/P_loc commutator zero certificate",
            "system_id;domain_id;Pi_M_owner;P_loc_owner;chain_map_proof;nabla_Ploc_zero;boundary_no_flux;source_path;valid_for_claim",
            "MISSING_PIM_CHAIN_MAP;MISSING_PLOC_PARALLEL_OWNER;MISSING_BOUNDARY_NO_FLUX;MISSING_SOURCE_PATH",
        ),
        (
            "FRF1654_2_commutator_numeric",
            "I_commutator numeric/source bound",
            "system_id;annulus;I_commutator;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_I_COMMUTATOR;MISSING_MHREF;MISSING_UNITS;MISSING_SOURCE_PATH",
        ),
        (
            "FRF1654_3_nabla_Ploc_bound",
            "nabla_Ploc finite-domain bound row",
            "domain_id;L_D;Riemann_norm;nabla_Riemann_norm;C_Fermi;C_Fermi2;nabla_Ploc_bound;units;source_path;valid_for_claim",
            "MISSING_DOMAIN;MISSING_LD;MISSING_CURVATURE_NORMS;MISSING_CONSTANTS;MISSING_SOURCE_PATH",
        ),
        (
            "FRF1654_4_Bobs_total",
            "B_obs source/projector no-cancellation total",
            "component_id;value;units;M_H_ref;coefficient;source_path;no_cancellation_flag;valid_for_claim",
            "MISSING_COMPONENT_ROWS;MISSING_MHREF;MISSING_COEFFICIENTS;MISSING_NO_CANCELLATION_VECTOR",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target_quantity": target_quantity,
            "required_columns": required_columns,
            "missing_fields": missing_fields,
            "raw_csv_count": raw_count,
            "accepted_csv_count": accepted_count,
            "row_status": "NO_FILL_ACCEPTED_STRICT_TEMPLATE_ONLY",
            "accepted_for_scoring": False,
            "first_row_ready": False,
            "valid_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, target_quantity, required_columns, missing_fields in rows
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1654_0_commutator_zero", "Pi_M/P_loc source-measure zero theorem", "REFUSE_SCORING", "MISSING_PIM_CHAIN_MAP;MISSING_HILBERT_TOPOLOGICAL_EQUALITY;MISSING_PLOC_PARALLEL_OWNER;MISSING_BOUNDARY_NO_FLUX;MISSING_MHREF"),
        ("RUN1654_1_commutator_bound", "projector/source-measure finite bound", "REFUSE_SCORING", "MISSING_I_COMMUTATOR;MISSING_NABLAPLOC_VALUES;MISSING_PROJECTOR_STRESS_MAP;MISSING_BOUNDARY_FLUX;MISSING_MHREF;MISSING_UNITS"),
        ("RUN1654_2_first_row_fill", "strict M_H_ref/B_obs first-row fill", "REFUSE_SCORING", "NO_RAW_OR_ACCEPTED_VALID_ROWS;TEMPLATES_ONLY"),
        ("RUN1654_3_local_branch", "local_GR_Newton_PPN_R10_WEP", "REFUSE_SCORING", "COMMUTATOR_OWNER_NOT_ACCEPTED;FIRST_ROWS_NOT_ACCEPTED;NO_LOCAL_CLAIM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": run_id,
            "quantity": quantity,
            "runner_decision": decision,
            "refusal_reasons": reasons,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for run_id, quantity, decision, reasons in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1654_0_commutator_zero", "Pi_M/P_loc commutator source-measure zero is proved", False, "BLOCKED", "owner and boundary clauses are unsigned"),
        ("CG1654_1_bound", "finite projector/source-measure bound is source-backed", False, "BLOCKED", "numeric rows and M_H_ref are missing"),
        ("CG1654_2_first_rows", "one strict M_H_ref/B_obs row is accepted", False, "BLOCKED", "raw/accepted live folders contain no valid source rows"),
        ("CG1654_3_local_GR", "local GR/Newton/PPN/R10/WEP follows from 1654", False, "NO_CLAIM", "1654 is a source-row and commutator gate only"),
        ("CG1654_4_guardrail", "1654 commutator/source-row gate installed", "INTERNAL_ONLY", "PASS_AS_INTERNAL_GUARDRAIL_ONLY", "guardrail is not evidence"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1654_0_commutator_identity", "COMMUTATOR_LAW_DERIVED_NOT_ZERO", "product-rule and P_loc derivative identities identify the exact leakage terms", "retain [d,Pi_M]J_H and nabla P_loc terms unless parent-zero or source bounds arrive"),
        ("DEC1654_1_zero_route", "PROJECTOR_ZERO_ROUTE_NOT_CLOSED", "Pi_M chain-map, Hilbert/topological equality, P_loc parallel split, boundary no-flux, and M_H_ref are not jointly signed", "do not promote source-measure zero"),
        ("DEC1654_2_bound_route", "BOUND_ROUTE_IS_BEST_NEXT_SOURCE_LANE", "1208/1283 already reduce P_loc uncertainty to finite-domain curvature/parallel-splitting inputs", "prioritize nabla_Ploc/I_commutator/M_H_ref rows"),
        ("DEC1654_3_next", "NEXT_1655_NABLAPLOC_ICOMM_MHREF_SOURCE_ROW", "the next smallest real progress is a source-ready bound row for nabla_Ploc or I_commutator, joined to M_H_ref", "select 1655 projector-gradient/commutator source row or M_H_ref denominator fill"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1655-Y5-R2FR-nablaPloc-Icommutator-bound-row-or-MHref-denominator-fill.md",
            "script": "scripts/Y5_R2FR_nablaPloc_Icommutator_bound_row_or_MHref_denominator_fill.py",
            "objective": "try to fill one source-ready bound row for nabla_Ploc or I_commutator, or a same-frame M_H_ref denominator row; otherwise keep all local claims blocked with exact missing inputs",
            "success_condition": "one row obtains numeric/sourced units and valid_for_claim=true without orbital-GM import, or every candidate remains valid_for_claim=false with precise blockers",
            "forbidden_shortcuts": "no orbital-GM denominator; no source-measure zero without Pi_M/P_loc owner; no cancellation; no local-GR/PPN/R10/WEP claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, intake_rows, commutator, owner_gate, bound_ledger, first_rows, refusal, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1654_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1654 source paths exist and needles are present"),
        ("VAL1654_1_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1654_2_commutator_identity_written", any(row["current_status"] == "DERIVED_IDENTITY" for row in commutator) and any(row["current_status"] == "ZERO_NOT_CLAIMED" for row in commutator), "commutator/product-rule law is written but zero is not claimed"),
        ("VAL1654_3_owner_gate_blocked", len(owner_gate) == 7 and any(row["current_status"] == "OWNER_NOT_ACCEPTED" for row in owner_gate), "Pi_M/P_loc owner gate is complete and blocked"),
        ("VAL1654_4_bound_ledger_ready", len(bound_ledger) == 5 and all(row["accepted_for_scoring"] is False for row in bound_ledger), "projector bound formulas are staged as nonclaim rows"),
        ("VAL1654_5_first_rows_refused", len(first_rows) == 5 and all(row["row_status"] == "NO_FILL_ACCEPTED_STRICT_TEMPLATE_ONLY" for row in first_rows), "strict source-row fill runner accepts no current rows"),
        ("VAL1654_6_refusal_runner_blocks", len(refusal) == 4 and all(row["runner_decision"] == "REFUSE_SCORING" for row in refusal), "refusal runner blocks all current lanes"),
        ("VAL1654_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1654_8_next_target_selected", next_targets[0]["next_target"] == "1655-Y5-R2FR-nablaPloc-Icommutator-bound-row-or-MHref-denominator-fill.md", "next target selects projector-gradient/commutator source row or M_H_ref denominator fill"),
        ("VAL1654_9_csv_parse", generated_csv_parse, "all generated 1654 CSVs parse"),
        ("VAL1654_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1654 generated rows keep MTS claim/no-score flags false"),
        ("VAL1654_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1654_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1654_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1654_14_formalization_untouched", not formalization_dirty, "no 1654 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1654_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1654 Pi_M/P_loc commutator owner or first strict source-row fill validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(source_rows, intake_rows, commutator, owner_gate, bound_ledger, first_rows, refusal, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1654 - PiM Ploc Commutator Owner Or First Strict Source Row Fill

**Private status:** nonclaim commutator/source-row gate. No `Pi_M/P_loc` owner, source-measure zero, `M_H_ref`, `B_obs_source_measure_over_MH`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

`1654` gets the projector/source-measure obstruction into its smallest honest mathematical form:

```text
d(Pi_M J_H) = Pi_M dJ_H + [d, Pi_M]J_H
nabla_mu(P_loc K) = P_loc nabla_mu K + (nabla_mu P_loc)K
```

This is real progress because it separates the two ways the local branch can fail: a mass-current commutator `I_commutator`, or a local projection drift `nabla P_loc`. Existing `1208/1283` work already makes the `P_loc` side boundable by finite-domain curvature or parallel-splitting data.

But the zero theorem does **not** close. `Pi_M` is not yet a parent-signed chain map on the observed Hilbert/source-current complex, `P_loc` is not yet a parent-signed parallel projector on the same domain/connection, boundary no-flux is unsigned, and `M_H_ref` is still missing. Therefore the runner refuses local scoring and stages the next source-row lane.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## Projector Commutator Derivation

{markdown_table(commutator, ["derivation_id", "object", "mathematical_form", "current_status", "remaining_blocker"])}

## PiM/Ploc Owner Gate

{markdown_table(owner_gate, ["gate_id", "needed_clause", "mathematical_test", "current_status", "blocker"])}

## Bound Formula Ledger

{markdown_table(bound_ledger, ["bound_id", "quantity", "formula", "needed_input", "current_status"])}

## First Strict Source Row Fill Runner

{markdown_table(first_rows, ["row_id", "target_quantity", "missing_fields", "raw_csv_count", "accepted_csv_count", "row_status"])}

## Refusal Runner

{markdown_table(refusal, ["run_id", "quantity", "runner_decision", "refusal_reasons"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The coupling bottleneck has now split into a theorem route and a data route. The theorem route needs `Pi_M` to be a parent-owned chain map and `P_loc` to be a parent-owned parallel/readout projector. The data route needs source-backed values for `I_commutator`, `nabla P_loc`, boundary flux, and `M_H_ref`. Until one of those routes closes, the local-GR reduction remains disciplined but unclaimed.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    intake_rows = intake_scan_rows()
    commutator = commutator_derivation_rows()
    owner_gate = owner_gate_rows()
    bound_ledger = bound_ledger_rows()
    first_rows = first_row_fill_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (INTAKE_SCAN, intake_rows),
        (COMMUTATOR_DERIVATION, commutator),
        (OWNER_GATE, owner_gate),
        (BOUND_LEDGER, bound_ledger),
        (FIRST_ROW_FILL, first_rows),
        (REFUSAL_RUNNER, refusal),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, intake_rows, commutator, owner_gate, bound_ledger, first_rows, refusal, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, commutator, owner_gate, bound_ledger, first_rows, refusal, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1654 validation failed; see P8_Y5_BRR545_1654_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1654 validation PASS")


if __name__ == "__main__":
    main()
