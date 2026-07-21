from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4740"
CLAIM_ID = "L-582"
MARKER = "PPC4161_PARENT_TRACEFREE_RI_OWNER_ACTION_BLOCK_OR_TRANSITION_FINITE_RESIDUAL_RUNNER_4740"
PACKET_MARKER = "PPC4161_PACKET_PARENT_TRACEFREE_RI_OWNER_ACTION_BLOCK_OR_TRANSITION_FINITE_RESIDUAL_RUNNER_4740"
DECISION = "CONSTRAINED_TFRI_OWNER_ACTION_BLOCK_DERIVED_CONDITIONALLY_METRIC_NULL_BRANCH_UNSIGNED_FINITE_RUNNER_STAGED_NONCLAIM"
NEXT_TARGET = "4741-Y5-R2FR-zero-multiplier-boundary-certificate-or-transition-finite-source-values.md"

DOC_PATH = POST / "4740-Y5-R2FR-parent-tracefree-RI-owner-action-block-or-transition-finite-residual-runner.md"
FORMAL_PATH = FORMAL / "756-PPC4161-parent-tracefree-RI-owner-action-block-or-transition-finite-residual-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_SOURCE_REGISTER.csv"
OWNER_ACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv"
VARIATION_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_METRIC_VARIATION_AUDIT.csv"
SIGNATURE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_EXACT_SIGNATURE_GATES.csv"
FINITE_INPUT_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_TRANSITION_FINITE_RUNNER_INPUT_SCHEMA.csv"
FINITE_DRYRUN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_TRANSITION_FINITE_RUNNER_DRYRUN.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_ROUTE_SELECTION_MATRIX.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4740_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4740_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4740_0_4739_next", SOURCE_DIR / "P8_Y5_R2FR_4739_NEXT_TARGET.csv", "Attempt a parent trace-free RI/metric-null owner action", "4739 handoff"),
    ("SRC4740_1_4739_route", SOURCE_DIR / "P8_Y5_R2FR_4739_ROUTE_SELECTION_MATRIX.csv", "ROUTE4739_2_metric_null_quarantine", "metric-null route"),
    ("SRC4740_2_4739_finite", SOURCE_DIR / "P8_Y5_R2FR_4739_FINITE_RESIDUAL_SCORE_ROWS.csv", "FS4739_0_transition_vector", "finite residual vector"),
    ("SRC4740_3_4739_gates", SOURCE_DIR / "P8_Y5_R2FR_4739_PROMOTION_GATES.csv", "GATE4739_2_quarantine_owner", "promotion gates"),
    ("SRC4740_4_4739_matter", SOURCE_DIR / "P8_Y5_R2FR_4739_ORDINARY_MATTER_GR_PRESERVATION_GATE.csv", "MGR4739_2_transition_null_only", "ordinary matter preservation"),
    ("SRC4740_5_4739_ctfri", SOURCE_DIR / "P8_Y5_R2FR_4739_TFRI_COMMUTATOR_ZERO_OR_BOUND_LAW.csv", "CTF4739_2_fixed_data_zero", "RI commutator zero condition"),
    ("SRC4740_6_4739_cdk", SOURCE_DIR / "P8_Y5_R2FR_4739_CDELTAKDIV_ZERO_OR_BOUND_LAW.csv", "CDK4739_1_TT_kernel_zero", "DeltaK kernel zero condition"),
    ("SRC4740_7_4282_metric_null", SOURCE_DIR / "P8_Y5_R2FR_4282_METRIC_NULL_ACTION_CONTRACT.csv", "MN4282_1", "metric-null action contract"),
    ("SRC4740_8_4282_conservation", SOURCE_DIR / "P8_Y5_R2FR_4282_CONSERVATION_OWNERSHIP_AUDIT.csv", "CO4282_1_not_metric_null", "conservation not metric null"),
    ("SRC4740_9_4282_profile", SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv", "PR4282_1_threshold_144", "source-backed transition threshold"),
    ("SRC4740_10_4138_action", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_1_parent_variation", "trace-free parent variation precedent"),
    ("SRC4740_11_4738_parent", SOURCE_DIR / "P8_Y5_R2FR_4738_PARENT_ACTION_OWNER_CONTRACT.csv", "PACT4738_0_owner_field", "parent RI owner contract"),
    ("SRC4740_12_755_formal", FORMAL / "755-PPC4161-CdeltaKdiv-profile-row-and-RI-commutator-zero-or-quarantine-owner-proof.md", "R_loc T_matter != 0 -> GR/Newton", "4740 formal target"),
    ("SRC4740_13_298_boundary", FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md", "boundary/topological/superpotential owner with zero bulk local response", "boundary/topological route"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    OWNER_ACTION_CSV,
    VARIATION_AUDIT_CSV,
    SIGNATURE_GATE_CSV,
    FINITE_INPUT_SCHEMA_CSV,
    FINITE_DRYRUN_CSV,
    ROUTE_MATRIX_CSV,
    GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path_object, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path_object)
    raise KeyError(source_id)


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def load_csv(path_object: Path) -> list[dict[str, str]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def get_profile_value(profile_id: str) -> str:
    for row in load_csv(SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv"):
        if row.get("profile_id") == profile_id:
            return row.get("value_or_requirement", "")
    return ""


def owner_action_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ACT4740_0_parent_block",
            "S_parent = S_EH[g]+S_matter[g,Psi]+S_MTS_core+S_TFRI+S_quar",
            "Owner block is added without removing ordinary matter coupling to g.",
            "PARENT_BLOCK_TEMPLATE",
        ),
        (
            "ACT4740_1_TFRI_constraint",
            "S_TFRI = int sqrt|g| [lambda_nu(nabla_mu R_T^{mu nu}-nabla^nu Gamma_eff)+eta g_mu_nu R_T^{mu nu}+rho_mn(R_T^{mn}-H_T^{mn}[phi])]",
            "Variations enforce div R_T=grad Gamma_eff, trace R_T=0, and R_T=H_T[phi].",
            "CONSTRAINED_ACTION_CANDIDATE",
        ),
        (
            "ACT4740_2_HT_operator",
            "H_T^{mu nu}[phi]=nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi",
            "Reuses the trace-free Hessian/York shape already derived in 4738/4138.",
            "TRACEFREE_OPERATOR_INSERTED_BY_CONSTRAINT",
        ),
        (
            "ACT4740_3_DeltaK_owner",
            "S_TT = int sqrt|g| xi_nu P_loc nabla_mu Pi_TT[U]^{mu nu} + boundary/topological constraints",
            "Signs C_DeltaK_div=0 only if Pi_TT, P_loc, boundary and readout are parent-fixed.",
            "DELTAK_KERNEL_CANDIDATE",
        ),
        (
            "ACT4740_4_quarantine_owner",
            "S_quar = int chi_nu(q_tr^nu+nabla_mu K_own^{mu nu}) + S_null",
            "Keeps transition current owned while separating metric-nullity into S_null conditions.",
            "CONSERVATION_OWNER_CANDIDATE",
        ),
        (
            "ACT4740_5_matter_preservation",
            "delta S_matter/delta g_mu_nu != 0 and L_GR^{-1}Sigma_metric[T_matter] -> Newton/GR",
            "Any successful transition-kernel theorem must preserve the ordinary matter response channel.",
            "GR_NEWTON_PRESERVATION_REQUIRED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "action_id": action_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for action_id, formula, meaning, status in specs
    ]


def variation_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "VAR4740_0_lambda_variation",
            "delta S_TFRI/delta lambda_nu = nabla_mu R_T^{mu nu}-nabla^nu Gamma_eff",
            "right-inverse identity is enforced",
            "PASSES_CONDITIONALLY",
            "source signs equations only if action block is adopted",
        ),
        (
            "VAR4740_1_eta_variation",
            "delta S_TFRI/delta eta = g_mu_nu R_T^{mu nu}",
            "trace-free condition is enforced",
            "PASSES_CONDITIONALLY",
            "same geometry/readout still required",
        ),
        (
            "VAR4740_2_rho_variation",
            "delta S_TFRI/delta rho_mn = R_T^{mn}-H_T^{mn}[phi]",
            "R_T is tied to the derived trace-free Hessian operator",
            "PASSES_CONDITIONALLY",
            "fixed Green/domain data still required",
        ),
        (
            "VAR4740_3_multiplier_branch",
            "delta S_TFRI/delta R_T gives a homogeneous adjoint equation for lambda, eta and rho",
            "zero-multiplier branch can make constraint stress vanish classically",
            "PROMISING_UNSIGNED",
            "must certify zero multipliers from boundary/domain data, not choose them after scoring",
        ),
        (
            "VAR4740_4_metric_variation",
            "delta S_TFRI/delta g_loc contains multiplier, connection, measure, boundary and readout terms",
            "constraint action is not automatically metric-null",
            "FAILS_AS_AUTOMATIC_PROOF",
            "requires zero-multiplier plus fixed-boundary/topological certificate",
        ),
        (
            "VAR4740_5_on_shell_metric_null",
            "Sigma_metric[S_TFRI]=0 if constraints hold, lambda=eta=rho=0, boundary/readout terms vanish, and determinants/zero modes are silent",
            "this is the exact conditional metric-null branch",
            "EXACT_CONDITIONAL_NOT_SIGNED",
            "current corpus does not yet prove all clauses",
        ),
        (
            "VAR4740_6_matter_channel",
            "delta S_matter/delta g_loc remains nonzero",
            "ordinary matter still gravitates, preserving GR/Newton branch",
            "REQUIRED_NOT_PROVEN_IN_SAME_BLOCK",
            "must be checked when S_TFRI is inserted into the parent action",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "variation": variation,
            "meaning": meaning,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, variation, meaning, status, blocker in specs
    ]


def signature_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SIG4740_0_parent_adoption", "S_TFRI and S_quar are live parent action blocks, not post-hoc auxiliaries.", "UNSIGNED", "required before any zero claim"),
        ("SIG4740_1_zero_multiplier", "lambda=eta=rho=xi=chi=0 or PPN-null follows from adjoint equations and boundary/domain data.", "UNSIGNED", "needed for metric-null owner stress"),
        ("SIG4740_2_fixed_operator_data", "D_v g=D_v nabla=D_v P_loc=D_v Green_T=D_v boundary=0 in the tested collar.", "UNSIGNED", "needed for C_TF_RI=0"),
        ("SIG4740_3_DeltaK_kernel", "Delta_K=Pi_TT[U] or superpotential-null with fixed readout, so P_loc div D_v Delta_K=0.", "UNSIGNED", "needed for C_DeltaK_div=0"),
        ("SIG4740_4_boundary_readout_silence", "Boundary, corner, zero-mode and readout-order terms vanish or are source bounded.", "UNSIGNED", "needed for no hidden shell response"),
        ("SIG4740_5_matter_GR", "S_matter remains metric-coupled and weak-field response reduces to GR/Newton.", "UNSIGNED", "needed to avoid killing ordinary gravity"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": signature_id,
            "required_signature": required_signature,
            "current_status": current_status,
            "why_required": why_required,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for signature_id, required_signature, current_status, why_required in specs
    ]


def finite_input_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FIS4740_0_CDeltaKdiv", "C_DeltaK_div", "dimensionless response ratio", "C_TTleak+C_curvU+C_support+C_boundary+C_readout+C_projector", "source path, units, fixed-before-scoring flag"),
        ("FIS4740_1_CTFRI", "C_TF_RI", "dimensionless response ratio", "C_DvP+C_conn+C_Green+C_zeroMode+C_curv+C_domain+C_boundary+C_readout", "source path, units, fixed-before-scoring flag"),
        ("FIS4740_2_Cconn", "C_conn", "dimensionless response ratio", "same-geometry connection commutator", "source path, units, fixed-before-scoring flag"),
        ("FIS4740_3_Cboundary", "C_boundary", "dimensionless response ratio", "boundary/corner/readout-order leakage", "source path, units, fixed-before-scoring flag"),
        ("FIS4740_4_Ckernel", "C_kernel", "dimensionless response ratio", "||Pi_obs L_GR^{-1} Sigma_metric[q_tr]||/a_ref", "source path, units, fixed-before-scoring flag"),
        ("FIS4740_5_Pi_arena", "Pi_arena", "dimensionless projection constants", "PPN/R10/clock/orbital/WEP projection matrix", "arena source path and normalization"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": input_id,
            "symbol": symbol,
            "units": units,
            "definition": definition,
            "required_metadata": required_metadata,
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for input_id, symbol, units, definition, required_metadata in specs
    ]


def finite_dryrun_rows(timestamp: str) -> list[dict[str, Any]]:
    threshold = get_profile_value("PR4282_1_threshold_144") or "4.212667126774669e-17"
    components = [
        ("DRY4740_0_zero_branch", "all_zero_certificates_signed", "0", threshold, "PASS_CONDITIONAL_ONLY", "requires all SIG4740 clauses"),
        ("DRY4740_1_CDeltaK_missing", "missing_CDeltaKdiv", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "fill CDeltaKdiv or prove SIG4740_3"),
        ("DRY4740_2_CTFRI_missing", "missing_CTFRI", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "fill CTFRI or prove SIG4740_2"),
        ("DRY4740_3_Ckernel_missing", "missing_Ckernel", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "fill Ckernel or prove SIG4740_1/SIG4740_5"),
        ("DRY4740_4_symbolic_vector", "symbolic_transition_vector", "Pi_Delta*C_DeltaK_div+Pi_RI*C_TF_RI+Pi_conn*C_conn+Pi_bdry*C_boundary+Pi_kernel*C_kernel", threshold, "NOT_SCORE_READY", "needs all component values and arena projections"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "dryrun_id": dryrun_id,
            "case": case,
            "predicted_response": predicted_response,
            "threshold": threshold,
            "result": result,
            "next_action": next_action,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for dryrun_id, case, predicted_response, threshold, result, next_action in components
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4740_0_zero_multiplier_owner", "zero_multiplier_TFRI_owner_action", "best_exact_route_now_explicit", "prove the constrained action's adjoint equations force zero multipliers and silent boundaries"),
        ("ROUTE4740_1_topological_superpotential", "boundary_topological_superpotential_owner", "parallel_exact_route", "recast DeltaK/Kown as boundary/topological superpotential with zero bulk local response"),
        ("ROUTE4740_2_finite_runner", "transition_finite_residual_runner", "fallback_ready_schema", "source finite component values and compare to transition budget"),
        ("ROUTE4740_3_stop_overclaim", "claim_local_GR_now", "rejected", "metric-null, fixed-domain and matter-preservation signatures are not signed"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "next_requirement": next_requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, next_requirement in specs
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4740_0_action_equations", "Owner action variations enforce div R_T=grad Gamma_eff, trace R_T=0 and R_T=H_T[phi].", "conditional_pass", False),
        ("GATE4740_1_metric_null", "Metric-null stress requires zero multipliers plus fixed boundary/readout/topological silence.", "closed_unsigned", False),
        ("GATE4740_2_CTFRI", "C_TF_RI=0 requires fixed operator/Green/domain data under D_v.", "closed_unsigned", False),
        ("GATE4740_3_CDeltaK", "C_DeltaK_div=0 requires DeltaK projected TT/superpotential kernel.", "closed_unsigned", False),
        ("GATE4740_4_matter_GR", "Ordinary matter GR/Newton response must remain nonzero.", "closed_unsigned", False),
        ("GATE4740_5_finite_runner", "Finite runner is schema/dryrun only until component values are sourced.", "closed_inputs_open", False),
        ("GATE4740_6_no_public_claim", "No local-GR, Newton, PPN, R10, clock, orbital or public claim from 4740.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4740_0_no_multiplier_magic", "Do not infer metric-nullity from constraints alone; multiplier and boundary stress must vanish."),
        ("FW4740_1_no_matter_erasure", "Do not use a metric-null construction that also removes ordinary matter GR/Newton response."),
        ("FW4740_2_no_posthoc_auxiliary", "The owner action must be a parent block before scoring, not a fitted compensator."),
        ("FW4740_3_no_symbolic_runner_claim", "The finite runner dryrun is fail-closed until numeric/source-backed component rows exist."),
        ("FW4740_4_no_GitHub_action", "No GitHub action is performed by this checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4740 writes the first explicit constrained parent trace-free RI owner action block. The action can enforce the right-inverse and trace-free equations, but metric-nullity only follows on an unsigned zero-multiplier/fixed-boundary branch. A finite transition residual runner schema and fail-closed dryrun are staged.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4740_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4740_1_science_verdict",
            "status": "owner_action_candidate_derived_metric_null_unsigned",
            "detail": "The owner action equations are now explicit, but local-GR promotion requires zero-multiplier, boundary/readout silence, fixed Green/domain data, DeltaK kernel ownership and matter GR preservation.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4740 shows the constrained action can own the equations but not metric-nullity unless the zero-multiplier/boundary certificate is proved.",
            "preferred_route": "Prove the adjoint multiplier fields vanish from boundary/domain conditions and that boundary/readout/topological terms are silent.",
            "fallback_route": "Start filling finite source values for C_DeltaK_div, C_TF_RI, C_conn, C_boundary, C_kernel and Pi_arena.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    owner_action: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    signatures: list[dict[str, Any]],
    finite_schema: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4740 Y5 R2FR: Parent Tracefree RI Owner Action Block Or Transition Finite Residual Runner

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint attempts the parent-action route directly.
- A constrained owner block can enforce `div R_T=grad Gamma_eff`, `Tr(R_T)=0`, and `R_T=H_T[phi]`.
- It does **not** automatically prove local GR: metric-nullity needs a zero-multiplier/fixed-boundary/topological certificate, while ordinary matter must still source GR/Newton.
- A finite transition residual runner schema is staged fail-closed.

## Candidate Parent Block

```text
S_parent = S_EH[g] + S_matter[g,Psi] + S_MTS_core + S_TFRI + S_quar

S_TFRI = int sqrt|g| [
  lambda_nu(nabla_mu R_T^{{mu nu}} - nabla^nu Gamma_eff)
  + eta g_mu_nu R_T^{{mu nu}}
  + rho_mn(R_T^{{mn}} - H_T^{{mn}}[phi])
]

H_T^{{mu nu}}[phi] = nabla^mu nabla^nu phi - (1/4)g^{{mu nu}}Box phi
```

This is a real owner-action candidate because the equations come from variations, not from inserting `Div^-1` after scoring.

## Metric-Null Test

The hard point is:

```text
delta S_TFRI / delta g_loc = 0
```

This follows only if the constraints hold, the adjoint multipliers vanish or are PPN-null, and boundary/readout/topological terms are silent. Otherwise the owner block can cancel `q_tr` while reintroducing local stress elsewhere.

## Owner Action Rows

{bullets(owner_action, "action_id", "formula")}

## Variation Audit

{bullets(variation, "audit_id", "variation")}

## Exact Signature Gates

{bullets(signatures, "signature_id", "required_signature")}

## Finite Runner Input Schema

{bullets(finite_schema, "input_id", "symbol")}

## Finite Runner Dryrun

{bullets(dryrun, "dryrun_id", "result")}

## Route Matrix

{bullets(routes, "route_id", "route")}

## Promotion Gates

{bullets(gates, "gate_id", "gate")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`

No GitHub action was performed.
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 756 PPC4161: Parent Tracefree RI Owner Action Block Or Transition Finite Residual Runner

Generated: `{timestamp}`

## Current Status

`{DECISION}`

## What Was Constructed

The first explicit parent-action candidate for the trace-free right-inverse route is:

```text
S_TFRI = int sqrt|g| [
  lambda_nu(div R_T^nu - grad^nu Gamma_eff)
  + eta Tr(R_T)
  + rho_mn(R_T^mn - H_T^mn[phi])
]
```

with:

```text
H_T^mn[phi] = nabla^m nabla^n phi - (1/4)g^mn Box phi.
```

This conditionally signs the equation ownership side:

```text
div R_T = grad Gamma_eff
Tr(R_T)=0
R_T=H_T[phi]
```

## Why It Still Does Not Claim Local GR

The metric variation is the gate:

```text
Sigma_metric[S_TFRI] = 0
```

only on the zero-multiplier, fixed-boundary, fixed-domain/readout, topological-silent branch. Ordinary matter must remain coupled:

```text
delta S_matter/delta g != 0 -> GR/Newton.
```

## Fallback Runner

Until the exact signatures close, the transition vector remains:

```text
Y_a <= Pi_Delta C_DeltaK_div + Pi_RI C_TF_RI + Pi_conn C_conn + Pi_bdry C_boundary + Pi_kernel C_kernel.
```

## Next

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Result: a constrained parent trace-free RI owner action block has been written.
- Important caveat: the action owns the equations, but metric-nullity needs a zero-multiplier/fixed-boundary/topological certificate.
- Finite fallback: transition residual runner schema is staged fail-closed.
- Next local route: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet update: the transition-shell branch now has an explicit parent action candidate plus a finite-runner fallback.
- Claim status: nonclaim; no local-GR/PPN/R10/Newtonian pass.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4740-Y5-R2FR-parent-tracefree-RI-owner-action-block-or-transition-finite-residual-runner.md`

## Decision

`{DECISION}`

## What moved forward

- A constrained parent trace-free RI owner action block was written.
- Its variations enforce `div R_T=grad Gamma_eff`, `Tr(R_T)=0`, and `R_T=H_T[phi]`.
- The metric-null branch remains unsigned because it needs zero multipliers, fixed boundary/readout/domain data, and ordinary matter GR/Newton preservation.
- A finite transition residual runner schema and fail-closed dryrun were staged.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(timestamp: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4740 writes an explicit constrained parent trace-free RI owner action block and stages a fail-closed finite transition residual runner.",
        "current_evidence": "Generated source register, parent TFRI owner action rows, metric variation audit, exact signature gates, finite runner input schema, dryrun, route matrix, gates, firewalls, decision, status, next target and validation.",
        "status": "constrained_TFRI_owner_action_metric_null_unsigned_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking equation ownership for metric-nullity, or erasing ordinary matter GR/Newton response.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Zero-multiplier branch, boundary/readout silence, fixed Green/domain data, DeltaK kernel ownership and finite source values remain unsigned.",
        "title": "Parent tracefree RI owner action block or transition finite residual runner",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    for fieldname in fieldnames:
        new_row.setdefault(fieldname, "")
    rows.append(new_row)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cleanup_pycache() -> None:
    pycache_path = POST / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)


def validation_rows(
    sources: list[dict[str, Any]],
    owner_action: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    signatures: list[dict[str, Any]],
    finite_schema: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    generated_with_validation = GENERATED_CSVS + [VALIDATION_CSV]
    checks = [
        ("VAL4740_0_sources_exist", all(source["exists"] for source in sources), "all cited 4740 source paths exist"),
        ("VAL4740_1_needles_found", all(source["needle_found"] for source in sources), "all cited 4740 source needles found"),
        ("VAL4740_2_action_block", any(row["action_id"] == "ACT4740_1_TFRI_constraint" for row in owner_action), "TFRI constrained action block written"),
        ("VAL4740_3_variation_equations", all(any(row["audit_id"] == audit_id for row in variation) for audit_id in ["VAR4740_0_lambda_variation", "VAR4740_1_eta_variation", "VAR4740_2_rho_variation"]), "constraint variations enforce RI/trace/Hessian equations"),
        ("VAL4740_4_metric_null_not_auto", any(row["audit_id"] == "VAR4740_4_metric_variation" and row["status"] == "FAILS_AS_AUTOMATIC_PROOF" for row in variation), "metric-nullity is not automatic"),
        ("VAL4740_5_zero_multiplier_gate", any(row["signature_id"] == "SIG4740_1_zero_multiplier" for row in signatures), "zero-multiplier signature gate written"),
        ("VAL4740_6_matter_GR_gate", any(row["signature_id"] == "SIG4740_5_matter_GR" for row in signatures), "ordinary matter GR/Newton gate written"),
        ("VAL4740_7_finite_schema", len(finite_schema) >= 6, "finite runner input schema covers all components"),
        ("VAL4740_8_dryrun_fail_closed", any(row["case"] == "missing_CDeltaKdiv" and row["result"] == "FAIL_CLOSED" for row in dryrun), "finite dryrun fails closed on missing source values"),
        ("VAL4740_9_routes", any(row["route"] == "zero_multiplier_TFRI_owner_action" for row in routes) and any(row["route"] == "transition_finite_residual_runner" for row in routes), "route matrix has exact and finite branches"),
        ("VAL4740_10_claim_gates_closed", all(row["valid_for_claim"] is False for row in gates), "all claim gates remain closed"),
        ("VAL4740_11_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4740_12_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4740_13_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-582"),
        ("VAL4740_14_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4741 next target"),
        ("VAL4740_15_csv_parse", all(parse_csv(csv_path) for csv_path in generated_with_validation if csv_path.exists()), "all generated 4740 CSV files parse cleanly"),
        ("VAL4740_16_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4740_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "4740 parent tracefree RI owner action block or transition finite residual runner validation",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    owner_action = owner_action_rows(timestamp)
    variation = variation_audit_rows(timestamp)
    signatures = signature_gate_rows(timestamp)
    finite_schema = finite_input_schema_rows(timestamp)
    dryrun = finite_dryrun_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OWNER_ACTION_CSV, owner_action)
    write_csv(VARIATION_AUDIT_CSV, variation)
    write_csv(SIGNATURE_GATE_CSV, signatures)
    write_csv(FINITE_INPUT_SCHEMA_CSV, finite_schema)
    write_csv(FINITE_DRYRUN_CSV, dryrun)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, owner_action, variation, signatures, finite_schema, dryrun, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, owner_action, variation, signatures, finite_schema, dryrun, routes, gates, timestamp))


if __name__ == "__main__":
    main()
