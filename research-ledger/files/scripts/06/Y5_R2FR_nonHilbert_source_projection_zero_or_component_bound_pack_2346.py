from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NONHILBERT_SOURCE_PROJECTION_ZERO_OR_COMPONENT_BOUND_PACK_2346"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md"

PATHS = {
    "2345_doc": ROOT / "2345-Y5-R2FR-current-owner-normal-form-from-parent-variation-or-sourceGM-residual-first-row.md",
    "2345_validation": OUT / "P8_Y5_BRR545_2345_VALIDATION.csv",
    "2345_next": OUT / "P8_Y5_PARENT_QLOC_2345_NEXT_TARGET.csv",
    "2345_residual": OUT / "P8_Y5_PARENT_QLOC_2345_SOURCEGM_CURRENT_OWNER_RESIDUAL_FIRST_ROW.csv",
    "2332_trident": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv",
    "2332_envelopes": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_RESIDUAL_ENVELOPES.csv",
    "2333_nohyper": OUT / "P8_Y5_PARENT_QLOC_2333_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
    "2333_p4": OUT / "P8_Y5_PARENT_QLOC_2333_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
    "2335_srng": OUT / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
    "2337_boundary": OUT / "P8_Y5_PARENT_QLOC_2337_BOUNDARY_IMPROVEMENT_QUEUE.csv",
    "2338_boundary_deps": OUT / "P8_Y5_PARENT_QLOC_2338_BOUNDARY_DENOMINATOR_DEPENDENCY.csv",
    "2311_boundary_neutrality": OUT / "P8_Y5_PARENT_QLOC_2311_BOUNDARY_SOURCE_NEUTRALITY.csv",
    "2042_nohyper": OUT / "P8_Y5_PARENT_QLOC_2042_NO_HYPERMOMENTUM_THEOREM_ATTEMPT.csv",
    "2041_connection": OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
    "2122_readout_owner": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
    "2118_readout_zero": OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv",
}

SOURCES = [
    ("SRC2346_00_2345_doc", "2345_doc", ["RCO2345_0_schema", "NEXT2345_0"], "2345 selected non-Hilbert projection zero"),
    ("SRC2346_01_2345_validation", "2345_validation", ["VAL2345_OVERALL", "PASS"], "2345 validation"),
    ("SRC2346_02_2345_next", "2345_next", ["NEXT2345_0", "nonHilbert-source-projection"], "machine-readable 2346 target"),
    ("SRC2346_03_2345_residual", "2345_residual", ["RCO2345_0_schema", "epsilon_current_owner_NH_abs"], "current-owner residual schema"),
    ("SRC2346_04_2332_trident", "2332_trident", ["NHT2332_0_total", "NOT_ZERO_RETAIN_COMPONENTS"], "three-headed non-Hilbert silence audit"),
    ("SRC2346_05_2332_envelopes", "2332_envelopes", ["NHE2332_0_total_abs", "E_spin"], "non-Hilbert envelope rows"),
    ("SRC2346_06_2333_nohyper", "2333_nohyper", ["NHL2333_6_verdict", "NOT_DERIVED"], "no-hypermomentum/Levi-Civita proof audit"),
    ("SRC2346_07_2333_p4", "2333_p4", ["P4R2333_0_hypermomentum_total", "Delta_abs"], "P4 hypermomentum residual rows"),
    ("SRC2346_08_2335_srng", "2335_srng", ["SRNG2335_6_verdict", "Gamma-free"], "source/readout no-Gamma argument certificate"),
    ("SRC2346_09_2337_boundary", "2337_boundary", ["BND2337_0_B_zero_flux", "MISSING_THEOREM_OR_VALUE"], "boundary improvement queue"),
    ("SRC2346_10_2338_boundary_deps", "2338_boundary_deps", ["BDD2338_0_theta_Qtau", "MISSING_PARENT_EXTRACTION"], "boundary denominator dependencies"),
    ("SRC2346_11_2311_boundary_neutrality", "2311_boundary_neutrality", ["BSN2311_4_no_cancellation_policy", "BSN2311_5_verdict"], "boundary/source neutrality certificate"),
    ("SRC2346_12_2042_nohyper", "2042_nohyper", ["NH2042_1_no_gamma_slot", "NH2042_5_verdict"], "older no-hypermomentum theorem attempt"),
    ("SRC2346_13_2041_connection", "2041_connection", ["LC2041_4_P4_fallback", "LC2041_5_verdict"], "torsion/connection decision ledger"),
    ("SRC2346_14_2122_readout_owner", "2122_readout_owner", ["SRO2122_6_verdict", "not signed"], "source/readout owner lemma"),
    ("SRC2346_15_2118_readout_zero", "2118_readout_zero", ["SRZ2118_6_verdict", "source/readout Gamma silence"], "source/readout zero theorem attempt"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2346_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_SOURCE_PROJECTION_ZERO_AUDIT.csv",
    "components": OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
    "priority": OUT / "P8_Y5_PARENT_QLOC_2346_COMPONENT_PRIORITY_LEDGER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2346_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2346_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2346_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2346_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2346_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2346_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2346_0_zero_audit", OUTPUTS["zero_audit"], BETA_DOCS / "NONHILBERT_SOURCE_PROJECTION_ZERO_AUDIT_2346_NONCLAIM.csv"),
    ("COPY2346_1_components", OUTPUTS["components"], MICRO_RESIDUALS / "NONHILBERT_COMPONENT_BOUND_PACK_2346_NONCLAIM.csv"),
    ("COPY2346_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2346_NONHILBERT_DECISION_LEDGER_NONCLAIM.csv"),
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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
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


def build_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHZ2346_0_target",
            "projection_channel": "total non-Hilbert source projection",
            "zero_condition": "P_source[J_NH]=0 where J_NH=J_spin/torsion+J_boundary+J_readout+J_improvement+J_shadow_connection+J_projector",
            "status": "TARGET_SHARPENED",
            "proof_status": "requires every component zero or explicit bound",
            "residual_if_unsigned": "epsilon_current_owner_NH_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHZ2346_1_spin_torsion",
            "projection_channel": "spin/torsion/nonmetricity/hypermomentum",
            "zero_condition": "observed ordinary/source/readout branch is metric-only LC, or Palatini EH plus no hypermomentum and projective silence",
            "status": "CONDITIONAL_ROUTE_EXISTS_NOT_SIGNED",
            "proof_status": "2333/2042 give exact conditional clauses but no parent-signed no-Gamma/no-hypermomentum certificate for all local source arenas",
            "residual_if_unsigned": "epsilon_spin_torsion_abs; Delta_abs_P4",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHZ2346_2_boundary",
            "projection_channel": "boundary/worldtube/improvement flux",
            "zero_condition": "fixed differentiable Hamiltonian representative with zero compact local boundary/source projection",
            "status": "NOT_DERIVED",
            "proof_status": "boundary needs theta/Qtau extraction, fixed reference, positive M_H_ref, worldtube selector and Pi_M equality",
            "residual_if_unsigned": "epsilon_boundary_source_abs; B_zero_flux",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHZ2346_3_readout_reentry",
            "projection_channel": "readout/domain/source-label reentry",
            "zero_condition": "source/readout maps are downstream functors of q/e_obs/A_owned/theta and cannot create a source-labelled current",
            "status": "CONDITIONAL_ROUTE_EXISTS_NOT_SIGNED",
            "proof_status": "2335/SRNG is a strong certificate-shaped clause but not yet adopted or derived as parent theorem",
            "residual_if_unsigned": "epsilon_readout_current_reentry_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHZ2346_4_shadow_projector",
            "projection_channel": "shadow connection/projector/domain support",
            "zero_condition": "no independent shadow coframe/connection/source projector, or its source projection is theorem-zero",
            "status": "NOT_DERIVED",
            "proof_status": "projector/domain/support terms remain retained across boundary/source-neutrality ledgers",
            "residual_if_unsigned": "epsilon_shadow_connection_abs; epsilon_projector_domain_abs",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHZ2346_5_verdict",
            "projection_channel": "promote P_source[J_NH]=0",
            "zero_condition": "all NHZ2346_1..4 channels pass in the same parent branch with no cancellation",
            "status": "ZERO_NOT_DERIVED_COMPONENT_PACK_REQUIRED",
            "proof_status": "the trident is clean, but no head is fully parent-signed; total residual remains nonclaim",
            "residual_if_unsigned": "epsilon_current_owner_NH_abs component envelope",
            "valid_for_claim": "false",
        },
    ]


def build_component_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHC2346_0_total",
            "quantity": "epsilon_current_owner_NH_abs",
            "component": "absolute total current-owner residual envelope",
            "bound_formula": "epsilon_current_owner_NH_abs <= E_spin + E_boundary + E_readout + E_shadow + E_projector",
            "units": "dimensionless after source normalization",
            "current_value": "MISSING_COMPONENT_VALUES",
            "required_input": "all component theorem-zeroes or numeric source-backed rows",
            "observable_links": "local_GR;Newton_GM;PPN;WEP;R10;orbital;clock",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHC2346_1_spin",
            "quantity": "E_spin",
            "component": "spin/torsion/nonmetricity/hypermomentum source projection",
            "bound_formula": "E_spin >= ||P_source[J_spin/torsion/nonmetricity/hypermomentum]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_NO_GAMMA_CERTIFICATE_OR_P4_VALUE",
            "required_input": "SRNG/no-Gamma adoption or P4 Delta_abs component values",
            "observable_links": "PPN;clock;spin_transport;local_GR;R10",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHC2346_2_boundary",
            "quantity": "E_boundary",
            "component": "boundary/worldtube/improvement source projection",
            "bound_formula": "E_boundary >= ||P_source[J_boundary+J_improvement]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless or declared GM_flux normalization",
            "current_value": "MISSING_B_ZERO_FLUX_OR_SOURCE_BOUND",
            "required_input": "theta/Qtau, fixed reference, M_H_ref, worldtube selector, Pi_M equality",
            "observable_links": "Newton_GM;orbital;PPN;local_GR",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHC2346_3_readout",
            "quantity": "E_readout",
            "component": "readout/source-label reentry source projection",
            "bound_formula": "E_readout >= ||P_source[J_readout_reentry]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_READOUT_REENTRY_ZERO_OR_LEAKAGE_VALUE",
            "required_input": "source/readout no-reentry theorem or arena leakage coefficients",
            "observable_links": "WEP;R10;clock;PPN;orbital",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHC2346_4_shadow_projector",
            "quantity": "E_shadow_projector",
            "component": "shadow connection/domain/projector/support tail",
            "bound_formula": "E_shadow >= ||P_source[J_shadow_connection+J_projector+J_support]|| / ||P_source[J_Hilbert]||",
            "units": "dimensionless",
            "current_value": "MISSING_SHADOW_PROJECTOR_SUPPORT_VALUE",
            "required_input": "single observed coframe/projector theorem or c_g/b_dis/q_nonH/support coefficients",
            "observable_links": "R10;PPN;clock;local_GR;source_normalization",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NHC2346_5_no_cancellation",
            "quantity": "absolute_sum_policy",
            "component": "unknown-channel cancellation guard",
            "bound_formula": "total uses sum of absolute component envelopes; no cancellation between unsigned channels",
            "units": "policy",
            "current_value": "ACTIVE_GUARD",
            "required_input": "component zero/proven signs before any cancellation credit",
            "observable_links": "all local source arenas",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2346_0_connection_first",
            "component": "spin/torsion/nonmetricity/hypermomentum",
            "reason_to_attack": "it has the crispest zero route: no independent Gamma slot / LC connection / no hypermomentum",
            "risk": "SRNG/no-Gamma still looks like a parent clause rather than a derivation",
            "recommended_next": "2347 noGamma/SRNG adoption or P4 component row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2346_1_boundary_second",
            "component": "boundary/improvement/worldtube",
            "reason_to_attack": "needed for Newtonian GM and Hamiltonian charge honesty",
            "risk": "depends on theta/Qtau, H_ref, M_H_ref and Pi_M equality; too many debts for immediate closure",
            "recommended_next": "after Gamma channel or in parallel bound acquisition",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRI2346_2_readout_third",
            "component": "readout reentry",
            "reason_to_attack": "important for WEP/R10/clocks but downstream of source current definition",
            "risk": "requires arena-specific kernels to become empirical",
            "recommended_next": "fold into SRNG/no-reentry proof after no-Gamma",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2346_0_result", "decision": "do not claim P_source[J_NH]=0", "reason": "spin/torsion, boundary/improvement, readout reentry and shadow/projector channels are not jointly parent-signed", "consequence": "local GR/Newton source recovery remains blocked by epsilon_current_owner_NH_abs", "status": "ZERO_NOT_DERIVED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2346_1_progress", "decision": "compress non-Hilbert obstruction into component pack", "reason": "2345 vague residual is now split into named component rows with absolute-sum policy", "consequence": "future tests cannot hide a source-current tail inside measured GM", "status": "COMPONENT_PACK_INSTALLED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2346_2_next", "decision": "attack no-Gamma/SRNG connection channel first", "reason": "connection/hypermomentum has the cleanest mathematical zero route and would remove E_spin/P4 before the messier boundary problem", "consequence": "next target is SRNG adoption/no independent Gamma or P4 component row", "status": "SELECT_CONNECTION_CHANNEL_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2346_3_boundary_caveat", "decision": "do not pretend connection closure finishes local GR", "reason": "boundary and readout heads remain even if E_spin closes", "consequence": "connection win would be serious but not final", "status": "TRIDENT_DISCIPLINE_RETAINED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2346_4_public_policy", "decision": "no GitHub update from 2346", "reason": "private source-current obstruction triage and bound-pack staging", "consequence": "continue private derivation work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2346_0_total_zero", "gate": "P_source[J_NH]=0 theorem derived", "passed": "false", "claim_effect": "total non-Hilbert residual remains live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2346_1_spin_zero", "gate": "spin/torsion/hypermomentum source projection zero", "passed": "false", "claim_effect": "E_spin or P4 residual required", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2346_2_boundary_zero", "gate": "boundary/improvement source projection zero", "passed": "false", "claim_effect": "B_zero/worldtube residual required", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2346_3_readout_zero", "gate": "readout reentry source projection zero", "passed": "false", "claim_effect": "E_readout residual required", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2346_4_components_score_ready", "gate": "component bound pack score-ready", "passed": "false", "claim_effect": "component values/source paths missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2346_5_local_GR_Newton", "gate": "local GR/Newton source recovery derived", "passed": "false", "claim_effect": "source-current trident remains open", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2346_6_github", "gate": "safe public GitHub update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2346_0_hilbert_silences_all", "claim": "Hilbert current owner makes all non-Hilbert source terms vanish", "allowed": "false", "reason": "Hilbert ownership of S_matter does not eliminate independent connection, boundary, readout or projector source tails", "blocking_rows": "NHZ2346_1_spin_torsion;NHZ2346_2_boundary;NHZ2346_3_readout_reentry", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2346_1_noGamma_claim", "claim": "SRNG/no-Gamma certificate proves spin/torsion source zero now", "allowed": "false", "reason": "SRNG is certificate-shaped but not adopted/derived as parent theorem for all local source arenas", "blocking_rows": "NHZ2346_1_spin_torsion;CG2346_1_spin_zero", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2346_2_boundary_zero", "claim": "boundary/improvement flux is zero by compactness", "allowed": "false", "reason": "boundary rows still need theta/Qtau, fixed reference, M_H_ref, worldtube selector and Pi_M equality", "blocking_rows": "NHZ2346_2_boundary;NHC2346_2_boundary", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2346_3_cancellation", "claim": "unknown non-Hilbert components can cancel", "allowed": "false", "reason": "no cancellation between unsigned channels; total uses absolute component envelopes", "blocking_rows": "NHC2346_5_no_cancellation", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2346_4_local_claim", "claim": "2346 proves local GR/Newton source recovery", "allowed": "false", "reason": "2346 stages a component pack and selects the next zero route; it does not close the trident", "blocking_rows": "DEC2346_0_result;CG2346_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2346_0", "next_target": "2347-Y5-R2FR-noGamma-SRNG-adoption-or-P4-hypermomentum-component-row.md", "why": "the connection/hypermomentum channel is the cleanest first head of the non-Hilbert trident: prove no independent Gamma/source hypermomentum, or fill the P4 residual row", "route_type": "private_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2346_1", "next_target": "2347b-Y5-R2FR-boundary-Bzero-source-current-component-row.md", "why": "fallback/parallel route for the boundary head if no-Gamma stalls", "route_type": "fallback_nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2346_2", "next_target": "2347c-Y5-R2FR-readout-no-reentry-component-row.md", "why": "downstream readout source-label leakage must eventually be zero-proved or bounded for WEP/R10/clocks", "route_type": "parallel_nonclaim", "valid_for_claim": "false"},
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source, destination in BRANCH_COPY_SPECS:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": str(source.relative_to(ROOT)),
                "branch_copy_path": str(destination),
                "copy_exists": bool_text(destination.exists()),
                "row_count": len(read_csv_rows(destination)),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation(
    sources: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    priority_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"timestamp_utc": timestamp(), "branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    add("VAL2346_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2346_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2346_02_zero_not_promoted", any(row["row_id"] == "NHZ2346_5_verdict" and row["status"] == "ZERO_NOT_DERIVED_COMPONENT_PACK_REQUIRED" for row in zero_rows), "P_source[J_NH]=0 not promoted")
    add("VAL2346_03_trident_complete", all(any(token in row["projection_channel"] for row in zero_rows) for token in ["spin/torsion", "boundary", "readout"]), "spin/boundary/readout trident represented")
    add("VAL2346_04_component_pack_nonclaim", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in component_rows), "component bound pack remains non-score-ready")
    add("VAL2346_05_no_cancellation_policy", any(row["row_id"] == "NHC2346_5_no_cancellation" and row["current_value"] == "ACTIVE_GUARD" for row in component_rows), "absolute-sum no-cancellation policy active")
    add("VAL2346_06_priority_selects_connection", any(row["row_id"] == "PRI2346_0_connection_first" and "noGamma" in row["recommended_next"] for row in priority_rows), "connection/no-Gamma route selected first")
    add("VAL2346_07_claim_gates_blocked", all(row["passed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows), "all claim gates remain blocked")
    add("VAL2346_08_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2346_09_next_selected", any(row["row_id"] == "NEXT2346_0" and "noGamma-SRNG" in row["next_target"] for row in next_rows), "2347 noGamma/SRNG target recorded")
    add("VAL2346_10_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, zero_rows, component_rows, priority_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2346_11_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "NONHILBERT_SOURCE_PROJECTION_ZERO_AUDIT_2346",
        "NONHILBERT_COMPONENT_BOUND_PACK_2346",
        "JR2346_NONHILBERT",
        "Y5_R2FR_nonHilbert_source_projection",
    ]
    formalization_hits: list[str] = []
    if FORMALIZATION.exists():
        for needle in checkpoint_needles:
            try:
                result = subprocess.run(["rg", "-n", "--fixed-strings", needle, str(FORMALIZATION)], capture_output=True, text=True, timeout=30, check=False)
            except (OSError, subprocess.TimeoutExpired):
                result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
            if result.returncode == 0 and result.stdout.strip():
                formalization_hits.extend(result.stdout.strip().splitlines())
    add("VAL2346_12_formalization_untouched_by_2346", not formalization_hits, "no 2346 checkpoint output appears in formalization-workbench")
    add("VAL2346_13_no_github_policy", any(row["row_id"] == "DEC2346_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2346")
    add("VAL2346_OVERALL", all(row["status"] == "PASS" for row in rows), "2346 rejects total non-Hilbert source-projection zero, installs a component bound pack, and selects no-Gamma/SRNG or P4 hypermomentum as 2347.")
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    priority_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2346 - Non-Hilbert Source Projection Zero Or Component Bound Pack",
        "",
        "## Summary",
        "",
        "2346 tries to close the non-Hilbert source-current tail left by 2345.",
        "",
        "Result: the total zero `P_source[J_NH]=0` is not derived. The obstruction is now split into a trident:",
        "`spin/torsion/nonmetricity/hypermomentum`, `boundary/worldtube/improvement flux`, and `readout/source-label reentry`,",
        "plus a shadow/projector/support tail. No cancellation between these unknown channels is allowed.",
        "",
        "The most promising next derivation route is the connection channel: prove the source/readout branch has no independent",
        "`Gamma`/hypermomentum slot via SRNG/no-Gamma adoption, or demote that head to a P4 component row.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Non-Hilbert Source Projection Zero Audit",
        "",
        markdown_table(zero_rows, ["row_id", "projection_channel", "zero_condition", "status", "proof_status", "residual_if_unsigned", "valid_for_claim"]),
        "",
        "## Non-Hilbert Component Bound Pack",
        "",
        markdown_table(component_rows, ["row_id", "quantity", "component", "bound_formula", "units", "current_value", "required_input", "observable_links", "score_ready", "valid_for_claim"]),
        "",
        "## Component Priority Ledger",
        "",
        markdown_table(priority_rows, ["row_id", "component", "reason_to_attack", "risk", "recommended_next", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(decision_rows, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "route_type", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = build_sources()
    zero_rows = build_zero_rows()
    component_rows = build_component_rows()
    priority_rows = build_priority_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero_audit"], zero_rows)
    write_csv(OUTPUTS["components"], component_rows)
    write_csv(OUTPUTS["priority"], priority_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(sources, zero_rows, component_rows, priority_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(sources, zero_rows, component_rows, priority_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows, validation_rows)
    print(f"2346 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
