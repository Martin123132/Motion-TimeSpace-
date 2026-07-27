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

CHECKPOINT = "3029"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3029-Y5-R2FR-covariant-LHcore-lift-or-first-Cbeta-component-value-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3029_00_3028_doc": ROOT / "3028-Y5-R2FR-parent-LHcore-density-adoption-test-or-Cbeta-component-values-under-AX1090.md",
    "SRC3029_01_3028_candidate": RESIDUALS / "P8_Y5_R2FR_3028_LHCORE_DENSITY_ADOPTION_CANDIDATE.csv",
    "SRC3029_02_3028_audit": RESIDUALS / "P8_Y5_R2FR_3028_ADOPTION_CLAUSE_AUDIT.csv",
    "SRC3029_03_3028_variation": RESIDUALS / "P8_Y5_R2FR_3028_CONDITIONAL_VARIATION_TEST.csv",
    "SRC3029_04_3028_residual": RESIDUALS / "P8_Y5_R2FR_3028_AUGMENTED_CBETACORE_RESIDUAL_LAW.csv",
    "SRC3029_05_3028_carry": RESIDUALS / "P8_Y5_R2FR_3028_COMPONENT_FILL_CARRYFORWARD.csv",
    "SRC3029_06_3028_next": RESIDUALS / "P8_Y5_R2FR_3028_NEXT_TARGET.csv",
    "SRC3029_07_3027_components": RESIDUALS / "P8_Y5_R2FR_3027_CBETACORE_COMPONENT_FILL_ROWS.csv",
    "SRC3029_08_3026_contract": RESIDUALS / "P8_Y5_R2FR_3026_SIGMAH_FPSI_EXTRACTION_CONTRACT.csv",
    "SRC3029_09_3006_current_chain": RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv",
    "SRC3029_10_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3029_11_2924_reduction": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3029_SOURCE_REGISTER.csv",
    "lift": RESIDUALS / "P8_Y5_R2FR_3029_COVARIANT_LHCORE_LIFT_CANDIDATE.csv",
    "clauses": RESIDUALS / "P8_Y5_R2FR_3029_COVARIANT_LIFT_CLAUSE_AUDIT.csv",
    "reduction": RESIDUALS / "P8_Y5_R2FR_3029_STATIC_REDUCTION_MAP.csv",
    "component": RESIDUALS / "P8_Y5_R2FR_3029_FIRST_COMPONENT_VALUE_ATTEMPT.csv",
    "risks": RESIDUALS / "P8_Y5_R2FR_3029_CLOCK_LIFT_RISK_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3029_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3029_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3029_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3029_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3029_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lift_copy": PARENT_ACTION / "covariant_LHcore_clock_lift_candidate_3029_REJECTED_NONCLAIM.csv",
    "clauses_copy": PARENT_ACTION / "covariant_LHcore_lift_clause_audit_3029_REJECTED.csv",
    "component_copy": LOCAL_BOUNDS / "first_Cbeta_component_value_attempt_3029_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3029_CLOCK_LIFT_CLAUSES_OR_FIRST_COMPONENT_SOURCE_NEXT_NONCLAIM.csv",
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
    "SRC3029_00_3028_doc": "3028 handoff: static density useful but not adopted",
    "SRC3029_01_3028_candidate": "L_Hcore^N candidate density",
    "SRC3029_02_3028_audit": "adoption clause audit",
    "SRC3029_03_3028_variation": "conditional variation test",
    "SRC3029_04_3028_residual": "augmented C_beta residual law",
    "SRC3029_05_3028_carry": "component carry-forward",
    "SRC3029_06_3028_next": "machine-readable 3029 target",
    "SRC3029_07_3027_components": "C_beta component fill rows",
    "SRC3029_08_3026_contract": "sigma_H/f_psi extraction contract",
    "SRC3029_09_3006_current_chain": "current-chain parent action blockers",
    "SRC3029_10_3007_grammar": "parent action grammar",
    "SRC3029_11_2924_reduction": "MTS-to-EH reduction blockers",
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

lift_rows = [
    base(
        {
            "lift_id": "LIFT3029_0_clock_foliation_candidate",
            "covariant_density": "L_cov^N = -C_N/2 sqrt(-g) K_N(psi_N,U,Z) h_T^{mu nu} nabla_mu psi_N nabla_nu psi_N + sqrt(-g) J_H psi_N + L_constraints + L_boundary",
            "clock_structure": "T scalar clock; n_mu=-N_T nabla_mu T; N_T=(-g^{ab}nabla_a T nabla_b T)^(-1/2); h_T^{mu nu}=g^{mu nu}+n^mu n^nu",
            "lapse_link": "constraint C_Nlap enforces psi_N=-log N_T on the local branch",
            "static_target": "T=t, shift=0, h_T^{ij}=hbar^{ij}, U=u=W/c^2 gives the 3028 static density",
            "status": "COVARIANT_LIFT_CANDIDATE_NOT_ADOPTED",
        }
    )
]

clause_rows = [
    base(
        {
            "clause_id": "CLIFT3029_0_scalar_clock",
            "clause": "clock/foliation field is a parent MTS primitive or constrained auxiliary",
            "required_evidence": "T or tau_source in parent field list, variation status, constraint class and gauge fixing",
            "current_status": "MISSING_PARENT_CLOCK_FIELD_ADOPTION",
            "passes_lift": False,
            "why": "otherwise the lift adds a preferred foliation by hand",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_1_lapse_constraint",
            "clause": "psi_N=-log N_T is enforced by a parent constraint",
            "required_evidence": "C_Nlap multiplier, constraint variation and no extra propagating lapse mode",
            "current_status": "MISSING_LAPSE_CONSTRAINT",
            "passes_lift": False,
            "why": "psi_N owner remains unsigned",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_2_U_source_scalar",
            "clause": "U=u=W/c^2 is parent-owned before static reduction",
            "required_evidence": "source potential or constrained scalar tied to J_H/M_H_ref without orbital-GM import",
            "current_status": "MISSING_SOURCE_POTENTIAL_OWNER",
            "passes_lift": False,
            "why": "U cannot be inserted as a fitted Newtonian potential",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_3_source_current",
            "clause": "J_H is the same Hilbert/Hamiltonian/worldtube source",
            "required_evidence": "matter descent, Ward/source support, H_tau/M_H_ref and exterior silence",
            "current_status": "MISSING_SOURCE_BRIDGE_AND_MHREF",
            "passes_lift": False,
            "why": "source term controls A_source and can fake the Newton bridge",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_4_static_reduction",
            "clause": "covariant lift reduces to the 3028 static density",
            "required_evidence": "T=t branch, fixed shift/lapse convention, boundary class and h_T^{ij}=hbar^{ij}",
            "current_status": "CONDITIONAL_REDUCTION_MAP_WRITTEN",
            "passes_lift": False,
            "why": "map is algebraic but parent branch rule is not signed",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_5_first_variation",
            "clause": "variation includes metric, clock, psi_N, source and boundary pieces",
            "required_evidence": "E_psi, E_T, E_g, theta_Hcore and constraint terms",
            "current_status": "PARTIAL_FORMAL_VARIATION_ONLY",
            "passes_lift": False,
            "why": "clock and constraint variations introduce new equations and currents",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_6_preferred_frame",
            "clause": "clock lift does not generate alpha1/alpha2/xi leakage",
            "required_evidence": "preferred-frame residual zero theorem or numeric bounds",
            "current_status": "MISSING_PREFERRED_FRAME_GUARD",
            "passes_lift": False,
            "why": "a foliation can repair lapse while breaking PPN elsewhere",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_7_component_values",
            "clause": "A_source, K0, sigma_H, f_psi, K_TF and C_beta are filled or theorem-zero",
            "required_evidence": "component rows with units, source paths and gate policy",
            "current_status": "MISSING_COMPONENT_VALUES",
            "passes_lift": False,
            "why": "no beta score without coefficient values",
        }
    ),
    base(
        {
            "clause_id": "CLIFT3029_8_verdict",
            "clause": "covariant L_Hcore^N lift adopted",
            "required_evidence": "CLIFT3029_0 through CLIFT3029_7 pass together",
            "current_status": "COVARIANT_LIFT_REJECTED_CURRENTLY",
            "passes_lift": False,
            "why": "the lift is a coherent candidate, not a parent-signed theory block",
        }
    ),
]

reduction_rows = [
    base(
        {
            "map_id": "REDUCE3029_0_clock_gauge",
            "covariant_object": "T scalar clock and projector h_T^{mu nu}",
            "static_branch": "T=t, n_mu=-N dt, h_T^{ij}=hbar^{ij}",
            "gives_static_object": "sqrt(-g) h_T^{ij} -> N sqrt(hbar) hbar^{ij}; with local N factor absorbed into K_N convention through O(u)",
            "status": "CONDITIONAL_MAP_NOT_PARENT_SIGNED",
        }
    ),
    base(
        {
            "map_id": "REDUCE3029_1_lapse",
            "covariant_object": "constraint psi_N=-log N_T",
            "static_branch": "N_T=N",
            "gives_static_object": "psi_N=-log N",
            "status": "MISSING_CONSTRAINT_SOURCE",
        }
    ),
    base(
        {
            "map_id": "REDUCE3029_2_source_free",
            "covariant_object": "J_H and boundary/source support",
            "static_branch": "J_H=0 outside compact source and boundary fixed",
            "gives_static_object": "exterior Euler equation used in 3028",
            "status": "MISSING_SOURCE_SILENCE_AND_BOUNDARY_PROOF",
        }
    ),
]

component_rows = [
    base(
        {
            "component_id": "CVAL3029_0_K0_normalization",
            "symbol": "K0_norm",
            "attempted_value": "1",
            "derivation": "if K0 is positive, finite and branch-constant, absorb K0 into C_N and use K_tr/K0 for sigma_H/f_psi extraction",
            "status": "NORMALIZATION_CONVENTION_CONDITIONAL_NOT_SOURCED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "missing_for_claim": "MISSING_PARENT_K0_POSITIVITY_AND_CONSTANCY; MISSING_C_N_NORMALIZATION_SOURCE",
        }
    ),
    base(
        {
            "component_id": "CVAL3029_1_first_physical_value",
            "symbol": "A_source_or_sigma_H_or_f_psi",
            "attempted_value": "MISSING",
            "derivation": "no physical C_beta component has a source-backed numeric value in current corpus",
            "status": "NO_SOURCE_BACKED_COMPONENT_VALUE_FOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "missing_for_claim": "MISSING_PARENT_SOURCE_PATH_AND_UNITS",
        }
    ),
]

risk_rows = [
    base(
        {
            "risk_id": "RISK3029_0_preferred_frame",
            "risk": "clock/foliation lift creates preferred-frame degrees of freedom",
            "affected_tests": "PPN alpha1; PPN alpha2; xi; clock/readout anisotropy",
            "required_control": "zero theorem or finite residual rows before any local-GR claim",
            "status": "ACTIVE_RISK",
        }
    ),
    base(
        {
            "risk_id": "RISK3029_1_source_potential",
            "risk": "U=W/c^2 is inserted rather than derived",
            "affected_tests": "Newton bridge; beta denominator; R10 radial/source hair",
            "required_control": "source potential owner tied to J_H/M_H_ref without measured-GM absorption",
            "status": "ACTIVE_RISK",
        }
    ),
    base(
        {
            "risk_id": "RISK3029_2_constraint_stress",
            "risk": "lapse/clock constraints add stress or boundary charge",
            "affected_tests": "beta; gamma; alpha3; source mass",
            "required_control": "constraint stress and theta/Q_tau pieces zero, exact, or bounded",
            "status": "ACTIVE_RISK",
        }
    ),
]

gate_rows = [
    base({"gate_id": "GATE3029_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed lift audit"}),
    base({"gate_id": "GATE3029_1_lift_written", "gate": "covariant clock-lift candidate is explicit", "result": True, "notes": "candidate density and static map emitted"}),
    base({"gate_id": "GATE3029_2_static_reduction", "gate": "static reduction map is algebraically written", "result": True, "notes": "conditional map only"}),
    base({"gate_id": "GATE3029_3_parent_adoption", "gate": "clock lift adopted as parent MTS action", "result": False, "notes": "clock, lapse constraint, source and preferred-frame clauses unsigned"}),
    base({"gate_id": "GATE3029_4_K0_norm", "gate": "K0 normalization convention staged", "result": True, "notes": "not a physical sourced component value"}),
    base({"gate_id": "GATE3029_5_physical_component_value", "gate": "first physical C_beta component value is source-backed", "result": False, "notes": "no sourced A_source/sigma_H/f_psi/K_TF value found"}),
    base({"gate_id": "GATE3029_6_local_GR_claim", "gate": "local GR/Newton reduction claimable", "result": False, "notes": "covariant lift rejected and component values missing"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3029_0_lift",
            "decision": "reject current covariant lift adoption",
            "rationale": "clock lift is coherent but imports unsigned clock/lapse/source/preferred-frame structure",
            "consequence": "do not claim parent L_Hcore^N or beta closure",
        }
    ),
    base(
        {
            "decision_id": "DEC3029_1_K0",
            "decision": "stage K0=1 only as a normalization convention",
            "rationale": "K0 can be absorbed into C_N if positive and constant, but that premise is not parent-signed",
            "consequence": "K0_norm helps bookkeeping but is not a physical claim row",
        }
    ),
    base(
        {
            "decision_id": "DEC3029_2_next",
            "decision": "target clock-lift clauses or first physical component source",
            "rationale": "the fork is now clean: either adopt the clock/lapse machinery or stop and source a real coefficient",
            "consequence": "3030 should try to sign the clock/lapse constraint package or fill A_source first",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3029_0_3030",
            "target_doc": "3030-Y5-R2FR-clock-lapse-constraint-package-or-first-Asource-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_clock_lapse_constraint_package_or_first_Asource_row_under_AX1090_3030.py",
            "mission": "try to source the clock/lapse constraint package that would make psi_N parent-owned; if it cannot be sourced, fill the first A_source row from the Hcore/source denominator route as strict nonclaim input",
            "success_condition": "either psi_N=-log N_T becomes parent-owned with clock/preferred-frame guards, or A_source gets a source-backed nonclaim row with units and no orbital-GM import",
            "forbidden": "no EH/GR import as MTS proof; no clock lift without preferred-frame guards; no fitted Newtonian U insertion; no orbital-GM denominator; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["lift"], lift_rows)
write_csv(OUTPUTS["clauses"], clause_rows)
write_csv(OUTPUTS["reduction"], reduction_rows)
write_csv(OUTPUTS["component"], component_rows)
write_csv(OUTPUTS["risks"], risk_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_rows = []
for key, source_key in [
    ("lift_copy", "lift"),
    ("clauses_copy", "clauses"),
    ("component_copy", "component"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3029_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = source_register + lift_rows + clause_rows + reduction_rows + component_rows + risk_rows + gate_rows + decision_rows + next_rows

validation_rows = [
    {"validation_id": "VAL3029_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3029_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3029_02_lift_candidate", "passed": any(row["lift_id"] == "LIFT3029_0_clock_foliation_candidate" for row in lift_rows), "requirement": "covariant lift candidate is recorded", "evidence": OUTPUTS["lift"].name},
    {"validation_id": "VAL3029_03_lift_rejected", "passed": any(row["clause_id"] == "CLIFT3029_8_verdict" and row["current_status"] == "COVARIANT_LIFT_REJECTED_CURRENTLY" for row in clause_rows), "requirement": "covariant lift fails closed", "evidence": OUTPUTS["clauses"].name},
    {"validation_id": "VAL3029_04_static_map", "passed": any(row["map_id"] == "REDUCE3029_0_clock_gauge" for row in reduction_rows), "requirement": "static reduction map exists", "evidence": OUTPUTS["reduction"].name},
    {"validation_id": "VAL3029_05_K0_nonclaim", "passed": any(row["component_id"] == "CVAL3029_0_K0_normalization" and not boolish(row["valid_for_claim"]) for row in component_rows), "requirement": "K0 normalization is explicitly nonclaim", "evidence": OUTPUTS["component"].name},
    {"validation_id": "VAL3029_06_risks_present", "passed": any(row["risk_id"] == "RISK3029_0_preferred_frame" for row in risk_rows), "requirement": "clock-lift preferred-frame risk is recorded", "evidence": OUTPUTS["risks"].name},
    {"validation_id": "VAL3029_07_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3029 generated ledgers"},
    {"validation_id": "VAL3029_08_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3029 generated ledgers"},
    {"validation_id": "VAL3029_09_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3029_10_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3029_11_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3029_12_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3030-Y5-R2FR-clock-lapse-constraint"), "requirement": "next target selects clock-lapse package or first A_source row", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3029_99_overall",
        "passed": overall_pass,
        "requirement": "all 3029 validation checks pass",
        "evidence": "aggregate of VAL3029_00 through VAL3029_12",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3029 - Covariant LHcore Lift Or First Cbeta Component Value under AX1090

Status: `Y5_R2FR_3029_clock_lift_candidate_rejected_K0_normalization_nonclaim_3030_next`

## Verdict

3029 tries the natural covariant lift of the static log-lapse density: introduce a parent clock/foliation scalar `T`, define a unit normal/projector, and link

`psi_N = -log N_T`

by constraint.

This is the right kind of lift if the theory wants the lapse/log-lapse branch to be parent-owned rather than a coordinate trick.

But it does **not** close yet. The clock field, lapse constraint, source potential `U`, source current `J_H`, preferred-frame guards, and component values are all unsigned.

So the lift is retained as a serious candidate, but rejected as a current claim.

The only component progress is bookkeeping: if `K0` is positive, finite, and branch-constant, it can be normalized to `K0=1` by absorbing it into `C_N`. That is useful, but it is not a sourced physical component value.

## Covariant Lift Candidate

{md_table(lift_rows, ["lift_id", "covariant_density", "clock_structure", "lapse_link", "static_target", "status"])}

## Covariant Lift Clause Audit

{md_table(clause_rows, ["clause_id", "clause", "current_status", "passes_lift", "why"])}

## Static Reduction Map

{md_table(reduction_rows, ["map_id", "covariant_object", "static_branch", "gives_static_object", "status"])}

## First Component Value Attempt

{md_table(component_rows, ["component_id", "symbol", "attempted_value", "derivation", "status", "valid_for_claim", "missing_for_claim"])}

## Clock Lift Risk Ledger

{md_table(risk_rows, ["risk_id", "risk", "affected_tests", "required_control", "status"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Promotion Gates

{md_table(gate_rows, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_rows, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["lift"]}`
- `{OUTPUTS["clauses"]}`
- `{OUTPUTS["reduction"]}`
- `{OUTPUTS["component"]}`
- `{OUTPUTS["risks"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["lift_copy"]}`
- `{BRANCH_OUTPUTS["clauses_copy"]}`
- `{BRANCH_OUTPUTS["component_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass from a clock lift until preferred-frame, source, lapse-constraint and boundary clauses are parent-signed or bounded.
- No physical component value claim from `K0=1`; it is a conditional normalization convention only.
- No fitted Newtonian `U` insertion.
- No EH/GR import as MTS proof.
- No reciprocal `R_AB` density substitution for log-lapse `psi_N`.
- No orbital-`GM` denominator.
- No local-GR/Newton claim from this lift alone.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
