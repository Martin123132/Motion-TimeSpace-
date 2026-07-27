from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1699"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_SOURCE = MICROSCOPE / "branch_locked_wep" / "source"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1699-Y5-R2FR-parent-source-owner-grammar-or-finite-WEP-request-pack.md"
REQUEST_TEMPLATE = BRANCH_SOURCE / "MICROSCOPE_WEP_data_request_template_1699.md"

SOURCE_FILES = {
    "1698_doc": ROOT / "1698-Y5-R2FR-owner-axiom-derivation-test-or-WEP-data-request-runner.md",
    "1698_validation": OUT / "P8_Y5_BRR545_1698_VALIDATION.csv",
    "1698_derivation_test": OUT / "P8_Y5_PARENT_QLOC_1698_AXIOM_DERIVATION_TEST.csv",
    "1698_countermodels": OUT / "P8_Y5_PARENT_QLOC_1698_AXIOM_MINIMALITY_COUNTERMODEL.csv",
    "1698_wep_request": OUT / "P8_Y5_PARENT_QLOC_1698_WEP_DATA_REQUEST_DRY_RUN.csv",
    "1698_download_manifest": OUT / "P8_Y5_PARENT_QLOC_1698_DOWNLOAD_SCRIPT_MANIFEST.csv",
    "1698_next_target": OUT / "P8_Y5_PARENT_QLOC_1698_NEXT_TARGET.csv",
    "1698_dry_run_script": ROOT / "scripts" / "MICROSCOPE_WEP_public_source_download_dry_run.py",
    "1450_label_forgetting": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1452_measure_current": OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv",
    "1464_connected_category": OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv",
    "1478_action_line": MICROSCOPE / "quarantine" / "1478" / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv",
    "1479_typing": MICROSCOPE / "quarantine" / "1479" / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv",
    "1480_hom": MICROSCOPE / "quarantine" / "1480" / "COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT_NONCLAIM.csv",
}

NEEDLES = {
    "1698_doc": ["NEXT1698_0_primary", "AX1697 is not promoted"],
    "1698_validation": ["VAL1698_OVERALL", "PASS"],
    "1698_derivation_test": ["DER1698_7_verdict", "AXIOM_NOT_DERIVED_COUNTERMODELS_PRESENT"],
    "1698_countermodels": ["CM1698_5_remove_no_reentry", "bare exclusion is bypassed"],
    "1698_wep_request": ["REQ1698_3_CNES_ONERA_request", "manual_request_needed"],
    "1698_download_manifest": ["DL1698_7_verdict", "DATA_NOT_ACQUIRED"],
    "1698_next_target": ["NEXT1698_0_primary", "parent-source-owner-grammar"],
    "1698_dry_run_script": ["DRY_RUN_DEFAULT = True", "No executable public machine-readable CMSM array URL"],
    "1450_label_forgetting": ["HT1450_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1452_measure_current": ["CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "1464_connected_category": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1478_action_line": ["SAL1478_4_verdict", "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED"],
    "1479_typing": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    "1480_hom": ["CDH1480_5_verdict", "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1699_SOURCE_REGISTER.csv"
GRAMMAR = OUT / "P8_Y5_PARENT_QLOC_1699_PARENT_SOURCE_OWNER_GRAMMAR.csv"
HOM_PROOF = OUT / "P8_Y5_PARENT_QLOC_1699_HOM_EXCLUSION_CONDITIONAL_PROOF.csv"
SIGNOFFS = OUT / "P8_Y5_PARENT_QLOC_1699_REMAINING_SIGNOFFS.csv"
WEP_REQUEST_PACK = OUT / "P8_Y5_PARENT_QLOC_1699_MICROSCOPE_REQUEST_PACK.csv"
REQUEST_TEMPLATE_MANIFEST = OUT / "P8_Y5_PARENT_QLOC_1699_REQUEST_TEMPLATE_MANIFEST.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1699_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1699_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1699_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1699_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    GRAMMAR,
    HOM_PROOF,
    SIGNOFFS,
    WEP_REQUEST_PACK,
    REQUEST_TEMPLATE_MANIFEST,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    GRAMMAR,
    HOM_PROOF,
    SIGNOFFS,
    WEP_REQUEST_PACK,
    REQUEST_TEMPLATE_MANIFEST,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    GRAMMAR: [
        QUARANTINE / "PARENT_SOURCE_OWNER_GRAMMAR.csv",
        BRANCH_RESIDUALS / "R2FR_parent_source_owner_grammar_1699.csv",
        QUEUE / "JR1699_PARENT_SOURCE_OWNER_GRAMMAR.csv",
    ],
    HOM_PROOF: [
        QUARANTINE / "HOM_EXCLUSION_CONDITIONAL_PROOF.csv",
        BRANCH_RESIDUALS / "R2FR_Hom_exclusion_conditional_proof_1699.csv",
        QUEUE / "JR1699_HOM_EXCLUSION_CONDITIONAL_PROOF.csv",
    ],
    SIGNOFFS: [
        QUARANTINE / "REMAINING_SIGNOFFS.csv",
        BRANCH_RESIDUALS / "R2FR_remaining_signoffs_1699.csv",
        QUEUE / "JR1699_REMAINING_SIGNOFFS.csv",
    ],
    WEP_REQUEST_PACK: [
        QUARANTINE / "MICROSCOPE_REQUEST_PACK.csv",
        BRANCH_RESIDUALS / "R2FR_MICROSCOPE_request_pack_1699.csv",
        QUEUE / "JR1699_MICROSCOPE_REQUEST_PACK.csv",
    ],
    REQUEST_TEMPLATE_MANIFEST: [
        QUARANTINE / "REQUEST_TEMPLATE_MANIFEST.csv",
        BRANCH_RESIDUALS / "R2FR_request_template_manifest_1699.csv",
        QUEUE / "JR1699_REQUEST_TEMPLATE_MANIFEST.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1699.csv",
        QUEUE / "JR1699_NEXT_TARGET.csv",
    ],
}


REQUEST_TEMPLATE_BODY = """# MICROSCOPE WEP Data Request Template - 1699 Dry Draft

Private MTS source-branch work only. This template is not a claim that data have been acquired.

## Purpose

We are trying to reproduce a finite WEP projection/tau lower-bound calculation for a private theoretical consistency gate. We need machine-readable MICROSCOPE data products and metadata sufficient to reconstruct the differential acceleration readout and its relation to the published Eotvos-ratio analysis.

## Requested Items

- N0 raw acceleration and housekeeping data, or public-equivalent session files, including sampling rates and units.
- N1 pre-calibrated acceleration data, masks, calibration metadata, and segment definitions.
- N2 science/calibrated products used for EP analysis, including ADAM/MECM-ready inputs if available.
- Session table for SUEP/SUREF runs, including orbit/session IDs, start times, durations, spin/orbit configuration, and discarded-data masks.
- Differential accelerometer readout matrix or sufficient CMSM/CECT documentation to reconstruct it.
- Satellite position and attitude products in the relevant reference frame conventions.
- Measurement-equation metadata, differential sensitive matrix, offcentring parameters, and calibration conventions needed for source projection.
- Test-mass material/composition metadata for Ti alloy and Pt/Rh alloy sufficient for source-response modelling.
- Data dictionary, license/access conditions, checksums, and citation instructions.

## Non-Claim Guardrail

Until these items are received, parsed, unit-checked, and hashed, the MTS branch must keep `valid_for_claim=false`, `data_acquired=false`, and `claim_allowed=false`.
"""


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    BRANCH_SOURCE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1699": "parent source-owner grammar proof attempt and finite WEP request pack",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def grammar_rows() -> list[dict[str, object]]:
    rows = [
        (
            "G1699_0_sort_geometry",
            "sort",
            "ObsGeometry",
            "observed coframe/metric/connection data descended from quotient q",
            "allowed_argument",
            "geometric source owner H is varied to define T_H",
        ),
        (
            "G1699_1_sort_matter_fields",
            "sort",
            "MatterField_A",
            "ordinary matter dynamical fields Psi_A",
            "allowed_argument",
            "species labels index fields but are not source coefficients",
        ),
        (
            "G1699_2_sort_gauge_current",
            "sort",
            "GaugeCurrent",
            "gauge fields, currents, charges, representations, and measured material parameters",
            "allowed_argument",
            "charge/material dependence may enter dynamics, not an extra active-source multiplier",
        ),
        (
            "G1699_3_sort_universal_constants",
            "sort",
            "UniversalConstant",
            "common c, hbar, G/kappa calibration and shared measure constants",
            "allowed_argument",
            "one common normalization can be absorbed into the gravitational coupling",
        ),
        (
            "G1699_4_forbidden_target",
            "forbidden_target",
            "Coeff_active_source[species]",
            "a source-only coefficient multiplying delta S_A/delta H by species/source label",
            "excluded_by_grammar_if_parent_signed",
            "this is exactly the w_A gap",
        ),
        (
            "G1699_5_action_constructor",
            "constructor",
            "S_ord",
            "S_ord = integral dmu_q L_ord(ObsGeometry, MatterField_A, GaugeCurrent, UniversalConstant)",
            "conditional_constructor",
            "single owner line; no sum_A w_A S_A constructor",
        ),
        (
            "G1699_6_source_constructor",
            "constructor",
            "T_H",
            "T_H := delta S_ord / delta ObsGeometry before readout/material/orbit selectors",
            "conditional_constructor",
            "source is parent-owned before experiment-specific projection",
        ),
        (
            "G1699_7_readout_rule",
            "preservation_rule",
            "ReadoutProjection",
            "readout maps may project/weight observables but may not create Coeff_active_source[species]",
            "unsigned_preservation_rule",
            "compresses no-reentry/readout clauses into one remaining signoff",
        ),
        (
            "G1699_8_verdict",
            "verdict",
            "SourceOwnerGrammar",
            "inside this grammar Hom(species_label,Coeff_active_source)=0 except common constant; but grammar exhaustiveness is not yet parent-signed",
            "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED",
            "progress: six blockers reduce to grammar-exhaustiveness plus readout-preservation signoff",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "grammar_id": gid,
            "entry_type": entry_type,
            "object_or_rule": obj,
            "definition": definition,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gid, entry_type, obj, definition, status, effect in rows
    ]


def hom_proof_rows() -> list[dict[str, object]]:
    rows = [
        (
            "HP1699_0_assume_grammar",
            "Assume grammar G1699_0..G1699_7 is exhaustive for ordinary matter source construction",
            "assumption_not_parent_signed",
            "without exhaustiveness a new source-only object can be added",
        ),
        (
            "HP1699_1_typing",
            "Coeff_active_source[species] is not in the codomain of any allowed constructor",
            "conditional_step",
            "follows from forbidden target row, not from a deeper parent action yet",
        ),
        (
            "HP1699_2_label_forgetting",
            "species labels may index fields/representations but cannot map to an active-source prefactor",
            "conditional_step",
            "uses prior label-forgetting direction but still needs parent grammar signature",
        ),
        (
            "HP1699_3_common_constant",
            "a source multiplier independent of species/source is a universal calibration mode and is absorbed into kappa/G",
            "conditional_step",
            "does not create WEP/local residual because it is common",
        ),
        (
            "HP1699_4_Hom_result",
            "Hom(species_label,Coeff_active_source)=0 modulo one common constant",
            "conditional_theorem_inside_grammar",
            "this is the first clean source-owner theorem shape",
        ),
        (
            "HP1699_5_Delta_w_result",
            "Delta_w_A=0 follows only if grammar exhaustiveness and readout preservation are parent-signed",
            "blocked_no_claim",
            "cannot set Delta_w_A=0 from a conditional grammar theorem",
        ),
        (
            "HP1699_6_verdict",
            "The proof works as a typed theorem inside the proposed grammar, but not yet as a parent-MTS derivation",
            "HOM_EXCLUSION_CONDITIONAL_NOT_CLAIM",
            "next work should sign or reject grammar exhaustiveness",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": pid,
            "statement": statement,
            "status": status,
            "limitation": limitation,
            "parent_derived": False,
            "conditional_inside_grammar": status in {"conditional_step", "conditional_theorem_inside_grammar"},
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pid, statement, status, limitation in rows
    ]


def signoff_rows() -> list[dict[str, object]]:
    rows = [
        (
            "SO1699_0_parent_grammar_exhaustiveness",
            "Parent grammar exhaustiveness",
            "prove all ordinary-matter active-source terms are generated only by G1699 allowed constructors",
            "required_before_claim",
            "without this, w_A can be added as an extra primitive object",
        ),
        (
            "SO1699_1_readout_no_reentry",
            "Readout/effective no-reentry",
            "prove projection, EFT, boundary, material and instrument maps preserve the no-source-coefficient target",
            "required_before_claim",
            "without this, source weights can return after variation",
        ),
        (
            "SO1699_2_connected_common_mode",
            "Connected common calibration",
            "prove ordinary matter sectors are connected enough that any surviving scalar is common",
            "partly_compressed_but_unsigned",
            "prior connected-category attempt is not parent-signed",
        ),
        (
            "SO1699_3_action_measure_owner",
            "Single action/measure owner",
            "prove component actions do not carry independent measure/action units",
            "partly_compressed_but_unsigned",
            "prior action-line proof is not closed",
        ),
        (
            "SO1699_4_verdict",
            "Reduced blocker count",
            "1699 reduces the conceptual problem but does not close the parent derivation",
            "SOURCE_OWNER_GAP_REDUCED_NOT_CLOSED",
            "next step: attack grammar exhaustiveness directly",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "signoff_id": sid,
            "signoff": signoff,
            "needed_statement": needed,
            "status": status,
            "why_needed": why,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for sid, signoff, needed, status, why in rows
    ]


def wep_request_pack_rows() -> list[dict[str, object]]:
    rows = [
        (
            "WR1699_0_public_source_final",
            "MICROSCOPE final WEP result",
            "https://arxiv.org/abs/2209.15487",
            "published eta_TiPt and analysis provenance",
            "source_anchor_recorded",
            "not a raw/CMSM array source",
        ),
        (
            "WR1699_1_public_source_ground",
            "MICROSCOPE mission scenario and data processing",
            "https://arxiv.org/pdf/2201.10841",
            "states N0/N1/N2 data-flow, raw ASCII to CMSM, session/segment metadata, future data availability",
            "source_anchor_recorded",
            "dedicated server endpoint still not identified locally",
        ),
        (
            "WR1699_2_public_source_cnes",
            "CNES Microscope project page",
            "https://cnes.fr/en/projects/microscope",
            "mission status, partners, Ti/Pt-PtRh test masses, 2022 final-result milestone",
            "source_anchor_recorded",
            "project page does not expose needed machine-readable arrays",
        ),
        (
            "WR1699_3_request_N0",
            "N0 raw data package",
            "manual_request_to_CNES_ONERA_CMSM",
            "raw acceleration, housekeeping, masks, timestamps, sessions, units",
            "request_item_ready",
            "needed to reconstruct instrument readout if higher-level products insufficient",
        ),
        (
            "WR1699_4_request_N1_N2",
            "N1/N2 calibrated science data",
            "manual_request_to_CNES_ONERA_CMSM",
            "pre-calibrated/calibrated segment products, ADAM/MECM inputs, masks, calibration parameters",
            "request_item_ready",
            "needed for finite tau_WEP projection",
        ),
        (
            "WR1699_5_request_orbit_attitude",
            "orbit/attitude/source geometry",
            "manual_request_to_CNES_ONERA_CMSM",
            "satellite position, attitude, J2000 conventions, source geometry kernels",
            "request_item_ready",
            "needed to build P_WEP_R_source_Earth_worldtube.csv",
        ),
        (
            "WR1699_6_request_material",
            "Ti/Pt material composition metadata",
            "manual_request_to_CNES_ONERA_CMSM_or_public_material_model",
            "TA6V and PtRh10 composition/uncertainty and material response conventions",
            "request_item_ready",
            "needed to build P_WEP_TiPt_material_response_tensor.csv",
        ),
        (
            "WR1699_7_request_license_hash",
            "data dictionary, license, checksums, citation",
            "manual_request_to_CNES_ONERA_CMSM",
            "schema, units, hashes, access/citation conditions",
            "request_item_ready",
            "needed before any valid_for_claim=true row",
        ),
        (
            "WR1699_8_verdict",
            "manual request pack",
            str(REQUEST_TEMPLATE),
            "request template created but not sent; no data acquired",
            "REQUEST_PACK_READY_DATA_NOT_ACQUIRED",
            "finite WEP route remains blocked until external files exist",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "request_id": rid,
            "item": item,
            "source_or_route": route,
            "purpose": purpose,
            "status": status,
            "blocker": blocker,
            "downloaded": False,
            "data_acquired": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, item, route, purpose, status, blocker in rows
    ]


def request_template_manifest_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RT1699_0_template",
            str(REQUEST_TEMPLATE),
            "manual request draft for MICROSCOPE WEP arrays/metadata",
            "written_not_sent",
            "contains explicit non-claim guardrail",
        ),
        (
            "RT1699_1_required_artifact_readout",
            "P_WEP_K_CMSM_readout.csv",
            "official CMSM/readout matrix or reconstructable equivalent",
            "missing",
            "must remain valid_for_claim=false until acquired and validated",
        ),
        (
            "RT1699_2_required_artifact_source",
            "P_WEP_R_source_Earth_worldtube.csv",
            "source geometry/worldtube projection input",
            "missing",
            "must remain valid_for_claim=false until acquired/derived and validated",
        ),
        (
            "RT1699_3_required_artifact_material",
            "P_WEP_TiPt_material_response_tensor.csv",
            "Ti/Pt material source-response tensor",
            "missing",
            "must remain valid_for_claim=false until sourced or parent-derived",
        ),
        (
            "RT1699_4_required_artifact_tau",
            "P_WEP_tau_min_lower_bound.csv",
            "strictly positive finite tau lower bound",
            "missing",
            "must remain valid_for_claim=false until computed/proved",
        ),
        (
            "RT1699_5_required_artifact_manifest",
            "P_WEP_tau_parser_manifest.json",
            "parser manifest with hashes/schema/units",
            "missing",
            "must remain valid_for_claim=false until all inputs exist",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "manifest_id": mid,
            "artifact_or_path": artifact,
            "purpose": purpose,
            "status": status,
            "guardrail": guardrail,
            "sent": False,
            "downloaded": False,
            "data_acquired": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for mid, artifact, purpose, status, guardrail in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1699_0_parent_grammar_claim", "claim source-owner grammar as parent-derived", "REJECT_PARENT_GRAMMAR_CLAIM", "grammar is a conditional theorem environment, not signed by parent action"),
        ("RUN1699_1_Hom_claim", "claim Hom exclusion as full MTS theorem", "REJECT_HOM_CLAIM", "Hom exclusion only follows inside unsigned grammar"),
        ("RUN1699_2_Delta_w_zero", "set Delta_w_A=0", "REJECT_DELTA_W_ZERO", "remaining signoffs are unsigned"),
        ("RUN1699_3_WEP_data", "claim MICROSCOPE data acquired", "REJECT_DATA_ACQUIRED", "request template written but not sent and no arrays acquired"),
        ("RUN1699_4_tau_min", "claim tau_WEP positive", "REJECT_TAU_MIN", "readout/source/material/parser artifacts remain missing"),
        ("RUN1699_5_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "source-owner gap reduced but not closed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": rid,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1699_0_primary",
            "1700-Y5-R2FR-parent-grammar-exhaustiveness-proof-or-readout-no-reentry.md",
            "scripts/Y5_R2FR_parent_grammar_exhaustiveness_proof_or_readout_no_reentry.py",
            "attack the strongest remaining signoff: prove parent grammar exhaustiveness; if it fails, isolate readout no-reentry as the next finite bound leg",
            "selected",
        ),
        (
            "NEXT1699_1_theory",
            "1700a-Y5-R2FR-parent-ordinary-matter-grammar-exhaustiveness.md",
            "scripts/Y5_R2FR_parent_ordinary_matter_grammar_exhaustiveness.py",
            "prove no extra source-only coefficient object can be added to ordinary matter parent grammar",
            "held_fallback",
        ),
        (
            "NEXT1699_2_empirical",
            "1700b-Y5-R2FR-MICROSCOPE-request-ledger-and-parser-shell.md",
            "scripts/Y5_R2FR_MICROSCOPE_request_ledger_and_parser_shell.py",
            "turn the 1699 request pack into a parser shell and manual acquisition ledger without claim flags",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": rid,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, target, script, objective, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1699_0_parent_grammar", "parent source-owner grammar derived", "BLOCKED_NO_CLAIM", "conditional grammar is not parent-signed"),
        ("CG1699_1_Hom_exclusion", "Hom(species_label,Coeff_active_source)=0 as MTS theorem", "BLOCKED_NO_CLAIM", "conditional theorem only"),
        ("CG1699_2_Delta_w", "Delta_w_A=0 theorem", "BLOCKED_NO_CLAIM", "remaining signoffs required"),
        ("CG1699_3_WEP_data", "MICROSCOPE WEP data acquired", "BLOCKED_NO_CLAIM", "request pack only"),
        ("CG1699_4_tau_min", "tau_WEP positive lower bound", "BLOCKED_NO_CLAIM", "missing finite input artifacts"),
        ("CG1699_5_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "coupling/source-owner gap remains open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": cid,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, claim, status, reason in rows
    ]


def write_request_template() -> None:
    REQUEST_TEMPLATE.write_text(REQUEST_TEMPLATE_BODY, encoding="utf-8")


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in (
                "can_score",
                "accepted_for_scoring",
                "score_ready",
                "valid_prediction_row",
                "valid_for_claim",
                "claim_allowed",
                "downloaded",
                "data_acquired",
                "sent",
            ):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows_: list[dict[str, object]],
    grammar_rows_: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    signoff_rows_: list[dict[str, object]],
    request_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows_)
    grammar_has_forbidden_target = any(row["object_or_rule"] == "Coeff_active_source[species]" and row["entry_type"] == "forbidden_target" for row in grammar_rows_)
    grammar_not_signed = all(not bool_cell(row["parent_signed"]) for row in grammar_rows_)
    hom_conditional = any(row["proof_id"] == "HP1699_4_Hom_result" and row["status"] == "conditional_theorem_inside_grammar" for row in proof_rows)
    delta_w_blocked = any(row["proof_id"] == "HP1699_5_Delta_w_result" and row["status"] == "blocked_no_claim" for row in proof_rows)
    remaining_signoffs_present = {"Parent grammar exhaustiveness", "Readout/effective no-reentry"}.issubset({str(row["signoff"]) for row in signoff_rows_})
    reduced_not_closed = any(row["signoff_id"] == "SO1699_4_verdict" and row["status"] == "SOURCE_OWNER_GAP_REDUCED_NOT_CLOSED" for row in signoff_rows_)
    request_items_ready = {"N0 raw data package", "N1/N2 calibrated science data", "orbit/attitude/source geometry", "Ti/Pt material composition metadata"}.issubset({str(row["item"]) for row in request_rows})
    no_data_acquired = all(not bool_cell(row["downloaded"]) and not bool_cell(row["data_acquired"]) for row in request_rows + template_rows)
    template_exists = REQUEST_TEMPLATE.exists() and "Non-Claim Guardrail" in read_text(REQUEST_TEMPLATE) and "N0 raw acceleration" in read_text(REQUEST_TEMPLATE)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1699_0_primary" and row["selection_status"] == "selected" for row in next_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1699*"))) == 0 if FORMALIZATION.exists() else True
    checks = [
        ("VAL1699_0_sources_exist", sources_ok, "all cited local source paths exist and required needles are present"),
        ("VAL1699_1_forbidden_target_present", grammar_has_forbidden_target, "grammar explicitly excludes Coeff_active_source[species]"),
        ("VAL1699_2_grammar_not_signed", grammar_not_signed, "grammar remains conditional and not parent-signed"),
        ("VAL1699_3_Hom_conditional", hom_conditional, "Hom exclusion is proved only inside the proposed grammar"),
        ("VAL1699_4_Delta_w_blocked", delta_w_blocked, "Delta_w theorem-zero remains blocked"),
        ("VAL1699_5_signoffs_present", remaining_signoffs_present, "remaining parent signoffs are explicit"),
        ("VAL1699_6_gap_reduced_not_closed", reduced_not_closed, "source-owner gap is reduced but not closed"),
        ("VAL1699_7_request_items_ready", request_items_ready, "finite WEP request pack includes key data artifacts"),
        ("VAL1699_8_no_data_acquired", no_data_acquired, "request pack creates no data-acquired claim"),
        ("VAL1699_9_template_exists", template_exists, "manual request template exists with non-claim guardrail"),
        ("VAL1699_10_runner_blocks", runner_blocks, "runner blocks grammar, Hom, tau, WEP and local-GR claims"),
        ("VAL1699_11_next_selected", next_selected, "next target selects grammar exhaustiveness or readout no-reentry"),
        ("VAL1699_12_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1699_13_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1699_14_csv_parse", csv_parse, "all generated 1699 CSVs parse"),
        ("VAL1699_15_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1699_16_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1699_17_formalization_untouched", formalization_untouched, "no 1699 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": cid,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1699_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1699 parent source-owner grammar and finite WEP request pack validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows_: list[dict[str, object]],
    grammar_rows_: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    signoff_rows_: list[dict[str, object]],
    request_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1699 - Parent Source-Owner Grammar Or Finite WEP Request Pack

## Verdict

1699 makes real progress, but it is not the victory lap yet.

The best route is a typed parent source-owner grammar. Inside that grammar the bad coupling is not an allowed object: `Coeff_active_source[species]` is a forbidden target, so `Hom(species_label, Coeff_active_source)=0` modulo one common calibration constant. That means the Hom-exclusion proof now has a clean mathematical shape.

But the parent MTS action has not yet signed the grammar as exhaustive. So the result is **conditional**, not a local-GR/Newton claim. The source-owner gap has been compressed from six fuzzy blockers into the sharper question: can the parent ordinary-matter grammar be proved exhaustive, and can readout/effective maps be proved unable to reintroduce source coefficients?

The finite WEP branch is also upgraded from a dry-run source list into a manual request pack and template for MICROSCOPE data products. No data are marked acquired.

## Source Register

{markdown_table(source_rows_, ["source_key", "source_path", "exists", "needles_present", "use_in_1699"])}

## Parent Source-Owner Grammar

{markdown_table(grammar_rows_, ["grammar_id", "entry_type", "object_or_rule", "status", "effect"])}

## Hom Exclusion Conditional Proof

{markdown_table(proof_rows, ["proof_id", "statement", "status", "limitation"])}

## Remaining Signoffs

{markdown_table(signoff_rows_, ["signoff_id", "signoff", "status", "why_needed"])}

## MICROSCOPE Request Pack

{markdown_table(request_rows, ["request_id", "item", "source_or_route", "status", "blocker"])}

## Request Template Manifest

{markdown_table(template_rows, ["manifest_id", "artifact_or_path", "purpose", "status", "guardrail"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is probably the best position we have had on the coupling problem. We did not magically solve it; better, we isolated the exact mathematical lock. If the parent ordinary-matter grammar is exhaustive, the source-only coupling has nowhere to live. If that exhaustiveness cannot be proved, the theory must either admit a closure axiom or survive through finite empirical bounds. That is the clean fork.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    write_request_template()
    source_rows_ = source_register_rows()
    grammar_rows_ = grammar_rows()
    proof_rows = hom_proof_rows()
    signoff_rows_ = signoff_rows()
    request_rows = wep_request_pack_rows()
    template_rows = request_template_manifest_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows_, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1699", "valid_for_claim", "claim_allowed"])
    write_csv(GRAMMAR, grammar_rows_, ["branch_id", "grammar_id", "entry_type", "object_or_rule", "definition", "status", "effect", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(HOM_PROOF, proof_rows, ["branch_id", "proof_id", "statement", "status", "limitation", "parent_derived", "conditional_inside_grammar", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(SIGNOFFS, signoff_rows_, ["branch_id", "signoff_id", "signoff", "needed_statement", "status", "why_needed", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(WEP_REQUEST_PACK, request_rows, ["branch_id", "request_id", "item", "source_or_route", "purpose", "status", "blocker", "downloaded", "data_acquired", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(REQUEST_TEMPLATE_MANIFEST, template_rows, ["branch_id", "manifest_id", "artifact_or_path", "purpose", "status", "guardrail", "sent", "downloaded", "data_acquired", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows_, grammar_rows_, proof_rows, signoff_rows_, request_rows, template_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows_, grammar_rows_, proof_rows, signoff_rows_, request_rows, template_rows, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {REQUEST_TEMPLATE}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1699 validation PASS")


if __name__ == "__main__":
    main()
