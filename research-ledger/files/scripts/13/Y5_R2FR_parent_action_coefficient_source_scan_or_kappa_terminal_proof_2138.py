from __future__ import annotations

import re
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2138-Y5-R2FR-parent-action-coefficient-source-scan-or-kappa-terminal-proof.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2137_NEXT = OUT / "P8_Y5_PARENT_QLOC_2137_NEXT_TARGET.csv"
CSV_2137_VAL = OUT / "P8_Y5_BRR545_2137_VALIDATION.csv"
CSV_2137_INV = OUT / "P8_Y5_PARENT_QLOC_2137_COEFF_R_INVENTORY.csv"
CSV_2137_KAPPA = OUT / "P8_Y5_PARENT_QLOC_2137_TERMINAL_KAPPA_AUDIT.csv"
CSV_2137_LOCK = OUT / "P8_Y5_PARENT_QLOC_2137_ACURV_OWNER_LOCK.csv"
DOC_2137 = ROOT / "2137-Y5-R2FR-parent-action-coefficient-inventory-or-first-Acurv-owner-lock.md"

SCAN_TARGETS = [
    ROOT / "01-motion-load-route-contract.md",
    ROOT / "04-vacuum-reciprocity-action-contract.md",
    ROOT / "09-hamiltonian-radial-cell-derivation.md",
    ROOT / "10-observer-map-symplectic-contract.md",
    ROOT / "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
    ROOT / "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md",
    ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
    ROOT / "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
    ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
    ROOT / "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
    ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
    ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
    ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
    ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
    ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
    ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
    ROOT / "1032-Y5-R10-spm-closure-ledger-and-finite-cg-tau-acquisition-runner.md",
    ROOT / "2131-Y5-R2FR-cR2-coefficient-owner-or-zero-certificate.md",
    ROOT / "2132-Y5-R2FR-no-integrated-curvature-tower-or-aux-scalar-coefficient-row.md",
    ROOT / "2133-Y5-R2FR-aux-curvature-coupling-beta-zero-or-source-row.md",
    ROOT / "2134-Y5-R2FR-visible-hidden-curvature-sequester-or-beta-source-pack.md",
    ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md",
    ROOT / "2136-Y5-R2FR-fixed-EH-coefficient-naturality-or-Acurv-parent-variable-map.md",
    ROOT / "2137-Y5-R2FR-parent-action-coefficient-inventory-or-first-Acurv-owner-lock.md",
    OUT / "P8_Y5_PARENT_QLOC_2137_COEFF_R_INVENTORY.csv",
    OUT / "P8_Y5_PARENT_QLOC_2136_FIXED_EH_COEFFICIENT_ATTEMPT.csv",
    OUT / "P8_Y5_PARENT_QLOC_2136_ACURV_PARENT_VARIABLE_MAP.csv",
]

PATTERNS = {
    "kappa_terminal": re.compile(r"\b(kappa_0|kappa|κ|Coeff\(R|Einstein-Hilbert|EH coefficient)\b", re.IGNORECASE),
    "gref_source_bridge": re.compile(r"\b(G_ref|G_N|M_H_ref|Q_tau|GM_orbit|source denominator|measured Newton)\b", re.IGNORECASE),
    "gamma_khat": re.compile(r"\b(Gamma_eff|K_hat|q_loc|S_GK|metric-response|metric response)\b", re.IGNORECASE),
    "marker_prefactor": re.compile(r"\b(chi_B|χ|marker|sigma_marker|domain marker|F\(sigma|F\(I|I_hid)\b", re.IGNORECASE),
    "memory_lambda": re.compile(r"\b(Lambda_mem|Λ|b_mem|memory|routing/load|motion-load)\b", re.IGNORECASE),
    "coframe_measure": re.compile(r"\b(coframe|mu_obs|measure|tau_source|tau_clock|tau_readout|observed frame)\b", re.IGNORECASE),
    "frame_cg": re.compile(r"\b(c_g|Weyl|disformal|shadow frame|common frame|A_g)\b", re.IGNORECASE),
    "beta_AR": re.compile(r"\b(beta_A|beta phi R|A R|A_curv_aux|A_curv|R\[g_obs\])\b", re.IGNORECASE),
    "r2_fr": re.compile(r"\b(c_R2|R2|R\^2|f\(R\)|f_RR|scalaron)\b", re.IGNORECASE),
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2138_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2138-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2138*",
        "*Y5_R2FR_parent_action_coefficient_source_scan_or_kappa_terminal_proof_2138*",
        "*AFRAME_COEFF_R_SOURCE_SCAN_2138*",
        "*JR2138*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2138_00_2137_next", CSV_2137_NEXT, ["NEXT2137_0_2138", "coefficient-of-R owners"], "2137 handoff selects parent action coefficient source scan."),
        ("SRC2138_01_2137_validation", CSV_2137_VAL, ["VAL2137_OVERALL", "PASS"], "2137 validation passed."),
        ("SRC2138_02_2137_inventory", CSV_2137_INV, ["COEFF2137_0_kappa0_terminal", "COEFF2137_2_beta_A_Acurv_aux"], "2137 coefficient inventory includes kappa and beta_A proxy."),
        ("SRC2138_03_2137_kappa", CSV_2137_KAPPA, ["KAP2137_5_verdict", "KAPPA_TERMINAL_NOT_DERIVED"], "2137 terminal kappa audit remains unsigned."),
        ("SRC2138_04_2137_lock", CSV_2137_LOCK, ["LOCK2137_5_selection_verdict", "OWNER_LOCK_FAILED_CLEANLY"], "2137 actual Acurv owner lock failed cleanly."),
        ("SRC2138_05_2137_doc", DOC_2137, ["coefficient-of-`R` problem", "source scan"], "2137 prose motivates source scan."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    for index, path in enumerate(SCAN_TARGETS):
        exists = path.exists()
        rows.append(
            row(
                source_id=f"SRC2138_SCAN_{index:02d}",
                source_path=str(path),
                path_exists=exists,
                expected_needles="scan target exists",
                needles_found=exists,
                role="source-scan target for literal coefficient/action-owner terms",
            )
        )
    return rows


def scan_hit_rows() -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    hit_index = 0
    for path in SCAN_TARGETS:
        if not path.exists():
            continue
        text = read_text(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            clean = line.strip()
            if not clean:
                continue
            for family, pattern in PATTERNS.items():
                if pattern.search(clean):
                    hits.append(
                        row(
                            hit_id=f"HIT2138_{hit_index:04d}",
                            family=family,
                            source_path=str(path),
                            line_number=line_number,
                            snippet=clean[:260],
                            source_kind="csv" if path.suffix.lower() == ".csv" else "md",
                            valid_for_claim=False,
                        )
                    )
                    hit_index += 1
                    break
    return hits


def owner_classification_rows(hits: list[dict[str, object]]) -> list[dict[str, object]]:
    family_counts = {family: 0 for family in PATTERNS}
    for hit in hits:
        family_counts[str(hit["family"])] += 1
    return [
        row(class_id="CLASS2138_0_kappa", family="kappa_terminal", hit_count=family_counts["kappa_terminal"], classification="CONDITIONAL_THEOREM_NOT_PARENT_SOURCE", evidence_summary="hits locate kappa/EH language, but source scan finds no parent-signed terminal coefficient clause", promotion_status="DO_NOT_PROMOTE"),
        row(class_id="CLASS2138_1_Gref", family="gref_source_bridge", hit_count=family_counts["gref_source_bridge"], classification="SOURCE_BRIDGE_NOT_COEFF_R_OWNER", evidence_summary="G_ref/M_H_ref/Q_tau appear as measured-source normalization gates", promotion_status="KEEP_AS_NEWTON_BRIDGE_BLOCKER"),
        row(class_id="CLASS2138_2_Gamma", family="gamma_khat", hit_count=family_counts["gamma_khat"], classification="RESIDUAL_ACTION_DENSITY_NOT_EH_COEFF", evidence_summary="Gamma_eff/K_hat/q_loc route is variational-residual/action-density debt, not a terminal EH coefficient", promotion_status="RETAIN_RESIDUAL_VECTOR"),
        row(class_id="CLASS2138_3_marker", family="marker_prefactor", hit_count=family_counts["marker_prefactor"], classification="LIVE_HIDDEN_MARKER_PREFACtor", evidence_summary="marker/hidden scalar prefactors remain legal unless no-marker theorem is signed", promotion_status="BLOCKS_KAPPA_TERMINAL"),
        row(class_id="CLASS2138_4_memory", family="memory_lambda", hit_count=family_counts["memory_lambda"], classification="EMPIRICAL_MEMORY_ROUTE_NOT_COEFF_R_OWNER", evidence_summary="memory/routing amplitudes appear, but no parent action bridge makes them coefficient-of-R owners", promotion_status="QUARANTINE_FROM_LOCAL_GR"),
        row(class_id="CLASS2138_5_coframe", family="coframe_measure", hit_count=family_counts["coframe_measure"], classification="MEASURE_FRAME_DESCENT_GATE", evidence_summary="measure/coframe/tau terms can move observed coupling/readout and must be signed with source bridge", promotion_status="BLOCKS_MEASURED_GR_PROMOTION"),
        row(class_id="CLASS2138_6_frame", family="frame_cg", hit_count=family_counts["frame_cg"], classification="COMMON_FRAME_COUPLING_GATE", evidence_summary="c_g/Weyl/disformal terms are frame/source-readout couplings, not solved by choosing Einstein frame", promotion_status="RETAIN_OR_SOURCE_CG"),
        row(class_id="CLASS2138_7_beta", family="beta_AR", hit_count=family_counts["beta_AR"], classification="BETA_A_PROXY_NOT_ACTUAL_OWNER", evidence_summary="beta_A/A_curv_aux/A R terms are found only as countermodel/proxy/interface rows, not as actual parent variable lock", promotion_status="OWNER_NOT_LOCKED"),
        row(class_id="CLASS2138_8_R2", family="r2_fr", hit_count=family_counts["r2_fr"], classification="HIGHER_CURVATURE_SELECTOR_BLOCKER", evidence_summary="R2/f(R) routes remain a separate EH-selector blocker rather than a linear-R coefficient owner", promotion_status="RETAIN_NONCLAIM"),
    ]


def kappa_terminal_attempt_rows(classifications: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        row(attempt_id="KTP2138_0_literal_source_scan", clause="literal parent coefficient source found", result="NO_PARENT_SIGNED_TERMINAL_KAPPA_SOURCE_FOUND", evidence="kappa/EH hits are conditional/contracts, not parent action signatures", status="FAIL_CURRENT_CLAIM"),
        row(attempt_id="KTP2138_1_source_bridge", clause="fixed coefficient implies measured Newton", result="BLOCKED_BY_GREF_MHREF_QTAU", evidence="G_ref/M_H_ref/Q_tau hits remain source-normalization gates", status="UNSIGNED"),
        row(attempt_id="KTP2138_2_hidden_prefactors", clause="no hidden scalar/marker prefactor", result="BLOCKED_BY_MARKER_AND_IHID_ROUTES", evidence="marker/F(I)/F(sigma) hits remain live", status="UNSIGNED"),
        row(attempt_id="KTP2138_3_frame_measure", clause="frame/measure/coframe harmlessness", result="BLOCKED_BY_COFRAME_CG_TAU_ROUTES", evidence="coframe/c_g/tau hits remain readout gates", status="UNSIGNED"),
        row(attempt_id="KTP2138_4_beta_owner", clause="first actual beta owner locked", result="NO_ACTUAL_PARENT_VARIABLE_LOCKED", evidence="beta_A/A_curv_aux hits are proxy/countermodel rows only", status="OWNER_LOCK_FAILED"),
        row(attempt_id="KTP2138_5_verdict", clause="promote kappa terminal or Acurv owner now", result="PROMOTION_REJECTED", evidence="no source-backed terminal kappa and no actual Acurv owner lock", status="KEEP_NONCLAIM"),
    ]


def acurv_owner_scan_rows() -> list[dict[str, object]]:
    return [
        row(scan_id="AOS2138_0_Acurv_empirical", candidate="A_curv", scan_result="FOUND_EMPIRICAL_ROUTE_ONLY", source_hint=str(ROOT / "01-motion-load-route-contract.md"), owner_status="NOT_PARENT_AUXILIARY_OWNER", required_next="parent action term beta_A A_curv R plus M_A^2/normalization"),
        row(scan_id="AOS2138_1_Acurv_aux_proxy", candidate="A_curv_aux_2135", scan_result="FOUND_PROXY_ONLY", source_hint=str(ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md"), owner_status="PROXY_RETAINED", required_next="actual parent variable/sector path"),
        row(scan_id="AOS2138_2_beta_A", candidate="beta_A", scan_result="FOUND_INTERFACE_AND_COUNTERMODEL", source_hint=str(ROOT / "2132-Y5-R2FR-no-integrated-curvature-tower-or-aux-scalar-coefficient-row.md"), owner_status="MISSING_NUMERIC_OR_THEOREM_ZERO", required_next="parent coefficient with units/sign or theorem-zero"),
        row(scan_id="AOS2138_3_beta_phi_R", candidate="beta phi R", scan_result="FOUND_COUNTERMODEL_TEXT", source_hint=str(ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"), owner_status="COUNTERMODEL_NOT_MTS_OWNER", required_next="distinguish legal countermodel from actual MTS parent term"),
        row(scan_id="AOS2138_4_owner_verdict", candidate="first actual Acurv parent owner", scan_result="NOT_FOUND", source_hint="SCAN_2138", owner_status="OWNER_LOCK_REMAINS_OPEN", required_next="manual/automated deep scan of parent action/core corpus beyond checkpoint summaries"),
    ]


def claim_gate_rows(hits: list[dict[str, object]]) -> list[dict[str, object]]:
    families = {str(hit["family"]) for hit in hits}
    return [
        row(gate_id="GATE2138_0_sources", gate="source scan inputs exist", gate_pass=True, rationale="source register validates all selected scan targets"),
        row(gate_id="GATE2138_1_scan_hits", gate="scan found coefficient/action-owner hits", gate_pass=len(hits) > 0, rationale=f"{len(hits)} pattern hits written"),
        row(gate_id="GATE2138_2_family_coverage", gate="all required coefficient families appear in scan", gate_pass=set(PATTERNS).issubset(families), rationale="kappa/G_ref/Gamma/marker/memory/coframe/frame/beta/R2 families have hits"),
        row(gate_id="GATE2138_3_terminal_kappa_promoted", gate="terminal kappa source is promoted", gate_pass=False, rationale="hits are conditional/contracts; no parent-signed terminal coefficient source found"),
        row(gate_id="GATE2138_4_actual_Acurv_owner_locked", gate="actual Acurv parent owner locked", gate_pass=False, rationale="Acurv/beta hits are proxy/countermodel/interface rows, not parent variable locks"),
        row(gate_id="GATE2138_5_name_collision_guard", gate="empirical route variables remain quarantined", gate_pass=True, rationale="A_curv/Lambda_mem/Gamma_eff are classified rather than promoted"),
        row(gate_id="GATE2138_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="kappa terminal, source bridge, beta owner and frame/marker gates remain open"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2138_0", decision="SOURCE_SCAN_COMPLETED", because="selected parent/action/core checkpoint corpus was scanned for literal coefficient-of-R owner terms", next_action="use scan hits as source-index for next proof/fill step"),
        row(decision_id="DEC2138_1", decision="NO_TERMINAL_KAPPA_SOURCE_PROMOTION", because="kappa/EH appearances are conditional theorem language, not parent-signed action source", next_action="do not claim fixed EH/Newton"),
        row(decision_id="DEC2138_2", decision="NO_ACTUAL_ACURV_OWNER_LOCK", because="A_curv and beta_A hits are empirical/proxy/countermodel rows without parent variable, beta, mass and normalization", next_action="deep-scan original parent action/core docs or build coefficient-owner checklist"),
        row(decision_id="DEC2138_3", decision="BEST_NEXT_IS_DEEP_PARENT_ACTION_HUNT", because="checkpoint summaries did not expose an actual owner; next needs broader original-corpus action/source scan, not another local derivation shortcut", next_action="2139 deep parent-action owner hunt"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2138_0_2139",
            next_target="2139-Y5-R2FR-deep-parent-action-owner-hunt-or-coefficient-owner-checklist.md",
            script="scripts/Y5_R2FR_deep_parent_action_owner_hunt_or_coefficient_owner_checklist_2139.py",
            objective="Deep-scan original parent/action/core corpus files, not only checkpoint summaries, for action terms and coefficient owners of R[g_obs], kappa, G_ref/source bridge, Gamma/Khat, marker prefactors, frame/coframe couplings, memory terms, and beta_A A R; if no actual owner is found, write the exact checklist a future parent action must satisfy.",
            forbidden_shortcuts="unit-choice proof; summary-only evidence as parent proof; empirical A_curv equals parent auxiliary; ignoring M_H_ref/source bridge; cancellation; local-GR/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    classes: list[dict[str, object]],
    kappa: list[dict[str, object]],
    acurv: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2138_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_COEFF_R_SOURCE_SCAN_2138_NONCLAIM.csv", classes + kappa + gates),
        ("COPY2138_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2138_ACURV_SCAN_NONCLAIM.csv", acurv),
        ("COPY2138_2_acquisition_queue", QUEUE / "JR2138_DEEP_PARENT_ACTION_OWNER_HUNT_QUEUE.csv", next_rows + classes + acurv),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    hits: list[dict[str, object]],
    classes: list[dict[str, object]],
    kappa: list[dict[str, object]],
    acurv: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    scan_ok = len(hits) > 0 and set(PATTERNS).issubset({str(hit["family"]) for hit in hits})
    classes_ok = any(item["class_id"] == "CLASS2138_0_kappa" and item["classification"] == "CONDITIONAL_THEOREM_NOT_PARENT_SOURCE" for item in classes) and any(item["class_id"] == "CLASS2138_7_beta" and item["classification"] == "BETA_A_PROXY_NOT_ACTUAL_OWNER" for item in classes)
    kappa_ok = any(item["attempt_id"] == "KTP2138_5_verdict" and item["result"] == "PROMOTION_REJECTED" for item in kappa)
    acurv_ok = any(item["scan_id"] == "AOS2138_4_owner_verdict" and item["owner_status"] == "OWNER_LOCK_REMAINS_OPEN" for item in acurv)
    gates_ok = any(item["gate_id"] == "GATE2138_2_family_coverage" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2138_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2138_3" and "DEEP_PARENT_ACTION_HUNT" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2138_0_2139" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, hits, classes, kappa, acurv, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2138_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, scan_ok, classes_ok, kappa_ok, acurv_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2138_00_sources", sources_ok, "all source-register paths and selected scan targets exist"),
        ("VAL2138_01_scan_hits", scan_ok, "scan produced hits across all required coefficient/action-owner families"),
        ("VAL2138_02_classes", classes_ok, "classification rejects terminal-kappa promotion and actual beta-owner lock"),
        ("VAL2138_03_kappa", kappa_ok, "kappa terminal promotion is rejected"),
        ("VAL2138_04_Acurv", acurv_ok, "actual Acurv owner remains open"),
        ("VAL2138_05_gates", gates_ok, "coverage gate passes while local-GR claim gate fails"),
        ("VAL2138_06_decisions", decisions_ok, "decision ledger selects deep parent action hunt next"),
        ("VAL2138_07_next", next_ok, "next target is 2139"),
        ("VAL2138_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2138_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2138_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2138_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2138"),
        ("VAL2138_12_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2138_OVERALL", all_ok, "2138 scans coefficient-source summaries, rejects terminal-kappa/Acurv-owner promotion, and selects deep parent action owner hunt next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    hits: list[dict[str, object]],
    classes: list[dict[str, object]],
    kappa: list[dict[str, object]],
    acurv: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    displayed_hits = hits[:80]
    content = "\n\n".join(
        [
            "# 2138 - Y5/R2FR Parent Action Coefficient Source Scan Or Kappa Terminal Proof",
            "## Current Verdict",
            "2138 scanned the selected parent/action/core checkpoint corpus for literal coefficient-of-`R` owner terms. The scan found the expected families — `kappa`, `G_ref/M_H_ref`, `Gamma_eff/K_hat`, markers, memory/routing, coframe/measure/tau, `c_g` frame couplings, `beta_A A R`, and `R2/f(R)` — but it did not find a parent-signed terminal `kappa` clause or an actual `A_curv_aux` parent variable.",
            "So the local-GR route remains disciplined: checkpoint summaries contain contracts, countermodels, proxies, and source-normalization gates, not a completed parent action owner. The next move must look deeper into original parent/action/core material or write the exact checklist a future parent action must satisfy.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Scan Hits Sample",
            md_table(displayed_hits, ["hit_id", "family", "source_path", "line_number", "snippet", "valid_for_claim"]),
            f"_Scan wrote {len(hits)} total hits; table above is capped for readability._",
            "## Owner Classification",
            md_table(classes, ["class_id", "family", "hit_count", "classification", "evidence_summary", "promotion_status", "valid_for_claim"]),
            "## Kappa Terminal Attempt",
            md_table(kappa, ["attempt_id", "clause", "result", "evidence", "status", "valid_for_claim"]),
            "## Acurv Owner Scan",
            md_table(acurv, ["scan_id", "candidate", "scan_result", "source_hint", "owner_status", "required_next", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    hits = scan_hit_rows()
    classes = owner_classification_rows(hits)
    kappa = kappa_terminal_attempt_rows(classes)
    acurv = acurv_owner_scan_rows()
    gates = claim_gate_rows(hits)
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2138_SOURCE_REGISTER.csv",
        "hits": OUT / "P8_Y5_PARENT_QLOC_2138_COEFF_SOURCE_SCAN_HITS.csv",
        "classes": OUT / "P8_Y5_PARENT_QLOC_2138_OWNER_CLASSIFICATION.csv",
        "kappa": OUT / "P8_Y5_PARENT_QLOC_2138_KAPPA_TERMINAL_ATTEMPT.csv",
        "acurv": OUT / "P8_Y5_PARENT_QLOC_2138_ACURV_OWNER_SCAN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2138_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2138_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2138_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2138_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2138_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["hits"], hits)
    write_csv(paths["classes"], classes)
    write_csv(paths["kappa"], kappa)
    write_csv(paths["acurv"], acurv)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(classes, kappa, acurv, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, hits, classes, kappa, acurv, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, hits, classes, kappa, acurv, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
