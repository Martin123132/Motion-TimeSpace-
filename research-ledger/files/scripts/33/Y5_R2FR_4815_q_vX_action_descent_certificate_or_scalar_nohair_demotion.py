from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4815"
CLAIM_ID = "L-657"
MARKER = "PPC4161_QVX_ACTION_DESCENT_CERTIFICATE_OR_SCALAR_NOHAIR_DEMOTION_4815"
PACKET_MARKER = "PPC4161_PACKET_QVX_ACTION_DESCENT_CERTIFICATE_OR_SCALAR_NOHAIR_DEMOTION_4815"
DECISION = "QVX_CERTIFICATE_FAILS_CURRENT_MTS_SCALAR_SOURCE_BRANCH_NEXT_NONCLAIM"
NEXT_TARGET = "4816-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"

DOC_PATH = POST / "4815-Y5-R2FR-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
FORMAL_PATH = FORMAL / "831-PPC4161-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "q_vX_action_descent_certificate_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_SOURCE_REGISTER.csv"
CERTIFICATE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_QVX_CERTIFICATE_INPUT.csv"
CERTIFICATE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_QVX_CERTIFICATE_OUTPUT.csv"
COUPLING_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_COUPLING_DESCENT_AUDIT.csv"
DEMOTION_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_DEMOTION_LEDGER.csv"
SCALAR_INPUT_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_SCALAR_SOURCE_INPUT_PACK.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_DECISION_LEDGER.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4815_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4815_VALIDATION.csv"

DOC_4814 = POST / "4814-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
TARGET_4814 = SOURCE_DIR / "P8_Y5_R2FR_4814_TARGET_AUDIT.csv"
DOC_1023 = POST / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
QVC_1023 = SOURCE_DIR / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
CDA_1023 = SOURCE_DIR / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv"
DEM_1023 = SOURCE_DIR / "P8_Y5_R10_1023_DEMOTION_LEDGER.csv"
SNH_1023 = SOURCE_DIR / "P8_Y5_R10_1023_SCALAR_SOURCE_INPUT_PACK.csv"
VQC_1022 = SOURCE_DIR / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv"
QVT_581 = SOURCE_DIR / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv"
QMAP_637 = SOURCE_DIR / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv"
OBS_637 = SOURCE_DIR / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv"
DVM_590 = SOURCE_DIR / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv"
SOURCEFREE_670 = SOURCE_DIR / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv"

CERTIFICATE_CLAUSES = (
    "parent_q_signed",
    "NX_integrability_signed",
    "Dq_vX_zero_signed",
    "action_descent_signed",
    "matter_descent_signed",
    "constants_marker_silence_signed",
    "hidden_frame_exclusion_signed",
    "vertical_generator_signed",
    "momentum_map_signed",
    "boundary_silence_signed",
    "degree_count_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

SOURCE_SPECS = [
    ("SRC4815_00_4814_doc", DOC_4814, "q_vX_action_descent_certificate_is_next", "4814 selects the q/v_X certificate as next target."),
    ("SRC4815_01_4814_target", TARGET_4814, "TGA4814_0_target_import", "4814 target audit inheritance."),
    ("SRC4815_02_1023_doc", DOC_1023, "QVC1023_0_parent_q", "1023 q/v_X certificate precedent."),
    ("SRC4815_03_1023_qvc", QVC_1023, "QVC1023_0_parent_q", "1023 certificate clause table."),
    ("SRC4815_04_1023_coupling", CDA_1023, "CDA1023_0_metric_chain_rule", "1023 coupling descent audit."),
    ("SRC4815_05_1023_demotion", DEM_1023, "DEM1023_0_scope", "1023 demotion ledger."),
    ("SRC4815_06_1023_scalar", SNH_1023, "SNH1023_0_Z_X", "1023 scalar/source input pack."),
    ("SRC4815_07_1022_vertical", VQC_1022, "VQC1022_0_q_map", "1022 vertical quotient construction."),
    ("SRC4815_08_581_chain", QVT_581, "QVT581_0_parent_projection", "581 quotient theorem chain."),
    ("SRC4815_09_637_qmap", QMAP_637, "QM637_2_vertical_kernel", "637 quotient map derivation."),
    ("SRC4815_10_637_obs", OBS_637, "OF637_1_chain_rule", "637 observed functor matter chain rule."),
    ("SRC4815_11_590_map", DVM_590, "DVM590_3_precise_map", "590 DCdagger vertical map."),
    ("SRC4815_12_670_sourcefree", SOURCEFREE_670, "PSF670_0_operator_form", "670 source-free fallback chain."),
    ("SRC4815_13_runner", RUNNER, "def certificate_row", "4815 executable certificate runner."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def bools(value: bool) -> dict[str, bool]:
    return {clause: value for clause in CERTIFICATE_CLAUSES}


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": bool(text and needle in text),
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def write_inputs(timestamp: str) -> None:
    certificate_rows = [
        {
            "certificate_id": "QVC4815_0_current_physical_certificate",
            "route": "current_MTS_physical",
            "required_object": "single parent q/v_X/action descent certificate",
            **bools(False),
            "no_GR_import_signed": True,
            "no_fit_to_bound_signed": True,
            "source_path": "MISSING_PARENT_QVX_ACTION_DESCENT_CERTIFICATE",
            "equation_ref": "q:Conf_parent->Q_obs; Dq[v_X]=0; S_parent=S_red[q]+B_top; S_m=Sbar_m[Obs(q),Psi,theta]",
            "current_evidence": "4814 selected the quotient/vertical route, but did not sign q, v_X, action descent, matter descent, boundary silence, or degree count.",
            "claim_effect_if_signed": "K_X=qbar_XT=Qbar_XH=0 and local X alpha branch inactive.",
            "notes": "This row is deliberately blocked until a parent-owned certificate exists.",
            "provenance": "4814 live route plus 1023 precedent",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "QVC4815_1_conditional_parent_certificate",
            "route": "conditional_theorem_skeleton",
            "required_object": "future parent certificate theorem",
            **bools(True),
            "source_path": str(DOC_1023),
            "equation_ref": "QVC1023_0_to_QVC1023_8 conditional theorem skeleton",
            "current_evidence": "If all certificate clauses are supplied together by a parent action, the quotient route is mathematically clean.",
            "claim_effect_if_signed": "X becomes representative/gauge data on the compact local branch.",
            "notes": "Passes only as a future theorem template; valid_for_claim remains false.",
            "provenance": "1023 certificate contract",
            "valid_for_claim": False,
        },
        {
            "certificate_id": "QVC4815_2_forbidden_post_readout_control",
            "route": "forbidden_control",
            "required_object": "anti-circularity failure control",
            **bools(True),
            "source_path": "POST_READOUT_QUOTIENT_ASSERT_VERTICALITY_AFTER_READOUT_GR_IMPORT",
            "equation_ref": "FORBIDDEN_QVX_SHORTCUT",
            "current_evidence": "Control row must fail if verticality is asserted after observables/GR readout have already been chosen.",
            "claim_effect_if_signed": "none",
            "notes": "This protects against fitting q after the fact.",
            "provenance": "forbidden control",
            "valid_for_claim": False,
        },
    ]
    write_csv(CERTIFICATE_INPUT_CSV, certificate_rows)


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(CERTIFICATE_INPUT_CSV), str(CERTIFICATE_OUTPUT_CSV)], check=True)


def write_ledgers(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    certificate = read_csv(CERTIFICATE_OUTPUT_CSV)
    coupling = [
        {
            "audit_id": "CDA4815_0_metric_chain_rule",
            "object": "metric/coframe matter variation",
            "result": "conditional_math_pass",
            "reason": "DObs(Dq[v_X])=0 kills the metric/frame pullback only if v_X is truly vertical before readout.",
            "remaining_coupling": "none from metric/frame if the full certificate closes",
            "demotion_effect": "if q/v_X fails, retain finite qbar_XT or matter-coupling row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CDA4815_1_constants_markers",
            "object": "theta_A constants/material labels",
            "result": "not_closed",
            "reason": "L_vX theta_A=0 is not parent-owned for EM, clocks, masses, or material labels.",
            "remaining_coupling": "constant/material marker X-dependence",
            "demotion_effect": "retain WEP/clock/fifth-force source rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CDA4815_2_hidden_frame",
            "object": "hidden conformal/disformal X channel",
            "result": "counterexample_filter_only",
            "reason": "Any hidden X-frame dependence is observable unless it factors through q.",
            "remaining_coupling": "F_X prime or disformal coefficient if present",
            "demotion_effect": "source/coefficient route, not quotient theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CDA4815_3_projector_boundary",
            "object": "Hamiltonian/projector boundary coupling",
            "result": "open",
            "reason": "B_X, Pi_M^H[Q_edge], K_boundary, and source split remain unsigned.",
            "remaining_coupling": "edge/source projection into measured Hamiltonian mass",
            "demotion_effect": "retain EDGEBOUND and Qbar_edge_XH rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CDA4815_4_verdict",
            "object": "coupling descent verdict",
            "result": "coupling_not_theorem_zero",
            "reason": "matter descent and boundary/projector descent are conditional, not parent-signed.",
            "remaining_coupling": "qbar_XT;Qbar_XH;edge terms;clock/WEP channels",
            "demotion_effect": "move to scalar/source input pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    demotion = [
        {
            "demotion_id": "DEM4815_0_scope",
            "demoted_object": "current quotient/vertical no-pole route",
            "demotion": "demoted_to_conditional_only_for_current_MTS",
            "reason": "the single certificate fails at field-by-field v_X, action descent, matter/no-marker descent, boundary silence, and degree count",
            "what_survives": "future parent action can reopen the route if it signs every clause together",
            "next_required_row": "scalar/source input pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "demotion_id": "DEM4815_1_scalar_operator",
            "demoted_object": "scalar no-hair fallback",
            "demotion": "promoted_to_next_work_target_not_claim",
            "reason": "after q/v_X fails, the cleanest executable route is positive operator/source-free proof",
            "what_survives": "positive energy identity can still kill X if all inputs close",
            "next_required_row": "Z_X;M_X2;J_X;boundary_flux_X;lambda_X",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "demotion_id": "DEM4815_2_sourced_residual",
            "demoted_object": "finite coupling/source branch",
            "demotion": "retained_as_scoreable_if_scalar_nohair_fails",
            "reason": "nonzero J_X or matter coupling must be tested, not hidden",
            "what_survives": "R10/R11 alpha/source rows",
            "next_required_row": "K_X;Qbar_XH;qbar_XT;alpha_X(lambda);EDGEBOUND terms",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "demotion_id": "DEM4815_3_claim_ceiling",
            "demoted_object": "local-GR/R10/R11 local silence",
            "demotion": "blocked",
            "reason": "no theorem-zero branch or valid source-bound branch closes",
            "what_survives": "discipline: no local claim from this chain",
            "next_required_row": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    scalar_inputs = [
        {
            "input_id": "SNH4815_0_Z_X",
            "quantity": "Z_X",
            "needed_for": "positive kinetic term",
            "required_source": "parent Hessian second variation with field units",
            "current_status": "MISSING_PARENT_INPUT",
            "if_missing": "no scalar no-hair theorem; score residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SNH4815_1_M_X2",
            "quantity": "M_X^2",
            "needed_for": "positive mass gap and lambda_X",
            "required_source": "parent Hessian curvature/range derivation with units",
            "current_status": "MISSING_PARENT_INPUT",
            "if_missing": "zero/long-range/tachyonic mode remains possible",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SNH4815_2_J_X_zero",
            "quantity": "J_X=0",
            "needed_for": "source-free exterior equation",
            "required_source": "matter/hidden/source variation proof or sourced current bound",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "if_missing": "qbar_XT/source coupling row required",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SNH4815_3_boundary_flux_zero",
            "quantity": "boundary_flux_X=0",
            "needed_for": "positive energy identity conclusion",
            "required_source": "boundary class/no-hair/projector silence or flux bound",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "if_missing": "EDGEBOUND and Qbar_edge rows remain live",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SNH4815_4_alpha_coefficients",
            "quantity": "K_X;Qbar_XH;qbar_XT;lambda_X",
            "needed_for": "R10/R11 residual scoring if no-hair fails",
            "required_source": "source-normalized coefficient rows with units and no-cancellation envelope",
            "current_status": "MISSING_ARENA_PROJECTION",
            "if_missing": "no local empirical pass",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    claim_gates = [
        {"gate_id": "CG4815_0_sources_registered", "claim": "4815 source chain exists", "gate_pass": True, "reason": "all cited quotient, matter, vertical, and fallback files are found", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_1_q_vX_certificate", "claim": "q/v_X/action certificate closes", "gate_pass": False, "reason": "single certificate fails at multiple required clauses", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_2_coupling_zero", "claim": "matter/coupling descent theorem-zero", "gate_pass": False, "reason": "constants/markers, hidden frame, and boundary/projector coupling remain open", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_3_scalar_nohair_claim", "claim": "scalar no-hair theorem", "gate_pass": False, "reason": "Z_X, M_X2, J_X=0, and boundary_flux_X=0 remain missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_4_residual_score_claim", "claim": "finite residual score", "gate_pass": False, "reason": "alpha/source coefficient rows are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_5_demotion_written", "claim": "current quotient route demoted", "gate_pass": True, "reason": "current MTS keeps quotient route conditional and moves executable work to scalar/source inputs", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_6_local_GR_claim", "claim": "local GR/Newton reduction", "gate_pass": False, "reason": "no local branch closes theorem-zero or source-bound pass", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4815_7_guardrail", "claim": "no fake quotient credit", "gate_pass": True, "reason": "post-readout quotient and scalar-as-edge-proof are forbidden", "claim_allowed": False, "valid_for_claim": False},
    ]
    decisions = [
        {"decision_id": "DEC4815_0_certificate_result", "decision": "The q/v_X/action descent certificate does not close for current MTS.", "because": "conditional q-map pieces exist, but no field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence, or degree count is signed.", "next_action": "do not spend no-pole credit from quotient route", "valid_for_claim": False},
        {"decision_id": "DEC4815_1_demotion", "decision": "Demote the current local branch to scalar no-hair/source-coefficient work.", "because": "this is the honest executable route after the quotient certificate fails in current files.", "next_action": "fill scalar positive operator/source/boundary inputs before testing", "valid_for_claim": False},
        {"decision_id": "DEC4815_2_future_reopen", "decision": "The quotient route can be reopened only by a real parent action certificate.", "because": "future q/v_X proof would still be the cleanest local-GR route if it supplies all missing clauses together.", "next_action": "require q, v_X, action descent, matter descent, boundary silence, and degree count in one source-backed row", "valid_for_claim": False},
        {"decision_id": "DEC4815_3_next_target", "decision": "Next target is scalar no-hair input pack or residual alpha coefficient runner.", "because": "Z_X, M_X2, J_X=0, boundary_flux_X=0, and alpha coefficients are now the executable local branch inputs.", "next_action": NEXT_TARGET, "valid_for_claim": False},
    ]
    status = [
        {"status_id": "STATUS4815_0_certificate", "status": "QVX_CERTIFICATE_FAILS_CURRENT_MTS", "detail": "current route remains conditional only"},
        {"status_id": "STATUS4815_1_coupling", "status": "COUPLING_NOT_THEOREM_ZERO", "detail": "ordinary matter/marker/hidden-frame/boundary channels remain open"},
        {"status_id": "STATUS4815_2_demotion", "status": "SCALAR_SOURCE_BRANCH_NEXT", "detail": NEXT_TARGET},
        {"status_id": "STATUS4815_3_claim", "status": "LOCAL_GR_CLAIM_BLOCKED", "detail": "no theorem-zero or source-bound branch closes"},
    ]
    next_rows = [
        {
            "next_target": NEXT_TARGET,
            "objective": "fill or reject the scalar no-hair input pack: Z_X, M_X^2, J_X=0, boundary_flux_X=0, lambda_X, and fallback alpha coefficients with units and source paths",
            "include": "parent Hessian signs, field units, self-adjoint domain, matter/source zero proof, boundary flux zero/bound, lambda_X, K_X, Qbar_XH, qbar_XT, no-cancellation envelope",
            "exclude": "quotient no-pole credit without certificate, scalar no-hair as edge exactness, source-free by assertion, placeholder coefficients, R10/R11 pass, local-GR claim, GitHub action",
            "valid_for_claim": False,
        }
    ]
    write_csv(COUPLING_AUDIT_CSV, coupling)
    write_csv(DEMOTION_LEDGER_CSV, demotion)
    write_csv(SCALAR_INPUT_PACK_CSV, scalar_inputs)
    write_csv(CLAIM_GATES_CSV, claim_gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {
        "certificate": certificate,
        "coupling": coupling,
        "demotion": demotion,
        "scalar_inputs": scalar_inputs,
        "claim_gates": claim_gates,
        "decisions": decisions,
        "status": status,
        "next": next_rows,
    }


def write_docs(tables: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]], timestamp: str) -> None:
    source_rows = read_csv(SOURCE_REGISTER_CSV)
    certificate_input = read_csv(CERTIFICATE_INPUT_CSV)
    doc = f"""# 4815 Y5 R2FR q vX action descent certificate or scalar nohair demotion

**Status:** The single `q/v_X/action` certificate does not close for current MTS. The route is demoted to conditional-only, and the scalar/source coefficient branch becomes the next executable target.

Decision: `{DECISION}`

Generated: `{timestamp}`

## Core theorem contract

The clean local-GR route would be a parent-owned quotient theorem, not a fitted local suppression rule:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + B_top/domain
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
L_vX theta_A = 0
delta G_X = Omega(delta Phi, v_X)
Q_X = 0/proper/exact and Pi_M^H[Q_X] = 0
```

If all clauses are parent-signed together, `K_X=qbar_XT=Qbar_XH=0` is a theorem result. In current files the clauses remain conditional or missing, so no local-GR/R10/R11 claim is allowed from this route.

## Source register
{table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"])}

## q/v_X certificate input
{table(certificate_input, ["certificate_id", "route", "required_object", "current_evidence", "claim_effect_if_signed", "valid_for_claim"])}

## q/v_X certificate output
{table(tables["certificate"], ["certificate_id", "route", "certificate_status", "certificate_theorem", "missing_for_claim", "anti_circularity_status", "claim_allowed"])}

## Coupling descent audit
{table(tables["coupling"], ["audit_id", "object", "result", "reason", "remaining_coupling", "demotion_effect", "valid_for_claim"])}

## Demotion ledger
{table(tables["demotion"], ["demotion_id", "demoted_object", "demotion", "reason", "what_survives", "next_required_row", "valid_for_claim"])}

## Scalar/source input pack
{table(tables["scalar_inputs"], ["input_id", "quantity", "needed_for", "required_source", "current_status", "if_missing", "valid_for_claim"])}

## Claim gates
{table(tables["claim_gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"])}

## Decision ledger
{table(tables["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Validation
{table(validation, ["check_id", "description", "result", "evidence"])}

## Next target
{table(tables["next"], ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    formal = f"""# 831 PPC4161 q vX action descent certificate or scalar nohair demotion

Marker: `{MARKER}`

4815 formalizes the parent certificate required before the local quotient route can be used:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + B_top/domain
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
```

The current branch fails the single-certificate gate because action descent, matter/no-marker descent, hidden-frame exclusion, boundary silence, and degree count are not parent-signed. Therefore the quotient route is conditional-only, and the next executable route is:

`{NEXT_TARGET}`

No local-GR, R10, R11, clock, orbital, or PPN claim is promoted by this checkpoint.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker not in current:
        with path.open("a", encoding="utf-8", newline="") as handle:
            if current and not current.endswith("\n"):
                handle.write("\n")
            handle.write(text)


def append_claim(timestamp: str) -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    columns = read_text(CLAIMS_PATH).splitlines()[0].split(",")
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "q_vX_action_descent_certificate_or_scalar_nohair_demotion",
        "current_evidence": "4815 writes the exact parent quotient/action/matter/boundary/degree certificate and shows current MTS does not yet sign it.",
        "status": "qvx_certificate_failed_current_mts_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "post-readout quotient; hidden matter frame; constants/markers; boundary/projector coupling; missing degree count",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "quotient route remains conditional; scalar/source branch inputs still missing",
        "title": "q/v_X action descent certificate or scalar no-hair demotion",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4815 installs the parent certificate required to make the local quotient route real:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + B_top/domain
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
```

The current MTS files do not sign the full certificate. The route survives only as a future theorem target; the next executable local branch is scalar no-hair/source coefficients.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
""",
    )
    RESUME_PATH.write_text(
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4815-Y5-R2FR-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md`
Marker: `{MARKER}`

## Where we are

4815 tried the exact local quotient route:

```text
q: Conf_parent -> Q_obs = Conf_parent / N_X
Dq[v_X] = 0
S_parent[Phi] = S_red[q(Phi)] + B_top/domain
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
```

## Live blockers

- The current MTS corpus does not yet sign the full parent q/v_X/action/matter/boundary/degree certificate.
- Coupling is not theorem-zero because constants/markers, hidden frame, and boundary/projector channels remain open.
- The scalar/source branch is now the honest executable next route.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def compile_and_clean() -> bool:
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(str(SCRIPT_DIR / "Y5_R2FR_4815_q_vX_action_descent_certificate_or_scalar_nohair_demotion.py"), doraise=True)
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    return not cache.exists()


def validate(cache_removed: bool) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    certificate = {row["certificate_id"]: row for row in read_csv(CERTIFICATE_OUTPUT_CSV)}
    coupling = {row["audit_id"]: row for row in read_csv(COUPLING_AUDIT_CSV)}
    demotion = {row["demotion_id"]: row for row in read_csv(DEMOTION_LEDGER_CSV)}
    scalar = {row["input_id"]: row for row in read_csv(SCALAR_INPUT_PACK_CSV)}
    gates = {row["gate_id"]: row for row in read_csv(CLAIM_GATES_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4815_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4815_1_current_blocks", "description": "current physical q/v_X certificate remains blocked", "result": "PASS" if certificate["QVC4815_0_current_physical_certificate"]["certificate_status"] == "BLOCKED_MISSING_QVX_CERTIFICATE_INPUTS" else "FAIL", "evidence": str(CERTIFICATE_OUTPUT_CSV)},
        {"check_id": "VAL4815_2_conditional_passes", "description": "conditional parent certificate template passes only as nonclaim", "result": "PASS" if certificate["QVC4815_1_conditional_parent_certificate"]["certificate_theorem"] == "True" and certificate["QVC4815_1_conditional_parent_certificate"]["claim_allowed"] == "False" else "FAIL", "evidence": str(CERTIFICATE_OUTPUT_CSV)},
        {"check_id": "VAL4815_3_forbidden_fails", "description": "post-readout/GR-import quotient shortcut fails", "result": "PASS" if certificate["QVC4815_2_forbidden_post_readout_control"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(CERTIFICATE_OUTPUT_CSV)},
        {"check_id": "VAL4815_4_coupling_open", "description": "coupling descent verdict remains theorem-open", "result": "PASS" if coupling["CDA4815_4_verdict"]["result"] == "coupling_not_theorem_zero" else "FAIL", "evidence": str(COUPLING_AUDIT_CSV)},
        {"check_id": "VAL4815_5_demotion_written", "description": "quotient route demotion is written", "result": "PASS" if demotion["DEM4815_0_scope"]["demotion"] == "demoted_to_conditional_only_for_current_MTS" else "FAIL", "evidence": str(DEMOTION_LEDGER_CSV)},
        {"check_id": "VAL4815_6_scalar_inputs_nonclaim", "description": "scalar/source inputs are explicit and remain missing", "result": "PASS" if all(row["valid_for_claim"] == "False" and row["current_status"].startswith("MISSING") for row in scalar.values()) else "FAIL", "evidence": str(SCALAR_INPUT_PACK_CSV)},
        {"check_id": "VAL4815_7_claim_gates_block", "description": "claim gates block local-GR/R10/R11 promotion", "result": "PASS" if gates["CG4815_6_local_GR_claim"]["gate_pass"] == "False" and gates["CG4815_5_demotion_written"]["gate_pass"] == "True" else "FAIL", "evidence": str(CLAIM_GATES_CSV)},
        {"check_id": "VAL4815_8_claim_register", "description": "claim register includes L-657 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4815_9_resume", "description": "resume points at 4816", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
        {"check_id": "VAL4815_10_docs", "description": "post and formal docs exist", "result": "PASS" if DOC_PATH.exists() and FORMAL_PATH.exists() else "FAIL", "evidence": f"{DOC_PATH}; {FORMAL_PATH}"},
        {"check_id": "VAL4815_11_pycache", "description": "scripts compiled and __pycache__ removed", "result": "PASS" if cache_removed else "FAIL", "evidence": str(SCRIPT_DIR / "__pycache__")},
    ]
    checks.append({"check_id": "VAL4815_OVERALL", "description": "all 4815 q/v_X certificate/demotion checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def main() -> int:
    timestamp = now()
    write_inputs(timestamp)
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    run_runner()
    tables = write_ledgers(timestamp)
    update_registers(timestamp)
    cache_removed = compile_and_clean()
    validation = validate(cache_removed)
    write_docs(tables, validation, timestamp)
    validation = validate(cache_removed)
    write_docs(tables, validation, timestamp)
    if any(row["result"] != "PASS" for row in validation):
        return 1
    print(f"{MARKER}: validation PASS; next {NEXT_TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
