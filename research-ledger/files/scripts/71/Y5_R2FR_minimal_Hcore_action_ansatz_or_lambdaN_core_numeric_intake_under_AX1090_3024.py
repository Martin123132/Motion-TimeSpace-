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

CHECKPOINT = "3024"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
BETA_BOUND_ABS = 7.8e-5
F1_BOUND_IF_SIGMA_ZERO = 4.0 * BETA_BOUND_ABS

DOC = ROOT / "3024-Y5-R2FR-minimal-Hcore-action-ansatz-or-lambdaN-core-numeric-intake-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3024_00_3023_doc": ROOT / "3023-Y5-R2FR-Hcore-action-block-or-first-lambdaN-bound-row-under-AX1090.md",
    "SRC3024_01_3023_hcore": RESIDUALS / "P8_Y5_R2FR_3023_HCORE_ACTION_BLOCK_AUDIT.csv",
    "SRC3024_02_3023_lambda_schema": RESIDUALS / "P8_Y5_R2FR_3023_FIRST_LAMBDAN_BOUND_ROW_SCHEMA.csv",
    "SRC3024_03_3023_validator": RESIDUALS / "P8_Y5_R2FR_3023_LAMBDAN_ROW_VALIDATOR.csv",
    "SRC3024_04_3023_next": RESIDUALS / "P8_Y5_R2FR_3023_NEXT_TARGET.csv",
    "SRC3024_05_3022_owner": RESIDUALS / "P8_Y5_R2FR_3022_PSIN_HAMILTONIAN_OWNER_AUDIT.csv",
    "SRC3024_06_3021_lambda": RESIDUALS / "P8_Y5_R2FR_3021_LAMBDA_N_RESIDUAL_LEDGER.csv",
    "SRC3024_07_3020_lapse": RESIDUALS / "P8_Y5_R2FR_3020_LAPSE_COEFFICIENT_MAP.csv",
    "SRC3024_08_2924_reduction": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "SRC3024_09_3007_grammar": RESIDUALS / "P8_Y5_R2FR_3007_MINIMAL_PARENT_ACTION_GRAMMAR.csv",
    "SRC3024_10_3007_variation": RESIDUALS / "P8_Y5_R2FR_3007_SECTOR_VARIATION_LEDGER.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3024_SOURCE_REGISTER.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_3024_VARIATION_DERIVATION.csv",
    "coefficient": RESIDUALS / "P8_Y5_R2FR_3024_LAMBDAN_CORE_COEFFICIENT_MAP.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3024_KINETIC_SLOPE_BOUND_TRANSLATION.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3024_CLOSURE_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3024_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3024_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3024_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3024_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ansatz_copy": PARENT_ACTION / "minimal_Hcore_log_lapse_ansatz_3024_CONDITIONAL.csv",
    "coefficient_copy": LOCAL_BOUNDS / "lambdaN_core_kinetic_slope_map_3024_NONCLAIM.csv",
    "bound_copy": LOCAL_BOUNDS / "lambdaN_core_f1_sigma_bound_3024_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3024_PARENT_SIGN_F1_SIGMA_CANCELLATION_OR_BOUND_NEXT_NONCLAIM.csv",
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
    "SRC3024_00_3023_doc": "3023 handoff: Hcore action block not filled; first lambda_N_core schema emitted",
    "SRC3024_01_3023_hcore": "Hcore action block audit",
    "SRC3024_02_3023_lambda_schema": "lambda_N_core schema and beta comparator",
    "SRC3024_03_3023_validator": "lambda_N row validator",
    "SRC3024_04_3023_next": "machine-readable 3024 target",
    "SRC3024_05_3022_owner": "psi_N Hamiltonian owner audit",
    "SRC3024_06_3021_lambda": "lambda_N residual family ledger",
    "SRC3024_07_3020_lapse": "exact lapse/log-lapse to beta coefficient map",
    "SRC3024_08_2924_reduction": "MTS-to-EH reduction clauses still unsigned",
    "SRC3024_09_3007_grammar": "minimal parent action grammar",
    "SRC3024_10_3007_variation": "sector variation ledger",
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

ansatz_rows = [
    base(
        {
            "ansatz_id": "ANZ3024_0_field",
            "object": "log-lapse field",
            "mathematical_form": "psi_N=-log(N)",
            "role": "candidate Hcore scalar whose exterior first-order solution is psi_N=A_source u with u=W/c^2",
            "status": "CANDIDATE_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_PARENT_FIELD_IDENTIFICATION_IN_MTS_PRIMITIVES",
        }
    ),
    base(
        {
            "ansatz_id": "ANZ3024_1_readout",
            "object": "physical lapse readout",
            "mathematical_form": "g00=-N^2=-exp(-2 psi_N)",
            "role": "turns log-lapse linearity into beta square law when lambda_N_core=0",
            "status": "ALGEBRAIC_READOUT_DEFINED",
            "missing_for_claim": "MISSING_PARENT_READOUT_MAP_TO_OBSERVED_PPN_GAUGE",
        }
    ),
    base(
        {
            "ansatz_id": "ANZ3024_2_kinetic_density",
            "object": "minimal static Hcore kinetic block",
            "mathematical_form": "S_N=-C_N/2 int K_N^{ij}(u,psi_N) partial_i psi_N partial_j psi_N + int J_H psi_N + boundary",
            "role": "smallest local block able to own the psi_N exterior equation without importing Schwarzschild",
            "status": "CONDITIONAL_ANSATZ",
            "missing_for_claim": "MISSING_SOURCE_IN_CORPUS_AS_PARENT_ACTION_TERM",
        }
    ),
    base(
        {
            "ansatz_id": "ANZ3024_3_kinetic_expansion",
            "object": "first nonlinear kinetic/coframe drift",
            "mathematical_form": "K_N^{ij}=K0 delta^{ij}[1+sigma_H u+f_psi psi_N+O(u^2)]",
            "role": "isolates the exact coefficient that can create or cancel lambda_N_core",
            "status": "DERIVATION_PARAMETERIZATION_READY",
            "missing_for_claim": "MISSING_PARENT_VALUES_FOR_sigma_H_AND_f_psi",
        }
    ),
    base(
        {
            "ansatz_id": "ANZ3024_4_vacuum_silence",
            "object": "exterior source silence",
            "mathematical_form": "J_H=0 outside compact source; no potential/mass term through O(u^2); boundary fixed before readout",
            "role": "prevents a hidden exterior source from faking or spoiling lambda_N_core=0",
            "status": "REQUIRED_CLAUSE_NOT_SIGNED",
            "missing_for_claim": "MISSING_WORLDTUBE_SOURCE_GLUE_AND_BOUNDARY_REFERENCE",
        }
    ),
]

variation_rows = [
    base(
        {
            "derivation_id": "VAR3024_0_Euler_block",
            "statement": "varying S_N with respect to psi_N gives the exterior Euler equation",
            "formula": "partial_i(K_N^{ij} partial_j psi_N)-1/2 (partial K_N^{ij}/partial psi_N) partial_i psi_N partial_j psi_N=0",
            "assumptions": "static exterior; J_H=0; fixed boundary; isotropic first-order branch",
            "result": "ACTION_VARIATION_DERIVED_FOR_ANSATZ",
            "claim_status": "CONDITIONAL_NOT_MTS_SIGNED",
        }
    ),
    base(
        {
            "derivation_id": "VAR3024_1_expansion",
            "statement": "insert psi_N=A_source u+lambda_N_core u^2+O(u^3) with Delta u=0 outside source",
            "formula": "2 lambda_N_core + sigma_H A_source + (f_psi/2) A_source^2 = 0",
            "assumptions": "u=W/c^2 is harmonic in the exterior comparator chart; retained terms are O(u^2)",
            "result": "SECOND_ORDER_COEFFICIENT_EQUATION",
            "claim_status": "CONDITIONAL_NOT_MTS_SIGNED",
        }
    ),
    base(
        {
            "derivation_id": "VAR3024_2_lambda_map",
            "statement": "solve the coefficient equation for the quadratic log-lapse residual",
            "formula": "lambda_N_core/A_source^2 = -sigma_H/(2 A_source)-f_psi/4",
            "assumptions": "A_source finite and nonzero; same source-normalized branch",
            "result": "EXACT_CONDITIONAL_LAMBDAN_MAP",
            "claim_status": "NONCLAIM_UNTIL_A_SOURCE_SIGMA_F_SIGNED",
        }
    ),
]

coefficient_rows = [
    base(
        {
            "map_id": "LCM3024_0_general",
            "symbol": "lambda_N_core",
            "formula": "lambda_N_core/A_source^2 = -sigma_H/(2 A_source)-f_psi/4",
            "zero_condition": "2 sigma_H/A_source + f_psi = 0",
            "interpretation": "beta core is suppressed by a cancellation between coframe/measure drift and explicit log-lapse kinetic coupling slope",
            "current_status": "DERIVED_CONDITIONAL_MAP_PARENT_VALUES_MISSING",
            "needed_for_claim": "parent-signed A_source, sigma_H, f_psi and vacuum-silence clauses",
        }
    ),
    base(
        {
            "map_id": "LCM3024_1_flat_measure_special_case",
            "symbol": "lambda_N_core",
            "formula": "if sigma_H=0, lambda_N_core/A_source^2=-f_psi/4",
            "zero_condition": "f_psi=0",
            "interpretation": "a flat/silent coframe branch needs a stationary kinetic metric at psi_N=0",
            "current_status": "SPECIAL_CASE_ONLY",
            "needed_for_claim": "parent-signed sigma_H=0 and f_psi=0",
        }
    ),
    base(
        {
            "map_id": "LCM3024_2_GR_like_cancellation",
            "symbol": "lambda_N_core",
            "formula": "if A_source=1, sigma_H=1, f_psi=-2, then lambda_N_core=0",
            "zero_condition": "sigma_H=1 and f_psi=-2 in the same observed branch",
            "interpretation": "a GR-like lapse/coframe coupling can kill the quadratic log-lapse term without pretending the coframe is flat",
            "current_status": "REFERENCE_MORPHOLOGY_NOT_MTS_PROOF",
            "needed_for_claim": "MTS parent action must derive these coefficients, not import them",
        }
    ),
]

bound_rows = [
    base(
        {
            "bound_id": "BND3024_0_general_combo",
            "quantity": "C_beta_core=sigma_H/(2 A_source)+f_psi/4",
            "beta_projection": "abs(lambda_N_core/A_source^2)=abs(C_beta_core)",
            "bound": f"abs(C_beta_core)<={BETA_BOUND_ABS}",
            "numeric_bound": BETA_BOUND_ABS,
            "units": "dimensionless",
            "source": "Cassini-style beta absolute comparator inherited from 3023 schema",
            "current_status": "NONCLAIM_UNTIL_A_SOURCE_SIGMA_F_SOURCED",
        }
    ),
    base(
        {
            "bound_id": "BND3024_1_flat_measure_fpsi",
            "quantity": "f_psi under sigma_H=0",
            "beta_projection": "abs(f_psi)/4",
            "bound": f"abs(f_psi)<={F1_BOUND_IF_SIGMA_ZERO:.6g}",
            "numeric_bound": F1_BOUND_IF_SIGMA_ZERO,
            "units": "dimensionless",
            "source": "derived from BND3024_0 with sigma_H=0",
            "current_status": "SPECIAL_CASE_NONCLAIM",
        }
    ),
]

gate_rows = [
    base({"gate_id": "GATE3024_0_sources", "gate": "every cited local source path exists", "result": all(boolish(row["exists"]) for row in source_register), "notes": "source-backed continuation from 3023"}),
    base({"gate_id": "GATE3024_1_ansatz_written", "gate": "minimal Hcore ansatz is explicit", "result": True, "notes": "field, readout, kinetic density, source silence and boundary clauses are recorded"}),
    base({"gate_id": "GATE3024_2_variation_map", "gate": "Euler variation gives lambda_N_core coefficient equation", "result": True, "notes": "conditional map derived from ansatz"}),
    base({"gate_id": "GATE3024_3_parent_signed", "gate": "MTS corpus signs A_source, sigma_H and f_psi", "result": False, "notes": "values are not yet sourced from parent MTS action"}),
    base({"gate_id": "GATE3024_4_lambda_zero_claim", "gate": "lambda_N_core=0 theorem claimable", "result": False, "notes": "zero condition is exact but unsigned"}),
    base({"gate_id": "GATE3024_5_beta_core_score", "gate": "core beta residual can be scored", "result": False, "notes": "requires numeric/source-backed A_source, sigma_H, f_psi or a parent zero theorem"}),
    base({"gate_id": "GATE3024_6_local_GR_claim", "gate": "local GR/Newton reduction claimable", "result": False, "notes": "gamma, beta total, source bridge, alpha3/current and readout still need closure"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3024_0_route",
            "decision": "take the derivation-first route, not numeric lambda_N intake",
            "rationale": "a minimal Hcore ansatz yields an exact coefficient law and exposes the coupling/cancellation needed for beta",
            "consequence": "lambda_N_core is not just missing; it is tied to sigma_H and f_psi",
        }
    ),
    base(
        {
            "decision_id": "DEC3024_1_status",
            "decision": "keep the result conditional and nonclaim",
            "rationale": "the ansatz is source-ready but not parent-signed by the MTS corpus",
            "consequence": "no local-GR/beta pass is promoted",
        }
    ),
    base(
        {
            "decision_id": "DEC3024_2_next",
            "decision": "hunt the parent source of sigma_H and f_psi",
            "rationale": "these are now the two coefficients that decide whether the local log-lapse branch lives or dies",
            "consequence": "3025 should search the parent action/coframe/coupling files for this cancellation or create strict bound-input rows",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3024_0_3025",
            "target_doc": "3025-Y5-R2FR-parent-sign-sigmaH-fpsi-cancellation-or-bound-input-rows-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_parent_sign_sigmaH_fpsi_cancellation_or_bound_input_rows_under_AX1090_3025.py",
            "mission": "search the parent action, coframe/readout and coupling ledgers for A_source, sigma_H and f_psi; if the zero condition is not signed, stage strict nonclaim bound rows for the combination C_beta_core",
            "success_condition": "either parent evidence signs 2 sigma_H/A_source + f_psi=0, or the missing coefficients become explicit bound-input rows with claim_allowed=false",
            "forbidden": "no GR/EH import as MTS proof; no flat-coframe assumption unless sourced; no orbital-GM denominator; no hidden cancellation; no local-GR claim; no formalization-workbench edits; no GitHub action",
            "selected": True,
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["ansatz"], ansatz_rows)
write_csv(OUTPUTS["variation"], variation_rows)
write_csv(OUTPUTS["coefficient"], coefficient_rows)
write_csv(OUTPUTS["bound"], bound_rows)
write_csv(OUTPUTS["gates"], gate_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_rows = []
for key, source_key in [
    ("ansatz_copy", "ansatz"),
    ("coefficient_copy", "coefficient"),
    ("bound_copy", "bound"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3024_{len(branch_rows)}",
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
claim_rows = source_register + ansatz_rows + variation_rows + coefficient_rows + bound_rows + gate_rows + decision_rows + next_rows

validation_rows = [
    {"validation_id": "VAL3024_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "every cited local source path exists", "evidence": OUTPUTS["sources"].name},
    {"validation_id": "VAL3024_01_csv_parse", "passed": all(csv_ok(path) for path in all_csv), "requirement": "generated CSV rows parse cleanly", "evidence": "all generated CSV artifacts import with csv.DictReader"},
    {"validation_id": "VAL3024_02_ansatz_complete", "passed": all(any(row["ansatz_id"] == required for row in ansatz_rows) for required in ["ANZ3024_0_field", "ANZ3024_1_readout", "ANZ3024_2_kinetic_density", "ANZ3024_3_kinetic_expansion", "ANZ3024_4_vacuum_silence"]), "requirement": "minimal Hcore ansatz records field, readout, kinetic density, coefficient expansion and vacuum silence", "evidence": OUTPUTS["ansatz"].name},
    {"validation_id": "VAL3024_03_variation_formula", "passed": any(row["derivation_id"] == "VAR3024_1_expansion" and "2 lambda_N_core" in row["formula"] for row in variation_rows), "requirement": "variation produces the second-order coefficient equation", "evidence": OUTPUTS["variation"].name},
    {"validation_id": "VAL3024_04_lambda_map", "passed": any(row["map_id"] == "LCM3024_0_general" and "sigma_H" in row["formula"] and "f_psi" in row["formula"] for row in coefficient_rows), "requirement": "lambda_N_core map is recorded", "evidence": OUTPUTS["coefficient"].name},
    {"validation_id": "VAL3024_05_zero_condition", "passed": any(row["map_id"] == "LCM3024_0_general" and "2 sigma_H/A_source + f_psi = 0" in row["zero_condition"] for row in coefficient_rows), "requirement": "zero condition is explicit", "evidence": OUTPUTS["coefficient"].name},
    {"validation_id": "VAL3024_06_bound_translation", "passed": any(row["bound_id"] == "BND3024_0_general_combo" and float(row["numeric_bound"]) == BETA_BOUND_ABS for row in bound_rows), "requirement": "beta comparator bound translates to the kinetic/coframe coefficient combination", "evidence": OUTPUTS["bound"].name},
    {"validation_id": "VAL3024_07_parent_values_missing", "passed": any(row["gate_id"] == "GATE3024_3_parent_signed" and not boolish(row["result"]) for row in gate_rows), "requirement": "parent coefficients remain unsigned", "evidence": OUTPUTS["gates"].name},
    {"validation_id": "VAL3024_08_claims_blocked", "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows) and all(not boolish(row.get("valid_for_claim")) for row in claim_rows), "requirement": "all rows remain nonclaim/private-control rows", "evidence": "all 3024 generated ledgers"},
    {"validation_id": "VAL3024_09_missing_markers_nonclaim", "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))), "requirement": "rows with MISSING markers are never valid_for_claim=true", "evidence": "all 3024 generated ledgers"},
    {"validation_id": "VAL3024_10_branch_copies_exist", "passed": all(boolish(row["exists"]) for row in branch_rows), "requirement": "branch copies and acquisition queue exist", "evidence": OUTPUTS["branches"].name},
    {"validation_id": "VAL3024_11_outputs_scoped", "passed": all(under(path, ROOT) for path in all_generated), "requirement": "no generated file is outside post-checkpoint-work", "evidence": "generated path scope check"},
    {"validation_id": "VAL3024_12_formalization_not_targeted", "passed": not any(under(path, FORMALIZATION) for path in all_generated), "requirement": "formalization-workbench is not modified by this checkpoint", "evidence": "output target list excludes formalization-workbench"},
    {"validation_id": "VAL3024_13_next_target_selected", "passed": next_rows[0]["target_doc"].startswith("3025-Y5-R2FR-parent-sign-sigmaH-fpsi"), "requirement": "next target selects parent signing of sigma_H/f_psi cancellation or bound rows", "evidence": OUTPUTS["next"].name},
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3024_99_overall",
        "passed": overall_pass,
        "requirement": "all 3024 validation checks pass",
        "evidence": "aggregate of VAL3024_00 through VAL3024_13",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3024 - Minimal Hcore Action Ansatz Or LambdaN Core Numeric Intake under AX1090

Status: `Y5_R2FR_3024_conditional_Hcore_ansatz_derives_lambdaN_core_map_parent_coefficients_unsigned_3025_next`

## Verdict

3024 takes the derivation route rather than immediately treating `lambda_N_core` as a dead numeric input.

The useful leap is this:

`lambda_N_core` is not just a random missing beta coefficient. In the smallest local log-lapse action that could own it, it is controlled by a coupling/coframe cancellation:

`lambda_N_core/A_source^2 = -sigma_H/(2 A_source)-f_psi/4`.

Therefore

`lambda_N_core=0`

requires

`2 sigma_H/A_source + f_psi = 0`.

This is the cleanest current form of the local beta wound.

If the parent MTS action derives that cancellation, the core log-lapse beta route closes. If it does not, the beta residual is bounded by

`abs(sigma_H/(2 A_source)+f_psi/4) <= {BETA_BOUND_ABS}`.

So yes: the coupling really is the key here. But this checkpoint does **not** claim the cancellation. `A_source`, `sigma_H`, `f_psi`, exterior source silence, boundary/reference fixing, and the observed PPN gauge map are still not parent-signed in the corpus.

## Meaning Of The New Coefficients

- `A_source`: first-order source-normalized log-lapse coefficient, `psi_N=A_source W/c^2+...`.
- `sigma_H`: first-order coframe/measure/projection drift in the kinetic density, `K_N^{{ij}} ~ delta^{{ij}}(1+sigma_H W/c^2+...)`.
- `f_psi`: explicit log-lapse kinetic coupling slope, `K_N^{{ij}} ~ delta^{{ij}}(1+f_psi psi_N+...)`.

The flat/silent-coframe special case is only a special case:

`sigma_H=0 -> lambda_N_core/A_source^2=-f_psi/4`.

The more GR-like-looking cancellation is:

`A_source=1, sigma_H=1, f_psi=-2 -> lambda_N_core=0`.

That row is reference morphology only, not an MTS proof.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Minimal Hcore Ansatz

{md_table(ansatz_rows, ["ansatz_id", "object", "mathematical_form", "role", "status", "missing_for_claim"])}

## Variation Derivation

{md_table(variation_rows, ["derivation_id", "statement", "formula", "assumptions", "result", "claim_status"])}

## LambdaN Core Coefficient Map

{md_table(coefficient_rows, ["map_id", "symbol", "formula", "zero_condition", "interpretation", "current_status", "needed_for_claim"])}

## Bound Translation

{md_table(bound_rows, ["bound_id", "quantity", "beta_projection", "bound", "units", "current_status"])}

## Closure Gates

{md_table(gate_rows, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "rationale", "consequence"])}

## Next Target

{md_table(next_rows, ["next_id", "target_doc", "target_script", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["ansatz"]}`
- `{OUTPUTS["variation"]}`
- `{OUTPUTS["coefficient"]}`
- `{OUTPUTS["bound"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["ansatz_copy"]}`
- `{BRANCH_OUTPUTS["coefficient_copy"]}`
- `{BRANCH_OUTPUTS["bound_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No beta pass until `A_source`, `sigma_H`, and `f_psi` are parent-signed or strictly bounded.
- No `lambda_N_core=0` claim from the ansatz alone.
- No flat-coframe assumption unless the parent readout/coframe map signs `sigma_H=0`.
- No GR/EH import as MTS proof.
- No orbital-`GM` denominator.
- No hidden cancellation across residual families.
- No local-GR/Newton claim from core beta alone.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
