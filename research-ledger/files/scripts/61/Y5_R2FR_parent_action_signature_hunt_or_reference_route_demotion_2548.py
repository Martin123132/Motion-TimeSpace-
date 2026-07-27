from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT_ID = "2548"
BRANCH_ID = "MTS_R2FR_PARENT_ACTION_SIGNATURE_HUNT_OR_REFERENCE_ROUTE_DEMOTION_2548"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2548-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2548_SOURCE_REGISTER.csv",
    "scan": RESIDUALS / "P8_Y5_NO_SHADOW_2548_CORPUS_SCAN_TOP_HITS.csv",
    "matrix": RESIDUALS / "P8_Y5_NO_SHADOW_2548_SIGNATURE_HUNT_MATRIX.csv",
    "demotion": RESIDUALS / "P8_Y5_NO_SHADOW_2548_REFERENCE_ROUTE_DEMOTION_GATE.csv",
    "bounds": RESIDUALS / "P8_Y5_NO_SHADOW_2548_DELTA_REF_BOUND_ACQUISITION_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2548_DECISION_LEDGER.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2548_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2548_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2548_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2548_VALIDATION.csv",
}

BRANCH_COPIES = {
    "matrix": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "JR2548_PARENT_ACTION_SIGNATURE_HUNT_MATRIX_NONCLAIM.csv",
    "demotion": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "JR2548_REFERENCE_ROUTE_DEMOTION_GATE_NONCLAIM.csv",
    "hamiltonian_bounds": POST_ROOT / "source-intake" / "hamiltonian-source" / "Delta_ref_bound_acquisition_ledger_2548_NONCLAIM.csv",
    "local_bounds": POST_ROOT / "source-intake" / "local_bounds" / "Delta_ref_bound_acquisition_ledger_2548_NONCLAIM.csv",
}

SOURCE_SPECS = [
    (
        "SRC2548_00_2547_doc",
        POST_ROOT / "2547-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md",
        ["FRS2547_2_chain_rule_to_Bref", "NEXT2547_0_selected", "VAL2547_OVERALL"],
        "current fixed-reference contract and handoff to signature hunt",
    ),
    (
        "SRC2548_01_2547_signature",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
        ["SIG2547_7_denominator", "MISSING_SAME_FRAME_N_E_OR_MHREF", "BLOCKED_NONCLAIM"],
        "current required fixed-reference signatures",
    ),
    (
        "SRC2548_02_2458_doc",
        POST_ROOT / "2458-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
        ["REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS", "NEXT2458_0_selected", "VAL2458_OVERALL"],
        "older completed signature hunt and demotion precedent",
    ),
    (
        "SRC2548_03_2458_matrix",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2458_SIGNATURE_HUNT_MATRIX.csv",
        ["CAND2458_1016_worldtube", "promote_signature", "False"],
        "machine-readable older signature matrix",
    ),
    (
        "SRC2548_04_2458_demotion",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2458_REFERENCE_ROUTE_DEMOTION_GATE.csv",
        ["DEM2458_0_signature_hunt_result", "NO_CURRENT_PARENT_SIGNATURE"],
        "machine-readable older demotion gate",
    ),
    (
        "SRC2548_05_2457_contract",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2457_PARENT_ACTION_CONTRACT.csv",
        ["PAC2457_0_parent_fields", "PAC2457_5_no_shortcut_guard"],
        "exact parent Dirichlet contract to be hunted",
    ),
    (
        "SRC2548_06_1006_denominator",
        POST_ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        ["CG1006_0_MHref_positive_same_frame", "ORBITAL_GM_IMPORT_NOT_EXCLUDED"],
        "same-frame denominator blocker and anti-circularity guard",
    ),
    (
        "SRC2548_07_138_formalization_contract",
        FORMALIZATION / "138-metric-null-action-block-contract.md",
        ["Private ruthless status: contract written; not derived.", "transition_route_current_status = contract_only_closure"],
        "formalization precedent for contract-only demotion",
    ),
    (
        "SRC2548_08_10_core_parent_skeleton",
        FORMALIZATION / "10-core-consistency-repair.md",
        ["## 4. Parent Action Skeleton"],
        "older parent-action skeleton candidate",
    ),
]

SCAN_PATTERNS = [
    "parent action",
    "action descent",
    "fixed boundary",
    "Dirichlet",
    "boundary condition",
    "boundary term",
    "counterterm",
    "B_ref",
    "B_ct",
    "tau",
    "coframe",
    "same-frame",
    "superselection",
    "topological",
    "embedding Hessian",
    "M_H_ref",
]

SIGNATURES = [
    ("SIG2548_0_configuration_bundle", "C_D(beta_0) declared by current parent theory", ["C_D(beta_0)", "parent configuration", "current theorem"], ["parent action", "action descent", "configuration", "S_parent"]),
    ("SIG2548_1_boundary_surface", "S/domain fixed before source/readout", ["fixed boundary", "source-blind surface", "not readout"], ["surface", "boundary", "domain", "worldtube", "homology"]),
    ("SIG2548_2_boundary_metric", "sigma_AB fixed/source-blind by parent boundary condition", ["sigma_AB", "fixed", "parent boundary"], ["sigma_AB", "boundary metric", "Dirichlet", "boundary condition"]),
    ("SIG2548_3_tau_coframe", "tau/coframe fixed and shared by source, reference, clocks and readout", ["tau_source=tau_charge", "D_a tau", "parent-signed"], ["tau", "coframe", "public metric", "same-frame"]),
    ("SIG2548_4_topology", "C_top superselected before local variation", ["C_top", "superselected", "parent"], ["topological", "cohomology", "boundary class", "fixed boundary/topological"]),
    ("SIG2548_5_counterterm", "B_ct fixed by parent boundary variational principle", ["B_ct", "fixed", "parent variational"], ["counterterm", "B_ct", "reference subtraction", "boundary term"]),
    ("SIG2548_6_embedding", "embedding Hessian/operator norm controlled", ["embedding Hessian", "operator norm", "parent-signed"], ["embedding", "isometric", "Hessian", "operator norm"]),
    ("SIG2548_7_denominator", "positive same-frame N_E/M_H_ref exists without orbital-GM import", ["positive same-frame", "M_H_ref", "parent-signed"], ["M_H_ref", "same-frame", "denominator", "orbital GM"]),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in SOURCE_SPECS:
        rows.append(
            stamp(
                {
                    "row_id": source_id,
                    "source_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "needles": "; ".join(needles),
                    "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                    "source_role": role,
                }
            )
        )
    return rows


def candidate_files() -> list[Path]:
    files = list(POST_ROOT.glob("*.md"))
    if FORMALIZATION.exists():
        files.extend(FORMALIZATION.glob("*.md"))
    return sorted({path for path in files if path.is_file()})


def corpus_scan_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in candidate_files():
        text = read_text(path).lower()
        matched = [pattern for pattern in SCAN_PATTERNS if pattern.lower() in text]
        if len(matched) >= 7:
            rows.append(
                stamp(
                    {
                        "row_id": f"SCAN2548_{len(rows):03d}",
                        "source_path": str(path),
                        "scan_score": len(matched),
                        "matched_terms": ";".join(matched),
                        "candidate_class": "strong_partial" if len(matched) >= 12 else "partial",
                    }
                )
            )
    rows.sort(key=lambda row: int(row["scan_score"]), reverse=True)
    for index, row in enumerate(rows[:40]):
        row["rank"] = index + 1
    return rows[:40]


def selected_candidate_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    selected = scan_rows[:12]
    required_paths = [
        POST_ROOT / "2458-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
        POST_ROOT / "2457-Y5-R2FR-parent-Dirichlet-boundary-action-contract-or-Delta-ref-bound-values.md",
        POST_ROOT / "2547-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md",
        POST_ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        POST_ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        POST_ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        POST_ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        FORMALIZATION / "138-metric-null-action-block-contract.md",
        FORMALIZATION / "10-core-consistency-repair.md",
    ]
    selected_paths = {Path(row["source_path"]) for row in selected}
    for path in required_paths:
        if path.exists() and path not in selected_paths:
            text = read_text(path).lower()
            matched = [pattern for pattern in SCAN_PATTERNS if pattern.lower() in text]
            selected.append(
                stamp(
                    {
                        "row_id": f"SCAN2548_REQUIRED_{len(selected)}",
                        "source_path": str(path),
                        "scan_score": len(matched),
                        "matched_terms": ";".join(matched),
                        "candidate_class": "required_context",
                        "rank": "required",
                    }
                )
            )
            selected_paths.add(path)
    return selected


def signature_matrix_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    candidates = selected_candidate_rows(scan_rows)
    rows: list[dict[str, object]] = []
    for candidate_index, candidate in enumerate(candidates):
        path = Path(str(candidate["source_path"]))
        text = read_text(path)
        lower = text.lower()
        for signature_id, required, strict_terms, partial_terms in SIGNATURES:
            strict_matched = [term for term in strict_terms if term.lower() in lower]
            partial_matched = [term for term in partial_terms if term.lower() in lower]
            if len(strict_matched) == len(strict_terms):
                match_status = "STRICT_TERMS_PRESENT_BUT_NOT_AUTHORITY"
                authority_status = "NOT_ONE_PARENT_ACTION_SIGNATURE"
            elif partial_matched:
                match_status = "PARTIAL_ONLY"
                authority_status = "NOT_PARENT_SIGNED"
            else:
                match_status = "NO_MATCH"
                authority_status = "NO_EVIDENCE"
            rows.append(
                stamp(
                    no_claim(
                        {
                            "row_id": f"SHM2548_{candidate_index:02d}_{signature_id}",
                            "candidate_path": str(path),
                            "signature_id": signature_id,
                            "required_signature": required,
                            "match_status": match_status,
                            "matched_terms": ";".join(strict_matched + partial_matched),
                            "authority_status": authority_status,
                            "known_blocker": "not a single current parent action signing beta_0, tau/coframe, C_top, B_ct, embedding and denominator together",
                            "promote_signature": "false",
                        }
                    )
                )
            )
    return rows


def demotion_rows(matrix_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    promotions = [row for row in matrix_rows if str(row.get("promote_signature", "")).lower() == "true"]
    verdict = "CURRENT_PARENT_SIGNATURE_FOUND" if promotions else "NO_CURRENT_PARENT_SIGNATURE"
    route = "REFERENCE_ZERO_ROUTE_OPEN_FOR_STRICT_PROMOTION" if promotions else "REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS"
    rows = [
        {
            "row_id": "DEM2548_0_signature_hunt_result",
            "question": "Does the current active chain contain a source-backed parent action satisfying all fixed-reference clauses?",
            "evidence": f"{len(promotions)} promotable signatures found across refreshed 2548 candidates",
            "verdict": verdict,
            "route_status": route,
        },
        {
            "row_id": "DEM2548_1_future_route",
            "question": "Is the parent-Dirichlet route mathematically dead?",
            "evidence": "2547 gives an exact sufficient contract, but current sources do not sign it",
            "verdict": "FUTURE_PARENT_CONTRACT_ROUTE_RETAINED",
            "route_status": "REOPEN_ONLY_IF_ONE_PARENT_ACTION_SIGNS_ALL_CLAUSES",
        },
        {
            "row_id": "DEM2548_2_bound_fallback",
            "question": "What replaces theorem-zero for current testing?",
            "evidence": "2455-2547 give exact leak channels and nonclaim bound-value schemas",
            "verdict": "MOVE_TO_FINITE_DELTA_REF_BOUND_VALUES",
            "route_status": "BOUND_ACQUISITION_REQUIRED",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def bound_acquisition_rows() -> list[dict[str, object]]:
    rows = [
        ("BND2548_0_metric_leak", "C_sigma*max(||D_q sigma_AB||,||D_source sigma_AB||)/M_H_ref", "embedding operator norm plus boundary metric q/source derivative profile", "MISSING_VALUE", "sigma_AB is the strongest direct B_ref leak channel"),
        ("BND2548_1_tau_leak", "C_tau*max(||D_q tau||,||D_source tau||)/M_H_ref", "tau/coframe lock theorem or finite tau variation profile", "MISSING_VALUE", "tau controls reference charge, clocks, readout and PPN frame"),
        ("BND2548_2_counterterm_leak", "max(|D_q B_ct|,|D_source B_ct|)/M_H_ref", "boundary variational counterterm rule or finite counterterm derivative profile", "MISSING_VALUE", "counterterm cannot be used as a cancellation knob"),
        ("BND2548_3_topological_leak", "C_top*max(|D_q C_top|,|D_source C_top|)/M_H_ref", "topological superselection rule or finite class-jump bound", "MISSING_VALUE", "class switching is a hidden reference route unless fixed"),
        ("BND2548_4_same_frame_denominator", "M_H_ref or N_E", "positive same-frame Hamiltonian/source charge, not orbital GM", "MISSING_VALUE", "all finite leak values require honest normalization"),
        ("BND2548_5_no_cancellation_total", "Delta_ref_boundary_leak_over_M_H_ref", "absolute sum of BND2548_0 through BND2548_4 components", "NOT_COMPUTED_COMPONENTS_MISSING", "this becomes local PPN/Newton residual input if zero route remains closure-only"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "quantity": quantity,
                    "source_target": source_target,
                    "current_value": current_value,
                    "why_next": why_next,
                }
            )
        )
        for row_id, quantity, source_target, current_value, why_next in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DEC2548_0_no_existing_signature",
            "decision": "do not promote fixed-reference zero from the current active chain",
            "reason": "refreshed signature matrix inherits 2458: candidates are partial, conditional, or not one parent action signing every clause",
            "effect": "Delta_ref zero is not current MTS evidence",
            "status": "NO_CURRENT_SIGNATURE_PROMOTION",
        },
        {
            "row_id": "DEC2548_1_demote_current_zero_route",
            "decision": "demote reference-zero route to explicit closure-only for current MTS",
            "reason": "the fixed-beta proof is exact but exact contracts are not evidence until sourced",
            "effect": "local branch must use finite residual values or find a new parent-action source",
            "status": "REFERENCE_ZERO_CLOSURE_ONLY_CURRENTLY",
        },
        {
            "row_id": "DEC2548_2_keep_future_derivation",
            "decision": "retain parent-Dirichlet as a future derivation route",
            "reason": "one parent action signing beta_ref, tau/coframe, B_ct, C_top, embedding and denominator would reopen it cleanly",
            "effect": "do not discard the route; require one-source ownership",
            "status": "FUTURE_ROUTE_RETAINED",
        },
        {
            "row_id": "DEC2548_3_next_bound_values",
            "decision": "move next to finite Delta_ref bound values unless new source material appears",
            "reason": "finite residual values preserve testability without pretending theorem-zero",
            "effect": "2549 should start denominator/value acquisition",
            "status": "SELECT_2549_BOUND_VALUES",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG2548_0_signature_hunt_done", "current active chain searched for fixed-reference parent signatures", "PASS_NONCLAIM_AUDIT", "scan/matrix written, not public evidence"),
        ("CG2548_1_parent_signature_found", "one current parent action signs all fixed beta_ref clauses", "FAIL", "no promotable signature in refreshed matrix"),
        ("CG2548_2_zero_route_current", "reference-zero route is current MTS theorem", "DEMOTED_TO_CLOSURE_ONLY", "exact contract lacks current signatures"),
        ("CG2548_3_bound_values_ready", "finite Delta_ref bound values ready for PPN/Newton scoring", "FAIL", "bound acquisition ledger has missing values"),
        ("CG2548_4_local_GR_Newton", "local GR/Newton/PPN branch passes", "FAIL_NONCLAIM", "reference route closure-only and finite residual values missing"),
    ]
    return [
        stamp(no_claim({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}))
        for row_id, gate, status, effect in rows
    ]


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2548_0_selected",
            "priority": "selected",
            "next_file": "2549-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md",
            "next_script": "scripts/Y5_R2FR_first_Delta_ref_bound_value_runner_or_same_frame_denominator_source_2549.py",
            "success_condition": "source positive same-frame M_H_ref/N_E and at least one finite metric/tau/counterterm leak bound row with units and no-cancellation total",
            "fallback_condition": "keep Delta_ref closure-only/nonclaim and record blocker ledger for missing denominator/value sources",
        },
        {
            "row_id": "NEXT2548_1_parallel",
            "priority": "parallel",
            "next_file": "2549b-Y5-R2FR-Hilbert-topological-source-equality-or-Req-row.md",
            "next_script": "scripts/Y5_R2FR_Hilbert_topological_source_equality_or_Req_row_2549b.py",
            "success_condition": "prove Hamiltonian/topological charge equals Hilbert/source charge in same compact worldtube",
            "fallback_condition": "retain R_eq_integral_over_MH as live bound row",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def branch_copy_rows() -> list[dict[str, object]]:
    copies = {
        BRANCH_COPIES["matrix"]: read_csv(OUTPUTS["matrix"]),
        BRANCH_COPIES["demotion"]: read_csv(OUTPUTS["demotion"]),
        BRANCH_COPIES["hamiltonian_bounds"]: read_csv(OUTPUTS["bounds"]),
        BRANCH_COPIES["local_bounds"]: read_csv(OUTPUTS["bounds"]),
    }
    rows: list[dict[str, object]] = []
    for path, payload in copies.items():
        write_csv(path, payload)
        rows.append(
            stamp(
                {
                    "row_id": f"COPY2548_{len(rows)}",
                    "copy_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "purpose": "nonclaim branch handoff copy",
                }
            )
        )
    return rows


def csv_has(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def all_flags_false(paths: list[Path]) -> bool:
    watched = {"valid_for_claim", "claim_allowed", "score_ready", "parent_signed", "theorem_zero", "numeric_prediction_present", "promote_signature"}
    for path in paths:
        for row in read_csv(path):
            for key in watched.intersection(row):
                if str(row[key]).strip().lower() in {"true", "yes", "1", "pass_for_claim"}:
                    return False
    return True


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = list(outputs.values())
    generated_before_validation = [path for key, path in outputs.items() if key != "validation"]
    scan_rows = read_csv(outputs["scan"]) if outputs["scan"].exists() else []
    matrix_rows = read_csv(outputs["matrix"]) if outputs["matrix"].exists() else []
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2548_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist"))
    checks.append(("VAL2548_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found"))
    checks.append(("VAL2548_02_outputs_exist", all(path.exists() for path in generated_before_validation), "all 2548 output files written before validation"))
    csv_parse_ok = True
    for path in generated_before_validation:
        try:
            csv_parse_ok = csv_parse_ok and len(read_csv(path)) > 0
        except Exception:
            csv_parse_ok = False
    checks.append(("VAL2548_03_csv_parse", csv_parse_ok, "all generated CSV files parse and contain rows"))
    checks.append(("VAL2548_04_scan_has_hits", len(scan_rows) >= 10, f"corpus scan found {len(scan_rows)} candidate parent-action/boundary files"))
    signature_ids = {signature_id for signature_id, *_ in SIGNATURES}
    matrix_signature_ids = {row.get("signature_id", "") for row in matrix_rows}
    checks.append(("VAL2548_05_matrix_covers_signatures", signature_ids.issubset(matrix_signature_ids), "signature matrix covers all required fixed-reference clauses"))
    checks.append(("VAL2548_06_no_promotions", all(row.get("promote_signature", "false").lower() == "false" for row in matrix_rows), "no source-backed signature is promoted from partial matches"))
    checks.append(("VAL2548_07_demotion_written", csv_has(outputs["demotion"], "REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS"), "reference zero route demoted for current MTS"))
    checks.append(("VAL2548_08_future_route_retained", csv_has(outputs["demotion"], "FUTURE_PARENT_CONTRACT_ROUTE_RETAINED"), "future parent-contract route retained under stricter conditions"))
    checks.append(("VAL2548_09_bound_acquisition_nonclaim", csv_has(outputs["bounds"], "BND2548_5_no_cancellation_total") and csv_has(outputs["bounds"], "MISSING_VALUE"), "finite bound acquisition ledger is nonclaim"))
    checks.append(("VAL2548_10_claim_gates_safe", csv_has(outputs["claims"], "CG2548_4_local_GR_Newton") and csv_has(outputs["claims"], "FAIL_NONCLAIM"), "local-GR/PPN/Newton claims remain blocked"))
    checks.append(("VAL2548_11_next_selected", csv_has(outputs["next"], "NEXT2548_0_selected") and csv_has(outputs["next"], "2549-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md"), "finite Delta_ref bound-value target selected"))
    checks.append(("VAL2548_12_branch_copies", all(path.exists() for path in BRANCH_COPIES.values()), "all nonclaim branch copies exist"))
    checks.append(("VAL2548_13_no_positive_claim_flags", all_flags_false(generated_before_validation + list(BRANCH_COPIES.values())), "all generated claim/readiness flags remain negative"))
    checks.append(("VAL2548_14_formalization_untouched", all(str(path).startswith(str(POST_ROOT)) for path in generated + list(BRANCH_COPIES.values()) + [DOC_PATH]), "generator writes only under post-checkpoint-work"))
    checks.append(("VAL2548_15_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(ok for _, ok, _ in checks)
    rows = [stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}) for row_id, ok, detail in checks]
    rows.append(
        stamp(
            {
                "row_id": "VAL2548_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2548 refreshes the signature hunt, finds no current parent-action promotion, demotes reference-zero to closure-only, and selects finite Delta_ref bound acquisition",
            }
        )
    )
    return rows


def table(columns: list[str], rows: list[dict[str, object]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    sources = read_csv(outputs["source"])
    scan = read_csv(outputs["scan"])
    matrix = read_csv(outputs["matrix"])
    demotion = read_csv(outputs["demotion"])
    bounds = read_csv(outputs["bounds"])
    decision = read_csv(outputs["decision"])
    claims = read_csv(outputs["claims"])
    next_target = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2548 - parent action signature hunt or reference route demotion

## Result

2548 refreshes the fixed-reference signature hunt for the current no-shadow chain.

The verdict is uncomfortable but clean: the exact `beta_ref`/Dirichlet reference contract survives as a future
derivation route, but the current active corpus still does not provide one parent action that signs the configuration
bundle, fixed boundary data, tau/coframe lock, topological class, counterterm rule, embedding control, and positive
same-frame `M_H_ref/N_E` together.

Therefore the fixed-reference theorem-zero route is demoted to explicit closure-only for current MTS.  The next honest
path is finite `Delta_ref` bound acquisition, not another theorem-zero restatement.

## Source Register

{table(["row_id", "source_path", "exists", "needles_found", "source_role"], sources)}

## Corpus Scan Top Hits

{table(["row_id", "rank", "source_path", "scan_score", "matched_terms", "candidate_class"], scan[:40])}

## Signature Hunt Matrix

{table(["row_id", "candidate_path", "signature_id", "match_status", "matched_terms", "authority_status", "promote_signature"], matrix)}

## Reference Route Demotion Gate

{table(["row_id", "question", "evidence", "verdict", "route_status"], demotion)}

## Delta-ref Bound Acquisition Ledger

{table(["row_id", "quantity", "source_target", "current_value", "why_next"], bounds)}

## Decision Ledger

{table(["row_id", "decision", "reason", "effect", "status"], decision)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], claims)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_target)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Practical Status

This is the right kind of grim: not a collapse, but a discipline upgrade.  We keep the exact fixed-reference contract as
a future route, but we stop letting it act like a current proof.  For current local-GR/PPN/Newton work, `Delta_ref`
must now be treated as a finite residual until values or a real parent signature arrive.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    scan_rows = corpus_scan_rows()
    write_csv(OUTPUTS["scan"], scan_rows)
    matrix_rows = signature_matrix_rows(scan_rows)
    write_csv(OUTPUTS["matrix"], matrix_rows)
    write_csv(OUTPUTS["demotion"], demotion_rows(matrix_rows))
    write_csv(OUTPUTS["bounds"], bound_acquisition_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
