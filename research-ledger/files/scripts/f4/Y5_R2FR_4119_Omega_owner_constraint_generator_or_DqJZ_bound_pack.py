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
DOC_PATH = ROOT / "4119-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_STRICT_QUOTIENT_ABSENT_POLE_CURRENT_SPINE_4119"
CHECKPOINT_ID = "4119"
DECISION = "STRICT_QUOTIENT_ABSENT_POLE_THEOREM_CONSTRUCTED_DQZ_EVALUATION_NEXT"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4119_00_4118_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4118_NEXT_TARGET.csv",
        "4119-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md",
        "4118 selected the same-parent Omega-owner or coefficient-pack target.",
    ),
    "SRC4119_01_4118_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4118_STATUS.csv",
        "DCDAGGER_VERTICAL_GENERATOR_TEST_WRITTEN_Z_MAP_UNSIGNED_OMEGA_OWNER_NEXT",
        "Current-chain vertical generator contract.",
    ),
    "SRC4119_02_3632_owner_routes": (
        SOURCE_DIR / "P8_Y5_R2FR_3632_SAME_PARENT_OWNER_ROUTES.csv",
        "strict quotient action / no independent X or Z pole",
        "Older owner-route ranking: strict quotient is the cleanest local-test route.",
    ),
    "SRC4119_03_3632_chain_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_3632_OMEGA_THETA_PJQ_CHAIN_GATE.csv",
        "OWNER_CHAIN_NOT_SIGNED_BOUND_PACK_REQUIRED",
        "Older same-parent chain gate for Omega/theta/P/J/q/boundary.",
    ),
    "SRC4119_04_3632_bound_pack": (
        SOURCE_DIR / "P8_Y5_R2FR_3632_DQJZ_BOUND_PACK.csv",
        "Dq_Z_norm",
        "Dq/J_Z/X-sector fallback pack if strict quotient fails.",
    ),
    "SRC4119_05_3633_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3633_STRICT_QUOTIENT_THEOREM.csv",
        "no_X_Green_function",
        "Older conditional strict-quotient absent-pole theorem.",
    ),
    "SRC4119_06_3633_qmap": (
        SOURCE_DIR / "P8_Y5_R2FR_3633_CANDIDATE_Q_MAP.csv",
        "QMAP3633_4_excluded_residual_fibre",
        "Older candidate q-map split and excluded residual fibre row.",
    ),
    "SRC4119_07_3633_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3633_ABSENT_POLE_AUDIT.csv",
        "NO_CLAIM_DQZ_TARGET_SELECTED",
        "Older audit selecting Dq_Z_norm as next exact obstruction.",
    ),
    "SRC4119_08_3633_coverage": (
        SOURCE_DIR / "P8_Y5_R2FR_3633_R0_R11_COVERAGE_GATE.csv",
        "R10_fifth_force",
        "Coverage gate showing strict quotient helps R10 but not all local-GR channels.",
    ),
    "SRC4119_09_3633_fill_targets": (
        SOURCE_DIR / "P8_Y5_R2FR_3633_BOUND_PACK_FILL_TARGETS.csv",
        "BFT3633_0_Dq_Z_norm",
        "First bound-pack fill target: compute or prove Dq_Z_norm.",
    ),
    "SRC4119_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4119_Omega_owner_constraint_generator_or_DqJZ_bound_pack.py",
        "Reproducible generator for this 4119 checkpoint.",
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


def strict_theorem_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "THM4119_0_parent_quotient_setup",
            "Let C be parent configuration space, q:C->Q the ordinary-matter quotient, and V=ker(Dq) the fibre directions.",
            "v in V iff Dq[v]=0",
            "X/Z may label representatives only if they are fibre coordinates, not independent coordinates of Q.",
            "CONDITIONAL_DEFINITION_NOT_PARENT_SIGNED",
        ),
        (
            "THM4119_1_action_pullback",
            "If the parent action is a quotient pullback, every fibre variation is an off-shell null variation of the bulk action.",
            "S_parent[Phi,Psi]=S_red[q(Phi),Psi]+S_top[q(Phi)]; delta_v S_parent=delta S_red[Dq[v]]+delta S_top[Dq[v]]=0",
            "This is absence before variation, not a fitted K_X=0 or post-solution cancellation.",
            "CONDITIONAL_PROOF_CONSTRUCTED",
        ),
        (
            "THM4119_2_matter_source_descent",
            "If matter, clocks, source normalization and hidden source terms depend on Phi only through q(Phi), fibre source currents vanish.",
            "J_X=J_Z=(1/sqrt(-g)) delta(S_matter+S_source+S_hidden)/delta(X,Z)|_fibre=0",
            "This is the clean answer to the coupling problem only if the matter/source pullback is parent-owned.",
            "CONDITIONAL_PROOF_NOT_LIVE",
        ),
        (
            "THM4119_3_presymplectic_null",
            "If theta is also a quotient pullback up to an exact/proper boundary term, fibre directions are presymplectic null/proper gauge.",
            "theta=q^*theta_red+d beta; i_v Omega=0 modulo delta Q_v; Q_boundary[v]=0/exact/proper",
            "No physical Hamiltonian generator or edge charge survives in the fibre direction.",
            "CONDITIONAL_PROOF_NOT_LIVE_BOUNDARY_UNSIGNED",
        ),
        (
            "THM4119_4_no_green_function_pole",
            "If X/Z is not a physical tangent direction of the reduced phase space, no local X/Z propagator or Yukawa pole exists.",
            "no_XZ_Green_function: {Z_X,M_X^2,K_X,qbar_XT,Qbar_XH,lambda_X,alpha_X(lambda)} are absent-not-zero",
            "This removes the R10/R11 fifth-force pressure more cleanly than tiny coupling tuning.",
            "CONDITIONAL_PROOF_NOT_LIVE_DQZ_TARGET",
        ),
        (
            "THM4119_5_scope_limit",
            "Strict quotient absence closes only the X/Z pole/source channel; it does not by itself prove full local GR.",
            "R_local^i = R_EH/PPN/boundary/clock/EM channels + possible Dq leaks outside X/Z",
            "EH operator selection, PPN metric solution, clocks/WEP/Gdot, and EM/Poynting stress remain separate gates.",
            "THEOREM_SCOPE_LIMIT_NO_LOCAL_GR_CLAIM",
        ),
    ]
    for theorem_id, claim, identity, proof_step, live_status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "claim": claim,
                "identity": identity,
                "proof_step": proof_step,
                "live_status": live_status,
                "blocks_if_missing": "explicit q-map, matter/source descent, theta/Omega pullback, and boundary silence are required before any claim",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def pullback_contract_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "PAC4119_0_q_components",
            "ordinary quotient components",
            "q(Phi)=(g_obs,e_obs,connection_obs,matter_readout,source_mass,clock_map,theta_marker,boundary_projector)",
            "each component is defined before variation and before fitting data.",
            "Q_COMPONENT_LIST_CONTRACT_WRITTEN",
        ),
        (
            "PAC4119_1_excluded_fibre",
            "residual/fibre coordinates",
            "Fibre=(X,Z,phi,R_phys representative labels)",
            "these may appear only as redundant chart labels, constrained gauge labels, or absent quotient-null directions.",
            "EXCLUDED_FIBRE_CONTRACT_WRITTEN",
        ),
        (
            "PAC4119_2_action_form",
            "strict pullback parent action",
            "S_parent=S_red[q(Phi),Psi]+S_top[q(Phi)]+S_constraint[proper fibre gauge]",
            "no independent L_X/L_Z Hessian, source current, or finite-range pole is introduced.",
            "PULLBACK_ACTION_SHAPE_CONSTRUCTED_CONDITIONAL",
        ),
        (
            "PAC4119_3_theta_Omega_form",
            "quotient presymplectic owner",
            "theta_parent=q^*theta_red+d beta; Omega_parent=q^*Omega_red",
            "fibre directions are null unless a boundary charge makes them physical.",
            "PRESYMPLECTIC_PULLBACK_CONSTRUCTED_CONDITIONAL",
        ),
        (
            "PAC4119_4_boundary_rule",
            "edge/collar silence",
            "Q_boundary[partial_X/Z]=0, exact, or proper-gauge on the local compact collar",
            "prevents alpha3/source-normalization leakage through the edge.",
            "BOUNDARY_RULE_REQUIRED_NOT_SIGNED",
        ),
        (
            "PAC4119_5_claim_gate",
            "live claim criterion",
            "Dq[partial_X]=Dq[partial_Z]=0 componentwise AND theta/Omega/boundary pull back through q",
            "only then may X/Z pole/source rows be removed rather than bounded.",
            "CLAIM_GATE_NOT_MET",
        ),
    ]
    for contract_id, object_name, formula, condition, status in data:
        row = row_base()
        row.update(
            {
                "contract_id": contract_id,
                "object": object_name,
                "formula": formula,
                "condition": condition,
                "current_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def dqz_target_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("DQZ4119_0_geometry", "g_obs;e_obs;connection_obs", "partial_Z q_geometry", "Dq[partial_Z]=0 in observed geometry/coframe/connection", "MISSING_EXPLICIT_Q_GEOMETRY_Z_DERIVATIVE"),
        ("DQZ4119_1_matter_readout", "matter_readout;test_body_path", "partial_Z q_matter", "particle/matter equations read only q(Phi), not Z representative labels", "MISSING_MATTER_READOUT_Z_DERIVATIVE"),
        ("DQZ4119_2_source_mass", "source_mass;mu_obs;Hamiltonian_mass", "partial_Z q_source", "source normalization and Newtonian mass readout are Z independent", "MISSING_SOURCE_MASS_Z_DERIVATIVE"),
        ("DQZ4119_3_clock_marker", "clock_map;theta_marker;local_time_readout", "partial_Z q_clock_theta", "clock/redshift/material markers descend through q", "MISSING_CLOCK_THETA_Z_DERIVATIVE"),
        ("DQZ4119_4_boundary_projector", "boundary_projector;collar_charge;Pi_M", "partial_Z q_boundary plus Q_boundary[partial_Z]", "boundary/projector channel is zero, exact, or proper-gauge", "MISSING_BOUNDARY_Z_DERIVATIVE_AND_CHARGE"),
        ("DQZ4119_5_EM_stress", "Maxwell_F;T_EM;Poynting_flux", "partial_Z q_EM or Pi_EM^B Q_boundary", "EM/Poynting stress is either in the quotient variables or separately scored, not hidden", "MISSING_EM_POYNTING_Z_SEPARATION"),
        ("DQZ4119_6_X_parallel", "X fibre channel", "partial_X q and Q_boundary[partial_X]", "same absence test must hold for X if X and Z are the same local residual family", "MISSING_X_PARALLEL_DQ_TEST"),
        ("DQZ4119_7_norm", "Dq_Z_norm", "||Dq[partial_Z]|| over all listed components", "componentwise theorem-zero or first nonzero leak row with units/source/comparator", "NEXT_TARGET_EXACT_OBSTRUCTION"),
    ]
    for target_id, q_component, derivative, pass_condition, status in data:
        row = row_base()
        row.update(
            {
                "target_id": target_id,
                "q_component": q_component,
                "derivative_or_charge": derivative,
                "pass_condition": pass_condition,
                "current_status": status,
                "next_action": "evaluate from explicit q map or demote to executable Dq/J_Z coefficient row",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def coverage_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("R0_metric_limit", "metric/EH limit", "not_closed", "strict quotient does not choose EH-only operator by itself"),
        ("R1_WEP", "source/test body universality", "conditional_help", "helps only if matter/source descent through q is proved"),
        ("R2_clock", "redshift/local clock map", "conditional_help", "clock map must be Z/X independent"),
        ("R3_gamma", "PPN gamma", "not_closed", "requires weak-field metric solution and non-EH operator audit"),
        ("R4_beta", "PPN beta", "not_closed", "requires second-order weak-field solution"),
        ("R5_alpha1", "preferred-frame alpha1", "not_closed", "boundary/source-current channels remain live"),
        ("R6_alpha2", "preferred-frame alpha2", "not_closed", "boundary/source-current channels remain live"),
        ("R7_alpha3", "preferred-frame alpha3", "not_closed", "boundary charge silence is essential"),
        ("R8_xi", "preferred-location xi", "not_closed", "collar/projector dependence must be scored"),
        ("R9_Gdot", "time drift of source coupling", "conditional_help", "helps only if source and clock readouts descend through q"),
        ("R10_fifth_force", "Yukawa/fifth-force X/Z pole", "best_hit_if_DqZ_zero", "strict quotient removes the X/Z pole if absence theorem closes"),
        ("R11_operator_ledger", "non-EH operator coefficients", "partial_only", "X/Z pole absence helps but EH-only operator selection remains separate"),
        ("R12_EM_Poynting", "Maxwell/EM stress and Poynting flux", "not_closed", "must be quotient stress or separately bounded; not absorbed by wording"),
    ]
    for row_id, observable, strict_effect, still_missing in data:
        row = row_base()
        row.update(
            {
                "row_id": row_id,
                "observable": observable,
                "strict_quotient_effect": strict_effect,
                "still_missing": still_missing,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def fallback_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("FB4119_0_Dq_Z_norm", 1, "Dq_Z_norm", "Dq_leak", "||Dq[partial_Z]|| over geometry/source/clock/boundary/EM", "explicit q components; Z basis; norm convention; no-cancellation guard", "not_scoreable_q_map_missing"),
        ("FB4119_1_J_Z", 2, "J_Z", "source_current", "(1/sqrt(-g)) delta(S_matter+S_source+S_hidden)/delta Z", "matter/source pullback; hidden source terms; units", "not_scoreable_source_zero_not_derived"),
        ("FB4119_2_XZ_operator", 3, "Z_X;M_X^2;K_X;lambda_X", "physical_operator", "lambda_X=sqrt(Z_X/M_X^2); alpha_X=K_X Qbar_XH qbar_XT", "parent Hessian; units; Green-function normalization; source/test charges", "not_scoreable_parent_operator_missing"),
        ("FB4119_3_boundary_flux", 4, "Q_boundary;boundary_flux_XZ", "boundary_charge", "Q_boundary[partial_X/Z] plus projector leakage", "boundary class; reference term; Pi_M; compact-collar condition", "not_scoreable_boundary_owner_missing"),
        ("FB4119_4_EM_Poynting", 5, "w_EM;Phi_EM_boundary;Poynting_flux", "EM_stress_flux", "K_EM * Poynting_or_bound_flux_projection", "Maxwell stress definition; boundary flux normalization; comparator bound", "not_scoreable_EM_flux_owner_missing"),
    ]
    for target_id, rank, quantity, target_type, candidate_formula, required_inputs, score_status in data:
        row = row_base()
        row.update(
            {
                "target_id": target_id,
                "rank": rank,
                "quantity": quantity,
                "target_type": target_type,
                "candidate_formula": candidate_formula,
                "required_inputs": required_inputs,
                "score_status": score_status,
                "next_action": "keep nonclaim until theorem-zero or source-backed numeric coefficient exists",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4119_0_theorem",
            "The strict quotient absent-pole theorem is constructed in current chain: pullback through q makes fibre variations null and removes X/Z source/pole rows if all hypotheses close.",
            "CONDITIONAL_THEOREM_CONSTRUCTED",
            "use it as the preferred local route because it removes the coupling before variation rather than tuning it.",
        ),
        (
            "DEC4119_1_live_claim",
            "The live corpus does not yet prove the hypotheses: explicit q-map, matter/source descent, theta/Omega pullback, and boundary silence remain unsigned.",
            "NO_CLAIM",
            "do not claim local GR, Newton, PPN, R10, R11, WEP, clock, Gdot or EM silence.",
        ),
        (
            "DEC4119_2_exact_next",
            "The next non-vague obstruction is Dq_Z_norm componentwise across geometry, matter/source, clock/theta, boundary/projector, and EM/Poynting channels.",
            "NEXT_TARGET_REDUCED",
            "construct/evaluate the explicit q map or open the first nonzero leak row.",
        ),
        (
            "DEC4119_3_fallback",
            "If Dq_Z_norm is nonzero or cannot be theorem-zeroed, X/Z must become a scored residual family with J_Z, operator, boundary, and EM flux coefficients.",
            "BOUND_PACK_STAGED",
            "keep all fallback rows nonclaim until units, source paths, comparator bounds, and no-cancellation guards exist.",
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
            "next_id": "NEXT4119_0",
            "target_doc": "4120-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-XZ-source-row.md",
            "target_script": "scripts/Y5_R2FR_4120_explicit_q_map_and_DqZ_evaluation_or_XZ_source_row.py",
            "objective": "construct the explicit ordinary-matter quotient q enough to evaluate Dq[partial_Z] and Dq[partial_X] componentwise; if any component depends on X/Z, demote the absent-pole route and open source-ready J_Z/operator/boundary/EM flux rows",
            "success_gate": "Dq_Z_norm and Dq_X_norm are theorem-zero componentwise across geometry, matter/source, clock/theta, boundary/projector, and EM/Poynting channels, or the first nonzero leak is recorded with units/source/comparator/no-cancellation requirements",
            "reason": "4119 proves the conditional absent-pole theorem; 4120 must decide whether its q-map hypothesis is actually true.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4119_0",
            "result": DECISION,
            "summary": (
                "4119 constructs the current-chain strict quotient absent-pole theorem. If S_parent is a pullback "
                "through an ordinary-matter quotient q, and X/Z lie only in ker(Dq) with matter/source/theta/boundary "
                "also descending through q, then delta_X/Z S=0, J_X/J_Z=0, fibre directions are presymplectic null/proper, "
                "and there is no X/Z Green-function pole or Yukawa alpha row. This is the cleanest coupling route, but "
                "it is not claim-live until Dq_Z_norm/Dq_X_norm are proven zero componentwise."
            ),
            "theorem_constructed": "True",
            "dqz_evaluation_target_written": "True",
            "same_parent_owner_signed": "False",
            "local_gr_claimed": "False",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, R11, WEP, clock, Gdot, or EM_source claim",
            "next_target": "4120 explicit q-map and DqZ/DqX evaluation or XZ source row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4119_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4119_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4119_STRICT_QUOTIENT_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4119_STRICT_QUOTIENT_THEOREM.csv",
        "P8_Y5_R2FR_4119_PULLBACK_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4119_PULLBACK_CONTRACT.csv",
        "P8_Y5_R2FR_4119_DQZ_COMPONENT_TARGETS": SOURCE_DIR / "P8_Y5_R2FR_4119_DQZ_COMPONENT_TARGETS.csv",
        "P8_Y5_R2FR_4119_R0_R11_EM_COVERAGE": SOURCE_DIR / "P8_Y5_R2FR_4119_R0_R11_EM_COVERAGE.csv",
        "P8_Y5_R2FR_4119_FALLBACK_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4119_FALLBACK_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4119_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4119_DECISION_GATES.csv",
        "P8_Y5_R2FR_4119_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4119_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4119_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4119_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4119 - Omega Owner, Strict Quotient Absent Pole, or Bound Pack",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- This is the clean coupling route: do not make the coupling tiny; remove the physical pole before variation if `X/Z` are strict quotient-null fibre labels.",
        "- Conditional theorem: if `S_parent` is a pullback through `q` and `X/Z in ker(Dq)`, then `delta_X/Z S=0`, `J_X/J_Z=0`, and there is no `X/Z` Green-function/Yukawa pole.",
        "- Not claim-live yet: explicit `q`, matter/source descent, `theta/Omega` pullback, and boundary silence are not signed.",
        "- Next exact obstruction: compute/prove `Dq_Z_norm=0` and `Dq_X_norm=0` componentwise.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Strict Quotient Theorem", "", "| theorem_id | identity | live_status |", "|---|---|---|"])
    for row in strict_theorem_rows():
        sections.append(f"| {row['theorem_id']} | `{row['identity']}` | {row['live_status']} |")
    sections.extend(["", "## Pullback Contract", "", "| contract_id | formula | current_status |", "|---|---|---|"])
    for row in pullback_contract_rows():
        sections.append(f"| {row['contract_id']} | `{row['formula']}` | {row['current_status']} |")
    sections.extend(["", "## DqZ/DqX Evaluation Targets", "", "| target_id | q_component | pass_condition | current_status |", "|---|---|---|---|"])
    for row in dqz_target_rows():
        sections.append(f"| {row['target_id']} | {row['q_component']} | {row['pass_condition']} | {row['current_status']} |")
    sections.extend(["", "## Coverage Limits", "", "| row_id | observable | strict_quotient_effect | still_missing |", "|---|---|---|---|"])
    for row in coverage_rows():
        sections.append(f"| {row['row_id']} | {row['observable']} | {row['strict_quotient_effect']} | {row['still_missing']} |")
    sections.extend(["", "## Decisions", "", "| decision_id | status | next_action |", "|---|---|---|"])
    for row in decision_rows():
        sections.append(f"| {row['decision_id']} | {row['status']} | {row['next_action']} |")
    sections.extend(
        [
            "",
            "## Next Target",
            "",
            "- `4120-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-XZ-source-row.md`",
            "- Build the explicit quotient map enough to test `Dq[partial_Z]` and `Dq[partial_X]`; if any component leaks, open the first source-ready coefficient row instead of pretending it is silent.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4119_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4119_STRICT_QUOTIENT_THEOREM": strict_theorem_rows,
        "P8_Y5_R2FR_4119_PULLBACK_CONTRACT": pullback_contract_rows,
        "P8_Y5_R2FR_4119_DQZ_COMPONENT_TARGETS": dqz_target_rows,
        "P8_Y5_R2FR_4119_R0_R11_EM_COVERAGE": coverage_rows,
        "P8_Y5_R2FR_4119_FALLBACK_BOUND_ROWS": fallback_rows,
        "P8_Y5_R2FR_4119_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4119_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4119_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4119_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4119_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

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
    add("VAL4119_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4119_STRICT_QUOTIENT_THEOREM"]])
    theorem_ok = all(token in theorem_text for token in ["ker(Dq)", "delta_v S_parent", "J_X=J_Z", "no_XZ_Green_function"])
    add("VAL4119_3_theorem", "strict quotient theorem includes ker(Dq), null variation, source-zero, and absent-pole pieces", theorem_ok, "theorem tokens checked")

    contract_text = flatten_rows([outputs["P8_Y5_R2FR_4119_PULLBACK_CONTRACT"]])
    contract_ok = all(token in contract_text for token in ["q(Phi)", "S_parent", "theta_parent", "Omega_parent", "Q_boundary"])
    add("VAL4119_4_pullback_contract", "pullback contract includes q/action/theta/Omega/boundary requirements", contract_ok, "contract tokens checked")

    dqz_text = flatten_rows([outputs["P8_Y5_R2FR_4119_DQZ_COMPONENT_TARGETS"]])
    dqz_ok = all(token in dqz_text for token in ["Dq_Z_norm", "partial_Z", "source_mass", "Poynting", "boundary_projector", "partial_X"])
    add("VAL4119_5_dqz_targets", "DqZ/DqX targets cover source, boundary, and EM/Poynting channels", dqz_ok, "Dq target tokens checked")

    coverage_text = flatten_rows([outputs["P8_Y5_R2FR_4119_R0_R11_EM_COVERAGE"]])
    coverage_ok = all(token in coverage_text for token in ["R10_fifth_force", "R11_operator_ledger", "R12_EM_Poynting", "R3_gamma"])
    add("VAL4119_6_coverage", "coverage gate keeps R10/R11/PPN/EM limits separated", coverage_ok, "coverage tokens checked")

    fallback_text = flatten_rows([outputs["P8_Y5_R2FR_4119_FALLBACK_BOUND_ROWS"]])
    fallback_ok = all(token in fallback_text for token in ["Dq_Z_norm", "J_Z", "lambda_X", "Poynting_flux", "not_scoreable"])
    add("VAL4119_7_fallback_rows", "fallback bound rows retain Dq/JZ/operator/boundary/EM coefficients", fallback_ok, "fallback tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4119_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4120-Y5-R2FR-explicit-q-map-and-DqZ-evaluation-or-XZ-source-row.md"
    add("VAL4119_8_next_target", "next target is 4120 explicit q-map DqZ evaluation", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4119_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no local_GR" in status_rows_local[0].get("claim_state", "")
    add("VAL4119_9_status", "status records theorem and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4119_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4119*")) or any(FORMALIZATION.rglob("4119-Y5-R2FR*"))
    add("VAL4119_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4119_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4119_VALIDATION.csv"
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
