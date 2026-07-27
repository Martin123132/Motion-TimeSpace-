from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3631"
BRANCH_ID = "MTS_R2FR_Y5_VERTICAL_GENERATOR_Z_MAP_OR_JZ_COEFFICIENT_RUNNER_3631"
DOC = ROOT / "3631-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3631_SOURCE_REGISTER.csv",
        "vertical_generator_test": RESIDUALS / "P8_Y5_R2FR_3631_VERTICAL_GENERATOR_TEST.csv",
        "dcdagger_generator_map": RESIDUALS / "P8_Y5_R2FR_3631_DCDAGGER_VERTICAL_GENERATOR_MAP.csv",
        "z_observable_map": RESIDUALS / "P8_Y5_R2FR_3631_Z_OBSERVABLE_MAP.csv",
        "leak_coefficients": RESIDUALS / "P8_Y5_R2FR_3631_DQ_Z_LEAK_AND_JZ_COEFFICIENTS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3631_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3631_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3631_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_vertical_generator_Z_map_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3631_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3630",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3630_NEXT_TARGET.csv"),
            "needle": "vertical generator",
            "role": "3630 selected the vertical-generator and Z-observable map as the next unsigned premise.",
        },
        {
            "source_id": "parent_action_3630",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv"),
            "needle": "Dq[e_A]=0",
            "role": "parent-action clause requiring Z directions to be vertical to q.",
        },
        {
            "source_id": "signature_audit_3630",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3630_PARENT_SIGNATURE_AUDIT.csv"),
            "needle": "MISSING_DQ_VERTICAL_GENERATOR_MAP",
            "role": "current vertical-generator blocker.",
        },
        {
            "source_id": "field_chart_1667",
            "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv"),
            "needle": "PFC1667_3_Z_block",
            "role": "candidate parent field chart containing Q, R_phys, Z, matter, and boundary blocks.",
        },
        {
            "source_id": "dq_tests_1667",
            "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv"),
            "needle": "DQT1667_1_Z_normal_form",
            "role": "prior Dq tests showing Z verticality is not closed.",
        },
        {
            "source_id": "dq_leaks_1667",
            "path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"),
            "needle": "DQL1667_0_Dq_Z",
            "role": "nonclaim Dq leak rows to carry forward if verticality fails.",
        },
        {
            "source_id": "dcdagger_591",
            "path": str(RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv"),
            "needle": "DCA591_4_compare_to_Omega_flat",
            "role": "DCdagger/Omega-flat comparison can be sharpened into a vertical-generator reconstruction test.",
        },
        {
            "source_id": "omega_compare_591",
            "path": str(RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"),
            "needle": "CMP591_5_verdict",
            "role": "prior verdict that the formula exists but lacks parent Omega/P/J ownership.",
        },
        {
            "source_id": "noether_583",
            "path": str(RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"),
            "needle": "NMC583_1_vertical_generator",
            "role": "Noether momentum-map vertical generator contract.",
        },
        {
            "source_id": "lx_candidates_669",
            "path": str(RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"),
            "needle": "LX669_1_vertical_constraint",
            "role": "vertical constraint is the best active theorem route if an actual generator can be supplied.",
        },
        {
            "source_id": "local_residual_template",
            "path": str(RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv"),
            "needle": "R11_EH_operator_ledger",
            "role": "R0-R11 observable target rows for the Z-observable map.",
        },
        {
            "source_id": "jz_coeffs_3629",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv"),
            "needle": "JZC3629_8_R11_operator",
            "role": "J_Z coefficient rows to merge with any retained Dq leak.",
        },
    ]


def source_rows(t: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in source_map():
        path = Path(source["path"])
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source["source_id"],
                "path": source["path"],
                "exists": exists,
                "needle": source["needle"],
                "needle_found": exists and contains(path, source["needle"]),
                "role": source["role"],
            }
        )
    return rows


def vertical_generator_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "VGT3631_0_chart_split",
            "statement": "Use a local parent chart Phi=(Q_vis,R_phys,Z,phi,Psi,theta,B) and treat q(Phi)=Q_vis only if the parent action adopts this split before readout.",
            "formula": "Dq[e_A]=D_Q q[e_A^Q]+D_R q[e_A^R]+D_Z q[e_A^Z]+D_B q[e_A^B]",
            "pass_condition": "q is an explicit parent map and the chosen e_A gives zero in every visible matter/source/readout/boundary component.",
            "current_status": "CHART_CANDIDATE_EXISTS_NOT_PARENT_ADOPTED",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "VGT3631_1_naive_Z_generator",
            "statement": "The tempting generator e_A=partial/partial Z^A is vertical only in a product chart where q is independent of Z.",
            "formula": "Dq[partial_ZA]=partial q/partial Z^A",
            "pass_condition": "partial_Z q=0 for coframe, source/readout, theta markers, and boundary/projector data.",
            "current_status": "NOT_PROVED_RETAIN_DQ_Z_LEAK",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "VGT3631_2_compensated_vertical_generator",
            "statement": "If q has Z-dependence, a compensated generator can be written formally but is not automatically a parent symmetry.",
            "formula": "e_A=partial_ZA-C_A^I partial_QI, with D_Q q[C_A]=D_ZA q when D_Q q has a right inverse",
            "pass_condition": "C_A is parent-defined, local, covariant, not after-solve fitted, and does not move observed matter/source data physically.",
            "current_status": "FORMAL_REPAIR_WRITTEN_NOT_ADMISSIBLE_WITHOUT_PARENT_OWNER",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "VGT3631_3_constraint_first_escape",
            "statement": "The cleanest route is to make Z a first-class constrained/vertical variable before matter coupling, not to hide its visible effect afterwards.",
            "formula": "S_parent=S_obs[q]+int Lambda^A C_A; e_epsilon^i={Phi^i,G[epsilon]}; Dq[e_epsilon]=0; Q_boundary[epsilon]=0/proper",
            "pass_condition": "constraint algebra closes, Noether charge is differentiable, and boundary charge is zero/proper on compact local collars.",
            "current_status": "BEST_ROUTE_SELECTED_NOT_CLOSED",
            "source_path": str(RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "VGT3631_4_verdict",
            "statement": "Current corpus has a computable vertical-generator test but not a parent-signed generator.",
            "formula": "Z vertical iff Dq[e_A]=0 and e_A comes from parent Noether/constraint/Omega data before readout.",
            "pass_condition": "VGT3631_0 through VGT3631_3 pass together.",
            "current_status": "VERTICAL_GENERATOR_NOT_CLAIMED",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_DECISION.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def dcdagger_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "DVG3631_0_reconstruction_equation",
            "statement": "DCdagger becomes a vertical-generator test only after it is matched to the field-space symplectic form.",
            "formula": "Omega_flat(e_X)_A = DCdagger_A[X]",
            "meaning": "if Omega is invertible/modded by gauge, e_X=Omega^{-1}DCdagger[X] is the candidate generator.",
            "current_status": "FORMULA_PROGRESS_PARENT_OMEGA_MISSING",
            "source_path": str(RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "DVG3631_1_verticality_gate",
            "statement": "The reconstructed generator must be invisible to the quotient.",
            "formula": "Dq[Omega^{-1}DCdagger[X]]=0",
            "meaning": "this is the exact bridge from the DCdagger machinery to quotient descent.",
            "current_status": "TEST_WRITTEN_NOT_RUNNABLE_WITHOUT_Q_AND_OMEGA",
            "source_path": str(RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "DVG3631_2_boundary_charge_gate",
            "statement": "A vertical generator still fails local GR if its Hamiltonian boundary charge is improper or physical.",
            "formula": "G[epsilon]=int Sigma epsilon^A C_A + int_boundary Q_epsilon; require Q_epsilon=0/exact/proper and delta G differentiable",
            "meaning": "prevents a fake vertical proof that leaves alpha3/source-normalization flux on the collar.",
            "current_status": "BOUNDARY_CHARGE_NOT_DERIVED",
            "source_path": str(RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "DVG3631_3_parent_owner_gate",
            "statement": "P, J, theta, Omega, and q must come from one parent action, not separate fits.",
            "formula": "delta L=E_i delta Phi^i+d theta; C_X=-nabla P+J; DCdagger=Omega_flat(e_X)",
            "meaning": "same-parent ownership is the criterion that keeps this a field theory rather than closure bookkeeping.",
            "current_status": "SAME_PARENT_OWNER_MISSING",
            "source_path": str(RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "DVG3631_4_verdict",
            "statement": "DCdagger has been mapped to the actual vertical-generator contract, but the contract is unsigned.",
            "formula": "parent L -> theta/Omega/P/J/q -> e_X=Omega^{-1}DCdagger -> Dq[e_X]=0 -> Q_boundary proper",
            "meaning": "this is the right target for a derivation; if it fails, Dq and J_Z coefficients must be scored.",
            "current_status": "DCDAGGER_TO_VERTICAL_MAP_CONDITIONAL_NO_CLAIM",
            "source_path": str(RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def z_observable_rows(t: str) -> list[dict[str, object]]:
    templates = [
        ("ZOM3631_0_q_loc", "q_loc^nu", "Z_q^nu = Pi_q Z", "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}", "MISSING_Z_TO_QLOC_PROJECTION"),
        ("ZOM3631_1_gamma_beta", "gamma_minus_1;beta_minus_1", "Z_PPN_scalar = Pi_gamma_beta Z", "weak-field metric solution maps Z stress/source to gamma,beta", "MISSING_WEAK_FIELD_Z_METRIC_SOLUTION"),
        ("ZOM3631_2_preferred_frame", "alpha1;alpha2;alpha3;xi", "Z_PF^I = Pi_PF^I Z + boundary_flux^I", "preferred-frame/location projections must include collar and source-current terms", "MISSING_PREFERRED_FRAME_Z_PROJECTION"),
        ("ZOM3631_3_Newton_source", "delta_Newton_MTS;mu_extra;alpha(lambda)", "Z_N = Pi_M L^{-1}J_Z plus Dq_Z source leak", "Newton/R10 depends on source-normalization and finite-range profile, not only bulk q_loc", "MISSING_SOURCE_MASS_AND_RANGE_MAP"),
        ("ZOM3631_4_clock_WEP_Gdot", "alpha_clock;eta_source_AB;Gdot/G", "Z_clock/source/time = Pi_clock/source/time Z", "clock/WEP/Gdot need same observed coframe and species/source charge descent", "MISSING_CLOCK_WEP_TIME_MAP"),
        ("ZOM3631_5_EM_flux", "w_EM;Phi_EM_boundary", "Z_EM = physical F-sector stress or coupling leakage, not hidden q_loc", "Poynting/Maxwell flux must be counted as physical stress/current unless absent or boundary-silent", "MISSING_EM_FLUX_SEPARATION_MAP"),
        ("ZOM3631_6_R11", "non_EH_operator_coefficients", "Z_R11 = operator-family projection of retained Z/Dq/J_Z terms", "R11 needs executable operator coefficients for any retained non-EH/source-normalization branch", "MISSING_EXECUTABLE_R11_Z_VECTOR"),
    ]
    rows: list[dict[str, object]] = []
    for map_id, observable, formula, condition, status in templates:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "map_id": map_id,
                "observable": observable,
                "map_formula": formula,
                "condition_for_use": condition,
                "rank_gate": "the Z basis must span this residual component with no hidden null leakage",
                "current_status": status,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "ZOM3631_7_verdict",
            "observable": "full local residual vector",
            "map_formula": "R_local^i = M^i_A Z^A + N^i_a Dq_leak^a + B^i_boundary + O(Z^2)",
            "condition_for_use": "M has full row coverage for R0-R11 or unspanned components have independent theorem-zero/bounds",
            "rank_gate": "FULL_RANK_OR_BOUND_EVERY_MISSING_COMPONENT",
            "current_status": "Z_OBSERVABLE_MAP_NOT_CLAIMED_BOUND_ROWS_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    )
    return rows


def leak_rows(t: str) -> list[dict[str, object]]:
    dq_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv")
    jz_rows = read_csv(RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv")
    rows: list[dict[str, object]] = []
    for row in dq_rows:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "row_id": row["leak_id"].replace("DQL1667", "DQL3631"),
                "type": "Dq_leak",
                "quantity": row["symbol"],
                "formula_or_template": row["value_or_formula"],
                "affected_channel": row["channel"],
                "minimum_inputs": "numeric norm or theorem-zero; units; source path; no-cancellation guard",
                "score_status": "not_scoreable",
                "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    for row in jz_rows:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "row_id": row["coupling_id"].replace("JZC3629", "JZC3631"),
                "type": "J_Z_coefficient",
                "quantity": row["observable"],
                "formula_or_template": row["prediction_template"],
                "affected_channel": row["target_row"],
                "minimum_inputs": row["missing_input"] + "; L inverse/profile; observable projection; bound source",
                "score_status": "not_scoreable",
                "source_path": str(RESIDUALS / "P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv"),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def decision_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3631_0_DCd_to_vertical",
            "decision": "DCdagger is no longer just boundary algebra: the exact generator test is Omega_flat(e_X)=DCdagger[X] followed by Dq[e_X]=0.",
            "status": "REAL_DERIVATION_TARGET_WRITTEN",
            "next_action": "source or construct parent Omega, q, P, J and boundary charge to run the test",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3631_1_Z_map",
            "decision": "Z cannot be treated as physical merely by naming it; the required map is R_local=MZ+N Dq_leak+B_boundary.",
            "status": "OBSERVABLE_MAP_CONTRACT_WRITTEN",
            "next_action": "derive M and prove full-rank coverage or bound each unspanned component",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3631_2_current_claim",
            "decision": "Verticality and Z-observable lock are not claimed; Dq leak and J_Z coefficient rows remain live.",
            "status": "NO_CLAIM",
            "next_action": "carry both leak families into the next owner-or-bound runner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3631_3_next_target",
            "decision": "Next target should try the constraint-first/Omega owner route, because it is the only path that can make Z genuinely vertical without after-solve compensation.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3632-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3631_0",
            "result": "DCDAGGER_TO_VERTICAL_TEST_WRITTEN_Z_MAP_UNSIGNED_BOUND_ROWS_STAGED",
            "summary": "3631 turns the loose DCdagger clue into an exact vertical-generator test: solve Omega_flat(e_X)=DCdagger[X], then require Dq[e_X]=0 and proper/zero boundary charge. It also writes the required observable map R_local=MZ+N Dq_leak+B_boundary. Current MTS does not yet claim verticality or Z-observable lock because q, Omega/P/J, boundary charge, and full-rank residual map are unsigned; Dq leak and J_Z coefficient rows remain staged.",
            "dcdagger_vertical_test_written": True,
            "z_observable_map_written": True,
            "verticality_claimed": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3631_0",
            "target_doc": "3632-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md",
            "target_script": "scripts/Y5_R2FR_3632_Omega_owner_constraint_generator_or_DqJZ_bound_pack.py",
            "objective": "attempt to construct or source the same-parent Omega/theta/P/J/q owner needed to solve Omega_flat(e_X)=DCdagger and verify Dq[e_X]=0; if not, package Dq leak and J_Z rows into executable coefficient inputs",
            "success_gate": "parent Omega, q, P, J, and boundary charge are signed from one action and produce a proper vertical e_X, or every failed piece is converted into source-ready Dq/J_Z coefficient rows",
            "reason": "3631 makes the test exact; the remaining fork is owner construction versus coefficient pack.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_rows(t: str) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": t,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_object": "vertical_generator_Z_map",
            "canonical_status": "DCDAGGER_VERTICAL_TEST_AND_Z_MAP_WRITTEN_UNSIGNED",
            "usable_result": "candidate generator e_X must satisfy Omega_flat(e_X)=DCdagger[X], Dq[e_X]=0, and proper/zero boundary charge; local observables require R_local=MZ+N Dq_leak+B_boundary",
            "hard_block": "same-parent Omega/q/P/J/boundary owner and full-rank Z-to-R0-R11 observable map",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def md(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(rows: list[dict[str, object]], cols: list[str]) -> str:
    out = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(col, "")) for col in cols) + " |")
    return "\n".join(out)


def write_doc(src: list[dict[str, object]], vgt: list[dict[str, object]], dvg: list[dict[str, object]], zom: list[dict[str, object]], leaks: list[dict[str, object]], decisions: list[dict[str, object]], status: list[dict[str, object]], nxt: list[dict[str, object]]) -> None:
    text = "\n\n".join(
        [
            "# 3631 Y5 R2FR vertical generator Z map or J_Z coefficient runner",
            f"**Status:** {status[0]['summary']}",
            "**Claim ceiling:** no verticality, quotient descent, `J_Z=0`, local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, or EM-source claim is allowed from 3631.",
            "## Core result",
            (
                "3631 turns the old `DCdagger` clue into a hard test:\n\n"
                "```text\n"
                "Omega_flat(e_X)_A = DCdagger_A[X]\n"
                "Dq[e_X] = 0\n"
                "Q_boundary[e_X] = 0 / exact / proper\n"
                "```\n\n"
                "If those three lines are parent-owned, `e_X` is a genuine vertical generator. Separately, the physical residual map must be:\n\n"
                "```text\n"
                "R_local^i = M^i_A Z^A + N^i_a Dq_leak^a + B^i_boundary + O(Z^2)\n"
                "```\n\n"
                "So `Z=0` only helps local GR if `M` covers the actual observable rows or the uncovered rows are independently zero/bounded."
            ),
            "## Source register",
            table(src, ["source_id", "path", "exists", "needle_found", "role"]),
            "## Vertical generator test",
            table(vgt, ["test_id", "statement", "formula", "pass_condition", "current_status"]),
            "## DCdagger to vertical generator",
            table(dvg, ["map_id", "statement", "formula", "meaning", "current_status"]),
            "## Z observable map",
            table(zom, ["map_id", "observable", "map_formula", "condition_for_use", "rank_gate", "current_status"]),
            "## Dq leak and J_Z coefficient rows",
            table(leaks, ["row_id", "type", "quantity", "formula_or_template", "affected_channel", "minimum_inputs", "score_status"]),
            "## Decisions",
            table(decisions, ["decision_id", "decision", "status", "next_action"]),
            "## Next target",
            table(nxt, ["target_doc", "target_script", "objective", "success_gate"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def validate(all_paths: dict[str, Path], src: list[dict[str, object]]) -> list[dict[str, object]]:
    t = utc_now()
    rows: list[dict[str, object]] = []

    def add(vid: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": t,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": vid,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3631_0_sources_exist", all(row["exists"] for row in src), "all sources exist")
    add("VAL3631_1_needles_found", all(row["needle_found"] for row in src), "all source anchors found")
    pre = {name: path for name, path in all_paths.items() if name != "validation"}
    add("VAL3631_2_outputs_exist", all(path.exists() for path in pre.values()) and DOC.exists(), "all pre-validation outputs written")
    details: list[str] = []
    parse_ok = True
    for name, path in pre.items():
        try:
            count = len(read_csv(path))
            details.append(f"{name}:{count}")
            parse_ok = parse_ok and count > 0
        except Exception as exc:
            details.append(f"{name}:ERR:{exc}")
            parse_ok = False
    add("VAL3631_3_csv_parse", parse_ok, "; ".join(details))

    vgt = read_csv(all_paths["vertical_generator_test"])
    dvg = read_csv(all_paths["dcdagger_generator_map"])
    zom = read_csv(all_paths["z_observable_map"])
    leaks = read_csv(all_paths["leak_coefficients"])
    decisions = read_csv(all_paths["decision_gates"])
    status = read_csv(all_paths["status"])
    nxt = read_csv(all_paths["next_target"])

    add("VAL3631_4_Dq_test_written", any("Dq[" in row["formula"] for row in vgt), "Dq verticality tests written")
    add("VAL3631_5_DCd_Omega_equation_written", any("Omega_flat" in row["formula"] and "DCdagger" in row["formula"] for row in dvg), "DCdagger/Omega generator equation written")
    add("VAL3631_6_Z_observable_rank_gate_written", any("R_local" in row["map_formula"] and "FULL_RANK" in row["rank_gate"] for row in zom), "Z-to-observable full-rank gate written")
    add("VAL3631_7_leak_rows_carried", len(leaks) >= 16 and any(row["type"] == "Dq_leak" for row in leaks) and any(row["type"] == "J_Z_coefficient" for row in leaks), "Dq leak and J_Z coefficient rows carried forward")
    add("VAL3631_8_no_vertical_claim", all(row["valid_for_claim"].lower() == "false" for row in vgt + dvg + zom + leaks), "all map/test rows remain nonclaim")
    add("VAL3631_9_status_decision_nonclaim", all(row["valid_for_claim"].lower() == "false" for row in status + decisions + nxt), "status, decision, and next rows remain nonclaim")
    formalization_leak = list(FORMALIZATION.rglob("*3631*")) if FORMALIZATION.exists() else []
    add("VAL3631_10_no_formalization_leak", not formalization_leak, "no 3631 files in formalization-workbench")
    add("VAL3631_11_next_target_written", bool(nxt) and "3632" in nxt[0]["target_doc"], "3632 Omega owner target written")
    add("VAL3631_12_canonical_status_written", all_paths["canonical_status"].exists() and "DCDAGGER_VERTICAL_TEST" in all_paths["canonical_status"].read_text(encoding="utf-8", errors="replace"), "canonical vertical-generator/Z-map status written")
    return rows


def main() -> None:
    t = utc_now()
    all_paths = paths()
    src = source_rows(t)
    vgt = vertical_generator_rows(t)
    dvg = dcdagger_rows(t)
    zom = z_observable_rows(t)
    leaks = leak_rows(t)
    decisions = decision_rows(t)
    status = status_rows(t)
    nxt = next_rows(t)
    canonical = canonical_rows(t)

    write_csv(all_paths["source_register"], src)
    write_csv(all_paths["vertical_generator_test"], vgt)
    write_csv(all_paths["dcdagger_generator_map"], dvg)
    write_csv(all_paths["z_observable_map"], zom)
    write_csv(all_paths["leak_coefficients"], leaks)
    write_csv(all_paths["decision_gates"], decisions)
    write_csv(all_paths["status"], status)
    write_csv(all_paths["next_target"], nxt)
    write_csv(all_paths["canonical_status"], canonical)
    write_doc(src, vgt, dvg, zom, leaks, decisions, status, nxt)

    validation = validate(all_paths, src)
    write_csv(all_paths["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3631 validation failed: {failures}")
    print(f"wrote 3631 checkpoint with {len(validation)} validation checks")


if __name__ == "__main__":
    main()
