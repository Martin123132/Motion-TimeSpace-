from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2628-Y5-R2FR-constraint-auxiliary-memory-source-elimination-or-residual-interface.md"

PREFIX = "P8_Y5_CONSTRAINT_ELIMINATION_2628"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "elimination_theorem": RESIDUALS / f"{PREFIX}_CONSTRAINT_ELIMINATION_THEOREM_GATE.csv",
    "parent_package": RESIDUALS / f"{PREFIX}_PARENT_PACKAGE_AUDIT.csv",
    "dr_interface": RESIDUALS / f"{PREFIX}_DR_SR_INTERFACE_AUDIT.csv",
    "residual_interface": RESIDUALS / f"{PREFIX}_RLOCAL_RESIDUAL_INTERFACE.csv",
    "route_verdict": RESIDUALS / f"{PREFIX}_ROUTE_VERDICT.csv",
    "countermodels": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2628_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2628_00_2627_handoff",
        "role": "2627 selects constraint/auxiliary memory source elimination",
        "path": ROOT / "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md",
        "needles": ["DEC2627_3_best_next", "CONSTRAINT_AUXILIARY_MEMORY_SOURCE_ELIMINATION_NEXT", "JX_ZERO_NOT_PROVED"],
    },
    {
        "source_id": "SRC2628_01_2627_validation",
        "role": "2627 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_2627_VALIDATION.csv",
        "needles": ["VAL2627_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2628_02_1857_constraint_route",
        "role": "exact conditional constraint/auxiliary local-GR theorem",
        "path": ROOT / "1857-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md",
        "needles": ["CLG1857_5_local_GR_consequence", "FAIL_CURRENT_CLAIM_PREMISES_UNSIGNED", "DEC1857_2_next"],
    },
    {
        "source_id": "SRC2628_03_1858_parent_package",
        "role": "parent constraint package no-GR-import gate",
        "path": ROOT / "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md",
        "needles": ["CONSTRAINT_PACKAGE_CONDITIONAL_NOT_CLOSED", "NO_GR_IMPORT_ACTIVE_BUT_PARENT_PACKAGE_OPEN", "DEC1858_1_primary_bottleneck"],
    },
    {
        "source_id": "SRC2628_04_1859_phase_volume",
        "role": "direct phase-volume rejected; parent Euler bridge selected",
        "path": ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
        "needles": ["REJECT_DIRECT_PARENT_DERIVATION_CURRENT_CORPUS", "SELECT_PRIMARY", "DEC1859_1_best_derivation_route"],
    },
    {
        "source_id": "SRC2628_05_1860_qloc",
        "role": "Gamma/Khat/q_loc formal mechanism not live parent-signed",
        "path": ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
        "needles": ["QLOC_ZERO_NOT_DERIVED_CURRENT_CORPUS", "epsilon_GK_q_loc", "DEC1860_2_next_route"],
    },
    {
        "source_id": "SRC2628_06_1861_coupling_lock",
        "role": "source-functional evenness/coupling lock not activated",
        "path": ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
        "needles": ["EVENNESS_THEOREM_NOT_ACTIVATED", "JBC1861_5_acceptance", "DEC1861_1_Y5_primary"],
    },
    {
        "source_id": "SRC2628_07_1862_source_chain",
        "role": "Y5 source-normalization chain reintegrated but not closed",
        "path": ROOT / "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
        "needles": ["Y5_SOURCE_OWNER_NOT_PROVED", "Delta_Hsrc", "DEC1862_2_next_target"],
    },
    {
        "source_id": "SRC2628_08_1863_current_chain",
        "role": "single parent current chain not signed; I_X/J_X demoted",
        "path": ROOT / "1863-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md",
        "needles": ["SINGLE_PARENT_CURRENT_CHAIN_NOT_SIGNED", "R_local^MTS", "IX_JX_DEMOTED_TO_FINITE_NONCLAIM_RESIDUAL_VECTOR"],
    },
    {
        "source_id": "SRC2628_09_1864_lgr_contract",
        "role": "local-GR reduction contract and residual-vector prioritizer",
        "path": ROOT / "1864-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md",
        "needles": ["LOCAL_GR_REDUCTION_CONTRACT_READY_NOT_DERIVED", "DR_NORMAL_FORM_AND_SR_DECOMPOSITION_SELECTED_FIRST", "RLOCAL_MUST_ENTER_SR_EXPLICITLY"],
    },
    {
        "source_id": "SRC2628_10_1865_dr_attempt",
        "role": "D_R derivation attempted; selector/Hcore missing",
        "path": ROOT / "1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md",
        "needles": ["DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS", "RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION_NEXT", "GENERIC_EULER_DIFFERENCE_NO_GO_GUARD_ADDED"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def b(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source["path"]),
                "exists": b(exists),
                "needles_present": b(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2628_0_memory_source_gate",
            "input": "2627",
            "result": "J_X map written but J_X=0 not proved; constraint route selected",
            "use_now": "move from scalar source-zero to pre-readout elimination",
            "status": "nonclaim_handoff",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2628_1_constraint_theorem",
            "input": "1857",
            "result": "elimination before phase space/readout removes physical scalar hair as an exact conditional theorem",
            "use_now": "treat as theorem target, not achieved result",
            "status": "exact_conditional_parent_unsigned",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2628_2_no_GR_import_package",
            "input": "1858/1859",
            "result": "direct phase-volume derivation rejected; parent Euler/source-map route selected",
            "use_now": "keep GR import guard active and avoid AB=1/plateau shortcut",
            "status": "origin_motivated_not_derived",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2628_3_current_and_coupling_locks",
            "input": "1860/1861/1862/1863",
            "result": "q_loc, coupling, Y5 source-normalization, and single-current-chain gates remain unsigned",
            "use_now": "carry them into one residual interface",
            "status": "residual_vector_required",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2628_4_local_reduction_contract",
            "input": "1864/1865",
            "result": "D_R/S_R contract ready; generic Euler difference does not derive the needed normal form",
            "use_now": "select reciprocity-selector/Hcore source equation as next missing object",
            "status": "DR_contract_ready_selector_missing",
            "valid_for_claim": "False",
        },
    ]


def elimination_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CET2628_0_setup",
            "claim_piece": "pre-readout elimination setup",
            "statement": "Let parent phase space contain a local residual X/Z and a constraint or auxiliary equation C_X(Phi)=0 before quotient, ordinary matter, and readout are defined.",
            "proof_status": "SETUP_ONLY",
            "missing_for_activation": "MISSING_PARENT_PHASE_SPACE;MISSING_CONSTRAINT_OR_AUXILIARY_EQUATION",
            "claim_effect": "no scalar local-GR claim",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CET2628_1_elimination_chain",
            "claim_piece": "no physical scalar hair",
            "statement": "If C_X removes X before physical phase space and q(Phi)|C_X=qbar(Q_vis), then Dq[v_X]=0 and ordinary matter/readout cannot source the removed direction if they descend through Q_vis.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_activation": "MISSING_Q_MAP_KERNEL;MISSING_MATTER_READOUT_DESCENT;MISSING_PHYSICAL_COMPONENT_LOCK",
            "claim_effect": "would eliminate the local fifth-force scalar route if parent-signed",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CET2628_2_first_class_route",
            "claim_piece": "gauge/quotient elimination",
            "statement": "A differentiable first-class generator G_X with zero/proper boundary charge and closed bracket removes the residual pair from reduced phase space.",
            "proof_status": "CONDITIONAL_ROUTE",
            "missing_for_activation": "MISSING_GENERATOR;MISSING_BOUNDARY_CHARGE;MISSING_BRACKET_CLOSURE;MISSING_DEGREE_COUNT",
            "claim_effect": "held route; clean but algebra-heavy",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CET2628_3_second_class_auxiliary",
            "claim_piece": "algebraic auxiliary elimination",
            "statement": "A local algebraic auxiliary pair can be solved before readout if the solve has no nonlocal tail, stress hair, boundary source, or readout re-entry.",
            "proof_status": "CONDITIONAL_ROUTE",
            "missing_for_activation": "MISSING_LOCAL_SOLVE;MISSING_NO_TAIL;MISSING_BOUNDARY_AND_MATTER_DESCENT",
            "claim_effect": "best fallback if first-class proof is too expensive",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "CET2628_4_current_branch_verdict",
            "claim_piece": "constraint/auxiliary memory source elimination",
            "statement": "The theorem shape is valid, but the live MTS branch has not supplied one parent-owned constraint/auxiliary/current package, so X elimination is not claimed.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_ACTIVATED",
            "missing_for_activation": "MISSING_SINGLE_PARENT_CURRENT_CERTIFICATE",
            "claim_effect": "retain residual interface and continue derivation",
            "valid_for_claim": "False",
        },
    ]


def parent_package_rows() -> list[dict[str, Any]]:
    return [
        {
            "package_id": "PPA2628_0_parent_action",
            "needed_object": "one parent action/grammar",
            "required_statement": "L_parent declares fields, quotient, constants, constraints/auxiliaries, matter, boundary, history, source, and readout slots before local limit.",
            "current_status": "MISSING_SINGLE_PARENT_ACTION_GRAMMAR",
            "blocks": "sublemmas may live in different closures without one common parent branch",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_1_constraint_origin",
            "needed_object": "C_X=0 or C_R=0 parent origin",
            "required_statement": "constraint follows from MTS parent motion-load/phase-volume/Euler/Dirac law without inserting AB=1, p=1, or GR vacuum equations.",
            "current_status": "PARENT_ORIGIN_NOT_DERIVED",
            "blocks": "constraint route remains closure if multiplier is magic",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_2_generator_auxiliary",
            "needed_object": "differentiable generator or algebraic auxiliary solve",
            "required_statement": "either Omega(delta Phi,v_X)=delta G_X with proper Q_X, or E_Lambda/E_X solve X locally before phase space/readout.",
            "current_status": "FORMAL_ROUTE_ONLY",
            "blocks": "X can remain physical hair or leave nonlocal tail",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_3_boundary_degree",
            "needed_object": "boundary charge and degree count",
            "required_statement": "Q_X is zero/proper/exact and the constraint removes exactly the dangerous residual pair.",
            "current_status": "BOUNDARY_AND_DEGREE_UNSIGNED",
            "blocks": "edge charge or hidden scalar pair can survive",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_4_matter_constants_readout",
            "needed_object": "matter/readout descent and constant superselection",
            "required_statement": "ordinary matter, EM, masses, clocks, source weights, and readouts descend after elimination with no shadow frame/source-only slots.",
            "current_status": "MATTER_COUPLING_LOCK_UNSIGNED",
            "blocks": "J_X, qbar_XT, b_alpha/b_mA/b_clock, and source-label terms survive",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_5_q_loc_current_chain",
            "needed_object": "Gamma/Khat/q_loc and PiM/Y5 current chain",
            "required_statement": "Gamma_eff/K_hat are one variational pair, q_loc is parent-zero or bounded, and Delta_Hsrc/I_X/J_X are owned by one parent current chain.",
            "current_status": "CURRENT_CHAIN_AND_QLOC_UNSIGNED",
            "blocks": "local EH/Newton inheritance remains blocked",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_6_no_GR_import",
            "needed_object": "no-GR-import guard",
            "required_statement": "local GR identities may be targets/benchmarks, not premises.",
            "current_status": "PASS_GUARD_NONCLAIM",
            "blocks": "does not block; it keeps the proof honest",
            "valid_for_claim": "False",
        },
        {
            "package_id": "PPA2628_7_verdict",
            "needed_object": "full constraint-source elimination package",
            "required_statement": "PPA2628_0 through PPA2628_6 close in one branch.",
            "current_status": "CONSTRAINT_ELIMINATION_PACKAGE_NOT_CLOSED",
            "blocks": "no local GR/Newton claim",
            "valid_for_claim": "False",
        },
    ]


def dr_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "dr_id": "DRI2628_0_target",
            "object": "D_R normal form",
            "statement": "D_R[MTS]=E_time-E_radial=partial_r C_R-S_R[R_local^MTS]=0 or partial_r(W_R partial_r C_R)=J_R with W_R>0.",
            "current_status": "EXACT_TARGET_NOT_DERIVED",
            "missing_input": "MISSING_E_TIME;MISSING_E_RADIAL;MISSING_L_MTS_CORE",
            "valid_for_claim": "False",
        },
        {
            "dr_id": "DRI2628_1_generic_variation_guard",
            "object": "generic Euler difference",
            "statement": "For generic L(x,y,x',y'), E_x-E_y=(partial_x-partial_y)L-d/dr[(partial_xprime-partial_yprime)L], which does not automatically produce partial_r C_R.",
            "current_status": "NO_GO_GUARD",
            "missing_input": "MISSING_RECIPROCITY_SELECTOR_ORIENTATION",
            "valid_for_claim": "False",
        },
        {
            "dr_id": "DRI2628_2_selector_operator",
            "object": "reciprocity selector/Hcore",
            "statement": "A parent kernel/operator must make the time/radial Euler combination select C_R rather than another variable direction.",
            "current_status": "PRIMARY_MISSING_OBJECT",
            "missing_input": "MISSING_SELECTOR_KERNEL;MISSING_HCORE_SOURCE_EQUATION",
            "valid_for_claim": "False",
        },
        {
            "dr_id": "DRI2628_3_SR_decomposition",
            "object": "S_R residual source side",
            "statement": "All retained residuals enter S_R explicitly: Delta_Hsrc, I_X/J_X, qbar_XT, constants, boundary/history, q_loc, Q_R/J_R, readout leakage.",
            "current_status": "SYMBOLIC_READY_VALUES_MISSING",
            "missing_input": "MISSING_COEFFICIENTS;MISSING_COMMON_UNITS;MISSING_ARENA_PROJECTIONS",
            "valid_for_claim": "False",
        },
        {
            "dr_id": "DRI2628_4_boundary_no_charge",
            "object": "Q_R=0 and normalization",
            "statement": "Source-free D_R integrates to C_R=0 only if boundary/reference class proves Q_R=0 and C_R(infinity)=0 or equivalent regular matching.",
            "current_status": "BOUNDARY_NO_CHARGE_UNSIGNED",
            "missing_input": "MISSING_QR_ZERO;MISSING_BOUNDARY_CLASS",
            "valid_for_claim": "False",
        },
        {
            "dr_id": "DRI2628_5_verdict",
            "object": "local GR/Newton bridge",
            "statement": "D_R is a precise theorem contract, but not a derived MTS equation in the current corpus.",
            "current_status": "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS",
            "missing_input": "MISSING_RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION",
            "valid_for_claim": "False",
        },
    ]


def residual_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RLI2628_0_Delta_Hsrc",
            "symbol": "Delta_Hsrc",
            "meaning": "source-normalization mismatch between parent Hamiltonian charge and observed mass/source readout",
            "enters": "S_R_source_measure",
            "status": "CENTRAL_Y5_RESIDUAL_RETAINED",
            "missing_for_zero_or_bound": "MISSING_PARENT_CURRENT_OWNER;MISSING_DELTA_HSRC_BOUND",
            "arena_links": "Newton;orbital;PPN;Gauss",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_1_I_X",
            "symbol": "I_X",
            "meaning": "first non-EH curl/source component in current integrability",
            "enters": "S_R_current_curl",
            "status": "NOT_THEOREM_ZERO",
            "missing_for_zero_or_bound": "MISSING_IX_ZERO;MISSING_IX_BOUND;MISSING_PIM_PROJECTION",
            "arena_links": "source_normalization;orbital;PPN;local_GR",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_2_J_X_qbarXT",
            "symbol": "J_X/qbar_XT",
            "meaning": "ordinary and hidden matter source current in the dangerous residual direction",
            "enters": "S_R_matter_source",
            "status": "SOURCE_ZERO_NOT_PROVED_COMPONENT_VALUES_MISSING",
            "missing_for_zero_or_bound": "MISSING_Q_KERNEL;MISSING_MATTER_DESCENT;MISSING_COMPONENT_VALUES",
            "arena_links": "R10;WEP;clock;PPN;orbital",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_3_constants",
            "symbol": "b_alpha;b_mu;b_mA;b_nuc;b_clock",
            "meaning": "EM/mass/nuclear/clock leakage into local source and readout",
            "enters": "S_R_constant_composition",
            "status": "CONSTANT_CHANNELS_RETAINED",
            "missing_for_zero_or_bound": "MISSING_NO_EXTRA_F2;MISSING_NO_MASS_VERTEX;MISSING_CONSTANT_SUPERSELECTION",
            "arena_links": "fine_structure;WEP;clock;R10",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_4_boundary_history",
            "symbol": "J_boundary;J_history;qbar_nonH",
            "meaning": "edge charge, reference, support, domain, non-Hilbert and memory/history tails",
            "enters": "S_R_boundary_history",
            "status": "TAILS_NOT_ZERO_NOT_BOUNDED",
            "missing_for_zero_or_bound": "MISSING_BOUNDARY_FLUX_ZERO;MISSING_HISTORY_KERNEL_BOUND;MISSING_NONHILBERT_BOUND",
            "arena_links": "orbital;source_normalization;R10;local_GR",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_5_q_loc",
            "symbol": "epsilon_GK_q_loc",
            "meaning": "Gamma/Khat/q_loc residual blocking local EH/GR inheritance",
            "enters": "S_R_extra_sector",
            "status": "QLOC_ZERO_NOT_DERIVED",
            "missing_for_zero_or_bound": "MISSING_GAMMA_KHAT_ACTION_PAIR;MISSING_OBSERVABLE_LOCK;MISSING_SR_COEFFICIENT",
            "arena_links": "local_GR;PPN;clock;orbital;WEP;R10",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_6_reciprocal_hair",
            "symbol": "Q_R;J_R",
            "meaning": "integration charge/source imbalance in the reciprocal radial-cell equation",
            "enters": "S_R_QR_hair",
            "status": "NO_CHARGE_THEOREM_NOT_DERIVED",
            "missing_for_zero_or_bound": "MISSING_QR_ZERO;MISSING_JR_SOURCE_MAP;MISSING_BOUNDARY_NO_CHARGE",
            "arena_links": "PPN_gamma;orbital;lightcone;local_GR",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RLI2628_7_total",
            "symbol": "R_local^MTS",
            "meaning": "minimal local residual vector after failed current/constraint activation",
            "enters": "S_R_total_abs",
            "status": "FINITE_NONCLAIM_VECTOR_REQUIRED",
            "missing_for_zero_or_bound": "MISSING_COMMON_UNITS;MISSING_ARENA_PROJECTIONS;MISSING_NUMERIC_BOUNDS;MISSING_PARENT_ZERO_THEOREMS",
            "arena_links": "R10;WEP;PPN;clock;orbital;local_GR",
            "valid_for_claim": "False",
        },
    ]


def route_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RV2628_0_physical_scalar",
            "route": "propagating memory/X scalar",
            "verdict": "DEMOTED_TO_CLOSURE_SCAFFOLD",
            "reason": "primitive owner/source/gap/projection gates fail and local tests would punish scalar hair",
            "next_use": "residual template only",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RV2628_1_constraint_auxiliary",
            "route": "constraint/auxiliary/quotient-first elimination",
            "verdict": "LIVE_CONDITIONAL_NOT_PROVED",
            "reason": "exact theorem shape avoids scalar hair, but parent package/current chain is unsigned",
            "next_use": "primary derivation route",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RV2628_2_direct_phase_volume",
            "route": "direct motion-load/phase-volume J_q=1 proof",
            "verdict": "REJECT_AS_CURRENT_DERIVATION",
            "reason": "motivates the condition but does not supply parent Euler/constraint/no-charge machinery",
            "next_use": "intuition and closure baseline only",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RV2628_3_parent_Euler_bridge",
            "route": "D_R[MTS]=partial_r C_R-S_R bridge",
            "verdict": "BEST_STRUCTURAL_ROUTE_BUT_SELECTOR_MISSING",
            "reason": "generic variation does not produce D_R; needs parent reciprocity-selector/Hcore",
            "next_use": "2629 primary target",
            "valid_for_claim": "False",
        },
        {
            "route_id": "RV2628_4_residual_interface",
            "route": "finite local residual vector",
            "verdict": "RETAIN_AS_BACKSTOP_NONCLAIM",
            "reason": "if derivation fails, every live source channel must be bounded rather than hidden",
            "next_use": "source-ready residual rows after selector/source-map exists",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2628_0_magic_multiplier",
            "countermodel": "insert lambda_R C_R or lambda_X X by hand",
            "blocks": "claim that constraint is parent-derived",
            "required_kill_clause": "derive multiplier/constraint from MTS parent action or label closure-only",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2628_1_wrong_Euler_orientation",
            "countermodel": "E_time-E_radial selects the wrong variable combination",
            "blocks": "D_R normal form",
            "required_kill_clause": "parent reciprocity-selector orientation/kernel certificate",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2628_2_boundary_edge_charge",
            "countermodel": "constraint/current has nonzero boundary charge or reciprocal hair",
            "blocks": "Q_R=0 and X elimination",
            "required_kill_clause": "zero/proper/exact boundary charge plus no-charge theorem",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2628_3_matter_reentry",
            "countermodel": "matter, constants, source weights, or readout re-enter after reduction",
            "blocks": "Dq[v_X]=0/J_X=0 physical implication",
            "required_kill_clause": "matter functor/no-shadow/no-source-only-slot/readout-after-variation theorem",
            "retained": "True",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2628_4_q_loc_extra_stress",
            "countermodel": "Gamma/Khat/q_loc formal normal form applies to a shadow variable, not live local residual",
            "blocks": "EH/GR inheritance",
            "required_kill_clause": "live Gamma/Khat action metric-response and observable lock",
            "retained": "True",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2628_0_constraint_eliminates_X",
            "claim": "constraint/auxiliary route eliminates X before physical phase space and matter readout",
            "current_evidence": "exact conditional theorem; parent package unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2628_1_parent_current_chain",
            "claim": "one parent current chain signs L_parent, Theta_total, Q_tau, q/Dq, matter, boundary, q_loc and Euler bridge",
            "current_evidence": "1863 says single parent current chain not signed",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2628_2_DR_normal_form",
            "claim": "D_R[MTS]=partial_r C_R-S_R is derived",
            "current_evidence": "1865 says selector/Hcore missing",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2628_3_SR_zero_or_bound",
            "claim": "S_R=0 or source-backed finite residual bounds exist",
            "current_evidence": "S_R decomposition symbolic; coefficients/units/projections missing",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2628_4_local_GR_Newton",
            "claim": "MTS locally reduces to GR/Newton in current branch",
            "current_evidence": "constraint, D_R, S_R, Q_R, source/current/q_loc gates blocked",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2628_5_empirical_local_pass",
            "claim": "R10/WEP/PPN/clock/orbital arenas pass from this derivation",
            "current_evidence": "finite residual vector lacks source-backed coefficients",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2628_0_conditional_theorem",
            "decision": "CONSTRAINT_ELIMINATION_THEOREM_IS_EXACT_CONDITIONAL",
            "reason": "if X is removed before physical phase space and matter/readout descend, scalar hair is absent",
            "next_action": "keep as proof target, not claim",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2628_1_current_status",
            "decision": "CONSTRAINT_ELIMINATION_NOT_PARENT_ACTIVATED",
            "reason": "parent package, single current chain, D_R selector, S_R silence and boundary no-charge remain unsigned",
            "next_action": "retain R_local^MTS residual interface",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2628_2_no_loop",
            "decision": "DO_NOT_RERUN_SCALAR_OR_PHASE_VOLUME_LOOPS",
            "reason": "physical scalar is closure-only and direct phase-volume is motivational, not a parent derivation",
            "next_action": "attack the smallest live missing object instead",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2628_3_best_next",
            "decision": "RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION_NEXT",
            "reason": "1865 found this is the missing gear between the exact C_R theorem and a derivable local-GR branch",
            "next_action": "derive parent selector/Hcore or demote D_R to closure-only benchmark with source-ready Z_R/J_R/S_R rows",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2629-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
            "script": "scripts/Y5_R2FR_reciprocity_selector_operator_or_Hcore_source_equation_2629.py",
            "objective": "derive the parent reciprocity-selector orientation/kernel or H_core/L_MTS_core source equation that makes the time/radial Euler combination select C_R; if unavailable, demote D_R to closure-only benchmark and emit source-ready Z_R/J_R/S_R residual rows",
            "include": "local variables x=lnT,y=lnsqrtS,C_R; selector orientation; H_core/L_MTS_core; W_R kernel; J_R source map; Q_R boundary/no-charge row; S_R residual coefficient slots",
            "exclude": "AB=1 or p=1 as premise, Einstein-equation import, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "False",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("COPY2628_elimination_gate", "constraint_elimination_theorem_gate", OUTPUTS["elimination_theorem"], LOCAL_BOUNDS / "Constraint_elimination_theorem_gate_2628_NONCLAIM.csv"),
        ("COPY2628_parent_package", "parent_package_audit", OUTPUTS["parent_package"], LOCAL_BOUNDS / "Constraint_parent_package_audit_2628_NONCLAIM.csv"),
        ("COPY2628_dr_interface", "DR_SR_interface_audit", OUTPUTS["dr_interface"], LOCAL_BOUNDS / "DR_SR_interface_audit_2628_NONCLAIM.csv"),
        ("COPY2628_residual_interface", "Rlocal_residual_interface", OUTPUTS["residual_interface"], LOCAL_BOUNDS / "Rlocal_residual_interface_2628_NONCLAIM.csv"),
        ("COPY2628_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2628_RECIPROCITY_SELECTOR_OPERATOR_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source, destination in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source),
                "destination_path": str(destination),
                "destination_exists": b(destination.exists()),
                "csv_parses": b(csv_parses(destination)),
                "row_count": len(read_csv(destination)) if destination.exists() else 0,
            }
        )
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            if row.get("valid_for_claim", "False") != "False":
                return False
            if row.get("claim_allowed", "False") != "False":
                return False
            if row.get("gate_pass", "False") == "True":
                return False
    return True


def missing_not_ready(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and row.get("valid_for_claim", "False") != "False":
                return False
    return True


def validation_rows(generated_paths: list[Path], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    theorem_rows = read_csv(OUTPUTS["elimination_theorem"])
    package_rows = read_csv(OUTPUTS["parent_package"])
    dr_rows = read_csv(OUTPUTS["dr_interface"])
    residual_rows = read_csv(OUTPUTS["residual_interface"])
    route_rows = read_csv(OUTPUTS["route_verdict"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_read = read_csv(OUTPUTS["decision"])
    formalization_patterns = [
        "2628-Y5-R2FR-constraint-auxiliary-memory-source-elimination-or-residual-interface.md",
        "Y5_R2FR_constraint_auxiliary_memory_source_elimination_or_residual_interface_2628.py",
        f"{PREFIX}*",
        "P8_Y5_BRR545_2628_VALIDATION.csv",
        "Constraint_elimination_theorem_gate_2628_NONCLAIM.csv",
        "Constraint_parent_package_audit_2628_NONCLAIM.csv",
        "DR_SR_interface_audit_2628_NONCLAIM.csv",
        "Rlocal_residual_interface_2628_NONCLAIM.csv",
        "JR2628_RECIPROCITY_SELECTOR_OPERATOR_NEXT.csv",
    ]
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in formalization_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks = [
        (
            "VAL2628_00_sources_exist",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and needles are present",
        ),
        (
            "VAL2628_01_conditional_theorem_not_promoted",
            any(row["theorem_id"] == "CET2628_4_current_branch_verdict" and row["proof_status"] == "EXACT_CONDITIONAL_NOT_PARENT_ACTIVATED" for row in theorem_rows),
            "constraint theorem is exact conditional but not parent activated",
        ),
        (
            "VAL2628_02_parent_package_open",
            any(row["package_id"] == "PPA2628_7_verdict" and row["current_status"] == "CONSTRAINT_ELIMINATION_PACKAGE_NOT_CLOSED" for row in package_rows),
            "parent package remains unsigned",
        ),
        (
            "VAL2628_03_DR_not_derived",
            any(row["dr_id"] == "DRI2628_5_verdict" and row["current_status"] == "DR_NORMAL_FORM_NOT_DERIVED_CURRENT_CORPUS" for row in dr_rows),
            "D_R normal form is not derived",
        ),
        (
            "VAL2628_04_residual_interface_retained",
            any(row["residual_id"] == "RLI2628_7_total" and row["status"] == "FINITE_NONCLAIM_VECTOR_REQUIRED" for row in residual_rows),
            "R_local residual interface is retained",
        ),
        (
            "VAL2628_05_scalar_and_phase_loops_blocked",
            any(row["route_id"] == "RV2628_0_physical_scalar" and row["verdict"] == "DEMOTED_TO_CLOSURE_SCAFFOLD" for row in route_rows)
            and any(row["route_id"] == "RV2628_2_direct_phase_volume" and row["verdict"] == "REJECT_AS_CURRENT_DERIVATION" for row in route_rows),
            "physical scalar and direct phase-volume loops are not promoted",
        ),
        (
            "VAL2628_06_claim_gates_safe",
            all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in gate_rows),
            "all local/theory/test claim gates are false",
        ),
        (
            "VAL2628_07_no_claim_flags",
            no_claim_flags([OUTPUTS["elimination_theorem"], OUTPUTS["parent_package"], OUTPUTS["dr_interface"], OUTPUTS["residual_interface"], OUTPUTS["route_verdict"], OUTPUTS["countermodels"], OUTPUTS["decision"], OUTPUTS["next_target"]]),
            "no generated claim-sensitive row is promoted",
        ),
        (
            "VAL2628_08_missing_not_ready",
            missing_not_ready([OUTPUTS["elimination_theorem"], OUTPUTS["parent_package"], OUTPUTS["dr_interface"], OUTPUTS["residual_interface"]]),
            "no MISSING_* row is marked claim-ready",
        ),
        (
            "VAL2628_09_decision_next",
            any(row["decision_id"] == "DEC2628_3_best_next" and row["decision"] == "RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION_NEXT" for row in decision_rows_read),
            "decision selects reciprocity selector/Hcore source equation",
        ),
        (
            "VAL2628_10_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch/local/queue copies exist and parse",
        ),
        (
            "VAL2628_11_formalization_untouched",
            len(formalization_hits) == 0,
            "no 2628 outputs found under formalization-workbench",
        ),
        (
            "VAL2628_12_csv_parse",
            all(csv_parses(path) for path in generated_paths),
            "all generated 2628 CSVs parse",
        ),
        (
            "VAL2628_13_pycache_absent",
            not pycache_path.exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2628_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2628 constraint/auxiliary memory source elimination or residual interface",
            "valid_for_claim": "False",
        }
    )
    return rows


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_doc(tables: dict[str, list[dict[str, Any]]]) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    return f"""# 2628 — Y5 R2/f(R) Constraint/Auxiliary Memory Source Elimination Or Residual Interface

Generated: `{generated_at}`

Status: `Y5_R2FR_2628_constraint_elimination_exact_conditional_parent_unsigned_DR_selector_missing_Rlocal_residual_interface_nonclaim`

Claim ceiling: no constraint-elimination proof, no `D_R` derivation, no `S_R=0`, no boundary no-charge proof, no local-GR/Newton reduction, no R10/WEP/PPN/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is made.

## Summary

2628 answers the question: can we replace the physical scalar route with a cleaner constraint/auxiliary route?

Mathematically, yes as a conditional theorem. If `X` is removed before physical phase space and before ordinary matter/readout are defined, then the dangerous local scalar hair can disappear rather than being tuned quiet.

Physically, not yet. The live MTS branch has not supplied the parent package: one parent action/current chain, constraint origin, generator or auxiliary solve, boundary charge, degree count, matter descent, source-current ownership, `q_loc` lock, and `D_R` selector. So this checkpoint does **not** claim local GR. It keeps the route alive and makes the residual interface explicit.

The key new synthesis is the 1865 obstruction: generic Euler variation does not automatically produce `D_R[MTS]=partial_r C_R-S_R`. The missing gear is a parent reciprocity-selector operator or `H_core/L_MTS_core` source equation.

## Source Register

{markdown_table(tables["source_register"])}

## Lineage Ledger

{markdown_table(tables["lineage"])}

## Constraint Elimination Theorem Gate

{markdown_table(tables["elimination_theorem"])}

## Parent Package Audit

{markdown_table(tables["parent_package"])}

## DR / SR Interface Audit

{markdown_table(tables["dr_interface"])}

## Rlocal Residual Interface

{markdown_table(tables["residual_interface"])}

## Route Verdict

{markdown_table(tables["route_verdict"])}

## Countermodel Ledger

{markdown_table(tables["countermodels"])}

## Claim Gates

{markdown_table(tables["claim_gates"])}

## Decision Ledger

{markdown_table(tables["decision"])}

## Next Target

{markdown_table(tables["next_target"])}

## Branch Copies

{markdown_table(tables["branch_copies"])}

## Validation

{markdown_table(tables["validation"])}

## Plain-English Verdict

This is the best route, but not a win yet. The physical scalar branch stays demoted. The constraint/auxiliary route stays alive because it is the less fragile way to get local GR: remove the residual before matter can see it.

But the route needs one specific missing object now, not vibes: the parent reciprocity-selector or `H_core/L_MTS_core` equation that makes the time/radial Euler combination select `C_R`. If we can derive that, the local-GR problem becomes `S_R=0` plus boundary no-charge. If we cannot, `D_R` becomes a closure benchmark and `R_local^MTS` must fight the data as a finite residual vector.
"""


def main() -> None:
    ensure_dirs()
    tables = {
        "source_register": source_register_rows(),
        "lineage": lineage_rows(),
        "elimination_theorem": elimination_theorem_rows(),
        "parent_package": parent_package_rows(),
        "dr_interface": dr_interface_rows(),
        "residual_interface": residual_interface_rows(),
        "route_verdict": route_verdict_rows(),
        "countermodels": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in tables.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    tables["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(generated_paths, branch_rows)
    tables["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC_PATH.write_text(build_doc(tables), encoding="utf-8")
    print(DOC_PATH)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
