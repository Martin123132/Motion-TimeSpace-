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
DOC_PATH = ROOT / "4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SPIN_TORSION_REANCHOR_4101"
CHECKPOINT_ID = "4101"
DECISION = (
    "LOCAL_LC_NO_INDEPENDENT_AFFINE_BRANCH_REANCHORED_"
    "E_SPIN_ZERO_INSIDE_BRANCH_SELECTOR_OR_P4_REQUIRED"
)

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4101_00_4100_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4100_NEXT_TARGET.csv",
        "4101-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md",
        "4100 selects spin/torsion/hypermomentum as the leading live non-Hilbert bypass channel.",
    ),
    "SRC4101_01_4100_component": (
        SOURCE_DIR / "P8_Y5_R2FR_4100_COMPONENT_GATES.csv",
        "CG4100_0_spin_torsion",
        "4100 component gate marks E_spin as live unless metric-only/LC or Palatini no-hypermomentum branch closes.",
    ),
    "SRC4101_02_4100_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4100_OFFICIAL_FALLBACK_ROWS.csv",
        "FNH4100_1_spin",
        "4100 official nonclaim fallback row for spin/torsion/hypermomentum.",
    ),
    "SRC4101_03_3565_fork": (
        SOURCE_DIR / "P8_Y5_R2FR_3565_SPIN_TORSION_THEOREM_STACK.csv",
        "STH3565_0_connection_fork",
        "3565 establishes the strict no-Gamma-or-P4 connection fork.",
    ),
    "SRC4101_04_3565_sector": (
        SOURCE_DIR / "P8_Y5_R2FR_3565_SECTOR_GAMMA_SLOT_VERDICT.csv",
        "SECT3565_0_total",
        "3565 sector audit lists which Gamma slots are zero, conditional, or fallback-only.",
    ),
    "SRC4101_05_3565_p4": (
        SOURCE_DIR / "P8_Y5_R2FR_3565_P4_SPIN_HYPERMOMENTUM_BOUND_ROWS.csv",
        "P4H3565_0_total",
        "3565 P4 rows provide the official affine fallback envelope.",
    ),
    "SRC4101_06_3565_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_3565_DECISION_LEDGER.csv",
        "DEC3565_0_exact_fork",
        "3565 decision ledger makes the fork canonical.",
    ),
    "SRC4101_07_3566_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv",
        "SIG3566_0_configuration",
        "3566 writes the private local LC/no-independent-affine parent action branch.",
    ),
    "SRC4101_08_3566_variation": (
        SOURCE_DIR / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "VAR3566_0_total_noGamma",
        "3566 derives zero independent-Gamma variation inside the LC branch.",
    ),
    "SRC4101_09_3566_p4_queue": (
        SOURCE_DIR / "P8_Y5_R2FR_3566_FIRST_SPIN_P4_COEFFICIENT_QUEUE.csv",
        "P4C3566_0_branch_selector",
        "3566 keeps the affine counterbranch coefficient queue ready.",
    ),
    "SRC4101_10_3566_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_3566_DECISION_LEDGER.csv",
        "DEC3566_3_best_next",
        "3566 selects branch-selector derivation as the next non-smuggled step.",
    ),
    "SRC4101_11_3566_doc": (
        ROOT / "3566-Y5-R2FR-parent-local-action-variable-signature-or-first-spin-P4-coefficient.md",
        "local LC parent-action branch explicitly",
        "Human-readable 3566 checkpoint verdict.",
    ),
    "SRC4101_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4101_spin_torsion_hypermomentum_silence_or_P4_bound.py",
        "Reproducible generator for this 4101 checkpoint.",
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


def connection_fork_theorem_rows() -> List[dict]:
    entries = [
        (
            "CFT4101_0_strict_fork",
            "strict local connection fork",
            "The local connection sector has two disciplined routes only: no independent affine/spin connection in the ordinary/source/readout action, or explicit P4 affine/torsion residual rows.",
            "3565 made this structural: if Gamma_ind/omega_ind is absent from the action domain, the Frechet derivative is zero; if present, hypermomentum is a live residual, not a silence.",
            "same local branch; no cancellation between unsigned residual heads",
            "EXACT_STRUCTURAL_FORK_CURRENT_CHAIN",
            "removes the fog option after 4100; E_spin must be zero by branch choice or carried as P4",
            "SRC4101_03_3565_fork",
        ),
        (
            "CFT4101_1_variable_absence_zero",
            "variable-absence hypermomentum zero",
            "For any sector S_i whose argument list excludes Gamma_ind and omega_ind, delta S_i / delta Gamma_ind and delta S_i / delta omega_ind are zero or vacuous on the reduced configuration space.",
            "A functional derivative with respect to a non-coordinate is not a hidden equation; it is absent. Sectorwise zero gives an absolute zero without cancellation.",
            "explicit Arg(S_i) list; no representative Gamma dependence smuggled into readouts",
            "EXACT_CONDITIONAL_THEOREM",
            "kills matter/spin/source/readout affine source terms inside a signed LC/no-independent-affine branch",
            "SRC4101_08_3566_variation",
        ),
        (
            "CFT4101_2_3566_LC_branch_signature",
            "private local LC branch signature",
            "3566 writes S_loc^LC on Conf_loc^LC = {q(Phi), e_obs(q), g_obs(e_obs), Psi_A, A_Q, theta_A(q), tau(q), H_ref, boundary/topology class, Pi_M(q,e_obs,tau)} with no Gamma_ind or omega_ind action coordinate.",
            "The gravity block uses Levi-Civita data of e_obs/g_obs; ordinary matter uses omega_LC[e_obs]; EM uses A_Q, F_Q and *_obs(e_obs); readouts are post-variation functors.",
            "accept the local LC branch as a private branch, not as a public parent selector",
            "PRIVATE_BRANCH_SIGNATURE_REANCHORED",
            "E_spin_abs is zero inside this branch, but public MTS still needs the selector theorem",
            "SRC4101_07_3566_signature",
        ),
        (
            "CFT4101_3_source_product_rule_closure",
            "source hypermomentum product-rule closure",
            "In the q/e_obs/tau-natural projector branch, delta_Gamma(Pi_M J_H)=Pi_M delta_Gamma J_H + (delta_Gamma Pi_M)J_H = 0.",
            "3566 gives delta_Gamma J_H=0 because J_H is Hilbert/coframe-owned; 3498/3565 give delta_Gamma Pi_M=0 only for q/e_obs/tau/topology-natural projectors.",
            "regular compact support; fixed reference; Pi_M does not use Gamma_ind transport",
            "PARTIAL_THEOREM_REANCHORED",
            "turns the source tail from vague coupling worry into a precise product-rule gate",
            "SRC4101_08_3566_variation",
        ),
        (
            "CFT4101_4_EM_Poynting_Hilbert_owner",
            "EM/Poynting owner clause",
            "Visible EM and Poynting energy enter the Hilbert/coframe source through S_EM[A_Q,F_Q,*_obs(e_obs),lambda_A,theta_A], not through an independent affine Gamma source, inside the LC branch.",
            "The Hodge star and stress variation depend on e_obs; the affine Gamma derivative is zero. The live EM coupling problem is therefore lambda_A/alpha ownership, not E_spin.",
            "public-Hodge EM branch; lambda_A constant/universal or separately bounded",
            "AFFINE_GAMMA_ZERO_EM_COUPLING_OPEN",
            "keeps the user's Poynting-vector intuition in the right owner bucket: Hilbert stress yes, hidden affine source no",
            "SRC4101_07_3566_signature",
        ),
        (
            "CFT4101_5_selector_gap",
            "local LC branch selector gap",
            "The corpus has an internal LC/no-independent-affine branch theorem, but it has not derived why compact local MTS must select that branch rather than an affine/torsion counterbranch.",
            "3566 explicitly names B_LC_selector as missing. Without B_LC_selector=1 from parent quotient/gauge/regularity, E_spin=0 is branch-internal rather than public.",
            "parent-owned selector or source-backed affine coefficients",
            "CORE_GAP_NOW_SHARP_NOT_VAGUE",
            "next work should derive B_LC_selector first; if it fails, fill K_spin/c_A/c_T/c_Q rows",
            "SRC4101_09_3566_p4_queue",
        ),
        (
            "CFT4101_6_total_verdict",
            "4101 total connection verdict",
            "E_spin is no longer the foggiest blocker: it is zero inside the written LC branch and retained as official P4 outside it. The public local-GR route now hinges on branch selection plus source-owner/PPN gates.",
            "4100 left E_spin live; 3565 provided the fork; 3566 supplied the LC action signature and variation derivation; 4101 imports that into the current chain.",
            "no public local-GR claim; no affine residual ignored",
            "CONNECTION_HEAD_TAMED_CONDITIONALLY",
            "move to local LC branch selector or K_spin/P4 map",
            "SRC4101_10_3566_decision",
        ),
    ]
    return [
        {
            **row_base(),
            "theorem_id": theorem_id,
            "name": name,
            "statement": statement,
            "derivation": derivation,
            "required_premises": premises,
            "current_status": status,
            "effect": effect,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "branch_internal_zero_allowed": bool_string(theorem_id in {"CFT4101_1_variable_absence_zero", "CFT4101_2_3566_LC_branch_signature", "CFT4101_3_source_product_rule_closure", "CFT4101_4_EM_Poynting_Hilbert_owner"}),
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, name, statement, derivation, premises, status, effect, source_key in entries
    ]


def lc_branch_signature_rows() -> List[dict]:
    entries = [
        (
            "LCS4101_0_configuration",
            "S_loc^LC / Conf_loc^LC",
            "{q(Phi), e_obs(q), g_obs(e_obs), Psi_A, A_Q, theta_A(q), tau(q), H_ref, boundary/topology, Pi_M(q,e_obs,tau)}",
            "Gamma_ind and omega_ind are not coordinates",
            "BRANCH_REANCHORED_FROM_3566",
            "E_spin variation can be evaluated as a missing-coordinate zero inside this branch.",
            "SRC4101_07_3566_signature",
        ),
        (
            "LCS4101_1_gravity",
            "S_EH[e_obs]",
            "(2 kappa0)^-1 int sqrt(-g_obs)(R[g_obs]-2 Lambda0)",
            "Levi-Civita connection of e_obs/g_obs only",
            "STANDARD_LOCAL_BLOCK_STAGED",
            "Gives the spin-2/EH local operator branch; G_ref/source normalization remains separate.",
            "SRC4101_07_3566_signature",
        ),
        (
            "LCS4101_2_matter_spin",
            "S_m",
            "sum_A int mu_obs L_A(Psi_A, D_LC[e_obs,A_Q]Psi_A, e_obs, A_Q, theta_A(q))",
            "spin connection is omega_LC[e_obs], not torsionful omega_ind",
            "NO_INDEPENDENT_SPIN_HYPERMOMENTUM_INSIDE_BRANCH",
            "Spin backreaction is coframe/Hilbert-owned rather than an independent torsion source.",
            "SRC4101_07_3566_signature",
        ),
        (
            "LCS4101_3_visible_EM",
            "S_EM",
            "-lambda_A/2 int F_Q wedge *_obs F_Q + theta_A/2 int F_Q wedge F_Q",
            "A_Q is visible U(1); affine Gamma_ind is not an EM argument",
            "POYNTING_STRESS_HILBERT_OWNED_ALPHA_OPEN",
            "Poynting/Maxwell stress contributes to Hilbert source; D_X ln(lambda_A) remains a separate coupling target.",
            "SRC4101_07_3566_signature",
        ),
        (
            "LCS4101_4_source_mass",
            "J_H[tau], W_source, M_H",
            "J_H from e_obs variation of matter+EM; W_source=closure(supp J_H[tau]); M_H from Hamiltonian/Gauss charge",
            "source is Hilbert/Noether-owned, not Gamma_ind-owned",
            "SOURCE_GAMMA_ZERO_CONDITIONAL_SUPPORT",
            "Kills independent source hypermomentum modulo regular support, H_ref/integrability and q-natural projector clauses.",
            "SRC4101_08_3566_variation",
        ),
        (
            "LCS4101_5_readouts",
            "R_arena",
            "R_bar(e_obs,A_Q,J_H,M_H,tau,theta_A) evaluated after variation",
            "readouts cannot be parent-action Gamma variables",
            "NO_SOURCE_REENTRY_INSIDE_BRANCH",
            "Clocks, light, orbit, WEP, PPN and R10 can test residuals but cannot create the parent source current.",
            "SRC4101_07_3566_signature",
        ),
        (
            "LCS4101_6_boundary",
            "S_boundary/H_ref",
            "GHY[e_obs] plus exact/topological/fixed-reference terms",
            "boundary objects use e_obs/LC data",
            "NO_GAMMA_TAIL_BUT_SOURCE_OWNER_OPEN",
            "No independent affine tail inside branch; local GR still needs source-owner/boundary/G_ref closure.",
            "SRC4101_07_3566_signature",
        ),
    ]
    return [
        {
            **row_base(),
            "signature_id": signature_id,
            "object": obj,
            "formal_signature": signature,
            "connection_policy": policy,
            "status": status,
            "effect": effect,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "branch_signed_private": "True",
            "public_parent_derived": "False",
            "valid_for_claim": "False",
        }
        for signature_id, obj, signature, policy, status, effect, source_key in entries
    ]


def sector_verdict_rows() -> List[dict]:
    entries = [
        (
            "SECT4101_0_total",
            "total ordinary/source/readout connection head",
            "E_spin_abs",
            "ZERO_INSIDE_LC_BRANCH_PUBLIC_SELECTOR_MISSING",
            "B_LC_selector=1 plus all sector Gamma variables absent; otherwise P4 envelope",
            "derive selector or source affine coefficients",
            "E_spin_abs official P4 fallback",
            "True",
            "False",
            "SRC4101_05_3565_p4",
        ),
        (
            "SECT4101_1_matter_spin",
            "ordinary matter and spin transport",
            "Delta_matter + Delta_spin",
            "ZERO_INSIDE_LC_BRANCH",
            "S_m uses e_obs and omega_LC[e_obs], not Gamma_ind/omega_ind",
            "public selector and second-order PPN still separate",
            "c_A/c_T/c_Q if affine counterbranch is used",
            "True",
            "False",
            "SRC4101_08_3566_variation",
        ),
        (
            "SECT4101_2_EM_light",
            "visible EM/light/Poynting stress",
            "Delta_light_affine",
            "AFFINE_GAMMA_ZERO_INSIDE_LC_BRANCH_ALPHA_OPEN",
            "S_EM depends on A_Q,F_Q,*_obs(e_obs),lambda_A,theta_A; no Gamma_ind argument",
            "D_X ln(lambda_A) and detector/readout operator tests remain",
            "D_X ln(lambda_A) plus optical response if affine branch used",
            "True",
            "False",
            "SRC4101_07_3566_signature",
        ),
        (
            "SECT4101_3_source_current",
            "source mass/worldtube/support",
            "Delta_source",
            "CONDITIONAL_ZERO_INSIDE_Q_NATURAL_LC_BRANCH",
            "delta_Gamma J_H=0 and regular support gives no support drift",
            "H_ref/integrability/source-owner proof still separate",
            "epsilon_hypermomentum_source_kernel",
            "True",
            "False",
            "SRC4101_08_3566_variation",
        ),
        (
            "SECT4101_4_projector",
            "projector/support map",
            "Delta_projector_comm",
            "WEAKEST_LINK_ZERO_IF_Q_NATURAL",
            "delta_Gamma Pi_M=0 only when Pi_M descends through q/e_obs/tau/topology",
            "operator norm required if any Gamma transport appears",
            "K_projector_comm",
            "True",
            "False",
            "SRC4101_09_3566_p4_queue",
        ),
        (
            "SECT4101_5_clock_orbit_readout",
            "clock, orbit, WEP, PPN and R10 readouts",
            "Delta_clock + Delta_orbit",
            "NO_SOURCE_REENTRY_INSIDE_BRANCH_OPERATOR_TESTS_REMAIN",
            "readouts are post-variation functors and cannot redefine source current",
            "must still pass clock/orbit/PPN residual tests",
            "clock/orbit affine response kernels if counterbranch used",
            "True",
            "False",
            "SRC4101_07_3566_signature",
        ),
        (
            "SECT4101_6_boundary_projective",
            "boundary/reference/projective trace",
            "Delta_boundary + Delta_projective",
            "NO_INDEPENDENT_PROJECTIVE_IN_LC_BRANCH_BOUNDARY_OWNER_OPEN",
            "LC branch has no independent projective trace; boundary uses e_obs/LC data",
            "boundary/source-owner/G_ref proof still needed for local GR",
            "P4_boundary and P4_projective if affine branch used",
            "True",
            "False",
            "SRC4101_07_3566_signature",
        ),
        (
            "SECT4101_7_affine_counterbranch",
            "independent affine/torsion/nonmetricity branch",
            "P4_affine_stack",
            "RETAINED_NOT_ZEROED",
            "if Gamma_ind/omega_ind appears, hypermomentum must be carried",
            "numeric/source-backed P4 coefficient rows missing",
            "c_A,c_T,c_Q,K_spin,K_projector_comm,D_X ln(lambda_A)",
            "False",
            "False",
            "SRC4101_09_3566_p4_queue",
        ),
    ]
    return [
        {
            **row_base(),
            "sector_id": sector_id,
            "sector": sector,
            "residual_symbol": symbol,
            "status": status,
            "zero_condition": zero_condition,
            "remaining_gap": gap,
            "fallback": fallback,
            "source_path": str(LOCAL_SOURCES[source_key][0]),
            "branch_zero_live": branch_zero,
            "public_zero_live": public_zero,
            "valid_for_claim": "False",
        }
        for sector_id, sector, symbol, status, zero_condition, gap, fallback, branch_zero, public_zero, source_key in entries
    ]


def p4_fallback_queue_rows() -> List[dict]:
    entries = [
        (
            "P4Q4101_0_branch_selector",
            "B_LC_selector",
            "structural branch selector",
            "B_LC_selector=1 if parent local action must exclude Gamma_ind/omega_ind in compact local physics; otherwise use affine residual rows",
            "PRIMARY_DERIVATION_TARGET",
            "derive from quotient/gauge/regularity/no vertical affine slot or demote to effective closure",
            "MISSING_OR_STRUCTURAL",
        ),
        (
            "P4Q4101_1_axial_torsion",
            "c_A",
            "axial torsion coupling coefficient",
            "S_axial_abs = ||c_A S_mu J5^mu||/N_source",
            "ZERO_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_COEFFICIENT",
            "source c_A from affine/torsion action or set c_A=0 by selector",
            "ZERO_IN_PRIVATE_LC_BRANCH_ONLY",
        ),
        (
            "P4Q4101_2_trace_torsion",
            "c_T",
            "trace torsion coupling coefficient",
            "T_trace_abs = ||c_T T_mu J_T^mu||/N_source",
            "ZERO_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_COEFFICIENT",
            "source c_T from affine/torsion action or set c_T=0 by selector",
            "ZERO_IN_PRIVATE_LC_BRANCH_ONLY",
        ),
        (
            "P4Q4101_3_weyl_nonmetricity",
            "c_Q",
            "Weyl nonmetricity coupling coefficient",
            "Q_weyl_abs = ||c_Q Q_mu J_Q^mu||/N_source",
            "ZERO_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_COEFFICIENT",
            "source c_Q from affine/nonmetricity action or set c_Q=0 by selector",
            "ZERO_IN_PRIVATE_LC_BRANCH_ONLY",
        ),
        (
            "P4Q4101_4_projector_comm",
            "K_projector_comm",
            "projector/domain commutator kernel",
            "epsilon_projector_comm <= ||delta_Gamma Pi_M|| ||J_H||/|M_H_ref|",
            "CANDIDATE_ZERO_IF_Q_NATURAL_ELSE_BOUND_MISSING",
            "prove Pi_M q/e_obs/tau-natural or source operator norm",
            "MISSING_OR_STRUCTURAL",
        ),
        (
            "P4Q4101_5_EM_scalar_coupling",
            "D_X ln(lambda_A)",
            "visible EM scalar coupling / alpha owner",
            "alpha_EM drift/source coupling proportional to D_X ln(lambda_A/e_obs^2)",
            "NOT_E_SPIN_BUT_CORE_COUPLING_TARGET",
            "lock lambda_A constant/universal or derive alpha/source response",
            "MISSING_OR_STRUCTURAL",
        ),
        (
            "P4Q4101_6_Kspin_map",
            "K_spin",
            "weak-field map from E_spin_abs to local tests",
            "epsilon_local_connection <= K_spin E_spin_abs",
            "MISSING_IF_AFFINE_BRANCH_USED",
            "component basis, units, lab-frame response and arena bounds",
            "MISSING_OR_STRUCTURAL",
        ),
        (
            "P4Q4101_7_no_cancellation",
            "sum_abs_components",
            "policy guard",
            "claim_allowed = all components zero OR every absolute component bound passes arena limits",
            "ACTIVE_GUARD",
            "forbid cancellation between unsigned affine/source/readout/projective terms",
            "POLICY",
        ),
    ]
    return [
        {
            **row_base(),
            "queue_id": queue_id,
            "symbol": symbol,
            "role": role,
            "formula": formula,
            "status": status,
            "next_input_required": next_input,
            "numeric_value": numeric,
            "source_path": str(LOCAL_SOURCES["SRC4101_09_3566_p4_queue"][0]),
            "source_backed_numeric": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for queue_id, symbol, role, formula, status, next_input, numeric in entries
    ]


def decision_gate_rows() -> List[dict]:
    entries = [
        (
            "DEC4101_0_reanchor",
            "re-anchor 3565/3566 spin-torsion result into the current 4100 chain",
            "4100 reopened E_spin as the live non-Hilbert channel; 3565/3566 already solved the branch-internal LC case",
            "E_spin is now classified as conditionally closed inside LC/no-independent-affine branch, not merely missing",
            "CONNECTION_HEAD_TAMED_CONDITIONALLY",
            "SRC4101_01_4100_component",
        ),
        (
            "DEC4101_1_private_branch_zero",
            "accept E_spin=0 inside the written local LC branch",
            "Gamma_ind/omega_ind are absent from the branch action variables and all affine derivatives are zero/vacuous there",
            "use the LC branch as the preferred private derivation path while keeping no public local-GR claim",
            "PRIVATE_BRANCH_THEOREM_ACCEPTED",
            "SRC4101_08_3566_variation",
        ),
        (
            "DEC4101_2_no_selector_overclaim",
            "do not claim parent MTS must select the LC branch yet",
            "B_LC_selector is structural and still not derived from the parent quotient/gauge/regularity mechanism",
            "public local GR/Newton and R10/PPN pass remain blocked",
            "PUBLIC_CLAIM_BLOCKED",
            "SRC4101_09_3566_p4_queue",
        ),
        (
            "DEC4101_3_next",
            "derive the local LC branch selector before chasing numeric P4 unless the proof fails",
            "the cheapest clean win is structural: prove no independent affine slot in compact local physics; otherwise source K_spin/c_A/c_T/c_Q",
            "4102 targets local LC branch selector or Kspin/P4 map",
            "NEXT_TARGET_SELECTED",
            "SRC4101_10_3566_decision",
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
        (
            "CLAIM4101_0_branch_internal_Espin",
            "E_spin=0 inside S_loc^LC",
            "PRIVATE_BRANCH_THEOREM_TRUE_CONDITIONAL",
            "allowed only as internal checkpoint logic; not a public parent theory claim",
            "B_LC_selector not derived",
        ),
        (
            "CLAIM4101_1_public_local_GR",
            "local GR/Newton recovery",
            "BLOCKED",
            "connection head is tamed conditionally, but source-owner/G_ref/Poisson-Gauss/boundary/PPN gates remain",
            "selector plus remaining local GR gates",
        ),
        (
            "CLAIM4101_2_affine_counterbranch",
            "affine/torsion/nonmetricity branch safe bound",
            "BLOCKED",
            "P4 rows are symbolic and source_backed_numeric=false",
            "K_spin and first affine coefficients with units and arena projection",
        ),
        (
            "CLAIM4101_3_EM_alpha",
            "EM/Poynting coupling fully closed",
            "BLOCKED_AS_SEPARATE_COUPLING_TARGET",
            "affine Gamma source is zero in LC branch, but lambda_A/alpha owner is not derived here",
            "D_X ln(lambda_A) constant/universal theorem or bounded response",
        ),
    ]
    return [
        {
            **row_base(),
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "missing_gate": missing_gate,
            "public_claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for claim_id, claim, status, reason, missing_gate in entries
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "next_id": "NEXT4101_0",
            "target_doc": "4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md",
            "target_script": "scripts/Y5_R2FR_4102_local_LC_branch_selector_or_Kspin_P4_map.py",
            "objective": "derive why compact local MTS selects the LC/no-independent-affine branch from quotient/gauge/regularity/no vertical affine slot; if not, make K_spin and first affine torsion coefficients source-ready",
            "success_gate": "B_LC_selector=1 from parent mechanism, or first source-backed K_spin/c_A coefficient row with units and arena projection",
            "reason": "4101 makes E_spin zero inside the written branch; the non-smuggled leap is branch selection or official affine fallback",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[dict]:
    return [
        {
            **row_base(),
            "status_id": "STATUS4101_0",
            "decision": DECISION,
            "connection_status": "E_spin_zero_inside_private_LC_branch; official_P4_fallback_retained_outside_branch",
            "public_status": "no_local_GR_or_R10_or_PPN_claim",
            "next_target": "4102 local LC branch selector or Kspin/P4 map",
            "valid_for_claim": "False",
        }
    ]


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4101_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4101_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM.csv",
        "P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE": SOURCE_DIR / "P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE.csv",
        "P8_Y5_R2FR_4101_SECTOR_GAMMA_SLOT_VERDICT": SOURCE_DIR / "P8_Y5_R2FR_4101_SECTOR_GAMMA_SLOT_VERDICT.csv",
        "P8_Y5_R2FR_4101_P4_FALLBACK_QUEUE": SOURCE_DIR / "P8_Y5_R2FR_4101_P4_FALLBACK_QUEUE.csv",
        "P8_Y5_R2FR_4101_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4101_DECISION_GATE.csv",
        "P8_Y5_R2FR_4101_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4101_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4101_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4101_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4101_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4101_STATUS.csv",
    }


def write_doc() -> None:
    lines = [
        "# 4101 - Spin/torsion/hypermomentum silence or P4 bound",
        "",
        "## Verdict",
        "4101 re-anchors the old spin/torsion result into the current 4100 chain: the local LC/no-independent-affine branch is now the clean private branch, and `E_spin` is zero inside that branch by variable absence.",
        "",
        "That is real progress, but not a public local-GR claim. The still-missing leap is the selector: why the full parent MTS theory must choose this compact local LC branch rather than an affine/torsion/nonmetricity counterbranch. If that selector cannot be derived, the P4 queue is the honest fallback.",
        "",
        f"Decision: `{DECISION}`",
        "",
        "## Exact fork",
        "- Route A: `Gamma_ind` and `omega_ind` are not variables of `S_loc^LC`; then `delta_Gamma S_i=0` sectorwise.",
        "- Route B: an independent affine/spin connection is present; then `E_spin` must remain as explicit P4 residuals.",
        "- No route is allowed where the affine coupling is unstated and then silently ignored.",
        "",
        "## What is actually closed",
        "- Matter/spin: closed inside the LC branch because spin transport uses `omega_LC[e_obs]`.",
        "- EM/Poynting: affine-Gamma silent inside the LC branch; Poynting stress is Hilbert/coframe-owned, while `lambda_A/alpha` remains a separate coupling target.",
        "- Source current: `delta_Gamma(Pi_M J_H)=0` only when `J_H` is Hilbert-owned and `Pi_M` is `q/e_obs/tau` natural.",
        "- Projective trace: absent in the LC branch, not merely gauge-waved away.",
        "",
        "## Not claimed",
        "- No public local-GR, Newton, R10, WEP, clock, orbital or PPN pass follows from this checkpoint alone.",
        "- No affine/torsion branch is numerically bounded yet.",
        "- `B_LC_selector`, `K_spin`, `c_A`, `c_T`, `c_Q`, `K_projector_comm` and `D_X ln(lambda_A)` remain nonclaim rows.",
        "",
        "## Outputs",
        "- `P8_Y5_R2FR_4101_SOURCE_REGISTER.csv`",
        "- `P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM.csv`",
        "- `P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE.csv`",
        "- `P8_Y5_R2FR_4101_SECTOR_GAMMA_SLOT_VERDICT.csv`",
        "- `P8_Y5_R2FR_4101_P4_FALLBACK_QUEUE.csv`",
        "- `P8_Y5_R2FR_4101_DECISION_GATE.csv`",
        "- `P8_Y5_R2FR_4101_CLAIM_GATE.csv`",
        "- `P8_Y5_R2FR_4101_NEXT_TARGET.csv`",
        "- `P8_Y5_R2FR_4101_STATUS.csv`",
        "- `P8_Y5_BRR545_4101_VALIDATION.csv`",
        "",
        "## Next target",
        "- `4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md`",
        "- Objective: derive the local LC branch selector first; if that fails, source `K_spin` and the first affine torsion/nonmetricity coefficient map.",
    ]
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4101_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM"], connection_fork_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE"], lc_branch_signature_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_SECTOR_GAMMA_SLOT_VERDICT"], sector_verdict_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_P4_FALLBACK_QUEUE"], p4_fallback_queue_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4101_STATUS"], status_rows())
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
    add("VAL4101_0_sources_exist", "every local source path exists", not missing_sources, ";".join(missing_sources) or "all sources exist")
    add("VAL4101_1_sources_contain_needles", "every source contains its expected needle", not missing_needles, ";".join(missing_needles) or "all needles found")

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
    add("VAL4101_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4101_CONNECTION_FORK_THEOREM"]))
    required_theorem_tokens = ["Gamma_ind", "omega_ind", "E_spin", "B_LC_selector", "P4", "Poynting", "delta_Gamma(Pi_M J_H)"]
    missing_theorem = [token for token in required_theorem_tokens if token not in theorem_text]
    add("VAL4101_3_theorem_tokens", "connection theorem contains required fork tokens", not missing_theorem, ";".join(missing_theorem) or "all theorem tokens present")

    signature_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4101_LC_BRANCH_SIGNATURE"]))
    required_signature_tokens = ["S_loc^LC", "e_obs", "omega_LC", "lambda_A", "J_H", "R_arena"]
    missing_signature = [token for token in required_signature_tokens if token not in signature_text]
    add("VAL4101_4_signature_tokens", "LC branch signature contains the source/readout owners", not missing_signature, ";".join(missing_signature) or "all signature tokens present")

    sector_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4101_SECTOR_GAMMA_SLOT_VERDICT"]))
    required_sector_tokens = ["E_spin_abs", "Delta_matter", "Delta_spin", "Delta_light", "Delta_source", "Delta_projector_comm", "Delta_clock", "Delta_orbit", "Delta_boundary", "Delta_projective"]
    missing_sector = [token for token in required_sector_tokens if token not in sector_text]
    add("VAL4101_5_sector_coverage", "sector verdict covers all live affine slots", not missing_sector, ";".join(missing_sector) or "all sector tokens present")

    p4_text = " ".join(" ".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4101_P4_FALLBACK_QUEUE"]))
    required_p4_tokens = ["B_LC_selector", "c_A", "c_T", "c_Q", "K_spin", "D_X ln(lambda_A)", "sum_abs_components"]
    missing_p4 = [token for token in required_p4_tokens if token not in p4_text]
    add("VAL4101_6_p4_queue", "P4 fallback queue keeps selector and coefficient rows", not missing_p4, ";".join(missing_p4) or "all P4 tokens present")

    claims = parse_csv(outputs["P8_Y5_R2FR_4101_CLAIM_GATE"])
    no_public_claim = all(row.get("public_claim_allowed") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    add("VAL4101_7_no_public_claims", "all claim rows remain nonpublic and nonclaim", no_public_claim, f"claim_rows={len(claims)}")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4101_NEXT_TARGET"])
    next_ok = any("4102-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md" in row.get("target_doc", "") for row in next_rows)
    add("VAL4101_8_next_target", "next target is branch selector or Kspin/P4 map", next_ok, str(next_rows))

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    add("VAL4101_9_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4101_10_compile", "generator script compiles", compile_ok, compile_detail)

    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4101_VALIDATION.csv"
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
