from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NONHILBERT_CURRENT_SILENCE_TRIDENT_2332"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2332-Y5-R2FR-nonHilbert-current-silence-spin-boundary-readout-trident.md"

PATHS = {
    "2331_doc": ROOT / "2331-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md",
    "2331_validation": OUT / "P8_Y5_BRR545_2331_VALIDATION.csv",
    "2331_identity": OUT / "P8_Y5_PARENT_QLOC_2331_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv",
    "2331_residual": OUT / "P8_Y5_PARENT_QLOC_2331_NONHILBERT_RESIDUAL_ROW.csv",
    "2331_impact": OUT / "P8_Y5_PARENT_QLOC_2331_SOURCE_CHARGE_GATE_IMPACT.csv",
    "1450_guard": OUT / "P8_Y5_R10_1450_NONHILBERT_CURRENT_GUARD.csv",
    "1452_ledger": OUT / "P8_Y5_R10_1452_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv",
    "1453_zeta": OUT / "P8_Y5_R10_1453_ZETA_A_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv",
    "1453_audit": OUT / "P8_Y5_R10_1453_HILBERT_NOETHER_ROUTE_AUDIT.csv",
    "1767_audit": OUT / "P8_Y5_PARENT_QLOC_1767_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv",
    "1958_attempt": OUT / "P8_Y5_PARENT_QLOC_1958_CURRENT_OWNER_NONHILBERT_ATTEMPT.csv",
    "1958_bound": OUT / "P8_Y5_PARENT_QLOC_1958_NONHILBERT_CURRENT_BOUND_LEDGER.csv",
    "2041_torsion": OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
    "960_torsion": OUT / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
    "2061_boundary": OUT / "P8_Y5_PARENT_QLOC_2061_BOUNDARY_CURRENT_DERIVATION.csv",
    "592_improvement": OUT / "P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv",
    "729_improvement": OUT / "P8_Y5_R10_729_IMPROVEMENT_AMBIGUITY_GATE.csv",
    "1700_readout": OUT / "P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv",
    "1486_readout": OUT / "P8_Y5_R10_1486_NO_SHADOW_READOUT_REENTRY_AUDIT.csv",
    "1523_projector": OUT / "P8_Y5_PARENT_QLOC_1523_PLOC_PROJECTOR_AUDIT.csv",
}

SOURCES = [
    ("SRC2332_00_2331_doc", "2331_doc", PATHS["2331_doc"], ["NEXT2331_0", "nonHilbert-current-silence"], "2331 handoff"),
    ("SRC2332_01_2331_validation", "2331_validation", PATHS["2331_validation"], ["VAL2331_OVERALL", "PASS"], "2331 validation"),
    ("SRC2332_02_2331_identity", "2331_identity", PATHS["2331_identity"], ["NSCI2331_5_nonhilbert_channels", "OPEN_RETAIN_RESIDUAL_ROW"], "non-Hilbert identity gap"),
    ("SRC2332_03_2331_residual", "2331_residual", PATHS["2331_residual"], ["NHR2331_0_total", "J_spin/torsion"], "non-Hilbert residual contract"),
    ("SRC2332_04_2331_impact", "2331_impact", PATHS["2331_impact"], ["SCI2331_2_nonhilbert_gate", "retained_residual"], "source charge impact"),
    ("SRC2332_05_1450_guard", "1450_guard", PATHS["1450_guard"], ["NHG1450_3_retained", "RETAINED_NONCLAIM"], "non-Hilbert guard"),
    ("SRC2332_06_1452_ledger", "1452_ledger", PATHS["1452_ledger"], ["NH1452_3_retained", "RETAINED_NONCLAIM"], "non-Hilbert ledger"),
    ("SRC2332_07_1453_zeta", "1453_zeta", PATHS["1453_zeta"], ["ZETA1453_4_bound_route", "BOUND_INPUTS_MISSING"], "zeta non-Hilbert bound route"),
    ("SRC2332_08_1453_audit", "1453_audit", PATHS["1453_audit"], ["HNA1453_5_verdict", "PARTIAL_NOT_CLOSED"], "Hilbert/Noether route audit"),
    ("SRC2332_09_1767_audit", "1767_audit", PATHS["1767_audit"], ["NHB1767_5_verdict", "INVENTORY_READY_NONCLAIM"], "non-Hilbert inventory"),
    ("SRC2332_10_1958_attempt", "1958_attempt", PATHS["1958_attempt"], ["OWN1958_6_verdict", "ZERO_PROOF_FAILED_CLEANLY"], "current-owner non-Hilbert attempt"),
    ("SRC2332_11_1958_bound", "1958_bound", PATHS["1958_bound"], ["NB1958_0_nonHilbert_bound", "MISSING_FACTORS"], "non-Hilbert bound ledger"),
    ("SRC2332_12_2041_torsion", "2041_torsion", PATHS["2041_torsion"], ["LC2041_3_hypermomentum", "SELECTED_NEXT_BLOCKED_GATE"], "torsion/no-hypermomentum route"),
    ("SRC2332_13_960_torsion", "960_torsion", PATHS["960_torsion"], ["LC960_4_verdict", "not_closed_current_corpus"], "Levi-Civita gate"),
    ("SRC2332_14_2061_boundary", "2061_boundary", PATHS["2061_boundary"], ["DER2061_2_zero_theorem", "THEOREM_EXACT_IF_ALL_CLAUSES_PARENT_SIGNED"], "boundary current derivation"),
    ("SRC2332_15_592_improvement", "592_improvement", PATHS["592_improvement"], ["IAG592_0_superpotential_improvement", "open"], "improvement ambiguity source"),
    ("SRC2332_16_729_improvement", "729_improvement", PATHS["729_improvement"], ["IAG729_4_matter_improper_charge", "open"], "improvement ambiguity audit"),
    ("SRC2332_17_1700_readout", "1700_readout", PATHS["1700_readout"], ["RNR1700_2_commutator", "formula_target"], "readout no-reentry target"),
    ("SRC2332_18_1486_readout", "1486_readout", PATHS["1486_readout"], ["NSR1486_4_verdict", "OBSTRUCTION_SURVIVES"], "shadow readout reentry audit"),
    ("SRC2332_19_1523_projector", "1523_projector", PATHS["1523_projector"], ["PLOC1523_3_variation_silence", "NOT_ZERO_DERIVED"], "projector stress audit"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2332_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv",
    "envelopes": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_RESIDUAL_ENVELOPES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2332_TRIDENT_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2332_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2332_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2332_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2332_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2332_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2332_0_audit", OUTPUTS["audit"], BETA_DOCS / "NONHILBERT_TRIDENT_SILENCE_AUDIT_2332_NONCLAIM.csv"),
    ("COPY2332_1_envelopes", OUTPUTS["envelopes"], MICRO_RESIDUALS / "nonHilbert_residual_envelopes_2332_nonclaim.csv"),
    ("COPY2332_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2332_TRIDENT_DECISION_LEDGER_NONCLAIM.csv"),
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
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHT2332_0_total",
            "trident_head": "total non-Hilbert source current",
            "zero_route": "J_NH=0 if spin/torsion, boundary/improvement, and readout reentry heads are each absent/exact/projected-silent",
            "result": "NOT_ZERO_RETAIN_COMPONENTS",
            "obstruction": "none of the three heads is parent-signed silent in current corpus",
            "fallback": "absolute residual envelope, no cancellation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHT2332_1_spin_torsion",
            "trident_head": "spin/torsion/nonmetricity/hypermomentum",
            "zero_route": "connection is metric-only Levi-Civita, or Palatini EH plus no matter/source/readout hypermomentum, or projection is exact/silent",
            "result": "NOT_ZERO_DERIVED",
            "obstruction": "metric-only parent, EH-only Palatini, projective silence, and no-hypermomentum clauses remain unsigned",
            "fallback": "retain ||J_spin/torsion|| envelope or P4 connection residual rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHT2332_2_boundary_improvement",
            "trident_head": "boundary/worldtube/improvement flux",
            "zero_route": "boundary charge/improvement flux is fixed by differentiable Hamiltonian reference and has zero compact local projection",
            "result": "NOT_ZERO_DERIVED",
            "obstruction": "boundary clauses, improvement representative, orientation, and improper charge projection remain open",
            "fallback": "retain ||J_boundary|| + ||J_improvement_flux|| envelope",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHT2332_3_readout_reentry",
            "trident_head": "readout/domain/frame reentry",
            "zero_route": "all readout maps act downstream and cannot create Coeff_active_source[species] or source-labelled current terms",
            "result": "NOT_ZERO_DERIVED",
            "obstruction": "readout closure, shadow-frame guard, commutator, and projector-stress silence remain unsigned",
            "fallback": "retain ||J_readout|| envelope and readout-variation commutator row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHT2332_4_partial_win",
            "trident_head": "Hilbert owner still useful",
            "zero_route": "variation of the fixed matter action owns T_H and prevents post-variation source rescaling when readout order is signed",
            "result": "PARTIAL_CONDITIONAL_WIN",
            "obstruction": "does not kill the three non-Hilbert heads",
            "fallback": "use T_H as baseline and add J_NH envelope explicitly",
            "valid_for_claim": "false",
        },
    ]


def build_envelope_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHE2332_0_total_abs",
            "quantity": "P_source_J_NH_abs",
            "bound_form": "||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement",
            "component_inputs": "E_spin; E_boundary; E_readout; E_improvement",
            "units": "source-current units; convert to PPN/WEP/orbit units by arena projector",
            "status": "CONTRACT_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHE2332_1_spin",
            "quantity": "E_spin",
            "bound_form": "E_spin >= ||P_source[J_spin/torsion/nonmetricity/hypermomentum]||",
            "component_inputs": "torsionless theorem or P4 torsion/nonmetricity/hypermomentum coefficient map",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHE2332_2_boundary",
            "quantity": "E_boundary",
            "bound_form": "E_boundary >= ||P_source[J_boundary/worldtube]||",
            "component_inputs": "boundary no-flux theorem, orientation convention, compact support/falloff, source-worldtube envelope",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHE2332_3_readout",
            "quantity": "E_readout",
            "bound_form": "E_readout >= ||P_source[J_readout_reentry]||",
            "component_inputs": "readout no-reentry theorem or commutator/residual map for each arena",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHE2332_4_improvement",
            "quantity": "E_improvement",
            "bound_form": "E_improvement >= ||P_source[improvement/superpotential flux]||",
            "component_inputs": "Hamiltonian representative, proper vertical domain, edge projection, compact flux bound",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NTD2332_0_spin_first",
            "decision": "attack spin/torsion/no-hypermomentum first",
            "reason": "this is closest to a GR-like structural restriction: metric-only matter connection or Palatini no-hypermomentum",
            "effect": "could remove one major non-Hilbert bypass and simplify clocks/WEP/light/source coupling",
            "status": "SELECTED_NEXT_PRIMARY",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NTD2332_1_boundary_parallel",
            "decision": "keep boundary/improvement flux parallel",
            "reason": "boundary terms can masquerade as source charge; exact accounting exists but zero clauses are unsigned",
            "effect": "prevents accidental loss of physical edge/ADM/Hamiltonian charge",
            "status": "PARALLEL_GATE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NTD2332_2_readout_parallel",
            "decision": "keep readout reentry parallel",
            "reason": "readout maps are the easiest place to smuggle species-labelled source coefficients after variation",
            "effect": "requires commutator/no-reentry proof or finite residual maps per arena",
            "status": "PARALLEL_GATE",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NTD2332_3_verdict",
            "decision": "do not promote non-Hilbert silence",
            "reason": "all three heads are named, but none is parent-signed zero",
            "effect": "source-side GR remains conditional; residual envelopes are mandatory",
            "status": "NONHILBERT_SILENCE_NOT_CLOSED",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2332_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2332_1_trident_classified", "gate": "three non-Hilbert heads classified", "passed": "true", "claim_effect": "obstruction localized", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2332_2_spin_silence", "gate": "spin/torsion/nonmetricity head silent", "passed": "false", "claim_effect": "no-hypermomentum/LC gate open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2332_3_boundary_silence", "gate": "boundary/improvement head silent", "passed": "false", "claim_effect": "boundary flux gate open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2332_4_readout_silence", "gate": "readout reentry head silent", "passed": "false", "claim_effect": "readout commutator gate open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2332_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "non-Hilbert silence not closed", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2332_6_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "private residual checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2332_0_hilbert_owner_as_silence", "claim": "Hilbert source owner kills all non-Hilbert currents", "allowed": "false", "reason": "Hilbert owner gives baseline T_H, but spin/torsion, boundary/improvement and readout reentry are separate channels", "blocking_rows": "NHT2332_1_spin_torsion;NHT2332_2_boundary_improvement;NHT2332_3_readout_reentry", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2332_1_exact_boundary_shortcut", "claim": "boundary/improvement terms are exact so they can be dropped", "allowed": "false", "reason": "exact terms can carry compact/improper edge charge unless projection/falloff/reference are signed", "blocking_rows": "NHT2332_2_boundary_improvement;NHE2332_4_improvement", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2332_2_readout_downstream_shortcut", "claim": "readout is downstream so no reentry proof is needed", "allowed": "false", "reason": "downstream order must be supplemented by commutator/no-source-codomain proof per arena", "blocking_rows": "NHT2332_3_readout_reentry;NHE2332_3_readout", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2332_3_public_claim", "claim": "2332 proves local GR/Newton", "allowed": "false", "reason": "2332 classifies residual channels and selects the next gate; it does not close them", "blocking_rows": "CG2332_5_local_GR_Newton;NTD2332_3_verdict", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2332_0",
            "next_target": "2333-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md",
            "why": "spin/torsion/no-hypermomentum is the cleanest structural route: either show matter/source/readout do not vary an independent connection, or emit first P4 residual row.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2332_1",
            "next_target": "2333b-Y5-R2FR-boundary-improvement-flux-zero-or-envelope.md",
            "why": "boundary/improvement flux remains a parallel source-charge bypass and must not be silently dropped.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2332_2",
            "next_target": "2333c-Y5-R2FR-readout-no-reentry-commutator-or-envelope.md",
            "why": "readout reentry needs a per-arena commutator/no-source-codomain proof or finite residual map.",
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

    add("VAL2332_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2332_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    audit_rows = read_csv_rows(OUTPUTS["audit"])
    add("VAL2332_02_trident_heads", all(any(row.get("row_id") == expected for row in audit_rows) for expected in ["NHT2332_1_spin_torsion", "NHT2332_2_boundary_improvement", "NHT2332_3_readout_reentry"]), "three trident heads audited")
    add("VAL2332_03_zero_not_promoted", any(row.get("row_id") == "NHT2332_0_total" and row.get("result") == "NOT_ZERO_RETAIN_COMPONENTS" for row in audit_rows), "non-Hilbert silence not promoted")
    envelope_rows = read_csv_rows(OUTPUTS["envelopes"])
    add("VAL2332_04_envelope_total", any(row.get("row_id") == "NHE2332_0_total_abs" and "E_spin" in row.get("bound_form", "") for row in envelope_rows), "absolute non-Hilbert envelope exists")
    add("VAL2332_05_envelopes_nonready", all(row.get("score_ready") == "false" for row in envelope_rows), "all envelopes remain non-score-ready")
    decision_rows = read_csv_rows(OUTPUTS["decision"])
    add("VAL2332_06_next_primary", any(row.get("row_id") == "NTD2332_0_spin_first" and row.get("status") == "SELECTED_NEXT_PRIMARY" for row in decision_rows), "spin/torsion selected as next primary gate")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2332_07_claim_gates_block", any(row.get("row_id") == "CG2332_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2332_08_github_blocked", any(row.get("row_id") == "CG2332_6_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2332_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2332_10_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2332_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2332_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2332*.csv", "*2332-Y5*.md", "*NONHILBERT*2332*", "*TRIDENT*2332*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2332_13_formalization_untouched_by_2332", not formalization_hits, "no 2332 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2332_OVERALL", all(row["status"] == "PASS" for row in rows), "2332 classifies the non-Hilbert trident, refuses to promote silence, stages absolute residual envelopes, selects no-hypermomentum/Levi-Civita as next primary gate, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2332 - nonHilbert Current Silence Spin/Boundary/Readout Trident

## Summary

2332 splits the non-Hilbert source-current bypass into three heads:

1. spin/torsion/nonmetricity/hypermomentum,
2. boundary/worldtube/improvement flux,
3. readout/domain/frame reentry.

Result: none of the three is parent-signed silent yet. The useful gain is that the source-side obstruction is no longer
vague. It is now an absolute residual envelope:

`||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement`.

The best next primary attack is no-hypermomentum / Levi-Civita source connection: either show ordinary matter/source/readout
do not vary an independent connection, or emit a first P4 residual row.

This remains private, nonclaim work.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## nonHilbert Trident Silence Audit

{markdown_table(audit_rows, ["row_id", "trident_head", "zero_route", "result", "obstruction", "fallback", "valid_for_claim"])}

## nonHilbert Residual Envelopes

{markdown_table(envelope_rows, ["row_id", "quantity", "bound_form", "component_inputs", "units", "status", "score_ready", "valid_for_claim"])}

## Trident Decision Ledger

{markdown_table(decision_rows, ["row_id", "decision", "reason", "effect", "status", "valid_for_claim"])}

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
        "audit": build_audit_rows(),
        "envelopes": build_envelope_rows(),
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
        rows_by_output["audit"],
        rows_by_output["envelopes"],
        rows_by_output["decision"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2332 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
