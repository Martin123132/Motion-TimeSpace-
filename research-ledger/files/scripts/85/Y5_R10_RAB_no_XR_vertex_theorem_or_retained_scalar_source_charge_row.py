from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1344"
TITLE = "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
VERTEX_ALGEBRA_PATH = OUT_DIR / f"{PACK_ID}_VERTEX_ALGEBRA.csv"
THEOREM_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_NO_XR_VERTEX_THEOREM_ATTEMPT.csv"
SOURCE_CHARGE_PATH = OUT_DIR / f"{PACK_ID}_RETAINED_SCALAR_SOURCE_CHARGE_TEMPLATE.csv"
OBSERVABLE_MAP_PATH = OUT_DIR / f"{PACK_ID}_OBSERVABLE_MAP.csv"
RUNNER_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_DRYRUN.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1344_VALIDATION.csv"


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
    return [path for path in FORMALIZATION.rglob("*1344*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1344_0_1343_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1343_NEXT_TARGET.csv",
            "needle": "NEXT1343_0_1344",
            "role": "selected 1344 target",
        },
        {
            "source_id": "SRC1344_1_1343_law",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1343_PARENT_COEFFICIENT_LAW.csv",
            "needle": "LAW1343_0_quadratic_parent_block",
            "role": "parent coefficient law",
        },
        {
            "source_id": "SRC1344_2_1343_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1343_ZERO_SIGNATURE_ATTEMPT.csv",
            "needle": "ZERO1343_1_no_XR_vertex",
            "role": "no-XR key blocker",
        },
        {
            "source_id": "SRC1344_3_1343_nohair",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1343_CURVATURE_SOURCE_NOHAIR_CORRECTION.csv",
            "needle": "NH1343_0_old_silence_lemma",
            "role": "curvature-source nohair correction",
        },
        {
            "source_id": "SRC1344_4_705_no_FchiR",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_705_NO_FCHIR_THEOREM_AUDIT.csv",
            "needle": "NFC705_8_verdict",
            "role": "no variable EH prefactor audit",
        },
        {
            "source_id": "SRC1344_5_705_prefactors",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_705_VARIABLE_PREFACTOR_CHANNELS.csv",
            "needle": "VPC705_3_bulk_X",
            "role": "variable prefactor channels",
        },
        {
            "source_id": "SRC1344_6_703_lock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
            "needle": "PAL703_1_no_variable_prefactor",
            "role": "parent coupling lock audit",
        },
        {
            "source_id": "SRC1344_7_966_generators",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv",
            "needle": "GE966_5_finite_fibre_spectrum",
            "role": "retained generator ledger",
        },
        {
            "source_id": "SRC1344_8_707_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_707_SCALAR_CLASS_ZERO_THEOREM_AUDIT.csv",
            "needle": "SCZ707_6_no_frame_transfer",
            "role": "scalar/class frame-transfer gap",
        },
        {
            "source_id": "SRC1344_9_1343_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1343_VALIDATION.csv",
            "needle": "VAL1343_9_overall",
            "role": "1343 pass gate",
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

    vertex_algebra = [
        {
            "algebra_id": "VERT1344_0_definitions",
            "quantity": "B_X and C_X",
            "definition": "B_X := delta^2 S_parent/(delta X delta R_obs) on the local branch; C_X := delta^2 S_matter/(delta X delta T_or_Lm) in the same observed frame",
            "equation_or_effect": "L_X X = B_X R_obs + C_X T + J_X + boundary",
            "implication": "B_X=0 and C_X=0 are needed before positive-operator local silence can kill X",
            "status": "DEFINITION_WRITTEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "algebra_id": "VERT1344_1_prefactor_expansion",
            "quantity": "F(X) R",
            "definition": "F(X0 + delta X) R = [F0 + F'_0 delta X + 1/2 F''_0 delta X^2 + ...] R",
            "equation_or_effect": "B_X is proportional to F'_0; F'_0=0 kills the linear XR source but F'' terms still require measure/boundary review",
            "implication": "a branch extremum can help, but only if parent-signed and matter-frame-safe",
            "status": "CONDITIONAL_BRANCH_EXTREMUM_ROUTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "algebra_id": "VERT1344_2_matter_frame",
            "quantity": "A_m(X) matter coupling",
            "definition": "S_matter[Psi, A_m^2(X) g_obs] or equivalent species/source map",
            "equation_or_effect": "C_X is proportional to d ln A_m/dX on the branch, with species dependence if A_m is not universal",
            "implication": "even if B_X=0, C_X can source fifth-force/PPN/WEP rows",
            "status": "SAME_FRAME_SOURCE_GATE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "algebra_id": "VERT1344_3_body_charge",
            "quantity": "Q_X[body]",
            "definition": "Q_X = integral_body sqrt(gamma) W_X [B_X R_obs + C_X T + J_X] + Q_boundary",
            "equation_or_effect": "outside body, X(r) approximately Q_X exp(-r/lambda_X)/(4*pi*Z_X*r) for a simple massive scalar",
            "implication": "exterior Ricci-flatness does not erase scalar charge sourced inside the body",
            "status": "SOURCE_CHARGE_LAW_WRITTEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_attempt = [
        {
            "attempt_id": "NXV1344_0_parent_absence",
            "route": "X absent from parent action",
            "required_statement": "the parent object language contains no local scalar/class/fibre/memory variable X that can couple to R or T",
            "current_evidence": "P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER keeps memory and finite-fibre generators live",
            "status": "NOT_DERIVED",
            "if_fails": "B_X/C_X source-charge row remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NXV1344_1_readout_only",
            "route": "X is readout-only, not an argument of S_parent",
            "required_statement": "readout variables are maps Sol(S_parent)->Obs and cannot appear in varied parent action terms",
            "current_evidence": "GE966_0_readout_projector is schema-lock candidate but not parent-signed",
            "status": "CONDITIONAL_ONLY",
            "if_fails": "post-readout reduced actions can smuggle source terms back in",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NXV1344_2_branch_extremum",
            "route": "F'_X(X0)=0 and A'_X(X0)=0 at the local branch",
            "required_statement": "local stationary solution is an extremum of both gravitational prefactor and matter-frame coupling",
            "current_evidence": "no parent potential or extremum certificate exists for each retained generator",
            "status": "UNSIGNED",
            "if_fails": "curvature/source trace drives a finite scalar amplitude",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NXV1344_3_symmetry",
            "route": "X-parity or shift symmetry",
            "required_statement": "a parent symmetry forbids linear X R and X T vertices while allowing the observed EH term",
            "current_evidence": "no named symmetry currently forbids the vertices across scalar/class/memory/fibre sectors",
            "status": "UNSIGNED",
            "if_fails": "vertex absence would be a closure choice rather than a theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NXV1344_4_same_frame_guard",
            "route": "no frame transfer",
            "required_statement": "Weyl/disformal transformations cannot move B_X into C_X or species-dependent clocks/masses",
            "current_evidence": "NFC705_5 and SCZ707_6 remain not_parent_signed",
            "status": "UNSIGNED",
            "if_fails": "apparent gravitational-frame silence may become matter-frame fifth force",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NXV1344_5_boundary_charge",
            "route": "no boundary/body scalar charge",
            "required_statement": "body interior, surface, and projection boundary terms add no Q_boundary and no scalar charge",
            "current_evidence": "NFC705_6 boundary guard remains not_parent_signed",
            "status": "UNSIGNED",
            "if_fails": "exterior scalar tail survives even when exterior R_obs=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NXV1344_6_verdict",
            "route": "B_X=C_X=0 theorem",
            "required_statement": "NXV1344_0 through NXV1344_5 close for every retained local generator",
            "current_evidence": "absence/readout/extremum/symmetry/frame/boundary routes all remain unsigned or conditional",
            "status": "NO_XR_VERTEX_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "if_fails": "retain source-charge branch as nonclaim local residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_charge = [
        {
            "charge_id": "QX1344_0_generic_template",
            "mode_family": "retained scalar/class/memory/fibre X",
            "source_density": "rho_X = B_X R_obs + C_X T + J_X",
            "body_charge": "Q_X[body] = integral_body sqrt(gamma) W_X rho_X + Q_boundary",
            "exterior_profile": "X(r) = Q_X exp(-r/lambda_X)/(4*pi*Z_X*r) for simple massive branch",
            "lambda_input": "lambda_X = sqrt(Z_X/M_X2) or convention-specific scalaron range",
            "alpha_input": "alpha_X requires source/test charge normalization and matter-frame map",
            "missing_for_execution": "Z_X;M_X2;B_X;C_X;J_X;W_X;Q_boundary;screening/body model;source paths",
            "status": "NONCLAIM_TEMPLATE_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "charge_id": "QX1344_1_R2FR_link",
            "mode_family": "R2/fR scalar residual",
            "source_density": "rho_X inherits B_X R_obs and/or C_X T when scalaron-like branch is retained",
            "body_charge": "nonzero Q_X maps to finite-range alpha(lambda) comparison",
            "exterior_profile": "Yukawa tail; exact normalization branch-dependent",
            "lambda_input": "from c_R2/fRR or parent mass M_X",
            "alpha_input": "alpha=1/3 only for exact unscreened metric f(R) branch; otherwise symbolic",
            "missing_for_execution": "MTS coefficient; frame; screening; source-charge normalization",
            "status": "R2FR_RUNNER_INPUT_SHAPE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "charge_id": "QX1344_2_zero_switch",
            "mode_family": "theorem-zero route",
            "source_density": "rho_X=0 only if B_X=C_X=J_X=Q_boundary=0 parent-signed",
            "body_charge": "Q_X=0",
            "exterior_profile": "X=0 under positive operator and zero boundary",
            "lambda_input": "not_applicable_if_zero",
            "alpha_input": "0 only if theorem signed",
            "missing_for_execution": "B_X=C_X=0 theorem not signed",
            "status": "ZERO_SWITCH_REJECTED_UNTIL_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    observable_map = [
        {
            "obs_id": "OBS1344_0_R10",
            "arena": "R10_short_range",
            "observable": "alpha_X(lambda_X)",
            "source_charge_dependency": "requires source and test Q_X/m normalization",
            "status": "BLOCKED_NONCLAIM",
            "reason": "no numeric B_X/C_X/Z_X/M_X2 and full claim-grade curve still absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obs_id": "OBS1344_1_PPN",
            "arena": "solar_system_PPN",
            "observable": "gamma_minus_1 and beta_minus_1",
            "source_charge_dependency": "depends on scalar range, body charge, frame, screening, and light/matter coupling",
            "status": "BLOCKED_NONCLAIM",
            "reason": "no body-charge/no-frame-transfer theorem or numeric map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obs_id": "OBS1344_2_WEP_clock",
            "arena": "WEP_clock_source_normalization",
            "observable": "eta_AB, clock drift, source-normalization residual",
            "source_charge_dependency": "species/frame dependence enters through C_X and matter functor",
            "status": "BLOCKED_NONCLAIM",
            "reason": "same-frame matter functor and species blindness remain conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_dryrun = [
        {
            "run_id": "RUN1344_0_no_vertex_zero",
            "input_branch": "B_X=C_X=0 theorem",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_NO_XR_VERTEX_THEOREM_NOT_DERIVED",
            "missing_fields": "parent_absence;readout_only;branch_extremum;symmetry;same_frame_guard;boundary_charge_zero",
            "reason": "no route is parent-signed for every retained generator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1344_1_source_charge_template",
            "input_branch": "QX1344_0_generic_template",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_SYMBOLIC_SOURCE_CHARGE_ONLY",
            "missing_fields": "Z_X;M_X2;B_X;C_X;J_X;W_X;Q_boundary;screening;source_paths",
            "reason": "template names the charge but supplies no parent numeric coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1344_2_observable_branch",
            "input_branch": "R10_PPN_WEP_observables",
            "accepted_for_scoring": False,
            "verdict": "REJECTED_OBSERVABLE_MAP_INPUTS_MISSING",
            "missing_fields": "alpha_lambda;PPN_projection;species_frame_map",
            "reason": "observables are mapped but not executable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1344_VERDICT",
            "input_branch": "all no-XR/source-charge routes",
            "accepted_for_scoring": False,
            "verdict": "NO_XR_THEOREM_FAILED_SOURCE_CHARGE_RETAINED_NONCLAIM",
            "missing_fields": "parent vertex inventory or numeric source-charge coefficients",
            "reason": "1344 converts the blocker into an explicit retained source-charge row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1344_0_theorem_status",
            "decision": "no-XR/no-source vertex theorem is not derived",
            "because": "parent inventory, readout-only domain, branch extremum, symmetry, frame guard, and boundary charge clauses are unsigned",
            "effect": "B_X and C_X cannot be set to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1344_1_source_charge_status",
            "decision": "retained scalar source-charge row is now explicit",
            "because": "Q_X[body] names the exact body/interior/boundary source needed for R10 and PPN comparisons",
            "effect": "future work can fill coefficients or prove they vanish without ambiguity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1344_2_best_next",
            "decision": "next move should build a parent vertex inventory, not more external bounds",
            "because": "bounds cannot score until B_X/C_X/Z_X/M_X2 or a no-vertex theorem exists",
            "effect": "1345 should inventory allowed parent vertices by generator and mark theorem-zero versus retained-source branches",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1344_0_1345",
            "target_file": "1345-Y5-R10-RAB-parent-vertex-inventory-by-generator-or-source-charge-runner-inputs.md",
            "target_script": "scripts/Y5_R10_RAB_parent_vertex_inventory_by_generator_or_source_charge_runner_inputs.py",
            "task": "inventory each live generator from GE966 against B_X, C_X, Z_X, M_X2, J_X, boundary charge, and source paths; classify theorem-zero, closure-only, or retained symbolic source-charge",
            "success_condition": "a generator-by-generator vertex matrix with no hidden scalar source ambiguity, all rows nonclaim unless parent-signed",
            "do_not": "do not promote no-XR theorem globally; do not infer numeric coefficients from the existence of a template",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables = [
        source_register,
        vertex_algebra,
        theorem_attempt,
        source_charge,
        observable_map,
        runner_dryrun,
        decision_ledger,
        next_target,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(VERTEX_ALGEBRA_PATH, vertex_algebra)
    write_csv(THEOREM_ATTEMPT_PATH, theorem_attempt)
    write_csv(SOURCE_CHARGE_PATH, source_charge)
    write_csv(OBSERVABLE_MAP_PATH, observable_map)
    write_csv(RUNNER_DRYRUN_PATH, runner_dryrun)
    write_csv(DECISION_PATH, decision_ledger)
    write_csv(NEXT_PATH, next_target)

    sources_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in source_register)
    algebra_written = vertex_algebra[0]["status"] == "DEFINITION_WRITTEN"
    theorem_blocked = theorem_attempt[-1]["status"] == "NO_XR_VERTEX_THEOREM_NOT_DERIVED_CURRENT_CORPUS"
    charge_retained = source_charge[0]["status"] == "NONCLAIM_TEMPLATE_RETAINED"
    observables_blocked = all(row["status"] == "BLOCKED_NONCLAIM" for row in observable_map)
    runner_rejects = runner_dryrun[-1]["verdict"] == "NO_XR_THEOREM_FAILED_SOURCE_CHARGE_RETAINED_NONCLAIM"
    formalization_hits = generated_inside_formalization()
    overall_ok = (
        sources_ok
        and algebra_written
        and theorem_blocked
        and charge_retained
        and observables_blocked
        and runner_rejects
        and all_nonclaim(tables)
        and len(formalization_hits) == 0
    )

    validation = [
        validation_row(
            "VAL1344_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1344_1_vertex_algebra_written",
            "B_X/C_X vertex algebra is written",
            algebra_written,
            "L_X X = B_X R_obs + C_X T + J_X + boundary",
        ),
        validation_row(
            "VAL1344_2_no_vertex_not_promoted",
            "no-XR/no-source vertex theorem remains blocked",
            theorem_blocked,
            theorem_attempt[-1]["status"],
        ),
        validation_row(
            "VAL1344_3_source_charge_retained",
            "retained scalar source-charge template is explicit",
            charge_retained,
            "Q_X[body] template written and nonclaim",
        ),
        validation_row(
            "VAL1344_4_observables_blocked",
            "R10/PPN/WEP observable maps remain blocked",
            observables_blocked,
            ";".join(f"{row['obs_id']}={row['status']}" for row in observable_map),
        ),
        validation_row(
            "VAL1344_5_runner_rejects",
            "strict dry-run rejects theorem and source-charge branches",
            runner_rejects,
            runner_dryrun[-1]["verdict"],
        ),
        validation_row(
            "VAL1344_6_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1344_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_hits) == 0,
            f"formalization_generated_output_count={len(formalization_hits)}",
        ),
        validation_row(
            "VAL1344_8_next_target_1345",
            "next target routes to parent vertex inventory by generator",
            next_target[0]["next_id"] == "NEXT1344_0_1345",
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1344_9_overall",
            "overall 1344 validation",
            overall_ok,
            "1344 fails the no-XR theorem honestly and retains an explicit scalar source-charge template",
        ),
    ]
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1344 does not prove the no-`X R`/no-source vertex theorem. The parent corpus still does not sign absence, readout-only status, branch extremum, symmetry, same-frame guard, or boundary-charge silence for every retained generator.

**Main progress:** the scalar source-charge law is now explicit. The retained local branch is not vague anymore: `L_X X = B_X R_obs + C_X T + J_X + boundary`, with `Q_X[body]` feeding R10/PPN/WEP observables if not zeroed.

**Decision:** move to `1345`: build a generator-by-generator parent vertex inventory, because bounds cannot score until `B_X`, `C_X`, `Z_X`, `M_X2`, and boundary/source terms are either parent-zeroed or explicitly retained.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Vertex Algebra
{markdown_table(vertex_algebra, ["algebra_id", "quantity", "definition", "equation_or_effect", "implication", "status", "valid_for_claim", "claim_allowed"])}

## No-XR Vertex Theorem Attempt
{markdown_table(theorem_attempt, ["attempt_id", "route", "required_statement", "current_evidence", "status", "if_fails", "valid_for_claim", "claim_allowed"])}

## Retained Scalar Source-Charge Template
{markdown_table(source_charge, ["charge_id", "mode_family", "source_density", "body_charge", "exterior_profile", "lambda_input", "alpha_input", "missing_for_execution", "status", "valid_for_claim", "claim_allowed"])}

## Observable Map
{markdown_table(observable_map, ["obs_id", "arena", "observable", "source_charge_dependency", "status", "reason", "valid_for_claim", "claim_allowed"])}

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
