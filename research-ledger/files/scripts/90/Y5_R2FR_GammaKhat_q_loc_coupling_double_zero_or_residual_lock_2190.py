from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2190"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2190-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2190_SOURCE_REGISTER.csv",
    "derivation_gate": OUT / "P8_Y5_PARENT_QLOC_2190_DERIVATION_GATE.csv",
    "candidate_routes": OUT / "P8_Y5_PARENT_QLOC_2190_CANDIDATE_ROUTE_AUDIT.csv",
    "residual_lock": OUT / "P8_Y5_PARENT_QLOC_2190_QLOC_RESIDUAL_LOCK_INTERFACE.csv",
    "projection_queue": OUT / "P8_Y5_PARENT_QLOC_2190_LOCAL_TEST_PROJECTION_QUEUE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2190_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2190_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2190_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2190_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2190_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2190_QLOC_LOCAL_TEST_PROJECTION_QUEUE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2190_QLOC_RESIDUAL_LOCK_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_GAMMAKHAT_QLOC_DERIVATION_GATE_2190_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2190_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2190-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2190*",
        "*P8_Y5_BRR545_2190*",
        "*Y5_R2FR_GammaKhat_q_loc_coupling_double_zero_or_residual_lock_2190*",
        "*JR2190*",
        "*PARENT_GAMMAKHAT_QLOC_DERIVATION_GATE_2190*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2189_handoff",
            ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md",
            ["NEXT2189_0_2190", "Gamma/Khat/q_loc", "VAL2189_OVERALL"],
            "2189 selects Gamma/Khat/q_loc as the next non-circling derivation target.",
        ),
        (
            "GK_first_variation_contract",
            OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            ["GK513_0_action_existence", "GK513_3_double_zero", "GK513_5_boundary_no_flux"],
            "first-variation contract defines action, Helmholtz, Euler, double-zero, projector, and boundary clauses.",
        ),
        (
            "GK_action_candidates",
            OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
            ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch"],
            "candidate routes include metric-response scalar density and explicit residual branch.",
        ),
        (
            "GK_metric_response_audit",
            OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["MA515_1_Khat_metric_response", "MA515_4_double_zero", "MA515_6_units_and_readout"],
            "metric-response audit says Khat/Gamma are not yet matched as a variational stress with units.",
        ),
        (
            "Gamma_owner_candidates",
            OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner"],
            "candidate Gamma owners include response doublet, auxiliary energy, topological boundary, and residual runner.",
        ),
        (
            "q_loc_bound_spec",
            OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
            ["QB516_0_compact_shell_budget", "QB516_3_PPN_metric_tail", "QB516_4_R11_operator"],
            "bound runner spec defines the fallback local-test residual interface if owner fails.",
        ),
        (
            "q_loc_trigger_ledger",
            OUT / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
            ["BT517_0_owner_match_fails", "BT517_4_PPN_lock_missing"],
            "trigger ledger says owner/metric-response failure activates direct q_loc scoring.",
        ),
        (
            "1189_component_pack",
            ROOT / "1189-Y5-R10-q_loc-component-residual-pack-or-profile-theorem-zero-certificate.md",
            ["q_loc component residual pack", "theorem-zero certificate", "No claim"],
            "1189 componentized q_loc for PPN, R10, clock, and orbital interfaces.",
        ),
        (
            "1190_tracefree_solver",
            ROOT / "1190-Y5-R10-P_loc-parent-domain-commutator-or-tracefree-Khat-solver-gate.md",
            ["KLS1190_2_covariant_cancellation_condition", "PLC1190_2_derivative_commutator", "RES1190_3_Khat_metric_footprint"],
            "old 1190 proves a formal tracefree Khat route but leaves Ricci, P_loc, boundary, and amplitude residuals.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def derivation_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DG2190_0_identity_target",
            "q_loc identity",
            "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}).",
            "EXACT_TARGET_RESTATED",
            "this is the object that must be theorem-zero or residual-locked.",
        ),
        (
            "DG2190_1_action_owner",
            "S_GK exists",
            "There is a local diffeomorphism-invariant scalar action S_GK[g,Phi] whose Hilbert stress is T_GK^{mu nu}.",
            "REQUIRED_NOT_PROVED",
            "without this Gamma/Khat is bookkeeping, not a field-theory sector.",
        ),
        (
            "DG2190_2_metric_response",
            "Khat equals metric response",
            "K_hat^{mu nu}=K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} plus declared boundary convention.",
            "REQUIRED_NOT_PROVED",
            "metric-response mismatch becomes q_metric_response_defect.",
        ),
        (
            "DG2190_3_Helmholtz",
            "Helmholtz integrability",
            "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} has symmetric second variation up to boundary terms.",
            "REQUIRED_NOT_PROVED",
            "non-integrable stress becomes q_Helmholtz_defect.",
        ),
        (
            "DG2190_4_Ward_Euler",
            "Ward/Euler closure",
            "Diffeomorphism invariance gives nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary; compact local vacuum sets E_A=0.",
            "CONDITIONAL_THEOREM_WRITTEN_NOT_PARENT_SIGNED",
            "if action and Euler clauses close, q_loc becomes on-shell rather than plateau-imposed.",
        ),
        (
            "DG2190_5_double_zero",
            "T_GK double zero",
            "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0, equivalently Gamma/Khat amplitude and first variation vanish at the local fixed point.",
            "REQUIRED_NOT_PROVED",
            "first-order local hair remains live as epsilon_C0_GammaKhat and epsilon_dC_GammaKhat.",
        ),
        (
            "DG2190_6_Ploc",
            "P_loc owner/commutator",
            "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0, and derivative/readout commutator is zero or retained.",
            "REQUIRED_NOT_PROVED",
            "projection can otherwise hide unprojected force or boundary flux.",
        ),
        (
            "DG2190_7_boundary",
            "boundary/symplectic no flux",
            "integral_boundary Delta(theta_GK,Q_GK,tau)=0 or fixed topological subtraction on compact local collars.",
            "REQUIRED_NOT_PROVED",
            "bulk q_loc cancellation does not silence Hamiltonian/source leakage.",
        ),
        (
            "DG2190_8_tracefree_solver",
            "tracefree Khat solver route",
            "K_L can formally satisfy div K_L=grad Gamma_eff in a flat patch, but the curved condition includes Ricci, P_loc commutator, boundary, and amplitude debts.",
            "FORMAL_ROUTE_RETAINED_NOT_THEOREM_ZERO",
            "use as a candidate inside the residual interface, not as local-GR proof.",
        ),
        (
            "DG2190_9_verdict",
            "q_loc theorem-zero status",
            "The conditional theorem is exact, but current MTS does not parent-sign S_GK, metric response, Helmholtz, double-zero, P_loc, or boundary clauses together.",
            "QLOC_ZERO_NOT_CLAIMED_RESIDUAL_LOCK_REQUIRED",
            "q_loc becomes the official local-test residual interface until the missing certificates are real.",
        ),
    ]
    return [
        base_row(gate_id=gate_id, clause=clause, statement=statement, status=status, implication=implication)
        for gate_id, clause, statement, status, implication in specs
    ]


def candidate_route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CR2190_A_metric_response_density",
            "S_GK=-int sqrt(-g) Gamma_eff",
            "best formal action-owner route",
            "REFUSED_FOR_NOW",
            "Gamma_eff scalar-density owner and K_hat metric variation are not source-signed; units/readout map missing",
            "q_metric_response_defect;q_Helmholtz_defect",
        ),
        (
            "CR2190_B_response_doublet",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "candidate double-zero mechanism",
            "REFUSED_FOR_NOW",
            "doublet component map covers only partial sectors and is not locked to physical q_loc/PPN vector",
            "epsilon_C0_memory_response;epsilon_dC_memory_response;q_PPN_lock_defect",
        ),
        (
            "CR2190_C_positive_auxiliary",
            "positive auxiliary energy density",
            "candidate compact exterior gap",
            "REFUSED_FOR_NOW",
            "positive operator is formal; parent fields/source-free collar and boundary conditions are unsigned",
            "q_Euler_source_defect;q_gap_hair",
        ),
        (
            "CR2190_D_topological_boundary",
            "exact/topological GK density",
            "candidate bulk force-free sector",
            "REFUSED_FOR_NOW",
            "boundary/cohomology/reference class is not fixed before readout; boundary flux remains live",
            "q_boundary_flux;B_GK_flux",
        ),
        (
            "CR2190_E_tracefree_Khat_solver",
            "K_L^{mu nu}=2 nabla^mu nabla^nu phi - 1/2 g^{mu nu} Box phi",
            "formal cancellation route",
            "REFUSED_AS_THEOREM_ZERO_RETAINED_AS_COMPONENT",
            "curved source equation, Ricci term, P_loc commutator, boundary flux and Khat metric footprint remain open",
            "q_Ricci_Khat;q_Ploc_commutator;q_Khat_metric_footprint",
        ),
        (
            "CR2190_F_residual_lock",
            "no S_GK accepted yet",
            "safe local-test interface",
            "SELECTED_CURRENT_BRANCH",
            "keeps q_loc explicit instead of claiming plateau or bookkeeping zero",
            "q_loc_residual_vector;Delta_PPN_q;alpha_R10_q;clock_q;orbital_q",
        ),
    ]
    return [
        base_row(route_id=route_id, route=route, role=role, verdict=verdict, reason=reason, residuals=residuals)
        for route_id, route, role, verdict, reason, residuals in rows
    ]


def residual_lock_rows() -> list[dict[str, Any]]:
    rows = [
        ("QL2190_0_action", "q_action_owner_defect", "failure of a parent S_GK action to exist/source Gamma_eff and K_hat", "MISSING_PARENT_S_GK", "MISSING_ACTION_OWNER", "stress_divergence_or_force_density", "local_GR;PPN", "MISSING_SOURCE_PATH"),
        ("QL2190_1_metric_response", "q_metric_response_defect", "K_hat minus metric response of sqrt(-g)Gamma_eff under declared boundary convention", "MISSING_METRIC_RESPONSE_MATCH", "MISSING_KHAT_METRIC_RESPONSE", "stress_divergence_or_force_density", "PPN;R10;local_GR", "MISSING_SOURCE_PATH"),
        ("QL2190_2_Helmholtz", "q_Helmholtz_defect", "non-integrable stress defect if second variation symmetry fails", "MISSING_HELMHOLTZ_CERTIFICATE", "MISSING_HELMHOLTZ_INTEGRABILITY", "stress_divergence_or_force_density", "PPN;local_GR", "MISSING_SOURCE_PATH"),
        ("QL2190_3_Euler", "q_Euler_source_defect", "sum_A E_A nabla^nu Phi^A plus source-current terms in compact local vacuum", "MISSING_EULER_SOURCE_ZERO", "MISSING_EULER_CLOSURE", "force_density", "PPN;clocks;orbital", "MISSING_SOURCE_PATH"),
        ("QL2190_4_C0", "epsilon_C0_GammaKhat", "zeroth-order T_GK/GammaKhat amplitude at Phi0", "MISSING_C0_VALUE", "MISSING_TGK_ZERO", "dimensionless_or_stress_norm", "PPN;R10;local_GR", "MISSING_SOURCE_PATH"),
        ("QL2190_5_dC", "epsilon_dC_GammaKhat", "first variation partial_A T_GK(Phi0)", "MISSING_DC_VALUE", "MISSING_TGK_DERIVATIVE_ZERO", "dimensionless_operator_norm", "PPN;R10;local_GR", "MISSING_SOURCE_PATH"),
        ("QL2190_6_Ricci", "q_Ricci_Khat", "curved tracefree Khat leftover 2 R^nu_sigma nabla^sigma phi plus convention corrections", "MISSING_RICCI_KHAT_BOUND", "MISSING_CURVED_SOLVER_BOUND", "force_density_or_dimensionless_after_projection", "PPN;orbital", "MISSING_SOURCE_PATH"),
        ("QL2190_7_Ploc", "q_Ploc_commutator", "derivative/readout commutator (nabla_mu P_loc)K_hat and kernel leakage", "MISSING_PLOC_COMMUTATOR_BOUND", "MISSING_PLOC_PARENT_OWNER", "force_density_or_dimensionless_after_projection", "PPN_alpha_i;WEP;local_GR", "MISSING_SOURCE_PATH"),
        ("QL2190_8_boundary", "q_GK_boundary_flux", "compact local boundary/symplectic flux from theta_GK/Q_GK", "MISSING_GK_BOUNDARY_FLUX", "MISSING_BOUNDARY_NO_FLUX", "force_flux_or_GM_flux", "Newton;R10;R11;PPN", "MISSING_SOURCE_PATH"),
        ("QL2190_9_metric_footprint", "q_Khat_metric_footprint", "metric/PPN response from Khat carrier amplitude even if divergence cancellation works", "MISSING_METRIC_RESPONSE_MATRIX", "MISSING_KHAT_METRIC_SAFETY", "PPN_vector_or_metric_coefficients", "PPN;clocks;orbital", "MISSING_SOURCE_PATH"),
        ("QL2190_10_total", "q_loc_residual_vector_abs", "absolute no-cancellation vector envelope across action, metric-response, Helmholtz, Euler, double-zero, Ricci, P_loc, boundary, and metric-footprint components", "MISSING_COMPONENT_INPUTS", "RESIDUAL_LOCK_ACTIVE_COMPONENTS_MISSING", "arena_normalized_vector", "local_GR;PPN;R10;R11;clocks;orbital", "MISSING_SOURCE_PATH"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            value=value,
            status=status,
            units=units,
            observable_link=observable_link,
            source_path=source_path,
            score_ready=False,
        )
        for row_id, symbol, definition, value, status, units, observable_link, source_path in rows
    ]


def projection_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("PQ2190_0_PPN", "PPN", "Delta_PPN_q = R_PPN[q_loc_residual_vector]", "beta,gamma,alpha_i,zeta_i,xi response map", "MISSING_PPN_RESPONSE_OPERATOR", "valid only after observed-frame vector components and source normalization are declared"),
        ("PQ2190_1_R10", "R10_short_range", "alpha_R10_q(lambda)=R_R10[q_loc(lambda)]", "finite-range projection / alpha(lambda) conversion", "MISSING_R10_PROJECTION_OPERATOR", "use only nonclaim until units/source paths and bound curve are real"),
        ("PQ2190_2_R11", "R11_source_normalization", "c_GK_operator_vector(lambda)=R_R11[q_loc]", "operator/source-normalization coefficient vector", "MISSING_R11_OPERATOR_MAP", "parallel to PiM/source-measure rows"),
        ("PQ2190_3_clocks", "clock_time", "Delta_clock_q=R_clock[q_loc]", "clock redshift/frequency drift response", "MISSING_CLOCK_RESPONSE_OPERATOR", "requires matter frame and metric-readout owner"),
        ("PQ2190_4_orbital", "orbital_systems", "Delta_orbital_q=R_orbital[q_loc]", "perihelion/range/GMdot/orbital residual response", "MISSING_ORBITAL_RESPONSE_OPERATOR", "requires source mass and readout gauge lock"),
        ("PQ2190_5_shell_budget", "compact_shell_smoke", "max_shell_budget from QB516_0 is a nonclaim smoke input", "compact-shell leakage budget carried as fallback only", "NONCLAIM_SMOKE_ONLY", "not a pass until official arena projection and provenance are complete"),
    ]
    return [
        base_row(queue_id=queue_id, arena=arena, projected_quantity=projected_quantity, required_operator=required_operator, status=status, notes=notes)
        for queue_id, arena, projected_quantity, required_operator, status, notes in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2190_0_conditional_theorem", "q_loc zero theorem shape is written", "PASS_GUARDRAIL", "the exact certificates needed for a future theorem-zero are explicit"),
        ("CG2190_1_action_owner", "S_GK parent action exists and is source-signed", "BLOCKED_NONCLAIM", "current sources do not provide a full action owner"),
        ("CG2190_2_metric_response", "Khat is metric response of Gamma_eff", "BLOCKED_NONCLAIM", "metric-response audit remains unmatched"),
        ("CG2190_3_Helmholtz_Euler", "Helmholtz and Euler/Ward closure are parent-signed", "BLOCKED_NONCLAIM", "no integrability/Euler certificate is present"),
        ("CG2190_4_double_zero", "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 are parent-signed", "BLOCKED_NONCLAIM", "double-zero remains a requirement, not a result"),
        ("CG2190_5_Ploc_boundary", "P_loc and boundary no-flux are parent-signed", "BLOCKED_NONCLAIM", "projection and boundary residuals remain active"),
        ("CG2190_6_residual_lock", "q_loc residual interface is active", "PASS_GUARDRAIL", "q_loc is retained as explicit local-test vector instead of zeroed by assertion"),
        ("CG2190_7_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "q_loc theorem-zero is not proved and residual rows are not bounded"),
        ("CG2190_8_GitHub", "public/github update is triggered", "BLOCKED_NONCLAIM", "private goal work only; no GitHub action"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2190_0_gain",
            "QLOC_ZERO_THEOREM_CONTRACT_EXACT",
            "The required theorem-zero chain is now explicit: S_GK, metric response, Helmholtz, Euler/Ward closure, double-zero, P_loc, and boundary no-flux.",
            "selected",
        ),
        (
            "DEC2190_1_limit",
            "QLOC_ZERO_NOT_PROVED",
            "Current sources fail the owner, metric-response, Helmholtz, double-zero, P_loc, and boundary certificates together.",
            "selected",
        ),
        (
            "DEC2190_2_live_interface",
            "QLOC_RESIDUAL_LOCK_SELECTED",
            "Until those certificates exist, q_loc is the official local-test residual vector rather than a silent zero.",
            "selected",
        ),
        (
            "DEC2190_3_next",
            "BUILD_QLOC_COMPONENT_PROJECTION_RUNNER_NEXT",
            "The next non-circling move is to make the residual lock executable: component schema, units, arena response operators, and smoke projections.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2190_0_2191",
            selection_status="selected",
            target_file="2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            target_script="scripts/Y5_R2FR_q_loc_component_projection_runner_and_theorem_zero_certificate_2191.py",
            objective="turn the 2190 q_loc residual lock into an executable local-test interface: component schema, units, source paths, PPN/R10/R11/clock/orbital projection operators, and an all-or-nothing theorem-zero certificate slot",
            success_condition="q_loc zero remains false unless all theorem certificates pass; otherwise each arena has explicit nonclaim projection rows ready for sourced inputs",
            do_not_do="do not claim q_loc=0, do not use scalar proxy as vector proof, do not score placeholders as evidence, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2190_1_theory_parallel",
            selection_status="held_parallel",
            target_file="2191b-Y5-R2FR-GK-metric-response-Helmholtz-certificate-attempt.md",
            target_script="scripts/Y5_R2FR_GK_metric_response_Helmholtz_certificate_attempt_2191b.py",
            objective="attempt the pure derivation route for S_GK and K_hat metric response/Helmholtz symmetry using current Gamma owner candidates",
            success_condition="a real scalar density, metric-response formula, and second-variation symmetry are source-signed or the route is formally demoted",
            do_not_do="do not use response-doublet symmetry unless mapped to physical q_loc components",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["projection_queue"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["residual_lock"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["derivation_gate"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2190_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2190_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    gate_statuses = {row["status"] for row in rows_by_name["derivation_gate"]}
    derivation_pass = {"EXACT_TARGET_RESTATED", "FORMAL_ROUTE_RETAINED_NOT_THEOREM_ZERO", "QLOC_ZERO_NOT_CLAIMED_RESIDUAL_LOCK_REQUIRED"}.issubset(gate_statuses)
    validations.append(base_row(validation_id="VAL2190_02_derivation_gate", status="PASS" if derivation_pass else "FAIL", detail="q_loc identity, theorem-zero conditions and residual-lock verdict are explicit"))

    selected_routes = {row["route_id"] for row in rows_by_name["candidate_routes"] if row["verdict"] == "SELECTED_CURRENT_BRANCH"}
    validations.append(base_row(validation_id="VAL2190_03_candidate_routes", status="PASS" if "CR2190_F_residual_lock" in selected_routes else "FAIL", detail="derivation candidates refused for now; residual lock selected"))

    residual_symbols = ";".join(row["symbol"] for row in rows_by_name["residual_lock"])
    residual_required = ["q_action_owner_defect", "q_metric_response_defect", "q_Helmholtz_defect", "epsilon_C0_GammaKhat", "q_Ploc_commutator", "q_loc_residual_vector_abs"]
    residual_pass = all(symbol in residual_symbols for symbol in residual_required) and all(str(row["source_path"]).startswith("MISSING_") for row in rows_by_name["residual_lock"])
    validations.append(base_row(validation_id="VAL2190_04_residual_lock", status="PASS" if residual_pass else "FAIL", detail=f"q_loc residual components={len(rows_by_name['residual_lock'])} remain source-missing/nonclaim"))

    arenas = {row["arena"] for row in rows_by_name["projection_queue"]}
    required_arenas = {"PPN", "R10_short_range", "R11_source_normalization", "clock_time", "orbital_systems", "compact_shell_smoke"}
    validations.append(base_row(validation_id="VAL2190_05_projection_queue", status="PASS" if required_arenas.issubset(arenas) else "FAIL", detail=f"projection arenas covered={len(required_arenas.intersection(arenas))}/{len(required_arenas)}"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2190_06_claim_gate", status="PASS" if "PASS_GUARDRAIL" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses else "FAIL", detail="claim gate blocks q_loc/local-GR while retaining residual interface"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2190_07_decision", status="PASS" if "QLOC_RESIDUAL_LOCK_SELECTED" in decisions and "BUILD_QLOC_COMPONENT_PROJECTION_RUNNER_NEXT" in decisions else "FAIL", detail="decision locks q_loc residual and selects executable projection runner next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2190_08_next_target", status="PASS" if "NEXT2190_0_2191" in routes else "FAIL", detail="2191 q_loc component projection runner selected"))

    validations.append(base_row(validation_id="VAL2190_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2190_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2190_11_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2190_12_formalization_clean", status="PASS" if not formalization_has_2190_artifacts() else "FAIL", detail="formalization-workbench has no 2190 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2190_13_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2190_OVERALL", status=overall, detail="2190 refuses q_loc theorem-zero promotion, locks q_loc as the official local-test residual interface, and selects executable projection runner next"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2190 - Y5/R2FR GammaKhat q_loc Coupling Double-Zero Or Residual Lock",
        "",
        "## Current Verdict",
        "",
        "2190 is the cleanest possible current answer to the `Gamma/Khat/q_loc` problem: **not derived zero yet, but no longer a ghost**.",
        "",
        "The exact target remains",
        "",
        "`q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})`.",
        "",
        "A future parent proof may still make this vanish. The required theorem chain is precise: `S_GK` exists, `K_hat` is the metric response of `Gamma_eff`, Helmholtz symmetry holds, Ward/Euler closure is parent-signed, `T_GK(Phi0)=0`, `partial_A T_GK(Phi0)=0`, `P_loc` is parent-owned, and boundary flux vanishes.",
        "",
        "Current evidence does not close that chain. Therefore the active branch is a residual lock: `q_loc` becomes the official local-test residual vector for PPN/R10/R11/clock/orbital projections until the theorem-zero certificates are real.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Derivation Gate",
        "",
        md_table(rows_by_name["derivation_gate"], ["gate_id", "clause", "statement", "status", "implication", "valid_for_claim"]),
        "",
        "## Candidate Route Audit",
        "",
        md_table(rows_by_name["candidate_routes"], ["route_id", "route", "role", "verdict", "reason", "residuals", "valid_for_claim"]),
        "",
        "## q_loc Residual Lock Interface",
        "",
        md_table(rows_by_name["residual_lock"], ["row_id", "symbol", "definition", "value", "status", "units", "observable_link", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Local-Test Projection Queue",
        "",
        md_table(rows_by_name["projection_queue"], ["queue_id", "arena", "projected_quantity", "required_operator", "status", "notes", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This is not a retreat from derivation; it is the proper discipline around a missing derivation. `q_loc=0` is still a valid future theorem target, but the project now has a safe interface if it is not yet proved.",
        "",
        "Next: make that interface executable, with components, units, source paths, and arena response operators. Then the theory can be tested without smuggling local GR by silence.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "derivation_gate": derivation_gate_rows(),
        "candidate_routes": candidate_route_rows(),
        "residual_lock": residual_lock_rows(),
        "projection_queue": projection_queue_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
