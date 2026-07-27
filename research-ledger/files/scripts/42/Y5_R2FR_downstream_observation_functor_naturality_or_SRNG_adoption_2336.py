from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_DOWNSTREAM_OBSERVATION_FUNCTOR_OR_SRNG_ADOPTION_2336"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md"

PATHS = {
    "2335_doc": ROOT / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md",
    "2335_validation": OUT / "P8_Y5_BRR545_2335_VALIDATION.csv",
    "2335_next": OUT / "P8_Y5_PARENT_QLOC_2335_NEXT_TARGET.csv",
    "2335_certificate": OUT / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
    "2335_theorem": OUT / "P8_Y5_PARENT_QLOC_2335_SRNG_THEOREM_ATTEMPT.csv",
    "637_obs": OUT / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv",
    "943_doc": ROOT / "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md",
    "944_doc": ROOT / "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md",
    "1003_frame": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
    "1016_worldtube": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "1963_action": OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv",
    "2330_restriction": OUT / "P8_Y5_PARENT_QLOC_2330_PARENT_ACTION_RESTRICTION_DRAFT.csv",
}

SOURCES = [
    ("SRC2336_00_2335_doc", "2335_doc", PATHS["2335_doc"], ["NEXT2335_0", "downstream observation functor naturality"], "2335 handoff"),
    ("SRC2336_01_2335_validation", "2335_validation", PATHS["2335_validation"], ["VAL2335_OVERALL", "PASS"], "2335 validation"),
    ("SRC2336_02_2335_next", "2335_next", PATHS["2335_next"], ["NEXT2335_0", "downstream-observation-functor"], "machine-readable 2336 target"),
    ("SRC2336_03_2335_certificate", "2335_certificate", PATHS["2335_certificate"], ["SRNG2335_6_verdict", "PARTIAL_CERTIFICATE_READY_NOT_DERIVED"], "SRNG certificate status"),
    ("SRC2336_04_2335_theorem", "2335_theorem", PATHS["2335_theorem"], ["THM2335_3_SRNG_sum", "CONDITIONAL_THEOREM_READY"], "SRNG zero effect"),
    ("SRC2336_05_637_obs", "637_obs", PATHS["637_obs"], ["OF637_0_observed_geometry", "conditional_descent"], "observed functor derivation"),
    ("SRC2336_06_943_doc", "943_doc", PATHS["943_doc"], ["CFC943_2_matter_functor", "contract_exact_but_unsigned"], "single observed coframe contract"),
    ("SRC2336_07_944_doc", "944_doc", PATHS["944_doc"], ["QDG944_2_observed_coframe_functor", "QDG944_7_total"], "quotient coframe descent proof attempt"),
    ("SRC2336_08_1003_frame", "1003_frame", PATHS["1003_frame"], ["CFA1003_2_matter_functor", "fail_current_claim"], "same-frame readout caveat"),
    ("SRC2336_09_1016_worldtube", "1016_worldtube", PATHS["1016_worldtube"], ["PSC1016_7_coupling_descent_silence", "DEC1016_1_current_MTS_status"], "source/worldtube selector caveat"),
    ("SRC2336_10_1963_action", "1963_action", PATHS["1963_action"], ["ACT1963_5_no_independent_Gamma_clause", "NO_GAMMA_BY_VARIABLE_SIGNATURE"], "owned-coframe no-Gamma branch"),
    ("SRC2336_11_2330_restriction", "2330_restriction", PATHS["2330_restriction"], ["PAR2330_3_no_hidden_return", "OPEN_PARALLEL_GATE"], "private matter-coupling restriction caveat"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2336_SOURCE_REGISTER.csv",
    "naturality": OUT / "P8_Y5_PARENT_QLOC_2336_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv",
    "contract": OUT / "P8_Y5_PARENT_QLOC_2336_OBSERVATION_FUNCTOR_CONTRACT.csv",
    "adoption": OUT / "P8_Y5_PARENT_QLOC_2336_SRNG_ADOPTION_DECISION_MATRIX.csv",
    "p4": OUT / "P8_Y5_PARENT_QLOC_2336_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2336_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2336_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2336_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2336_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2336_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2336_0_naturality", OUTPUTS["naturality"], BETA_DOCS / "DOWNSTREAM_NATURALITY_DERIVATION_AUDIT_2336_NONCLAIM.csv"),
    ("COPY2336_1_adoption", OUTPUTS["adoption"], RAB_QUEUE / "JR2336_SRNG_ADOPTION_DECISION_MATRIX_NONCLAIM.csv"),
    ("COPY2336_2_p4", OUTPUTS["p4"], MICRO_RESIDUALS / "P4_residual_status_after_SRNG_adoption_2336_nonclaim.csv"),
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


def build_naturality_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_0_target",
            "derivation_piece": "derive SRNG from downstream observation functor naturality",
            "formal_statement": "If observations are natural functors O_i: Sol(Q_obs)->Readout_i evaluated after the variational problem, then O_i cannot add Gamma_ind to S_parent.",
            "status": "TARGET_SHARPENED",
            "proof_gain": "turns readout silence from an ad hoc clause into functorial bookkeeping",
            "obstruction": "must prove readouts are not hidden action/source terms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_1_quotient_domain",
            "derivation_piece": "observed quotient domain",
            "formal_statement": "q: Phi_parent -> Q_obs is fixed before readout, and e_obs/g_obs/omega_LC[e_obs] are functors of Q_obs.",
            "status": "CONDITIONAL_FROM_637_943_944",
            "proof_gain": "readouts can depend on observed fields without depending on representative/Gamma slots",
            "obstruction": "q and full observed coframe descent remain not parent-signed in the current corpus",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_2_downstream_separation",
            "derivation_piece": "action/readout separation",
            "formal_statement": "S_parent is varied over dynamical fields first; O_clock, O_light, O_orbit and detector readouts are maps on solutions, not extra action terms.",
            "status": "EXACT_IF_PARENT_OBSERVATION_POLICY_SIGNED",
            "proof_gain": "delta O_i/delta Gamma_ind is irrelevant to hypermomentum because O_i is not in S_parent",
            "obstruction": "instrument backreaction and marker/domain selection must be included as ordinary matter or residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_3_naturality",
            "derivation_piece": "naturality under vertical/gauge maps",
            "formal_statement": "For v in ker(Dq), O_i(q(Phi)) is invariant: delta_v O_i = D O_i[Dq(v)] = 0.",
            "status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "proof_gain": "kills fake readout-frame dependence without fitting",
            "obstruction": "actual MTS vertical directions and no-shadow-frame clauses are still conditional",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_4_source_selector",
            "derivation_piece": "source/worldtube selector",
            "formal_statement": "W_source=closure(supp J_H[tau]) is legal only when the source worldtube is selected from the same Hilbert/coframe matter current before readout.",
            "status": "CONDITIONAL_NOT_CLOSED",
            "proof_gain": "prevents measured GM/source support from becoming a post-readout mask",
            "obstruction": "compactness, M_H_ref, tau/frame lock, boundary/reference and coupling descent are unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_5_orbit_readout",
            "derivation_piece": "test-body and orbit readout",
            "formal_statement": "A trajectory readout is admissible only as a downstream limit of the same matter action; an independent autoparallel Gamma_ind law is a new coupling.",
            "status": "EXACT_CONDITIONAL_FILTER",
            "proof_gain": "blocks importing GR geodesics by words while keeping a derivable route",
            "obstruction": "finite-body marker/domain and test-body limit not yet written as parent data",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_6_boundary_projective_limit",
            "derivation_piece": "boundary and projective limitation",
            "formal_statement": "Downstream functor naturality does not itself kill boundary/improvement flux or projective trace coupling.",
            "status": "LIMIT_EXPLICIT",
            "proof_gain": "stops SRNG from eating a separate residual channel",
            "obstruction": "Delta_boundary and Delta_projective require their own zero proof or P4 policy",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DNF2336_7_verdict",
            "derivation_piece": "derive SRNG now",
            "formal_statement": "DNF2336_1 through DNF2336_5 would derive SRNG for source/readout sectors if parent-signed together.",
            "status": "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED",
            "proof_gain": "SRNG is now grounded in a precise downstream-functor theorem shape",
            "obstruction": "current corpus has contracts and conditional lemmas, not the full parent observation policy",
            "valid_for_claim": "false",
        },
    ]


def build_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFC2336_0_domain",
            "contract_piece": "observation functor domain",
            "clause": "Readouts are maps O_i: Sol(Q_obs, boundary data, theta)->Reported_i.",
            "effect": "readouts depend on solved observed fields, not on hidden parent representatives",
            "status": "CONTRACT_WRITTEN_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFC2336_1_action_separation",
            "contract_piece": "no readout in parent variation",
            "clause": "O_i is not an argument of S_parent and contributes no Euler-Lagrange or hypermomentum current.",
            "effect": "clock/light/orbit readout cannot create Delta_i unless promoted to apparatus matter or residual",
            "status": "CONTRACT_WRITTEN_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFC2336_2_vertical_invariance",
            "contract_piece": "vertical invariance",
            "clause": "If Dq(v)=0, then delta_v O_i=0 for all ordinary readouts.",
            "effect": "readout frame dependence is forbidden unless it descends through Q_obs or is residualized",
            "status": "EXACT_IF_Q_NATURALITY_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFC2336_3_no_gamma_slot",
            "contract_piece": "no independent Gamma in readout",
            "clause": "O_i may use g_obs/e_obs and omega_LC[e_obs], but not Gamma_ind as an independent probe variable.",
            "effect": "turns SRNG into a consequence of observation object language",
            "status": "CONTRACT_WRITTEN_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFC2336_4_apparatus_backreaction",
            "contract_piece": "apparatus backreaction rule",
            "clause": "If an instrument changes the source, it is included in ordinary matter/source action before variation; if not, it remains downstream.",
            "effect": "prevents sneaking source-current physics into a measurement map",
            "status": "CONTRACT_WRITTEN_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OFC2336_5_status",
            "contract_piece": "contract status",
            "clause": "OFC2336 is suitable as a private working parent-observation clause, not as a public derivation.",
            "effect": "supports disciplined local-branch development while retaining proof debt",
            "status": "PRIVATE_CONTRACT_READY_NOT_DERIVED",
            "valid_for_claim": "false",
        },
    ]


def build_adoption_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2336_0_derivation_route",
            "option": "derive SRNG from q-natural downstream observation",
            "status": "BEST_ROUTE_BUT_NOT_CLOSED",
            "reason": "requires parent-signed q, observation policy, same-frame/tau/source selector and no-shadow clauses",
            "allowed_use": "future theorem target only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2336_1_private_adoption",
            "option": "adopt SRNG/OFC as private working parent-action/observation clause",
            "status": "RECOMMENDED_PRIVATE_WORKING_CLAUSE",
            "reason": "it is minimal, non-fitted, and blocks Gamma/readout leakage without altering data by hand",
            "allowed_use": "internal local-branch calculations with explicit nonclaim label",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2336_2_reject_or_unresolved",
            "option": "do not adopt SRNG",
            "status": "FALLBACK_TO_P4_COMPONENT_BOUNDS",
            "reason": "then Delta_source/clock/light/orbit must be bounded with units and projection maps",
            "allowed_use": "P4 residual row fill only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2336_3_decision",
            "option": "dual track",
            "status": "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT",
            "reason": "use SRNG internally as a named clause while continuing to derive it; never count it as public GR/Newton proof",
            "allowed_use": "next checkpoint may use SRNG-gated branch and separately attack boundary/projective residuals",
            "valid_for_claim": "false",
        },
    ]


def build_p4_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "P4A2336_0_SRNG_effect", "component": "Delta_source+Delta_clock+Delta_light+Delta_orbit", "status_if_private_SRNG_used": "THEOREM_ZERO_INSIDE_PRIVATE_BRANCH_ONLY", "status_if_SRNG_rejected": "REQUIRES_P4_BOUNDS", "still_live": "false_inside_private_branch_true_publicly", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4A2336_1_spin", "component": "Delta_spin", "status_if_private_SRNG_used": "UNCHANGED", "status_if_SRNG_rejected": "UNCHANGED", "still_live": "true", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4A2336_2_boundary", "component": "Delta_boundary", "status_if_private_SRNG_used": "STILL_REQUIRES_BOUNDARY_CERTIFICATE", "status_if_SRNG_rejected": "STILL_REQUIRES_BOUNDARY_CERTIFICATE", "still_live": "true", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4A2336_3_projective", "component": "Delta_projective", "status_if_private_SRNG_used": "STILL_REQUIRES_PROJECTIVE_POLICY", "status_if_SRNG_rejected": "STILL_REQUIRES_PROJECTIVE_POLICY", "still_live": "true", "score_ready": "false", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "P4A2336_4_reduced_total", "component": "Delta_abs_private_SRNG_branch", "status_if_private_SRNG_used": "Delta_abs -> Delta_matter/private + Delta_spin + Delta_boundary + Delta_projective", "status_if_SRNG_rejected": "full Delta_abs component queue retained", "still_live": "true", "score_ready": "false", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2336_0_naturality_derived", "gate": "downstream observation naturality derived from parent MTS", "passed": "false", "claim_effect": "conditional theorem only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2336_1_SRNG_public", "gate": "SRNG is public active theorem", "passed": "false", "claim_effect": "private working clause only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2336_2_source_readout_zero_public", "gate": "Delta_source/clock/light/orbit zero for public claim", "passed": "false", "claim_effect": "zero only inside private adopted branch", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2336_3_boundary_projective_closed", "gate": "boundary/projective residuals closed", "passed": "false", "claim_effect": "still live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2336_4_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "connection subgate improved but not complete", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2336_5_github", "gate": "safe public evidence update", "passed": "false", "claim_effect": "no GitHub evidence update", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2336_0_private_as_public", "claim": "private SRNG adoption proves local GR publicly", "allowed": "false", "reason": "private adoption is a named working clause, not a derivation from parent MTS", "blocking_rows": "ADM2336_1_private_adoption;CG2336_1_SRNG_public", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2336_1_readout_backreaction_ignored", "claim": "all measurement apparatus is downstream by definition", "allowed": "false", "reason": "apparatus that changes the source must be included as matter/source before variation or residualized", "blocking_rows": "OFC2336_4_apparatus_backreaction", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2336_2_boundary_eaten_by_SRNG", "claim": "SRNG removes boundary and projective terms", "allowed": "false", "reason": "downstream observation naturality does not kill integration-boundary or projective trace channels", "blocking_rows": "DNF2336_6_boundary_projective_limit;P4A2336_2_boundary;P4A2336_3_projective", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2336_3_import_orbits", "claim": "orbit equations can be imported from GR geodesics", "allowed": "false", "reason": "orbit readout must come from the Hilbert/coframe test-body limit or remain a P4 residual", "blocking_rows": "DNF2336_5_orbit_readout", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2336_0",
            "next_target": "2337-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md",
            "why": "with SRNG available as a private working clause, the live connection residuals reduce to spin, boundary/improvement and projective trace.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2336_1",
            "next_target": "2337b-Y5-R2FR-parent-observation-policy-derivation.md",
            "why": "pure derivation route: try to parent-sign q-natural downstream observation instead of adopting it.",
            "claim_status": "parallel_derivation_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2336_2",
            "next_target": "2337c-Y5-R2FR-P4-source-readout-component-bounds-if-SRNG-rejected.md",
            "why": "fallback route if private SRNG is rejected: fill Delta_source/clock/light/orbit units and bounds.",
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

    add("VAL2336_00_required_sources_exist", all(row["exists"] == "true" for row in required_sources), "every required source path exists")
    add("VAL2336_01_required_needles_found", all(row["needles_found"] == "true" for row in required_sources), "all required source needles were found")
    nat_rows = read_csv_rows(OUTPUTS["naturality"])
    add("VAL2336_02_naturality_not_closed", any(row.get("row_id") == "DNF2336_7_verdict" and row.get("status") == "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED" for row in nat_rows), "downstream naturality remains conditional")
    contract_rows = read_csv_rows(OUTPUTS["contract"])
    add("VAL2336_03_observation_contract_written", any(row.get("row_id") == "OFC2336_5_status" and row.get("status") == "PRIVATE_CONTRACT_READY_NOT_DERIVED" for row in contract_rows), "observation functor contract written as private nonclaim")
    adoption_rows = read_csv_rows(OUTPUTS["adoption"])
    add("VAL2336_04_private_adoption_selected", any(row.get("row_id") == "ADM2336_3_decision" and row.get("status") == "PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT" for row in adoption_rows), "private SRNG/OFC adoption selected with derivation audit")
    p4_rows = read_csv_rows(OUTPUTS["p4"])
    add("VAL2336_05_boundary_projective_still_live", any(row.get("row_id") == "P4A2336_2_boundary" and row.get("still_live") == "true" for row in p4_rows) and any(row.get("row_id") == "P4A2336_3_projective" and row.get("still_live") == "true" for row in p4_rows), "boundary and projective residuals remain live")
    add("VAL2336_06_p4_nonready", all(row.get("score_ready") == "false" for row in p4_rows), "P4 residual rows remain non-score-ready")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2336_07_local_claims_block", any(row.get("row_id") == "CG2336_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2336_08_github_blocked", any(row.get("row_id") == "CG2336_5_github" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended from 2336")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2336_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    next_rows = read_csv_rows(OUTPUTS["next"])
    add("VAL2336_10_next_boundary_projective", any(row.get("row_id") == "NEXT2336_0" and "boundary-projective" in row.get("next_target", "") for row in next_rows), "boundary/projective residual split selected next")
    add("VAL2336_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")

    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2336_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2336*.csv", "*2336*.md", "*SRNG*2336*", "*DOWNSTREAM*NATURALITY*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2336_13_formalization_untouched_by_2336", not formalization_hits, "no 2336 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2336_OVERALL", all(row["status"] == "PASS" for row in rows), "2336 derives the downstream observation functor route as a sharp conditional, adopts SRNG/OFC only as a private working clause, keeps public local-GR/Newton claims blocked, and selects boundary/projective residual splitting next.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    naturality_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    adoption_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2336 - downstream observation functor naturality or SRNG adoption

## Summary

2336 tries to derive the SRNG clause from a cleaner principle:

`readouts are downstream natural functors of the observed quotient solution`.

That gives a real conditional theorem: if clocks, light, orbits and detectors are maps on solved `Q_obs` fields,
not extra action/current terms, then they cannot source an independent `Gamma_ind`.

Current result: the theorem shape is clean, but current MTS has not parent-signed the full observation policy.
So 2336 makes a deliberate private move: adopt SRNG/OFC as a **private working clause**, not a public derivation.
Inside that private branch, source/readout Gamma leakage is switched off by contract. Publicly, it remains proof debt.

The next live residuals are now sharper: spin, boundary/improvement, and projective trace.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Downstream Naturality Derivation Audit

{markdown_table(naturality_rows, ["row_id", "derivation_piece", "formal_statement", "status", "proof_gain", "obstruction", "valid_for_claim"])}

## Observation Functor Contract

{markdown_table(contract_rows, ["row_id", "contract_piece", "clause", "effect", "status", "valid_for_claim"])}

## SRNG Adoption Decision Matrix

{markdown_table(adoption_rows, ["row_id", "option", "status", "reason", "allowed_use", "valid_for_claim"])}

## P4 Residual Status After SRNG Adoption

{markdown_table(p4_rows, ["row_id", "component", "status_if_private_SRNG_used", "status_if_SRNG_rejected", "still_live", "score_ready", "valid_for_claim"])}

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
        "naturality": build_naturality_rows(),
        "contract": build_contract_rows(),
        "adoption": build_adoption_rows(),
        "p4": build_p4_rows(),
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
        rows_by_output["naturality"],
        rows_by_output["contract"],
        rows_by_output["adoption"],
        rows_by_output["p4"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2336 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
