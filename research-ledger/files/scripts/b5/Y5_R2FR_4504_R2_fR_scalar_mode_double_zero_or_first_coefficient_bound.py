from __future__ import annotations

import csv
import math
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4504"
CLAIM_ID = "L-346"
MARKER = "PPC4161_R2_FR_SCALAR_MODE_DOUBLE_ZERO_OR_FIRST_COEFFICIENT_BOUND_4504"
PACKET_MARKER = "PPC4161_PACKET_R2_FR_SCALAR_MODE_DOUBLE_ZERO_OR_FIRST_COEFFICIENT_BOUND_4504"
DECISION = "R2FR_SCALARON_GATE_EXACT_YUKAWA_HESSIAN_AND_STANDARD_BOUND_IMPORTED_MTS_COEFFICIENT_PARENT_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4505-Y5-R2FR-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"

FORMAL_PATH = FORMAL / "520-PPC4161-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"
DOC_PATH = POST / "4504-Y5-R2FR-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4504_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4504_SOURCE_REGISTER.csv"
VARIATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_R2FR_SCALARON_VARIATION_LAW.csv"
HESSIAN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_YUKAWA_HESSIAN_SLIP_TEST.csv"
ZERO_ROUTES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_ZERO_ROUTES.csv"
BOUND_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_STANDARD_BOUND_IMPORT.csv"
COEFFICIENT_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_MTS_COEFFICIENT_LAW_MERGE.csv"
FINITE_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_FINITE_BOUND_CONTRACT.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4504_DECISION.csv"

FORMAL_519 = FORMAL / "519-PPC4161-DeltaE-R11-EH-only-operator-or-first-coefficient-bound.md"
POST_4503 = POST / "4503-Y5-R2FR-DeltaE-R11-EH-only-operator-or-first-coefficient-bound.md"
SCRIPT_4503 = SCRIPT_DIR / "Y5_R2FR_4503_DeltaE_R11_EH_only_operator_or_first_coefficient_bound.py"
QUEUE_4503 = SOURCE_DIR / "P8_Y5_R2FR_4503_FIRST_COEFFICIENT_BOUND_QUEUE.csv"
ZERO_4503 = SOURCE_DIR / "P8_Y5_R2FR_4503_DELTAE_R11_ZERO_THEOREM.csv"
COMPONENT_BUDGET_4501 = SOURCE_DIR / "P8_Y5_R2FR_4501_COMPONENT_TRANSFER_BUDGET.csv"
R11_VECTOR_EXEC = SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv"
POST_4087 = POST / "4087-Y5-R2FR-first-nonEH-R11-projection-fill-gamma-beta-bound.md"
POST_4088 = POST / "4088-Y5-R2FR-map-MTS-cR2-normalization-or-Ricci-Weyl-spin2-slip-bound.md"
POST_1343 = POST / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md"
POST_4471 = POST / "4471-Y5-R2FR-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"
POST_4472 = POST / "4472-Y5-R2FR-refinement-parameter-gauge-proof-or-ellcell-source-normalization.md"
POST_4473 = POST / "4473-Y5-R2FR-no-marker-source-extension-proof-or-cell-marker-residual-row.md"
POST_4474 = POST / "4474-Y5-R2FR-external-readout-no-backreaction-proof-or-marker-coupling-fill.md"
POST_4475 = POST / "4475-Y5-R2FR-marker-bulk-coupling-zero-theorem-or-first-lambdaM-source-row.md"
POST_4476 = POST / "4476-Y5-R2FR-parent-action-inventory-signature-or-lambdaM-projection-map.md"
POST_4479 = POST / "4479-Y5-R2FR-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def rows_by(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    return {row[key]: row for row in csv_rows(path) if key in row}


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def constants() -> Dict[str, float]:
    row = rows_by(COMPONENT_BUDGET_4501, "budget_id").get("CB4501_A_E", {})
    lambda_m = 9.306372e7
    return {
        "equal_a": float(row.get("equal_no_cancellation_A_budget", "3.502129240739837e-14")),
        "single_a": float(row.get("single_survivor_A_bound", "1.400851696295935e-13")),
        "c_j2": float(row.get("rho1_abs_coefficient", "2.355709750522272e5")),
        "cassini_b_gamma": 2.3e-5,
        "beta_bound": 8.0e-5,
        "gamma_x_min": 10.274540,
        "beta_x_min": 11.960837,
        "lambda_r_m": lambda_m,
        "lambda_r_au": 6.220925e-4,
        "lambda_r_rsun": 1.337699e-1,
        "m_r_au_inv": 1.607478e3,
        "mu_bound_m2": lambda_m * lambda_m / 6.0,
    }


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4504_00_formal519", "4503 formal handoff", FORMAL_519, "R2_fR_scalar_mode", "selected first family"),
        ("SRC4504_01_post4503", "4503 post mirror", POST_4503, "R2_fR_scalar_mode", "post checkpoint target"),
        ("SRC4504_02_script4503", "4503 generator", SCRIPT_4503, 'CHECKPOINT = "4503"', "reproducible predecessor"),
        ("SRC4504_03_queue4503", "4503 coefficient queue", QUEUE_4503, "FCB4503_1_R2_fR_scalar_mode", "first coefficient queue row"),
        ("SRC4504_04_zero4503", "4503 zero theorem", ZERO_4503, "D4503_4_hessian_kill", "Hessian kill route"),
        ("SRC4504_05_r11_vector", "R11 executable vector", R11_VECTOR_EXEC, "R2_fR_scalar_mode", "retained R2/fR row"),
        ("SRC4504_06_4087_scalar_bound", "4087 standard f(R) bound", POST_4087, "m_R^2 = 1/(6 mu)", "standard scalaron mass/range"),
        ("SRC4504_07_4087_gamma", "4087 gamma derivation", POST_4087, "gamma_R2(b)", "PPN gamma formula"),
        ("SRC4504_08_4088_map_audit", "4088 MTS cR2 map audit", POST_4088, "c_R2 = conversion_factor * mu", "MTS-to-standard coefficient map issue"),
        ("SRC4504_09_1343_coeff_law", "1343 parent coefficient law", POST_1343, "LAW1343_0_quadratic_parent_block", "hidden-mode c_R2_eff law"),
        ("SRC4504_10_4471_no_grain", "4471 visible no-grain theorem", POST_4471, "NG4471_0_cell_scaling_lemma", "visible ell^2 scaling"),
        ("SRC4504_11_4472_refinement", "4472 refinement gauge contract", POST_4472, "RPG4472_6_verdict", "ell gauge parent status"),
        ("SRC4504_12_4473_marker", "4473 no-marker contract", POST_4473, "NME4473_6_verdict", "marker/source extension status"),
        ("SRC4504_13_4474_readout", "4474 readout no-backreaction", POST_4474, "ERN4474_5_curvature_vertex_zero", "curvature vertex zero condition"),
        ("SRC4504_14_4475_lambdaM", "4475 marker coupling", POST_4475, "LMB4475_0_coefficient_definition", "lambda_M action projection"),
        ("SRC4504_15_4476_projection", "4476 projection map", POST_4476, "PMAP4476_1_curvature_square", "lambda_M to c_R2 projection"),
        ("SRC4504_16_4479_shape", "4479 profile anisotropy", POST_4479, "LSS4479_4_quadrupole_bound", "anisotropic quadrupole fallback"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def variation_rows() -> List[Dict[str, object]]:
    return [
        {
            "law_id": "R2V4504_0_action",
            "object": "standard metric f(R) scalar subset",
            "formula": "S = (1/2 kappa) int sqrt(-g) [R + mu R^2] + S_m",
            "derived_result": "f_R=1+2 mu R",
            "meaning": "mu is the standard R^2 coefficient only after MTS maps c_R2_eff into this convention",
            "status": "STANDARD_TEMPLATE_NOT_MTS_CLAIM",
            "valid_for_claim": False,
        },
        {
            "law_id": "R2V4504_1_metric_variation",
            "object": "R^2 contribution to metric equations",
            "formula": "E_R2_mn = 2 mu [R R_mn - (1/4) g_mn R^2 - nabla_m nabla_n R + g_mn Box R]",
            "derived_result": "linearized Ricci-flat branch keeps derivative terms -2mu(nabla_mn R - g_mn Box R)",
            "meaning": "the dangerous local operator is a scalar-Hessian/slip channel, not a vague residual",
            "status": "DERIVED_OPERATOR_LAW",
            "valid_for_claim": False,
        },
        {
            "law_id": "R2V4504_2_trace",
            "object": "scalaron equation",
            "formula": "trace gives -R + 6 mu Box R = kappa T",
            "derived_result": "(Box - m_R^2) R = kappa T/(6 mu), with m_R^2=1/(6 mu)",
            "meaning": "finite positive mu gives a propagating scalar range lambda_R=sqrt(6 mu)",
            "status": "DERIVED_SCALARON_EQUATION",
            "valid_for_claim": False,
        },
        {
            "law_id": "R2V4504_3_exterior_solution",
            "object": "static exterior scalaron",
            "formula": "(nabla^2 - m_R^2)R=0 => R=A exp(-m_R r)/r + B exp(+m_R r)/r",
            "derived_result": "asymptotic regularity kills B; A is the body/source scalar charge",
            "meaning": "exterior Ricci-flatness is not automatic; A=0, m_R infinity, or short range is required",
            "status": "DERIVED_EXTERIOR_BRANCH",
            "valid_for_claim": False,
        },
        {
            "law_id": "R2V4504_4_zero_implication",
            "object": "R2/fR local-GR gate",
            "formula": "mu=0 or F(0)=F'(0)=0 or A_body=0 or lambda_R below bounds",
            "derived_result": "those are the exact exits for the scalaron in this standard branch",
            "meaning": "q-chain-rule silence alone is not a scalaron proof",
            "status": "SCALAR_GATE_REDUCED_TO_EXACT_EXITS",
            "valid_for_claim": False,
        },
    ]


def hessian_rows() -> List[Dict[str, object]]:
    return [
        {
            "test_id": "YH4504_0_1946_zero_ode",
            "profile": "generic radial scalar f(r)",
            "quantity": "P_TF[partial_i partial_j f]",
            "formula": "(f''-f'/r)(n_i n_j-delta_ij/3)",
            "result": "zero iff f''=f'/r, so f=a r^2+b",
            "implication": "bounded/decaying local scalar is silent only if constant or zero-charge/common-mode",
            "valid_for_claim": False,
        },
        {
            "test_id": "YH4504_1_yukawa_derivative",
            "profile": "f(r)=A exp(-m r)/r",
            "quantity": "f''-f'/r",
            "formula": "A exp(-m r)(m^2/r + 3m/r^2 + 3/r^3)",
            "result": "nonzero for finite A and finite r",
            "implication": "a live scalaron tail fails the Hessian silence route; it must be absent/source-silent/short-ranged/bounded",
            "valid_for_claim": False,
        },
        {
            "test_id": "YH4504_2_infinite_mass",
            "profile": "m_R -> infinity at fixed exterior r",
            "quantity": "A exp(-m_R r)/r",
            "formula": "lim_{m_R r -> infinity} exp(-m_R r)=0",
            "result": "scalar tail exponentially suppressed",
            "implication": "short-range bound is an empirical substitute for parent-zero, not a derivation of mu=0",
            "valid_for_claim": False,
        },
        {
            "test_id": "YH4504_3_source_charge_zero",
            "profile": "A_body=0",
            "quantity": "R_exterior",
            "formula": "R=A_body exp(-m_R r)/r",
            "result": "R_exterior=0 for the scalaron branch",
            "implication": "source/body-charge silence is as important as coefficient silence",
            "valid_for_claim": False,
        },
    ]


def zero_route_rows() -> List[Dict[str, object]]:
    return [
        {
            "route_id": "ZR4504_0_double_zero_selector",
            "zero_condition": "mu(Z)=O(Z^2) and Z=0 on the local branch",
            "derivation": "delta[mu(Z)R^2]=mu delta(R^2)+mu' R^2 delta Z; both terms vanish when mu(0)=mu'(0)=0",
            "current_status": "SELECTOR_THEOREM_CONDITIONAL_ACTUAL_PARENT_SELECTOR_UNSIGNED",
            "what_it_kills": "bare/visible R2 operator first variation",
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4504_1_cR2_eff_zero",
            "zero_condition": "c_R2_eff_total=c_cell+c_bare+0.5 B^T L^-1 B+c_measure+c_boundary=0 by parent identity",
            "derivation": "1343 coefficient law says hidden modes regenerate R^2 unless every component is zero/topological/identity-cancelled",
            "current_status": "PARENT_ZERO_SIGNATURE_UNSIGNED",
            "what_it_kills": "effective scalaron coefficient",
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4504_2_no_grain_refinement",
            "zero_condition": "ell is gauge refinement, c2 smooth, no singular running and no hidden residue",
            "derivation": "visible cell R2 term scales as ell^2 relative to EH and vanishes in the cylindrical refinement limit",
            "current_status": "VISIBLE_COMPONENT_DERIVED_TOTAL_ZERO_UNSIGNED",
            "what_it_kills": "visible c_R2_cell only, unless residue clauses also sign",
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4504_3_no_marker_action_inventory",
            "zero_condition": "Pi_{I_M}(S_bulk)=0 and no finite J/spurion/auxiliary/boundary escape route",
            "derivation": "4475/4476 turn marker coupling into an action-ideal projection; empty marker ideal gives lambda_M=0",
            "current_status": "INVENTORY_SIGNATURE_UNSIGNED",
            "what_it_kills": "marker-induced c_R2_marker and source coupling",
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4504_4_source_charge_zero",
            "zero_condition": "A_body=0 or C_total=0 for the scalaron source/body charge",
            "derivation": "exterior scalar solution is proportional to body charge even when the differential equation is homogeneous outside",
            "current_status": "SOURCE_CHARGE_THEOREM_UNSIGNED",
            "what_it_kills": "exterior Yukawa scalar tail",
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4504_5_short_range_bound",
            "zero_condition": "lambda_R small enough that PPN/R10/J2 projections are below bounds",
            "derivation": "4087 standard f(R) import gives a beta-asymptotic local bound for unscreened alpha=1/3 scalar",
            "current_status": "STANDARD_BOUND_TEMPLATE_READY_MTS_MAP_UNSIGNED",
            "what_it_kills": "claim pressure from a finite but very short-range scalar, not the coefficient itself",
            "valid_for_claim": False,
        },
    ]


def standard_bound_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    gamma_y = 3.0 * c["cassini_b_gamma"] / (2.0 - c["cassini_b_gamma"])
    return [
        {
            "bound_id": "SB4504_0_gamma_exact",
            "branch": "standard metric f(R)=R+mu R^2 unscreened scalar",
            "formula": "gamma_R2(b)=(3-y)/(3+y), y=exp(-b/lambda_R), |gamma-1|=2y/(3+y)",
            "threshold": f"y <= {gamma_y:.15e}; b/lambda_R >= {c['gamma_x_min']:.6f}",
            "result": "gamma condition imported from 4087",
            "claim_status": "standard_template_only",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SB4504_1_beta_asymptotic",
            "branch": "standard quadratic-gravity 2PN scalar/f(R) limit",
            "formula": "G_eff^2 beta - 1 ~= (1/3)x exp(-x) ln(2x) + ((9 gamma_E-4)/27)x exp(-x)",
            "threshold": f"b/lambda_R >= {c['beta_x_min']:.6f}",
            "result": "beta asymptotic condition stricter than gamma in 4087",
            "claim_status": "standard_template_only",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SB4504_2_combined_range",
            "branch": "standard f(R) scalar range",
            "formula": "lambda_R=sqrt(6 mu)",
            "threshold": f"lambda_R <= {c['lambda_r_m']:.6e} m = {c['lambda_r_au']:.6e} AU = {c['lambda_r_rsun']:.6e} R_sun",
            "result": f"mu <= {c['mu_bound_m2']:.6e} m^2 if MTS uses the same normalization",
            "claim_status": "requires_MTS_mu_map_and_screening_branch",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SB4504_3_r10_alpha",
            "branch": "standard unscreened metric f(R) finite-range force",
            "formula": "alpha_eff=1/3, lambda_R=sqrt(6 mu)",
            "threshold": "must compare alpha=1/3 to a valid full alpha_bound(lambda_R) curve",
            "result": "R10 branch is structurally ready but not claim-grade without the MTS coefficient/range and curve",
            "claim_status": "curve_and_parent_map_required",
            "valid_for_claim": False,
        },
    ]


def coefficient_law_rows() -> List[Dict[str, object]]:
    return [
        {
            "law_id": "CL4504_0_total_effective",
            "quantity": "c_R2_eff_total",
            "formula": "c_R2_eff_total = c_cell + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary + c_marker",
            "source_basis": "1343 plus 4471-4476",
            "current_status": "SYMBOLIC_LAW_DERIVED_VALUES_UNSIGNED",
            "promotion_need": "each term zero/topological/boundary-routed or numeric with units/source path",
            "valid_for_claim": False,
        },
        {
            "law_id": "CL4504_1_visible_cell",
            "quantity": "c_cell",
            "formula": "c_cell = xi_shape*c2_visible*ell_cell^2/N_EH",
            "source_basis": "4471/4472",
            "current_status": "VISIBLE_SCALING_DERIVED_ELL_GAUGE_UNSIGNED",
            "promotion_need": "prove ell is gauge and no singular residue, or source ell_cell/c2_visible/xi_shape/N_EH",
            "valid_for_claim": False,
        },
        {
            "law_id": "CL4504_2_hidden_mode",
            "quantity": "0.5 B^T L^-1 B",
            "formula": "hidden X with B_X X R gives R L_X^-1 R after elimination",
            "source_basis": "1343",
            "current_status": "CURVATURE_VERTEX_BLOCKER_IDENTIFIED",
            "promotion_need": "prove B_X=0/no XR vertex and no source/frame transfer, or source Z_X,M_X^2,B_X,C_X",
            "valid_for_claim": False,
        },
        {
            "law_id": "CL4504_3_marker",
            "quantity": "c_marker",
            "formula": "c_R2_marker=lambda_M*(zeta_R2*mu0_M+zeta_R2_grad*mu2_M/L_loc^2)/N_EH + c_marker_aux + c_marker_boundary",
            "source_basis": "4476/4479",
            "current_status": "PROJECTION_LAW_DERIVED_MOMENTS_UNSIGNED",
            "promotion_need": "prove marker ideal empty or source lambda_M, moments, projectors and anisotropy bounds",
            "valid_for_claim": False,
        },
        {
            "law_id": "CL4504_4_standard_mu_map",
            "quantity": "mu",
            "formula": "mu = N_MTS_to_fR * c_R2_eff_total",
            "source_basis": "4088 map audit",
            "current_status": "CONVERSION_FACTOR_NOT_PARENT_OWNED",
            "promotion_need": "declare and source the exact action normalization converting MTS c_R2_eff into standard f(R) mu",
            "valid_for_claim": False,
        },
    ]


def finite_contract_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "FB4504_0_local_AE_gate",
            "target": "4502 A_E equal budget",
            "formula": f"||W_STF||_1 ||K_2^X|| |c_R2_eff_total| N_R2_fR_scalar_mode <= {c['equal_a']:.15e}",
            "needed_inputs": "W_STF; K_2^X; N_R2_fR_scalar_mode; c_R2_eff_total or zero certificate",
            "status": "FORMULA_READY_VALUES_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "FB4504_1_standard_mu_bound",
            "target": "PPN scalar range template",
            "formula": f"if mu=N_MTS_to_fR*c_R2_eff_total in standard units, mu <= {c['mu_bound_m2']:.6e} m^2",
            "needed_inputs": "N_MTS_to_fR; c_R2_eff_total; screening/body-charge branch",
            "status": "STANDARD_BOUND_READY_MTS_MAP_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "FB4504_2_R10_curve",
            "target": "R10 finite-range alpha(lambda)",
            "formula": "lambda_R=sqrt(6 mu), alpha_eff=1/3*C_body^2 or declared screened/body-charge value",
            "needed_inputs": "valid full alpha_bound(lambda); mu; C_body/screening; source path",
            "status": "CURVE_BRANCH_READY_INPUTS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "FB4504_3_yukawa_hessian",
            "target": "Hessian/DeltaE_R11 scalar tail",
            "formula": "|A_body| exp(-m r)(m^2/r+3m/r^2+3/r^3) times projector/normalization <= residual budget",
            "needed_inputs": "A_body; m_R; support radius r; projector normalization; no-cancellation convention",
            "status": "HESSIAN_BOUND_FORMULA_DERIVED_INPUTS_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4504_0_double_zero_selector",
            "clause": "actual R2/fR coefficient has parent-owned double-zero selector",
            "current_status": "UNSIGNED",
            "evidence": str(ZERO_4503),
            "effect": "without this, the R2/fR first variation can survive",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4504_1_cR2_total_zero",
            "clause": "all c_R2_eff_total components vanish or are identity/topological/boundary-routed",
            "current_status": "UNSIGNED",
            "evidence": str(POST_1343),
            "effect": "hidden curvature-linear vertices can regenerate R2 after elimination",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4504_2_refinement_no_grain",
            "clause": "ell is gauge refinement with no marker, singular running, or hidden residue",
            "current_status": "VISIBLE_COMPONENT_DERIVED_TOTAL_UNSIGNED",
            "evidence": str(POST_4471),
            "effect": "visible c_cell can vanish but total c_R2_eff remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4504_3_marker_inventory",
            "clause": "marker ideal is empty or lambda_M projection is zero",
            "current_status": "UNSIGNED",
            "evidence": str(POST_4476),
            "effect": "marker/source readout can generate c_R2_marker if material",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4504_4_source_charge",
            "clause": "scalaron body/source charge A_body or C_total vanishes",
            "current_status": "UNSIGNED",
            "evidence": str(POST_1343),
            "effect": "finite scalar coefficient may still produce exterior Yukawa field",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4504_5_MTS_mu_map",
            "clause": "MTS c_R2_eff is mapped to standard f(R) mu with units/sign/frame",
            "current_status": "UNSIGNED",
            "evidence": str(POST_4088),
            "effect": "standard PPN/R10 bounds cannot be claimed as MTS bounds yet",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4504_0_variation_law",
            "gate": "standard R2/fR scalaron equation derived",
            "passed": True,
            "claim_allowed": False,
            "detail": "metric variation, trace equation and exterior Yukawa branch are explicit",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4504_1_hessian_test",
            "gate": "Yukawa Hessian silence tested",
            "passed": True,
            "claim_allowed": False,
            "detail": "live Yukawa scalar gives nonzero f''-f'/r; it must be absent, source-silent, short-ranged or bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4504_2_standard_bound_import",
            "gate": "4087 standard scalar bound imported",
            "passed": True,
            "claim_allowed": False,
            "detail": "standard f(R) bound is available only as a template until MTS coefficient/range map signs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4504_3_MTS_parent_zero",
            "gate": "MTS c_R2_eff or source charge parent-zero signed",
            "passed": False,
            "claim_allowed": False,
            "detail": "c_R2_eff total, marker inventory, source charge and MTS-to-mu normalization remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4504_4_local_GR_promotion",
            "gate": "local GR/R2 scalar branch promoted",
            "passed": False,
            "claim_allowed": False,
            "detail": "4504 narrows the branch but does not claim local GR, PPN, R10 or J2 safety",
            "valid_for_claim": False,
        },
    ]


def status_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "variation_law_derived": True,
            "yukawa_hessian_test_derived": True,
            "standard_bound_imported": True,
            "MTS_cR2_parent_zero_signed": False,
            "MTS_mu_map_signed": False,
            "local_GR_claim": False,
            "first_open_component": "c_R2_eff_total_or_scalaron_body_charge",
            "equal_AE_budget": f"{c['equal_a']:.15e}",
            "standard_mu_bound_m2": f"{c['mu_bound_m2']:.6e}",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4504_0",
            "target": NEXT_TARGET,
            "preferred_route": "prove c_R2_eff_total=0 by parent action inventory/no-XR/no-marker/no-residue, or prove scalaron body charge A_body=0",
            "fallback_route": "source c_R2_eff_total, MTS-to-mu normalization, body charge/screening and run the PPN/R10/A_E finite gates",
            "do_not_do": "use exterior Ricci-flatness, absence of a table, or standard f(R) bound as an MTS local-GR proof",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "what_moved_forward": "4504 derives the standard R2/fR scalaron equation and the exact Yukawa Hessian failure of the scalar-Hessian silence route.",
            "what_is_derived": "live f(R) scalar tails are non-silent unless coefficient/source charge is zero or the range is short enough; standard PPN beta/gamma range bounds are imported as guarded templates.",
            "what_remains_blocked": "MTS has not parent-signed c_R2_eff_total=0, scalaron body-charge zero, marker inventory silence, or the conversion from c_R2_eff_total to standard mu.",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def append_section_once(path: Path, marker: str, section: str) -> None:
    body = text(path)
    if marker in body:
        return
    path.write_text(body.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    claim = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_scalaron",
        "claim": "4504 derives the R2/fR scalaron variation, proves a live Yukawa scalar fails the Hessian silence route, imports the standard PPN scalar range bound as a guarded template, and reduces MTS promotion to c_R2_eff/source-charge/mu-map signatures.",
        "current_evidence": "4504 source register, scalaron variation law, Yukawa Hessian slip test, zero routes, standard bound import, MTS coefficient law merge, finite bound contract, parent audit, gates, status and validation.",
        "status": "private_R2FR_scalaron_gate_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "treating standard f(R) formulas or exterior Ricci-flatness as an MTS parent-zero proof.",
        "sector": "local_gr_newton_r2fr_scalaron",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "c_R2_eff_total, scalaron body charge and MTS-to-mu normalization remain unsigned.",
    }
    rows = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(claim)


def generated_csv_paths() -> List[Path]:
    return [
        SOURCE_REGISTER,
        VARIATION_CSV,
        HESSIAN_CSV,
        ZERO_ROUTES_CSV,
        BOUND_IMPORT_CSV,
        COEFFICIENT_LAW_CSV,
        FINITE_CONTRACT_CSV,
        PARENT_AUDIT_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]


def claim_flags_safe(rows: Iterable[Mapping[str, object]]) -> bool:
    for row in rows:
        for key in ("valid_for_claim", "claim_allowed"):
            if str(row.get(key, "")).lower() == "true":
                return False
    return True


def validation_rows(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    sources = all_rows["sources"]
    csv_ok = True
    csv_detail: List[str] = []
    for path in generated_csv_paths():
        try:
            parsed = csv_rows(path)
            if not parsed:
                csv_ok = False
                csv_detail.append(f"{path.name}:empty")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{path.name}:{exc}")

    flat_rows: List[Mapping[str, object]] = []
    for rows in all_rows.values():
        flat_rows.extend(rows)

    checks = [
        {
            "validation_id": "VAL4504_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_01_variation",
            "status": "PASS" if any("m_R^2=1/(6 mu)" in str(row.get("derived_result", "")) for row in all_rows["variation"]) else "FAIL",
            "detail": "scalaron trace equation and mass law derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_02_hessian",
            "status": "PASS" if any("m^2/r + 3m/r^2 + 3/r^3" in str(row.get("formula", "")) for row in all_rows["hessian"]) else "FAIL",
            "detail": "Yukawa Hessian non-silence formula recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_03_bound_import",
            "status": "PASS" if any(row.get("bound_id") == "SB4504_2_combined_range" for row in all_rows["bounds"]) else "FAIL",
            "detail": "standard f(R) combined range/mu bound imported as template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_04_coefficient_law",
            "status": "PASS" if any(row.get("quantity") == "c_R2_eff_total" for row in all_rows["coeff"]) else "FAIL",
            "detail": "MTS effective coefficient law merged from prior work",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_05_parent_audit_blocks_claim",
            "status": "PASS" if all(row.get("current_status") != "SIGNED" for row in all_rows["parent"]) else "FAIL",
            "detail": "parent zero/mu-map/source-charge signatures remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_06_claim_flags_safe",
            "status": "PASS" if claim_flags_safe(flat_rows) else "FAIL",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_07_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows" if csv_ok else "; ".join(csv_detail),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_08_next_target",
            "status": "PASS" if all_rows["next"] and all_rows["next"][0]["target"] == NEXT_TARGET else "FAIL",
            "detail": "4505 c_R2 effective zero/source-charge target selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4504_09_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4504_OVERALL",
            "status": overall,
            "detail": "4504 R2/fR scalar mode double-zero or first coefficient bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def build_doc(
    sources: Sequence[Mapping[str, object]],
    variation: Sequence[Mapping[str, object]],
    hessian: Sequence[Mapping[str, object]],
    zero_routes: Sequence[Mapping[str, object]],
    bounds: Sequence[Mapping[str, object]],
    coeff: Sequence[Mapping[str, object]],
    finite: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    c = constants()
    return f"""# 4504 - R2/fR Scalar Mode Double-Zero Or First Coefficient Bound

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4504 takes the `R2_fR_scalar_mode` target and turns it into an exact scalaron gate.

For the standard metric branch `f(R)=R+mu R^2`, the trace equation is

`(Box - m_R^2) R = kappa T/(6 mu)`, with `m_R^2=1/(6 mu)` and `lambda_R=sqrt(6 mu)`.

The exterior solution is Yukawa-like, `R=A_body exp(-m_R r)/r`. That is important because the 1946 Hessian silence test does not let this hide: for `f=A exp(-m r)/r`,

`f''-f'/r = A exp(-m r)(m^2/r + 3m/r^2 + 3/r^3)`.

So a live scalaron tail is not locally silent. It needs one of four honest exits: parent-zero coefficient, parent-zero body/source charge, short-range empirical suppression, or a fully sourced finite bound. The standard 4087 PPN template gives `lambda_R <= {c['lambda_r_m']:.6e} m` and `mu <= {c['mu_bound_m2']:.6e} m^2`, but this is not yet an MTS result because `c_R2_eff_total -> mu` is not parent-owned.

## Source Register

{table(sources)}

## Scalaron Variation Law

{table(variation)}

## Yukawa Hessian Slip Test

{table(hessian)}

## Zero Routes

{table(zero_routes)}

## Standard Bound Import

{table(bounds)}

## MTS Coefficient Law Merge

{table(coeff)}

## Finite Bound Contract

{table(finite)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    c = constants()
    sources = source_rows()
    variation = variation_rows()
    hessian = hessian_rows()
    zero_routes = zero_route_rows()
    bounds = standard_bound_rows(c)
    coeff = coefficient_law_rows()
    finite = finite_contract_rows(c)
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows(c)
    next_target = next_rows()
    decisions = decision_rows()

    all_rows = {
        "sources": sources,
        "variation": variation,
        "hessian": hessian,
        "zero": zero_routes,
        "bounds": bounds,
        "coeff": coeff,
        "finite": finite,
        "parent": parent,
        "gates": gates,
        "status": status,
        "next": next_target,
        "decisions": decisions,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(VARIATION_CSV, variation)
    write_csv(HESSIAN_CSV, hessian)
    write_csv(ZERO_ROUTES_CSV, zero_routes)
    write_csv(BOUND_IMPORT_CSV, bounds)
    write_csv(COEFFICIENT_LAW_CSV, coeff)
    write_csv(FINITE_CONTRACT_CSV, finite)
    write_csv(PARENT_AUDIT_CSV, parent)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validation_rows(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, variation, hessian, zero_routes, bounds, coeff, finite, parent, gates, status, next_target, decisions, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)

    append_claim_once()
    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4504 R2/fR Scalar Mode Double-Zero Or First Coefficient Bound

Marker: `{MARKER}`  
4504 turns `R2_fR_scalar_mode` into an exact scalaron gate. In the standard branch `f(R)=R+mu R^2`, the trace equation gives `m_R^2=1/(6mu)` and exterior `R=A_body exp(-m_R r)/r`. The Yukawa profile fails the Hessian silence test because `f''-f'/r=A_body exp(-m_R r)(m_R^2/r+3m_R/r^2+3/r^3)`. Thus the branch closes only by parent-zero coefficient, parent-zero body/source charge, short-range empirical suppression, or a sourced finite bound. The standard template bound is `mu <= {c['mu_bound_m2']:.6e} m^2`, but MTS promotion needs a parent-owned `c_R2_eff_total -> mu` map.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4504 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has a hard scalaron test instead of a vague R2/fR gap. A live Yukawa scalar tail is not Hessian-silent; it must be killed by coefficient/source-charge zero or scored through the PPN/R10/A_E finite gates. Next target: prove `c_R2_eff_total=0` or `A_body=0`, otherwise source the `c_R2_eff_total -> mu` normalization and body-charge branch.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
