from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_EH_DESCENT_COUPLING_PIM_LOCK_2579"
CHECKPOINT_ID = "2579"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2579-Y5-R2FR-EH-fixed-point-descent-coupling-PiM-lock-or-double-zero-residuals.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_SOURCE_REGISTER.csv",
    "descent_package": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_DESCENT_PACKAGE_AUDIT.csv",
    "sector_inventory_seed": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_EXTRA_SECTOR_INVENTORY_SEED.csv",
    "coupling_pim_gate": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_COUPLING_PIM_LOCK_GATE.csv",
    "residual_envelope": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv",
    "implications": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_NEWTON_GR_IMPLICATIONS.csv",
    "claim_gates": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EH_DESCENT_COUPLING_PIM_2579_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2579_VALIDATION.csv",
}

COPY_TARGETS = {
    "descent_package": QUEUE / "JR2579_EH_DESCENT_COUPLING_PIM_PACKAGE_AUDIT_NONCLAIM.csv",
    "sector_inventory_seed": QUEUE / "JR2579_EXTRA_SECTOR_INVENTORY_SEED_NONCLAIM.csv",
    "coupling_pim_gate": LOCAL_BOUNDS / "EH_descent_coupling_PiM_lock_gate_2579_NONCLAIM.csv",
    "residual_envelope": BETA_SOURCE / "LOCAL_GR_EH_DESCENT_COUPLING_PIM_RESIDUAL_ENVELOPE_2579_NONCLAIM.csv",
    "next_target": QUEUE / "JR2579_PARENT_EXTRA_SECTOR_INVENTORY_COUPLING_MAP_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2579_00_2578_handoff",
        "source_path": ROOT / "2578-Y5-R2FR-PiM-Hamiltonian-coupling-identity-or-source-backed-residual-fill.md",
        "needles": ["NEXT2578_0_selected", "CPS2578_3_EH_transfer", "CPS2578_5_current_verdict", "VAL2578_OVERALL"],
        "role": "active handoff selecting EH fixed-point descent with coupling/PiM lock",
    },
    {
        "source_id": "SRC2579_01_2188_double_zero",
        "source_path": ROOT / "2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md",
        "needles": ["DZ2188_4_F1_law", "PIM2188_6_verdict", "VAL2188_OVERALL"],
        "role": "double-zero theorem and PiM lock contract",
    },
    {
        "source_id": "SRC2579_02_2187_radial_gauge",
        "source_path": ROOT / "2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md",
        "needles": ["RGC2187_6_current_status", "EDS2187_7_verdict", "VAL2187_OVERALL"],
        "role": "parent-owned radial/angle gauge contract and EH descent signature matrix",
    },
    {
        "source_id": "SRC2579_03_2186_descent_gate",
        "source_path": ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
        "needles": ["DEG2186_0_EH_core", "DEG2186_4_PiM_lock", "VAL2186_OVERALL"],
        "role": "MTS EH descent gate and PiM lock blocker",
    },
    {
        "source_id": "SRC2579_04_2185_EH_coefficients",
        "source_path": ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
        "needles": ["WAE2185_4_delta", "IHG2185_1_MTS_descent", "VAL2185_OVERALL"],
        "role": "EH fixed-point coefficient extraction and MTS descent limitation",
    },
    {
        "source_id": "SRC2579_05_A511_action_blocks",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "needles": ["A511_0_EH_core", "A511_1_kappa_topological", "A511_6_metric_readout"],
        "role": "minimal local-GR action blocks",
    },
    {
        "source_id": "SRC2579_06_FP511_conditions",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "needles": ["FP511_1_double_zero_nonEH_coupling", "FP511_5_parent_PiM_lock", "FP511_7_metric_PPN_readout"],
        "role": "fixed-point conditions for local-GR descent",
    },
    {
        "source_id": "SRC2579_07_T505_noether",
        "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "needles": ["T505_conditional_Noether_mass_charge_closure", "T505_Newton_limit_corollary"],
        "role": "conditional Noether mass-charge and Newton/Gauss closure",
    },
    {
        "source_id": "SRC2579_08_HSM541_measure",
        "source_path": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_6_constant_universal_G"],
        "role": "Hamiltonian PiM and constant coupling contract",
    },
    {
        "source_id": "SRC2579_09_2578_validation",
        "source_path": OUT / "P8_Y5_BRR545_2578_VALIDATION.csv",
        "needles": ["VAL2578_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def descent_package_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "package_id": "EDP2579_0_EH_core",
            "required_clause": "local compact parent branch reduces to EH core",
            "mathematical_form": "S_parent -> (2*kappa0)^-1 int sqrt(-g_obs)(R-2 Lambda0) + locally silent sectors",
            "current_status": "EH_CORE_CONTRACT_EXISTS_NOT_PARENT_SIGNED",
            "closes_if_signed": "EH weak-field v coefficients from 2185 become MTS inheritance rather than GR import",
            "failure_residual": "epsilon_EH_fixed_point_descent",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_1_stationary_fixed_point",
            "required_clause": "local exterior fixed point solves parent Euler equations",
            "mathematical_form": "E_A(Phi0)=0, L_tau Phi0=0, J_A^exterior=0",
            "current_status": "FIXED_POINT_REQUIRED_NOT_MATCHED",
            "closes_if_signed": "no plateau axiom is smuggled in",
            "failure_residual": "epsilon_fixed_point_Euler",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_2_extra_double_zero",
            "required_clause": "all non-EH metric/source/readout/projector couplings have double zero",
            "mathematical_form": "C_i(Phi0)=0 and partial_A C_i(Phi0)=0; therefore F1_extra=0",
            "current_status": "GENERIC_THEOREM_EXISTS_ACTUAL_CI_INVENTORY_MISSING",
            "closes_if_signed": "first-order fifth-force/source-normalization/PPN leakage is removed",
            "failure_residual": "F1_extra_linear_leakage_norm",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_3_positive_gap",
            "required_clause": "non-gauge extra modes have positive source-free compact exterior operator",
            "mathematical_form": "int_A <delta Phi,L delta Phi> >= m_min^2 ||delta Phi||^2 with zero source/boundary flux",
            "current_status": "POSITIVE_GAP_REQUIRED_NOT_PROVED",
            "closes_if_signed": "extra hair is zero or exponentially/source bounded",
            "failure_residual": "epsilon_extra_gap_hair",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_4_PiM_lock",
            "required_clause": "mass projector is EH/Hamiltonian projector at the fixed point",
            "mathematical_form": "Pi_M(Phi0)=Pi_EH, partial_A Pi_M(Phi0)=0, [d,Pi_M]J_H=0, projector stress=0",
            "current_status": "PIM_LOCK_CONTRACT_EXISTS_NOT_PARENT_SIGNED",
            "closes_if_signed": "source mass cannot be recalibrated by projector freedom",
            "failure_residual": "epsilon_PiM_lock;epsilon_DPiM;I_commutator;epsilon_projector_stress",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_5_coupling_baseline",
            "required_clause": "kappa_MTS and ell_J/source frame fixed in the same local branch",
            "mathematical_form": "d kappa_MTS=0, delta_ellJ=0, universal observed coframe/source current",
            "current_status": "COUPLING_SOURCE_BASELINE_NOT_PARENT_SIGNED",
            "closes_if_signed": "Delta_kappa and Delta_ellJ leave the source/Newton envelope",
            "failure_residual": "delta_kappa;delta_ellJ;epsilon_source_frame",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_6_boundary_readout",
            "required_clause": "zero compact boundary flux and parent-owned radial/angle readout gauge",
            "mathematical_form": "int_boundary Delta(theta,Q,tau)=0; areal/isotropic gauge functional fixed before PPN scoring",
            "current_status": "BOUNDARY_AND_READOUT_OWNER_OPEN",
            "closes_if_signed": "2PN gauge warning stays a coordinate issue, not a physics residual",
            "failure_residual": "epsilon_boundary_reference_zero;epsilon_radial_gauge_owner",
            "valid_for_claim": False,
        },
        {
            "package_id": "EDP2579_7_verdict",
            "required_clause": "full EH fixed-point descent package for current MTS",
            "mathematical_form": "EH core + fixed point + C_i double zeros + positive gap + PiM lock + coupling baseline + boundary/readout owner",
            "current_status": "EH_DESCENT_COUPLING_PIM_PACKAGE_NOT_DERIVED_CURRENT_CORPUS",
            "closes_if_signed": "Newton/local-GR derivation route can reopen as parent inheritance",
            "failure_residual": "Delta_local_GR_EH_descent_coupled_abs",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def sector_inventory_seed_rows() -> list[dict[str, Any]]:
    sectors = [
        ("INV2579_0_GammaKhat", "Gamma_eff/K_hat/q_loc sector", "metric/source reciprocal current coupling", "C_GK(Phi0)=0; partial_A C_GK(Phi0)=0", "MISSING_GK_OPERATOR_INVENTORY", "PPN;R10;local_GR"),
        ("INV2579_1_memory", "memory/response sector", "compact memory source or clock/orbital response coupling", "C_mem(Phi0)=0; partial_A C_mem(Phi0)=0", "MISSING_MEMORY_OPERATOR_INVENTORY", "clocks;PPN;orbital"),
        ("INV2579_2_motion_time", "motion/time sector", "time-flow or motion-field local stress/source coupling", "C_T(Phi0)=0; partial_A C_T(Phi0)=0", "MISSING_TIME_MOTION_OPERATOR_INVENTORY", "clock;WEP;PPN"),
        ("INV2579_3_domain_projector", "domain/range/projector sector", "domain selector, range, PiM or projector-stress coupling", "C_D(Phi0)=0; partial_A C_D(Phi0)=0; PiM lock", "MISSING_DOMAIN_PROJECTOR_INVENTORY", "PPN;source_mass;R10"),
        ("INV2579_4_matter_species", "matter/source-frame sector", "species-dependent matter coupling or ell_J source-scale slope", "partial_A ln m_species(Phi0)=0; delta_ellJ=0", "MISSING_UNIVERSAL_MATTER_INVENTORY", "WEP;source_mass;clocks"),
        ("INV2579_5_boundary_symplectic", "boundary/symplectic sector", "extra theta/Q/reference or exact/topological flux", "Delta_boundary=0; Delta_symp=0", "MISSING_BOUNDARY_SYMPLECTIC_INVENTORY", "Newton;PPN;local_GR"),
        ("INV2579_6_coupling_kappa", "kappa/G-sector", "radial/source/frame variation of gravitational coefficient", "d kappa_MTS=0; G_ref matches kappa_MTS", "MISSING_KAPPA_COUPLING_INVENTORY", "Newton;PPN;clock;orbital"),
        ("INV2579_7_readout_gauge", "readout/radial-angular gauge sector", "metric readout, angular coframe, endpoint and PPN gauge coupling", "g_readout=g_obs+O((Phi-Phi0)^2); parent gauge owner", "MISSING_READOUT_OPERATOR_INVENTORY", "2PN;PPN;local_GR"),
    ]
    return [
        stamp(
            {
                "inventory_id": inventory_id,
                "sector": sector,
                "possible_operator": operator,
                "double_zero_test": test,
                "current_status": status,
                "arenas": arenas,
                "next_action": "inventory parent C_i/O_i source terms, then classify as derived_zero, source_bounded, or closure_only",
                "valid_for_claim": False,
            }
        )
        for inventory_id, sector, operator, test, status, arenas in sectors
    ]


def coupling_pim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CPG2579_0_kappa", "kappa_MTS fixed baseline", "d kappa_MTS=0 and G_ref inherited from same parent EH coefficient", "CONDITIONAL_BLOCK_NOT_PARENT_SIGNED", "delta_kappa"),
        ("CPG2579_1_ellJ", "ell_J/source-current baseline", "ell_J fixed before W_source and v source equation; no species/source-frame slope", "SOURCE_SCALE_OWNER_OPEN", "delta_ellJ"),
        ("CPG2579_2_PiM_value", "PiM value lock", "Pi_M(Phi0)=Pi_EH=Pi_M^H", "PIM_VALUE_LOCK_OPEN", "epsilon_PiM_value"),
        ("CPG2579_3_PiM_derivative", "PiM derivative silence", "partial_A Pi_M(Phi0)=0 and [d,Pi_M]J_H=0", "PIM_DERIVATIVE_COMMUTATOR_OPEN", "epsilon_DPiM;I_commutator"),
        ("CPG2579_4_projector_stress", "projector stress silence", "metric/source variation of Pi_M carries no local stress or boundary mass", "PROJECTOR_STRESS_OPEN", "epsilon_projector_stress"),
        ("CPG2579_5_same_domain", "same Hilbert source domain", "PiM acts on the same J_H, tau, reference and W_source as EH Hamiltonian charge", "SAME_DOMAIN_OPEN", "epsilon_PiM_Hamiltonian;R_eq_integral"),
        ("CPG2579_6_verdict", "coupling plus PiM lock package", "kappa/ellJ/PiM/reference/source domain fixed together", "COUPLING_PIM_LOCK_PACKAGE_NOT_DERIVED", "Delta_PiM_coupled_abs"),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "lock": lock,
                "required_identity": required,
                "current_status": status,
                "residual_if_missing": residual,
                "valid_for_claim": False,
            }
        )
        for gate_id, lock, required, status, residual in rows
    ]


def residual_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2579_0_EH", "epsilon_EH_fixed_point_descent", "failure to parent-derive EH core in compact local branch", "MISSING_MTS_EH_DESCENT", "dimensionless_or_declared", "local_GR;WEP;PPN"),
        ("ENV2579_1_fixed_point", "epsilon_fixed_point_Euler", "failure of Phi0 to solve parent local exterior Euler equations", "MISSING_FIXED_POINT_EULER_PROOF", "dimensionless_or_declared", "local_GR;PPN"),
        ("ENV2579_2_F1", "F1_extra_linear_leakage_norm", "first-order extra-sector leakage envelope across actual C_i/O_i inventory", "MISSING_ACTUAL_CI_DOUBLE_ZERO_INVENTORY", "dimensionless_or_declared", "PPN;WEP;local_GR"),
        ("ENV2579_3_gap", "epsilon_extra_gap_hair", "compact exterior extra hair after double-zero algebra", "MISSING_POSITIVE_GAP_CERTIFICATE", "dimensionless_or_length_scale", "PPN;orbital;R10"),
        ("ENV2579_4_PiM", "epsilon_PiM_lock", "PiM value/derivative/domain/stress lock failure", "MISSING_PARENT_PIM_LOCK", "dimensionless_or_GM_flux", "Newton;R10;PPN"),
        ("ENV2579_5_kappa", "delta_kappa", "local gravitational coupling mismatch or drift", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "dimensionless", "Newton;PPN;clock"),
        ("ENV2579_6_ellJ", "delta_ellJ", "source-current normalization mismatch", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "dimensionless", "Newton;WEP;PPN"),
        ("ENV2579_7_boundary", "epsilon_boundary_reference_zero", "extra/reference/boundary flux through compact local linking surfaces", "MISSING_BOUNDARY_ZERO_OR_BOUND", "GM_flux_or_dimensionless", "Newton;local_GR"),
        ("ENV2579_8_readout", "epsilon_radial_gauge_owner", "parent ownership failure for areal/isotropic radial and angular gauge map", "MISSING_RADIAL_GAUGE_OWNER", "dimensionless_or_2PN", "2PN;PPN;local_GR"),
        ("ENV2579_9_total", "Delta_local_GR_EH_descent_coupled_abs", "absolute no-cancellation sum of EH, fixed-point, F1, gap, PiM, coupling, boundary and readout residuals", "MISSING_COMPONENT_INPUTS", "dimensionless_or_declared", "local_GR;Newton;PPN;WEP"),
    ]
    return [
        stamp(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "value": "MISSING_NUMERIC_VALUE",
                "status": status,
                "units": units,
                "observable_link": arenas,
                "source_path": "MISSING_SOURCE_PATH",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
        for row_id, symbol, definition, status, units, arenas in rows
    ]


def implication_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "implication_id": "IMP2579_0_F1",
            "premise_package": "actual C_i/O_i inventory plus C_i(Phi0)=0 and partial_A C_i(Phi0)=0 for every retained local non-EH sector",
            "implication": "F1_extra_linear_leakage_norm=0",
            "current_status": "GENERIC_THEOREM_ONLY",
            "missing_piece": "actual sector inventory and parent-signed zeros",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2579_1_Newton",
            "premise_package": "EH core, PiM/Hamiltonian source glue, fixed kappa/ellJ, zero boundary flux, and v coefficient inheritance",
            "implication": "Delta_Newton_v_coupled=0",
            "current_status": "BLOCKED_CONDITIONAL",
            "missing_piece": "descent package not parent-signed",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2579_2_PPN",
            "premise_package": "above plus parent-owned areal/isotropic readout and full PPN vector silence",
            "implication": "gamma=1, beta=1, preferred-frame/conservation channels silent in local branch",
            "current_status": "BLOCKED_CONDITIONAL",
            "missing_piece": "readout ownership and extra/PiM/boundary/coupling residuals",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2579_3_local_GR",
            "premise_package": "Delta_local_GR_EH_descent_coupled_abs=0 plus tested finite residual fallback if any term survives",
            "implication": "local GR recovery would be derivable rather than imported",
            "current_status": "NOT_CLAIMED",
            "missing_piece": "parent descent proof or source-backed residual bounds",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2579_0_internal_progress", "full EH descent/coupling/PiM package is now an explicit checklist plus sector inventory seed", "PASS_INTERNAL_PROGRESS", "the missing proof is narrower and operationalized", True),
        ("GATE2579_1_EH_descent", "MTS parent derives EH fixed point", "BLOCKED", "EH core and fixed point remain contracts rather than parent variation", False),
        ("GATE2579_2_double_zero", "all local non-EH double zeros are parent-signed", "BLOCKED", "actual C_i/O_i inventory is missing", False),
        ("GATE2579_3_PiM_lock", "PiM value/derivative/domain/stress lock is parent-signed", "BLOCKED", "PiM lock remains a contract", False),
        ("GATE2579_4_coupling_baseline", "kappa_MTS and ell_J are parent fixed in same branch", "BLOCKED", "coupling/source baseline not derived", False),
        ("GATE2579_5_boundary_readout", "boundary zero and readout gauge owner are parent-signed", "BLOCKED", "zero compact flux and radial/angle owner remain open", False),
        ("GATE2579_6_local_GR", "local GR/Newton recovery is derived", "BLOCKED", "descent package and empirical residual bounds remain incomplete", False),
        ("GATE2579_7_no_shortcuts", "generic double-zero theorem, EH import, fitted G, or gauge contract can be used as proof", "PASS_GUARDRAIL", "all are explicitly nonclaim until parent-signed", True),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2579_0_gain",
            "decision": "EH_DESCENT_PACKAGE_UNIFIED_WITH_COUPLING_AND_PIM",
            "reason": "EH core, fixed point, double zeros, gap, PiM lock, kappa/ellJ, boundary, and gauge owner are now a single local-GR descent gate",
            "effect": "local-GR proof debt is structured rather than diffuse",
        },
        {
            "decision_id": "DEC2579_1_limit",
            "decision": "CURRENT_MTS_PARENT_SIGNATURES_STILL_MISSING",
            "reason": "no current source lists actual local C_i/O_i inventory or signs every zero/gap/PiM/coupling/boundary clause",
            "effect": "no Newton/local-GR claim",
        },
        {
            "decision_id": "DEC2579_2_best_route",
            "decision": "ACTUAL_OPERATOR_INVENTORY_IS_NEXT",
            "reason": "the generic double-zero theorem cannot close without knowing every local non-EH operator that can leak",
            "effect": "move to sector-by-sector inventory and classification",
        },
        {
            "decision_id": "DEC2579_3_fallback",
            "decision": "SOURCE_BACKED_RESIDUAL_BOUNDS_REMAIN_PARALLEL_FALLBACK",
            "reason": "any sector that cannot be parent-zeroed must become a finite nonclaim residual",
            "effect": "testing can proceed honestly after residual rows gain sources/units",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2579_0_selected",
            "selection_status": "selected",
            "target_file": "2580-Y5-R2FR-parent-extra-sector-inventory-coupling-map-or-leakage-bounds.md",
            "target_script": "scripts/Y5_R2FR_parent_extra_sector_inventory_coupling_map_or_leakage_bounds_2580.py",
            "task": "inventory every local non-EH parent operator C_i O_i that could affect metric/source/readout/PiM/coupling sectors, then classify each as parent-derived double-zero, source-bounded, or closure-only residual",
            "acceptance_target": "no unlabelled local coupling remains in the EH descent envelope; every retained sector has C_i(Phi0), partial_A C_i(Phi0), gap, boundary, PiM/coupling effect and claim status recorded",
            "guardrails": "no GitHub; no formalization-workbench edits; no generic double-zero claim without actual inventory; no fitted G/source normalization; no local-GR claim",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "descent_package": OUTPUTS["descent_package"],
        "sector_inventory_seed": OUTPUTS["sector_inventory_seed"],
        "coupling_pim_gate": OUTPUTS["coupling_pim_gate"],
        "residual_envelope": OUTPUTS["residual_envelope"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2579_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2579_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2579_01_descent_verdict_blocked",
        any(row["package_id"] == "EDP2579_7_verdict" and row["current_status"] == "EH_DESCENT_COUPLING_PIM_PACKAGE_NOT_DERIVED_CURRENT_CORPUS" for row in data["descent_package"]),
        "EH descent/coupling/PiM package remains blocked",
    )
    add(
        "VAL2579_02_inventory_seed_complete",
        len(data["sector_inventory_seed"]) >= 8 and all(row["valid_for_claim"] is False for row in data["sector_inventory_seed"]),
        "sector inventory seed covers local leakage classes and remains nonclaim",
    )
    add(
        "VAL2579_03_coupling_pim_verdict_blocked",
        any(row["gate_id"] == "CPG2579_6_verdict" and row["current_status"] == "COUPLING_PIM_LOCK_PACKAGE_NOT_DERIVED" for row in data["coupling_pim_gate"]),
        "coupling plus PiM lock package remains blocked",
    )
    required_residuals = {"epsilon_EH_fixed_point_descent", "F1_extra_linear_leakage_norm", "epsilon_PiM_lock", "delta_kappa", "delta_ellJ", "epsilon_boundary_reference_zero", "epsilon_radial_gauge_owner"}
    actual_residuals = {row["symbol"] for row in data["residual_envelope"]}
    add(
        "VAL2579_04_required_residual_rows",
        required_residuals.issubset(actual_residuals) and all(row["valid_for_claim"] is False and row["score_ready"] is False for row in data["residual_envelope"]),
        "local-GR descent residual rows exist and remain nonclaim/not score-ready",
    )
    add(
        "VAL2579_05_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows EH descent, Newton, or local-GR claim",
    )
    add(
        "VAL2579_06_next_target_written",
        any(row["route_id"] == "NEXT2579_0_selected" for row in data["next"]),
        "2580 parent extra-sector inventory/coupling map target selected",
    )
    add(
        "VAL2579_07_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2579*", "*P8_Y5_EH_DESCENT_COUPLING_PIM_2579*", "*JR2579*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2579_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2579 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2579_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2579_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2579_OVERALL",
        overall,
        "2579 unifies the EH fixed-point descent, coupling baseline, PiM lock and double-zero package, keeps local-GR nonclaim, and selects actual parent extra-sector inventory next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2579 Y5 R2FR EH Fixed-Point Descent Coupling PiM Lock Or Double-Zero Residuals",
        "",
        "**Status:** private nonclaim derivation checkpoint. The local-GR descent package is now unified, but not parent-derived for current MTS.",
        "",
        "**Main result:** the required local branch is: `MTS parent action -> EH core -> stationary Phi0 -> actual C_i/O_i inventory -> C_i(Phi0)=0 -> partial_A C_i(Phi0)=0 -> positive compact gap -> PiM lock -> fixed kappa_MTS/ell_J -> zero boundary flux -> parent-owned areal/isotropic readout`. The generic double-zero theorem is useful, but it is not enough. The next proof must inventory the actual local non-EH operators and classify each one; otherwise every leakage channel remains an explicit residual.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## EH Descent Package Audit",
        markdown_table(data["descent_package"], ["package_id", "required_clause", "mathematical_form", "current_status", "closes_if_signed", "failure_residual", "valid_for_claim"]),
        "",
        "## Extra-Sector Inventory Seed",
        markdown_table(data["sector_inventory_seed"], ["inventory_id", "sector", "possible_operator", "double_zero_test", "current_status", "arenas", "next_action", "valid_for_claim"]),
        "",
        "## Coupling PiM Lock Gate",
        markdown_table(data["coupling_pim_gate"], ["gate_id", "lock", "required_identity", "current_status", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Local-GR Residual Envelope",
        markdown_table(data["residual_envelope"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Newton / GR Implications",
        markdown_table(data["implications"], ["implication_id", "premise_package", "implication", "current_status", "missing_piece", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    BETA_SOURCE.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "descent_package": descent_package_rows(),
        "sector_inventory_seed": sector_inventory_seed_rows(),
        "coupling_pim_gate": coupling_pim_gate_rows(),
        "residual_envelope": residual_envelope_rows(),
        "implications": implication_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["descent_package"], data["descent_package"])
    write_csv(OUTPUTS["sector_inventory_seed"], data["sector_inventory_seed"])
    write_csv(OUTPUTS["coupling_pim_gate"], data["coupling_pim_gate"])
    write_csv(OUTPUTS["residual_envelope"], data["residual_envelope"])
    write_csv(OUTPUTS["implications"], data["implications"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2579_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
