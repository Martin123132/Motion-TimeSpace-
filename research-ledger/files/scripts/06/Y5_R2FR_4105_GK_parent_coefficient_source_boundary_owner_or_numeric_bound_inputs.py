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
DOC_PATH = ROOT / "4105-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_GK_INPUT_GATE_4105"
CHECKPOINT_ID = "4105"
DECISION = (
    "GK_INPUTS_AUDITED_LAMBDA_UNSIGNED_NONCOERCIVE_AND_ABSORPTION_ROUTES_"
    "IMPORTED_SOURCE_COUPLING_PIVOT_SELECTED"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4105_00_4104_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4104_NEXT_TARGET.csv",
        "4105-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md",
        "4104 selects the GK parent-input gate as the next concrete task.",
    ),
    "SRC4105_01_4104_gk_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS.csv",
        "epsilon_GK_hair",
        "4104 imports the GK theorem-or-bound channel and names its inputs.",
    ),
    "SRC4105_02_3587_owner": (
        SOURCE_DIR / "P8_Y5_R2FR_3587_GK_INPUT_OWNER_MATRIX.csv",
        "GIO3587_0_lambda_GK",
        "3587 stages the GK input owner matrix.",
    ),
    "SRC4105_03_3587_candidate": (
        SOURCE_DIR / "P8_Y5_R2FR_3587_GK_CANDIDATE_BOUND_INPUT_ROWS.csv",
        "GIB3587_0_lambda_GK_candidate",
        "3587 records candidate values/blockers for GK inputs.",
    ),
    "SRC4105_04_3587_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3587_STATUS.csv",
        "GK_INPUTS_STAGED_NOT_SIGNED_OR_NUMERIC",
        "3587 status: GK inputs are staged but not signed or numeric.",
    ),
    "SRC4105_05_3588_lambda": (
        SOURCE_DIR / "P8_Y5_R2FR_3588_LAMBDA_GK_SIGNATURE_ATTEMPT.csv",
        "LAMB3588_6_verdict",
        "3588 audits the exact lambda_GK positivity condition.",
    ),
    "SRC4105_06_3588_switch": (
        SOURCE_DIR / "P8_Y5_R2FR_3588_NONCOERCIVE_SWITCH_ROWS.csv",
        "NCS3588_0_branch_decision",
        "3588 switches away from the coercive denominator route.",
    ),
    "SRC4105_07_3589_input_pack": (
        SOURCE_DIR / "P8_Y5_R2FR_3589_NONCOERCIVE_INPUT_PACK.csv",
        "NCI3589_6_F_outer_GK_abs",
        "3589 builds the finite noncoercive GK input pack.",
    ),
    "SRC4105_08_3589_finite_epsilon": (
        SOURCE_DIR / "P8_Y5_R2FR_3589_FIRST_FINITE_EPSILON_ROW.csv",
        "FFE3589_2_epsilon_GK_hair_nc",
        "3589 derives the first finite noncoercive epsilon row.",
    ),
    "SRC4105_09_3590_absorption": (
        SOURCE_DIR / "P8_Y5_R2FR_3590_ABSORPTION_THEOREM.csv",
        "ABS3590_2_absorbed_bound",
        "3590 derives the absorption theorem for quadratic GK defects.",
    ),
    "SRC4105_10_3590_branch": (
        SOURCE_DIR / "P8_Y5_R2FR_3590_BRANCH_VERDICT.csv",
        "BV3590_3_demoted_residual_parameter",
        "3590 demotes GK finite hair to an explicit residual when eta/F0 are unsigned.",
    ),
    "SRC4105_11_3591_gm_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_3591_GM_TRANSFER_CONTRACT.csv",
        "GMT3591_3_Hamiltonian_equals_Hilbert_mass",
        "3591 gives the exact GM transfer contract and central charge equality.",
    ),
    "SRC4105_12_3591_epsilon_mu": (
        SOURCE_DIR / "P8_Y5_R2FR_3591_EPSILON_MU_RESIDUAL_CONTRACT.csv",
        "EMU3591_8_epsilon_mu_total",
        "3591 propagates unclosed source coupling as epsilon_mu.",
    ),
    "SRC4105_13_3591_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3591_NEXT_TARGET.csv",
        "3592-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md",
        "3591 selects Pi_M-Hilbert charge equality as the next high-value target.",
    ),
    "SRC4105_14_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4105_GK_parent_coefficient_source_boundary_owner_or_numeric_bound_inputs.py",
        "Reproducible generator for this 4105 checkpoint.",
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
    with path.open(newline="", encoding="utf-8-sig") as handle:
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


def gk_input_owner_rows() -> List[dict]:
    entries = [
        (
            "GIO4105_0_lambda_GK",
            "lambda_GK",
            "min(Z_A*lambda1_A + m_A2, Z_G*lambda1_G + m_G2) - abs(c_AG)*C_cross",
            "coercive denominator / operator lower-bound owner",
            "UNSIGNED_POSITIVITY_IMPORTED_DO_NOT_SPEND",
            "Z_A,Z_G,m_A2,m_G2,c_AG,lambda1_A,lambda1_G,C_cross,domain_id,norm_id",
            "positive denominator route is blocked; use only as a conditional theorem clause",
            "SRC4105_05_3588_lambda",
        ),
        (
            "GIO4105_1_J_GK_norm",
            "J_GK_norm",
            "||(J_A,J_gamma)||_* in the selected GK domain",
            "source/current owner",
            "FINITE_INPUT_OR_ZERO_SOURCE_REQUIRED",
            "parent source-zero theorem or finite dual source norm with units",
            "enters a_GK on the finite branch and epsilon_mu via source residuals",
            "SRC4105_02_3587_owner",
        ),
        (
            "GIO4105_2_Phi_boundary_GK",
            "Phi_boundary_GK",
            "absolute GK boundary/symplectic flux after integration by parts",
            "boundary/reference owner",
            "FINITE_INPUT_OR_ZERO_BOUNDARY_REQUIRED",
            "self-adjoint domain, reference lock, boundary flux value or zero theorem",
            "enters a_GK and F0_GK_abs; cannot be erased by local projection",
            "SRC4105_07_3589_input_pack",
        ),
        (
            "GIO4105_3_Q_top_GK",
            "Q_top_GK",
            "topological/projector/gauge-kernel charge not controlled by local coercivity",
            "topology/projector owner",
            "FINITE_INPUT_OR_TOPOLOGY_ZERO_REQUIRED",
            "relative cohomology lock, projector kernel audit, gauge fix or finite value",
            "topology is a real escape channel, not a cosmetic missing parameter",
            "SRC4105_07_3589_input_pack",
        ),
        (
            "GIO4105_4_K_GK",
            "K_GK",
            "operator-to-observable map from GK amplitude to selected local residual",
            "arena projection owner",
            "OPERATOR_TO_OBSERVABLE_MAP_REQUIRED",
            "R10/PPN/clock/orbital kernels, units, and source paths",
            "without K_GK no empirical score can be claim-grade",
            "SRC4105_07_3589_input_pack",
        ),
        (
            "GIO4105_5_X_GK_residual",
            "X_GK_residual",
            "explicit local residual amplitude carried after eta_GK/F0_GK_abs fail to close",
            "residual propagation owner",
            "STRUCTURAL_NON_SCORE_READY_RESIDUAL",
            "eta_GK<1 or noncircular F0_GK_abs, plus K_GK map, if the residual is to become a bound",
            "prevents another loop that pretends the GK input pack is score-ready",
            "SRC4105_10_3590_branch",
        ),
    ]
    return [
        {
            **row_base(),
            "input_id": input_id,
            "symbol": symbol,
            "definition_or_formula": formula,
            "owner_type": owner_type,
            "status": status,
            "required_inputs": required,
            "route_decision": route_decision,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for input_id, symbol, formula, owner_type, status, required, route_decision, source_key in entries
    ]


def lambda_positivity_rows() -> List[dict]:
    entries = [
        (
            "LAMB4105_0_exact_formula",
            "lambda_GK",
            "lambda_GK = min(Z_A*lambda1_A + m_A2, Z_G*lambda1_G + m_G2) - abs(c_AG)*C_cross",
            "exact sufficient lower-bound form imported from the older GK chain",
            "FORMULA_AVAILABLE_CONDITIONAL",
            "SRC4105_05_3588_lambda",
        ),
        (
            "LAMB4105_1_diagonal_signs",
            "Z_A,Z_G,m_A2,m_G2",
            "Z_A>0, Z_G>0, m_A2>=0, m_G2>=0",
            "positive kinetic/mass signs are requirements, not parent-owned values",
            "MISSING_PARENT_SIGNATURE",
            "SRC4105_05_3588_lambda",
        ),
        (
            "LAMB4105_2_domain_floor",
            "lambda1_A,lambda1_G",
            "positive Poincare/domain floors after boundary, gauge and topology quotient",
            "domain constants and kernel removal are not parent-signed",
            "MISSING_DOMAIN_AND_QUOTIENT_LOCK",
            "SRC4105_05_3588_lambda",
        ),
        (
            "LAMB4105_3_cross_smallness",
            "c_AG,C_cross",
            "abs(c_AG)*C_cross < min(Z_A*lambda1_A + m_A2, Z_G*lambda1_G + m_G2)",
            "cross-term smallness is a formal Schur/Young condition, not sourced as a coefficient row",
            "MISSING_CROSS_TERM_BOUND",
            "SRC4105_05_3588_lambda",
        ),
        (
            "LAMB4105_4_dynamical_lock",
            "Lorentzian stability and physical residual lock",
            "stationary positive energy must come from a stable parent action and control measured residuals",
            "local positivity alone is not a full physical theorem",
            "MISSING_LORENTZIAN_AND_OBSERVABLE_LOCK",
            "SRC4105_05_3588_lambda",
        ),
        (
            "LAMB4105_5_verdict",
            "positive-denominator policy",
            "do not use 1/lambda_GK, lambda_GK>0, or the coercive GK no-hair theorem as active evidence",
            "using lambda_GK as positive would be a hidden closure axiom",
            "COERCIVE_ROUTE_BLOCKED_NONCLAIM",
            "SRC4105_06_3588_switch",
        ),
    ]
    return [
        {
            **row_base(),
            "audit_id": audit_id,
            "symbol": symbol,
            "formula_or_condition": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "uses_positive_lambda_denominator": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, symbol, formula, meaning, status, source_key in entries
    ]


def noncoercive_pack_rows() -> List[dict]:
    entries = [
        (
            "NCP4105_0_a_GK",
            "a_GK",
            "a_GK = C_Poincare_GK*J_GK_norm + C_trace_GK*abs(Phi_boundary_GK) + C_top_GK*abs(Q_top_GK)",
            "linear finite branch forcing collected by duality/trace/topology constants",
            "DERIVED_SYMBOLIC_NONCLAIM",
            "SRC4105_08_3589_finite_epsilon",
        ),
        (
            "NCP4105_1_X_GK_bound_nc",
            "X_GK_bound_nc",
            "X_GK <= 0.5*(a_GK + sqrt(a_GK^2 + 4*F_outer_GK_abs))",
            "first finite noncoercive amplitude law before quadratic-defect absorption",
            "DERIVED_SYMBOLIC_INPUTS_MISSING",
            "SRC4105_08_3589_finite_epsilon",
        ),
        (
            "NCP4105_2_epsilon_GK_hair_nc",
            "epsilon_GK_hair_nc",
            "epsilon_GK_hair_nc <= K_GK*X_GK_bound_nc",
            "noncoercive observable residual row without using lambda_GK",
            "FIRST_FINITE_EPSILON_ROW_NONCLAIM",
            "SRC4105_08_3589_finite_epsilon",
        ),
        (
            "NCP4105_3_required_inputs",
            "finite noncoercive input pack",
            "C_Poincare_GK,C_trace_GK,C_top_GK,J_GK_norm,Phi_boundary_GK,Q_top_GK,F_outer_GK_abs,K_GK,domain_id,norm_id,units",
            "input pack is complete as a source contract but not numeric/claim-ready",
            "SOURCE_READY_VALUES_MISSING",
            "SRC4105_07_3589_input_pack",
        ),
        (
            "NCP4105_4_no_loop_rule",
            "GK branch workflow rule",
            "do not refill the same noncoercive input pack again unless a new parent source or numeric value appears",
            "prevents circling and forces the next step onto absorption/source coupling",
            "PASS_GUARD",
            "SRC4105_10_3590_branch",
        ),
    ]
    return [
        {
            **row_base(),
            "pack_id": pack_id,
            "symbol": symbol,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "uses_positive_lambda_denominator": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for pack_id, symbol, formula, meaning, status, source_key in entries
    ]


def absorption_residual_rows() -> List[dict]:
    entries = [
        (
            "ABS4105_0_absorption_inequality",
            "X_GK",
            "X_GK^2 <= a_GK*X_GK + F0_GK_abs + eta_GK*X_GK^2",
            "lawful way to handle quadratic GK/cross/projector defects",
            "DERIVED_IMPORTED",
            "SRC4105_09_3590_absorption",
        ),
        (
            "ABS4105_1_absorbed_bound",
            "X_GK_absorbed_bound",
            "X_GK <= [a_GK + sqrt(a_GK^2 + 4*(1-eta_GK)*F0_GK_abs)]/[2*(1-eta_GK)]",
            "exact bound if eta_GK<1 and F0_GK_abs is noncircular",
            "CONDITIONAL_FORMULA_AVAILABLE",
            "SRC4105_09_3590_absorption",
        ),
        (
            "ABS4105_2_eta_gate",
            "eta_GK<1",
            "eta_GK = eta_cross_GK + eta_projector_GK + eta_boundary_feedback_GK + eta_metric_response_GK",
            "strict smallness is not parent-signed in the current corpus",
            "FAIL_CURRENT_SCORE",
            "SRC4105_10_3590_branch",
        ),
        (
            "ABS4105_3_F0_gate",
            "F0_GK_abs",
            "F_source_tail_GK_abs + F_boundary_fixed_GK_abs + F_topology_fixed_GK_abs + F_geometry_background_GK_abs",
            "fixed outer work must be independent of X_GK and source-backed",
            "FAIL_CURRENT_SCORE",
            "SRC4105_10_3590_branch",
        ),
        (
            "ABS4105_4_residual_contract",
            "X_GK_residual",
            "retain GK finite hair as an explicit residual parameter carried into source/Newton/PPN tests",
            "do this rather than recycling the GK input-pack search",
            "STRUCTURAL_NON_SCORE_READY_RESIDUAL",
            "SRC4105_10_3590_branch",
        ),
    ]
    return [
        {
            **row_base(),
            "residual_id": residual_id,
            "symbol": symbol,
            "formula_or_contract": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for residual_id, symbol, formula, meaning, status, source_key in entries
    ]


def source_coupling_pivot_rows() -> List[dict]:
    entries = [
        (
            "PIV4105_0_pivot_reason",
            "why leave the GK loop now",
            "3587-3590 already stage GK inputs, reject unsigned lambda positivity, derive the noncoercive law, and derive the eta absorption law.",
            "The remaining blocker is not another name for a GK input; it is whether the residual/source charge is calibrated into Newtonian GM.",
            "GK_LOOP_EXIT_JUSTIFIED",
            "SRC4105_10_3590_branch",
        ),
        (
            "PIV4105_1_GM_transfer_contract",
            "Newtonian GM bridge",
            "all clauses close => mu_obs = G_ref*M_H, epsilon_mu=0, and a_r=-G_ref*M_H/r^2",
            "This is the real GR/Newton route: not just an EH-looking equation with fitted GM.",
            "EXACT_CONTRACT_IMPORTED_NOT_ACTIVATED",
            "SRC4105_11_3591_gm_contract",
        ),
        (
            "PIV4105_2_central_equality",
            "Pi_M J_H equals Hamiltonian/Hilbert mass charge",
            "B_xi/G_ref = M_H[Pi_M J_H], with projector variation handled before readout",
            "This is the shortest high-value source-coupling clause to attack next.",
            "NEXT_DERIVATION_TARGET",
            "SRC4105_11_3591_gm_contract",
        ),
        (
            "PIV4105_3_residual_vector",
            "epsilon_mu",
            "epsilon_mu = epsilon_frame + epsilon_current + epsilon_flux + epsilon_extra + epsilon_GK_source + epsilon_operator + epsilon_calibration + epsilon_PPN_source",
            "If the equality cannot be proved yet, propagate the residual honestly into Newton/PPN/R10.",
            "RESIDUAL_PROPAGATION_READY_VALUES_MISSING",
            "SRC4105_12_3591_epsilon_mu",
        ),
    ]
    return [
        {
            **row_base(),
            "pivot_id": pivot_id,
            "target": target,
            "formula_or_reason": formula,
            "meaning": meaning,
            "status": status,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for pivot_id, target, formula, meaning, status, source_key in entries
    ]


def decision_rows() -> List[dict]:
    entries = [
        (
            "DEC4105_0_input_gate",
            "accept the GK input owner matrix as staged",
            "the concrete inputs are lambda_GK, J_GK_norm, Phi_boundary_GK, Q_top_GK, K_GK, and X_GK_residual",
            "GK no-hair is not generic anymore, but the claim route remains blocked",
            "INPUT_GATE_STAGED",
            "SRC4105_02_3587_owner",
        ),
        (
            "DEC4105_1_lambda_policy",
            "do not spend lambda_GK as a positive denominator",
            "the exact formula exists but parent coefficient signs/domain floors/cross smallness are unsigned",
            "coercive GK theorem stays conditional only",
            "LAMBDA_POSITIVITY_UNSIGNED",
            "SRC4105_05_3588_lambda",
        ),
        (
            "DEC4105_2_noncoercive_policy",
            "retain the noncoercive finite formula as a source contract",
            "a_GK, X_GK_bound_nc and epsilon_GK_hair_nc are derived symbolically without lambda_GK",
            "score stays blocked until noncircular values and units exist",
            "NONCOERCIVE_FORMULA_IMPORTED",
            "SRC4105_08_3589_finite_epsilon",
        ),
        (
            "DEC4105_3_absorption_policy",
            "carry X_GK_residual unless eta_GK<1 or F0_GK_abs closes",
            "the exact absorption law prevents cross/projector defects from being hidden in F_outer",
            "GK finite hair becomes an explicit residual, not a loop",
            "GK_RESIDUAL_CONTRACT_ACTIVE",
            "SRC4105_09_3590_absorption",
        ),
        (
            "DEC4105_4_next",
            "pivot to Pi_M-Hilbert charge equality",
            "source coupling/Newtonian GM calibration is now higher leverage than another GK refill",
            "4106 attacks the central source-charge equality or builds epsilon_mu input rows",
            "NEXT_TARGET_SELECTED",
            "SRC4105_13_3591_next",
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
        ("CLAIM4105_0_GK_zero", "Gamma/Khat exterior hair is zero", "BLOCKED", "lambda_GK/source/boundary/topology/K_GK inputs are not parent-signed or numeric/sourced"),
        ("CLAIM4105_1_lambda_GK", "lambda_GK>0 active denominator", "BLOCKED", "positive denominator would smuggle unsigned coefficients/domain constants"),
        ("CLAIM4105_2_GK_finite_score", "finite GK epsilon score", "BLOCKED", "eta_GK<1 and noncircular F0_GK_abs are not signed; K_GK map missing"),
        ("CLAIM4105_3_Newton_GM", "Newtonian measured GM derived", "BLOCKED", "Pi_M-Hilbert/Hamiltonian charge equality and universal G_ref are not parent-signed"),
        ("CLAIM4105_4_local_GR_PPN_R10", "local GR/PPN/R10 pass", "BLOCKED", "epsilon_mu and X_GK_residual must be propagated or closed first"),
    ]
    return [
        {
            **row_base(),
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for claim_id, claim, status, reason in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4105_0",
            "target_doc": "4106-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md",
            "target_script": "scripts/Y5_R2FR_4106_PiM_Hilbert_charge_equality_or_epsilon_mu_input_pack.py",
            "objective": "attack the central source-coupling clause: derive Pi_M J_H equals the Hamiltonian/Hilbert mass charge, or build the first source-ready epsilon_mu input pack for measured-GM residuals",
            "success_gate": "B_xi/G_ref=M_H[Pi_M J_H] is parent-signed with projector variation handled, or epsilon_mu components get source/unit/input rows without Newton/PPN claims",
            "reason": "4105 prevents another GK loop; the sharpest route to GR/Newton now runs through calibrated source coupling",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4105_0",
            "decision": DECISION,
            "strongest_result": "4105 closes the immediate GK-input audit loop by importing the full older GK trail: inputs are staged, lambda_GK positivity is unsigned, the finite noncoercive formula exists, and the eta absorption law shows why unresolved GK hair must be carried as X_GK_residual rather than refilled again.",
            "what_moved_forward": "the next branch is no longer another GK missing-input pass; it is the source-coupling theorem needed to turn a weak-field/EH-looking branch into measured Newtonian GM",
            "still_missing": "Pi_M origin; Hamiltonian-Hilbert source equality; projector variation; closed source flux; universal G_ref; numeric/source-backed epsilon_mu components; K_GK_mu map; PPN/source stability",
            "public_status": "no local_GR_Newton_PPN_R10 claim",
            "next_target": "4106 Pi_M-Hilbert charge equality or epsilon_mu input pack",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4105_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4105_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4105_GK_INPUT_OWNER_MATRIX": SOURCE_DIR / "P8_Y5_R2FR_4105_GK_INPUT_OWNER_MATRIX.csv",
        "P8_Y5_R2FR_4105_LAMBDA_GK_POSITIVITY_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4105_LAMBDA_GK_POSITIVITY_AUDIT.csv",
        "P8_Y5_R2FR_4105_NONCOERCIVE_INPUT_PACK_IMPORT": SOURCE_DIR / "P8_Y5_R2FR_4105_NONCOERCIVE_INPUT_PACK_IMPORT.csv",
        "P8_Y5_R2FR_4105_ABSORPTION_RESIDUAL_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4105_ABSORPTION_RESIDUAL_CONTRACT.csv",
        "P8_Y5_R2FR_4105_SOURCE_COUPLING_PIVOT": SOURCE_DIR / "P8_Y5_R2FR_4105_SOURCE_COUPLING_PIVOT.csv",
        "P8_Y5_R2FR_4105_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4105_DECISION_GATE.csv",
        "P8_Y5_R2FR_4105_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4105_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4105_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4105_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4105_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4105_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4105 - GK parent coefficient/source/boundary owner or numeric bound inputs",
        "",
        "## Verdict",
        "4105 is deliberately not another spin around the same GK missing-input roundabout. It audits the GK input gate, imports the older resolved trail, and moves the live route forward.",
        "",
        "The result is sharp:",
        "",
        "- `lambda_GK` has an exact conditional lower-bound formula, but the signs/domain/cross/stability/observable-lock package is not parent-signed.",
        "- The coercive `1/lambda_GK` no-hair route is therefore blocked.",
        "- The noncoercive finite branch exists: `a_GK=C_Poincare_GK J_GK_norm + C_trace_GK |Phi_boundary_GK| + C_top_GK |Q_top_GK|`, `X_GK<=0.5*(a_GK+sqrt(a_GK^2+4F_outer_GK_abs))`, and `epsilon_GK_hair_nc<=K_GK X_GK`.",
        "- The absorption law also exists: from `X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2`, `eta_GK<1` gives the exact absorbed root.",
        "- Because `eta_GK<1`, `F0_GK_abs`, and `K_GK` remain unsigned, GK hair is now carried as `X_GK_residual`, not endlessly refilled.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Practical consequence",
        "The best next attack is source coupling: prove the `Pi_M J_H` to Hamiltonian/Hilbert mass-charge equality, or build the first source-ready `epsilon_mu` input pack. That is the path from an EH/weak-field branch to actual Newtonian measured `GM`.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4105_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4105_GK_INPUT_OWNER_MATRIX.csv`",
        "- `P8_Y5_R2FR_4105_LAMBDA_GK_POSITIVITY_AUDIT.csv`",
        "- `P8_Y5_R2FR_4105_NONCOERCIVE_INPUT_PACK_IMPORT.csv`",
        "- `P8_Y5_R2FR_4105_ABSORPTION_RESIDUAL_CONTRACT.csv`",
        "- `P8_Y5_R2FR_4105_SOURCE_COUPLING_PIVOT.csv`",
        "- `P8_Y5_R2FR_4105_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4105_CLAIM_GATE.csv`",
        "- `P8_Y5_R2FR_4105_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4105_STATUS.csv`",
        "- `P8_Y5_BRR545_4105_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4106-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md`",
        "- Objective: derive `B_xi/G_ref=M_H[Pi_M J_H]` with projector variation handled, or construct source/unit/input rows for `epsilon_mu` without claiming Newton/PPN.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4105_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_GK_INPUT_OWNER_MATRIX"], gk_input_owner_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_LAMBDA_GK_POSITIVITY_AUDIT"], lambda_positivity_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_NONCOERCIVE_INPUT_PACK_IMPORT"], noncoercive_pack_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_ABSORPTION_RESIDUAL_CONTRACT"], absorption_residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_SOURCE_COUPLING_PIVOT"], source_coupling_pivot_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4105_STATUS"], status_rows())
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
    add("VAL4105_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4105_1_sources_contain_needles", "every local source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

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
    add("VAL4105_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    owners = parse_csv(outputs["P8_Y5_R2FR_4105_GK_INPUT_OWNER_MATRIX"])
    required_symbols = {"lambda_GK", "J_GK_norm", "Phi_boundary_GK", "Q_top_GK", "K_GK", "X_GK_residual"}
    found_symbols = {row.get("symbol", "") for row in owners}
    add("VAL4105_3_owner_symbols", "GK owner matrix contains required symbols including X_GK_residual", required_symbols.issubset(found_symbols), ";".join(sorted(required_symbols - found_symbols)) or "all owner symbols present")

    lambda_rows = parse_csv(outputs["P8_Y5_R2FR_4105_LAMBDA_GK_POSITIVITY_AUDIT"])
    lambda_text = " ".join(" ".join(row.values()) for row in lambda_rows)
    lambda_tokens = ["Z_A", "Z_G", "m_A2", "m_G2", "c_AG", "lambda1_A", "lambda1_G", "C_cross", "COERCIVE_ROUTE_BLOCKED_NONCLAIM"]
    missing_lambda = [token for token in lambda_tokens if token not in lambda_text]
    no_denominator = all(row.get("uses_positive_lambda_denominator") == "False" for row in lambda_rows)
    add("VAL4105_4_lambda_blockers", "lambda audit includes full blocker set and no denominator use", not missing_lambda and no_denominator, ";".join(missing_lambda) or "lambda blockers and policy present")

    nc_rows = parse_csv(outputs["P8_Y5_R2FR_4105_NONCOERCIVE_INPUT_PACK_IMPORT"])
    nc_text = " ".join(" ".join(row.values()) for row in nc_rows)
    nc_tokens = ["a_GK", "X_GK_bound_nc", "epsilon_GK_hair_nc", "F_outer_GK_abs", "K_GK", "no_loop_rule"]
    missing_nc = [token for token in nc_tokens if token not in nc_text]
    nc_no_lambda = all(row.get("uses_positive_lambda_denominator") == "False" for row in nc_rows)
    add("VAL4105_5_noncoercive_import", "noncoercive finite branch is imported without lambda denominator", not missing_nc and nc_no_lambda, ";".join(missing_nc) or "noncoercive branch present")

    abs_rows = parse_csv(outputs["P8_Y5_R2FR_4105_ABSORPTION_RESIDUAL_CONTRACT"])
    abs_text = " ".join(" ".join(row.values()) for row in abs_rows)
    abs_tokens = ["eta_GK<1", "F0_GK_abs", "X_GK_residual", "STRUCTURAL_NON_SCORE_READY_RESIDUAL"]
    missing_abs = [token for token in abs_tokens if token not in abs_text]
    add("VAL4105_6_absorption_residual", "absorption law and residual contract are present", not missing_abs, ";".join(missing_abs) or "absorption residual contract present")

    pivot_rows = parse_csv(outputs["P8_Y5_R2FR_4105_SOURCE_COUPLING_PIVOT"])
    pivot_text = " ".join(" ".join(row.values()) for row in pivot_rows)
    pivot_tokens = ["Pi_M J_H", "B_xi/G_ref", "epsilon_mu", "Newtonian GM"]
    missing_pivot = [token for token in pivot_tokens if token not in pivot_text]
    add("VAL4105_7_source_pivot", "source-coupling pivot names GM and Pi_M-Hilbert target", not missing_pivot, ";".join(missing_pivot) or "source-coupling pivot present")

    claims = parse_csv(outputs["P8_Y5_R2FR_4105_CLAIM_GATE"])
    no_public_claim = all(row.get("public_claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    add("VAL4105_8_no_public_claims", "all claim rows remain nonpublic and nonclaim", no_public_claim, f"claim_rows={len(claims)}")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4105_NEXT_TARGET"])
    next_ok = any("4106-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4105_9_next_target", "next target pivots to Pi_M-Hilbert/epsilon_mu", next_ok, str(next_rows))

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4105*")) or any(
            FORMALIZATION.rglob("4105-Y5-R2FR*")
        )
    add("VAL4105_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4105_11_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4105_VALIDATION.csv"
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
