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

CHECKPOINT = "4741"
CLAIM_ID = "L-583"
MARKER = "PPC4161_ZERO_MULTIPLIER_BOUNDARY_CERTIFICATE_OR_TRANSITION_FINITE_SOURCE_VALUES_4741"
PACKET_MARKER = "PPC4161_PACKET_ZERO_MULTIPLIER_BOUNDARY_CERTIFICATE_OR_TRANSITION_FINITE_SOURCE_VALUES_4741"
DECISION = "ZERO_MULTIPLIER_CERTIFICATE_REDUCED_TO_ADJOINT_COERCIVITY_NO_ZERO_MODE_AND_BOUNDARY_SILENCE_FINITE_SOURCE_VALUES_STAGED_NONCLAIM"
NEXT_TARGET = "4742-Y5-R2FR-adjoint-coercivity-no-zero-mode-proof-or-first-transition-source-value.md"

DOC_PATH = POST / "4741-Y5-R2FR-zero-multiplier-boundary-certificate-or-transition-finite-source-values.md"
FORMAL_PATH = FORMAL / "757-PPC4161-zero-multiplier-boundary-certificate-or-transition-finite-source-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_SOURCE_REGISTER.csv"
ADJOINT_CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_ADJOINT_MULTIPLIER_CERTIFICATE.csv"
BOUNDARY_CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_BOUNDARY_READOUT_CERTIFICATE.csv"
ZERO_MODE_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_ZERO_MODE_LEDGER.csv"
MATTER_GR_CHECK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_MATTER_GR_PRESERVATION_CHECK.csv"
FINITE_SOURCE_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_TRANSITION_FINITE_SOURCE_VALUE_LEDGER.csv"
FINITE_DRYRUN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_FINITE_RUNNER_DRYRUN.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4741_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4741_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4741_0_4740_doc", POST / "4740-Y5-R2FR-parent-tracefree-RI-owner-action-block-or-transition-finite-residual-runner.md", "zero-multiplier/fixed-boundary/topological certificate", "4740 zero-branch handoff"),
    ("SRC4741_1_4740_formal", FORMAL / "756-PPC4161-parent-tracefree-RI-owner-action-block-or-transition-finite-residual-runner.md", "delta S_matter/delta g != 0 -> GR/Newton", "formal matter preservation anchor"),
    ("SRC4741_2_4740_action", SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv", "S_TFRI = int sqrt|g|", "parent constrained action"),
    ("SRC4741_3_4740_variation", SOURCE_DIR / "P8_Y5_R2FR_4740_METRIC_VARIATION_AUDIT.csv", "VAR4740_5_on_shell_metric_null", "metric-null audit"),
    ("SRC4741_4_4740_signatures", SOURCE_DIR / "P8_Y5_R2FR_4740_EXACT_SIGNATURE_GATES.csv", "lambda=eta=rho=xi=chi=0", "zero-multiplier gate"),
    ("SRC4741_5_4740_schema", SOURCE_DIR / "P8_Y5_R2FR_4740_TRANSITION_FINITE_RUNNER_INPUT_SCHEMA.csv", "C_DeltaK_div", "finite residual schema"),
    ("SRC4741_6_4740_dryrun", SOURCE_DIR / "P8_Y5_R2FR_4740_TRANSITION_FINITE_RUNNER_DRYRUN.csv", "MISSING_SOURCE_VALUE", "fail-closed dryrun precedent"),
    ("SRC4741_7_4740_next", SOURCE_DIR / "P8_Y5_R2FR_4740_NEXT_TARGET.csv", "Prove the adjoint multiplier fields vanish", "4741 target"),
    ("SRC4741_8_4739_matter", SOURCE_DIR / "P8_Y5_R2FR_4739_ORDINARY_MATTER_GR_PRESERVATION_GATE.csv", "MGR4739_2_transition_null_only", "ordinary matter channel"),
    ("SRC4741_9_4282_metric_null", SOURCE_DIR / "P8_Y5_R2FR_4282_METRIC_NULL_ACTION_CONTRACT.csv", "MN4282_1", "metric-null contract"),
    ("SRC4741_10_4282_threshold", SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv", "PR4282_1_threshold_144", "transition threshold"),
    ("SRC4741_11_4138_boundary", SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv", "TF4138_5_boundary_improvement", "boundary/collar silence precedent"),
    ("SRC4741_12_4739_formal", FORMAL / "755-PPC4161-CdeltaKdiv-profile-row-and-RI-commutator-zero-or-quarantine-owner-proof.md", "R_loc T_matter != 0 -> GR/Newton", "ordinary matter nonzero formal clause"),
    ("SRC4741_13_298_boundary", FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md", "boundary/topological/superpotential owner with zero bulk local response", "boundary/topological route"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    ADJOINT_CERTIFICATE_CSV,
    BOUNDARY_CERTIFICATE_CSV,
    ZERO_MODE_LEDGER_CSV,
    MATTER_GR_CHECK_CSV,
    FINITE_SOURCE_LEDGER_CSV,
    FINITE_DRYRUN_CSV,
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


def get_threshold() -> str:
    source_path = SOURCE_DIR / "P8_Y5_R2FR_4282_SHELL_PROFILE_SOURCE_ROWS.csv"
    if source_path.exists():
        for row in load_csv(source_path):
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


def adjoint_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ADJ4741_0_multiplier_vector",
            "m=(lambda,eta,rho,xi,chi)",
            "Collects every transition-owner Lagrange multiplier or adjoint field into one multiplier vector.",
            "DEFINED",
            "not a claim; notation only",
        ),
        (
            "ADJ4741_1_homogeneous_adjoint_equation",
            "A_TFRI^dagger m = 0 on the local collar W_loc",
            "Once the constraint equations hold, the remaining owner-field variations must be homogeneous adjoint equations for m.",
            "DERIVED_CONDITIONALLY",
            "requires parent action and fixed local collar/domain",
        ),
        (
            "ADJ4741_2_energy_identity",
            "int_W <m,A_TFRI A_TFRI^dagger m> = ||A_TFRI^dagger m||^2 + B_adj[m]",
            "The zero proof should use a positive adjoint energy identity, not a hand-inserted plateau axiom.",
            "PROOF_ROUTE_EXPLICIT",
            "coercivity constant and boundary term remain unsigned",
        ),
        (
            "ADJ4741_3_coercive_zero_theorem",
            "if c_adj||m||^2 <= ||A_TFRI^dagger m||^2 + B_adj[m] and B_adj[m]=0 and Pi_zero m=0, then lambda=eta=rho=xi=chi=0",
            "This is the exact local suppression law: zero multipliers follow from coercivity, boundary silence, and no zero modes.",
            "THEOREM_CONDITIONAL_UNSIGNED",
            "needs c_adj>0, B_adj=0, and no-zero-mode certificate",
        ),
        (
            "ADJ4741_4_metric_null_consequence",
            "lambda=eta=rho=xi=chi=0 => Sigma_metric[S_TFRI+S_TT+S_quar]_loc = 0",
            "If the theorem is signed, transition ownership can be metric-null while ordinary matter remains GR-coupled.",
            "CONSEQUENCE_CONDITIONAL_UNSIGNED",
            "does not claim local GR until matter and domain gates pass",
        ),
        (
            "ADJ4741_5_unsigned_obstruction",
            "C_zeroMode + C_boundary + C_domain + C_readout + C_kernel remain as residual owners if any theorem clause fails",
            "Failure is no longer vague: it becomes a finite residual vector with named components.",
            "FINITE_FALLBACK_STAGED",
            "requires sourced numeric or theorem values before scoring",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": certificate_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "blocker_or_requirement": blocker,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, formula, meaning, status, blocker in specs
    ]


def boundary_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "BND4741_0_adjoint_boundary",
            "B_adj[m]|partial W_loc = 0",
            "Adjoint integration-by-parts boundary terms must vanish by compact support, Dirichlet/Neumann data, or parent topological cancellation.",
            "UNSIGNED_CERTIFICATE_REQUIRED",
        ),
        (
            "BND4741_1_fixed_collar_domain",
            "D_v(partial W_loc)=0 and D_v(domain(A_TFRI))=0",
            "The local collar and operator domain must not move under the vertical variation being quarantined.",
            "UNSIGNED_CERTIFICATE_REQUIRED",
        ),
        (
            "BND4741_2_fixed_projector_green",
            "D_v P_loc = 0 and D_v G_loc = 0 before local scoring",
            "Projector and Green/readout data must be fixed before the transition response is scored.",
            "UNSIGNED_CERTIFICATE_REQUIRED",
        ),
        (
            "BND4741_3_topological_silence",
            "delta_g S_boundary/topological = 0 in the local bulk",
            "Boundary/topological/superpotential ownership is allowed only if it has zero bulk local metric response.",
            "UNSIGNED_CERTIFICATE_REQUIRED",
        ),
        (
            "BND4741_4_readout_order",
            "Pi_obs delta_g S_owner = delta_g Pi_obs S_owner = 0",
            "Readout order cannot hide residual stress in a post-selected projection.",
            "UNSIGNED_CERTIFICATE_REQUIRED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "boundary_id": boundary_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for boundary_id, condition, meaning, status in specs
    ]


def zero_mode_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZM4741_0_killing", "Killing/vector zero modes", "Pi_zero^K m = 0", "MISSING_NO_ZERO_MODE_CERTIFICATE"),
        ("ZM4741_1_conformal_killing", "conformal-Killing leakage", "Pi_zero^CK m = 0", "MISSING_NO_ZERO_MODE_CERTIFICATE"),
        ("ZM4741_2_harmonic_scalar", "harmonic scalar/York kernel", "Pi_zero^H phi = 0", "MISSING_NO_ZERO_MODE_CERTIFICATE"),
        ("ZM4741_3_TT_kernel", "TT/superpotential kernel", "Pi_zero^TT U = 0 or owned topologically", "MISSING_NO_ZERO_MODE_CERTIFICATE"),
        ("ZM4741_4_green_kernel", "Green-function zero mode", "kernel(G_loc)^perp fixed", "MISSING_NO_ZERO_MODE_CERTIFICATE"),
        ("ZM4741_5_boundary_corner", "corner/edge data", "corner modes have zero metric response", "MISSING_BOUNDARY_CERTIFICATE"),
        ("ZM4741_6_gauge_residual", "gauge/representative residual", "quotient representative coefficients vanish", "MISSING_GAUGE_CERTIFICATE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_mode_id": zero_mode_id,
            "mode_family": mode_family,
            "required_projection": required_projection,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for zero_mode_id, mode_family, required_projection, status in specs
    ]


def matter_gr_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "MGR4741_0_matter_channel_kept",
            "delta S_matter/delta g_mu_nu != 0",
            "Ordinary matter must keep its metric coupling; only the transition-owner residual is quarantined.",
            "CONDITIONAL_PASS_FROM_SOURCE",
        ),
        (
            "MGR4741_1_newton_limit_required",
            "L_GR^{-1} Sigma_metric[T_matter] -> Phi_N with nabla^2 Phi_N = 4 pi G rho",
            "The branch is not allowed to win by deleting the GR/Newton response channel.",
            "EXTERNAL_LIMIT_STILL_REQUIRED",
        ),
        (
            "MGR4741_2_owner_null_only",
            "Sigma_metric[S_owner]_loc=0 while Sigma_metric[S_matter]_loc != 0",
            "This separates local-GR preservation from transition-current cancellation.",
            "TARGET_SIGNATURE",
        ),
        (
            "MGR4741_3_failure_condition",
            "if zero-multiplier proof also forces T_matter=0, reject the branch",
            "A metric-null owner theorem that erases ordinary matter is physically unusable.",
            "FIREWALL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "matter_id": matter_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for matter_id, condition, meaning, status in specs
    ]


def finite_source_ledger_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FSV4741_0_CDeltaKdiv", "C_DeltaK_div", "dimensionless", "projected DeltaK-divergence residual", "MISSING_SOURCE_VALUE"),
        ("FSV4741_1_CTFRI", "C_TF_RI", "dimensionless", "trace-free RI commutator residual", "MISSING_SOURCE_VALUE"),
        ("FSV4741_2_Cconn", "C_conn", "dimensionless", "same-geometry connection commutator residual", "MISSING_SOURCE_VALUE"),
        ("FSV4741_3_Cboundary", "C_boundary", "dimensionless", "adjoint boundary/corner/readout leakage", "MISSING_SOURCE_VALUE"),
        ("FSV4741_4_Ckernel", "C_kernel", "dimensionless", "metric response kernel leakage", "MISSING_SOURCE_VALUE"),
        ("FSV4741_5_CzeroMode", "C_zeroMode", "dimensionless", "unremoved adjoint zero-mode leakage", "MISSING_NO_ZERO_MODE_CERTIFICATE_OR_VALUE"),
        ("FSV4741_6_Cdomain", "C_domain", "dimensionless", "moving local collar/domain leakage", "MISSING_DOMAIN_CERTIFICATE_OR_VALUE"),
        ("FSV4741_7_Creadout", "C_readout", "dimensionless", "projector/Green/readout-order leakage", "MISSING_READOUT_CERTIFICATE_OR_VALUE"),
        ("FSV4741_8_Pi_arena", "Pi_arena", "dimensionless matrix", "PPN/R10/clock/orbital/WEP projection normalization", "MISSING_ARENA_PROJECTION"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "finite_value_id": finite_value_id,
            "symbol": symbol,
            "units": units,
            "definition": definition,
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for finite_value_id, symbol, units, definition, status in specs
    ]


def finite_dryrun_rows(timestamp: str) -> list[dict[str, Any]]:
    threshold = get_threshold()
    specs = [
        ("DRY4741_0_zero_certificate", "all_zero_multiplier_boundary_zero_mode_clauses_signed", "0", threshold, "PASS_CONDITIONAL_ONLY", "requires ADJ4741_3 plus all BND/ZM clauses"),
        ("DRY4741_1_missing_CDeltaKdiv", "missing_C_DeltaK_div", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "source FSV4741_0 or prove C_DeltaK_div=0"),
        ("DRY4741_2_missing_CTFRI", "missing_C_TF_RI", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "source FSV4741_1 or prove C_TF_RI=0"),
        ("DRY4741_3_missing_boundary", "missing_C_boundary", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "sign B_adj=0 or source a bound"),
        ("DRY4741_4_missing_zero_mode", "missing_C_zeroMode", "MISSING_SOURCE_VALUE", threshold, "FAIL_CLOSED", "prove Pi_zero m=0 or source a bound"),
        ("DRY4741_5_missing_projection", "missing_Pi_arena", "MISSING_ARENA_PROJECTION", threshold, "FAIL_CLOSED", "source arena projection normalization"),
        ("DRY4741_6_symbolic_vector", "symbolic_transition_residual", "Pi_Delta*C_DeltaK_div+Pi_RI*C_TF_RI+Pi_conn*C_conn+Pi_bdry*C_boundary+Pi_kernel*C_kernel+Pi_zero*C_zeroMode+Pi_domain*C_domain+Pi_readout*C_readout", threshold, "NOT_SCORE_READY", "requires all finite values and projections"),
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
        for dryrun_id, case, predicted_response, threshold, result, next_action in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4741_0_zero_proof", "prove adjoint coercivity plus no-zero-mode and boundary silence", "best_route", "try to sign c_adj>0, B_adj=0, Pi_zero m=0"),
        ("ROUTE4741_1_finite_source", "source first finite transition residual value", "fallback_route", "start with C_zeroMode or C_boundary if theorem remains unsigned"),
        ("ROUTE4741_2_matter_preservation", "audit matter response against GR/Newton", "parallel_gate", "ensure owner-null theorem does not erase ordinary matter"),
        ("ROUTE4741_3_no_claim", "claim local-GR/Newton pass now", "rejected", "zero theorem and finite values remain unsigned/non-numeric"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "next_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, requirement in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4741_0_sources", "All cited 4741 source anchors exist and contain the expected handoff text.", "pass_internal", False),
        ("GATE4741_1_adjoint_zero_theorem", "Need c_adj>0, B_adj=0, Pi_zero m=0 to infer lambda=eta=rho=xi=chi=0.", "closed_unsigned", False),
        ("GATE4741_2_boundary_readout", "Need fixed boundary/domain/projector/Green/readout order.", "closed_unsigned", False),
        ("GATE4741_3_finite_values", "Need numeric/source-backed values for finite residual vector if theorem fails.", "closed_missing_inputs", False),
        ("GATE4741_4_matter_GR", "Need ordinary matter GR/Newton preservation alongside owner-nullity.", "conditional_open", False),
        ("GATE4741_5_no_public_claim", "No R10, PPN, WEP, clock, orbital, local-GR or public claim from 4741.", "closed_firewall", False),
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
        ("FW4741_0_no_plateau_axiom", "Do not assume local suppression by plateau; derive it from adjoint coercivity or score finite residuals."),
        ("FW4741_1_no_boundary_smuggling", "Do not discard B_adj, corner, domain, Green or readout terms without a parent certificate."),
        ("FW4741_2_no_zero_mode_handwave", "Do not set Killing/harmonic/TT/Green zero modes to zero without a projection or boundary proof."),
        ("FW4741_3_no_matter_erasure", "Do not make local GR by removing ordinary matter stress response."),
        ("FW4741_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
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
            "summary": "4741 converts the zero-multiplier route into a precise theorem contract: homogeneous adjoint equation, coercive energy identity, silent boundary/readout/domain terms and no zero modes. The exact theorem is conditionally written but not signed; finite residual source rows are staged fail-closed.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4741_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4741_1_science_verdict",
            "status": "exact_route_reduced_to_signed_functional_analysis_or_finite_values",
            "detail": "The branch has moved from vague missing coupling to a concrete adjoint coercivity/no-zero-mode/boundary-silence theorem contract.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4741 shows the local suppression law is provable only if the adjoint operator has a coercive no-zero-mode certificate with silent boundary/readout/domain terms.",
            "preferred_route": "Try to prove c_adj>0 and Pi_zero m=0 for the fixed local collar/operator; if this fails, source the first finite residual value.",
            "fallback_route": "Quantify C_zeroMode or C_boundary first because those are the shortest routes to a finite transition residual bound.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    adjoint: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    zero_modes: list[dict[str, Any]],
    matter: list[dict[str, Any]],
    finite_values: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4741 Y5 R2FR: Zero Multiplier Boundary Certificate Or Transition Finite Source Values

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint does the derivation-first step for the 4740 parent-action route.
- The exact local suppression route is no longer a plateau axiom: it reduces to an adjoint zero theorem.
- The theorem is:

```text
m = (lambda, eta, rho, xi, chi)
A_TFRI^dagger m = 0
B_adj[m] = 0
Pi_zero m = 0
c_adj > 0
--------------------------------
lambda=eta=rho=xi=chi=0
```

- If those clauses are parent-signed, the transition-owner block can be locally metric-null.
- If any clause remains unsigned, the branch falls back to a finite residual vector with explicit source rows.
- No local-GR, Newton, PPN, R10, clock, WEP or orbital claim is made here.

## What Actually Moved

The missing object is now sharp:

```text
C_res = Pi_Delta*C_DeltaK_div
      + Pi_RI*C_TF_RI
      + Pi_conn*C_conn
      + Pi_bdry*C_boundary
      + Pi_kernel*C_kernel
      + Pi_zero*C_zeroMode
      + Pi_domain*C_domain
      + Pi_readout*C_readout
```

So the route is no longer "find the coupling somehow". It is either:

1. prove the adjoint theorem and set every term above to zero by parent signature; or
2. source the finite terms and score them against the transition threshold.

## Adjoint Certificate

{bullet(adjoint, "certificate_id", "formula")}

## Boundary / Readout Certificate

{bullet(boundary, "boundary_id", "condition")}

## Zero-Mode Ledger

{bullet(zero_modes, "zero_mode_id", "mode_family")}

## Matter GR Preservation

{bullet(matter, "matter_id", "condition")}

## Finite Source Values

{bullet(finite_values, "finite_value_id", "symbol")}

## Dry Run

{bullet(dryrun, "dryrun_id", "result")}

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

    formal = f"""# 757 PPC4161: Zero Multiplier Boundary Certificate Or Transition Finite Source Values

Generated: `{timestamp}`

## Local Theorem Contract

The 4740 constrained action can own the equations, but metric-nullity needs a signed adjoint branch. 4741 writes the exact contract:

```text
A_TFRI^dagger m = 0,
m=(lambda,eta,rho,xi,chi),
B_adj[m]=0,
Pi_zero m=0,
c_adj>0
=> lambda=eta=rho=xi=chi=0.
```

When this holds, `Sigma_metric[S_TFRI+S_TT+S_quar]_loc=0` is allowed. When it does not hold, the residual is not hidden; it is represented by `C_zeroMode`, `C_boundary`, `C_domain`, `C_readout`, `C_kernel`, `C_TF_RI`, and `C_DeltaK_div`.

## GR / Newton Firewall

The owner-null theorem may only silence transition-owner stress. It must preserve `delta S_matter/delta g != 0 -> GR/Newton`. Any branch that obtains local quiet by erasing ordinary matter is rejected.

## Current Status

- Exact zero route: conditional theorem written, unsigned.
- Finite route: source-value ledger written, fail-closed.
- Claim status: nonclaim.
- Next target: `{NEXT_TARGET}`.

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4741 reduces the zero-multiplier route to `A_TFRI^dagger m=0`, `B_adj[m]=0`, `Pi_zero m=0`, and `c_adj>0`.
- Conditional consequence: `lambda=eta=rho=xi=chi=0`, hence transition-owner local metric stress may vanish.
- Unsigned blockers are now named: `C_zeroMode`, `C_boundary`, `C_domain`, `C_readout`, `C_kernel`, `C_TF_RI`, and `C_DeltaK_div`.
- Ordinary matter remains protected by the firewall `delta S_matter/delta g != 0 -> GR/Newton`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4741 local packet update: the local suppression branch is a theorem contract, not an axiom. Prove adjoint coercivity/no-zero-mode/boundary silence or score a finite residual vector. No local-GR claim is opened.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4741-Y5-R2FR-zero-multiplier-boundary-certificate-or-transition-finite-source-values.md`

## Decision

`{DECISION}`

## What moved forward

- The 4740 zero-multiplier route was converted into an exact adjoint theorem contract.
- The local suppression proof now requires `A_TFRI^dagger m=0`, `B_adj[m]=0`, `Pi_zero m=0`, and `c_adj>0`.
- If signed, this gives `lambda=eta=rho=xi=chi=0`; if unsigned, the branch falls back to named finite residuals.
- Finite source rows were staged for `C_zeroMode`, `C_boundary`, `C_domain`, `C_readout`, `C_kernel`, `C_TF_RI`, and `C_DeltaK_div`.
- Ordinary matter GR/Newton preservation remains a hard firewall.

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
        "4741 reduces the zero-multiplier local-suppression route to an adjoint coercivity/no-zero-mode/boundary-silence theorem contract and stages finite residual source rows.",
        "Generated source register, adjoint multiplier certificate, boundary/readout certificate, zero-mode ledger, matter GR preservation check, finite source value ledger, dryrun, route matrix, gates, firewalls, decision, status, next target and validation.",
        "adjoint_zero_theorem_contract_unsigned_finite_values_staged_nonclaim",
        NEXT_TARGET,
        "Mistaking a conditional adjoint theorem for a signed local-GR pass, or hiding zero modes/boundary terms in the projection.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need c_adj>0, B_adj=0, Pi_zero m=0, fixed domain/readout, finite source values if theorem fails, and ordinary matter GR/Newton preservation.",
        "Zero multiplier boundary certificate or transition finite source values",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    adjoint: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    zero_modes: list[dict[str, Any]],
    matter: list[dict[str, Any]],
    finite_values: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4741_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4741_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4741_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4741_2_adjoint_theorem", "adjoint theorem row contains A_TFRI^dagger and zero multipliers", any("A_TFRI^dagger" in row["formula"] for row in adjoint) and any("lambda=eta=rho=xi=chi=0" in row["formula"] for row in adjoint), str(ADJOINT_CERTIFICATE_CSV)))
    checks.append(("VAL4741_3_boundary_rows", "boundary/readout certificate rows present", len(boundary) >= 5 and any("B_adj" in row["condition"] for row in boundary), str(BOUNDARY_CERTIFICATE_CSV)))
    checks.append(("VAL4741_4_zero_mode_rows", "zero-mode ledger rows present", len(zero_modes) >= 7 and any("TT" in row["mode_family"] for row in zero_modes), str(ZERO_MODE_LEDGER_CSV)))
    checks.append(("VAL4741_5_matter_firewall", "ordinary matter GR/Newton firewall present", any("GR/Newton" in row["condition"] or "GR/Newton" in row["meaning"] for row in matter), str(MATTER_GR_CHECK_CSV)))
    checks.append(("VAL4741_6_finite_ledger", "finite ledger covers at least 8 nonclaim symbols", len(finite_values) >= 8 and all(row["valid_for_claim"] is False for row in finite_values), str(FINITE_SOURCE_LEDGER_CSV)))
    checks.append(("VAL4741_7_dryrun_fail_closed", "missing finite-value dryrun rows fail closed", all(row["result"] == "FAIL_CLOSED" for row in dryrun if row["case"].startswith("missing_")), str(FINITE_DRYRUN_CSV)))
    checks.append(("VAL4741_8_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4741_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4741_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4741_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4741_12_claim_row", "claim row L-583 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4741_13_resume", "resume points from 4741 to 4742", "4741-Y5" in resume_text and "4742-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4741_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4741_OVERALL",
            "check": "all 4741 local generation and nonclaim checks pass",
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
    adjoint = adjoint_certificate_rows(timestamp)
    boundary = boundary_certificate_rows(timestamp)
    zero_modes = zero_mode_rows(timestamp)
    matter = matter_gr_rows(timestamp)
    finite_values = finite_source_ledger_rows(timestamp)
    dryrun = finite_dryrun_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ADJOINT_CERTIFICATE_CSV, adjoint)
    write_csv(BOUNDARY_CERTIFICATE_CSV, boundary)
    write_csv(ZERO_MODE_LEDGER_CSV, zero_modes)
    write_csv(MATTER_GR_CHECK_CSV, matter)
    write_csv(FINITE_SOURCE_LEDGER_CSV, finite_values)
    write_csv(FINITE_DRYRUN_CSV, dryrun)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, adjoint, boundary, zero_modes, matter, finite_values, dryrun, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, adjoint, boundary, zero_modes, matter, finite_values, dryrun, gates, timestamp))


if __name__ == "__main__":
    main()
