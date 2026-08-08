from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_NOGAMMA_SRNG_ADOPTION_OR_P4_HYPERMOMENTUM_COMPONENT_ROW_2347"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2347-Y5-R2FR-noGamma-SRNG-adoption-or-P4-hypermomentum-component-row.md"

PATHS = {
    "2346_doc": ROOT / "2346-Y5-R2FR-nonHilbert-source-projection-zero-or-component-bound-pack.md",
    "2346_validation": OUT / "P8_Y5_BRR545_2346_VALIDATION.csv",
    "2346_next": OUT / "P8_Y5_PARENT_QLOC_2346_NEXT_TARGET.csv",
    "2346_components": OUT / "P8_Y5_PARENT_QLOC_2346_NONHILBERT_COMPONENT_BOUND_PACK.csv",
    "2336_doc": ROOT / "2336-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md",
    "2336_naturality": OUT / "P8_Y5_PARENT_QLOC_2336_DOWNSTREAM_NATURALITY_DERIVATION_AUDIT.csv",
    "2336_adoption": OUT / "P8_Y5_PARENT_QLOC_2336_SRNG_ADOPTION_DECISION_MATRIX.csv",
    "2336_p4": OUT / "P8_Y5_PARENT_QLOC_2336_P4_RESIDUAL_STATUS_AFTER_SRNG_ADOPTION.csv",
    "2335_certificate": OUT / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv",
    "2335_theorem": OUT / "P8_Y5_PARENT_QLOC_2335_SRNG_THEOREM_ATTEMPT.csv",
    "2335_p4": OUT / "P8_Y5_PARENT_QLOC_2335_P4_DELTA_STATUS_AFTER_SRNG.csv",
    "2334_slots": OUT / "P8_Y5_PARENT_QLOC_2334_GAMMA_SLOT_SECTOR_AUDIT.csv",
    "2334_stack": OUT / "P8_Y5_PARENT_QLOC_2334_NO_GAMMA_THEOREM_STACK.csv",
    "2334_p4": OUT / "P8_Y5_PARENT_QLOC_2334_P4_DELTA_COMPONENT_QUEUE.csv",
    "2333_nohyper": OUT / "P8_Y5_PARENT_QLOC_2333_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
    "2333_p4": OUT / "P8_Y5_PARENT_QLOC_2333_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
    "2332_trident": OUT / "P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv",
}

SOURCES = [
    ("SRC2347_00_2346_doc", "2346_doc", ["NEXT2346_0", "no independent Gamma/source hypermomentum"], "2346 selected no-Gamma/SRNG or P4"),
    ("SRC2347_01_2346_validation", "2346_validation", ["VAL2346_OVERALL", "PASS"], "2346 validation"),
    ("SRC2347_02_2346_next", "2346_next", ["NEXT2346_0", "noGamma-SRNG"], "machine-readable 2347 target"),
    ("SRC2347_03_2346_components", "2346_components", ["NHC2346_1_spin", "MISSING_NO_GAMMA_CERTIFICATE_OR_P4_VALUE"], "2346 E_spin component row"),
    ("SRC2347_04_2336_doc", "2336_doc", ["PRIVATE_ADOPTION_PLUS_DERIVATION_AUDIT", "spin, boundary/improvement, and projective trace"], "SRNG private adoption narrative"),
    ("SRC2347_05_2336_naturality", "2336_naturality", ["DNF2336_7_verdict", "PARTIAL_DERIVATION_NOT_CORPUS_CLOSED"], "downstream functor derivation status"),
    ("SRC2347_06_2336_adoption", "2336_adoption", ["ADM2336_1_private_adoption", "RECOMMENDED_PRIVATE_WORKING_CLAUSE"], "SRNG/OFC private adoption decision"),
    ("SRC2347_07_2336_p4", "2336_p4", ["P4A2336_0_SRNG_effect", "THEOREM_ZERO_INSIDE_PRIVATE_BRANCH_ONLY"], "P4 residual status after SRNG"),
    ("SRC2347_08_2335_certificate", "2335_certificate", ["SRNG2335_6_verdict", "PARTIAL_CERTIFICATE_READY_NOT_DERIVED"], "source/readout no-Gamma certificate"),
    ("SRC2347_09_2335_theorem", "2335_theorem", ["THM2335_3_SRNG_sum", "CONDITIONAL_THEOREM_READY"], "SRNG conditional zero theorem"),
    ("SRC2347_10_2335_p4", "2335_p4", ["P4S2335_6_reduced_total", "REDUCTION_CONDITIONAL_ONLY"], "P4 Delta status after SRNG"),
    ("SRC2347_11_2334_slots", "2334_slots", ["NGSA2334_9_verdict", "NOT_PARENT_SIGNED_RETAIN_P4_COMPONENTS"], "Gamma slot sector audit"),
    ("SRC2347_12_2334_stack", "2334_stack", ["NGT2334_2_sector_sum", "EXACT_MATH_CONDITIONAL"], "no-Gamma theorem stack"),
    ("SRC2347_13_2334_p4", "2334_p4", ["P4DQ2334_0_total", "MISSING_COMPONENT_ZERO_PROOFS_OR_BOUNDS"], "P4 component queue"),
    ("SRC2347_14_2333_nohyper", "2333_nohyper", ["NHL2333_6_verdict", "NOT_DERIVED_RETAIN_P4_ROW"], "no-hypermomentum/LC verdict"),
    ("SRC2347_15_2333_p4", "2333_p4", ["P4R2333_0_hypermomentum_total", "MISSING_DELTA_COMPONENT_VALUES"], "P4 hypermomentum residual row"),
    ("SRC2347_16_2332_trident", "2332_trident", ["NHT2332_1_spin_torsion", "NOT_ZERO_DERIVED"], "non-Hilbert trident spin/torsion head"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2347_SOURCE_REGISTER.csv",
    "srng": OUT / "P8_Y5_PARENT_QLOC_2347_SRNG_ADOPTION_AND_SCOPE_AUDIT.csv",
    "p4": OUT / "P8_Y5_PARENT_QLOC_2347_P4_HYPERMOMENTUM_COMPONENT_ROW.csv",
    "spin": OUT / "P8_Y5_PARENT_QLOC_2347_SPIN_CONNECTION_NEXT_PROOF_OBLIGATION.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2347_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2347_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2347_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2347_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2347_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2347_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2347_0_srng", OUTPUTS["srng"], BETA_DOCS / "SRNG_ADOPTION_AND_SCOPE_AUDIT_2347_NONCLAIM.csv"),
    ("COPY2347_1_p4", OUTPUTS["p4"], MICRO_RESIDUALS / "P4_HYPERMOMENTUM_COMPONENT_ROW_2347_NONCLAIM.csv"),
    ("COPY2347_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2347_NOGAMMA_SRNG_DECISION_LEDGER_NONCLAIM.csv"),
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


def build_srng_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2347_0_private_scope",
            "clause": "private SRNG/OFC working branch",
            "effect": "Delta_source=Delta_clock=Delta_light=Delta_orbit=0 inside the private SRNG/OFC branch",
            "status": "PRIVATE_REDUCTION_ALLOWED_NONCLAIM",
            "public_status": "not a derived public MTS theorem",
            "remaining_residual": "Delta_matter/private; Delta_spin; Delta_boundary; Delta_projective",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2347_1_derivation_status",
            "clause": "downstream observation functor naturality",
            "effect": "readouts cannot source Gamma_ind if they are maps on solved Q_obs rather than action/current terms",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_CLOSED",
            "public_status": "proof debt remains: q, observation policy, same-frame source selector and no-shadow clauses",
            "remaining_residual": "public Delta_source/clock/light/orbit retained unless SRNG adopted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2347_2_no_gamma_sector_sum",
            "clause": "sector-sum no-Gamma theorem",
            "effect": "if each sector excludes Gamma_ind then Delta_abs vanishes componentwise without cancellation",
            "status": "EXACT_MATH_CONDITIONAL",
            "public_status": "sector slots are not all parent-signed",
            "remaining_residual": "unsigned sectors go to P4 component queue",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2347_3_boundary_limit",
            "clause": "boundary/projective limitation",
            "effect": "SRNG does not close boundary/improvement flux or projective trace coupling",
            "status": "LIMIT_RETAINED",
            "public_status": "boundary/projective live even in private SRNG branch",
            "remaining_residual": "Delta_boundary; Delta_projective",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SRNG2347_4_verdict",
            "clause": "promote no-Gamma/SRNG as public connection zero",
            "effect": "would set E_spin/source-readout Gamma leakage to zero only if parent-signed across matter, spin, source/readout, boundary/projective sectors",
            "status": "NOT_PROMOTED_PRIVATE_SCOPE_ONLY",
            "public_status": "P4 hypermomentum component row remains required",
            "remaining_residual": "P4 public row plus spin/boundary/projective proof obligations",
            "valid_for_claim": "false",
        },
    ]


def build_p4_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4H2347_0_total_public",
            "quantity": "Delta_abs_public",
            "component": "public hypermomentum/no-Gamma residual",
            "formula": "||Delta_matter|| + ||Delta_spin|| + ||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit|| + ||Delta_boundary|| + ||Delta_projective||",
            "private_srng_status": "source/clock/light/orbit zero only in private branch",
            "current_value": "MISSING_COMPONENT_ZERO_PROOFS_OR_BOUNDS",
            "units": "hypermomentum norm or normalized dimensionless envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4H2347_1_reduced_private",
            "quantity": "Delta_abs_private_SRNG",
            "component": "private SRNG-reduced hypermomentum residual",
            "formula": "||Delta_matter/private|| + ||Delta_spin|| + ||Delta_boundary|| + ||Delta_projective||",
            "private_srng_status": "allowed for internal nonclaim calculations only",
            "current_value": "MISSING_SPIN_BOUNDARY_PROJECTIVE_VALUES",
            "units": "hypermomentum norm or normalized dimensionless envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4H2347_2_spin",
            "quantity": "Delta_spin",
            "component": "spin/torsion/nonmetricity connection current",
            "formula": "||spin/torsion/nonmetricity connection current||",
            "private_srng_status": "unchanged by source/readout SRNG",
            "current_value": "MISSING_SPIN_BRANCH_EXCLUSION_OR_BOUND",
            "units": "spin-current or normalized torsion envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4H2347_3_source_readout_public",
            "quantity": "Delta_source_readout_public",
            "component": "source/clock/light/orbit Gamma slot outside private SRNG",
            "formula": "||Delta_source|| + ||Delta_clock|| + ||Delta_light|| + ||Delta_orbit||",
            "private_srng_status": "zero in private SRNG branch; retained publicly",
            "current_value": "MISSING_PUBLIC_SRNG_DERIVATION_OR_COMPONENT_BOUNDS",
            "units": "source/readout normalized envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4H2347_4_boundary_projective",
            "quantity": "Delta_boundary_projective",
            "component": "boundary/improvement plus projective trace",
            "formula": "||Delta_boundary|| + ||Delta_projective||",
            "private_srng_status": "still live in private SRNG branch",
            "current_value": "MISSING_BOUNDARY_PROJECTIVE_CERTIFICATE_OR_BOUND",
            "units": "source-current or normalized projective envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_spin_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2347_0_target",
            "proof_obligation": "coframe-owned spin connection / no independent torsionful Gamma",
            "formal_condition": "omega_obs=omega_LC[e_obs] for spinors/transport, or any Einstein-Cartan/metric-affine branch is explicit and residualized",
            "why_next": "SRNG does not touch Delta_spin; this is the cleanest remaining connection head",
            "fallback": "P4H2347_2_spin axial torsion/nonmetricity bound row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2347_1_metric_only_parent",
            "proof_obligation": "parent ordinary branch variable list is metric/coframe-only",
            "formal_condition": "Arg(S_ord) contains e_obs/g_obs, omega_LC[e_obs], owned gauge fields and theta, not Gamma_ind",
            "why_next": "would make Delta_matter and Delta_spin vanish by variable absence and chain rule",
            "fallback": "retain independent connection channel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SPIN2347_2_projective_caveat",
            "proof_obligation": "projective trace policy",
            "formal_condition": "projective mode is gauge/fixed/unobservable in spin transport, clocks, source charge, lightcones and orbital readout",
            "why_next": "Palatini/metric-affine route cannot become LC without trace silence",
            "fallback": "Delta_projective residual",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2347_0_result", "decision": "do not promote no-Gamma/SRNG as public theorem", "reason": "SRNG/OFC is a private working clause; downstream naturality is conditional, not parent-closed", "consequence": "public P4 hypermomentum component row remains live", "status": "PRIVATE_REDUCTION_PUBLIC_P4_RETAINED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2347_1_private_win", "decision": "use private SRNG to reduce source/readout Gamma leakage internally", "reason": "the clause is minimal, non-fitted and already explicitly labelled nonclaim", "consequence": "private branch focuses on Delta_spin, Delta_boundary and Delta_projective", "status": "SRNG_PRIVATE_SCOPE_CONFIRMED", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2347_2_p4_row", "decision": "install P4 public and private-reduced hypermomentum rows", "reason": "keeps public proof debt separate from private working simplification", "consequence": "future calculations cannot confuse private closure with claim-grade GR reduction", "status": "P4_ROWS_STAGED_NONCLAIM", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2347_3_next", "decision": "attack coframe-owned spin connection next", "reason": "Delta_spin is unchanged by SRNG and is the cleanest remaining connection residual", "consequence": "next target is spin connection coframe ownership or axial torsion P4 row", "status": "SELECT_SPIN_CONNECTION_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2347_4_public_policy", "decision": "no GitHub update from 2347", "reason": "private/public scope split and P4 row staging, not public GR/Newton proof", "consequence": "continue private derivation work", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2347_0_SRNG_public", "gate": "SRNG/OFC derived as public parent theorem", "passed": "false", "claim_effect": "private working clause only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2347_1_private_SRNG", "gate": "SRNG usable as private nonclaim working clause", "passed": "true", "claim_effect": "private branch reduction only; not valid_for_claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2347_2_Delta_source_readout_public_zero", "gate": "Delta_source/clock/light/orbit zero publicly", "passed": "false", "claim_effect": "public P4 source/readout components retained", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2347_3_Delta_spin_zero", "gate": "Delta_spin theorem-zero", "passed": "false", "claim_effect": "spin/torsion component remains next", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2347_4_P4_score_ready", "gate": "P4 hypermomentum rows score-ready", "passed": "false", "claim_effect": "component values/source paths missing", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2347_5_local_GR_Newton", "gate": "local GR/Newton source recovery derived", "passed": "false", "claim_effect": "connection plus boundary/projective gates remain", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2347_6_github", "gate": "safe public GitHub update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2347_0_private_as_public", "claim": "private SRNG adoption proves public no-Gamma theorem", "allowed": "false", "reason": "SRNG/OFC is explicitly a private working clause while derivation remains open", "blocking_rows": "SRNG2347_0_private_scope;CG2347_0_SRNG_public", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2347_1_srng_closes_spin", "claim": "SRNG closes spin/torsion/hypermomentum", "allowed": "false", "reason": "source/readout SRNG does not prove coframe-owned spin connection or exclude metric-affine branches", "blocking_rows": "P4H2347_2_spin;SPIN2347_0_target", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2347_2_srng_closes_boundary", "claim": "SRNG closes boundary/projective residuals", "allowed": "false", "reason": "boundary/improvement and projective trace are separate live residual channels", "blocking_rows": "SRNG2347_3_boundary_limit;P4H2347_4_boundary_projective", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2347_3_p4_as_pass", "claim": "P4 residual row is an empirical pass", "allowed": "false", "reason": "P4 rows are nonclaim placeholders until component values, units, source paths and projection maps exist", "blocking_rows": "P4H2347_0_total_public;CG2347_4_P4_score_ready", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2347_4_local_claim", "claim": "2347 proves local GR/Newton connection recovery", "allowed": "false", "reason": "2347 confirms private scope and stages P4 rows; spin, boundary and projective gates remain open", "blocking_rows": "DEC2347_0_result;CG2347_5_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2347_0", "next_target": "2348-Y5-R2FR-spin-connection-coframe-owned-or-axial-torsion-P4-row.md", "why": "private SRNG reduces source/readout Gamma leakage, but Delta_spin is untouched and is now the cleanest connection residual to derive or bound", "route_type": "private_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2347_1", "next_target": "2348b-Y5-R2FR-boundary-projective-Bzero-after-private-SRNG.md", "why": "parallel route for boundary/projective residuals that SRNG cannot close", "route_type": "parallel_nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2347_2", "next_target": "2348c-Y5-R2FR-public-SRNG-parent-observation-policy-proof.md", "why": "pure derivation route if we want to turn private SRNG into public theorem instead of continuing private branch reductions", "route_type": "parallel_derivation_nonclaim", "valid_for_claim": "false"},
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
    srng_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    spin_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"timestamp_utc": timestamp(), "branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    add("VAL2347_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists")
    add("VAL2347_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found")
    add("VAL2347_02_private_srng_confirmed", any(row["row_id"] == "SRNG2347_0_private_scope" and row["status"] == "PRIVATE_REDUCTION_ALLOWED_NONCLAIM" for row in srng_rows), "private SRNG reduction recorded as nonclaim")
    add("VAL2347_03_public_not_promoted", any(row["row_id"] == "SRNG2347_4_verdict" and row["status"] == "NOT_PROMOTED_PRIVATE_SCOPE_ONLY" for row in srng_rows), "SRNG not promoted publicly")
    add("VAL2347_04_p4_rows_nonready", all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in p4_rows), "P4 rows remain non-score-ready")
    add("VAL2347_05_spin_next_obligation", any(row["row_id"] == "SPIN2347_0_target" and "coframe-owned" in row["proof_obligation"] for row in spin_rows), "spin connection next proof obligation recorded")
    partial_gate = [row for row in claim_rows if row["row_id"] == "CG2347_1_private_SRNG"]
    other_gates = [row for row in claim_rows if row["row_id"] != "CG2347_1_private_SRNG"]
    add("VAL2347_06_claim_gates_blocked_except_private", bool(partial_gate and partial_gate[0]["passed"] == "true") and all(row["passed"] == "false" for row in other_gates) and all(row["valid_for_claim"] == "false" for row in claim_rows), "only private SRNG gate passes and remains not valid_for_claim")
    add("VAL2347_07_refusals_block_shortcuts", all(row["allowed"] == "false" for row in refusal_rows), "shortcut claims refused")
    add("VAL2347_08_next_selected", any(row["row_id"] == "NEXT2347_0" and "spin-connection" in row["next_target"] for row in next_rows), "2348 spin connection target recorded")
    add("VAL2347_09_branch_copies_parse", all(row["copy_exists"] == "true" and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse")
    generated_groups = [sources, srng_rows, p4_rows, spin_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    add("VAL2347_10_no_claim_flags", all(row.get("valid_for_claim") == "false" for group in generated_groups for row in group), "no generated row is valid_for_claim=true")
    checkpoint_needles = [
        "SRNG_ADOPTION_AND_SCOPE_AUDIT_2347",
        "P4_HYPERMOMENTUM_COMPONENT_ROW_2347",
        "JR2347_NOGAMMA_SRNG",
        "Y5_R2FR_noGamma_SRNG",
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
    add("VAL2347_11_formalization_untouched_by_2347", not formalization_hits, "no 2347 checkpoint output appears in formalization-workbench")
    add("VAL2347_12_no_github_policy", any(row["row_id"] == "DEC2347_4_public_policy" and row["status"] == "NO_GITHUB_EVIDENCE_UPDATE" for row in decision_rows), "public GitHub update not recommended from 2347")
    add("VAL2347_OVERALL", all(row["status"] == "PASS" for row in rows), "2347 confirms private SRNG reduction, refuses public promotion, stages public/private P4 hypermomentum rows, and selects spin-connection coframe ownership as 2348.")
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    srng_rows: list[dict[str, Any]],
    p4_rows: list[dict[str, Any]],
    spin_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2347 - noGamma SRNG Adoption Or P4 Hypermomentum Component Row",
        "",
        "## Summary",
        "",
        "2347 resolves the scope of SRNG rather than pretending it is magic.",
        "",
        "Inside the private SRNG/OFC working branch, source/readout Gamma leakage is switched off for",
        "`Delta_source`, `Delta_clock`, `Delta_light` and `Delta_orbit`. That is useful and disciplined, but it is",
        "not a public derivation from the parent MTS action.",
        "",
        "Publicly, the P4 hypermomentum row stays live. Even privately, SRNG does not close `Delta_spin`,",
        "`Delta_boundary` or `Delta_projective`. The next clean derivation target is therefore the spin connection:",
        "prove it is coframe-owned/Levi-Civita, or keep an axial-torsion/P4 residual row.",
        "",
        "## Source Register",
        "",
        markdown_table(sources, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## SRNG Adoption And Scope Audit",
        "",
        markdown_table(srng_rows, ["row_id", "clause", "effect", "status", "public_status", "remaining_residual", "valid_for_claim"]),
        "",
        "## P4 Hypermomentum Component Row",
        "",
        markdown_table(p4_rows, ["row_id", "quantity", "component", "formula", "private_srng_status", "current_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Spin Connection Next Proof Obligation",
        "",
        markdown_table(spin_rows, ["row_id", "proof_obligation", "formal_condition", "why_next", "fallback", "valid_for_claim"]),
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
    srng_rows = build_srng_rows()
    p4_rows = build_p4_rows()
    spin_rows = build_spin_rows()
    decision_rows = build_decision_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["srng"], srng_rows)
    write_csv(OUTPUTS["p4"], p4_rows)
    write_csv(OUTPUTS["spin"], spin_rows)
    write_csv(OUTPUTS["decision"], decision_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = build_validation(sources, srng_rows, p4_rows, spin_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(sources, srng_rows, p4_rows, spin_rows, decision_rows, claim_rows, refusal_rows, next_rows, copy_rows, validation_rows)
    print(f"2347 checkpoint generated: {DOC}")
    print(f"Validation: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
