from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4354"
CLAIM_ID = "L-195"
BRANCH = "MTS_R2FR_Y5_HTAU_MHREF_SOURCE_CHARGE_OWNER_OR_FINITE_GN_DRIFT_BOUND_4354"
DECISION = "CONDITIONAL_HTAU_MHREF_NEWTON_BRIDGE_DERIVED_PRIVATE_SELECTOR_GN_DRIFT_BOUND_RETAINED_NONCLAIM"
MARKER = "PPC4161_HTAU_MHREF_SOURCE_CHARGE_OWNER_OR_FINITE_GN_DRIFT_BOUND_4354"
PACKET_MARKER = "PPC4161_PACKET_HTAU_MHREF_SOURCE_CHARGE_OWNER_OR_FINITE_GN_DRIFT_BOUND_4354"
NEXT_TARGET = "4355-Y5-R2FR-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md"

FORMAL_PATH = FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"
DOC_PATH = POST / "4354-Y5-R2FR-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4354_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4354_00_4353_next": (
        FORMAL / "369-PPC4161-full-clean-owner-tail-to-local-residual-vector-or-finite-score.md",
        "4354-Y5-R2FR-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md",
        "4353 handoff selecting H_tau/M_Hdress and calibrated-coupling gate.",
    ),
    "SRC4354_01_181_gate": (
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "kappa_eff = kappa_* Z_H",
        "Original kappa/G normalization gate.",
    ),
    "SRC4354_02_182_ZH": (
        FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md",
        "D_A delta_ZH = 0",
        "Hilbert source-measure no-drift condition.",
    ),
    "SRC4354_03_184_kappa": (
        FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md",
        "=> D_A ln kappa_* = 0.",
        "Parent-adopted topological kappa lock.",
    ),
    "SRC4354_04_187_newton": (
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "nabla^2 Phi_N = 4*pi G_N rho_H.",
        "Poisson/Gauss/Newton readout from Hamiltonian source charge.",
    ),
    "SRC4354_05_194_calibrated": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi).",
        "Calibrated source-coupling to G_N law.",
    ),
    "SRC4354_06_222_fair_G": (
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "MTS does not need to numerically predict G_N to reduce to GR/Newton.",
        "Fair GR-style calibrated-G posture.",
    ),
    "SRC4354_07_222_MH": (
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "M_H^dress = H_tau[S_link] - H_ref",
        "Source-charge caveat imported into calibrated bridge.",
    ),
    "SRC4354_08_227_contract": (
        FORMAL / "227-PPC4161-Htau-MHsource-parent-charge-owner.md",
        "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref",
        "Hamiltonian/Hilbert parent source charge owner contract.",
    ),
    "SRC4354_09_228_operator": (
        FORMAL / "228-PPC4161-Htau-integrability-operator-and-curl-bound.md",
        "H_tau exists on the allowed local branch",
        "Hamiltonian integrability iff field-space curl vanishes.",
    ),
    "SRC4354_10_307_pimh_glue": (
        FORMAL / "307-PPC4161-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md",
        "epsilon_PiH :=",
        "Pi_M/H_tau glue solved inside the private Hamiltonian selector.",
    ),
    "SRC4354_11_4215_reference": (
        SOURCE_DIR / "P8_Y5_R2FR_4215_REFERENCE_LOCK_THEOREM.csv",
        "D_source H_ref",
        "Fixed H_ref derivative-silence theorem and fallback.",
    ),
    "SRC4354_12_4216_tau_frame": (
        SOURCE_DIR / "P8_Y5_R2FR_4216_TAU_SURFACE_FRAME_THEOREM.csv",
        "TSF4216_0_one_time_generator",
        "One tau/surface/frame selector theorem and fallback.",
    ),
    "SRC4354_13_4217_boundary": (
        SOURCE_DIR / "P8_Y5_R2FR_4217_BOUNDARY_CORNER_THEOREM.csv",
        "N_G int_A d(Pi_M J_H[tau])",
        "Boundary/corner/no-flux collar theorem and fallback.",
    ),
    "SRC4354_14_1017_MHref": (
        POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "M_H_ref is a positive same-frame dressed source denominator",
        "Older strict denominator guard showing M_H_ref remains a real gate.",
    ),
}

ARENAS = [
    ("R10_short_range", "alpha(lambda) fifth-force source coupling", "epsilon_Gsrc projected into alpha_X rows with lambda_X and no cancellation"),
    ("PPN_solar_system", "gamma/beta/preferred-frame residuals", "epsilon_Gsrc plus readout/projector/EM residuals must sit below PPN bounds"),
    ("clock_redshift", "Gdot/G and clock-frame drift", "|D_t ln kappa_eff| plus tau/frame leakage"),
    ("orbital_GM", "Newtonian acceleration and Kepler charge", "GM_orbit must equal G_cal M_Hdress after the Hamiltonian source charge is fixed"),
    ("WEP_species", "species-dependent source measure", "Delta_species delta_ZH plus source-charge species hair"),
    ("local_Newton_GR", "Poisson/Gauss/Newton local reduction", "requires clean H_tau/M_Hdress plus constant source-blind G_cal"),
    ("EM_Poynting", "visible EM stress counted once", "stationary Poynting enters T_H once or radiative flux is a boundary row"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def coupling_lock_rows() -> List[Dict[str, str]]:
    return [
        {
            "lock_id": "CL4354_0_kappa_star",
            "object": "topological parent coupling kappa_*",
            "exact_law": "D_A ln kappa_* = 0",
            "close_if": "parent-adopted topological kappa sector is selected before source/readout variation",
            "fallback_if_open": "|D_A ln kappa_*|",
            "current_status": "CONDITIONALLY_ZERO_IN_PRIVATE_PARENT_SELECTOR",
            "claim_policy": "not a numeric prediction of G_N",
            "valid_for_claim": "False",
        },
        {
            "lock_id": "CL4354_1_ZH",
            "object": "Hilbert source-measure normalization Z_H",
            "exact_law": "Z_H = Z_0 exp(delta_ZH), delta_ZH=0, D_A delta_ZH=0",
            "close_if": "same Hilbert source measure descends for all sources/species/frames/ranges/readouts",
            "fallback_if_open": "|delta_ZH| + |D_A delta_ZH|",
            "current_status": "CONDITIONAL_SOURCE_MEASURE_GATE",
            "claim_policy": "source-measure drift is a real observable residual",
            "valid_for_claim": "False",
        },
        {
            "lock_id": "CL4354_2_kappa_eff",
            "object": "effective local coupling kappa_eff",
            "exact_law": "kappa_eff = kappa_* Z_H and D_A ln kappa_eff = D_A ln kappa_* + D_A delta_ZH = 0",
            "close_if": "CL4354_0 and CL4354_1 both close on the same branch",
            "fallback_if_open": "epsilon_kappa_A <= |D_A ln kappa_*| + |D_A delta_ZH|",
            "current_status": "DERIVED_IF_COMPONENT_LOCKS_CLOSE",
            "claim_policy": "constant source-blind coupling is the GR-style local-reduction requirement",
            "valid_for_claim": "False",
        },
        {
            "lock_id": "CL4354_3_Gcal",
            "object": "calibrated Newton coupling",
            "exact_law": "G_cal := c^4 kappa_eff/(8*pi), G_N^obs := G_cal",
            "close_if": "kappa_eff is source-blind and calibrated once",
            "fallback_if_open": "G drift or source dependence scored by epsilon_kappa_A",
            "current_status": "STRUCTURAL_CALIBRATION_ALLOWED_NUMERIC_G_NOT_PREDICTED",
            "claim_policy": "fair comparison with GR: MTS need not derive numeric G_N here",
            "valid_for_claim": "False",
        },
        {
            "lock_id": "CL4354_4_no_hidden_drift",
            "object": "source/time/species/frame/range/readout drift",
            "exact_law": "D_A ln G_cal = 0 for A in {time,species,frame,range,environment,readout}",
            "close_if": "no hidden dependence survives kappa_* or Z_H",
            "fallback_if_open": "epsilon_Gdrift = sup_A |D_A ln G_cal|",
            "current_status": "FINITE_DRIFT_BOUND_RETAINED",
            "claim_policy": "no local-GR claim if any hidden G/source drift remains unsigned",
            "valid_for_claim": "False",
        },
    ]


def source_charge_rows() -> List[Dict[str, str]]:
    return [
        {
            "charge_id": "SC4354_0_same_worldtube",
            "object": "Hilbert source worldtube",
            "required_law": "W_H fixed before readout and int_W rho_H dV_H = M_H^dress[W_H;tau]",
            "current_evidence": "227 owner contract defines the worldtube requirement",
            "fallback_if_open": "|Delta_worldtube_domain|",
            "status": "CONDITION_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_1_Htau_MHref",
            "object": "Hamiltonian/Hilbert mass charge",
            "required_law": "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref",
            "current_evidence": "227 and 222 define the exact source charge",
            "fallback_if_open": "|Delta_MH_definition|/M_H_ref",
            "status": "DEFINED_NOT_PUBLICLY_CLOSED",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_2_PiM_glue",
            "object": "Pi_M/H_tau private selector glue",
            "required_law": "epsilon_PiH := |ell_M(Pi_M^H J_H_total)-(H_tau[S_link]-H_ref)|/|M_H^dress| = 0",
            "current_evidence": "4291/307 solves this inside the private Hamiltonian selector",
            "fallback_if_open": "epsilon_PiH retained outside selector",
            "status": "ZERO_INSIDE_PRIVATE_SELECTOR_ONLY",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_3_integrability",
            "object": "Hamiltonian one-form exactness",
            "required_law": "alpha_tau,S(delta)=int_S(delta Q_tau-i_tau theta_total(delta))-delta H_ref is exact iff I_tau,S=0",
            "current_evidence": "228 derives the operator; full MTS curl still needs every non-EH/projector/boundary piece closed",
            "fallback_if_open": "|I_MTS|/M_H_ref",
            "status": "OPERATOR_DERIVED_FULL_ZERO_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_4_reference_lock",
            "object": "fixed H_ref",
            "required_law": "H_ref chosen before source/radius/frame/readout variation and D_source H_ref=D_radius H_ref=D_frame H_ref=D_readout H_ref=0",
            "current_evidence": "4215 supplies conditional reference-lock theorem",
            "fallback_if_open": "(|R_ref_selector|+|R_ref_source|+|R_ref_radius|+|R_ref_frame|+|R_ref_fit|+|R_ref_boundary|)/M_H_ref",
            "status": "CONDITIONAL_ZERO_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_5_tau_frame_lock",
            "object": "one time generator and observed coframe",
            "required_law": "tau_source=tau_charge=tau_clock=tau_orbit=tau_PPN=tau_readout and same e_obs",
            "current_evidence": "4216 supplies conditional tau/surface/frame lock",
            "fallback_if_open": "(|R_tau_split|+|R_surface_motion|+|R_frame_coframe|+|R_clock_readout|+|R_orbital_readout|+|R_units|)/M_H_ref",
            "status": "CONDITIONAL_ZERO_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_6_boundary_flux",
            "object": "boundary/corner/radiative collar",
            "required_law": "no source crossing, no imposed incoming radiation, no open-memory pullback and no hidden wall/shear flux",
            "current_evidence": "4217 supplies conditional boundary/corner/no-flux theorem",
            "fallback_if_open": "(|R_diff_owner|+|R_corner_edge|+|R_rad_flux|+|R_source_crossing|+|R_memory_pullback|+|R_improvement|)/M_H_ref",
            "status": "CONDITIONAL_ZERO_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_7_MHref_positive",
            "object": "positive same-frame denominator",
            "required_law": "M_H_ref > 0, stable, same-frame and source-backed",
            "current_evidence": "1017 guard shows this remains a real denominator gate",
            "fallback_if_open": "|delta_MHref|/M_H_ref or BLOCKED_NO_NORMALIZER",
            "status": "OPEN_HIGH_LEVERAGE_GATE",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_8_anti_circularity",
            "object": "no orbital-GM or fitted-G source definition",
            "required_law": "no orbital GM, fitted acceleration, R10 residual, PPN residual or measured numerical G defines M_H^dress or H_ref",
            "current_evidence": "187/194/227 all enforce anti-circularity",
            "fallback_if_open": "CLAIM_BLOCKED_CIRCULAR_SOURCE",
            "status": "FIREWALL_ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "charge_id": "SC4354_9_full_source_charge",
            "object": "parent-owned Newton/GR source mass",
            "required_law": "SC4354_0 through SC4354_8 hold on the same branch",
            "current_evidence": "conditional branch law assembled by 4354",
            "fallback_if_open": "epsilon_Gsrc finite no-cancellation envelope",
            "status": "CONDITIONAL_THEOREM_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "False",
        },
    ]


def newton_bridge_rows() -> List[Dict[str, str]]:
    return [
        {
            "bridge_id": "NB4354_0_field_equation",
            "step": "local GR block",
            "law": "G_mu_nu[g_obs] = kappa_eff T_H_mu_nu + residual_mu_nu",
            "requires": "parent selector, EH block, same observed coframe, source-blind kappa_eff",
            "result": "structural GR coupling if residual_mu_nu=0 or bounded",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "NB4354_1_poisson",
            "step": "weak-field Newton limit",
            "law": "G_00^lin = 2 nabla^2 Phi_N/c^2 and kappa_eff=8*pi G_cal/c^4 imply nabla^2 Phi_N = 4*pi G_cal rho_H",
            "requires": "same rho_H source measure and no coupling drift",
            "result": "Poisson equation with calibrated universal G_cal",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "NB4354_2_gauss",
            "step": "source charge insertion",
            "law": "int_W rho_H dV_H = M_H^dress[W_H;tau]",
            "requires": "H_tau integrability, fixed H_ref, positive denominator and same worldtube",
            "result": "int_S grad Phi_N dot dS = 4*pi G_cal M_H^dress",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "NB4354_3_acceleration",
            "step": "local orbital readout",
            "law": "Phi_N = -G_cal M_H^dress/r and a_r = -G_cal M_H^dress/r^2",
            "requires": "no hidden readout/source/frame/range dependence",
            "result": "Newtonian acceleration follows without defining the source by observed orbital GM",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "NB4354_4_conditional_theorem",
            "step": "4354 theorem",
            "law": "If coupling locks and source-charge locks close on the same local branch, MTS reduces structurally to the local GR/Newton source law with calibrated G_cal",
            "requires": "CL4354_* and SC4354_* on one branch",
            "result": "real derivation target; public claim still blocked until all selectors are parent-signed",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "NB4354_5_numeric_G_firewall",
            "step": "fair-comparison guard",
            "law": "numeric(G_cal) remains empirical calibration unless a parent dimensionful invariant fixes kappa_*",
            "requires": "do not smuggle measured G into kappa_* or M_Hdress",
            "result": "not predicting G_N is not a failure relative to GR",
            "valid_for_claim": "False",
        },
    ]


def drift_bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "DB4354_0_kappa_drift",
            "residual": "epsilon_kappa_A",
            "formula": "|D_A ln kappa_*| + |D_A delta_ZH|",
            "meaning": "effective G/source-measure drift in time/species/frame/range/environment/readout direction A",
            "zero_if": "CL4354_0 and CL4354_1 close",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_1_integrability",
            "residual": "delta_H_tau_nonintegrable_over_MH",
            "formula": "|I_MTS|/M_H_ref",
            "meaning": "Hamiltonian one-form curl obstruction",
            "zero_if": "full MTS H_tau curl vanishes for all allowed variations",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_2_reference",
            "residual": "Delta_ref_over_MH",
            "formula": "(|R_ref_selector|+|R_ref_source|+|R_ref_radius|+|R_ref_frame|+|R_ref_fit|+|R_ref_boundary|)/M_H_ref",
            "meaning": "fixed-reference failure or post-fit reference leakage",
            "zero_if": "H_ref is fixed and derivative-silent before readout",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_3_tau_frame_surface",
            "residual": "Delta_tau_frame_surface_over_MH",
            "formula": "(|R_tau_split|+|R_surface_motion|+|R_frame_coframe|+|R_clock_readout|+|R_orbital_readout|+|R_units|)/M_H_ref",
            "meaning": "time generator, surface, coframe or readout mismatch",
            "zero_if": "same tau/surface/e_obs branch selected before variation",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_4_boundary_flux",
            "residual": "Delta_boundary_flux_over_MH",
            "formula": "(|R_diff_owner|+|R_corner_edge|+|R_rad_flux|+|R_source_crossing|+|R_memory_pullback|+|R_improvement|)/M_H_ref",
            "meaning": "boundary, corner, radiative or memory flux through the local collar",
            "zero_if": "differentiability-owned no-flux collar holds",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_5_PiH_glue",
            "residual": "epsilon_PiH",
            "formula": "|ell_M(Pi_M^H J_H_total)-(H_tau[S_link]-H_ref)|/|M_H^dress|",
            "meaning": "source-denominator glue mismatch outside the private Hamiltonian selector",
            "zero_if": "private Hamiltonian selector adopted before readout",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_6_MHref",
            "residual": "Delta_MHref_normalizer",
            "formula": "BLOCKED_NO_NORMALIZER or |delta_MHref|/M_H_ref",
            "meaning": "positive same-frame M_H_ref denominator missing or unstable",
            "zero_if": "M_H_ref>0 is source-backed in the same frame",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_7_worldtube_species",
            "residual": "Delta_worldtube_species",
            "formula": "|Delta_worldtube_domain| + |Delta_species delta_ZH| + |Delta_source_hair|",
            "meaning": "wrong source region, species-dependent source measure or remaining source hair",
            "zero_if": "same Hilbert worldtube/source measure for every tested body",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "DB4354_8_total",
            "residual": "epsilon_Gsrc",
            "formula": "sup_A epsilon_kappa_A + |I_MTS|/M_H_ref + |Delta_ref|/M_H_ref + |Delta_tau_frame_surface|/M_H_ref + |Delta_boundary_flux|/M_H_ref + epsilon_PiH + Delta_MHref_normalizer + Delta_worldtube_species",
            "meaning": "no-cancellation source/coupling envelope for local tests",
            "zero_if": "all coupling and H_tau/MHref/source selectors close on one branch",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, observable, projection in ARENAS:
        rows.append(
            {
                "arena_id": f"AR4354_{arena}",
                "arena": arena,
                "observable": observable,
                "clean_branch_input": "epsilon_Gsrc = 0 plus existing nonowner residual gates",
                "finite_branch_projection": projection,
                "required_before_claim": "real projection constants, units, source paths and no-cancellation runner rows",
                "claim_status": "NO_PASS_FROM_4354_ALONE",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4354_0_clean",
            "input": "CL4354_* and SC4354_* close on the same private local branch",
            "action": "PROMOTE_TO_PRIVATE_STRUCTURAL_NEWTON_BRIDGE",
            "result": "D_A ln G_cal=0, int rho_H=M_Hdress, Phi_N=-G_cal M_Hdress/r",
            "claim_policy": "private theorem only until parent/global selector and empirical projections are signed",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4354_1_finite",
            "input": "any H_tau/MHref/source/coupling clause open",
            "action": "KEEP_EPSILON_GSRC_NO_CANCELLATION_BOUND",
            "result": "local arenas receive explicit finite source/coupling residual rows",
            "claim_policy": "no pass unless every row has numeric/theorem-zero provenance",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4354_2_current",
            "input": "current corpus after 4353",
            "action": "CLASSIFY_CURRENT_STATE",
            "result": "kappa/G fair route and Pi_M/H_tau glue are sharpened; full public source charge remains blocked by selector adoption, full integrability and M_H_ref positivity",
            "claim_policy": "do not call local GR solved",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4354_3_next",
            "input": "Pi_M/H_tau glue solved inside private selector",
            "action": "ATTACK_TRANSITION_SOURCE_HAIR",
            "result": NEXT_TARGET,
            "claim_policy": "transition non-Hilbert residue must be zero or bounded before source branch can score cleanly",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4354_0",
            "rule": "Do not require MTS to predict the numerical value of G_N at this stage.",
            "reason": "GR also uses one empirically calibrated universal G; the serious requirement is source-blind constancy and a non-circular source charge.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4354_1",
            "rule": "Do not define M_Hdress using orbital GM, fitted acceleration, measured G, PPN residuals or R10 residuals.",
            "reason": "Those are tests of the source law, not ingredients in the source definition.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4354_2",
            "rule": "Do not use Pi_M/H_tau private selector glue as a global/public parent-action proof.",
            "reason": "4291/307 solves the glue only inside the private Hamiltonian selector.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4354_3",
            "rule": "Do not cancel unknown source/coupling residuals against each other.",
            "reason": "epsilon_Gsrc is an absolute no-cancellation envelope.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4354_4",
            "rule": "Do not claim local GR/Newton until M_H_ref is positive, stable, same-frame and source-backed.",
            "reason": "Without the denominator, normalized integrability/reference/boundary rows are not evidence.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4354_0",
            "decision": DECISION,
            "reason": "4354 derives the precise local source-coupling fork. If kappa_* and Z_H are source-blind, and if the same-worldtube Hamiltonian/Hilbert mass charge M_Hdress=H_tau-H_ref is integrable, fixed-reference, same-tau/frame, no-flux and positive, then the weak-field Poisson/Gauss/Newton law follows with calibrated universal G_cal. Current MTS has strong private pieces, including Pi_M/H_tau glue inside the private selector, but the full public source charge remains blocked by selector adoption, full MTS integrability and M_H_ref positivity. Therefore epsilon_Gsrc remains as the finite no-cancellation bound.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4354_0",
            "item": "numeric G_N",
            "status": "NOT_REQUIRED_FOR_STRUCTURAL_LOCAL_REDUCTION",
            "note": "MTS can be GR-competitive with one calibrated source-blind G_cal.",
        },
        {
            "status_id": "STAT4354_1",
            "item": "kappa_eff drift",
            "status": "DERIVED_ZERO_IF_KAPPA_AND_ZH_LOCKS_CLOSE",
            "note": "D_A ln kappa_eff = D_A ln kappa_* + D_A delta_ZH.",
        },
        {
            "status_id": "STAT4354_2",
            "item": "Pi_M/H_tau glue",
            "status": "ZERO_INSIDE_PRIVATE_HAMILTONIAN_SELECTOR",
            "note": "This is progress, but it is not global parent adoption.",
        },
        {
            "status_id": "STAT4354_3",
            "item": "M_H_ref",
            "status": "OPEN_DENOMINATOR_GATE",
            "note": "Positive same-frame source-backed denominator remains required.",
        },
        {
            "status_id": "STAT4354_4",
            "item": "epsilon_Gsrc",
            "status": "FINITE_NO_CANCELLATION_BOUND_RETAINED",
            "note": "All unsigned source/coupling clauses remain testable rather than erased.",
        },
        {
            "status_id": "STAT4354_5",
            "item": "next target",
            "status": "TRANSITION_SOURCE_HAIR",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4354_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the transition shell be shown to stay in the same Hilbert worldtube with no non-Hilbert residue, or must finite source-hair rows be carried into local tests?",
            "preferred_route": "derive transition same-worldtube membership, epsilon_mu_tr=0, Q_l>=1_tr=0 and time/range/frame/species/beta hair = 0 from the private Hamiltonian selector",
            "fallback_route": "create source-backed finite rows for transition non-Hilbert residue and feed them into epsilon_Gsrc",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "coupling": coupling_lock_rows(),
        "charge": source_charge_rows(),
        "newton": newton_bridge_rows(),
        "drift": drift_bound_rows(),
        "arenas": arena_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4354_SOURCE_REGISTER.csv",
        "coupling": "P8_Y5_R2FR_4354_COUPLING_LOCK_ROWS.csv",
        "charge": "P8_Y5_R2FR_4354_SOURCE_CHARGE_ROWS.csv",
        "newton": "P8_Y5_R2FR_4354_NEWTON_BRIDGE_ROWS.csv",
        "drift": "P8_Y5_R2FR_4354_DRIFT_BOUND_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4354_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4354_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4354_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4354_DECISION.csv",
        "status": "P8_Y5_R2FR_4354_STATUS.csv",
        "next": "P8_Y5_R2FR_4354_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 370 PPC4161 Htau MHref source charge owner or finite GN drift bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4354 is not a public local-GR proof, not a Newtonian-mechanics proof, not an R10/PPN/clock/orbital pass, and not a numerical prediction of `G_N`.

It is a real source-coupling fork:

```text
clean branch:
  D_A ln kappa_* = 0
  D_A delta_ZH = 0
  D_A ln kappa_eff = 0
  G_cal := c^4 kappa_eff/(8*pi)
  M_H^dress[W_H;tau] = H_tau[S_link] - H_ref
  int_W rho_H dV_H = M_H^dress

=> nabla^2 Phi_N = 4*pi G_cal rho_H
=> Phi_N = -G_cal M_H^dress/r
=> a_r = -G_cal M_H^dress/r^2.
```

If any source/coupling clause is open, the branch keeps the finite no-cancellation residual:

```text
epsilon_Gsrc <=
  sup_A (|D_A ln kappa_*| + |D_A delta_ZH|)
  + |I_MTS|/M_H_ref
  + |Delta_ref|/M_H_ref
  + |Delta_tau_frame_surface|/M_H_ref
  + |Delta_boundary_flux|/M_H_ref
  + epsilon_PiH
  + Delta_MHref_normalizer
  + Delta_worldtube_species.
```

## What Actually Moved

The coupling problem is no longer "derive the numerical value of `G_N`". The fair GR-like target is one calibrated universal `G_cal` with no source/time/species/frame/range/readout drift.

The source-denominator problem is also sharper than a missing vibe. 4291/307 gives:

```text
Pi_M/H_tau = solved inside private Hamiltonian selector,
Pi_M/H_tau = explicit epsilon_PiH residual outside selector.
```

So the live problem is now the same-branch source charge: full `H_tau` integrability, fixed `H_ref`, same `tau/e_obs`, no boundary/radiative leakage, positive same-frame `M_H_ref`, and transition-shell source hair.

## Conditional Theorem

If all rows `CL4354_*` and `SC4354_*` close on the same local branch, then MTS has the local GR/Newton source law in the same structural sense GR has it: a universal calibrated coupling and a Hamiltonian/Hilbert source mass. No orbital `GM`, fitted acceleration, measured numerical `G`, PPN residual, or R10 residual is allowed to define the source mass.

Current status: conditional private branch law only. `epsilon_Gsrc` remains active until the unsigned clauses are parent-signed or source-backed.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Coupling Lock Rows

{md_table(tables["coupling"], ["lock_id", "object", "exact_law", "close_if", "fallback_if_open", "current_status", "claim_policy", "valid_for_claim"])}

## Source Charge Rows

{md_table(tables["charge"], ["charge_id", "object", "required_law", "current_evidence", "fallback_if_open", "status", "valid_for_claim"])}

## Newton Bridge Rows

{md_table(tables["newton"], ["bridge_id", "step", "law", "requires", "result", "valid_for_claim"])}

## Drift Bound Rows

{md_table(tables["drift"], ["bound_id", "residual", "formula", "meaning", "zero_if", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "observable", "clean_branch_input", "finite_branch_projection", "required_before_claim", "claim_status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4354 Y5-R2FR Htau MHref source charge owner or finite GN drift bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4354 derives the exact local source-coupling fork. Clean branch:

```text
D_A ln G_cal = 0,
M_H^dress = H_tau[S_link] - H_ref,
int_W rho_H dV_H = M_H^dress,
nabla^2 Phi_N = 4*pi G_cal rho_H,
a_r = -G_cal M_H^dress/r^2.
```

The branch is private and conditional. Current MTS has the fair calibrated-`G` route and private `Pi_M/H_tau` glue, but no public local-GR claim until full `H_tau` integrability, fixed `H_ref`, same `tau/e_obs`, no boundary leakage, positive `M_H_ref`, and transition-shell source hair close.

If any clause opens, use `epsilon_Gsrc` as the finite no-cancellation source/coupling residual.

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        csv.writer(handle).writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4354 derives the exact H_tau/M_Href source-charge and calibrated-coupling fork. If kappa_* and Z_H are source-blind on the same branch, then D_A ln kappa_eff=0 and G_cal=c^4 kappa_eff/(8*pi) is a universal calibrated coupling. If the same-worldtube source mass is parent-owned as M_Hdress=H_tau[S_link]-H_ref, with H_tau integrable, H_ref fixed and derivative-silent, tau/frame/surface locked, boundary/radiative flux silent, Pi_M/H_tau glue adopted inside the private Hamiltonian selector, and M_H_ref positive same-frame and source-backed, then the weak-field Newton bridge follows: nabla^2 Phi_N=4*pi G_cal rho_H, Phi_N=-G_cal M_Hdress/r, a_r=-G_cal M_Hdress/r^2. This is a conditional private branch law, not a public local-GR claim. If any clause is open, epsilon_Gsrc remains as an absolute no-cancellation finite drift/source-charge bound."
                ),
                (
                    "4354 source register, coupling lock rows, source charge rows, Newton bridge rows, drift bound rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "conditional_private_newton_source_bridge_finite_Gsrc_bound_nonclaim",
                (
                    "Attack transition-shell same-worldtube membership and non-Hilbert source hair, or fill finite source-backed residual rows."
                ),
                (
                    "Numerical G_N prediction requirement at this stage; using orbital GM or measured G to define M_Hdress; globalizing private Pi_M/H_tau selector glue; cancelling unknown source/coupling residuals; claiming local GR without positive same-frame M_H_ref."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4354 Htau/MHref source charge and calibrated coupling fork

Marker: `{MARKER}`

4354 sharpens the local GR/Newton bridge into a conditional branch theorem:

```text
D_A ln kappa_eff = 0,
G_cal := c^4 kappa_eff/(8*pi),
M_H^dress = H_tau[S_link] - H_ref,
int_W rho_H dV_H = M_H^dress

=> nabla^2 Phi_N = 4*pi G_cal rho_H
=> a_r = -G_cal M_H^dress/r^2.
```

This is the fair GR-style route: MTS need not predict the numerical value of `G_N` here, but it must prove one calibrated source-blind coupling and one non-circular Hamiltonian/Hilbert source mass. Current status remains private nonclaim because full MTS `H_tau` integrability, positive same-frame `M_H_ref`, global parent selector adoption and transition source hair remain open. The fallback residual is `epsilon_Gsrc`, an absolute no-cancellation source/coupling envelope.
"""
    packet_block = f"""

## PPC4161 packet update 4354 source-coupling fork

Marker: `{PACKET_MARKER}`

Packet update: the source/coupling problem is now split cleanly. The `kappa_eff/G_cal` side is a calibrated no-drift law, while the source-mass side is the parent-owned `H_tau/H_ref/M_Hdress` theorem. `Pi_M/H_tau` glue is zero inside the private Hamiltonian selector, so the next live target is transition same-worldtube membership and non-Hilbert source hair.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    formal_text = read_text(FORMAL_PATH)
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in formal_text, MARKER))
    checks.append(("decision_in_formal", DECISION in formal_text, DECISION))
    checks.append(("clean_branch_law_present", "D_A ln kappa_eff = 0" in formal_text, "coupling zero"))
    checks.append(("newton_bridge_present", "nabla^2 Phi_N = 4*pi G_cal rho_H" in formal_text, "Poisson law"))
    checks.append(("source_charge_present", "M_H^dress[W_H;tau] = H_tau[S_link] - H_ref" in formal_text, "source charge"))
    checks.append(("finite_bound_present", "epsilon_Gsrc <=" in formal_text, "finite bound"))
    checks.append(("numeric_G_firewall_present", "not a numerical prediction of `G_N`" in formal_text, "numeric G firewall"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("coupling_rows_present", len(tables["coupling"]) >= 5, str(len(tables["coupling"]))))
    checks.append(("source_charge_rows_present", len(tables["charge"]) >= 10, str(len(tables["charge"]))))
    checks.append(("newton_rows_present", len(tables["newton"]) >= 6, str(len(tables["newton"]))))
    checks.append(("drift_rows_present", len(tables["drift"]) >= 9, str(len(tables["drift"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4354_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4354_COUPLING_LOCK_ROWS.csv",
        "P8_Y5_R2FR_4354_SOURCE_CHARGE_ROWS.csv",
        "P8_Y5_R2FR_4354_NEWTON_BRIDGE_ROWS.csv",
        "P8_Y5_R2FR_4354_DRIFT_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4354_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4354_RUNNER.csv",
        "P8_Y5_R2FR_4354_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4354_DECISION.csv",
        "P8_Y5_R2FR_4354_STATUS.csv",
        "P8_Y5_R2FR_4354_NEXT_TARGET.csv",
    ]:
        path = SOURCE_DIR / filename
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8"))) if path.exists() else []
        checks.append((f"csv_{filename}_parse_rows", bool(rows), f"{len(rows)} rows"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    write_tables(tables)
    write_docs(tables)
    append_claim_once()
    append_spine_and_packet()
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failures = [row for row in validation_rows if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 11 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
