from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "780-Y5-R10-parent-action-coupling-signature-search-or-local-GR-branch-triage.md"
NEXT_TARGET = "781-Y5-R10-minimal-parent-coupling-owner-action-or-empirical-residual-interface.md"
STATUS = "Y5_R10_780_parent_action_coupling_signature_search_done_only_conditional_hits_local_GR_branch_triaged_nonclaim"
CLAIM_CEILING = "signature_search_and_branch_triage_only_no_parent_coupling_owner_no_coupling_zero_no_source_measure_bound_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_780_SOURCE_REGISTER.csv"
SIGNATURE_SEARCH_PATH = RESIDUALS / "P8_Y5_R10_780_SIGNATURE_SEARCH_LEDGER.csv"
CANDIDATE_SCORECARD_PATH = RESIDUALS / "P8_Y5_R10_780_PARENT_ACTION_CANDIDATE_SCORECARD.csv"
TRIAGE_PATH = RESIDUALS / "P8_Y5_R10_780_LOCAL_GR_BRANCH_TRIAGE.csv"
EMPIRICAL_HANDOFF_PATH = RESIDUALS / "P8_Y5_R10_780_EMPIRICAL_RESIDUAL_HANDOFF.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_780_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_780_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_780_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_780_PARENT_COUPLING_OWNER_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_780_COUPLING_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_780_SOURCE_MEASURE_BOUND_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_780_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SIGNATURE_SEARCH_PATH,
    CANDIDATE_SCORECARD_PATH,
    TRIAGE_PATH,
    EMPIRICAL_HANDOFF_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "779_doc": {
        "path": POST_CHECKPOINT / "779-Y5-R10-parent-coupling-descent-signature-or-source-measure-bound-runner.md",
        "needles": ["D779_3_next_target", "prove the parent coupling owner"],
        "role": "immediate 780 handoff",
        "source_kind": "runner_handoff",
    },
    "779_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_779_VALIDATION.csv",
        "needles": ["V779_6_zero_route_blocked", "V779_10_bound_route_blocked"],
        "role": "prior validation guard",
        "source_kind": "validation",
    },
    "621_normal_form": {
        "path": POST_CHECKPOINT / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
        "needles": ["S_matter = sum_A int det(e_obs)", "not_parent_derived"],
        "role": "ordinary matter normal-form theorem attempt",
        "source_kind": "conditional_theorem_attempt",
    },
    "625_weyl_disformal": {
        "path": POST_CHECKPOINT / "625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md",
        "needles": ["S_matter = Sbar_matter[q(Phi), Psi, theta]", "is not promoted"],
        "role": "representative Weyl/disformal exclusion attempt",
        "source_kind": "conditional_theorem_attempt",
    },
    "632_frame_selector": {
        "path": POST_CHECKPOINT / "632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md",
        "needles": ["quotient_only_zero", "no explicit parent matter-frame source"],
        "role": "matter-frame branch selector",
        "source_kind": "branch_selector",
    },
    "716_source_charge": {
        "path": POST_CHECKPOINT / "716-Y5-R10-matter-coupling-source-charge-derivation-or-free-coefficient-lock.md",
        "needles": ["matter functor factorization", "zero_not_derived"],
        "role": "matter/source charge derivation attempt",
        "source_kind": "derivation_attempt",
    },
    "759_coupling_owner": {
        "path": POST_CHECKPOINT / "759-Y5-R10-coupling-owner-action-or-residual-vector-acquisition-runner.md",
        "needles": ["coupling owner action is not parent-signed yet", "S_matter[Phi_parent,Psi]"],
        "role": "coupling owner audit",
        "source_kind": "owner_audit",
    },
    "762_geometry_stack": {
        "path": POST_CHECKPOINT / "762-Y5-R10-geometry-stack-descent-or-coupling-source-fill.md",
        "needles": ["geometry-stack descent contract written but not parent-signed", "Lie_v S_matter"],
        "role": "geometry-stack descent audit",
        "source_kind": "descent_contract",
    },
    "763_no_marker": {
        "path": POST_CHECKPOINT / "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md",
        "needles": ["no-marker/no-spurion theorem is only a classification theorem shape", "Lie_v S_matter=0"],
        "role": "no-marker/no-spurion theorem attempt",
        "source_kind": "classification_contract",
    },
    "778_theorem_gate": {
        "path": RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_THEOREM_GATE.csv",
        "needles": ["CDT778_7_theorem_result", "conditional_theorem_only_not_current_MTS_claim"],
        "role": "latest conditional descent theorem gate",
        "source_kind": "gate_csv",
    },
    "779_signature_audit": {
        "path": RESIDUALS / "P8_Y5_R10_779_PARENT_COUPLING_SIGNATURE_AUDIT.csv",
        "needles": ["SIG779_0_coupling_descent", "fail_missing_or_nonclaim_inputs"],
        "role": "latest signature audit",
        "source_kind": "gate_csv",
    },
}

SIGNATURES: dict[str, dict[str, Any]] = {
    "SIG780_0_parent_quotient": {
        "label": "parent quotient map and vertical generator",
        "needles": ["q(Phi", "ker(Dq", "quotient"],
        "claim_needs": "explicit q, Dq, vertical generator basis, and gauge quotient proof",
    },
    "SIG780_1_observed_geometry": {
        "label": "one observed coframe/metric",
        "needles": ["e_obs", "g_obs", "observed coframe"],
        "claim_needs": "single parent-owned geometry used by matter/source/clock/photon/orbit/EM",
    },
    "SIG780_2_matter_action": {
        "label": "quotient-invariant matter action",
        "needles": ["S_matter", "Sbar_matter", "Lie_v S_matter"],
        "claim_needs": "actual matter Lagrangian factorized through q(Phi) with no representative dependence",
    },
    "SIG780_3_source_current": {
        "label": "Hilbert source current before measured-GM calibration",
        "needles": ["source current", "J_H", "Hilbert"],
        "claim_needs": "closed projected mass/source current and Gauss/orbital calibration owner",
    },
    "SIG780_4_readout_descent": {
        "label": "clock/photon/orbit/EM/PPN readout descent",
        "needles": ["readout", "clock", "photon", "orbit", "EM", "PPN"],
        "claim_needs": "all readout functionals use e_obs/q(Phi) with no hidden map",
    },
    "SIG780_5_no_hidden_frame": {
        "label": "no hidden Weyl/disformal/marker spurion",
        "needles": ["hidden", "Weyl", "disformal", "marker", "spurion"],
        "claim_needs": "hidden frame, marker, charge-normalization, and species-source weights absent or retained as residuals",
    },
    "SIG780_6_numeric_bound_inputs": {
        "label": "numeric source-measure bound inputs",
        "needles": ["C_qmu", "flux", "M_H", "coefficient", "bound"],
        "claim_needs": "numeric sourced coefficients with units and no-cancellation total",
    },
}

BLOCKER_NEEDLES = [
    "not_parent_signed",
    "not parent-signed",
    "not_parent_derived",
    "not_closed",
    "conditional",
    "blocked",
    "MISSING",
    "not promoted",
    "zero_not_derived",
    "fail_current_corpus",
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "source_kind": spec["source_kind"],
                "exists": bool_string(path.exists()),
                "needle_check": bool_string(text_contains(path, spec["needles"])),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def count_needles(text: str, needles: list[str]) -> tuple[int, str]:
    found = [needle for needle in needles if needle.lower() in text.lower()]
    return len(found), ";".join(found)


def signature_search_rows(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for signature_id, signature in SIGNATURES.items():
        for source_id, spec in SOURCE_SPECS.items():
            path = Path(spec["path"])
            text = read_text(path)
            hit_count, found = count_needles(text, signature["needles"])
            blocker_count, blockers = count_needles(text, BLOCKER_NEEDLES)
            if hit_count == 0:
                evidence_status = "no_hit"
            elif blocker_count > 0:
                evidence_status = "conditional_or_blocked_hit"
            else:
                evidence_status = "unblocked_text_hit_needs_manual_review"
            rows.append(
                {
                    "search_id": f"{signature_id}_{source_id}",
                    "signature_id": signature_id,
                    "signature_label": signature["label"],
                    "source_id": source_id,
                    "path": str(path),
                    "source_kind": spec["source_kind"],
                    "hit_count": hit_count,
                    "found_needles": found,
                    "blocker_count": blocker_count,
                    "blocker_needles": blockers,
                    "evidence_status": evidence_status,
                    "claim_needs": signature["claim_needs"],
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
    return rows


def candidate_scorecard_rows(search_rows: list[dict[str, Any]], generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        source_hits = [row for row in search_rows if row["source_id"] == source_id and int(row["hit_count"]) > 0]
        signatures_hit = sorted({row["signature_id"] for row in source_hits})
        blocked_hits = [row for row in source_hits if row["evidence_status"] == "conditional_or_blocked_hit"]
        unblocked_hits = [row for row in source_hits if row["evidence_status"] == "unblocked_text_hit_needs_manual_review"]
        if len(signatures_hit) >= 4 and blocked_hits:
            verdict = "strong_conditional_not_signed"
        elif len(signatures_hit) >= 4 and unblocked_hits and not blocked_hits:
            verdict = "text_candidate_manual_review_only"
        elif signatures_hit:
            verdict = "partial_signature_context"
        else:
            verdict = "no_relevant_signature_context"
        rows.append(
            {
                "candidate_id": f"PCS780_{source_id}",
                "source_id": source_id,
                "path": str(spec["path"]),
                "source_kind": spec["source_kind"],
                "signatures_hit": ";".join(signatures_hit),
                "signature_count": len(signatures_hit),
                "blocked_hit_count": len(blocked_hits),
                "unblocked_text_hit_count": len(unblocked_hits),
                "candidate_verdict": verdict,
                "promotion_requirement": "real parent-action source line/equation with no blocker markers and valid_for_claim=true",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def triage_rows(scorecard: list[dict[str, Any]], generated_utc: str) -> list[dict[str, Any]]:
    parent_signed_found = any(row["candidate_verdict"] == "text_candidate_manual_review_only" for row in scorecard)
    conditional_count = sum(1 for row in scorecard if row["candidate_verdict"] == "strong_conditional_not_signed")
    return [
        {
            "triage_id": "LGT780_0_signature_search_outcome",
            "question": "Does the curated coupling lineage contain a parent-signed coupling owner?",
            "evidence": f"parent_signed_found={parent_signed_found}; strong_conditional_not_signed={conditional_count}",
            "verdict": "no_parent_signed_owner_found",
            "branch_effect": "local-GR proof remains blocked",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "triage_id": "LGT780_1_zero_route",
            "question": "Can B_obs_source_measure be set to zero by theorem?",
            "evidence": "only conditional quotient/descent/no-marker theorem shapes were found",
            "verdict": "zero_route_not_available",
            "branch_effect": "do not erase coupling residual",
            "next_action": "try minimal parent coupling owner action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "triage_id": "LGT780_2_bound_route",
            "question": "Can a sourced finite coupling bound be computed now?",
            "evidence": "779 runner: C_qmu, flux, readout, and PPN response rows are missing/nonclaim",
            "verdict": "numeric_bound_route_not_ready",
            "branch_effect": "empirical residual interface must be built before testing",
            "next_action": "define residual coefficients and fit-interface schema",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "triage_id": "LGT780_3_project_strategy",
            "question": "What is the least-scrutiny route?",
            "evidence": "derivation route has clean theorem shape; empirical route is honest fallback if signatures stay absent",
            "verdict": "derive_first_then_empirical_residual_if_needed",
            "branch_effect": "do not demote yet, but stop calling local branch derived",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "triage_id": "LGT780_4_local_GR_status",
            "question": "Is derived local GR achieved?",
            "evidence": "coupling owner, q_loc, Y5/Y6, PPN, boundary, and source-measure gates are not jointly closed",
            "verdict": "not_derived_not_dead",
            "branch_effect": "amber/red: viable research branch, not a claim branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def empirical_handoff_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "ERH780_0_b_g",
            "residual_channel": "common frame/Weyl geometry coupling",
            "definition": "b_g or c_g-like derivative of matter frame with respect to local representative field",
            "test_arena": "R10, PPN gamma/beta/alpha_i, clocks, orbit readout",
            "needed_for_fit": "coefficient prior or theorem-zero source path",
            "status": "open_if_parent_owner_absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "ERH780_1_b_theta",
            "residual_channel": "constants/charge/mass-ratio spurion",
            "definition": "vertical derivative of theta_A, alpha_EM, q_A, or mass ratios at fixed observed geometry",
            "test_arena": "clocks, EM/charge, WEP, source composition",
            "needed_for_fit": "superselection proof or residual coefficient row",
            "status": "open_if_no_marker_theorem_absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "ERH780_2_b_kappa",
            "residual_channel": "source current/source weight coupling",
            "definition": "species/source weighting or nonuniversal kappa_A/kappa source residual",
            "test_arena": "measured GM, WEP, orbital calibration, local Newton limit",
            "needed_for_fit": "Hilbert current closure or source-weight bound",
            "status": "open_if_source_current_owner_absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "ERH780_3_C_qmu",
            "residual_channel": "q_loc/source-measure leakage coefficient",
            "definition": "coefficient multiplying q_loc/source-measure flux in B_obs_source_measure/M_H",
            "test_arena": "R10, local force, PPN alpha3, compact-orbit residuals",
            "needed_for_fit": "numeric C_qmu, units, q_loc component, M_H normalization",
            "status": "missing_numeric_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "ERH780_4_B_SM",
            "residual_channel": "source-measure boundary/flux total",
            "definition": "B_obs_source_measure/M_H with no-cancellation component accounting",
            "test_arena": "local-GR recovery, Newton limit, orbit/source calibration",
            "needed_for_fit": "flux values, M_H_ref, assumptions, no-cancellation total",
            "status": "missing_flux_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "ERH780_5_W_PPN_coupling",
            "residual_channel": "PPN coupling response matrix",
            "definition": "partial DeltaPPN_I / partial hidden coupling channel with gauge/frame certificate",
            "test_arena": "PPN, clocks, photons, orbit timing, R11",
            "needed_for_fit": "linear response matrix W_Ic or theorem-zero rows",
            "status": "missing_response_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D780_0_search_done",
            "decision": "curated coupling-lineage signature search completed",
            "reason": "the relevant earlier work contains strong conditional theorem shapes but no parent-signed owner",
            "claim_status": "search_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D780_1_no_zero_promotion",
            "decision": "do not promote coupling/source-measure zero",
            "reason": "all strong hits are conditional or explicitly blocked",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D780_2_local_GR_triage",
            "decision": "keep local-GR derivation route alive but label it not derived",
            "reason": "the branch is structurally coherent but missing the owner signatures needed to reduce to GR/Newton",
            "claim_status": "not_derived_not_dead",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D780_3_next_target",
            "decision": "write the minimal parent coupling owner action or build empirical residual interface",
            "reason": "this is the clean fork after the signature search",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "curated signature search found strong conditional coupling-owner mathematics but no parent-signed coupling owner",
            "hard_blocker": "current corpus still lacks the explicit q/e_obs/S_matter/source/readout parent action signature needed for derived local GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    search: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    triage: list[dict[str, Any]],
    handoff: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_779_clean = all(validation_clean(number) for number in range(665, 780))
    signature_search_complete = len(search) == len(SIGNATURES) * len(SOURCE_SPECS)
    all_signatures_checked = set(SIGNATURES) == {row["signature_id"] for row in search}
    scorecard_complete = len(scorecard) == len(SOURCE_SPECS)
    conditional_hits_found = any(row["candidate_verdict"] == "strong_conditional_not_signed" for row in scorecard)
    no_parent_signed_claim = all(row["candidate_verdict"] != "text_candidate_manual_review_only" for row in scorecard)
    triage_complete = len(triage) == 5
    local_gr_not_claimed = any(row["triage_id"] == "LGT780_4_local_GR_status" and row["verdict"] == "not_derived_not_dead" for row in triage)
    handoff_complete = len(handoff) == 6
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, search, scorecard, triage, handoff, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D780_3_next_target" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V780_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V780_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V780_2_prior_665_779_clean", prior_665_779_clean, "665-779 validation rows have no failures"),
        ("V780_3_signature_search_complete", signature_search_complete, "all signatures searched across source set"),
        ("V780_4_all_signatures_checked", all_signatures_checked, "signature id coverage complete"),
        ("V780_5_scorecard_complete", scorecard_complete, "candidate scorecard complete"),
        ("V780_6_conditional_hits_found", conditional_hits_found, "strong conditional-but-not-signed hits found"),
        ("V780_7_no_parent_signed_claim", no_parent_signed_claim, "no source promoted as parent-signed owner"),
        ("V780_8_triage_complete", triage_complete, "local-GR branch triage complete"),
        ("V780_9_local_GR_not_claimed", local_gr_not_claimed, "local-GR branch labelled not derived, not dead"),
        ("V780_10_empirical_handoff_complete", handoff_complete, "empirical residual handoff rows complete"),
        ("V780_11_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V780_12_claim_artifacts_absent", claim_artifacts_absent, "no parent-owner/zero/bound/local-GR claim artifact fabricated"),
        ("V780_13_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V780_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V780_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V780_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    search: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    triage: list[dict[str, Any]],
    handoff: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    display_search = [row for row in search if int(row["hit_count"]) > 0][:24]
    text = f"""# 780 - Y5 R10 Parent-Action Coupling Signature Search Or Local-GR Branch Triage

Current result: **the curated coupling-lineage search found strong conditional theorem shapes, but no parent-signed coupling owner**. That is the honest state: the local-GR branch is not dead, because the quotient/descent/no-marker route is mathematically coherent; but it is not derived, because every strong hit still carries `conditional`, `not_parent_signed`, `not_closed`, `MISSING`, or equivalent blocker language.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Candidate Scorecard

{markdown_table(scorecard, ["candidate_id", "source_id", "source_kind", "signature_count", "blocked_hit_count", "unblocked_text_hit_count", "candidate_verdict", "promotion_requirement", "valid_for_claim"])}

## Signature Search Hits

{markdown_table(display_search, ["search_id", "signature_label", "source_id", "hit_count", "found_needles", "blocker_count", "blocker_needles", "evidence_status", "valid_for_claim"])}

## Local-GR Branch Triage

{markdown_table(triage, ["triage_id", "question", "evidence", "verdict", "branch_effect", "next_action", "valid_for_claim"])}

## Empirical Residual Handoff

{markdown_table(handoff, ["residual_id", "residual_channel", "definition", "test_arena", "needed_for_fit", "status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "source_kind", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a useful checkpoint because it prevents a subtle self-deception: old conditional lemmas are not the same as a parent action. The next move should be surgical: write the minimal parent coupling owner action and see if it really signs `q`, `e_obs`, `S_matter`, source current, readouts, and no-spurion constants. If that fails, stop trying to call the local branch derived and build the empirical residual interface.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    search = signature_search_rows(generated_utc)
    scorecard = candidate_scorecard_rows(search, generated_utc)
    triage = triage_rows(scorecard, generated_utc)
    handoff = empirical_handoff_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, search, scorecard, triage, handoff, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "source_kind", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SIGNATURE_SEARCH_PATH, search, ["search_id", "signature_id", "signature_label", "source_id", "path", "source_kind", "hit_count", "found_needles", "blocker_count", "blocker_needles", "evidence_status", "claim_needs", "valid_for_claim", "generated_utc"])
    write_csv(CANDIDATE_SCORECARD_PATH, scorecard, ["candidate_id", "source_id", "path", "source_kind", "signatures_hit", "signature_count", "blocked_hit_count", "unblocked_text_hit_count", "candidate_verdict", "promotion_requirement", "valid_for_claim", "generated_utc"])
    write_csv(TRIAGE_PATH, triage, ["triage_id", "question", "evidence", "verdict", "branch_effect", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(EMPIRICAL_HANDOFF_PATH, handoff, ["residual_id", "residual_channel", "definition", "test_arena", "needed_for_fit", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, search, scorecard, triage, handoff, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"780 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
