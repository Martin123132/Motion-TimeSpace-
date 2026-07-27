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
DOC_PATH = ROOT / "4095-Y5-R2FR-Yloc-no-linear-source-symmetry-or-source-current-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "EXCHANGE_DOUBLET_PARENTIZATION_SELECTED_AS_BEST_NO_LINEAR_SOURCE_ROUTE_COMPONENT_MAP_AND_EVEN_SOURCE_ROWS_STILL_UNSIGNED"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4095_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4094_NEXT_TARGET.csv",
        "4095-Y5-R2FR-Yloc-no-linear-source-symmetry-or-source-current-bound.md",
        "4094 selects the Yloc no-linear-source symmetry/source-current bound target.",
    ),
    "SRC4095_01_no_linear_theorem": (
        SOURCE_DIR / "P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv",
        "T1_exact_reflection",
        "No-linear-source theorem template: exact reflection/evenness forbids odd linear terms.",
    ),
    "SRC4095_02_parent_contract": (
        SOURCE_DIR / "P8_YLOC_NO_LINEAR_SOURCE_PARENT_CONTRACT.csv",
        "C5_composite_residual_lock",
        "Parent contract showing the physical residual lock is a required unsourced clause.",
    ),
    "SRC4095_03_component_audit": (
        SOURCE_DIR / "P8_YLOC_NO_LINEAR_SOURCE_COMPONENT_AUDIT.csv",
        "Y5_source_normalization",
        "Component audit identifying source-normalization as a hard local residual row.",
    ),
    "SRC4095_04_counterexamples": (
        SOURCE_DIR / "P8_YLOC_NO_LINEAR_SOURCE_COUNTEREXAMPLES.csv",
        "CE3_source_normalization_offset",
        "Counterexample ledger showing source-normalization offsets survive naive reflection.",
    ),
    "SRC4095_05_aux_action": (
        SOURCE_DIR / "P8_YLOC_AUX_PARENT_ACTION_CANDIDATES.csv",
        "A2_odd_residual_parentization",
        "Auxiliary parent-action candidates selecting odd residual parentization as best theorem target.",
    ),
    "SRC4095_06_aux_decision": (
        SOURCE_DIR / "P8_YLOC_AUX_PARENT_DECISION.csv",
        "odd_residual_parentization",
        "Decision ledger preserving the lock/Z2 triangle and selecting odd parentization.",
    ),
    "SRC4095_07_exchange_theorem": (
        SOURCE_DIR / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv",
        "E2_odd_residual",
        "Exchange-doublet theorem candidate: Z^A=(R_+^A-R_-^A)/2 and Yloc identity through PPN.",
    ),
    "SRC4095_08_exchange_contract": (
        SOURCE_DIR / "P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv",
        "O3_component_identity",
        "Exchange-doublet contract showing component identity is not derived.",
    ),
    "SRC4095_09_component_map": (
        SOURCE_DIR / "P8_ODD_RESIDUAL_COMPONENT_MAP.csv",
        "Y5_source_normalization",
        "Component map marking Y5 source normalization failed-current.",
    ),
    "SRC4095_10_even_odd_split": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_EVEN_ODD_SPLIT.csv",
        "E2_even_extra_source",
        "Even/odd source-normalization split showing even source offsets are not killed by exchange.",
    ),
    "SRC4095_11_closure_fill": (
        SOURCE_DIR / "P8_ODD_RESIDUAL_CLOSURE_FILL.csv",
        "F3_source_normalization_gap",
        "Closure fill for component-map, boundary, source-normalization and even-stress gaps.",
    ),
    "SRC4095_12_4094_r11": (
        SOURCE_DIR / "P8_Y5_R2FR_4094_R11_SELECTOR_MATRIX.csv",
        "R11DZ4094_6_source_normalization",
        "4094 R11 selector matrix showing source-normalization remains a nonprojector R11 family.",
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
            "source_id": "SRC4095_13_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4095 no-linear-source gate and source-current fallback.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def no_linear_source_gate_rows() -> List[dict]:
    return [
        {
            "gate_id": "NLS4095_0_exchange_doublet_parent_variables",
            "required_clause": "Every dangerous local residual channel has parent representatives R_+^A and R_-^A.",
            "mathematical_role": "Makes the odd local residual a structural parent variable, not a notational sign flip.",
            "formula": "Z^A=(R_+^A-R_-^A)/2; R_even^A=(R_+^A+R_-^A)/2",
            "current_status": "BEST_ROUTE_NOT_PARENT_SIGNED",
            "if_closed": "oddness becomes object-language and linear Z terms can be symmetry-forbidden",
            "if_open": "Yloc zero remains a closure/bound problem",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_1_exact_exchange_symmetry",
            "required_clause": "The parent action and admissible local branch are exactly invariant under R_+^A <-> R_-^A.",
            "mathematical_role": "Forbids every exchange-odd linear source coefficient.",
            "formula": "S[Z]=S[-Z] => delta S/dZ|_{Z=0}=J_Z=0",
            "current_status": "CONDITIONAL_TEMPLATE",
            "if_closed": "bulk odd source current is zero",
            "if_open": "CE0-style conserved scalar source remains legal",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_2_even_matter_readout",
            "required_clause": "Matter and clocks couple only to exchange-even quotient geometry and constants.",
            "mathematical_role": "Stops compact matter from sourcing the odd residual sector.",
            "formula": "S_matter=S_matter[Psi,e_obs(R_even),theta_even]",
            "current_status": "NOT_DERIVED",
            "if_closed": "local compact matter does not generate J_Z",
            "if_open": "matter-visible odd charge can reintroduce preferred-frame/source residuals",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_3_boundary_odd_charge_zero",
            "required_clause": "Compact local domains carry no exchange-odd boundary charge or flux.",
            "mathematical_role": "Forbids boundary B_Z terms that feed alpha3, zeta, beta and source hair.",
            "formula": "B_Z=0 on local compact branch",
            "current_status": "NOT_DERIVED",
            "if_closed": "boundary flux cannot source Yloc",
            "if_open": "retain W_boundary_alpha3*epsilon_boundary_flux",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_4_component_identity",
            "required_clause": "The exchange-odd parent residual equals the physical compact-local residual through scored PPN order.",
            "mathematical_role": "Zeros the actual residuals rather than an auxiliary shadow variable.",
            "formula": "Z^A=Y_loc^A+O(PPN beyond gate)",
            "current_status": "NOT_DERIVED_FOR_Y0_Y6",
            "if_closed": "positive operator can force Y_loc=0",
            "if_open": "exchange symmetry zeros only bookkeeping fields",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_5_positive_operator",
            "required_clause": "The exchange-odd sector has positive Hessian after constraints/gauge are removed.",
            "mathematical_role": "Turns zero source and zero boundary into a zero-amplitude theorem.",
            "formula": "M_AB Z^B=0 with M>0 => Z^A=0",
            "current_status": "FORMAL_CANDIDATE_FROM_YLOC_POSITIVITY",
            "if_closed": "exchange no-source theorem yields Yloc zero once component identity closes",
            "if_open": "zero source is insufficient; flat/unstable modes survive",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_6_source_normalization_even_split",
            "required_clause": "Source-normalization residuals are either odd and no-charged, theorem-zero, or explicitly bounded.",
            "mathematical_role": "Prevents even measured-GM/source offsets from slipping through the odd-sector proof.",
            "formula": "Delta_mu_source = mu_odd + mu_even; exchange kills only mu_odd",
            "current_status": "HARD_BLOCKER_Y5_FAILED_CURRENT",
            "if_closed": "R11 source-normalization family can enter double-zero route",
            "if_open": "retain c_domain_source_normalization_operator",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NLS4095_7_even_extra_stress_accounting",
            "required_clause": "Exchange-even extra stress is topological/invisible through local PPN or retained as a residual vector.",
            "mathematical_role": "Exchange symmetry does not erase even conserved stress/Bianchi debt.",
            "formula": "Pi_PPN[T_extra_even]=0 or keep Delta_PPN[T_extra]",
            "current_status": "RETAINED_DEBT_Y6",
            "if_closed": "Y6 no longer blocks local-GR branch",
            "if_open": "retain T_extra residual vector and xi/zeta/beta rows",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def exchange_doublet_parentization_rows() -> List[dict]:
    return [
        {
            "step_id": "ED4095_0_parent_doublet",
            "statement": "Introduce paired parent representatives for each local residual channel rather than asserting Yloc -> -Yloc by hand.",
            "formula": "R_+^A,R_-^A; E(R_+^A)=R_-^A",
            "result": "odd residual is structurally available",
            "status": "BEST_DERIVATION_ROUTE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "step_id": "ED4095_1_even_observable_sector",
            "statement": "Observable rods, clocks and matter read out only exchange-even quotient data.",
            "formula": "O_obs=O_obs[(R_+^A+R_-^A)/2]",
            "result": "matter neutrality would be derived if parent-signed",
            "status": "UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "step_id": "ED4095_2_odd_residual_no_source",
            "statement": "An exact exchange-even parent action has no term linear in the odd residual around Z=0.",
            "formula": "S[Z]=S[-Z]; S_Z=S_0+1/2 <Z,MZ>+O(Z^4); no <J,Z>",
            "result": "J_Z=0",
            "status": "CONDITIONAL_THEOREM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "step_id": "ED4095_3_boundary_silence",
            "statement": "The same exchange rule must hold for the boundary/local projection data.",
            "formula": "delta S_boundary/dZ|_{Z=0}=B_Z=0",
            "result": "no boundary-driven local residual",
            "status": "UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "step_id": "ED4095_4_component_map",
            "statement": "The parent odd residual must be the actual residual being used by the R11 double-zero theorem.",
            "formula": "Z^A=Y_loc^A+O(PPN^n beyond scored gate)",
            "result": "Yloc zero would become physical rather than auxiliary",
            "status": "MAIN_OPEN_PROOF",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "step_id": "ED4095_5_double_zero_activation",
            "statement": "If all exchange gates close, positivity gives Yloc=0 and activates the 4094 Sigma_loc double-zero R11 selector.",
            "formula": "J_Z=B_Z=0; M>0; Z=Yloc => Sigma_loc=0=delta Sigma_loc",
            "result": "nonprojector R11 can be silenced only conditionally",
            "status": "CONDITIONAL_UNLOCK_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def yloc_component_verdict_rows() -> List[dict]:
    return [
        {
            "component_id": "Y0_trace_expansion",
            "best_exchange_map": "antisymmetric trace-load doublet",
            "verdict": "NOT_DERIVED",
            "why": "matter trace can be exchange-even and still source scalar geometry",
            "theorem_or_bound_need": "derive trace-load odd neutrality or retain trace source-current closure",
            "fallback_contract": "trace_load_source_current_row",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y1_coherent_projector",
            "best_exchange_map": "antisymmetric coherent-projector representative",
            "verdict": "NOT_DERIVED",
            "why": "projector ownership/topological stress map is incomplete",
            "theorem_or_bound_need": "derive projector stress as exchange-odd or keep retained projector stress ledger",
            "fallback_contract": "projector_stress_residual_vector",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y2_boundary_flux",
            "best_exchange_map": "exchange-odd boundary current class",
            "verdict": "CONDITIONAL_PROMISING",
            "why": "boundary flux is a natural odd-charge candidate, but zero odd boundary charge is not proved",
            "theorem_or_bound_need": "prove compact local no-odd-flux theorem",
            "fallback_contract": "W_boundary_alpha3*epsilon_boundary_flux",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y3_domain_vector",
            "best_exchange_map": "exchange-odd domain vector representative",
            "verdict": "CONDITIONAL_BEST",
            "why": "domain vector/preferred-frame rows are the cleanest match to exchange-odd residuals",
            "theorem_or_bound_need": "parent-derive local scalar-zero/topological selector and exact domain-vector oddness",
            "fallback_contract": "W_domain_alpha1/alpha2/alpha3 * epsilon_domain_vector",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y4_domain_STF_stress",
            "best_exchange_map": "antisymmetric STF projector stress",
            "verdict": "NOT_DERIVED",
            "why": "tidal STF source and even conserved stress remain legal",
            "theorem_or_bound_need": "derive STF stress as odd/no-charged or retain xi bound product",
            "fallback_contract": "W_domain_xi*epsilon_domain_anisotropy",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y5_source_normalization",
            "best_exchange_map": "antisymmetric source-normalization offset after even/odd split",
            "verdict": "FAILED_CURRENT",
            "why": "measured GM/source normalization is an observed even scalar unless a deeper split is derived",
            "theorem_or_bound_need": "prove even source-normalization invisibility or fill c_domain_source_normalization_operator",
            "fallback_contract": "c_domain_source_normalization_operator",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "component_id": "Y6_stress_Bianchi",
            "best_exchange_map": "no direct odd map; divergence/stress ledger",
            "verdict": "RETAINED_DEBT",
            "why": "Bianchi-owned extra stress can be exchange-even and nonzero",
            "theorem_or_bound_need": "derive topological invisibility or keep stress residual vector through PPN",
            "fallback_contract": "T_extra_residual_vector",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def source_current_bound_contract_rows() -> List[dict]:
    return [
        {
            "bound_id": "SC4095_0_boundary_alpha3",
            "residual": "boundary odd/even flux if no-flux theorem fails",
            "symbolic_prediction": "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_flux",
            "required_bound": "abs(alpha3_boundary) <= 4e-20",
            "arena": "local PPN / pulsar preferred-frame alpha3",
            "source_path_needed": "preferred-frame alpha3 bound source plus parent W_boundary projection",
            "status": "SOURCE_CURRENT_BOUND_CONTRACT_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SC4095_1_domain_vector_alpha1",
            "residual": "domain vector preferred-frame current",
            "symbolic_prediction": "alpha1_domain = W_domain_alpha1 * epsilon_domain_vector",
            "required_bound": "abs(alpha1_domain) <= 4e-5",
            "arena": "solar-system/binary preferred-frame alpha1",
            "source_path_needed": "preferred-frame alpha1 bound source plus parent W_domain projection",
            "status": "SOURCE_CURRENT_BOUND_CONTRACT_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SC4095_2_domain_vector_alpha2",
            "residual": "domain vector anisotropic-frame current",
            "symbolic_prediction": "alpha2_domain = W_domain_alpha2 * epsilon_domain_vector",
            "required_bound": "abs(alpha2_domain) <= 2e-9",
            "arena": "spin/precession preferred-frame alpha2",
            "source_path_needed": "preferred-frame alpha2 bound source plus parent W_domain projection",
            "status": "SOURCE_CURRENT_BOUND_CONTRACT_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SC4095_3_domain_vector_alpha3",
            "residual": "domain vector self-acceleration/current nonconservation",
            "symbolic_prediction": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "required_bound": "abs(alpha3_domain) <= 4e-20",
            "arena": "pulsar/self-acceleration alpha3",
            "source_path_needed": "preferred-frame alpha3 bound source plus parent W_domain projection",
            "status": "SOURCE_CURRENT_BOUND_CONTRACT_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SC4095_4_domain_STF_xi",
            "residual": "domain STF anisotropy / Whitehead-style current",
            "symbolic_prediction": "xi_domain = W_domain_xi * epsilon_domain_anisotropy",
            "required_bound": "abs(xi_domain) <= 4e-9",
            "arena": "preferred-location / local anisotropy xi",
            "source_path_needed": "xi preferred-location bound source plus parent STF projection",
            "status": "SOURCE_CURRENT_BOUND_CONTRACT_ONLY",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SC4095_5_source_normalization",
            "residual": "even source-normalization/radial/source hair",
            "symbolic_prediction": "Delta_mu_source = c_domain_source_normalization_operator + mu_odd",
            "required_bound": "parent coefficient map plus radial/boundary/species/time-drift source constraints",
            "arena": "R11 source normalization / Newtonian source / zeta-beta-Gdot",
            "source_path_needed": "MTS parent coefficient map and external source-normalization constraints",
            "status": "HARD_ROW_NO_NUMERIC_CLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SC4095_6_even_extra_stress",
            "residual": "exchange-even Bianchi/stress residual",
            "symbolic_prediction": "Delta_PPN = Pi_PPN[T_extra_even]",
            "required_bound": "gamma/beta/zeta/xi residual vector coefficients",
            "arena": "local PPN and conservation laws",
            "source_path_needed": "parent stress projection and PPN residual map",
            "status": "HARD_ROW_NO_NUMERIC_CLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def r11_impact_update_rows() -> List[dict]:
    return [
        {
            "impact_id": "R11I4095_0_if_exchange_closes",
            "condition": "exact exchange symmetry + even matter readout + zero odd boundary charge + component identity + positivity",
            "impact_on_4094": "Yloc=0 becomes parent-owned, so Sigma_loc=0 and delta Sigma_loc=0",
            "r11_status": "double-zero selector can activate for any R11 family multiplied by Sigma_loc",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "R11I4095_1_current_state",
            "condition": "component map and Y5/Y6 even rows unsigned",
            "impact_on_4094": "4094 double-zero theorem remains conditional",
            "r11_status": "nonprojector R11 remains theorem-or-bound branch",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "impact_id": "R11I4095_2_best_next_push",
            "condition": "attack the component map rather than making more ledgers",
            "impact_on_4094": "Y2/Y3 are plausible; Y5/Y6 decide whether local branch can derive GR or must carry closure coefficients",
            "r11_status": "next target must derive exchange component map or even-source split",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_gate_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4095_0_route",
            "decision": "select exchange-doublet parentization as the best no-linear-source derivation route",
            "meaning": "This is the least-cheaty route because oddness lives in parent variables, not in an imposed plateau axiom.",
            "result": "proceed to component-map proof, especially Y5/Y6",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4095_1_not_enough",
            "decision": "do not claim Yloc=0 from the current corpus",
            "meaning": "Exact exchange symmetry, matter evenness, boundary odd-charge zero, component identity and even-source accounting are not all signed.",
            "result": "local-GR/R11/gamma-beta remains conditional",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4095_2_fallback",
            "decision": "write source-current bound contract for every row exchange does not kill",
            "meaning": "If derivation fails, the work does not collapse; it becomes a coefficient-bound branch with explicit targets.",
            "result": "alpha3/alpha1/alpha2/xi/source-normalization/stress contracts created",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4095_0_exchange_route",
            "claim": "exchange-doublet parentization is the best current route to forbidding linear Yloc sources",
            "allowed": "True",
            "reason": "It structurally explains oddness and addresses the lock/Z2 triangle better than naive reflection.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4095_1_no_linear_source",
            "claim": "the current parent action forbids all Yloc linear source and boundary terms",
            "allowed": "False",
            "reason": "exact exchange, matter readout, boundary odd-charge and component identity are not parent-signed.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4095_2_Yloc_zero",
            "claim": "Yloc=0 is derived",
            "allowed": "False",
            "reason": "positive operator is conditional and source/boundary/component-map gates remain open.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4095_3_local_GR_R11",
            "claim": "local GR, gamma=beta=1 or nonprojector R11 silence is proved",
            "allowed": "False",
            "reason": "4095 advances the mechanism but does not close Y5 source-normalization or Y6 stress/Bianchi rows.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4095_4_bound_pass",
            "claim": "source-current fallback rows pass PPN bounds",
            "allowed": "False",
            "reason": "fallback rows are symbolic contracts; parent projection coefficients and external bound source files are not filled here.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4095_0",
            "next_target": "4096-Y5-R2FR-exchange-doublet-component-map-or-even-source-normalization-split.md",
            "script": "scripts/Y5_R2FR_4096_exchange_doublet_component_map_or_even_source_normalization_split.py",
            "why": "4095 selects the exchange-doublet route. The next leap is to prove Z^A=Y_loc^A component by component, or split Y5/Y6 into theorem-zero and bound-retained pieces.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4095_1",
            "next_target": "source_current_bound_coefficients_if_Y5_Y6_fail",
            "script": "defer_until_4096_component_map_attempt",
            "why": "If Y5 source normalization and Y6 even stress cannot be derived, immediately fill coefficient-bound rows rather than circling.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4095",
            "decision": DECISION,
            "best_derivation_route": "exchange_doublet_parentization",
            "Yloc_zero_public": "False",
            "R11_silence_public": "False",
            "local_GR_public": "False",
            "hard_rows": "Y5_source_normalization;Y6_stress_Bianchi;boundary_odd_charge;component_identity",
            "next_required_gate": "exchange_doublet_component_map_or_even_source_normalization_split",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4095 - Yloc No-Linear-Source Symmetry Or Source-Current Bound",
                "",
                "## Purpose",
                "",
                "4094 reduced the nonprojector `R11` obstruction to a sharp local question: can the parent theory prove `Y_loc=0`, rather than assuming a local-vacuum plateau? 4095 attacks the hardest part of that proof: forbidding the linear source and boundary terms that would drive `Y_loc` away from zero.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public `Y_loc=0` claim: `false`",
                "- Public local-GR/R11/gamma-beta claim: `false`",
                "",
                "## The Forward Route",
                "",
                "The best route is not a bare `Y_loc -> -Y_loc` rule. The cleaner route is exchange-doublet parentization:",
                "",
                "```text",
                "R_+^A <-> R_-^A",
                "Z^A = (R_+^A - R_-^A)/2",
                "R_even^A = (R_+^A + R_-^A)/2",
                "S[Z] = S[-Z]  =>  J_Z = 0",
                "B_Z = 0, M_AB > 0, Z^A = Y_loc^A  =>  Y_loc^A = 0",
                "```",
                "",
                "This is a real derivation target: if the parent action owns the doublets, matter sees only the even quotient, the boundary has no odd charge, and `Z^A` is the physical local residual, then the 4094 `Sigma_loc` double-zero mechanism activates.",
                "",
                "## What Actually Improved",
                "",
                "- The local branch now has a specific mechanism to chase, not a vague plateau axiom.",
                "- `Y2` boundary flux and `Y3` domain vector look like plausible exchange-odd rows.",
                "- `Y5` source normalization and `Y6` stress/Bianchi are the hard test: they are not naturally killed by oddness because even measured-GM/source/stress pieces can survive.",
                "- A fallback source-current bound contract now exists, so a failed derivation turns into coefficient targets rather than hand-waving.",
                "",
                "## No Claim Yet",
                "",
                "This checkpoint does not prove local GR. It advances the proof path and blocks overclaiming. The unsigned clauses are exact exchange, even matter readout, zero odd boundary charge, the component identity `Z^A=Y_loc^A`, and even-source/stress accounting.",
                "",
                "## Next Target",
                "",
                "`4096-Y5-R2FR-exchange-doublet-component-map-or-even-source-normalization-split.md` should try to prove the component map directly. If `Y5` and `Y6` do not derive, they must become explicit bound/closure rows immediately rather than another long loop.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4095_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4095_NO_LINEAR_SOURCE_GATE.csv`",
                "- `P8_Y5_R2FR_4095_EXCHANGE_DOUBLET_PARENTIZATION.csv`",
                "- `P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT.csv`",
                "- `P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT.csv`",
                "- `P8_Y5_R2FR_4095_R11_IMPACT_UPDATE.csv`",
                "- `P8_Y5_R2FR_4095_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4095_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4095_NEXT_TARGET.csv`",
                "- `P8_Y5_R2FR_4095_STATUS.csv`",
                "- `P8_Y5_BRR545_4095_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4095_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4095_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4095_NO_LINEAR_SOURCE_GATE": SOURCE_DIR / "P8_Y5_R2FR_4095_NO_LINEAR_SOURCE_GATE.csv",
        "P8_Y5_R2FR_4095_EXCHANGE_DOUBLET_PARENTIZATION": SOURCE_DIR / "P8_Y5_R2FR_4095_EXCHANGE_DOUBLET_PARENTIZATION.csv",
        "P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT": SOURCE_DIR / "P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT.csv",
        "P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT.csv",
        "P8_Y5_R2FR_4095_R11_IMPACT_UPDATE": SOURCE_DIR / "P8_Y5_R2FR_4095_R11_IMPACT_UPDATE.csv",
        "P8_Y5_R2FR_4095_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4095_DECISION_GATE.csv",
        "P8_Y5_R2FR_4095_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4095_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4095_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4095_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4095_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4095_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4095_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_NO_LINEAR_SOURCE_GATE"], no_linear_source_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_EXCHANGE_DOUBLET_PARENTIZATION"], exchange_doublet_parentization_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT"], yloc_component_verdict_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT"], source_current_bound_contract_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_R11_IMPACT_UPDATE"], r11_impact_update_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4095_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4095_SRC_{source_id}",
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
                "check_id": f"VAL4095_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    gate = parse_csv(outputs["P8_Y5_R2FR_4095_NO_LINEAR_SOURCE_GATE"])
    gate_text = "\n".join(str(row) for row in gate)
    gate_ok = all(
        needle in gate_text
        for needle in [
            "R_+^A",
            "R_-^A",
            "J_Z=0",
            "B_Z=0",
            "Z^A=Y_loc^A",
            "source-normalization",
            "T_extra",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4095_NO_LINEAR_GATE",
            "check": "no-linear-source gate contains exchange, source, boundary, component and hard even rows",
            "passed": bool_string(gate_ok),
            "detail": "requires exchange doublets, J_Z, B_Z, Z=Yloc, Y5 and Y6 hard rows",
            "timestamp_utc": TIMESTAMP,
        }
    )

    exchange = parse_csv(outputs["P8_Y5_R2FR_4095_EXCHANGE_DOUBLET_PARENTIZATION"])
    exchange_text = "\n".join(str(row) for row in exchange)
    exchange_ok = all(needle in exchange_text for needle in ["R_+^A", "S[Z]=S[-Z]", "M>0", "Sigma_loc"])
    rows.append(
        {
            "check_id": "VAL4095_EXCHANGE_THEOREM",
            "check": "exchange-doublet theorem route is explicit and conditional",
            "passed": bool_string(exchange_ok),
            "detail": "requires doublet, even action, positivity and Sigma_loc activation",
            "timestamp_utc": TIMESTAMP,
        }
    )

    components = parse_csv(outputs["P8_Y5_R2FR_4095_YLOC_COMPONENT_VERDICT"])
    component_text = "\n".join(str(row) for row in components)
    component_ok = all(f"Y{i}_" in component_text for i in range(7))
    hard_rows_ok = all(needle in component_text for needle in ["FAILED_CURRENT", "RETAINED_DEBT", "CONDITIONAL_BEST"])
    rows.append(
        {
            "check_id": "VAL4095_COMPONENT_COVERAGE",
            "check": "component verdict covers Y0-Y6 and identifies hard rows",
            "passed": bool_string(component_ok and hard_rows_ok),
            "detail": f"component_rows={len(components)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4095_SOURCE_CURRENT_BOUND_CONTRACT"])
    bound_text = "\n".join(str(row) for row in bounds)
    bound_ok = all(needle in bound_text for needle in ["4e-20", "4e-5", "2e-9", "4e-9", "c_domain_source_normalization_operator"])
    rows.append(
        {
            "check_id": "VAL4095_BOUND_CONTRACT",
            "check": "source-current fallback contract records alpha and xi bound targets plus source-normalization hard row",
            "passed": bool_string(bound_ok),
            "detail": "requires alpha3, alpha1, alpha2, xi and source-normalization contracts",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claims = parse_csv(outputs["P8_Y5_R2FR_4095_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    rows.append(
        {
            "check_id": "VAL4095_NO_PUBLIC_CLAIM",
            "check": "4095 does not promote Yloc zero, local GR, R11 silence or bound pass",
            "passed": bool_string(no_public),
            "detail": "all claim rows remain private/nonclaim",
            "timestamp_utc": TIMESTAMP,
        }
    )

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4095_NEXT_TARGET"])
    next_text = "\n".join(str(row) for row in next_rows)
    next_ok = "4096-Y5-R2FR-exchange-doublet-component-map-or-even-source-normalization-split.md" in next_text
    rows.append(
        {
            "check_id": "VAL4095_NEXT_TARGET",
            "check": "next target is component-map/even-source split rather than another source sweep",
            "passed": bool_string(next_ok),
            "detail": "requires 4096 next target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4095_SCOPE",
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
            "check_id": "VAL4095_SCRIPT_COMPILES",
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
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4095_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4095 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()
