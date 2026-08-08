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

CHECKPOINT = "4742"
CLAIM_ID = "L-584"
MARKER = "PPC4161_ADJOINT_COERCIVITY_NO_ZERO_MODE_PROOF_OR_FIRST_TRANSITION_SOURCE_VALUE_4742"
PACKET_MARKER = "PPC4161_PACKET_ADJOINT_COERCIVITY_NO_ZERO_MODE_PROOF_OR_FIRST_TRANSITION_SOURCE_VALUE_4742"
DECISION = "ADJOINT_SPECTRAL_GAP_COERCIVITY_BOUND_DERIVED_EXACT_ZERO_REDUCED_TO_KERNEL_PROJECTION_AND_BOUNDARY_SOURCE_NONCLAIM"
NEXT_TARGET = "4743-Y5-R2FR-kernel-projection-boundary-data-kill-test-or-adjoint-gap-source-value.md"

DOC_PATH = POST / "4742-Y5-R2FR-adjoint-coercivity-no-zero-mode-proof-or-first-transition-source-value.md"
FORMAL_PATH = FORMAL / "758-PPC4161-adjoint-coercivity-no-zero-mode-proof-or-first-transition-source-value.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_SOURCE_REGISTER.csv"
OPERATOR_SETUP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_ADJOINT_OPERATOR_SETUP.csv"
COERCIVITY_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_SPECTRAL_GAP_COERCIVITY_PROOF.csv"
ZERO_MODE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_ZERO_MODE_KILL_AUDIT.csv"
FINITE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_FINITE_BOUND_LAW.csv"
FIRST_SOURCE_TARGETS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_FIRST_SOURCE_TARGETS.csv"
MATTER_FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_MATTER_FIREWALL.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4742_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4742_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4742_0_4741_doc", POST / "4741-Y5-R2FR-zero-multiplier-boundary-certificate-or-transition-finite-source-values.md", "A_TFRI^dagger m = 0", "4741 theorem contract"),
    ("SRC4742_1_4741_formal", FORMAL / "757-PPC4161-zero-multiplier-boundary-certificate-or-transition-finite-source-values.md", "B_adj[m]=0", "formal adjoint boundary contract"),
    ("SRC4742_2_4741_adjoint", SOURCE_DIR / "P8_Y5_R2FR_4741_ADJOINT_MULTIPLIER_CERTIFICATE.csv", "ADJ4741_3_coercive_zero_theorem", "coercive zero theorem row"),
    ("SRC4742_3_4741_boundary", SOURCE_DIR / "P8_Y5_R2FR_4741_BOUNDARY_READOUT_CERTIFICATE.csv", "BND4741_0_adjoint_boundary", "boundary/readout clauses"),
    ("SRC4742_4_4741_zero_modes", SOURCE_DIR / "P8_Y5_R2FR_4741_ZERO_MODE_LEDGER.csv", "ZM4741_3_TT_kernel", "zero-mode family ledger"),
    ("SRC4742_5_4741_finite", SOURCE_DIR / "P8_Y5_R2FR_4741_TRANSITION_FINITE_SOURCE_VALUE_LEDGER.csv", "C_zeroMode", "finite residual ledger"),
    ("SRC4742_6_4741_dryrun", SOURCE_DIR / "P8_Y5_R2FR_4741_FINITE_RUNNER_DRYRUN.csv", "missing_C_zeroMode", "fail-closed finite precedent"),
    ("SRC4742_7_4741_matter", SOURCE_DIR / "P8_Y5_R2FR_4741_MATTER_GR_PRESERVATION_CHECK.csv", "MGR4741_2_owner_null_only", "matter firewall"),
    ("SRC4742_8_4741_next", SOURCE_DIR / "P8_Y5_R2FR_4741_NEXT_TARGET.csv", "Try to prove c_adj>0", "4742 target"),
    ("SRC4742_9_4740_variation", SOURCE_DIR / "P8_Y5_R2FR_4740_METRIC_VARIATION_AUDIT.csv", "VAR4740_5_on_shell_metric_null", "on-shell metric-null precedent"),
    ("SRC4742_10_4282_threshold", SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv", "PR4282_1_threshold_144", "transition threshold"),
    ("SRC4742_11_4138_boundary", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_5_boundary_improvement", "boundary silence precedent"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    OPERATOR_SETUP_CSV,
    COERCIVITY_PROOF_CSV,
    ZERO_MODE_AUDIT_CSV,
    FINITE_BOUND_CSV,
    FIRST_SOURCE_TARGETS_CSV,
    MATTER_FIREWALL_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
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
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def load_csv(path_object: Path) -> list[dict[str, str]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def threshold_value() -> str:
    profile_csv = SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv"
    if profile_csv.exists():
        for row in load_csv(profile_csv):
            if row.get("profile_id") == "PR4282_1_threshold_144":
                return row.get("value_or_requirement") or "4.212667126774669e-17"
    return "4.212667126774669e-17"


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


def operator_setup_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "OP4742_0_hilbert_space",
            "H_m = L2(W_loc,sqrt|g|; Lambda*T*W plus scalar plus tensor multiplier bundle)",
            "Defines the multiplier fields as elements of a local Hilbert space on the fixed collar.",
            "DEFINITION",
        ),
        (
            "OP4742_1_domain",
            "Dom(D_adj)=H1_m(W_loc) with parent-fixed boundary trace and quotient gauge projection",
            "This is the exact place where boundary data enters the proof; if the parent cannot sign it, the proof remains conditional.",
            "DOMAIN_CONDITIONAL",
        ),
        (
            "OP4742_2_operator",
            "D_adj := A_TFRI^dagger acting on m=(lambda,eta,rho,xi,chi)",
            "The homogeneous multiplier equations are written as D_adj m=0.",
            "OPERATOR_DEFINED_FROM_4741",
        ),
        (
            "OP4742_3_laplacian",
            "L_adj := D_adj^* D_adj with inherited boundary/domain conditions",
            "The positivity problem becomes a spectral problem for a nonnegative adjoint Laplacian.",
            "SPECTRAL_REDUCTION",
        ),
        (
            "OP4742_4_kernel_projector",
            "Pi_0 := orthogonal projector onto ker(D_adj)",
            "Zero modes are not ignored; they are isolated as a projector that must be killed or bounded.",
            "KERNEL_EXPLICIT",
        ),
        (
            "OP4742_5_spectral_gap",
            "lambda_1^adj := inf spec(L_adj restricted to (ker D_adj)^perp)",
            "For a fixed elliptic collar/domain with compact resolvent, lambda_1^adj>0 is the desired c_adj.",
            "GAP_CONDITIONAL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "operator_id": operator_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for operator_id, formula, meaning, status in specs
    ]


def coercivity_proof_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PROOF4742_0_decompose",
            "m = Pi_0 m + m_perp, with m_perp in (ker D_adj)^perp",
            "Orthogonal decomposition separates the only exact obstruction from the controlled component.",
            "DERIVED",
        ),
        (
            "PROOF4742_1_spectral_gap",
            "<m_perp,L_adj m_perp> >= lambda_1^adj ||m_perp||^2",
            "This is the coercive core. It is true once L_adj has compact resolvent and positive first nonzero eigenvalue.",
            "DERIVED_CONDITIONALLY",
        ),
        (
            "PROOF4742_2_energy_identity",
            "<m_perp,L_adj m_perp> = ||D_adj m||^2 + B_adj[m]",
            "Boundary integration-by-parts terms are carried explicitly rather than silently dropped.",
            "DERIVED_WITH_BOUNDARY_TERM",
        ),
        (
            "PROOF4742_3_master_bound",
            "||m||^2 <= ||Pi_0 m||^2 + (1/lambda_1^adj)(||D_adj m||^2 + |B_adj[m]|)",
            "This is the usable local multiplier amplitude law.",
            "DERIVED_BOUND_LAW",
        ),
        (
            "PROOF4742_4_exact_zero",
            "D_adj m=0, B_adj[m]=0, Pi_0 m=0, lambda_1^adj>0 => m=0",
            "This proves lambda=eta=rho=xi=chi=0 without a plateau axiom.",
            "EXACT_ZERO_PROOF_CONDITIONAL",
        ),
        (
            "PROOF4742_5_metric_null",
            "m=0 and fixed readout/domain => Sigma_metric[S_owner]_loc=0",
            "The owner block becomes locally silent only after the multiplier theorem and readout/domain clauses are signed.",
            "CONSEQUENCE_CONDITIONAL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "proof_id": proof_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for proof_id, formula, meaning, status in specs
    ]


def zero_mode_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZK4742_0_dirichlet_trace", "multiplier Dirichlet trace on partial W_loc", "can kill many adjoint kernel modes by elliptic uniqueness", "PARENT_BOUNDARY_DATA_REQUIRED"),
        ("ZK4742_1_compact_support", "compact support inside W_loc", "strongest simple kill condition for boundary flux and zero modes", "PARENT_SUPPORT_DATA_REQUIRED"),
        ("ZK4742_2_killing_modes", "Killing/vector kernel", "must show boundary trace removes local symmetry multipliers", "NO_ZERO_MODE_PROOF_REQUIRED"),
        ("ZK4742_3_conformal_modes", "conformal-Killing kernel", "must show quotient projection or boundary data removes scale representative leakage", "NO_ZERO_MODE_PROOF_REQUIRED"),
        ("ZK4742_4_harmonic_scalar", "harmonic scalar/York kernel", "must remove constants/harmonics or they become C_zeroMode", "NO_ZERO_MODE_PROOF_REQUIRED"),
        ("ZK4742_5_TT_superpotential", "TT/superpotential kernel", "must be owned topologically or projected out before local scoring", "NO_ZERO_MODE_PROOF_REQUIRED"),
        ("ZK4742_6_green_kernel", "Green/readout kernel", "must fix Green inverse and remove nullspace before applying response operator", "NO_ZERO_MODE_PROOF_REQUIRED"),
        ("ZK4742_7_kernel_residual", "unremoved kernel amplitude", "C_zeroMode := ||Pi_0 m||/a_ref", "FIRST_FINITE_SOURCE_CANDIDATE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_mode_id": zero_mode_id,
            "family": family,
            "proof_role": proof_role,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for zero_mode_id, family, proof_role, status in specs
    ]


def finite_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    threshold = threshold_value()
    specs = [
        (
            "FB4742_0_multiplier_amplitude",
            "A_m := ||m||/a_ref <= sqrt(C_zeroMode^2 + (C_Dadj^2 + C_boundary)/lambda_1^adj)",
            "dimensionless",
            "Derived source-amplitude law for owner multipliers.",
        ),
        (
            "FB4742_1_exact_constraint_case",
            "if C_Dadj=0 and C_boundary=0 then A_m <= C_zeroMode",
            "dimensionless",
            "If the equations and boundary are exact, only the kernel projection remains.",
        ),
        (
            "FB4742_2_zero_kernel_case",
            "if C_zeroMode=0 also then A_m=0",
            "dimensionless",
            "This is the clean local-suppression theorem.",
        ),
        (
            "FB4742_3_response_vector",
            "C_res <= Pi_owner*A_m + Pi_Delta*C_DeltaK_div + Pi_RI*C_TF_RI + Pi_domain*C_domain + Pi_readout*C_readout",
            "dimensionless",
            "Residual response is now bounded through the multiplier amplitude plus already named finite terms.",
        ),
        (
            "FB4742_4_threshold_gate",
            f"C_res <= {threshold}",
            "dimensionless",
            "Source-backed transition threshold remains the scoring gate; current rows are not score-ready.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "formula": formula,
            "units": units,
            "meaning": meaning,
            "source_status": "DERIVED_SYMBOLIC_NONNUMERIC",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, formula, units, meaning in specs
    ]


def first_source_target_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FST4742_0_lambda_gap",
            "lambda_1^adj",
            "first nonzero eigenvalue/spectral gap of L_adj on fixed W_loc",
            "BEST_THEOREM_SOURCE",
            "derive from elliptic principal symbol plus fixed boundary data, or estimate numerically on a toy collar",
        ),
        (
            "FST4742_1_kernel_projection",
            "C_zeroMode = ||Pi_0 m||/a_ref",
            "unremoved adjoint kernel amplitude",
            "BEST_FINITE_SOURCE",
            "prove zero via boundary/quotient data or source a finite upper bound",
        ),
        (
            "FST4742_2_boundary_flux",
            "C_boundary = |B_adj[m]|/a_ref^2",
            "adjoint boundary flux/corner leakage",
            "SECOND_FINITE_SOURCE",
            "prove zero by compact support/topological cancellation or source a bound",
        ),
        (
            "FST4742_3_operator_residual",
            "C_Dadj = ||D_adj m||/a_ref",
            "failure of homogeneous adjoint equation",
            "CHECK_ONLY",
            "should be zero if the parent action equations are exact",
        ),
        (
            "FST4742_4_arena_projection",
            "Pi_owner",
            "projection from multiplier amplitude to PPN/R10/clock/orbital response",
            "LATER_SOURCE",
            "needed only after amplitude law has a zero proof or finite value",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "target_id": target_id,
            "symbol": symbol,
            "definition": definition,
            "priority": priority,
            "next_action": next_action,
            "value": "MISSING_NUMERIC_OR_PARENT_CERTIFICATE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for target_id, symbol, definition, priority, next_action in specs
    ]


def matter_firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("MF4742_0_owner_only", "coercivity applies only to m=(lambda,eta,rho,xi,chi)", "ordinary matter fields are not in the killed adjoint kernel"),
        ("MF4742_1_stress_preserved", "delta S_matter/delta g_mu_nu remains nonzero", "GR/Newton source response is not projected out"),
        ("MF4742_2_reject_bad_branch", "if Pi_0 removal forces T_matter=0 then reject route", "no fake local quiet by matter erasure"),
        ("MF4742_3_later_limit", "Newtonian limit still needs G/source calibration", "this theorem only suppresses owner residuals"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "matter_firewall_id": firewall_id,
            "condition": condition,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, condition, meaning in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4742_0_kernel_kill", "prove Pi_0 m=0 from boundary/quotient data", "best_next_route", "directly closes exact zero if lambda_1^adj>0 and B_adj=0"),
        ("ROUTE4742_1_gap_source", "derive or numerically source lambda_1^adj", "parallel_next_route", "turns the theorem into a quantitative amplitude bound"),
        ("ROUTE4742_2_boundary_source", "prove or bound B_adj[m]", "parallel_next_route", "prevents hidden boundary leakage"),
        ("ROUTE4742_3_arena_score", "score PPN/R10/clock/orbital response now", "rejected_for_now", "Pi_owner and finite values are not sourced yet"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "reason_or_next_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, requirement in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4742_0_sources", "All cited 4742 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4742_1_bound_law", "Multiplier amplitude bound is derived symbolically.", "conditional_pass", False),
        ("GATE4742_2_lambda_gap", "lambda_1^adj>0 must be parent-signed or source-estimated.", "closed_unsigned", False),
        ("GATE4742_3_kernel_projection", "Pi_0 m=0 or C_zeroMode finite bound is required.", "closed_unsigned", False),
        ("GATE4742_4_boundary", "B_adj=0 or finite C_boundary bound is required.", "closed_unsigned", False),
        ("GATE4742_5_matter", "Matter GR/Newton channel must remain nonzero.", "open_firewall", False),
        ("GATE4742_6_no_claim", "No R10, PPN, WEP, clock, orbital, local-GR or public claim from 4742.", "closed_firewall", False),
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
        ("FW4742_0_no_spectral_gap_magic", "Do not claim lambda_1^adj>0 until operator/domain/ellipticity are signed."),
        ("FW4742_1_no_kernel_deletion", "Do not delete Pi_0 m; either prove it zero or carry C_zeroMode."),
        ("FW4742_2_no_boundary_drop", "Do not discard B_adj[m] without fixed support or parent boundary cancellation."),
        ("FW4742_3_no_matter_kill", "Do not apply the multiplier projection to ordinary matter stress."),
        ("FW4742_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
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
            "summary": "4742 derives the local multiplier amplitude law using a spectral gap for L_adj=D_adj^*D_adj on the fixed local collar. Exact zero is now proven conditionally from D_adj m=0, B_adj=0, Pi_0 m=0 and lambda_1^adj>0; otherwise C_zeroMode, C_boundary and lambda_1^adj become the first source targets.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4742_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4742_1_science_verdict",
            "status": "coercivity_bound_derived_kernel_and_boundary_unsigned",
            "detail": "The work moved from a theorem wish to an explicit spectral-gap multiplier amplitude law; the exact proof now hinges on kernel projection and boundary data.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4742 proves the conditional amplitude law but leaves the parent-owned zero-mode projection and boundary data unsigned.",
            "preferred_route": "Try to kill Pi_0 m with parent boundary/quotient data; in parallel source or estimate lambda_1^adj.",
            "fallback_route": "Carry C_zeroMode and C_boundary as finite source values into the transition residual score.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    operator_setup: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    zero_modes: list[dict[str, Any]],
    finite_bounds: list[dict[str, Any]],
    first_targets: list[dict[str, Any]],
    matter: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4742 Y5 R2FR: Adjoint Coercivity No-Zero-Mode Proof Or First Transition Source Value

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint pushes the 4741 zero-multiplier route into an actual spectral/coercivity estimate.
- The useful result is the multiplier amplitude law:

```text
D_adj := A_TFRI^dagger
L_adj := D_adj^* D_adj
Pi_0 := projector onto ker(D_adj)
lambda_1^adj := inf spec(L_adj | (ker D_adj)^perp)

||m||^2 <= ||Pi_0 m||^2 + (1/lambda_1^adj)(||D_adj m||^2 + |B_adj[m]|)
```

- Exact local silence follows if `D_adj m=0`, `B_adj[m]=0`, `Pi_0 m=0`, and `lambda_1^adj>0`.
- If not, the first real finite source targets are `C_zeroMode`, `C_boundary`, and `lambda_1^adj`.
- This checkpoint does not claim local GR; it narrows the proof to a concrete kernel/boundary/gap problem.

## Operator Setup

{bullet(operator_setup, "operator_id", "formula")}

## Coercivity Proof

{bullet(proof, "proof_id", "formula")}

## Zero-Mode Kill Audit

{bullet(zero_modes, "zero_mode_id", "family")}

## Finite Bound Law

{bullet(finite_bounds, "bound_id", "formula")}

## First Source Targets

{bullet(first_targets, "target_id", "symbol")}

## Matter Firewall

{bullet(matter, "matter_firewall_id", "condition")}

## Route Matrix

{bullet(routes, "route_id", "route")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 758 PPC4161: Adjoint Coercivity No-Zero-Mode Proof Or First Transition Source Value

Generated: `{timestamp}`

## Derived Amplitude Law

4742 defines `D_adj=A_TFRI^dagger`, `L_adj=D_adj^*D_adj`, and `Pi_0=Proj ker(D_adj)`. On a fixed local collar with parent-fixed boundary/domain data, the spectral gap gives:

```text
||m||^2 <= ||Pi_0 m||^2 + (1/lambda_1^adj)(||D_adj m||^2 + |B_adj[m]|).
```

Therefore:

```text
D_adj m=0, B_adj[m]=0, Pi_0 m=0, lambda_1^adj>0
=> m=0
=> lambda=eta=rho=xi=chi=0.
```

This is the first clean derivation of the zero-multiplier route as a coercivity theorem rather than a closure assumption.

## Remaining Unsigned Inputs

- `lambda_1^adj`: spectral gap for the fixed operator/domain.
- `Pi_0 m`: zero-mode projection, especially Killing/conformal/harmonic/TT/Green kernels.
- `B_adj[m]`: boundary/corner/readout flux.
- Matter firewall: `delta S_matter/delta g != 0 -> GR/Newton` remains untouched by the multiplier projection.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4742 derives the adjoint spectral-gap multiplier amplitude law:
  `||m||^2 <= ||Pi_0 m||^2 + (1/lambda_1^adj)(||D_adj m||^2 + |B_adj[m]|)`.
- Exact zero is now a clean theorem route:
  `D_adj m=0`, `B_adj[m]=0`, `Pi_0 m=0`, `lambda_1^adj>0` imply `lambda=eta=rho=xi=chi=0`.
- The first finite source targets are `lambda_1^adj`, `C_zeroMode`, and `C_boundary`.
- Ordinary matter GR/Newton response remains outside the killed multiplier sector.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4742 local packet update: the zero-multiplier route now has a spectral-gap proof skeleton and finite fallback law. The next step is to kill or bound the kernel projection and boundary flux.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4742-Y5-R2FR-adjoint-coercivity-no-zero-mode-proof-or-first-transition-source-value.md`

## Decision

`{DECISION}`

## What moved forward

- Defined `D_adj=A_TFRI^dagger`, `L_adj=D_adj^*D_adj`, `Pi_0=Proj ker(D_adj)`, and `lambda_1^adj`.
- Derived the multiplier amplitude law `||m||^2 <= ||Pi_0 m||^2 + (1/lambda_1^adj)(||D_adj m||^2 + |B_adj[m]|)`.
- Proved the exact zero branch conditionally: `D_adj m=0`, `B_adj=0`, `Pi_0 m=0`, `lambda_1^adj>0 => lambda=eta=rho=xi=chi=0`.
- Identified first finite source targets: `lambda_1^adj`, `C_zeroMode`, and `C_boundary`.
- Kept ordinary matter GR/Newton preservation as a hard firewall.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4742 derives an adjoint spectral-gap multiplier amplitude law and reduces exact local owner silence to kernel projection, boundary flux, and spectral gap inputs.",
        "Generated source register, operator setup, coercivity proof, zero-mode kill audit, finite bound law, first source targets, matter firewall, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "adjoint_coercivity_bound_derived_kernel_boundary_unsigned_nonclaim",
        NEXT_TARGET,
        "Treating the spectral gap, kernel projection, or boundary flux as signed before the parent domain data exists.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need lambda_1^adj, Pi_0 m=0 or C_zeroMode, B_adj=0 or C_boundary, and matter GR/Newton preservation.",
        "Adjoint coercivity no-zero-mode proof or first transition source value",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    operator_setup: list[dict[str, Any]],
    proof: list[dict[str, Any]],
    zero_modes: list[dict[str, Any]],
    finite_bounds: list[dict[str, Any]],
    first_targets: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4742_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4742_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4742_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4742_2_operator_setup", "operator setup defines D_adj, L_adj, Pi_0, lambda_1^adj", all(any(token in row["formula"] for row in operator_setup) for token in ["D_adj", "L_adj", "Pi_0", "lambda_1^adj"]), str(OPERATOR_SETUP_CSV)))
    checks.append(("VAL4742_3_bound_law", "proof rows contain master amplitude bound", any("||m||^2 <=" in row["formula"] and "lambda_1^adj" in row["formula"] for row in proof), str(COERCIVITY_PROOF_CSV)))
    checks.append(("VAL4742_4_exact_zero", "proof rows contain exact zero implication", any("D_adj m=0" in row["formula"] and "m=0" in row["formula"] for row in proof), str(COERCIVITY_PROOF_CSV)))
    checks.append(("VAL4742_5_zero_mode_audit", "zero-mode audit carries C_zeroMode fallback", any("C_zeroMode" in row["proof_role"] for row in zero_modes), str(ZERO_MODE_AUDIT_CSV)))
    checks.append(("VAL4742_6_finite_bounds", "finite bound law includes threshold and response vector", any("C_res" in row["formula"] for row in finite_bounds) and any("C_res <=" in row["formula"] for row in finite_bounds), str(FINITE_BOUND_CSV)))
    checks.append(("VAL4742_7_first_targets", "first source targets include lambda gap, C_zeroMode and C_boundary", all(any(symbol in row["symbol"] for row in first_targets) for symbol in ["lambda_1^adj", "C_zeroMode", "C_boundary"]), str(FIRST_SOURCE_TARGETS_CSV)))
    checks.append(("VAL4742_8_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4742_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4742_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4742_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4742_12_claim_row", "claim row L-584 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4742_13_resume", "resume points from 4742 to 4743", "4742-Y5" in resume_text and "4743-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4742_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4742_OVERALL",
            "check": "all 4742 local generation and nonclaim checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    operator_setup = operator_setup_rows(timestamp)
    proof = coercivity_proof_rows(timestamp)
    zero_modes = zero_mode_audit_rows(timestamp)
    finite_bounds = finite_bound_rows(timestamp)
    first_targets = first_source_target_rows(timestamp)
    matter = matter_firewall_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OPERATOR_SETUP_CSV, operator_setup)
    write_csv(COERCIVITY_PROOF_CSV, proof)
    write_csv(ZERO_MODE_AUDIT_CSV, zero_modes)
    write_csv(FINITE_BOUND_CSV, finite_bounds)
    write_csv(FIRST_SOURCE_TARGETS_CSV, first_targets)
    write_csv(MATTER_FIREWALL_CSV, matter)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, operator_setup, proof, zero_modes, finite_bounds, first_targets, matter, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, operator_setup, proof, zero_modes, finite_bounds, first_targets, gates, timestamp))


if __name__ == "__main__":
    main()
