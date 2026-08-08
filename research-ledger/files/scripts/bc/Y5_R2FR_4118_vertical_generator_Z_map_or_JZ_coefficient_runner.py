from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_VERTICAL_GENERATOR_Z_MAP_CURRENT_SPINE_4118"
CHECKPOINT_ID = "4118"
DECISION = "DCDAGGER_VERTICAL_GENERATOR_TEST_WRITTEN_Z_MAP_UNSIGNED_OMEGA_OWNER_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4118_00_4117_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4117_NEXT_TARGET.csv",
        "4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md",
        "4117 selected the vertical-generator Z-map target.",
    ),
    "SRC4118_01_4117_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4117_STATUS.csv",
        "PARENT_ACTION_JZ_ZERO_THEOREM_IMPORTED_VERTICAL_Z_MAP_NEXT",
        "Current-chain parent-action theorem handoff.",
    ),
    "SRC4118_02_4117_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_4117_PARENT_ACTION_CLAUSE.csv",
        "Dq[e_A]=0",
        "Parent-action clause requiring quotient-vertical generators.",
    ),
    "SRC4118_03_4117_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4117_JZ_ZERO_THEOREM.csv",
        "J_A^matter=0",
        "4117 conditional J_Z=0 theorem if vertical/descent clauses close.",
    ),
    "SRC4118_04_3631_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3631_STATUS.csv",
        "DCDAGGER_TO_VERTICAL_TEST_WRITTEN_Z_MAP_UNSIGNED_BOUND_ROWS_STAGED",
        "Older 3631 scaffold for DCdagger verticality and Z-observable map.",
    ),
    "SRC4118_05_591_dcdagger": (
        SOURCE_DIR / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv",
        "DCdagger",
        "Prior DCdagger formula source.",
    ),
    "SRC4118_06_591_omega_compare": (
        SOURCE_DIR / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv",
        "formula_progress_but_no_certificate",
        "Prior verdict: formula exists but parent Omega/P/J ownership is missing.",
    ),
    "SRC4118_07_583_noether": (
        SOURCE_DIR / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "parent symplectic potential",
        "Noether/momentum-map contract for the same-parent owner route.",
    ),
    "SRC4118_08_583_owner": (
        SOURCE_DIR / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv",
        "parent",
        "Parent momentum-map owner attempt.",
    ),
    "SRC4118_09_1667_chart": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
        "parent",
        "Parent field chart candidate for q and local residual coordinates.",
    ),
    "SRC4118_10_1667_dq": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
        "Dq",
        "Prior Dq-on-Z/phi leak tests.",
    ),
    "SRC4118_11_669_constraints": (
        SOURCE_DIR / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
        "operator",
        "Candidate constraint/operator rows useful for the next owner route.",
    ),
    "SRC4118_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4118_vertical_generator_Z_map_or_JZ_coefficient_runner.py",
        "Reproducible generator for this 4118 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def vertical_generator_criterion_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "VGC4118_0_parent_phase_space",
            "Start from one parent action S_parent[Phi] with variation delta L=E_i delta Phi^i+d theta(delta Phi).",
            "Omega=delta theta on parent field space, after gauge degeneracies and boundary conditions are declared.",
            "theta, Omega, q, P, J and boundary terms are all owned by the same parent action.",
            "SAME_PARENT_PHASE_SPACE_NOT_YET_SIGNED",
        ),
        (
            "VGC4118_1_reconstruction",
            "DCdagger is not itself a motion field; it is a parent-field-space one-form that may reconstruct a generator.",
            "Omega_flat(e_X)=DCdagger[X]",
            "DCdagger[X] annihilates ker(Omega) and lies in the image of Omega_flat, modulo proper gauge.",
            "FORMAL_RECONSTRUCTION_WRITTEN_PARENT_OMEGA_MISSING",
        ),
        (
            "VGC4118_2_verticality",
            "The reconstructed generator is quotient-vertical only if it leaves the observable quotient map silent.",
            "Dq[e_X]=Dq[Omega^{-1}DCdagger[X]]=0",
            "zero in observed coframe, matter/source readout, theta markers, and boundary/projector data.",
            "VERTICALITY_TEST_EXACT_BUT_NOT_RUNNABLE_WITHOUT_Q_AND_OMEGA",
        ),
        (
            "VGC4118_3_boundary_charge",
            "A generator that is bulk-vertical can still be physically visible through an edge/collar charge.",
            "delta G_X=Omega(e_X,delta Phi); G_X=int_Sigma C_X+int_boundary Q_boundary[X]",
            "G_X differentiable and Q_X=0, exact, or proper-gauge on the local compact collar.",
            "BOUNDARY_CHARGE_SILENCE_NOT_DERIVED",
        ),
        (
            "VGC4118_4_local_GR_consequence",
            "If VGC4118_0 through VGC4118_3 close, then the 4117 parent-action theorem can set J_Z=0 without smuggling.",
            "vertical e_X + quotient descent + proper Q_X => J_Z=0 for descended matter/source/boundary sectors",
            "all required parent clauses are signed from one action, not patched after the local solution.",
            "CONDITIONAL_THEOREM_NO_CURRENT_CLAIM",
        ),
        (
            "VGC4118_5_failure_consequence",
            "If any criterion fails, the failed piece is physical leakage, not an optional closure convention.",
            "R_local^i=M^i_A Z^A+N^i_a Dq[e_a]+B^i_boundary+S^i_J L^{-1}J_Z+O(2)",
            "each leak has a theorem-zero, numeric coefficient, or sourced empirical bound.",
            "LEAK_COEFFICIENT_ROUTE_REQUIRED_IF_OWNER_ROUTE_FAILS",
        ),
    ]
    for criterion_id, statement, formula, pass_condition, current_status in data:
        row = row_base()
        row.update(
            {
                "criterion_id": criterion_id,
                "statement": statement,
                "formula": formula,
                "pass_condition": pass_condition,
                "current_status": current_status,
                "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4117_PARENT_ACTION_CLAUSE.csv"),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def dcdagger_map_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "DVG4118_0_image_test",
            "DCdagger-to-generator image condition",
            "exists e_X such that Omega_flat(e_X)=DCdagger[X]",
            "parent Omega supplied by theta=delta L boundary term; DCdagger is not hand-paired.",
            "MISSING_PARENT_OMEGA_FLAT",
        ),
        (
            "DVG4118_1_null_test",
            "No hidden obstruction from presymplectic null directions",
            "DCdagger[X](n)=0 for every n in ker(Omega)",
            "otherwise no Hamiltonian generator exists for that DCdagger row.",
            "MISSING_KERNEL_AUDIT",
        ),
        (
            "DVG4118_2_same_parent_owner",
            "same-parent ownership gate",
            "parent L -> theta/Omega/P/J/q -> e_X=Omega^{-1}DCdagger -> Dq[e_X]=0",
            "P, J, theta, Omega and q are not separate fitted closures.",
            "SAME_PARENT_OWNER_MISSING",
        ),
        (
            "DVG4118_3_constraint_first_route",
            "clean construction route",
            "S_parent=S_obs[q(Phi),Psi]+int Lambda^A C_A(Phi); e_epsilon={Phi,G[epsilon]}",
            "first-class C_A, closed algebra, differentiable G, zero/proper boundary charge.",
            "BEST_ROUTE_SELECTED_NOT_CLOSED",
        ),
        (
            "DVG4118_4_verdict",
            "DCdagger has an exact vertical-generator contract, but the current corpus has not signed the parent owner.",
            "Omega_flat(e_X)=DCdagger[X] AND Dq[e_X]=0 AND Q_boundary proper/zero",
            "close all three gates before claiming local-GR silence; otherwise score Dq/J_Z leaks.",
            "DCDAGGER_TO_VERTICAL_MAP_CONDITIONAL_NO_CLAIM",
        ),
    ]
    for map_id, statement, formula, gate, current_status in data:
        row = row_base()
        row.update(
            {
                "map_id": map_id,
                "statement": statement,
                "formula": formula,
                "gate": gate,
                "current_status": current_status,
                "source_path": str(SOURCE_DIR / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def observable_map_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("ZOM4118_0_q_loc", "q_loc^nu", "Pi_q Z + Pi_Dq Dq[e_X]", "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}", "MISSING_Z_TO_QLOC_PROJECTION"),
        ("ZOM4118_1_gamma_beta", "gamma_minus_1;beta_minus_1", "Pi_gamma_beta Z + Pi_gamma_beta^D Dq[e_X]", "weak-field metric solution maps residual stress/source into PPN scalar sector", "MISSING_WEAK_FIELD_Z_METRIC_SOLUTION"),
        ("ZOM4118_2_preferred_frame", "alpha1;alpha2;alpha3;xi", "Pi_PF Z + Pi_PF^D Dq[e_X] + Pi_PF^B Q_boundary", "preferred-frame/location projections include collar/source-current terms", "MISSING_PREFERRED_FRAME_Z_PROJECTION"),
        ("ZOM4118_3_Newton_source", "delta_Newton_MTS;mu_extra;alpha(lambda)", "Pi_M L^{-1}J_Z + Pi_M^D Dq[e_X]", "Newton/R10 depends on source normalization and finite-range profile", "MISSING_SOURCE_MASS_AND_RANGE_MAP"),
        ("ZOM4118_4_clock_WEP_Gdot", "alpha_clock;eta_source_AB;Gdot/G", "Pi_clock/source/time(Z,Dq[e_X],J_Z)", "clock/WEP/Gdot use the same observed coframe and species/source charge descent", "MISSING_CLOCK_WEP_TIME_MAP"),
        ("ZOM4118_5_EM_Poynting_flux", "w_EM;Phi_EM_boundary;Poynting_flux", "Pi_EM Z + Pi_EM^B Q_boundary + Pi_EM^S S_Poynting", "Maxwell/Poynting flux must be counted as physical stress/current unless theorem-zero or boundary-silent", "MISSING_EM_FLUX_SEPARATION_MAP"),
        ("ZOM4118_6_R11", "non_EH_operator_coefficients", "operator_family_projection(Z,Dq[e_X],J_Z,Q_boundary)", "R11 needs executable operator coefficients for retained non-EH/source-normalization branch", "MISSING_EXECUTABLE_R11_Z_VECTOR"),
        ("ZOM4118_7_verdict", "full local residual vector", "R_local^i=M^i_A Z^A+N^i_a Dq[e_a]+B^i Q_i+S^i_A(L^{-1}J_Z)^A+O(2)", "full row rank for R0-R11 or every unspanned component has theorem-zero/bound", "Z_OBSERVABLE_MAP_NOT_CLAIMED_BOUND_ROWS_REQUIRED"),
    ]
    for map_id, observable, formula, condition, status in data:
        row = row_base()
        row.update(
            {
                "map_id": map_id,
                "observable": observable,
                "map_formula": formula,
                "condition_for_use": condition,
                "rank_gate": "full row coverage or independent theorem-zero/bound",
                "current_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def leak_coefficient_rows() -> List[dict]:
    rows: List[dict] = []
    dq_data = [
        ("DQL4118_0_Dq_Z", "Dq_leak", "Dq_Z_norm", "Z normal-form quotient leak"),
        ("DQL4118_1_Dq_phi", "Dq_leak", "Dq_phi_norm", "phi improvement quotient leak"),
        ("DQL4118_2_Dq_RAB_Jq", "Dq_leak", "Dq_RAB_or_Jq_norm", "R_AB/J_q cell-visible leak"),
        ("DQL4118_3_DObs_e", "Dq_leak", "DObs_e_Dq_leak", "observed geometry channel"),
        ("DQL4118_4_Dsource_readout", "Dq_leak", "Dsource_readout_Dq_leak", "Newton/source/readout channel"),
        ("DQL4118_5_Dtheta_marker", "Dq_leak", "Dtheta_marker_Dq_leak", "constants/material marker channel"),
        ("DQL4118_6_boundary_projector", "Dq_leak", "Dboundary_projector_Dq_leak", "boundary and projector channel"),
    ]
    jz_data = [
        ("JZC4118_0_gamma", "J_Z_coefficient", "gamma_minus_1", "K_gamma_JZ * ||L^{-1}J_Z||_gamma", "R3_gamma"),
        ("JZC4118_1_beta", "J_Z_coefficient", "beta_minus_1", "K_beta_JZ * ||L^{-1}J_Z||_beta + delta_beta_source", "R4_beta"),
        ("JZC4118_2_preferred_frame", "J_Z_coefficient", "alpha1;alpha2;alpha3;xi", "P_PF(L^{-1}J_Z + Q_boundary)", "R5_R6_R7_R8"),
        ("JZC4118_3_Newton_source", "J_Z_coefficient", "delta_Newton_MTS;alpha(lambda);mu_extra", "delta_mu_JZ = K_mu_JZ * Pi_M(L^{-1}J_Z)", "R10_R11_Newton"),
        ("JZC4118_4_clock", "J_Z_coefficient", "alpha_clock_redshift", "K_clock_JZ * frame_clock_projection(L^{-1}J_Z)", "R2_clock"),
        ("JZC4118_5_WEP_source", "J_Z_coefficient", "eta_source_AB", "Delta_AB ln mu_obs[J_Z]", "R1_WEP_source_charge"),
        ("JZC4118_6_Gdot", "J_Z_coefficient", "Gdot_over_G", "partial_t ln mu_obs[J_Z]", "R9_Gdot"),
        ("JZC4118_7_EM_flux", "J_Z_coefficient", "w_EM;Phi_EM_boundary;Poynting_flux", "K_EM_JZ * Poynting_or_bound_flux_projection", "ENV3625_5_EM_source"),
        ("JZC4118_8_R11_operator", "J_Z_coefficient", "non_EH_operator_coefficients", "c_JZ_operator_vector from retained L^{-1}J_Z operator family", "R11_EH_operator_ledger"),
    ]
    for leak_id, family, coefficient, interpretation in dq_data:
        row = row_base()
        row.update(
            {
                "coefficient_id": leak_id,
                "family": family,
                "observable": coefficient,
                "coefficient_formula": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "arena": interpretation,
                "requirement": "numeric norm or theorem-zero; units; source path; no-cancellation guard",
                "score_status": "not_scoreable",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    for coeff_id, family, observable, formula, arena in jz_data:
        row = row_base()
        row.update(
            {
                "coefficient_id": coeff_id,
                "family": family,
                "observable": observable,
                "coefficient_formula": formula,
                "arena": arena,
                "requirement": "L inverse/profile; observable projection; bound source; no-cancellation guard",
                "score_status": "not_scoreable",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4118_0_derivation",
            "DCdagger has been converted into an exact Hamiltonian/quotient verticality theorem target.",
            "REAL_DERIVATION_STEP",
            "construct or source parent Omega/q/P/J/boundary owner; do not call DCdagger physical by naming it.",
        ),
        (
            "DEC4118_1_no_smuggling",
            "The Z-local-GR route now has a clean no-smuggling rule: verticality means Dq[Omega^{-1}DCdagger]=0 plus proper boundary charge.",
            "NO_CLOSURE_AXIOM_ALLOWED",
            "if any clause fails, keep Dq/J_Z leak coefficients live.",
        ),
        (
            "DEC4118_2_EM_flux",
            "Poynting/Maxwell flux is explicitly in the observable map, so EM cannot be hidden inside q_loc by language.",
            "EM_STRESS_COUNTED",
            "derive theorem-zero or score its flux coefficient in the next bound pack.",
        ),
        (
            "DEC4118_3_current_claim",
            "Verticality, local-GR silence, Newton/PPN/R10/R11 pass, and EM-source silence remain unclaimed.",
            "NO_CLAIM",
            "advance to same-parent Omega owner route or coefficient pack.",
        ),
        (
            "DEC4118_4_next_target",
            "The best route is constraint-first/Omega-owner construction, because it can turn the whole branch from closure into derivation.",
            "NEXT_TARGET_SELECTED",
            "4119-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4118_0",
            "target_doc": "4119-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_4119_Omega_owner_constraint_generator_or_DqJZ_bound_pack.py",
            "objective": "try to construct the same-parent parent action owner L -> theta/Omega/P/J/q that makes Omega_flat(e_X)=DCdagger and Dq[e_X]=0 executable; if this cannot be signed, convert every failed piece into Dq/J_Z/boundary/EM flux coefficient inputs",
            "success_gate": "parent Omega, q, P, J, and boundary charge are signed from one action and produce a proper vertical e_X, or every failed piece is source-ready with observable coefficients and bound targets",
            "reason": "4118 makes the verticality test exact; 4119 must either close the owner route or stop pretending the local branch is silent.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4118_0",
            "result": DECISION,
            "summary": (
                "4118 advances the local-GR/Newton route by deriving the exact vertical-generator contract for the "
                "DCdagger/Z branch: reconstruct e_X by Omega_flat(e_X)=DCdagger[X], require Dq[e_X]=0 on the parent "
                "quotient map, and require zero/proper boundary charge. This is the non-smuggling route into the 4117 "
                "J_Z=0 theorem. The current corpus does not yet claim verticality because the same-parent Omega/q/P/J/"
                "boundary owner is unsigned; therefore Dq leak, J_Z coefficient, boundary, and EM/Poynting flux rows remain live."
            ),
            "verticality_test_written": "True",
            "z_observable_map_written": "True",
            "same_parent_owner_signed": "False",
            "verticality_claimed": "False",
            "score_ready": "False",
            "claim_state": "no verticality, local_GR, Newton, PPN, R10, R11, WEP, clock, Gdot, or EM_source claim",
            "next_target": "4119 Omega-owner constraint generator or Dq/JZ/boundary/EM coefficient pack",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4118_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4118_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4118_VERTICAL_GENERATOR_CRITERION": SOURCE_DIR / "P8_Y5_R2FR_4118_VERTICAL_GENERATOR_CRITERION.csv",
        "P8_Y5_R2FR_4118_DCDAGGER_VERTICAL_GENERATOR_MAP": SOURCE_DIR / "P8_Y5_R2FR_4118_DCDAGGER_VERTICAL_GENERATOR_MAP.csv",
        "P8_Y5_R2FR_4118_Z_OBSERVABLE_MAP": SOURCE_DIR / "P8_Y5_R2FR_4118_Z_OBSERVABLE_MAP.csv",
        "P8_Y5_R2FR_4118_DQ_Z_LEAK_AND_JZ_COEFFICIENTS": SOURCE_DIR / "P8_Y5_R2FR_4118_DQ_Z_LEAK_AND_JZ_COEFFICIENTS.csv",
        "P8_Y5_R2FR_4118_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4118_DECISION_GATES.csv",
        "P8_Y5_R2FR_4118_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4118_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4118_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4118_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4118 - Vertical Generator Z Map or J_Z Coefficient Runner",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- This is forward progress, not a vibes ledger: `DCdagger` is now converted into the exact local test it must pass to become a genuine parent vertical generator.",
        "- The required chain is `Omega_flat(e_X)=DCdagger[X]`, then `Dq[e_X]=0`, then zero/proper boundary charge.",
        "- If that chain closes from one parent action, the 4117 `J_Z=0` theorem can be used without smuggling a plateau/closure axiom.",
        "- If it does not close, the failed pieces are physical leakage rows: `Dq`, `J_Z`, boundary charge, and EM/Poynting flux coefficients.",
        "",
        "## Strongest Current Result",
        "",
        "- The local branch now has a necessary-and-sufficient style contract for the DCdagger route:",
        "  `exists e_X: Omega_flat(e_X)=DCdagger[X]` and `Dq[e_X]=0` and `Q_boundary` is zero/proper.",
        "- That is the right mathematical door into local GR/Newton silence: it would make `Z` a gauge/constraint direction rather than a hidden physical field.",
        "- The current corpus does not yet sign the same-parent owner `L -> theta/Omega/P/J/q`, so no local-GR/PPN/R10/R11/EM claim is made.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(
        [
            "",
            "## Vertical Generator Criterion",
            "",
            "| criterion_id | statement | formula | current_status |",
            "|---|---|---|---|",
        ]
    )
    for row in vertical_generator_criterion_rows():
        sections.append(f"| {row['criterion_id']} | {row['statement']} | `{row['formula']}` | {row['current_status']} |")
    sections.extend(["", "## DCdagger To Parent Generator", "", "| map_id | formula | current_status |", "|---|---|---|"])
    for row in dcdagger_map_rows():
        sections.append(f"| {row['map_id']} | `{row['formula']}` | {row['current_status']} |")
    sections.extend(["", "## Observable Residual Map", "", "| map_id | observable | map_formula | current_status |", "|---|---|---|---|"])
    for row in observable_map_rows():
        sections.append(f"| {row['map_id']} | {row['observable']} | `{row['map_formula']}` | {row['current_status']} |")
    sections.extend(["", "## Decisions", "", "| decision_id | status | next_action |", "|---|---|---|"])
    for row in decision_rows():
        sections.append(f"| {row['decision_id']} | {row['status']} | {row['next_action']} |")
    sections.extend(
        [
            "",
            "## Next Target",
            "",
            "- `4119-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md`",
            "- Try the parent-owner/constraint route first. If it fails, stop treating the local branch as silent and convert every leak into executable coefficient/bound rows.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4118_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4118_VERTICAL_GENERATOR_CRITERION": vertical_generator_criterion_rows,
        "P8_Y5_R2FR_4118_DCDAGGER_VERTICAL_GENERATOR_MAP": dcdagger_map_rows,
        "P8_Y5_R2FR_4118_Z_OBSERVABLE_MAP": observable_map_rows,
        "P8_Y5_R2FR_4118_DQ_Z_LEAK_AND_JZ_COEFFICIENTS": leak_coefficient_rows,
        "P8_Y5_R2FR_4118_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4118_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4118_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    text_parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            text_parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(text_parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4118_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4118_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4118_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    criterion_text = flatten_rows([outputs["P8_Y5_R2FR_4118_VERTICAL_GENERATOR_CRITERION"]])
    criterion_ok = all(token in criterion_text for token in ["Omega_flat(e_X)=DCdagger[X]", "Dq[e_X]", "Q_boundary", "J_Z=0"])
    add("VAL4118_3_criterion", "vertical generator criterion includes Omega, Dq, boundary, and J_Z consequence", criterion_ok, "criterion tokens checked")

    map_text = flatten_rows([outputs["P8_Y5_R2FR_4118_DCDAGGER_VERTICAL_GENERATOR_MAP"]])
    map_ok = all(token in map_text for token in ["same-parent", "theta", "Omega", "q", "P", "J"])
    add("VAL4118_4_dcdagger_map", "DCdagger map requires same-parent theta/Omega/P/J/q ownership", map_ok, "map tokens checked")

    observable_text = flatten_rows([outputs["P8_Y5_R2FR_4118_Z_OBSERVABLE_MAP"]])
    observable_ok = all(token in observable_text for token in ["q_loc", "gamma_minus_1", "beta_minus_1", "alpha1", "Poynting", "non_EH"])
    add("VAL4118_5_observable_map", "observable residual map covers q_loc, PPN, EM/Poynting, and R11 arenas", observable_ok, "observable tokens checked")

    coeff_text = flatten_rows([outputs["P8_Y5_R2FR_4118_DQ_Z_LEAK_AND_JZ_COEFFICIENTS"]])
    coeff_ok = all(token in coeff_text for token in ["Dq_leak", "J_Z_coefficient", "not_scoreable", "Poynting_flux"])
    add("VAL4118_6_coefficients", "Dq and J_Z coefficient rows remain live and not score-ready", coeff_ok, "coefficient tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4118_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4119-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md"
    add("VAL4118_7_next_target", "next target is 4119 Omega owner route", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4118_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no verticality" in status_rows_local[0].get("claim_state", "")
    add("VAL4118_8_status", "status records decision and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4118_9_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4118*")) or any(FORMALIZATION.rglob("4118-Y5-R2FR*"))
    add("VAL4118_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4118_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4118_VALIDATION.csv"
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
