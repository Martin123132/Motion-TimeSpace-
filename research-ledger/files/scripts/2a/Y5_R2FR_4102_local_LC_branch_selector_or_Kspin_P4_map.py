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
DOC_PATH = ROOT / "4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_LC_SELECTOR_REANCHOR_4102"
CHECKPOINT_ID = "4102"
DECISION = (
    "BLC_SELECTOR_REDUCED_TO_NO_VERTICAL_AFFINE_SLOT_PLUS_PRODUCT_GATE_"
    "PROJECTOR_GAMMA_CLOSED_POYNTING_FLUX_RETAINED"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4102_00_4101_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4101_NEXT_TARGET.csv",
        "4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md",
        "4101 selects the local LC branch selector or Kspin/P4 map as next target.",
    ),
    "SRC4102_01_4101_connection": (
        SOURCE_DIR / "P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM.csv",
        "CFT4101_5_selector_gap",
        "4101 sharpens the missing gate to B_LC_selector.",
    ),
    "SRC4102_02_4101_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE.csv",
        "LCS4101_0_configuration",
        "4101 re-anchors the local LC/no-independent-affine branch signature.",
    ),
    "SRC4102_03_3571_selector": (
        SOURCE_DIR / "P8_Y5_R2FR_3571_BLC_SELECTOR_THEOREM.csv",
        "BLC3571_0_exact_product_gate",
        "3571 derives the finite product selector gate.",
    ),
    "SRC4102_04_3571_matrix": (
        SOURCE_DIR / "P8_Y5_R2FR_3571_BLC_SECTOR_PRODUCT_MATRIX.csv",
        "SELP3571_9_total",
        "3571 sector product matrix lists public/private selector factors.",
    ),
    "SRC4102_05_3572_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        "PN3572_6_result",
        "3572 closes the Gamma projector commutator inside the q/e_obs/tau-natural branch.",
    ),
    "SRC4102_06_3568_coercivity": (
        SOURCE_DIR / "P8_Y5_R2FR_3568_MC_COERCIVITY_CERTIFICATE.csv",
        "COER3568_3_lambda_formula",
        "3568 gives the symbolic lambda_C coercivity formula for affine fallback.",
    ),
    "SRC4102_07_3568_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3568_LAMBDAC_KSPIN_BOUND_ROWS.csv",
        "LAMB3568_4_master_bound",
        "3568 stages the master K_spin/lambda_C fallback bound.",
    ),
    "SRC4102_08_3570_axial": (
        SOURCE_DIR / "P8_Y5_R2FR_3570_PARENT_AXIAL_ZERO_CERTIFICATE.csv",
        "AZC3570_7_total",
        "3570 records axial zero inside the selected LC branch.",
    ),
    "SRC4102_09_3576_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_3576_CANDIDATE_PARENT_BRANCH_ADOPTION_PACKET.csv",
        "ADOPT3576_6_no_extra_mass",
        "3576 candidate branch keeps extra mass/Poynting/source-coordinate residuals explicit.",
    ),
    "SRC4102_10_3579_poynting": (
        SOURCE_DIR / "P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv",
        "PEM3579_2_poynting_flux_identity",
        "3579 derives the public EM/Poynting no-flux branch conditions.",
    ),
    "SRC4102_11_3579_conditions": (
        SOURCE_DIR / "P8_Y5_R2FR_3579_NO_FLUX_CONDITIONS.csv",
        "NFC3579_3_no_radiative_boundary_flux",
        "3579 lists no-radiation/current-crossing/surface-gauge clauses.",
    ),
    "SRC4102_12_2416_spine": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_2416_PARENT_ACTION_SIGNATURE_SPINE.csv",
        "PAS2416_0_domain",
        "2416 parent ordinary action spine excludes Gamma_ind in the private candidate branch.",
    ),
    "SRC4102_13_3506_em": (
        SOURCE_DIR / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv",
        "GEN3506_1_no_extra_tensor_domain",
        "3506 visible EM action domain caps hidden constitutive/affine slots.",
    ),
    "SRC4102_14_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4102_local_LC_branch_selector_or_Kspin_P4_map.py",
        "Reproducible generator for this 4102 checkpoint.",
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


def row_base() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                **row_base(),
                "source_id": source_id,
                "source_type": "local_checkpoint_or_generator",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "contains_needle": bool_string(path.exists() and needle in read_text(path)),
                "valid_for_claim": "False",
            }
        )
    return rows


def selector_theorem_rows() -> List[dict]:
    rows = [
        (
            "SEL4102_0_no_vertical_affine_slot",
            "NoAffineGenerator structural selector",
            "If compact local MTS has only quotient-visible fields {q(Phi), e_obs(q), g_obs(e_obs), Psi_A, A_Q, theta_A(q), tau(q), H_ref, Pi_M(q,e_obs,tau)} and no independent C/Gamma_ind/omega_ind generator, then the local connection is the Levi-Civita natural connection of g_obs.",
            "The only connection naturally determined by a nondegenerate observed metric/coframe with torsion-free, metric-compatible transport is Gamma_LC[g_obs]. Any nonzero distortion C=Gamma-Gamma_LC is a tensorial extra field or residual, not a consequence of the quotient geometry alone.",
            "NoAffineGenerator; quotient naturality; no hidden background tensor; no representative-dependent affine readout",
            "CONDITIONAL_STRUCTURAL_SELECTOR_THEOREM",
            "turns the selector from a taste into a field-inventory theorem, provided the parent field inventory is signed",
            "SRC4102_02_4101_signature",
        ),
        (
            "SEL4102_1_exact_product_gate",
            "finite no-smuggling product gate",
            "B_LC_selector = product_s I_s, where I_s=1 only when sector s has no Gamma_ind/omega_ind action slot and no downstream source-current reentry.",
            "This is a no-cancellation rule: one live affine/source/boundary/readout leak keeps the public selector from being one.",
            "sectorwise domain exhaustion or explicit bound row for every active sector",
            "DERIVED_PRODUCT_GATE_REANCHORED",
            "makes public LC selection a finite checklist rather than an undefined coupling argument",
            "SRC4102_03_3571_selector",
        ),
        (
            "SEL4102_2_projector_gamma_closed",
            "projector Gamma commutator closure",
            "Inside the q/e_obs/tau-natural LC branch, delta_Gamma_ind Pi_M=0 and delta_Gamma(Pi_M J_H)=0.",
            "3572 applies the chain rule: Pi_M has no Gamma_ind argument when it descends through q,e_obs,tau,H_ref/topology; 3566 gives delta_Gamma J_H=0 inside the branch.",
            "Pi_M=Pi_bar(q,e_obs,tau,H_ref,topology); no Gamma collar transport",
            "PRIVATE_BRANCH_SUBGATE_CLOSED",
            "removes projector Gamma commutator as the current spin/source-hypermomentum bottleneck",
            "SRC4102_05_3572_projector",
        ),
        (
            "SEL4102_3_EM_Poynting_owner",
            "Poynting belongs to public Hilbert/H_tau flux, not affine torsion source",
            "A_Q,F_Q,*_obs(e_obs) have no affine Gamma slot; Poynting energy enters the public matter+EM Hilbert current or an explicit boundary-flux residual.",
            "3579 gives d_t U_EM + int_boundary S_Poynting dot n = -int J dot E, so stationary no-radiation/no-current-crossing exteriors can set the public EM flux component to zero; otherwise the flux is retained.",
            "same observed Hodge/current owner; no radiative boundary flux; no current crossing; fixed EM gauge surface",
            "PUBLIC_EM_FLUX_BRANCH_SHARPENED",
            "keeps the user's Poynting-vector instinct in the derivation rather than sweeping it under the rug",
            "SRC4102_10_3579_poynting",
        ),
        (
            "SEL4102_4_distortion_fallback",
            "dynamic affine fallback",
            "If C is retained, M_C C = Delta_Gamma - B_C - P_C - N_C(C) and lambda_C = min_i a_i(1-eta_i) controls the zero theorem or the K_spin/lambda_C bound.",
            "3568 decomposes torsion/nonmetricity/projective modes and derives the diagonal-dominance sign certificate. Missing parent signs make this a fallback, not a claim.",
            "a_i and eta_ij signed; source/boundary/projective/nonlinear numerator bounded",
            "EXECUTABLE_SYMBOLIC_P4_ROUTE",
            "prevents fake closure: if NoAffineGenerator fails, local tests must see K_spin/lambda_C rows",
            "SRC4102_06_3568_coercivity",
        ),
        (
            "SEL4102_5_public_verdict",
            "4102 public selector verdict",
            "The best current route is structural: prove NoAffineGenerator and the product gate. Public B_LC_selector is still not one because boundary/H_ref/M_H, Poynting exterior clauses, clock/light/orbit readout, alpha/lambda_A, GM calibration and PPN gates remain live.",
            "4102 imports the strongest old rungs into the 4101 chain: projector Gamma is closed privately, EM/Poynting is correctly owned, and affine fallback has lambda_C/K_spin form.",
            "parent-owned NoAffineGenerator plus all product factors or source-backed residual bounds",
            "SELECTOR_ADVANCED_PUBLIC_CLAIM_BLOCKED",
            "next target should attack the largest live product leak: local exterior/H_ref/Poynting flux/source-surface certificate",
            "SRC4102_04_3571_matrix",
        ),
    ]
    return [
        {
            **row_base(),
            "selector_id": selector_id,
            "name": name,
            "statement": statement,
            "derivation": derivation,
            "required_premises": premises,
            "status": status,
            "effect": effect,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for selector_id, name, statement, derivation, premises, status, effect, source_key in rows
    ]


def no_vertical_affine_slot_rows() -> List[dict]:
    rows = [
        (
            "NVAS4102_0_field_inventory",
            "field inventory",
            "Conf_loc contains q(Phi), e_obs(q), g_obs(e_obs), Psi_A, A_Q, theta_A(q), tau(q), H_ref and q/e_obs/tau-natural projectors; it does not contain C, Gamma_ind or omega_ind.",
            "This is exactly the 4101/3566 LC branch field list.",
            "PRIVATE_BRANCH_AVAILABLE_PUBLIC_PARENT_INVENTORY_UNSIGNED",
            "SRC4102_02_4101_signature",
        ),
        (
            "NVAS4102_1_unique_natural_connection",
            "Levi-Civita naturality",
            "Given g_obs/e_obs and the torsion-free metric-compatible transport requirement, Gamma_LC[g_obs] is the unique natural connection in the local branch.",
            "The branch can use Gamma_LC as a derived object because it is constructed from g_obs, not introduced as an independent source-coupled field.",
            "EXACT_STANDARD_GEOMETRIC_STEP_INSIDE_BRANCH",
            "SRC4102_02_4101_signature",
        ),
        (
            "NVAS4102_2_distortion_requires_generator",
            "distortion tensor slot",
            "C=Gamma-Gamma_LC is tensorial. A nonzero C needs an independent tensorial generator, hidden background, representative-dependent map, or dynamical affine action.",
            "If none of those are in the parent field list, C cannot be nonzero without adding a new field beyond motion/time/space observed geometry.",
            "NO_AFFINE_GENERATOR_CONDITION_EXPLICIT",
            "SRC4102_01_4101_connection",
        ),
        (
            "NVAS4102_3_EM_not_affine_generator",
            "EM/Poynting separation",
            "Public EM supplies Hilbert stress and boundary flux through A_Q,F_Q,*_obs(e_obs); it is not an independent affine distortion generator inside the LC branch.",
            "The Poynting vector remains physically active in H_tau/source flux; it just does not re-enter as Gamma_ind hypermomentum unless an affine EM coupling is explicitly added.",
            "POYNTING_OWNED_NOT_IGNORED",
            "SRC4102_10_3579_poynting",
        ),
        (
            "NVAS4102_4_counterbranch_guard",
            "counterbranch guard",
            "If flow/hidden structure does generate an affine distortion, it must appear as C with M_C/lambda_C/K_spin or explicit c_A,c_T,c_Q coefficients.",
            "This prevents the selector theorem from becoming a closure assumption: a failed NoAffineGenerator proof automatically activates the P4 route.",
            "AFFINE_COUNTERBRANCH_RETAINED",
            "SRC4102_07_3568_bounds",
        ),
        (
            "NVAS4102_5_result",
            "selector result",
            "B_LC_selector=1 is derived only for the signed NoAffineGenerator product branch. Current corpus has the branch and several subgate proofs, but not the global public signature.",
            "Therefore 4102 is a real derivation step but still nonclaim.",
            "CONDITIONAL_SELECTOR_NOT_PUBLIC_CLAIM",
            "SRC4102_03_3571_selector",
        ),
    ]
    return [
        {
            **row_base(),
            "slot_id": slot_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "parent_signed_public": "False",
            "valid_for_claim": "False",
        }
        for slot_id, claim_piece, statement, derivation, status, source_key in rows
    ]


def sector_indicator_rows() -> List[dict]:
    rows = [
        ("SEC4102_0_matter", "ordinary matter", "I_matter", "S_m[Psi,e_obs,omega_LC[e_obs],A_Q,theta] has no Gamma_ind", "PRIVATE_PASS", "parent/global ordinary-branch selector unsigned", "SRC4102_12_2416_spine"),
        ("SEC4102_1_spin", "spin transport", "I_spin", "omega_spin=omega_LC[e_obs] and no torsionful omega_ind", "PRIVATE_PASS", "metric-affine spin counterbranch not globally excluded", "SRC4102_12_2416_spine"),
        ("SEC4102_2_EM", "EM and Poynting", "I_EM", "A_Q,F_Q,*_obs(e_obs) with Poynting in Hilbert/H_tau or flux residual", "PARTIAL_PASS", "alpha/lambda_A and strict no-flux exterior clauses open", "SRC4102_13_3506_em"),
        ("SEC4102_3_source", "source worldtube/current", "I_source", "J_H[tau] from e_obs Hilbert variation and regular support", "PRIVATE_PASS_CONDITIONAL", "H_ref/M_H, source-owner and finite boundary support open", "SRC4102_02_4101_signature"),
        ("SEC4102_4_projector_gamma", "projector Gamma commutator", "I_projector_Gamma", "Pi_M q/e_obs/tau-natural implies delta_Gamma Pi_M=0", "PRIVATE_SUBGATE_PASS", "metric projector stress and flux closure remain separate", "SRC4102_05_3572_projector"),
        ("SEC4102_5_boundary_href", "boundary, H_ref and M_H", "I_boundary_Href", "fixed reference and no extra boundary/source-owner flux", "OPEN_PRIMARY_LEAK", "H_ref/M_H integrability, positivity and source-blind reference not public", "SRC4102_09_3576_adoption"),
        ("SEC4102_6_poynting_exterior", "public EM/Poynting exterior", "I_Poynting", "stationary no-radiation, no current crossing and fixed EM surface gauge", "OPEN_BUT_THEOREM_BRANCH_WRITTEN", "NFC3579_2 through NFC3579_5 not parent-signed", "SRC4102_11_3579_conditions"),
        ("SEC4102_7_clock", "clock readout", "I_clock", "downstream matter/gauge/e_obs clock standards", "OPEN_READOUT_GATE", "clock protocol argument list and alpha response not parent-signed", "SRC4102_04_3571_matrix"),
        ("SEC4102_8_light", "light/optical readout", "I_light", "metric/public-Hodge ray/detector readout", "OPEN_READOUT_GATE", "detector/ray downstream proof and hidden Hodge guards open", "SRC4102_04_3571_matrix"),
        ("SEC4102_9_orbit_GM", "orbit and measured GM transfer", "I_orbit * I_GM", "metric geodesic and GM transfer downstream of M_H", "OPEN_NEWTON_TRANSFER_GATE", "test-body limit, measured-GM calibration and PPN beta/gamma open", "SRC4102_09_3576_adoption"),
        ("SEC4102_10_total", "total selector", "B_LC_selector", "product_s I_s", "FALSE_PUBLICLY_CURRENTLY", "one open leak keeps public selector nonclaim", "SRC4102_03_3571_selector"),
    ]
    return [
        {
            **row_base(),
            "sector_gate_id": sector_id,
            "sector": sector,
            "indicator": indicator,
            "zero_condition": zero_condition,
            "current_status": status,
            "open_gap": gap,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "private_branch_value": "1" if "PASS" in status else "open",
            "public_value": "0_or_unproven",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for sector_id, sector, indicator, zero_condition, status, gap, source_key in rows
    ]


def distortion_fallback_rows() -> List[dict]:
    rows = [
        (
            "DFB4102_0_lambdaC",
            "lambda_C",
            "lambda_C = min_i a_i(1-eta_i)",
            "operator eigenvalue / inverse length^2 after normalization",
            "SOURCE_READY_SCHEMA_NUMERIC_VALUES_MISSING",
            "a_i, eta_ij, active modes, boundary/gauge policy",
            "SRC4102_06_3568_coercivity",
        ),
        (
            "DFB4102_1_master",
            "epsilon_local_connection",
            "epsilon_local_connection <= K_spin/lambda_C * (||Delta_Gamma||+||B_C||+||P_C||+||N_C||)",
            "arena residual units",
            "EXECUTABLE_SYMBOLIC_NONCLAIM",
            "K_spin/lambda_C plus source, boundary, projective and nonlinear norms",
            "SRC4102_07_3568_bounds",
        ),
        (
            "DFB4102_2_axial",
            "epsilon_axial_torsion_spin",
            "epsilon_A <= K_A/[a_A(1-eta_A)] * (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||)",
            "spin/clock/WEP/KRT response units",
            "AXIAL_DENOMINATOR_DERIVED_SYMBOLIC_INPUTS_MISSING",
            "Z_A,m_A^2,lambda_1,eta_A,K_A,c_A and numerator norms",
            "SRC4102_08_3570_axial",
        ),
        (
            "DFB4102_3_projector_counterbranch",
            "epsilon_projector_comm",
            "epsilon_projector_comm <= K_projector_Gamma ||J_H||/abs(M_H_ref)",
            "source-current response units",
            "ZERO_INSIDE_NATURAL_BRANCH_ELSE_BOUND_READY",
            "K_projector_Gamma if Gamma-dependent projector/collar transport is admitted",
            "SRC4102_05_3572_projector",
        ),
        (
            "DFB4102_4_poynting_flux",
            "Phi_EM_rad + W_public_exchange + C_EM_surface_gauge",
            "replace I_matter_EM_flux by explicit EM radiation/work/surface-corner flux rows if no-flux clauses fail",
            "H_tau curl / source mass flux units",
            "BOUND_ROWS_READY_INPUTS_MISSING",
            "radiative boundary flux, current-crossing integral, EM gauge corner term",
            "SRC4102_11_3579_conditions",
        ),
        (
            "DFB4102_5_no_cancellation",
            "epsilon_selector_leak",
            "absolute sum of open selector leaks unless parent signs cancellation",
            "dimensionless or arena-declared residual units",
            "ACTIVE_GUARD",
            "forbid cancellation between boundary, Poynting, readout, alpha and affine tails",
            "SRC4102_04_3571_matrix",
        ),
    ]
    return [
        {
            **row_base(),
            "fallback_id": fallback_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "required_inputs": required,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "source_backed_numeric": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for fallback_id, symbol, formula, units, status, required, source_key in rows
    ]


def live_leakage_rows() -> List[dict]:
    rows = [
        ("LEAK4102_0_Href_MH", "H_ref/M_H reference lock", "epsilon_Href_lock", "H_ref fixed/source-blind, H_tau integrable and M_H positive", "derive reference lock or retain Href residual", "SRC4102_09_3576_adoption"),
        ("LEAK4102_1_boundary_source_owner", "boundary/source-owner flux", "epsilon_boundary_flux", "no extra GHY/domain/worldtube flux outside Hilbert source", "derive zero compact boundary work or source bound", "SRC4102_09_3576_adoption"),
        ("LEAK4102_2_Poynting_radiation", "Poynting/radiation exterior", "Phi_EM_rad", "no net radiative EM flux through linking boundary", "derive local exterior no-radiation certificate or fill flux row", "SRC4102_11_3579_conditions"),
        ("LEAK4102_3_current_crossing", "charged current crossing surface", "W_public_exchange", "no public charge/current crosses the source linking surface", "derive worldtube containment or bound J dot E work", "SRC4102_11_3579_conditions"),
        ("LEAK4102_4_EM_surface_gauge", "EM surface gauge/corner", "C_EM_surface_gauge", "fixed EM gauge representative on linking surface or exact improvement only", "derive gauge-surface rule or bound corner term", "SRC4102_11_3579_conditions"),
        ("LEAK4102_5_alpha_lambda", "EM alpha/lambda owner", "D_X ln(lambda_A)", "lambda_A constant/universal or bounded response to MTS fields", "derive alpha owner separately from affine selector", "SRC4102_13_3506_em"),
        ("LEAK4102_6_clock_light_orbit", "clock/light/orbit readout", "epsilon_readout_tail", "readouts downstream of solved public fields with no source-current reentry", "write protocol argument signatures and PPN readout kernels", "SRC4102_04_3571_matrix"),
        ("LEAK4102_7_GM_PPN", "measured GM and PPN transfer", "epsilon_GM_PPN", "M_H transfers to measured Newtonian GM and beta/gamma/preferred-frame residuals vanish or bound", "derive Newton/PPN transfer gate after source lock", "SRC4102_09_3576_adoption"),
    ]
    return [
        {
            **row_base(),
            "leak_id": leak_id,
            "leak": leak,
            "symbol": symbol,
            "zero_condition": condition,
            "next_action": action,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "status": "LIVE_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for leak_id, leak, symbol, condition, action, source_key in rows
    ]


def decision_gate_rows() -> List[dict]:
    rows = [
        (
            "DEC4102_0_selector_product",
            "accept B_LC_selector=product_s I_s as the current selector theorem",
            "this is the strongest no-smuggling form: every active sector must be zero by domain or explicitly bounded",
            "public selector is now a finite checklist, not vague coupling fog",
            "SELECTOR_GATE_CANONICAL",
            "SRC4102_03_3571_selector",
        ),
        (
            "DEC4102_1_no_vertical_affine_route",
            "promote NoAffineGenerator as the clean derivation route",
            "a nonzero C=Gamma-Gamma_LC requires an extra tensorial generator beyond q/e_obs/g_obs unless admitted as affine residual",
            "next local-GR work should try to sign the field-inventory/no-affine-generator clause, not fit torsion tiny",
            "STRUCTURAL_ROUTE_SELECTED_CONDITIONALLY",
            "SRC4102_02_4101_signature",
        ),
        (
            "DEC4102_2_projector_update",
            "treat projector Gamma commutator as privately closed in the natural branch",
            "3572 proves delta_Gamma Pi_M=0 when Pi_M descends through q/e_obs/tau/H_ref/topology",
            "projector Gamma is no longer the main selector leak; metric stress/flux/source lock remain",
            "SUBGATE_ADVANCED",
            "SRC4102_05_3572_projector",
        ),
        (
            "DEC4102_3_poynting_update",
            "keep Poynting as a public Hilbert/H_tau flux gate",
            "3579 gives a real no-flux theorem branch but not the strict local-exterior certificate",
            "Poynting is neither ignored nor made into hidden affine torsion; it is the next source-surface gate",
            "POYNTING_GATE_SHARPENED",
            "SRC4102_10_3579_poynting",
        ),
        (
            "DEC4102_4_no_public_claim",
            "do not claim local GR/Newton/PPN/R10 pass",
            "boundary/H_ref/M_H, Poynting exterior, alpha, readout and GM/PPN gates remain open",
            "continue private derivation; no GitHub/public claim from this checkpoint",
            "PUBLIC_CLAIM_BLOCKED",
            "SRC4102_04_3571_matrix",
        ),
        (
            "DEC4102_5_next",
            "attack local exterior, H_ref and Poynting source-surface certificate next",
            "that is the largest live product leak after projector Gamma closure",
            "4103 targets no-radiation/worldtube/surface/H_ref certificate or concrete flux rows",
            "NEXT_TARGET_SELECTED",
            "SRC4102_11_3579_conditions",
        ),
    ]
    return [
        {
            **row_base(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "valid_for_claim": "False",
        }
        for decision_id, decision, reason, consequence, status, source_key in rows
    ]


def claim_gate_rows() -> List[dict]:
    rows = [
        ("CLAIM4102_0_private_selector", "B_LC_selector=1 inside signed LC branch", "PRIVATE_CONDITIONAL_ONLY", "NoAffineGenerator/product gate not public parent-signed", "parent field inventory plus all sector indicators"),
        ("CLAIM4102_1_public_local_GR", "local GR/Newton recovery", "BLOCKED", "selector advanced but source/H_ref/GM/PPN gates remain open", "boundary/H_ref/M_H plus Newton/PPN transfer"),
        ("CLAIM4102_2_public_EM", "Maxwell/Poynting fully closed", "BLOCKED", "public no-flux theorem branch exists but strict exterior and alpha/lambda_A owner remain open", "no-radiation/current-crossing/gauge-surface plus alpha owner"),
        ("CLAIM4102_3_affine_fallback", "affine/torsion safe bound", "BLOCKED", "lambda_C/K_spin rows are symbolic and unsourced", "a_i, eta_ij, K_spin and numerator norms"),
    ]
    return [
        {
            **row_base(),
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "missing_gate": missing,
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for claim_id, claim, status, reason, missing in rows
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4102_0",
            "target_doc": "4103-Y5-R2FR-local-exterior-Href-Poynting-no-flux-certificate-or-flux-rows.md",
            "target_script": "scripts/Y5_R2FR_4103_local_exterior_Href_Poynting_no_flux_certificate_or_flux_rows.py",
            "objective": "derive the strict compact local exterior certificate tying H_ref/M_H, no-radiative Poynting flux, no current crossing, and fixed EM surface gauge into the same source worldtube; if not, emit concrete nonclaim flux rows",
            "success_gate": "H_ref/M_H and NFC3579_2..5 are parent-signed for the same local exterior branch, or Phi_EM_rad/W_public_exchange/C_EM_surface_gauge/Href rows are source-ready with units",
            "reason": "4102 reduces the selector to a product gate and closes projector Gamma privately; the largest live product leak is now source-surface/H_ref/Poynting exterior flux",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4102_0",
            "decision": DECISION,
            "selector_status": "product_gate_reanchored; NoAffineGenerator structural route selected conditionally; projector_Gamma private subgate closed",
            "poynting_status": "Hilbert/H_tau flux owner retained; no-flux theorem branch exists but local exterior clauses unsigned",
            "public_status": "no_local_GR_Newton_Maxwell_PPN_R10_claim",
            "next_target": "4103 local exterior/Href/Poynting no-flux certificate or flux rows",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4102_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4102_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4102_SELECTOR_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4102_SELECTOR_THEOREM.csv",
        "P8_Y5_R2FR_4102_NO_VERTICAL_AFFINE_SLOT": SOURCE_DIR / "P8_Y5_R2FR_4102_NO_VERTICAL_AFFINE_SLOT.csv",
        "P8_Y5_R2FR_4102_SECTOR_INDICATOR_MATRIX": SOURCE_DIR / "P8_Y5_R2FR_4102_SECTOR_INDICATOR_MATRIX.csv",
        "P8_Y5_R2FR_4102_DISTORTION_FALLBACK_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4102_DISTORTION_FALLBACK_ROWS.csv",
        "P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER": SOURCE_DIR / "P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER.csv",
        "P8_Y5_R2FR_4102_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4102_DECISION_GATE.csv",
        "P8_Y5_R2FR_4102_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4102_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4102_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4102_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4102_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4102_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4102 - Local LC branch selector or Kspin/P4 map",
        "",
        "## Verdict",
        "4102 takes the leap that 4101 set up: the LC/no-independent-affine route is now reduced to a concrete selector theorem, not a vibe. The clean selector is `NoAffineGenerator + B_LC_selector = product_s I_s`.",
        "",
        "Meaning: if compact local MTS contains only the quotient-visible motion/time/space geometry `q -> e_obs -> g_obs`, visible matter/EM fields, and downstream readouts, then a nonzero distortion `C=Gamma-Gamma_LC` has no natural field slot. It must either be absent, or be admitted honestly as an affine residual with `M_C`, `lambda_C`, and `K_spin` rows.",
        "",
        "This is progress, but still not a public local-GR/Newton/Maxwell claim. The projector Gamma commutator is privately closed; Poynting is correctly owned as public Hilbert/H_tau flux; the live product leaks are now boundary/H_ref/M_H, strict no-radiation/current-crossing/EM-surface clauses, alpha/lambda_A, readout protocols, GM transfer and PPN.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Selector theorem",
        "- `NoAffineGenerator`: no independent `C`, `Gamma_ind`, or `omega_ind` is present in the compact local parent field inventory.",
        "- `B_LC_selector = product_s I_s`: every active sector must exclude independent affine slots or carry an explicit residual bound.",
        "- If the selector is signed, `C=0` by field-domain/naturality rather than by fitting torsion small.",
        "- If it is not signed, the fallback is `epsilon_local_connection <= K_spin/lambda_C * residual_norm_sum`.",
        "",
        "## What moved forward",
        "- Projector Gamma: `delta_Gamma Pi_M=0` inside the q/e_obs/tau-natural branch.",
        "- EM/Poynting: Poynting stress is Hilbert/H_tau owned; no-radiation exterior clauses decide whether flux vanishes or becomes a bound row.",
        "- Affine fallback: `lambda_C=min_i a_i(1-eta_i)` and the axial denominator route are retained as executable symbolic nonclaim rows.",
        "",
        "## Not claimed",
        "- No public local GR, Newton, R10, WEP, clock, orbital, Maxwell-normalization, alpha, or PPN pass.",
        "- No numeric `K_spin`, `lambda_C`, `a_i`, `eta_i`, `K_A`, or `c_A` values are sourced here.",
        "- No cancellation between open leaks is allowed.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4102_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4102_SELECTOR_THEOREM.csv`",
        "- `P8_Y5_R2FR_4102_NO_VERTICAL_AFFINE_SLOT.csv`",
        "- `P8_Y5_R2FR_4102_SECTOR_INDICATOR_MATRIX.csv`",
        "- `P8_Y5_R2FR_4102_DISTORTION_FALLBACK_ROWS.csv`",
        "- `P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER.csv`",
        "- `P8_Y5_R2FR_4102_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4102_CLAIM_GATE.csv`",
        "- `P8_Y5_R2FR_4102_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4102_STATUS.csv`",
        "- `P8_Y5_BRR545_4102_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4103-Y5-R2FR-local-exterior-Href-Poynting-no-flux-certificate-or-flux-rows.md`",
        "- Objective: derive the same-worldtube local exterior certificate for `H_ref/M_H`, no radiative Poynting flux, no current crossing, and fixed EM surface gauge; otherwise write concrete flux rows.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4102_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_SELECTOR_THEOREM"], selector_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_NO_VERTICAL_AFFINE_SLOT"], no_vertical_affine_slot_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_SECTOR_INDICATOR_MATRIX"], sector_indicator_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_DISTORTION_FALLBACK_ROWS"], distortion_fallback_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER"], live_leakage_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4102_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **row_base(),
                "check_id": check_id,
                "check": check,
                "passed": bool_string(passed),
                "detail": detail,
                "valid_for_claim": "False",
            }
        )

    source_rows = source_register_rows()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "True"]
    missing_needles = [row["source_id"] for row in source_rows if row["contains_needle"] != "True"]
    add("VAL4102_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4102_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

    parse_counts = {}
    parse_ok = True
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[name] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_counts[name] = f"ERROR:{exc}"
            parse_ok = False
    add("VAL4102_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    selector_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4102_SELECTOR_THEOREM"]))
    selector_tokens = ["B_LC_selector", "product_s", "NoAffineGenerator", "Gamma_ind", "omega_ind", "C=Gamma-Gamma_LC", "Poynting", "lambda_C", "K_spin"]
    missing_selector = [token for token in selector_tokens if token not in selector_text]
    add("VAL4102_3_selector_tokens", "selector theorem includes product/no-affine/fallback tokens", not missing_selector, ";".join(missing_selector) or "all selector tokens present")

    slot_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4102_NO_VERTICAL_AFFINE_SLOT"]))
    slot_tokens = ["Conf_loc", "Levi-Civita", "distortion", "Poynting", "NoAffineGenerator"]
    missing_slot = [token for token in slot_tokens if token not in slot_text]
    add("VAL4102_4_no_affine_slot_tokens", "no vertical affine slot theorem has required pieces", not missing_slot, ";".join(missing_slot) or "all no-affine tokens present")

    sector_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4102_SECTOR_INDICATOR_MATRIX"]))
    sector_tokens = ["I_matter", "I_spin", "I_EM", "I_source", "I_projector", "I_boundary", "I_Poynting", "I_clock", "I_light", "I_orbit", "I_GM", "B_LC_selector"]
    missing_sector = [token for token in sector_tokens if token not in sector_text]
    add("VAL4102_5_sector_product_coverage", "sector matrix covers selector product factors", not missing_sector, ";".join(missing_sector) or "all sector tokens present")

    fallback_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4102_DISTORTION_FALLBACK_ROWS"]))
    fallback_tokens = ["lambda_C", "K_spin", "epsilon_local_connection", "epsilon_axial_torsion_spin", "Phi_EM_rad", "epsilon_selector_leak"]
    missing_fallback = [token for token in fallback_tokens if token not in fallback_text]
    add("VAL4102_6_fallback_coverage", "fallback rows cover affine and Poynting residuals", not missing_fallback, ";".join(missing_fallback) or "all fallback tokens present")

    leak_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER"]))
    leak_tokens = ["H_ref", "Poynting", "current crossing", "EM surface", "alpha", "PPN", "GM"]
    missing_leak = [token for token in leak_tokens if token not in leak_text]
    add("VAL4102_7_leakage_coverage", "live leakage ledger covers the remaining product leaks", not missing_leak, ";".join(missing_leak) or "all leakage tokens present")

    claims = parse_csv(outputs["P8_Y5_R2FR_4102_CLAIM_GATE"])
    no_public_claim = all(row.get("public_claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    add("VAL4102_8_no_public_claims", "all claim rows remain nonpublic and nonclaim", no_public_claim, f"claim_rows={len(claims)}")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4102_NEXT_TARGET"])
    next_ok = any("4103-Y5_R2FR" in row.get("target_doc", "").replace("-", "_") or "4103-Y5-R2FR-local-exterior-Href-Poynting-no-flux-certificate-or-flux-rows.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4102_9_next_target", "next target attacks local exterior/Href/Poynting flux", next_ok, str(next_rows))

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    add("VAL4102_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4102_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4102_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
