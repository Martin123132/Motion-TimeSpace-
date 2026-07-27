from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_READOUT_NOGAMMA_ARGUMENT_CERTIFICATE_2335"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md"

PATHS = {
    "2334_doc": ROOT / "2334-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md",
    "2334_validation": OUT / "P8_Y5_BRR545_2334_VALIDATION.csv",
    "2334_next": OUT / "P8_Y5_PARENT_QLOC_2334_NEXT_TARGET.csv",
    "2334_slots": OUT / "P8_Y5_PARENT_QLOC_2334_GAMMA_SLOT_SECTOR_AUDIT.csv",
    "2334_p4_queue": OUT / "P8_Y5_PARENT_QLOC_2334_P4_DELTA_COMPONENT_QUEUE.csv",
    "1963_action": OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv",
    "1963_no_gamma": OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv",
    "2329_signature": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv",
    "2330_restriction": OUT / "P8_Y5_PARENT_QLOC_2330_PARENT_ACTION_RESTRICTION_DRAFT.csv",
    "2331_nonhilbert": OUT / "P8_Y5_PARENT_QLOC_2331_NONHILBERT_RESIDUAL_ROW.csv",
    "1016_worldtube": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "1003_frame": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
}

SOURCES = [
    ("SRC2335_00_2334_doc", "2334_doc", PATHS["2334_doc"], ["NEXT2334_0", "source/readout action-argument certificate"], "2334 handoff"),
    ("SRC2335_01_2334_validation", "2334_validation", PATHS["2334_validation"], ["VAL2334_OVERALL", "PASS"], "2334 validation"),
    ("SRC2335_02_2334_next", "2334_next", PATHS["2334_next"], ["NEXT2334_0", "action-argument-certificate"], "machine-readable 2335 target"),
    ("SRC2335_03_2334_slots", "2334_slots", PATHS["2334_slots"], ["NGSA2334_4_source_worldtube", "NGSA2334_5_clock_readout"], "source/readout no-Gamma slots"),
    ("SRC2335_04_2334_p4_queue", "2334_p4_queue", PATHS["2334_p4_queue"], ["P4DQ2334_3_source", "P4DQ2334_6_orbit"], "P4 Delta component queue"),
    ("SRC2335_05_1963_action", "1963_action", PATHS["1963_action"], ["ACT1963_5_no_independent_Gamma_clause", "NO_GAMMA_BY_VARIABLE_SIGNATURE"], "owned-coframe no-Gamma branch"),
    ("SRC2335_06_1963_no_gamma", "1963_no_gamma", PATHS["1963_no_gamma"], ["NGT1963_0_theorem", "CONDITIONAL_PROOF_VALID"], "variable-absence theorem"),
    ("SRC2335_07_2329_signature", "2329_signature", PATHS["2329_signature"], ["SBF2329_1_source_blind_functor", "CORE_SIGNATURE_WRITTEN"], "source-blind matter functor"),
    ("SRC2335_08_2330_restriction", "2330_restriction", PATHS["2330_restriction"], ["PAR2330_3_no_hidden_return", "OPEN_PARALLEL_GATE"], "hidden-return caveat"),
    ("SRC2335_09_2331_nonhilbert", "2331_nonhilbert", PATHS["2331_nonhilbert"], ["NHR2331_3_readout_reentry", "MISSING_ZERO_OR_ENVELOPE"], "readout re-entry residual"),
    ("SRC2335_10_1016_worldtube", "1016_worldtube", PATHS["1016_worldtube"], ["PSC1016_7_coupling_descent_silence", "FIS1016_6_coupling_descent_certificate"], "worldtube/source-measure selector"),
    ("SRC2335_11_1003_frame", "1003_frame", PATHS["1003_frame"], ["CFA1003_2_matter_functor", "all ordinary readouts use the same descended coframe"], "same-frame readout caveat"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2335_SOURCE_REGISTER.csv",
    "certificate": OUT / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2335_SRNG_THEOREM_ATTEMPT.csv",
    "p4_status": OUT / "P8_Y5_PARENT_QLOC_2335_P4_DELTA_STATUS_AFTER_SRNG.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2335_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2335_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2335_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2335_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2335_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2335_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2335_0_certificate", OUTPUTS["certificate"], BETA_DOCS / "SOURCE_READOUT_NOGAMMA_ARGUMENT_CERTIFICATE_2335_NONCLAIM.csv"),
    ("COPY2335_1_p4_status", OUTPUTS["p4_status"], MICRO_RESIDUALS / "P4_delta_status_after_SRNG_2335_nonclaim.csv"),
    ("COPY2335_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2335_SRNG_DECISION_LEDGER_NONCLAIM.csv"),
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


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
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


def build_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_0_total_clause",
            "sector": "total source/readout branch",
            "object_type": "parent-action restriction",
            "allowed_arguments": "S_source uses Psi_src,e_obs,omega_LC[e_obs],A_owned,theta_src; O_clock/O_light/O_orbit/O_readout are downstream functors of solved observed fields",
            "forbidden_arguments": "Gamma_ind; source-only affine current; fitted readout mask inside variation; independent autoparallel law",
            "certificate_clause": "Source-Readout No-Gamma (SRNG): no source/readout object appears in the variational action with Gamma_ind as an argument.",
            "status": "CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED",
            "closes_delta": "Delta_source+Delta_clock+Delta_light+Delta_orbit",
            "remaining_gap": "parent adoption or deeper quotient/naturality derivation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_1_source_worldtube",
            "sector": "source worldtube and GM support",
            "object_type": "source action / support selector",
            "allowed_arguments": "W_source=closure(supp J_H[tau]); J_H from same Hilbert/coframe matter action; compact support and fixed linking surfaces",
            "forbidden_arguments": "Gamma_ind current; fitted radius/source mask; boundary torsion; post-readout GM rescaling",
            "certificate_clause": "source support is selected from the Hilbert current of the same Gamma-free matter action, not by a new connection-sensitive source law",
            "status": "CONDITIONAL_FROM_WORLDTUBE_SELECTOR_NOT_SIGNED",
            "closes_delta": "Delta_source",
            "remaining_gap": "compactness, boundary/reference lock, M_H_ref and coupling descent are not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_2_clock",
            "sector": "clock and frequency readout",
            "object_type": "downstream observation functor",
            "allowed_arguments": "O_clock[solution fields, e_obs, A_owned, theta_clock, tau]",
            "forbidden_arguments": "Gamma_ind probe term; source-labelled clock current; separate clock frame",
            "certificate_clause": "clock readout is not a term in S_ord; it reads the same solved observed coframe/gauge branch",
            "status": "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "closes_delta": "Delta_clock",
            "remaining_gap": "clock model and tau/frame lock still need explicit parent signature",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_3_light",
            "sector": "light, EM, Shapiro and deflection readout",
            "object_type": "EM action plus downstream null/ray readout",
            "allowed_arguments": "A_owned, e_obs/g_obs, omega_LC[e_obs], detector constants; WKB/null readout after variation",
            "forbidden_arguments": "affine Gamma_ind as optical connection; independent ray-autoparallel postulate",
            "certificate_clause": "light propagation is owned by EM/gauge plus metric/coframe readout, not by an independent affine connection",
            "status": "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "closes_delta": "Delta_light",
            "remaining_gap": "Maxwell/WKB and detector readout need parent-side statement in MTS language",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_4_orbit",
            "sector": "orbital/test-body readout",
            "object_type": "test-body limit / downstream trajectory readout",
            "allowed_arguments": "point/compact body action from same e_obs/g_obs matter branch; trajectory readout after variation",
            "forbidden_arguments": "independent Gamma_ind autoparallel law; fitted orbit frame; marker current inside source variation",
            "certificate_clause": "test-body motion must be the limit of Hilbert/coframe matter, not an added affine-autoparallel rule",
            "status": "CONTRACT_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "closes_delta": "Delta_orbit",
            "remaining_gap": "test-body reduction and marker/domain map still need parent certificate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_5_boundary",
            "sector": "boundary/domain/improvement",
            "object_type": "support and integration boundary policy",
            "allowed_arguments": "fixed compact support, exact/projected-silent improvement, fixed reference boundary data",
            "forbidden_arguments": "Gamma-sensitive boundary current; readout-selected domain; cancellation by sign",
            "certificate_clause": "boundary terms do not enter Delta_abs if compact support and improvement flux are parent-fixed or projected exact",
            "status": "NOT_CLOSED_REQUIRES_SEPARATE_BOUNDARY_CERTIFICATE",
            "closes_delta": "Delta_boundary",
            "remaining_gap": "worldtube flux and improvement current zero theorem/bound is still live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2335_6_verdict",
            "sector": "all source/readout sectors",
            "object_type": "certificate verdict",
            "allowed_arguments": "source/readout can be made Gamma-free by SRNG as a single parent clause",
            "forbidden_arguments": "calling SRNG derived before quotient/naturality or parent adoption is signed",
            "certificate_clause": "SRNG is a clean parent-action contract that would zero Delta_source/clock/light/orbit, but it is not yet derived from deeper MTS primitives",
            "status": "PARTIAL_CERTIFICATE_READY_NOT_DERIVED",
            "closes_delta": "conditional: Delta_source+Delta_clock+Delta_light+Delta_orbit",
            "remaining_gap": "derive SRNG from quotient/naturality or adopt it as a private working parent clause; boundary/projective remain separate",
            "valid_for_claim": "false",
        },
    ]


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "THM2335_0_downstream_readout",
            "claim_piece": "downstream readout lemma",
            "statement": "If O_i is evaluated after solving the variational problem and is not an action/current term, then O_i does not contribute delta S/delta Gamma_ind.",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "obstruction": "must prove clocks/light/orbits are downstream functors, not hidden action/source terms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THM2335_1_hilbert_source_selector",
            "claim_piece": "Hilbert source selector lemma",
            "statement": "If W_source is selected from the support of the Hilbert current of the same Gamma-free matter action, it introduces no independent Gamma source current.",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "obstruction": "compactness, M_H_ref, boundary/reference lock and same-frame tau are unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THM2335_2_orbit_test_body",
            "claim_piece": "test-body no-autoparallel lemma",
            "statement": "If test-body motion is a limit of the same Hilbert/coframe matter action, an independent Gamma_ind autoparallel law is inadmissible.",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "obstruction": "test-body limit and marker/domain maps must be written in parent variables",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THM2335_3_SRNG_sum",
            "claim_piece": "SRNG zero sum",
            "statement": "Under SRNG plus the 1963 no-Gamma matter branch, Delta_source=Delta_clock=Delta_light=Delta_orbit=0 without cancellation.",
            "result": "CONDITIONAL_THEOREM_READY",
            "obstruction": "SRNG is written here as a contract, not derived or adopted as active MTS parent action",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "THM2335_4_boundary_warning",
            "claim_piece": "boundary warning",
            "statement": "SRNG does not by itself kill boundary/improvement/projective trace residuals unless those are separately fixed, exact, gauge, or bounded.",
            "result": "LIMIT_EXPLICIT",
            "obstruction": "Delta_boundary and Delta_projective remain live",
            "valid_for_claim": "false",
        },
    ]


def build_p4_status_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_0_source", "component": "Delta_source", "status_after_SRNG": "ZERO_IF_SRNG_PARENT_SIGNED_ELSE_BOUND", "current_status": "SRNG_CONTRACT_NOT_SIGNED", "needed_for_score": "source/worldtube no-Gamma adoption or finite source-current bound", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_1_clock", "component": "Delta_clock", "status_after_SRNG": "ZERO_IF_DOWNSTREAM_CLOCK_FUNCTOR_SIGNED_ELSE_BOUND", "current_status": "CLOCK_ARGUMENT_LIST_NOT_SIGNED", "needed_for_score": "clock readout parent functor or frequency residual bound", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_2_light", "component": "Delta_light", "status_after_SRNG": "ZERO_IF_EM_LIGHT_READOUT_SIGNED_ELSE_BOUND", "current_status": "LIGHT_ARGUMENT_LIST_NOT_SIGNED", "needed_for_score": "EM/WKB/null readout certificate or PPN light bound", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_3_orbit", "component": "Delta_orbit", "status_after_SRNG": "ZERO_IF_TEST_BODY_LIMIT_SIGNED_ELSE_BOUND", "current_status": "ORBIT_ARGUMENT_LIST_NOT_SIGNED", "needed_for_score": "test-body/marker parent map or orbital residual bound", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_4_boundary", "component": "Delta_boundary", "status_after_SRNG": "STILL_OPEN_SEPARATE_CERTIFICATE", "current_status": "BOUNDARY_ZERO_OR_BOUND_MISSING", "needed_for_score": "boundary no-flux/improvement theorem or source-backed bound", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_5_projective", "component": "Delta_projective", "status_after_SRNG": "STILL_OPEN_PARALLEL_CERTIFICATE", "current_status": "PROJECTIVE_TRACE_POLICY_MISSING", "needed_for_score": "projective gauge/fixed/unobservable certificate or residual policy", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4S2335_6_reduced_total", "component": "Delta_abs_reduced", "status_after_SRNG": "IF_SRNG_AND_MATTER_BRANCH_SIGNED_THEN_REDUCE_TO_DELTA_SPIN_BOUNDARY_PROJECTIVE", "current_status": "REDUCTION_CONDITIONAL_ONLY", "needed_for_score": "SRNG adoption plus spin/boundary/projective closure", "score_ready": "false", "valid_for_claim": "false"},
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2335_0_SRNG_contract", "decision": "SRNG source-readout no-Gamma contract is now explicit", "reason": "it forbids Gamma_ind in source/readout actions and keeps clocks/light/orbits downstream", "consequence": "several leak paths can close together if adopted or derived", "status": "CONTRACT_READY_NONCLAIM", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2335_1_no_public_promotion", "decision": "do not promote SRNG as current MTS theorem", "reason": "contract is written but not derived from deeper quotient/naturality or adopted in formal spine", "consequence": "no local-GR/Newton/WEP/PPN claim", "status": "NO_PROMOTION", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2335_2_best_next", "decision": "try to derive downstream observation functor naturality next", "reason": "if q/naturality forces readouts downstream, SRNG becomes less axiomatic", "consequence": "otherwise adopt SRNG privately or fill P4 component bounds", "status": "SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2335_3_public_policy", "decision": "no GitHub evidence update", "reason": "this is a private contract/derivation gate", "consequence": "continue in post-checkpoint-work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2335_0_SRNG_active", "gate": "SRNG active in parent action", "passed": "false", "claim_effect": "contract only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2335_1_source_readout_zero", "gate": "Delta_source/clock/light/orbit theorem-zero", "passed": "false", "claim_effect": "zero only if SRNG parent-signed", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2335_2_boundary_projective", "gate": "boundary/projective residuals closed", "passed": "false", "claim_effect": "still open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2335_3_P4_score", "gate": "P4 components score-ready", "passed": "false", "claim_effect": "no numeric units/maps/bounds yet", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2335_4_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "connection/EH/GM gates remain", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2335_5_github", "gate": "safe public evidence update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2335_0_contract_as_derivation", "claim": "SRNG is derived from MTS now", "allowed": "false", "reason": "2335 writes the exact contract but does not derive it from deeper q/naturality", "blocking_rows": "SRNG2335_6_verdict;DEC2335_1_no_public_promotion", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2335_1_ignore_boundary", "claim": "source/readout no-Gamma also closes boundary/projective terms", "allowed": "false", "reason": "boundary/improvement and projective trace are separate residual channels", "blocking_rows": "P4S2335_4_boundary;P4S2335_5_projective", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2335_2_autoparallel_import", "claim": "orbits use LC because GR says so", "allowed": "false", "reason": "test-body motion must be derived as the Hilbert/coframe matter limit or residualized", "blocking_rows": "SRNG2335_4_orbit;THM2335_2_orbit_test_body", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2335_3_local_gr", "claim": "2335 proves local GR/Newton", "allowed": "false", "reason": "SRNG would close one connection subgate only; EH, GM normalization, boundary and projective gates remain", "blocking_rows": "CG2335_4_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2335_0",
            "next_target": "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
            "why": "best derivation route: prove clocks/light/orbits/readouts are downstream natural functors of q-observed fields, not new source-current arguments.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2335_1",
            "next_target": "2336b-Y5-R2FR-boundary-projective-residual-split.md",
            "why": "even if SRNG is adopted, boundary/improvement and projective trace need their own zero proof or P4 residual policy.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2335_2",
            "next_target": "2336c-Y5-R2FR-P4-source-readout-component-bounds.md",
            "why": "fallback route if SRNG is rejected or remains unsigned: fill Delta_source/clock/light/orbit units, maps and source-backed bounds.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    required_sources = [row for row in source_rows if row["required"] == "true"]

    add("VAL2335_00_required_sources_exist", all(row["exists"] == "true" for row in required_sources), "every required source path exists")
    add("VAL2335_01_required_needles_found", all(row["needles_found"] == "true" for row in required_sources), "all required source needles were found")
    certificate_rows = read_csv_rows(OUTPUTS["certificate"])
    add("VAL2335_02_SRNG_written", any(row.get("row_id") == "SRNG2335_0_total_clause" and row.get("status") == "CERTIFICATE_WRITTEN_NOT_PARENT_SIGNED" for row in certificate_rows), "SRNG total contract written as nonclaim")
    add("VAL2335_03_SRNG_not_promoted", any(row.get("row_id") == "SRNG2335_6_verdict" and row.get("status") == "PARTIAL_CERTIFICATE_READY_NOT_DERIVED" for row in certificate_rows), "SRNG not promoted as derived")
    theorem_rows = read_csv_rows(OUTPUTS["theorem"])
    add("VAL2335_04_theorem_attempt_limits", any(row.get("row_id") == "THM2335_4_boundary_warning" and row.get("result") == "LIMIT_EXPLICIT" for row in theorem_rows), "boundary/projective limitation explicit")
    p4_rows = read_csv_rows(OUTPUTS["p4_status"])
    required_p4 = {"Delta_source", "Delta_clock", "Delta_light", "Delta_orbit", "Delta_boundary", "Delta_projective"}
    add("VAL2335_05_p4_status_components", required_p4.issubset({row.get("component") for row in p4_rows}), "source/readout/boundary/projective P4 status rows present")
    add("VAL2335_06_p4_nonready", all(row.get("score_ready") == "false" for row in p4_rows), "P4 status rows remain non-score-ready")
    decision_rows = read_csv_rows(OUTPUTS["decision"])
    add("VAL2335_07_next_derivation_selected", any(row.get("row_id") == "DEC2335_2_best_next" and row.get("status") == "SELECT_DOWNSTREAM_FUNCTOR_DERIVATION_NEXT" for row in decision_rows), "downstream observation functor derivation selected next")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2335_08_local_claims_block", any(row.get("row_id") == "CG2335_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2335_09_github_blocked", any(row.get("row_id") == "CG2335_5_github" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended from 2335")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2335_10_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2335_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")

    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2335_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2335*.csv", "*2335*.md", "*SRNG*2335*", "*SOURCE_READOUT*NOGAMMA*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2335_13_formalization_untouched_by_2335", not formalization_hits, "no 2335 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2335_OVERALL", all(row["status"] == "PASS" for row in rows), "2335 writes the SRNG source-readout no-Gamma argument certificate, proves its conditional zero effect, refuses to promote it as derived, keeps boundary/projective/P4 rows live, and selects downstream observation functor naturality next.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    certificate_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    p4_status_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2335 - source-readout noGamma action-argument certificate

## Summary

2335 takes the 2334 leak paths and compresses them into one explicit parent clause:

`SRNG`: source/readout no-Gamma. Source support, clocks, light, orbits and readout maps may use the observed
coframe/metric, `omega_LC[e_obs]`, owned gauge fields, constants and solved fields, but not an independent
`Gamma_ind` argument inside the variational source/action.

This is a real step forward, but still not a public claim. Under SRNG, `Delta_source`, `Delta_clock`, `Delta_light`
and `Delta_orbit` vanish by the same variable-absence theorem. Current status: SRNG is a clean private contract,
not yet derived from deeper quotient/naturality and not yet adopted as the formal parent action.

Boundary/improvement and projective trace remain separate live residuals.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## SRNG Argument Certificate

{markdown_table(certificate_rows, ["row_id", "sector", "object_type", "allowed_arguments", "forbidden_arguments", "status", "closes_delta", "remaining_gap", "valid_for_claim"])}

## SRNG Theorem Attempt

{markdown_table(theorem_rows, ["row_id", "claim_piece", "statement", "result", "obstruction", "valid_for_claim"])}

## P4 Delta Status After SRNG

{markdown_table(p4_status_rows, ["row_id", "component", "status_after_SRNG", "current_status", "needed_for_score", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "certificate": build_certificate_rows(),
        "theorem": build_theorem_rows(),
        "p4_status": build_p4_status_rows(),
        "decision": build_decision_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["certificate"],
        rows_by_output["theorem"],
        rows_by_output["p4_status"],
        rows_by_output["decision"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2335 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
