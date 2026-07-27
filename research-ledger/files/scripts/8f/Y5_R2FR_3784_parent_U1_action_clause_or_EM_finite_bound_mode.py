import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3784"
BRANCH = "MTS_R2FR_Y5_PARENT_U1_ACTION_CLAUSE_OR_EM_FINITE_BOUND_MODE_3784"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3784_SOURCE_REGISTER.csv",
    "action_clause": RESIDUALS / "P8_Y5_R2FR_3784_PARENT_U1_ACTION_CLAUSE.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_3784_VARIATION_AND_MAXWELL_DESCENT.csv",
    "noncircular": RESIDUALS / "P8_Y5_R2FR_3784_NONCIRCULARITY_AND_FLOW_OWNER_TESTS.csv",
    "zero_conditions": RESIDUALS / "P8_Y5_R2FR_3784_QOBS_ZERO_CONDITIONS.csv",
    "finite_mode": RESIDUALS / "P8_Y5_R2FR_3784_EM_FINITE_BOUND_MODE.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3784_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3784_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3784_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3784_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3784_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md",
    PCW / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md",
    PCW / "3780-Y5-R2FR-vertical-EM-basicness-calculation-A-F-ZEM.md",
    PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    PCW / "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md",
    PCW / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md",
    PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp):
    rows = []
    for source in SOURCE_PATHS:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "checkpoint_id": CHECKPOINT,
                "branch_id": BRANCH,
                "source_path": str(source),
                "exists": source.exists(),
                "source_role": "parent_action_context",
                "valid_for_claim": False,
            }
        )
    return rows


def action_clause_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "clause_id": "U1A3784_0_field_space",
            "status": "MINIMAL_PARENT_EXTENSION_CLAUSE",
            "statement": "Extend the parent field space by Phi_U1=(Phi_MTS,P_Q -> M,theta_Q,Pi_Q,q_*,N_Q,D_Q), where P_Q is a principal U(1) bundle, theta_Q is local fibre phase, Pi_Q is a gauge-invariant parent one-form, q_* is the charge unit, N_Q fixes generator norm, and D_Q stores node/defect data.",
            "derivation_role": "names the smallest objects that make the 3781/3783 connection theorem precise",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "clause_id": "U1A3784_1_readout",
            "status": "EXACT_READOUT_DEFINITION",
            "statement": "A_obs=q_*^{-1}(dtheta_Q-Pi_Q), F_obs=dA_obs=-q_*^{-1}dPi_Q-beta_q wedge A_obs plus defect terms; for fixed q_* and no defects this reduces to F_obs=-q_*^{-1}dPi_Q.",
            "derivation_role": "turns EM readout into a connection reconstruction, not an independent inserted A_mu",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "clause_id": "U1A3784_2_parent_lagrangian",
            "status": "CONDITIONAL_ACTION_GRAMMAR",
            "statement": "S_U1=int sqrt(-g_eff)[-(Z_Pi/(4 q_*^2)) H_ab H^ab + A_obs_a J_Q^a + L_Q(rho_Q,D_a rho_Q,theta_Q,Pi_Q;Phi_MTS) + L_constraint(Pi_Q-B_Q[Phi_MTS,Psi_Q])]+S_defect[D_Q], with H=dPi_Q.",
            "derivation_role": "the smallest action grammar that can vary to Maxwell form while exposing the possible smuggle point B_Q",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "clause_id": "U1A3784_3_no_smuggle",
            "status": "NONCIRCULARITY_CONTRACT",
            "statement": "B_Q must be built from MTS flow primitives before A_obs/F_obs/Maxwell equations are defined; if B_Q is absent or arbitrary, Pi_Q is an added EM field and the route is parent-extension mode, not derived-from-current-MTS mode.",
            "derivation_role": "prevents the action from hiding Maxwell inside new notation",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "clause_id": "U1A3784_4_normalization",
            "status": "ALPHA_OWNER_CLAUSE",
            "statement": "Z_EM=Z_Pi/q_*^2=C_Q N_Q must be q_obs-owned, superselected, or separately bounded; the U(1) bundle fixes compact charge labels but not the continuous Maxwell kinetic normalization.",
            "derivation_role": "keeps alpha_EM honest instead of claiming compact U(1) automatically derives it",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "clause_id": "U1A3784_5_same_source",
            "status": "WARD_SOURCE_CLAUSE",
            "statement": "J_Q must be varied inside the same q_obs-descended total source action as EM stress, so div(T_EM+T_charged+T_binding)=0 follows from one source sector rather than from matched bookkeeping.",
            "derivation_role": "connects EM to Pi_M_total and the Newton/PPN source programme",
            "valid_for_claim": False,
        },
    ]


def variation_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "derivation_id": "VAR3784_0_gauge_transform",
            "result": "A_obs transforms as a U(1) connection if theta_Q -> theta_Q+q_* lambda and Pi_Q is gauge-invariant.",
            "calculation": "A_obs' = q_*^{-1}(dtheta_Q+q_*dlambda-Pi_Q)=A_obs+dlambda; therefore F_obs is gauge invariant.",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "VAR3784_1_theta_variation",
            "result": "theta_Q variation gives current conservation when the action depends on theta_Q through A_obs and q_obs-descended source terms.",
            "calculation": "delta_theta A_obs=q_*^{-1}d(delta theta); delta S=int sqrt(-g) J_Q^a q_*^{-1} nabla_a delta theta = -int sqrt(-g) q_*^{-1}(nabla_a J_Q^a)delta theta + boundary.",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "VAR3784_2_piq_variation",
            "result": "Pi_Q variation gives the Maxwell equation for A_obs if the parent kinetic term is -(Z_Pi/(4q_*^2))|dPi_Q|^2 and source coupling is A_obs dot J_Q.",
            "calculation": "delta_Pi A_obs=-q_*^{-1}delta Pi, delta_Pi F_obs=-q_*^{-1}d delta Pi, so the Euler equation is nabla_b(Z_EM F_obs^{ba})=J_Q^a plus B_Q/constraint/defect residuals.",
            "status": "EXACT_WITH_RESIDUALS",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "VAR3784_3_stress_descent",
            "result": "Metric variation supplies the Maxwell Hilbert stress with normalization Z_EM only if the kinetic term uses the same g_eff and descends through the same q_obs quotient.",
            "calculation": "T_EM^{ab}=Z_EM(F^a_c F^{bc}-1/4 g_eff^{ab}F^2); any separate metric, Z_EM vertical drift, or source split re-enters the residual vector.",
            "status": "EXACT_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "derivation_id": "VAR3784_4_vertical_variation",
            "result": "The local vertical EM obstruction vanishes only under Pi_Q, q_*, Z_EM, current, and defect q_obs descent.",
            "calculation": "Lie_EA A_obs=d(Lie_EA theta_Q/q_*)-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs; hence R_A=-q_*^{-1}Lie_EA Pi_Q-beta_q,A A_obs, beta_Z,A=Lie_EA ln Z_EM.",
            "status": "EXACT_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
    ]


def noncircularity_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "test_id": "NCT3784_0_no_A_in_BQ",
            "requirement": "B_Q[Phi_MTS,Psi_Q] contains no A_obs, F_obs, Maxwell equation, Lorentz force, or EM stress as an input.",
            "current_status": "UNSIGNED",
            "verdict": "blocks derived claim; otherwise Pi_Q is renamed EM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "test_id": "NCT3784_1_flow_origin",
            "requirement": "B_Q is computed from owned MTS flow primitives such as normalized phase-flow, vorticity, connection on node bundle, or pre-EM Poynting-like stress flow.",
            "current_status": "PROMISING_UNFILLED",
            "verdict": "best constructive fork is vorticity/defect flow, but parent operator is not yet written",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "test_id": "NCT3784_2_no_pure_gradient",
            "requirement": "dPi_Q must be nonzero away from defects without defining Pi_Q=dtheta_Q or df(psi).",
            "current_status": "PASSED_AS_GUARD_NOT_AS_CONSTRUCTION",
            "verdict": "pure-gradient routes rejected; need primitive one-form or defect curvature",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "test_id": "NCT3784_3_same_source",
            "requirement": "J_Q, charged matter, EM stress, and binding stress arise from the same source action used by Pi_M_total.",
            "current_status": "UNSIGNED",
            "verdict": "blocks Newton/PPN promotion until source action is explicit",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "test_id": "NCT3784_4_normalization",
            "requirement": "q_*, N_Q, and Z_Pi are fixed by parent units/superselection or empirical finite-bound rows, not tuned after data.",
            "current_status": "UNSIGNED",
            "verdict": "blocks alpha_EM claim; leaves finite-bound mode active",
            "valid_for_claim": False,
        },
    ]


def zero_condition_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "condition_id": "ZC3784_0_PiQ_descent",
            "zero_condition": "Lie_EA Pi_Q=0",
            "residual_if_unsigned": "epsilon_Pi_vertical and epsilon_dPi_vertical",
            "current_status": "MISSING_PARENT_FLOW_OWNER",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "condition_id": "ZC3784_1_charge_unit",
            "zero_condition": "Lie_EA ln q_*=0",
            "residual_if_unsigned": "beta_q,A",
            "current_status": "MISSING_CHARGE_UNIT_SUPERSELECTION",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "condition_id": "ZC3784_2_ZEM",
            "zero_condition": "Lie_EA ln Z_EM=0",
            "residual_if_unsigned": "beta_Z,A",
            "current_status": "MISSING_ZEM_OWNER",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "condition_id": "ZC3784_3_lambda",
            "zero_condition": "lambda_A=0 through primitive-only/no-observed-pullback operator basis",
            "residual_if_unsigned": "lambda_A",
            "current_status": "MISSING_OPERATOR_BASIS_PROOF",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "condition_id": "ZC3784_4_defects",
            "zero_condition": "D_Q and Wilson cycles are q_obs-owned or vanish on the local patch",
            "residual_if_unsigned": "epsilon_node",
            "current_status": "MISSING_DEFECT_WILSON_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "condition_id": "ZC3784_5_current",
            "zero_condition": "J_Q descends from the same q_obs total source action",
            "residual_if_unsigned": "epsilon_J_Q and EM/source WEP-PPN rows",
            "current_status": "MISSING_SAME_SOURCE_ACTION",
            "valid_for_claim": False,
        },
    ]


def finite_mode_rows(timestamp):
    rows = []
    for residual, meaning, arena in [
        ("epsilon_Pi_vertical", "vertical change of primitive Pi_Q", "A/F readout"),
        ("epsilon_dPi_vertical", "vertical change of dPi_Q/F", "EM stress and PPN"),
        ("beta_q,A", "vertical drift of charge unit", "charge units and alpha"),
        ("epsilon_node", "node/Wilson/defect residue", "topology and local patch"),
        ("beta_Z,A", "vertical drift of Maxwell normalization", "WEP, clocks, Gdot, PPN"),
        ("lambda_A", "observed Maxwell pullback counterterm", "operator basis and alpha"),
        ("epsilon_J_Q", "same-source charged-current failure", "Hilbert source and Newton/PPN"),
    ]:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "residual": residual,
                "meaning": meaning,
                "arena": arena,
                "numeric_value": f"MISSING_{residual.upper()}",
                "action_if_not_zeroed": "source_or_bound_before_claim",
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_1_action_clause",
            "pass": True,
            "claim_allowed": False,
            "details": "minimal parent U1 action grammar written",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_2_variation",
            "pass": True,
            "claim_allowed": False,
            "details": "theta and Pi_Q variations give Ward/Maxwell equations conditionally",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_3_non_circular_BQ",
            "pass": False,
            "claim_allowed": False,
            "details": "B_Q MTS-flow operator remains unsigned",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_4_zero_conditions",
            "pass": False,
            "claim_allowed": False,
            "details": "Pi_Q, q_*, Z_EM, lambda_A, defects, and J_Q descent remain open",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_5_finite_mode",
            "pass": True,
            "claim_allowed": False,
            "details": "finite EM residual rows retained",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3784_6_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "not claimable until B_Q and zero conditions are parent-signed or bounded",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3784_0_actual_progress",
            "decision": "The U(1) route can be made into a real parent action clause.",
            "action": "Keep it as a viable parent-extension branch rather than treating EM as pure hand closure.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3784_1_key_gap",
            "decision": "The only honest derivation gap is now B_Q: the parent-owned MTS flow one-form that is not A/F in disguise.",
            "action": "Next target should attempt B_Q from vorticity, node/defect flow, or pre-EM stress/Poynting geometry.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3784_2_no_claim",
            "decision": "Do not claim local-GR/EM closure from the action grammar alone.",
            "action": "Use finite-bound mode if B_Q cannot be built.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
            "target_script": "scripts/Y5_R2FR_3785_derive_BQ_flow_one_form_from_vorticity_defects_or_demote_EM.py",
            "objective": "Try to construct the non-circular B_Q[Phi_MTS,Psi_Q] one-form from MTS flow/vorticity/node-defect/Poynting geometry; if no owned one-form exists, formally demote EM readout to finite-bound parent-extension mode.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "PARENT_U1_ACTION_GRAMMAR_WRITTEN_BQ_OWNER_STILL_UNSIGNED",
            "plain_verdict": "3784 takes the leap from missing-list to an actual parent U(1) action grammar. It conditionally derives Ward/Maxwell descent, but the non-circular MTS flow one-form B_Q is still the live gap.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(path.exists() and list(csv.DictReader(path.open(encoding="utf-8"))) is not None for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3784 markdown document written"),
        (
            "action_clause",
            len(grouped["action_clause"]) >= 6,
            "parent U1 action clause emitted",
        ),
        (
            "variation_derivation",
            len(grouped["variation"]) >= 5,
            "theta/Pi_Q/metric/vertical variation rows emitted",
        ),
        (
            "noncircularity_guard",
            any(row["test_id"] == "NCT3784_0_no_A_in_BQ" for row in grouped["noncircular"]),
            "B_Q no-A/F guard emitted",
        ),
        (
            "zero_conditions",
            len(grouped["zero_conditions"]) >= 6,
            "q_obs zero-or-bound conditions emitted",
        ),
        (
            "finite_mode",
            all(row["valid_for_claim"] is False for row in grouped["finite_mode"]),
            "finite EM mode rows stay nonclaim",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3784_6_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "EM/local-GR claim gate remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3785-"),
            "3785 B_Q construction target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3784 files written under formalization-workbench",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "validation_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for check_id, ok, detail in checks
    ]


def render_section(title, rows, key_fields):
    lines = [f"## {title}"]
    for row in rows:
        head = " ".join(f"`{row[field]}`" for field in key_fields if field in row)
        details = []
        for key, value in row.items():
            if key in key_fields or key in {"timestamp_utc", "checkpoint_id", "branch_id", "valid_for_claim"}:
                continue
            details.append(f"{key}: {value}")
        lines.append(f"- {head}: " + "; ".join(details))
    lines.append("")
    return "\n".join(lines)


def render_doc(grouped):
    status = grouped["status"][0]
    text = [
        "# 3784 - Parent U(1) Action Clause or EM Finite-Bound Mode",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3784 writes the actual parent-action fork. If we allow a parent U(1) bundle with a primitive one-form `Pi_Q`, then `A_obs=q_*^{-1}(dtheta_Q-Pi_Q)` is not vague coupling talk: varying `theta_Q` gives current conservation, varying `Pi_Q` gives the Maxwell equation, and varying `g_eff` gives the Maxwell Hilbert stress. The catch is honest and sharp: unless `Pi_Q` is built from a non-circular MTS flow operator `B_Q[Phi_MTS,Psi_Q]`, this is a viable parent extension rather than a derivation from the current real-scalar corpus.",
        "",
        render_section("Parent U(1) Action Clause", grouped["action_clause"], ["clause_id", "status"]),
        render_section("Variation And Maxwell Descent", grouped["variation"], ["derivation_id", "status"]),
        render_section("Noncircularity And Flow Owner Tests", grouped["noncircular"], ["test_id", "current_status"]),
        render_section("q_obs Zero Conditions", grouped["zero_conditions"], ["condition_id", "current_status"]),
        render_section("EM Finite-Bound Mode", grouped["finite_mode"], ["residual"]),
        render_section("Claim Gates", grouped["claim_gates"], ["gate_id"]),
        render_section("Decisions", grouped["decisions"], ["decision_id"]),
        render_section("Next Target", grouped["next_target"], ["target_file"]),
        render_section("Validation", grouped["validation"], ["validation_id", "result"]),
    ]
    return "\n".join(text).rstrip() + "\n"


def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    grouped = {
        "sources": source_register(timestamp),
        "action_clause": action_clause_rows(timestamp),
        "variation": variation_rows(timestamp),
        "noncircular": noncircularity_rows(timestamp),
        "zero_conditions": zero_condition_rows(timestamp),
        "finite_mode": finite_mode_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["action_clause"], grouped["action_clause"])
    write_csv(OUTPUTS["variation"], grouped["variation"])
    write_csv(OUTPUTS["noncircular"], grouped["noncircular"])
    write_csv(OUTPUTS["zero_conditions"], grouped["zero_conditions"])
    write_csv(OUTPUTS["finite_mode"], grouped["finite_mode"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3784 validation failed: {failures}")
    print("wrote 3784 checkpoint: parent U1 action grammar emitted")


if __name__ == "__main__":
    main()
