from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4096-Y5-R2FR-exchange-doublet-component-map-or-even-source-normalization-split.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "COMPONENT_SPLIT_LAW_BUILT_EXCHANGE_KILLS_ODD_ONLY_CONSTANT_G_IS_CALIBRATED_COMMON_MODE_Y5_Y6_REDUCED_TO_DERIVATIVE_HAIR_OR_RETAINED_BOUNDS"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4096_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4095_NEXT_TARGET.csv",
        "4096-Y5-R2FR-exchange-doublet-component-map-or-even-source-normalization-split.md",
        "4095 selects exchange-doublet component map or even source-normalization split.",
    ),
    "SRC4096_01_4095_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT.csv",
        "Y5_source_normalization",
        "4095 component verdict identifies Y5/Y6 as hard rows.",
    ),
    "SRC4096_02_4095_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT.csv",
        "c_domain_source_normalization_operator",
        "4095 source-current fallback contract for hard rows.",
    ),
    "SRC4096_03_exchange_score": (
        SOURCE_DIR / "P8_EXCHANGE_COMPONENT_MAP_SCORE.csv",
        "Y5_source_normalization",
        "Old exchange component map scores all Yloc channels.",
    ),
    "SRC4096_04_exchange_gates": (
        SOURCE_DIR / "P8_EXCHANGE_COMPONENT_GATE_TESTS.csv",
        "G2_source_normalization",
        "Exchange gate tests show source normalization is not killed by oddness alone.",
    ),
    "SRC4096_05_exchange_hard_rows": (
        SOURCE_DIR / "P8_EXCHANGE_COMPONENT_HARD_ROWS.csv",
        "Y6_stress_Bianchi",
        "Hard-row ledger for Y5/Y6, matter readout, and boundary odd charge.",
    ),
    "SRC4096_06_source_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S5_Newton_gate",
        "Source-normalization theorem stack: same frame, constant kappa, Gauss mass, no extra charge.",
    ),
    "SRC4096_07_source_routes": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_ROUTE_CLASSIFICATION.csv",
        "absolute_calibration_offset",
        "Route classification separates theorem-first rows from retained calibration offsets.",
    ),
    "SRC4096_08_source_zero_targets": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
        "DZ7_parent_fixed_calibration",
        "Derived-zero targets include parent-fixed calibration and derivative-hair conditions.",
    ),
    "SRC4096_09_source_coefficients": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv",
        "F0_c_domain_source_normalization_operator",
        "Coefficient fill for source-normalization and local PPN residuals.",
    ),
    "SRC4096_10_weak_field": (
        SOURCE_DIR / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv",
        "WFS3377_6_normalization_verdict",
        "Weak-field source-normalization theorem target linking EH coefficient, Hilbert source, Poisson and PPN.",
    ),
    "SRC4096_11_newton_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
        "NEW3382_0_same_kappa",
        "Newton source-normalization chain: fixed kappa gives Poisson coefficient; numeric G remains calibrated.",
    ),
    "SRC4096_12_gm_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv",
        "SNG3818_3_no_orbital_GM_import",
        "Anti-circular measured-GM guardrails.",
    ),
    "SRC4096_13_ppn_map": (
        SOURCE_DIR / "P8_Y5_R2FR_3954_PPN_SOURCE_NORMALIZATION_RESIDUAL_MAP.csv",
        "PPN3954_7_Geff_product",
        "PPN source-normalization residual map for product drift/source hair.",
    ),
    "SRC4096_14_em_stress": (
        SOURCE_DIR / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv",
        "SP3274_3_Poynting_readout",
        "EM Hilbert stress/Poynting interface for Maxwell stress as ordinary even source, not killed residual.",
    ),
    "SRC4096_15_hilbert_exchange": (
        SOURCE_DIR / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv",
        "NEC2615_4_common_mode",
        "Noether exchange collapse: connected ordinary matter leaves common source calibration.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4096_16_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4096 exchange/even source-normalization split.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def component_split_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "CST4096_0_split_definition",
            "statement": "Each compact-local residual must be split into exchange-odd, exchange-even invisible/common, and retained active pieces.",
            "formula": "Y_loc^A = Y_odd^A + Y_even,invis^A + Y_ret^A",
            "derivation_payoff": "exchange symmetry is used only where it is mathematically licensed",
            "current_status": "SPLIT_LAW_ADOPTED_FOR_NEXT_LOCAL_BRANCH",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "CST4096_1_exchange_zero",
            "statement": "Exact exchange doublets can only zero the odd piece.",
            "formula": "E: Z^A -> -Z^A and S[Z]=S[-Z], B_Z=0, M>0 => Y_odd^A=0",
            "derivation_payoff": "prevents the false move of killing even source normalization by symmetry",
            "current_status": "CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "CST4096_2_even_invisible",
            "statement": "An exchange-even piece is harmless only if it is topological/exact, derivative-free common calibration, or outside the scored local PPN projection.",
            "formula": "Pi_PPN[Y_even,invis^A]=0 and D_r,t,species Y_even,invis^A=0",
            "derivation_payoff": "keeps universal G_ref calibration separate from physical source hair",
            "current_status": "THEOREM_TARGET_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "CST4096_3_retained_bound",
            "statement": "Any remaining active piece must be carried as a coefficient/vector bound row.",
            "formula": "Y_ret^A != 0 => map to alpha1, alpha2, alpha3, xi, gamma, beta, zeta_i, Gdot, R10/R11 as appropriate",
            "derivation_payoff": "failed derivation becomes testable rather than hidden closure",
            "current_status": "BOUND_BRANCH_READY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def yloc_component_split_rows() -> List[dict]:
    return [
        {
            "component_id": "Y0_trace_expansion",
            "odd_candidate": "antisymmetric trace-load residual",
            "even_invisible_candidate": "pure common EH trace calibration if same-frame and derivative-free",
            "retained_active_piece": "trace/source scalar hair",
            "verdict_4096": "SPLIT_NOT_CLOSED",
            "next_proof_or_bound": "prove same-frame EH trace owner or retain scalar/source-current row",
            "blocks": "gamma; beta; R11; source normalization",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y1_coherent_projector",
            "odd_candidate": "antisymmetric nontrace projector representative",
            "even_invisible_candidate": "topological projector stress with zero local metric variation",
            "retained_active_piece": "projector stress ledger",
            "verdict_4096": "SPLIT_NOT_CLOSED",
            "next_proof_or_bound": "derive projector topological invisibility or retain T_projector coefficient",
            "blocks": "xi; alpha_i; zeta_i; R11",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y2_boundary_flux",
            "odd_candidate": "relative boundary-current class",
            "even_invisible_candidate": "exact/topological boundary term or fixed reference subtraction",
            "retained_active_piece": "boundary flux/source measure",
            "verdict_4096": "CONDITIONAL_ODD_OR_TOPOLOGICAL_ROUTE",
            "next_proof_or_bound": "prove compact local no-odd-flux and exact boundary variation; otherwise alpha3/zeta bound",
            "blocks": "alpha3; zeta_i; beta; source calibration",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y3_domain_vector",
            "odd_candidate": "exchange-odd domain vector representative",
            "even_invisible_candidate": "scalar/topological domain selector with no local vector",
            "retained_active_piece": "preferred-frame vector current",
            "verdict_4096": "BEST_COMPONENT_TO_PROVE_NEXT",
            "next_proof_or_bound": "derive domain vector oddness and zero odd local charge; otherwise alpha1/alpha2/alpha3 products",
            "blocks": "alpha1; alpha2; alpha3; R11",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y4_domain_STF_stress",
            "odd_candidate": "antisymmetric STF stress",
            "even_invisible_candidate": "transverse/topological STF stress outside local PPN projection",
            "retained_active_piece": "tidal/projector anisotropy",
            "verdict_4096": "SPLIT_NOT_CLOSED",
            "next_proof_or_bound": "prove local STF invisibility or retain xi anisotropy bound",
            "blocks": "xi; alpha_i; gamma/beta anisotropy",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y5_source_normalization",
            "odd_candidate": "mu_odd from exchange-odd extra source charge",
            "even_invisible_candidate": "universal parent-fixed G_ref/common calibration with no radial/time/species derivatives",
            "retained_active_piece": "mu_ret(r,t,species,range) and c_domain_source_normalization_operator",
            "verdict_4096": "REDUCED_TO_DERIVATIVE_HAIR_OR_RETAINED_BOUND",
            "next_proof_or_bound": "derive same-frame constant kappa/Gauss-law source owner and prove partial_r,t,species mu_ret=0; otherwise fill source-normalization residual map",
            "blocks": "Newton source coupling; Gdot; WEP source charge; R10; R11; gamma/beta/zeta",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y6_stress_Bianchi",
            "odd_candidate": "exchange-current stress transfer pair",
            "even_invisible_candidate": "topological/exact stress or common cosmological/constant mode outside local PPN",
            "retained_active_piece": "T_extra_even with PPN projection",
            "verdict_4096": "REDUCED_TO_TOPOLOGICAL_INVISIBILITY_OR_STRESS_BOUND",
            "next_proof_or_bound": "derive Pi_PPN[T_extra_even]=0 using Ward/topological route or retain stress residual vector",
            "blocks": "Bianchi consistency; gamma; beta; zeta_i; xi; EM/source exchange",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def source_normalization_law_rows() -> List[dict]:
    return [
        {
            "law_id": "SNL4096_0_observed_EH_source",
            "object": "ordinary observed mass/source",
            "formula": "mu_obs = G_ref M_H when S_EH[g_obs] and S_matter[psi,g_obs] share the same frame",
            "meaning": "Newtonian source normalization is derived as a single parent coefficient if same-frame EH plus Hilbert source is parent-owned",
            "status": "CONDITIONAL_PARENT_BRANCH",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "law_id": "SNL4096_1_constant_G_ref",
            "object": "Newton constant status",
            "formula": "kappa_MTS = 8*pi*G_ref/c^4; G_ref is calibrated, not numerically derived here",
            "meaning": "Matching GR/Newton requires deriving one universal constant's role, not deriving its numerical value from nothing",
            "status": "IMPORTANT_CLARIFICATION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "law_id": "SNL4096_2_odd_extra_source",
            "object": "exchange-odd extra source charge",
            "formula": "mu_odd -> 0 if exact exchange + zero local odd charge + positive operator",
            "meaning": "exchange symmetry can help only this sector",
            "status": "CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "law_id": "SNL4096_3_even_extra_source",
            "object": "even source-normalization hair",
            "formula": "mu_even_ret = mu_even(r,t,A,lambda,species) with D mu_even_ret != 0",
            "meaning": "even range/time/species/radial source hair is physical and must be zeroed by theorem or bounded",
            "status": "LIVE_BOUND_ROUTE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "law_id": "SNL4096_4_harmless_common_mode",
            "object": "common connected-source prefactor",
            "formula": "T_active = w_star T_total and kappa_eff=kappa*w_star, with D w_star=0",
            "meaning": "a universal derivative-free common factor is calibration, not a preferred-frame/fifth-force signal",
            "status": "CONDITIONAL_HARMLESS_IF_PARENT_FIXED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "law_id": "SNL4096_5_no_absorption_cheat",
            "object": "anti-circular measured-GM policy",
            "formula": "GM_orbit/G_ref cannot fill M_H unless Poisson/Gauss/source chain is already derived",
            "meaning": "do not import orbital GM to prove Newton; derive the source chain first",
            "status": "GUARDRAIL_RETAINED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def constant_g_calibration_rows() -> List[dict]:
    return [
        {
            "row_id": "G4096_0_GR_baseline",
            "question": "Does GR derive the numerical value of Newton's constant?",
            "answer": "No; GR takes the EH coefficient/G as an empirical constant while deriving its universal role in field equations and Newtonian limit.",
            "MTS_requirement": "MTS must derive the same single-coefficient role from parent action/readout, not necessarily the numeric value of G_ref.",
            "status": "BASELINE_CLARIFIED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "G4096_1_success_condition",
            "question": "What would count as source-coupling success?",
            "answer": "One single universal coefficient, the parent-owned kappa/G_ref, controls EH variation, Hilbert source, Hamiltonian/Gauss mass, Poisson equation and first PPN potential U.",
            "MTS_requirement": "S_EH[g_obs] + S_matter[psi,g_obs] + fixed H_ref/Pi_M source charge with no independent source scaling.",
            "status": "THEOREM_TARGET",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "G4096_2_failure_condition",
            "question": "What would fail the Newton/GR bridge?",
            "answer": "Any independent range/time/species/radial source-normalization factor not theorem-zeroed or bounded.",
            "MTS_requirement": "D_r G_eff = D_t G_eff = D_species G_eff = D_lambda G_eff = 0, or executable residual bounds.",
            "status": "BOUND_IF_NOT_DERIVED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def em_poynting_interface_rows() -> List[dict]:
    return [
        {
            "interface_id": "EM4096_0_keep_EM_as_source",
            "object": "Maxwell/EM Hilbert stress",
            "formula": "T_EM^{mu nu}=Z_Q(F^{mu rho}F^nu_rho - 1/4 g_obs^{mu nu}F^2)",
            "role_in_local_GR": "EM stress is ordinary even source in T_H, not a residual to be killed by exchange",
            "test": "same g_obs/coframe and same kappa/G_ref must source curvature",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "interface_id": "EM4096_1_Poynting_exchange",
            "object": "Poynting vector/readout",
            "formula": "u_EM=Z_Q(E^2+B^2)/2; S_EM=Z_Q(E x B)",
            "role_in_local_GR": "Poynting flow belongs inside conserved total Hilbert stress unless Z_Q/readout gradients create Q_Z",
            "test": "Q_Z^nu=0 theorem or retain EM/source exchange residual",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "interface_id": "EM4096_2_stress_residual",
            "object": "unowned EM/source exchange",
            "formula": "q_loc^nu ~ P_loc nabla_mu T_extra^{mu nu}; Q_Z^nu contributes if Maxwell owner/readout is not fixed",
            "role_in_local_GR": "EM does not close local GR unless its stress is same-frame and Ward-owned",
            "test": "future Maxwell gate must prove same-frame EM Hilbert stress or bound Q_Z",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def retained_bound_queue_rows() -> List[dict]:
    return [
        {
            "queue_id": "RB4096_0_source_derivative_hair",
            "retained_object": "mu_ret(r,t,species,lambda)",
            "zero_route": "same-frame EH source owner + constant kappa + no extra long-range charge",
            "bound_route": "Gdot, inverse-square/R10, WEP species charge, radial source-hair map",
            "priority": "P0",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "queue_id": "RB4096_1_domain_vector",
            "retained_object": "epsilon_domain_vector",
            "zero_route": "exchange-odd domain vector + zero local odd charge",
            "bound_route": "alpha1<=4e-5; alpha2<=2e-9; alpha3<=4e-20 products",
            "priority": "P0",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "queue_id": "RB4096_2_boundary_flux",
            "retained_object": "epsilon_boundary_flux",
            "zero_route": "exact/topological boundary or compact no-flux theorem",
            "bound_route": "alpha3<=4e-20; zeta/beta boundary rows",
            "priority": "P1",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "queue_id": "RB4096_3_STF_stress",
            "retained_object": "epsilon_domain_anisotropy",
            "zero_route": "topological/transverse STF invisibility",
            "bound_route": "xi<=4e-9 and anisotropic PPN residuals",
            "priority": "P1",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "queue_id": "RB4096_4_EM_stress_exchange",
            "retained_object": "Q_Z^nu / EM readout-gradient exchange",
            "zero_route": "same-frame Maxwell Hilbert stress and constant Z_Q owner",
            "bound_route": "clock/WEP/source-exchange residual vector",
            "priority": "P1",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "queue_id": "RB4096_5_even_extra_stress",
            "retained_object": "Pi_PPN[T_extra_even]",
            "zero_route": "topological/exact or common cosmological mode locally invisible",
            "bound_route": "gamma/beta/zeta_i/xi residual coefficients",
            "priority": "P0",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_gate_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4096_0_main",
            "decision": "adopt the component split law",
            "meaning": "Exchange doublets kill odd local residuals only; even source normalization is treated as common calibration, invisible topology, or retained bound.",
            "result": "Y5 and Y6 are no longer vague blockers; they are derivative-hair/stress-projection tests",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4096_1_G",
            "decision": "do not chase the numerical derivation of G_ref at this stage",
            "meaning": "GR also calibrates G; the correct local-GR target is deriving a single universal coefficient's role.",
            "result": "next proof focuses on same-frame kappa/Hilbert/Gauss/Poisson chain",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4096_2_EM",
            "decision": "keep EM/Poynting stress as ordinary even source unless readout gradients create an exchange residual",
            "meaning": "Poynting is not background magic to erase; it is part of total Hilbert stress if same-frame Maxwell ownership holds.",
            "result": "future Maxwell gate should prove same-frame stress or bound Q_Z",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4096_3_no_claim",
            "decision": "no local-GR/Newton/Maxwell/source-coupling pass is claimed",
            "meaning": "The route is sharper but still conditional until same-frame source owner and derivative-hair silence are parent-signed.",
            "result": "move to executable source-coupling theorem gate",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4096_0_component_split",
            "claim": "component split law is a valid next formal route",
            "allowed": "True",
            "reason": "It prevents exchange-odd overclaim while preserving theorem and bound paths.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4096_1_Yloc_zero",
            "claim": "Yloc=0 is derived",
            "allowed": "False",
            "reason": "Y_even,invis and Y_ret pieces are not yet zeroed or bounded.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4096_2_Newton_source",
            "claim": "MTS derives source-normalized Newtonian mechanics",
            "allowed": "False",
            "reason": "same-frame kappa/Hilbert/Gauss/Poisson chain is conditional and derivative-hair rows remain live.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4096_3_G_number",
            "claim": "MTS derives the numerical value of Newton's constant",
            "allowed": "False",
            "reason": "not required for local-GR matching and not derived here; G_ref remains calibrated like GR's G.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4096_4_EM_Maxwell",
            "claim": "Maxwell/EM stress coupling is fully derived",
            "allowed": "False",
            "reason": "4096 only installs the same-frame Hilbert/Poynting interface and residual test.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4096_0",
            "next_target": "4097-Y5-R2FR-same-frame-source-coupling-theorem-or-derivative-hair-bound.md",
            "script": "scripts/Y5_R2FR_4097_same_frame_source_coupling_theorem_or_derivative_hair_bound.py",
            "why": "4096 reduces Y5 to a concrete source-coupling theorem: same frame, constant kappa, Hilbert source, Gauss mass and no derivative hair.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4096_1",
            "next_target": "4098-Y5-R2FR-EM-Maxwell-Hilbert-Poynting-same-frame-gate.md",
            "script": "defer_until_4097_source_chain",
            "why": "EM/Poynting should be tested as same-frame Hilbert stress after the source-coupling theorem is stabilized.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4096",
            "decision": DECISION,
            "new_forward_object": "Y_loc_split=Y_odd+Y_even_invis+Y_retained_bound",
            "Yloc_zero_public": "False",
            "Newton_source_public": "False",
            "G_numeric_derivation_public": "False",
            "EM_Maxwell_public": "False",
            "next_required_gate": "same_frame_source_coupling_theorem_or_derivative_hair_bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4096 - Exchange Doublet Component Map Or Even Source-Normalization Split",
                "",
                "## Purpose",
                "",
                "4095 selected exchange-doublet parentization as the cleanest no-linear-source route. 4096 makes the next leap: exchange symmetry kills only odd residuals, so each local residual must be split before we can judge whether local GR/Newton is derivable.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public `Y_loc=0` claim: `false`",
                "- Public Newton/source-coupling claim: `false`",
                "- Public Maxwell/EM stress claim: `false`",
                "",
                "## Component Split Law",
                "",
                "```text",
                "Y_loc^A = Y_odd^A + Y_even,invis^A + Y_ret^A",
                "",
                "exchange doublets can prove:       Y_odd^A = 0",
                "topology/common calibration can hide: Pi_PPN[Y_even,invis^A] = 0",
                "anything else must be bounded:      Y_ret^A -> alpha_i, xi, gamma, beta, zeta, Gdot, R10/R11",
                "```",
                "",
                "This is important because it stops the bad move: pretending source normalization is odd. Measured `GM` is exchange-even. The derivable target is not killing `GM`; it is proving that one parent-owned `G_ref/kappa` controls EH variation, Hilbert source, Gauss mass, Poisson/Newton, and the first PPN potential without extra derivative hair.",
                "",
                "## Newton Constant Clarification",
                "",
                "GR does not derive the numerical value of `G`; it calibrates it. MTS does not need to derive the number of `G_ref` to reduce to GR/Newton. What it must derive is that there is only one universal source coefficient in the local branch, with no independent range, time, species, radial, or readout-dependent source scaling.",
                "",
                "## EM/Poynting Hook",
                "",
                "EM stress and the Poynting vector belong in ordinary same-frame Hilbert stress if the Maxwell block is parent-owned. They are not residuals to kill. The residual is any unowned readout-gradient/source-exchange current `Q_Z^nu`, which must be theorem-zeroed or bounded.",
                "",
                "## What Improved",
                "",
                "- `Y5_source_normalization` is now reduced to derivative-hair/source-coupling tests, not a vague missing coupling.",
                "- `Y6_stress_Bianchi` is reduced to topological invisibility or a retained stress residual vector.",
                "- `Y3_domain_vector` remains the best pure exchange component to try proving next, but `Y5` is the main Newton/GR gate.",
                "- A calibrated `G_ref` is treated correctly: allowed as a GR-like empirical constant, forbidden as a place to absorb unproved source hair.",
                "",
                "## Next Target",
                "",
                "`4097-Y5-R2FR-same-frame-source-coupling-theorem-or-derivative-hair-bound.md` should try to prove the same-frame source-coupling chain directly. If it fails, it must fill derivative-hair/source-normalization bound rows.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4096_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4096_COMPONENT_SPLIT_THEOREM.csv`",
                "- `P8_Y5_R2FR_4096_YLOC_COMPONENT_SPLIT.csv`",
                "- `P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW.csv`",
                "- `P8_Y5_R2FR_4096_CONSTANT_G_CALIBRATION.csv`",
                "- `P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE.csv`",
                "- `P8_Y5_R2FR_4096_RETAINED_BOUND_QUEUE.csv`",
                "- `P8_Y5_R2FR_4096_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4096_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4096_NEXT_TARGET.csv`",
                "- `P8_Y5_R2FR_4096_STATUS.csv`",
                "- `P8_Y5_BRR545_4096_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4096_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4096_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4096_COMPONENT_SPLIT_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4096_COMPONENT_SPLIT_THEOREM.csv",
        "P8_Y5_R2FR_4096_YLOC_COMPONENT_SPLIT": SOURCE_DIR / "P8_Y5_R2FR_4096_YLOC_COMPONENT_SPLIT.csv",
        "P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW": SOURCE_DIR / "P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW.csv",
        "P8_Y5_R2FR_4096_CONSTANT_G_CALIBRATION": SOURCE_DIR / "P8_Y5_R2FR_4096_CONSTANT_G_CALIBRATION.csv",
        "P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE": SOURCE_DIR / "P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE.csv",
        "P8_Y5_R2FR_4096_RETAINED_BOUND_QUEUE": SOURCE_DIR / "P8_Y5_R2FR_4096_RETAINED_BOUND_QUEUE.csv",
        "P8_Y5_R2FR_4096_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4096_DECISION_GATE.csv",
        "P8_Y5_R2FR_4096_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4096_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4096_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4096_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4096_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4096_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4096_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_COMPONENT_SPLIT_THEOREM"], component_split_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_YLOC_COMPONENT_SPLIT"], yloc_component_split_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW"], source_normalization_law_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_CONSTANT_G_CALIBRATION"], constant_g_calibration_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE"], em_poynting_interface_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_RETAINED_BOUND_QUEUE"], retained_bound_queue_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4096_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4096_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4096_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4096_COMPONENT_SPLIT_THEOREM"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(
        needle in theorem_text
        for needle in ["Y_odd", "Y_even,invis", "Y_ret", "exchange", "BOUND_BRANCH_READY"]
    )
    rows.append(
        {
            "check_id": "VAL4096_COMPONENT_SPLIT_THEOREM",
            "check": "component split theorem separates odd, even-invisible and retained-bound pieces",
            "passed": bool_string(theorem_ok),
            "detail": "requires Y_odd, Y_even,invis and Y_ret branches",
            "timestamp_utc": TIMESTAMP,
        }
    )

    components = parse_csv(outputs["P8_Y5_R2FR_4096_YLOC_COMPONENT_SPLIT"])
    component_text = "\n".join(str(row) for row in components)
    component_ok = all(f"Y{i}_" in component_text for i in range(7))
    hard_ok = all(
        needle in component_text
        for needle in [
            "REDUCED_TO_DERIVATIVE_HAIR_OR_RETAINED_BOUND",
            "REDUCED_TO_TOPOLOGICAL_INVISIBILITY_OR_STRESS_BOUND",
            "BEST_COMPONENT_TO_PROVE_NEXT",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4096_COMPONENT_COVERAGE",
            "check": "Yloc component split covers Y0-Y6 and identifies Y3/Y5/Y6 roles",
            "passed": bool_string(component_ok and hard_ok),
            "detail": f"component_rows={len(components)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    source_law = parse_csv(outputs["P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW"])
    source_text = "\n".join(str(row) for row in source_law)
    source_ok = all(needle in source_text for needle in ["G_ref", "kappa_MTS", "mu_odd", "mu_even_ret", "GM_orbit"])
    rows.append(
        {
            "check_id": "VAL4096_SOURCE_NORMALIZATION_LAW",
            "check": "source normalization law separates observed EH source, odd extra source, even hair and anti-circular guard",
            "passed": bool_string(source_ok),
            "detail": "requires G_ref/kappa, odd source, even retained hair and GM guard",
            "timestamp_utc": TIMESTAMP,
        }
    )

    g_rows = parse_csv(outputs["P8_Y5_R2FR_4096_CONSTANT_G_CALIBRATION"])
    g_text = "\n".join(str(row) for row in g_rows)
    g_ok = all(needle in g_text for needle in ["GR takes", "single universal coefficient", "D_r G_eff"])
    rows.append(
        {
            "check_id": "VAL4096_G_CALIBRATION",
            "check": "constant-G status is correctly treated as calibrated common mode, not numerically derived",
            "passed": bool_string(g_ok),
            "detail": "prevents wasting route on deriving numeric G before source role is closed",
            "timestamp_utc": TIMESTAMP,
        }
    )

    em_rows = parse_csv(outputs["P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE"])
    em_text = "\n".join(str(row) for row in em_rows)
    em_ok = all(needle in em_text for needle in ["T_EM", "S_EM", "Q_Z"])
    rows.append(
        {
            "check_id": "VAL4096_EM_INTERFACE",
            "check": "EM/Poynting interface keeps Maxwell stress as even source and isolates exchange residual",
            "passed": bool_string(em_ok),
            "detail": "requires T_EM, Poynting S_EM and Q_Z residual",
            "timestamp_utc": TIMESTAMP,
        }
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4096_RETAINED_BOUND_QUEUE"])
    bound_text = "\n".join(str(row) for row in bounds)
    bound_ok = all(needle in bound_text for needle in ["Gdot", "alpha1<=4e-5", "alpha2<=2e-9", "alpha3<=4e-20", "xi<=4e-9", "Q_Z"])
    rows.append(
        {
            "check_id": "VAL4096_BOUND_QUEUE",
            "check": "retained bound queue covers derivative hair, preferred-frame, boundary, xi, EM and stress residuals",
            "passed": bool_string(bound_ok),
            "detail": f"bound_rows={len(bounds)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claims = parse_csv(outputs["P8_Y5_R2FR_4096_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    rows.append(
        {
            "check_id": "VAL4096_NO_PUBLIC_CLAIM",
            "check": "4096 does not promote Yloc zero, Newton source, numeric G or Maxwell claims",
            "passed": bool_string(no_public),
            "detail": "all claim rows remain private/nonclaim",
            "timestamp_utc": TIMESTAMP,
        }
    )

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4096_NEXT_TARGET"])
    next_text = "\n".join(str(row) for row in next_rows)
    next_ok = "4097-Y5-R2FR-same-frame-source-coupling-theorem-or-derivative-hair-bound.md" in next_text
    rows.append(
        {
            "check_id": "VAL4096_NEXT_TARGET",
            "check": "next target is same-frame source coupling theorem or derivative-hair bound",
            "passed": bool_string(next_ok),
            "detail": "requires 4097 next target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4096_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4096_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4096_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4096 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
