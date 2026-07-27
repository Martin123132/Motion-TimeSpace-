from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2214"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2214-Y5-R2FR-algebraic-residual-coefficient-map-or-DqZ-source-descent-proof.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2214_SOURCE_REGISTER.csv",
    "descent_attempt": OUT / "P8_Y5_PARENT_QLOC_2214_DQZ_SOURCE_DESCENT_PROOF_ATTEMPT.csv",
    "coefficient_map": OUT / "P8_Y5_PARENT_QLOC_2214_ALGEBRAIC_RESIDUAL_COEFFICIENT_MAP.csv",
    "arena_projection": OUT / "P8_Y5_PARENT_QLOC_2214_ARENA_PROJECTION_MAP.csv",
    "acquisition_rows": OUT / "P8_Y5_PARENT_QLOC_2214_NONCLAIM_COEFFICIENT_ACQUISITION_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2214_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2214_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2214_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2214_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2214_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2214_ALGEBRAIC_RESIDUAL_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2214_ARENA_PROJECTION_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_ALGEBRAIC_RESIDUAL_MAP_2214_NONCLAIM.csv",
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


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


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
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2214_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2214-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2214*",
        "*P8_Y5_BRR545_2214*",
        "*Y5_R2FR_algebraic_residual_coefficient_map_or_DqZ_source_descent_proof_2214*",
        "*JR2214*",
        "*PARENT_QLOC_ALGEBRAIC_RESIDUAL_MAP_2214*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2213_handoff",
            ROOT / "2213-Y5-R2FR-rank-zero-source-current-identity-or-algebraic-residual-row.md",
            ["NEXT2213_0_2214", "RALG2213_1_observed_residual_vector", "VAL2213_OVERALL"],
            "2213 selects the algebraic residual coefficient map and Dq_Z/source descent proof attempt.",
        ),
        (
            "2213_residual",
            OUT / "P8_Y5_PARENT_QLOC_2213_ALGEBRAIC_RESIDUAL_ROW.csv",
            ["RALG2213_0_eliminated_coordinate", "RALG2213_4_DqZ_leak_piece", "STAGED_FOR_2214_COEFFICIENT_MAP"],
            "machine-readable R_alg skeleton.",
        ),
        (
            "2213_arena_blockers",
            OUT / "P8_Y5_PARENT_QLOC_2213_ARENA_PROJECTION_BLOCKER.csv",
            ["APB2213_0_Newton", "APB2213_2_R10", "APB2213_6_R11"],
            "arena projection blockers to expand into coefficient rows.",
        ),
        (
            "2213_clause_audit",
            OUT / "P8_Y5_PARENT_QLOC_2213_JA_BA_DQZ_CLAUSE_AUDIT.csv",
            ["JBD2213_0_M_lock", "JBD2213_3_DqZ_zero", "JBD2213_6_verdict"],
            "J_A/B_A/Dq_Z/CDB/M-lock clause audit.",
        ),
        (
            "1675_leak_vector",
            OUT / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
            ["LEAK1675_0_coframe", "LEAK1675_4_boundary", "LEAK1675_5_residual_lock"],
            "Dq_Z leak components to map into arena projections.",
        ),
        (
            "1620_chain_rule",
            OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
            ["CR1620_1_zero_lemma", "CR1620_5_verdict", "SOURCE_CURRENT_ZERO_NOT_DERIVED_CURRENT_MTS"],
            "source-current zero lemma and current failure.",
        ),
        (
            "1045_functor",
            OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            ["MFS1045_1_observed_coframe_functor", "MFS1045_5_constants_split", "MFS1045_6_verdict"],
            "coframe/matter functor clauses that would collapse Dq_Z and J_A.",
        ),
        (
            "1229_source_coupling",
            OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
            ["THM1229_1_iff", "THM1229_3_residual_vector", "OBSTRUCTION_ACTIVE"],
            "universal source coupling obstruction and source residual vector.",
        ),
        (
            "1023_descent",
            OUT / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
            ["CDA1023_0_metric_chain_rule", "CDA1023_3_projector_boundary", "CDA1023_4_verdict"],
            "conditional metric chain rule and open boundary/projector coupling.",
        ),
    ]
    rows: list[dict[str, Any]] = []
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


def descent_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            attempt_id="DSD2214_0_exact_chain_rule",
            target="collapse J_A and E_DqZ by descent",
            mathematical_statement="delta_Z S_matter = D Sbar.Dq_Z + J_theta Lie_Z(theta) + J_direct[Z] + delta_Z B_matter.",
            current_status="EXACT_CONDITIONAL_FORMULA_AVAILABLE",
            collapse_condition="Dq_Z=0, Lie_Z(theta)=0, J_direct=0, and boundary/projector terms proper or zero.",
            current_failure="each collapse condition is unsigned in the current parent branch.",
            result_for_2214="do not set J_A or E_DqZ to zero; expose their coefficients.",
        ),
        base_row(
            attempt_id="DSD2214_1_metric_coframe_channel",
            target="collapse observed metric/coframe leakage",
            mathematical_statement="If e_obs=Obs_e(q(Phi)) and Z is vertical/constraint-eliminated, then Dq_Z[e_obs,g_obs,mu,D]=0.",
            current_status="CONDITIONAL_SUPPORT_NOT_PARENT_SIGNED",
            collapse_condition="parent-owned observed coframe functor plus measure/connection descent.",
            current_failure="1045 and 1675 keep coframe/measure/connection descent unsigned.",
            result_for_2214="retain K_coframe^I coefficient rows.",
        ),
        base_row(
            attempt_id="DSD2214_2_source_weight_channel",
            target="collapse Newton/source normalization leakage",
            mathematical_statement="If all source multipliers are quotient-equivalent to one common scale or null-projected in every arena, source residual q_source^nu vanishes.",
            current_status="IFF_CONTRACT_ONLY",
            collapse_condition="single action scale/current-owner theorem or null-projection proof.",
            current_failure="1229 countermodel keeps independent source weights alive.",
            result_for_2214="retain K_source^I and Delta_w_Z coefficient rows.",
        ),
        base_row(
            attempt_id="DSD2214_3_constants_marker_channel",
            target="collapse clock/EM/material marker leakage",
            mathematical_statement="Lie_Z(theta_A)=0 and no hidden material marker/source-only frame implies no direct clock/EM/WEP source.",
            current_status="NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            collapse_condition="constants are representation/superselection data or retained explicit residual fields.",
            current_failure="1045 and 1023 keep constants/markers/hidden frames legal unless explicitly ruled out.",
            result_for_2214="retain K_theta^I and K_marker^I coefficient rows.",
        ),
        base_row(
            attempt_id="DSD2214_4_boundary_projector_channel",
            target="collapse B_A and P_loc leakage",
            mathematical_statement="B_A=0 only if the boundary primitive is proper/exact on the compact collar and source-worldtube/corner/reference/projector terms vanish or are separately bounded.",
            current_status="PARTIAL_NARROW_ZERO_ONLY",
            collapse_condition="proper-collar zero plus source-boundary/projector no-flux theorem.",
            current_failure="source-worldtube/corner/reference and projector commutator terms remain open.",
            result_for_2214="retain K_boundary^I and K_comm^I coefficient rows.",
        ),
        base_row(
            attempt_id="DSD2214_5_verdict",
            target="Dq_Z/source descent proof",
            mathematical_statement="No current clause collapses the full R_obs^I map to theorem-zero.",
            current_status="PROOF_ATTEMPT_FAILS_CURRENT_CORPUS",
            collapse_condition="all above clauses close in one parent action signature.",
            current_failure="M_AB lock, source-current, boundary, Dq_Z and arena projections remain unsigned together.",
            result_for_2214="emit coefficient map and acquisition rows instead of claiming local GR/Newton.",
        ),
    ]


def coefficient_map_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            coefficient_id="CM2214_0_M_inverse",
            object="algebraic lock / inverse response",
            coefficient_symbol="G_alg^{AB}",
            exact_role="maps source vector S_B into eliminated coordinate Z^A",
            symbolic_definition="G_alg^{AB}=(M^{-1})^{AB} on parent-owned non-null quotient directions; else M^+ plus null constraint P_null S=0",
            collapse_or_bound_condition="M_AB rank/sign/units/eigenbasis parent-signed and null directions removed or bounded",
            current_status="MISSING_PARENT_SIGNATURE",
            required_source="parent quadratic action Hessian, quotient basis, units, rank/sign theorem",
            acquisition_status="ACQUIRE_BEFORE_ANY_NUMERIC_LOCAL_TEST",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_1_J_source",
            object="source-current forcing",
            coefficient_symbol="J_A",
            exact_role="ordinary matter/source normalization forcing of Z",
            symbolic_definition="J_A=D Sbar.Dq_Z + J_theta Lie_Z(theta) + J_direct[Z] + delta_Z B_matter",
            collapse_or_bound_condition="chain-rule premises close or every term gets finite source-backed coefficient",
            current_status="SOURCE_CURRENT_ZERO_BLOCKED",
            required_source="matter descent, no-marker/current owner, direct vertex list, matter boundary term",
            acquisition_status="NONCLAIM_COEFFICIENT_ROW_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_2_B_boundary",
            object="boundary/projector forcing",
            coefficient_symbol="B_A",
            exact_role="edge/projector/source-worldtube forcing of Z",
            symbolic_definition="B_A=B_A^proper+B_A^worldtube+B_A^corner+B_A^reference+[P_loc,D]_A",
            collapse_or_bound_condition="proper-collar zero plus source-worldtube/corner/reference/projector no-flux theorem",
            current_status="BOUNDARY_PROJECTOR_OPEN",
            required_source="boundary primitive, compact-support condition, source-edge rows, projector commutator",
            acquisition_status="NONCLAIM_COEFFICIENT_ROW_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_3_CDB",
            object="connection/domain/boundary commutator forcing",
            coefficient_symbol="C_A^CDB",
            exact_role="strict-branch leakage from K_conn, K_domain, K_boundary and K_comm",
            symbolic_definition="C_A^CDB=C_A^conn+C_A^domain+C_A^boundary+C_A^comm",
            collapse_or_bound_condition="CDB principal-symbol/source split shows zero or finite residual in each component",
            current_status="LIVE_PARALLEL_BLOCKER",
            required_source="CDB derivative-order extraction and componentwise source/boundary split",
            acquisition_status="NONCLAIM_COEFFICIENT_ROW_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_4_R_src_readout",
            object="source/readout residual forcing",
            coefficient_symbol="R_A^src/readout/projector",
            exact_role="constants, markers, hidden frames, readout standards and source normalization forcing",
            symbolic_definition="R_A=R_A^theta+R_A^marker+R_A^hidden_frame+R_A^clock+R_A^EM+R_A^source_measure",
            collapse_or_bound_condition="ordinary matter functor/no-marker/source-owner theorem or finite rows by channel",
            current_status="MATTER_SOURCE_READOUT_DESCENT_UNSIGNED",
            required_source="1045 matter functor, 1229 source coupling, 1023 coupling descent, arena-specific readout maps",
            acquisition_status="NONCLAIM_COEFFICIENT_ROW_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_5_E_DqZ",
            object="observed descent leak",
            coefficient_symbol="E_DqZ^I",
            exact_role="direct observed arena leakage after algebraic elimination",
            symbolic_definition="E_DqZ^I=Pi_coframe^I Dq_Z[e,g,mu,D]+Pi_source^I Dq_Z[J_H]+Pi_readout^I Dq_Z[O_i]+Pi_boundary^I Dq_Z[B_edge,P_loc,Q_X]",
            collapse_or_bound_condition="Dq_Z=0 theorem or finite LEAK1675 projection coefficients",
            current_status="DESCENT_LEAK_RETAINED",
            required_source="1675 leak vector, projection coefficients, arena units",
            acquisition_status="NONCLAIM_COEFFICIENT_ROW_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_6_L_arena",
            object="arena projection",
            coefficient_symbol="L_A^I",
            exact_role="maps eliminated coordinate/source response into measurable arena residual I",
            symbolic_definition="R_obs^I=L_A^I G_alg^{AB}(J_B+B_B+C_B^CDB+R_B)+E_DqZ^I",
            collapse_or_bound_condition="linearized weak-field/readout solution supplies L_A^I with units and bounds",
            current_status="ARENA_PROJECTION_MISSING",
            required_source="Newton, PPN, R10/contact, WEP, clock, EM, orbital and R11 projection maps",
            acquisition_status="NONCLAIM_ARENA_ROWS_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            coefficient_id="CM2214_7_verdict",
            object="full algebraic residual map",
            coefficient_symbol="R_obs^I",
            exact_role="single nonclaim map for all strict-branch local tests",
            symbolic_definition="R_obs^I=L_A^I G_alg^{AB}S_B+E_DqZ^I, S_B=J_B+B_B+C_B^CDB+R_B^src/readout/projector",
            collapse_or_bound_condition="all coefficients are either theorem-zero or source-backed finite numbers below arena bounds",
            current_status="MAP_DERIVED_SYMBOLIC_NUMERIC_INPUTS_MISSING",
            required_source="all rows CM2214_0 through CM2214_6",
            acquisition_status="STAGED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
        ),
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            arena_id="APR2214_0_Newton",
            arena="Newton/source-normalized GM",
            projection_formula="Delta_GM = L_GM,A G_alg^{AB}S_B + E_GM,DqZ",
            needs_coefficients="G_alg;J_source;B_boundary;CDB;source_weight;L_GM;E_GM",
            missing_now="single action scale/current-owner theorem; measured Hamiltonian mass map; L_GM units",
            strict_branch_rule="contact/algebraic source residual only, not alpha(lambda)",
            score_ready=False,
        ),
        base_row(
            arena_id="APR2214_1_PPN",
            arena="PPN gamma,beta,alpha_i,xi,Gdot",
            projection_formula="Delta_PPN^I = L_PPN,A^I G_alg^{AB}S_B + E_PPN,DqZ^I",
            needs_coefficients="G_alg;L_PPN;E_DqZ;weak-field metric solution; source boundary split",
            missing_now="linearized metric solution and residual-to-PPN basis",
            strict_branch_rule="no local-GR pass until every PPN residual row is zero or bounded",
            score_ready=False,
        ),
        base_row(
            arena_id="APR2214_2_R10",
            arena="short-range/R10",
            projection_formula="F_R10 or contact residual = L_R10,A G_alg^{AB}S_B + E_R10,DqZ",
            needs_coefficients="G_alg;source/test charge projection; contact geometry; CDB range check",
            missing_now="strict branch has no lambda; live CDB must reopen range or row remains contact/bound residual",
            strict_branch_rule="do not run alpha(lambda) for strict branch",
            score_ready=False,
        ),
        base_row(
            arena_id="APR2214_3_WEP",
            arena="WEP/composition",
            projection_formula="eta_AB = L_WEP,A^{AB} G_alg^{AC}(Delta J_C^species+Delta R_C^marker)+E_WEP,DqZ^{AB}",
            needs_coefficients="species weight split; marker silence; L_WEP; composition source map",
            missing_now="no-marker/species-weight theorem not parent-signed",
            strict_branch_rule="composition dependence must be theorem-zero or finite bounded",
            score_ready=False,
        ),
        base_row(
            arena_id="APR2214_4_clock_EM",
            arena="clocks/EM/fine-structure",
            projection_formula="Delta_clock/alpha = L_theta,A G_alg^{AB}S_B + Pi_theta Lie_Z(theta) + E_readout,DqZ",
            needs_coefficients="theta superselection; clock readout map; EM standards map; hidden-frame coefficients",
            missing_now="constants/markers/hidden frames remain legal counterexamples",
            strict_branch_rule="clock/EM standards cannot be silently assumed quotient-invariant",
            score_ready=False,
        ),
        base_row(
            arena_id="APR2214_5_orbital",
            arena="orbital/local dynamics",
            projection_formula="Delta_orbit^I = L_orb,A^I G_alg^{AB}(J_B+B_B+C_B^CDB+R_B)+E_orb,DqZ^I",
            needs_coefficients="weak-field source map; worldtube boundary; compact-source projector; ephemeris observable map",
            missing_now="source-worldtube and weak-field residual map open",
            strict_branch_rule="orbital pass requires source/boundary rows, not just bulk algebra",
            score_ready=False,
        ),
        base_row(
            arena_id="APR2214_6_R11",
            arena="non-EH/R11 operator family",
            projection_formula="c_R11^I = L_R11,A^I G_alg^{AB}S_B + E_R11,DqZ^I",
            needs_coefficients="operator basis; EFT dimensions; projection to non-EH coefficients",
            missing_now="operator units and basis map missing",
            strict_branch_rule="R11 row stays symbolic until basis and units are owned",
            score_ready=False,
        ),
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    specs = [
        ("ACQ2214_0_M", "G_alg/M_AB", "M_AB rank, sign, units, eigenbasis, null projector", "parent quadratic action; quotient basis", "all arenas"),
        ("ACQ2214_1_J", "J_A", "matter descent, theta silence, direct vertex list, matter boundary term", "parent matter functor and current-owner theorem", "Newton;WEP;R10;clock;EM"),
        ("ACQ2214_2_B", "B_A", "proper/worldtube/corner/reference/projector coefficients", "boundary primitive and source-worldtube ledger", "R10;WEP;orbital"),
        ("ACQ2214_3_CDB", "C_A^CDB", "K_conn/K_domain/K_boundary/K_comm source split and derivative order", "CDB principal-symbol extraction", "PPN;R10;orbital;R11"),
        ("ACQ2214_4_Rsrc", "R_A^src/readout/projector", "source weights, markers, hidden frames, clock/EM readouts", "1045/1229/1023 parent signatures", "Newton;WEP;clock;EM"),
        ("ACQ2214_5_EDqZ", "E_DqZ^I", "LEAK1675 projection coefficients and units", "Dq_Z leak vector plus arena maps", "PPN;R10;WEP;clock;EM;orbital;R11"),
        ("ACQ2214_6_LNewton", "L_GM,A", "Newton/source-normalized GM projection", "weak-field/source normalization derivation", "Newton"),
        ("ACQ2214_7_LPPN", "L_PPN,A^I", "PPN projection vector", "linearized weak-field metric solution", "PPN"),
        ("ACQ2214_8_LR10", "L_R10,A", "strict contact projection or CDB range-owner projection", "R10 force/contact map and CDB range decision", "R10"),
        ("ACQ2214_9_LWEP", "L_WEP,A", "composition projection", "species/source material map", "WEP"),
        ("ACQ2214_10_LClockEM", "L_clock/EM,A", "clock and fine-structure projection", "constants/readout map", "clock;EM"),
        ("ACQ2214_11_LOrbital", "L_orb,A^I", "orbital observable projection", "weak-field compact source and ephemeris map", "orbital"),
        ("ACQ2214_12_LR11", "L_R11,A^I", "non-EH operator projection", "R11 operator basis and EFT units", "R11"),
    ]
    for acquisition_id, coefficient, required_input, source_needed, arena in specs:
        rows.append(
            base_row(
                acquisition_id=acquisition_id,
                coefficient=coefficient,
                required_input=required_input,
                source_needed=source_needed,
                arena=arena,
                current_value="MISSING_PARENT_INPUT",
                current_units="MISSING_UNITS",
                source_path="MISSING_SOURCE_PATH",
                status="VALID_FOR_CLAIM_FALSE_PENDING_SOURCE",
                score_ready=False,
                valid_prediction_row=False,
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2214_0_DqZ_source_descent",
            gate="Dq_Z/source descent theorem closes",
            status="BLOCKED_NONCLAIM",
            reason="descent attempt identifies exact clauses but no parent action signs them together.",
        ),
        base_row(
            gate_id="CG2214_1_coefficient_map",
            gate="R_obs coefficient map written",
            status="PASS_NONCLAIM",
            reason="symbolic map R_obs^I=L_A^I G_alg^{AB}S_B+E_DqZ^I is explicit.",
        ),
        base_row(
            gate_id="CG2214_2_acquisition_coverage",
            gate="all surviving components have acquisition rows",
            status="PASS_NONCLAIM",
            reason="M, J, B, CDB, source/readout, E_DqZ and arena projections all have nonclaim rows.",
        ),
        base_row(
            gate_id="CG2214_3_score_ready",
            gate="any local test row score-ready",
            status="BLOCKED_NONCLAIM",
            reason="all coefficient values, units and source paths remain missing.",
        ),
        base_row(
            gate_id="CG2214_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="M_AB lock and source/descent zeros are not proved; coefficient rows are symbolic only.",
        ),
        base_row(
            gate_id="CG2214_5_GitHub",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation checkpoint only.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2214_0_gain",
            decision="RALG_MAP_IS_NOW_EXPLICIT",
            rationale="the strict branch now has a single algebraic coefficient map instead of scattered blockers.",
            next_action="fill or derive each coefficient row.",
        ),
        base_row(
            decision_id="DEC2214_1_descent",
            decision="DQZ_SOURCE_DESCENT_NOT_CLOSED",
            rationale="the chain-rule route is exact but still needs parent signatures for coframe, source weights, markers and boundary.",
            next_action="do not collapse J_A or E_DqZ to zero yet.",
        ),
        base_row(
            decision_id="DEC2214_2_next",
            decision="MAB_LOCK_FIRST",
            rationale="without G_alg=M^{-1}/M^+, no source/current coefficient can be turned into a bounded local prediction.",
            next_action="derive M_AB rank/sign/units/eigenbasis or demote strict branch to pseudoinverse/null residual branch.",
        ),
        base_row(
            decision_id="DEC2214_3_scope",
            decision="NO_LOCAL_CLAIM_NO_R10_LAMBDA",
            rationale="strict branch remains algebraic/contact; alpha(lambda) still belongs only to a live CDB range-owner branch.",
            next_action="keep all rows nonclaim and private.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2214_0_2215",
            selection_status="selected",
            target_file="2215-Y5-R2FR-MAB-lock-signature-or-pseudoinverse-residual-branch.md",
            target_script="scripts/Y5_R2FR_MAB_lock_signature_or_pseudoinverse_residual_branch_2215.py",
            objective="derive whether M_AB is parent-owned, signed, unit-normalized and invertible on physical quotient directions; if not, write the M^+/null residual branch explicitly.",
            success_condition="G_alg row becomes parent-signed or the null/pseudoinverse obstruction is staged as a nonclaim residual with arena projections.",
            do_not_do="do not claim local GR/Newton, do not score local tests, do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2214_1_source_parallel",
            selection_status="held_parallel",
            target_file="2215b-Y5-R2FR-source-current-owner-and-no-marker-proof.md",
            target_script="scripts/Y5_R2FR_source_current_owner_and_no_marker_proof_2215b.py",
            objective="derive source-current/no-marker/current-owner theorem to collapse J_A and source/readout forcing.",
            success_condition="J_A row theorem-zeroes for ordinary matter or receives finite source-backed coefficient rows.",
            do_not_do="do not assume source weights are universal.",
        ),
        base_row(
            route_id="NEXT2214_2_CDB_parallel",
            selection_status="held_parallel",
            target_file="2213b-Y5-R2FR-CDB-principal-symbol-extraction.md",
            target_script="scripts/Y5_R2FR_CDB_principal_symbol_extraction_2213b.py",
            objective="decide whether CDB reopens a genuine principal-symbol/range branch or only adds algebraic/source leakage.",
            success_condition="CDB components classify as kinetic, algebraic, boundary, source, or zero.",
            do_not_do="do not resurrect R10 lambda without a principal symbol.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["acquisition_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["arena_projection"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["coefficient_map"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        count = 0
        if source.exists():
            shutil.copyfile(source, target)
            copied = True
            parse_ok, count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    descent_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    acquisition_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2214_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2214_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    descent_ok = any(row.get("attempt_id") == "DSD2214_5_verdict" and row.get("current_status") == "PROOF_ATTEMPT_FAILS_CURRENT_CORPUS" for row in descent_rows)
    add("VAL2214_02_descent_attempt", descent_ok, "Dq_Z/source descent proof attempted and correctly not adopted")

    required_coeffs = {"CM2214_0_M_inverse", "CM2214_1_J_source", "CM2214_2_B_boundary", "CM2214_3_CDB", "CM2214_4_R_src_readout", "CM2214_5_E_DqZ", "CM2214_6_L_arena", "CM2214_7_verdict"}
    coeff_ok = required_coeffs <= {row.get("coefficient_id") for row in coefficient_rows}
    coeff_ok = coeff_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in coefficient_rows)
    add("VAL2214_03_coefficient_map", coeff_ok, "full R_obs coefficient map staged with no scoring flags")

    arena_ok = len(arena_rows) == 7 and all(not truthy(row.get("score_ready")) for row in arena_rows)
    add("VAL2214_04_arena_projection_map", arena_ok, "seven arena projection rows staged and non-score-ready")

    acquisition_ok = len(acquisition_rows_) == 13
    acquisition_ok = acquisition_ok and all(row.get("current_value") == "MISSING_PARENT_INPUT" for row in acquisition_rows_)
    acquisition_ok = acquisition_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in acquisition_rows_)
    add("VAL2214_05_acquisition_rows", acquisition_ok, "all required coefficient acquisition rows are explicit and nonclaim")

    claim_ok = any(row.get("gate_id") == "CG2214_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2214_3_score_ready" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2214_06_claim_gate", claim_ok, "local claims and score-ready gates remain blocked")

    decision_ok = any(row.get("decision") == "MAB_LOCK_FIRST" for row in decision_rows_)
    add("VAL2214_07_decision", decision_ok, "decision ledger selects M_AB lock first")

    next_ok = any(row.get("route_id") == "NEXT2214_0_2215" and "MAB" in str(row.get("target_file")) for row in next_rows)
    add("VAL2214_08_next_target", next_ok, "2215 M_AB lock/pseudoinverse branch selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2214_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2214_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, descent_rows, coefficient_rows, arena_rows, acquisition_rows_, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2214_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_missing_promoted = all(not truthy(row.get("score_ready")) for row in arena_rows)
    no_missing_promoted = no_missing_promoted and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in acquisition_rows_)
    add("VAL2214_12_missing_not_promoted", no_missing_promoted, "missing inputs are not promoted to score-ready or prediction rows")

    formalization_clean = not formalization_has_2214_artifacts()
    add("VAL2214_13_formalization_clean", formalization_clean, "formalization-workbench has no 2214 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2214_14_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2214_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2214 attempts Dq_Z/source descent, refuses theorem-zero, builds the full nonclaim algebraic coefficient map, and selects M_AB lock/pseudoinverse branch next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    descent_rows: list[dict[str, Any]],
    coefficient_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    acquisition_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2214 - Y5/R2FR Algebraic Residual Coefficient Map Or DqZ Source Descent Proof",
        "",
        "## Current Verdict",
        "",
        "2214 tries the derivation route first. The chain-rule/descent route is mathematically exact, but the current parent branch still does not sign the clauses needed to set `J_A`, `B_A`, `Dq_Z`, source/readout terms, or CDB leakage to zero.",
        "",
        "So the useful result is the coefficient map:",
        "",
        "`R_obs^I = L_A^I G_alg^{AB} S_B + E_DqZ^I`, with `S_B = J_B + B_B + C_B^CDB + R_B^src/readout/projector`.",
        "",
        "This is not a claim. It is the strict branch's local-test contract: every future Newton/PPN/R10/WEP/clock/EM/orbital/R11 statement must either theorem-zero one of these terms or provide a sourced finite coefficient.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Dq_Z / Source Descent Proof Attempt",
        "",
        md_table(descent_rows, ["attempt_id", "target", "mathematical_statement", "current_status", "collapse_condition", "current_failure", "result_for_2214", "valid_for_claim"]),
        "",
        "## Algebraic Residual Coefficient Map",
        "",
        md_table(coefficient_rows, ["coefficient_id", "object", "coefficient_symbol", "exact_role", "symbolic_definition", "collapse_or_bound_condition", "current_status", "required_source", "acquisition_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Arena Projection Map",
        "",
        md_table(arena_rows, ["arena_id", "arena", "projection_formula", "needs_coefficients", "missing_now", "strict_branch_rule", "score_ready", "valid_for_claim"]),
        "",
        "## Nonclaim Coefficient Acquisition Rows",
        "",
        md_table(acquisition_rows_, ["acquisition_id", "coefficient", "required_input", "source_needed", "arena", "current_value", "current_units", "source_path", "status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is progress, but it is the unglamorous kind: the local branch now has an engineering interface. We did not prove GR today; we made it much harder to fool ourselves tomorrow. The next genuinely high-leverage move is `M_AB`: if the algebraic lock is not parent-signed, the whole strict branch becomes a pseudoinverse/null-residual problem.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    descent_rows = descent_attempt_rows()
    coefficient_rows = coefficient_map_rows()
    arena_rows = arena_projection_rows()
    acquisition_rows_ = acquisition_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["descent_attempt"], descent_rows),
        (OUTPUTS["coefficient_map"], coefficient_rows),
        (OUTPUTS["arena_projection"], arena_rows),
        (OUTPUTS["acquisition_rows"], acquisition_rows_),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        descent_rows,
        coefficient_rows,
        arena_rows,
        acquisition_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        descent_rows,
        coefficient_rows,
        arena_rows,
        acquisition_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
