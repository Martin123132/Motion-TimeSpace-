from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1253"
TITLE = "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
HCORE_SOURCE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_RECIPROCAL_HCORE_SOURCE_EQUATION_ATTEMPT.csv"
BOUNDARY_CHARGE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_BOUNDARY_CHARGE_CLASS_ATTEMPT.csv"
NO_CHARGE_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_NO_CHARGE_THEOREM_CANDIDATE.csv"
FINITE_HANDOFF_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QR_HANDOFF_STATUS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1253_VALIDATION.csv"


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
            "source_id": "SRC1253_0_1252_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1252_NEXT_TARGET.csv",
            "needle": "NEXT1252_0_1253",
            "purpose": "handoff to reciprocal H_core/boundary-charge derivation attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_1_1252_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1252_LOCAL_BRANCH_STATUS_LEDGER.csv",
            "needle": "LBS1252_1_finite_Hcore",
            "purpose": "finite H_core q_Rhat coefficient status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_2_1251_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1251_HCORE_TO_QRHAT_MAP_ATTEMPT.csv",
            "needle": "CMAP1251_0_required_chain",
            "purpose": "required chain from H_core to reciprocal source/current",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_3_1251_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1251_BLOCKER_LEDGER.csv",
            "needle": "explicit weak-field H_core missing",
            "purpose": "current H_core and boundary blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_4_1246_zero_clauses",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1246_PARENT_QR_ZERO_THEOREM_CLAUSES.csv",
            "needle": "QZT1246_5_topological",
            "purpose": "prior zero-theorem routes and topological-neutrality blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_5_1248_failures",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_FAILURE_LEDGER.csv",
            "needle": "FAIL1248_3_boundary",
            "purpose": "minimal lambda_R ansatz boundary failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_6_07_constraint",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB",
            "purpose": "algebraic nonpropagating constraint route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_7_10_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "a conserved cell current with a no-charge theorem",
            "purpose": "parent action contract and acceptable route list",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_8_11_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "W partial_r R_AB = Q_R",
            "purpose": "ordinary reciprocal current gives a constant charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_9_582_boundary",
            "local_path": "582-Y5-R10-boundary-charge-and-constraint-algebra-no-pole-audit.md",
            "needle": "K_boundary = 0",
            "purpose": "boundary differentiability and cocycle gate shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_10_1039_boundary",
            "local_path": "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md",
            "needle": "proper compact representative-`X` transformations",
            "purpose": "narrow compact/proper boundary-silence result and source-boundary blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1253_11_1040_BX",
            "local_path": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "needle": "Q_X[epsilon]=int_partialSigma epsilon_nu B_X^nu dS",
            "purpose": "explicit boundary charge formula contract to analogize for reciprocal sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    hcore_source_attempt = [
        {
            "attempt_id": "HCE1253_0_reciprocal_euler_source",
            "target_equation": "E_R := delta H_core/delta R_AB = rho_R or an equivalent canonical source equation",
            "derivation_route": "vary reciprocal sector of parent H_core/L_MTS_core",
            "required_input": "explicit weak-field H_core or L_MTS_core for R_AB/T/S/e_pub/chi_load",
            "current_evidence": "1251 and 1252 both mark H_core missing",
            "result": "SOURCE_EQUATION_NOT_DERIVED",
            "blocker": "MISSING_EXPLICIT_HCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "HCE1253_1_boundary_flux_definition",
            "target_equation": "Q_R = lim_{r->infinity} integral_{S_r} B_R dS, with B_R reducing to W partial_r R_AB in the spherical weak-field limit",
            "derivation_route": "turn the 11-current integration constant into a parent-owned boundary charge",
            "required_input": "boundary density B_R, units, orientation/sign convention, source boundary class, and reference subtraction",
            "current_evidence": "11 gives W partial_r R_AB = Q_R but not a boundary/corner class",
            "result": "FORMAL_SHAPE_ONLY",
            "blocker": "MISSING_BOUNDARY_CHARGE_CLASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "HCE1253_2_nonpropagating_constraint_origin",
            "target_equation": "delta S/delta lambda_R = R_AB = 0 and no kinetic reciprocal charge mode",
            "derivation_route": "promote lambda_R R_AB from clean closure/ansatz into parent-derived primary constraint",
            "required_input": "parent origin of lambda_R, Dirac bracket closure, matter compatibility, and boundary silence",
            "current_evidence": "07 works algebraically; 1248 rejects the ansatz as underived",
            "result": "WORKS_ONLY_IF_PARENT_SIGNED",
            "blocker": "MISSING_MULTIPLIER_ORIGIN_AND_DIRAC_CHAIN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "HCE1253_3_constraint_preservation",
            "target_equation": "{R_AB, H_T} approx 0 should close without creating Q_R hair or a second-class remnant",
            "derivation_route": "Hamiltonian preservation/no-hair route",
            "required_input": "canonical variables, Poisson brackets, H_core, boundary term, and source term",
            "current_evidence": "09 sharpens the contract but says ordinary Hamiltonian/Liouville preservation is too weak",
            "result": "BRACKET_TEST_NOT_COMPUTABLE",
            "blocker": "MISSING_CANONICAL_BRACKETS_AND_HCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    boundary_charge_attempt = [
        {
            "charge_id": "BCA1253_0_QR_current_constant",
            "object": "Q_R",
            "candidate_formula": "W partial_r R_AB = Q_R; for W=r^2, R_AB=R_infinity-Q_R/r",
            "inherited_from": "11-cell-current-origin-attempt.md",
            "required_signature": "source-backed boundary charge with units and allowed boundary class",
            "current_status": "CONSERVATION_CONSTANT_ONLY",
            "obstruction": "constant charge is not automatically zero and not yet normalized to q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "charge_id": "BCA1253_1_BR_boundary_density",
            "object": "B_R",
            "candidate_formula": "B_R analogous to B_X^nu = sigma n_mu P_X^{mu nu}+B_ct^nu+B_ref^nu+B_exact^nu",
            "inherited_from": "1040 boundary charge formula contract",
            "required_signature": "parent reciprocal symplectic potential Theta_R and momentum P_R",
            "current_status": "ANALOGY_ONLY",
            "obstruction": "no parent reciprocal sector owner fixes P_R, counterterms, exact terms, or reference subtraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "charge_id": "BCA1253_2_Kboundary_R",
            "object": "K_boundary_R",
            "candidate_formula": "K_boundary_R[epsilon,eta]=delta_eta Q_R[epsilon]-delta_epsilon Q_R[eta]-Q_R[[epsilon,eta]] plus Omega_boundary terms",
            "inherited_from": "582 and 1040 cocycle contracts",
            "required_signature": "differentiable generator and parent symplectic form",
            "current_status": "UNCOMPUTED",
            "obstruction": "without Omega/H_core the first-class/no-cocycle test cannot be run",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "charge_id": "BCA1253_3_compact_proper_zero",
            "object": "proper compact boundary silence",
            "candidate_formula": "Q_R=K_boundary_R=0 only if the relevant generator and finite jets vanish on a boundary collar",
            "inherited_from": "1039 compact/proper boundary result",
            "required_signature": "proof that physical source/test boundaries are in the compact/proper class",
            "current_status": "TOO_NARROW_FOR_LOCAL_SOURCES",
            "obstruction": "does not cover source worldtubes, large transformations, reference terms, or q_R_hat projection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    no_charge_theorem = [
        {
            "candidate_id": "NCT1253_0_ordinary_conservation",
            "theorem_statement": "partial_r(W partial_r R_AB)=0 implies Q_R=0",
            "evidence": "11 and 1246 show conservation gives Q_R=constant",
            "verdict": "REJECTED",
            "required_for_success": "extra neutrality condition, boundary class, or first-class constraint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "NCT1253_1_asymptotic_reciprocity",
            "theorem_statement": "R_infinity=0 removes all reciprocal hair",
            "evidence": "11 gives R_AB=-Q_R/r after killing the offset",
            "verdict": "REJECTED",
            "required_for_success": "boundary condition on flux/charge, not just field value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "NCT1253_2_topological_neutrality",
            "theorem_statement": "Q_R = integral rho_R = 0 by source representation or topological selection",
            "evidence": "1246 identifies this as possible but missing",
            "verdict": "CONDITIONAL_NOT_DERIVED",
            "required_for_success": "parent source complex, allowed local source class, and neutrality proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "NCT1253_3_first_class_constraint",
            "theorem_statement": "R_AB is eliminated by a parent first-class constraint and therefore carries no Q_R hair",
            "evidence": "07 gives the algebraic result; 1248 says the parent Dirac chain is missing",
            "verdict": "POSSIBLE_NOT_PRESENT",
            "required_for_success": "lambda_R origin, primary/secondary constraints, bracket closure, and matter descent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "NCT1253_4_compact_boundary_silence",
            "theorem_statement": "boundary charge and cocycle vanish for the physical local branch",
            "evidence": "1039 proves only a narrow proper compact sub-branch; 1040 keeps source/large boundaries open",
            "verdict": "NARROW_SUBLEMMA_NOT_FULL_THEOREM",
            "required_for_success": "source/test boundaries must be shown proper-compact or exact/counterterm-silent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_handoff = [
        {
            "handoff_id": "FQH1253_0_zero_path",
            "route": "parent Q_R=0 theorem",
            "current_status": "NOT_DERIVED",
            "score_action": "do not create theorem-zero q_R_hat row",
            "required_inputs": "parent H_core/source equation or first-class no-charge theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "FQH1253_1_finite_path",
            "route": "finite q_R_hat from H_core/boundary charge",
            "current_status": "FORMAL_ONLY_VALUE_MISSING",
            "score_action": "only fill 1250 template if Q_R or q_R_hat is source-backed with units",
            "required_inputs": "B_R/Q_R value, GM convention, uncertainty/sign policy, source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "FQH1253_2_phenomenological_path",
            "route": "phenomenological finite q_R_hat bound",
            "current_status": "BEST_AVAILABLE_FALLBACK_AFTER_1253",
            "score_action": "stage a nonclaim source-backed bound row and route it through 1249 policy",
            "required_inputs": "numeric q_R_hat or upper bound, derivation/status label, local arena source, valid_for_claim=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1253_0_parent_source_equation",
            "claim": "reciprocal source equation is parent-derived",
            "status": "BLOCKED",
            "reason": "delta H_core/delta R_AB or equivalent source equation is not present",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1253_1_boundary_no_charge",
            "claim": "boundary/no-charge theorem proves Q_R=0",
            "status": "BLOCKED",
            "reason": "ordinary conservation and asymptotic field value fail; topological/first-class routes remain conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1253_2_finite_qRhat",
            "claim": "finite q_R_hat value or bound is score-ready",
            "status": "BLOCKED",
            "reason": "Q_R boundary class, units, and source-backed value are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1253_3_closure_separation",
            "claim": "closure zero was not reused as derivation",
            "status": "PASS_NONCLAIM",
            "reason": "lambda_R/R_AB=0 remains labelled algebraic/closure unless parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1253_4_local_GR",
            "claim": "local GR/PPN branch is derived",
            "status": "BLOCKED",
            "reason": "local branch still lacks Q_R zero/value, beta/matter compatibility, and boundary proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1253_0_derivation_attempt",
            "decision": "reciprocal H_core/boundary charge route remains open but unsigned",
            "because": "the exact source equation and boundary charge class can now be named, but neither is supplied by the current corpus",
            "next_action": "do not claim local GR; either source a finite q_Rhat bound or build a stricter boundary-flux/no-hair certificate with real inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1253_1_best_next",
            "decision": "move to a source-backed finite-qRhat handoff unless a new parent H_core equation is supplied",
            "because": "1253 exhausts the current H_core/boundary proof route without producing zero or value evidence",
            "next_action": "1254-Y5-R10-boundary-flux-source-template-or-phenomenological-qRhat-row.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1253_0_1254",
            "target_file": "1254-Y5-R10-boundary-flux-source-template-or-phenomenological-qRhat-row.md",
            "target_script": "scripts/Y5_R10_boundary_flux_source_template_or_phenomenological_qRhat_row.py",
            "task": "build the strict source-backed boundary-flux/q_Rhat intake route now that the current derivation route has no parent-signed H_core source equation",
            "success_condition": "produce a nonclaim finite q_Rhat/bound row template with exact units/provenance requirements, or a blocker ledger if no source-backed row exists",
            "do_not": "do not promote closure zero, compact-proper boundary silence, or unsourced H_core analogies as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (HCORE_SOURCE_ATTEMPT_PATH, hcore_source_attempt),
        (BOUNDARY_CHARGE_ATTEMPT_PATH, boundary_charge_attempt),
        (NO_CHARGE_THEOREM_PATH, no_charge_theorem),
        (FINITE_HANDOFF_PATH, finite_handoff),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decision_ledger),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    )
    source_equation_blocked = all(row["result"] != "DERIVED" for row in hcore_source_attempt)
    no_charge_not_accepted = all(row["verdict"] != "ACCEPTED" for row in no_charge_theorem)
    finite_no_value = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in finite_handoff)
    closure_separated = any(row["gate_id"] == "GATE1253_3_closure_separation" and row["status"] == "PASS_NONCLAIM" for row in claim_gates)
    claims_blocked = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row["claim_allowed"]) for row in claim_gates)
    next_is_1254 = next_target[0]["target_file"].startswith("1254-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover - validation writes failure detail
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1253_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1253_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1253_2_hcore_source_not_claimed", "H_core source equation remains blocked unless explicit source appears", source_equation_blocked, f"attempt_rows={len(hcore_source_attempt)}; derived_rows=0"),
        validation_row("VAL1253_3_boundary_no_charge_not_accepted", "no-charge theorem candidates are not accepted", no_charge_not_accepted, f"candidate_rows={len(no_charge_theorem)}; accepted_rows=0"),
        validation_row("VAL1253_4_finite_handoff_nonclaim", "finite q_Rhat handoff remains nonclaim", finite_no_value, "zero/value/pheno rows are all valid_for_claim=false and claim_allowed=false"),
        validation_row("VAL1253_5_closure_separated", "closure zero is not reused as derivation", closure_separated, "lambda_R/R_AB=0 remains algebraic/closure unless parent-signed"),
        validation_row("VAL1253_6_claim_gates", "claim gates block local GR and finite q_Rhat claims", claims_blocked, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1253_7_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1253_8_next_target_1254", "next target is strict boundary-flux/q_Rhat source handoff", next_is_1254, str(next_target[0]["target_file"])),
        validation_row("VAL1253_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1253_10_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1253_11_overall",
            "overall 1253 validation",
            overall,
            "1253 names the exact reciprocal H_core/boundary charge proof contract, rejects current zero/value promotion, and hands off to nonclaim finite sourcing",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1253 tried the reciprocal `H_core` / boundary-charge derivation route directly. The clean formula-shape is sharper now, but the parent source equation and no-charge theorem are still not derived.

**Main progress:** the missing object is no longer vague. The theory needs either `delta H_core/delta R_AB` as a parent-owned reciprocal source equation, or a boundary flux theorem that turns `Q_R` into zero or a source-backed finite coefficient.

**No-claim guard:** no local GR, local PPN, finite `q_R_hat`, R10/WEP, or source-coupling claim is promoted. Closure zero, compact-proper boundary silence, and unsourced H_core analogies remain nonclaim only.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Reciprocal H_core Source Equation Attempt
{markdown_table(hcore_source_attempt, ["attempt_id", "target_equation", "derivation_route", "required_input", "current_evidence", "result", "blocker", "valid_for_claim", "claim_allowed"])}

## Boundary Charge Class Attempt
{markdown_table(boundary_charge_attempt, ["charge_id", "object", "candidate_formula", "inherited_from", "required_signature", "current_status", "obstruction", "valid_for_claim", "claim_allowed"])}

## No-Charge Theorem Candidate
{markdown_table(no_charge_theorem, ["candidate_id", "theorem_statement", "evidence", "verdict", "required_for_success", "valid_for_claim", "claim_allowed"])}

## Finite q_R Handoff Status
{markdown_table(finite_handoff, ["handoff_id", "route", "current_status", "score_action", "required_inputs", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision_ledger, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
