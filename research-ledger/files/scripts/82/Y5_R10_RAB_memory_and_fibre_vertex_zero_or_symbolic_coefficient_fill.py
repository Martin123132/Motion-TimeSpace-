from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1346"
TITLE = "1346-Y5-R10-RAB-memory-and-fibre-vertex-zero-or-symbolic-coefficient-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
MEMORY_ZERO_PATH = OUT_DIR / f"{PACK_ID}_MEMORY_VERTEX_ZERO_ATTEMPT.csv"
FIBRE_ZERO_PATH = OUT_DIR / f"{PACK_ID}_FIBRE_VERTEX_ZERO_ATTEMPT.csv"
COEFF_PACK_PATH = OUT_DIR / f"{PACK_ID}_SYMBOLIC_COEFFICIENT_PACK.csv"
RUNNER_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_INPUT_CONTRACT.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1346_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def falsey(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "n", ""}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not falsey(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not falsey(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1346*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1346_0_1345_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1345_NEXT_TARGET.csv",
            "needle": "NEXT1345_0_1346",
            "role": "selected 1346 target",
        },
        {
            "source_id": "SRC1346_1_1345_matrix",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1345_GENERATOR_VERTEX_MATRIX.csv",
            "needle": "VM1345_4_memory_class_scalar",
            "role": "memory/fibre vertex matrix",
        },
        {
            "source_id": "SRC1346_2_1345_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1345_SOURCE_CHARGE_RUNNER_INPUTS.csv",
            "needle": "QIN1345_5_5_finite_fibre_spectrum",
            "role": "1345 source-charge runner skeleton",
        },
        {
            "source_id": "SRC1346_3_1343_law",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1343_PARENT_COEFFICIENT_LAW.csv",
            "needle": "LAW1343_1_low_momentum_limit",
            "role": "symbolic integrated-out coefficient law",
        },
        {
            "source_id": "SRC1346_4_1344_charge",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1344_RETAINED_SCALAR_SOURCE_CHARGE_TEMPLATE.csv",
            "needle": "QX1344_0_generic_template",
            "role": "retained source-charge law",
        },
        {
            "source_id": "SRC1346_5_966_generators",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv",
            "needle": "GE966_5_finite_fibre_spectrum",
            "role": "memory/fibre generator blockers",
        },
        {
            "source_id": "SRC1346_6_969_minimal_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_969_MINIMAL_ACTION_CONSTRUCTION_TARGETS.csv",
            "needle": "MACT969_3_no_integrated_out_tower",
            "role": "minimal action construction targets",
        },
        {
            "source_id": "SRC1346_7_1345_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1345_VALIDATION.csv",
            "needle": "VAL1345_9_overall",
            "role": "1345 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    memory_zero = [
        {
            "attempt_id": "MEM1346_0_absent_or_readout",
            "route": "memory/class variable absent or readout-only",
            "required_statement": "theta/M is not an argument of S_parent, or is a readout map only",
            "current_evidence": "GE966_4 keeps memory/class scalar live",
            "status": "NOT_DERIVED",
            "consequence": "memory vertex cannot be zeroed by domain alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "MEM1346_1_branch_extremum",
            "route": "F'_M(M0)=0 and A'_M(M0)=0",
            "required_statement": "local branch sits at a parent-signed extremum of both gravitational prefactor and matter-frame coupling",
            "current_evidence": "no parent potential or extremum certificate for M/theta exists",
            "status": "UNSIGNED",
            "consequence": "B_mem and C_mem remain symbolic",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "MEM1346_2_positive_operator",
            "route": "positive local operator",
            "required_statement": "L_M = -Z_mem nabla^2 + M_mem^2 with Z_mem>0 and M_mem^2>=0",
            "current_evidence": "MACT969_0 defines target shape but parent Z_mem/M_mem^2 are missing",
            "status": "SHAPE_ONLY",
            "consequence": "operator positivity cannot be used as a theorem-zero yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "MEM1346_3_source_boundary_silence",
            "route": "J_mem=0 and Q_boundary_mem=0",
            "required_statement": "ordinary source, body charge, chi_D wall, and boundary flux vanish in the compact local branch",
            "current_evidence": "1344 shows J_X=0 is insufficient unless B_X=C_X=0 too",
            "status": "UNSIGNED",
            "consequence": "body-source scalar charge remains retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "MEM1346_4_verdict",
            "route": "memory vertex zero",
            "required_statement": "B_mem=C_mem=J_mem=Q_boundary_mem=0 plus positive operator",
            "current_evidence": "absence, extremum, source, and boundary clauses are not parent-signed",
            "status": "MEMORY_VERTEX_ZERO_NOT_DERIVED_SYMBOLIC_PACK_SELECTED",
            "consequence": "memory branch remains direct R10/PPN scalar pressure row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    fibre_zero = [
        {
            "attempt_id": "FIB1346_0_unique_h0",
            "route": "unique source-independent fibre vacuum",
            "required_statement": "delta S/delta h=0 has one gapped solution h0 independent of matter/source/body data",
            "current_evidence": "GE966_5 says no parent fibre potential, mass gap, or uniqueness theorem is signed",
            "status": "NOT_DERIVED",
            "consequence": "fibre fluctuations cannot be collapsed to constants",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FIB1346_1_no_curvature_vertex",
            "route": "no h R vertex",
            "required_statement": "B_h = delta^2 S_parent/(delta h delta R_obs)=0 for all fibre fluctuations",
            "current_evidence": "no parent vertex inventory supplies B_h=0",
            "status": "UNSIGNED",
            "consequence": "integrating h can generate R L_h^-1 R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FIB1346_2_matter_blindness",
            "route": "h-blind matter functor",
            "required_statement": "C_h=0 and matter action has no fibre-dependent masses/clocks/source maps",
            "current_evidence": "GE966_5 explicitly depends on matter blindness, which is not signed",
            "status": "UNSIGNED",
            "consequence": "composition/WEP/source-normalization charge remains possible",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FIB1346_3_gap_operator",
            "route": "gapped fibre operator",
            "required_statement": "L_h = -Z_h nabla^2 + M_h^2 or discrete gapped stiffness with Z_h/M_h^2 sourced",
            "current_evidence": "Z_h and M_h^2 are not parent-extracted",
            "status": "SHAPE_ONLY",
            "consequence": "finite fibre range cannot be bounded or zeroed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FIB1346_4_verdict",
            "route": "fibre vertex zero",
            "required_statement": "unique h0, B_h=C_h=J_h=0, gapped operator, and projection flux silence",
            "current_evidence": "all decisive clauses remain unsigned",
            "status": "FIBRE_VERTEX_ZERO_NOT_DERIVED_SYMBOLIC_PACK_SELECTED",
            "consequence": "finite fibre branch remains direct R10/WEP/source-normalization pressure row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coeff_pack = [
        {
            "pack_id": "COEFF1346_M_Z",
            "mode": "memory_class_scalar",
            "symbol": "Z_mem",
            "definition": "kinetic/operator normalization in L_mem",
            "required_units": "parent_defined",
            "current_value": "MISSING_PARENT_INPUT",
            "role": "lambda_mem = sqrt(Z_mem/M2_mem)",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_M_M2",
            "mode": "memory_class_scalar",
            "symbol": "M2_mem",
            "definition": "mass/gap term of the memory/class scalar",
            "required_units": "inverse_length_squared_or_parent_equivalent",
            "current_value": "MISSING_PARENT_INPUT",
            "role": "sets finite range and positivity",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_M_B",
            "mode": "memory_class_scalar",
            "symbol": "B_mem",
            "definition": "curvature-linear vertex coefficient multiplying delta M R_obs",
            "required_units": "parent_defined_to_make_action_dimensionless",
            "current_value": "MISSING_NO_XR_VERTEX_OR_VALUE",
            "role": "sources R L^-1 R and R2/fR residual if nonzero",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_M_C",
            "mode": "memory_class_scalar",
            "symbol": "C_mem",
            "definition": "matter/source trace vertex in same observed frame",
            "required_units": "parent_defined",
            "current_value": "MISSING_NO_MATTER_VERTEX_OR_VALUE",
            "role": "sets body/source charge and PPN/WEP response",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_M_J",
            "mode": "memory_class_scalar",
            "symbol": "J_mem",
            "definition": "non-curvature/non-matter memory source in local branch",
            "required_units": "same_as_L_mem_times_mem_field",
            "current_value": "MISSING_SOURCE_SILENCE_THEOREM",
            "role": "independent local scalar source",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_M_QB",
            "mode": "memory_class_scalar",
            "symbol": "Q_boundary_mem",
            "definition": "boundary/projection/body-surface scalar charge contribution",
            "required_units": "source_charge_units",
            "current_value": "MISSING_BOUNDARY_NO_HAIR",
            "role": "exterior scalar tail even when bulk source is quiet",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_M_LAMBDA_ALPHA",
            "mode": "memory_class_scalar",
            "symbol": "lambda_mem;alpha_mem",
            "definition": "range and fifth-force amplitude",
            "required_units": "length;dimensionless",
            "current_value": "DERIVED_FORMULA_ONLY",
            "role": "lambda_mem=sqrt(Z_mem/M2_mem); alpha_mem requires source/test charge normalization",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_Z",
            "mode": "finite_fibre_spectrum",
            "symbol": "Z_h",
            "definition": "fibre fluctuation kinetic/stiffness normalization",
            "required_units": "parent_defined",
            "current_value": "MISSING_PARENT_INPUT",
            "role": "lambda_h = sqrt(Z_h/M2_h) if continuum massive approximation applies",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_M2",
            "mode": "finite_fibre_spectrum",
            "symbol": "M2_h",
            "definition": "fibre mass/gap/stiffness eigenvalue",
            "required_units": "inverse_length_squared_or_discrete_gap_equivalent",
            "current_value": "MISSING_FIBRE_GAP",
            "role": "sets finite range or decoupling",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_B",
            "mode": "finite_fibre_spectrum",
            "symbol": "B_h",
            "definition": "curvature-linear vertex coefficient multiplying delta h R_obs",
            "required_units": "parent_defined_to_make_action_dimensionless",
            "current_value": "MISSING_NO_FIBRE_CURVATURE_VERTEX_OR_VALUE",
            "role": "sources fibre-mediated R2/fR-like residual if nonzero",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_C",
            "mode": "finite_fibre_spectrum",
            "symbol": "C_h",
            "definition": "matter/fibre vertex through clocks, masses, source maps, or composition",
            "required_units": "parent_defined",
            "current_value": "MISSING_H_BLIND_MATTER_FUNCTOR",
            "role": "sets WEP/composition/source-normalization charge",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_J",
            "mode": "finite_fibre_spectrum",
            "symbol": "J_h",
            "definition": "source dependence of fibre solution h0 or fluctuations",
            "required_units": "same_as_L_h_times_h_field",
            "current_value": "MISSING_SOURCE_INDEPENDENT_H0_PROOF",
            "role": "tests whether fibre spectrum renormalizes constants only",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_QB",
            "mode": "finite_fibre_spectrum",
            "symbol": "Q_boundary_h",
            "definition": "projection/boundary flux from fibre sector",
            "required_units": "source_charge_units",
            "current_value": "MISSING_PROJECTION_FLUX_CHECK",
            "role": "possible exterior/local residual even when bulk fibre is gapped",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "pack_id": "COEFF1346_H_LAMBDA_ALPHA",
            "mode": "finite_fibre_spectrum",
            "symbol": "lambda_h;alpha_h",
            "definition": "range and fifth-force/composition amplitude for fibre branch",
            "required_units": "length;dimensionless",
            "current_value": "DERIVED_FORMULA_ONLY",
            "role": "lambda_h from gap; alpha_h requires source/test charge and matter map",
            "ready_for_runner": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_contract = [
        {
            "contract_id": "RUNIN1346_0_memory",
            "mode": "memory_class_scalar",
            "field_equation": "(-Z_mem nabla^2 + M2_mem) M = B_mem R_obs + C_mem T + J_mem + boundary",
            "source_charge": "Q_mem[body]=integral_body W_mem(B_mem R_obs + C_mem T + J_mem)+Q_boundary_mem",
            "range_formula": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "amplitude_formula": "alpha_mem requires source/test charge normalization and frame map",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_SYMBOLIC_MEMORY_PACK_ONLY",
            "missing_for_execution": "Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;W_mem;screening;source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "RUNIN1346_1_fibre",
            "mode": "finite_fibre_spectrum",
            "field_equation": "(-Z_h nabla^2 + M2_h) h = B_h R_obs + C_h T + J_h + boundary",
            "source_charge": "Q_h[body]=integral_body W_h(B_h R_obs + C_h T + J_h)+Q_boundary_h",
            "range_formula": "lambda_h=sqrt(Z_h/M2_h) or discrete gap analogue",
            "amplitude_formula": "alpha_h requires fibre source/test charge and matter map",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_SYMBOLIC_FIBRE_PACK_ONLY",
            "missing_for_execution": "Z_h;M2_h;B_h;C_h;J_h;Q_boundary_h;W_h;screening;source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "RUNIN1346_VERDICT",
            "mode": "memory_and_fibre",
            "field_equation": "both direct scalar pressure rows remain symbolic",
            "source_charge": "neither Q_mem nor Q_h is zero-signed or numeric",
            "range_formula": "blocked",
            "amplitude_formula": "blocked",
            "accepted_for_scoring": False,
            "verdict": "DIRECT_SCALAR_PRESSURE_PACKS_COMPLETE_BUT_NONEXECUTABLE",
            "missing_for_execution": "parent zero theorem or numeric symbolic-pack values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gate = [
        {
            "gate_id": "GATE1346_0_memory_zero",
            "claim": "memory/class scalar does not source local scalar residuals",
            "allowed_if": "MEM1346_4 becomes theorem-zero with B_mem=C_mem=J_mem=Q_boundary_mem=0 and positive operator",
            "current_status": "BLOCKED",
            "reason": "MEM1346_4 selected symbolic pack, not theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1346_1_fibre_zero",
            "claim": "finite fibre spectrum renormalizes constants only",
            "allowed_if": "FIB1346_4 becomes theorem-zero with unique source-independent h0 and no vertices",
            "current_status": "BLOCKED",
            "reason": "FIB1346_4 selected symbolic pack, not theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1346_2_R10_PPN_runner",
            "claim": "memory/fibre finite scalar branch can be compared to R10/PPN",
            "allowed_if": "runner contract rows have numeric sourced Z/M/B/C/J/boundary/source maps",
            "current_status": "BLOCKED",
            "reason": "packs are complete symbolic templates only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1346_0_memory",
            "decision": "memory/class scalar zero is not derived",
            "because": "absence, branch extremum, source silence, and boundary silence remain unsigned",
            "effect": "memory coefficient pack retained as high-priority nonclaim input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1346_1_fibre",
            "decision": "finite fibre zero is not derived",
            "because": "unique gapped h0, no curvature vertex, and h-blind matter functor remain unsigned",
            "effect": "fibre coefficient pack retained as high-priority nonclaim input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1346_2_next",
            "decision": "next move should search for an owner of the missing coefficients",
            "because": "1346 has complete symbolic packs but no parent source path or numeric/theorem-zero value",
            "effect": "target branch-extremum/symmetry/source-owner search before data bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1346_0_1347",
            "target_file": "1347-Y5-R10-RAB-memory-fibre-coefficient-owner-search-or-explicit-closure.md",
            "target_script": "scripts/Y5_R10_RAB_memory_fibre_coefficient_owner_search_or_explicit_closure.py",
            "task": "search the parent corpus for an owner of B_mem/C_mem/Z_mem/M2_mem and B_h/C_h/Z_h/M2_h, especially branch-extremum, symmetry, matter-blindness, and mass-gap mechanisms; otherwise mark the direct scalar branch as explicit closure/nonclaim residual",
            "success_condition": "a sourced owner for at least one memory/fibre coefficient family, or a sharper closure ledger saying exactly which coefficient must be postulated",
            "do_not": "do not run R10/PPN scoring from symbolic-only packs; do not infer zeros from missing terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        memory_zero,
        fibre_zero,
        coeff_pack,
        runner_contract,
        claim_gate,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(MEMORY_ZERO_PATH, memory_zero)
    write_csv(FIBRE_ZERO_PATH, fibre_zero)
    write_csv(COEFF_PACK_PATH, coeff_pack)
    write_csv(RUNNER_CONTRACT_PATH, runner_contract)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    memory_not_zero = memory_zero[-1]["status"] == "MEMORY_VERTEX_ZERO_NOT_DERIVED_SYMBOLIC_PACK_SELECTED"
    fibre_not_zero = fibre_zero[-1]["status"] == "FIBRE_VERTEX_ZERO_NOT_DERIVED_SYMBOLIC_PACK_SELECTED"
    required_symbols = {
        "Z_mem",
        "M2_mem",
        "B_mem",
        "C_mem",
        "J_mem",
        "Q_boundary_mem",
        "lambda_mem;alpha_mem",
        "Z_h",
        "M2_h",
        "B_h",
        "C_h",
        "J_h",
        "Q_boundary_h",
        "lambda_h;alpha_h",
    }
    pack_symbols = {str(row["symbol"]) for row in coeff_pack}
    pack_complete = required_symbols.issubset(pack_symbols)
    runner_rejects = runner_contract[-1]["verdict"] == "DIRECT_SCALAR_PRESSURE_PACKS_COMPLETE_BUT_NONEXECUTABLE"
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and memory_not_zero
        and fibre_not_zero
        and pack_complete
        and runner_rejects
        and claims_blocked
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1346_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1346_1_memory_not_zero",
            "memory vertex zero theorem is not promoted",
            memory_not_zero,
            memory_zero[-1]["status"],
        ),
        validation_row(
            "VAL1346_2_fibre_not_zero",
            "fibre vertex zero theorem is not promoted",
            fibre_not_zero,
            fibre_zero[-1]["status"],
        ),
        validation_row(
            "VAL1346_3_coefficient_pack_complete",
            "memory and fibre symbolic coefficient packs include required symbols",
            pack_complete,
            ";".join(sorted(pack_symbols)),
        ),
        validation_row(
            "VAL1346_4_runner_rejects",
            "runner contract rejects symbolic-only packs",
            runner_rejects,
            runner_contract[-1]["verdict"],
        ),
        validation_row(
            "VAL1346_5_claims_blocked",
            "memory zero, fibre zero, and R10/PPN runner claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1346_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1346_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1346_8_next_target_1347",
            "next target routes to memory/fibre coefficient owner search",
            next_target[0]["next_id"] == "NEXT1346_0_1347",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1346_9_overall",
            "overall 1346 validation",
            overall_ok,
            "1346 keeps memory/fibre zero unclaimed and creates complete symbolic nonclaim coefficient packs",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1346 does not zero the direct scalar-pressure rows. Memory/class and finite-fibre vertices remain unproven, but both are now converted into complete symbolic nonclaim coefficient packs.

**Main progress:** the two dangerous rows are no longer vague. Memory now needs `Z_mem`, `M2_mem`, `B_mem`, `C_mem`, `J_mem`, `Q_boundary_mem`; fibre now needs `Z_h`, `M2_h`, `B_h`, `C_h`, `J_h`, `Q_boundary_h`, plus source/test charge normalizations before R10/PPN scoring.

**Decision:** move to `1347`: search for an actual parent owner of these coefficients, especially a branch-extremum, symmetry, matter-blindness, or mass-gap mechanism. No R10/PPN/local-GR claim is made from symbolic packs.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Memory Vertex Zero Attempt
{markdown_table(memory_zero, ["attempt_id", "route", "required_statement", "current_evidence", "status", "consequence", "valid_for_claim", "claim_allowed"])}

## Fibre Vertex Zero Attempt
{markdown_table(fibre_zero, ["attempt_id", "route", "required_statement", "current_evidence", "status", "consequence", "valid_for_claim", "claim_allowed"])}

## Symbolic Coefficient Pack
{markdown_table(coeff_pack, ["pack_id", "mode", "symbol", "definition", "required_units", "current_value", "role", "ready_for_runner", "valid_for_claim", "claim_allowed"])}

## Runner Input Contract
{markdown_table(runner_contract, ["contract_id", "mode", "field_equation", "source_charge", "range_formula", "amplitude_formula", "accepted_for_scoring", "verdict", "missing_for_execution", "valid_for_claim", "claim_allowed"])}

## Claim Gate
{markdown_table(claim_gate, ["gate_id", "claim", "allowed_if", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision_ledger, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
