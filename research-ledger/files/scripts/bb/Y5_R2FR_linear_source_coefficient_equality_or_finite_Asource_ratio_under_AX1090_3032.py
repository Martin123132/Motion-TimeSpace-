from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3032"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3032-Y5-R2FR-linear-source-coefficient-equality-or-finite-Asource-ratio-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3032_00_3031_doc": ROOT / "3031-Y5-R2FR-Asource-denominator-owner-or-first-source-backed-value-under-AX1090.md",
    "SRC3032_01_3031_ratio": RESIDUALS / "P8_Y5_R2FR_3031_ASOURCE_RATIO_THEOREM_ATTEMPT.csv",
    "SRC3032_02_3031_coefficients": RESIDUALS / "P8_Y5_R2FR_3031_LINEAR_SOURCE_COEFFICIENT_ROWS.csv",
    "SRC3032_03_3031_denominator": RESIDUALS / "P8_Y5_R2FR_3031_DENOMINATOR_OWNER_AUDIT.csv",
    "SRC3032_04_3031_candidates": RESIDUALS / "P8_Y5_R2FR_3031_ASOURCE_CANDIDATE_VALUE_ROWS.csv",
    "SRC3032_05_3031_next": RESIDUALS / "P8_Y5_R2FR_3031_NEXT_TARGET.csv",
    "SRC3032_06_3030_clock_lapse": RESIDUALS / "P8_Y5_R2FR_3030_CLOCK_LAPSE_PACKAGE_AUDIT.csv",
    "SRC3032_07_3022_psin_owner": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3032_08_3024_hcore_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3032_09_3024_variation": RESIDUALS / "P8_Y5_R2FR_3024_VARIATION_DERIVATION.csv",
    "SRC3032_10_2921_source_mass": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "SRC3032_11_2921_pg_bridge": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3032_12_2924_source_attempt": RESIDUALS / "P8_Y5_R2FR_2924_SOURCE_MASS_FIRST_ROW_ATTEMPT.csv",
    "SRC3032_13_2945_denominator": RESIDUALS / "P8_Y5_R2FR_2945_DENOMINATOR_BLOCKER_ROWS.csv",
    "SRC3032_14_2947_import_guards": RESIDUALS / "P8_Y5_R2FR_2947_CHARGE_IMPORT_GUARDS.csv",
    "SRC3032_15_3006_htau": RESIDUALS / "P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv",
    "SRC3032_16_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3032_17_3008_coupling": RESIDUALS / "P8_Y5_R2FR_3008_COUPLING_GUARD_ROWS.csv",
    "SRC3032_18_3017_ward": RESIDUALS / "P8_Y5_R2FR_3017_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "SRC3032_19_hamiltonian_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "SRC3032_20_worldtube_theorem": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3032_SOURCE_REGISTER.csv",
    "equality_proof": RESIDUALS / "P8_Y5_R2FR_3032_COEFFICIENT_EQUALITY_PROOF_ATTEMPT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3032_COEFFICIENT_EQUALITY_COUNTERMODEL_LEDGER.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_3032_FINITE_COEFFICIENT_INPUT_ROWS.csv",
    "ratio_runner": RESIDUALS / "P8_Y5_R2FR_3032_ASOURCE_RATIO_RUNNER_SCHEMA.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3032_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3032_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3032_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3032_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3032_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "equality_copy": PARENT_ACTION / "linear_source_coefficient_equality_proof_3032_NOT_SIGNED.csv",
    "countermodel_copy": LOCAL_BOUNDS / "coefficient_equality_countermodels_3032_NONCLAIM.csv",
    "finite_rows_copy": LOCAL_BOUNDS / "finite_CpsiH_CWH_input_rows_3032_NONCLAIM.csv",
    "ratio_runner_copy": LOCAL_BOUNDS / "A_source_ratio_runner_schema_3032_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3032_SOURCE_VERTEX_OR_FINITE_COEFFICIENT_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_roles = {
    "SRC3032_00_3031_doc": "3031 handoff: A_source ratio law",
    "SRC3032_01_3031_ratio": "A_source=C_psiH/C_WH ratio theorem",
    "SRC3032_02_3031_coefficients": "missing C_psiH/C_WH coefficient rows",
    "SRC3032_03_3031_denominator": "denominator owner audit",
    "SRC3032_04_3031_candidates": "A_source candidate value rows",
    "SRC3032_05_3031_next": "3032 target selection",
    "SRC3032_06_3030_clock_lapse": "clock/lapse package not signed",
    "SRC3032_07_3022_psin_owner": "psi_N parent owner audit",
    "SRC3032_08_3024_hcore_ansatz": "minimal Hcore ansatz",
    "SRC3032_09_3024_variation": "Hcore variation derivation",
    "SRC3032_10_2921_source_mass": "parent source mass identity audit",
    "SRC3032_11_2921_pg_bridge": "Poisson/Gauss/orbital bridge audit",
    "SRC3032_12_2924_source_attempt": "source mass first-row attempt",
    "SRC3032_13_2945_denominator": "denominator blocker rows",
    "SRC3032_14_2947_import_guards": "EH/orbital import guards",
    "SRC3032_15_3006_htau": "H_tau extraction rows",
    "SRC3032_16_3007_grammar": "minimal parent action grammar",
    "SRC3032_17_3008_coupling": "coupling guard rows",
    "SRC3032_18_3017_ward": "source-current Ward owner attempt",
    "SRC3032_19_hamiltonian_contract": "Hamiltonian source-measure contract",
    "SRC3032_20_worldtube_theorem": "worldtube source-measure theorem",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

equality_rows = [
    base(
        {
            "proof_id": "EQ3032_0_common_branch_variable",
            "claim": "psi_N and W/c^2 are the same parent scalar or are linked by a parent constraint before readout",
            "mathematical_role": "identifies the fields whose source coefficients are being compared",
            "required_evidence": "parent variable map or multiplier constraint with variation and boundary terms",
            "current_status": "MISSING_PARENT_FIELD_OR_CONSTRAINT_LINK",
            "passes_equality": False,
            "if_missing": "C_psiH and C_WH may be independent coefficients",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_1_same_operator",
            "claim": "both weak-field equations use the same normalized linear operator L_loc",
            "mathematical_role": "lets uniqueness compare coefficients rather than two different Green functions",
            "required_evidence": "operator normalization, kinetic density, gauge/boundary class and no harmonic mode",
            "current_status": "MISSING_OPERATOR_BOUNDARY_MATCH",
            "passes_equality": False,
            "if_missing": "A_source can differ by kinetic normalization even with the same source",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_2_same_source_current",
            "claim": "the source on both sides is the same J_H/H_tau/M_H_ref/worldtube object",
            "mathematical_role": "prevents comparing a Hilbert current to a Hamiltonian/orbital readout current",
            "required_evidence": "J_H/H_tau/Pi_M/worldtube equality and same tau/surface/frame",
            "current_status": "MISSING_HILBERT_TO_HTAU_MAP",
            "passes_equality": False,
            "if_missing": "unity could be a relabelled source normalization",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_3_same_coupling_constant",
            "claim": "G_ref/kappa/ell_J/source-current scale is common and derivative-silent",
            "mathematical_role": "removes source-scale drift from C_WH relative to C_psiH",
            "required_evidence": "constant universal coupling with no source/range/species/frame drift",
            "current_status": "MISSING_CONSTANT_KAPPA_AND_ELLJ_PROOF",
            "passes_equality": False,
            "if_missing": "C_psiH/C_WH carries coupling-scale residuals",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_4_same_source_vertex",
            "claim": "the parent action contains one source vertex whose variation feeds both coefficients with equal weight",
            "mathematical_role": "the direct route to C_psiH=C_WH",
            "required_evidence": "single source vertex, no source-only prefactor, no hidden frame, no independent W or psi_N source weights",
            "current_status": "MISSING_SINGLE_SOURCE_VERTEX_OWNER",
            "passes_equality": False,
            "if_missing": "a legal countermodel can set C_psiH=(1+epsilon)C_WH",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_5_residual_silence",
            "claim": "R_psi and R_W vanish or are source-bounded before equality is promoted",
            "mathematical_role": "prevents boundary/projector/memory/source-shadow terms from masquerading as coefficient equality",
            "required_evidence": "zero theorem or finite rows for source-shadow, non-Hilbert, projector, boundary and radial residuals",
            "current_status": "MISSING_RESIDUAL_ZERO_OR_BOUND",
            "passes_equality": False,
            "if_missing": "ratio theorem is exact only up to retained residuals",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_6_no_EH_or_orbital_import",
            "claim": "C_WH is not imported from EH-only reference or measured orbital GM",
            "mathematical_role": "keeps equality from becoming a GR calibration disguised as MTS derivation",
            "required_evidence": "MTS parent source coefficient with anti-circularity certificate",
            "current_status": "GUARD_PRESENT_VALUE_MISSING",
            "passes_equality": True,
            "if_missing": "claim would be circular; guard exists but coefficient still absent",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_7_countermodel_exclusion",
            "claim": "all legal unequal-coefficient countermodels are excluded by parent grammar",
            "mathematical_role": "turns the conditional equality into a theorem",
            "required_evidence": "no independent source coefficient, no relative sector weights, no hidden frame, no separate clock/lapse source slot",
            "current_status": "COUNTERMODELS_NOT_EXCLUDED",
            "passes_equality": False,
            "if_missing": "C_psiH=C_WH is plausible but not forced",
        }
    ),
    base(
        {
            "proof_id": "EQ3032_8_verdict",
            "claim": "C_psiH=C_WH is parent-signed",
            "mathematical_role": "would imply A_source=1 under the 3031 ratio law",
            "required_evidence": "EQ3032_0 through EQ3032_7 pass together",
            "current_status": "COEFFICIENT_EQUALITY_NOT_SIGNED",
            "passes_equality": False,
            "if_missing": "A_source=1 remains a target theorem, not a claim",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3032_0_independent_source_weight",
            "description": "parent action has equal-looking geometry but source vertex J_H[(1+epsilon_psi)psi_N + W/c^2]",
            "effect_on_ratio": "A_source=1+epsilon_psi",
            "allowed_by_current_corpus": True,
            "blocked_by": "single source vertex/no independent psi_N source weight theorem",
            "status": "LIVE_COUNTERMODEL",
        }
    ),
    base(
        {
            "countermodel_id": "CM3032_1_operator_normalization",
            "description": "psi_N and W/c^2 share J_H but have kinetic operators L_psi=(1+epsilon_L)L_W",
            "effect_on_ratio": "A_source=(C_psiH/C_WH)/(1+epsilon_L)",
            "allowed_by_current_corpus": True,
            "blocked_by": "same normalized operator and boundary theorem",
            "status": "LIVE_COUNTERMODEL",
        }
    ),
    base(
        {
            "countermodel_id": "CM3032_2_hidden_frame_source",
            "description": "matter/source couples through a hidden conformal/disformal frame before observed readout",
            "effect_on_ratio": "C_psiH and C_WH see different source density",
            "allowed_by_current_corpus": True,
            "blocked_by": "observed coframe descent/no hidden frame proof",
            "status": "LIVE_COUNTERMODEL",
        }
    ),
    base(
        {
            "countermodel_id": "CM3032_3_source_shadow_channel",
            "description": "boundary, projector, memory or non-Hilbert current contributes to one equation but not the other",
            "effect_on_ratio": "A_source gains residual term R_shadow/C_WH",
            "allowed_by_current_corpus": True,
            "blocked_by": "residual zero theorem or finite residual rows",
            "status": "LIVE_COUNTERMODEL",
        }
    ),
    base(
        {
            "countermodel_id": "CM3032_4_EH_calibration_import",
            "description": "C_WH is set from EH/GR Poisson normalization while C_psiH remains MTS-defined",
            "effect_on_ratio": "apparent A_source=1 can be circular",
            "allowed_by_current_corpus": False,
            "blocked_by": "anti-circularity guards",
            "status": "REJECTED_SHORTCUT_GUARD_ACTIVE",
        }
    ),
]

finite_rows = [
    base(
        {
            "input_id": "FIN3032_0_C_psiH",
            "symbol": "C_psiH",
            "definition": "coefficient of the parent source current in the linearized psi_N equation",
            "required_equation_shape": "L_psi psi_N = C_psiH rho_H + R_psi",
            "required_columns": "operator_id; source_current_id; tau_frame_id; boundary_class; numeric_value; units; source_path; equation_ref; residual_policy; valid_for_claim",
            "numeric_value": "MISSING_C_PSIH",
            "units": "operator_units_per_mass_density",
            "status": "FINITE_INPUT_ROW_TEMPLATE_ONLY",
            "missing_for_claim": "MISSING_PARENT_PSI_N_EQUATION; MISSING_SOURCE_VERTEX; MISSING_UNITS; MISSING_BOUNDARY_CLASS",
        }
    ),
    base(
        {
            "input_id": "FIN3032_1_C_WH",
            "symbol": "C_WH",
            "definition": "coefficient of the parent source current in the linearized W/c^2 Poisson/Gauss equation",
            "required_equation_shape": "L_W(W/c^2) = C_WH rho_H + R_W",
            "required_columns": "operator_id; source_current_id; G_ref; M_H_ref; tau_frame_id; numeric_value; units; source_path; equation_ref; no_orbital_GM_import; valid_for_claim",
            "numeric_value": "MISSING_C_WH",
            "units": "operator_units_per_mass_density",
            "status": "FINITE_INPUT_ROW_TEMPLATE_ONLY",
            "missing_for_claim": "MISSING_PARENT_W_EQUATION; MISSING_G_REF; MISSING_M_H_REF; MISSING_NO_ORBITAL_GM_CERTIFICATE",
        }
    ),
    base(
        {
            "input_id": "FIN3032_2_delta_A_source",
            "symbol": "delta_A_source",
            "definition": "deviation from the unity theorem target",
            "required_equation_shape": "delta_A_source = C_psiH/C_WH - 1",
            "required_columns": "C_psiH; C_WH; covariance_or_error; denominator_nonzero; residual_envelope; units; valid_for_claim",
            "numeric_value": "MISSING_DELTA_A_SOURCE",
            "units": "dimensionless",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "missing_for_claim": "MISSING_C_PSIH; MISSING_C_WH; MISSING_RESIDUAL_ENVELOPE",
        }
    ),
    base(
        {
            "input_id": "FIN3032_3_residual_envelope",
            "symbol": "epsilon_A_residual_abs",
            "definition": "absolute no-cancellation envelope for R_psi, R_W, boundary mismatch and source-shadow channels",
            "required_equation_shape": "epsilon_A_residual_abs >= abs(R_psi/C_WH)+abs(R_W*C_psiH/C_WH^2)+abs(boundary/harmonic/source_shadow)",
            "required_columns": "R_psi_bound; R_W_bound; boundary_bound; source_shadow_bound; no_cancellation_guard; units; valid_for_claim",
            "numeric_value": "MISSING_RESIDUAL_ENVELOPE",
            "units": "dimensionless",
            "status": "BOUND_TEMPLATE_ONLY",
            "missing_for_claim": "MISSING_R_PSI_BOUND; MISSING_R_W_BOUND; MISSING_BOUNDARY_BOUND; MISSING_SOURCE_SHADOW_BOUND",
        }
    ),
]

ratio_runner_rows = [
    base(
        {
            "runner_id": "RUN3032_0_unity_theorem",
            "input_condition": "EQ3032_0..7 all pass",
            "output": "A_source=1",
            "current_result": "REFUSE_THEOREM_PROMOTION",
            "why": "coefficient equality not parent-signed",
        }
    ),
    base(
        {
            "runner_id": "RUN3032_1_finite_ratio",
            "input_condition": "finite C_psiH and C_WH rows pass with denominator_nonzero=true",
            "output": "A_source=C_psiH/C_WH and delta_A_source",
            "current_result": "REFUSE_NUMERIC_RATIO",
            "why": "finite coefficient rows are templates only",
        }
    ),
    base(
        {
            "runner_id": "RUN3032_2_local_GR_reentry",
            "input_condition": "A_source row plus residual envelope and PPN followthrough all pass",
            "output": "local Newton/GR source-normalization reopens",
            "current_result": "BLOCKED_NO_CLAIM",
            "why": "A_source, M_H_ref, preferred-frame and second-order residuals are still nonclaim",
        }
    ),
]

promotion_gate_rows = [
    base(
        {
            "gate_id": "GATE3032_0_sources",
            "gate": "every cited local source path exists",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "source-backed audit only",
        }
    ),
    base(
        {
            "gate_id": "GATE3032_1_conditional_proof",
            "gate": "conditional proof that C_psiH=C_WH implies A_source=1 is recorded",
            "result": True,
            "notes": "proof route is exact under listed clauses",
        }
    ),
    base(
        {
            "gate_id": "GATE3032_2_equality_signed",
            "gate": "C_psiH=C_WH is parent-signed",
            "result": False,
            "notes": "single source vertex, same operator and same source bridge are missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3032_3_countermodels_excluded",
            "gate": "unequal-coefficient countermodels are excluded",
            "result": False,
            "notes": "independent source weight, operator normalization and hidden-frame countermodels remain live",
        }
    ),
    base(
        {
            "gate_id": "GATE3032_4_finite_ratio_ready",
            "gate": "finite C_psiH/C_WH ratio can be computed",
            "result": False,
            "notes": "finite coefficient rows are templates only",
        }
    ),
    base(
        {
            "gate_id": "GATE3032_5_A_source_claim",
            "gate": "A_source is claimable",
            "result": False,
            "notes": "neither unity theorem nor finite ratio route is ready",
        }
    ),
    base(
        {
            "gate_id": "GATE3032_6_local_GR_claim",
            "gate": "local GR/Newton reduction is claimable",
            "result": False,
            "notes": "source coefficient equality, denominator, residual envelope and PPN followthrough remain open",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3032_0_unity",
            "decision": "reject current A_source=1 claim",
            "rationale": "the equality proof is conditionally exact but live countermodels remain legal",
            "consequence": "A_source=1 stays a theorem target, not an adopted value",
        }
    ),
    base(
        {
            "decision_id": "DEC3032_1_countermodels",
            "decision": "keep unequal-coefficient countermodels explicit",
            "rationale": "they show what a parent action must forbid, not that the theory is dead",
            "consequence": "next route should target the single source vertex / common operator clause",
        }
    ),
    base(
        {
            "decision_id": "DEC3032_2_finite_rows",
            "decision": "stage finite C_psiH and C_WH intake rows",
            "rationale": "if equality cannot be proved, the ratio law still gives a disciplined finite path",
            "consequence": "no A_source numeric claim until both coefficient rows pass",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3032_0_3033",
            "target_doc": "3033-Y5-R2FR-single-source-vertex-or-common-linear-operator-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_single_source_vertex_or_common_linear_operator_under_AX1090_3033.py",
            "mission": "try to parent-sign the single source vertex/common operator clause that would force C_psiH=C_WH; if not, fill the first concrete C_psiH or C_WH source-row field from existing Hcore or Poisson/Gauss material",
            "success_condition": "either unequal-coefficient countermodels are excluded by a parent source-vertex theorem, or the first finite coefficient input row becomes source-backed nonclaim with units and equation path",
            "forbidden": "no EH-only coefficient import; no orbital-GM denominator; no convention-only A_source=1; no cancellation; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

for key, output_rows in {
    "sources": source_register,
    "equality_proof": equality_rows,
    "countermodels": countermodel_rows,
    "finite_rows": finite_rows,
    "ratio_runner": ratio_runner_rows,
    "gates": promotion_gate_rows,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[key], output_rows)

copy_plan = {
    "equality_copy": OUTPUTS["equality_proof"],
    "countermodel_copy": OUTPUTS["countermodels"],
    "finite_rows_copy": OUTPUTS["finite_rows"],
    "ratio_runner_copy": OUTPUTS["ratio_runner"],
    "next_copy": OUTPUTS["next"],
}

for copy_key, source_path in copy_plan.items():
    shutil.copyfile(source_path, BRANCH_OUTPUTS[copy_key])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(BRANCH_OUTPUTS[copy_id]),
            "source_exists": source_path.exists(),
            "copy_exists": BRANCH_OUTPUTS[copy_id].exists(),
            "purpose": {
                "equality_copy": "parent-action branch copy of coefficient equality proof attempt",
                "countermodel_copy": "local-bound branch copy of live unequal-coefficient countermodels",
                "finite_rows_copy": "local-bound branch copy of finite coefficient intake rows",
                "ratio_runner_copy": "local-bound branch copy of A_source ratio runner refusal schema",
                "next_copy": "RAB acquisition queue handoff",
            }[copy_id],
        }
    )
    for copy_id, source_path in copy_plan.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

claim_rows = (
    source_register
    + equality_rows
    + countermodel_rows
    + finite_rows
    + ratio_runner_rows
    + promotion_gate_rows
    + decision_rows
    + next_rows
    + branch_rows
)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
csv_paths_before_validation = [path for key, path in OUTPUTS.items() if key != "validation"]


def missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(as_str(value) for value in row.values())


validation_rows = [
    {
        "validation_id": "VAL3032_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": "P8_Y5_R2FR_3032_SOURCE_REGISTER.csv",
    },
    {
        "validation_id": "VAL3032_01_csv_parse",
        "passed": all(csv_ok(path) for path in csv_paths_before_validation),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all 3032 CSV artifacts except validation import with csv.DictReader",
    },
    {
        "validation_id": "VAL3032_02_equality_rejected",
        "passed": any(row["current_status"] == "COEFFICIENT_EQUALITY_NOT_SIGNED" and not boolish(row["passes_equality"]) for row in equality_rows),
        "requirement": "C_psiH=C_WH fails closed",
        "evidence": "P8_Y5_R2FR_3032_COEFFICIENT_EQUALITY_PROOF_ATTEMPT.csv",
    },
    {
        "validation_id": "VAL3032_03_countermodels_live",
        "passed": any(row["status"] == "LIVE_COUNTERMODEL" for row in countermodel_rows),
        "requirement": "unequal-coefficient countermodels are recorded",
        "evidence": "P8_Y5_R2FR_3032_COEFFICIENT_EQUALITY_COUNTERMODEL_LEDGER.csv",
    },
    {
        "validation_id": "VAL3032_04_finite_rows_present",
        "passed": {"C_psiH", "C_WH", "delta_A_source"}.issubset({row["symbol"] for row in finite_rows}),
        "requirement": "finite coefficient intake rows exist",
        "evidence": "P8_Y5_R2FR_3032_FINITE_COEFFICIENT_INPUT_ROWS.csv",
    },
    {
        "validation_id": "VAL3032_05_unity_not_claimed",
        "passed": any(row["runner_id"] == "RUN3032_0_unity_theorem" and row["current_result"] == "REFUSE_THEOREM_PROMOTION" for row in ratio_runner_rows),
        "requirement": "A_source=1 is not claim-promoted",
        "evidence": "P8_Y5_R2FR_3032_ASOURCE_RATIO_RUNNER_SCHEMA.csv",
    },
    {
        "validation_id": "VAL3032_06_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if missing_marker(row)),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all generated 3032 claim-control rows",
    },
    {
        "validation_id": "VAL3032_07_branch_copies_exist",
        "passed": all(path.exists() for path in BRANCH_OUTPUTS.values()),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": "P8_Y5_R2FR_3032_BRANCH_COPIES.csv",
    },
    {
        "validation_id": "VAL3032_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in generated_paths),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3032_09_formalization_not_targeted",
        "passed": all(not under(path, FORMALIZATION) for path in generated_paths),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3032_10_no_shortcuts",
        "passed": any("no convention-only A_source=1" in row["forbidden"] and "no orbital-GM denominator" in row["forbidden"] for row in next_rows),
        "requirement": "shortcut guards remain active",
        "evidence": "P8_Y5_R2FR_3032_NEXT_TARGET.csv",
    },
    {
        "validation_id": "VAL3032_11_next_target_selected",
        "passed": any(boolish(row["selected"]) and "3033" in row["target_doc"] for row in next_rows),
        "requirement": "next target selects source vertex/common operator",
        "evidence": "P8_Y5_R2FR_3032_NEXT_TARGET.csv",
    },
]

overall = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3032_99_overall",
        "passed": overall,
        "requirement": "all 3032 validation checks pass",
        "evidence": "aggregate of VAL3032_00 through VAL3032_11",
    }
)
validation_rows = [base(row) for row in validation_rows]
write_csv(OUTPUTS["validation"], validation_rows)

doc_sections = [
    "# 3032 - Linear Source Coefficient Equality Or Finite A_source Ratio under AX1090",
    "",
    "Status: `Y5_R2FR_3032_coefficient_equality_not_signed_countermodels_live_finite_rows_staged_3033_next`",
    "",
    "## Verdict",
    "",
    "3032 tests the exact condition needed to turn the 3031 ratio law into the clean local-GR value:",
    "",
    "`A_source=1` iff `C_psiH=C_WH`.",
    "",
    "The conditional theorem is sound: if `psi_N` and `W/c^2` are governed by the same parent linear operator, the same source current, the same coupling scale, the same boundary/reference class, and no residual source-shadow channels, then the equality follows and `A_source=1` is derived.",
    "",
    "Current MTS does **not** yet prove those premises. Live countermodels remain: independent source weights, operator normalization differences, hidden matter/source frames, and source-shadow channels. Therefore `A_source=1` is still a theorem target, not a claim.",
    "",
    "The finite fallback is now ready in strict nonclaim form: fill `C_psiH`, `C_WH`, and `delta_A_source=C_psiH/C_WH-1` only from parent-sourced coefficient rows with units and no orbital-GM import.",
    "",
    "## Coefficient Equality Proof Attempt",
    "",
    md_table(equality_rows, ["proof_id", "claim", "current_status", "passes_equality", "if_missing"]),
    "",
    "## Countermodel Ledger",
    "",
    md_table(countermodel_rows, ["countermodel_id", "description", "effect_on_ratio", "allowed_by_current_corpus", "status"]),
    "",
    "## Finite Coefficient Input Rows",
    "",
    md_table(finite_rows, ["input_id", "symbol", "numeric_value", "status", "missing_for_claim"]),
    "",
    "## Ratio Runner Schema",
    "",
    md_table(ratio_runner_rows, ["runner_id", "input_condition", "output", "current_result", "why"]),
    "",
    "## Source Register",
    "",
    md_table(source_register, ["source_id", "exists", "role", "status"]),
    "",
    "## Promotion Gates",
    "",
    md_table(promotion_gate_rows, ["gate_id", "gate", "result", "notes"]),
    "",
    "## Decision Ledger",
    "",
    md_table(decision_rows, ["decision_id", "decision", "rationale", "consequence"]),
    "",
    "## Next Target",
    "",
    md_table(next_rows, ["next_id", "target_doc", "target_script", "mission", "success_condition"]),
    "",
    "## Validation",
    "",
    md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"]),
    "",
    "## Files Written",
    "",
]
doc_sections.extend(f"- `{path}`" for path in generated_paths if path.exists())
DOC.write_text("\n".join(doc_sections) + "\n", encoding="utf-8")

print(f"Wrote 3032 checkpoint: {DOC}")
print(f"Overall validation: {overall}")
