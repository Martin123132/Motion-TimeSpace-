from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1345"
TITLE = "1345-Y5-R10-RAB-parent-vertex-inventory-by-generator-or-source-charge-runner-inputs"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
VERTEX_MATRIX_PATH = OUT_DIR / f"{PACK_ID}_GENERATOR_VERTEX_MATRIX.csv"
RUNNER_INPUTS_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_CHARGE_RUNNER_INPUTS.csv"
CLASSIFICATION_PATH = OUT_DIR / f"{PACK_ID}_ZERO_OR_RETAINED_CLASSIFICATION.csv"
OBS_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_OBSERVABLE_PRIORITY_QUEUE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1345_VALIDATION.csv"


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
    return [path for path in FORMALIZATION.rglob("*1345*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1345_0_1344_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1344_NEXT_TARGET.csv",
            "needle": "NEXT1344_0_1345",
            "role": "selected 1345 target",
        },
        {
            "source_id": "SRC1345_1_1344_vertex",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1344_VERTEX_ALGEBRA.csv",
            "needle": "VERT1344_0_definitions",
            "role": "B_X/C_X vertex algebra",
        },
        {
            "source_id": "SRC1345_2_1344_charge",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1344_RETAINED_SCALAR_SOURCE_CHARGE_TEMPLATE.csv",
            "needle": "QX1344_0_generic_template",
            "role": "retained source-charge template",
        },
        {
            "source_id": "SRC1345_3_1344_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1344_NO_XR_VERTEX_THEOREM_ATTEMPT.csv",
            "needle": "NXV1344_6_verdict",
            "role": "no-XR theorem failure",
        },
        {
            "source_id": "SRC1345_4_GE966",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv",
            "needle": "GE966_7_verdict",
            "role": "live generator list",
        },
        {
            "source_id": "SRC1345_5_705_prefactors",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
            "needle": "VPC705_9_verdict",
            "role": "variable prefactor channels",
        },
        {
            "source_id": "SRC1345_6_703_coupling_lock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
            "needle": "PAL703_8_verdict",
            "role": "parent coupling lock failure",
        },
        {
            "source_id": "SRC1345_7_707_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv",
            "needle": "SCZ707_8_verdict",
            "role": "scalar/class prefactor zero failure",
        },
        {
            "source_id": "SRC1345_8_1343_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1343_FINITE_SCALAR_MAP_TEMPLATE.csv",
            "needle": "FSM1343_0_required_mode_row",
            "role": "finite scalar map requirements",
        },
        {
            "source_id": "SRC1345_9_1344_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1344_VALIDATION.csv",
            "needle": "VAL1344_9_overall",
            "role": "1344 pass gate",
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

    vertex_matrix = [
        {
            "matrix_id": "VM1345_0_readout_projector",
            "ge966_id": "GE966_0_readout_projector",
            "generator": "post-readout projector",
            "B_X_status": "ZERO_IF_READOUT_ONLY_DOMAIN_SIGNED_ELSE_UNOWNED",
            "C_X_status": "ZERO_IF_NO_REDUCED_ACTION_BACKREACTION_SIGNED_ELSE_UNOWNED",
            "Z_X_status": "not_applicable_if_readout_map_only",
            "M_X2_status": "not_applicable_if_readout_map_only",
            "J_X_status": "reduced_action_backreaction_possible_until_domain_lock",
            "boundary_charge_status": "not_primary_boundary_charge",
            "observable_links": "R0/R11 closure; hidden projector source",
            "classification": "CLOSURE_ONLY_UNTIL_PARENT_DOMAIN_SIGNED",
            "next_evidence_needed": "parent action domain excludes P_read and forbids varying readout-selected reduced actions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "VM1345_1_species_constants",
            "ge966_id": "GE966_1_species_constants",
            "generator": "species/source constants",
            "B_X_status": "not_curvature_vertex_primary",
            "C_X_status": "MISSING_NO_SOURCE_ONLY_SPECIES_SLOT_THEOREM",
            "Z_X_status": "not_applicable_for_constant_slot",
            "M_X2_status": "not_applicable_for_constant_slot",
            "J_X_status": "source_only_prefactor_w_A_live",
            "boundary_charge_status": "not_primary_boundary_charge",
            "observable_links": "WEP/source-normalization/clocks/composition",
            "classification": "RETAINED_SOURCE_NORMALIZATION_SYMBOLIC",
            "next_evidence_needed": "one total matter functor with no species-only source prefactor slot",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "VM1345_2_relative_domain_class",
            "ge966_id": "GE966_2_relative_domain_class",
            "generator": "relative boundary/domain class",
            "B_X_status": "POSSIBLE_DOMAIN_PREFATOR_F(D)R_UNTIL_TOPOLOGY_ZERO",
            "C_X_status": "POSSIBLE_DOMAIN_SOURCE_COUPLING_UNTIL_SELECTOR_DERIVED",
            "Z_X_status": "not_declared",
            "M_X2_status": "not_declared",
            "J_X_status": "boundary_exchange_source_possible",
            "boundary_charge_status": "MISSING_RELATIVE_COHOMOLOGY_AND_NO_DEFECT_PROOF",
            "observable_links": "PPN/source normalization/orbital/domain residuals",
            "classification": "RETAINED_BOUNDARY_SOURCE_CHARGE_SYMBOLIC",
            "next_evidence_needed": "H_rel(D,dD)=0/no-defect plus zero boundary exchange theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "VM1345_3_domain_selector",
            "ge966_id": "GE966_3_domain_selector",
            "generator": "chi_D/domain selector",
            "B_X_status": "POSSIBLE_SELECTOR_PREFATOR_F(chi_D)R_UNTIL_TOPOLOGICAL",
            "C_X_status": "POSSIBLE_DOMAIN_STRESS_OR_SOURCE_UNTIL_BIANCHI_SAFE",
            "Z_X_status": "not_declared_auxiliary_or_topological",
            "M_X2_status": "not_declared_auxiliary_or_topological",
            "J_X_status": "epsilon_threshold_origin_open",
            "boundary_charge_status": "MISSING_SELECTOR_BOUNDARY_NO_HAIR",
            "observable_links": "preferred-frame/domain/source-normalization/local-FLRW split",
            "classification": "RETAINED_SELECTOR_SOURCE_CHARGE_SYMBOLIC",
            "next_evidence_needed": "first-class/topological selector with no local stress and no boundary exchange",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "VM1345_4_memory_class_scalar",
            "ge966_id": "GE966_4_memory_class_scalar",
            "generator": "memory/class scalar",
            "B_X_status": "MISSING_NO_XR_VERTEX_OR_FPRIME_ZERO",
            "C_X_status": "MISSING_NO_MATTER_FRAME_SOURCE_VERTEX",
            "Z_X_status": "MISSING_PARENT_OPERATOR_NORMALIZATION",
            "M_X2_status": "MISSING_PARENT_GAP_OR_MASS",
            "J_X_status": "MISSING_SOURCE_SILENCE_AND_BODY_CHARGE",
            "boundary_charge_status": "MISSING_ZERO_BOUNDARY_DATA_OR_TOPOLOGICAL_FLUX",
            "observable_links": "R10 finite scalar; PPN gamma/beta; clocks; Gdot; R11 non-EH prefactor",
            "classification": "RETAINED_SCALAR_SOURCE_CHARGE_SYMBOLIC_HIGH_PRIORITY",
            "next_evidence_needed": "B_X=C_X=J_X=Q_boundary=0 theorem or numeric Z_X/M_X2/source-charge row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "VM1345_5_finite_fibre_spectrum",
            "ge966_id": "GE966_5_finite_fibre_spectrum",
            "generator": "finite-cell fibre spectrum",
            "B_X_status": "MISSING_NO_FIBRE_CURVATURE_VERTEX",
            "C_X_status": "MISSING_H_BLIND_MATTER_FUNCTOR",
            "Z_X_status": "MISSING_FIBRE_KINETIC_OR_STIFFNESS_NORMALIZATION",
            "M_X2_status": "MISSING_FIBRE_GAP_UNIQUENESS_THEOREM",
            "J_X_status": "MISSING_SOURCE_INDEPENDENT_H0_PROOF",
            "boundary_charge_status": "not_primary_but_projection_flux_unchecked",
            "observable_links": "R10 finite scalar; WEP/composition; source-normalization; local constants",
            "classification": "RETAINED_FIBRE_SOURCE_CHARGE_SYMBOLIC_HIGH_PRIORITY",
            "next_evidence_needed": "unique gapped source-independent h0 and no matter/curvature vertex to fluctuations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "matrix_id": "VM1345_6_orientation_time_arrow",
            "ge966_id": "GE966_6_orientation_time_arrow",
            "generator": "orientation/time-arrow marker",
            "B_X_status": "POSSIBLE_CONNECTION_OR_PSEUDOSCALAR_CURVATURE_VERTEX_UNCHECKED",
            "C_X_status": "POSSIBLE_MATTER_PARITY_OR_CLOCK_VERTEX_UNCHECKED",
            "Z_X_status": "not_declared_if_global_orientation_else_missing_dynamic_operator",
            "M_X2_status": "not_declared_if_global_orientation_else_missing_gap",
            "J_X_status": "dynamic_arrow_source_not_excluded",
            "boundary_charge_status": "orientation_boundary_or_torsion_flux_unchecked",
            "observable_links": "preferred-frame; torsion/nonmetricity; parity/time-asymmetry; PPN",
            "classification": "RETAINED_CONNECTION_OR_PREFERRED_FRAME_SYMBOLIC",
            "next_evidence_needed": "orientation contained in observed coframe/spin structure or global nondynamical datum",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_inputs = [
        {
            "input_id": f"QIN1345_{index}_{row['ge966_id'].replace('GE966_', '')}",
            "matrix_id": row["matrix_id"],
            "generator": row["generator"],
            "equation": "L_X X = B_X R_obs + C_X T + J_X + boundary",
            "B_X": row["B_X_status"],
            "C_X": row["C_X_status"],
            "Z_X": row["Z_X_status"],
            "M_X2": row["M_X2_status"],
            "J_X": row["J_X_status"],
            "Q_boundary": row["boundary_charge_status"],
            "lambda_X": "NOT_EXECUTABLE_UNTIL_Z_X_AND_M_X2_NUMERIC",
            "alpha_X": "NOT_EXECUTABLE_UNTIL_SOURCE_AND_TEST_CHARGES_NORMALIZED",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_SYMBOLIC_OR_CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(vertex_matrix)
    ]
    runner_inputs.append(
        {
            "input_id": "QIN1345_VERDICT",
            "matrix_id": "all_generators",
            "generator": "all live GE966 generators",
            "equation": "source-charge runner requires numeric theorem-zero or numeric retained branch rows",
            "B_X": "no row claim-ready",
            "C_X": "no row claim-ready",
            "Z_X": "no scalar row numeric",
            "M_X2": "no scalar row numeric",
            "J_X": "not source-signed",
            "Q_boundary": "not zero-signed",
            "lambda_X": "blocked",
            "alpha_X": "blocked",
            "accepted_for_scoring": False,
            "verdict": "ALL_GENERATOR_VERTEX_ROWS_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    classification = [
        {
            "class_id": "CLASS1345_0_closure_only",
            "row_group": "readout_projector",
            "meaning": "row can vanish by parent action domain, but current corpus has only a conditional schema lock",
            "rows": "VM1345_0_readout_projector",
            "current_status": "CLOSURE_ONLY_NOT_THEOREM",
            "claim_effect": "cannot support local-GR/R2-fR zero claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1345_1_source_normalization",
            "row_group": "species_constants",
            "meaning": "not an R2/fR scalaron by itself, but can break universal source coupling",
            "rows": "VM1345_1_species_constants",
            "current_status": "RETAINED_SYMBOLIC_SOURCE_NORMALIZATION",
            "claim_effect": "routes to WEP/clock/source-normalization gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1345_2_boundary_domain",
            "row_group": "relative_domain_class;domain_selector",
            "meaning": "domain/topology/projector generators can source boundary charge or variable EH prefactors",
            "rows": "VM1345_2_relative_domain_class;VM1345_3_domain_selector",
            "current_status": "RETAINED_SYMBOLIC_BOUNDARY_DOMAIN_CHARGE",
            "claim_effect": "routes to PPN/source/orbital/domain residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1345_3_direct_scalar_pressure",
            "row_group": "memory_class_scalar;finite_fibre_spectrum",
            "meaning": "these are the direct R2/fR/R10 pressure rows because B_X/C_X/Z_X/M_X2 can define a finite scalar branch",
            "rows": "VM1345_4_memory_class_scalar;VM1345_5_finite_fibre_spectrum",
            "current_status": "RETAINED_SYMBOLIC_SCALAR_SOURCE_CHARGE_HIGH_PRIORITY",
            "claim_effect": "blocks R2/fR zero and local EH until theorem-zero or finite-branch bounds exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "class_id": "CLASS1345_4_connection_preferred_frame",
            "row_group": "orientation_time_arrow",
            "meaning": "not the first R2/fR scalar target, but can re-enter as torsion/preferred-frame PPN residual",
            "rows": "VM1345_6_orientation_time_arrow",
            "current_status": "RETAINED_SYMBOLIC_CONNECTION_OR_PREFERRED_FRAME",
            "claim_effect": "routes to torsion/nonmetricity/preferred-frame gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    obs_priority = [
        {
            "priority": 1,
            "target_generator": "memory/class scalar",
            "why_first": "directly owns B_X X R and finite scalar R10/PPN risk",
            "observable_gate": "R10 alpha(lambda); PPN gamma/beta; clocks/Gdot",
            "next_action": "try B_X=C_X=0 from branch extremum/symmetry, else fill symbolic coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority": 2,
            "target_generator": "finite-cell fibre spectrum",
            "why_first": "hardest quotient-invariant scalar generator and possible source-dependent local constants",
            "observable_gate": "R10 finite scalar; WEP/composition; source normalization",
            "next_action": "prove source-independent gapped h0/no matter vertex, else retain fibre charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority": 3,
            "target_generator": "domain selector and relative domain class",
            "why_first": "can fake local/FLRW split and boundary charge",
            "observable_gate": "PPN/domain/orbital/source residuals",
            "next_action": "prove topological/no-stress/no-boundary-exchange selector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority": 4,
            "target_generator": "species/source constants",
            "why_first": "source-only prefactor breaks universality even without R2/fR",
            "observable_gate": "WEP/clocks/source normalization",
            "next_action": "prove no source-only species slot or retain w_A",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority": 5,
            "target_generator": "orientation/time-arrow marker",
            "why_first": "secondary for R2/fR but important for PPN preferred-frame and torsion residuals",
            "observable_gate": "preferred-frame/torsion/nonmetricity",
            "next_action": "classify as observed coframe/spin structure or retained dynamic connection residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gate = [
        {
            "gate_id": "GATE1345_0_R2FR_zero",
            "claim": "R2/fR scalar branch is zero",
            "allowed_if": "memory_class_scalar and finite_fibre_spectrum have B_X=C_X=J_X=Q_boundary=0 plus no bare/measure/boundary R2",
            "current_status": "BLOCKED",
            "reason": "direct scalar pressure rows are retained symbolic",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1345_1_finite_scalar_bound",
            "claim": "finite scalar branch passes R10/PPN",
            "allowed_if": "numeric Z_X, M_X2, B_X, C_X, source/test charge, screening, and source-backed bound rows exist",
            "current_status": "BLOCKED",
            "reason": "all runner inputs are symbolic/nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1345_2_local_GR_EH",
            "claim": "local EH/GR reduction is derived",
            "allowed_if": "all GE966 generators are absent, pure gauge, topological/no-stress, universal constants, or bounded residuals",
            "current_status": "BLOCKED",
            "reason": "generator matrix has retained symbolic rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1345_0_inventory_complete",
            "decision": "every live GE966 generator now has an explicit vertex/source-charge status",
            "because": "B_X/C_X/Z_X/M_X2/J_X/boundary columns are filled for each row",
            "effect": "hidden scalar source ambiguity is removed at the bookkeeping level",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1345_1_direct_R2FR_pressure",
            "decision": "memory/class scalar and finite fibre spectrum are the direct next pressure rows",
            "because": "they are the only rows with a straightforward finite scalar alpha(lambda) path",
            "effect": "next target should attack these before more bound-curve work",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1345_2_no_claim",
            "decision": "no theorem-zero or bound-pass claim is allowed",
            "because": "every executable coefficient remains missing or closure-only",
            "effect": "local-GR/EH remains a disciplined target, not a result",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1345_0_1346",
            "target_file": "1346-Y5-R10-RAB-memory-and-fibre-vertex-zero-or-symbolic-coefficient-fill.md",
            "target_script": "scripts/Y5_R10_RAB_memory_and_fibre_vertex_zero_or_symbolic_coefficient_fill.py",
            "task": "attack VM1345_4 and VM1345_5: prove B_X=C_X=0 for memory/class and finite-fibre generators, or fill a stricter symbolic coefficient pack for R10/PPN source-charge runners",
            "success_condition": "direct scalar pressure rows either parent-zeroed by a named mechanism or promoted to complete symbolic nonclaim coefficient packs",
            "do_not": "do not work on lower-priority bounds or public claims before memory/fibre vertices are owned",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        vertex_matrix,
        runner_inputs,
        classification,
        obs_priority,
        claim_gate,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(VERTEX_MATRIX_PATH, vertex_matrix)
    write_csv(RUNNER_INPUTS_PATH, runner_inputs)
    write_csv(CLASSIFICATION_PATH, classification)
    write_csv(OBS_PRIORITY_PATH, obs_priority)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    matrix_complete = (
        len(vertex_matrix) == 7
        and all(row["B_X_status"] and row["C_X_status"] and row["Z_X_status"] and row["M_X2_status"] for row in vertex_matrix)
        and all(row["classification"] for row in vertex_matrix)
    )
    no_hidden_ambiguity = all("MISSING" in row["next_evidence_needed"] or row["classification"] for row in vertex_matrix)
    runner_rejects = runner_inputs[-1]["verdict"] == "ALL_GENERATOR_VERTEX_ROWS_NONCLAIM"
    direct_pressure_selected = obs_priority[0]["target_generator"] == "memory/class scalar" and obs_priority[1]["target_generator"] == "finite-cell fibre spectrum"
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and matrix_complete
        and no_hidden_ambiguity
        and runner_rejects
        and direct_pressure_selected
        and claims_blocked
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1345_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1345_1_vertex_matrix_complete",
            "generator vertex matrix covers all seven GE966 live generators",
            matrix_complete,
            f"vertex_rows={len(vertex_matrix)}",
        ),
        validation_row(
            "VAL1345_2_no_hidden_ambiguity",
            "each row names its retained or closure-only source status",
            no_hidden_ambiguity,
            ";".join(f"{row['ge966_id']}={row['classification']}" for row in vertex_matrix),
        ),
        validation_row(
            "VAL1345_3_runner_rejects",
            "source-charge runner inputs remain nonclaim and rejected",
            runner_rejects,
            runner_inputs[-1]["verdict"],
        ),
        validation_row(
            "VAL1345_4_direct_pressure_selected",
            "memory and fibre rows selected as direct R2/fR scalar pressure targets",
            direct_pressure_selected,
            "priority1=memory/class scalar;priority2=finite-cell fibre spectrum",
        ),
        validation_row(
            "VAL1345_5_claims_blocked",
            "R2/fR zero, finite scalar bound, and local-GR claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1345_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1345_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1345_8_next_target_1346",
            "next target routes to memory/fibre vertex zero or symbolic coefficient fill",
            next_target[0]["next_id"] == "NEXT1345_0_1346",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1345_9_overall",
            "overall 1345 validation",
            overall_ok,
            "1345 inventories all live generator vertices and selects memory/fibre rows as next direct scalar pressure targets",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1345 completes the generator-by-generator vertex inventory, but no row is claim-ready. The local scalar/R2-fR ambiguity is now explicit rather than hidden.

**Main progress:** every live `GE966` generator now has `B_X`, `C_X`, `Z_X`, `M_X2`, `J_X`, boundary-charge, classification, and observable-link columns. The direct R2/fR pressure rows are `memory/class scalar` and `finite-cell fibre spectrum`.

**Decision:** move to `1346`: attack the memory/fibre vertices first. Bounds and public claims still wait until these direct scalar-pressure rows are either parent-zeroed or filled as nonclaim coefficient packs.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Generator Vertex Matrix
{markdown_table(vertex_matrix, ["matrix_id", "ge966_id", "generator", "B_X_status", "C_X_status", "Z_X_status", "M_X2_status", "J_X_status", "boundary_charge_status", "observable_links", "classification", "next_evidence_needed", "valid_for_claim", "claim_allowed"])}

## Source-Charge Runner Inputs
{markdown_table(runner_inputs, ["input_id", "matrix_id", "generator", "equation", "B_X", "C_X", "Z_X", "M_X2", "J_X", "Q_boundary", "lambda_X", "alpha_X", "accepted_for_scoring", "verdict", "valid_for_claim", "claim_allowed"])}

## Zero Or Retained Classification
{markdown_table(classification, ["class_id", "row_group", "meaning", "rows", "current_status", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Observable Priority Queue
{markdown_table(obs_priority, ["priority", "target_generator", "why_first", "observable_gate", "next_action", "valid_for_claim", "claim_allowed"])}

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
