import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3790"
BRANCH = "MTS_R2FR_Y5_CHARGE_UNIT_SUPERSELECTION_OR_BETAQ_BOUND_3790"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3790_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3790_QSTAR_SUPERSELECTION_THEOREM.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3790_CURRENT_CORPUS_QSTAR_SIGNATURE_AUDIT.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_3790_BETAQ_ZERO_OR_BOUND_COMPONENTS.csv",
    "ra_dra_update": RESIDUALS / "P8_Y5_R2FR_3790_RA_DRA_UPDATE.csv",
    "alpha_guard": RESIDUALS / "P8_Y5_R2FR_3790_ALPHA_ZEM_OVERCLAIM_GUARD.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3790_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3790_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3790_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3790_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3790_VALIDATION.csv",
}

SOURCE_PATHS = [
    PCW / "3789-Y5-R2FR-BQ-first-norm-and-patch-convention-or-field-map-fill.md",
    PCW / "3788-Y5-R2FR-BQ-first-coefficient-source-pack-RA-dRA.md",
    PCW / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md",
    PCW / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md",
    PCW / "3781-Y5-R2FR-construct-EM-connection-from-MTS-flow-or-bound-RA-betaZ.md",
    PCW / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md",
    PCW / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
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
            "source_role": "qstar_superselection_betaq_context",
            "valid_for_claim": False,
        }
        for path in SOURCE_PATHS
    ]


def theorem_rows(timestamp):
    rows = [
        {
            "theorem_id": "QST3790_0_constant_superselection_template",
            "claim_piece": "vertical silence of a constant/charge unit",
            "mathematical_form": "If q_*(Phi)=qbar_*(q_obs(Phi)) or q_* is discrete/topological representation data, then Dq_obs[E_A]=0 implies Lie_EA q_*=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "parent classification that q_* is quotient-owned or topological charge-lattice data",
            "if_unsigned": "retain beta_q,A",
        },
        {
            "theorem_id": "QST3790_1_compact_lattice_route",
            "claim_piece": "q_* as compact U(1) charge-lattice period",
            "mathematical_form": "For a fixed compact U(1) parent bundle, charges are representation/lattice labels n in Z and q_* is the global lattice scale; admissible local vertical variations preserve the lattice, so Lie_EA ln q_*=0.",
            "proof_status": "EXACT_IF_PARENT_U1_LATTICE_SIGNED",
            "missing_for_current_claim": "parent-signed P_Q, fixed charge lattice/generator, and nonrescalable normalization",
            "if_unsigned": "beta_q,A remains a finite residual row",
        },
        {
            "theorem_id": "QST3790_2_betaq_derivative",
            "claim_piece": "d beta_q,A",
            "mathematical_form": "If beta_q,A:=Lie_EA ln q_*=0 as a superselection identity on U_good, then d beta_q,A=0 on U_good.",
            "proof_status": "EXACT_CONDITIONAL_COROLLARY",
            "missing_for_current_claim": "same parent-signed q_* superselection as QST3790_1",
            "if_unsigned": "eps_dbetaqA remains a finite residual row",
        },
        {
            "theorem_id": "QST3790_3_not_alpha_owner",
            "claim_piece": "q_* silence does not imply alpha_EM or Z_EM silence",
            "mathematical_form": "Compactness fixes charge labels/connection periods, but Z_EM, N_Q, lambda_A, current normalization, and readout descent can still vary.",
            "proof_status": "ACTIVE_OVERCLAIM_GUARD",
            "missing_for_current_claim": "unique Maxwell F^2 normalization, fixed generator norm, same-current owner, and readout descent",
            "if_unsigned": "retain beta_Z,A, lambda_A, epsilon_J_Q, and alpha/readout residuals",
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
        row["valid_for_claim"] = False
    return rows


def audit_rows(timestamp):
    rows = [
        {
            "audit_id": "AUD3790_0_3783_qstar",
            "source_signal": "3783 marks qstar_superselected as false/missing charge-unit owner",
            "current_result": "CURRENT_CORPUS_UNSIGNED",
            "impact": "cannot promote beta_q,A=0 as a current derived MTS result",
            "valid_for_claim": False,
        },
        {
            "audit_id": "AUD3790_1_3784_action_clause",
            "source_signal": "3784 includes q_* in the minimal parent U(1) field space and names charge-unit zero as a required zero condition",
            "current_result": "PARENT_EXTENSION_ROUTE_AVAILABLE",
            "impact": "q_* can be signed as a clean parent-extension clause without changing the RA/dRA algebra",
            "valid_for_claim": False,
        },
        {
            "audit_id": "AUD3790_2_1047_constant_theorem",
            "source_signal": "1047 proves the exact conditional criterion: quotient-descended or topological constants are vertical-silent",
            "current_result": "THEOREM_TEMPLATE_AVAILABLE",
            "impact": "q_* silence is mathematically justified if q_* is classified as charge-lattice/topological data",
            "valid_for_claim": False,
        },
        {
            "audit_id": "AUD3790_3_1056_alpha_guard",
            "source_signal": "1056 says compact U1 fixes charge lattice/periods but not continuous Maxwell kinetic coefficient",
            "current_result": "NO_ALPHA_PROMOTION",
            "impact": "zeroing beta_q,A does not zero beta_Z,A or derive alpha_EM",
            "valid_for_claim": False,
        },
        {
            "audit_id": "AUD3790_4_current_verdict",
            "source_signal": "all relevant sources support a conditional q_* theorem but do not parent-sign the current corpus",
            "current_result": "CONDITIONAL_ZERO_EXTENSION_OR_FINITE_BOUND_FALLBACK",
            "impact": "emit both the exact zero branch and nonclaim beta_q bound rows",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def component_rows(timestamp):
    rows = [
        {
            "component_id": "BQ3790_0_beta_qA",
            "symbol": "beta_q,A",
            "definition": "Lie_EA ln q_*",
            "zero_if": "q_* is quotient-owned or compact charge-lattice/superselection data and E_A preserves the parent bundle/lattice",
            "conditional_value": "0",
            "fallback_value": "MISSING_BETA_QA_OR_PARENT_ZERO_THEOREM",
            "feeds": "eps_qA;eps_betaqF;alpha_source_leakage;Gdot_source_rate",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "BQ3790_1_d_beta_qA",
            "symbol": "d beta_q,A",
            "definition": "exterior derivative on U_good of beta_q,A",
            "zero_if": "beta_q,A=0 as a superselection identity or beta_q,A is constant on U_good",
            "conditional_value": "0",
            "fallback_value": "MISSING_DBETA_QA_PROFILE_OR_BOUND",
            "feeds": "eps_dbetaqA",
            "status": "CONDITIONAL_ZERO_CURRENTLY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "BQ3790_2_eps_qA",
            "symbol": "eps_qA",
            "definition": "|beta_q,A| ||A_obs||_A/A_ref",
            "zero_if": "beta_q,A=0",
            "conditional_value": "0",
            "fallback_value": "|beta_q,A| ||A_obs||_A/A_ref",
            "feeds": "RA_normed",
            "status": "ZERO_IN_QSTAR_EXTENSION_BRANCH_ELSE_BOUND_ROW",
            "valid_for_claim": False,
        },
        {
            "component_id": "BQ3790_3_eps_betaqF",
            "symbol": "eps_betaqF",
            "definition": "|beta_q,A| ||F_obs||_F/F_ref",
            "zero_if": "beta_q,A=0",
            "conditional_value": "0",
            "fallback_value": "|beta_q,A| ||F_obs||_F/F_ref",
            "feeds": "dRA_normed",
            "status": "ZERO_IN_QSTAR_EXTENSION_BRANCH_ELSE_BOUND_ROW",
            "valid_for_claim": False,
        },
        {
            "component_id": "BQ3790_4_eps_dbetaqA",
            "symbol": "eps_dbetaqA",
            "definition": "||d beta_q,A wedge A_obs||_F/F_ref",
            "zero_if": "d beta_q,A=0 or A_obs wedge d beta_q,A=0 by source-backed profile",
            "conditional_value": "0",
            "fallback_value": "||d beta_q,A wedge A_obs||_F/F_ref",
            "feeds": "dRA_normed",
            "status": "ZERO_IN_QSTAR_EXTENSION_BRANCH_ELSE_BOUND_ROW",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def ra_dra_update_rows(timestamp):
    rows = [
        {
            "update_id": "RDU3790_0_full_3789_nonclaim",
            "branch": "finite_current_corpus",
            "formula": "RA_normed <= eps_BQ_descent_A + eps_BQ_chart_A + eps_qA",
            "conditions": "no q_* superselection claim; chart may or may not be local-zero",
            "status": "RETAINED_BOUND_FORM",
            "valid_for_claim": False,
        },
        {
            "update_id": "RDU3790_1_qstar_zero",
            "branch": "qstar_superselected_parent_extension",
            "formula": "RA_normed <= eps_BQ_descent_A + eps_BQ_chart_A",
            "conditions": "Lie_EA q_*=0 from parent-signed compact charge lattice",
            "status": "CONDITIONAL_SIMPLIFICATION",
            "valid_for_claim": False,
        },
        {
            "update_id": "RDU3790_2_qstar_and_Ugood_zero",
            "branch": "qstar_superselected_on_Ugood",
            "formula": "RA_normed <= eps_BQ_descent_A",
            "conditions": "q_* superselected plus U_good chart/Wilson zero",
            "status": "CONDITIONAL_LOCAL_SIMPLIFICATION",
            "valid_for_claim": False,
        },
        {
            "update_id": "RDU3790_3_dRA_qstar_zero",
            "branch": "qstar_superselected_parent_extension",
            "formula": "dRA_normed <= eps_dBQ_A + eps_dchart_A",
            "conditions": "beta_q,A=0 and d beta_q,A=0 from parent-signed charge lattice",
            "status": "CONDITIONAL_SIMPLIFICATION",
            "valid_for_claim": False,
        },
        {
            "update_id": "RDU3790_4_dRA_qstar_and_Ugood_zero",
            "branch": "qstar_superselected_on_Ugood",
            "formula": "dRA_normed <= eps_dBQ_A",
            "conditions": "q_* superselected plus U_good chart/Wilson zero",
            "status": "CONDITIONAL_LOCAL_SIMPLIFICATION",
            "valid_for_claim": False,
        },
        {
            "update_id": "RDU3790_5_hard_remainder",
            "branch": "local_EM_GR_remainder",
            "formula": "local EM closure now reduces to B_Q descent/owner/rank/Z_EM/current/lambda/defect clauses after q_* is signed",
            "conditions": "does not prove B_Q owner, Z_EM owner, same-source current, or unique Maxwell kinetic normalization",
            "status": "REMAINDER_EXPLICIT",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def alpha_guard_rows(timestamp):
    rows = [
        {
            "guard_id": "AG3790_0_charge_lattice_not_alpha",
            "rule": "Do not infer beta_Z,A=0 or b_alpha=0 from beta_q,A=0.",
            "because": "compact U(1) fixes charge labels/periods, while Maxwell kinetic normalization and readout can vary independently",
            "retained_rows": "beta_Z,A;lambda_A;N_Q;Z_EM;epsilon_J_Q;b_alpha",
            "valid_for_claim": False,
        },
        {
            "guard_id": "AG3790_1_no_generator_rescale_cheat",
            "rule": "A fixed charge lattice must include a nonrescalable parent generator/norm; otherwise q_* can be conventionally rescaled with A_Q/current labels.",
            "because": "1056 rescaling ledger keeps generator/current normalization unsigned",
            "retained_rows": "N_Q;current normalization;readout descent",
            "valid_for_claim": False,
        },
        {
            "guard_id": "AG3790_2_parent_extension_flag",
            "rule": "The q_* zero is a valid parent-extension clause, not yet a derivation from the current real-scalar MTS corpus.",
            "because": "3783/3784 explicitly say the parent U(1) bundle and primitive Pi_Q remain unsigned",
            "retained_rows": "P_Q;Pi_Q;B_Q owner;D_Q defects",
            "valid_for_claim": False,
        },
    ]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def claim_gate_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_0_sources",
            "pass": True,
            "claim_allowed": False,
            "details": "all cited source paths resolve",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_1_qstar_theorem_shape",
            "pass": True,
            "claim_allowed": False,
            "details": "exact conditional q_* superselection theorem emitted",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_2_current_qstar_signed",
            "pass": False,
            "claim_allowed": False,
            "details": "current corpus still lacks parent-signed U(1) bundle/generator/lattice owner",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_3_extension_branch_zeroes_betaq",
            "pass": True,
            "claim_allowed": False,
            "details": "if q_* is accepted as parent-superselected charge-lattice data, beta_q,A and d beta_q,A vanish",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_4_no_alpha_overclaim",
            "pass": True,
            "claim_allowed": False,
            "details": "Z_EM/alpha/current/readout rows remain live despite q_* zero branch",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_5_numeric_bound_ready",
            "pass": False,
            "claim_allowed": False,
            "details": "finite fallback still lacks numeric beta_q,A or d beta_q,A bound/profile",
        },
        {
            "timestamp_utc": timestamp,
            "gate_id": "CG3790_6_local_GR_EM_claim",
            "pass": False,
            "claim_allowed": False,
            "details": "no local-GR/EM claim; q_* theorem only removes one charge-unit residual branch conditionally",
        },
    ]


def decision_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3790_0_take_conditional_win",
            "decision": "q_* superselection is an exact conditional theorem and should be used in the parent U(1) extension branch.",
            "action": "Mark beta_q,A, eps_qA, eps_betaqF, and eps_dbetaqA as zero only under the signed charge-lattice clause.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3790_1_keep_current_corpus_honest",
            "decision": "The current real-scalar corpus still has not derived the parent U(1) bundle or q_* owner.",
            "action": "Retain beta_q finite-bound rows for current-corpus mode.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3790_2_no_alpha_jump",
            "decision": "Charge-unit silence does not own alpha_EM.",
            "action": "Keep beta_Z,A, lambda_A, N_Q/Z_EM, current normalization, and readout descent as separate gates.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "decision_id": "DEC3790_3_next",
            "decision": "After q_* zero, the next cheap exact target is Z_EM/Maxwell normalization or same-current owner; the hardest remaining target is still B_Q owner.",
            "action": "Attempt Z_EM fixed-normalization/no-independent-F2 gate in the R2FR local EM branch.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "target_file": "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md",
            "target_script": "scripts/Y5_R2FR_3791_ZEM_fixed_normalization_or_betaZ_bound.py",
            "objective": "Try to prove beta_Z,A=0 from fixed parent generator norm/unique Maxwell kinetic normalization/no independent F^2 operator in the local EM branch; if it fails, emit source-ready beta_Z/lambda_A bound rows without claiming alpha_EM ownership.",
            "valid_for_claim": False,
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "checkpoint_id": CHECKPOINT,
            "branch_id": BRANCH,
            "status": "QSTAR_SUPERSELECTION_EXACT_IF_PARENT_SIGNED_CURRENT_CORPUS_UNSIGNED_BETAQ_ROWS_RETAINED",
            "plain_verdict": "3790 proves the exact conditional q_* route: a parent-signed compact charge lattice makes beta_q,A=0 and d beta_q,A=0, which zeroes eps_qA, eps_betaqF, and eps_dbetaqA. The current corpus still has q_* unsigned, so finite beta_q bound rows remain. This does not derive alpha_EM or Z_EM.",
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
        ("doc_written", DOC_PATH.exists(), "3790 markdown document written"),
        (
            "qstar_theorem",
            any(row["theorem_id"] == "QST3790_1_compact_lattice_route" for row in grouped["theorem"]),
            "compact charge-lattice q_* theorem emitted",
        ),
        (
            "current_unsigned",
            any(row["audit_id"] == "AUD3790_0_3783_qstar" and row["current_result"] == "CURRENT_CORPUS_UNSIGNED" for row in grouped["audit"]),
            "current corpus unsigned status retained",
        ),
        (
            "zero_components",
            all(
                any(row["symbol"] == symbol and row["conditional_value"] == "0" for row in grouped["components"])
                for symbol in ["beta_q,A", "d beta_q,A", "eps_qA", "eps_betaqF", "eps_dbetaqA"]
            ),
            "conditional zero rows emitted for beta_q branch",
        ),
        (
            "alpha_guard",
            any(row["guard_id"] == "AG3790_0_charge_lattice_not_alpha" for row in grouped["alpha_guard"]),
            "alpha/Z_EM overclaim guard emitted",
        ),
        (
            "claim_gate_closed",
            any(row["gate_id"] == "CG3790_6_local_GR_EM_claim" and row["pass"] is False for row in grouped["claim_gates"]),
            "local GR/EM claim remains closed",
        ),
        (
            "next_target",
            grouped["next_target"][0]["target_file"].startswith("3791-"),
            "3791 Z_EM target emitted",
        ),
        (
            "formalization_clean",
            not any("formalization-workbench" in str(path) for path in OUTPUTS.values()),
            "no 3790 files written under formalization-workbench",
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
        "# 3790 - Charge Unit Superselection or beta_q Bound",
        "",
        "## Status",
        "",
        f"`{status['status']}`.",
        "",
        status["plain_verdict"],
        "",
        "## Result In Plain Terms",
        "",
        "3790 takes a real conditional win without cheating. If `q_*` is a fixed compact U(1) charge-lattice/superselection datum in the parent branch, then `Lie_EA q_*=0`, so `beta_q,A=0` and `d beta_q,A=0`. That kills `eps_qA`, `eps_betaqF`, and `eps_dbetaqA` in the local `R_A/dR_A` response. But the current corpus has not yet signed the parent U(1) bundle/generator/lattice owner, so finite `beta_q` rows stay live in current-corpus mode. Also: this does not derive `alpha_EM`, `Z_EM`, or the Maxwell kinetic coefficient.",
        "",
        "## Compact Result",
        "",
        "`beta_q,A := Lie_EA ln q_*`.",
        "",
        "If `q_*` is quotient-owned or compact charge-lattice superselected, then `beta_q,A=0` and `d beta_q,A=0`.",
        "",
        "Then `eps_qA=0`, `eps_betaqF=0`, and `eps_dbetaqA=0`.",
        "",
        "With the `U_good` chart-zero from 3789, the local response reduces conditionally to `RA_normed <= eps_BQ_descent_A` and `dRA_normed <= eps_dBQ_A`.",
        "",
        "The remaining hard blockers are `B_Q` owner/descent, `Z_EM`, `lambda_A`, same-current descent, defects, and source/Hilbert stress ownership.",
        "",
        render_section("q_* Superselection Theorem", grouped["theorem"], ["theorem_id", "claim_piece"]),
        render_section("Current Corpus Signature Audit", grouped["audit"], ["audit_id"]),
        render_section("beta_q Zero or Bound Components", grouped["components"], ["component_id", "symbol"]),
        render_section("R_A/dR_A Update", grouped["ra_dra_update"], ["update_id", "branch"]),
        render_section("Alpha/Z_EM Overclaim Guard", grouped["alpha_guard"], ["guard_id"]),
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
        "theorem": theorem_rows(timestamp),
        "audit": audit_rows(timestamp),
        "components": component_rows(timestamp),
        "ra_dra_update": ra_dra_update_rows(timestamp),
        "alpha_guard": alpha_guard_rows(timestamp),
        "claim_gates": claim_gate_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
        "validation": [],
    }

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["components"], grouped["components"])
    write_csv(OUTPUTS["ra_dra_update"], grouped["ra_dra_update"])
    write_csv(OUTPUTS["alpha_guard"], grouped["alpha_guard"])
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
        raise SystemExit(f"3790 validation failed: {failures}")
    print("wrote 3790 checkpoint: q_* superselection theorem and beta_q fallback emitted")


if __name__ == "__main__":
    main()
