from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "R11-executable-vector-minimum-fill-skeleton"
CHECKPOINT_DOC = "464-R11-executable-vector-minimum-fill-skeleton.md"
STATUS = "R11_executable_vector_minimum_fill_skeleton_written_10_family_parseable_no_claim_skeleton_missing_fields_explicit_no_EH_R11_Newton_or_local_GR_pass"
CLAIM_CEILING = "R11_minimum_vector_skeleton_only_no_EH_R11_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "465-constant-GM-derivative-hair-fill-gate.md"
SKELETON_PATH = Path("source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv")
MISSING_LEDGER_PATH = Path("source-intake/mts_residuals/R11_MTS_VECTOR_MISSING_FIELD_LEDGER.csv")
VALIDATION_RULES_PATH = Path("source-intake/mts_residuals/R11_MTS_VECTOR_VALIDATION_RULES.csv")
R10_LINK_PATH = Path("source-intake/mts_residuals/R11_R10_LINK_REQUIREMENTS.csv")


SCHEMA_COLUMNS = [
    "model_id",
    "branch_id",
    "vector_id",
    "operator_family",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "induced_observable",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

MISSING_COLUMNS = [
    "operator_family",
    "missing_field",
    "required_replacement",
    "why_required",
    "claim_blocked_until",
    "priority",
]

VALIDATION_COLUMNS = [
    "rule_id",
    "rule",
    "pass_condition",
    "current_status",
    "failure_action",
]

R10_LINK_COLUMNS = [
    "operator_family",
    "requires_R10_curve",
    "why",
    "required_R10_artifact",
    "current_status",
    "fallback_if_no_curve",
]


SOURCE_DOCS = [
    {
        "path": "463-EH-only-or-R11-executable-vector-gate.md",
        "role": "immediate EH/R11 fork and fill queue",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "canonical R11 coefficient-vector schema and comparison rules",
    },
    {
        "path": "437-R10-alpha-lambda-executable-curve-contract.md",
        "role": "R10 alpha(lambda) curve contract for finite-range R11 families",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "canonical template used as source family list",
    },
    {
        "path": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
        "role": "operator-family status from 463",
    },
    {
        "path": "source-intake/mts_residuals/R11_OPERATOR_VECTOR_FILL_QUEUE.csv",
        "role": "operator-family priority queue from 463",
    },
    {
        "path": "source-intake/mts_residuals/R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv",
        "role": "EH/R11 branch gate from 463",
    },
    {
        "path": "source-intake/mts_residuals/P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv",
        "role": "source-normalization residual row inputs feeding R11 source operator",
    },
    {
        "path": "source-intake/mts_residuals/R11_P6_metric_operator_rows_TEMPLATE.csv",
        "role": "P6 higher-curvature/nonlocal metric operator subtemplate",
    },
    {
        "path": "source-intake/mts_residuals/R11_P4_connection_rows_TEMPLATE.csv",
        "role": "P4 torsion/nonmetricity connection subtemplate",
    },
    {
        "path": "runs/20260602-202500-EH-only-or-R11-executable-vector-gate/status.json",
        "role": "status proving EH-only failed and actual R11 vector missing",
    },
    {
        "path": "runs/20260602-124500-R10-alpha-lambda-executable-curve-contract/status.json",
        "role": "status proving R10 curve is template-only",
    },
]


FAMILY_SPECS = [
    {
        "priority": "4",
        "operator_family": "boundary_topological_terms",
        "coefficient_symbol": "c_boundary_or_c_GB",
        "operator_form": "boundary/class/topological functionals and induced boundary stress",
        "affected_rows": "R3;R4;R7;R8;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;alpha3;xi;operator_ledger",
        "normalization": "MISSING_BOUNDARY_NORMALIZATION_RELATIVE_TO_EH_OR_MEASURED_G",
        "weak_field_map": "MISSING_BOUNDARY_NOHAIR_OR_R3_R4_R7_R8_MAP",
        "needs_r10": "false",
        "notes": "Boundary/topological terms are harmless only after boundary/class no-hair is sourced.",
    },
    {
        "priority": "2",
        "operator_family": "R2_fR_scalar_mode",
        "coefficient_symbol": "c_R2_or_c_fR",
        "operator_form": "sqrt(-g)(c_R2 R^2 + c_fR f_extra(R))",
        "affected_rows": "R3;R4;R10;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;alpha(lambda);operator_ledger",
        "normalization": "MISSING_LENGTH_POWER_OR_CUTOFF_NORMALIZATION",
        "weak_field_map": "MISSING_GAMMA_BETA_SCALAR_MASS_ALPHA_LAMBDA_MAP",
        "needs_r10": "true",
        "notes": "Finite scalar range also needs an R10 alpha(lambda) curve.",
    },
    {
        "priority": "6",
        "operator_family": "Ricci_Weyl_squared",
        "coefficient_symbol": "c_Ricci_or_c_Weyl",
        "operator_form": "sqrt(-g)(c_Ricci R_mn R^mn + c_Weyl C_mnrs C^mnrs)",
        "affected_rows": "R3;R8;R11",
        "induced_observable": "gamma_minus_1;xi;operator_ledger",
        "normalization": "MISSING_LENGTH_POWER_OR_CUTOFF_NORMALIZATION",
        "weak_field_map": "MISSING_GAMMA_XI_SLIP_WAVE_SECTOR_MAP",
        "needs_r10": "false",
        "notes": "Topological combinations still need boundary no-hair before claim credit.",
    },
    {
        "priority": "7",
        "operator_family": "scalar_tensor_class_metric",
        "coefficient_symbol": "F_phi_C_or_c_scalar",
        "operator_form": "sqrt(-g)[F(phi,C)R - 1/2(nabla phi)^2 - V(phi,C)]",
        "affected_rows": "R2;R3;R4;R9;R10;R11",
        "induced_observable": "clock_residual;gamma_minus_1;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger",
        "normalization": "MISSING_SCALAR_SOURCE_AND_EH_NORMALIZATION",
        "weak_field_map": "MISSING_CLOCK_PPN_GDOT_RANGE_MAP",
        "needs_r10": "true",
        "notes": "Same-frame scalar language is not source-normalized GR unless scalar/class field is silent or mapped.",
    },
    {
        "priority": "5",
        "operator_family": "vector_preferred_frame",
        "coefficient_symbol": "c_V_or_c_domain_vector",
        "operator_form": "c_V V_mu V_nu, projector/domain vector stress, or aether-like terms",
        "affected_rows": "R5;R6;R7;R8;R11",
        "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "normalization": "MISSING_VECTOR_FRAME_NORMALIZATION",
        "weak_field_map": "MISSING_ALPHA1_ALPHA2_ALPHA3_XI_MAP",
        "needs_r10": "false",
        "notes": "Covariance does not remove preferred-frame/location residuals.",
    },
    {
        "priority": "3",
        "operator_family": "torsion_nonmetricity",
        "coefficient_symbol": "c_T_or_c_Q",
        "operator_form": "c_T T^2 + c_Q Q^2 + matter spin/light-cone connection couplings",
        "affected_rows": "R0;R1;R2;R11",
        "induced_observable": "eta_WEP;source_charge_residual;clock_residual;lightcone_residual;operator_ledger",
        "normalization": "MISSING_CONNECTION_SCALE_OR_NO_GAMMA_THEOREM",
        "weak_field_map": "MISSING_WEP_CLOCK_LIGHTCONE_SPIN_SOURCE_MAP",
        "needs_r10": "false",
        "notes": "Clean win is no-independent-connection or Levi-Civita parent theorem; otherwise fill P4 rows.",
    },
    {
        "priority": "8",
        "operator_family": "bulk_X_force_law",
        "coefficient_symbol": "q_X_or_c_X",
        "operator_form": "(-Delta + m_X^2)X = q_X rho_source plus metric/source stress",
        "affected_rows": "R1;R3;R4;R10;R11",
        "induced_observable": "eta_source_AB;gamma_minus_1;beta_minus_1;alpha(lambda);operator_ledger",
        "normalization": "MISSING_SOURCE_TEST_CHARGE_AND_MEASURED_G_NORMALIZATION",
        "weak_field_map": "MISSING_ALPHA_X_LAMBDA_X_PPN_SOURCE_MAP",
        "needs_r10": "true",
        "notes": "Mass gap alone is not enough; source/test charge normalization sets alpha.",
    },
    {
        "priority": "9",
        "operator_family": "nonlocal_memory_kernel",
        "coefficient_symbol": "c_nonlocal_or_K_norm",
        "operator_form": "R Box^-1 R or integral K(x,x_prime) I[g](x_prime)dV_prime",
        "affected_rows": "R7;R9;R10;R11",
        "induced_observable": "alpha3;Gdot_over_G;alpha(lambda);operator_ledger",
        "normalization": "MISSING_KERNEL_NORM_AND_LOCALITY_NORMALIZATION",
        "weak_field_map": "MISSING_ALPHA3_GDOT_ALPHA_LAMBDA_KERNEL_MAP",
        "needs_r10": "true",
        "notes": "Cosmology memory activity cannot be imported as local kernel silence.",
    },
    {
        "priority": "1",
        "operator_family": "source_normalization_operator",
        "coefficient_symbol": "mu_extra_or_delta_GM_operator_vector",
        "operator_form": "mu_obs = G_eff M_eff + mu_extra with source-normalization operator corrections",
        "affected_rows": "R1;R4;R9;R10;R11",
        "induced_observable": "eta_source_AB;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger",
        "normalization": "MISSING_MU_EXTRA_OVER_GEFF_MEFF_AND_DERIVATIVE_NORMALIZATION",
        "weak_field_map": "MISSING_P8_RESIDUAL_COMPONENT_MAP",
        "needs_r10": "true",
        "notes": "Highest priority for Newton: constant measured GM needs source-normalization residual rows filled or theorem-zero.",
    },
    {
        "priority": "5",
        "operator_family": "projector_domain_stress",
        "coefficient_symbol": "c_projector_or_c_domain",
        "operator_form": "delta_g P_D, delta_g chi_D, lambda_P constraint stress, or readout-mask backreaction",
        "affected_rows": "R5;R6;R7;R8;R11",
        "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "normalization": "MISSING_PROJECTOR_DOMAIN_STRESS_NORMALIZATION",
        "weak_field_map": "MISSING_PREFERRED_FRAME_LOCATION_STRESS_MAP",
        "needs_r10": "false",
        "notes": "Readout/projector/domain variation must be topological/metric-independent or mapped.",
    },
]


MISSING_FIELDS = [
    ("coefficient_value", "numeric coefficient, derived_zero certificate, or derived_bound envelope"),
    ("coefficient_units", "units after normalization"),
    ("weak_field_map", "formula or artifact mapping coefficient to local residual rows"),
    ("predicted_residual_or_bound_source", "numeric residual, curve/vector map, or theorem-zero source artifact"),
    ("derivation_status", "derived_zero, derived_bound, fitted, phenomenological, closure_assumed, or speculative with source"),
    ("formula_reference", "file/equation proving the coefficient and map"),
    ("source_file", "existing source derivation or run artifact supplying the row"),
    ("assumptions", "frame/locality/source-normalization/boundary/range assumptions"),
]


VALIDATION_RULES = [
    {
        "rule_id": "V11_0_schema",
        "rule": "Skeleton rows must match the canonical 19-column R11 schema.",
        "pass_condition": "all schema columns present and parseable by csv.DictReader",
        "current_status": "pass_skeleton",
        "failure_action": "reject vector file",
    },
    {
        "rule_id": "V11_1_family_completeness",
        "rule": "Every retained operator family from 463 must appear exactly once.",
        "pass_condition": "10 family rows present",
        "current_status": "pass_skeleton",
        "failure_action": "reject vector file",
    },
    {
        "rule_id": "V11_2_no_generic_fill_placeholders",
        "rule": "Generic fill_* placeholders are replaced by explicit MISSING_* fields.",
        "pass_condition": "no field starts with fill_",
        "current_status": "pass_skeleton_no_claim",
        "failure_action": "replace generic placeholder with explicit missing-field marker",
    },
    {
        "rule_id": "V11_3_missing_markers_block_claims",
        "rule": "Any MISSING_* value forces valid_for_claim=false.",
        "pass_condition": "all current skeleton rows have valid_for_claim=false",
        "current_status": "pass_no_claim",
        "failure_action": "block row from evaluator claim credit",
    },
    {
        "rule_id": "V11_4_R10_link_required",
        "rule": "Any family inducing finite-range/range rows must cite a valid R10 curve or theorem-zero source.",
        "pass_condition": "R10 link artifact exists and no required link is omitted",
        "current_status": "links_declared_no_curves_loaded",
        "failure_action": "keep alpha(lambda)/R10 rows retained",
    },
    {
        "rule_id": "V11_5_source_path_required",
        "rule": "A claimable row needs a real source_file path and formula_reference.",
        "pass_condition": "source path exists and formula reference is not missing",
        "current_status": "fail_for_claim",
        "failure_action": "valid_for_claim remains false",
    },
    {
        "rule_id": "V11_6_units_required",
        "rule": "A nonzero or bounded coefficient must declare units and normalization.",
        "pass_condition": "coefficient_units and normalization are concrete, not MISSING_*",
        "current_status": "fail_for_claim",
        "failure_action": "valid_for_claim remains false",
    },
]


def skeleton_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for spec in FAMILY_SPECS:
        rows.append(
            {
                "model_id": "MTS_source_normalized_Newton_branch",
                "branch_id": "post_checkpoint_R11_minimum_skeleton",
                "vector_id": "R11_MTS_minimum_executable_vector",
                "operator_family": spec["operator_family"],
                "coefficient_symbol": spec["coefficient_symbol"],
                "coefficient_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT",
                "coefficient_units": "MISSING_COEFFICIENT_UNITS",
                "normalization": spec["normalization"],
                "operator_form": spec["operator_form"],
                "weak_field_map": spec["weak_field_map"],
                "affected_rows": spec["affected_rows"],
                "induced_observable": spec["induced_observable"],
                "predicted_residual_or_bound_source": "MISSING_RESIDUAL_BOUND_OR_THEOREM_SOURCE",
                "derivation_status": "retained_unfilled",
                "formula_reference": "MISSING_FORMULA_REFERENCE",
                "source_file": "MISSING_SOURCE_FILE",
                "assumptions": "MISSING_FRAME_LOCALITY_SOURCE_NORMALIZATION_BOUNDARY_RANGE_ASSUMPTIONS",
                "valid_for_claim": "false",
                "notes": f"parseable skeleton row only; priority={spec['priority']}; needs_R10_curve={spec['needs_r10']}; {spec['notes']}",
            }
        )
    return rows


def missing_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    priority_lookup = {spec["operator_family"]: spec["priority"] for spec in FAMILY_SPECS}
    family_reason = {
        "coefficient_value": "without a coefficient or theorem-zero source, the operator cannot be scored",
        "coefficient_units": "dimensionful operator coefficients are meaningless without units",
        "weak_field_map": "local rows need a formula mapping the coefficient into observables",
        "predicted_residual_or_bound_source": "the evaluator needs numeric residuals, curves, vectors, or theorem-zero proof",
        "derivation_status": "claim policy depends on whether the row is derived, bounded, fitted, or speculative",
        "formula_reference": "the row must cite the equation or artifact that defines it",
        "source_file": "source paths must exist before the row can be trusted",
        "assumptions": "frame, locality, source normalization, boundary, and range assumptions must be explicit",
    }
    for spec in FAMILY_SPECS:
        for field, replacement in MISSING_FIELDS:
            rows.append(
                {
                    "operator_family": spec["operator_family"],
                    "missing_field": field,
                    "required_replacement": replacement,
                    "why_required": family_reason[field],
                    "claim_blocked_until": f"{field} is concrete and sourced",
                    "priority": priority_lookup[spec["operator_family"]],
                }
            )
    return rows


def r10_link_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for spec in FAMILY_SPECS:
        needs = spec["needs_r10"]
        rows.append(
            {
                "operator_family": spec["operator_family"],
                "requires_R10_curve": needs,
                "why": "operator can induce alpha(lambda), finite-range, radial, or range-dependent source strength" if needs == "true" else "no direct R10 curve required unless later weak-field map creates range dependence",
                "required_R10_artifact": "source-intake/mts_residuals/R10_alpha_lambda_curve_<branch>.csv or theorem-zero source" if needs == "true" else "none_currently",
                "current_status": "required_but_missing" if needs == "true" else "not_required_by_skeleton",
                "fallback_if_no_curve": "keep alpha(lambda)/R10 retained and valid_for_claim=false" if needs == "true" else "continue R11 row validation",
            }
        )
    return rows


def utc_now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def exists(path: str) -> bool:
    return (ROOT / path).exists()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_csv_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def count_generic_fill_tokens(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    return text.count("fill_")


def count_missing_markers(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    return text.count("MISSING_")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    return [
        {
            "source_file": item["path"],
            "exists": str(exists(item["path"])),
            "role": item["role"],
        }
        for item in SOURCE_DOCS
    ]


def gate_results(source_paths_missing: int, template_rows: int, skeleton_count: int, missing_count: int, r10_count: int, fill_tokens: int, missing_markers: int) -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
        },
        {
            "gate": "canonical_template_loaded",
            "status": "pass" if template_rows == 10 else "fail",
            "evidence": f"{template_rows} canonical R11 template rows",
        },
        {
            "gate": "minimum_skeleton_written",
            "status": "pass" if skeleton_count == 10 else "fail",
            "evidence": f"{skeleton_count} branch skeleton rows",
        },
        {
            "gate": "missing_field_ledger_written",
            "status": "pass" if missing_count == 80 else "fail",
            "evidence": f"{missing_count} missing field rows",
        },
        {
            "gate": "R10_link_requirements_written",
            "status": "pass" if r10_count == 10 else "fail",
            "evidence": f"{r10_count} R10 link rows",
        },
        {
            "gate": "generic_fill_placeholders_removed",
            "status": "pass" if fill_tokens == 0 else "fail",
            "evidence": f"fill_ token count in skeleton = {fill_tokens}",
        },
        {
            "gate": "missing_markers_explicit",
            "status": "pass" if missing_markers > 0 else "fail",
            "evidence": f"MISSING_ marker count in skeleton = {missing_markers}",
        },
        {
            "gate": "all_skeleton_rows_no_claim",
            "status": "pass",
            "evidence": "all rows valid_for_claim=false and derivation_status=retained_unfilled",
        },
        {
            "gate": "actual_R11_vector_supplied",
            "status": "fail",
            "evidence": "skeleton only; missing fields are explicit but unfilled",
        },
        {
            "gate": "R11_promoted",
            "status": "fail",
            "evidence": "no row has real coefficient/source/map validation",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "R11 and P8 source-normalization rows remain retained",
        },
        {
            "gate": "local_GR_claim_allowed",
            "status": "fail",
            "evidence": "operator skeleton only; no EH/R11/PPN pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def render_doc(timestamp: str, run_dir: Path, source_paths_missing: int, template_rows: int, skeleton_count: int, missing_count: int, r10_count: int, fill_tokens: int, missing_markers: int) -> str:
    sources = source_register()
    skeleton = skeleton_rows()
    missing = missing_rows()
    r10_links = r10_link_rows()
    gates = gate_results(source_paths_missing, template_rows, skeleton_count, missing_count, r10_count, fill_tokens, missing_markers)

    status_rows = [
        {
            "claim": "minimum parseable R11 skeleton written",
            "status": "pass",
            "evidence": "10 branch-specific operator-family rows with canonical schema",
            "claim_credit": "scaffold_only",
        },
        {
            "claim": "generic fill placeholders removed",
            "status": "pass" if fill_tokens == 0 else "fail",
            "evidence": f"fill_ token count = {fill_tokens}; MISSING_ marker count = {missing_markers}",
            "claim_credit": "scaffold_only",
        },
        {
            "claim": "actual executable R11 vector supplied",
            "status": "fail",
            "evidence": "all rows retain explicit MISSING_* fields and valid_for_claim=false",
            "claim_credit": "none",
        },
        {
            "claim": "R11/Newton/local-GR promoted",
            "status": "fail",
            "evidence": "skeleton only; no coefficients, maps, source files, R10 curves, or theorem-zero proofs loaded",
            "claim_credit": "none",
        },
    ]

    return f"""# 464 - R11 Executable Vector Minimum Fill Skeleton

Private R11 operator-vector checkpoint. This is not a public Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Purpose

Checkpoint 463 decided the fork:

```text
EH-only?         not currently parent-derived.
R11 executable?  not currently supplied.
```

This checkpoint converts the generic R11 template into a branch-specific minimum skeleton. The skeleton is parseable and concrete enough for future filling, but every row remains invalid for claim.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R11_executable_vector_minimum_fill_skeleton.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Skeleton CSV | `{SKELETON_PATH}` |
| Missing-field ledger | `{MISSING_LEDGER_PATH}` |
| Validation rules | `{VALIDATION_RULES_PATH}` |
| R10 link requirements | `{R10_LINK_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(sources, ["source_file", "exists", "role"])}

## 4. Minimum R11 Skeleton

The minimum branch-specific skeleton has been written to `{SKELETON_PATH}`.

{md_table(skeleton, SCHEMA_COLUMNS)}

## 5. Missing-Field Ledger

The missing-field ledger has been written to `{MISSING_LEDGER_PATH}`.

Only the first twenty rows are shown here; the CSV contains every missing field for every family.

{md_table(missing[:20], MISSING_COLUMNS)}

## 6. R10 Link Requirements

The R10 link table has been written to `{R10_LINK_PATH}`.

{md_table(r10_links, R10_LINK_COLUMNS)}

## 7. Validation Rules

The validation rules have been written to `{VALIDATION_RULES_PATH}`.

{md_table(VALIDATION_RULES, VALIDATION_COLUMNS)}

## 8. Gate Results

{md_table(gates, ["gate", "status", "evidence"])}

## 9. Theorem Status

{md_table(status_rows, ["claim", "status", "evidence", "claim_credit"])}

## 10. Decision

The R11 vector is no longer a vague template. It is now a branch-specific parseable skeleton with ten operator-family rows and eighty explicit missing-field debts. Generic `fill_*` placeholders have been removed from the skeleton and replaced by `MISSING_*` markers.

This does not make R11 pass. It does the opposite: it makes the failure exact. A future row becomes claimable only when the missing coefficient, units, weak-field map, source path, formula reference, assumptions, and any required R10 curve/theorem-zero source are supplied.

Practical read: this is the spreadsheet version of "put gloves on." The R11 fighters are named, their weight classes are named, and their missing paperwork is named. They still have not fought a measured row yet.

## 11. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 465-constant-GM-derivative-hair-fill-gate.md | highest-priority R11 family is source_normalization_operator, which controls measured GM/Newton |
| 2 | R11_P6_metric_operator_rows executable fill | second priority is R2/fR scalar mode because it hits gamma, beta, and R10 |
| 3 | R11_P4_connection_rows executable fill | third priority is torsion/nonmetricity because it hits WEP, clocks, and source charge |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_paths_missing = sum(1 for item in SOURCE_DOCS if not exists(item["path"]))
    missing_sources = [item["path"] for item in SOURCE_DOCS if not exists(item["path"])]

    template_rows = read_csv_count(ROOT / "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv")

    skeleton = skeleton_rows()
    missing = missing_rows()
    r10_links = r10_link_rows()

    write_csv(ROOT / SKELETON_PATH, skeleton, SCHEMA_COLUMNS)
    write_csv(ROOT / MISSING_LEDGER_PATH, missing, MISSING_COLUMNS)
    write_csv(ROOT / VALIDATION_RULES_PATH, VALIDATION_RULES, VALIDATION_COLUMNS)
    write_csv(ROOT / R10_LINK_PATH, r10_links, R10_LINK_COLUMNS)
    write_csv(results_dir / "R11_MTS_minimum_executable_vector_skeleton.csv", skeleton, SCHEMA_COLUMNS)
    write_csv(results_dir / "R11_MTS_vector_missing_field_ledger.csv", missing, MISSING_COLUMNS)
    write_csv(results_dir / "R11_MTS_vector_validation_rules.csv", VALIDATION_RULES, VALIDATION_COLUMNS)
    write_csv(results_dir / "R11_R10_link_requirements.csv", r10_links, R10_LINK_COLUMNS)

    skeleton_count = read_csv_count(ROOT / SKELETON_PATH)
    missing_count = read_csv_count(ROOT / MISSING_LEDGER_PATH)
    r10_count = read_csv_count(ROOT / R10_LINK_PATH)
    fill_tokens = count_generic_fill_tokens(ROOT / SKELETON_PATH)
    missing_markers = count_missing_markers(ROOT / SKELETON_PATH)

    doc_text = render_doc(timestamp, run_dir, source_paths_missing, template_rows, skeleton_count, missing_count, r10_count, fill_tokens, missing_markers)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": source_paths_missing,
        "missing_sources": missing_sources,
        "canonical_template_rows": template_rows,
        "skeleton_rows": skeleton_count,
        "missing_field_rows": missing_count,
        "validation_rule_rows": len(VALIDATION_RULES),
        "R10_link_rows": r10_count,
        "generic_fill_placeholder_tokens_in_skeleton": fill_tokens,
        "missing_markers_in_skeleton": missing_markers,
        "all_skeleton_rows_valid_for_claim_false": True,
        "actual_R11_vector_supplied": False,
        "R11_promoted": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=utc_now_tag())
    args = parser.parse_args()
    status = write_run(args.timestamp)
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
