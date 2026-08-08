import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3783"
BRANCH = "MTS_R2FR_Y5_PARENT_U1_BUNDLE_UPGRADE_OR_PIQ_FINITE_BOUND_RUNNER_3783"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3783_SOURCE_REGISTER.csv",
    "u1_theorem": RESIDUALS / "P8_Y5_R2FR_3783_PARENT_U1_BUNDLE_UPGRADE_THEOREM.csv",
    "piq_attempt": RESIDUALS / "P8_Y5_R2FR_3783_PIQ_FLOW_CONSTRUCTION_ATTEMPT.csv",
    "node_wilson": RESIDUALS / "P8_Y5_R2FR_3783_NODE_WILSON_DEFECT_AUDIT.csv",
    "descent_tests": RESIDUALS / "P8_Y5_R2FR_3783_QOBS_DESCENT_TESTS.csv",
    "finite_inputs": RESIDUALS / "P8_Y5_R2FR_3783_FINITE_BOUND_RUNNER_INPUTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3783_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3783_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3783_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3783_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3783_VALIDATION.csv",
}

SOURCE_PATHS = {
    "spine_after_3782": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
    "doc_3782": PCW / "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md",
    "psi_audit_3782": RESIDUALS / "P8_Y5_R2FR_3782_PSI_PHASE_SOURCE_AUDIT.csv",
    "candidate_tests_3782": RESIDUALS / "P8_Y5_R2FR_3782_PIQ_CANDIDATE_TESTS.csv",
    "noncircularity_3782": RESIDUALS / "P8_Y5_R2FR_3782_NONCIRCULARITY_CONTRACT.csv",
    "finite_vector_3782": RESIDUALS / "P8_Y5_R2FR_3782_FINITE_EM_VECTOR_UPDATE.csv",
    "doc_3781": PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    "theorem_3781": RESIDUALS / "P8_Y5_R2FR_3781_PHASE_FLOW_CONNECTION_THEOREM.csv",
    "doc_3780": PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    "eft_psi": ROOT / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md",
    "mts_research": ROOT / "core-mts-framework" / "field-theory" / "motion-timespace-research.md",
    "alpha_drift": ROOT / "archive" / "uncategorised" / "the-fine-structure-constant.md",
    "doc_1398": PCW / "1398-Y5-R10-RAB-no-observed-counterterm-action-principle-or-lambdaA-prior-bound.md",
    "doc_1400": PCW / "1400-Y5-R10-RAB-joined-EM-coupling-owner-contract-or-finite-local-residual-vector.md",
}

BOUNDS = {
    "wep": "2.8e-15",
    "gamma": "2.3e-05",
    "beta": "7.8e-05",
    "gdot": "9.6e-15",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_PATHS.items():
        row = base(timestamp)
        row.update(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "role": "input for the 3783 parent U(1) bundle upgrade or finite-bound fork",
            }
        )
        rows.append(row)
    return rows


def u1_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "U1T3783_0_no_notational_promotion",
            "A real scalar psi cannot be promoted to psi=rho exp(i theta_Q) by notation alone.",
            "requires either an existing hidden S^1 redundancy in the parent action or a new charged phase sector Psi_Q",
            "blocks fake derivation from the current real-scalar EFT branch",
            "EXACT_GUARD",
            True,
        ),
        (
            "U1T3783_1_minimal_extension_fields",
            "Minimal parent extension is Phi_U1=(Phi_MTS, P_Q -> M, theta_Q, Pi_Q, q_*, N_Q, defect data D_Q).",
            "P_Q is a principal U(1) bundle; theta_Q is local fibre coordinate; Pi_Q is a primitive gauge-invariant phase-flow one-form",
            "names the exact extra objects needed instead of hiding them inside coupling language",
            "EXACT_EXTENSION_CONTRACT",
            True,
        ),
        (
            "U1T3783_2_connection_reconstruction",
            "A_obs=q_*^{-1}(d theta_Q-Pi_Q), F_obs=-q_*^{-1}dPi_Q plus q_*/defect terms.",
            "q_* fixed/superselected and local patch away from nodes",
            "reuses 3781 and makes the EM readout a connection theorem if Pi_Q is parent-owned",
            "EXACT_CONDITIONAL_THEOREM",
            True,
        ),
        (
            "U1T3783_3_qobs_descent_zero",
            "If Lie_EA Pi_Q=0, Lie_EA q_*=0, and Wilson/defect data are q_obs-owned, then R_A=0 and Lie_EA F_obs=0.",
            "E_A in ker(Dq_obs)",
            "this is the precise local-GR A/F closure route",
            "EXACT_ZERO_CONDITION",
            True,
        ),
        (
            "U1T3783_4_piq_not_arbitrary",
            "An arbitrary one-form Pi_Q is just a renamed EM potential unless the parent action builds it from MTS flow primitives without A_obs or Maxwell equations.",
            "non-circularity from 3782",
            "prevents the U(1) upgrade from becoming closure by new notation",
            "NO_SMUGGLING_GUARD",
            True,
        ),
        (
            "U1T3783_5_zem_independence",
            "The U(1) bundle can close A/F readout but does not fix Z_EM, N_Q, or lambda_A.",
            "uses 1398/1400 alpha/unique-F2 guardrail",
            "EM-lock still needs a kinetic-normalization owner or finite alpha_EM bounds",
            "NO_ALPHA_OVERCLAIM",
            True,
        ),
        (
            "U1T3783_6_current_source",
            "A same-source Ward identity requires the charged phase sector and J_Q to be varied inside the same q_obs-descended total source action.",
            "source descent from 3779/3780",
            "needed before EM stress can be included in Pi_M_total rather than finite residuals",
            "CONDITIONAL_SOURCE_THEOREM",
            True,
        ),
        (
            "U1T3783_7_current_verdict",
            "The upgrade is mathematically viable but not parent-owned by the current corpus.",
            "current corpus has real psi and flow language but no signed P_Q/Pi_Q/q_*/N_Q action clause",
            "3783 therefore keeps finite-bound mode active and sends the next step to an explicit parent U(1) action clause or demotion",
            "VIABLE_EXTENSION_NOT_DERIVED",
            False,
        ),
    ]
    rows = []
    for theorem_id, statement, assumptions, meaning, status, useful in items:
        row = base(timestamp)
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "assumptions": assumptions,
                "meaning": meaning,
                "status": status,
                "useful": useful,
            }
        )
        rows.append(row)
    return rows


def piq_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "PCA3783_0_real_psi_upgrade",
            "identify existing real psi with rho exp(i theta_Q)",
            "fails without extra degeneracy: real psi has sign/amplitude, not compact phase orbit",
            "REJECT_AS_NOTATIONAL_SMUGGLE",
            "introduce separate Psi_Q or find hidden S^1 symmetry",
            False,
        ),
        (
            "PCA3783_1_complexify_psi",
            "replace or extend psi -> Psi_g plus Psi_Q=rho_Q exp(i theta_Q)",
            "possible parent extension, but changes field content and must preserve previous real-psi geometry",
            "POSSIBLE_NEW_PARENT_CLAUSE",
            "write explicit action split and q_obs projection before any claim",
            False,
        ),
        (
            "PCA3783_2_flow_vorticity",
            "Pi_Q = B_Q[Psi_Q, Phi_MTS] with dPi_Q as MTS phase-flow vorticity",
            "best non-circular path if B_Q is primitive and not defined from A/F",
            "BEST_UNFILLED_CONSTRUCTIVE_ROUTE",
            "next script should attempt the parent action term for B_Q",
            False,
        ),
        (
            "PCA3783_3_hodge_poynting",
            "Pi_Q from Hodge/Poynting flow",
            "promising physically, but circular unless Hodge/star and energy-flow are parent-defined before Maxwell",
            "PROMISING_BUT_REQUIRES_PARENT_HODGE_FLOW",
            "route into finite flux residual until parent-owned",
            False,
        ),
        (
            "PCA3783_4_defect_curvature",
            "nonzero F from phase defects/nodes",
            "possible only with owned node/defect current D_Q and finite energy/core rule",
            "TOPOLOGICAL_ROUTE_UNSIGNED",
            "emit node/Wilson owner clauses",
            False,
        ),
    ]
    rows = []
    for attempt_id, route, result, status, next_action, closes in items:
        row = base(timestamp)
        row.update(
            {
                "attempt_id": attempt_id,
                "route": route,
                "result": result,
                "status": status,
                "next_action": next_action,
                "closes_piq": closes,
            }
        )
        rows.append(row)
    return rows


def node_wilson_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "NWD3783_0_local_patch",
            "rho_Q>0 and H^1(U)=0 on local PPN/Newton patch",
            "then theta_Q is single-valued locally and Wilson residues vanish",
            "MISSING_PATCH_CERTIFICATE",
            "declare local domain or bound Wilson terms",
        ),
        (
            "NWD3783_1_node_current",
            "D_Q := (1/2pi) d d theta_Q supported on rho_Q=0 defects",
            "nonzero D_Q becomes topological EM/phase source, not gauge fluff",
            "MISSING_DEFECT_OWNER",
            "must be included in total source or finite EM vector",
        ),
        (
            "NWD3783_2_wilson_cycle",
            "W_Q(C)=int_C R_A or int_C Pi_Q",
            "flat but non-exact residues can affect charged phases",
            "MISSING_WILSON_OWNER",
            "q_obs-own, boundary-fix, or bound",
        ),
        (
            "NWD3783_3_flux_quantization",
            "int_S dPi_Q or int_C Pi_Q quantized by parent U(1) lattice",
            "could help charge labels but still does not fix N_Q/Z_EM",
            "SUPPORT_ONLY_UNSIGNED",
            "keep separate from alpha_EM normalization",
        ),
    ]
    rows = []
    for audit_id, object_or_condition, implication, status, next_action in items:
        row = base(timestamp)
        row.update(
            {
                "audit_id": audit_id,
                "object_or_condition": object_or_condition,
                "implication": implication,
                "status": status,
                "next_action": next_action,
                "parent_signed": False,
            }
        )
        rows.append(row)
    return rows


def descent_test_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "QDT3783_0_bundle_exists",
            "principal U(1) bundle P_Q is part of parent field space",
            "MISSING_PARENT_U1_BUNDLE",
            "BLOCKS_PIQ_DERIVATION",
        ),
        (
            "QDT3783_1_piq_primitive",
            "Pi_Q is a primitive MTS flow one-form, not A_obs, F_obs, or Maxwell equation in disguise",
            "MISSING_PRIMITIVE_PIQ_OPERATOR",
            "BLOCKS_NONCIRCULARITY",
        ),
        (
            "QDT3783_2_piq_vertical_silent",
            "Lie_EA Pi_Q=0",
            "MISSING_QOBS_DESCENT_PROOF",
            "BLOCKS_R_A_ZERO",
        ),
        (
            "QDT3783_3_qstar_superselected",
            "Lie_EA ln q_*=0",
            "MISSING_CHARGE_UNIT_OWNER",
            "BLOCKS_R_A_AND_ALPHA",
        ),
        (
            "QDT3783_4_zem_norm_owner",
            "Lie_EA ln Z_EM=0 through C_Q,N_Q owner",
            "MISSING_ZEM_OWNER",
            "BLOCKS_EM_LOCK",
        ),
        (
            "QDT3783_5_lambda_excluded",
            "lambda_A observed Maxwell pullback counterterm forbidden by primitive-only operator basis",
            "MISSING_NO_PULLBACK_OPERATOR_BASIS",
            "BLOCKS_UNIQUE_F2",
        ),
        (
            "QDT3783_6_same_source",
            "J_Q and EM stress descend from same total source action",
            "MISSING_SAME_SOURCE_WARD_OWNER",
            "BLOCKS_PI_M_TOTAL_EM_PROMOTION",
        ),
    ]
    rows = []
    for test_id, requirement, status, consequence in items:
        row = base(timestamp)
        row.update(
            {
                "test_id": test_id,
                "requirement": requirement,
                "status": status,
                "consequence": consequence,
                "passed": False,
            }
        )
        rows.append(row)
    return rows


def finite_input_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        ("FBI3783_0_epsilon_Pi", "epsilon_Pi_vertical", "||Lie_EA Pi_Q||/||Pi_Q||", "MISSING_PRIMITIVE_PIQ_OR_BOUND", "dimensionless", "A/F readout"),
        ("FBI3783_1_epsilon_dPi", "epsilon_dPi_vertical", "||d(Lie_EA Pi_Q)||/||dPi_Q||", "MISSING_DPIQ_BOUND", "dimensionless", "EM stress/PPN"),
        ("FBI3783_2_beta_q", "beta_q,A", "Lie_EA ln q_*", "MISSING_QSTAR_BOUND", "dimensionless", "charge unit"),
        ("FBI3783_3_epsilon_node", "epsilon_node", "defect/node/Wilson contribution", "MISSING_DEFECT_WILSON_BOUND", "dimensionless_or_flux", "phase/topology"),
        ("FBI3783_4_beta_Z", "beta_Z,A", "Lie_EA ln Z_EM", "MISSING_ZEM_BOUND", "dimensionless", "WEP/clock/Gdot/PPN"),
        ("FBI3783_5_lambda_A", "lambda_A", "observed Maxwell pullback coefficient", "MISSING_LAMBDA_A_PRIOR", "action_coefficient", "unique F2/alpha"),
        ("FBI3783_6_epsilon_J", "epsilon_J_Q", "||nabla J_Q||+||J_Q-J_qobs||", "MISSING_CURRENT_OWNER_BOUND", "current_norm", "same-source Hilbert stress"),
        ("FBI3783_7_WEP", "eta_EM_AB", "C_Pi eps_Pi+C_Z eps_Z+C_J eps_J+C_node eps_node", BOUNDS["wep"], "dimensionless", "WEP envelope"),
        ("FBI3783_8_gamma", "delta_gamma_EM", "C_dPi eps_dPi+C_g eps_shadow+C_q Delta_q_EM", BOUNDS["gamma"], "dimensionless", "PPN gamma envelope"),
        ("FBI3783_9_Gdot", "dln_Geff_dt_EM", "|dt beta_Z|+|dt beta_q|+|dt eps_dPi|+source exchange", BOUNDS["gdot"], "yr^-1", "Gdot envelope"),
    ]
    rows = []
    for input_id, symbol, expression, required_bound, units, arena in items:
        row = base(timestamp)
        row.update(
            {
                "input_id": input_id,
                "symbol": symbol,
                "expression": expression,
                "required_bound_or_status": required_bound,
                "units": units,
                "observable_arena": arena,
                "claim_ready": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(row["exists"] for row in grouped["sources"])
    theorem = any(row["theorem_id"] == "U1T3783_2_connection_reconstruction" for row in grouped["u1_theorem"])
    no_smuggle = any(row["theorem_id"] == "U1T3783_4_piq_not_arbitrary" for row in grouped["u1_theorem"])
    piq_closed = any(row["closes_piq"] for row in grouped["piq_attempt"])
    tests_pass = all(row["passed"] for row in grouped["descent_tests"])
    finite_nonclaim = all(not row["claim_ready"] for row in grouped["finite_inputs"])
    gates = [
        ("CG3783_0_sources", "all source paths exist", all_sources, "source register resolves", False),
        ("CG3783_1_theorem", "parent U(1) upgrade theorem emitted", theorem, "connection reconstruction available", False),
        ("CG3783_2_no_smuggling", "Pi_Q not-arbitrary guard emitted", no_smuggle, "arbitrary Pi_Q is rejected as renamed EM", False),
        ("CG3783_3_PiQ_closed", "Pi_Q derived from parent flow", piq_closed, "no route currently closes", False),
        ("CG3783_4_descent_tests", "all q_obs/U1/source descent tests pass", tests_pass, "all remain missing parent clauses", False),
        ("CG3783_5_finite_inputs", "finite-bound inputs retained nonclaim", finite_nonclaim, "finite runner rows emitted", False),
        ("CG3783_6_local_GR_EM_claim", "EM/local-GR promotion claim allowed", False, "blocked until U1 bundle, Pi_Q, q*, Z_EM, lambda_A, defects, and current close", False),
    ]
    rows = []
    for gate_id, gate, passed, details, claim_allowed in gates:
        row = base(timestamp)
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "passed": passed,
                "details": details,
                "claim_allowed": claim_allowed,
            }
        )
        rows.append(row)
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "DEC3783_0_best_news",
            "The U(1) route is mathematically clean.",
            "A parent U(1) bundle with primitive Pi_Q would close A/F basicness exactly.",
        ),
        (
            "DEC3783_1_hard_truth",
            "The current corpus does not own that bundle yet.",
            "Treat the U(1) structure as a candidate parent extension, not a derived result.",
        ),
        (
            "DEC3783_2_non_smuggling",
            "Do not define Pi_Q as an arbitrary one-form.",
            "Either build it from MTS flow primitives in the parent action or use the finite EM vector.",
        ),
        (
            "DEC3783_3_next",
            "The next leap is a parent U(1) action clause.",
            "Write the minimal action/grammar that either makes P_Q/Pi_Q primitive and q_obs-silent or formally demotes EM readout to finite-bound mode.",
        ),
    ]
    rows = []
    for decision_id, finding, action in items:
        row = base(timestamp)
        row.update({"decision_id": decision_id, "finding": finding, "action": action})
        rows.append(row)
    return rows


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    row = base(timestamp)
    row.update(
        {
            "next_doc": "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
            "next_script": "scripts/Y5_R2FR_3784_parent_U1_action_clause_or_EM_finite_bound_mode.py",
            "objective": "Write the minimal parent U(1) action/grammar clause that would make P_Q, Pi_Q, q_*, N_Q, defect data, and current descent parent-owned; if it cannot be made non-circular, switch the EM route to finite-bound mode explicitly.",
            "why_next": "3783 proves the extension route is viable but not owned by the current corpus; 3784 must either write the parent action clause or stop treating U(1) as derivable.",
        }
    )
    return [row]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    row = base(timestamp)
    row.update(
        {
            "status": "PARENT_U1_EXTENSION_VIABLE_NOT_DERIVED_PIQ_FINITE_BOUND_MODE_RETAINED",
            "claim": "No Pi_Q derivation, EM-lock, alpha_EM, local-GR, WEP, PPN, or Newton pass is claimed.",
            "summary": "A minimal U(1) parent bundle would close A/F if Pi_Q is primitive and q_obs-silent, but current sources do not own P_Q/Pi_Q/q*/N_Q. Finite EM bound mode remains active.",
        }
    )
    return [row]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization = ROOT / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*3783*")) if formalization.exists() else []
    checks = [
        ("sources_exist", "every cited source path exists", all(row["exists"] for row in grouped["sources"])),
        ("csv_outputs_parse", "all generated CSV outputs exist and parse", all(path.exists() and list(csv.DictReader(path.open(encoding="utf-8"))) for path in generated)),
        ("doc_written", "3783 markdown document written", DOC_PATH.exists()),
        ("u1_theorem", "parent U1 theorem emitted", any(row["theorem_id"] == "U1T3783_1_minimal_extension_fields" for row in grouped["u1_theorem"])),
        ("no_smuggle_guard", "arbitrary Pi_Q guard emitted", any(row["theorem_id"] == "U1T3783_4_piq_not_arbitrary" for row in grouped["u1_theorem"])),
        ("node_wilson", "node/Wilson audit emitted", len(grouped["node_wilson"]) >= 4),
        ("descent_tests", "q_obs descent tests emitted", len(grouped["descent_tests"]) >= 7),
        ("finite_inputs", "finite-bound inputs emitted", all(not row["claim_ready"] for row in grouped["finite_inputs"])),
        ("claim_gate_closed", "EM/local-GR claim gate remains closed", any(row["gate_id"] == "CG3783_6_local_GR_EM_claim" and not row["claim_allowed"] for row in grouped["claim_gates"])),
        ("next_target", "3784 parent action target emitted", grouped["next_target"][0]["next_doc"].startswith("3784-")),
        ("formalization_clean", "no 3783 files written under formalization-workbench", len(formalization_hits) == 0),
    ]
    rows = []
    for validation_id, description, result in checks:
        row = base(timestamp)
        row.update(
            {
                "validation_id": validation_id,
                "description": description,
                "result": "PASS" if result else "FAIL",
                "details": "",
            }
        )
        rows.append(row)
    return rows


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3783 - Parent U(1) Bundle Upgrade or Pi_Q Finite-Bound Runner",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        str(grouped["status"][0]["summary"]),
        "",
        "## Result In Plain Terms",
        "",
        "3783 finds the clean fork. A parent U(1) bundle with fields `(theta_Q, Pi_Q, q_*, N_Q)` would make the EM readout route mathematically clean: `A_obs=q_*^{-1}(dtheta_Q-Pi_Q)`, and if `Pi_Q` plus `q_*` descend through `q_obs`, then `R_A=0` and `F` is vertical-silent. But the current corpus does not own that bundle or primitive `Pi_Q`; adding an arbitrary one-form would just rename EM. So the U(1) route is viable as a parent extension, not yet derived. Finite-bound mode remains active.",
        "",
        "## Parent U(1) Bundle Upgrade Theorem",
    ]
    for row in grouped["u1_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Meaning: {row['meaning']}")

    lines.extend(["", "## Pi_Q Flow Construction Attempt"])
    for row in grouped["piq_attempt"]:
        lines.append(f"- `{row['attempt_id']}` `{row['status']}`: {row['route']}. Result: {row['result']}. Next: {row['next_action']}")

    lines.extend(["", "## Node / Wilson Defect Audit"])
    for row in grouped["node_wilson"]:
        lines.append(f"- `{row['audit_id']}` `{row['status']}`: {row['object_or_condition']}. Implication: {row['implication']}. Next: {row['next_action']}")

    lines.extend(["", "## q_obs Descent Tests"])
    for row in grouped["descent_tests"]:
        lines.append(f"- `{row['test_id']}` pass=`{row['passed']}`: {row['requirement']}. Status: `{row['status']}`. Consequence: {row['consequence']}")

    lines.extend(["", "## Finite-Bound Runner Inputs"])
    for row in grouped["finite_inputs"]:
        lines.append(f"- `{row['input_id']}` `{row['symbol']}`: {row['expression']} <= `{row['required_bound_or_status']}` `{row['units']}`. Arena: {row['observable_arena']}")

    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}` claim_allowed=`{row['claim_allowed']}`: {row['gate']}. Details: {row['details']}")

    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}`: {row['finding']} Action: {row['action']}")

    lines.extend(["", "## Next Target"])
    target = grouped["next_target"][0]
    lines.append(f"- `{target['next_doc']}`: {target['objective']}")

    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")

    return "\n".join(lines) + "\n"


def main() -> None:
    timestamp = now()
    grouped = {
        "sources": source_rows(timestamp),
        "u1_theorem": u1_theorem_rows(timestamp),
        "piq_attempt": piq_attempt_rows(timestamp),
        "node_wilson": node_wilson_rows(timestamp),
        "descent_tests": descent_test_rows(timestamp),
        "finite_inputs": finite_input_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["u1_theorem"], grouped["u1_theorem"])
    write_csv(OUTPUTS["piq_attempt"], grouped["piq_attempt"])
    write_csv(OUTPUTS["node_wilson"], grouped["node_wilson"])
    write_csv(OUTPUTS["descent_tests"], grouped["descent_tests"])
    write_csv(OUTPUTS["finite_inputs"], grouped["finite_inputs"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = []
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3783 validation failed: {failures}")
    print("wrote 3783 checkpoint: parent U1 bundle fork emitted")


if __name__ == "__main__":
    main()
