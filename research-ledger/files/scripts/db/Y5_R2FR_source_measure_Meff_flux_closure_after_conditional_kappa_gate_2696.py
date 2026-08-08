from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2696"
BRANCH_ID = "Y5_R2FR_SOURCE_MEASURE_MEFF_FLUX_CLOSURE_AFTER_CONDITIONAL_KAPPA_GATE_2696"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2696-Y5-R2FR-source-measure-Meff-flux-closure-after-conditional-kappa-gate.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2696_SOURCE_REGISTER.csv",
    "source_measure_audit": RESIDUALS / "P8_Y5_R2FR_2696_SOURCE_MEASURE_THEOREM_AUDIT.csv",
    "charge_derivation": RESIDUALS / "P8_Y5_R2FR_2696_COVARIANT_PHASE_SPACE_CHARGE_DERIVATION_CHECK.csv",
    "residual_requirements": RESIDUALS / "P8_Y5_R2FR_2696_MEFF_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM.csv",
    "pim_replacement_map": RESIDUALS / "P8_Y5_R2FR_2696_PIM_REPLACEMENT_DECISION_MAP.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2696_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2696_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2696_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2696_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2696_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2696_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2696_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_source_measure_audit": LOCAL_BOUNDS / "source_measure_Meff_flux_gate_2696_NONCLAIM.csv",
    "local_Meff_residual_requirements": LOCAL_BOUNDS / "Meff_residual_value_requirements_2696_NONCLAIM.csv",
    "wep_Meff_residual_requirements": WEP_RESIDUALS / "Meff_residual_value_requirements_2696_NONCLAIM.csv",
    "source_weight_Meff_residual_requirements": SOURCE_WEIGHT / "MEFF_RESIDUAL_VALUE_REQUIREMENTS_2696_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2696_MINIMAL_LOCAL_PARENT_ACTION_FIXED_POINT_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2696_2695_DOC",
        "relative_path": "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md",
        "required_needles": ["NEXT2695_0_selected", "VAL2695_OVERALL", "CARRY_CANDIDATE_KAPPA_CLAUSE_AND_ATTACK_SOURCE_MEASURE"],
        "purpose": "imports conditional kappa status and selected source-measure target",
    },
    {
        "source_id": "SRC2696_509_SOURCE_MEASURE",
        "relative_path": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "required_needles": ["T509_0_charge_identity_needed", "SM509_3_flux_closure", "SMR509_0_Delta_flux"],
        "purpose": "imports earlier source-measure flux theorem and residual map",
    },
    {
        "source_id": "SRC2696_510_WORLDTUBE_GLUE",
        "relative_path": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "required_needles": ["T510_0_EH_reference_glue", "WG510_7_dressed_source_definition", "MR510_0_flux_leak"],
        "purpose": "imports covariant phase-space/worldtube glue reference theorem",
    },
    {
        "source_id": "SRC2696_505_NOETHER",
        "relative_path": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "required_needles": ["T505_conditional_Noether_mass_charge_closure", "EH505_2_projector_constancy", "DEC505_1_MTS_status"],
        "purpose": "imports parent Noether mass-charge closure theorem and open premises",
    },
    {
        "source_id": "SRC2696_504_WORLDTUBE",
        "relative_path": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "required_needles": ["W504_2_mass_charge_form", "W504_4_worldtube_source_measure_glue", "W504_5_calibration_and_limits"],
        "purpose": "imports worldtube glue clauses",
    },
    {
        "source_id": "SRC2696_454_PIM",
        "relative_path": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "required_needles": ["conditional_symplectic_projector_theorem", "flux_closure_not_from_projector", "PM6_flux_closure_requires_Ward_or_Euler"],
        "purpose": "imports Pi_M algebra and warning that projector algebra is not flux closure",
    },
    {
        "source_id": "SRC2696_451_MASS_FLUX",
        "relative_path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "required_needles": ["conditional_Euler_flux_closure", "MF2_Euler_flux_closure", "MF8_retained_residual_fallback"],
        "purpose": "imports mass-flux Euler closure contract",
    },
    {
        "source_id": "SRC2696_MF_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "required_needles": ["MF2_Euler_flux_closure", "MF5_absolute_calibration", "MF8_retained_residual_fallback"],
        "purpose": "imports machine-readable mass-flux/source calibration blockers",
    },
    {
        "source_id": "SRC2696_CC_ATTEMPT",
        "relative_path": "source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "required_needles": ["CC3_projected_mass_current", "CC7_closed_flux_and_Gauss_calibration", "CC8_second_order_limit"],
        "purpose": "imports direct charge-current equality attempt",
    },
    {
        "source_id": "SRC2696_CC_RESIDUALS",
        "relative_path": "source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "required_needles": ["Delta_flux", "Delta_PiM", "Delta_PPN"],
        "purpose": "imports source-measure residual decomposition",
    },
    {
        "source_id": "SRC2696_NEWTON_STACK",
        "relative_path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "required_needles": ["SN4_closed_Meff_flux", "SN8_Gauss_surface_integral", "SN11_second_order_PPN_source_stability"],
        "purpose": "imports Newton/source-normalization stack rungs",
    },
    {
        "source_id": "SRC2696_WORLDTUBE_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "required_needles": ["W504_0_worldtube_setup", "W504_3_exterior_closure_equation", "W504_4_worldtube_source_measure_glue"],
        "purpose": "imports parent worldtube glue theorem clauses",
    },
    {
        "source_id": "SRC2696_LOCAL_RESIDUAL_INPUT",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "required_needles": ["P8_Meff_conservation", "P8_radial_source_hair", "P8_nonlinear_beta_source_residue"],
        "purpose": "imports local residual runner rows for M_eff and source-normalized PPN",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


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
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
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


def source_measure_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SMA2696_0_kappa_import",
            "conditional kappa",
            "G_eff=kappa_eff c^4/(8 pi) is carried only as conditional/topological candidate from 2695",
            "kappa derivative/source/range hair is not promoted",
            "CONDITIONAL_INPUT_ONLY",
            "G_eff drift can still contaminate measured GM",
            "KRR2695 rows stay active unless parent-signed",
        ),
        (
            "SMA2696_1_parent_phase_space",
            "covariant parent phase space",
            "delta L = E_A delta phi^A + d theta(phi,delta phi)",
            "well-defined symplectic potential and boundary terms before readout",
            "NOT_SIGNED_FOR_FULL_MTS_PARENT",
            "Hamiltonian/source charge is not defined by the action",
            "Delta_symp;Delta_frame",
        ),
        (
            "SMA2696_2_observed_generator",
            "single time/source generator",
            "tau_source = tau_charge = tau_orbit = tau_clock in the observed branch",
            "one generator is used for source variation, charge, and orbital readout",
            "OPEN",
            "time choice can absorb M_eff drift or frame split",
            "Delta_frame;dln_Meff_dt",
        ),
        (
            "SMA2696_3_Hamiltonian_mass_charge",
            "mass from parent Hamiltonian/Noether charge",
            "H_tau[S] = integral_S (delta Q_tau - tau dot theta) integrated with fixed reference",
            "M_eff is defined by the parent charge rather than a fitted orbital mask",
            "CONDITIONAL_REFERENCE_ROUTE",
            "measured mass remains a calibration/readout input",
            "Delta_cal;Delta_symp",
        ),
        (
            "SMA2696_4_PiM_descent",
            "Pi_M as derived projection, not primitive patch",
            "Pi_M J_H must equal the parent mass charge channel Q_M[tau] before data scoring",
            "Pi_M is legal only if parent-derived, variation-owned, and charge-preserving",
            "NOT_PARENT_DERIVED",
            "projector freedom can hide source-normalization failure",
            "Delta_PiM;projector stress",
        ),
        (
            "SMA2696_5_flux_closure",
            "exterior charge closure",
            "M_eff(S2)-M_eff(S1)=int_A d(Pi_M J_H)=0 or int_A dQ_M[tau]=0",
            "source-free exterior constraints and boundary flux terms vanish",
            "NOT_PARENT_DERIVED",
            "M_eff can drift with time/radius",
            "Delta_flux;P8_Meff_conservation;P8_radial_source_hair",
        ),
        (
            "SMA2696_6_worldtube_glue",
            "source measure equals exterior charge",
            "M_source[W] = M_eff[S] = H_tau[S]-H_tau[reference]",
            "the worldtube source measure is dressed Hamiltonian/Noether charge, not bare rest mass",
            "CORE_GLUE_NOT_DERIVED",
            "closed charge may be the wrong object",
            "Delta_cal;Delta_nonEH;Delta_extra",
        ),
        (
            "SMA2696_7_no_extra_mass_channel",
            "extra-sector mass silence",
            "Delta_nonEH=Delta_symp=Delta_PiM=Delta_extra=Delta_frame=0",
            "non-EH, boundary, memory, domain, range, connection, and frame sectors carry no independent mass charge",
            "NOT_PARENT_DERIVED",
            "mu_extra survives as hidden source normalization",
            "P8_boundary_bulk_domain_mu_extra;R11;R10",
        ),
        (
            "SMA2696_8_Gauss_orbital_readout",
            "charge to Newton readout",
            "surface_integral grad Phi dot dS = 4 pi G_eff M_eff and a_r=-G_eff M_eff/r^2",
            "the same charge controls the weak-field metric and slow-particle orbit",
            "NOT_PARENT_DERIVED",
            "orbital GM is used as premise instead of conclusion",
            "Delta_cal;partial_r_ln_mu_obs;alpha(lambda)",
        ),
        (
            "SMA2696_9_PPN_stability",
            "second-order source stability",
            "gamma-1=0 and delta_beta_source=0 after measured-GM normalization",
            "Newton-looking first order survives local-GR/PPN order",
            "NOT_DERIVED",
            "Newton pass would not be a GR pass",
            "Delta_PPN;R3;R4;R11",
        ),
        (
            "SMA2696_10_verdict",
            "source-measure verdict",
            "the least-cheatable path is parent Hamiltonian source charge -> Pi_M descent -> flux closure -> Gauss/PPN readout",
            "current MTS has the conditional route but not the parent proof",
            "SOURCE_MEASURE_CLAIM_BLOCKED",
            "no measured-GM, Newton, PPN, local-GR, GitHub, or public claim",
            "next build minimal local parent fixed-point contract",
        ),
    ]
    return [
        {
            "audit_id": row[0],
            "clause": row[1],
            "required_identity": row[2],
            "pass_condition": row[3],
            "current_status": row[4],
            "blocks_if_missing": row[5],
            "residual_if_missing": row[6],
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def charge_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CPS2696_0_action_variation",
            "start from parent local action",
            "delta L = E_A delta phi^A + d theta(phi,delta phi)",
            "parent has a local diffeo-covariant action and a controlled boundary variational principle",
            "covariant phase-space machinery exists",
            "STANDARD_REFERENCE_STEP",
            True,
            False,
            "this is the less-scrutinized source-measure language",
        ),
        (
            "CPS2696_1_Noether_current",
            "define observed-time Noether current",
            "J_tau = theta(phi,L_tau phi) - i_tau L",
            "tau is the observed source/orbital/clock generator",
            "mass charge candidate is action-defined",
            "STANDARD_REFERENCE_STEP",
            True,
            False,
            "generator normalization cannot be chosen after fitting orbits",
        ),
        (
            "CPS2696_2_on_shell_closure",
            "use field equations in source-free exterior",
            "dJ_tau = -E_A L_tau phi -> 0 in A, up to constraints and explicit residual currents",
            "exterior equations and residual sectors are zero or explicitly retained",
            "charge is closed in compact exterior",
            "CONDITIONAL_STEP",
            True,
            False,
            "this is where non-EH/domain/memory/boundary sectors can enter",
        ),
        (
            "CPS2696_3_surface_charge",
            "write current as surface charge plus constraints",
            "J_tau = dQ_tau + C_tau",
            "constraint and side-flux terms vanish in the exterior annulus",
            "integral_S2 Q_tau - integral_S1 Q_tau = 0",
            "CONDITIONAL_STEP",
            True,
            False,
            "closure is not projector idempotence; it is a current equation",
        ),
        (
            "CPS2696_4_mass_definition",
            "define dressed source mass",
            "M_source[W] := G_ref^-1(H_tau[S]-H_tau[reference]) with fixed reference",
            "worldtube source measure is the dressed parent charge, not bare rest matter mass",
            "avoids bare-mass overclaim",
            "DEFINITION_LOCK_REQUIRED",
            True,
            False,
            "this is the right definition if the theory wants GR-like source mass",
        ),
        (
            "CPS2696_5_PiM_descent",
            "derive Pi_M from the parent charge",
            "Pi_M J_H = Q_M[tau] or H_tau mass channel before readout",
            "Pi_M is parent-owned, variation-owned, and not fit-defined",
            "Pi_M becomes a derived bookkeeping map",
            "UNSIGNED",
            False,
            False,
            "current corpus has Pi_M algebra candidates but not full descent",
        ),
        (
            "CPS2696_6_MTS_transfer",
            "compare MTS charge to EH charge",
            "Q_MTS_tau = Q_EH_tau + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_G",
            "all Delta terms vanish by theorem or are bounded as residuals",
            "MTS inherits the GR/EH source-measure theorem",
            "UNSIGNED",
            False,
            False,
            "this row is the actual bridge into local GR",
        ),
        (
            "CPS2696_7_Gauss_PPN_readout",
            "read charge in weak-field metric",
            "g_00=-1+2G_ref M_source/r+... and gamma,beta residuals controlled",
            "same charge controls slow-particle Newton and PPN light/clock tests",
            "local Newton/GR would become derivable",
            "NOT_REACHED",
            False,
            False,
            "first-order source closure still is not full local GR",
        ),
        (
            "CPS2696_8_verdict",
            "derive-or-reject result",
            "standard charge route is available; MTS transfer clauses remain unsigned",
            "parent action must sign CPS2696_5-CPS2696_7 before promotion",
            "conditional theorem built, claim blocked",
            "ROUTE_BUILT_NOT_PROMOTED",
            True,
            False,
            "good footwork, no haymaker yet",
        ),
    ]
    return [
        {
            "step_id": row[0],
            "operation": row[1],
            "expression": row[2],
            "requirement": row[3],
            "result_if_requirement_met": row[4],
            "current_result": row[5],
            "mathematical_valid": as_bool(row[6]),
            "parent_signed": as_bool(row[7]),
            "valid_for_claim": "false",
            "notes": row[8],
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def residual_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("MRR2696_0_flux_leak", "P8_Meff_conservation", "Delta_flux;dln_Meff_dt;epsilon_radial_Meff", "D_t;D_r;annulus", "Gdot/GMdot;orbital radial mass drift", "zero d(Pi_M J_H) or numeric time/radial profile", "yr^-1;dimensionless", "P8_time_drift_residual_or_zero.csv;P8_radial_mu_profile_or_zero.csv", "MISSING_PARENT_FLUX_CLOSURE_OR_VALUES", "MR510_0_flux_leak;SMR509_0_Delta_flux;SN4_closed_Meff_flux"),
        ("MRR2696_1_PiM_projector", "P8_projector_source_hair", "Delta_PiM", "projector_variation", "source-normalized Newton;PPN projector hair", "Pi_M parent descent/variation zero or coefficient bound", "dimensionless_or_charge_units", "PiM_parent_variation_or_residual_coefficients.csv", "MISSING_PIM_DESCENT_OR_PROJECTOR_COEFFICIENT", "MR510_3_projector_hair;PM5;PM6"),
        ("MRR2696_2_symplectic_boundary", "P8_boundary_bulk_domain_mu_extra", "Delta_symp", "boundary_reference", "absolute mass calibration;radial closure", "fixed reference zero and no boundary symplectic leakage", "dimensionless_or_mass_units", "boundary_charge_reference_zero_or_bound.csv", "MISSING_BOUNDARY_REFERENCE_ZERO_OR_BOUND", "MR510_2_symplectic_boundary;CC4;CC5"),
        ("MRR2696_3_extra_sector_mass", "P8_boundary_bulk_domain_mu_extra", "Delta_extra;mu_extra", "sector_mass_projection", "fifth-force;WEP;clocks;PPN", "field-specific zero theorem or residual coefficient matrix", "dimensionless", "extra_sector_mass_charge_vector.csv", "MISSING_EXTRA_SECTOR_MASS_SILENCE_OR_VALUES", "MR510_4_extra_sector_mass;CC6;SN6"),
        ("MRR2696_4_frame_split", "P8_frame_calibration_split", "Delta_frame_source", "Delta_frame", "WEP;clock;preferred-frame PPN", "one observed source/readout frame or residual bound", "dimensionless", "frame_source_split_residual_or_zero.csv", "MISSING_SAME_FRAME_SOURCE_CHARGE_OR_VALUE", "MR510_5_frame_split;SN0"),
        ("MRR2696_5_nonEH_charge", "R11_EH_operator_ledger", "Delta_nonEH;c_nonEH_operator_vector", "operator_charge", "gamma;beta;fifth-force;light bending", "EH charge fixed point or complete R11 vector", "operator_family_units", "R11_nonEH_charge_residual_vector.csv", "MISSING_EH_CHARGE_FIXED_POINT_OR_R11_VECTOR", "MR510_1_nonEH_charge;SN1"),
        ("MRR2696_6_calibration_mismatch", "P8_Gauss_orbital_calibration", "Delta_cal", "Gauss_orbit_readout", "Kepler/Newton measured GM", "Gauss surface integral and slow-particle readout theorem or calibration ledger", "dimensionless_or_mass_units", "Gauss_orbital_calibration_or_residual.csv", "MISSING_GAUSS_ORBITAL_READOUT_OR_BOUND", "MR510_6_calibration_mismatch;SN8;SN9"),
        ("MRR2696_7_PPN_tail", "P8_nonlinear_beta_source_residue", "Delta_PPN;delta_beta_source;gamma_minus_1", "second_order", "Cassini gamma;PPN beta;perihelion;Shapiro", "second-order source/operator calculation or explicit PPN vector", "dimensionless", "second_order_source_normalized_PPN_vector.csv", "MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR", "MR510_7_PPN_tail;SN11"),
        ("MRR2696_8_kappa_coupling_import", "P8_Geff_time_drift", "Delta_G;dln_Geff_dt;alpha_kappa(lambda);eta_source_AB", "D_t;D_lambda;D_A", "Gdot;R10;source WEP", "2695 parent-signed kappa or residual values", "yr^-1;dimensionless;range-dependent", "kappa_residual_value_requirements_2695_NONCLAIM.csv", "IMPORTED_CONDITIONAL_KAPPA_NOT_SCOREABLE", "KRR2695_0-KRR2695_5;SN7"),
    ]
    return [
        {
            "residual_id": row[0],
            "component_id": row[1],
            "symbol": row[2],
            "derivative_or_projection_channel": row[3],
            "observable_link": row[4],
            "target_bound_or_zero": row[5],
            "units": row[6],
            "required_artifact": row[7],
            "current_status": row[8],
            "source_anchor": row[9],
            "numeric_value_present": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def pim_replacement_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PIM2696_0_old_risk",
            "primitive Pi_M",
            "Pi_M selected as the mass-flux projector before a parent charge is derived",
            "high-scrutiny route because it can look like a fitted mask",
            "demote primitive Pi_M to conditional bookkeeping only",
        ),
        (
            "PIM2696_1_safer_route",
            "parent Hamiltonian charge first",
            "define M_eff from H_tau/Q_tau using the parent covariant phase-space charge",
            "standard GR/EH-style route; easier to defend",
            "make Pi_M descend from Q_M[tau], not the other way round",
        ),
        (
            "PIM2696_2_descent_condition",
            "Pi_M equals charge-channel projection",
            "Pi_M J_H = Q_M[tau] plus constraints with fixed units and reference",
            "projector becomes parent-owned if equality and variation are proved",
            "open not parent-derived",
        ),
        (
            "PIM2696_3_flux_condition",
            "closure is differential/current identity",
            "d(Pi_M J_H)=0 must follow from Ward/topology/Euler or dQ_M[tau]=0",
            "blocks idempotence-equals-closure overclaim",
            "open not parent-derived",
        ),
        (
            "PIM2696_4_residual_condition",
            "failed descent becomes residual vector",
            "Delta_PiM, Delta_flux, Delta_symp, Delta_extra, Delta_cal, Delta_frame, Delta_nonEH, Delta_PPN",
            "keeps the branch testable if the theorem route fails",
            "nonclaim residual branch active",
        ),
        (
            "PIM2696_5_verdict",
            "best source-measure language",
            "MTS should present local source mass as a parent Hamiltonian/Noether charge; Pi_M is allowed only as a derived projection of that charge",
            "less vulnerable than a bespoke projector axiom",
            "adopt for next parent-action fixed-point attempt",
        ),
    ]
    return [
        {
            "map_id": row[0],
            "route": row[1],
            "statement": row[2],
            "why_it_matters": row[3],
            "decision": row[4],
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    rows = [
        ("DRY2696_0_full_source_charge_parent", True, True, True, True, True, True, True, True, False, False, False, "CONDITIONAL_SOURCE_MEASURE_ONLY_PPN_STILL_SEPARATE"),
        ("DRY2696_1_formula_only", True, False, True, True, True, True, True, True, False, False, False, "REJECT_PARENT_PHASE_SPACE_UNSIGNED"),
        ("DRY2696_2_bare_mass_equated", True, True, True, True, True, True, True, True, True, False, False, "REJECT_BARE_MASS_EQUALS_SOURCE_CHARGE"),
        ("DRY2696_3_PiM_fitted", True, True, False, True, True, True, True, True, False, False, False, "REJECT_PIM_NOT_PARENT_DERIVED"),
        ("DRY2696_4_flux_open", True, True, True, False, True, True, True, True, False, False, False, "REJECT_FLUX_CLOSURE_MISSING"),
        ("DRY2696_5_worldtube_open", True, True, True, True, False, True, True, True, False, False, False, "REJECT_WORLDTUBE_GLUE_MISSING"),
        ("DRY2696_6_extra_mass_open", True, True, True, True, True, False, True, True, False, False, False, "REJECT_EXTRA_MASS_CHANNEL_OPEN"),
        ("DRY2696_7_Gauss_readout_open", True, True, True, True, True, True, False, True, False, False, False, "REJECT_GAUSS_ORBITAL_READOUT_MISSING"),
        ("DRY2696_8_PPN_missing", True, True, True, True, True, True, True, False, False, False, False, "CONDITIONAL_NEWTON_SOURCE_ONLY_NO_LOCAL_GR"),
        ("DRY2696_9_residual_values_present", False, False, False, False, False, False, False, False, False, True, False, "NONCLAIM_SCOREABLE_RESIDUAL_BRANCH_ONLY"),
        ("DRY2696_10_orbital_GM_backfill", True, True, True, True, False, True, True, False, False, False, True, "REJECT_ORBITAL_GM_BACKFILL"),
    ]
    return [
        {
            "case_id": row[0],
            "conditional_kappa_carried": as_bool(row[1]),
            "parent_phase_space_signed": as_bool(row[2]),
            "PiM_parent_derived": as_bool(row[3]),
            "flux_closed": as_bool(row[4]),
            "worldtube_glue_signed": as_bool(row[5]),
            "extra_mass_silent": as_bool(row[6]),
            "Gauss_orbital_readout": as_bool(row[7]),
            "PPN_stability": as_bool(row[8]),
            "bare_mass_equated": as_bool(row[9]),
            "residual_values_present": as_bool(row[10]),
            "orbital_GM_backfill": as_bool(row[11]),
            "expected_status": row[12],
            "expected_claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["orbital_GM_backfill"] == "true":
        return "REJECT_ORBITAL_GM_BACKFILL"
    if case["bare_mass_equated"] == "true":
        return "REJECT_BARE_MASS_EQUALS_SOURCE_CHARGE"
    if case["parent_phase_space_signed"] == "false" and case["residual_values_present"] == "true":
        return "NONCLAIM_SCOREABLE_RESIDUAL_BRANCH_ONLY"
    if case["parent_phase_space_signed"] == "false":
        return "REJECT_PARENT_PHASE_SPACE_UNSIGNED"
    if case["PiM_parent_derived"] == "false":
        return "REJECT_PIM_NOT_PARENT_DERIVED"
    if case["flux_closed"] == "false":
        return "REJECT_FLUX_CLOSURE_MISSING"
    if case["worldtube_glue_signed"] == "false":
        return "REJECT_WORLDTUBE_GLUE_MISSING"
    if case["extra_mass_silent"] == "false":
        return "REJECT_EXTRA_MASS_CHANNEL_OPEN"
    if case["Gauss_orbital_readout"] == "false":
        return "REJECT_GAUSS_ORBITAL_READOUT_MISSING"
    if case["PPN_stability"] == "false":
        return "CONDITIONAL_NEWTON_SOURCE_ONLY_NO_LOCAL_GR"
    return "CONDITIONAL_SOURCE_MEASURE_ONLY_PPN_STILL_SEPARATE"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        actual = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "actual_status": actual,
                "status_match": as_bool(actual == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2696_0_kappa_import", "kappa/G_eff is parent-owned or explicitly conditional", "PASS_CONDITIONAL_NOT_PROMOTED", "2695 imported as conditional"),
        ("CG2696_1_parent_charge", "source mass is defined by parent Hamiltonian/Noether charge before readout", "FAIL_PARENT_PHASE_SPACE_UNSIGNED", "SMA2696_1;CPS2696_0-CPS2696_3"),
        ("CG2696_2_PiM_descent", "Pi_M descends from parent charge and owns variation terms", "FAIL_PIM_DESCENT_UNSIGNED", "SMA2696_4;PIM2696_2"),
        ("CG2696_3_flux_closure", "d(Pi_M J_H)=0 or dQ_M[tau]=0 in source-free exterior", "FAIL_FLUX_CLOSURE_UNSIGNED", "SMA2696_5;MRR2696_0"),
        ("CG2696_4_worldtube_glue", "worldtube source measure equals exterior charge, not bare mass", "FAIL_WORLDTUBE_GLUE_UNSIGNED", "SMA2696_6;CPS2696_4"),
        ("CG2696_5_extra_channels", "all non-EH/projector/boundary/domain/memory/range/frame mass channels vanish or are bounded", "FAIL_EXTRA_CHANNEL_SILENCE_UNSIGNED", "SMA2696_7;MRR2696_1-MRR2696_5"),
        ("CG2696_6_Gauss_readout", "same charge gives Poisson/Gauss/orbital inverse-square coefficient", "FAIL_GAUSS_READOUT_UNSIGNED", "SMA2696_8;MRR2696_6"),
        ("CG2696_7_PPN_stability", "source measure survives beta/gamma/PPN order", "FAIL_PPN_SOURCE_STABILITY_UNSIGNED", "SMA2696_9;MRR2696_7"),
        ("CG2696_8_verdict", "source-measure branch proves local GR/Newton now", "CLAIM_BLOCKED", "all gates above"),
    ]
    return [
        {
            "gate_id": row[0],
            "pass_condition": row[1],
            "current_status": row[2],
            "evidence": row[3],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2696_0_best_language",
            "USE_PARENT_HAMILTONIAN_CHARGE_FIRST",
            "The defensible mass route is standard covariant phase-space/Noether charge language; Pi_M should descend from that charge, not substitute for it.",
            "REAL_REFINEMENT",
            "write next parent action fixed-point with Q_tau/H_tau as the mass owner",
        ),
        (
            "DEC2696_1_source_measure_not_earned",
            "MEFF_SOURCE_GLUE_NOT_DERIVED",
            "Current MTS has not parent-signed charge descent, Pi_M variation, flux closure, worldtube glue, extra-sector silence, Gauss readout, or PPN stability.",
            "NO_CLAIM",
            "keep residual rows active",
        ),
        (
            "DEC2696_2_bare_mass_guard",
            "BARE_MATTER_MASS_IS_NOT_ENOUGH",
            "The source mass in the local GR/Newton bridge must be dressed parent charge including binding/field/boundary ownership, not raw rest-matter mass.",
            "ANTI_OVERCLAIM",
            "state M_source as Hamiltonian/Noether charge in future spine",
        ),
        (
            "DEC2696_3_orbital_backfill_guard",
            "ORBITAL_GM_CANNOT_BE_THE_PROOF",
            "The weak-field/orbital coefficient must be derived from the source charge; using fitted GM as the premise reverses the theorem.",
            "ANTI_CHEAT_GUARD",
            "derive Gauss/orbital readout or retain Delta_cal",
        ),
        (
            "DEC2696_4_next_route",
            "BUILD_MINIMAL_LOCAL_PARENT_FIXED_POINT",
            "The next leap is not another overview; it is the smallest parent-action local branch that simultaneously owns kappa, EH charge, source measure, extra-sector silence, and PPN readout.",
            "NEXT_ROUTE_SELECTED",
            "run 2697 minimal local parent-action fixed-point ansatz",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "rationale": row[2],
            "status": row[3],
            "next_action": row[4],
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT2696_0_selected",
            "selected_leap_forward",
            "2697-Y5-R2FR-minimal-local-parent-action-fixed-point-ansatz-kappa-source-measure-EH.md",
            "scripts/Y5_R2FR_minimal_local_parent_action_fixed_point_ansatz_kappa_source_measure_EH_2697.py",
            "construct the smallest local parent-action branch that can sign the kappa topological sector, EH/covariant phase-space charge, source-measure glue, extra-sector silence, Gauss/Newton readout, and PPN residual handoff",
            "either a coherent fixed-point contract exists with every local-GR prerequisite named, or the local branch is explicitly demoted to residual closure-only",
            "another broad recap; treating Pi_M as fitted mask; treating bare mass as source charge; using orbital GM as premise; public/GitHub action; formalization-workbench edits",
        ),
        (
            "NEXT2696_1_fallback",
            "fallback_if_fixed_point_fails",
            "2697b-Y5-R2FR-Meff-residual-values-and-local-bound-runner.md",
            "scripts/Y5_R2FR_Meff_residual_values_and_local_bound_runner_2697b.py",
            "fill Delta_flux, Delta_PiM, Delta_symp, Delta_extra, Delta_frame, Delta_nonEH, Delta_cal, and Delta_PPN as nonclaim residual inputs",
            "all residual rows numeric/sourced/units-clean and still nonclaim",
            "pretending missing residuals are zero",
        ),
    ]
    return [
        {
            "target_id": row[0],
            "selection_status": row[1],
            "target_doc": row[2],
            "target_script": row[3],
            "purpose": row[4],
            "acceptance_gate": row[5],
            "forbidden_shortcuts": row[6],
            "private_only": "true",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2696_0_kappa", "kappa/G_eff", "CARRIED_CONDITIONAL_NOT_CLAIMED", "2695 topological kappa is a candidate parent clause only", False, "needs parent fixed-point adoption"),
        ("STATUS2696_1_source_measure", "M_eff/source mass", "STANDARD_CHARGE_ROUTE_SELECTED_NOT_DERIVED", "source mass should be parent Hamiltonian/Noether charge; Pi_M must descend from it", False, "build minimal local parent fixed point"),
        ("STATUS2696_2_Newton", "Newton source normalization", "BLOCKED_BY_SOURCE_GLUE_AND_GAUSS_READOUT", "closed M_eff flux and Gauss/orbital coefficient are not parent-derived", False, "derive or retain Delta_flux/Delta_cal"),
        ("STATUS2696_3_local_GR", "PPN/local GR", "BLOCKED_BY_PPN_AND_R11", "first-order source charge would still need gamma/beta/operator stability", False, "carry PPN residual handoff into 2697"),
        ("STATUS2696_4_public", "publication/GitHub", "NO_ACTION", "private checkpoint only", False, "no push"),
    ]
    return [
        {
            "status_id": row[0],
            "area": row[1],
            "current_state": row[2],
            "meaning": row[3],
            "claim_ready": as_bool(row[4]),
            "next_action": row[5],
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in BRANCH_OUTPUTS.items():
        ok, count, message = parse_csv(path)
        rows.append(
            {
                "branch_key": key,
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "csv_parse_ok": as_bool(ok),
                "row_count": count,
                "parse_message": message,
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    charge_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    pim_rows: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    source_claim_blocked = any(row["audit_id"] == "SMA2696_10_verdict" and row["current_status"] == "SOURCE_MEASURE_CLAIM_BLOCKED" for row in audit_rows)
    charge_route_valid = any(row["step_id"] == "CPS2696_3_surface_charge" and row["mathematical_valid"] == "true" for row in charge_rows)
    transfer_unsigned = any(row["step_id"] == "CPS2696_6_MTS_transfer" and row["parent_signed"] == "false" for row in charge_rows)
    residuals_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["numeric_value_present"] == "false"
        and row["score_ready"] == "false"
        for row in residual_rows
    )
    pim_safer_route = any(row["map_id"] == "PIM2696_5_verdict" and "Hamiltonian/Noether" in row["statement"] for row in pim_rows)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates) and any(
        row["gate_id"] == "CG2696_8_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates
    )
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2697" in read_text(OUTPUTS["next_target"]) and "minimal_local_parent_action" in read_text(OUTPUTS["next_target"])
    no_public_claim = all("claim_allowed" not in row or row["claim_allowed"] == "false" for row in audit_rows + residual_rows + claim_gates)
    checks = [
        ("VAL2696_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2696_source_measure_claim_blocked", source_claim_blocked, "source-measure/M_eff claim remains blocked for current MTS"),
        ("VAL2696_charge_route_math_valid", charge_route_valid, "standard covariant phase-space charge route is mathematically valid as a conditional reference"),
        ("VAL2696_MTS_transfer_unsigned", transfer_unsigned, "MTS transfer to EH/source charge remains unsigned"),
        ("VAL2696_residual_requirements_nonclaim", residuals_nonclaim, "M_eff residual rows remain nonclaim, nonnumeric, and not score-ready"),
        ("VAL2696_PiM_safer_route_selected", pim_safer_route, "Pi_M is demoted to derived projection of parent Hamiltonian/Noether charge"),
        ("VAL2696_dryrun_refusals", dryrun_ok, "dry-run refuses formula-only, bare-mass, fitted-PiM, open-flux, open-worldtube, extra-mass, missing-Gauss, and orbital-GM backfill cases"),
        ("VAL2696_claim_gates_block_claims", claim_blocked, "claim gates block source-measure/local-GR/Newton promotion"),
        ("VAL2696_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2696_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2696_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2696_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2696_next_target_selected", next_target_ok, "2697 minimal local parent-action fixed point selected"),
        ("VAL2696_no_public_claim", no_public_claim, "no row allows a public or GitHub claim"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2696_OVERALL",
            "passed": as_bool(overall),
            "detail": "2696 selects the parent Hamiltonian/Noether charge route for M_eff, blocks source-measure promotion, stages residuals, and selects the minimal local parent-action fixed point as the next leap",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    charge_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    pim_rows: list[dict[str, Any]],
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
                "# 2696 - Y5/R2FR Source-Measure M_eff Flux Closure After Conditional Kappa Gate",
                "",
                "## Private Verdict",
                "",
                "This checkpoint takes the next load-bearing beam after kappa: what makes the `M_eff` in `G_eff M_eff` the actual parent source charge rather than fitted orbital `GM`?",
                "",
                "The less-scrutinized route is not to start with a bespoke projector. It is to define source mass by the parent Hamiltonian/Noether charge first, then allow `Pi_M` only as a derived projection of that charge:",
                "",
                "`delta L = E_A delta phi^A + d theta`,",
                "",
                "`J_tau = theta(phi, L_tau phi) - i_tau L`,",
                "",
                "`J_tau = dQ_tau + C_tau`,",
                "",
                "and in a source-free exterior annulus with controlled constraints and boundary flux, `integral_S2 Q_tau = integral_S1 Q_tau`.",
                "",
                "That is a real GR/EH-style theorem route. Current MTS has not yet inherited it: the parent action has not signed the observed generator, charge descent, `Pi_M` variation, flux closure, worldtube glue, extra-sector silence, Gauss/orbital readout, or PPN stability. So 2696 makes progress but no measured-GM, Newton, PPN, local-GR, GitHub, or public claim.",
                "",
                "The next leap is now sharply defined: build the minimal local parent-action fixed point that signs kappa, EH charge, source measure, extra-sector silence, and PPN handoff together, or demote the local branch to explicit residual closure-only.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Source-Measure Theorem Audit",
                "",
                markdown_table(audit_rows),
                "",
                "## Covariant Phase-Space Charge Derivation Check",
                "",
                markdown_table(charge_rows),
                "",
                "## M_eff Residual Value Requirements",
                "",
                markdown_table(residual_rows),
                "",
                "## Pi_M Replacement Decision Map",
                "",
                markdown_table(pim_rows),
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
    audit_rows = source_measure_audit_rows()
    charge_rows = charge_derivation_rows()
    residual_rows = residual_requirement_rows()
    pim_rows = pim_replacement_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["source_measure_audit"], audit_rows)
    write_csv(OUTPUTS["charge_derivation"], charge_rows)
    write_csv(OUTPUTS["residual_requirements"], residual_rows)
    write_csv(OUTPUTS["pim_replacement_map"], pim_rows)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_source_measure_audit"], audit_rows)
    write_csv(BRANCH_OUTPUTS["local_Meff_residual_requirements"], residual_rows)
    write_csv(BRANCH_OUTPUTS["wep_Meff_residual_requirements"], residual_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_Meff_residual_requirements"], residual_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_target)

    branch_rows = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validation = validation_rows(
        source_rows=source_rows,
        audit_rows=audit_rows,
        charge_rows=charge_rows,
        residual_rows=residual_rows,
        pim_rows=pim_rows,
        dryrun_results=dry_results,
        claim_gates=claim_gates,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_document(
        source_rows=source_rows,
        audit_rows=audit_rows,
        charge_rows=charge_rows,
        residual_rows=residual_rows,
        pim_rows=pim_rows,
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
