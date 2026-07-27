from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1257"
TITLE = "1257-Y5-R10-ZR-lambdaR-selector-from-parent-primitives"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
PRIMITIVE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_PARENT_PRIMITIVE_SELECTOR_AUDIT.csv"
SELECTOR_CLAUSES_PATH = OUT_DIR / f"{PACK_ID}_ZR_LAMBDAR_SELECTOR_CLAUSES.csv"
THEOREM_CANDIDATE_PATH = OUT_DIR / f"{PACK_ID}_SELECTOR_THEOREM_CANDIDATE.csv"
BRANCH_ROUTING_PATH = OUT_DIR / f"{PACK_ID}_BRANCH_ROUTING_LEDGER.csv"
MISSING_PROOF_PATH = OUT_DIR / f"{PACK_ID}_MISSING_PROOF_OBLIGATIONS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1257_VALIDATION.csv"


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
            "source_id": "SRC1257_0_1256_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1256_NEXT_TARGET.csv",
            "needle": "NEXT1256_0_1257",
            "purpose": "handoff to Z_R/lambda_R selector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_1_1256_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
            "needle": "HC1256_0_minimal_density",
            "purpose": "minimal reciprocal H_core variational contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_2_1256_branches",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1256_VARIATIONAL_BRANCH_AUDIT.csv",
            "needle": "BR1256_0_nonprop_constraint",
            "purpose": "zero/finite/suppressed/boundary branch fork from 1256",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_3_1237_primitives",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1237_MTS_PRIMITIVE_DERIVATION_AUDIT.csv",
            "needle": "PRIM1237_1_reciprocity",
            "purpose": "MTS primitive audit for reciprocity and nonpropagating route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_4_1237_gates",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1237_CLAIM_GATES.csv",
            "needle": "GATE1237_3_RAB_zero",
            "purpose": "R_AB zero not parent-derived in primitive grammar audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_5_511_fixed_points",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
            "needle": "FP511_1_double_zero_nonEH_coupling",
            "purpose": "fixed-point/double-zero/mass-gap local silence conditions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_6_511_blocks",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "A511_3_extra_field_silence",
            "purpose": "extra-field local silence action block",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_7_03_origin",
            "local_path": "03-reciprocal-routing-parent-origin.md",
            "needle": "reciprocity itself is not parent-derived",
            "purpose": "original reciprocity parent-origin obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_8_07_nonprop",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open",
            "purpose": "clean nonpropagating route still parent-origin open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1257_9_12_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "gauge_noether_origin_not_derived_closure_only",
            "purpose": "gauge/Noether route does not yet force R_AB=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    primitive_audit = [
        {
            "audit_id": "PA1257_0_motion_load",
            "primitive": "motion-load capacity",
            "selector_pressure": "provides Newtonian/load scaffold and p=1 target",
            "supports_ZR0": "NO_DIRECT_SUPPORT",
            "supports_ZR_positive": "NO_DIRECT_SUPPORT",
            "verdict": "TARGET_ONLY_NOT_SELECTOR",
            "reason": "motion-load asks for p=1 but does not decide whether R_AB is constrained or dynamical",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PA1257_1_reciprocity",
            "primitive": "T^2 S=1 / R_AB=0",
            "selector_pressure": "if parent-derived, it selects the clean local GR lane",
            "supports_ZR0": "CONDITIONAL",
            "supports_ZR_positive": "NO",
            "verdict": "CONDITIONAL_CONSTRAINT_TARGET",
            "reason": "reciprocity is the condition to derive, not yet a parent primitive that selects Z_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PA1257_2_nonpropagating_constraint",
            "primitive": "nonpropagating reciprocal strain",
            "selector_pressure": "forbids exterior reciprocal hair if parent-owned",
            "supports_ZR0": "YES_IF_PARENT_SIGNED",
            "supports_ZR_positive": "NO",
            "verdict": "BEST_ZERO_SELECTOR_UNSIGNED",
            "reason": "07 supplies the clean algebra but not the parent origin",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PA1257_3_observer_map",
            "primitive": "observer coframe/J_q map",
            "selector_pressure": "makes R_AB a readout/compatibility strain rather than obviously independent matter",
            "supports_ZR0": "POSSIBLE_IF_RAB_NOT_INDEPENDENT",
            "supports_ZR_positive": "POSSIBLE_IF_RAB_PROMOTED_TO_FIELD",
            "verdict": "FIELD_STATUS_UNDECIDED",
            "reason": "current corpus does not prove whether R_AB is independent parent DOF or derived compatibility variable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "PA1257_4_extra_field_silence",
            "primitive": "A511_3/FP511 extra-sector fixed point",
            "selector_pressure": "generic extra fields need double-zero and positive mass gap to silence local hair",
            "supports_ZR0": "ONLY_IF_ALGEBRAIC_CONSTRAINT",
            "supports_ZR_positive": "YES_GENERIC_EFT_IF_INDEPENDENT_FIELD",
            "verdict": "DEFAULT_IF_FIELD_INDEPENDENT",
            "reason": "if R_AB is admitted as an independent local field, a kinetic coefficient is allowed unless symmetry/constraint forbids it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    selector_clauses = [
        {
            "clause_id": "SEL1257_0_field_exclusion",
            "selector_statement": "If R_AB is not an independent parent field but only a coframe compatibility constraint, derivative terms D_i R_AB D^i R_AB are forbidden.",
            "implies": "Z_R=0 and R_AB must be enforced by a parent constraint/multiplier or equivalent compatibility equation",
            "current_status": "NOT_PROVED",
            "missing_evidence": "typed parent field list or object-language exclusion showing R_AB cannot be varied independently",
            "route_if_fails": "allow Z_R branch and score/suppress reciprocal hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SEL1257_1_multiplier_origin",
            "selector_statement": "If Z_R=0 is selected, lambda_R must be parent-owned rather than inserted as a local closure multiplier.",
            "implies": "R_AB=0 can become a zero theorem only after Dirac/constraint closure and matter compatibility",
            "current_status": "NOT_PROVED",
            "missing_evidence": "parent primary constraint, secondary chain, bracket closure, and boundary silence",
            "route_if_fails": "Z_R=0 remains closure/ansatz only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SEL1257_2_generic_field_rule",
            "selector_statement": "If R_AB is an independent local scalar/strain field and no gauge/constraint removes it, locality permits a kinetic term.",
            "implies": "Z_R is not theorem-zero; finite or massive/suppressed residual branch must be kept",
            "current_status": "CONDITIONAL_RULE",
            "missing_evidence": "actual parent field-status decision and coefficient source",
            "route_if_fails": "return to field-exclusion/gauge proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "SEL1257_3_mass_gap_silence",
            "selector_statement": "If Z_R>0 but M_R^2>0 and local source flux is absent, reciprocal hair may be exponentially suppressed.",
            "implies": "local PPN can be protected by ell_R=sqrt(Z_R/M_R^2) and no-flux/source conditions, not by exact GR derivation",
            "current_status": "CONCEPTUAL_ONLY",
            "missing_evidence": "Z_R, M_R^2, J_R, B_R and scale separation from parent action",
            "route_if_fails": "finite q_Rhat bound branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_candidate = [
        {
            "candidate_id": "THM1257_0_conditional_ZR_selector",
            "theorem_name": "R_AB field-status selector",
            "candidate_statement": "A parent action may select the clean local-GR route only if R_AB is excluded as an independent propagating field and appears as a first-class/algebraic coframe compatibility constraint; otherwise the reciprocal sector must retain finite/suppressed residual tests.",
            "proof_status": "CONDITIONAL_NOT_DERIVED",
            "proof_gap": "current parent primitives do not provide a signed field list, first-class constraint, or object-language exclusion for R_AB",
            "claim_effect": "no local-GR claim; but next proof target is now narrow",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    branch_routing = [
        {
            "route_id": "ROUTE1257_0_clean_zero",
            "if_selector_finds": "R_AB excluded as independent field and parent lambda_R/constraint exists",
            "then_route": "Z_R=0; R_AB=0; q_Rhat=0 theorem candidate",
            "current_status": "BEST_ROUTE_NOT_SELECTED",
            "required_next_evidence": "independent-field exclusion plus Dirac/matter/boundary proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1257_1_kinetic_bound",
            "if_selector_finds": "R_AB is independent and massless/long-range",
            "then_route": "Z_R>0; finite q_Rhat branch scored against 1255 Cassini ceiling",
            "current_status": "KEPT_OPEN",
            "required_next_evidence": "Z_R and Q_R/J_R boundary-source value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1257_2_massive_suppression",
            "if_selector_finds": "R_AB is independent but has positive local Hessian/mass gap",
            "then_route": "Z_R>0, M_R^2>0; local Yukawa/suppressed residual branch",
            "current_status": "KEPT_OPEN",
            "required_next_evidence": "M_R^2/Z_R and source/no-flux scale separation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1257_3_boundary_nohair",
            "if_selector_finds": "R_AB kinetic exists but boundary/source flux is theorem-zero",
            "then_route": "Q_R=0 boundary no-hair branch without global R_AB=0 insertion",
            "current_status": "KEPT_OPEN",
            "required_next_evidence": "source worldtube boundary class and exact/no-flux theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    missing_proofs = [
        {
            "obligation_id": "OBL1257_0_field_list",
            "needed_proof": "typed parent field list classifies R_AB as derived compatibility variable or independent field",
            "why_it_matters": "decides whether Z_R can exist",
            "current_status": "MISSING",
            "next_test": "search/build R_AB independent-field exclusion certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obligation_id": "OBL1257_1_constraint_algebra",
            "needed_proof": "if R_AB is constrained, lambda_R has parent origin and the constraints close",
            "why_it_matters": "turns closure into derivation",
            "current_status": "MISSING",
            "next_test": "Dirac chain for R_AB/lambda_R with matter and boundary terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obligation_id": "OBL1257_2_coefficient_source",
            "needed_proof": "if R_AB is independent, Z_R and M_R^2 are sourced or bounded",
            "why_it_matters": "enables finite/suppressed branch scoring",
            "current_status": "MISSING",
            "next_test": "derive/read off second variation Hessian around local branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "obligation_id": "OBL1257_3_boundary_class",
            "needed_proof": "physical source/test boundaries are no-flux/exact/neutral or give a finite Q_R",
            "why_it_matters": "prevents hidden q_Rhat hair",
            "current_status": "MISSING",
            "next_test": "boundary worldtube source-class audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1257_0_selector_written",
            "claim": "Z_R/lambda_R selector clauses are explicit",
            "status": "PASS_NONCLAIM",
            "reason": "field-exclusion, multiplier-origin, generic-field, and mass-gap clauses are separated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1257_1_ZR_zero",
            "claim": "Z_R=0 is derived from parent primitives",
            "status": "BLOCKED",
            "reason": "R_AB independent-field exclusion and parent lambda_R origin are not proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1257_2_ZR_positive",
            "claim": "Z_R>0 finite/suppressed branch is derived",
            "status": "BLOCKED",
            "reason": "field status and coefficient source are not proved; branch remains open, not selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1257_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "status": "BLOCKED",
            "reason": "selector narrows the fork but does not close zero, finite, mass-gap, or boundary gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1257_0_selector_result",
            "decision": "do not select Z_R=0 yet",
            "because": "parent primitives support it only if R_AB is non-independent and lambda_R is parent-owned, neither of which is proved",
            "next_action": "prove or reject R_AB independent-field exclusion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1257_1_fork_retained",
            "decision": "retain finite and massive/suppressed branches",
            "because": "if R_AB is an independent local strain field, a kinetic coefficient is not forbidden by current evidence",
            "next_action": "if field exclusion fails, derive/bound Z_R, M_R^2, J_R, and B_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1257_0_1258",
            "target_file": "1258-Y5-R10-RAB-independent-field-exclusion-or-ZR-positive-bound.md",
            "target_script": "scripts/Y5_R10_RAB_independent_field_exclusion_or_ZR_positive_bound.py",
            "task": "try to prove R_AB is a derived coframe compatibility variable rather than an independent propagating parent field; if that fails, route to Z_R-positive coefficient/bound acquisition",
            "success_condition": "either a field-exclusion certificate that supports Z_R=0/lambda_R, or a blocker that moves to Z_R/M_R^2/J_R/B_R finite/suppression sourcing",
            "do_not": "do not choose Z_R=0 from desired GR behavior and do not demote the kinetic branch without a field-status proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (PRIMITIVE_AUDIT_PATH, primitive_audit),
        (SELECTOR_CLAUSES_PATH, selector_clauses),
        (THEOREM_CANDIDATE_PATH, theorem_candidate),
        (BRANCH_ROUTING_PATH, branch_routing),
        (MISSING_PROOF_PATH, missing_proofs),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    selector_complete = {row["clause_id"] for row in selector_clauses} == {
        "SEL1257_0_field_exclusion",
        "SEL1257_1_multiplier_origin",
        "SEL1257_2_generic_field_rule",
        "SEL1257_3_mass_gap_silence",
    }
    theorem_not_derived = theorem_candidate[0]["proof_status"] == "CONDITIONAL_NOT_DERIVED"
    routes_complete = {row["route_id"] for row in branch_routing} == {
        "ROUTE1257_0_clean_zero",
        "ROUTE1257_1_kinetic_bound",
        "ROUTE1257_2_massive_suppression",
        "ROUTE1257_3_boundary_nohair",
    }
    obligations_visible = all(row["current_status"] == "MISSING" for row in missing_proofs)
    claims_ok = all(row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row["claim_allowed"]) for row in claim_gates)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    )
    next_is_1258 = next_target[0]["target_file"].startswith("1258-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1257_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1257_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1257_2_selector_complete", "selector clauses cover field-exclusion/multiplier/generic/mass-gap cases", selector_complete, f"selector_rows={len(selector_clauses)}"),
        validation_row("VAL1257_3_theorem_not_derived", "selector theorem is conditional, not claimed", theorem_not_derived, theorem_candidate[0]["proof_status"]),
        validation_row("VAL1257_4_routes_complete", "zero/finite/massive/boundary routes are retained", routes_complete, f"route_rows={len(branch_routing)}"),
        validation_row("VAL1257_5_obligations_visible", "missing proof obligations are explicit", obligations_visible, f"obligation_rows={len(missing_proofs)}"),
        validation_row("VAL1257_6_claim_gates", "claim gates block Z_R selection and local GR", claims_ok, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1257_7_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1257_8_next_target_1258", "next target tests R_AB independent-field exclusion", next_is_1258, str(next_target[0]["target_file"])),
        validation_row("VAL1257_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1257_10_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1257_11_overall",
            "overall 1257 validation",
            overall,
            "1257 writes the Z_R/lambda_R selector, keeps the theorem conditional, and routes next to R_AB field-status proof",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1257 does not derive `Z_R=0`. It produces a conditional selector: the clean local-GR route works only if `R_AB` is not an independent propagating parent field and `lambda_R` is parent-owned.

**Main progress:** the selector fork is now explicit. If `R_AB` is a coframe-compatibility constraint, pursue `Z_R=0/lambda_R`. If `R_AB` is an independent local strain field, keep `Z_R>0` finite/suppressed residual branches and score them against the 1255 ceiling.

**No-claim guard:** no `Z_R=0` theorem, `Q_R=0` theorem, finite MTS `q_R_hat` prediction, or local-GR/Newton derivation is promoted.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Parent Primitive Selector Audit
{markdown_table(primitive_audit, ["audit_id", "primitive", "selector_pressure", "supports_ZR0", "supports_ZR_positive", "verdict", "reason", "valid_for_claim", "claim_allowed"])}

## Z_R / lambda_R Selector Clauses
{markdown_table(selector_clauses, ["clause_id", "selector_statement", "implies", "current_status", "missing_evidence", "route_if_fails", "valid_for_claim", "claim_allowed"])}

## Selector Theorem Candidate
{markdown_table(theorem_candidate, ["candidate_id", "theorem_name", "candidate_statement", "proof_status", "proof_gap", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Branch Routing Ledger
{markdown_table(branch_routing, ["route_id", "if_selector_finds", "then_route", "current_status", "required_next_evidence", "valid_for_claim", "claim_allowed"])}

## Missing Proof Obligations
{markdown_table(missing_proofs, ["obligation_id", "needed_proof", "why_it_matters", "current_status", "next_test", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
