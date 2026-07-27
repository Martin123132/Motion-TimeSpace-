import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3782"
BRANCH = "MTS_R2FR_Y5_INSTANTIATE_PIQ_FROM_PSI_PHASE_CURRENT_OR_FINITE_EM_VECTOR_3782"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3782_SOURCE_REGISTER.csv",
    "psi_audit": RESIDUALS / "P8_Y5_R2FR_3782_PSI_PHASE_SOURCE_AUDIT.csv",
    "candidate_tests": RESIDUALS / "P8_Y5_R2FR_3782_PIQ_CANDIDATE_TESTS.csv",
    "noncircularity": RESIDUALS / "P8_Y5_R2FR_3782_NONCIRCULARITY_CONTRACT.csv",
    "finite_vector": RESIDUALS / "P8_Y5_R2FR_3782_FINITE_EM_VECTOR_UPDATE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3782_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3782_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3782_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3782_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3782_VALIDATION.csv",
}

SOURCE_PATHS = {
    "spine_after_3781": PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
    "doc_3781": PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    "theorem_3781": RESIDUALS / "P8_Y5_R2FR_3781_PHASE_FLOW_CONNECTION_THEOREM.csv",
    "input_audit_3781": RESIDUALS / "P8_Y5_R2FR_3781_PHASE_FLOW_INPUT_AUDIT.csv",
    "local_vector_3781": RESIDUALS / "P8_Y5_R2FR_3781_EM_LOCAL_RESIDUAL_VECTOR.csv",
    "doc_3780": PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    "eft_psi": ROOT / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md",
    "mts_research": ROOT / "core-mts-framework" / "field-theory" / "motion-timespace-research.md",
    "alpha_drift": ROOT / "archive" / "uncategorised" / "the-fine-structure-constant.md",
    "alpha_angular": ROOT / "archive" / "uncategorised" / "the-fine-structure-constant-from-angular-bandwidth-in-motion-timespace-theory.md",
    "yang_mills": ROOT / "quantum-particle-field" / "yang-mills" / "yang-mills-mass-gap-via-the-motion-theory.md",
    "mbt_sr": ROOT / "core-mts-framework" / "relativity" / "mbt-special-relativity-a-respectful-extension-of-einstein.md",
    "doc_1398": PCW / "1398-Y5-R10-RAB-no-observed-counterterm-action-principle-or-lambdaA-prior-bound.md",
    "doc_1399": PCW / "1399-Y5-R10-RAB-gauge-level-index-owner-for-lambdaA-or-finite-alphaEM-prior-vector.md",
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
                "role": "source used to test whether Pi_Q is actually supplied by MTS psi/phase/current/flow material",
            }
        )
        rows.append(row)
    return rows


def psi_audit_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "PSA3782_0_eft_real_psi",
            "core EFT psi field",
            "the effective-field document defines the microscopic motion field as psi: R^4 -> R and builds geometry from <partial_mu psi partial_nu psi>",
            "REAL_SCALAR_NO_U1_PHASE",
            "cannot directly supply theta_Q or compact U(1) phase without extra structure",
            False,
        ),
        (
            "PSA3782_1_pgf_flow_psi",
            "PGF / contradiction-flow Psi",
            "motion-timespace-research treats Psi as scalar local tension/divergence of flow with damping/inertial PGF terms",
            "FLOW_SCALAR_NOT_U1_CONNECTION",
            "useful motivation for Pi_Q, but no one-form transformation law is present",
            False,
        ),
        (
            "PSA3782_2_alpha_phase_language",
            "fine-structure alpha / EM phase sampling",
            "alpha notes describe EM phase/coupling as curvature-memory bandwidth or resolution effect",
            "NORMALIZATION_ROUTE_NOT_CONNECTION",
            "feeds Z_EM/alpha, not A/F q_obs basicness",
            False,
        ),
        (
            "PSA3782_3_yang_mills_A",
            "Yang-Mills gauge potential A_mu",
            "Yang-Mills file imports a gauge potential and field strength for a gauge theory analogy",
            "GAUGE_FIELD_PRESENT_BUT_NOT_DERIVED_FROM_PSI",
            "cannot instantiate Pi_Q unless a parent map from psi/flow to A or Pi_Q is supplied",
            False,
        ),
        (
            "PSA3782_4_motion_flow",
            "momentum as motion-field flow",
            "relativity notes identify momentum as motion-field flow with resistance",
            "MOTIVATING_FLOW_LANGUAGE",
            "candidate source for Pi_Q, but lacks charge unit, U(1) fibre, and current owner",
            False,
        ),
    ]
    rows = []
    for audit_id, object_name, evidence, status, consequence, parent_signed in items:
        row = base(timestamp)
        row.update(
            {
                "audit_id": audit_id,
                "object_name": object_name,
                "evidence_summary": evidence,
                "status": status,
                "consequence": consequence,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def candidate_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "PQT3782_0_real_gradient",
            "Pi_Q = d f(psi)",
            "real scalar psi or scalar flow variable",
            "dPi_Q=0 away from singularities, so A=q_*^-1(dtheta_Q-df) is pure gauge or undefined",
            "FAILS_NONTRIVIAL_MAXWELL_CURVATURE",
            "could be a gauge/clock scalar, not ordinary EM",
            False,
        ),
        (
            "PQT3782_1_complex_phase_promote",
            "psi = rho exp(i theta_Q), Pi_Q^0=dtheta_Q",
            "requires adding complex U(1) phase not signed by the main EFT real-psi file",
            "A_obs=0 and F_obs=0 if Pi_Q=dtheta_Q",
            "SUPPORTS_PHASE_LABEL_ONLY",
            "needs independent Pi_Q flow one-form, not just phase gradient",
            False,
        ),
        (
            "PQT3782_2_noether_current_free",
            "J_phase = Im(psi^* dpsi)=rho^2 dtheta_Q; Pi_Q=J_phase/rho^2",
            "complex psi, no gauge field",
            "Pi_Q=dtheta_Q, so it still gives zero connection curvature",
            "FAILS_NONZERO_EM",
            "not enough for Maxwell unless defects/topology are separately owned",
            False,
        ),
        (
            "PQT3782_3_covariant_current",
            "J_Q = rho^2(dtheta_Q-q_* A_obs)",
            "standard charged current",
            "using this to define Pi_Q already assumes A_obs, so it is circular as an EM derivation",
            "CIRCULAR_IF_USED_TO_DERIVE_A",
            "allowed only after A_obs is independently derived",
            False,
        ),
        (
            "PQT3782_4_mts_flow_oneform",
            "Pi_Q = F_flow[psi,g_eff,tau_obs]",
            "hypothetical non-circular MTS flow-current one-form",
            "this would work if F_flow has U(1) transformation law, q_obs descent, fixed q_*, source current, and regularity",
            "BEST_ROUTE_NOT_FILLED",
            "next target should try to construct this exact F_flow",
            False,
        ),
        (
            "PQT3782_5_poynting_hodge",
            "Pi_Q from Hodge/Poynting/background energy-flow",
            "motivated by EM wave/Poynting heuristics",
            "requires already-descended Maxwell/Hodge structure; otherwise it imports EM to derive EM",
            "PROMISING_BUT_CIRCULAR_UNLESS_PARENT_HODGE_FLOW_EXISTS",
            "can become finite flux/source residual if not parent-owned",
            False,
        ),
        (
            "PQT3782_6_alpha_bandwidth",
            "Pi_Q from curvature-memory bandwidth l_max/Gamma_G",
            "fine-structure alpha route",
            "affects coupling normalization Z_EM/alpha, not the EM connection one-form",
            "ZEM_ONLY_NOT_PIQ",
            "keep under beta_Z,A/lambda_A not A/F basicness",
            False,
        ),
    ]
    rows = []
    for candidate_id, candidate, source, test, verdict, next_action, success in items:
        row = base(timestamp)
        row.update(
            {
                "candidate_id": candidate_id,
                "candidate": candidate,
                "source": source,
                "test": test,
                "verdict": verdict,
                "next_action": next_action,
                "success": success,
            }
        )
        rows.append(row)
    return rows


def noncircularity_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "NCC3782_0_parent_U1",
            "theta_Q is a parent S^1 fibre coordinate, not a post-readout label",
            "MISSING_PARENT_U1_BUNDLE",
            "without this, phase is a scalar convention rather than gauge structure",
        ),
        (
            "NCC3782_1_non_circular_PiQ",
            "Pi_Q[psi] is constructed without A_obs and without Maxwell equations",
            "MISSING_NONCIRCULAR_FLOW_ONEFORM",
            "otherwise the route defines A using A",
        ),
        (
            "NCC3782_2_qobs_descent",
            "Lie_EA Pi_Q=0 for every E_A in ker(Dq_obs)",
            "MISSING_PIQ_VERTICAL_SILENCE",
            "this is the direct R_A=0 input from 3781",
        ),
        (
            "NCC3782_3_fixed_qstar",
            "beta_q,A=Lie_EA ln q_*=0",
            "MISSING_CHARGE_UNIT_SUPERSELECTION",
            "otherwise charge-unit drift reopens R_A and dR_A",
        ),
        (
            "NCC3782_4_current_owner",
            "same source action owns J_Q and gives a Ward identity",
            "MISSING_SAME_SOURCE_WARD_OWNER",
            "needed to put EM stress into the total Hilbert source",
        ),
        (
            "NCC3782_5_node_regularization",
            "rho=|psi| is nonzero or defects/nodes have a declared source/topological owner",
            "MISSING_PSI_NODE_DEFECT_RULE",
            "phase current J/rho^2 is singular at nodes",
        ),
        (
            "NCC3782_6_ZEM_owner",
            "Z_EM/N_Q/lambda_A are fixed or bounded independently of A/F readout",
            "MISSING_ZEM_ALPHA_OWNER",
            "prevents a gauge-readout success from overclaiming alpha_EM",
        ),
    ]
    rows = []
    for clause_id, requirement, status, why in items:
        row = base(timestamp)
        row.update(
            {
                "clause_id": clause_id,
                "requirement": requirement,
                "status": status,
                "why_required": why,
                "parent_signed": False,
            }
        )
        rows.append(row)
    return rows


def finite_vector_rows(timestamp: str) -> list[dict[str, object]]:
    items = [
        (
            "FEV3782_0_Pi_vertical",
            "epsilon_Pi_vertical",
            "||Lie_EA Pi_Q||/||Pi_Q||",
            "MISSING_NONCIRCULAR_PIQ_MAP",
            "dimensionless",
            "A/F q_obs basicness",
        ),
        (
            "FEV3782_1_dPi_vertical",
            "epsilon_dPi_vertical",
            "||d(Lie_EA Pi_Q)||/||dPi_Q||",
            "MISSING_DPIQ_VERTICAL_SILENCE",
            "dimensionless",
            "F_obs leakage; EM stress",
        ),
        (
            "FEV3782_2_beta_q",
            "beta_q,A",
            "Lie_EA ln q_*",
            "MISSING_QSTAR_OWNER",
            "dimensionless",
            "charge-unit drift",
        ),
        (
            "FEV3782_3_node_defect",
            "epsilon_node",
            "defect/node contribution to dPi_Q or Wilson phase",
            "MISSING_PSI_NODE_DEFECT_RULE",
            "dimensionless_or_flux_units",
            "topological/phase EM residue",
        ),
        (
            "FEV3782_4_beta_Z",
            "beta_Z,A",
            "Lie_EA ln Z_EM",
            "MISSING_ZEM_NORM_OWNER",
            "dimensionless",
            "WEP; clocks; PPN; Gdot",
        ),
        (
            "FEV3782_5_lambda_A",
            "lambda_A",
            "allowed observed Maxwell pullback counterterm",
            "MISSING_PRIMITIVE_ONLY_OPERATOR_BASIS",
            "action_coefficient",
            "unique F2; alpha_EM",
        ),
        (
            "FEV3782_6_current",
            "epsilon_J_Q",
            "||nabla_a J_Q^a|| + ||J_Q-J_qobs||",
            "MISSING_SAME_SOURCE_CURRENT_OWNER",
            "current_norm",
            "Hilbert stress/source coupling",
        ),
        (
            "FEV3782_7_WEP",
            "eta_EM_AB",
            "C_Pi epsilon_Pi + C_Z epsilon_ZEM + C_J epsilon_J_Q + C_node epsilon_node",
            BOUNDS["wep"],
            "dimensionless",
            "WEP",
        ),
        (
            "FEV3782_8_PPN_gamma",
            "delta_gamma_EM",
            "C_F epsilon_dPi + C_g epsilon_EM_shadow_metric + C_q Delta_q_EM",
            BOUNDS["gamma"],
            "dimensionless",
            "PPN gamma",
        ),
        (
            "FEV3782_9_Gdot",
            "dln_Geff_dt_EM",
            "|d_t beta_Z| + |d_t beta_q| + |d_t epsilon_dPi| + source exchange",
            BOUNDS["gdot"],
            "yr^-1",
            "Gdot",
        ),
    ]
    rows = []
    for vector_id, symbol, expression, status_or_bound, units, arena in items:
        row = base(timestamp)
        row.update(
            {
                "vector_id": vector_id,
                "symbol": symbol,
                "expression": expression,
                "status_or_bound": status_or_bound,
                "units": units,
                "observable_arena": arena,
                "claim_ready": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(row["exists"] for row in grouped["sources"])
    real_psi_guard = any(row["audit_id"] == "PSA3782_0_eft_real_psi" for row in grouped["psi_audit"])
    circularity_guard = any(row["candidate_id"] == "PQT3782_3_covariant_current" for row in grouped["candidate_tests"])
    contract_emitted = any(row["clause_id"] == "NCC3782_1_non_circular_PiQ" for row in grouped["noncircularity"])
    finite_vector = all(not row["claim_ready"] for row in grouped["finite_vector"])
    piq_instantiated = any(row["success"] for row in grouped["candidate_tests"])
    gates = [
        ("CG3782_0_sources", "all source paths exist", all_sources, "source register resolves", False),
        ("CG3782_1_real_psi_guard", "real-scalar psi guard emitted", real_psi_guard, "main EFT psi is not yet U(1) phase", False),
        ("CG3782_2_circularity_guard", "covariant-current circularity guard emitted", circularity_guard, "do not derive A from a current already containing A", False),
        ("CG3782_3_non_circular_contract", "Pi_Q non-circularity contract emitted", contract_emitted, "exact clauses listed", False),
        ("CG3782_4_PiQ_instantiated", "Pi_Q successfully instantiated", piq_instantiated, "no candidate currently passes all parent clauses", False),
        ("CG3782_5_finite_vector_nonclaim", "finite EM vector remains nonclaim", finite_vector, "missing Pi_Q/q*/Z/current/node inputs retained", False),
        ("CG3782_6_EM_local_GR_claim", "EM/local-GR promotion claim allowed", False, "blocked until non-circular Pi_Q, q*, Z_EM, lambda_A, current, and node clauses close", False),
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
            "DEC3782_0_main_result",
            "Pi_Q is not yet instantiated from the current corpus.",
            "The main psi field is real/scalar in the EFT source, and phase/current language is not yet a parent U(1) bundle map.",
        ),
        (
            "DEC3782_1_best_route",
            "Do not abandon the route: build the missing parent object explicitly.",
            "The least-cheaty next step is a parent U(1)-bundle upgrade or proof that an existing complex psi sector already supplies it.",
        ),
        (
            "DEC3782_2_no_circularity",
            "A covariant matter current cannot be used to derive A if it already contains A.",
            "Use it only after A/Pi_Q is independently supplied, or keep it as a finite residual.",
        ),
        (
            "DEC3782_3_alpha_guard",
            "Alpha/Z_EM remains separate from A/F readout.",
            "Even a successful Pi_Q will still need N_Q/Z_EM/lambda_A owner work before EM-lock.",
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
            "next_doc": "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md",
            "next_script": "scripts/Y5_R2FR_3783_parent_U1_bundle_upgrade_or_PiQ_finite_bound_runner.py",
            "objective": "Try the minimal parent U(1)-bundle upgrade: promote or identify psi=rho exp(i theta_Q), define a non-circular Pi_Q flow one-form, handle nodes/Wilson sectors, and test q_obs descent; if this is not parent-owned, keep the finite EM vector as the local route.",
            "why_next": "3782 shows existing sources motivate phase/flow but do not instantiate Pi_Q; the next step must either add/sign the missing U(1) parent structure or stop trying to derive EM readout from real scalar psi.",
        }
    )
    return [row]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    row = base(timestamp)
    row.update(
        {
            "status": "PIQ_NOT_INSTANTIATED_CURRENT_CORPUS_NONCIRCULARITY_CONTRACT_AND_FINITE_EM_VECTOR_EMITTED",
            "claim": "No Pi_Q, EM-lock, alpha_EM, WEP, PPN, Newton, or local-GR pass is claimed.",
            "summary": "The current corpus motivates phase/flow but does not yet supply a non-circular q_obs-owned Pi_Q. A real scalar psi gives no U(1) phase; a covariant current containing A is circular. Finite EM residual rows are retained.",
        }
    )
    return [row]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization = ROOT / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*3782*")) if formalization.exists() else []
    checks = [
        ("sources_exist", "every cited source path exists", all(row["exists"] for row in grouped["sources"])),
        ("csv_outputs_parse", "all generated CSV outputs exist and parse", all(path.exists() and list(csv.DictReader(path.open(encoding="utf-8"))) for path in generated)),
        ("doc_written", "3782 markdown document written", DOC_PATH.exists()),
        ("real_psi_guard", "real psi guard emitted", any(row["audit_id"] == "PSA3782_0_eft_real_psi" for row in grouped["psi_audit"])),
        ("candidate_tests", "Pi_Q candidate tests emitted", len(grouped["candidate_tests"]) >= 6),
        ("noncircularity_contract", "non-circularity contract emitted", any(row["clause_id"] == "NCC3782_1_non_circular_PiQ" for row in grouped["noncircularity"])),
        ("finite_vector", "finite EM vector emitted", any(row["vector_id"] == "FEV3782_0_Pi_vertical" for row in grouped["finite_vector"])),
        ("claim_gate_closed", "EM/local-GR claim gate remains closed", any(row["gate_id"] == "CG3782_6_EM_local_GR_claim" and not row["claim_allowed"] for row in grouped["claim_gates"])),
        ("next_target", "3783 parent U(1) target emitted", grouped["next_target"][0]["next_doc"].startswith("3783-")),
        ("formalization_clean", "no 3782 files written under formalization-workbench", len(formalization_hits) == 0),
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
        "# 3782 - Instantiate Pi_Q from psi Phase Current or Finite EM Vector",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        str(grouped["status"][0]["summary"]),
        "",
        "## Result In Plain Terms",
        "",
        "3782 tries to fill `Pi_Q` from the actual MTS material. The result is useful but strict: the present core EFT uses a real scalar `psi`, so it does not yet provide a compact U(1) phase. A free complex phase current gives `Pi_Q=dtheta_Q`, which makes `A` pure gauge and `F=0`. A covariant charged current gives `Pi_Q=dtheta_Q-q_*A`, but that already contains `A`, so it is circular if used to derive `A`. Therefore `Pi_Q` is not yet instantiated; the finite EM residual vector stays live.",
        "",
        "## psi / Phase Source Audit",
    ]
    for row in grouped["psi_audit"]:
        lines.append(f"- `{row['audit_id']}` `{row['status']}`: {row['object_name']}. Evidence: {row['evidence_summary']}. Consequence: {row['consequence']}")

    lines.extend(["", "## Pi_Q Candidate Tests"])
    for row in grouped["candidate_tests"]:
        lines.append(f"- `{row['candidate_id']}` `{row['verdict']}`: {row['candidate']}. Test: {row['test']}. Next: {row['next_action']}")

    lines.extend(["", "## Non-Circularity Contract"])
    for row in grouped["noncircularity"]:
        lines.append(f"- `{row['clause_id']}` `{row['status']}`: {row['requirement']}. Why: {row['why_required']}")

    lines.extend(["", "## Finite EM Vector"])
    for row in grouped["finite_vector"]:
        lines.append(f"- `{row['vector_id']}` `{row['symbol']}`: {row['expression']} <= `{row['status_or_bound']}` `{row['units']}`. Arena: {row['observable_arena']}")

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
        "psi_audit": psi_audit_rows(timestamp),
        "candidate_tests": candidate_rows(timestamp),
        "noncircularity": noncircularity_rows(timestamp),
        "finite_vector": finite_vector_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["psi_audit"], grouped["psi_audit"])
    write_csv(OUTPUTS["candidate_tests"], grouped["candidate_tests"])
    write_csv(OUTPUTS["noncircularity"], grouped["noncircularity"])
    write_csv(OUTPUTS["finite_vector"], grouped["finite_vector"])
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
        raise SystemExit(f"3782 validation failed: {failures}")
    print("wrote 3782 checkpoint: Pi_Q instantiation attempt and finite EM vector emitted")


if __name__ == "__main__":
    main()
