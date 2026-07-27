from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_EXTRA_SECTOR_INVENTORY_COUPLING_MAP_2580"
CHECKPOINT_ID = "2580"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2580-Y5-R2FR-parent-extra-sector-inventory-coupling-map-or-leakage-bounds.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_SOURCE_REGISTER.csv",
    "operator_inventory": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_OPERATOR_INVENTORY.csv",
    "double_zero_matrix": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_DOUBLE_ZERO_STATUS_MATRIX.csv",
    "residual_rows": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_LEAKAGE_RESIDUAL_ROWS.csv",
    "priority_queue": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_PRIORITY_QUEUE.csv",
    "claim_gates": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EXTRA_INVENTORY_COUPLING_2580_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2580_VALIDATION.csv",
}

COPY_TARGETS = {
    "operator_inventory": QUEUE / "JR2580_EXTRA_SECTOR_OPERATOR_INVENTORY_COUPLING_MAP_NONCLAIM.csv",
    "double_zero_matrix": LOCAL_BOUNDS / "Extra_sector_double_zero_status_matrix_2580_NONCLAIM.csv",
    "residual_rows": QUEUE / "JR2580_EXTRA_SECTOR_LEAKAGE_RESIDUAL_ROWS_NONCLAIM.csv",
    "priority_queue": BETA_SOURCE / "EXTRA_SECTOR_INVENTORY_PRIORITY_QUEUE_2580_NONCLAIM.csv",
    "next_target": QUEUE / "JR2580_GAMMAKHAT_QLOC_COUPLING_DOUBLE_ZERO_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2580_00_2579_handoff",
        "source_path": ROOT / "2579-Y5-R2FR-EH-fixed-point-descent-coupling-PiM-lock-or-double-zero-residuals.md",
        "needles": ["NEXT2579_0_selected", "EDP2579_7_verdict", "VAL2579_OVERALL"],
        "role": "active handoff requiring actual parent extra-sector inventory",
    },
    {
        "source_id": "SRC2580_01_2189_inventory",
        "source_path": ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md",
        "needles": ["EI2189_0_GK", "CG2189_5_local_GR", "VAL2189_OVERALL"],
        "role": "prior extra-sector inventory and priority ordering",
    },
    {
        "source_id": "SRC2580_02_1010_GK_gate",
        "source_path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "needles": ["GKT1010_6_verdict", "QRES1010_0_q_loc_vector", "V1010_SUMMARY"],
        "role": "Gamma/Khat/q_loc action-existence and residual-retention gate",
    },
    {
        "source_id": "SRC2580_03_1009_parent_contract",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_4_Gamma_Khat_extra", "DEC1009_1_root_hard_block", "V1009_SUMMARY"],
        "role": "parent sector contract naming Gamma/Khat/q_loc as hard block",
    },
    {
        "source_id": "SRC2580_04_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["Gamma_eff", "q_loc^nu", "Pi_M"],
        "role": "symbol-to-action map for dangerous local variables",
    },
    {
        "source_id": "SRC2580_05_response_doublet",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "needles": ["RD516_1_even_scalar_density", "RD516_4_zero_odd_source", "RD516_5_PPN_lock"],
        "role": "response/memory doublet candidate and its missing physical lock",
    },
    {
        "source_id": "SRC2580_06_PiM_contract",
        "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "needles": ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"],
        "role": "PiM projector variation, commutator and source-measure residuals",
    },
    {
        "source_id": "SRC2580_07_kappa_contract",
        "source_path": OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv",
        "needles": ["T508_0_global_sector", "T508_1_topological_zeroform"],
        "role": "constant-kappa superselection/topological candidate",
    },
    {
        "source_id": "SRC2580_08_2579_validation",
        "source_path": OUT / "P8_Y5_BRR545_2579_VALIDATION.csv",
        "needles": ["VAL2579_OVERALL", "PASS"],
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


def inventory_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "sector_id": "EI2580_0_GK",
            "parent_sector": "Gamma/Khat/q_loc",
            "coupling_symbol": "C_GK(Phi) or T_GK(Phi)",
            "operator_symbol": "O_GK = variational metric-response stress from Gamma_eff and K_hat",
            "fields": "Gamma_eff;K_hat;q_loc^nu;P_loc;Phi^A",
            "local_effect": "direct PPN/local force residual, source-normalization leakage and R10/R11 residual interface",
            "classification": "HARD_BLOCK_DERIVATION_FIRST",
            "C0_test": "T_GK(Phi0)=0 after accepted background subtraction",
            "dC_test": "partial_A T_GK(Phi0)=0",
            "gap_or_closure_test": "S_GK action existence, metric-response equality, Helmholtz integrability, Euler/Ward closure",
            "boundary_test": "theta_GK/Q_GK no-flux plus source-current zero",
            "coupling_effect": "feeds q_loc^nu, preferred-frame PPN, local force and source-mass normalization",
            "next_action": "take as 2581 first target",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_1_response_memory",
            "parent_sector": "response/memory doublet",
            "coupling_symbol": "C_mem(Z)",
            "operator_symbol": "O_mem = even response density / memory stress",
            "fields": "R_+^A;R_-^A;Z^A;memory variables",
            "local_effect": "compact-local memory hair, clock drift, PPN/source-normalization leakage",
            "classification": "CANDIDATE_NOT_MATCHED_TO_PHYSICAL_LOCK",
            "C0_test": "Gamma_eff even/background-subtracted",
            "dC_test": "odd/linear response source zero",
            "gap_or_closure_test": "positive Z operator and PPN-lock map",
            "boundary_test": "B_Z=0 and no metric-response boundary flux",
            "coupling_effect": "possible mechanism for GK double-zero but not yet mapped to physical residual vector",
            "next_action": "use only after GK target fixes physical residual map",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_2_domain_projector",
            "parent_sector": "domain/projector selector",
            "coupling_symbol": "C_D(Phi)",
            "operator_symbol": "O_D = selector/projector stress and preferred-frame load",
            "fields": "u;h;X;Qcoh;chi_D;lambda_D;P_loc",
            "local_effect": "preferred-frame PPN, WEP/source selection and local/cosmology branch switching",
            "classification": "PARTIAL_CLAUSE_NOT_PARENT_CLOSED",
            "C0_test": "local selector/projector stress zero",
            "dC_test": "selector derivative/commutator zero",
            "gap_or_closure_test": "domain operator positive, algebraic or topological",
            "boundary_test": "domain boundary no-flux and no hidden source selection",
            "coupling_effect": "can change which branch is local without deriving transition scale",
            "next_action": "derive P_loc/domain before readout or keep explicit residual",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_3_metric_readout",
            "parent_sector": "metric/readout protection",
            "coupling_symbol": "D_A g_readout|Phi0",
            "operator_symbol": "O_readout = metric/coframe perturbation seen by clocks, rods and light",
            "fields": "g_obs;g_readout;e_obs;radial/angle gauge",
            "local_effect": "PPN beta/gamma/light-time/orbital mismatch even if source charge works",
            "classification": "READOUT_PROTECTION_OPEN",
            "C0_test": "g_readout(Phi0)=g_obs",
            "dC_test": "D_A g_readout(Phi0)=0",
            "gap_or_closure_test": "readout functional lock, not a bulk gap",
            "boundary_test": "radial/angle boundary coframe owner",
            "coupling_effect": "turns gauge debt into physical residual if not parent-owned",
            "next_action": "link to areal/isotropic parent readout owner",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_4_PiM",
            "parent_sector": "PiM/source-measure projector",
            "coupling_symbol": "Pi_M(Phi)-Pi_EH",
            "operator_symbol": "O_PiM = Hamiltonian mass-current projector and source charge",
            "fields": "Pi_M;J_H;omega_M;Sigma_ext;M_H_ref",
            "local_effect": "Newton source normalization, R10/R11 alpha rows and measured-GM calibration",
            "classification": "PARALLEL_BLOCKER_NOT_PARENT_DERIVED",
            "C0_test": "Pi_M(Phi0)=Pi_EH",
            "dC_test": "partial_A Pi_M(Phi0)=0",
            "gap_or_closure_test": "projector Ward/Euler closure and Hamiltonian identity",
            "boundary_test": "I_commutator/R_eq/B_zero no-flux",
            "coupling_effect": "even if GK closes, measured GM can still be wrong",
            "next_action": "keep parallel with GK; never absorb into G",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_5_species",
            "parent_sector": "universal matter/species source",
            "coupling_symbol": "partial_A ln m_species(Phi0)",
            "operator_symbol": "O_species = matter/source charge slope and composition current",
            "fields": "psi_A;e_obs;theta_A;J_univ;ell_J",
            "local_effect": "WEP, clock composition and source mass split",
            "classification": "UNIVERSALITY_OPEN",
            "C0_test": "species constants source-blind",
            "dC_test": "partial_A species/source charges zero",
            "gap_or_closure_test": "matter factorization through e_obs",
            "boundary_test": "bulk/boundary composition charge zero",
            "coupling_effect": "ell_J/source mass can become a hidden fit parameter",
            "next_action": "derive species-blind matter action or source WEP residuals",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_6_boundary",
            "parent_sector": "boundary/reference/exact/topological",
            "coupling_symbol": "C_B(Phi)",
            "operator_symbol": "O_B = theta_boundary, Q_tau_boundary, exact/topological improvement",
            "fields": "B_ref;Q_tau;theta;edge classes;counterterms",
            "local_effect": "hidden mass flux, reference drift and PPN/source-charge shift",
            "classification": "BOUNDARY_ZERO_OPEN",
            "C0_test": "fixed reference or zero extra boundary term",
            "dC_test": "boundary derivative silent",
            "gap_or_closure_test": "fixed-reference theorem or edge dynamics closure",
            "boundary_test": "compact linking-sphere flux zero",
            "coupling_effect": "can absorb kappa/ell_J drift by boundary bookkeeping",
            "next_action": "derive fixed-before-readout boundary/reference class",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_7_kappa",
            "parent_sector": "kappa_eff/G_eff topological sector",
            "coupling_symbol": "D_A kappa_eff",
            "operator_symbol": "O_kappa = local Newton coupling / EH normalization",
            "fields": "kappa_eff;A_3;G_eff",
            "local_effect": "Gdot, radial G drift and source normalization",
            "classification": "CONDITIONAL_SUPERSELECTION_NOT_ADOPTED_HERE",
            "C0_test": "d kappa_eff=0 on connected local domains",
            "dC_test": "no species/range/frame/domain labels",
            "gap_or_closure_test": "topological zero-form/three-form pair",
            "boundary_test": "boundary level convention fixed once",
            "coupling_effect": "direct delta_kappa term in Newton/local-GR envelope",
            "next_action": "adopt/derive topological sector or demote to residual",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_8_transition",
            "parent_sector": "local/cosmology transition activation",
            "coupling_symbol": "A_tr(Phi,source_scale)",
            "operator_symbol": "O_tr = activation/suppression functional between compact local and cosmological branches",
            "fields": "ell_tr;L_cg;source scale;operator spectrum",
            "local_effect": "hand switching between GR local branch and MTS galaxy/cosmology branch",
            "classification": "TRANSITION_CONTROL_OPEN",
            "C0_test": "A_tr local compact limit zero",
            "dC_test": "derivative zero below compact activation threshold",
            "gap_or_closure_test": "derived from spectrum/source scale",
            "boundary_test": "boundary/domain transition flux open",
            "coupling_effect": "can make local-GR recovery a manual switch unless derived",
            "next_action": "derive activation scale from operator spectrum, not a fit knob",
            "valid_for_claim": False,
        },
        {
            "sector_id": "EI2580_9_worldtube_source",
            "parent_sector": "worldtube/source glue",
            "coupling_symbol": "C_W(Phi)",
            "operator_symbol": "O_W = Hilbert current/topological current/worldtube charge equality",
            "fields": "W_source;J_H;J_M_top;B_zero;R_eq",
            "local_effect": "conserved wrong object and measured source mass mismatch",
            "classification": "SOURCE_GLUE_OPEN",
            "C0_test": "same Hilbert source class",
            "dC_test": "R_eq derivative/annulus variation zero",
            "gap_or_closure_test": "source current Ward/Euler closure",
            "boundary_test": "B_zero flux zero",
            "coupling_effect": "epsilon_M and ell_J source closure remain live",
            "next_action": "keep as parallel source-measure gate after GK/PiM",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def double_zero_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority = {
        "EI2580_0_GK": "highest",
        "EI2580_4_PiM": "highest_parallel",
        "EI2580_2_domain_projector": "high",
        "EI2580_3_metric_readout": "high",
        "EI2580_1_response_memory": "high",
        "EI2580_9_worldtube_source": "high_parallel",
    }
    rows = []
    for row in inventory:
        sector_id = row["sector_id"]
        if sector_id == "EI2580_1_response_memory":
            c0_status = d_status = gap_status = "candidate_only"
            boundary_status = "open"
        elif sector_id == "EI2580_7_kappa":
            c0_status = d_status = "conditional"
            gap_status = "topological_candidate"
            boundary_status = "open"
        else:
            c0_status = "not_signed" if sector_id in {"EI2580_0_GK", "EI2580_4_PiM"} else "open"
            d_status = "not_signed" if sector_id in {"EI2580_0_GK", "EI2580_4_PiM"} else "open"
            gap_status = "not_signed" if sector_id == "EI2580_0_GK" else "open"
            boundary_status = "not_signed" if sector_id == "EI2580_0_GK" else "open"
        rows.append(
            stamp(
                {
                    "sector_id": sector_id,
                    "parent_sector": row["parent_sector"],
                    "C0_status": c0_status,
                    "dC_status": d_status,
                    "gap_or_closure_status": gap_status,
                    "boundary_status": boundary_status,
                    "priority": priority.get(sector_id, "medium_high"),
                    "promotion_status": "not_promoted",
                    "reason": "current evidence inventory only; no full parent signature with source/equation path is present",
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def residual_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    residual_map = {
        "EI2580_0_GK": ("LR2580_0_GK", "epsilon_C0_GammaKhat;epsilon_dC_GammaKhat;q_loc^nu", "direct PPN/local force residual and source-normalization leakage"),
        "EI2580_1_response_memory": ("LR2580_1_response_memory", "epsilon_C0_memory_response;epsilon_dC_memory_response", "compact-local memory hair, clock drift and PPN leakage"),
        "EI2580_2_domain_projector": ("LR2580_2_domain_projector", "epsilon_domain_projector_stress;P_loc_commutator", "preferred-frame PPN, WEP/source selection and branch switching"),
        "EI2580_3_metric_readout": ("LR2580_3_metric_readout", "epsilon_readout_gauge_owner;epsilon_metric_readout_linear", "2PN/PPN/orbital readout leakage"),
        "EI2580_4_PiM": ("LR2580_4_PiM", "epsilon_PiM_value;epsilon_DPiM;I_commutator;R_eq_integral", "Newton source normalization and measured-GM calibration leakage"),
        "EI2580_5_species": ("LR2580_5_species", "epsilon_species_coupling;eta_source_AB;delta_ellJ", "WEP, clock composition and source mass split"),
        "EI2580_6_boundary": ("LR2580_6_boundary", "epsilon_boundary_reference_zero;B_zero_flux;Delta_boundary_coupling", "hidden mass flux, reference drift and source-charge shift"),
        "EI2580_7_kappa": ("LR2580_7_kappa", "epsilon_kappa_drift;epsilon_G_eff_source;delta_kappa", "Gdot, radial G drift and source normalization"),
        "EI2580_8_transition": ("LR2580_8_transition", "epsilon_transition_leak;ell_tr_over_Lcg", "manual local/cosmology branch switching"),
        "EI2580_9_worldtube_source": ("LR2580_9_worldtube_source", "R_eq_integral;B_zero_flux;epsilon_M;delta_ellJ", "wrong conserved object and measured source mass mismatch"),
    }
    rows = []
    for row in inventory:
        residual_id, symbols, definition = residual_map[row["sector_id"]]
        rows.append(
            stamp(
                {
                    "row_id": residual_id,
                    "symbol": symbols,
                    "definition": definition,
                    "value": "MISSING_COMPONENT_INPUTS",
                    "status": f"MISSING_PARENT_SIGNATURE_{row['classification']}",
                    "units": "dimensionless_or_declared_per_sector",
                    "observable_link": row["local_effect"],
                    "source_path": "MISSING_SOURCE_PATH",
                    "score_ready": False,
                    "valid_for_claim": False,
                }
            )
        )
    rows.append(
        stamp(
            {
                "row_id": "LR2580_TOTAL",
                "symbol": "Delta_local_GR_extra_inventory_coupled_abs",
                "definition": "absolute no-cancellation envelope over all inventoried extra-sector leakage and coupling residual families",
                "value": "MISSING_COMPONENT_INPUTS",
                "status": "MISSING_SECTOR_COMPONENT_INPUTS",
                "units": "dimensionless_or_declared",
                "observable_link": "local_GR;Newton;PPN;WEP;R10;R11",
                "source_path": "MISSING_SOURCE_PATH",
                "score_ready": False,
                "valid_for_claim": False,
            }
        )
    )
    return rows


def priority_rows() -> list[dict[str, Any]]:
    rows = [
        ("PR2580_0_GK", 1, "Gamma/Khat/q_loc", "direct local force/PPN residual; 1009 and 1010 already identify it as the hard block", "2581 derive C_GK/T_GK double-zero or lock q_loc residual"),
        ("PR2580_1_PiM", 2, "PiM/source-measure", "even a solved force residual fails Newton if measured GM projector is unowned", "keep parallel; do not absorb into G"),
        ("PR2580_2_domain_readout", 3, "domain/projector plus metric readout", "prevents branch switching and 2PN/PPN readout leakage", "derive P_loc/readout owner after GK route"),
        ("PR2580_3_response", 4, "response/memory doublet", "possible mechanism for double-zero, but not yet mapped to physical q_loc/PPN vector", "map components only after GK target is explicit"),
        ("PR2580_4_boundary_source", 5, "boundary/worldtube/species/kappa/transition", "important parallel residuals, but less surgical than GK for immediate local-GR survival", "retain as ledger; source or derive in later gates"),
    ]
    return [
        stamp(
            {
                "priority_id": priority_id,
                "rank": rank,
                "target_sector": sector,
                "reason": reason,
                "next_action": next_action,
                "valid_for_claim": False,
            }
        )
        for priority_id, rank, sector, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2580_0_inventory", "current extra-sector coupling inventory exists", "PASS_GUARDRAIL", "known local leakage suspects are explicit rows", True),
        ("CG2580_1_coverage", "inventory is complete enough for local-GR claim", "BLOCKED_NONCLAIM", "this is current-evidence inventory, not proof that the whole corpus has no other operators", False),
        ("CG2580_2_double_zero", "each inventoried C_i has parent-signed C0 and dC zero", "BLOCKED_NONCLAIM", "no inventoried sector has a full parent-signed double-zero certificate", False),
        ("CG2580_3_gap_boundary", "each sector has positive gap/closure and boundary silence", "BLOCKED_NONCLAIM", "gap, Ward/Euler, readout and boundary clauses remain open", False),
        ("CG2580_4_PiM_coupling", "PiM/source-measure and kappa/ell_J blockers are closed", "BLOCKED_NONCLAIM", "PiM, source-current and coupling residuals remain live", False),
        ("CG2580_5_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "inventory improves targeting but does not close descent", False),
        ("CG2580_6_no_shortcuts", "generic double-zero theorem or incomplete inventory can be promoted", "PASS_GUARDRAIL", "promotion is explicitly forbidden without parent-signed sector certificates", True),
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
            "decision_id": "DEC2580_0_gain",
            "decision": "POST_CHECKPOINT_COUPLING_INVENTORY_WRITTEN",
            "reason": "the 2189 inventory is updated into the 2579 coupling/PiM descent package and now tracks kappa/ell_J leakage explicitly",
            "effect": "no unlabelled local coupling is allowed to hide in the local-GR descent envelope",
        },
        {
            "decision_id": "DEC2580_1_limit",
            "decision": "NO_FULL_DOUBLE_ZERO_PROMOTION",
            "reason": "no sector currently carries a full parent-signed C_i(Phi0)=0, partial_A C_i(Phi0)=0, positive closure, and boundary silence proof",
            "effect": "no local-GR claim",
        },
        {
            "decision_id": "DEC2580_2_priority",
            "decision": "GAMMA_KHAT_QLOC_FIRST",
            "reason": "GK/q_loc is the direct local force and PPN residual channel; if it is bookkeeping rather than variational, local-GR descent fails",
            "effect": "next checkpoint attacks GK action-existence/metric-response/Helmholtz/Euler double-zero",
        },
        {
            "decision_id": "DEC2580_3_parallel",
            "decision": "PIM_SOURCE_MEASURE_PARALLEL_BLOCKER",
            "reason": "even if GK closes, measured source mass can still be wrong without PiM/Hamiltonian/source glue",
            "effect": "keep PiM residuals parallel, never absorb them into measured G",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2580_0_selected",
            "selection_status": "selected",
            "target_file": "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
            "target_script": "scripts/Y5_R2FR_GammaKhat_q_loc_coupling_double_zero_or_residual_lock_2581.py",
            "task": "take the EI2580_0 Gamma/Khat/q_loc sector and either derive its parent action, metric response, Helmholtz/Euler closure, T_GK(Phi0)=0, partial_A T_GK(Phi0)=0, P_loc and boundary silence, or lock q_loc as an explicit local-test residual",
            "acceptance_target": "C_GK/T_GK double-zero is parent-signed with source equations, or q_loc residual rows become the official local PPN/R10 interface with no theorem-zero claim",
            "guardrails": "do not repeat a generic double-zero theorem; do not use plateau silence; do not claim q_loc=0 without metric-response and Helmholtz/Euler proof; no GitHub; no formalization-workbench edits",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "operator_inventory": OUTPUTS["operator_inventory"],
        "double_zero_matrix": OUTPUTS["double_zero_matrix"],
        "residual_rows": OUTPUTS["residual_rows"],
        "priority_queue": OUTPUTS["priority_queue"],
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
                    "copy_id": f"COPY2580_{key}",
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

    add("VAL2580_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    required_sectors = {"EI2580_0_GK", "EI2580_1_response_memory", "EI2580_2_domain_projector", "EI2580_3_metric_readout", "EI2580_4_PiM", "EI2580_5_species", "EI2580_6_boundary", "EI2580_7_kappa", "EI2580_8_transition", "EI2580_9_worldtube_source"}
    actual_sectors = {row["sector_id"] for row in data["operator_inventory"]}
    add(
        "VAL2580_01_inventory_coverage",
        required_sectors == actual_sectors,
        f"inventory rows={len(actual_sectors)}; required sectors covered={len(required_sectors.intersection(actual_sectors))}/10",
    )
    add(
        "VAL2580_02_no_promotions",
        all(row["promotion_status"] == "not_promoted" and row["valid_for_claim"] is False for row in data["double_zero_matrix"]),
        "all inventory rows remain not_promoted/nonclaim",
    )
    add(
        "VAL2580_03_coupling_explicit",
        any(row["sector_id"] == "EI2580_7_kappa" for row in data["operator_inventory"]) and any("delta_ellJ" in row["symbol"] for row in data["residual_rows"]),
        "kappa and ell_J/source coupling residuals are explicit",
    )
    add(
        "VAL2580_04_residual_rows",
        any(row["row_id"] == "LR2580_TOTAL" for row in data["residual_rows"]) and all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["residual_rows"]),
        "residual rows remain missing/source-free/nonclaim",
    )
    add(
        "VAL2580_05_priority",
        any(row["priority_id"] == "PR2580_0_GK" and row["rank"] == 1 for row in data["priority_queue"]),
        "Gamma/Khat/q_loc selected as first derivation target",
    )
    add(
        "VAL2580_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "inventory is a guardrail, not a local-GR claim",
    )
    add(
        "VAL2580_07_next_target_written",
        any(row["route_id"] == "NEXT2580_0_selected" for row in data["next"]),
        "2581 Gamma/Khat/q_loc target selected",
    )
    add(
        "VAL2580_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )
    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2580*", "*P8_Y5_EXTRA_INVENTORY_COUPLING_2580*", "*JR2580*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2580_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2580 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2580_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2580_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2580_OVERALL",
        overall,
        "2580 writes the post-checkpoint extra-sector coupling inventory, keeps all sectors nonclaim, and selects Gamma/Khat/q_loc as the first derivation target",
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
        "# 2580 Y5 R2FR Parent Extra-Sector Inventory Coupling Map Or Leakage Bounds",
        "",
        "**Status:** private nonclaim inventory checkpoint. The local-GR descent theorem is not proven, but the dangerous local non-EH sectors are now explicit in the post-2579 coupling/PiM language.",
        "",
        "**Main result:** this checkpoint prevents another loop around the generic double-zero theorem. The live local leakage map is `Gamma/Khat/q_loc`, response/memory, domain/projector, metric readout, PiM/source-measure, species/source frame, boundary/reference, kappa/G, transition activation, and worldtube/source glue. No sector is promoted. `Gamma/Khat/q_loc` is selected first because it directly decides whether the local residual is a variational on-shell zero or a live PPN/R10 force residual.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Operator Inventory",
        markdown_table(data["operator_inventory"], ["sector_id", "parent_sector", "coupling_symbol", "operator_symbol", "fields", "local_effect", "classification", "C0_test", "dC_test", "gap_or_closure_test", "boundary_test", "coupling_effect", "next_action", "valid_for_claim"]),
        "",
        "## Double-Zero Status Matrix",
        markdown_table(data["double_zero_matrix"], ["sector_id", "parent_sector", "C0_status", "dC_status", "gap_or_closure_status", "boundary_status", "priority", "promotion_status", "reason", "valid_for_claim"]),
        "",
        "## Residual Rows",
        markdown_table(data["residual_rows"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Priority Queue",
        markdown_table(data["priority_queue"], ["priority_id", "rank", "target_sector", "reason", "next_action", "valid_for_claim"]),
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

    inventory = inventory_rows()
    data = {
        "sources": source_register_rows(),
        "operator_inventory": inventory,
        "double_zero_matrix": double_zero_rows(inventory),
        "residual_rows": residual_rows(inventory),
        "priority_queue": priority_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["operator_inventory"], data["operator_inventory"])
    write_csv(OUTPUTS["double_zero_matrix"], data["double_zero_matrix"])
    write_csv(OUTPUTS["residual_rows"], data["residual_rows"])
    write_csv(OUTPUTS["priority_queue"], data["priority_queue"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2580_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
