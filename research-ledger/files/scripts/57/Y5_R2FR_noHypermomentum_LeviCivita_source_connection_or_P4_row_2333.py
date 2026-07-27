from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NOHYPERMOMENTUM_LEVICIVITA_OR_P4_ROW_2333"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2333-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md"

PATHS = {
    "2332_doc": ROOT / "2332-Y5-R2FR-nonHilbert-current-silence-spin-boundary-readout-trident.md",
    "2332_validation": OUT / "P8_Y5_BRR545_2332_VALIDATION.csv",
    "2332_audit": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv",
    "2332_envelopes": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_RESIDUAL_ENVELOPES.csv",
    "2332_decision": OUT / "P8_Y5_PARENT_QLOC_2332_TRIDENT_DECISION_LEDGER.csv",
    "2041_torsion": OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
    "960_lc": OUT / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
    "1834_nohyper": OUT / "P8_Y5_PARENT_QLOC_1834_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
    "1960_nohyper": OUT / "P8_Y5_PARENT_QLOC_1960_LC_NO_HYPERMOMENTUM_ATTEMPT.csv",
    "2042_nohyper": OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
    "1831_p4_map": OUT / "P8_Y5_PARENT_QLOC_1831_P4_WEAK_FIELD_MAP_CONTRACT.csv",
    "1960_p4": OUT / "P8_Y5_PARENT_QLOC_1960_P4_CONNECTION_ENVELOPE_LEDGER.csv",
    "1961_p4_priority": OUT / "P8_Y5_PARENT_QLOC_1961_P4_FILL_PRIORITY_LEDGER.csv",
    "1962_p4_hyper": OUT / "P8_Y5_PARENT_QLOC_1962_P4_HYPERMOMENTUM_FALLBACK.csv",
    "1963_p4_schema": OUT / "P8_Y5_PARENT_QLOC_1963_P4_HYPERMOMENTUM_ROW_SCHEMA.csv",
    "2042_p4_interface": OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv",
    "2043_p4_rows": OUT / "P8_Y5_PARENT_QLOC_2043_FIRST_P4_BOUND_ROWS.csv",
    "2044_p4_map": OUT / "P8_Y5_PARENT_QLOC_2044_P4_MAPPING_REQUIREMENTS.csv",
    "2119_projective_cert": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_CERTIFICATE.csv",
    "2119_projective_policy": OUT / "P8_Y5_PARENT_QLOC_2119_PROJECTIVE_RESIDUAL_POLICY.csv",
}

SOURCES = [
    ("SRC2333_00_2332_doc", "2332_doc", PATHS["2332_doc"], ["NEXT2332_0", "noHypermomentum"], "2332 handoff"),
    ("SRC2333_01_2332_validation", "2332_validation", PATHS["2332_validation"], ["VAL2332_OVERALL", "PASS"], "2332 validation"),
    ("SRC2333_02_2332_audit", "2332_audit", PATHS["2332_audit"], ["NHT2332_1_spin_torsion", "NOT_ZERO_DERIVED"], "spin/torsion head"),
    ("SRC2333_03_2332_envelopes", "2332_envelopes", PATHS["2332_envelopes"], ["NHE2332_1_spin", "MISSING_ZERO_OR_ENVELOPE"], "spin residual envelope"),
    ("SRC2333_04_2332_decision", "2332_decision", PATHS["2332_decision"], ["NTD2332_0_spin_first", "SELECTED_NEXT_PRIMARY"], "spin first decision"),
    ("SRC2333_05_2041_torsion", "2041_torsion", PATHS["2041_torsion"], ["LC2041_3_hypermomentum", "SELECTED_NEXT_BLOCKED_GATE"], "torsion connection decision"),
    ("SRC2333_06_960_lc", "960_lc", PATHS["960_lc"], ["LC960_4_verdict", "not_closed_current_corpus"], "Levi-Civita gate attempt"),
    ("SRC2333_07_1834_nohyper", "1834_nohyper", PATHS["1834_nohyper"], ["NHM1834_6_verdict", "NO_HYPERMOMENTUM_THEOREM_NOT_PROVEN"], "no-hypermomentum theorem attempt"),
    ("SRC2333_08_1960_nohyper", "1960_nohyper", PATHS["1960_nohyper"], ["LC1960_6_verdict", "ZERO_PROOF_FAILED_CLEANLY"], "LC/no-hypermomentum attempt"),
    ("SRC2333_09_2042_nohyper", "2042_nohyper", PATHS["2042_nohyper"], ["NH2042_5_verdict", "CONDITIONAL_THEOREM_PARENT_SIGNATURE_MISSING"], "no-hypermomentum parent clause"),
    ("SRC2333_10_1831_p4_map", "1831_p4_map", PATHS["1831_p4_map"], ["P4M1831_2_weak_field_projection", "MISSING_WEAK_FIELD_MAP"], "P4 weak-field map contract"),
    ("SRC2333_11_1960_p4", "1960_p4", PATHS["1960_p4"], ["P4C1960_5_hypermomentum", "MISSING_NO_GAMMA_MATTER_PROOF_OR_BOUND"], "P4 connection envelope"),
    ("SRC2333_12_1961_priority", "1961_p4_priority", PATHS["1961_p4_priority"], ["P4F1961_1_first_priority", "MISSING_NO_GAMMA_PROOF_OR_BOUND"], "P4 priority ledger"),
    ("SRC2333_13_1962_hyper", "1962_p4_hyper", PATHS["1962_p4_hyper"], ["P4H1962_0_trigger", "ACTIVE_FALLBACK_NONCLAIM"], "P4 hypermomentum fallback"),
    ("SRC2333_14_1963_schema", "1963_p4_schema", PATHS["1963_p4_schema"], ["P4R1963_0_hypermomentum_row", "MISSING_COEFFICIENT_AND_PROJECTION"], "P4 hypermomentum schema"),
    ("SRC2333_15_2042_interface", "2042_p4_interface", PATHS["2042_p4_interface"], ["P4C1960_5_hypermomentum", "MISSING_NO_GAMMA_MATTER_PROOF_OR_BOUND"], "P4 connection interface"),
    ("SRC2333_16_2043_rows", "2043_p4_rows", PATHS["2043_p4_rows"], ["P4B2043_0_hypermomentum", "MISSING_DELTA_COMPONENT_VALUES"], "first P4 bound rows"),
    ("SRC2333_17_2044_map", "2044_p4_map", PATHS["2044_p4_map"], ["MAP2044_5_claim_rule", "CLAIM_BLOCKED_CURRENTLY"], "P4 mapping requirements"),
]

OPTIONAL_SOURCES = [
    ("SRC2333_18_2119_projective_cert", "2119_projective_cert", PATHS["2119_projective_cert"], ["projective"], "projective certificate if present"),
    ("SRC2333_19_2119_projective_policy", "2119_projective_policy", PATHS["2119_projective_policy"], ["projective"], "projective policy if present"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2333_SOURCE_REGISTER.csv",
    "proof": OUT / "P8_Y5_PARENT_QLOC_2333_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
    "p4": OUT / "P8_Y5_PARENT_QLOC_2333_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2333_CONNECTION_GATE_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2333_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2333_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2333_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2333_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2333_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2333_0_proof", OUTPUTS["proof"], BETA_DOCS / "NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT_2333_NONCLAIM.csv"),
    ("COPY2333_1_p4", OUTPUTS["p4"], MICRO_RESIDUALS / "P4_hypermomentum_residual_row_2333_nonclaim.csv"),
    ("COPY2333_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2333_CONNECTION_GATE_DECISION_LEDGER_NONCLAIM.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "required": "true",
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    for row_id, key, path, needles, role in OPTIONAL_SOURCES:
        found, note = needle_status(path, needles) if path.exists() else (False, "optional_missing")
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "required": "false",
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_0_target",
            "route": "no-hypermomentum / Levi-Civita source connection",
            "formal_statement": "Gamma_obs=Gamma_LC[g_obs] and Delta_lambda^{mu nu}=delta S_ord/delta Gamma^lambda_{mu nu}=0 for matter, source, clock, light, orbit and readout sectors.",
            "status": "TARGET_SHARPENED",
            "obstruction": "must be signed by parent variable selection or Palatini/no-hypermomentum theorem",
            "effect_if_closed": "E_spin=0 for independent connection hypermomentum and major GR coupling gate closes",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_1_metric_only_parent",
            "route": "metric-only observed ordinary sector",
            "formal_statement": "ordinary/source/readout configuration contains e_obs/g_obs and omega_LC[e_obs], but no independent Gamma argument",
            "status": "EXACT_IF_PARENT_VARIABLE_LIST_SIGNED",
            "obstruction": "parent variable-selection theorem is not signed for every matter/source/readout sector",
            "effect_if_closed": "Delta_lambda^{mu nu}=0 by absence of variable",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_2_chain_rule_spin_connection",
            "route": "coframe-owned spin connection",
            "formal_statement": "spin connection is omega[e_obs], so spinor variation is already counted through e_obs rather than an independent torsionful Gamma",
            "status": "EXACT_CONDITIONAL_CLAUSE",
            "obstruction": "spinor/transport sectors need explicit coframe-owned connection clause",
            "effect_if_closed": "ordinary spin does not create independent torsion source",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_3_palatini_route",
            "route": "Palatini EH + no hypermomentum",
            "formal_statement": "if independent Gamma enters only EH and Delta_lambda^{mu nu}=0, the Gamma equation gives Levi-Civita up to projective gauge",
            "status": "CONDITIONAL_ROUTE_NOT_ACTIVE",
            "obstruction": "EH-only operator, no-Gamma matter/source/readout, and projective silence remain unsigned",
            "effect_if_closed": "dynamic Levi-Civita compatibility rather than metric-only kinematics",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_4_source_readout_guard",
            "route": "source/readout Gamma-slot exclusion",
            "formal_statement": "delta S_source/delta Gamma = delta S_clock/delta Gamma = delta S_light/delta Gamma = delta S_orbit/delta Gamma = delta S_readout/delta Gamma = 0",
            "status": "REQUIRED_GUARD_UNSIGNED",
            "obstruction": "source/worldtube/clock/light/orbit/readout Gamma-slot audit is not parent-signed",
            "effect_if_closed": "connection cannot re-enter through measurement protocols",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_5_projective_caveat",
            "route": "projective trace silence",
            "formal_statement": "projective mode is gauge/fixed/unobservable in source charge, clocks, lightcones, spin transport and orbital readout",
            "status": "UNSIGNED_OR_OPTIONAL_SOURCE_MISSING",
            "obstruction": "projective certificate/policy may exist but is not claim-grade in this branch",
            "effect_if_closed": "Palatini route can avoid trace leakage",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHL2333_6_verdict",
            "route": "promote Levi-Civita/no-hypermomentum",
            "formal_statement": "current MTS corpus proves no independent connection source and no hypermomentum for all ordinary local tests",
            "status": "NOT_DERIVED_RETAIN_P4_ROW",
            "obstruction": "metric-only parent, Palatini/EH, spin connection, source/readout Gamma-slot and projective clauses are conditional/unsigned",
            "effect_if_closed": "not closed yet; use P4 hypermomentum residual row",
            "valid_for_claim": "false",
        },
    ]


def build_p4_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4R2333_0_hypermomentum_total",
            "channel": "independent_connection_hypermomentum",
            "residual_symbol": "Delta_abs",
            "residual_formula": "Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||",
            "affected_tests": "WEP;clock;source_charge;orbital;PPN;local_GR",
            "units": "hypermomentum units or normalized dimensionless envelope",
            "current_status": "MISSING_DELTA_COMPONENT_VALUES",
            "required_inputs": "Delta components; K_hyper; norm definition; weak-field projection; arena bounds; source path",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4R2333_1_no_gamma_switch",
            "channel": "zero-switch",
            "residual_symbol": "Delta_lambda^{mu nu}",
            "residual_formula": "Delta_lambda^{mu nu}=0 only if no independent Gamma slot exists in ordinary/source/readout branch",
            "affected_tests": "all local source-current arenas",
            "units": "boolean/theorem",
            "current_status": "REQUIRES_PARENT_VARIABLE_ABSENCE",
            "required_inputs": "parent variable list; matter/source/readout no-Gamma audit",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4R2333_2_axial_torsion_guard",
            "channel": "axial_torsion_spin_coupling",
            "residual_symbol": "S_axial_abs",
            "residual_formula": "S_axial_abs := ||c_A S_mu J5^mu|| or normalized spin-torsion response envelope",
            "affected_tests": "spin_transport;clock;WEP;source_charge",
            "units": "spin-current units or normalized dimensionless envelope",
            "current_status": "MISSING_SPIN_TORSION_COEFFICIENT",
            "required_inputs": "spinor action branch; torsion coefficient; fermion source density; clock_or_spin_bound; source path",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4R2333_3_mapping_contract",
            "channel": "P4 weak-field/arena map",
            "residual_symbol": "K_P4",
            "residual_formula": "epsilon_P4 <= K_hyper * Delta_abs plus absolute envelopes for torsion/nonmetricity components",
            "affected_tests": "R10;PPN;clock;WEP;orbital;lightcone",
            "units": "arena-specific after projection",
            "current_status": "MISSING_WEAK_FIELD_MAP_AND_UNIT_NORMALIZATION",
            "required_inputs": "component basis; unit normalization; lab frame; observable kernel; no-cancellation policy",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CGD2333_0_route",
            "decision": "no-hypermomentum theorem not promoted",
            "reason": "all clean routes require parent-signed variable/action/readout clauses that are not currently active",
            "consequence": "retain P4 hypermomentum row as mandatory fallback",
            "status": "P4_ROW_REQUIRED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CGD2333_1_best_next",
            "decision": "attack no-Gamma slot audit next",
            "reason": "absence of independent Gamma is stronger and cleaner than bounding arbitrary connection residues",
            "consequence": "if it fails, the P4 row already declares required inputs",
            "status": "SELECT_NO_GAMMA_AUDIT_NEXT",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CGD2333_2_public_policy",
            "decision": "do not publish as GR reduction",
            "reason": "Levi-Civita/no-hypermomentum is still conditional and P4 rows are not score-ready",
            "consequence": "private derivation/fallback checkpoint only",
            "status": "NO_GITHUB_EVIDENCE_UPDATE",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2333_0_sources", "gate": "source paths and required needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2333_1_metric_only_route", "gate": "metric-only observed connection parent-signed", "passed": "false", "claim_effect": "Levi-Civita not kinematically derived", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2333_2_palatini_route", "gate": "Palatini EH plus no hypermomentum closes", "passed": "false", "claim_effect": "dynamic LC route not active", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2333_3_no_gamma_source_readout", "gate": "source/readout Gamma-slot exclusion signed", "passed": "false", "claim_effect": "connection may re-enter via protocols", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2333_4_P4_score", "gate": "P4 hypermomentum residual score-ready", "passed": "false", "claim_effect": "values/maps/units missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2333_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "connection gate still open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2333_6_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "private connection-gate checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2333_0_import_GR_connection", "claim": "use Levi-Civita because GR uses it", "allowed": "false", "reason": "the goal is to derive GR/Newton recovery, so LC must be parent-signed or residualized", "blocking_rows": "NHL2333_1_metric_only_parent;NHL2333_3_palatini_route", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2333_1_spinor_shortcut", "claim": "ordinary spinors imply no independent torsion source automatically", "allowed": "false", "reason": "coframe-owned spin connection must be explicit; independent torsionful connection creates hypermomentum", "blocking_rows": "NHL2333_2_chain_rule_spin_connection;P4R2333_2_axial_torsion_guard", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2333_2_projective_ignore", "claim": "projective trace is harmless without proof", "allowed": "false", "reason": "projective mode must be gauge/fixed/unobservable in clocks, source charge, lightcones, spin transport and orbit readout", "blocking_rows": "NHL2333_5_projective_caveat", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2333_3_P4_claim", "claim": "P4 fallback row is an empirical pass", "allowed": "false", "reason": "P4 row has schema only; component values, units, weak-field map and source-backed bounds are missing", "blocking_rows": "P4R2333_0_hypermomentum_total;P4R2333_3_mapping_contract", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2333_0",
            "next_target": "2334-Y5-R2FR-noGamma-slot-matter-source-readout-audit.md",
            "why": "cleanest derivation route: prove ordinary matter, source support, clocks, light, orbit, and readout have no independent Gamma argument.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2333_1",
            "next_target": "2334b-Y5-R2FR-first-P4-hypermomentum-component-map-and-units.md",
            "why": "fallback route if no-Gamma slot audit fails: fill Delta components, units, weak-field projection and arena bounds.",
            "claim_status": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2333_2",
            "next_target": "2334c-Y5-R2FR-projective-trace-certificate-or-residual-policy.md",
            "why": "projective trace remains a required caveat for Palatini/metric-affine connection routes.",
            "claim_status": "parallel_nonclaim",
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
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    required_sources = [row for row in source_rows if row["required"] == "true"]
    add("VAL2333_00_required_sources_exist", all(row["exists"] == "true" for row in required_sources), "every required source path exists")
    add("VAL2333_01_required_needles_found", all(row["needles_found"] == "true" for row in required_sources), "all required source needles were found")
    proof_rows = read_csv_rows(OUTPUTS["proof"])
    add("VAL2333_02_nohyper_not_promoted", any(row.get("row_id") == "NHL2333_6_verdict" and row.get("status") == "NOT_DERIVED_RETAIN_P4_ROW" for row in proof_rows), "no-hypermomentum/LC not promoted")
    p4_rows = read_csv_rows(OUTPUTS["p4"])
    add("VAL2333_03_p4_row_exists", any(row.get("row_id") == "P4R2333_0_hypermomentum_total" and "Delta_abs" in row.get("residual_formula", "") for row in p4_rows), "P4 hypermomentum total row exists")
    add("VAL2333_04_p4_nonready", all(row.get("score_ready") == "false" for row in p4_rows), "P4 rows remain non-score-ready")
    decision_rows = read_csv_rows(OUTPUTS["decision"])
    add("VAL2333_05_next_audit_selected", any(row.get("row_id") == "CGD2333_1_best_next" and row.get("status") == "SELECT_NO_GAMMA_AUDIT_NEXT" for row in decision_rows), "no-Gamma audit selected next")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2333_06_claim_gates_block", any(row.get("row_id") == "CG2333_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2333_07_github_blocked", any(row.get("row_id") == "CG2333_6_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2333_08_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2333_09_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2333_10_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2333_11_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2333*.csv", "*2333-Y5*.md", "*NOHYPERMOMENTUM*2333*", "*P4*2333*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2333_12_formalization_untouched_by_2333", not formalization_hits, "no 2333 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2333_OVERALL", all(row["status"] == "PASS" for row in rows), "2333 tests no-hypermomentum/Levi-Civita source connection, refuses to import GR connection assumptions, retains the P4 hypermomentum residual row, selects no-Gamma slot audit next, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2333 - noHypermomentum LeviCivita Source Connection Or P4 Row

## Summary

2333 attacks the spin/torsion/nonmetricity head of the non-Hilbert trident.

The clean theorem route is:

`Gamma_obs = Gamma_LC[g_obs]` and `Delta_lambda^{{mu nu}} = delta S_ord / delta Gamma^lambda_{{mu nu}} = 0`.

That closes if the parent ordinary/source/readout branch has no independent `Gamma` argument, or if a Palatini/EH
route plus no-hypermomentum and projective silence is signed. Current corpus does not close either route.

So 2333 does not import Levi-Civita from GR by assumption. It retains the P4 hypermomentum residual row:

`Delta_abs := ||Delta_matter|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary||`.

Next clean target: audit every matter/source/readout sector for an independent `Gamma` slot.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## noHypermomentum LeviCivita Proof Audit

{markdown_table(proof_rows, ["row_id", "route", "formal_statement", "status", "obstruction", "effect_if_closed", "valid_for_claim"])}

## P4 Hypermomentum Residual Row

{markdown_table(p4_rows, ["row_id", "channel", "residual_symbol", "residual_formula", "affected_tests", "units", "current_status", "score_ready", "valid_for_claim"])}

## Connection Gate Decision Ledger

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
        "proof": build_proof_rows(),
        "p4": build_p4_rows(),
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
        rows_by_output["proof"],
        rows_by_output["p4"],
        rows_by_output["decision"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2333 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
