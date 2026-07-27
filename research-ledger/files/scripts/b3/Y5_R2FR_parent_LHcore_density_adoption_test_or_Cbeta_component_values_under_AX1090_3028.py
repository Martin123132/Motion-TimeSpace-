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

CHECKPOINT = "3028"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5

DOC = ROOT / "3028-Y5-R2FR-parent-LHcore-density-adoption-test-or-Cbeta-component-values-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3028_00_3027_doc": ROOT / "3027-Y5-R2FR-Hcore-kinetic-density-source-or-Cbeta-core-component-fill-under-AX1090.md",
    "SRC3028_01_3027_hunt": RESIDUALS / "P8_Y5_R2FR_3027_HCORE_KINETIC_DENSITY_SOURCE_HUNT.csv",
    "SRC3028_02_3027_candidate": RESIDUALS / "P8_Y5_R2FR_3027_PARAMETERIZED_KSCR_SOURCE_ROW_TEMPLATE.csv",
    "SRC3028_03_3027_components": RESIDUALS / "P8_Y5_R2FR_3027_CBETACORE_COMPONENT_FILL_ROWS.csv",
    "SRC3028_04_3027_validator": RESIDUALS / "P8_Y5_R2FR_3027_COMPONENT_ROW_VALIDATOR.csv",
    "SRC3028_05_3027_anisotropy": RESIDUALS / "P8_Y5_R2FR_3027_ANISOTROPIC_AND_CROSS_TERM_FILL_ROWS.csv",
    "SRC3028_06_3027_next": RESIDUALS / "P8_Y5_R2FR_3027_NEXT_TARGET.csv",
    "SRC3028_07_3026_contract": RESIDUALS / "P8_Y5_R2FR_3026_SIGMAH_FPSI_EXTRACTION_CONTRACT.csv",
    "SRC3028_08_3026_derivation": RESIDUALS / "P8_Y5_R2FR_3026_EXTRACTION_TO_LAMBDAN_DERIVATION.csv",
    "SRC3028_09_3025_bounds": RESIDUALS / "P8_Y5_R2FR_3025_C_BETA_CORE_BOUND_ROWS.csv",
    "SRC3028_10_3006_current_chain": RESIDUALS / "P8_Y5_R2FR_3006_PARENT_CURRENT_CHAIN_AUDIT.csv",
    "SRC3028_11_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3028_12_2923_hcore_checklist": RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3028_SOURCE_REGISTER.csv",
    "candidate": RESIDUALS / "P8_Y5_R2FR_3028_LHCORE_DENSITY_ADOPTION_CANDIDATE.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3028_ADOPTION_CLAUSE_AUDIT.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_3028_CONDITIONAL_VARIATION_TEST.csv",
    "residual_law": RESIDUALS / "P8_Y5_R2FR_3028_AUGMENTED_CBETACORE_RESIDUAL_LAW.csv",
    "carry": RESIDUALS / "P8_Y5_R2FR_3028_COMPONENT_FILL_CARRYFORWARD.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3028_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3028_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3028_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3028_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3028_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "candidate_copy": PARENT_ACTION / "LHcore_density_adoption_candidate_3028_REJECTED_NONCLAIM.csv",
    "audit_copy": PARENT_ACTION / "LHcore_density_adoption_clause_audit_3028_REJECTED.csv",
    "carry_copy": LOCAL_BOUNDS / "Cbeta_component_fill_carryforward_3028_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3028_COVARIANT_LHCORE_PARENT_OR_COMPONENT_VALUES_NEXT_NONCLAIM.csv",
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
    "SRC3028_00_3027_doc": "3027 handoff: Kscr source not found; component rows staged",
    "SRC3028_01_3027_hunt": "Hcore kinetic density source hunt",
    "SRC3028_02_3027_candidate": "parameterized Kscr template",
    "SRC3028_03_3027_components": "C_beta_core component fill rows",
    "SRC3028_04_3027_validator": "component validator",
    "SRC3028_05_3027_anisotropy": "anisotropic/cross-term rows",
    "SRC3028_06_3027_next": "machine-readable 3028 target",
    "SRC3028_07_3026_contract": "sigma_H/f_psi extraction contract",
    "SRC3028_08_3026_derivation": "extraction-to-lambda_N derivation",
    "SRC3028_09_3025_bounds": "C_beta_core bound rows",
    "SRC3028_10_3006_current_chain": "parent current-chain blocker audit",
    "SRC3028_11_3007_grammar": "minimal parent action grammar",
    "SRC3028_12_2923_hcore_checklist": "Hcore/Q_tau coefficient checklist",
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

candidate_rows = [
    base(
        {
            "candidate_id": "LHC3028_0_minimal_density",
            "density": "L_Hcore^N = -C_N/2 sqrt(hbar) K0[(1+sigma_H u+f_psi psi_N) hbar^{ij}+K_TF^{ij}] D_i psi_N D_j psi_N + sqrt(hbar) J_H psi_N + L_boundary",
            "field_list": "psi_N,u=W/c^2,hbar_ij/e_obs,Pi_M,Z,J_H,K_TF^{ij},boundary/reference,tau/source frame",
            "derivative_order": "quadratic first spatial derivatives of psi_N; second-order elliptic Euler equation in static exterior",
            "what_it_can_do": "if adopted, it supplies Kscr_N^{ij}, K0, sigma_H, f_psi and anisotropy rows by differentiation",
            "current_status": "CANDIDATE_ACTION_BLOCK_NOT_ADOPTED",
        }
    )
]

audit_rows = [
    base(
        {
            "clause_id": "ADOPT3028_0_field_list",
            "clause": "all retained fields and held-fixed variables are declared",
            "required_evidence": "psi_N, u, e_obs/hbar, Pi_M, Z, J_H, boundary/reference, tau/frame listed with variation status",
            "current_status": "PARTIAL_TEMPLATE_ONLY",
            "passes_adoption": False,
            "reason": "template lists fields but does not parent-sign which are varied, constrained, or fixed",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_1_covariant_parent",
            "clause": "static density descends from a diffeomorphism-covariant parent action",
            "required_evidence": "4D parent scalar density, gauge fixing/static reduction, and constraint algebra",
            "current_status": "MISSING_COVARIANT_PARENT_DENSITY",
            "passes_adoption": False,
            "reason": "3+1/static template alone is not a parent MTS action",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_2_psiN_owner",
            "clause": "psi_N=-log N is a parent-owned field/readout",
            "required_evidence": "variation or constraint links psi_N, lapse N and observed metric readout before PPN comparison",
            "current_status": "MISSING_PSI_N_PARENT_OWNER",
            "passes_adoption": False,
            "reason": "3022/3023 owner audits still fail",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_3_source_term",
            "clause": "J_H is the same observed Hilbert/Hamiltonian source current",
            "required_evidence": "J_H source descent, worldtube support, exterior silence, M_H_ref denominator and no orbital-GM import",
            "current_status": "MISSING_SOURCE_BRIDGE_AND_MHREF",
            "passes_adoption": False,
            "reason": "source term can fake A_source unless same-frame denominator is owned",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_4_boundary_reference",
            "clause": "boundary/reference fixed before readout",
            "required_evidence": "L_boundary variation, fixed reference class, no fitted subtraction and no exterior boundary source",
            "current_status": "MISSING_FIXED_BOUNDARY_REFERENCE",
            "passes_adoption": False,
            "reason": "boundary term can shift source mass and beta coefficients",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_5_variation",
            "clause": "Euler variation is computable",
            "required_evidence": "delta L gives E_psi delta psi + d theta with explicit surface term",
            "current_status": "CONDITIONAL_VARIATION_COMPUTABLE",
            "passes_adoption": False,
            "reason": "variation works for the template but theta/Q_tau ownership remains non-parent",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_6_coefficients",
            "clause": "K0, A_source, sigma_H and f_psi are values or theorem-zero",
            "required_evidence": "component rows filled with source paths and units",
            "current_status": "MISSING_COMPONENT_VALUES",
            "passes_adoption": False,
            "reason": "3027 component rows are explicit but unfilled",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_7_anisotropy",
            "clause": "K_TF and cross/silent terms are zero or bounded",
            "required_evidence": "trace-free kinetic tensor and silent-field cross terms pass zero/bound rows",
            "current_status": "MISSING_ANISOTROPIC_AND_CROSS_TERM_GUARDS",
            "passes_adoption": False,
            "reason": "scalar beta trace cannot hide preferred-frame or memory leakage",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_8_no_shortcuts",
            "clause": "no EH/GR import and no reciprocal R_AB substitution",
            "required_evidence": "MTS parent L_Hcore^N source, not comparator or foreign-field density",
            "current_status": "GUARD_PASSES",
            "passes_adoption": True,
            "reason": "shortcuts are explicitly rejected, but rejection does not prove adoption",
        }
    ),
    base(
        {
            "clause_id": "ADOPT3028_9_verdict",
            "clause": "adopt L_Hcore^N as parent action block",
            "required_evidence": "ADOPT3028_0 through ADOPT3028_8 close together",
            "current_status": "ADOPTION_REJECTED_CURRENTLY",
            "passes_adoption": False,
            "reason": "candidate is useful but not parent-signed",
        }
    ),
]

variation_rows = [
    base(
        {
            "variation_id": "VAR3028_0_template_variation",
            "statement": "conditional variation of the template density gives an exterior Euler equation",
            "formula": "D_i(sqrt(hbar) Kscr_N^{ij} D_j psi_N) - 1/2 sqrt(hbar) partial_{psi_N}Kscr_N^{ij} D_i psi_N D_j psi_N + sqrt(hbar) J_H + boundary_source = 0",
            "status": "CONDITIONAL_DERIVATION",
            "claim_effect": "shows mathematical coherence of the ansatz, not parent adoption",
        }
    ),
    base(
        {
            "variation_id": "VAR3028_1_local_exterior",
            "statement": "with J_H=0, fixed boundary, isotropic trace and harmonic u, the known coefficient law follows",
            "formula": "2 lambda_N_core + sigma_H A_source + (f_psi/2)A_source^2 + R_aniso + R_boundary + R_source + R_gauge = 0",
            "status": "AUGMENTED_COEFFICIENT_LAW",
            "claim_effect": "keeps every unowned piece as an explicit residual",
        }
    ),
    base(
        {
            "variation_id": "VAR3028_2_theta",
            "statement": "surface variation would define a theta_Hcore contribution",
            "formula": "theta_Hcore^i = -C_N sqrt(hbar) Kscr_N^{ij} D_j psi_N delta psi_N + boundary/corner terms",
            "status": "FORMAL_THETA_ONLY",
            "claim_effect": "not enough for Q_tau^MTS or H_tau without parent current chain",
        }
    ),
]

residual_law_rows = [
    base(
        {
            "law_id": "LAW3028_0_augmented_Cbeta",
            "symbol": "C_beta_core_aug",
            "formula": "C_beta_core_aug = sigma_H/(2 A_source)+f_psi/4 + C_aniso + C_boundary + C_source + C_gauge",
            "bound": f"abs(C_beta_core_aug) <= {BETA_BOUND_ABS}",
            "status": "NOT_SCORE_READY",
            "needed_for_score": "all components source-backed or theorem-zero; no fitted cancellation",
        }
    ),
    base(
        {
            "law_id": "LAW3028_1_identity_route",
            "symbol": "zero identity",
            "formula": "2 sigma_H/A_source + f_psi = 0 plus C_aniso=C_boundary=C_source=C_gauge=0",
            "bound": "theorem-zero route",
            "status": "NOT_PARENT_DERIVED",
            "needed_for_score": "identity from parent L_Hcore^N and zero/bound guards",
        }
    ),
]

carry_rows = []
for row in rows(SOURCE_PATHS["SRC3028_03_3027_components"]):
    carry_rows.append(
        base(
            {
                "carry_id": f"CARRY3028_{len(carry_rows)}",
                "source_component_id": row.get("component_id", ""),
                "symbol": row.get("symbol", ""),
                "carried_status": row.get("value_status", "MISSING"),
                "required_source": row.get("required_source", ""),
                "bound_or_gate": row.get("bound_or_gate", ""),
                "source_path": row.get("source_path", "MISSING_PARENT_SOURCE"),
            }
        )
    )

if not carry_rows:
    carry_rows = [
        base(
            {
                "carry_id": "CARRY3028_0_missing_component_source",
                "source_component_id": "MISSING_3027_COMPONENT_FILE",
                "symbol": "C_beta_core",
                "carried_status": "MISSING_COMPONENT_LEDGER",
                "required_source": "3027 component fill rows",
                "bound_or_gate": f"abs(C_beta_core)<={BETA_BOUND_ABS}",
                "source_path": "MISSING_PARENT_SOURCE",
            }
        )
    ]

gate_rows = [
    base({"gate_id": "GATE3028_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed adoption audit"}),
    base({"gate_id": "GATE3028_1_candidate_written", "gate": "candidate L_Hcore^N density is explicit", "result": True, "notes": "density template and field list emitted"}),
    base({"gate_id": "GATE3028_2_variation_computable", "gate": "conditional Euler variation is computable", "result": True, "notes": "template produces E_psi and theta_Hcore shape"}),
    base({"gate_id": "GATE3028_3_covariant_parent", "gate": "candidate descends from covariant parent action", "result": False, "notes": "missing 4D parent density/static reduction/constraint algebra"}),
    base({"gate_id": "GATE3028_4_source_boundary", "gate": "source and boundary clauses parent-signed", "result": False, "notes": "J_H/M_H_ref/boundary reference remain unsigned"}),
    base({"gate_id": "GATE3028_5_components", "gate": "K0, A_source, sigma_H, f_psi and anisotropy filled", "result": False, "notes": "component rows remain missing/nonclaim"}),
    base({"gate_id": "GATE3028_6_adoption", "gate": "L_Hcore^N adopted as parent action block", "result": False, "notes": "adoption rejected currently"}),
    base({"gate_id": "GATE3028_7_local_GR_claim", "gate": "local GR/Newton reduction claimable", "result": False, "notes": "parent action, source, beta/gamma, anisotropy and current gates remain open"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3028_0_adoption",
            "decision": "reject current adoption of L_Hcore^N",
            "rationale": "the template is variationally useful but lacks parent covariant source, source bridge, boundary reference and filled coefficients",
            "consequence": "no beta/local-GR claim",
        }
    ),
    base(
        {
            "decision_id": "DEC3028_1_retain",
            "decision": "retain the density as a test ansatz and component source template",
            "rationale": "it gives a precise way to compute sigma_H/f_psi once a real parent density exists",
            "consequence": "future work can fill values or attempt a covariant parent lift",
        }
    ),
    base(
        {
            "decision_id": "DEC3028_2_next",
            "decision": "attempt covariant parent lift or finite component values",
            "rationale": "the next leap must supply 4D parent provenance or stop pretending the template can self-adopt",
            "consequence": "3029 should test covariant lift clauses or fill the first component value",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3028_0_3029",
            "target_doc": "3029-Y5-R2FR-covariant-LHcore-lift-or-first-Cbeta-component-value-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_covariant_LHcore_lift_or_first_Cbeta_component_value_under_AX1090_3029.py",
            "mission": "try to lift L_Hcore^N to a covariant parent density with static reduction, source and boundary clauses; if that fails, fill the first sourced component value among A_source, K0, sigma_H, f_psi or anisotropic leakage",
            "success_condition": "either the covariant parent lift passes source-ready adoption clauses, or one component row becomes source-backed/nonclaim with units and gate policy",
            "forbidden": "no EH/GR import as MTS proof; no reciprocal R_AB substitution; no flat-coframe assumption without source; no fitted cancellation; no orbital-GM denominator; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["candidate"], candidate_rows)
write_csv(OUTPUTS["audit"], audit_rows)
write_csv(OUTPUTS["variation"], variation_rows)
write_csv(OUTPUTS["residual_law"], residual_law_rows)
write_csv(OUTPUTS["carry"], carry_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_rows = []
for key, source_key in [
    ("candidate_copy", "candidate"),
    ("audit_copy", "audit"),
    ("carry_copy", "carry"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3028_{len(branch_rows)}",
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
claim_rows = source_register + candidate_rows + audit_rows + variation_rows + residual_law_rows + carry_rows + gate_rows + decision_rows + next_rows

validation_rows = [
    {"validation_id": "VAL3028_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3028_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3028_02_candidate_present", "passed": any(row["candidate_id"] == "LHC3028_0_minimal_density" for row in candidate_rows), "requirement": "candidate L_Hcore density is recorded", "evidence": OUTPUTS["candidate"].name},
    {"validation_id": "VAL3028_03_adoption_rejected", "passed": any(row["clause_id"] == "ADOPT3028_9_verdict" and row["current_status"] == "ADOPTION_REJECTED_CURRENTLY" for row in audit_rows), "requirement": "adoption fails closed", "evidence": OUTPUTS["audit"].name},
    {"validation_id": "VAL3028_04_variation_formula", "passed": any(row["variation_id"] == "VAR3028_1_local_exterior" and "R_aniso" in row["formula"] for row in variation_rows), "requirement": "conditional variation records residual-augmented coefficient law", "evidence": OUTPUTS["variation"].name},
    {"validation_id": "VAL3028_05_components_carried", "passed": any(row["symbol"] == "sigma_H" for row in carry_rows) and any(row["symbol"] == "f_psi" for row in carry_rows), "requirement": "component fill rows are carried forward", "evidence": OUTPUTS["carry"].name},
    {"validation_id": "VAL3028_06_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3028 generated ledgers"},
    {"validation_id": "VAL3028_07_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3028 generated ledgers"},
    {"validation_id": "VAL3028_08_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3028_09_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3028_10_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3028_11_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3029-Y5-R2FR-covariant-LHcore-lift"), "requirement": "next target selects covariant lift or first component value", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3028_99_overall",
        "passed": overall_pass,
        "requirement": "all 3028 validation checks pass",
        "evidence": "aggregate of VAL3028_00 through VAL3028_11",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3028 - Parent LHcore Density Adoption Test Or Cbeta Component Values under AX1090

Status: `Y5_R2FR_3028_LHcore_density_adoption_rejected_variation_template_retained_3029_next`

## Verdict

3028 tests whether the minimal log-lapse density can be adopted as a real parent action block:

`L_Hcore^N = -C_N/2 sqrt(hbar) K0[(1+sigma_H u+f_psi psi_N) hbar^{{ij}}+K_TF^{{ij}}] D_i psi_N D_j psi_N + sqrt(hbar) J_H psi_N + L_boundary`.

The answer is **not yet**.

The density is mathematically useful: it has a clean conditional Euler variation and it reproduces the `sigma_H/f_psi` coefficient map.

But it is not parent-adoptable in the current corpus because the covariant parent density, field-variation status, source bridge, fixed boundary/reference, `A_source/M_H_ref`, filled coefficients, and anisotropy/cross-term guards are still unsigned.

So the branch has not failed, but the template remains a test ansatz, not a theory claim.

## Candidate Density

{md_table(candidate_rows, ["candidate_id", "density", "field_list", "derivative_order", "what_it_can_do", "current_status"])}

## Adoption Clause Audit

{md_table(audit_rows, ["clause_id", "clause", "current_status", "passes_adoption", "reason"])}

## Conditional Variation Test

{md_table(variation_rows, ["variation_id", "statement", "formula", "status", "claim_effect"])}

## Augmented Cbeta Residual Law

{md_table(residual_law_rows, ["law_id", "symbol", "formula", "bound", "status", "needed_for_score"])}

## Component Fill Carryforward

{md_table(carry_rows, ["carry_id", "source_component_id", "symbol", "carried_status", "required_source", "bound_or_gate", "source_path"])}

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
- `{OUTPUTS["candidate"]}`
- `{OUTPUTS["audit"]}`
- `{OUTPUTS["variation"]}`
- `{OUTPUTS["residual_law"]}`
- `{OUTPUTS["carry"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["candidate_copy"]}`
- `{BRANCH_OUTPUTS["audit_copy"]}`
- `{BRANCH_OUTPUTS["carry_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass until a covariant/source-backed `L_Hcore^N` or all component rows are filled below bound.
- No parent adoption from a static 3+1 template alone.
- No cancellation credit unless `2 sigma_H/A_source + f_psi = 0` is parent-derived.
- No scalar beta trace pass while anisotropy/cross terms are unbounded.
- No EH/GR import as MTS proof.
- No reciprocal `R_AB` density substitution for log-lapse `psi_N`.
- No orbital-`GM` denominator.
- No local-GR/Newton claim from this template alone.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
