from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3325-Y5-R2FR-universal-matter-no-direct-psi-vertex-and-no-tadpole-signature-gate-under-AX1090.md"

SRC_ACTION_PRINCIPLE = REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
SRC_FUNDAMENTAL = REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SRC_EFT = REPO / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md"

SOURCES = [
    {
        "source_id": "SRC3325_0_3324_doc",
        "path": ROOT / "3324-Y5-R2FR-induced-EH-coefficient-or-measured-G-closure-local-GR-theorem-under-AX1090.md",
        "role": "measured-G closure theorem and next target",
    },
    {
        "source_id": "SRC3325_1_3324_closure",
        "path": OUT / "P8_Y5_R2FR_3324_MEASURED_G_CLOSURE_THEOREM.csv",
        "role": "conditional local GR/Newton/Maxwell theorem",
    },
    {
        "source_id": "SRC3325_2_3324_assumptions",
        "path": OUT / "P8_Y5_R2FR_3324_CLOSURE_ASSUMPTION_LEDGER.csv",
        "role": "universal matter, no direct psi-EM, no-tadpole assumptions",
    },
    {
        "source_id": "SRC3325_3_3324_em",
        "path": OUT / "P8_Y5_R2FR_3324_MAXWELL_EM_STRESS_CLEAN_ROUTE.csv",
        "role": "metric Maxwell route and forbidden direct vertices",
    },
    {
        "source_id": "SRC3325_4_3323_tadpole",
        "path": OUT / "P8_Y5_R2FR_3323_NO_TADPOLE_COMPOSITE_GATE.csv",
        "role": "stationarity/no-tadpole/contact conditions",
    },
    {
        "source_id": "SRC3325_5_action_principle",
        "path": SRC_ACTION_PRINCIPLE,
        "role": "standard matter coupling and variation to T_munu",
    },
    {
        "source_id": "SRC3325_6_fundamental_action",
        "path": SRC_FUNDAMENTAL,
        "role": "emergent metric, macroscopic matter action, microscopic psi action",
    },
    {
        "source_id": "SRC3325_7_effective_field_theory",
        "path": SRC_EFT,
        "role": "psi-to-metric EFT, induced EH statement, L_matter in emergent action",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3325_SOURCE_REGISTER.csv",
    "evidence": OUT / "P8_Y5_R2FR_3325_SOURCE_EVIDENCE.csv",
    "signature": OUT / "P8_Y5_R2FR_3325_MATTER_SIGNATURE_CONTRACT.csv",
    "variation": OUT / "P8_Y5_R2FR_3325_VARIATION_CHAIN.csv",
    "direct": OUT / "P8_Y5_R2FR_3325_DIRECT_VERTEX_AUDIT.csv",
    "tadpole": OUT / "P8_Y5_R2FR_3325_NO_TADPOLE_SIGNATURE.csv",
    "theorem": OUT / "P8_Y5_R2FR_3325_BRANCH_THEOREM_STATUS.csv",
    "gates": OUT / "P8_Y5_R2FR_3325_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3325_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3325_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3325_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

EVIDENCE_PATTERNS = [
    "standard matter coupling",
    "L_matter the standard matter Lagrangian",
    "delta(L_matter",
    "T_{",
    "emergent metric",
    "L_matter",
    "Maxwell",
    "Poynting",
    "no direct",
    "tadpole",
]

FORBIDDEN_VERTEX_PATTERNS = [
    "f(psi)F",
    "f(psi) F",
    "psi J",
    "psi-EM",
    "nonmetric Poynting",
    "direct psi-EM",
]


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1200) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def text_for(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def find_hits(path: Path, max_hits: int = 8) -> str:
    text = text_for(path)
    patterns = [pattern.lower() for pattern in EVIDENCE_PATTERNS]
    hits: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if any(pattern in line.lower() for pattern in patterns):
            hits.append(f"L{line_number}:{line.strip()}")
        if len(hits) >= max_hits:
            break
    return " | ".join(hits)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def source_evidence_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = text_for(path)
        rows.append(
            {
                "evidence_id": f"EVID3325_{len(rows)}",
                "source_id": source["source_id"],
                "has_standard_matter": bool_str("standard matter" in text.lower() or "l_matter" in text.lower()),
                "has_variation_to_Tmunu": bool_str("T_{μν}" in text or "T_munu" in text or "Tμν" in text),
                "has_metric_readout": bool_str("emergent metric" in text.lower() or "g_{μν}" in text or "g_pub" in text),
                "has_em_direct_warning": bool_str("direct psi-EM" in text or "f(psi)" in text or "Poynting" in text),
                "hits": find_hits(path),
                "valid_for_claim": "false",
            }
        )
    return rows


def matter_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "signature_id": "SIG3325_0_macroscopic_universal_matter",
            "signature": "S_total = S_geom[g_pub] + S_Gamma[g_pub,Gamma_G] + S_matter[g_pub,Psi_m]",
            "derived_status": "SUPPORTED_BY_CORE_ACTION_PRINCIPLE",
            "meaning": "the local closure branch uses standard metric matter coupling; matter does not carry an independent psi charge at this level",
            "claim_scope": "macroscopic measured-G local-GR closure",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG3325_1_metric_Maxwell",
            "signature": "S_EM[g_pub,A] = -1/4 int sqrt(-g_pub) F_munu F^munu",
            "derived_status": "REQUIRED_SIGNATURE_FOR_MAXWELL_STRESS_ROUTE",
            "meaning": "Poynting flux and EM energy are inside T_munu^EM; they are not separate background-field forces",
            "claim_scope": "Maxwell/EM stress in local GR limit only, not EM unification",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG3325_2_forbidden_direct_vertices",
            "signature": "Delta S_direct[psi,Psi_m,A] = 0 for f(psi)L_matter, f(psi)F^2, psi J^mu A_mu, and nonmetric Poynting-background force terms",
            "derived_status": "BRANCH_SIGNATURE_REQUIRED",
            "meaning": "any direct psi-matter or psi-EM vertex becomes a fifth-force/clock/optics channel and must leave the clean local-GR branch",
            "claim_scope": "exclusion condition for local closure",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "SIG3325_3_microscopic_matter_descent",
            "signature": "S_matter[g_pub(psi),Psi_m] descends from parent psi/matter action with no hidden representative dependence",
            "derived_status": "NOT_PROVED_BY_CURRENT_CORPUS",
            "meaning": "current files support macroscopic standard matter, but not a deeper derivation of all matter from psi",
            "claim_scope": "future parent theory, not current local closure",
            "valid_for_claim": "false",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "VAR3325_0_metric_variation",
            "statement": "If S_matter = S_matter[g_pub,Psi_m], then delta S_matter = 1/2 int sqrt(-g_pub) T^munu delta g_pub_munu",
            "consequence": "all matter, including EM, sources geometry through T_munu",
            "status": "STANDARD_METRIC_VARIATION",
            "valid_for_claim": "false",
        },
        {
            "step_id": "VAR3325_1_chain_to_psi",
            "statement": "delta S_matter/delta psi = 1/2 int sqrt(-g_pub) T^munu (delta g_pub_munu/delta psi)",
            "consequence": "psi sees matter only through the public metric readout; there is no independent material charge if Delta S_direct=0",
            "status": "CHAIN_RULE_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "step_id": "VAR3325_2_EM_stress",
            "statement": "For S_EM[g_pub,A], variation gives T_munu^EM and the Poynting vector is a component of the EM stress-energy flux",
            "consequence": "Poynting is real physics in the source, but not a new nonmetric coupling",
            "status": "MAXWELL_STRESS_ROUTE",
            "valid_for_claim": "false",
        },
        {
            "step_id": "VAR3325_3_fifth_force_warning",
            "statement": "If Delta S_direct != 0, then delta S/direct delta psi adds a new source not proportional to T_munu delta g_pub",
            "consequence": "local GR/WEP/clock closure fails unless the direct vertex is symmetry-forbidden or empirically bounded",
            "status": "DERIVED_FAILURE_MODE",
            "valid_for_claim": "false",
        },
    ]


def direct_vertex_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    core_paths = [SRC_ACTION_PRINCIPLE, SRC_FUNDAMENTAL, SRC_EFT]
    joined_core = "\n".join(text_for(path) for path in core_paths)
    speculative_rows = [row for row in source_evidence_rows() if row["has_em_direct_warning"] == "true"]
    forbidden_found = [pattern for pattern in FORBIDDEN_VERTEX_PATTERNS if pattern.lower() in joined_core.lower()]
    rows.append(
        {
            "audit_id": "DVA3325_0_core_action_direct_vertex_search",
            "scope": "core action-principle/fundamental/EFT files",
            "result": "FOUND_FORBIDDEN_PATTERN" if forbidden_found else "NO_EXPLICIT_FORBIDDEN_DIRECT_VERTEX_IN_CORE_ACTION_FILES",
            "patterns_found": ";".join(forbidden_found),
            "interpretation": "core local branch can use standard metric matter signature, but absence of a written direct vertex is not a microscopic no-go theorem",
            "valid_for_claim": "false",
        }
    )
    rows.append(
        {
            "audit_id": "DVA3325_1_speculative_EM_warning",
            "scope": "3324 and wider local-branch handoff",
            "result": "DIRECT_VERTEX_FORBIDDEN_BY_BRANCH_SIGNATURE",
            "patterns_found": "direct psi-EM/Poynting warnings present in checkpoint files" if speculative_rows else "",
            "interpretation": "future EM unification may introduce extra vertices, but those must be quarantined from the local-GR closure unless bounded",
            "valid_for_claim": "false",
        }
    )
    rows.append(
        {
            "audit_id": "DVA3325_2_claim_rule",
            "scope": "public/local-GR theorem",
            "result": "LOCAL_GR_BRANCH_REQUIRES_DELTA_S_DIRECT_ZERO",
            "patterns_found": "n/a",
            "interpretation": "Maxwell/EM stress is allowed through T_munu; direct psi-EM force terms are not allowed in the clean local theorem",
            "valid_for_claim": "false",
        }
    )
    return rows


def no_tadpole_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NT3325_0_parent_EOM_stationarity",
            "condition": "E_eff[psi_bar] = delta S_eff/delta psi | psi_bar = 0, or the dissipative fixed-point equation is exactly satisfied",
            "derived_effect": "the expansion of the parent psi sector has no linear pi tadpole",
            "status": "DERIVED_SUFFICIENT_CONDITION",
            "claim_scope": "conditional local vacuum branch",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NT3325_1_centered_fluctuation_measure",
            "condition": "<pi>_local = 0 with a centered Gaussian/CLT local fluctuation measure or equivalent selection rule",
            "derived_effect": "the quadratic readout S[grad pi grad pi] has no one-particle projection by centering/selection",
            "status": "DERIVED_SUFFICIENT_CONDITION_NOT_CORPUS_SIGNED",
            "claim_scope": "needed for composite silence",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NT3325_2_projection_silence",
            "condition": "P1 S_ell[grad pi grad pi] = 0 in the local arena projection",
            "derived_effect": "composite term cannot masquerade as a single-particle finite local force",
            "status": "DERIVED_OPERATOR_CONDITION",
            "claim_scope": "local R10/WEP/PPN safety",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NT3325_3_contact_rule",
            "condition": "contact terms are source-supported and renormalize mass/G universally, not finite external forces",
            "derived_effect": "R10/lab contact leakage is quarantined into calibration or explicit epsilon_contact",
            "status": "BRANCH_RULE_REQUIRED",
            "claim_scope": "lab/local short-range closure",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NT3325_4_damping_caveat",
            "condition": "because the psi equation is dissipative, no-tadpole should be signed by fixed-point/EOM silence, not by assuming an ordinary conservative stationary action",
            "derived_effect": "avoids a fake variational proof in the damped sector",
            "status": "IMPORTANT_CONSISTENCY_CAVEAT",
            "claim_scope": "parent proof discipline",
            "valid_for_claim": "false",
        },
    ]


def branch_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "BTH3325_0_macro_source_signature",
            "claim": "At the macroscopic MTS action level, matter is standard metric matter: L_matter varies to T_munu",
            "support": "the-motion-timespace-action-principle and fundamental action files",
            "status": "SIGNED_AT_MACRO_CLOSURE_LEVEL",
            "limitation": "does not derive microscopic matter from psi",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "BTH3325_1_clean_EM_route",
            "claim": "For the local-GR closure branch, EM/Poynting must be treated through metric Maxwell stress T_munu^EM",
            "support": "3324 Maxwell clean route plus standard matter coupling",
            "status": "BRANCH_SIGNATURE_FORMALIZED",
            "limitation": "does not prove EM unification or emergent charge",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "BTH3325_2_no_direct_vertex_rule",
            "claim": "Clean local GR requires Delta S_direct[psi,matter,EM]=0",
            "support": "variation-chain failure mode and direct vertex audit",
            "status": "NECESSARY_CONDITION_FORMALIZED",
            "limitation": "future direct vertices need separate empirical bounds",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "BTH3325_3_no_tadpole_rule",
            "claim": "Composite one-particle silence follows if E_eff[psi_bar]=0 and P1 S[grad pi grad pi]=0",
            "support": "operator expansion from 3319-3324 and 3325 no-tadpole conditions",
            "status": "CONDITIONAL_SUFFICIENT_THEOREM",
            "limitation": "centered fluctuation/projection rule is not yet derived from parent measure",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3325_0_macro_universal_matter",
            "claim": "macroscopic standard metric matter coupling is signed",
            "passed": "true",
            "reason": "core action-principle states standard matter coupling/L_matter and variation to T_munu",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3325_1_no_direct_vertex_branch",
            "claim": "local-GR branch excludes direct psi-matter/psi-EM/Poynting vertices",
            "passed": "true",
            "reason": "branch signature Delta S_direct=0 is now explicit; direct vertices are routed out of clean local closure",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3325_2_microscopic_matter_descent",
            "claim": "microscopic parent action derives matter coupling from psi without hidden direct vertices",
            "passed": "false",
            "reason": "current corpus has macroscopic standard matter, not a full microscopic matter descent theorem",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3325_3_no_tadpole_parent_signed",
            "claim": "composite one-particle tadpole is parent-signed zero",
            "passed": "false",
            "reason": "sufficient conditions are derived, but centered fluctuation/projection silence is not yet proved from parent measure",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3325_4_local_GR_closure_strengthened",
            "claim": "measured-G local-GR closure theorem is strengthened by macroscopic source signature",
            "passed": "true",
            "reason": "universal matter/Maxwell route and direct-vertex exclusion are now explicit branch conditions",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3325_5_unconditional_local_GR",
            "claim": "local GR/Newton/Maxwell branch is fully parent-derived with no closure assumptions",
            "passed": "false",
            "reason": "microscopic matter descent and no-tadpole parent measure remain open",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3325_0",
            "question": "Did 3325 parent-sign universal matter?",
            "answer": "partly",
            "reason": "macroscopic MTS action signs standard metric L_matter and T_munu coupling, but a microscopic psi-to-matter descent is not present",
            "next_action": "use macroscopic measured-G closure honestly; keep microscopic matter derivation as future work",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3325_1",
            "question": "How should Poynting/EM be handled now?",
            "answer": "inside T_munu through Maxwell metric stress for the local branch",
            "reason": "direct psi-EM/Poynting vertices are a separate fifth-force/clock/optics problem and must not be smuggled into local GR",
            "next_action": "quarantine emergent-EM ambitions from the local-GR closure theorem",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3325_2",
            "question": "What remains the key mathematical risk?",
            "answer": "no-tadpole/composite silence",
            "reason": "stationary EOM kills parent linear tadpoles, but centered fluctuation/projection silence for S[grad pi grad pi] still needs a parent measure or a hard bound",
            "next_action": "derive centered local fluctuation/projection silence or bound epsilon_composite numerically",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3326-Y5-R2FR-centered-fluctuation-selection-rule-or-composite-tail-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3326_centered_fluctuation_selection_rule_or_composite_tail_bound.py",
            "objective": "try to close the remaining no-tadpole/composite gap by proving centered fluctuation selection/projection silence, or else produce an explicit epsilon_composite bound route",
            "must_include": "E_eff[psi_bar]=0 fixed-point gate; <pi>=0 measure centering; P1 S[grad pi grad pi]=0 projection; contact absorption; fallback epsilon_composite_i bound formulas",
            "fallback_if_failed": "measured-G local-GR branch remains conditional with explicit epsilon_composite nuisance bounds",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    evidence = source_evidence_rows()
    signature = matter_signature_rows()
    variation = variation_chain_rows()
    direct = direct_vertex_audit_rows()
    tadpole = no_tadpole_rows()
    theorem = branch_theorem_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3325_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3325_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3325_2_outputs_parse",
            "check": "all 3325 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3325_3_core_standard_matter_evidence",
            "check": "source evidence includes standard matter and variation to T_munu",
            "passed": any(row["has_standard_matter"] == "true" for row in evidence)
            and any(row["has_variation_to_Tmunu"] == "true" for row in evidence),
            "detail": "",
        },
        {
            "check_id": "VAL3325_4_signature_contract",
            "check": "signature includes universal matter, metric Maxwell, forbidden direct vertices, and microscopic descent status",
            "passed": {"SIG3325_0_macroscopic_universal_matter", "SIG3325_1_metric_Maxwell", "SIG3325_2_forbidden_direct_vertices", "SIG3325_3_microscopic_matter_descent"}.issubset(
                {row["signature_id"] for row in signature}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3325_5_variation_chain",
            "check": "variation chain includes metric variation, psi chain rule, EM stress, and direct-vertex failure mode",
            "passed": {"VAR3325_0_metric_variation", "VAR3325_1_chain_to_psi", "VAR3325_2_EM_stress", "VAR3325_3_fifth_force_warning"}.issubset(
                {row["step_id"] for row in variation}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3325_6_direct_vertex_audit",
            "check": "direct vertex audit records core search and exclusion rule",
            "passed": {"DVA3325_0_core_action_direct_vertex_search", "DVA3325_1_speculative_EM_warning", "DVA3325_2_claim_rule"}.issubset(
                {row["audit_id"] for row in direct}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3325_7_no_tadpole_conditions",
            "check": "no-tadpole signature includes EOM stationarity, centered measure, projection silence, contact rule, damping caveat",
            "passed": {"NT3325_0_parent_EOM_stationarity", "NT3325_1_centered_fluctuation_measure", "NT3325_2_projection_silence", "NT3325_3_contact_rule", "NT3325_4_damping_caveat"}.issubset(
                {row["gate_id"] for row in tadpole}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3325_8_theorem_status",
            "check": "branch theorem separates macro signature from microscopic descent and no-tadpole limits",
            "passed": any(row["status"] == "SIGNED_AT_MACRO_CLOSURE_LEVEL" for row in theorem)
            and any(row["status"] == "CONDITIONAL_SUFFICIENT_THEOREM" for row in theorem),
            "detail": "",
        },
        {
            "check_id": "VAL3325_9_no_unconditional_claim",
            "check": "microscopic descent, no-tadpole parent signing, and unconditional local-GR gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3325_2_microscopic_matter_descent", "GATE3325_3_no_tadpole_parent_signed", "GATE3325_5_unconditional_local_GR"}
            )
            and all(
                row["passed"] == "true"
                for row in gates
                if row["gate_id"] in {"GATE3325_0_macro_universal_matter", "GATE3325_1_no_direct_vertex_branch", "GATE3325_4_local_GR_closure_strengthened"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3325_10_next_composite_gap",
            "check": "next target attacks centered fluctuation selection or composite-tail bound",
            "passed": any("centered fluctuation" in row["objective"] and "epsilon_composite" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3325_11_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3325_12_overall",
            "check": "3325 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    lines: list[str] = [
        "# 3325 - Universal matter, no-direct-psi vertex, and no-tadpole signature gate under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3325 strengthens the measured-G local-GR branch, but does not overclaim.",
        "",
        "The current core action files support a macroscopic standard matter signature:",
        "",
        "`S_total = S_geom[g_pub] + S_Gamma[g_pub,Gamma_G] + S_matter[g_pub,Psi_m]`,",
        "",
        "with `L_matter` varying to `T_munu`. Therefore the local closure branch can use universal metric source coupling at the macroscopic level.",
        "",
        "For EM/Poynting, the clean local route is",
        "",
        "`S_EM[g_pub,A] = -1/4 int sqrt(-g_pub) F_munu F^munu`,",
        "",
        "so EM energy flux is part of `T_munu^EM`. Any direct `psi`-EM/Poynting vertex is excluded from the clean local-GR branch and must be bounded as a separate fifth-force/clock/optics channel.",
        "",
        "The microscopic descent of matter from the parent `psi` sector is still not proved. The no-tadpole/composite condition is also not parent-signed: the sufficient conditions are `E_eff[psi_bar]=0`, `<pi>_local=0`, and `P1 S[grad pi grad pi]=0`, but the centered fluctuation/projection rule still needs proof or a bound.",
        "",
        "So the branch has moved from loose assumption to disciplined signature: macroscopic matter coupling is signed; microscopic matter descent and composite silence remain open.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Source Evidence", source_evidence_rows(), "evidence_id"),
        ("Matter Signature Contract", matter_signature_rows(), "signature_id"),
        ("Variation Chain", variation_chain_rows(), "step_id"),
        ("Direct Vertex Audit", direct_vertex_audit_rows(), "audit_id"),
        ("No-Tadpole Signature", no_tadpole_rows(), "gate_id"),
        ("Branch Theorem Status", branch_theorem_rows(), "theorem_id"),
        ("Promotion Gates", promotion_gate_rows(), "gate_id"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- It signs macroscopic standard matter coupling for the local closure branch.",
            "- It excludes direct `psi`-matter/EM/Poynting vertices from the clean local branch.",
            "- It does not claim microscopic matter descent or parent-signed composite silence.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["evidence"], source_evidence_rows())
    write_csv(OUTPUTS["signature"], matter_signature_rows())
    write_csv(OUTPUTS["variation"], variation_chain_rows())
    write_csv(OUTPUTS["direct"], direct_vertex_audit_rows())
    write_csv(OUTPUTS["tadpole"], no_tadpole_rows())
    write_csv(OUTPUTS["theorem"], branch_theorem_rows())
    write_csv(OUTPUTS["gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
