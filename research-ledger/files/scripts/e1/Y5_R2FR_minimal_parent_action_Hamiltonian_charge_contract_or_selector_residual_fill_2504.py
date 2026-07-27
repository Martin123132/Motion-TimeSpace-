from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_MINIMAL_PARENT_ACTION_HAMILTONIAN_CHARGE_CONTRACT_2504"
CHECKPOINT_ID = "2504"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2504-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2504_SOURCE_REGISTER.csv",
    "action_contract": OUT / "P8_Y5_NO_SHADOW_2504_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT.csv",
    "noether_chain": OUT / "P8_Y5_NO_SHADOW_2504_NOETHER_HAMILTONIAN_CHARGE_CHAIN.csv",
    "v_bridge": OUT / "P8_Y5_NO_SHADOW_2504_V_LAPSE_READOUT_BRIDGE.csv",
    "residual_rows": OUT / "P8_Y5_NO_SHADOW_2504_PARENT_ACTION_RESIDUAL_ROWS.csv",
    "live_binding": OUT / "P8_Y5_NO_SHADOW_2504_LIVE_DESCENT_BINDING_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2504_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2504_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2504_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2504_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2504_VALIDATION.csv",
}

COPY_TARGETS = {
    "action_contract": LOCAL_BOUNDS / "Minimal_parent_action_charge_contract_2504_NONCLAIM.csv",
    "noether_chain": LOCAL_BOUNDS / "Noether_Hamiltonian_charge_chain_2504_NONCLAIM.csv",
    "v_bridge": BETA_DOCS / "V_lapse_readout_bridge_2504_NONCLAIM.csv",
    "residual_rows": QUEUE / "JR2504_PARENT_ACTION_RESIDUAL_ROWS_NONCLAIM.csv",
    "next_target": QUEUE / "JR2504_EH_TO_V_COEFFICIENT_EXTRACTION_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2504_00_2503_handoff",
        "source_path": ROOT / "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
        "needles": ["NEXT2503_0_selected", "WHS2503_6_current_verdict", "VAL2503_OVERALL"],
        "role": "live handoff into minimal parent-action Hamiltonian charge contract",
    },
    {
        "source_id": "SRC2504_01_2184_contract",
        "source_path": ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
        "needles": ["MAS2184_1_action_skeleton", "NHC2184_4_PiM_identification", "VAL2184_OVERALL"],
        "role": "prior minimal parent-action/Hamiltonian charge contract",
    },
    {
        "source_id": "SRC2504_02_2185_coefficients",
        "source_path": ROOT / "2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
        "needles": ["WAE2185_2_Kv", "PPE2185_2_beta", "VAL2185_OVERALL"],
        "role": "next coefficient extraction target and conditional EH win",
    },
    {
        "source_id": "SRC2504_03_2186_descent",
        "source_path": ROOT / "2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md",
        "needles": ["RGC2186_5_resolution", "DEG2186_7_verdict", "VAL2186_OVERALL"],
        "role": "later EH descent/readout gate showing 2PN warning is gauge debt, not immediate death",
    },
    {
        "source_id": "SRC2504_04_parent_action_attempt",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
        "needles": ["DAT537_0_variation", "DAT537_4_PiM_Hilbert_identification", "DAT537_5_local_readout"],
        "role": "formal Noether chain and PiM/Hilbert missing identity",
    },
    {
        "source_id": "SRC2504_05_hwt_clause_map",
        "source_path": OUT / "P8_Y5_PARENT_ACTION_TO_HWT536_CLAUSE_MAP.csv",
        "needles": ["HWT536_0_parent_worldtube_fixed", "HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_8_weak_field_readout_after_charge_glue"],
        "role": "parent-action outputs required for Hilbert worldtube source theorem",
    },
    {
        "source_id": "SRC2504_06_local_gr_blocks",
        "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        "needles": ["A511_0_EH_core", "A511_2_universal_matter", "A511_6_metric_readout"],
        "role": "minimal local-GR action blocks and caveats",
    },
    {
        "source_id": "SRC2504_07_symbol_map",
        "source_path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "needles": ["g_obs / g_readout", "Pi_M", "M_eff / M_source / Q_M"],
        "role": "symbol placement map for observed metric, mass projector and source charge",
    },
    {
        "source_id": "SRC2504_08_hamiltonian_source",
        "source_path": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_2_observed_worldtube_source", "HSM541_7_PPN_followthrough"],
        "role": "Hamiltonian source measure contract and remaining debts",
    },
    {
        "source_id": "SRC2504_09_2503_validation",
        "source_path": OUT / "P8_Y5_BRR545_2503_VALIDATION.csv",
        "needles": ["VAL2503_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
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
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def action_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "PAC2504_0_field_content",
            "object": "minimal local fields",
            "statement": "Phi=(e_obs, omega/Gamma, psi_m, X^A, kappa_eff, A_3, B_ref/top, readout constraint).",
            "status": "MINIMAL_FIELD_LIST_CANDIDATE",
            "what_it_buys": "e_obs owns clocks/orbits/sources; X^A carries motion/time/domain/memory/range residual sectors",
            "missing": "parent derivation of why this is the actual MTS field list",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_1_action_skeleton",
            "object": "parent action skeleton",
            "statement": "S_min=S_EH[e_obs,kappa_eff]+S_matter[psi_m,e_obs]+S_X[X,e_obs]+S_kappa_top[kappa_eff,A_3]+S_boundary[e_obs,B_ref]+S_readout_constraint.",
            "status": "MINIMAL_PARENT_ACTION_SKELETON_WRITTEN",
            "what_it_buys": "turns the source-selector route into an action-language contract",
            "missing": "not yet a derived MTS parent Lagrangian",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_2_EH_core",
            "object": "local EH fixed point",
            "statement": "Local branch must reduce to EH spin-2 operator plus constant kappa and locally negligible/background-subtracted Lambda.",
            "status": "CANDIDATE_FIXED_POINT_NOT_PARENT_SIGNED",
            "what_it_buys": "would let MTS inherit the correct Newton/PPN operator rather than fit it",
            "missing": "extra-sector double zeros and fixed-point descent proof",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_3_universal_matter",
            "object": "same observed source frame",
            "statement": "S_matter depends on e_obs and psi_m only at leading local order; J_H[tau]=delta S_matter/delta e_obs contracted with tau.",
            "status": "CONDITIONAL_HILBERT_SOURCE_OWNER",
            "what_it_buys": "single Hilbert source current for W_source, v source, clocks and orbits",
            "missing": "no species/source-only X^A coupling theorem",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_4_Hamiltonian_PiM",
            "object": "Hamiltonian mass projector",
            "statement": "Pi_M J_H is identified with the covariant phase-space Hamiltonian mass-charge map ell_H[J_H;tau,S] omega_M^H.",
            "status": "CORE_ADOPTION_NEEDED_NOT_PROVED",
            "what_it_buys": "prevents Pi_M from conserving a non-observed mass object",
            "missing": "PiM/Hilbert identity and projector-stress silence",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_5_worldtube_selector",
            "object": "source support selector",
            "statement": "W_source=supp(J_H[e_obs,tau]); linked surfaces must enclose the same W_source before exterior readout.",
            "status": "CONDITIONAL_SELECTOR_DERIVED_IF_JH_OWNED",
            "what_it_buys": "domain/source selector is no longer picked after fitting orbits",
            "missing": "fixed tau and parent source-support topology",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_6_boundary_reference",
            "object": "fixed reference and zero compact flux",
            "statement": "S_boundary must make H_tau integrable with one reference and zero compact exterior flux from B_ref/top/symplectic improvements.",
            "status": "BOUNDARY_CONTRACT_WRITTEN_NOT_CERTIFIED",
            "what_it_buys": "protects source mass from boundary bookkeeping shifts",
            "missing": "actual boundary variation and B_zero_flux=0 certificate",
            "valid_for_claim": False,
        },
        {
            "contract_id": "PAC2504_7_current_verdict",
            "object": "current parent-action status",
            "statement": "The contract is coherent, but current MTS has not parent-signed the action, PiM identity, X-sector double zeros, or boundary zero.",
            "status": "COHERENT_CONTRACT_CURRENT_CLAIM_FAILS",
            "what_it_buys": "sets the exact next derivation target",
            "missing": "EH-to-v coefficient extraction is conditional until descent clauses close",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def noether_chain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "chain_id": "NHC2504_0_variation",
            "object": "covariant variation",
            "equation": "delta L = E_A delta Phi^A + dTheta(Phi,delta Phi).",
            "status": "FORMAL_EXACT_IF_ACTION_SUPPLIED",
            "role": "defines equations and symplectic potential once S_min is real",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_1_Noether_current",
            "object": "diffeomorphism Noether current",
            "equation": "J_tau = Theta(Phi,L_tau Phi) - i_tau L.",
            "status": "FORMAL_EXACT_IF_TAU_FIXED",
            "role": "source charge depends on a parent-owned observed time generator",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_2_charge_decomposition",
            "object": "surface charge plus constraints",
            "equation": "On shell in a source-free annulus, J_tau=dQ_tau+C_tau and Delta H_tau[S2,S1]=int_A C_tau + boundary_flux.",
            "status": "EXACT_CONDITIONAL_HAMILTONIAN_CHAIN",
            "role": "radial source closure follows only when constraints and boundary flux vanish",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_3_source_measure",
            "object": "dressed source mass",
            "equation": "M_source[W]=H_tau[S]-H_tau[reference], with W_source=supp(J_H[e_obs,tau]).",
            "status": "CONDITIONAL_SOURCE_MEASURE_DEFINITION",
            "role": "bare rest mass is not enough; measured source is dressed Hamiltonian charge",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_4_PiM_identification",
            "object": "PiM/Hilbert identity",
            "equation": "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S]-H_tau[reference].",
            "status": "CORE_MISSING_IDENTITY_NOT_DERIVED",
            "role": "main equality needed to make Pi_M the observed source mass",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_5_topological_PD",
            "object": "topological representative",
            "equation": "J_M_top=M_source[W] omega_W, d omega_W=0, int_link omega_W=1 for the same W_source.",
            "status": "EXACT_CONDITIONAL_PD_MAP",
            "role": "topological current becomes same measured source object only after NHC2504_4",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_6_R_eq_zero",
            "object": "R_eq zero theorem",
            "equation": "If Pi_M J_H and J_M_top represent the same compact Hilbert source class, Pi_M J_H-J_M_top=dB_zero and R_eq=0.",
            "status": "EXACT_CONDITIONAL_R_EQ_ZERO",
            "role": "R_eq zero is downstream of PiM/Hamiltonian identity, not an independent axiom",
            "valid_for_claim": False,
        },
        {
            "chain_id": "NHC2504_7_boundary_zero",
            "object": "B_zero compact flux",
            "equation": "int_boundary dB_zero=0 with one fixed reference and no symplectic/projector stress shift.",
            "status": "BOUNDARY_ZERO_NOT_DERIVED",
            "role": "prevents exact improvement from shifting measured GM",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def v_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bridge_id": "VBR2504_0_lapse_readout",
            "object": "v as local lapse/coframe readout",
            "statement": "On compact local branch, v:=log(N_obs^2/c^2) with g_obs(tau,tau)=-N_obs^2, so g_tt=-exp(v)c^2 in adapted static chart.",
            "status": "LOCAL_READOUT_DEFINITION_CANDIDATE",
            "implication": "v is not a fitted force field if e_obs/tau are parent-owned",
            "missing": "parent-owned tau, radial gauge and readout map",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "VBR2504_1_parent_source",
            "object": "v source rho_H",
            "statement": "The rho in the v action must be the same Hilbert/Hamiltonian source measure M_source[W].",
            "status": "SOURCE_MEASURE_GLUE_OPEN",
            "implication": "right coefficient algebra can still have wrong mass if source glue fails",
            "missing": "PiM/Hamiltonian identity and W_source selector",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "VBR2504_2_EH_to_v_coefficients",
            "object": "EH fixed point coefficient target",
            "statement": "Expand S_EH+S_GHY+S_matter on the constrained static branch and compare with L_v=-K_v(grad v)^2-C_v rho c^2 v.",
            "status": "NEXT_COMPUTATION_LIVEPORTED_FROM_2185",
            "implication": "first non-handwave route to K_v=c^4/(32*piG), C_v=1/2 and delta_v_source_norm=0",
            "missing": "MTS fixed-point descent, not EH import",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "VBR2504_3_beta_readout",
            "object": "beta from lapse logarithm",
            "statement": "If EH fixed point gives v=-2U/c^2+O(U^3/c^6), then exp(v)=1-2U/c^2+2U^2/c^4+... and beta=1.",
            "status": "CONDITIONAL_BETA_ZERO_ROUTE",
            "implication": "kappa_v=0 becomes an EH fixed-point/readout extraction target",
            "missing": "MTS descent and radial/PPN gauge ownership",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "VBR2504_4_2PN_warning",
            "object": "reciprocal spatial 2PN warning",
            "statement": "2185/2186 show the +1/2 x^2 spatial warning is a gauge/readout-owner debt, not automatic death.",
            "status": "GAUGE_DEBT_NOT_FAILURE",
            "implication": "continue derivation; do not declare local branch dead from mixed-coordinate 2PN comparison",
            "missing": "parent radial/angular gauge map",
            "valid_for_claim": False,
        },
        {
            "bridge_id": "VBR2504_5_status",
            "object": "v bridge status",
            "statement": "The lapse-readout route is coherent, but EH-to-v extraction and MTS descent are not claimable in 2504.",
            "status": "BRIDGE_OPEN_NOT_CLAIMED",
            "implication": "2505 should compute/live-port EH-to-v coefficient extraction with GR-import guard",
            "missing": "parent descent and coefficient extraction in current live branch",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "PAR2504_0_parent_action",
            "symbol": "epsilon_parent_action",
            "definition": "failure of current corpus to supply and vary the explicit MTS parent action",
            "status": "MISSING_SIGNED_PARENT_LAGRANGIAN",
            "units": "dimensionless_or_declared",
            "observable_link": "all_local_arenas",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_1_PiM",
            "symbol": "epsilon_PiM_Hamiltonian",
            "definition": "failure of Pi_M J_H to equal the Hamiltonian mass-charge form",
            "status": "MISSING_PIM_HAMILTONIAN_IDENTITY",
            "units": "dimensionless_or_GM_flux",
            "observable_link": "Newton;PPN;R10;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_2_tau",
            "symbol": "epsilon_tau_fixed",
            "definition": "unfixed observed time generator contribution to H_tau",
            "status": "MISSING_TAU_SELECTOR",
            "units": "dimensionless_or_charge_fraction",
            "observable_link": "clocks;Newton;orbital",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_3_boundary",
            "symbol": "epsilon_boundary_flux",
            "definition": "compact local boundary/reference/exact/symplectic flux contribution to source mass",
            "status": "MISSING_BOUNDARY_ZERO_PROOF",
            "units": "dimensionless_or_GM_flux",
            "observable_link": "Newton;local_GR;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_4_extra",
            "symbol": "epsilon_extra_mass_channel",
            "definition": "non-EH/memory/domain/range/frame/projector extra mass-channel residual",
            "status": "MISSING_EXTRA_SECTOR_DOUBLE_ZERO",
            "units": "dimensionless_or_GM_flux",
            "observable_link": "Newton;WEP;PPN;clock;R10",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_5_v_coeff",
            "symbol": "delta_v_source_norm",
            "definition": "C_v c^4/(16*piG_ref K_v)-1 from local v/lapse action extraction",
            "status": "MISSING_EH_TO_V_COEFFICIENT_EXTRACTION_IN_LIVE_BRANCH",
            "units": "dimensionless",
            "observable_link": "Newton;PPN;orbital",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_6_kappa",
            "symbol": "kappa_v",
            "definition": "quadratic lapse/readout drift v=-2U/c^2+kappa_v U^2/c^4",
            "status": "MISSING_KAPPA_V_ZERO_OR_VALUE_IN_LIVE_BRANCH",
            "units": "dimensionless",
            "observable_link": "PPN_beta;local_GR",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_7_R_eq",
            "symbol": "R_eq_integral",
            "definition": "topological-Hilbert equality residual after Hamiltonian PiM adoption",
            "status": "MISSING_R_EQ_ZERO_OR_VALUE",
            "units": "dimensionless_after_M_H_ref",
            "observable_link": "Newton;R10;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "PAR2504_8_total",
            "symbol": "Delta_Newton_local_abs",
            "definition": "absolute envelope combining parent action, PiM, boundary, delta_v_source_norm, epsilon_M, kappa_v and extra-sector residuals",
            "status": "MISSING_COMPONENT_INPUTS",
            "units": "dimensionless",
            "observable_link": "Newton;local_GR;PPN",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def live_binding_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "binding_id": "LDB2504_0_from_2503",
            "object": "epsilon_M selector leg",
            "current_status": "2503 made same-object worldtube-Hilbert selector theorem live but nonclaim",
            "contract_effect": "2504 supplies the minimal parent-action/Hamiltonian charge chain needed to own the selector",
            "remaining_blocker": "PiM/Hamiltonian identity, tau, boundary zero and extra-channel silence unsigned",
            "valid_for_claim": False,
        },
        {
            "binding_id": "LDB2504_1_v_coefficients",
            "object": "delta_v_source_norm and kappa_v",
            "current_status": "2185 shows coefficients come out right inside EH fixed point",
            "contract_effect": "2504 frames this as derived inheritance only if MTS descends to EH locally",
            "remaining_blocker": "EH descent and coefficient extraction must be live-ported and guarded against GR import",
            "valid_for_claim": False,
        },
        {
            "binding_id": "LDB2504_2_2PN",
            "object": "reciprocal spatial 2PN warning",
            "current_status": "2186 demotes mixed isotropic/reciprocal mismatch to radial-gauge owner debt",
            "contract_effect": "2504 keeps gauge/readout ownership in residual envelope",
            "remaining_blocker": "parent radial/angular gauge map and PPN coordinate ownership",
            "valid_for_claim": False,
        },
        {
            "binding_id": "LDB2504_3_local_GR",
            "object": "local GR/Newton branch",
            "current_status": "not claimable",
            "contract_effect": "least-circular path now runs: parent action -> EH fixed point -> v coefficients -> PiM/source/boundary lock -> PPN gauge",
            "remaining_blocker": "all major clauses remain nonclaim until signed in one parent package",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2504_0_contract",
            "claim": "minimal parent-action/Hamiltonian charge contract is a valid internal construction target",
            "status": "PASS_INTERNAL_NONCLAIM",
            "reason": "action skeleton, Noether chain and v-lapse bridge are coherent contracts",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2504_1_parent_action",
            "claim": "MTS parent action is supplied and varied",
            "status": "BLOCKED",
            "reason": "2504 writes a skeleton/contract, not a completed Lagrangian derivation",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2504_2_PiM",
            "claim": "Pi_M is proved to be the Hamiltonian mass map",
            "status": "BLOCKED",
            "reason": "core PiM/Hilbert identity remains unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2504_3_boundary",
            "claim": "B_zero/reference boundary flux is zero",
            "status": "BLOCKED",
            "reason": "fixed reference and compact boundary cancellation are not computed",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2504_4_v_coefficients",
            "claim": "K_v/C_v and kappa_v=0 are live-branch MTS derivations",
            "status": "BLOCKED",
            "reason": "EH-to-v coefficient extraction is next and must be guarded against GR import",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2504_5_Newton_GR",
            "claim": "Newton/local-GR reduction can be claimed",
            "status": "BLOCKED",
            "reason": "source, coefficient, PPN, boundary and descent gates remain open",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2504_6_no_cheats",
            "claim": "skeleton alone, EH import, fitted G, or gamma-only pass can promote local GR",
            "status": "PASS_GUARDRAIL",
            "reason": "2504 explicitly refuses those promotions",
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2504_0_gain",
            "decision": "MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_LIVE",
            "reason": "local branch now has a coherent action skeleton, Noether/Hamiltonian chain, source selector and v-as-lapse bridge",
            "effect": "we know exactly what a future parent action must own",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2504_1_leap",
            "decision": "V_CAN_BE_LOCAL_LAPSE_READOUT_NOT_SEPARATE_FORCE_FIELD",
            "reason": "v=log(N_obs^2/c^2) can make K_v/C_v and beta inherit from EH fixed point rather than from an inserted motion field",
            "effect": "2505 should live-port the EH-to-v coefficient extraction",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2504_2_limit",
            "decision": "NOT_A_CLAIM_UNTIL_DESCENT_AND_EXTRACTION",
            "reason": "parent action, PiM identity, boundary zero, extra-sector double zeros and live coefficient extraction are not signed",
            "effect": "keep residual rows and GR-import guard active",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2504_3_next",
            "decision": "EH_FIXED_POINT_TO_V_COEFFICIENT_EXTRACTION_NEXT",
            "reason": "2185 shows the coefficient side works inside EH; the live branch must decide inheritance versus import",
            "effect": "2505 should compute/live-port K_v, C_v, delta_v_source_norm and kappa_v with claim flags false",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2504_0_selected",
            "selection_status": "selected",
            "target_file": "2505-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md",
            "target_script": "scripts/Y5_R2FR_EH_fixed_point_to_v_action_coefficient_extraction_or_GR_import_demotion_2505.py",
            "task": "compute/live-port the constrained local EH fixed-point expansion for v=log lapse, extract K_v/C_v and kappa_v, and decide whether the result is derived inheritance, GR import, or finite residual",
            "acceptance_target": "K_v=c^4/(32*piG_ref), C_v=1/2, delta_v_source_norm=0 and kappa_v=0 are derived inside EH fixed point; MTS owns them only if parent fixed-point/readout/source/boundary descent is signed",
            "guardrails": "do not fit G, assume beta=1 from gamma, replace MTS by GR without a fixed-point descent clause, claim local-GR from a skeleton, or use GitHub action",
            "valid_for_claim": False,
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "action_contract": OUTPUTS["action_contract"],
        "noether_chain": OUTPUTS["noether_chain"],
        "v_bridge": OUTPUTS["v_bridge"],
        "residual_rows": OUTPUTS["residual_rows"],
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
                    "copy_id": f"COPY2504_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2504_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2504_01_action_contract",
        any(row["contract_id"] == "PAC2504_7_current_verdict" and row["status"] == "COHERENT_CONTRACT_CURRENT_CLAIM_FAILS" for row in data["action_contract"]),
        "minimal action contract is written but not promoted",
    )
    add(
        "VAL2504_02_noether_chain",
        any(row["chain_id"] == "NHC2504_4_PiM_identification" and row["status"] == "CORE_MISSING_IDENTITY_NOT_DERIVED" for row in data["noether_chain"]),
        "Noether/Hamiltonian chain carries PiM identity blocker",
    )
    add(
        "VAL2504_03_v_bridge",
        any(row["bridge_id"] == "VBR2504_5_status" and row["status"] == "BRIDGE_OPEN_NOT_CLAIMED" for row in data["v_bridge"]),
        "v-lapse bridge is coherent but not claimed",
    )
    add(
        "VAL2504_04_residual_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["residuals"]),
        "all parent-action residual rows remain nonclaim and not score-ready",
    )
    add(
        "VAL2504_05_live_binding",
        any(row["binding_id"] == "LDB2504_3_local_GR" and row["current_status"] == "not claimable" for row in data["live_binding"]),
        "live local-GR binding remains nonclaim",
    )
    add(
        "VAL2504_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "claim gates deny parent-action/local-GR shortcut promotion",
    )
    add(
        "VAL2504_07_next_target",
        any(row["route_id"] == "NEXT2504_0_selected" for row in data["next"]),
        "2505 EH-to-v coefficient extraction target selected",
    )
    add(
        "VAL2504_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2504*", "*P8_Y5_NO_SHADOW_2504*", "*JR2504*"):
            formalization_artifacts.extend(path for path in FORMALIZATION.rglob(pattern) if path.is_file())
    add("VAL2504_09_no_formalization_artifacts", not formalization_artifacts, "no 2504 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2504_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2504_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2504_OVERALL",
        overall,
        "2504 live-ports the minimal parent-action/Hamiltonian charge contract, keeps current MTS nonclaim, and selects EH-to-v coefficient extraction next",
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
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2504 Y5 R2FR Minimal Parent-Action Hamiltonian Charge Contract Or Selector Residual Fill",
        "",
        "**Status:** private nonclaim checkpoint. `2504` live-ports the minimal parent-action/Hamiltonian charge contract into the current branch, but it does not claim a derived MTS parent action, Newton limit, PPN pass, or local GR.",
        "",
        "**Main result:** the least-circular route is now explicit: `MTS parent action -> local EH fixed point -> v as lapse readout -> EH/Hamiltonian charge -> K_v/C_v and beta extraction -> PiM/source/boundary lock`. This is coherent, but still a contract. The live blockers are parent action origin, PiM/Hamiltonian identity, boundary flux zero, extra-sector double zeros, and guarded EH-to-v coefficient extraction.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Minimal Parent-Action Charge Contract",
        markdown_table(data["action_contract"], ["contract_id", "object", "statement", "status", "what_it_buys", "missing", "valid_for_claim"]),
        "",
        "## Noether-Hamiltonian Charge Chain",
        markdown_table(data["noether_chain"], ["chain_id", "object", "equation", "status", "role", "valid_for_claim"]),
        "",
        "## V Lapse Readout Bridge",
        markdown_table(data["v_bridge"], ["bridge_id", "object", "statement", "status", "implication", "missing", "valid_for_claim"]),
        "",
        "## Parent-Action Residual Rows",
        markdown_table(data["residuals"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Live Descent Binding Status",
        markdown_table(data["live_binding"], ["binding_id", "object", "current_status", "contract_effect", "remaining_blocker", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "status", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "action_contract": action_contract_rows(),
        "noether_chain": noether_chain_rows(),
        "v_bridge": v_bridge_rows(),
        "residuals": residual_rows(),
        "live_binding": live_binding_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["action_contract"], data["action_contract"])
    write_csv(OUTPUTS["noether_chain"], data["noether_chain"])
    write_csv(OUTPUTS["v_bridge"], data["v_bridge"])
    write_csv(OUTPUTS["residual_rows"], data["residuals"])
    write_csv(OUTPUTS["live_binding"], data["live_binding"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
