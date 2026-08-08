from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1248"
TITLE = "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
MINIMAL_ANSATZ_PATH = OUT_DIR / f"{PACK_ID}_MINIMAL_PARENT_ACTION_ANSATZ.csv"
DIRAC_CHECK_PATH = OUT_DIR / f"{PACK_ID}_DIRAC_CHECK.csv"
FAILURE_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_FAILURE_LEDGER.csv"
ZERO_THEOREM_CANDIDATE_PATH = OUT_DIR / f"{PACK_ID}_ZERO_THEOREM_CANDIDATE_STATUS.csv"
FINITE_HANDOFF_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QR_HANDOFF.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1248_VALIDATION.csv"


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
            "source_id": "SRC1248_0_1247_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1247_NEXT_TARGET.csv",
            "needle": "NEXT1247_0_1248",
            "purpose": "handoff to minimal parent-action ansatz",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_1_1247_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1247_DIRAC_PARENT_CONTRACT.csv",
            "needle": "DC1247_2_primary_secondary",
            "purpose": "Dirac contract rows to be tested",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_2_1247_verdict",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1247_ROUTE_VERDICT.csv",
            "needle": "NEXT_BEST_DERIVATION_TARGET",
            "purpose": "minimal constrained action ansatz selected as next derivation target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_3_07_constraint",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB",
            "purpose": "algebraic hard-constraint action form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_4_08_phase",
            "local_path": "08-phase-volume-reciprocity-origin.md",
            "needle": "candidate principle, not a parent theorem",
            "purpose": "phase-cell motivation is not a parent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_5_09_hamiltonian",
            "local_path": "09-hamiltonian-radial-cell-derivation.md",
            "needle": "not yet a parent derivation",
            "purpose": "Hamiltonian route currently lacks parent derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_6_10_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "derive lambda_R or R_AB=0",
            "purpose": "observer-map contract asks for lambda_R derivation or demotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_7_12_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "Noether structure can explain a constraint only after the parent action has",
            "purpose": "Noether protection cannot replace parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1248_8_1246_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1246_FINITE_QR_SOURCE_HUNT.csv",
            "needle": "MISSING_NUMERIC_QR_HAT",
            "purpose": "finite q_R fallback remains staged",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    minimal_ansatz = [
        {
            "ansatz_id": "ANS1248_0_fields",
            "object": "parent field list",
            "candidate_form": "Phi_parent={T,S,e_pub,theta,chi_load,lambda_R,Psi_matter}; C_R=ln(T^2 S)",
            "what_it_buys": "makes the reciprocal constraint explicit enough to vary",
            "defect": "field list is proposed here, not derived from older parent action",
            "status": "ANSATZ_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ansatz_id": "ANS1248_1_action",
            "object": "minimal constrained action",
            "candidate_form": "S_min=integral sqrt(-g)[L_MTS_core(T,S,e_pub,theta,chi_load)+lambda_R ln(T^2 S)+L_matter(Psi,e_pub,theta)]",
            "what_it_buys": "delta_lambda_R gives C_R=0 and removes the Q_R hair channel if the action is legitimate",
            "defect": "L_MTS_core is still schematic and does not derive why lambda_R must be present",
            "status": "SCHEMATIC_ACTION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ansatz_id": "ANS1248_2_no_kinetic_RAB",
            "object": "nonpropagating reciprocity",
            "candidate_form": "omit kinetic term W(partial R_AB)^2; use lambda_R C_R only",
            "what_it_buys": "prevents conserved exterior Q_R hair in the hard-constraint branch",
            "defect": "omission is a design choice unless parent structure forbids the kinetic channel",
            "status": "DESIGN_CHOICE_NOT_THEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ansatz_id": "ANS1248_3_matter",
            "object": "matter/readout coupling",
            "candidate_form": "L_matter depends on the same public coframe e_pub and not on a hidden reciprocal frame",
            "what_it_buys": "prevents immediate shadow-frame/source-label leakage",
            "defect": "matter descent is asserted in ansatz form; not derived from quotient/naturality proof here",
            "status": "MATTER_DESCENT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dirac_check = [
        {
            "check_id": "DIR1248_0_primary",
            "contract_ref": "DC1247_2_primary_secondary",
            "calculation": "lambda_R has no time derivative in S_min, so pi_lambda approx 0",
            "result": "FORMAL_PASS_WITHIN_ANSATZ",
            "defect": "primary constraint exists only after ansatz inserts lambda_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1248_1_secondary",
            "contract_ref": "DC1247_2_primary_secondary",
            "calculation": "dot(pi_lambda)=-delta H/delta lambda_R=-C_R approx 0, so C_R=ln(T^2 S)=0",
            "result": "FORMAL_PASS_WITHIN_ANSATZ",
            "defect": "secondary constraint is the desired closure unless the action origin is independently derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1248_2_preservation",
            "contract_ref": "DC1247_2_primary_secondary",
            "calculation": "dot(C_R)={C_R,H_core}+lambda-sector terms must vanish or determine lambda_R",
            "result": "BLOCKED",
            "defect": "H_core and canonical brackets for T,S are not supplied, so closure of the constraint chain cannot be checked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1248_3_constraint_class",
            "contract_ref": "DC1247_3_constraint_class",
            "calculation": "classify {pi_lambda,C_R} and the brackets of C_R with the Hamiltonian/momentum constraints",
            "result": "BLOCKED",
            "defect": "no Poisson algebra or DOF count exists for the ansatz",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "DIR1248_4_boundary",
            "contract_ref": "DC1247_5_boundary_silence",
            "calculation": "verify no boundary term permits a reciprocal Q_R charge after C_R=0",
            "result": "BLOCKED",
            "defect": "boundary/corner variational class is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    failure_ledger = [
        {
            "failure_id": "FAIL1248_0_origin",
            "failed_clause": "DC1247_1_multiplier_origin",
            "failure": "lambda_R is introduced in the minimal ansatz but not derived from motion-load/observer-map first principles",
            "consequence": "cannot promote Q_R=0 theorem",
            "repair_path": "derive why the radial t-r cell is a parent constraint, not a selected closure branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1248_1_core",
            "failed_clause": "DC1247_2_primary_secondary",
            "failure": "constraint preservation cannot be checked because H_core and canonical brackets are unspecified",
            "consequence": "Dirac chain is formal only through the secondary constraint",
            "repair_path": "write L_MTS_core or H_core for T,S/e_pub/chi_load and compute bracket closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1248_2_matter",
            "failed_clause": "DC1247_4_matter_compatibility",
            "failure": "matter descent to one public coframe is asserted but not derived",
            "consequence": "source-coupling/local-GR branch still vulnerable to hidden-frame leakage",
            "repair_path": "supply matter action descent theorem or keep source-coupling residuals explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FAIL1248_3_boundary",
            "failed_clause": "DC1247_5_boundary_silence",
            "failure": "no boundary/corner audit proves reciprocal charge cannot reappear",
            "consequence": "Q_R=0 is not safe as a global/local exterior theorem",
            "repair_path": "derive boundary terms or build finite q_R_hat bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_theorem_candidate = [
        {
            "candidate_id": "ZTC1248_0_minimal_ansatz",
            "route_type": "parent_zero_theorem_candidate",
            "q_R_hat": "0",
            "q_R_hat_units": "dimensionless",
            "source_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "derivation_status": "ansatz_zero_not_parent_signed",
            "zero_theorem_statement": "Within S_min, delta_lambda_R gives C_R=ln(T^2S)=0, which would remove Q_R hair if the parent action origin and Dirac chain were signed.",
            "closure_used": True,
            "acceptance_status": "REJECT_ZERO_THEOREM_UNDERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    finite_handoff = [
        {
            "handoff_id": "FH1248_0_finite_qR_next",
            "fallback": "finite q_R_hat source acquisition",
            "why": "minimal lambda_R ansatz does not parent-sign zero theorem",
            "required_fields": "numeric q_R_hat; dimensionless units; GM convention; source path; N_sigma=1; sigma_gamma=2.3e-5; closure_used=false",
            "guardrail": "abs(q_R_hat)<=4.6e-05 for strict nonclaim smoke pass",
            "status": "READY_AS_NEXT_FALLBACK",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1248_0_ansatz_written",
            "claim": "minimal lambda_R parent-action ansatz exists",
            "status": "PASS_NONCLAIM",
            "reason": "S_min and C_R are explicitly staged",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1248_1_parent_signed",
            "claim": "minimal ansatz is parent-signed",
            "status": "BLOCKED",
            "reason": "lambda_R origin and H_core are schematic",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1248_2_dirac_chain",
            "claim": "full Dirac chain closes",
            "status": "BLOCKED",
            "reason": "primary/secondary steps are formal, but preservation/algebra/DOF count are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1248_3_QR_zero",
            "claim": "Q_R=0 theorem accepted as runner input",
            "status": "BLOCKED",
            "reason": "zero candidate is rejected as ansatz/closure, not parent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1248_4_local_GR",
            "claim": "derived local GR/Newton limit",
            "status": "BLOCKED",
            "reason": "lambda_R not parent-signed; beta, matter, conservation, and boundary gates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1248_0_ansatz_not_enough",
            "decision": "do not accept minimal lambda_R ansatz as theorem",
            "because": "the ansatz reproduces the desired constraint but does not derive its parent necessity",
            "next_action": "either construct H_core/bracket closure or switch to finite q_R_hat acquisition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1248_1_finite_fallback_primary",
            "decision": "make finite q_R_hat acquisition the next default branch",
            "because": "derivation-first attempt has now hit explicit missing H_core/matter/boundary clauses",
            "next_action": "build 1249 finite q_R_hat intake/scoring row with no placeholders accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1248_2_keep_parent_repair_path",
            "decision": "preserve a parent-action repair path",
            "because": "a derived local-GR theorem remains the high-value target, but it needs actual H_core and constraint algebra",
            "next_action": "if returning to derivation, fill L_MTS_core/H_core first rather than adding more closure language",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1248_0_1249",
            "target_file": "1249-Y5-R10-finite-qRhat-source-acquisition-and-policy-runner.md",
            "target_script": "scripts/Y5_R10_finite_qRhat_source_acquisition_and_policy_runner.py",
            "task": "because the minimal lambda_R ansatz is not parent-signed, switch to the finite q_R_hat fallback: scan/source candidate rows, reject placeholders, and feed any valid nonclaim row through the 1244/1245 policy runner",
            "success_condition": "no placeholder q_R_hat is accepted; any finite candidate must satisfy source, units, GM convention, no-closure, N_sigma/sigma_gamma, and guardrail fields",
            "do_not": "do not treat the ansatz zero or closure zero as a valid finite q_R_hat source",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        minimal_ansatz,
        dirac_check,
        failure_ledger,
        zero_theorem_candidate,
        finite_handoff,
        claim_gates,
        decisions,
        next_target,
    ]
    output_paths = [
        SOURCE_REGISTER_PATH,
        MINIMAL_ANSATZ_PATH,
        DIRAC_CHECK_PATH,
        FAILURE_LEDGER_PATH,
        ZERO_THEOREM_CANDIDATE_PATH,
        FINITE_HANDOFF_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(MINIMAL_ANSATZ_PATH, minimal_ansatz)
    write_csv(DIRAC_CHECK_PATH, dirac_check)
    write_csv(FAILURE_LEDGER_PATH, failure_ledger)
    write_csv(ZERO_THEOREM_CANDIDATE_PATH, zero_theorem_candidate)
    write_csv(FINITE_HANDOFF_PATH, finite_handoff)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    ansatz_written = len(minimal_ansatz) == 4 and any(row["ansatz_id"] == "ANS1248_1_action" for row in minimal_ansatz)
    formal_primary_secondary = all(
        any(row["check_id"] == check_id and row["result"] == "FORMAL_PASS_WITHIN_ANSATZ" for row in dirac_check)
        for check_id in ["DIR1248_0_primary", "DIR1248_1_secondary"]
    )
    dirac_blocks_present = all(
        any(row["check_id"] == check_id and row["result"] == "BLOCKED" for row in dirac_check)
        for check_id in ["DIR1248_2_preservation", "DIR1248_3_constraint_class", "DIR1248_4_boundary"]
    )
    zero_candidate_rejected = zero_theorem_candidate[0]["acceptance_status"] == "REJECT_ZERO_THEOREM_UNDERIVED"
    finite_handoff_ready = finite_handoff[0]["status"] == "READY_AS_NEXT_FALLBACK"
    parent_claim_blocked = any(row["gate_id"] == "GATE1248_1_parent_signed" and row["status"] == "BLOCKED" for row in claim_gates)
    next_is_1249 = next_target[0]["next_id"] == "NEXT1248_0_1249"
    no_claim_pass = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
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
        validation_row("VAL1248_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1248_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1248_2_ansatz_written", "minimal parent-action ansatz is written", ansatz_written, "S_min and C_R rows generated"),
        validation_row("VAL1248_3_primary_secondary", "formal primary/secondary checks are present", formal_primary_secondary, "pi_lambda=0 and C_R=0 within ansatz"),
        validation_row("VAL1248_4_dirac_blocks", "Dirac preservation/class/boundary blockers are explicit", dirac_blocks_present, "preservation, constraint class, and boundary checks BLOCKED"),
        validation_row("VAL1248_5_zero_candidate_rejected", "ansatz zero theorem candidate is rejected", zero_candidate_rejected, zero_theorem_candidate[0]["acceptance_status"]),
        validation_row("VAL1248_6_finite_handoff", "finite q_R_hat fallback is ready", finite_handoff_ready, "FH1248_0_finite_qR_next"),
        validation_row("VAL1248_7_parent_claim_blocked", "parent-signed ansatz claim remains blocked", parent_claim_blocked, "GATE1248_1_parent_signed -> BLOCKED"),
        validation_row("VAL1248_8_claim_gates", "claim gates remain nonclaim/blocked", no_claim_pass, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1248_9_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1248_10_next_target_1249", "next target is finite q_Rhat source acquisition", next_is_1249, next_target[0]["target_file"]),
        validation_row("VAL1248_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1248_12_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1248_13_overall",
            "overall 1248 validation",
            all(row["status"] == "PASS" for row in validation),
            "1248 constructs the minimal lambda_R ansatz, verifies only formal primary/secondary steps, rejects it as parent theorem, and hands off to finite q_Rhat acquisition",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1248 builds the minimal `lambda_R C_R` parent-action ansatz, but it still does not parent-sign the zero theorem. The primary/secondary Dirac steps work inside the ansatz; preservation, constraint class, matter descent, and boundary silence remain missing.",
        "",
        "**Main progress:** this is the clean derivation failure we needed. We now know exactly why the hard constraint is not yet a theorem: the missing object is `L_MTS_core/H_core` plus bracket closure and matter/boundary compatibility, not another repetition of `delta lambda_R`.",
        "",
        "**No-claim guard:** the ansatz zero is rejected as `REJECT_ZERO_THEOREM_UNDERIVED`; no local GR, local PPN, R10/WEP, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Minimal Parent Action Ansatz",
        markdown_table(minimal_ansatz, list(minimal_ansatz[0].keys())),
        "",
        "## Dirac Check",
        markdown_table(dirac_check, list(dirac_check[0].keys())),
        "",
        "## Failure Ledger",
        markdown_table(failure_ledger, list(failure_ledger[0].keys())),
        "",
        "## Zero Theorem Candidate Status",
        markdown_table(zero_theorem_candidate, list(zero_theorem_candidate[0].keys())),
        "",
        "## Finite QR Handoff",
        markdown_table(finite_handoff, list(finite_handoff[0].keys())),
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
