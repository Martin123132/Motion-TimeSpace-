from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1247"
TITLE = "1247-Y5-R10-parent-lambdaR-constraint-legitimacy-gate"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
LEGITIMACY_TEST_PATH = OUT_DIR / f"{PACK_ID}_LAMBDAR_LEGITIMACY_TEST.csv"
DIRAC_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_DIRAC_PARENT_CONTRACT.csv"
ROUTE_VERDICT_PATH = OUT_DIR / f"{PACK_ID}_ROUTE_VERDICT.csv"
DEMOTION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_CLOSURE_DEMOTION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1247_VALIDATION.csv"


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


def is_false(row: dict[str, object], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"false", "0", "no"}


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1247_0_1246_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1246_NEXT_TARGET.csv",
            "needle": "NEXT1246_0_1247",
            "purpose": "handoff to lambda_R legitimacy gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_1_1246_clauses",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1246_PARENT_QR_ZERO_THEOREM_CLAUSES.csv",
            "needle": "WORKS_ONLY_IF_PARENT_SIGNED",
            "purpose": "lambda_R route is conditional on parent signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_2_motion_load",
            "local_path": "01-motion-load-route-contract.md",
            "needle": "p=1 or gamma=1 is derived from motion-load/routing structure",
            "purpose": "promotion criterion for local GR lane",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_3_phase_volume",
            "local_path": "08-phase-volume-reciprocity-origin.md",
            "needle": "phase_volume_reciprocity_motivated_not_parent_derived",
            "purpose": "radial phase-cell principle motivates but does not derive lambda_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_4_phase_script",
            "local_path": "scripts/phase_volume_reciprocity_origin.py",
            "needle": "lambda_R_parent_origin",
            "purpose": "machine source says lambda_R parent origin gate fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_5_hamiltonian",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "hamiltonian_radial_cell_sharpened_not_parent_derived",
            "purpose": "Hamiltonian route sharpens but does not parent-derive radial cell",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_6_observer_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "a genuine constraint whose multiplier has a parent origin",
            "purpose": "observer-map contract names required lambda origin clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_7_nonprop_script",
            "local_path": "scripts/nonpropagating_reciprocity_constraint.py",
            "needle": "best_clean_route_if_lambda_R_has_parent_origin",
            "purpose": "nonpropagating route is clean only if lambda_R has parent origin",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_8_nonprop_parent_fail",
            "local_path": "scripts/nonpropagating_reciprocity_constraint.py",
            "needle": "constraint_parent_origin",
            "purpose": "machine gate marks parent origin unresolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_9_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "Noether identity derives R_AB=0",
            "purpose": "Noether-only route is rejected in current scaffold",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_10_closure_benchmark",
            "local_path": "13-local-closure-PPN-benchmark.md",
            "needle": "R_AB=0 and Q_R=0 are closure assumptions in this branch",
            "purpose": "closure branch is a control baseline, not parent derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1247_11_1246_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1246_FINITE_QR_SOURCE_HUNT.csv",
            "needle": "FQH1246_2_finite_direct_qRhat",
            "purpose": "fallback finite q_R_hat source hunt if lambda_R fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    legitimacy_test = [
        {
            "test_id": "LRT1247_0_variational_effect",
            "criterion": "delta_lambda_R S = R_AB = 0",
            "current_evidence": "nonpropagating script and 07 show this algebra works",
            "status": "PASS_CONDITIONAL",
            "blocker": "variation result alone does not prove lambda_R belongs in the parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "LRT1247_1_motion_load_origin",
            "criterion": "motion-load/routing principle selects the radial t-r cell constraint rather than an arbitrary volume constraint",
            "current_evidence": "08 says radial phase-cell preservation selects p=1 but remains a candidate principle",
            "status": "MOTIVATES_NOT_DERIVES",
            "blocker": "missing parent variational rule that elevates the radial t-r cell to a constraint equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "LRT1247_2_hamiltonian_origin",
            "criterion": "Hamiltonian/mass-shell structure derives the radial cell constraint",
            "current_evidence": "09 says Hamiltonian route sharpens but is not a parent derivation",
            "status": "FAILS_CURRENT_CORPUS",
            "blocker": "ordinary Hamiltonian/Liouville preservation is too weak",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "LRT1247_3_observer_map_origin",
            "criterion": "observer-map symplectic contract produces multiplier with parent origin",
            "current_evidence": "10 names this as an acceptable route but not as a completed proof",
            "status": "CONTRACT_ONLY",
            "blocker": "contract is a requirement, not a source term or constraint algebra",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "LRT1247_4_noether_origin",
            "criterion": "Noether/gauge identity forces R_AB=0",
            "current_evidence": "12 rejects Noether-only derivation unless the constraint equation is already present",
            "status": "FAILS_CURRENT_CORPUS",
            "blocker": "Noether can protect a constraint, not conjure it without parent variable/signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "LRT1247_5_closure_guard",
            "criterion": "lambda_R insertion is not just R_AB=0 closure renamed",
            "current_evidence": "13 says R_AB=0 and Q_R=0 are closure assumptions in the benchmark branch",
            "status": "BLOCKED",
            "blocker": "without parent-origin proof, lambda_R is closure with formal clothes on",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dirac_contract = [
        {
            "contract_id": "DC1247_0_parent_variable",
            "required_clause": "R_AB=ln(T^2 S) or C_R is a parent variable/constraint functional, not an externally chosen gauge condition",
            "minimum_evidence": "parent field list and action term showing C_R appears before the local-GR closure branch is selected",
            "current_status": "MISSING_PARENT_FIELD_LIST",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "DC1247_1_multiplier_origin",
            "required_clause": "lambda_R enters from the parent variational principle as a multiplier, auxiliary field, or constrained Hamiltonian variable",
            "minimum_evidence": "source equation S_parent contains lambda_R C_R with derivation of why the multiplier is required",
            "current_status": "MISSING_MULTIPLIER_ORIGIN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "DC1247_2_primary_secondary",
            "required_clause": "Dirac chain is explicit: pi_lambda=0, preserving pi_lambda yields C_R=0, and preserving C_R closes or fixes lambda_R consistently",
            "minimum_evidence": "Hamiltonian constraint table with primary/secondary constraints and no hidden Q_R hair mode",
            "current_status": "MISSING_DIRAC_CHAIN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "DC1247_3_constraint_class",
            "required_clause": "constraint class is named and degrees of freedom are counted",
            "minimum_evidence": "Poisson bracket/constraint algebra showing first-class gauge redundancy or second-class selection without inconsistency",
            "current_status": "MISSING_CONSTRAINT_ALGEBRA",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "DC1247_4_matter_compatibility",
            "required_clause": "matter/readout coupling respects C_R=0 without field-rename hiding, shadow metrics, or nonuniversal source labels",
            "minimum_evidence": "matter action descent clause plus PPN/source residual gate",
            "current_status": "MISSING_MATTER_DESCENT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "contract_id": "DC1247_5_boundary_silence",
            "required_clause": "boundary variation does not reintroduce Q_R as an allowed exterior charge",
            "minimum_evidence": "boundary/corner term audit proving no reciprocal hair charge survives",
            "current_status": "MISSING_BOUNDARY_CHARGE_AUDIT",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    route_verdict = [
        {
            "verdict_id": "RV1247_0_lambdaR_legitimacy",
            "route": "lambda_R R_AB constrained parent route",
            "verdict": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "reason": "algebraic variation works, but motion-load, phase-volume, Hamiltonian, observer-map, and Noether sources do not yet supply the multiplier origin/Dirac chain",
            "allowed_use": "explicit closure benchmark or future parent-action ansatz target",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "verdict_id": "RV1247_1_best_next_derivation",
            "route": "minimal constrained parent action ansatz",
            "verdict": "NEXT_BEST_DERIVATION_TARGET",
            "reason": "the missing object is concrete: parent field list, lambda_R origin, Dirac chain, constraint algebra, matter descent, and boundary silence",
            "allowed_use": "attempt a minimal action and try to pass DC1247_0..5",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "verdict_id": "RV1247_2_finite_fallback",
            "route": "finite q_R_hat source acquisition",
            "verdict": "FALLBACK_IF_ANSATZ_FAILS",
            "reason": "1246 source hunt is already ready if no parent-signed zero theorem appears",
            "allowed_use": "nonclaim smoke scoring only after real q_R_hat source/provenance",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    demotion_ledger = [
        {
            "demotion_id": "DEM1247_0_lambdaR_closure_status",
            "branch": "lambda_R hard constraint",
            "demoted_to": "explicit_closure_until_parent_signed",
            "why": "desired local-GR effect is insufficient proof of parent origin",
            "public_language": "may be described as a closure/selection branch, not as derived MTS local GR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "demotion_id": "DEM1247_1_local_GR_status",
            "branch": "local GR/Newton reduction",
            "demoted_to": "open_derivation_target",
            "why": "Q_R zero, beta, conservation, matter coupling, and boundary charges are not all parent-signed",
            "public_language": "local closure reproduces GR control behavior; parent derivation remains in progress",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1247_0_variation",
            "claim": "lambda_R variation enforces R_AB=0",
            "status": "PASS_CONDITIONAL",
            "reason": "algebraic constraint works if lambda_R is allowed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1247_1_parent_origin",
            "claim": "lambda_R has parent origin",
            "status": "BLOCKED",
            "reason": "missing parent field list, multiplier origin, and Dirac chain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1247_2_QR_zero",
            "claim": "parent Q_R=0 theorem exists",
            "status": "BLOCKED",
            "reason": "lambda_R route is not parent-signed and finite q_R_hat is absent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1247_3_local_PPN",
            "claim": "local PPN pass is derived",
            "status": "BLOCKED",
            "reason": "closure benchmark passes only conditionally; finite residual branch still lacks sourced q_R_hat",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1247_4_local_GR",
            "claim": "local GR/Newton limit is derived from MTS",
            "status": "BLOCKED",
            "reason": "constraint origin, beta, conservation, matter descent, and boundary terms remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1247_0_no_derivation_claim",
            "decision": "do not promote lambda_R route as derived",
            "because": "current evidence supports the effect of the constraint, not the parent necessity of the constraint",
            "next_action": "try a minimal constrained parent action ansatz against DC1247_0..5",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1247_1_keep_working_derivation_first",
            "decision": "attempt parent action ansatz before switching fully to finite q_R_hat acquisition",
            "because": "a derived local GR route is strategically more valuable than a bounded residual branch",
            "next_action": "1248 minimal lambda_R parent action ansatz and Dirac check",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1247_2_preserve_finite_fallback",
            "decision": "keep finite q_R_hat fallback alive",
            "because": "if parent signing fails, the theory still needs a testable local residual rather than a handwave",
            "next_action": "reuse FQH1246 finite source-hunt fields after ansatz attempt",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1247_0_1248",
            "target_file": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "target_script": "scripts/Y5_R10_minimal_lambdaR_parent_action_ansatz_and_Dirac_check.py",
            "task": "construct the minimal parent action ansatz that could legitimately contain lambda_R C_R, then run the Dirac/constraint/matter/boundary checks from DC1247_0..5",
            "success_condition": "either the ansatz supplies a parent-signed nonclaim zero-theorem candidate, or it fails with an exact clause telling us whether to demote lambda_R fully and move to finite q_R_hat source acquisition",
            "do_not": "do not call lambda_R derived just because its variation gives R_AB=0; do not hide closure inside notation",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]

    generated_sets = [
        source_register,
        legitimacy_test,
        dirac_contract,
        route_verdict,
        demotion_ledger,
        claim_gates,
        decisions,
        next_target,
    ]
    output_paths = [
        SOURCE_REGISTER_PATH,
        LEGITIMACY_TEST_PATH,
        DIRAC_CONTRACT_PATH,
        ROUTE_VERDICT_PATH,
        DEMOTION_LEDGER_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(LEGITIMACY_TEST_PATH, legitimacy_test)
    write_csv(DIRAC_CONTRACT_PATH, dirac_contract)
    write_csv(ROUTE_VERDICT_PATH, route_verdict)
    write_csv(DEMOTION_LEDGER_PATH, demotion_ledger)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    variation_pass_conditional = any(row["test_id"] == "LRT1247_0_variational_effect" and row["status"] == "PASS_CONDITIONAL" for row in legitimacy_test)
    parent_origin_blocked = any(row["gate_id"] == "GATE1247_1_parent_origin" and row["status"] == "BLOCKED" for row in claim_gates)
    dirac_contract_complete = len(dirac_contract) == 6 and all(str(row["current_status"]).startswith("MISSING") for row in dirac_contract)
    closure_demoted = any(row["demoted_to"] == "explicit_closure_until_parent_signed" for row in demotion_ledger)
    next_is_1248 = next_target[0]["next_id"] == "NEXT1247_0_1248"
    no_claim_pass = all(
        row["status"] in {"PASS_CONDITIONAL", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and (("claim_allowed" not in row) or is_false(row, "claim_allowed"))
        for rows in generated_sets
        for row in rows
        if "valid_for_claim" in row
    )

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in output_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:PARSE_FAIL:{exc}")

    fw_recent = recent_formalization_writes()

    validation = [
        validation_row("VAL1247_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1247_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1247_2_variation_conditional", "lambda_R variation passes only conditionally", variation_pass_conditional, "delta_lambda_R gives R_AB=0 only if lambda_R is legitimate"),
        validation_row("VAL1247_3_parent_origin_blocked", "lambda_R parent origin remains blocked", parent_origin_blocked, "GATE1247_1_parent_origin -> BLOCKED"),
        validation_row("VAL1247_4_dirac_contract", "Dirac parent contract is explicit", dirac_contract_complete, f"dirac_contract_rows={len(dirac_contract)} all missing current evidence"),
        validation_row("VAL1247_5_closure_demotion", "lambda_R route is demoted to closure until parent-signed", closure_demoted, "DEM1247_0_lambdaR_closure_status"),
        validation_row("VAL1247_6_claim_gates", "claim gates remain blocked/nonclaim", no_claim_pass, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1247_7_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1247_8_next_target_1248", "next target is minimal parent-action ansatz", next_is_1248, next_target[0]["target_file"]),
        validation_row("VAL1247_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1247_10_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1247_11_overall",
            "overall 1247 validation",
            all(row["status"] == "PASS" for row in validation),
            "1247 proves lambda_R is algebraically useful but not parent-legitimate in the current corpus; it supplies the exact Dirac contract for the next derivation attempt",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1247 does not parent-sign `lambda_R`. The variation `delta_lambda_R S -> R_AB=0` is clean, but current motion-load, phase-volume, Hamiltonian, observer-map, and Noether sources do not yet prove that `lambda_R` belongs to the parent action.",
        "",
        "**Main progress:** the missing derivation is now exact: parent field list, multiplier origin, Dirac primary/secondary chain, constraint class/degree count, matter descent, and boundary charge silence. That is the next theorem target.",
        "",
        "**No-claim guard:** `lambda_R R_AB` remains an explicit closure/selection branch until parent-signed. No local GR, local PPN, R10/WEP, or source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## LambdaR Legitimacy Test",
        markdown_table(legitimacy_test, list(legitimacy_test[0].keys())),
        "",
        "## Dirac Parent Contract",
        markdown_table(dirac_contract, list(dirac_contract[0].keys())),
        "",
        "## Route Verdict",
        markdown_table(route_verdict, list(route_verdict[0].keys())),
        "",
        "## Closure Demotion Ledger",
        markdown_table(demotion_ledger, list(demotion_ledger[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
