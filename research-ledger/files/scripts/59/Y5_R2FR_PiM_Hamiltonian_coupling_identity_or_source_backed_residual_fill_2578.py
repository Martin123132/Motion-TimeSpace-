from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PIM_HAMILTONIAN_COUPLING_IDENTITY_2578"
CHECKPOINT_ID = "2578"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2578-Y5-R2FR-PiM-Hamiltonian-coupling-identity-or-source-backed-residual-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_SOURCE_REGISTER.csv",
    "phase_space_audit": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COVARIANT_PHASE_SPACE_IDENTITY_AUDIT.csv",
    "transfer_gate": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_MTS_TRANSFER_PREMISE_GATE.csv",
    "coupling_gate": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv",
    "residual_ledger": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv",
    "implications": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_NEWTON_LOCAL_GR_IMPLICATIONS.csv",
    "claim_gates": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2578_VALIDATION.csv",
}

COPY_TARGETS = {
    "phase_space_audit": QUEUE / "JR2578_PIM_HAMILTONIAN_COUPLING_IDENTITY_AUDIT_NONCLAIM.csv",
    "transfer_gate": QUEUE / "JR2578_MTS_TRANSFER_PREMISE_GATE_NONCLAIM.csv",
    "coupling_gate": LOCAL_BOUNDS / "PiM_Hamiltonian_coupling_baseline_gate_2578_NONCLAIM.csv",
    "residual_ledger": QUEUE / "JR2578_PIM_HAMILTONIAN_COUPLING_RESIDUAL_LEDGER_NONCLAIM.csv",
    "next_target": QUEUE / "JR2578_EH_FIXED_POINT_DESCENT_COUPLING_PIM_LOCK_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2578_00_2577_handoff",
        "source_path": ROOT / "2577-Y5-R2FR-worldtube-Hilbert-source-selector-coupling-and-zero-boundary-flux-or-R-eq-fill.md",
        "needles": ["NEXT2577_0_selected", "WSC2577_2_Hamiltonian_PiM_identity", "EPS2577_2_absolute_envelope", "VAL2577_OVERALL"],
        "role": "active handoff selecting PiM/Hamiltonian/coupling identity",
    },
    {
        "source_id": "SRC2578_01_2184_action_contract",
        "source_path": ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
        "needles": ["MAS2184_4_Hamiltonian_PiM", "NHC2184_4_PiM_identification", "VAL2184_OVERALL"],
        "role": "minimal parent-action charge contract and PiM identity blocker",
    },
    {
        "source_id": "SRC2578_02_2185_EH_coefficients",
        "source_path": ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
        "needles": ["IHG2185_2_PiM", "CG2185_2_source_glue", "VAL2185_OVERALL"],
        "role": "EH fixed-point coefficient extraction and PiM/source glue debt",
    },
    {
        "source_id": "SRC2578_03_2186_descent",
        "source_path": ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
        "needles": ["DEG2186_4_PiM_lock", "DEG2186_7_verdict", "VAL2186_OVERALL"],
        "role": "MTS EH descent and PiM lock blocker",
    },
    {
        "source_id": "SRC2578_04_T510_worldtube_measure",
        "source_path": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "needles": ["T510_0_EH_reference_glue", "T510_2_MTS_transfer_condition"],
        "role": "covariant Noether/Hamiltonian source measure transfer condition",
    },
    {
        "source_id": "SRC2578_05_HSM541_measure_contract",
        "source_path": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_1_integrable_charge", "HSM541_6_constant_universal_G"],
        "role": "Hamiltonian PiM, integrable charge, and constant coupling contract",
    },
    {
        "source_id": "SRC2578_06_PAC537_parent_contract",
        "source_path": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "needles": ["PAC537_4_action_owned_PiM_projector", "PAC537_6_reference_and_boundary_zero"],
        "role": "parent-owned PiM projector and boundary-reference clauses",
    },
    {
        "source_id": "SRC2578_07_A511_action_blocks",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "needles": ["A511_0_EH_core", "A511_1_kappa_topological", "A511_6_metric_readout"],
        "role": "minimal local-GR action blocks: EH core, kappa constancy, and readout/PiM double zero",
    },
    {
        "source_id": "SRC2578_08_FP511_conditions",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
        "needles": ["FP511_3_constant_kappa", "FP511_5_parent_PiM_lock", "FP511_6_boundary_no_flux"],
        "role": "fixed-point conditions for constant kappa, PiM lock, and boundary no flux",
    },
    {
        "source_id": "SRC2578_09_T505_noether",
        "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "needles": ["T505_conditional_Noether_mass_charge_closure", "T505_source_measure_matching"],
        "role": "conditional Noether mass-charge closure and source measure matching theorem",
    },
    {
        "source_id": "SRC2578_10_2577_validation",
        "source_path": OUT / "P8_Y5_BRR545_2577_VALIDATION.csv",
        "needles": ["VAL2577_OVERALL", "PASS"],
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


def phase_space_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "CPS2578_0_Noether_current",
            "identity": "covariant diffeomorphism Noether current",
            "mathematical_form": "J_tau = Theta(phi,Lie_tau phi) - i_tau L; on shell J_tau = dQ_tau plus constraints",
            "status": "STANDARD_CONDITIONAL_REFERENCE",
            "would_close": "defines a surface charge independent of linked sphere when constraints and boundary flux vanish",
            "current_blocker": "MTS parent symplectic potential and constraint split are not explicitly derived",
            "coupling_clause": "L must contain the same fixed kappa_MTS coefficient used in local v dynamics",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPS2578_1_Hamiltonian_variation",
            "identity": "covariant phase-space Hamiltonian charge",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau - i_tau Theta), with one fixed reference subtraction",
            "status": "STANDARD_CONDITIONAL_REFERENCE",
            "would_close": "turns exterior charge into dressed source mass rather than bare rest mass",
            "current_blocker": "integrability, fixed reference, and zero symplectic/boundary flux are not certified for MTS",
            "coupling_clause": "reference cannot absorb delta_kappa or delta_ellJ",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPS2578_2_PiM_Hamiltonian_identity",
            "identity": "Pi_M as Hamiltonian mass map",
            "mathematical_form": "(4*pi*G_ref)^-1 integral_S Pi_M J_H = H_tau[S] - H_tau[reference]",
            "status": "CORE_IDENTITY_NOT_DERIVED_CURRENT_CORPUS",
            "would_close": "identifies Pi_M J_H with measured dressed source mass",
            "current_blocker": "Pi_M is still a projector contract, not a parent-derived Hamiltonian map",
            "coupling_clause": "G_ref must be inherited from kappa_MTS, not chosen after the readout",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPS2578_3_EH_transfer",
            "identity": "MTS local branch inherits EH Hamiltonian charge",
            "mathematical_form": "Q_MTS_tau = Q_EH_tau + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_kappa + Delta_ellJ",
            "status": "EXACT_TRANSFER_LEDGER",
            "would_close": "if every Delta term vanishes or is bounded, EH source measure can be inherited rather than imported",
            "current_blocker": "extra double zeros, PiM lock, boundary flux, readout frame, and coupling constancy remain open",
            "coupling_clause": "Delta_kappa and Delta_ellJ are explicit transfer terms",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPS2578_4_source_matching",
            "identity": "same Hilbert matter source controls Hamiltonian charge and v source equation",
            "mathematical_form": "rho_v dV_obs = ell_J J_H[tau] projected through Pi_M^H on the same W_source",
            "status": "SOURCE_MATCHING_NOT_DERIVED",
            "would_close": "prevents right coefficient algebra with wrong measured mass",
            "current_blocker": "single observed source frame and ell_J normalization are not parent-owned",
            "coupling_clause": "ell_J must not be a late source-scale fit",
            "valid_for_claim": False,
        },
        {
            "audit_id": "CPS2578_5_current_verdict",
            "identity": "PiM/Hamiltonian/coupling identity for current MTS",
            "mathematical_form": "Pi_M J_H = Pi_M^H J_H with fixed kappa_MTS, fixed ell_J, fixed reference, silent extra sectors, and zero boundary flux",
            "status": "PIM_HAMILTONIAN_COUPLING_IDENTITY_NOT_DERIVED_CURRENT_CORPUS",
            "would_close": "would close epsilon_PiM_Hamiltonian and make the source-selector route viable",
            "current_blocker": "current corpus provides a coherent contract, not the parent action/symplectic derivation",
            "coupling_clause": "coupling ownership is still a theorem premise, not metadata",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def transfer_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "TR2578_0_EH_core",
            "premise": "local compact branch reduces to EH core",
            "required_form": "S_parent -> S_EH[e_obs,kappa_eff] plus locally silent sectors",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_missing": "epsilon_EH_fixed_point_descent",
            "valid_for_claim": False,
        },
        {
            "gate_id": "TR2578_1_constant_kappa",
            "premise": "kappa_eff is locally constant and universal",
            "required_form": "d kappa_eff=0 from topological/superselection parent sector",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_missing": "delta_kappa",
            "valid_for_claim": False,
        },
        {
            "gate_id": "TR2578_2_universal_matter",
            "premise": "matter couples to one observed source frame",
            "required_form": "S_matter[psi,g_obs] with no species/source-dependent extra coupling at leading local order",
            "current_status": "OPEN",
            "residual_if_missing": "epsilon_source_frame;delta_ellJ",
            "valid_for_claim": False,
        },
        {
            "gate_id": "TR2578_3_extra_double_zero",
            "premise": "extra sectors have double zeros at the local fixed point",
            "required_form": "C_i(Phi0)=0 and partial_A C_i(Phi0)=0 with positive source-free operators",
            "current_status": "REQUIRED_NOT_PROVED",
            "residual_if_missing": "Delta_extra;epsilon_extra_mass_charge",
            "valid_for_claim": False,
        },
        {
            "gate_id": "TR2578_4_PiM_lock",
            "premise": "Pi_M is the EH/Hamiltonian mass projector at the fixed point",
            "required_form": "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0",
            "current_status": "PIM_LOCK_OPEN",
            "residual_if_missing": "epsilon_PiM_lock;epsilon_PiM_Hamiltonian",
            "valid_for_claim": False,
        },
        {
            "gate_id": "TR2578_5_boundary_no_flux",
            "premise": "local boundary/reference terms carry no extra mass flux",
            "required_form": "integral_boundary Delta(theta,Q,tau)=0 or fixed background subtraction",
            "current_status": "OPEN",
            "residual_if_missing": "Delta_boundary;B_zero_flux",
            "valid_for_claim": False,
        },
        {
            "gate_id": "TR2578_6_transfer_verdict",
            "premise": "MTS inherits EH Hamiltonian mass map with coupling",
            "required_form": "all transfer residuals vanish in the same local branch",
            "current_status": "MTS_TRANSFER_PREMISES_NOT_PARENT_SIGNED",
            "residual_if_missing": "Delta_PiM_H_abs",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def coupling_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "coupling_id": "COG2578_0_kappa_constant",
            "quantity": "kappa_MTS",
            "required_identity": "d kappa_MTS=0 on connected local exterior domains",
            "current_status": "CONDITIONAL_FROM_TOPOLOGICAL_BLOCK_NOT_PARENT_SIGNED",
            "failure_mode": "G_eff drift or radial/source-dependent gravitational coupling",
            "residual_symbol": "delta_kappa",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COG2578_1_Gref_match",
            "quantity": "G_ref",
            "required_identity": "G_ref is the inverse EH coefficient induced by kappa_MTS in the same frame",
            "current_status": "MATCH_NOT_DERIVED",
            "failure_mode": "right EH algebra but wrong normalization against measured source mass",
            "residual_symbol": "epsilon_Gref_match",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COG2578_2_ellJ_source_scale",
            "quantity": "ell_J",
            "required_identity": "ell_J is fixed by the parent matter/source-current normalization before readout",
            "current_status": "SOURCE_SCALE_OWNER_OPEN",
            "failure_mode": "source mass and orbital mass differ by a hidden scale factor",
            "residual_symbol": "delta_ellJ",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COG2578_3_no_reference_absorption",
            "quantity": "boundary/reference coupling silence",
            "required_identity": "H_tau[reference] and B_zero do not absorb kappa or ell_J shifts",
            "current_status": "REFERENCE_ABSORPTION_NOT_EXCLUDED",
            "failure_mode": "boundary bookkeeping mimics source-closure",
            "residual_symbol": "Delta_boundary_coupling",
            "valid_for_claim": False,
        },
        {
            "coupling_id": "COG2578_4_verdict",
            "quantity": "coupling baseline package",
            "required_identity": "kappa_MTS, G_ref, ell_J, PiM, and reference subtraction are fixed together by the parent action",
            "current_status": "COUPLING_BASELINE_IDENTITY_NOT_DERIVED",
            "failure_mode": "PiM/Hamiltonian identity cannot be used as source proof",
            "residual_symbol": "delta_kappa;delta_ellJ;epsilon_Gref_match;Delta_boundary_coupling",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("RES2578_0_PiM_H", "epsilon_PiM_Hamiltonian", "failure of Pi_M J_H to equal the Hamiltonian mass-charge form", "MISSING_PIM_HAMILTONIAN_IDENTITY", "dimensionless_or_GM_flux", "Newton;PPN;R10;R11"),
        ("RES2578_1_symp", "Delta_symp", "extra symplectic potential contribution to delta H_tau or radial charge drift", "MISSING_SYMPLECTIC_ZERO_OR_BOUND", "GM_flux", "Newton;PPN;local_GR"),
        ("RES2578_2_constraint", "Delta_constraint", "nonzero exterior constraint flux between linked surfaces", "MISSING_CONSTRAINT_FLUX_ZERO_OR_BOUND", "GM_flux", "Newton;orbital"),
        ("RES2578_3_boundary", "Delta_boundary", "fixed-reference, exact-term, inner/outer boundary, or B_zero flux residual", "MISSING_BOUNDARY_ZERO_OR_BOUND", "GM_flux_or_dimensionless", "Newton;PPN;R10;R11"),
        ("RES2578_4_extra", "Delta_extra", "nonEH/memory/motion/time/range/frame sector mass-charge contribution", "MISSING_EXTRA_DOUBLE_ZERO_OR_BOUND", "dimensionless_or_GM_flux", "WEP;PPN;local_GR"),
        ("RES2578_5_PiM_lock", "epsilon_PiM_lock", "failure of Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0", "MISSING_PARENT_PIM_LOCK", "dimensionless_or_GM_flux", "Newton;R10;R11;PPN"),
        ("RES2578_6_source_frame", "epsilon_source_frame", "failure of Hilbert source frame to match v-source and orbital/clock readout frame", "MISSING_UNIVERSAL_SOURCE_FRAME", "dimensionless", "WEP;Newton;PPN"),
        ("RES2578_7_delta_kappa", "delta_kappa", "Dln(kappa_MTS) or G_ref/kappa mismatch in local branch", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "dimensionless", "Newton;PPN;clock;orbital"),
        ("RES2578_8_delta_ellJ", "delta_ellJ", "Dln(ell_J) or source-current scale mismatch", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "dimensionless", "Newton;WEP;PPN;orbital"),
        ("RES2578_9_total", "Delta_PiM_H_abs", "absolute no-cancellation envelope for PiM/Hamiltonian/coupling transfer residuals", "MISSING_COMPONENT_INPUTS", "dimensionless", "Newton;local_GR;PPN;R10;R11"),
    ]
    return [
        stamp(
            {
                "residual_id": residual_id,
                "residual": residual,
                "definition": definition,
                "status": status,
                "units": units,
                "arenas": arenas,
                "numeric_value": "MISSING_NUMERIC_VALUE",
                "source_path": "MISSING_SOURCE_PATH",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for residual_id, residual, definition, status, units, arenas in rows
    ]


def implication_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "implication_id": "IMP2578_0_identity_zero",
            "premise_package": "Delta_symp=Delta_constraint=Delta_boundary=Delta_extra=epsilon_PiM_lock=epsilon_source_frame=delta_kappa=delta_ellJ=0",
            "implication": "epsilon_PiM_Hamiltonian=0 and Pi_M J_H is the dressed Hamiltonian source mass",
            "current_status": "EXACT_CONDITIONAL_NOT_CURRENT_CLAIM",
            "missing_piece": "MTS EH descent and coupling baseline are unsigned",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2578_1_source_selector",
            "premise_package": "PiM/Hamiltonian identity plus same W_source topological representative and zero B_zero flux",
            "implication": "R_eq=0, I_commutator=0, and epsilon_M source mismatch can close",
            "current_status": "BLOCKED_CONDITIONAL",
            "missing_piece": "boundary/reference zero and projector-stress silence",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2578_2_Newton",
            "premise_package": "epsilon_M=0 plus EH fixed-point v coefficients and fixed coupling baseline",
            "implication": "Delta_Newton_v_coupled=0",
            "current_status": "BLOCKED_CONDITIONAL",
            "missing_piece": "parent-signed transfer premises",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2578_3_local_GR",
            "premise_package": "MTS EH descent, PiM/source glue, boundary zero, extra double zeros, coupling baseline, radial gauge/readout ownership, and PPN vector silence",
            "implication": "local GR recovery becomes derivable rather than imported",
            "current_status": "NOT_CLAIMED",
            "missing_piece": "EH descent/PiM lock/coupling package is next",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2578_0_internal_progress", "PiM/Hamiltonian/coupling identity is reduced to covariant phase-space transfer residuals", "PASS_INTERNAL_PROGRESS", "the identity now has named proof premises and failure terms", True),
        ("GATE2578_1_PiM_identity", "Pi_M J_H is proved to be the Hamiltonian mass map", "BLOCKED", "core identity is still conditional", False),
        ("GATE2578_2_coupling_baseline", "kappa_MTS and ell_J are proved fixed in the same branch", "BLOCKED", "coupling baseline package is not parent-signed", False),
        ("GATE2578_3_MTS_transfer", "MTS inherits EH Hamiltonian charge", "BLOCKED", "EH descent, extra silence, boundary no-flux, PiM lock, and source frame remain open", False),
        ("GATE2578_4_Newton", "Newton source closure is derived", "BLOCKED", "PiM/Hamiltonian identity and epsilon_M closure remain unproved", False),
        ("GATE2578_5_local_GR", "local GR recovery is derived", "BLOCKED", "full EH descent, gauge/readout, source, boundary, and PPN vector gates remain open", False),
        ("GATE2578_6_no_shortcuts", "EH reference charge, fitted G, or projector choice can be imported as MTS proof", "PASS_GUARDRAIL", "GR import and fitted normalization remain explicitly forbidden", True),
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
            "decision_id": "DEC2578_0_gain",
            "decision": "PIM_HAMILTONIAN_IDENTITY_HAS_TRANSFER_LEDGER",
            "reason": "covariant phase-space charge gives a clean conditional route and exposes Delta_symp, Delta_boundary, Delta_extra, Delta_kappa, and Delta_ellJ",
            "effect": "PiM is no longer a vague source label; it must be the Hamiltonian map or a residual",
        },
        {
            "decision_id": "DEC2578_1_limit",
            "decision": "CURRENT_CORPUS_DOES_NOT_PROVE_IDENTITY",
            "reason": "explicit parent symplectic potential, PiM lock, fixed reference, extra double zeros, source-frame lock, and coupling baseline are unsigned",
            "effect": "no Newton/local-GR claim",
        },
        {
            "decision_id": "DEC2578_2_fallback",
            "decision": "SOURCE_BACKED_RESIDUAL_FILL_REMAINS_REQUIRED_IF_PROOF_FAILS",
            "reason": "the residual ledger is source-ready but has no numeric values or source paths",
            "effect": "future empirical local tests can carry finite failures honestly",
        },
        {
            "decision_id": "DEC2578_3_next",
            "decision": "EH_FIXED_POINT_DESCENT_COUPLING_PIM_LOCK_SELECTED_NEXT",
            "reason": "the identity can only close if MTS signs the EH fixed point, PiM lock, extra-sector double zeros, boundary no-flux, and fixed coupling baseline",
            "effect": "2579 should attack that package directly",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2578_0_selected",
            "selection_status": "selected",
            "target_file": "2579-Y5-R2FR-EH-fixed-point-descent-coupling-PiM-lock-or-double-zero-residuals.md",
            "target_script": "scripts/Y5_R2FR_EH_fixed_point_descent_coupling_PiM_lock_or_double_zero_residuals_2579.py",
            "task": "prove or reject the parent EH fixed-point descent package: EH core, extra-sector double zeros, PiM(Phi0)=Pi_EH, fixed kappa_MTS, fixed ell_J/source frame, zero boundary flux, and readout/gauge ownership; otherwise emit finite nonclaim residuals",
            "acceptance_target": "MTS signs the local EH/PiM/coupling descent package or every missing premise is carried as an explicit source-ready residual",
            "guardrails": "no GitHub; no formalization-workbench edits; no GR import as proof; no fitted G/source normalization; no local-GR claim",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "phase_space_audit": OUTPUTS["phase_space_audit"],
        "transfer_gate": OUTPUTS["transfer_gate"],
        "coupling_gate": OUTPUTS["coupling_gate"],
        "residual_ledger": OUTPUTS["residual_ledger"],
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
                    "copy_id": f"COPY2578_{key}",
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

    add("VAL2578_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2578_01_identity_verdict_blocked",
        any(row["audit_id"] == "CPS2578_5_current_verdict" and row["status"] == "PIM_HAMILTONIAN_COUPLING_IDENTITY_NOT_DERIVED_CURRENT_CORPUS" for row in data["phase_space_audit"]),
        "PiM/Hamiltonian/coupling identity remains blocked",
    )
    add(
        "VAL2578_02_transfer_ledger_has_couplings",
        any(row["audit_id"] == "CPS2578_3_EH_transfer" and "Delta_kappa" in row["mathematical_form"] and "Delta_ellJ" in row["mathematical_form"] for row in data["phase_space_audit"]),
        "EH transfer ledger includes coupling residuals",
    )
    add(
        "VAL2578_03_transfer_gate_blocked",
        any(row["gate_id"] == "TR2578_6_transfer_verdict" and row["current_status"] == "MTS_TRANSFER_PREMISES_NOT_PARENT_SIGNED" for row in data["transfer_gate"]),
        "MTS transfer premises remain unsigned",
    )
    add(
        "VAL2578_04_coupling_verdict_blocked",
        any(row["coupling_id"] == "COG2578_4_verdict" and row["current_status"] == "COUPLING_BASELINE_IDENTITY_NOT_DERIVED" for row in data["coupling_gate"]),
        "coupling baseline verdict remains blocked",
    )
    required_residuals = {"epsilon_PiM_Hamiltonian", "Delta_symp", "Delta_boundary", "Delta_extra", "epsilon_PiM_lock", "delta_kappa", "delta_ellJ"}
    actual_residuals = {row["residual"] for row in data["residual_ledger"]}
    add(
        "VAL2578_05_required_residual_rows",
        required_residuals.issubset(actual_residuals) and all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["residual_ledger"]),
        "PiM/Hamiltonian/coupling residual rows exist and remain nonclaim",
    )
    add(
        "VAL2578_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows PiM, Newton or local-GR claim",
    )
    add(
        "VAL2578_07_next_target_written",
        any(row["route_id"] == "NEXT2578_0_selected" for row in data["next"]),
        "2579 EH fixed-point descent/coupling/PiM lock target selected",
    )
    add(
        "VAL2578_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2578*", "*P8_Y5_PIM_HAMILTONIAN_COUPLING_2578*", "*JR2578*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2578_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2578 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2578_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2578_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2578_OVERALL",
        overall,
        "2578 reduces PiM/Hamiltonian/coupling identity to a covariant phase-space transfer ledger, keeps claims blocked, and selects EH fixed-point descent with coupling/PiM lock next",
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
        "# 2578 Y5 R2FR PiM Hamiltonian Coupling Identity Or Source-Backed Residual Fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. `Pi_M J_H` can be the measured dressed source mass only if it is the covariant phase-space Hamiltonian mass map in the same fixed `kappa_MTS`/`ell_J` frame. Current MTS has a coherent contract but not a parent-signed proof.",
        "",
        "**Main result:** the identity reduces to a transfer ledger: `Q_MTS_tau = Q_EH_tau + Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_kappa + Delta_ellJ`. If the MTS local branch parent-signs EH descent, PiM lock, universal source frame, fixed coupling, zero boundary/reference flux, and extra-sector double zeros, then `epsilon_PiM_Hamiltonian=0`. Current sources do not prove that package, so the identity remains blocked and residualized.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Covariant Phase-Space Identity Audit",
        markdown_table(data["phase_space_audit"], ["audit_id", "identity", "mathematical_form", "status", "would_close", "current_blocker", "coupling_clause", "valid_for_claim"]),
        "",
        "## MTS Transfer Premise Gate",
        markdown_table(data["transfer_gate"], ["gate_id", "premise", "required_form", "current_status", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Coupling Baseline Gate",
        markdown_table(data["coupling_gate"], ["coupling_id", "quantity", "required_identity", "current_status", "failure_mode", "residual_symbol", "valid_for_claim"]),
        "",
        "## Residual Input Ledger",
        markdown_table(data["residual_ledger"], ["residual_id", "residual", "definition", "status", "units", "arenas", "numeric_value", "source_path", "valid_for_claim", "claim_allowed"]),
        "",
        "## Newton / Local-GR Implications",
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

    data = {
        "sources": source_register_rows(),
        "phase_space_audit": phase_space_audit_rows(),
        "transfer_gate": transfer_gate_rows(),
        "coupling_gate": coupling_gate_rows(),
        "residual_ledger": residual_ledger_rows(),
        "implications": implication_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["phase_space_audit"], data["phase_space_audit"])
    write_csv(OUTPUTS["transfer_gate"], data["transfer_gate"])
    write_csv(OUTPUTS["coupling_gate"], data["coupling_gate"])
    write_csv(OUTPUTS["residual_ledger"], data["residual_ledger"])
    write_csv(OUTPUTS["implications"], data["implications"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2578_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
