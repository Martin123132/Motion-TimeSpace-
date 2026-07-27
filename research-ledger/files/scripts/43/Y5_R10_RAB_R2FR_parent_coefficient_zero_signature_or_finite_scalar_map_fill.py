from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1343"
TITLE = "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COEFFICIENT_LAW_PATH = OUT_DIR / f"{PACK_ID}_PARENT_COEFFICIENT_LAW.csv"
ZERO_SIGNATURE_PATH = OUT_DIR / f"{PACK_ID}_ZERO_SIGNATURE_ATTEMPT.csv"
NOHAIR_CORRECTION_PATH = OUT_DIR / f"{PACK_ID}_CURVATURE_SOURCE_NOHAIR_CORRECTION.csv"
FINITE_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_FINITE_SCALAR_MAP_TEMPLATE.csv"
RUNNER_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_DRYRUN.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1343_VALIDATION.csv"


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
    return [path for path in FORMALIZATION.rglob("*1343*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1343_0_1342_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1342_NEXT_TARGET.csv",
            "needle": "NEXT1342_0_1343",
            "role": "selected 1343 target",
        },
        {
            "source_id": "SRC1343_1_1342_tower",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1342_INTEGRATED_OUT_TOWER_ZERO_ATTEMPT.csv",
            "needle": "TOWER1342_7_verdict",
            "role": "R2/fR tower zero gap",
        },
        {
            "source_id": "SRC1343_2_963_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
            "needle": "CO963_4_verdict",
            "role": "coefficient owner audit",
        },
        {
            "source_id": "SRC1343_3_963_no_extra_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_NO_EXTRA_SCALAR_SIGNATURE.csv",
            "needle": "NES963_5_verdict",
            "role": "no-extra-scalar signature gap",
        },
        {
            "source_id": "SRC1343_4_964_minimality",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
            "needle": "MIN964_5_verdict",
            "role": "parent minimality attempt",
        },
        {
            "source_id": "SRC1343_5_965_primitive",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
            "needle": "PQ965_5_verdict",
            "role": "primitive/no-marker theorem attempt",
        },
        {
            "source_id": "SRC1343_6_966_generators",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv",
            "needle": "GE966_7_verdict",
            "role": "local invariant generator elimination ledger",
        },
        {
            "source_id": "SRC1343_7_969_action_targets",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_969_MINIMAL_ACTION_CONSTRUCTION_TARGETS.csv",
            "needle": "MACT969_3_no_integrated_out_tower",
            "role": "minimal action construction targets",
        },
        {
            "source_id": "SRC1343_8_706_AEH_inventory",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_706_AEH_TERM_INVENTORY.csv",
            "needle": "AEHT706_5_higher_curvature",
            "role": "EH prefactor and higher-curvature channel inventory",
        },
        {
            "source_id": "SRC1343_9_707_scalar_class",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv",
            "needle": "SCZ707_8_verdict",
            "role": "scalar/class F(phi,C)R zero audit",
        },
        {
            "source_id": "SRC1343_10_1341_scalar_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1341_SCALAR_MODE_MAP_CONTRACT.csv",
            "needle": "SMAP1341_1_quadratic_convention",
            "role": "existing nonclaim scalar-mode map contract",
        },
        {
            "source_id": "SRC1343_11_963_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
            "needle": "R2RUN963_4_decision_logic",
            "role": "R2/fR strict runner requirements",
        },
        {
            "source_id": "SRC1343_12_1342_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1342_VALIDATION.csv",
            "needle": "VAL1342_10_overall",
            "role": "1342 pass gate",
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

    coefficient_law = [
        {
            "law_id": "LAW1343_0_quadratic_parent_block",
            "object": "hidden scalar/vector/fibre modes X_A around the local branch",
            "symbolic_parent_block": "S_X = integral sqrt(-g)[-1/2 X_A L_AB X_B + X_A(B_A R + C_A T + J_A) + c_bare R^2 + ...]",
            "derived_effect": "solving X gives Delta S_eff contains 1/2 (B R + C T + J)^T L^{-1}(B R + C T + J)",
            "coefficient_or_map": "c_R2_eff(k) = c_bare + 1/2 B^T L^{-1}(k) B + c_measure + c_boundary, up to sign convention",
            "status": "DERIVED_CONDITIONAL_COEFFICIENT_LAW",
            "what_it_means": "a hidden mode with a curvature-linear vertex generates an R2/fR scalar residual even when ordinary matter source J is zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1343_1_low_momentum_limit",
            "object": "massive local mode with L(k)=Z_X k^2 + M_X^2",
            "symbolic_parent_block": "B_X X R coupling retained; ordinary compact exterior probes k^2 << M_X^2 if range is short",
            "derived_effect": "local expansion produces R^2 plus higher derivative tower",
            "coefficient_or_map": "c_R2_eff ~= c_bare + sum_X B_X^2/(2 M_X^2) + c_measure + c_boundary, convention-signed",
            "status": "DERIVED_SYMBOLIC_NO_NUMERIC_INPUTS",
            "what_it_means": "coefficient zero requires no curvature-linear vertex or an exact symmetry/identity cancellation, not just a preferred small number",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1343_2_finite_range_branch",
            "object": "retained finite scalar branch",
            "symbolic_parent_block": "same quadratic parent block without taking k^2 << M_X^2",
            "derived_effect": "propagator pole produces Yukawa-like range",
            "coefficient_or_map": "lambda_X = sqrt(Z_X/M_X^2) in c=hbar=1 units; alpha_X needs source coupling C_X and matter-frame normalization",
            "status": "FINITE_MAP_SHAPE_DERIVED_INPUTS_MISSING",
            "what_it_means": "curve comparison needs Z_X, M_X^2, B_X, C_X, frame, screening, and source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1343_3_tuning_guard",
            "object": "zero coefficient route",
            "symbolic_parent_block": "c_bare + 1/2 B^T L^{-1} B + c_measure + c_boundary = 0",
            "derived_effect": "exact cancellation is not a derivation unless owned by a Ward identity, topological identity, field-redefinition redundancy, or parent object-language exclusion",
            "coefficient_or_map": "Z_cR2 = true only if every term is zero/identity-cancelled with source paths",
            "status": "ZERO_SIGNATURE_REFINED_NOT_SIGNED",
            "what_it_means": "1343 sharpens the target: prove B_A=0/no bare R2/no measure/no boundary, or retain the scalar branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_signature = [
        {
            "zero_id": "ZERO1343_0_no_bare_R2",
            "required_clause": "no bare higher-curvature operator",
            "mathematical_test": "parent local action has no R^2, f(R), Ricci^2, Weyl^2, or nonlocal R F(Box) R term before reduction",
            "current_evidence": "AEHT706_5_higher_curvature and TOWER1342_7 remain central open",
            "current_status": "UNSIGNED",
            "if_missing": "bare c_bare can source c_R2_eff directly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1343_1_no_XR_vertex",
            "required_clause": "no curvature-linear hidden-sector vertex",
            "mathematical_test": "B_A = d^2 S_parent/(dX_A dR) = 0 for every eliminated scalar/class/fibre/memory mode in the observed frame",
            "current_evidence": "GE966_4_memory_class_scalar and GE966_5_finite_fibre_spectrum are not eliminated",
            "current_status": "UNSIGNED_KEY_BLOCKER",
            "if_missing": "even source-free hidden modes generate R L^{-1} R after elimination",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1343_2_no_matter_frame_transfer",
            "required_clause": "no Weyl/disformal or matter-frame debt",
            "mathematical_test": "setting F=1 in the gravitational frame must not move B_A or C_A into matter clocks, masses, or source charges",
            "current_evidence": "SCZ707_6_no_frame_transfer and AEHT706_8_frame_transfer are not parent-signed",
            "current_status": "UNSIGNED",
            "if_missing": "R2/fR may be hidden as a scalar-tensor/source-normalization residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1343_3_no_measure_boundary",
            "required_clause": "no measure/Jacobian/boundary counterterm",
            "mathematical_test": "c_measure = c_boundary = 0 or topological/no-flux under the local projection",
            "current_evidence": "TOWER1342_3 and TOWER1342_5 remain unsigned",
            "current_status": "UNSIGNED",
            "if_missing": "classical no-hair can still leave an effective curvature-squared counterterm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1343_4_no_tuned_cancellation",
            "required_clause": "no unexplained cancellation counted as derivation",
            "mathematical_test": "if terms cancel, cancellation must follow from a named parent identity and not fitted numeric balance",
            "current_evidence": "no parent Ward/topological identity currently sources the cancellation",
            "current_status": "NOT_AVAILABLE",
            "if_missing": "apparent c_R2=0 would be closure/fine tuning, not derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1343_5_verdict",
            "required_clause": "parent coefficient zero signature",
            "mathematical_test": "ZERO1343_0 through ZERO1343_4 all pass",
            "current_evidence": "key clauses are unsigned, especially B_A=0/no X R vertex",
            "current_status": "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS",
            "if_missing": "R2/fR finite scalar branch remains retained as nonclaim residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    nohair_correction = [
        {
            "correction_id": "NH1343_0_old_silence_lemma",
            "old_assumption": "J_X=0 plus positive operator L_X implies X=0 in the compact local branch",
            "correction": "if the parent action contains B_X X R, the X equation is L_X X = B_X R + C_X T + J_X + boundary",
            "effect": "ordinary source silence J_X=0 is insufficient because curvature/source trace can still drive X",
            "status": "LEMMA_REPAIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "correction_id": "NH1343_1_exterior_subtlety",
            "old_assumption": "R=0 in exterior means scalar charge vanishes",
            "correction": "a finite scalar can be sourced inside the body and appear outside as Yukawa boundary data unless body charge or B_X/C_X is zero",
            "effect": "local PPN/R10 branch needs source-charge no-hair, not just exterior Ricci-flatness",
            "status": "SOURCE_CHARGE_GATE_ADDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "correction_id": "NH1343_2_repaired_zero_route",
            "old_assumption": "positive operator alone closes local scalar hair",
            "correction": "positive operator closes only after B_X=0, C_X=0, J_X=0, and boundary flux=0 are parent-signed",
            "effect": "the best derivation target becomes no-XR/no-source-vertex theorem",
            "status": "NEXT_TARGET_REFINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_template = [
        {
            "template_id": "FSM1343_0_required_mode_row",
            "mode_or_family": "generic retained scalar/memory/fibre mode X",
            "Z_X": "MISSING_PARENT_INPUT",
            "M_X2": "MISSING_PARENT_INPUT",
            "B_XR": "MISSING_PARENT_INPUT",
            "C_XT_or_beta_m": "MISSING_PARENT_INPUT",
            "lambda_formula": "lambda_X = sqrt(Z_X/M_X2) in c=hbar=1 units, convert before runner",
            "alpha_formula": "generic alpha_X depends on matter-frame source coupling; metric f(R) unscreened convention may use alpha=1/3 only if that exact branch is sourced",
            "screening_or_body_charge": "MISSING",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "TEMPLATE_NOT_EXECUTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "FSM1343_1_quadratic_fR_convention",
            "mode_or_family": "R + c_R2 R^2 scalaron convention",
            "Z_X": "CONVENTION_DEPENDENT",
            "M_X2": "m_s^2 approximately 1/(6 c_R2) in common normalization",
            "B_XR": "encoded_by_fRR_or_c_R2",
            "C_XT_or_beta_m": "universal metric coupling if exact f(R) branch is selected",
            "lambda_formula": "lambda_s = hbar/(m_s c)",
            "alpha_formula": "alpha_s = 1/3 only for unscreened metric f(R) convention",
            "screening_or_body_charge": "MISSING_SCREENING_REGIME",
            "source_path": "P8_Y5_R10_1341_SCALAR_MODE_MAP_CONTRACT.csv",
            "status": "CONVENTION_GUARDED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "FSM1343_2_curve_binding",
            "mode_or_family": "R10 alpha(lambda) comparison",
            "Z_X": "requires_numeric_lambda",
            "M_X2": "requires_numeric_lambda",
            "B_XR": "requires_numeric_alpha_or_coupling",
            "C_XT_or_beta_m": "requires_matter_source_map",
            "lambda_formula": "must lie inside sourced curve domain",
            "alpha_formula": "must be compared to alpha_bound(lambda) from valid full curve",
            "screening_or_body_charge": "must be declared",
            "source_path": "P8_Y5_R10_1342_EXISTING_BOUND_CURVE_AUDIT.csv",
            "status": "RUNNER_BLOCKED_INPUTS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_dryrun = [
        {
            "run_id": "RUN1343_0_zero_signature",
            "input_branch": "parent c_R2/c_fRR zero",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_ZERO_SIGNATURE_NOT_DERIVED",
            "missing_fields": "no_bare_R2;no_XR_vertex;no_frame_transfer;no_measure_boundary;no_tuned_cancellation",
            "reason": "the coefficient law is sharper, but decisive parent clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1343_1_generic_finite_scalar",
            "input_branch": "FSM1343_0_required_mode_row",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_MISSING_PARENT_MODE_INPUTS",
            "missing_fields": "Z_X;M_X2;B_XR;C_XT_or_beta_m;screening_or_body_charge;source_path",
            "reason": "symbolic map exists but no numeric parent values exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1343_2_quadratic_convention",
            "input_branch": "FSM1343_1_quadratic_fR_convention",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_CONVENTION_GUARDED_NO_MTS_COEFFICIENT",
            "missing_fields": "c_R2_or_fRR;units;normalization;screening_regime",
            "reason": "alpha=1/3 and mass formula are not MTS predictions until the exact branch and coefficient are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1343_3_curve_branch",
            "input_branch": "R10 bound curve",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_BOUND_CURVE_NOT_CLAIM_GRADE_AND_NO_PREDICTION",
            "missing_fields": "valid full curve;numeric alpha_predicted;numeric lambda_predicted",
            "reason": "Lee 2020 review candidate remains private pressure data only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1343_VERDICT",
            "input_branch": "all R2/fR scalar routes",
            "accepted_for_scoring": False,
            "verdict": "R2FR_COEFFICIENT_BRANCH_REFINED_BUT_BLOCKED",
            "missing_fields": "parent no-XR vertex theorem or numeric finite scalar mode row",
            "reason": "1343 derives the symbolic coefficient law and repairs the no-hair target, but no claim-ready zero or finite branch exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1343_0_actual_gap",
            "decision": "the key missing theorem is no curvature-linear hidden-sector vertex",
            "because": "B_X X R generates R L^{-1} R even when ordinary J_X=0",
            "effect": "future local-GR proof must kill B_X/C_X/source charge, not merely invoke positive-operator no-hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1343_1_zero_status",
            "decision": "c_R2/c_fRR zero is not derived",
            "because": "bare higher curvature, X R vertices, frame transfer, measure, and boundary clauses are not parent-signed",
            "effect": "R2/fR remains an explicit retained R11/R10 residual family",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1343_2_finite_status",
            "decision": "finite scalar map is structurally sharper but non-executable",
            "because": "Z_X, M_X2, B_XR, source coupling, body charge, and screening are all missing",
            "effect": "no bound comparison can be run as evidence yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1343_0_1344",
            "target_file": "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
            "target_script": "scripts/Y5_R10_RAB_no_XR_vertex_theorem_or_retained_scalar_source_charge_row.py",
            "task": "prove the parent object language forbids every curvature-linear hidden-sector vertex B_X X R and matter source vertex C_X X T, or retain a scalar source-charge row with symbolic coefficients",
            "success_condition": "B_X=C_X=0 theorem with source paths, or a strict nonclaim source-charge template that names the local body-charge and R10/PPN observables",
            "do_not": "do not claim R2/fR zero from J_X=0 alone; do not count exterior Ricci-flatness as body scalar-charge silence; do not invent numeric coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        coefficient_law,
        zero_signature,
        nohair_correction,
        finite_template,
        runner_dryrun,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(COEFFICIENT_LAW_PATH, coefficient_law)
    write_csv(ZERO_SIGNATURE_PATH, zero_signature)
    write_csv(NOHAIR_CORRECTION_PATH, nohair_correction)
    write_csv(FINITE_TEMPLATE_PATH, finite_template)
    write_csv(RUNNER_DRYRUN_PATH, runner_dryrun)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    law_written = coefficient_law[0]["status"] == "DERIVED_CONDITIONAL_COEFFICIENT_LAW"
    zero_blocked = zero_signature[-1]["current_status"] == "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"
    nohair_repaired = nohair_correction[-1]["status"] == "NEXT_TARGET_REFINED"
    finite_blocked = finite_template[0]["status"] == "TEMPLATE_NOT_EXECUTABLE"
    runner_rejects = runner_dryrun[-1]["verdict"] == "R2FR_COEFFICIENT_BRANCH_REFINED_BUT_BLOCKED"
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and law_written
        and zero_blocked
        and nohair_repaired
        and finite_blocked
        and runner_rejects
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1343_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1343_1_coefficient_law_written",
            "symbolic parent coefficient law is written",
            law_written,
            "c_R2_eff(k) includes bare, integrated hidden-sector, measure, and boundary pieces",
        ),
        validation_row(
            "VAL1343_2_zero_not_promoted",
            "parent zero signature remains blocked",
            zero_blocked,
            zero_signature[-1]["current_status"],
        ),
        validation_row(
            "VAL1343_3_nohair_repaired",
            "positive-operator no-hair target is corrected for curvature source terms",
            nohair_repaired,
            "L_X X = B_X R + C_X T + J_X + boundary",
        ),
        validation_row(
            "VAL1343_4_finite_template_nonexecutable",
            "finite scalar map rows remain nonclaim and non-executable",
            finite_blocked,
            finite_template[0]["status"],
        ),
        validation_row(
            "VAL1343_5_runner_rejects",
            "strict runner dry-run rejects zero and finite branches",
            runner_rejects,
            runner_dryrun[-1]["verdict"],
        ),
        validation_row(
            "VAL1343_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1343_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1343_8_next_target_1344",
            "next target routes to no-XR/no-source-vertex theorem or retained source-charge row",
            next_target[0]["next_id"] == "NEXT1343_0_1344",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1343_9_overall",
            "overall 1343 validation",
            overall_ok,
            "1343 derives the symbolic coefficient law, identifies B_X X R as the key blocker, and keeps all claims blocked",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1343 sharpens the `R2/fR` problem but does not close it. The parent coefficient is zero only if the bare higher-curvature term, every hidden-sector `X R` vertex, measure/Jacobian terms, boundary terms, and frame-transfer debt are absent or identity-cancelled.

**Main progress:** the exact symbolic coefficient law is now explicit: an eliminated hidden mode with `B_X X R` generates `R L_X^-1 R`, so `J_X=0` no-hair is not enough. The next proof must kill the curvature-linear vertex `B_X`, not just ordinary source `J_X`.

**Decision:** move to `1344`: prove the no-`X R`/no-source-vertex theorem, or retain a scalar source-charge row. No local-GR, R10, PPN, or `R2/fR` pass is claimed.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Parent Coefficient Law
{markdown_table(coefficient_law, ["law_id", "object", "symbolic_parent_block", "derived_effect", "coefficient_or_map", "status", "what_it_means", "valid_for_claim", "claim_allowed"])}

## Zero Signature Attempt
{markdown_table(zero_signature, ["zero_id", "required_clause", "mathematical_test", "current_evidence", "current_status", "if_missing", "valid_for_claim", "claim_allowed"])}

## Curvature Source Nohair Correction
{markdown_table(nohair_correction, ["correction_id", "old_assumption", "correction", "effect", "status", "valid_for_claim", "claim_allowed"])}

## Finite Scalar Map Template
{markdown_table(finite_template, ["template_id", "mode_or_family", "Z_X", "M_X2", "B_XR", "C_XT_or_beta_m", "lambda_formula", "alpha_formula", "screening_or_body_charge", "source_path", "status", "valid_for_claim", "claim_allowed"])}

## Runner Dryrun
{markdown_table(runner_dryrun, ["run_id", "input_branch", "accepted_for_scoring", "verdict", "missing_fields", "reason", "valid_for_claim", "claim_allowed"])}

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
