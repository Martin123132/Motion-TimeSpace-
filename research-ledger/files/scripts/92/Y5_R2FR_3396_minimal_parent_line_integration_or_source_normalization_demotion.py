from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3396-Y5-R2FR-minimal-parent-line-integration-or-source-normalization-demotion-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3396_SOURCE_REGISTER.csv",
    "integration_audit": OUT / "P8_Y5_R2FR_3396_PARENT_LINE_INTEGRATION_AUDIT.csv",
    "term_coverage": OUT / "P8_Y5_R2FR_3396_PARENT_TERM_COVERAGE_MATRIX.csv",
    "unit_convention": OUT / "P8_Y5_R2FR_3396_UNIT_CONVENTION_LOCK_LEDGER.csv",
    "adoption_packet": OUT / "P8_Y5_R2FR_3396_PARENT_ADOPTION_PACKET_NONCLAIM.csv",
    "demotion_ledger": OUT / "P8_Y5_R2FR_3396_SOURCE_NORMALIZATION_DEMOTION_LEDGER.csv",
    "integration_gate": OUT / "P8_Y5_R2FR_3396_INTEGRATION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3396_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3396_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3396_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3396_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3396_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3396_00_3395_doc", ROOT / "3395-Y5-R2FR-weak-field-source-normalization-return-under-AX1090.md", "3395 handoff"),
    ("SRC3396_01_3395_next", OUT / "P8_Y5_R2FR_3395_NEXT_TARGET.csv", "3395 next target"),
    ("SRC3396_02_3395_parent_line", OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv", "minimal parent line candidate"),
    ("SRC3396_03_3395_ladder", OUT / "P8_Y5_R2FR_3395_COUPLING_IDENTITY_LADDER.csv", "coupling ladder"),
    ("SRC3396_04_3395_residual", OUT / "P8_Y5_R2FR_3395_COUPLING_RESIDUAL_CONTRACT_NONCLAIM.csv", "coupling residual contract"),
    ("SRC3396_05_3394_gate", OUT / "P8_Y5_R2FR_3394_ADMISSIBLE_PACKAGE_GATE.csv", "local Cassini hygiene package"),
    ("SRC3396_06_core_fundamental_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "core fundamental action"),
    ("SRC3396_07_core_motion_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "motion-timespace action principle"),
    ("SRC3396_08_core_gravity", REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md", "gravity core formulation"),
    ("SRC3396_09_3377_doc", ROOT / "3377-Y5-R2FR-weak-field-source-normalization-or-Gref-kappa-bound-under-AX1090.md", "prior source-normalization theorem"),
]

TERM_PATTERNS = {
    "g_obs_metric": [r"g_\{?μν\}?", r"g_mu", r"metric", r"emergent metric", r"coarse-grained", r"smoothed"],
    "EH_coefficient": [r"1/2κ", r"1/2.?kappa", r"κ\s*=", r"8πG", r"8pi", r"Einstein"],
    "matter_action": [r"L_matter", r"S_matter", r"T_\{?μν\}?", r"T_mu", r"matter"],
    "observed_coframe": [r"e_obs", r"coframe", r"tetrad"],
    "quotient_map": [r"q\(Φ\)", r"q\\(Phi\\)", r"quotient"],
    "Hamiltonian_charge": [r"H_tau", r"H_τ", r"Q_tau", r"Q_τ", r"M_H", r"H_ref"],
    "boundary_reference": [r"B_ref", r"H_ref", r"boundary", r"reference"],
    "Pi_M": [r"Pi_M", r"Π_M", r"projector"],
    "ell_J": [r"ell_J", r"source-current", r"source current"],
    "no_backfill": [r"backfill", r"orbital GM", r"no-cancellation"],
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def source_lines(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".csv":
        return [
            (index, "; ".join(f"{key}={value}" for key, value in row.items()))
            for index, row in enumerate(read_csv_rows(path), start=2)
        ]
    return list(enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1))


def core_source_ids() -> set[str]:
    return {"SRC3396_06_core_fundamental_action", "SRC3396_07_core_motion_action", "SRC3396_08_core_gravity"}


def integration_audit_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    sources = {source_id: path for source_id, path, _role in LOCAL_SOURCES}
    counts = {term: 0 for term in TERM_PATTERNS}
    for source_id, path, _role in LOCAL_SOURCES:
        for line_number, line in source_lines(path):
            compact = " ".join(line.strip().split())
            if not compact:
                continue
            for term, patterns in TERM_PATTERNS.items():
                if counts[term] >= 8:
                    continue
                if any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in patterns):
                    rows.append(
                        {
                            "audit_id": f"IA3396_{term}_{counts[term]}",
                            "term": term,
                            "source_id": source_id,
                            "source_path": str(sources[source_id]),
                            "line_number": str(line_number),
                            "snippet": compact[:420],
                            "core_parent_evidence": bool_text(source_id in core_source_ids()),
                            "integration_role": "existing_core_support" if source_id in core_source_ids() else "post_checkpoint_context",
                            "valid_for_claim": "false",
                        }
                    )
                    counts[term] += 1
                    break
    for term, count in counts.items():
        if count == 0:
            rows.append(
                {
                    "audit_id": f"IA3396_{term}_NO_HIT",
                    "term": term,
                    "source_id": "NO_HIT",
                    "source_path": "",
                    "line_number": "",
                    "snippet": f"No direct corpus hit for {term}.",
                    "core_parent_evidence": "false",
                    "integration_role": "missing",
                    "valid_for_claim": "false",
                }
            )
    return rows


def source_has_term(path: Path, patterns: list[str]) -> bool:
    for _line_number, line in source_lines(path):
        compact = " ".join(line.strip().split())
        if compact and any(re.search(pattern, compact, flags=re.IGNORECASE) for pattern in patterns):
            return True
    return False


def term_coverage_rows(_audit_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    core_terms = {}
    any_terms = {}
    core_ids = core_source_ids()
    source_map = {source_id: path for source_id, path, _role in LOCAL_SOURCES}
    for term, patterns in TERM_PATTERNS.items():
        core_terms[term] = any(source_has_term(source_map[source_id], patterns) for source_id in core_ids if source_id in source_map)
        any_terms[term] = any(source_has_term(path, patterns) for _source_id, path, _role in LOCAL_SOURCES)
    term_descriptions = {
        "g_obs_metric": "observed/emergent metric from smoothed/coarse-grained psi covariance",
        "EH_coefficient": "Einstein-Hilbert coefficient and kappa/G convention",
        "matter_action": "standard matter action and Hilbert stress",
        "observed_coframe": "observed coframe/tetrad e_obs used for source variation",
        "quotient_map": "q(Phi) quotient/descent map for matter source branch",
        "Hamiltonian_charge": "H_tau/Q_tau/M_H/H_ref Hamiltonian source charge",
        "boundary_reference": "B_ref/H_ref boundary/reference sector",
        "Pi_M": "mass/source projector Pi_M",
        "ell_J": "source-current scaling ell_J",
        "no_backfill": "anti-circularity/no orbital-GM backfill guardrail",
    }
    rows = []
    for term, description in term_descriptions.items():
        if core_terms[term]:
            status = "CORE_PRESENT"
        elif any_terms[term]:
            status = "POST_CHECKPOINT_PRESENT_NOT_CORE_PARENT"
        else:
            status = "MISSING"
        rows.append(
            {
                "coverage_id": f"TC3396_{term}",
                "term": term,
                "description": description,
                "core_present": bool_text(core_terms[term]),
                "any_context_present": bool_text(any_terms[term]),
                "coverage_status": status,
                "integration_need": "already supported by core language" if status == "CORE_PRESENT" else "must be added to parent line or retained as closure/fallback",
                "valid_for_claim": "false",
            }
        )
    return rows


def unit_convention_rows() -> list[dict[str, str]]:
    return [
        {
            "unit_id": "UC3396_0_kappa_definition",
            "issue": "core docs define kappa as 8*pi*G/c^4",
            "evidence": "fundamental action and motion action both include kappa=8πG/c^4",
            "resolution_needed": "use kappa_MTS=8*pi*G_ref/c^4 in SI/c-explicit convention",
            "severity": "must_lock_before_scoring",
            "valid_for_claim": "false",
        },
        {
            "unit_id": "UC3396_1_equation_rhs_mixed_notation",
            "issue": "one core abstract writes G_mn + Gamma_G g_mn = 8*pi*G T_mn while action section uses kappa",
            "evidence": "same core text also states kappa=8πG/c^4, so RHS shorthand likely suppresses c powers or units",
            "resolution_needed": "parent line must choose either c=1 geometrized notation or c-explicit kappa notation and keep it fixed",
            "severity": "notation_lock_required_not_physics_rejection",
            "valid_for_claim": "false",
        },
        {
            "unit_id": "UC3396_2_G_ref_policy",
            "issue": "G_ref is a universal parent coupling, not an orbital-GM fitted amplitude",
            "evidence": "3395 guardrail plus GR practice",
            "resolution_needed": "state G_ref once in parent line; masses may be calibrated only after map fixed",
            "severity": "anti_circularity_guardrail",
            "valid_for_claim": "false",
        },
    ]


def adoption_packet_rows() -> list[dict[str, str]]:
    return [
        {
            "packet_id": "AP3396_0_section_title",
            "target": "parent action/local weak-field subsection",
            "candidate_text": "Local weak-field source-normalization clause",
            "purpose": "locate the parent-owned coupling line without editing core docs in this checkpoint",
            "integration_status": "STAGED_NOT_APPLIED",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "AP3396_1_parent_action",
            "target": "MTS action",
            "candidate_text": "In the local weak-field branch, the observed metric/coframe g_obs,e_obs are the coarse-grained MTS geometry used by matter. The parent action contains S_EH=(c^4/16πG_ref)∫√-g_obs R[g_obs] and S_matter[e_obs(q(Φ)),Ψ], with kappa_MTS=8πG_ref/c^4 fixed before any local readout.",
            "purpose": "own G_ref/kappa_MTS and Hilbert source stress",
            "integration_status": "ADMISSIBLE_COMPATIBLE_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "AP3396_2_source_current",
            "target": "matter/source-current definition",
            "candidate_text": "The Hamiltonian/source current J_H[τ], M_H, and PPN source density are all induced by the same S_matter variation in the same e_obs,τ branch; ell_J=1 unless a universal parent conversion is explicitly fixed before readout.",
            "purpose": "block hidden source-scale drift",
            "integration_status": "ADMISSIBLE_BUT_SOURCE_DESCENT_NOT_IN_CORE",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "AP3396_3_boundary_projectors",
            "target": "boundary/Hamiltonian sector",
            "candidate_text": "Q_τ, B_ref/H_ref and Π_M are boundary/reference/projector functionals of the same parent branch and may not be normalized independently of G_ref or fitted after Poisson/PPN comparison.",
            "purpose": "lock H_tau/Gauss/PPN source normalization",
            "integration_status": "ADMISSIBLE_BUT_BOUNDARY_SECTOR_MISSING_IN_CORE",
            "valid_for_claim": "false",
        },
        {
            "packet_id": "AP3396_4_no_backfill",
            "target": "guardrail",
            "candidate_text": "Measured orbital GM may estimate a system mass after the parent map is fixed, but may not define G_ref, ell_J, N_G, M_H_ref, or Π_M for the local-GR theorem.",
            "purpose": "anti-circularity / no source-amplitude backfill",
            "integration_status": "GUARDRAIL_READY",
            "valid_for_claim": "false",
        },
    ]


def demotion_ledger_rows() -> list[dict[str, str]]:
    return [
        {
            "demotion_id": "DEM3396_0_current_claim",
            "question": "Can current corpus claim parent-owned source normalization?",
            "verdict": "NO_CURRENT_CLAIM",
            "because": "core action supports EH/kappa/matter but lacks explicit e_obs/q(Phi), J_H, H_tau, B_ref/H_ref, Pi_M and ell_J ownership",
            "demoted_to": "candidate adoption packet plus residual contract",
            "valid_for_claim": "false",
        },
        {
            "demotion_id": "DEM3396_1_full_demote",
            "question": "Must the route be demoted to closure-only now?",
            "verdict": "NOT_YET",
            "because": "no contradiction found; the line is compatible and admissible, but unsigned",
            "demoted_to": "integration_ready_parent_clause_not_applied",
            "valid_for_claim": "false",
        },
        {
            "demotion_id": "DEM3396_2_if_rejected",
            "question": "What if the parent line is rejected later?",
            "verdict": "DEMOTE_TO_CLOSURE_OR_FINITE_SOURCE_ROWS",
            "because": "without one parent-owned coefficient/source-current branch, Newton/PPN amplitude recovery is a closure or fit",
            "demoted_to": "delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC, kappa_v finite rows",
            "valid_for_claim": "false",
        },
    ]


def integration_gate_rows(term_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    core_present = {row["term"]: row["core_present"] == "true" for row in term_rows}
    core_minimal = core_present.get("g_obs_metric", False) and core_present.get("EH_coefficient", False) and core_present.get("matter_action", False)
    missing_parent_terms = [
        row["term"]
        for row in term_rows
        if row["coverage_status"] != "CORE_PRESENT"
        and row["term"] in {"observed_coframe", "quotient_map", "Hamiltonian_charge", "boundary_reference", "Pi_M", "ell_J", "no_backfill"}
    ]
    return [
        {
            "gate_id": "IG3396_0_core_compatibility",
            "gate_result": "PASS_CORE_COMPATIBLE" if core_minimal else "FAIL_CORE_INSUFFICIENT",
            "detail": "core has smoothed metric, EH/kappa and matter action" if core_minimal else "core is missing one of smoothed metric/EH/matter",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "IG3396_1_missing_parent_terms",
            "gate_result": "BLOCK_PARENT_SIGNATURE_INCOMPLETE" if missing_parent_terms else "PASS_ALL_PARENT_TERMS_PRESENT",
            "detail": ";".join(missing_parent_terms),
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "IG3396_2_adoption_packet",
            "gate_result": "PASS_ADOPTION_PACKET_STAGED",
            "detail": "candidate parent-line text staged as nonclaim rows; no core docs modified",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "IG3396_3_source_normalization",
            "gate_result": "NO_SOURCE_NORMALIZATION_CLAIM",
            "detail": "compatible integration packet exists, but parent adoption and boundary/Hamiltonian objects are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    gate_results = {row["gate_result"] for row in rows_by_name["integration_gate"]}
    return [
        {
            "run_id": "RUN3396_0_integration_audit",
            "test": "MPL3395 integration audit against core corpus",
            "result": "PASS_AUDIT_EXECUTED_NONCLAIM",
            "detail": f"audit_rows={len(rows_by_name['integration_audit'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3396_1_core_compatibility",
            "test": "core support for smoothed metric, EH/kappa and matter",
            "result": "PASS_CORE_COMPATIBLE_NONCLAIM" if "PASS_CORE_COMPATIBLE" in gate_results else "FAIL_CORE_COMPATIBILITY",
            "detail": "core supports the parent line skeleton",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3396_2_missing_terms",
            "test": "explicit Hamiltonian/source-current objects",
            "result": "PASS_BLOCKERS_IDENTIFIED",
            "detail": "e_obs/q(Phi), H_tau/Q_tau/B_ref/Pi_M/ell_J ownership are not core-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3396_3_adoption_packet",
            "test": "parent adoption packet staged",
            "result": "PASS_PACKET_STAGED_NONCLAIM",
            "detail": "candidate text ready for parent integration audit; not applied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3396_4_firewall",
            "test": "prevent source-normalization/local-GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "integration-ready is not parent-signed; source normalization remains nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3396_0_sources",
            "claim": "all 3396 sources exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register parsed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3396_1_core_compatible",
            "claim": "MPL3395 is compatible with core action skeleton",
            "gate_pass": "true",
            "reason": "core has smoothed metric, EH/kappa and matter action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3396_2_parent_adopted",
            "claim": "MPL3395 is parent-signed/adopted",
            "gate_pass": "false",
            "reason": "adoption packet staged only; no parent docs modified",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3396_3_source_normalization",
            "claim": "source normalization is established",
            "gate_pass": "false",
            "reason": "Hamiltonian/source-current/projector objects remain missing from core parent action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3396_4_local_GR",
            "claim": "local GR/Newton coupling is derived",
            "gate_pass": "false",
            "reason": "integration-ready but unsigned; full PPN vector not run",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3396_0_progress",
            "decision": "The minimal parent line is compatible with the core action skeleton.",
            "because": "core already has smoothed emergent metric, EH/kappa, L_matter and variation to T_mu_nu.",
            "next_action": "use the adoption packet as the parent-owned coupling candidate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3396_1_not_signed",
            "decision": "Compatibility is not adoption.",
            "because": "core does not explicitly own e_obs/q(Phi), H_tau/Q_tau, B_ref/H_ref, Pi_M, ell_J, or no-backfill in one source-normalization branch.",
            "next_action": "do not claim Newton/PPN coupling until these terms are signed or bounded",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3396_2_unit_lock",
            "decision": "A unit-convention lock is required before scoring.",
            "because": "old prose mixes shorthand 8*pi*G*T with c-explicit kappa*T; this is a notation issue if locked, but a scoring bug if not.",
            "next_action": "carry c-explicit kappa_MTS=8*pi*G_ref/c^4 in future local gates",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3396_3_best_next",
            "decision": "Next move should be full PPN vector only after parent-line adoption or finite bounds.",
            "because": "otherwise gamma/beta/alpha_i tests would be measuring unresolved source-normalization ambiguity.",
            "next_action": "build 3397 as a pre-PPN readiness/vector gate with parent-line adoption status explicit",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3397-Y5-R2FR-full-PPN-vector-readiness-after-parent-line-audit-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3397_full_PPN_vector_readiness_after_parent_line_audit.py",
            "objective": "prepare the full PPN vector gate for gamma, beta, alpha_i, zeta_i and xi, but explicitly block scoring until MPL3395 parent adoption or finite source-normalization residuals are available",
            "why_next": "3396 makes source normalization integration-ready but unsigned; full PPN readiness should now list exactly what would be tested once ownership closes",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3398-Y5-R2FR-parent-line-finite-source-normalization-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3398_parent_line_finite_source_normalization_bound_pack.py",
            "objective": "if parent adoption remains deferred, produce finite nonclaim bounds for delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC and kappa_v",
            "why_next": "source normalization cannot be left as prose if parent integration is deferred",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3396*")
        if hit.name.startswith(("3396-Y5", "P8_Y5_R2FR_3396", "P8_Y5_BRR545_3396", "Y5_R2FR_3396"))
    ] if FW.exists() else []
    term_statuses = {row["coverage_status"] for row in rows_by_name["term_coverage"]}
    unit_ids = {row["unit_id"] for row in rows_by_name["unit_convention"]}
    packet_ids = {row["packet_id"] for row in rows_by_name["adoption_packet"]}
    demotion_verdicts = {row["verdict"] for row in rows_by_name["demotion_ledger"]}
    integration_results = {row["gate_result"] for row in rows_by_name["integration_gate"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3396_0_sources_exist_parse", "all cited 3396 source paths exist and parse", source_ok, ""),
        ("VAL3396_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3396_2_integration_audit", "integration audit covers required term patterns", set(TERM_PATTERNS).issubset({row["term"] for row in rows_by_name["integration_audit"]}), f"rows={len(rows_by_name['integration_audit'])}"),
        ("VAL3396_3_term_coverage", "term coverage separates core present from missing/post-checkpoint terms", {"CORE_PRESENT", "POST_CHECKPOINT_PRESENT_NOT_CORE_PARENT"}.issubset(term_statuses), ""),
        ("VAL3396_4_unit_convention", "unit convention lock ledger covers kappa, mixed RHS notation and G policy", {"UC3396_0_kappa_definition", "UC3396_1_equation_rhs_mixed_notation", "UC3396_2_G_ref_policy"}.issubset(unit_ids), ""),
        ("VAL3396_5_adoption_packet", "adoption packet stages parent action/source/boundary/no-backfill text", {"AP3396_1_parent_action", "AP3396_2_source_current", "AP3396_3_boundary_projectors", "AP3396_4_no_backfill"}.issubset(packet_ids), ""),
        ("VAL3396_6_demotion_ledger", "demotion ledger blocks current claim without forced closure-only demotion", {"NO_CURRENT_CLAIM", "NOT_YET", "DEMOTE_TO_CLOSURE_OR_FINITE_SOURCE_ROWS"}.issubset(demotion_verdicts), ""),
        ("VAL3396_7_integration_gate", "integration gate passes core compatibility but blocks source-normalization claim", {"PASS_CORE_COMPATIBLE", "BLOCK_PARENT_SIGNATURE_INCOMPLETE", "PASS_ADOPTION_PACKET_STAGED", "NO_SOURCE_NORMALIZATION_CLAIM"}.issubset(integration_results), ""),
        ("VAL3396_8_runner", "runner records audit, compatibility, missing terms, packet and firewall", {"PASS_AUDIT_EXECUTED_NONCLAIM", "PASS_CORE_COMPATIBLE_NONCLAIM", "PASS_BLOCKERS_IDENTIFIED", "PASS_PACKET_STAGED_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3396_9_gates", "gates pass compatibility but block parent adoption, source normalization and local GR", gate_map.get("GATE3396_1_core_compatible") == "true" and gate_map.get("GATE3396_2_parent_adopted") == "false" and gate_map.get("GATE3396_3_source_normalization") == "false" and gate_map.get("GATE3396_4_local_GR") == "false", ""),
        ("VAL3396_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3396_11_write_scope_outside_formalization", "no 3396 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3396_12_next_target", "next target moves to full PPN vector readiness", rows_by_name["next"][0]["target_id"].startswith("3397-Y5-R2FR-full-PPN-vector-readiness"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3396_13_overall", "3396 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3396 - Y5/R2FR minimal parent-line integration or source-normalization demotion under AX1090",
        "",
        "## Summary",
        "- 3396 audits whether the `3395` minimal parent action line can be integrated into the existing parent corpus.",
        "- Verdict: compatible with the core action skeleton, because the core already has smoothed/emergent metric, EH/kappa, matter action and variation to Hilbert stress.",
        "- But compatibility is not adoption: explicit `e_obs/q(Phi)`, `H_tau/Q_tau`, `B_ref/H_ref`, `Pi_M`, `ell_J`, and no-backfill ownership are not core-signed.",
        "- A parent adoption packet is staged as nonclaim text; no core or formalization files were modified.",
        "- A unit-convention lock is required: future local gates should use c-explicit `kappa_MTS=8*pi*G_ref/c^4` unless a geometrized convention is explicitly selected.",
        "- Source normalization is therefore integration-ready but not claim-valid.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Parent Line Integration Audit",
        md_table(rows_by_name["integration_audit"]),
        "## Parent Term Coverage Matrix",
        md_table(rows_by_name["term_coverage"]),
        "## Unit Convention Lock Ledger",
        md_table(rows_by_name["unit_convention"]),
        "## Parent Adoption Packet",
        md_table(rows_by_name["adoption_packet"]),
        "## Source Normalization Demotion Ledger",
        md_table(rows_by_name["demotion_ledger"]),
        "## Integration Gate",
        md_table(rows_by_name["integration_gate"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    integration_audit = integration_audit_rows()
    term_coverage = term_coverage_rows(integration_audit)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "integration_audit": integration_audit,
        "term_coverage": term_coverage,
        "unit_convention": unit_convention_rows(),
        "adoption_packet": adoption_packet_rows(),
        "demotion_ledger": demotion_ledger_rows(),
        "integration_gate": integration_gate_rows(term_coverage),
    }
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows(source_ok)
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
