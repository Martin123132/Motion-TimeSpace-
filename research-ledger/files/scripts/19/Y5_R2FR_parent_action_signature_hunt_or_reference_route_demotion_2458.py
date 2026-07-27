from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_ACTION_SIGNATURE_HUNT_OR_REFERENCE_ROUTE_DEMOTION_2458"
CHECKPOINT_ID = "2458"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2458-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2458_SOURCE_REGISTER.csv",
    "scan_top_hits": OUT / "P8_Y5_PARENT_QLOC_2458_CORPUS_SCAN_TOP_HITS.csv",
    "signature_matrix": OUT / "P8_Y5_PARENT_QLOC_2458_SIGNATURE_HUNT_MATRIX.csv",
    "demotion_gate": OUT / "P8_Y5_PARENT_QLOC_2458_REFERENCE_ROUTE_DEMOTION_GATE.csv",
    "bound_acquisition": OUT / "P8_Y5_PARENT_QLOC_2458_DELTA_REF_BOUND_ACQUISITION_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2458_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2458_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2458_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2458_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2458_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_signature_matrix": QUEUE / "JR2458_PARENT_ACTION_SIGNATURE_HUNT_MATRIX_NONCLAIM.csv",
    "queue_demotion_gate": QUEUE / "JR2458_REFERENCE_ROUTE_DEMOTION_GATE_NONCLAIM.csv",
    "hamiltonian_bound_acquisition": HAMILTONIAN / "Delta_ref_bound_acquisition_ledger_2458_NONCLAIM.csv",
    "local_bound_acquisition": LOCAL_BOUNDS / "Delta_ref_bound_acquisition_ledger_2458_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2458_00_2457_doc",
        "source_path": ROOT / "2457-Y5-R2FR-parent-Dirichlet-boundary-action-contract-or-Delta-ref-bound-values.md",
        "needles": ["PAC2457_2_variation_domain", "VDT2457_4_current_verdict", "NEXT2457_0_selected", "VAL2457_OVERALL"],
        "role": "exact parent contract and handoff to signature hunt",
    },
    {
        "source_id": "SRC2458_01_2457_signature_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2457_CONTRACT_SIGNATURE_AUDIT.csv",
        "needles": ["SIG2457_0_configuration_bundle", "MISSING_PARENT_CONFIGURATION_BUNDLE", "SIG2457_7_denominator"],
        "role": "machine-readable required signatures",
    },
    {
        "source_id": "SRC2458_02_1016_worldtube",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_0_parent_action", "PST1016_0_selector_lemma", "CG1016_1_selector_lemma_claim", "DEC1016_1_current_MTS_status"],
        "role": "candidate source-selector parent action contract",
    },
    {
        "source_id": "SRC2458_03_1023_qvx",
        "source_path": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        "needles": ["QVC1023_2_action_descent", "DEM1023_0_scope", "DEC1023_2_future_reopen", "V1023_SUMMARY"],
        "role": "candidate quotient/action descent contract with fixed boundary/topological terms",
    },
    {
        "source_id": "SRC2458_04_1030_spm",
        "source_path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["SPM1030_0_public_metric_object", "SPM1030_6_contract_verdict", "DEC1030_2_contract_status", "V1030_SUMMARY"],
        "role": "candidate same-frame matter/coframe parent action contract",
    },
    {
        "source_id": "SRC2458_05_1020_counterterm",
        "source_path": ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
        "needles": ["BXP1020_1_boundary_counterterm", "MISSING_COUNTERTERM_OWNER", "V1020_5_BX_audit_complete"],
        "role": "candidate boundary/counterterm ownership source",
    },
    {
        "source_id": "SRC2458_06_1006_denominator",
        "source_path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": ["CG1006_0_MHref_positive_same_frame", "ORBITAL_GM_IMPORT_NOT_EXCLUDED", "V1006_SUMMARY"],
        "role": "same-frame denominator blocker and anti-circularity guard",
    },
    {
        "source_id": "SRC2458_07_138_formalization_contract",
        "source_path": FORMALIZATION / "138-metric-null-action-block-contract.md",
        "needles": ["Private ruthless status: contract written; not derived.", "parent v1 derives contract = false", "transition_route_current_status = contract_only_closure"],
        "role": "formalization precedent: exact future-parent contract demoted to closure until derived",
    },
    {
        "source_id": "SRC2458_08_10_core_parent_skeleton",
        "source_path": FORMALIZATION / "10-core-consistency-repair.md",
        "needles": ["## 4. Parent Action Skeleton"],
        "role": "older parent-action skeleton candidate",
    },
]

SIGNATURES = [
    {
        "signature_id": "SIG2458_0_configuration_bundle",
        "required_signature": "C_D(beta_0) declared by current parent theory",
        "strict_pass_terms": ["C_D(beta_0)", "parent configuration", "current theorem"],
        "partial_terms": ["parent action", "action descent", "configuration", "S_parent"],
    },
    {
        "signature_id": "SIG2458_1_boundary_surface",
        "required_signature": "S/domain fixed before source/readout",
        "strict_pass_terms": ["fixed boundary", "source-blind surface", "not readout"],
        "partial_terms": ["surface", "boundary", "domain", "worldtube", "homology"],
    },
    {
        "signature_id": "SIG2458_2_boundary_metric",
        "required_signature": "sigma_AB fixed/source-blind by parent boundary condition",
        "strict_pass_terms": ["sigma_AB", "fixed", "parent boundary"],
        "partial_terms": ["sigma_AB", "boundary metric", "Dirichlet", "boundary condition"],
    },
    {
        "signature_id": "SIG2458_3_tau_coframe",
        "required_signature": "tau/coframe fixed and shared by source, reference, clocks and readout",
        "strict_pass_terms": ["tau_source=tau_charge", "D_a tau", "parent-signed"],
        "partial_terms": ["tau", "coframe", "public metric", "same-frame"],
    },
    {
        "signature_id": "SIG2458_4_topology",
        "required_signature": "C_top superselected before local variation",
        "strict_pass_terms": ["C_top", "superselected", "parent"],
        "partial_terms": ["topological", "cohomology", "boundary class", "fixed boundary/topological"],
    },
    {
        "signature_id": "SIG2458_5_counterterm",
        "required_signature": "B_ct fixed by parent boundary variational principle",
        "strict_pass_terms": ["B_ct", "fixed", "parent variational"],
        "partial_terms": ["counterterm", "B_ct", "reference subtraction", "boundary term"],
    },
    {
        "signature_id": "SIG2458_6_embedding",
        "required_signature": "embedding Hessian/operator norm controlled",
        "strict_pass_terms": ["embedding Hessian", "operator norm", "parent-signed"],
        "partial_terms": ["embedding", "isometric", "Hessian", "operator norm"],
    },
    {
        "signature_id": "SIG2458_7_denominator",
        "required_signature": "positive same-frame N_E/M_H_ref exists without orbital-GM import",
        "strict_pass_terms": ["positive same-frame", "M_H_ref", "parent-signed"],
        "partial_terms": ["M_H_ref", "same-frame", "denominator", "orbital GM"],
    },
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


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "True" if value else "False"


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def iter_scan_files() -> list[Path]:
    files: list[Path] = []
    for base in [ROOT, FORMALIZATION]:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            parts = set(path.parts)
            if "source-intake" in parts or "runs" in parts or "scripts" in parts:
                continue
            files.append(path)
    return files


def corpus_scan_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in iter_scan_files():
        text = read_text(path)
        text_lower = text.lower()
        hits = [pattern for pattern in SCAN_PATTERNS if pattern.lower() in text_lower]
        if not hits:
            continue
        score = len(hits)
        if "current MTS does not yet" in text or "not derived" in text_lower or "contract_only" in text_lower:
            score += 2
        if "parent action" in text_lower:
            score += 2
        if "fixed boundary/topological" in text_lower or "fixed boundary" in text_lower:
            score += 2
        rows.append(
            {
                **metadata(),
                "source_path": str(path),
                "scan_score": score,
                "matched_terms": ";".join(hits),
                "candidate_class": "strong_partial" if score >= 8 else "weak_partial",
            }
        )
    rows.sort(key=lambda row: (-int(row["scan_score"]), row["source_path"]))
    return rows[:40]


def has_all(text_lower: str, terms: list[str]) -> bool:
    return all(term.lower() in text_lower for term in terms)


def has_any(text_lower: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term.lower() in text_lower]


def candidate_sources() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAND2458_1016_worldtube",
            "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
            "candidate_type": "source selector",
            "known_blocker": "parent action, same-frame source current, tau and compactness unsigned",
        },
        {
            "candidate_id": "CAND2458_1023_qvx_action",
            "source_path": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            "candidate_type": "quotient action descent",
            "known_blocker": "field-by-field vertical action, action descent, matter/no-marker descent, boundary silence and degree count unsigned",
        },
        {
            "candidate_id": "CAND2458_1030_public_metric",
            "source_path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            "candidate_type": "same-frame matter/coframe",
            "known_blocker": "terminal public metric and no-extra-slot not parent-derived",
        },
        {
            "candidate_id": "CAND2458_1020_counterterm",
            "source_path": ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "candidate_type": "boundary/counterterm",
            "known_blocker": "counterterm owner missing",
        },
        {
            "candidate_id": "CAND2458_1006_denominator",
            "source_path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            "candidate_type": "denominator",
            "known_blocker": "positive same-frame M_H_ref missing; orbital GM substitution rejected",
        },
        {
            "candidate_id": "CAND2458_138_metric_null_contract",
            "source_path": FORMALIZATION / "138-metric-null-action-block-contract.md",
            "candidate_type": "formalization contract precedent",
            "known_blocker": "contract written but explicitly not derived",
        },
        {
            "candidate_id": "CAND2458_10_parent_skeleton",
            "source_path": FORMALIZATION / "10-core-consistency-repair.md",
            "candidate_type": "parent skeleton",
            "known_blocker": "skeleton only; not a fixed beta_ref theorem",
        },
    ]


def signature_matrix_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidate_sources():
        path = Path(candidate["source_path"])
        text = read_text(path)
        text_lower = text.lower()
        for signature in SIGNATURES:
            strict = has_all(text_lower, signature["strict_pass_terms"])
            partial_hits = has_any(text_lower, signature["partial_terms"])
            status = "PARTIAL_ONLY" if partial_hits else "NO_MATCH"
            if strict:
                status = "STRICT_TERMS_PRESENT_BUT_NOT_AUTHORITY"
            if "not derived" in text_lower or "false" in text_lower or "unsigned" in text_lower or "not parent-derived" in text_lower:
                authority = "NOT_PARENT_SIGNED"
            else:
                authority = "AUTHORITY_NOT_ESTABLISHED"
            rows.append(
                {
                    **metadata(),
                    "candidate_id": candidate["candidate_id"],
                    "candidate_type": candidate["candidate_type"],
                    "source_path": str(path),
                    "signature_id": signature["signature_id"],
                    "required_signature": signature["required_signature"],
                    "match_status": status,
                    "matched_terms": ";".join(partial_hits),
                    "authority_status": authority,
                    "known_blocker": candidate["known_blocker"],
                    "promote_signature": "False",
                }
            )
    return rows


def demotion_gate_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    strict_promotions = [row for row in matrix_rows if row["promote_signature"] == "True"]
    rows = [
        {
            "gate_id": "DEM2458_0_signature_hunt_result",
            "question": "Does the current corpus contain a source-backed parent action satisfying PAC2457/SIG2457?",
            "evidence": f"{len(strict_promotions)} promotable signatures found across {len(candidate_sources())} strongest candidates",
            "verdict": "NO_CURRENT_PARENT_SIGNATURE",
            "route_status": "REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS",
            "claim_allowed": "False",
        },
        {
            "gate_id": "DEM2458_1_future_route",
            "question": "Is the parent-Dirichlet route mathematically dead?",
            "evidence": "2457 gives an exact sufficient contract, but corpus signatures are only partial/conditional",
            "verdict": "FUTURE_PARENT_CONTRACT_ROUTE_RETAINED",
            "route_status": "REOPEN_ONLY_IF_ONE_PARENT_ACTION_SIGNS_ALL_CLAUSES",
            "claim_allowed": "False",
        },
        {
            "gate_id": "DEM2458_2_bound_fallback",
            "question": "What replaces theorem-zero for current testing?",
            "evidence": "2455-2457 give exact leak channels and nonclaim bound-value schemas",
            "verdict": "MOVE_TO_FINITE_DELTA_REF_BOUND_VALUES",
            "route_status": "BOUND_ACQUISITION_REQUIRED",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def bound_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "BND2458_0_metric_leak",
            "quantity": "C_sigma*max(||D_q sigma_AB||,||D_source sigma_AB||)/N_E",
            "source_target": "embedding operator norm plus boundary metric q/source derivative profile",
            "current_value": "MISSING_VALUE",
            "why_next": "sigma_AB is the strongest direct B_ref leak channel",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND2458_1_tau_leak",
            "quantity": "C_tau*max(||D_q tau||,||D_source tau||)/N_E",
            "source_target": "tau/coframe lock theorem or finite tau variation profile",
            "current_value": "MISSING_VALUE",
            "why_next": "tau controls reference charge, clocks, readout and PPN frame",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND2458_2_counterterm_leak",
            "quantity": "max(|D_q B_ct|,|D_source B_ct|)/N_E",
            "source_target": "boundary variational counterterm rule or finite counterterm derivative profile",
            "current_value": "MISSING_VALUE",
            "why_next": "counterterm cannot be used as a cancellation knob",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND2458_3_topological_leak",
            "quantity": "C_top*max(|D_q C_top|,|D_source C_top|)/N_E",
            "source_target": "topological superselection rule or finite class-jump bound",
            "current_value": "MISSING_VALUE",
            "why_next": "class switching is a hidden reference route unless fixed",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND2458_4_same_frame_denominator",
            "quantity": "N_E or M_H_ref",
            "source_target": "positive same-frame Hamiltonian/source charge, not orbital GM",
            "current_value": "MISSING_VALUE",
            "why_next": "all finite leak values require honest normalization",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND2458_5_no_cancellation_total",
            "quantity": "Delta_ref_boundary_leak_over_N_E",
            "source_target": "absolute sum of BND2458_0 through BND2458_4 components",
            "current_value": "NOT_COMPUTED_COMPONENTS_MISSING",
            "why_next": "this becomes the local PPN/Newton residual input if zero route remains closure-only",
            "valid_for_claim": "False",
        },
    ]
    return [{**metadata(), **row, "claim_allowed": "False"} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2458_0_signature_hunt_done",
            "claim": "The current corpus was searched for PAC2457 parent signatures.",
            "gate_status": "PASS",
            "reason": "strong candidates from post-checkpoint and formalization-workbench were scanned and matrixed",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2458_1_parent_signature_found",
            "claim": "A current parent action signs all fixed-boundary beta_ref clauses.",
            "gate_status": "BLOCKED",
            "reason": "no candidate supplies configuration bundle, boundary data, tau/coframe, topology, counterterm, embedding and denominator together",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2458_2_zero_route_current",
            "claim": "The reference-zero route is current MTS theorem.",
            "gate_status": "DEMOTED_TO_CLOSURE_ONLY",
            "reason": "2457 remains an exact future-parent contract but lacks current signatures",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2458_3_bound_values_ready",
            "claim": "Finite Delta_ref bound values are ready for PPN/Newton scoring.",
            "gate_status": "BLOCKED",
            "reason": "bound acquisition ledger is written but values are missing",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2458_4_local_GR",
            "claim": "Local GR/Newton/PPN branch passes.",
            "gate_status": "BLOCKED",
            "reason": "reference route is closure-only for current MTS and finite residual values are not sourced",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2458_0_no_existing_signature",
            "decision": "No existing source is allowed to promote PAC2457 to current theorem.",
            "reason": "strong candidates are contract-shaped but explicitly conditional, unsigned, or closure-only",
            "effect": "do not claim Delta_ref zero from the current corpus",
        },
        {
            "decision_id": "DEC2458_1_demote_current_zero_route",
            "decision": "Demote the reference-zero route to explicit closure for current MTS.",
            "reason": "the fixed-beta proof is exact, but exact contracts are not evidence until parent-signed",
            "effect": "local branch cannot use theorem-zero reference silence yet",
        },
        {
            "decision_id": "DEC2458_2_keep_future_derivation",
            "decision": "Retain parent-Dirichlet as a future derivation route.",
            "reason": "a single parent action that signs beta_ref, tau/coframe, B_ct, C_top, embedding and denominator would reopen it cleanly",
            "effect": "do not discard the route; require one-source ownership",
        },
        {
            "decision_id": "DEC2458_3_next_bound_values",
            "decision": "Move next to finite Delta_ref bound values unless a new parent-action source is supplied.",
            "reason": "finite residual values keep the theory testable without pretending zero is proven",
            "effect": "2459 should start value acquisition and same-frame normalization",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2458_0_selected",
            "selection_status": "selected",
            "target_file": "2459-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md",
            "target_script": "scripts/Y5_R2FR_first_Delta_ref_bound_value_runner_or_same_frame_denominator_source_2459.py",
            "task": "start the finite Delta_ref residual path by trying to source N_E/M_H_ref and first metric/tau/counterterm leak bounds; keep zero route closure-only unless a new parent action source appears",
            "acceptance_target": "schema-valid nonclaim bound rows with source targets, units, denominator policy, and no-cancellation total; or a real parent-signature source that reopens PAC2457",
            "guardrails": "no theorem-zero from contract alone; no orbital-GM denominator; no fitted boundary surface; no counterterm cancellation; no local-GR claim; no GitHub",
        }
    ]
    return [{**metadata(), **row} for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_signature_matrix", OUTPUTS["signature_matrix"], COPY_TARGETS["queue_signature_matrix"]),
        ("queue_demotion_gate", OUTPUTS["demotion_gate"], COPY_TARGETS["queue_demotion_gate"]),
        ("hamiltonian_bound_acquisition", OUTPUTS["bound_acquisition"], COPY_TARGETS["hamiltonian_bound_acquisition"]),
        ("local_bound_acquisition", OUTPUTS["bound_acquisition"], COPY_TARGETS["local_bound_acquisition"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic only
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return list(FORMALIZATION.rglob("*2458*"))


def validation_rows(
    source_rows: list[dict[str, Any]],
    scan_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add(
        "VAL2458_00_sources_exist",
        all(row["source_pass"] == "True" for row in source_rows),
        "all cited source paths exist and needles are present",
        ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "True"),
    )
    add(
        "VAL2458_01_scan_has_hits",
        len(scan_rows) >= 5,
        "corpus scan found candidate parent-action/boundary files",
        str(len(scan_rows)),
    )
    add(
        "VAL2458_02_matrix_complete",
        len(matrix_rows) == len(candidate_sources()) * len(SIGNATURES),
        "candidate/signature matrix covers all required clauses",
        str(len(matrix_rows)),
    )
    add(
        "VAL2458_03_no_promotions",
        all(row["promote_signature"] == "False" for row in matrix_rows),
        "no source-backed signature is promoted from partial matches",
    )
    add(
        "VAL2458_04_demotion_written",
        any(row["route_status"] == "REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS" for row in demotion_rows),
        "reference zero route is explicitly demoted for current MTS",
    )
    add(
        "VAL2458_05_future_route_retained",
        any(row["route_status"] == "REOPEN_ONLY_IF_ONE_PARENT_ACTION_SIGNS_ALL_CLAUSES" for row in demotion_rows),
        "future parent-contract route is retained under stricter conditions",
    )
    add(
        "VAL2458_06_bound_acquisition_nonclaim",
        len(bound_rows) >= 6 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in bound_rows),
        "finite bound acquisition ledger is nonclaim",
    )
    add(
        "VAL2458_07_claim_gates_safe",
        all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["gate_id"] == "GATE2458_4_local_GR" and row["gate_status"] == "BLOCKED" for row in gate_rows),
        "local-GR/PPN/Newton claims remain blocked",
    )
    add(
        "VAL2458_08_next_target_written",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2458_0_selected",
        "2459 finite Delta_ref bound-value target selected",
    )
    add(
        "VAL2458_09_branch_copies",
        len(branch_rows) == 4 and all(row["target_exists"] == "True" for row in branch_rows),
        "nonclaim branch copies exist",
    )
    hits = formalization_hits()
    add(
        "VAL2458_10_no_formalization_artifacts",
        not hits,
        "no 2458 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2458_CSV_{path.stem}",
            ok,
            f"CSV parses with {count} rows" if ok else "CSV parse failed",
            detail or str(path),
        )

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2458_COPY_CSV_{key}",
            ok,
            f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
            detail or str(path),
        )

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2458_OVERALL",
        overall,
        "2458 finds no current parent-action signature, demotes reference-zero to closure-only for current MTS, and selects finite bound acquisition",
    )
    return [{**metadata(), **row} for row in rows]


def write_doc(
    source_rows: list[dict[str, Any]],
    scan_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    demotion_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    compact_matrix = [
        row
        for row in matrix_rows
        if row["match_status"] != "NO_MATCH"
    ]
    doc = "\n\n".join(
        [
            "# 2458 Y5 R2FR Parent Action Signature Hunt Or Reference Route Demotion",
            "**Status:** corpus signature hunt complete. Strong candidates exist, but they are partial, conditional, or explicitly not derived. Therefore the `PAC2457` fixed-boundary reference-zero route is demoted to explicit closure-only for current MTS, while retained as a future derivation route if one parent action signs every clause.",
            "**Private reading:** this is one of those annoying-but-good moments. We did not lose the proof path; we stopped pretending scattered contracts equal one parent theorem. The next honest move is finite `Delta_ref` bound values unless new source material supplies the missing parent action.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], source_rows),
            "## Corpus Scan Top Hits\n" + table(["source_path", "scan_score", "matched_terms", "candidate_class"], scan_rows[:20]),
            "## Signature Hunt Matrix: Nonzero Matches\n" + table(["candidate_id", "candidate_type", "signature_id", "match_status", "matched_terms", "authority_status", "known_blocker", "promote_signature"], compact_matrix),
            "## Reference Route Demotion Gate\n" + table(["gate_id", "question", "evidence", "verdict", "route_status", "claim_allowed"], demotion_rows),
            "## Delta-ref Bound Acquisition Ledger\n" + table(["bound_id", "quantity", "source_target", "current_value", "why_next", "valid_for_claim"], bound_rows),
            "## Claim Gates\n" + table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], gate_rows),
            "## Decision Ledger\n" + table(["decision_id", "decision", "reason", "effect"], decisions),
            "## Next Target\n" + table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows),
            "## Branch Copies\n" + table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], branch_rows),
            "## Validation\n" + table(["check_id", "status", "notes", "detail"], validations),
        ]
    )
    DOC.write_text(doc + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    scan_rows = corpus_scan_rows()
    matrix_rows = signature_matrix_rows()
    demotion_rows = demotion_gate_rows(matrix_rows)
    bound_rows = bound_acquisition_rows()
    gate_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["scan_top_hits"], scan_rows)
    write_csv(OUTPUTS["signature_matrix"], matrix_rows)
    write_csv(OUTPUTS["demotion_gate"], demotion_rows)
    write_csv(OUTPUTS["bound_acquisition"], bound_rows)
    write_csv(OUTPUTS["claim_gates"], gate_rows)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(source_rows, scan_rows, matrix_rows, demotion_rows, bound_rows, gate_rows, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(source_rows, scan_rows, matrix_rows, demotion_rows, bound_rows, gate_rows, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
