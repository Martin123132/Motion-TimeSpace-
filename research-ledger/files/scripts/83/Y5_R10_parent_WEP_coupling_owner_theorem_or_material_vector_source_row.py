from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1077-parent-WEP-coupling-owner-or-material-vector" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1077_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1077_WEP_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1077_0_1076_next", "source-intake/mts_residuals/P8_Y5_R10_1076_NEXT_TARGET.csv", "1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md", "1076 handoff."),
        ("SRC1077_1_1076_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1076_VALIDATION.csv", "V1076_SUMMARY", "1076 validation summary."),
        ("SRC1077_2_1076_contract", "source-intake/mts_residuals/P8_Y5_R10_1076_PARENT_PRODUCT_CONTRACT_UPDATE.csv", "PWC1076_2_theorem_zero", "parent product contract."),
        ("SRC1077_3_1076_derivation", "source-intake/mts_residuals/P8_Y5_R10_1076_PARENT_MAP_DERIVATION_ATTEMPT.csv", "DER1076_5_verdict", "parent map not derived."),
        ("SRC1077_4_1076_owner", "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv", "OWN1076_1_species_blind_measure", "owner gates."),
        ("SRC1077_5_1076_toy", "source-intake/mts_residuals/P8_Y5_R10_1076_TOY_MATERIAL_VECTOR_FROM_651.csv", "MV1076_delta_TA6V_minus_PtRh10", "toy finite material row."),
        ("SRC1077_6_1062_parent", "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "prior parent theorem attempt."),
        ("SRC1077_7_1066_scalar", "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "source scalar exclusion conditional."),
        ("SRC1077_8_1067_action", "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner conditional."),
        ("SRC1077_9_1068_direct", "source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv", "DPF1068_2_theorem_zero_route", "theorem-zero route unsigned."),
        ("SRC1077_10_708_map", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "source/test charge vector missing."),
        ("SRC1077_11_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "WCO1077_0_target",
            "claim": "parent WEP coupling-owner theorem",
            "formal_statement": "ordinary matter couples to the observed coframe/metric through one species-blind parent action measure/current owner, so no source-only relative species weight exists",
            "proof_move": "show all WEP-sensitive variations factor through universal Hilbert stress before readout",
            "result": "TARGET_SHARPENED",
            "gap": "clauses must be signed from parent action syntax, not adopted as taste",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WCO1077_1_conditional_theorem",
            "claim": "conditional theorem-zero",
            "formal_statement": "if parent object language excludes inert source-only scalars, action measure is species blind, and current/source normalization has one owner, then P_WEP=0",
            "proof_move": "Lie_v S_matter=0 for species-only source selectors; delta S/delta e_obs gives common Hilbert source; readout difference cancels",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "gap": "premises remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WCO1077_2_object_language",
            "claim": "no inert source-only parent argument",
            "formal_statement": "Arg(S_parent) contains geometry, matter fields, gauge/current data, representation constants, and universal constants only",
            "proof_move": "exclude species-indexed w_A unless it is carried by an observable field/current/representation object",
            "result": "CONDITIONAL_FROM_SSE1066",
            "gap": "parent object language not derived from MTS primitives",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WCO1077_3_action_measure",
            "claim": "species-blind action-scale/measure owner",
            "formal_statement": "S_parent/hbar_parent has one action scale and one measure/Jacobian for all ordinary matter species",
            "proof_move": "rule out S_A -> w_A S_A by quantum/statistical measure ownership",
            "result": "CONDITIONAL_FROM_ASO1067",
            "gap": "hbar/measure owner not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WCO1077_4_current_owner",
            "claim": "single current/source normalization owner",
            "formal_statement": "matter currents and source normalization descend from one parent current functor, not species-specific weights",
            "proof_move": "fix representation charges/currents before readout and disallow post-variation source selectors",
            "result": "NOT_DERIVED",
            "gap": "current functor/representation owner is still missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "WCO1077_5_verdict",
            "claim": "WEP theorem-zero closure",
            "formal_statement": "P_WEP=0 follows only after WCO1077_2..4 and readout/source closure are parent-signed",
            "proof_move": "assemble conditional theorem and test for unsigned clauses",
            "result": "THEOREM_ZERO_NOT_CLOSED_CURRENT_CORPUS",
            "gap": "object-language, measure/current owner, source worldtube/common-mode, and official readout array gates remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def clause_signature_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "CLAUSE1077_0_object_language",
            "needed_clause": "parent object-language typing excludes source-only species scalar w_A",
            "status": "CONDITIONAL_UNSIGNED",
            "source_evidence": "SSE1066_5_verdict",
            "if_signed_effect": "removes inert source-only scalar slot",
            "if_unsigned_effect": "finite WEP branch requires sourced material/source vectors",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "CLAUSE1077_1_action_measure",
            "needed_clause": "single species-blind action measure/hbar owner",
            "status": "CONDITIONAL_UNSIGNED",
            "source_evidence": "ASO1067_5_verdict",
            "if_signed_effect": "rules out w_A S_A source normalization",
            "if_unsigned_effect": "species action weights remain legal counterexamples",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "CLAUSE1077_2_current_owner",
            "needed_clause": "single current/source normalization owner",
            "status": "MISSING",
            "source_evidence": "THM1062_2_EM_source_owner; OWN1076_2_current_owner",
            "if_signed_effect": "prevents beta_source/current rescaling slot",
            "if_unsigned_effect": "source-only current normalization remains legal",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "CLAUSE1077_3_source_worldtube",
            "needed_clause": "Earth/source leg is universal common mode or sourced finite vector",
            "status": "MISSING",
            "source_evidence": "SWT1068_5_verdict; OWN1076_4_source_worldtube",
            "if_signed_effect": "common source mode can be removed without measured-G trick",
            "if_unsigned_effect": "finite source response vector R_source is required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "CLAUSE1077_4_material_tensor",
            "needed_clause": "Ti/Pt response is universal zero or sourced finite tensor",
            "status": "TOY_ONLY",
            "source_evidence": "MV1076_delta_TA6V_minus_PtRh10; MAT1068_5_verdict",
            "if_signed_effect": "theorem-zero or finite product becomes typed",
            "if_unsigned_effect": "toy vector remains algebra-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "CLAUSE1077_5_readout_kernel",
            "needed_clause": "official MICROSCOPE readout arrays or validated reconstruction",
            "status": "MISSING_OFFICIAL_ARRAYS",
            "source_evidence": "IMP1076_0_official_arrays; RG1075_0_official_arrays",
            "if_signed_effect": "empirical scoring can replace surrogate kernel",
            "if_unsigned_effect": "surrogate-only tests remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE1077_0_species_action_weight",
            "legal_if_unsigned": "ASO/action measure owner",
            "form": "S_matter = sum_A w_A S_A with constant w_A",
            "why_dangerous": "classical equations can look unchanged while Hilbert stress/source normalization changes",
            "blocks": "theorem-zero WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1077_1_current_rescaling",
            "legal_if_unsigned": "current owner",
            "form": "J_A -> c_A J_A or beta_source,A source marker",
            "why_dangerous": "creates species/source charge vector without changing geometry syntax",
            "blocks": "source-scalar exclusion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1077_2_disconnected_material_components",
            "legal_if_unsigned": "object-language/naturality connectedness",
            "form": "ordinary matter category has disconnected simple-object components with natural constants per component",
            "why_dangerous": "naturality alone does not force universal weights",
            "blocks": "material universality proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1077_3_post_variation_selector",
            "legal_if_unsigned": "variation-before-readout/readout closure",
            "form": "readout projection applies F(T_A,A) after Hilbert stress variation",
            "why_dangerous": "species labels can re-enter after common stress derivation",
            "blocks": "readout theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def material_source_row_status() -> list[dict[str, str]]:
    toy = next(row for row in read_csv(OUT / "P8_Y5_R10_1076_TOY_MATERIAL_VECTOR_FROM_651.csv") if row["material_vector_id"] == "MV1076_delta_TA6V_minus_PtRh10")
    return [
        {
            "material_source_id": "MVS1077_0_toy_delta_TA6V_minus_PtRh10",
            "route": "finite material vector fallback",
            "available_row": "MV1076_delta_TA6V_minus_PtRh10",
            "q_Z_over_A_toy": toy["q_Z_over_A_toy"],
            "q_neutron_excess_toy": toy["q_neutron_excess_toy"],
            "accepted_for": "algebra smoke tests only",
            "missing_for_claim": "source-backed isotope/chemical/material tensor or parent response theorem",
            "status": "TOY_SOURCE_ROW_AVAILABLE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_source_id": "MVS1077_1_required_claim_material",
            "route": "finite material vector claim route",
            "available_row": "none",
            "q_Z_over_A_toy": "",
            "q_neutron_excess_toy": "",
            "accepted_for": "future claim only",
            "missing_for_claim": "R_TA6V and R_PtRh10 from parent action or sourced material model",
            "status": "MISSING_CLAIM_VALID_MATERIAL_VECTOR",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_route_requirements() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "FIN1077_0_R_material",
            "object": "R_TA6V - R_PtRh10",
            "required_evidence": "parent-derived material response tensor or source-backed material model",
            "current_status": "TOY_VECTOR_ONLY",
            "blocks": "finite P_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "FIN1077_1_R_source",
            "object": "R_source^Earth",
            "required_evidence": "Earth/source composition/worldtube or parent theorem proving source common mode",
            "current_status": "MISSING_SOURCE_VECTOR",
            "blocks": "finite P_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "FIN1077_2_C_parent",
            "object": "C_parent coupling owner",
            "required_evidence": "parent coefficient/coupling basis with units and normalization",
            "current_status": "MISSING_COUPLING_OWNER",
            "blocks": "finite and theorem-zero routes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "FIN1077_3_K_readout",
            "object": "K_MICROSCOPE readout kernel",
            "required_evidence": "official CMSM arrays/masks or validated reconstruction",
            "current_status": "SURROGATE_ONLY",
            "blocks": "empirical scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1077_0_WEP_coupling_owner_theorem_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_COUPLING_OWNER_THEOREM_OR_SOURCED_FINITE_VECTORS",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
            "inputs_present": "conditional_zero_theorem;toy_material_vector;finite_route_requirements",
            "required_inputs": "signed object language; species-blind measure; current owner; source common-mode theorem OR sourced R_source/R_material/C_parent/readout kernel",
            "derivation_status": "THEOREM_ZERO_UNSIGNED_FINITE_ROUTE_MISSING",
            "valid_for_claim": "false",
            "notes": "conditional theorem is useful but no WEP product is score-ready",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1077_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; theorem-zero and finite vectors remain missing",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1077_0_WEP_coupling_owner_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject unsigned theorem/missing finite vectors and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1077_0_conditional_theorem",
            "claim_component": "conditional WEP theorem-zero",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "premises unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1077_1_parent_object_language",
            "claim_component": "parent object-language typing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "CONDITIONAL_UNSIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1077_2_current_measure_owner",
            "claim_component": "species-blind measure/current owner",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MEASURE_CONDITIONAL_CURRENT_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1077_3_finite_vectors",
            "claim_component": "sourced finite material/source vectors",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "TOY_MATERIAL_ONLY_SOURCE_VECTOR_MISSING",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1077_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1077_0_conditional_theorem_kept",
            "decision": "keep theorem-zero route because the conditional theorem is coherent",
            "evidence": "WCO1077_1_conditional_theorem",
            "consequence": "next work should try to sign the parent premises",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1077_1_no_WEP_claim",
            "decision": "do not claim WEP/local-GR pass",
            "evidence": "WCO1077_5_verdict; CG1077_4_product_runner",
            "consequence": "P_WEP remains missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1077_2_next_target",
            "decision": "attack the parent object-language/measure/current owner proof stack",
            "evidence": "CLAUSE1077_0_object_language; CLAUSE1077_1_action_measure; CLAUSE1077_2_current_owner",
            "consequence": "1078 should try to sign the theorem-zero premises or demote to finite sourced route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1077_0_1078",
            "next_target": "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md",
            "objective": "attempt to sign the three core premises of the WEP theorem-zero route: parent object-language typing, species-blind action measure, and single current/source normalization owner; if any remain unsigned, demote theorem-zero to closure-only and keep finite WEP as sourced-input route.",
            "include": "parent action syntax; allowed argument types; hbar/measure owner; current functor owner; counterexample kill list; finite-route demotion gates; product-runner refusal",
            "exclude": "Delta_w=0 by taste; tau=1; cancellation tuning; toy material vector as evidence; measured-G absorption; public claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    finite_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1077_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1077_1_conditional_theorem", any(row["theorem_id"] == "WCO1077_1_conditional_theorem" and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem_rows), "conditional theorem-zero statement staged"))
    checks.append(("V1077_2_theorem_not_closed", any(row["theorem_id"] == "WCO1077_5_verdict" and row["result"] == "THEOREM_ZERO_NOT_CLOSED_CURRENT_CORPUS" for row in theorem_rows), "theorem-zero remains unsigned"))
    checks.append(("V1077_3_clause_matrix_blocks", any(row["clause_id"] == "CLAUSE1077_2_current_owner" and row["status"] == "MISSING" for row in clause_rows) and any(row["clause_id"] == "CLAUSE1077_4_material_tensor" and row["status"] == "TOY_ONLY" for row in clause_rows), "clause matrix captures current-owner and material gaps"))
    checks.append(("V1077_4_counterexamples", len(counter_rows) == 4 and all(row["valid_for_claim"] == "false" for row in counter_rows), "counterexample kill list staged"))
    checks.append(("V1077_5_material_source_row_nonclaim", any(row["material_source_id"] == "MVS1077_0_toy_delta_TA6V_minus_PtRh10" and row["status"] == "TOY_SOURCE_ROW_AVAILABLE_NONCLAIM" for row in material_rows), "toy material source row demoted to nonclaim"))
    checks.append(("V1077_6_finite_route_requirements", {row["object"] for row in finite_rows} == {"R_TA6V - R_PtRh10", "R_source^Earth", "C_parent coupling owner", "K_MICROSCOPE readout kernel"}, "finite route requirements staged"))
    checks.append(("V1077_7_prediction_nonclaim_missing", any("MISSING_PARENT_COUPLING_OWNER_THEOREM" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing theorem or finite vectors"))
    checks.append(("V1077_8_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1077_9_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1077_10_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1077_11_next_target", any("1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md" in row["next_target"] for row in next_rows), "1078 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1077_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1077_13_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1077_VALIDATION.csv"), "all 1077 CSV outputs parse cleanly"))
    checks.append(("V1077_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1077_SUMMARY", True, "conditional WEP theorem-zero staged but unsigned; finite route requires sourced vectors; WEP/product claim blocked"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    finite_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1077 - Parent WEP coupling-owner theorem or material-vector source row",
            "",
            "## Current verdict",
            "1077 stages a clean conditional theorem-zero route for WEP, but it does not close it. The proof still needs parent-signed object-language typing, species-blind action measure, and current/source normalization owner. The finite route remains sourced-input-only because the Ti/Pt material vector is toy/nonclaim and the Earth/source vector is missing.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Coupling-owner theorem attempt",
            md_table(theorem_rows, ["theorem_id", "claim", "result", "gap"]),
            "## Clause signature matrix",
            md_table(clause_rows, ["clause_id", "needed_clause", "status", "source_evidence", "if_unsigned_effect"]),
            "## Counterexample audit",
            md_table(counter_rows, ["counterexample_id", "legal_if_unsigned", "form", "why_dangerous", "blocks"]),
            "## Material-vector source row status",
            md_table(material_rows, ["material_source_id", "route", "available_row", "q_Z_over_A_toy", "status", "missing_for_claim"]),
            "## Finite route requirements",
            md_table(finite_rows, ["requirement_id", "object", "required_evidence", "current_status", "blocks"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "product_symbol", "bound_value", "bound_units", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "evidence", "consequence"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    clause_rows = clause_signature_rows()
    counter_rows = counterexample_rows()
    material_rows = material_source_row_status()
    finite_rows = finite_route_requirements()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1077_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
        "clauses": OUT / "P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv",
        "counterexamples": OUT / "P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
        "material_status": OUT / "P8_Y5_R10_1077_MATERIAL_VECTOR_SOURCE_ROW_STATUS.csv",
        "finite_requirements": OUT / "P8_Y5_R10_1077_FINITE_ROUTE_REQUIREMENTS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1077_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1077_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1077_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1077_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1077_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1077_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem_rows)
    write_csv(outputs["clauses"], clause_rows)
    write_csv(outputs["counterexamples"], counter_rows)
    write_csv(outputs["material_status"], material_rows)
    write_csv(outputs["finite_requirements"], finite_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        theorem_rows,
        clause_rows,
        counter_rows,
        material_rows,
        finite_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        theorem_rows,
        clause_rows,
        counter_rows,
        material_rows,
        finite_rows,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
