from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_NO_FLUX_OR_BZERO_FIRST_BOUND_ROW_2338"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2338-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md"

PATHS = {
    "2337_doc": ROOT / "2337-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md",
    "2337_validation": OUT / "P8_Y5_BRR545_2337_VALIDATION.csv",
    "2337_next": OUT / "P8_Y5_PARENT_QLOC_2337_NEXT_TARGET.csv",
    "2337_boundary": OUT / "P8_Y5_PARENT_QLOC_2337_BOUNDARY_IMPROVEMENT_QUEUE.csv",
    "2337_reduced": OUT / "P8_Y5_PARENT_QLOC_2337_REDUCED_CONNECTION_GATE.csv",
    "boundary_status": OUT / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "hamiltonian_contract": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "flux_theorem": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "flux_residual_map": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "mass_flux_contract": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
    "1007_doc": ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
    "1013_doc": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "1014_doc": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1016_doc": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
}

SOURCES = [
    ("SRC2338_00_2337_doc", "2337_doc", PATHS["2337_doc"], ["NEXT2337_0", "BND2337_0_B_zero_flux"], "2337 handoff"),
    ("SRC2338_01_2337_validation", "2337_validation", PATHS["2337_validation"], ["VAL2337_OVERALL", "PASS"], "2337 validation"),
    ("SRC2338_02_2337_next", "2337_next", PATHS["2337_next"], ["NEXT2337_0", "boundary-no-flux"], "machine-readable 2338 target"),
    ("SRC2338_03_2337_boundary", "2337_boundary", PATHS["2337_boundary"], ["BND2337_0_B_zero_flux", "MISSING_THEOREM_OR_VALUE"], "B_zero queue"),
    ("SRC2338_04_2337_reduced", "2337_reduced", PATHS["2337_reduced"], ["RCG2337_2_boundary_live", "PRIMARY_LIVE_BLOCKER"], "reduced connection gate"),
    ("SRC2338_05_boundary_status", "boundary_status", PATHS["boundary_status"], ["B_zero_flux", "missing_claim_valid_source_or_zero_theorem"], "boundary first-row status"),
    ("SRC2338_06_hamiltonian_contract", "hamiltonian_contract", PATHS["hamiltonian_contract"], ["HC2_differentiable_integrable_Hxi", "HC9_retained_residual_fallback"], "Hamiltonian boundary contract"),
    ("SRC2338_07_flux_theorem", "flux_theorem", PATHS["flux_theorem"], ["T509_1_flux_closure", "closure_not_derived_for_current_MTS"], "M_eff flux theorem"),
    ("SRC2338_08_flux_residual_map", "flux_residual_map", PATHS["flux_residual_map"], ["SMR509_2_Delta_symp", "boundary"], "flux residual map"),
    ("SRC2338_09_mass_flux_contract", "mass_flux_contract", PATHS["mass_flux_contract"], ["MF6_zero_boundary_and_nonHilbert_flux", "not_parent_derived"], "mass flux contract"),
    ("SRC2338_10_1007_doc", "1007_doc", PATHS["1007_doc"], ["HTA1007_5_symplectic_boundary_flux", "fallback_required"], "H_tau fixed reference blocker"),
    ("SRC2338_11_1013_doc", "1013_doc", PATHS["1013_doc"], ["OBS1013_4_boundary_zero_flux", "MISSING_B_ZERO_FLUX"], "B_zero obstruction"),
    ("SRC2338_12_1014_doc", "1014_doc", PATHS["1014_doc"], ["PCC1014_2_B_zero_flux", "MISSING_B_ZERO_FLUX"], "PiM commutator B_zero obstruction"),
    ("SRC2338_13_1016_doc", "1016_doc", PATHS["1016_doc"], ["PSC1016_8_boundary_reference_lock", "missing_theorem_or_source_input"], "worldtube boundary/reference lock"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2338_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_PARENT_QLOC_2338_BZERO_NOFLUX_THEOREM_AUDIT.csv",
    "bound_row": OUT / "P8_Y5_PARENT_QLOC_2338_BZERO_FIRST_BOUND_ROW.csv",
    "dependencies": OUT / "P8_Y5_PARENT_QLOC_2338_BOUNDARY_DENOMINATOR_DEPENDENCY.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2338_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2338_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2338_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2338_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2338_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2338_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2338_0_theorem", OUTPUTS["theorem"], BETA_DOCS / "BZERO_NOFLUX_THEOREM_AUDIT_2338_NONCLAIM.csv"),
    ("COPY2338_1_bound", OUTPUTS["bound_row"], MICRO_RESIDUALS / "Bzero_first_bound_row_2338_nonclaim.csv"),
    ("COPY2338_2_decision", OUTPUTS["decision"], RAB_QUEUE / "JR2338_BZERO_DECISION_LEDGER_NONCLAIM.csv"),
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


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_key, path, needles, role in SOURCES:
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


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_0_target",
            "clause": "B_zero_flux theorem target",
            "mathematical_statement": "B_zero_flux=0 for compact linked surfaces if the parent boundary/reference/improvement current is fixed, exact or carries zero compact flux before readout.",
            "status": "TARGET_SHARPENED",
            "obstruction": "requires parent theta/Q_tau, fixed reference, boundary conditions, compact support/falloff, positive M_H_ref and no extra hidden charge",
            "fallback": "stage B_zero_flux/M_H_ref absolute residual row",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_1_parent_symplectic",
            "clause": "parent theta/Q_tau extraction",
            "mathematical_statement": "delta L_parent = E_A delta Phi^A + d theta_MTS and Q_tau^MTS exists for the same observed tau used by source, clocks and orbital readout.",
            "status": "MISSING_PARENT_THETA_QTAU",
            "obstruction": "1007 keeps parent symplectic/Noether structure unsigned",
            "fallback": "epsilon_HPiM_integrability_abs component",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_2_fixed_reference",
            "clause": "fixed reference/counterterm",
            "mathematical_statement": "H_ref and boundary representative are chosen before source/readout and cannot be fitted to cancel B_zero_flux.",
            "status": "MISSING_FIXED_REFERENCE",
            "obstruction": "reference/counterterm convention and selector source remain unowned",
            "fallback": "B_zero_flux_over_MH absolute numerator",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_3_compact_support",
            "clause": "compact support/falloff",
            "mathematical_statement": "The exterior annulus has no source support and linked surfaces carry no improvement flux through the caps/corners.",
            "status": "CONDITIONAL_WORLD_TUBE_NOT_SIGNED",
            "obstruction": "worldtube/source selector and linking surfaces are contract-ready but not current-MTS theorem",
            "fallback": "Delta_worldtube_domain and B_zero_flux terms",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_4_Hilbert_topological_equality",
            "clause": "Hilbert/topological equality",
            "mathematical_statement": "Pi_M J_H = J_M_top + dB_zero and integral_boundary dB_zero=0 in the linked compact exterior.",
            "status": "MISSING_EQUALITY_THEOREM",
            "obstruction": "closed topological charge can be the wrong charge; projector algebra is not flux closure",
            "fallback": "R_eq_integral + I_commutator + B_zero_flux",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_5_denominator",
            "clause": "positive same-frame denominator",
            "mathematical_statement": "B_zero_flux is scoreable only after M_H_ref=H_tau-H_ref is positive, finite, same-frame and source-backed.",
            "status": "MISSING_MHREF",
            "obstruction": "M_H_ref has no claim-valid theorem-zero or data row",
            "fallback": "keep first B_zero row non-score-ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZT2338_6_verdict",
            "clause": "B_zero_flux=0 now",
            "mathematical_statement": "BZT2338_1 through BZT2338_5 all parent-signed would imply B_zero_flux=0 or a scoreable normalized boundary residual.",
            "status": "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW",
            "obstruction": "the zero theorem stack is exact but unsigned in the current corpus",
            "fallback": "Bzero first bound row with valid_for_claim=false",
            "valid_for_claim": "false",
        },
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZR2338_0_first_row",
            "quantity": "epsilon_Bzero_abs",
            "formula": "epsilon_Bzero_abs := abs(B_zero_flux) / M_H_ref",
            "numerator": "B_zero_flux",
            "denominator": "M_H_ref",
            "units": "dimensionless after GM/source normalization",
            "current_value": "MISSING_B_ZERO_FLUX;MISSING_M_H_REF",
            "required_for_claim": "finite B_zero_flux; positive same-frame M_H_ref; source path; equation ref; fixed-reference certificate; no-cancellation guard",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZR2338_1_zero_switch",
            "quantity": "B_zero_flux_zero",
            "formula": "theorem_zero=true iff parent-signed boundary no-flux theorem supplies BZT2338_1..5",
            "numerator": "0 if theorem signed",
            "denominator": "M_H_ref still recorded for units/audit",
            "units": "boolean theorem switch plus dimensionless audit row",
            "current_value": "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNATURE",
            "required_for_claim": "parent theta/Q_tau; fixed reference; compact support; Hilbert/topological equality; positive M_H_ref",
            "status": "ZERO_SWITCH_BLOCKED",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BZR2338_2_absolute_sum_guard",
            "quantity": "epsilon_boundary_abs",
            "formula": "epsilon_boundary_abs >= abs(B_zero_flux)/M_H_ref + abs(Delta_symp)/M_H_ref + abs(Delta_worldtube_domain) + abs(I_commutator)/M_H_ref",
            "numerator": "B_zero_flux;Delta_symp;Delta_worldtube_domain;I_commutator",
            "denominator": "M_H_ref or dimensionless component normalization",
            "units": "dimensionless absolute envelope",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "required_for_claim": "all components finite, sourced, same-frame and absolute-summed",
            "status": "NO_CANCELLATION_GUARD_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_dependency_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "BDD2338_0_theta_Qtau", "dependency": "theta_MTS and Q_tau^MTS", "why_needed": "defines the actual parent boundary charge rather than importing EH charge", "current_status": "MISSING_PARENT_EXTRACTION", "blocks": "B_zero theorem and H_tau integrability", "next_input": "parent theta/Q_tau extraction or decomposition ledger", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BDD2338_1_fixed_reference", "dependency": "fixed H_ref/counterterm", "why_needed": "prevents fitted boundary cancellation", "current_status": "MISSING_FIXED_REFERENCE_CERTIFICATE", "blocks": "B_zero numerator and M_H_ref denominator", "next_input": "fixed reference selector source", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BDD2338_2_MHref", "dependency": "positive same-frame M_H_ref", "why_needed": "normalizes every B_zero/R_eq/I_commutator row", "current_status": "MISSING_M_H_REF", "blocks": "score-ready boundary row", "next_input": "H_tau-H_ref first row or theorem", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BDD2338_3_worldtube", "dependency": "worldtube/linking-surface selector", "why_needed": "defines the compact boundary pair and exterior annulus before readout", "current_status": "CONDITIONAL_NOT_PARENT_SIGNED", "blocks": "compact no-flux theorem", "next_input": "support selector and compactness/falloff proof", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "BDD2338_4_PiM_equality", "dependency": "Pi_M J_H = J_M_top + dB_zero", "why_needed": "prevents conserved-wrong-object error", "current_status": "MISSING_EQUALITY_THEOREM", "blocks": "Newton/source-normalization claim", "next_input": "Hilbert/topological equality or R_eq bound", "valid_for_claim": "false"},
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "DEC2338_0_theorem_result", "decision": "B_zero_flux zero theorem not derived", "reason": "theta/Q_tau, fixed reference, compact support, Hilbert/topological equality and M_H_ref are unsigned", "consequence": "retain Bzero bound row", "status": "ZERO_THEOREM_FAILED_CLEANLY", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2338_1_bound_row", "decision": "stage first Bzero bound row", "reason": "this gives the next executable object without claiming a value", "consequence": "epsilon_Bzero_abs schema ready but non-score-ready", "status": "FIRST_BOUND_ROW_STAGED_NONCLAIM", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2338_2_next", "decision": "attack parent theta/Qtau fixed-reference denominator next", "reason": "Bzero cannot be scored until the boundary charge and M_H_ref are owned", "consequence": "next target moves to theta/Q_tau/H_ref/M_H_ref extraction", "status": "SELECT_THETA_QTAU_FIXED_REFERENCE_NEXT", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "DEC2338_3_public_policy", "decision": "no GitHub evidence update", "reason": "boundary obstruction is still open and local-GR/Newton remains blocked", "consequence": "private checkpoint only", "status": "NO_GITHUB_EVIDENCE_UPDATE", "valid_for_claim": "false"},
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2338_0_Bzero_zero", "gate": "B_zero_flux=0 theorem derived", "passed": "false", "claim_effect": "zero theorem blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2338_1_Bzero_bound_score", "gate": "Bzero first row score-ready", "passed": "false", "claim_effect": "missing numerator and M_H_ref", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2338_2_fixed_reference", "gate": "fixed reference/counterterm signed", "passed": "false", "claim_effect": "fitted-reference guard remains live", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2338_3_MHref", "gate": "positive same-frame M_H_ref exists", "passed": "false", "claim_effect": "normalization blocked", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2338_4_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "boundary/source-normalization still blocks", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2338_5_github", "gate": "safe public evidence update", "passed": "false", "claim_effect": "private checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2338_0_reference_zero", "claim": "B_zero_flux=0 by choosing the reference", "allowed": "false", "reason": "fixed reference must be parent-owned before readout; fitted cancellation is refused", "blocking_rows": "BZT2338_2_fixed_reference;CG2338_2_fixed_reference", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2338_1_EH_import", "claim": "use EH boundary charge as the MTS boundary charge", "allowed": "false", "reason": "MTS theta/Q_tau must be extracted or EH reduction proven first", "blocking_rows": "BZT2338_1_parent_symplectic;BDD2338_0_theta_Qtau", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2338_2_unnormalized_bound", "claim": "score B_zero_flux without M_H_ref", "allowed": "false", "reason": "Bzero row needs positive same-frame denominator and units", "blocking_rows": "BZT2338_5_denominator;BZR2338_0_first_row", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2338_3_local_gr", "claim": "2338 proves local GR/Newton", "allowed": "false", "reason": "2338 stages a nonclaim boundary row and leaves source-normalization gates open", "blocking_rows": "CG2338_4_local_GR_Newton", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "NEXT2338_0", "next_target": "2339-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md", "why": "Bzero cannot be theorem-zero or score-ready until the parent boundary charge, fixed reference and M_H_ref denominator are owned.", "claim_status": "private_derivation_next_step", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2338_1", "next_target": "2339b-Y5-R2FR-Hilbert-topological-equality-or-Req-bound.md", "why": "closed topological charge is not enough; Pi_M J_H must equal the measured/topological charge or produce R_eq.", "claim_status": "parallel_nonclaim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "NEXT2338_2", "next_target": "2339c-Y5-R2FR-Bzero-source-backed-numerator-acquisition.md", "why": "fallback route if theorem path stalls: source a finite B_zero numerator and units without claiming a pass.", "claim_status": "fallback_nonclaim", "valid_for_claim": "false"},
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
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append({"branch_id": BRANCH_ID, "row_id": row_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": "false"})

    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    required_sources = [row for row in source_rows if row["required"] == "true"]

    add("VAL2338_00_required_sources_exist", all(row["exists"] == "true" for row in required_sources), "every required source path exists")
    add("VAL2338_01_required_needles_found", all(row["needles_found"] == "true" for row in required_sources), "all required source needles were found")
    theorem_rows = read_csv_rows(OUTPUTS["theorem"])
    add("VAL2338_02_zero_theorem_not_derived", any(row.get("row_id") == "BZT2338_6_verdict" and row.get("status") == "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW" for row in theorem_rows), "Bzero zero theorem not promoted")
    bound_rows = read_csv_rows(OUTPUTS["bound_row"])
    add("VAL2338_03_bound_row_staged", any(row.get("row_id") == "BZR2338_0_first_row" and "epsilon_Bzero_abs" in row.get("quantity", "") for row in bound_rows), "Bzero first bound row exists")
    add("VAL2338_04_bound_rows_nonready", all(row.get("score_ready") == "false" for row in bound_rows), "Bzero rows remain non-score-ready")
    dep_rows = read_csv_rows(OUTPUTS["dependencies"])
    add("VAL2338_05_dependencies_named", {"BDD2338_0_theta_Qtau", "BDD2338_1_fixed_reference", "BDD2338_2_MHref"}.issubset({row.get("row_id") for row in dep_rows}), "theta/Qtau, fixed reference and MHref dependencies named")
    decision_rows = read_csv_rows(OUTPUTS["decision"])
    add("VAL2338_06_next_selected", any(row.get("row_id") == "DEC2338_2_next" and row.get("status") == "SELECT_THETA_QTAU_FIXED_REFERENCE_NEXT" for row in decision_rows), "theta/Qtau fixed-reference next selected")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2338_07_local_claims_block", any(row.get("row_id") == "CG2338_4_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2338_08_github_blocked", any(row.get("row_id") == "CG2338_5_github" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended from 2338")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2338_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    next_rows = read_csv_rows(OUTPUTS["next"])
    add("VAL2338_10_next_target", any(row.get("row_id") == "NEXT2338_0" and "theta-Qtau" in row.get("next_target", "") for row in next_rows), "next target recorded")
    add("VAL2338_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")

    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2338_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))

    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ("*2338*.csv", "*2338*.md", "*BZERO*2338*", "*Bzero*2338*"):
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2338_13_formalization_untouched_by_2338", not formalization_hits, "no 2338 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2338_OVERALL", all(row["status"] == "PASS" for row in rows), "2338 attempts the B_zero_flux no-flux theorem, rejects zero promotion without parent theta/Qtau/fixed reference/MHref/Hilbert equality, stages the first nonclaim Bzero bound row, and selects parent theta/Qtau fixed-reference/MHref next.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    dependency_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2338 - boundary no-flux theorem or Bzero first bound row

## Summary

2338 attacks the boundary blocker selected by 2337.

The target theorem is `B_zero_flux = 0` for compact linked source boundaries. The exact route is clear, but current MTS
does not yet sign the required stack: parent `theta/Q_tau`, fixed reference, boundary conditions, compact support,
Hilbert/topological equality and positive same-frame `M_H_ref`.

So the zero theorem is not promoted. Instead, 2338 stages the first honest boundary row:

`epsilon_Bzero_abs := abs(B_zero_flux) / M_H_ref`.

This row is deliberately non-score-ready until the numerator, denominator, units, source path and no-cancellation guard
are real.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "required", "needles_found", "source_role", "valid_for_claim"])}

## Bzero No-Flux Theorem Audit

{markdown_table(theorem_rows, ["row_id", "clause", "mathematical_statement", "status", "obstruction", "fallback", "valid_for_claim"])}

## Bzero First Bound Row

{markdown_table(bound_rows, ["row_id", "quantity", "formula", "current_value", "required_for_claim", "status", "score_ready", "valid_for_claim"])}

## Boundary Denominator Dependency

{markdown_table(dependency_rows, ["row_id", "dependency", "why_needed", "current_status", "blocks", "next_input", "valid_for_claim"])}

## Decision Ledger

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
        "theorem": build_theorem_rows(),
        "bound_row": build_bound_rows(),
        "dependencies": build_dependency_rows(),
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
        rows_by_output["theorem"],
        rows_by_output["bound_row"],
        rows_by_output["dependencies"],
        rows_by_output["decision"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2338 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
