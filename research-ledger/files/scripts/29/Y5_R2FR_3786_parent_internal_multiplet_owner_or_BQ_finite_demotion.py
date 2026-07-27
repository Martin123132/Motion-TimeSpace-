import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3786"
BRANCH = "MTS_R2FR_Y5_PARENT_INTERNAL_MULTIPLET_OWNER_OR_BQ_FINITE_DEMOTION_3786"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3786_SOURCE_REGISTER.csv",
    "owner_theorem": RESIDUALS / "P8_Y5_R2FR_3786_INTERNAL_MULTIPLET_OWNER_THEOREM.csv",
    "source_audit": RESIDUALS / "P8_Y5_R2FR_3786_CURRENT_CORPUS_MULTIPLET_SOURCE_AUDIT.csv",
    "demotion_vector": RESIDUALS / "P8_Y5_R2FR_3786_BQ_OFFICIAL_FINITE_RESIDUAL_VECTOR.csv",
    "response_contract": RESIDUALS / "P8_Y5_R2FR_3786_BQ_RESPONSE_OPERATOR_CONTRACT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3786_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3786_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3786_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3786_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3786_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md",
    PCW / "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md",
    PCW / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md",
    PCW / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
    PCW / "1174-Y5-R10-local-Qflow-stationarity-theorem-or-first-Qflow-bound-row.md",
    PCW / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
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
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "source_path": str(path),
            "exists": path.exists(),
            "source_role": "internal_multiplet_owner_audit",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def owner_theorem_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "theorem_id": "IMO3786_0_parent_field_space",
            "status": "EXACT_CONDITIONAL",
            "statement": "If the parent field space contains either four pre-EM flow scalars Y_Q=(C1,D1,C2,D2) with fixed internal symplectic form omega_Q=dC1 wedge dD1+dC2 wedge dD2, or an equivalent normalized internal multiplet z:U->C^3 with U(1) chart redundancy, then B_Q can be parent-owned before EM readout.",
            "proof_role": "supplies the missing owner object for 3785 without defining it from A_obs/F_obs",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "theorem_id": "IMO3786_1_BQ_definition",
            "status": "EXACT_CONDITIONAL",
            "statement": "Define B_Q=C1 dD1+C2 dD2, or in the internal multiplet chart B_Q=-i z_dagger dz after quotienting the pure fibre phase. Then H_Q=dB_Q is closed and can have generic local rank.",
            "proof_role": "connects the internal owner to the 3784 action grammar and 3785 rank gate",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "theorem_id": "IMO3786_2_chart_covariance",
            "status": "EXACT_CONDITIONAL",
            "statement": "On overlaps, B_Q^a-B_Q^b=dchi_ab and H_Q is invariant. This gives the U(1) bundle transition rule needed by A_obs=q_*^{-1}(dtheta_Q-Pi_Q).",
            "proof_role": "turns the 3784 local one-form into a bundle object rather than a single-patch artifact",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "theorem_id": "IMO3786_3_non_smuggle",
            "status": "NO_SMUGGLE_CONDITION",
            "statement": "The coordinates Y_Q or z must be varied parent fields or derived functorially from MTS flow data before A_obs, F_obs, Maxwell equations, or Lorentz/Poynting EM stress are defined.",
            "proof_role": "prevents the multiplet route from parameterizing a known Maxwell field after the fact",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "theorem_id": "IMO3786_4_qobs_descent",
            "status": "ZERO_OR_BOUND_CONDITION",
            "statement": "If Lie_EA Y_Q=0 modulo chart gauge and Lie_EA q_*=Lie_EA Z_EM=0, then the B_Q route gives R_A=0 and beta_Z,A=0; otherwise the failure is measured by epsilon_BQ_owner, epsilon_BQ_rank, epsilon_BQ_chart, epsilon_BQ_descent, beta_q,A, beta_Z,A, lambda_A, and epsilon_J_Q.",
            "proof_role": "connects internal multiplet ownership to the local-GR/EM residual vector",
            "valid_for_claim": False,
        },
    ]


def source_audit_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "audit_id": "CSA3786_0_real_psi_branch",
            "candidate_source": "current real scalar psi",
            "owner_test": "Can psi supply four independent pre-EM flow scalars or CP2 chart coordinates?",
            "result": "FAIL_CURRENT_CORPUS",
            "reason": "3782/3785 show real psi and pure gradients do not generate generic nonzero dB_Q.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "CSA3786_1_phase_flow_U1",
            "candidate_source": "theta_Q/Pi_Q phase-flow route",
            "owner_test": "Does the existing corpus own theta_Q, Pi_Q, and q_* before EM readout?",
            "result": "FAIL_CURRENT_CORPUS",
            "reason": "3783/3784 make this a viable parent extension but current sources do not own P_Q/Pi_Q/q_*/N_Q.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "CSA3786_2_Qflow_stationarity",
            "candidate_source": "Q-flow / Theta_Q residual chain",
            "owner_test": "Can Q-flow stationarity provide CP2 or two Clebsch coordinates?",
            "result": "PARTIAL_SUPPORT_NOT_OWNER",
            "reason": "1174 supplies a scalar stationarity defect and projector issue, not a parent internal U(1) multiplet with generic two-form rank.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "CSA3786_3_motion_phase_volume",
            "candidate_source": "motion-load / phase-volume route",
            "owner_test": "Can phase-volume alone own the internal multiplet?",
            "result": "FAIL_AS_OWNER",
            "reason": "1859 rejects direct phase-volume as a parent derivation; it motivates flow structure but does not provide field coordinates or chart covariance.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "CSA3786_4_compact_U1_norm",
            "candidate_source": "compact U(1), T_Q, charge lattice, gauge norm",
            "owner_test": "Does compact U(1) own the internal multiplet and alpha normalization?",
            "result": "SUPPORT_ONLY_NOT_OWNER",
            "reason": "1056/1100 say compactness helps charge labels but not continuous gauge norm, current owner, no-extra-F2, or readout closure.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "audit_id": "CSA3786_5_verdict",
            "candidate_source": "current corpus total",
            "owner_test": "Is there a parent-owned two-pair/CP2 internal multiplet now?",
            "result": "NO_CURRENT_OWNER_FOUND",
            "reason": "The owner theorem is coherent, but no source currently provides the required parent object.",
            "valid_for_claim": False,
        },
    ]


def demotion_vector_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "residual_id": "BQR3786_0_owner",
            "symbol": "epsilon_BQ_owner",
            "definition": "failure of a parent-owned two-Clebsch-pair/CP2 internal multiplet before EM readout",
            "zero_condition": "Y_Q or z is a parent field/functor of MTS flow, not reconstructed from A_obs/F_obs",
            "current_status": "MISSING_PARENT_INTERNAL_MULTIPLET",
            "arena": "EM_readout;local_GR;PPN",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "residual_id": "BQR3786_1_rank",
            "symbol": "epsilon_BQ_rank",
            "definition": "rank loss from using one pair/CP1 where generic EM requires H_Q wedge H_Q support",
            "zero_condition": "two-pair or CP2/higher rank certificate signed",
            "current_status": "MISSING_GENERIC_RANK_CERTIFICATE",
            "arena": "generic_EM;stress;PPN",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "residual_id": "BQR3786_2_chart",
            "symbol": "epsilon_BQ_chart",
            "definition": "failure of bundle chart covariance B_Q^a-B_Q^b=dchi_ab",
            "zero_condition": "parent transition functions and Wilson/defect data are signed",
            "current_status": "MISSING_CHART_COVARIANCE_CERTIFICATE",
            "arena": "gauge;Wilson;defects",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "residual_id": "BQR3786_3_descent",
            "symbol": "epsilon_BQ_descent",
            "definition": "vertical q_obs leakage of the internal multiplet owner",
            "zero_condition": "Lie_EA Y_Q=0 modulo chart gauge, or Lie_EA z=i alpha_A z plus quotient-silent chart terms",
            "current_status": "MISSING_QOBS_DESCENT_PROOF",
            "arena": "R_A;dR_A;local_GR",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "residual_id": "BQR3786_4_norm",
            "symbol": "epsilon_BQ_norm",
            "definition": "failure to tie B_Q owner to fixed q_*, Z_EM, current, no-extra-F2, and readout normalization",
            "zero_condition": "1056/1100 T_Q/gauge-norm/current/no-lambda/readout signature closes",
            "current_status": "MISSING_ALPHA_AND_CURRENT_OWNER",
            "arena": "alpha;WEP;R10;clocks;source_coupling",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "residual_id": "BQR3786_5_total",
            "symbol": "epsilon_BQ_total_abs",
            "definition": "absolute no-cancellation sum of official B_Q residual components",
            "zero_condition": "all B_Q owner/rank/chart/descent/norm residuals zeroed or independently bounded below arena envelopes",
            "current_status": "MISSING_COMPONENT_BOUNDS",
            "arena": "EM;PPN;WEP;R10;clocks;orbital",
            "valid_for_claim": False,
        },
    ]


def response_contract_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "contract_id": "ROC3786_0_RA",
            "response": "R_A",
            "bound_form": "||R_A|| <= C_owner epsilon_BQ_owner + C_chart epsilon_BQ_chart + C_descent epsilon_BQ_descent + |beta_q,A| ||A_obs||",
            "needed_next": "source or derive coefficients C_owner,C_chart,C_descent and local field norm convention",
            "claim_status": "SOURCE_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "contract_id": "ROC3786_1_dRA",
            "response": "dR_A",
            "bound_form": "||dR_A|| <= C_rank epsilon_BQ_rank + C_descent_d epsilon_BQ_descent + C_node epsilon_node",
            "needed_next": "rank-sensitive EM stress/PPN projection coefficient",
            "claim_status": "SOURCE_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "contract_id": "ROC3786_2_alpha_source",
            "response": "alpha/source normalization leakage",
            "bound_form": "|delta ln Z_EM|+|delta ln q_*|+|lambda_A|+epsilon_J_Q+epsilon_BQ_norm",
            "needed_next": "connect to 1056/1100 alpha-owner and same-current rows",
            "claim_status": "SOURCE_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "contract_id": "ROC3786_3_no_cancellation",
            "response": "official B_Q finite envelope",
            "bound_form": "epsilon_BQ_total_abs=sum_i |epsilon_i| with i in owner,rank,chart,descent,norm",
            "needed_next": "choose arena projection coefficients for PPN/WEP/R10/clocks without cancellations",
            "claim_status": "SOURCE_READY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3786_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3786_1_owner_theorem",
            "pass": True,
            "claim_allowed": False,
            "details": "conditional internal multiplet owner theorem emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3786_2_current_owner",
            "pass": False,
            "claim_allowed": False,
            "details": "no current corpus source owns two-pair/CP2 multiplet",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3786_3_finite_demotion",
            "pass": True,
            "claim_allowed": False,
            "details": "official B_Q residual vector promoted as nonclaim finite branch",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3786_4_response_contract",
            "pass": True,
            "claim_allowed": False,
            "details": "source-ready response operator contracts emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3786_5_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "local GR/EM claim blocked until owner/rank/chart/descent/norm residuals are zeroed or bounded",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3786_0_owner_theorem_kept",
            "decision": "Keep the internal multiplet theorem as the cleanest derivation target.",
            "action": "Use it only as a parent-extension theorem until a source owns Y_Q or z.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3786_1_current_branch_demoted",
            "decision": "Current corpus does not derive B_Q from real psi/Q-flow/phase-volume/compact-U1 alone.",
            "action": "Promote official finite residuals epsilon_BQ_owner/rank/chart/descent/norm.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3786_2_next",
            "decision": "Next step should build the finite response operator map rather than re-hunting the same owner immediately.",
            "action": "Construct arena projection coefficients for R_A, dR_A, alpha/source leakage, and no-cancellation envelopes.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3787-Y5-R2FR-BQ-finite-response-operators-and-arena-projection-map.md",
            "target_script": "scripts/Y5_R2FR_3787_BQ_finite_response_operators_and_arena_projection_map.py",
            "objective": "Build the finite response-operator map from official B_Q residuals into R_A, dR_A, alpha/source leakage, PPN/WEP/R10/clock/orbital arenas; keep no-cancellation and nonclaim gates active.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "INTERNAL_MULTIPLET_OWNER_THEOREM_CONDITIONAL_CURRENT_BRANCH_FINITE_DEMOTED",
            "plain_verdict": "3786 keeps the best B_Q derivation target: a parent-owned two-Clebsch-pair or CP2/Berry internal multiplet would close the construction route. But the current corpus does not own that object, so the current branch is formally demoted to an official finite B_Q residual vector with response-operator contracts.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(timestamp, grouped):
    def csv_parses(path):
        if not path.exists():
            return False
        with path.open(encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True

    checks = [
        (
            "sources_exist",
            all(Path(row["source_path"]).exists() for row in grouped["sources"]),
            "every cited source path exists",
        ),
        (
            "csv_outputs_parse",
            all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation"),
            "all generated CSV outputs exist and parse",
        ),
        ("doc_written", DOC_PATH.exists(), "3786 markdown document written"),
        (
            "owner_theorem",
            len(grouped["owner_theorem"]) >= 5,
            "internal multiplet owner theorem emitted",
        ),
        (
            "source_audit",
            any(row["audit_id"] == "CSA3786_5_verdict" for row in grouped["source_audit"]),
            "current corpus owner audit verdict emitted",
        ),
        (
            "finite_vector",
            len(grouped["demotion_vector"]) >= 6,
            "official B_Q finite residual vector emitted",
        ),
        (
            "response_contract",
            len(grouped["response_contract"]) >= 4,
            "response operator contracts emitted",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3786_5_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "EM/local-GR claim gate remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3787-"),
            "3787 finite response target emitted",
        ),
        (
            "all_nonclaim",
            all(row.get("valid_for_claim") is False for rows in grouped.values() if isinstance(rows, list) for row in rows if isinstance(row, dict) and "valid_for_claim" in row),
            "all science rows remain nonclaim",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3786 files written under formalization-workbench",
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
        "# 3786 - Parent Internal Multiplet Owner or B_Q Finite Demotion",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3786 keeps the leap but stops pretending the current branch already owns it. A parent-owned two-Clebsch-pair flow chart `Y_Q=(C1,D1,C2,D2)` or equivalent CP2/Berry multiplet `z` would make `B_Q` a real pre-EM object and feed the 3784 U(1) action without smuggling Maxwell in. The current corpus does not yet provide that owner. So the route stays alive as a clean parent-extension theorem, while the present branch is officially demoted to finite residuals: `epsilon_BQ_owner`, `epsilon_BQ_rank`, `epsilon_BQ_chart`, `epsilon_BQ_descent`, and `epsilon_BQ_norm`.",
        "",
        render_section("Internal Multiplet Owner Theorem", grouped["owner_theorem"], ["theorem_id", "status"]),
        render_section("Current Corpus Multiplet Source Audit", grouped["source_audit"], ["audit_id", "result"]),
        render_section("Official B_Q Finite Residual Vector", grouped["demotion_vector"], ["residual_id", "symbol"]),
        render_section("B_Q Response Operator Contract", grouped["response_contract"], ["contract_id", "response"]),
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
        "owner_theorem": owner_theorem_rows(timestamp),
        "source_audit": source_audit_rows(timestamp),
        "demotion_vector": demotion_vector_rows(timestamp),
        "response_contract": response_contract_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["owner_theorem"], grouped["owner_theorem"])
    write_csv(OUTPUTS["source_audit"], grouped["source_audit"])
    write_csv(OUTPUTS["demotion_vector"], grouped["demotion_vector"])
    write_csv(OUTPUTS["response_contract"], grouped["response_contract"])
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
        raise SystemExit(f"3786 validation failed: {failures}")
    print("wrote 3786 checkpoint: internal multiplet theorem conditional; B_Q finite residuals official")


if __name__ == "__main__":
    main()
