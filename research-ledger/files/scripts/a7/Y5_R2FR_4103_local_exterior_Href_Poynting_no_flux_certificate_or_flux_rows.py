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
DOC_PATH = ROOT / "4103-Y5-R2FR-local-exterior-Href-Poynting-no-flux-certificate-or-flux-rows.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_EXTERIOR_HREF_POYNTING_4103"
CHECKPOINT_ID = "4103"
DECISION = (
    "POYNTING_ANCHOR_ZERO_CARRIED_ESTAT_UNIQUENESS_ROUTE_REANCHORED_"
    "HREF_INTERNAL_LOCK_RETAINED_DENOMINATOR_AND_HOMOGENEOUS_MODE_OPEN"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4103_00_4102_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4102_NEXT_TARGET.csv",
        "4103-Y5-R2FR-local-exterior-Href-Poynting-no-flux-certificate-or-flux-rows.md",
        "4102 selects the local exterior/Href/Poynting certificate as next target.",
    ),
    "SRC4103_01_4102_leaks": (
        SOURCE_DIR / "P8_Y5_R2FR_4102_LIVE_LEAKAGE_LEDGER.csv",
        "LEAK4102_2_Poynting_radiation",
        "4102 live leakage ledger identifies H_ref/M_H and Poynting exterior as current product leaks.",
    ),
    "SRC4103_02_3580_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3580_LOCAL_EXTERIOR_CERTIFICATE_THEOREM.csv",
        "LET3580_3_zero_anchor",
        "3580 proves Poynting transport and reduces no-radiation to a zero anchor plus same-surface certificate.",
    ),
    "SRC4103_03_3580_transport": (
        SOURCE_DIR / "P8_Y5_R2FR_3580_STATIONARY_COLLAR_TRANSPORT_LAW.csv",
        "TRL3580_3_surface_transport",
        "3580 stationary collar transport law.",
    ),
    "SRC4103_04_3581_package": (
        SOURCE_DIR / "P8_Y5_R2FR_3581_STATIONARY_ANNULUS_PACKAGE_THEOREM.csv",
        "SAP3581_1_activation_implication",
        "3581 packages tau/surface/worldtube/anchor/gauge into one activation switch.",
    ),
    "SRC4103_05_3581_rows": (
        SOURCE_DIR / "P8_Y5_R2FR_3581_FINITE_ROWS.csv",
        "FAR3581_6_R_ann_abs",
        "3581 finite annulus residual rows.",
    ),
    "SRC4103_06_3582_anchor": (
        SOURCE_DIR / "P8_Y5_R2FR_3582_PHI_ANCHOR_ASYMPTOTIC_ZERO_THEOREM.csv",
        "PAZ3582_2_zero_flux_estimate",
        "3582 derives Phi_infty=0 for stationary asymptotic public EM with no radiative O(R^-1) field.",
    ),
    "SRC4103_07_3582_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3582_PHI_ANCHOR_BOUND_ROWS.csv",
        "PAB3582_1_Phi_anchor_abs",
        "3582 fills the anchor row conditionally.",
    ),
    "SRC4103_08_3583_Estat": (
        SOURCE_DIR / "P8_Y5_R2FR_3583_SAME_PANN_DOMAIN_THEOREM.csv",
        "SPD3583_5_residual_collapse",
        "3583 reduces tau/surface/worldtube/seam geometry to one E_stat owner.",
    ),
    "SRC4103_09_3583_stack": (
        SOURCE_DIR / "P8_Y5_R2FR_3583_GEOMETRY_RESIDUAL_STACK.csv",
        "GRS3583_7_R_ann_abs_after_3583",
        "3583 residual stack after carrying the anchor zero.",
    ),
    "SRC4103_10_3584_Estat_route": (
        SOURCE_DIR / "P8_Y5_R2FR_3584_PARENT_ESTAT_THEOREM_ATTEMPT.csv",
        "PET3584_6_current_verdict",
        "3584 gives the parent E_stat uniqueness/no-homogeneous-mode route.",
    ),
    "SRC4103_11_3584_stack": (
        SOURCE_DIR / "P8_Y5_R2FR_3584_ESTAT_EPSILON_STACK.csv",
        "ESE3584_6_Rann_after_3584",
        "3584 decomposes epsilon_Estat into source-ready residual components.",
    ),
    "SRC4103_12_3577_href": (
        SOURCE_DIR / "P8_Y5_R2FR_3577_HREF_REFERENCE_LOCK.csv",
        "REF3577_0_fixed_reference_rule",
        "3577 fixed-reference derivative silence for H_ref.",
    ),
    "SRC4103_13_3577_denominator": (
        SOURCE_DIR / "P8_Y5_R2FR_3577_MHREF_POSITIVE_DENOMINATOR_ROUTE.csv",
        "DEN3577_1_lower_bound",
        "3577 positive denominator route for M_H_ref.",
    ),
    "SRC4103_14_3577_epsilon": (
        SOURCE_DIR / "P8_Y5_R2FR_3577_EPSILON_HREF_LOCK_ROWS.csv",
        "EHL3577_5_total",
        "3577 narrowed epsilon_Href_lock formula.",
    ),
    "SRC4103_15_3579_public": (
        SOURCE_DIR / "P8_Y5_R2FR_3579_PUBLIC_EM_POYNTING_THEOREM.csv",
        "PEM3579_3_covariant_phase_space_zero",
        "3579 public EM/matter H_tau curl component theorem branch.",
    ),
    "SRC4103_16_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4103_local_exterior_Href_Poynting_no_flux_certificate_or_flux_rows.py",
        "Reproducible generator for this 4103 checkpoint.",
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


def exterior_certificate_rows() -> List[dict]:
    entries = [
        (
            "EXT4103_0_public_EM_current",
            "public EM Killing-energy current",
            "j_EM^mu[tau] := -T_EM^{mu nu} tau_nu, with div j_EM = -T_EM^{mu nu} nabla_(mu tau_nu) + tau_nu F^{nu lambda}J_lambda.",
            "This is the covariant Poynting identity in the observed public Maxwell branch. A Killing tau and source-free collar make the current closed.",
            "same observed Hodge/current owner; public Maxwell stress",
            "EXACT_CONDITIONAL_IDENTITY",
            "SRC4103_02_3580_theorem",
        ),
        (
            "EXT4103_1_transport",
            "stationary collar flux transport",
            "Phi_out-Phi_in = integral_A[partial_tau u_EM + J dot E + T_EM^{mu nu}nabla_(mu tau_nu)] dV + C_corner.",
            "If the collar is stationary, source-free, same-tau and corner-free, Poynting flux is transported between linked surfaces.",
            "same tau; no current crossing; actual S_in/S_out; fixed EM surface gauge",
            "TRANSPORT_THEOREM_REANCHORED",
            "SRC4103_03_3580_transport",
        ),
        (
            "EXT4103_2_anchor_zero",
            "asymptotic stationary public EM zero anchor",
            "For compact stationary Maxwell sources with no transverse radiative O(R^-1) field, E=O(R^-2), B=O(R^-3), so n.(E x H)=O(R^-5) and Phi_infty=0.",
            "The surface area is O(R^2), hence the flux integral is O(R^-3)->0. This conditionally fills Phi_anchor_abs=0.",
            "stationary asymptotic public EM branch; no radiative homogeneous mode",
            "ANCHOR_ZERO_DERIVED_CONDITIONALLY",
            "SRC4103_06_3582_anchor",
        ),
        (
            "EXT4103_3_same_package",
            "same P_ann package switch",
            "Z_Poynting = Z_tau & Z_same_tau & Z_surface & Z_worldtube & Z_anchor & Z_gauge & Z_no_seams.",
            "3581 prevents scoring a zero anchor in one package and transport in another. All clauses must belong to one stationary annulus package.",
            "single package P_ann=(tau_obs,Sigma_tau,W_source,S_in,S_out,H_ref,EM_gauge_class,Phi_anchor)",
            "EXACT_BOOLEAN_SWITCH_RETAINED",
            "SRC4103_04_3581_package",
        ),
        (
            "EXT4103_4_Estat_collapse",
            "single E_stat geometry owner",
            "E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty) implies tau/same-tau/surface/worldtube/no-seam clauses together.",
            "One parent-owned stationary exterior domain supplies the Killing generator, surfaces, compact no-crossing source worldtube and smooth annulus. With Phi_anchor=0, the annulus residual becomes C_EM_surface_gauge_abs + epsilon_Estat.",
            "parent-owned E_stat before readout; no seams; compact K-invariant source support",
            "GEOMETRY_STACK_COLLAPSES_CONDITIONALLY",
            "SRC4103_08_3583_Estat",
        ),
        (
            "EXT4103_5_parent_Estat_route",
            "E_stat from uniqueness/no-homogeneous-mode theorem",
            "If parent exterior equations, boundary data and source/current data are K-invariant, and the exterior boundary-value problem is unique modulo gauge with no radiative homogeneous kernel, then L_K fields=0 and E_stat follows.",
            "The K-flowed solution has the same data; uniqueness makes it the same solution. The missing clause is not stationarity-by-axiom but uniqueness/no-radiative-kernel plus source/current ownership.",
            "parent operator route; boundary K; source K; uniqueness modulo gauge; no homogeneous radiative mode; no extra hair",
            "EXACT_CONDITIONAL_ROUTE_NOT_PUBLIC",
            "SRC4103_10_3584_Estat_route",
        ),
        (
            "EXT4103_6_public_EM_Htau_component",
            "public EM H_tau curl component",
            "I_matter_EM_flux=0 if E_stat, Phi_infty=0 and EM surface gauge/corner silence all close; otherwise I_matter_EM_flux <= A_F sup_BF R_ann_abs.",
            "This is the component-level feed into H_tau/H_ref. It narrows the EM term but does not close the full H_tau curl or local GR.",
            "same branch; positive M_H_ref denominator; no cancellation with other curl components",
            "HTAU_COMPONENT_CONTRACT_READY",
            "SRC4103_15_3579_public",
        ),
    ]
    return [
        {
            **row_base(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_form": statement,
            "derivation": derivation,
            "required_premises": premises,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, statement, derivation, premises, status, source_key in entries
    ]


def package_activation_rows() -> List[dict]:
    entries = [
        ("ACT4103_0_same_public_EM", "Z_public_EM", "same observed Hodge/current owner", "PASS_CONDITIONAL_PUBLIC_EM", "full EM alpha/lambda_A owner still separate", "SRC4103_15_3579_public"),
        ("ACT4103_1_anchor", "Z_anchor", "Phi_anchor_abs=Phi_infty=0 on stationary asymptotic no-radiation branch", "PASS_CONDITIONAL_PUBLIC_EM_ZERO_ANCHOR", "requires no radiative O(R^-1) homogeneous mode", "SRC4103_06_3582_anchor"),
        ("ACT4103_2_Href_fixed", "Z_Href", "H_ref fixed before source/orbit/PPN scoring; D_source H_ref=0", "PASS_INTERNAL_CANDIDATE_ONLY", "M_H_ref positivity and H_tau curl still open", "SRC4103_12_3577_href"),
        ("ACT4103_3_Estat", "Z_Estat", "one parent-owned stationary exterior domain supplies K,tau,surfaces,worldtube,no seams", "FAIL_CURRENT_PUBLIC_CLAIM", "parent E_stat theorem premises unsigned", "SRC4103_10_3584_Estat_route"),
        ("ACT4103_4_gauge_corner", "Z_gauge", "EM gauge representative fixed on surfaces or exact/proper corner only", "FAIL_CURRENT_PUBLIC_CLAIM", "C_EM_surface_gauge_abs remains live", "SRC4103_09_3583_stack"),
        ("ACT4103_5_MHref_positive", "Z_MHref_positive", "M_H_ref exact positive or M_H_ref_lower>0 from EH comparator", "FAIL_CURRENT_PUBLIC_CLAIM", "M_EH and epsilon_abs component rows unfilled", "SRC4103_13_3577_denominator"),
        ("ACT4103_6_public_EM_flux_zero", "Z_I_matter_EM_flux", "Z_public_EM & Z_anchor & Z_Estat & Z_gauge", "FAIL_CURRENT_PUBLIC_CLAIM", "E_stat and gauge/corner remain unsigned", "SRC4103_08_3583_Estat"),
        ("ACT4103_7_local_GR", "Z_local_GR", "selector plus source/Href/EM/GM/PPN all close", "FAIL_CURRENT_PUBLIC_CLAIM", "local GR/Newton/PPN remain downstream", "SRC4103_01_4102_leaks"),
    ]
    return [
        {
            **row_base(),
            "activation_id": activation_id,
            "indicator": indicator,
            "zero_condition": condition,
            "status": status,
            "remaining_gap": gap,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for activation_id, indicator, condition, status, gap, source_key in entries
    ]


def href_denominator_rows() -> List[dict]:
    entries = [
        (
            "HREF4103_0_fixed_reference",
            "epsilon_ref_source",
            "epsilon_ref_source := |D_X H_ref|/M_H_ref_lower = 0 inside the parent-fixed reference candidate branch.",
            "dimensionless",
            "INTERNAL_CANDIDATE_ZERO_NONCLAIM",
            "H_ref selector chosen before source/orbit/PPN scoring with no measured-GM laundering",
            "SRC4103_12_3577_href",
        ),
        (
            "HREF4103_1_exact_MHref",
            "M_H_ref",
            "M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref).",
            "mass or energy/G_ref convention",
            "DEFINITION_READY_VALUE_MISSING",
            "finite H_tau, fixed H_ref, constant G_ref, same frame and positive value",
            "SRC4103_13_3577_denominator",
        ),
        (
            "HREF4103_2_positive_lower_bound",
            "M_H_ref_lower",
            "M_H_ref >= M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_ref*M_EH).",
            "same as M_EH",
            "DERIVED_LOWER_BOUND_LAW_COMPONENTS_MISSING",
            "source-backed M_EH>0 and epsilon_abs<1 without importing orbital GM",
            "SRC4103_13_3577_denominator",
        ),
        (
            "HREF4103_3_EM_feed",
            "epsilon_Htau_curl_EM",
            "epsilon_Htau_curl_EM <= A_F sup_BF R_ann_abs / M_H_ref_lower.",
            "dimensionless",
            "NARROWED_TO_RANN_STACK_NONCLAIM",
            "R_ann_abs from E_stat/gauge stack plus positive M_H_ref_lower",
            "SRC4103_09_3583_stack",
        ),
        (
            "HREF4103_4_total_Href_lock",
            "epsilon_Href_lock",
            "epsilon_Href_lock <= epsilon_Htau_curl + epsilon_tau_surface_frame + epsilon_symplectic_boundary + epsilon_MHref_qbasic.",
            "dimensionless no-cancellation envelope",
            "FORMULA_READY_COMPONENTS_RETAINED",
            "non-EM H_tau curl, tau/surface/frame, symplectic boundary and q-basic denominator leakage",
            "SRC4103_14_3577_epsilon",
        ),
    ]
    return [
        {
            **row_base(),
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "required_inputs": required,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, formula, units, status, required, source_key in entries
    ]


def flux_residual_rows() -> List[dict]:
    entries = [
        ("FLUX4103_0_Phi_anchor", "Phi_anchor_abs", "0 on stationary asymptotic public EM no-radiation branch", "same as Phi_infty", "ZERO_IF_3582_BRANCH_CONDITIONS_HOLD", "SRC4103_07_3582_bounds"),
        ("FLUX4103_1_Estat", "epsilon_Estat", "epsilon_boundary_K + epsilon_source_K + epsilon_unique_ext + epsilon_hom_mode + epsilon_extra_hair", "Hamiltonian numerator or normalized residual", "NO_CANCELLATION_ESTAT_STACK_READY_VALUES_MISSING", "SRC4103_11_3584_stack"),
        ("FLUX4103_2_gauge", "C_EM_surface_gauge_abs", "absolute EM gauge/corner term on S_in union S_out", "Hamiltonian numerator", "MISSING_EM_GAUGE_CORNER_VALUE_OR_ZERO_THEOREM", "SRC4103_09_3583_stack"),
        ("FLUX4103_3_Rann", "R_ann_abs", "C_EM_surface_gauge_abs + epsilon_Estat", "Hamiltonian numerator or normalized residual", "REDUCED_RESIDUAL_STACK_NONCLAIM", "SRC4103_11_3584_stack"),
        ("FLUX4103_4_Htau_feed", "I_matter_EM_flux", "I_matter_EM_flux <= A_F sup_BF R_ann_abs", "Hamiltonian curl numerator units", "HTAU_FEED_READY_NONCLAIM", "SRC4103_02_3580_theorem"),
        ("FLUX4103_5_selector_feed", "epsilon_selector_leak", "epsilon_selector_leak includes normalized R_ann_abs and H_ref/M_H denominator leakage until source-backed zero or bound", "dimensionless after denominator declaration", "SELECTOR_PRODUCT_LEAK_REDUCED_NOT_CLOSED", "SRC4103_01_4102_leaks"),
    ]
    return [
        {
            **row_base(),
            "flux_id": flux_id,
            "symbol": symbol,
            "value_or_bound": value,
            "units": units,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "source_backed_numeric": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for flux_id, symbol, value, units, status, source_key in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4103_0_transport_anchor",
            "carry forward the Poynting transport plus asymptotic zero-anchor theorem",
            "3580 proves transport and 3582 conditionally fills Phi_anchor_abs=0; this is real public EM progress",
            "Poynting no-flux is now blocked by same-package geometry/gauge, not by a missing radiation placeholder",
            "POYNTING_ANCHOR_ADVANCED",
            "SRC4103_06_3582_anchor",
        ),
        (
            "DEC4103_1_Estat_reduction",
            "collapse tau/surface/worldtube/no-seam clauses into E_stat",
            "3583 shows one parent-owned stationary exterior domain would close the geometry stack together",
            "do not chase each surface clause separately unless E_stat route fails",
            "ESTAT_SELECTED_AS_GEOMETRY_GATE",
            "SRC4103_08_3583_Estat",
        ),
        (
            "DEC4103_2_parent_Estat_route",
            "use uniqueness/no-homogeneous-mode as the non-smuggled E_stat derivation route",
            "3584 gives the theorem pattern: K-invariant equations/data plus unique exterior solution imply stationarity",
            "next work should attack no radiative homogeneous mode and extra-hair silence",
            "UNIQUENESS_ROUTE_SELECTED",
            "SRC4103_10_3584_Estat_route",
        ),
        (
            "DEC4103_3_Href",
            "retain fixed H_ref as internal credit but keep denominator open",
            "3577 zeros reference-source laundering internally but M_H_ref positivity and H_tau curl remain unfilled",
            "no Newton/local-GR claim until M_H_ref_lower and curl components are sourced or zero-derived",
            "HREF_NARROWED_NOT_CLOSED",
            "SRC4103_14_3577_epsilon",
        ),
        (
            "DEC4103_4_no_public_claim",
            "do not claim public local GR/Newton/Maxwell/PPN",
            "E_stat, gauge corner, M_H_ref positivity, alpha/lambda_A, source coupling and PPN remain open",
            "continue private derivation discipline",
            "PUBLIC_CLAIM_BLOCKED",
            "SRC4103_01_4102_leaks",
        ),
        (
            "DEC4103_5_next",
            "attack no-homogeneous exterior mode and extra hair next",
            "this is the hard unsigned clause in the E_stat theorem and decides whether no-radiation is a theorem or a bound row",
            "4104 targets no-homogeneous exterior mode or epsilon_hom/epsilon_extra rows",
            "NEXT_TARGET_SELECTED",
            "SRC4103_11_3584_stack",
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
        for decision_id, decision, reason, consequence, status, source_key in entries
    ]


def claim_gate_rows() -> List[dict]:
    entries = [
        ("CLAIM4103_0_Phi_anchor", "Phi_anchor_abs=0", "CONDITIONAL_PUBLIC_EM_BRANCH_ONLY", "valid only for stationary asymptotic no-radiation branch; same package still needed", "E_stat/gauge package"),
        ("CLAIM4103_1_I_matter_EM_flux", "I_matter_EM_flux=0", "BLOCKED", "requires E_stat and EM gauge/corner silence in same package", "Z_Estat and Z_gauge"),
        ("CLAIM4103_2_Href_MH", "H_ref/M_H source denominator closed", "BLOCKED", "fixed H_ref internal, but positive M_H_ref and H_tau curl components remain", "M_H_ref_lower and residual components"),
        ("CLAIM4103_3_local_GR_Newton", "local GR/Newton/PPN recovery", "BLOCKED", "source coupling, GM transfer, denominator positivity and PPN residuals remain", "source/GM/PPN gates"),
        ("CLAIM4103_4_Maxwell_owner", "full Maxwell/alpha owner", "BLOCKED", "Poynting flux narrowed, but alpha/lambda_A normalization and hidden EM owner remain separate", "D_X ln(lambda_A) and EM owner gates"),
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
        for claim_id, claim, status, reason, missing in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4103_0",
            "target_doc": "4104-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md",
            "target_script": "scripts/Y5_R2FR_4104_no_homogeneous_exterior_mode_or_extra_hair_epsilon_row.py",
            "objective": "prove no radiative/time-dependent homogeneous exterior mode or retained extra-field hair survives the local stationary boundary class; if not, write epsilon_hom_mode and epsilon_extra_hair residual rows with units",
            "success_gate": "E_stat uniqueness/no-homogeneous-mode clause closes, or epsilon_hom_mode and epsilon_extra_hair become explicit finite nonclaim rows",
            "reason": "4103 reduces Poynting/Href exterior leakage to E_stat uniqueness plus EM gauge corner and denominator positivity; no-homogeneous-mode is the hardest E_stat clause",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4103_0",
            "decision": DECISION,
            "poynting_status": "Phi_anchor_abs conditionally zero; R_ann_abs reduced to C_EM_surface_gauge_abs + epsilon_Estat",
            "href_status": "fixed H_ref derivative silence internal; M_H_ref_lower and H_tau curl denominator still retained",
            "estat_status": "E_stat route identified by uniqueness/no-homogeneous-mode theorem but not public-signed",
            "public_status": "no local_GR_Newton_Maxwell_PPN claim",
            "next_target": "4104 no homogeneous exterior mode or extra hair epsilon row",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4103_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4103_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE": SOURCE_DIR / "P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE.csv",
        "P8_Y5_R2FR_4103_PACKAGE_ACTIVATION": SOURCE_DIR / "P8_Y5_R2FR_4103_PACKAGE_ACTIVATION.csv",
        "P8_Y5_R2FR_4103_HREF_DENOMINATOR_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4103_HREF_DENOMINATOR_ROWS.csv",
        "P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK": SOURCE_DIR / "P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK.csv",
        "P8_Y5_R2FR_4103_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4103_DECISION_GATE.csv",
        "P8_Y5_R2FR_4103_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4103_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4103_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4103_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4103_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4103_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4103 - Local exterior Href/Poynting no-flux certificate or flux rows",
        "",
        "## Verdict",
        "4103 moves the Poynting/Hamiltonian exterior gate forward instead of merely restating it. The public EM flux anchor is conditionally filled: for a stationary asymptotic public Maxwell branch with no radiative `O(R^-1)` field, `Phi_infty=0` because `n.(E x H)=O(R^-5)` and the sphere area is `O(R^2)`.",
        "",
        "Carrying 3583/3584 forward, the same-package geometry problem collapses to one object: `E_stat=(D_ext,K,r,W_source,Sigma_tau,S_in,S_out,Phi_infty)`. If the parent exterior equations/data are `K`-invariant and the exterior solution is unique modulo gauge with no radiative homogeneous kernel, `E_stat` follows. If not, the honest residual is `epsilon_Estat`.",
        "",
        "So the reduced annulus residual is now `R_ann_abs = C_EM_surface_gauge_abs + epsilon_Estat`. `H_ref` also gains internal credit: fixed-reference derivative silence is retained, but `M_H_ref` positivity and full `H_tau` curl remain open.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## What Closed Conditionally",
        "- `Phi_anchor_abs=0` on the stationary asymptotic no-radiation public EM branch.",
        "- Poynting transport is a theorem in a stationary source-free collar.",
        "- Same-tau/surface/worldtube/no-seam clauses reduce to one `E_stat` certificate.",
        "- `H_ref` source/readout derivative silence is internally signed in the fixed-reference candidate branch.",
        "",
        "## What Remains Live",
        "- `E_stat` is not parent-derived yet: uniqueness/no-homogeneous-mode, source-current ownership, and extra-field silence remain unsigned.",
        "- `C_EM_surface_gauge_abs` remains a live gauge/corner residual.",
        "- `M_H_ref_lower>0` still needs `M_EH` and residual component rows.",
        "- Local GR/Newton/Maxwell/PPN claims remain blocked.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4103_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE.csv`",
        "- `P8_Y5_R2FR_4103_PACKAGE_ACTIVATION.csv`",
        "- `P8_Y5_R2FR_4103_HREF_DENOMINATOR_ROWS.csv`",
        "- `P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK.csv`",
        "- `P8_Y5_R2FR_4103_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4103_CLAIM_GATE.csv`",
        "- `P8_Y5_R2FR_4103_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4103_STATUS.csv`",
        "- `P8_Y5_BRR545_4103_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4104-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md`",
        "- Objective: prove no radiative/time-dependent homogeneous exterior mode or retained extra-field hair survives the local stationary boundary class, or write `epsilon_hom_mode` and `epsilon_extra_hair` rows.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4103_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE"], exterior_certificate_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_PACKAGE_ACTIVATION"], package_activation_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_HREF_DENOMINATOR_ROWS"], href_denominator_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK"], flux_residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4103_STATUS"], status_rows())
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
    add("VAL4103_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4103_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

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
    add("VAL4103_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    exterior_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4103_LOCAL_EXTERIOR_CERTIFICATE"]))
    exterior_tokens = ["j_EM", "Poynting", "Phi_infty=0", "E_stat", "I_matter_EM_flux", "homogeneous"]
    missing_exterior = [token for token in exterior_tokens if token not in exterior_text]
    add("VAL4103_3_exterior_tokens", "local exterior certificate has Poynting/Estat/Htau tokens", not missing_exterior, ";".join(missing_exterior) or "all exterior tokens present")

    activation_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4103_PACKAGE_ACTIVATION"]))
    activation_tokens = ["Z_anchor", "Z_Estat", "Z_gauge", "Z_MHref_positive", "Z_I_matter_EM_flux", "Z_local_GR"]
    missing_activation = [token for token in activation_tokens if token not in activation_text]
    add("VAL4103_4_activation_tokens", "package activation covers anchor/Estat/gauge/MHref/localGR", not missing_activation, ";".join(missing_activation) or "all activation tokens present")

    href_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4103_HREF_DENOMINATOR_ROWS"]))
    href_tokens = ["epsilon_ref_source", "M_H_ref", "M_H_ref_lower", "epsilon_Htau_curl_EM", "epsilon_Href_lock"]
    missing_href = [token for token in href_tokens if token not in href_text]
    add("VAL4103_5_href_tokens", "Href denominator rows cover reference, lower bound and EM feed", not missing_href, ";".join(missing_href) or "all Href tokens present")

    flux_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4103_FLUX_RESIDUAL_STACK"]))
    flux_tokens = ["Phi_anchor_abs", "epsilon_Estat", "C_EM_surface_gauge_abs", "R_ann_abs", "I_matter_EM_flux"]
    missing_flux = [token for token in flux_tokens if token not in flux_text]
    add("VAL4103_6_flux_stack", "flux residual stack has reduced annulus/Htau rows", not missing_flux, ";".join(missing_flux) or "all flux tokens present")

    claims = parse_csv(outputs["P8_Y5_R2FR_4103_CLAIM_GATE"])
    no_public_claim = all(row.get("public_claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    add("VAL4103_7_no_public_claims", "all claim rows remain nonpublic and nonclaim", no_public_claim, f"claim_rows={len(claims)}")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4103_NEXT_TARGET"])
    next_ok = any("4104-Y5-R2FR-no-homogeneous-exterior-mode-or-extra-hair-epsilon-row.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4103_8_next_target", "next target attacks no homogeneous exterior mode", next_ok, str(next_rows))

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    add("VAL4103_9_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4103_10_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4103_VALIDATION.csv"
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
