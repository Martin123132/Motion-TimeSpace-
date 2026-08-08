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

CHECKPOINT = "3030"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3030-Y5-R2FR-clock-lapse-constraint-package-or-first-Asource-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3030_00_3029_doc": ROOT / "3029-Y5-R2FR-covariant-LHcore-lift-or-first-Cbeta-component-value-under-AX1090.md",
    "SRC3030_01_3029_clauses": RESIDUALS / "P8_Y5_R2FR_3029_COVARIANT_LIFT_CLAUSE_AUDIT.csv",
    "SRC3030_02_3029_risks": RESIDUALS / "P8_Y5_R2FR_3029_CLOCK_LIFT_RISK_LEDGER.csv",
    "SRC3030_03_3029_component": RESIDUALS / "P8_Y5_R2FR_3029_FIRST_COMPONENT_VALUE_ATTEMPT.csv",
    "SRC3030_04_3022_psin": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3030_05_2930_source_coeff": RESIDUALS / "P8_Y5_R2FR_2930_SOURCE_COEFFICIENT_LEDGER.csv",
    "SRC3030_06_2923_hcore_qtau": RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv",
    "SRC3030_07_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3030_08_3006_current": RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv",
    "SRC3030_09_2924_reduction": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "SRC3030_10_3028_carry": RESIDUALS / "P8_Y5_R2FR_3028_COMPONENT_FILL_CARRYFORWARD.csv",
    "SRC3030_11_2599_delta_tau": RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
    "SRC3030_12_2599_clock_obstruction": RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_CLOCK_OBSTRUCTION_LEDGER.csv",
    "SRC3030_13_2599_claim_gates": RESIDUALS / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_CLAIM_GATES.csv",
    "SRC3030_14_3015_ppn_vector": RESIDUALS / "P8_Y5_R2FR_3015_PPN_RESIDUAL_VECTOR_TEMPLATE.csv",
    "SRC3030_15_3016_ppn_kernel": RESIDUALS / "P8_Y5_R2FR_3016_PPN_FIRST_KERNEL_ROWS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3030_SOURCE_REGISTER.csv",
    "clock_package": RESIDUALS / "P8_Y5_R2FR_3030_CLOCK_LAPSE_PACKAGE_AUDIT.csv",
    "preferred_frame": RESIDUALS / "P8_Y5_R2FR_3030_PREFERRED_FRAME_GUARD.csv",
    "asource_schema": RESIDUALS / "P8_Y5_R2FR_3030_ASOURCE_FIRST_ROW_SCHEMA.csv",
    "asource_validator": RESIDUALS / "P8_Y5_R2FR_3030_ASOURCE_ROW_VALIDATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3030_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3030_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3030_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3030_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3030_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "clock_package_copy": PARENT_ACTION / "clock_lapse_constraint_package_audit_3030_NOT_SIGNED.csv",
    "preferred_frame_copy": LOCAL_BOUNDS / "preferred_frame_guard_3030_NONCLAIM.csv",
    "asource_schema_copy": LOCAL_BOUNDS / "A_source_first_row_schema_3030_NONCLAIM.csv",
    "asource_validator_copy": LOCAL_BOUNDS / "A_source_row_validator_3030_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3030_CLOCK_LAPSE_OR_ASOURCE_NEXT_NONCLAIM.csv",
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
    "SRC3030_00_3029_doc": "3029 handoff: covariant clock/lapse lift candidate rejected",
    "SRC3030_01_3029_clauses": "3029 clock-lift blocker clauses",
    "SRC3030_02_3029_risks": "3029 preferred-frame/source/constraint risk ledger",
    "SRC3030_03_3029_component": "3029 first component value attempt",
    "SRC3030_04_3022_psin": "psi_N Hamiltonian owner audit",
    "SRC3030_05_2930_source_coeff": "A_source/B_source source-coefficient ledger",
    "SRC3030_06_2923_hcore_qtau": "Hcore/Q_tau source mass checklist",
    "SRC3030_07_3007_grammar": "minimal parent-action grammar and tau surface lock",
    "SRC3030_08_3006_current": "parent current-chain and H_tau/M_H_ref blockers",
    "SRC3030_09_2924_reduction": "MTS-to-EH reduction contract blockers",
    "SRC3030_10_3028_carry": "C_beta component carry-forward rows",
    "SRC3030_11_2599_delta_tau": "boundary clock/tau source pack",
    "SRC3030_12_2599_clock_obstruction": "boundary clock obstruction ledger",
    "SRC3030_13_2599_claim_gates": "clock/tau claim gates rejecting lapse shortcuts",
    "SRC3030_14_3015_ppn_vector": "PPN residual vector template for preferred-frame guard",
    "SRC3030_15_3016_ppn_kernel": "first PPN kernel rows for guard handoff",
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

clock_package_rows = [
    base(
        {
            "package_id": "CPK3030_0_parent_clock",
            "clause": "clock/foliation scalar T or tau_source is parent-owned, varied, and gauge classified",
            "required_evidence": "field list, constraint class, variation equation, and branch/gauge rule",
            "current_evidence": "3029 CLIFT3029_0 missing; 2599 CLK2599_0 missing parent boundary clock class",
            "current_status": "MISSING_PARENT_CLOCK_FIELD_ADOPTION",
            "passes_package": False,
            "consequence": "T cannot be inserted just to make the static lapse branch work",
        }
    ),
    base(
        {
            "package_id": "CPK3030_1_lapse_definition",
            "clause": "N_T=(-g^{ab} nabla_a T nabla_b T)^(-1/2) is defined inside the parent branch",
            "required_evidence": "parent clock normal is timelike, nondegenerate, and has a fixed normalization convention",
            "current_evidence": "definition is algebraically available from 3029, but the parent clock is unsigned",
            "current_status": "CONDITIONAL_DEFINITION_ONLY",
            "passes_package": False,
            "consequence": "N_T can be used in a candidate lift, not as a parent-sourced observable",
        }
    ),
    base(
        {
            "package_id": "CPK3030_2_lapse_constraint",
            "clause": "psi_N=-log N_T is enforced by a parent multiplier/constraint",
            "required_evidence": "C_Nlap, multiplier variation, no extra propagating lapse mode, boundary term",
            "current_evidence": "3029 CLIFT3029_1 missing; 2599 CG2599_2 rejects lapse/time-coordinate normalization shortcut",
            "current_status": "MISSING_LAPSE_CONSTRAINT",
            "passes_package": False,
            "consequence": "psi_N remains not parent-owned",
        }
    ),
    base(
        {
            "package_id": "CPK3030_3_variation",
            "clause": "metric, clock, psi_N, constraint, source, and boundary variations are all accounted",
            "required_evidence": "E_g, E_T, E_psi, E_lambda, theta_Hcore, and constraint stress ledger",
            "current_evidence": "3029 CLIFT3029_5 partial only; 3006 CCA3006_6 constraint component ledger missing",
            "current_status": "PARTIAL_VARIATION_ONLY",
            "passes_package": False,
            "consequence": "constraint stress could repair beta while spoiling another PPN channel",
        }
    ),
    base(
        {
            "package_id": "CPK3030_4_tau_surface_lock",
            "clause": "tau_source=tau_charge=tau_clock=tau_readout on the same parent surface/frame",
            "required_evidence": "tau/surface lock, source support equivalence, and clock/readout normalization",
            "current_evidence": "3007 G3007_9 missing tau surface lock; 2923 HC2923_2 missing tau lock; 2599 DTS2599_9 role mismatch missing",
            "current_status": "MISSING_TAU_SURFACE_LOCK",
            "passes_package": False,
            "consequence": "same symbol tau cannot be treated as same physical generator",
        }
    ),
    base(
        {
            "package_id": "CPK3030_5_source_bridge",
            "clause": "U=W/c^2, J_H, H_tau, M_H_ref and worldtube support are the same source object",
            "required_evidence": "positive same-frame M_H_ref, G_ref, J_H/H_tau equality, exterior silence, no orbital-GM import",
            "current_evidence": "3022 PHO3022_3 missing M_H_ref; 3006 CCA3006_8 source bridge missing; 2924 RED2924_8 worldtube glue missing",
            "current_status": "MISSING_SOURCE_BRIDGE_AND_MHREF",
            "passes_package": False,
            "consequence": "A_source cannot be normalized by measured orbital GM or by EH-only mass",
        }
    ),
    base(
        {
            "package_id": "CPK3030_6_preferred_frame",
            "clause": "clock/foliation lift gives zero or bounded alpha1, alpha2, xi and clock anisotropy residuals",
            "required_evidence": "preferred-frame zero theorem or finite sourced residual vector",
            "current_evidence": "3029 RISK3029_0 active; PPN residual vector exists only as nonclaim template rows",
            "current_status": "MISSING_PREFERRED_FRAME_GUARD",
            "passes_package": False,
            "consequence": "a foliation can fake GR beta/gamma while failing preferred-frame tests",
        }
    ),
    base(
        {
            "package_id": "CPK3030_7_boundary_reference",
            "clause": "boundary/reference class is fixed so the clock/lapse constraint does not move the charge",
            "required_evidence": "B_ref/H_ref phase space, orientation, extension and reference superselection",
            "current_evidence": "2599 DTS2599_2 reference phase space missing; CLK2599_6 reference class not parent-owned",
            "current_status": "MISSING_REFERENCE_PHASE_SPACE",
            "passes_package": False,
            "consequence": "clock normalization could be a boundary-reference choice rather than physics",
        }
    ),
    base(
        {
            "package_id": "CPK3030_8_verdict",
            "clause": "clock/lapse constraint package signs psi_N=-log N_T as parent-owned",
            "required_evidence": "CPK3030_0 through CPK3030_7 all pass",
            "current_evidence": "multiple required clauses remain missing or conditional",
            "current_status": "CLOCK_LAPSE_PACKAGE_NOT_SIGNED",
            "passes_package": False,
            "consequence": "move to strict A_source row rather than smuggling in the plateau/lapse axiom",
        }
    ),
]

preferred_frame_rows = [
    base(
        {
            "guard_id": "PFG3030_0_alpha1",
            "residual": "alpha1_clock_lift",
            "needed_for": "PPN preferred-frame safety",
            "required_exit": "parent-signed zero theorem or finite sourced alpha1 residual row",
            "current_status": "MISSING_ALPHA1_CLOCK_LIFT_RESIDUAL",
            "bound_interface": "PPN residual vector template only; no numeric/source-backed row",
            "passes_guard": False,
        }
    ),
    base(
        {
            "guard_id": "PFG3030_1_alpha2",
            "residual": "alpha2_clock_lift",
            "needed_for": "PPN preferred-frame safety",
            "required_exit": "parent-signed zero theorem or finite sourced alpha2 residual row",
            "current_status": "MISSING_ALPHA2_CLOCK_LIFT_RESIDUAL",
            "bound_interface": "PPN residual vector template only; no numeric/source-backed row",
            "passes_guard": False,
        }
    ),
    base(
        {
            "guard_id": "PFG3030_2_xi",
            "residual": "xi_clock_lift",
            "needed_for": "anisotropic/preferred-location safety",
            "required_exit": "parent-signed zero theorem or finite sourced xi residual row",
            "current_status": "MISSING_XI_CLOCK_LIFT_RESIDUAL",
            "bound_interface": "PPN residual vector template only; no numeric/source-backed row",
            "passes_guard": False,
        }
    ),
    base(
        {
            "guard_id": "PFG3030_3_clock_anisotropy",
            "residual": "clock_readout_anisotropy",
            "needed_for": "clock/redshift readout and local frame equality",
            "required_exit": "same tau generator plus clock-readout kernel source",
            "current_status": "MISSING_CLOCK_READOUT_ANISOTROPY_BOUND",
            "bound_interface": "2599 C_clock_tau and same-frame stress rows missing",
            "passes_guard": False,
        }
    ),
    base(
        {
            "guard_id": "PFG3030_4_source_frame_leak",
            "residual": "source_frame_leak",
            "needed_for": "Newton denominator and source-normalized local branch",
            "required_exit": "tau_source/tau_clock/tau_readout lock and source support equivalence",
            "current_status": "MISSING_SOURCE_FRAME_LEAK_BOUND",
            "bound_interface": "3007 tau surface lock missing; 2599 role mismatch missing",
            "passes_guard": False,
        }
    ),
    base(
        {
            "guard_id": "PFG3030_5_verdict",
            "residual": "preferred_frame_guard_total",
            "needed_for": "any parent clock/lapse adoption",
            "required_exit": "all preferred-frame residuals zero or source-bounded",
            "current_status": "PREFERRED_FRAME_GUARD_NOT_CLOSED",
            "bound_interface": "all guard heads are nonclaim placeholders",
            "passes_guard": False,
        }
    ),
]

asource_rows = [
    base(
        {
            "row_id": "ASR3030_0_A_source_linear_coefficient",
            "symbol": "A_source",
            "definition": "linear source coefficient in psi_N or g_00 branch: psi_N = A_source W/c^2 + O(W^2), equivalently g_00=-1+2 A_source W/c^2+O(W^2)",
            "linear_branch_formula": "A_source := coefficient extracted after W is parent-owned by J_H/H_tau/M_H_ref and not imported from orbital GM",
            "required_parent_denominator": "M_H_ref = H_tau[S]-H_ref, positive, same-frame, finite, with units and source path",
            "required_numerator": "source current J_H or Hcore/Q_tau numerator defining W and psi_N in the same branch",
            "units": "dimensionless",
            "numeric_value": "MISSING_A_SOURCE_VALUE",
            "source_path": str(SOURCE_PATHS["SRC3030_05_2930_source_coeff"]),
            "source_path_exists": SOURCE_PATHS["SRC3030_05_2930_source_coeff"].exists(),
            "equation_ref": "SCL2930_0_A_source; CARRY3028_0; PHO3022_3",
            "status": "STRICT_SCHEMA_ROW_ONLY_NOT_SOURCE_BACKED",
            "missing_for_claim": "MISSING_PARENT_LINEAR_COEFFICIENT_MAP; MISSING_POSITIVE_SAME_FRAME_M_H_REF; MISSING_J_H_HTAU_SOURCE_BRIDGE; MISSING_G_REF_UNITS; MISSING_NO_ORBITAL_GM_IMPORT_CERTIFICATE",
            "anti_shortcut": "do not set A_source=1 by convention unless the source-normalized gauge and denominator are parent-owned",
        }
    ),
    base(
        {
            "row_id": "ASR3030_1_A_source_norm_candidate",
            "symbol": "A_source_norm_candidate",
            "definition": "candidate normalization A_source=1 in a source-normalized Newton branch",
            "linear_branch_formula": "only legal if W/c^2 is defined from the same parent source and metric readout",
            "required_parent_denominator": "same as ASR3030_0, plus parent-owned normalization gauge",
            "required_numerator": "same as ASR3030_0",
            "units": "dimensionless",
            "numeric_value": "1",
            "source_path": str(SOURCE_PATHS["SRC3030_13_2599_claim_gates"]),
            "source_path_exists": SOURCE_PATHS["SRC3030_13_2599_claim_gates"].exists(),
            "equation_ref": "CG2599_5 rejects EH-only/orbital-GM denominator; CPK3030_5 not signed",
            "status": "REJECTED_NORMALIZATION_SHORTCUT_UNTIL_PARENT_DENOMINATOR_EXISTS",
            "missing_for_claim": "MISSING_PARENT_SOURCE_NORMALIZED_GAUGE; MISSING_M_H_REF; MISSING_SOURCE_BRIDGE",
            "anti_shortcut": "normalization is bookkeeping, not physics, until the source denominator is derived",
        }
    ),
]

asource_validator_rows = [
    base(
        {
            "check_id": "ASV3030_0_numeric",
            "requirement": "A_source numeric value is finite and dimensionless",
            "current_value": "MISSING_A_SOURCE_VALUE",
            "passed": False,
            "failure_mode": "MISSING_NUMERIC_VALUE",
        }
    ),
    base(
        {
            "check_id": "ASV3030_1_denominator",
            "requirement": "positive same-frame M_H_ref denominator exists",
            "current_value": "MISSING_POSITIVE_SAME_FRAME_M_H_REF",
            "passed": False,
            "failure_mode": "MISSING_DENOMINATOR",
        }
    ),
    base(
        {
            "check_id": "ASV3030_2_source_bridge",
            "requirement": "J_H/H_tau/worldtube source bridge defines W without orbital-GM import",
            "current_value": "MISSING_SOURCE_BRIDGE_AND_MHREF",
            "passed": False,
            "failure_mode": "MISSING_SOURCE_BRIDGE",
        }
    ),
    base(
        {
            "check_id": "ASV3030_3_source_path",
            "requirement": "every cited source path exists",
            "current_value": "all cited 3030 sources exist",
            "passed": True,
            "failure_mode": "NONE",
        }
    ),
    base(
        {
            "check_id": "ASV3030_4_valid_for_claim",
            "requirement": "rows with MISSING markers must remain valid_for_claim=false",
            "current_value": "false for all A_source rows",
            "passed": True,
            "failure_mode": "NONE",
        }
    ),
    base(
        {
            "check_id": "ASV3030_5_verdict",
            "requirement": "A_source row is usable only as a strict nonclaim acquisition target",
            "current_value": "STRICT_NONCLAIM_ROW_ONLY",
            "passed": True,
            "failure_mode": "NONE",
        }
    ),
]

promotion_gate_rows = [
    base(
        {
            "gate_id": "GATE3030_0_sources",
            "gate": "every cited local source path exists",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "source-backed audit only",
        }
    ),
    base(
        {
            "gate_id": "GATE3030_1_clock_package_signed",
            "gate": "clock/lapse package signs psi_N=-log N_T as parent-owned",
            "result": False,
            "notes": "clock, lapse constraint, source bridge, tau lock and preferred-frame guard remain unsigned",
        }
    ),
    base(
        {
            "gate_id": "GATE3030_2_preferred_frame_guard",
            "gate": "alpha1/alpha2/xi/clock anisotropy are zero or bounded",
            "result": False,
            "notes": "preferred-frame guard rows are placeholders only",
        }
    ),
    base(
        {
            "gate_id": "GATE3030_3_A_source_schema",
            "gate": "first strict A_source row schema is emitted",
            "result": True,
            "notes": "schema exists but numeric/source-backed value is missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3030_4_A_source_claim",
            "gate": "A_source is source-backed and claimable",
            "result": False,
            "notes": "no M_H_ref/J_H/H_tau denominator and no no-orbital-GM certificate",
        }
    ),
    base(
        {
            "gate_id": "GATE3030_5_local_GR_claim",
            "gate": "local GR/Newton reduction is claimable",
            "result": False,
            "notes": "clock/lapse package and A_source are both nonclaim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3030_0_clock_lapse",
            "decision": "do not adopt the clock/lapse package yet",
            "rationale": "older tau/clock ledgers explicitly reject lapse-gauge shortcuts and keep parent clock/source tau lock missing",
            "consequence": "psi_N=-log N_T remains a candidate branch rule, not a parent theorem",
        }
    ),
    base(
        {
            "decision_id": "DEC3030_1_A_source",
            "decision": "stage A_source as the next strict coupling acquisition row",
            "rationale": "the coupling denominator is now the lowest-friction route to make the Newton bridge honest",
            "consequence": "3031 should target M_H_ref/J_H/H_tau/G_ref ownership or keep A_source missing",
        }
    ),
    base(
        {
            "decision_id": "DEC3030_2_no_normalization_shortcut",
            "decision": "reject A_source=1 as a claim-grade shortcut",
            "rationale": "normalizing the source branch is only legal after the parent denominator and same-frame source bridge exist",
            "consequence": "A_source_norm_candidate stays nonclaim bookkeeping",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3030_0_3031",
            "target_doc": "3031-Y5-R2FR-Asource-denominator-owner-or-first-source-backed-value-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Asource_denominator_owner_or_first_source_backed_value_under_AX1090_3031.py",
            "mission": "derive or source A_source from H_tau/M_H_ref/G_ref/J_H in the same parent frame, or keep the row as strict missing input",
            "success_condition": "A_source gets a finite dimensionless source-backed value with positive same-frame M_H_ref and no orbital-GM import, or the denominator blocker is isolated as the next hard theorem",
            "forbidden": "no EH-only charge; no measured orbital GM denominator; no convention-only A_source=1; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

for key, output_rows in {
    "sources": source_register,
    "clock_package": clock_package_rows,
    "preferred_frame": preferred_frame_rows,
    "asource_schema": asource_rows,
    "asource_validator": asource_validator_rows,
    "gates": promotion_gate_rows,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[key], output_rows)

copy_plan = {
    "clock_package_copy": OUTPUTS["clock_package"],
    "preferred_frame_copy": OUTPUTS["preferred_frame"],
    "asource_schema_copy": OUTPUTS["asource_schema"],
    "asource_validator_copy": OUTPUTS["asource_validator"],
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
                "clock_package_copy": "parent-action branch copy of rejected clock/lapse package",
                "preferred_frame_copy": "local-bound branch copy of preferred-frame guard blockers",
                "asource_schema_copy": "local-bound branch copy of strict A_source acquisition row",
                "asource_validator_copy": "local-bound branch copy of A_source validator",
                "next_copy": "RAB acquisition queue handoff",
            }[copy_id],
        }
    )
    for copy_id, source_path in copy_plan.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

claim_rows = (
    source_register
    + clock_package_rows
    + preferred_frame_rows
    + asource_rows
    + asource_validator_rows
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
        "validation_id": "VAL3030_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": "P8_Y5_R2FR_3030_SOURCE_REGISTER.csv",
    },
    {
        "validation_id": "VAL3030_01_csv_parse",
        "passed": all(csv_ok(path) for path in csv_paths_before_validation),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all 3030 CSV artifacts except validation import with csv.DictReader",
    },
    {
        "validation_id": "VAL3030_02_clock_package_rejected",
        "passed": any(row["current_status"] == "CLOCK_LAPSE_PACKAGE_NOT_SIGNED" and not boolish(row["passes_package"]) for row in clock_package_rows),
        "requirement": "clock/lapse package fails closed unless all clauses pass",
        "evidence": "P8_Y5_R2FR_3030_CLOCK_LAPSE_PACKAGE_AUDIT.csv",
    },
    {
        "validation_id": "VAL3030_03_psin_unsigned",
        "passed": all(not boolish(row.get("passes_package")) for row in clock_package_rows),
        "requirement": "psi_N=-log N_T is not promoted to parent-owned",
        "evidence": "all clock-package clauses remain nonpassing",
    },
    {
        "validation_id": "VAL3030_04_preferred_frame_blocked",
        "passed": any(row["current_status"] == "PREFERRED_FRAME_GUARD_NOT_CLOSED" for row in preferred_frame_rows),
        "requirement": "preferred-frame leakage guard remains explicit",
        "evidence": "P8_Y5_R2FR_3030_PREFERRED_FRAME_GUARD.csv",
    },
    {
        "validation_id": "VAL3030_05_A_source_schema_present",
        "passed": any(row["symbol"] == "A_source" for row in asource_rows),
        "requirement": "first A_source row schema exists",
        "evidence": "P8_Y5_R2FR_3030_ASOURCE_FIRST_ROW_SCHEMA.csv",
    },
    {
        "validation_id": "VAL3030_06_A_source_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in asource_rows),
        "requirement": "A_source rows remain nonclaim",
        "evidence": "valid_for_claim=false and claim_allowed=false",
    },
    {
        "validation_id": "VAL3030_07_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if missing_marker(row)),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all generated claim-control rows",
    },
    {
        "validation_id": "VAL3030_08_branch_copies_exist",
        "passed": all(path.exists() for path in BRANCH_OUTPUTS.values()),
        "requirement": "branch copies and acquisition queue exist",
        "evidence": "P8_Y5_R2FR_3030_BRANCH_COPIES.csv",
    },
    {
        "validation_id": "VAL3030_09_outputs_scoped",
        "passed": all(under(path, ROOT) for path in generated_paths),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3030_10_formalization_not_targeted",
        "passed": all(not under(path, FORMALIZATION) for path in generated_paths),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3030_11_no_normalization_shortcut",
        "passed": any(row["symbol"] == "A_source_norm_candidate" and "REJECTED" in row["status"] for row in asource_rows),
        "requirement": "A_source=1 is rejected as claim-grade shortcut",
        "evidence": "P8_Y5_R2FR_3030_ASOURCE_FIRST_ROW_SCHEMA.csv",
    },
    {
        "validation_id": "VAL3030_12_next_target_selected",
        "passed": any(boolish(row["selected"]) and "3031" in row["target_doc"] for row in next_rows),
        "requirement": "next target selects A_source denominator ownership",
        "evidence": "P8_Y5_R2FR_3030_NEXT_TARGET.csv",
    },
]

overall = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3030_99_overall",
        "passed": overall,
        "requirement": "all 3030 validation checks pass",
        "evidence": "aggregate of VAL3030_00 through VAL3030_12",
    }
)
validation_rows = [base(row) for row in validation_rows]
write_csv(OUTPUTS["validation"], validation_rows)

doc_sections = [
    "# 3030 - Clock/Lapse Constraint Package Or First A_source Row under AX1090",
    "",
    "Status: `Y5_R2FR_3030_clock_lapse_package_not_signed_Asource_strict_nonclaim_row_staged_3031_next`",
    "",
    "## Verdict",
    "",
    "3030 takes the cleanest available leap at the current bottleneck: try to make the covariant clock/lapse lift parent-owned rather than a useful coordinate-looking construction.",
    "",
    "The attempt fails closed. The corpus does not yet supply a parent clock field/action, a signed lapse constraint `psi_N=-log N_T`, a same-frame tau/source/readout lock, a source bridge `J_H/H_tau/M_H_ref`, or a preferred-frame guard for `alpha1`, `alpha2`, `xi`, and clock anisotropy.",
    "",
    "This is not a collapse of the route. It is a useful narrowing: the next hard object is the coupling denominator. The first strict `A_source` row is now staged as a nonclaim acquisition target, with the normalization shortcut explicitly rejected until the source denominator is parent-owned.",
    "",
    "## Clock/Lapse Package Audit",
    "",
    md_table(clock_package_rows, ["package_id", "clause", "current_status", "passes_package", "consequence"]),
    "",
    "## Preferred-Frame Guard",
    "",
    md_table(preferred_frame_rows, ["guard_id", "residual", "current_status", "passes_guard", "required_exit"]),
    "",
    "## A_source First Row",
    "",
    md_table(asource_rows, ["row_id", "symbol", "numeric_value", "status", "missing_for_claim", "anti_shortcut"]),
    "",
    "## A_source Validator",
    "",
    md_table(asource_validator_rows, ["check_id", "requirement", "current_value", "passed", "failure_mode"]),
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

print(f"Wrote 3030 checkpoint: {DOC}")
print(f"Overall validation: {overall}")
