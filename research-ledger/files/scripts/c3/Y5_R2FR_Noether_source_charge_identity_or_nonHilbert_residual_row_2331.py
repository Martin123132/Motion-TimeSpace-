from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NOETHER_SOURCE_CHARGE_IDENTITY_OR_NONHILBERT_RESIDUAL_2331"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2331-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md"

PATHS = {
    "2330_doc": ROOT / "2330-Y5-R2FR-parent-action-adoption-vs-deeper-quotient-derivation-decision.md",
    "2330_validation": OUT / "P8_Y5_BRR545_2330_VALIDATION.csv",
    "2330_derivation": OUT / "P8_Y5_PARENT_QLOC_2330_DEEPER_QUOTIENT_DERIVATION_AUDIT.csv",
    "2330_decision": OUT / "P8_Y5_PARENT_QLOC_2330_ADOPTION_DECISION_MATRIX.csv",
    "2330_restriction": OUT / "P8_Y5_PARENT_QLOC_2330_PARENT_ACTION_RESTRICTION_DRAFT.csv",
    "2330_impact": OUT / "P8_Y5_PARENT_QLOC_2330_DOWNSTREAM_GATE_IMPACT.csv",
    "2329_signature": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv",
    "2329_proof": OUT / "P8_Y5_PARENT_QLOC_2329_NOSOURCE_SLOT_THEOREM_PROOF.csv",
    "no_species_contract": OUT / "P8_no_species_source_charge_CONTRACT.csv",
    "ward_owner_contract": OUT / "P8_Ward_source_owner_identity_CONTRACT.csv",
    "ward_universality_contract": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "1936_hilbert_contract": OUT / "P8_Y5_PARENT_QLOC_1936_HILBERT_SOURCE_CONTRACT.csv",
    "1937_hilbert_theorem": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
    "1938_ward_bianchi": OUT / "P8_Y5_PARENT_QLOC_1938_WARD_BIANCHI_CONSERVATION_THEOREM.csv",
    "1958_owner": OUT / "P8_Y5_PARENT_QLOC_1958_CURRENT_OWNER_NONHILBERT_ATTEMPT.csv",
    "1958_bound": OUT / "P8_Y5_PARENT_QLOC_1958_NONHILBERT_CURRENT_BOUND_LEDGER.csv",
    "2146_noether": OUT / "P8_Y5_PARENT_QLOC_2146_NOETHER_CURRENT_GATE.csv",
    "1889_ward_owner": OUT / "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "1793_charge_owner": OUT / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
}

SOURCES = [
    ("SRC2331_00_2330_doc", "2330_doc", PATHS["2330_doc"], ["NEXT2330_0", "Noether-source-charge"], "2330 handoff"),
    ("SRC2331_01_2330_validation", "2330_validation", PATHS["2330_validation"], ["VAL2330_OVERALL", "PASS"], "2330 validation"),
    ("SRC2331_02_2330_derivation", "2330_derivation", PATHS["2330_derivation"], ["DQD2330_4_no_independent_gravitational_charge", "BEST_DEEPER_DERIVATION_TARGET"], "deeper derivation target"),
    ("SRC2331_03_2330_decision", "2330_decision", PATHS["2330_decision"], ["ADM2330_3_decision", "PROVISIONAL_ADOPTION_PLUS_DERIVATION_AUDIT"], "dual-track decision"),
    ("SRC2331_04_2330_restriction", "2330_restriction", PATHS["2330_restriction"], ["PAR2330_0_name", "PROVISIONAL_PRIVATE_CONTRACT_ONLY"], "private MUMC restriction"),
    ("SRC2331_05_2330_impact", "2330_impact", PATHS["2330_impact"], ["DGI2330_3_local_GR_Newton", "blocked"], "downstream local-GR impact"),
    ("SRC2331_06_2329_signature", "2329_signature", PATHS["2329_signature"], ["SBF2329_5_nonhilbert_residual_policy", "OPEN_PARALLEL_GATE_RETAINED"], "source-blind signature hidden-current caveat"),
    ("SRC2331_07_2329_proof", "2329_proof", PATHS["2329_proof"], ["NST2329_5_source_side_GR", "CONDITIONAL_SOURCE_SIDE_GR_THEOREM"], "source-side GR conditional"),
    ("SRC2331_08_no_species_contract", "no_species_contract", PATHS["no_species_contract"], ["S4_source_normalization_species_blind", "not_parent_derived"], "no species source charge contract"),
    ("SRC2331_09_ward_owner_contract", "ward_owner_contract", PATHS["ward_owner_contract"], ["C5_no_species_or_marker_source_charge", "not_parent_derived"], "Ward source owner contract"),
    ("SRC2331_10_ward_universality", "ward_universality_contract", PATHS["ward_universality_contract"], ["SC4_no_nonHilbert_source_current", "not_parent_derived"], "source-current Ward universality contract"),
    ("SRC2331_11_1936_hilbert_contract", "1936_hilbert_contract", PATHS["1936_hilbert_contract"], ["HIL1936_2_no_species_weight", "MISSING_NO_SOURCE_WEIGHT_THEOREM"], "Hilbert source contract"),
    ("SRC2331_12_1937_hilbert_theorem", "1937_hilbert_theorem", PATHS["1937_hilbert_theorem"], ["HST1937_3_verdict", "NOT_DERIVED"], "Hilbert theorem status"),
    ("SRC2331_13_1938_ward_bianchi", "1938_ward_bianchi", PATHS["1938_ward_bianchi"], ["WB1938_0_matter_ward_identity", "EXACT_CONDITIONAL_THEOREM"], "Ward/Bianchi theorem"),
    ("SRC2331_14_1958_owner", "1958_owner", PATHS["1958_owner"], ["OWN1958_6_verdict", "ZERO_PROOF_FAILED_CLEANLY"], "current-owner non-Hilbert attempt"),
    ("SRC2331_15_1958_bound", "1958_bound", PATHS["1958_bound"], ["NB1958_0_nonHilbert_bound", "MISSING_FACTORS"], "non-Hilbert bound ledger"),
    ("SRC2331_16_2146_noether", "2146_noether", PATHS["2146_noether"], ["NC2146_5_source_hamiltonian_bridge", "PRIMARY_SOURCE_SIDE_BLOCKER"], "Noether current gate"),
    ("SRC2331_17_1889_ward_owner", "1889_ward_owner", PATHS["1889_ward_owner"], ["SWO1889_7_verdict", "SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED"], "Ward source-current owner attempt"),
    ("SRC2331_18_1793_charge_owner", "1793_charge_owner", PATHS["1793_charge_owner"], ["Y5SC1793_7_verdict", "SOURCE_CHARGE_OWNER_THEOREM_NOT_ACTIVATED"], "source charge owner attempt"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2331_SOURCE_REGISTER.csv",
    "identity": OUT / "P8_Y5_PARENT_QLOC_2331_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv",
    "residual": OUT / "P8_Y5_PARENT_QLOC_2331_NONHILBERT_RESIDUAL_ROW.csv",
    "impact": OUT / "P8_Y5_PARENT_QLOC_2331_SOURCE_CHARGE_GATE_IMPACT.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2331_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2331_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2331_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2331_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2331_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2331_0_identity", OUTPUTS["identity"], BETA_DOCS / "NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT_2331_NONCLAIM.csv"),
    ("COPY2331_1_residual", OUTPUTS["residual"], MICRO_RESIDUALS / "nonHilbert_residual_row_2331_nonclaim.csv"),
    ("COPY2331_2_impact", OUTPUTS["impact"], RAB_QUEUE / "JR2331_SOURCE_CHARGE_GATE_IMPACT_NONCLAIM.csv"),
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


def build_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_0_target",
            "identity_piece": "Noether source charge identity",
            "formal_statement": "J_active for ordinary matter equals the Hilbert/Noether source charge of the same observed matter action, with no independent gravitational source charge.",
            "status": "TARGET_SHARPENED",
            "proof_or_obstruction": "this is the purist derivation target behind Minimal Universal Matter Coupling",
            "if_closed": "source-only species charge is derived absent rather than provisionally restricted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_1_hilbert_owner",
            "identity_piece": "Hilbert source owner",
            "formal_statement": "If a single observed matter action is fixed, T_H := delta S_m/delta e_obs is the active source before readout.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "works only after the parent matter action/signature is fixed; does not itself forbid pre-action w_A",
            "if_closed": "post-variation source-current rescaling is killed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_2_ward_noether",
            "identity_piece": "Ward/Noether conservation",
            "formal_statement": "Diffeomorphism invariance of S_m gives covariant conservation of T_H on matter shell.",
            "status": "EXACT_CONDITIONAL_CONSERVATION",
            "proof_or_obstruction": "conservation of the chosen source does not choose the source or its universal normalization",
            "if_closed": "source current is dynamically consistent, not yet unique against all countermodels",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_3_canonical_improvement",
            "identity_piece": "canonical-to-Hilbert improvement",
            "formal_statement": "Noether/canonical stress differs from Hilbert stress by owned improvement terms plus possible boundary flux.",
            "status": "CONDITIONAL_IMPROVEMENT_BOUND_REQUIRED",
            "proof_or_obstruction": "safe only if compact exterior boundary/improvement flux is zero or bounded",
            "if_closed": "ordinary current ambiguity does not become independent source charge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_4_pre_action_weight",
            "identity_piece": "pre-action species weights",
            "formal_statement": "S_m=sum_A w_A S_A still has a Hilbert/Noether current, but it is a weighted current if w_A is legal before variation.",
            "status": "COUNTERMODEL_SURVIVES_WITHOUT_MUMC",
            "proof_or_obstruction": "Noether identity conserves the weighted current; it does not forbid the weight",
            "if_closed": "requires MUMC/source-blind signature or deeper no-independent-gravitational-charge theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_5_nonhilbert_channels",
            "identity_piece": "non-Hilbert source-current channels",
            "formal_statement": "spin/torsion, boundary/worldtube, readout reentry, and improvement flux channels must vanish, be exact/projected silent, or remain explicit residuals.",
            "status": "OPEN_RETAIN_RESIDUAL_ROW",
            "proof_or_obstruction": "Hilbert/Noether identity for ordinary matter does not automatically silence all non-Hilbert currents",
            "if_closed": "source-side GR theorem can drop a major bypass channel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_6_projected_mass_charge",
            "identity_piece": "projected measured-GM charge",
            "formal_statement": "M_eff must be a closed calibrated projection of the Hilbert/Hamiltonian/worldtube charge before Kepler/PPN readout.",
            "status": "PROJECTED_MASS_CHARGE_NOT_CLOSED",
            "proof_or_obstruction": "Pi_M commutator, exchange current, boundary flux, and orbital calibration remain stronger than Ward conservation",
            "if_closed": "measured GM becomes a derived source charge rather than fitted normalization",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NSCI2331_7_verdict",
            "identity_piece": "derive no independent gravitational source charge now",
            "formal_statement": "2331 proves ordinary matter has no independent gravitational source charge beyond Hilbert/Noether stress source in the active corpus.",
            "status": "NOT_DERIVED_RETAIN_NONHILBERT_ROW",
            "proof_or_obstruction": "Noether/Hilbert gives a conditional owner, but pre-action weights, non-Hilbert channels, and projected mass-charge closure remain open",
            "if_closed": "not closed yet; use residual ledger and continue derivation",
            "valid_for_claim": "false",
        },
    ]


def build_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHR2331_0_total",
            "residual_symbol": "||P_source[J_NH]||",
            "definition": "projected non-Hilbert source-current envelope after Hilbert matter current is extracted",
            "bound_form": "||P_source[J_NH]|| <= ||J_spin/torsion|| + ||J_boundary|| + ||J_readout|| + ||J_improvement_flux||",
            "units": "source-current units; projection-dependent",
            "status": "CONTRACT_READY_FACTORS_MISSING",
            "next_input": "zero theorem or envelope for each component in common units",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHR2331_1_spin_torsion",
            "residual_symbol": "||J_spin/torsion||",
            "definition": "spin, torsion, nonmetricity, or hypermomentum source-current projection",
            "bound_form": "zero if parent connection is Levi-Civita/metric-compatible for matter source or projected exact; otherwise finite envelope",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "next_input": "torsionless/Levi-Civita matter-connection theorem or sourced spin-current envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHR2331_2_boundary_worldtube",
            "residual_symbol": "||J_boundary||",
            "definition": "boundary, worldtube, compact flux, or improvement surface source current",
            "bound_form": "zero if exterior compact flux vanishes; otherwise boundary/source-worldtube envelope",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "next_input": "boundary no-flux theorem or source-backed flux bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHR2331_3_readout_reentry",
            "residual_symbol": "||J_readout||",
            "definition": "post-variation readout, domain, marker, or frame map that re-enters as source-labelled current",
            "bound_form": "zero if readout is downstream and source-blind; otherwise retained marker-current envelope",
            "units": "source-current units",
            "status": "MISSING_ZERO_OR_ENVELOPE",
            "next_input": "readout no-reentry proof or explicit marker/source residual",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHR2331_4_projected_mass",
            "residual_symbol": "Delta_M_projected",
            "definition": "commutator/exchange term between Hilbert charge conservation and measured-GM mass projector",
            "bound_form": "Delta_M_projected = [d,Pi_M]J_H + Pi_M J_exchange + boundary/anomaly flux",
            "units": "mass-charge or dimensionless after GM normalization",
            "status": "PROJECTOR_CLOSURE_MISSING",
            "next_input": "Pi_M ownership, exchange-current silence, and Gauss/orbital calibration",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCI2331_0_MUMC_branch",
            "gate": "Minimal Universal Matter Coupling private branch",
            "impact": "under MUMC, pre-action w_A is forbidden by restriction, not derived by 2331",
            "still_missing": "Noether/source-charge derivation of the restriction",
            "claim_status": "private_condition_only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCI2331_1_no_species_charge",
            "gate": "no independent gravitational source charge",
            "impact": "Hilbert/Noether identity supports the source owner once the action is fixed",
            "still_missing": "proof that no pre-action species source coefficient is admissible",
            "claim_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCI2331_2_nonhilbert_gate",
            "gate": "non-Hilbert/boundary/readout source currents",
            "impact": "must be zero/bounded before source-side GR claim",
            "still_missing": "spin/torsion, boundary flux, readout reentry, improvement flux inputs",
            "claim_status": "retained_residual",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCI2331_3_GM_source_charge",
            "gate": "measured-GM projected source charge",
            "impact": "Ward conservation alone does not derive calibrated GM",
            "still_missing": "closed Pi_M J_H, exchange silence, boundary flux zero, Kepler calibration",
            "claim_status": "not_closed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCI2331_4_local_GR_Newton",
            "gate": "full local GR/Newton recovery",
            "impact": "2331 improves the source-side map but does not close local GR",
            "still_missing": "left-hand EH/Newton limit, PPN/readout residuals, projector/domain closure",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2331_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2331_1_Hilbert_Noether_owner", "gate": "Hilbert/Noether source owner exact conditionally", "passed": "true", "claim_effect": "conditional theorem retained", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2331_2_no_independent_charge_derived", "gate": "no independent gravitational source charge derived now", "passed": "false", "claim_effect": "pre-action weights and source-charge identity still open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2331_3_nonhilbert_silence", "gate": "non-Hilbert source current is zero", "passed": "false", "claim_effect": "residual row required", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2331_4_projected_GM_charge", "gate": "measured-GM charge derived from closed Hilbert projection", "passed": "false", "claim_effect": "GM source normalization not claimed", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2331_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "not enough yet", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2331_6_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "private derivation/residual checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2331_0_conservation_as_uniqueness", "claim": "Ward conservation proves unique species-blind source normalization", "allowed": "false", "reason": "conservation preserves a chosen weighted current; it does not forbid pre-action weights", "blocking_rows": "NSCI2331_2_ward_noether;NSCI2331_4_pre_action_weight", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2331_1_hilbert_as_nonhilbert_silence", "claim": "Hilbert owner automatically kills non-Hilbert currents", "allowed": "false", "reason": "spin/torsion, boundary, readout reentry, and improvement flux remain separate channels", "blocking_rows": "NSCI2331_5_nonhilbert_channels;NHR2331_0_total", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2331_2_GM_from_Ward_only", "claim": "Ward identity derives measured GM/source-normalized Newton", "allowed": "false", "reason": "projected mass-charge closure and orbital calibration are stronger than unprojected conservation", "blocking_rows": "NSCI2331_6_projected_mass_charge;NHR2331_4_projected_mass", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2331_3_public_claim", "claim": "2331 proves local GR/Newton", "allowed": "false", "reason": "2331 records a conditional source owner and residual row; local GR remains blocked", "blocking_rows": "SCI2331_4_local_GR_Newton;CG2331_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2331_0",
            "next_target": "2332-Y5-R2FR-nonHilbert-current-silence-spin-boundary-readout-trident.md",
            "why": "2331 leaves three non-Hilbert bypasses: spin/torsion, boundary/improvement flux, and readout reentry; the next clean move is to attack them separately.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2331_1",
            "next_target": "2332b-Y5-R2FR-Hilbert-Noether-mass-projector-closure.md",
            "why": "parallel source-normalized Newton route: close d(Pi_M J_H)=0 and GM calibration rather than only unprojected Ward conservation.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2331_2",
            "next_target": "2332c-Y5-R2FR-MUMC-private-branch-ledger-update.md",
            "why": "track which rows are conditional on the private MUMC restriction so later docs do not confuse it with a derivation.",
            "claim_status": "branch_bookkeeping_nonclaim",
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

    add("VAL2331_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2331_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    identity_rows = read_csv_rows(OUTPUTS["identity"])
    add("VAL2331_02_conditional_owner", any(row.get("row_id") == "NSCI2331_1_hilbert_owner" and row.get("status") == "EXACT_CONDITIONAL_THEOREM" for row in identity_rows), "Hilbert/Noether source owner retained conditionally")
    add("VAL2331_03_identity_not_overclaimed", any(row.get("row_id") == "NSCI2331_7_verdict" and row.get("status") == "NOT_DERIVED_RETAIN_NONHILBERT_ROW" for row in identity_rows), "no independent source charge not overclaimed")
    residual_rows = read_csv_rows(OUTPUTS["residual"])
    add("VAL2331_04_residual_row_exists", any(row.get("row_id") == "NHR2331_0_total" and "J_spin/torsion" in row.get("bound_form", "") for row in residual_rows), "non-Hilbert residual total row exists")
    add("VAL2331_05_residual_nonready", all(row.get("score_ready") == "false" for row in residual_rows), "non-Hilbert residual rows remain non-score-ready")
    impact_rows = read_csv_rows(OUTPUTS["impact"])
    add("VAL2331_06_local_gr_still_blocked", any(row.get("row_id") == "SCI2331_4_local_GR_Newton" and row.get("claim_status") == "blocked" for row in impact_rows), "local GR/Newton still not claimed")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2331_07_claim_gates_block", any(row.get("row_id") == "CG2331_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2331_08_github_blocked", any(row.get("row_id") == "CG2331_6_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2331_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2331_10_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2331_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2331_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2331*.csv", "*2331-Y5*.md", "*NOETHER_SOURCE*2331*", "*NONHILBERT*2331*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2331_13_formalization_untouched_by_2331", not formalization_hits, "no 2331 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2331_OVERALL", all(row["status"] == "PASS" for row in rows), "2331 shows Hilbert/Noether source ownership is exact only conditionally, refuses to infer no independent source charge from conservation alone, stages the non-Hilbert residual row, keeps projected-GM/local-GR gates blocked, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2331 - Noether Source Charge Identity Or NonHilbert Residual Row

## Summary

2331 tries the purist source-charge route.

Result: Hilbert/Noether source ownership is real, but conditional. Once an observed matter action is fixed, its
Hilbert variation is the ordinary matter source and Ward/Noether identities conserve it on shell. That is a useful
source-owner theorem.

But it does **not** by itself prove that no independent gravitational source charge exists. A pre-action species weight
can still be conserved if it is legal, and non-Hilbert channels can still re-enter through spin/torsion, boundary flux,
readout reentry, or improvement flux. The projected measured-GM charge is also stronger than unprojected Ward
conservation.

So 2331 keeps the theorem conditional and stages the residual row:

`||P_source[J_NH]|| <= ||J_spin/torsion|| + ||J_boundary|| + ||J_readout|| + ||J_improvement_flux||`.

This is not local GR yet. It is a sharper source-side map.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Noether Source Charge Identity Attempt

{markdown_table(identity_rows, ["row_id", "identity_piece", "formal_statement", "status", "proof_or_obstruction", "if_closed", "valid_for_claim"])}

## NonHilbert Residual Row

{markdown_table(residual_rows, ["row_id", "residual_symbol", "definition", "bound_form", "units", "status", "next_input", "score_ready", "valid_for_claim"])}

## Source Charge Gate Impact

{markdown_table(impact_rows, ["row_id", "gate", "impact", "still_missing", "claim_status", "valid_for_claim"])}

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
        "identity": build_identity_rows(),
        "residual": build_residual_rows(),
        "impact": build_impact_rows(),
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
        rows_by_output["identity"],
        rows_by_output["residual"],
        rows_by_output["impact"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2331 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
