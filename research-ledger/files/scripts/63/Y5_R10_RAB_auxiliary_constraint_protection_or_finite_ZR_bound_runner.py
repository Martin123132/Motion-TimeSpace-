from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1265"
TITLE = "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
AUX_PROTECTION_PATH = OUT_DIR / f"{PACK_ID}_AUXILIARY_PROTECTION_AUDIT.csv"
ELIMINATION_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_AUXILIARY_ELIMINATION_THEOREM.csv"
REGENERATION_RISK_PATH = OUT_DIR / f"{PACK_ID}_REGENERATION_RISK_LEDGER.csv"
BOUND_RUNNER_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_BOUND_RUNNER_SCHEMA.csv"
BOUND_RUNNER_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_BOUND_RUNNER_DRYRUN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1265_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        AUX_PROTECTION_PATH,
        ELIMINATION_THEOREM_PATH,
        REGENERATION_RISK_PATH,
        BOUND_RUNNER_SCHEMA_PATH,
        BOUND_RUNNER_DRYRUN_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def live_intake_counts() -> tuple[int, int, int]:
    raw_dir = RAB_INTAKE_DIR / "raw"
    accepted_dir = RAB_INTAKE_DIR / "accepted"
    docs_dir = RAB_INTAKE_DIR / "docs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    raw_rows = sum(len(read_csv(path)) for path in raw_dir.glob("*.csv"))
    accepted_rows = sum(len(read_csv(path)) for path in accepted_dir.glob("*.csv"))
    docs_rows = sum(len(read_csv(path)) for path in docs_dir.glob("*.csv"))
    return raw_rows, accepted_rows, docs_rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1265_0_1264_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_NEXT_TARGET.csv",
            "needle": "NEXT1264_0_1265",
            "purpose": "handoff to auxiliary protection or finite-ZR bound runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_1_1264_aux",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_AUXILIARY_COMPATIBILITY_ROUTE.csv",
            "needle": "AUX1264_0_parent_block",
            "purpose": "candidate auxiliary compatibility block",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_2_1264_theta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_THETA_OMEGA_VR_FILL_AUDIT.csv",
            "needle": "TVR1264_3_on_shell_nullness",
            "purpose": "on-shell auxiliary nullness caveat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_3_1264_boundary",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_BOUNDARY_ZERO_TEST.csv",
            "needle": "BT1264_1_boundary_functional",
            "purpose": "boundary/corner risk from R_AB terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_4_1264_zr_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_ZR_OPERATOR_STATUS.csv",
            "needle": "ZOS1264_1_EFT_counterterm",
            "purpose": "readout/EFT regeneration risk",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_5_1264_finite_req",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_FINITE_ZR_SOURCE_ROW_REQUIREMENTS.csv",
            "needle": "FZR1264_4_arena",
            "purpose": "finite residual source row requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_6_1263_kinetic",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1263_KINETIC_TERM_CONTRADICTION_AUDIT.csv",
            "needle": "EXACT_CONDITIONAL_ON_TRUE_NULLNESS",
            "purpose": "conditional null/kinetic contradiction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_7_1260_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1260_COEFFICIENT_TO_QRHAT_OR_SUPPRESSION_MAP.csv",
            "needle": "MAP1260_1_massive_suppression",
            "purpose": "finite Z_R residual branch map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1265_8_1264_template",
            "local_path": "source-intake/rab-sector/docs/ZR1264_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1264_TEMPLATE_DO_NOT_SCORE",
            "purpose": "finite-ZR source-row docs template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    aux_protection = [
        {
            "clause_id": "AP1265_0_auxiliary_signature",
            "protection_clause": "`R_AB` and `Lambda_R` are parent auxiliary/constraint variables, not quotient observables and not hidden physical fields.",
            "test": "R_AB appears only in algebraic compatibility block `Lambda_R(R_AB-C_AB[q,theta,top])`.",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "failure_mode": "R_AB can be physical; Z_R kinetic term becomes legal.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_1_no_derivatives",
            "protection_clause": "Parent grammar forbids `D R_AB`, `D Lambda_R`, vertical fibre metric, vertical connection, and Sobolev norms.",
            "test": "no operator constructor can form `G_vert(DR,DR)` or `h^{ij}D_iR_ABD_jR_AB`.",
            "current_status": "UNSIGNED_GRAMMAR_PROTECTION",
            "failure_mode": "tree-level or effective `Z_R` term can be generated.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_2_eliminability",
            "protection_clause": "Auxiliary equations are algebraic and eliminate `R_AB,Lambda_R` without leaving a nonlocal determinant or residual source.",
            "test": "E_Lambda: R_AB=C_AB and E_R: Lambda_R=0, with no additional R_AB matter/source term.",
            "current_status": "EXACT_IF_AUXILIARY_BLOCK_IS_COMPLETE",
            "failure_mode": "extra source term leaves finite Lambda_R or effective R_AB force.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_3_boundary_silence",
            "protection_clause": "Parent boundary/corner grammar contains no `B_R(R_AB)` and no R_AB Hamiltonian charge.",
            "test": "`partial B_R/partial R_AB=0` and `Q_R=0` before readout.",
            "current_status": "UNSIGNED_BOUNDARY_PROTECTION",
            "failure_mode": "bulk auxiliary status still allows boundary hair.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_4_readout_stability",
            "protection_clause": "Readout/effective reduction preserves the auxiliary quotient grammar.",
            "test": "S_eff remains in Image(ParentGenerate[q,theta,top]) and cannot regenerate finite `Z_R`.",
            "current_status": "UNSIGNED_READOUT_PROTECTION",
            "failure_mode": "radiative/readout `Z_R` survives even if tree-level block is auxiliary.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    elimination_theorem = [
        {
            "theorem_id": "AET1265_0_auxiliary_elimination",
            "theorem_name": "algebraic auxiliary elimination for R_AB",
            "statement": "If AP1265_0 through AP1265_4 are parent-signed, `R_AB` and `Lambda_R` can be eliminated to a reduced action with no R_AB symplectic sector, no R_AB boundary momentum, and no legal `Z_R` kinetic operator.",
            "proof_sketch": "`E_Lambda` sets `R_AB=C_AB[q,theta,top]`; `E_R` sets `Lambda_R=0`; no derivatives imply `theta_R=Omega_R=Pi_R^n=0`; protected grammar forbids regeneration.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_effect": "would close the R_AB branch without fitting finite `Z_R`",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "AET1265_1_not_gauge_but_eliminated",
            "theorem_name": "on-shell auxiliary nullness is acceptable only after elimination",
            "statement": "The route does not need to pretend `R_AB` is an off-shell gauge generator if the algebraic pair is eliminated before local readout.",
            "proof_sketch": "After solving algebraic equations, there is no independent R_AB direction left in reduced phase space; the earlier `v_R` is a bookkeeping variation, not a physical phase-space vector.",
            "proof_status": "CONDITIONAL_CLARIFICATION",
            "claim_effect": "removes one false blocker, but only if elimination is parent-owned and stable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "AET1265_2_fallback_trigger",
            "theorem_name": "finite residual trigger",
            "statement": "If any protection clause fails, finite `Z_R`, `M_R^2`, `J_R`, and `B_R` rows are mandatory before local tests.",
            "proof_sketch": "A physical, vertically-metrized, boundary-supported, or readout-regenerated R_AB sector has legal local residuals.",
            "proof_status": "RESIDUAL_BRANCH_MANDATORY_IF_UNSIGNED",
            "claim_effect": "prevents local-GR/R10/PPN promotion from a half-protected auxiliary ansatz",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    regeneration_risks = [
        {
            "risk_id": "RR1265_0_tree_operator",
            "risk": "tree-level `D R_AB` operator added outside auxiliary grammar",
            "needed_block": "primitive action grammar excluding derivative constructors",
            "status": "UNSIGNED",
            "finite_fallback": "Z_R source row or theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "risk_id": "RR1265_1_boundary_operator",
            "risk": "boundary/corner `B_R(R_AB)` source",
            "needed_block": "boundary grammar/no-hair theorem for R_AB",
            "status": "UNSIGNED",
            "finite_fallback": "B_R source row or boundary flux bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "risk_id": "RR1265_2_matter_source",
            "risk": "ordinary matter couples directly to R_AB or Lambda_R",
            "needed_block": "matter action factors through quotient variables only",
            "status": "UNSIGNED",
            "finite_fallback": "J_R source row or matter descent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "risk_id": "RR1265_3_readout_EFT",
            "risk": "readout/effective action regenerates `Z_R` after eliminating auxiliaries",
            "needed_block": "radiative/readout closure of auxiliary quotient grammar",
            "status": "UNSIGNED",
            "finite_fallback": "finite `Z_R(lambda)` bound runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_runner_schema = [
        {
            "branch_id": "BR1265_0_theorem_zero",
            "required_inputs": "parent-signed AET1265 auxiliary elimination theorem",
            "observable_relation": "Z_R=0, J_R=0, B_R=0 on protected R_AB branch",
            "acceptance_gate": "all AP1265 clauses signed and no finite residual rows required",
            "current_status": "BLOCKED_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1265_1_finite_qRhat",
            "required_inputs": "Z_R plus J_R/B_R or direct Q_R source value",
            "observable_relation": "gamma_minus_1_QR=-q_Rhat/2 and abs(q_Rhat)<=4.6e-05 smoke ceiling",
            "acceptance_gate": "source-backed coefficient rows and local arena projection",
            "current_status": "WAITING_FOR_LIVE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1265_2_massive_suppression",
            "required_inputs": "Z_R and M_R^2 with no/source flux conditions",
            "observable_relation": "ell_R=sqrt(Z_R/M_R^2); require range/profile below R10/PPN sensitivity",
            "acceptance_gate": "source-backed mass gap or theorem-zero",
            "current_status": "WAITING_FOR_LIVE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1265_3_boundary_flux",
            "required_inputs": "B_R or Pi_R^n source/boundary theorem",
            "observable_relation": "boundary hair contributes finite exterior q_Rhat or force residual",
            "acceptance_gate": "boundary zero theorem or finite flux bound",
            "current_status": "WAITING_FOR_LIVE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    raw_rows, accepted_rows, docs_rows = live_intake_counts()
    bound_runner_dryrun = [
        {
            "dryrun_id": "DR1265_0_intake_counts",
            "branch": "all finite-ZR branches",
            "status": "NO_LIVE_ROWS",
            "details": f"raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dryrun_id": "DR1265_1_theorem_zero",
            "branch": "theorem-zero",
            "status": "BLOCKED_NOT_PARENT_SIGNED",
            "details": "AP1265 clauses remain unsigned; AET1265 theorem is exact conditional only",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "dryrun_id": "DR1265_2_finite_bound",
            "branch": "finite residual",
            "status": "BLOCKED_NO_SOURCE_BACKED_COEFFICIENTS",
            "details": "Z_R/M_R2/J_R/B_R and tau_R10/tau_PPN/tau_clock/tau_orbital missing",
            "runner_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1265_0_aux_theorem",
            "claim": "protected auxiliary theorem closes `Z_R=0`",
            "status": "BLOCKED",
            "reason": "auxiliary elimination theorem is exact conditional but AP1265 clauses are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1265_1_finite_runner",
            "claim": "finite-ZR bound runner can score",
            "status": "BLOCKED",
            "reason": "raw/accepted live coefficient rows are absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1265_2_no_boundary_hair",
            "claim": "R_AB boundary hair is zero",
            "status": "BLOCKED",
            "reason": "boundary/corner grammar and B_R zero are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1265_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither protected theorem-zero nor finite residual bound is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1265_0_best_result",
            "decision": "auxiliary elimination is the cleanest current route for `R_AB`",
            "because": "it replaces off-shell gauge hand-waving with algebraic elimination: no derivative means no theta/Omega/Pi_R sector after reduction",
            "status": "EXACT_CONDITIONAL_PROGRESS",
            "next_action": "source/sign AP1265 protection clauses from parent primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1265_1_not_claimed",
            "decision": "do not promote `Z_R=0` yet",
            "because": "the auxiliary block and its protection clauses are candidate-written, not parent-derived",
            "status": "BLOCKED_FOR_CLAIM",
            "next_action": "either derive primitive auxiliary grammar or run finite residual intake once source rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1265_2_runner_state",
            "decision": "finite-ZR bound runner schema is ready but not executable",
            "because": "there are no live raw/accepted Z_R coefficient rows",
            "status": "RUNNER_SCHEMA_READY_NO_LIVE_ROWS",
            "next_action": "build a source-hunt/protection checklist for AP1265 before spending time on numeric bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1265_0_1266",
            "target_file": "1266-Y5-R10-RAB-primitive-auxiliary-grammar-source-hunt-or-finite-ZR-intake-review.md",
            "target_script": "scripts/Y5_R10_RAB_primitive_auxiliary_grammar_source_hunt_or_finite_ZR_intake_review.py",
            "task": "hunt the corpus for a primitive motion/time/space source that signs the auxiliary grammar and protection clauses; if absent, review finite-ZR intake readiness without scoring",
            "success_condition": "source-backed AP1265 clause evidence or a clear blocker ledger that routes to finite residual source acquisition",
            "do_not": "do not claim local tests or theorem-zero from the conditional auxiliary theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (AUX_PROTECTION_PATH, aux_protection),
        (ELIMINATION_THEOREM_PATH, elimination_theorem),
        (REGENERATION_RISK_PATH, regeneration_risks),
        (BOUND_RUNNER_SCHEMA_PATH, bound_runner_schema),
        (BOUND_RUNNER_DRYRUN_PATH, bound_runner_dryrun),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    aux_protection_complete = len(aux_protection) == 5
    theorem_conditional = elimination_theorem[0]["proof_status"] == "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"
    dryrun_blocked = all(not bool(row["runner_eligible"]) for row in bound_runner_dryrun)
    no_live_rows = raw_rows == 0 and accepted_rows == 0
    gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_rows_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _path, rows in generated_tables
        for row in rows
    )
    next_is_1266 = next_target[0]["target_file"].startswith("1266-")

    csv_parse_ok = True
    csv_parse_details: list[str] = []
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAILED:{exc}")

    formalization_writes = generated_inside_formalization()

    validation_rows = [
        validation_row("VAL1265_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1265_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1265_2_protection_complete", "auxiliary protection audit covers all required clauses", aux_protection_complete, f"aux_protection_rows={len(aux_protection)}"),
        validation_row("VAL1265_3_theorem_conditional", "auxiliary elimination theorem remains conditional", theorem_conditional, elimination_theorem[0]["proof_status"]),
        validation_row("VAL1265_4_bound_runner_blocked", "finite-ZR bound runner dry-run remains blocked", dryrun_blocked, f"dryrun_rows={len(bound_runner_dryrun)}"),
        validation_row("VAL1265_5_no_live_rows", "no live raw/accepted R_AB coefficient rows exist", no_live_rows, f"raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}"),
        validation_row("VAL1265_6_claim_gates", "all claim gates remain blocked", gates_blocked, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1265_7_nonclaim_policy", "all generated rows remain nonclaim", all_rows_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1265_8_next_target_1266", "next target is primitive auxiliary grammar source hunt", next_is_1266, next_target[0]["target_file"]),
        validation_row("VAL1265_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1265_10_formalization_untouched", "formalization-workbench untouched by generated outputs", not formalization_writes, f"formalization_generated_output_count={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1265_11_overall",
            "overall 1265 validation",
            overall,
            "1265 upgrades the auxiliary route into an exact conditional elimination theorem and builds a nonclaim finite-ZR bound-runner schema, with all claims blocked",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1265 improves the route: the right theorem is algebraic auxiliary elimination, not off-shell gauge magic. If `R_AB,Lambda_R` are parent-signed algebraic auxiliaries and protected against derivative, boundary, matter, and readout regeneration, then `R_AB` disappears from the reduced phase space and `Z_R=0`.

**Main progress:** this is a cleaner local-GR reduction mechanism. It explains why `theta_R`, `Omega_R`, and `Pi_R^n` vanish after reduction, and it gives a finite-`Z_R` bound-runner fallback if protection fails.

**No-claim guard:** the protection clauses are not parent-signed yet, and no live finite coefficient rows exist. No `Z_R=0`, local-GR/Newton, R10, PPN, clock, or orbital claim is made.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Auxiliary Protection Audit
{markdown_table(aux_protection, ["clause_id", "protection_clause", "test", "current_status", "failure_mode", "valid_for_claim", "claim_allowed"])}

## Auxiliary Elimination Theorem
{markdown_table(elimination_theorem, ["theorem_id", "theorem_name", "statement", "proof_sketch", "proof_status", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Regeneration Risk Ledger
{markdown_table(regeneration_risks, ["risk_id", "risk", "needed_block", "status", "finite_fallback", "valid_for_claim", "claim_allowed"])}

## Finite Z_R Bound Runner Schema
{markdown_table(bound_runner_schema, ["branch_id", "required_inputs", "observable_relation", "acceptance_gate", "current_status", "valid_for_claim", "claim_allowed"])}

## Finite Z_R Bound Runner Dryrun
{markdown_table(bound_runner_dryrun, ["dryrun_id", "branch", "status", "details", "runner_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
