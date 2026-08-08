from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PROJECTIVE_TRACE_SILENCE_OR_P4_PROJECTIVE_COMPONENT_ROW_2349"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2349-Y5-R2FR-projective-trace-silence-or-P4-projective-component-row.md"

PATHS = {
    "2348_doc": ROOT / "2348-Y5-R2FR-spin-connection-coframe-owned-or-axial-torsion-P4-row.md",
    "2348_next": OUT / "P8_Y5_PARENT_QLOC_2348_NEXT_TARGET.csv",
    "2348_claims": OUT / "P8_Y5_PARENT_QLOC_2348_CLAIM_GATES.csv",
    "2119_cert": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_CERTIFICATE.csv",
    "2119_policy": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_RESIDUAL_POLICY.csv",
    "2337_projective": OUT / "P8_Y5_PARENT_QLOC_2337_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv",
    "2118_zero": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
    "2118_kernels": OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv",
    "2117_exceptions": OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv",
    "2117_zero_matrix": OUT / "P8_Y5_PARENT_QLOC_2117_ZERO_ACTIVATION_MATRIX.csv",
    "2099_map": OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv",
    "2043_guard": OUT / "P8_Y5_PARENT_QLOC_2043_SPIN_PROJECTIVE_GUARD.csv",
    "1960_lc": OUT / "P8_Y5_PARENT_QLOC_1960_LC_NO_HYPERMOMENTUM_ATTEMPT.csv",
    "1960_p4": OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
    "1833_boundary_projective": OUT / "P8_Y5_PARENT_QLOC_1833_BOUNDARY_PROJECTIVE_LEDGER.csv",
}

SOURCES = [
    ("SRC2349_00_2348_doc", "2348_doc", ["NEXT2348_0", "projective trace silence"], "2348 selected projective trace as next connection caveat"),
    ("SRC2349_01_2348_next", "2348_next", ["NEXT2348_0", "projective-trace"], "machine-readable 2349 target"),
    ("SRC2349_02_2348_claims", "2348_claims", ["CG2348_3_projective_guard", "false"], "2348 projective gate remained blocked"),
    ("SRC2349_03_2119_cert", "2119_cert", ["PJC2119_5_verdict", "GLOBAL_CERTIFICATE_BLOCKED"], "projective certificate status"),
    ("SRC2349_04_2119_policy", "2119_policy", ["PRP2119_1_global_corpus", "residual_retained"], "projective residual policy"),
    ("SRC2349_05_2337_projective", "2337_projective", ["PRJ2337_3_verdict", "PRIVATE_ZERO_PUBLIC_NONCLAIM"], "private SRNG projective-zero split"),
    ("SRC2349_06_2118_zero", "2118_zero", ["SRZ2118_5_projective_zero", "CONDITIONAL_ZERO_NOT_SIGNED"], "source/readout projective zero attempt"),
    ("SRC2349_07_2118_kernels", "2118_kernels", ["KSR2118_6_projective_trace_kernel", "CERTIFICATE_OR_BOUND_MISSING"], "fallback projective trace kernel"),
    ("SRC2349_08_2117_exceptions", "2117_exceptions", ["SEC2117_8_projective_trace", "all-sector projective invariance proof missing"], "sector exception ledger"),
    ("SRC2349_09_2117_zero_matrix", "2117_zero_matrix", ["Z2117_7_projective", "all-sector invariance proof missing"], "projective zero activation matrix"),
    ("SRC2349_10_2099_map", "2099_map", ["DGM2099_6_projective", "MAP_REGISTERED_PROJECTION_MISSING"], "DeltaGamma projective component map"),
    ("SRC2349_11_2043_guard", "2043_guard", ["SPG2043_1_projective_guard", "UNSIGNED"], "spin/projective guard"),
    ("SRC2349_12_1960_lc", "1960_lc", ["LC1960_5_projective_caveat", "PARTIAL_NOT_FULL_P4"], "LC projective caveat"),
    ("SRC2349_13_1960_p4", "1960_p4", ["P4C1960_2_projective_trace", "MISSING_PROJECTIVE_INVARIANCE_OR_BOUND"], "P4 projective envelope"),
    ("SRC2349_14_1833_boundary_projective", "1833_boundary_projective", ["BPL1833_1_projective_trace", "MISSING_PROJECTIVE_INVARIANCE"], "older boundary/projective ledger"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2349_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_TRACE_SILENCE_AUDIT.csv",
    "proof": OUT / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_PROOF_STACK.csv",
    "p4": OUT / "P8_Y5_PARENT_QLOC_2349_P4_PROJECTIVE_COMPONENT_ROW.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2349_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2349_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2349_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2349_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2349_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2349_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2349_0_projective_audit", OUTPUTS["audit"], BETA_DOCS / "PROJECTIVE_TRACE_SILENCE_AUDIT_2349_NONCLAIM.csv"),
    ("COPY2349_1_projective_p4", OUTPUTS["p4"], MICRO_RESIDUALS / "P4_PROJECTIVE_COMPONENT_ROW_2349_NONCLAIM.csv"),
    ("COPY2349_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2349_PROJECTIVE_TRACE_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "source_path": str(path),
                "exists": bool_text(exists),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(exists and not missing),
                "missing_needles": ";".join(missing),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def build_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2349_0_transform",
            "clause": "projective trace direction",
            "formal_statement": "Gamma^lambda_{mu nu} -> Gamma^lambda_{mu nu} + delta^lambda_mu A_nu; the trace mode is harmless only if it is not a physical variable or all observable sectors are invariant/gauge-fixed.",
            "status": "TARGET_SHARPENED",
            "obstruction": "must handle source, clock, WEP, light, orbit and boundary readouts, not just the gravitational EH equation",
            "effect_if_closed": "Delta_projective can be set to zero without fitting",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2349_1_owned_coframe_private_zero",
            "clause": "private owned-coframe + SRNG branch",
            "formal_statement": "If Gamma_ind is absent and source/readout exceptions are excluded by private SRNG/OFC, there is no projective variable direction to couple.",
            "status": "ZERO_INSIDE_PRIVATE_BRANCH_ONLY",
            "obstruction": "private branch is not yet the public/canonical parent action",
            "effect_if_closed": "Delta_projective_private = 0 inside the working branch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2349_2_palatini_gauge_route",
            "clause": "Palatini/no-hypermomentum gauge route",
            "formal_statement": "If independent Gamma enters only an EH/Palatini sector and all matter/source/readout hypermomentum vanishes, the remaining projective vector may be gauge-fixed.",
            "status": "EXACT_CONDITIONAL_ROUTE",
            "obstruction": "EH-only premise, no-hypermomentum, and all-sector readout invariance are unsigned",
            "effect_if_closed": "projective trace cannot leak into observables after gauge fixing",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2349_3_unparameterized_orbit_guard",
            "clause": "orbit/readout guard",
            "formal_statement": "Projective shifts preserve unparameterized autoparallel paths only up to reparameterization; physical clock/orbit observables still require metric-time and source-GM readout clauses.",
            "status": "CONDITIONAL_READOUT_GUARD",
            "obstruction": "orbital/clock/GM transfer kernels remain unsigned",
            "effect_if_closed": "stops projective trace from hiding as a fitted-G or clock convention",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2349_4_source_clock_WEP_gap",
            "clause": "source/clock/WEP coupling gap",
            "formal_statement": "Any direct trace coupling to source charge, clocks, rods or WEP material response makes P_projective[source,clock,WEP] nonzero.",
            "status": "FALLBACK_RETAINED",
            "obstruction": "trace-coupling normalization and response operators are missing",
            "effect_if_closed": "if not closed, the P4 projective residual must be bounded",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PROJ2349_5_verdict",
            "clause": "promote projective trace silence",
            "formal_statement": "Current corpus proves projective trace is gauge/fixed/unobservable in every local test arena.",
            "status": "PRIVATE_ZERO_PUBLIC_FALLBACK_RETAINED",
            "obstruction": "global all-sector certificate is blocked; independent affine fallback still needs bound inputs",
            "effect_if_closed": "not closed publicly; keep projective P4 row",
            "valid_for_claim": "false",
        },
    ]


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSTACK2349_0_no_variable",
            "lemma": "no projective variable in owned-coframe branch",
            "statement": "A projective trace transformation cannot source a current when Gamma_ind is not in the ordinary local branch configuration space.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_parent_input": "owned-coframe/SRNG branch must be promoted or explicitly labelled private",
            "use": "private projective zero switch",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSTACK2349_1_EH_projective_gauge",
            "lemma": "projective gauge in Palatini route",
            "statement": "EH/Palatini connection equations leave at most a projective vector when matter/source/readout hypermomentum is zero.",
            "proof_status": "EXACT_CONDITIONAL_ROUTE",
            "missing_parent_input": "EH-only operator and no-hypermomentum theorem",
            "use": "candidate public route if parent action keeps independent Gamma",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSTACK2349_2_all_sector_invariance",
            "lemma": "all-sector observability guard",
            "statement": "A gauge vector is physically harmless only when matter, source, clocks, rods, light, orbits and boundary readouts do not couple to it.",
            "proof_status": "REQUIRED_GUARD_UNSIGNED",
            "missing_parent_input": "all-sector projective invariance proof or explicit gauge fixing before coupling",
            "use": "prevents using gravitational gauge freedom to hide matter/readout couplings",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSTACK2349_3_no_cancellation",
            "lemma": "projective no-cancellation rule",
            "statement": "Projective source, clock, WEP, orbit and boundary pieces must each be zero or bounded; they cannot cancel against spin/nonmetricity/source terms.",
            "proof_status": "STRUCTURAL_RULE",
            "missing_parent_input": "component values or zero theorems",
            "use": "keeps the GR bridge non-fitted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PSTACK2349_4_parent_contract",
            "lemma": "future parent action contract",
            "statement": "A future parent action must either omit Gamma_ind, gauge-fix projective trace before coupling, or expose a sourced P_projective residual with units and arena maps.",
            "proof_status": "CONTRACT_READY_NOT_SIGNED",
            "missing_parent_input": "common parent action text",
            "use": "acceptance test for the local-GR connection branch",
            "valid_for_claim": "false",
        },
    ]


def build_p4_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_0_projective_total",
            "quantity": "P_projective_abs",
            "component": "total projective trace residual",
            "formula": "P_source_trace_abs + P_clock_trace_abs + P_WEP_trace_abs + P_orbit_trace_abs + P_boundary_trace_abs",
            "units": "projective trace normalization or dimensionless response after projection",
            "current_value": "MISSING_COMPONENT_VALUES",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_1_source_trace",
            "quantity": "P_source_trace_abs",
            "component": "source charge / finite-worldtube trace coupling",
            "formula": "||c_Ps P_mu J_source^mu|| / N_source",
            "units": "dimensionless after source normalization",
            "current_value": "MISSING_SOURCE_TRACE_COUPLING",
            "source_path": "MISSING_PARENT_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_2_clock_trace",
            "quantity": "P_clock_trace_abs",
            "component": "clock/rod projective trace coupling",
            "formula": "||c_Pc P_mu J_clock^mu|| / N_clock",
            "units": "fractional clock or dimensionless response",
            "current_value": "MISSING_CLOCK_TRACE_RESPONSE",
            "source_path": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_3_WEP_trace",
            "quantity": "P_WEP_trace_abs",
            "component": "composition/WEP trace coupling",
            "formula": "||P_projective[source,test_A] - P_projective[source,test_B]||",
            "units": "eta-equivalent or dimensionless WEP response",
            "current_value": "MISSING_WEP_TRACE_KERNEL",
            "source_path": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_4_orbit_trace",
            "quantity": "P_orbit_trace_abs",
            "component": "orbital/GM transfer trace coupling",
            "formula": "||P_projective[orbit, GM, range_law]||",
            "units": "GM, PPN, or fifth-force response after projection",
            "current_value": "MISSING_ORBIT_TRACE_KERNEL",
            "source_path": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_5_boundary_trace",
            "quantity": "P_boundary_trace_abs",
            "component": "boundary/domain projective trace coupling",
            "formula": "||P_projective[boundary, support, projector]||",
            "units": "boundary current or dimensionless envelope",
            "current_value": "MISSING_BOUNDARY_TRACE_KERNEL",
            "source_path": "MISSING_BOUNDARY_NO_FLUX_OR_BOUND",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_6_weak_field_map",
            "quantity": "epsilon_P4_projective_abs",
            "component": "weak-field projective residual mapped to local tests",
            "formula": "epsilon_P4_projective_abs <= K_projective * P_projective_abs",
            "units": "PPN/WEP/clock/orbital residual units after arena projection",
            "current_value": "MISSING_K_PROJECTIVE_AND_RESPONSE_OPERATORS",
            "source_path": "MISSING_ARENA_PROJECTION",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4P2349_7_no_claim",
            "quantity": "local_GR_projective_gate",
            "component": "claim policy",
            "formula": "claim_allowed = Z_projective_global OR sourced_numeric_bound_passes_all_local_arenas",
            "units": "boolean gate",
            "current_value": "FALSE",
            "source_path": "P8_Y5_PARENT_QLOC_2349_CLAIM_GATES.csv",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2349_0_result", "decision": "do not promote global projective trace silence", "reason": "private owned-coframe+SRNG gives zero by variable absence, but global all-sector invariance/gauge-fix is not parent-signed", "consequence": "retain P4 projective component row", "status": "PRIVATE_ZERO_PUBLIC_P4_RETAINED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2349_1_private_use", "decision": "use projective trace as zero inside the private branch only", "reason": "within owned-coframe+SRNG there is no independent Gamma trace direction and source/readout exceptions are switched off privately", "consequence": "private connection residual narrows to boundary/improvement plus parent-signature promotion", "status": "PRIVATE_PROJECTIVE_ZERO_SWITCH", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2349_2_public_fallback", "decision": "treat affine/projective fallback as nonzero unless gauge-fixed or bounded", "reason": "source, clock, WEP, orbit and boundary trace couplings remain live in public/global corpus", "consequence": "P4P2349 rows require coefficients, units, response maps and source paths before scoring", "status": "AFFINE_PROJECTIVE_FALLBACK_EXPLICIT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2349_3_next", "decision": "attack boundary/improvement current next", "reason": "after private SRNG, coframe spin, and projective zero switches, boundary/improvement is the cleanest remaining private-branch local-GR leak", "consequence": "next target is boundary no-flux / Bzero proof or P4 boundary row", "status": "SELECT_BOUNDARY_IMPROVEMENT_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2349_4_public_policy", "decision": "no GitHub update from 2349", "reason": "checkpoint clarifies private/public projective status but does not prove local GR/Newton", "consequence": "continue private derivation work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2349_0_private_projective_zero", "gate": "projective trace zero inside private owned-coframe+SRNG branch", "passed": "true", "claim_effect": "private branch switch only; not valid_for_claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2349_1_global_projective_zero", "gate": "projective trace globally gauge/fixed/unobservable", "passed": "false", "claim_effect": "public P4 projective row retained", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2349_2_all_sector_invariance", "gate": "all matter/source/readout sectors are projectively invariant", "passed": "false", "claim_effect": "source/readout exceptions remain", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2349_3_affine_bound_score_ready", "gate": "projective fallback has values, units, source paths and arena projections", "passed": "false", "claim_effect": "nonclaim placeholder only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2349_4_local_GR_Newton", "gate": "local GR/Newton projective caveat closed publicly", "passed": "false", "claim_effect": "boundary/source/parent-signature gates remain", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2349_0_private_as_public", "claim": "private projective zero proves public/global projective silence", "allowed": "false", "reason": "private owned-coframe+SRNG is not a canonical parent-signed public branch", "blocking_rows": "PROJ2349_1_owned_coframe_private_zero;CG2349_1_global_projective_zero", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2349_1_EH_gauge_hides_matter", "claim": "EH projective gauge freedom alone makes the trace harmless", "allowed": "false", "reason": "matter/source/readout couplings must also be invariant or gauge-fixed before coupling", "blocking_rows": "PROJ2349_4_source_clock_WEP_gap;PSTACK2349_2_all_sector_invariance", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2349_2_orbit_reparam_as_full_readout", "claim": "projective reparameterization invariance closes orbital/clock tests", "allowed": "false", "reason": "physical clock time, source-GM transfer and fitted-G guards are additional readout clauses", "blocking_rows": "PROJ2349_3_unparameterized_orbit_guard;P4P2349_4_orbit_trace", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2349_3_p4_as_pass", "claim": "P4 projective row is an empirical pass", "allowed": "false", "reason": "component values, trace normalization, source paths and arena projections are missing", "blocking_rows": "P4P2349_0_projective_total;P4P2349_6_weak_field_map", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2349_4_local_GR_claim", "claim": "2349 proves local GR/Newton reduction", "allowed": "false", "reason": "2349 closes only private projective trace; public projective, boundary, source and parent signature gates remain", "blocking_rows": "CG2349_4_local_GR_Newton;DEC2349_3_next", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2349_0", "next_target": "2350-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md", "why": "private SRNG/source-readout, coframe spin, and projective trace have usable private zero switches; boundary/improvement is now the sharpest remaining private-branch leakage route", "route_type": "local_GR_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2349_1", "next_target": "2350b-Y5-R2FR-parent-ordinary-action-variable-signature.md", "why": "promotes private zero switches into a parent-signed public branch if the action can be written cleanly", "route_type": "parent_action_contract_parallel", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2349_2", "next_target": "2350c-Y5-R2FR-affine-projective-bound-input-acquisition.md", "why": "fallback route if the owned-coframe branch is rejected or public affine Gamma is retained", "route_type": "fallback_nonclaim", "valid_for_claim": "false"},
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(source.relative_to(ROOT)),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": len(read_csv_rows(destination)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"timestamp_utc": timestamp(), "branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    add("VAL2349_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2349_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2349_02_private_zero_recorded", any(row["row_id"] == "PROJ2349_1_owned_coframe_private_zero" and row["status"] == "ZERO_INSIDE_PRIVATE_BRANCH_ONLY" for row in audit_rows), "projective trace private zero switch recorded")
    add("VAL2349_03_public_fallback_retained", any(row["row_id"] == "PROJ2349_5_verdict" and row["status"] == "PRIVATE_ZERO_PUBLIC_FALLBACK_RETAINED" for row in audit_rows), "public/global projective fallback retained")
    add("VAL2349_04_all_sector_guard_unsigned", any(row["row_id"] == "PSTACK2349_2_all_sector_invariance" and row["proof_status"] == "REQUIRED_GUARD_UNSIGNED" for row in proof_rows), "all-sector invariance guard remains unsigned")
    add("VAL2349_05_p4_rows_nonready", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in p4_rows), "P4 projective rows are non-score-ready and nonclaim")
    add("VAL2349_06_p4_missing_inputs_flagged", any("MISSING_SOURCE_TRACE_COUPLING" in row["current_value"] for row in p4_rows) and any("MISSING_K_PROJECTIVE" in row["current_value"] for row in p4_rows), "P4 rows explicitly flag missing trace coupling and weak-field map")
    private_gate = [row for row in claim_rows if row["row_id"] == "CG2349_0_private_projective_zero"]
    public_gates = [row for row in claim_rows if row["row_id"] != "CG2349_0_private_projective_zero"]
    add("VAL2349_07_claim_gates_blocked_except_private", bool(private_gate and private_gate[0]["passed"] == "true") and all(row["passed"] == "false" for row in public_gates) and all(row["valid_for_claim"] == "false" for row in claim_rows), "only private projective switch passes and remains not valid_for_claim")
    add("VAL2349_08_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2349_09_next_selected", any(row["row_id"] == "NEXT2349_0" and "boundary-improvement" in row["next_target"] for row in next_rows), "boundary/improvement next target recorded")
    add("VAL2349_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, audit_rows, proof_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2349_11_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "PROJECTIVE_TRACE_SILENCE_AUDIT_2349",
        "P4_PROJECTIVE_COMPONENT_ROW_2349",
        "JR2349_PROJECTIVE_TRACE",
        "Y5_R2FR_projective_trace",
    ]
    formalization_hits: list[str] = []
    if FORMALIZATION.exists():
        for needle in checkpoint_needles:
            try:
                result = subprocess.run(["rg", "-n", "--fixed-strings", needle, str(FORMALIZATION)], capture_output=True, text=True, timeout=30, check=False)
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
            if result.returncode == 0 and result.stdout.strip():
                formalization_hits.extend(result.stdout.strip().splitlines())
    add("VAL2349_12_formalization_untouched_by_2349", not formalization_hits, "no 2349 checkpoint output appears in formalization-workbench")
    add("VAL2349_13_no_github_policy", any(row["row_id"] == "DEC2349_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2349")
    add("VAL2349_OVERALL", all(row["status"] == "PASS" for row in rows), "2349 records projective trace zero inside the private owned-coframe+SRNG branch, refuses public promotion, stages P4 projective fallback, and selects boundary/improvement current next.")
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2349 - Projective Trace Silence Or P4 Projective Component Row",
        "",
        "## Summary",
        "",
        "2349 handles the projective trace caveat left by the local connection branch.",
        "",
        "Inside the private owned-coframe + SRNG/OFC working branch, the result is clean: there is no",
        "independent `Gamma_ind`, source/readout trace exceptions are privately excluded, and therefore the",
        "projective trace has no physical variable direction. So `Delta_projective_private = 0` is usable inside",
        "that private branch.",
        "",
        "Publicly, this is not yet a claim. If an affine/Palatini branch is retained, projective gauge freedom is",
        "harmless only after all matter, source, clock, light, orbit and boundary readouts are invariant or gauge-fixed",
        "before coupling. That all-sector certificate is still missing, so the P4 projective row remains live.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Projective Trace Silence Audit",
        "",
        markdown_table(audit_rows, ["row_id", "clause", "formal_statement", "status", "obstruction", "effect_if_closed", "valid_for_claim"]),
        "",
        "## Projective Proof Stack",
        "",
        markdown_table(proof_rows, ["row_id", "lemma", "statement", "proof_status", "missing_parent_input", "use", "valid_for_claim"]),
        "",
        "## P4 Projective Component Row",
        "",
        markdown_table(p4_rows, ["row_id", "quantity", "component", "formula", "units", "current_value", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "route_type", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = build_sources()
    audit_rows = build_audit_rows()
    proof_rows = build_proof_rows()
    p4_rows = build_p4_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit_rows)
    write_csv(OUTPUTS["proof"], proof_rows)
    write_csv(OUTPUTS["p4"], p4_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(sources, audit_rows, proof_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(sources, audit_rows, proof_rows, p4_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows, validation_rows)
    print(f"2349 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
